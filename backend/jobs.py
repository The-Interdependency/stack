"""PostgreSQL durable state for stack fresh-making.

PostgreSQL is the single production orchestration boundary. Repository canon and
artifacts remain owned by their repositories; the database owns derivation specs,
logical jobs, attempts/leases, receipts, dependency edges, accepted freshness, and
visible hmmm.
"""
from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_fresh_postgres_ledger
#   module_name: fresh_postgres_ledger
#   module_kind: engine
#   summary: stores derivation specs, executor-independent logical jobs, attempts, leases, receipts, acceptance, dependencies, and hmmm in one PostgreSQL authority
#   owner: stack
#   public_surface: Job, Attempt, Acceptance, Receipt, JobLedger
#   auth_boundary: write
#   storage_boundary: migration
#   network_boundary: internal
#   tests: backend.tests.test_orchestrator, backend.tests.test_worker_postgres
#   rollout: PostgreSQL on the stack VM
#   rollback: stop workers; database state remains inspectable and repository canon remains external
# === END MODULE_BUILD ===

# === BOUNDARIES ===
# id: stack_fresh_postgres_storage_boundary
#   summary: PostgreSQL owns orchestration and freshness evidence only; repositories retain source, canon, and artifact authority
#   auth_boundary: write
#   storage_boundary: write
#   network_boundary: internal
#   user_data_boundary: none
#   admin_only: true
#   side_effects: database, job
#   owner: stack
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: stack_fresh_job_identity_executor_independent
#   given: the same kind, target, and desired freshness key are requested through different executors
#   then: one logical job identity is retained while executor choice remains attempt metadata
#   class: idempotency
#
# id: stack_fresh_job_claim_skip_locked
#   given: multiple workers claim queued fresh-making jobs concurrently
#   then: PostgreSQL FOR UPDATE SKIP LOCKED leases each logical job to at most one worker attempt
#   class: concurrency
#
# id: stack_fresh_job_stale_lease_visible
#   given: a worker dies before completing an attempt and its lease expires
#   then: the attempt is preserved as hmmm and the logical job returns to queued
#   class: resilience
#
# id: stack_fresh_attempt_history_preserved
#   given: a terminal logical job is retried for the same freshness key
#   then: prior attempts and receipts remain evidence and a new ordinal attempt is created
#   class: evidence
# === END CONTRACTS ===

from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
from pathlib import Path
import uuid
from typing import Any

JOB_STATES = ("queued", "leased", "running", "verifying", "succeeded", "failed", "hmmm", "cancelled")
ACTIVE_STATES = ("queued", "leased", "running", "verifying")
TERMINAL_STATES = ("succeeded", "failed", "hmmm", "cancelled")


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _iso(value: Any) -> str | None:
    if value is None:
        return None
    return value.isoformat() if isinstance(value, datetime) else str(value)


@dataclass(frozen=True)
class Job:
    id: str
    dedupe_key: str
    kind: str
    target: str
    freshness_key: str
    preferred_executor: str
    state: str
    attempts: int
    payload: dict[str, Any]
    created_at: str
    updated_at: str
    lease_owner: str | None
    lease_until: str | None
    active_attempt_id: str | None
    receipt_id: str | None
    error: str | None
    hmmm: str | None


@dataclass(frozen=True)
class Attempt:
    id: str
    job_id: str
    ordinal: int
    executor: str
    worker_id: str
    state: str
    created_at: str
    started_at: str | None
    finished_at: str | None
    error: str | None
    hmmm: str | None


@dataclass(frozen=True)
class Acceptance:
    target: str
    freshness_key: str
    receipt_id: str
    accepted_at: str


@dataclass(frozen=True)
class Receipt:
    id: str
    job_id: str
    target: str
    freshness_key: str
    output_path: str
    output_sha256: str
    receipt: dict[str, Any]
    verified_at: str


class JobLedger:
    """PostgreSQL-only fresh-making state and transactional worker claims."""

    def __init__(self, database_url: str, *, receipt_dir: str | Path | None = None):
        if not database_url.startswith(("postgresql://", "postgres://")):
            raise ValueError("JobLedger requires a PostgreSQL database URL")
        self.database_url = database_url
        self.receipt_dir = Path(receipt_dir or "/var/lib/stack-orchestrator/receipts").resolve()

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
    def _dedupe_key(*, kind: str, target: str, freshness_key: str) -> str:
        material = {"kind": kind, "target": target, "freshness_key": freshness_key}
        return hashlib.sha256(_canonical_json(material).encode("utf-8")).hexdigest()

    @staticmethod
    def _row_to_job(row: dict[str, Any]) -> Job:
        payload = row["payload_json"]
        if isinstance(payload, str):
            payload = json.loads(payload)
        return Job(
            id=row["id"], dedupe_key=row["dedupe_key"], kind=row["kind"], target=row["target"],
            freshness_key=row["freshness_key"], preferred_executor=row["preferred_executor"],
            state=row["state"], attempts=int(row["attempts"]), payload=dict(payload),
            created_at=str(_iso(row["created_at"])), updated_at=str(_iso(row["updated_at"])),
            lease_owner=row["lease_owner"], lease_until=_iso(row["lease_until"]),
            active_attempt_id=row["active_attempt_id"], receipt_id=row["receipt_id"],
            error=row["error"], hmmm=row["hmmm"],
        )

    @staticmethod
    def _row_to_attempt(row: dict[str, Any]) -> Attempt:
        return Attempt(
            id=row["id"], job_id=row["job_id"], ordinal=int(row["ordinal"]),
            executor=row["executor"], worker_id=row["worker_id"], state=row["state"],
            created_at=str(_iso(row["created_at"])), started_at=_iso(row["started_at"]),
            finished_at=_iso(row["finished_at"]), error=row["error"], hmmm=row["hmmm"],
        )

    def upsert_derivation(self, spec: dict[str, Any], freshness_key: str) -> None:
        target = str(spec["target"])
        dependencies = [str(item) for item in spec.get("depends_on", [])]
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO derivations(target, kind, freshness_key, spec_json)
                    VALUES (%s, %s, %s, %s::jsonb)
                    ON CONFLICT(target) DO UPDATE SET
                      kind=EXCLUDED.kind, freshness_key=EXCLUDED.freshness_key,
                      spec_json=EXCLUDED.spec_json, updated_at=CURRENT_TIMESTAMP
                    """,
                    (target, spec["kind"], freshness_key, _canonical_json(spec)),
                )
                cur.execute("DELETE FROM derivation_dependencies WHERE target=%s", (target,))
                for dependency in dependencies:
                    cur.execute(
                        """INSERT INTO derivation_dependencies(target, depends_on_target)
                           VALUES (%s, %s) ON CONFLICT DO NOTHING""",
                        (target, dependency),
                    )
            conn.commit()

    def get_derivation(self, target: str) -> dict[str, Any]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT spec_json FROM derivations WHERE target=%s", (target,))
                row = cur.fetchone()
        if row is None:
            raise KeyError(target)
        value = row["spec_json"]
        return json.loads(value) if isinstance(value, str) else dict(value)

    def list_derivations(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT spec_json FROM derivations ORDER BY target")
                rows = cur.fetchall()
        out: list[dict[str, Any]] = []
        for row in rows:
            value = row["spec_json"]
            out.append(json.loads(value) if isinstance(value, str) else dict(value))
        return out

    def enqueue(self, *, kind: str, target: str, freshness_key: str,
                payload: dict[str, Any], executor: str = "local") -> Job:
        if len(freshness_key) != 64:
            raise ValueError("freshness_key must be a SHA-256 hex digest")
        dedupe_key = self._dedupe_key(kind=kind, target=target, freshness_key=freshness_key)
        job_id = f"job_{dedupe_key[:24]}"
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO jobs(id, dedupe_key, kind, target, freshness_key,
                                     preferred_executor, state, payload_json)
                    VALUES (%s,%s,%s,%s,%s,%s,'queued',%s::jsonb)
                    ON CONFLICT(dedupe_key) DO NOTHING
                    """,
                    (job_id, dedupe_key, kind, target, freshness_key, executor,
                     _canonical_json(payload)),
                )
                cur.execute("SELECT * FROM jobs WHERE dedupe_key=%s", (dedupe_key,))
                row = cur.fetchone()
            conn.commit()
        assert row is not None
        return self._row_to_job(row)

    def get(self, job_id: str) -> Job:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM jobs WHERE id=%s", (job_id,))
                row = cur.fetchone()
        if row is None:
            raise KeyError(job_id)
        return self._row_to_job(row)

    def list(self, *, limit: int = 100, target: str | None = None) -> list[Job]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                if target:
                    cur.execute("SELECT * FROM jobs WHERE target=%s ORDER BY created_at DESC LIMIT %s", (target, limit))
                else:
                    cur.execute("SELECT * FROM jobs ORDER BY created_at DESC LIMIT %s", (limit,))
                rows = cur.fetchall()
        return [self._row_to_job(row) for row in rows]

    def attempts_for(self, job_id: str) -> list[Attempt]:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM attempts WHERE job_id=%s ORDER BY ordinal", (job_id,))
                rows = cur.fetchall()
        return [self._row_to_attempt(row) for row in rows]

    def active_job_for_target(self, target: str) -> Job | None:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT * FROM jobs WHERE target=%s
                       AND state IN ('queued','leased','running','verifying')
                       ORDER BY created_at DESC LIMIT 1""",
                    (target,),
                )
                row = cur.fetchone()
        return self._row_to_job(row) if row else None

    def _lease_row(self, cur, row: dict[str, Any], *, executor: str,
                   worker_id: str, lease_seconds: int) -> dict[str, Any]:
        ordinal = int(row["attempts"]) + 1
        attempt_id = f"attempt_{uuid.uuid4().hex}"
        cur.execute(
            """
            INSERT INTO attempts(id, job_id, ordinal, executor, worker_id, state)
            VALUES (%s,%s,%s,%s,%s,'leased')
            """,
            (attempt_id, row["id"], ordinal, executor, worker_id),
        )
        cur.execute(
            """
            UPDATE jobs SET state='leased', attempts=%s, preferred_executor=%s,
                lease_owner=%s,
                lease_until=CURRENT_TIMESTAMP + (%s * INTERVAL '1 second'),
                active_attempt_id=%s, error=NULL, hmmm=NULL,
                updated_at=CURRENT_TIMESTAMP
            WHERE id=%s
            """,
            (ordinal, executor, worker_id, lease_seconds, attempt_id, row["id"]),
        )
        cur.execute("SELECT * FROM jobs WHERE id=%s", (row["id"],))
        updated = cur.fetchone()
        assert updated is not None
        return updated

    def acquire_lease(self, job_id: str, *, worker_id: str, executor: str = "local",
                      lease_seconds: int = 1800) -> Job:
        if lease_seconds <= 0:
            raise ValueError("lease_seconds must be positive")
        self.requeue_stale()
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM jobs WHERE id=%s FOR UPDATE", (job_id,))
                row = cur.fetchone()
                if row is None:
                    raise KeyError(job_id)
                if row["state"] != "queued":
                    raise ValueError(f"job must be queued before lease: {row['state']}")
                updated = self._lease_row(
                    cur, row, executor=executor, worker_id=worker_id,
                    lease_seconds=lease_seconds,
                )
            conn.commit()
        return self._row_to_job(updated)

    def claim_next(self, *, executor: str, worker_id: str, lease_seconds: int) -> Job | None:
        self.requeue_stale()
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT * FROM jobs
                    WHERE state='queued' AND kind='fresh.make'
                    ORDER BY created_at, id
                    FOR UPDATE SKIP LOCKED LIMIT 1
                    """
                )
                row = cur.fetchone()
                if row is None:
                    conn.commit()
                    return None
                updated = self._lease_row(
                    cur, row, executor=executor, worker_id=worker_id,
                    lease_seconds=lease_seconds,
                )
            conn.commit()
        return self._row_to_job(updated)

    def start(self, job_id: str, *, worker_id: str) -> Job:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM jobs WHERE id=%s FOR UPDATE", (job_id,))
                row = cur.fetchone()
                if row is None:
                    raise KeyError(job_id)
                if row["state"] != "leased" or row["lease_owner"] != worker_id:
                    raise ValueError("start requires the caller's active lease")
                cur.execute(
                    "UPDATE jobs SET state='running', updated_at=CURRENT_TIMESTAMP WHERE id=%s",
                    (job_id,),
                )
                cur.execute(
                    "UPDATE attempts SET state='running', started_at=CURRENT_TIMESTAMP WHERE id=%s",
                    (row["active_attempt_id"],),
                )
                cur.execute("SELECT * FROM jobs WHERE id=%s", (job_id,))
                updated = cur.fetchone()
            conn.commit()
        assert updated is not None
        return self._row_to_job(updated)

    def heartbeat(self, job_id: str, *, worker_id: str, lease_seconds: int) -> Job:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM jobs WHERE id=%s FOR UPDATE", (job_id,))
                row = cur.fetchone()
                if row is None:
                    raise KeyError(job_id)
                if row["state"] not in {"leased", "running", "verifying"} or row["lease_owner"] != worker_id:
                    raise ValueError("heartbeat requires the caller's active lease")
                cur.execute(
                    """UPDATE jobs SET lease_until=CURRENT_TIMESTAMP + (%s * INTERVAL '1 second'),
                       updated_at=CURRENT_TIMESTAMP WHERE id=%s""",
                    (lease_seconds, job_id),
                )
                cur.execute("SELECT * FROM jobs WHERE id=%s", (job_id,))
                updated = cur.fetchone()
            conn.commit()
        assert updated is not None
        return self._row_to_job(updated)

    def mark_verifying(self, job_id: str, *, worker_id: str) -> Job:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM jobs WHERE id=%s FOR UPDATE", (job_id,))
                row = cur.fetchone()
                if row is None:
                    raise KeyError(job_id)
                if row["state"] != "running" or row["lease_owner"] != worker_id:
                    raise ValueError("verification requires the caller's running lease")
                cur.execute("UPDATE jobs SET state='verifying', updated_at=CURRENT_TIMESTAMP WHERE id=%s", (job_id,))
                cur.execute("UPDATE attempts SET state='verifying' WHERE id=%s", (row["active_attempt_id"],))
                cur.execute("SELECT * FROM jobs WHERE id=%s", (job_id,))
                updated = cur.fetchone()
            conn.commit()
        assert updated is not None
        return self._row_to_job(updated)

    def _finish(self, job_id: str, state: str, *, error: str | None = None,
                hmmm: str | None = None) -> Job:
        if state not in {"failed", "hmmm", "cancelled"}:
            raise ValueError("_finish handles only non-success terminal states")
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM jobs WHERE id=%s FOR UPDATE", (job_id,))
                row = cur.fetchone()
                if row is None:
                    raise KeyError(job_id)
                if row["state"] not in {"leased", "running", "verifying", "queued", "failed", "hmmm"}:
                    raise ValueError(f"cannot finish from {row['state']}")
                attempt_id = row["active_attempt_id"]
                cur.execute(
                    """UPDATE jobs SET state=%s, error=%s, hmmm=%s, lease_owner=NULL,
                       lease_until=NULL, active_attempt_id=NULL, updated_at=CURRENT_TIMESTAMP
                       WHERE id=%s""",
                    (state, error, hmmm, job_id),
                )
                if attempt_id:
                    cur.execute(
                        """UPDATE attempts SET state=%s, finished_at=CURRENT_TIMESTAMP,
                           error=%s, hmmm=%s WHERE id=%s""",
                        (state, error, hmmm, attempt_id),
                    )
                if hmmm:
                    cur.execute(
                        "INSERT INTO hmmm(id, target, job_id, constraint) VALUES (%s,%s,%s,%s)",
                        (f"hmmm_{uuid.uuid4().hex}", row["target"], job_id, hmmm),
                    )
                cur.execute("SELECT * FROM jobs WHERE id=%s", (job_id,))
                updated = cur.fetchone()
            conn.commit()
        assert updated is not None
        return self._row_to_job(updated)

    def fail(self, job_id: str, *, error: str, hmmm: str | None = None) -> Job:
        return self._finish(job_id, "failed", error=error, hmmm=hmmm)

    def hold(self, job_id: str, *, constraint: str, error: str | None = None) -> Job:
        return self._finish(job_id, "hmmm", error=error or constraint, hmmm=constraint)

    def cancel(self, job_id: str) -> Job:
        return self._finish(job_id, "cancelled")

    def retry(self, job_id: str, *, executor: str | None = None) -> Job:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM jobs WHERE id=%s FOR UPDATE", (job_id,))
                row = cur.fetchone()
                if row is None:
                    raise KeyError(job_id)
                if row["state"] not in TERMINAL_STATES:
                    raise ValueError(f"only terminal jobs can be requeued: {row['state']}")
                cur.execute(
                    """UPDATE jobs SET state='queued', preferred_executor=%s,
                       lease_owner=NULL, lease_until=NULL, active_attempt_id=NULL,
                       error=NULL, hmmm=NULL, updated_at=CURRENT_TIMESTAMP WHERE id=%s""",
                    (executor or row["preferred_executor"], job_id),
                )
                cur.execute("SELECT * FROM jobs WHERE id=%s", (job_id,))
                updated = cur.fetchone()
            conn.commit()
        assert updated is not None
        return self._row_to_job(updated)

    def requeue_stale(self) -> int:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT * FROM jobs WHERE state IN ('leased','running','verifying')
                       AND lease_until < CURRENT_TIMESTAMP FOR UPDATE"""
                )
                rows = cur.fetchall()
                for row in rows:
                    constraint = "worker lease expired before a terminal fresh-making receipt was accepted"
                    if row["active_attempt_id"]:
                        cur.execute(
                            """UPDATE attempts SET state='hmmm', finished_at=CURRENT_TIMESTAMP,
                               hmmm=%s WHERE id=%s""",
                            (constraint, row["active_attempt_id"]),
                        )
                    cur.execute(
                        "INSERT INTO hmmm(id,target,job_id,constraint) VALUES (%s,%s,%s,%s)",
                        (f"hmmm_{uuid.uuid4().hex}", row["target"], row["id"], constraint),
                    )
                    cur.execute(
                        """UPDATE jobs SET state='queued', lease_owner=NULL, lease_until=NULL,
                           active_attempt_id=NULL, hmmm=%s, error=NULL,
                           updated_at=CURRENT_TIMESTAMP WHERE id=%s""",
                        (constraint, row["id"]),
                    )
            conn.commit()
        return len(rows)

    def accept_success(self, job_id: str, *, receipt: dict[str, Any],
                       output_path: str, output_sha256: str) -> Job:
        """Atomically accept receipt, target freshness, attempt, and job success."""
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM jobs WHERE id=%s FOR UPDATE", (job_id,))
                row = cur.fetchone()
                if row is None:
                    raise KeyError(job_id)
                if row["state"] != "verifying":
                    raise ValueError(f"success requires verifying state, got {row['state']}")
                if receipt.get("freshness_key_sha256") != row["freshness_key"]:
                    raise ValueError("receipt freshness key differs from job")
                attempt_id = row["active_attempt_id"]
                if not attempt_id:
                    raise ValueError("success requires an active attempt")
                receipt_id = f"receipt_{uuid.uuid4().hex}"
                cur.execute(
                    """INSERT INTO receipts(id,job_id,target,freshness_key,attempt_id,
                           output_path,output_sha256,receipt_json)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s::jsonb)""",
                    (receipt_id, job_id, row["target"], row["freshness_key"], attempt_id,
                     output_path, output_sha256, _canonical_json(receipt)),
                )
                cur.execute(
                    """INSERT INTO target_acceptance(target,freshness_key,receipt_id)
                       VALUES (%s,%s,%s)
                       ON CONFLICT(target) DO UPDATE SET freshness_key=EXCLUDED.freshness_key,
                         receipt_id=EXCLUDED.receipt_id, accepted_at=CURRENT_TIMESTAMP""",
                    (row["target"], row["freshness_key"], receipt_id),
                )
                cur.execute(
                    """UPDATE jobs SET state='succeeded', receipt_id=%s, error=NULL, hmmm=NULL,
                       lease_owner=NULL, lease_until=NULL, active_attempt_id=NULL,
                       updated_at=CURRENT_TIMESTAMP WHERE id=%s""",
                    (receipt_id, job_id),
                )
                cur.execute(
                    "UPDATE attempts SET state='succeeded', finished_at=CURRENT_TIMESTAMP WHERE id=%s",
                    (attempt_id,),
                )
                cur.execute(
                    """UPDATE hmmm SET resolved_at=CURRENT_TIMESTAMP,
                       resolution='fresh-making target later accepted' WHERE target=%s AND resolved_at IS NULL""",
                    (row["target"],),
                )
                cur.execute("SELECT * FROM jobs WHERE id=%s", (job_id,))
                updated = cur.fetchone()
            conn.commit()
        assert updated is not None
        return self._row_to_job(updated)

    def get_acceptance(self, target: str) -> Acceptance | None:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM target_acceptance WHERE target=%s", (target,))
                row = cur.fetchone()
        if row is None:
            return None
        return Acceptance(
            target=row["target"], freshness_key=row["freshness_key"],
            receipt_id=row["receipt_id"], accepted_at=str(_iso(row["accepted_at"])),
        )

    def get_receipt(self, receipt_id: str) -> Receipt:
        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM receipts WHERE id=%s", (receipt_id,))
                row = cur.fetchone()
        if row is None:
            raise KeyError(receipt_id)
        payload = row["receipt_json"]
        if isinstance(payload, str):
            payload = json.loads(payload)
        return Receipt(
            id=row["id"], job_id=row["job_id"], target=row["target"],
            freshness_key=row["freshness_key"], output_path=row["output_path"],
            output_sha256=row["output_sha256"], receipt=dict(payload),
            verified_at=str(_iso(row["verified_at"])),
        )
