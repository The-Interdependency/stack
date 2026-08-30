"""PostgreSQL-backed durable job ledger for stack-level orchestration.

Production usage:
    ledger = JobLedger(os.environ["STACK_DATABASE_URL"])
    ledger.migrate()
    job = ledger.enqueue(
        kind="msdmd.refresh",
        target="ucns",
        source_sha="<40-hex>",
        generator_identity="<sha256>",
        executor="local",
        payload={"root": "/srv/stack-repos/ucns", "out": "...", "generator_root": "..."},
    )

`JobLedger` is intentionally PostgreSQL-only. The retired SQLite prototype is
not a production fallback: one durable VM service should own orchestration
state, leases, attempts, receipts, dependencies, and visible hmmm.
"""
from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_durable_job_ledger
#   module_name: durable_job_ledger
#   module_kind: engine
#   summary: persists idempotent stack orchestration jobs, leases, attempts, receipts, dependencies, and hmmm in PostgreSQL
#   owner: stack
#   public_surface: Job, JobLedger
#   internal_surface: PostgreSQL migration, transactional state transitions, SKIP LOCKED claims
#   auth_boundary: write
#   storage_boundary: migration
#   network_boundary: internal
#   user_data_boundary: none
#   admin_only: true
#   tests: backend.tests.test_orchestrator
#   rollout: PostgreSQL on the stack VM; frontend.cli.stackctl is the operator surface
#   rollback: stop worker; PostgreSQL records remain inspectable
# === END MODULE_BUILD ===

# === BOUNDARIES ===
# id: stack_durable_job_ledger_storage
#   summary: PostgreSQL owns orchestration state only; repositories retain artifact and canon authority
#   auth_boundary: write
#   storage_boundary: write
#   network_boundary: internal
#   user_data_boundary: none
#   admin_only: true
#   side_effects: job, database
#   owner: stack
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: stack_job_enqueue_idempotent
#   given: the same kind, target, source identity, generator identity, executor, and payload are enqueued repeatedly
#   then: the ledger returns one stable job instead of creating duplicate work
#   class: idempotency
#
# id: stack_job_transition_fail_closed
#   given: a caller requests a state transition that is not allowed from the current job state
#   then: the ledger raises ValueError and leaves persisted state unchanged
#   class: correctness
#
# id: stack_job_claim_skip_locked
#   given: multiple VM workers claim queued jobs concurrently
#   then: PostgreSQL row locking permits only one worker to own each claimed attempt
#   class: concurrency
#
# id: stack_job_stale_lease_visible
#   given: a VM worker dies before recording a terminal result
#   then: the expired attempt is recorded as hmmm and the job is requeued
#   class: resilience
# === END CONTRACTS ===

from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
from pathlib import Path
import uuid
from typing import Any

JOB_STATES = ("queued", "running", "succeeded", "failed", "hmmm", "cancelled")
_ALLOWED_TRANSITIONS = {
    "queued": {"running", "cancelled"},
    "running": {"succeeded", "failed", "hmmm"},
    "succeeded": set(),
    "failed": {"queued", "cancelled"},
    "hmmm": {"queued", "cancelled"},
    "cancelled": {"queued"},
}

def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))

def _iso(value: Any) -> str:
    return value.isoformat() if isinstance(value, datetime) else str(value)

@dataclass(frozen=True)
class Job:
    id: str
    dedupe_key: str
    kind: str
    target: str
    source_sha: str
    generator_identity: str
    executor: str
    state: str
    attempts: int
    payload: dict[str, Any]
    created_at: str
    updated_at: str
    artifact_path: str | None
    artifact_sha256: str | None
    error: str | None
    hmmm: str | None

class JobLedger:
    """PostgreSQL orchestration ledger with explicit migration and leases."""

    def __init__(self, database_url: str, *, receipt_dir: str | Path | None = None):
        if not database_url.startswith(("postgresql://", "postgres://")):
            raise ValueError("JobLedger requires a PostgreSQL database URL")
        self.database_url = database_url
        self.receipt_dir = Path(receipt_dir or ".stack/state/receipts").resolve()

    @staticmethod
    def _psycopg():
        try:
            import psycopg
            from psycopg.rows import dict_row
        except ImportError as exc:
            raise RuntimeError("psycopg is required; install backend/requirements.txt") from exc
        return psycopg, dict_row

    def _connect(self):
        psycopg, dict_row = self._psycopg()
        return psycopg.connect(self.database_url, row_factory=dict_row)

    def migrate(self) -> None:
        sql = (Path(__file__).resolve().parent / "sql" / "001_postgres.sql").read_text(encoding="utf-8")
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()

    @staticmethod
    def _dedupe_key(*, kind: str, target: str, source_sha: str,
                    generator_identity: str, executor: str,
                    payload: dict[str, Any]) -> str:
        material = {
            "kind": kind,
            "target": target,
            "source_sha": source_sha,
            "generator_identity": generator_identity,
            "executor": executor,
            "payload": payload,
        }
        return hashlib.sha256(_canonical_json(material).encode("utf-8")).hexdigest()

    @staticmethod
    def _row_to_job(row: dict[str, Any]) -> Job:
        payload = row["payload_json"]
        if isinstance(payload, str):
            payload = json.loads(payload)
        return Job(
            id=row["id"], dedupe_key=row["dedupe_key"], kind=row["kind"],
            target=row["target"], source_sha=row["source_sha"],
            generator_identity=row["generator_identity"], executor=row["executor"],
            state=row["state"], attempts=int(row["attempts"]), payload=dict(payload),
            created_at=_iso(row["created_at"]), updated_at=_iso(row["updated_at"]),
            artifact_path=row["artifact_path"], artifact_sha256=row["artifact_sha256"],
            error=row["error"], hmmm=row["hmmm"],
        )

    def enqueue(self, *, kind: str, target: str, source_sha: str,
                generator_identity: str, executor: str, payload: dict[str, Any],
                hmmm: str | None = None) -> Job:
        dedupe_key = self._dedupe_key(
            kind=kind, target=target, source_sha=source_sha,
            generator_identity=generator_identity, executor=executor, payload=payload,
        )
        job_id = f"job_{dedupe_key[:24]}"
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO jobs (
                        id, dedupe_key, kind, target, source_sha, generator_identity,
                        executor, state, attempts, payload_json, hmmm
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, 'queued', 0, %s::jsonb, %s)
                    ON CONFLICT (dedupe_key) DO NOTHING
                    """,
                    (job_id, dedupe_key, kind, target, source_sha, generator_identity,
                     executor, _canonical_json(payload), hmmm),
                )
                cur.execute("SELECT * FROM jobs WHERE dedupe_key = %s", (dedupe_key,))
                row = cur.fetchone()
            conn.commit()
        assert row is not None
        return self._row_to_job(row)

    def get(self, job_id: str) -> Job:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
                row = cur.fetchone()
        if row is None:
            raise KeyError(job_id)
        return self._row_to_job(row)

    def list(self, *, limit: int = 100) -> list[Job]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM jobs ORDER BY created_at DESC LIMIT %s", (limit,))
                rows = cur.fetchall()
        return [self._row_to_job(row) for row in rows]

    @staticmethod
    def _close_attempt(cur, job_id: str, state: str, *, error: str | None = None) -> None:
        cur.execute(
            """
            UPDATE attempts
            SET state = %s, finished_at = CURRENT_TIMESTAMP, error = %s
            WHERE job_id = %s AND state = 'running'
            """,
            (state, error, job_id),
        )

    def _transition(self, job_id: str, to_state: str, *,
                    artifact_path: str | None = None,
                    artifact_sha256: str | None = None,
                    error: str | None = None, hmmm: str | None = None) -> Job:
        if to_state not in JOB_STATES:
            raise ValueError(f"unknown job state: {to_state}")
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM jobs WHERE id = %s FOR UPDATE", (job_id,))
                row = cur.fetchone()
                if row is None:
                    raise KeyError(job_id)
                current = str(row["state"])
                if to_state not in _ALLOWED_TRANSITIONS[current]:
                    raise ValueError(f"invalid job transition: {current} -> {to_state}")
                cur.execute(
                    """
                    UPDATE jobs
                    SET state = %s,
                        updated_at = CURRENT_TIMESTAMP,
                        artifact_path = COALESCE(%s, artifact_path),
                        artifact_sha256 = COALESCE(%s, artifact_sha256),
                        error = %s,
                        hmmm = %s,
                        lease_owner = CASE WHEN %s IN ('running') THEN lease_owner ELSE NULL END,
                        lease_until = CASE WHEN %s IN ('running') THEN lease_until ELSE NULL END
                    WHERE id = %s
                    """,
                    (to_state, artifact_path, artifact_sha256, error, hmmm,
                     to_state, to_state, job_id),
                )
                if to_state in {"succeeded", "failed", "hmmm", "cancelled"}:
                    self._close_attempt(cur, job_id, to_state, error=error or hmmm)
                if to_state == "hmmm" and hmmm:
                    cur.execute(
                        "INSERT INTO hmmm (id, job_id, constraint) VALUES (%s, %s, %s)",
                        (f"hmmm_{uuid.uuid4().hex}", job_id, hmmm),
                    )
                if to_state == "succeeded":
                    cur.execute(
                        """
                        UPDATE hmmm SET resolved_at = CURRENT_TIMESTAMP,
                            resolution = 'job later succeeded'
                        WHERE job_id = %s AND resolved_at IS NULL
                        """,
                        (job_id,),
                    )
                cur.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
                updated = cur.fetchone()
            conn.commit()
        assert updated is not None
        return self._row_to_job(updated)

    def start(self, job_id: str, *, worker_id: str = "operator") -> Job:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM jobs WHERE id = %s FOR UPDATE", (job_id,))
                row = cur.fetchone()
                if row is None:
                    raise KeyError(job_id)
                if row["state"] != "queued":
                    raise ValueError(f"invalid job transition: {row['state']} -> running")
                cur.execute(
                    """
                    UPDATE jobs SET state = 'running', attempts = attempts + 1,
                        updated_at = CURRENT_TIMESTAMP WHERE id = %s
                    """,
                    (job_id,),
                )
                cur.execute(
                    "INSERT INTO attempts (id, job_id, executor, worker_id, state) VALUES (%s, %s, %s, %s, 'running')",
                    (f"attempt_{uuid.uuid4().hex}", job_id, row["executor"], worker_id),
                )
                cur.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
                updated = cur.fetchone()
            conn.commit()
        assert updated is not None
        return self._row_to_job(updated)

    def claim_next(self, *, executor: str, worker_id: str,
                   lease_seconds: int) -> Job | None:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT j.* FROM jobs AS j
                    WHERE j.state = 'queued' AND j.executor = %s
                      AND NOT EXISTS (
                          SELECT 1 FROM job_dependencies AS d
                          JOIN jobs AS upstream ON upstream.id = d.depends_on_job_id
                          WHERE d.job_id = j.id AND upstream.state <> d.required_state
                      )
                    ORDER BY j.created_at, j.id
                    FOR UPDATE SKIP LOCKED
                    LIMIT 1
                    """,
                    (executor,),
                )
                row = cur.fetchone()
                if row is None:
                    conn.commit()
                    return None
                cur.execute(
                    """
                    UPDATE jobs SET state = 'running', attempts = attempts + 1,
                        lease_owner = %s,
                        lease_until = CURRENT_TIMESTAMP + (%s * INTERVAL '1 second'),
                        updated_at = CURRENT_TIMESTAMP WHERE id = %s
                    """,
                    (worker_id, lease_seconds, row["id"]),
                )
                cur.execute(
                    "INSERT INTO attempts (id, job_id, executor, worker_id, state) VALUES (%s, %s, %s, %s, 'running')",
                    (f"attempt_{uuid.uuid4().hex}", row["id"], row["executor"], worker_id),
                )
                cur.execute("SELECT * FROM jobs WHERE id = %s", (row["id"],))
                updated = cur.fetchone()
            conn.commit()
        assert updated is not None
        return self._row_to_job(updated)

    def requeue_stale(self) -> int:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id FROM jobs
                    WHERE state = 'running' AND lease_until IS NOT NULL
                      AND lease_until < CURRENT_TIMESTAMP
                    FOR UPDATE
                    """
                )
                stale_ids = [row["id"] for row in cur.fetchall()]
                for job_id in stale_ids:
                    constraint = "worker lease expired before a terminal receipt was recorded"
                    self._close_attempt(cur, job_id, "hmmm", error=constraint)
                    cur.execute(
                        "INSERT INTO hmmm (id, job_id, constraint) VALUES (%s, %s, %s)",
                        (f"hmmm_{uuid.uuid4().hex}", job_id, constraint),
                    )
                    cur.execute(
                        """
                        UPDATE jobs SET state = 'queued', lease_owner = NULL,
                            lease_until = NULL, error = NULL, hmmm = %s,
                            updated_at = CURRENT_TIMESTAMP WHERE id = %s
                        """,
                        (constraint, job_id),
                    )
            conn.commit()
        return len(stale_ids)

    def succeed(self, job_id: str, *, artifact_path: str,
                artifact_sha256: str) -> Job:
        """Atomically close a running job and persist its SQL receipt."""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM jobs WHERE id = %s FOR UPDATE", (job_id,))
                row = cur.fetchone()
                if row is None:
                    raise KeyError(job_id)
                current = str(row["state"])
                if "succeeded" not in _ALLOWED_TRANSITIONS[current]:
                    raise ValueError(f"invalid job transition: {current} -> succeeded")
                cur.execute(
                    """
                    UPDATE jobs SET state = 'succeeded', updated_at = CURRENT_TIMESTAMP,
                        artifact_path = %s, artifact_sha256 = %s, error = NULL,
                        hmmm = NULL, lease_owner = NULL, lease_until = NULL
                    WHERE id = %s
                    """,
                    (artifact_path, artifact_sha256, job_id),
                )
                self._close_attempt(cur, job_id, "succeeded")
                cur.execute(
                    """
                    INSERT INTO receipts (
                        job_id, source_sha, generator_identity,
                        artifact_path, artifact_sha256, verified_at
                    ) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    ON CONFLICT (job_id) DO UPDATE
                    SET source_sha = EXCLUDED.source_sha,
                        generator_identity = EXCLUDED.generator_identity,
                        artifact_path = EXCLUDED.artifact_path,
                        artifact_sha256 = EXCLUDED.artifact_sha256,
                        verified_at = EXCLUDED.verified_at
                    """,
                    (job_id, row["source_sha"], row["generator_identity"],
                     artifact_path, artifact_sha256),
                )
                cur.execute(
                    """
                    UPDATE hmmm SET resolved_at = CURRENT_TIMESTAMP,
                        resolution = 'job later succeeded'
                    WHERE job_id = %s AND resolved_at IS NULL
                    """,
                    (job_id,),
                )
                cur.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
                updated = cur.fetchone()
            conn.commit()
        assert updated is not None
        return self._row_to_job(updated)

    def fail(self, job_id: str, *, error: str) -> Job:
        return self._transition(job_id, "failed", error=error, hmmm=None)

    def hold(self, job_id: str, *, constraint: str, error: str | None = None) -> Job:
        return self._transition(job_id, "hmmm", error=error or constraint, hmmm=constraint)

    def retry(self, job_id: str) -> Job:
        return self._transition(job_id, "queued", error=None, hmmm=None)

    def cancel(self, job_id: str) -> Job:
        return self._transition(job_id, "cancelled")

    def add_dependency(self, job_id: str, depends_on_job_id: str) -> None:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO job_dependencies (job_id, depends_on_job_id)
                    VALUES (%s, %s) ON CONFLICT DO NOTHING
                    """,
                    (job_id, depends_on_job_id),
                )
            conn.commit()
