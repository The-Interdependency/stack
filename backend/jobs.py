"""Durable executor-independent job ledger for stack fresh-making."""
from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_fresh_job_ledger
#   module_name: fresh_job_ledger
#   module_kind: engine
#   summary: persists executor-independent fresh-making jobs, attempts, leases, and accepted receipts in SQLite
#   owner: stack
#   public_surface: Job, Attempt, Acceptance, JobLedger
#   storage_boundary: write
#   network_boundary: none
#   tests: backend.tests.test_orchestrator
#   rollout: backend.msdmd and frontend.cli.stackctl
#   rollback: stop callers; untracked .stack state can be removed without altering repo canon
# === END MODULE_BUILD ===

# === BOUNDARIES ===
# id: stack_fresh_job_storage
#   summary: writes operational SQLite state only; repository canon is never stored as authority here
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   side_effects: job
#   owner: stack
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: stack_fresh_job_identity_executor_independent
#   given: the same target and desired freshness key are requested through different executors
#   then: one logical job identity is retained while executor choice remains attempt metadata
#   class: idempotency
#
# id: stack_fresh_job_lease_recovery
#   given: an executor dies while holding an expired lease
#   then: the attempt remains recorded and the logical job returns to queued for bounded retry
#   class: resilience
#
# id: stack_fresh_attempt_history_preserved
#   given: a failed, cancelled, hmmm, or expired attempt is retried
#   then: previous attempt rows remain immutable evidence and a new ordinal attempt is created
#   class: evidence
# === END CONTRACTS ===

from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any


JOB_STATES = ("queued", "leased", "running", "verifying", "succeeded", "failed", "cancelled", "hmmm")
_ACTIVE_STATES = {"leased", "running", "verifying"}
_ALLOWED_TRANSITIONS = {
    "queued": {"leased", "cancelled"},
    "leased": {"running", "queued", "failed", "cancelled", "hmmm"},
    "running": {"verifying", "failed", "cancelled", "hmmm"},
    "verifying": {"succeeded", "failed", "cancelled", "hmmm"},
    "succeeded": {"queued"},
    "failed": {"queued", "cancelled"},
    "cancelled": {"queued"},
    "hmmm": {"queued", "cancelled"},
}


def _now_dt() -> datetime:
    return datetime.now(timezone.utc)


def _now() -> str:
    return _now_dt().isoformat()


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


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
    lease_expires_at: str | None
    active_attempt_id: str | None
    receipt_path: str | None
    error: str | None
    hmmm: str | None


@dataclass(frozen=True)
class Attempt:
    id: str
    job_id: str
    ordinal: int
    executor: str
    state: str
    lease_owner: str
    created_at: str
    started_at: str | None
    finished_at: str | None
    error: str | None
    hmmm: str | None


@dataclass(frozen=True)
class Acceptance:
    target: str
    freshness_key: str
    receipt_path: str
    accepted_at: str


class JobLedger:
    """SQLite-backed fresh-making jobs, attempts, leases, and accepted receipts.

    The historical ``jobs`` table from the prototype is intentionally left
    untouched if it exists. Fresh-making uses versioned ``fresh_*`` tables so
    old rows are not silently reinterpreted under stronger semantics.
    """

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA busy_timeout = 5000")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS fresh_jobs (
                    id TEXT PRIMARY KEY,
                    dedupe_key TEXT NOT NULL UNIQUE,
                    kind TEXT NOT NULL,
                    target TEXT NOT NULL,
                    freshness_key TEXT NOT NULL,
                    preferred_executor TEXT NOT NULL,
                    state TEXT NOT NULL,
                    attempts INTEGER NOT NULL DEFAULT 0,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    lease_owner TEXT,
                    lease_expires_at TEXT,
                    active_attempt_id TEXT,
                    receipt_path TEXT,
                    error TEXT,
                    hmmm TEXT,
                    CHECK (state IN ('queued','leased','running','verifying','succeeded','failed','cancelled','hmmm'))
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS fresh_attempts (
                    id TEXT PRIMARY KEY,
                    job_id TEXT NOT NULL,
                    ordinal INTEGER NOT NULL,
                    executor TEXT NOT NULL,
                    state TEXT NOT NULL,
                    lease_owner TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    started_at TEXT,
                    finished_at TEXT,
                    error TEXT,
                    hmmm TEXT,
                    UNIQUE(job_id, ordinal),
                    FOREIGN KEY(job_id) REFERENCES fresh_jobs(id)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS fresh_acceptance (
                    target TEXT PRIMARY KEY,
                    freshness_key TEXT NOT NULL,
                    receipt_path TEXT NOT NULL,
                    accepted_at TEXT NOT NULL
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS fresh_jobs_target_idx ON fresh_jobs(target, created_at)")
            conn.execute("CREATE INDEX IF NOT EXISTS fresh_jobs_state_idx ON fresh_jobs(state)")

    @staticmethod
    def _dedupe_key(*, kind: str, target: str, freshness_key: str) -> str:
        material = {"kind": kind, "target": target, "freshness_key": freshness_key}
        return hashlib.sha256(_canonical_json(material).encode("utf-8")).hexdigest()

    @staticmethod
    def _row_to_job(row: sqlite3.Row) -> Job:
        return Job(
            id=row["id"],
            dedupe_key=row["dedupe_key"],
            kind=row["kind"],
            target=row["target"],
            freshness_key=row["freshness_key"],
            preferred_executor=row["preferred_executor"],
            state=row["state"],
            attempts=int(row["attempts"]),
            payload=json.loads(row["payload_json"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            lease_owner=row["lease_owner"],
            lease_expires_at=row["lease_expires_at"],
            active_attempt_id=row["active_attempt_id"],
            receipt_path=row["receipt_path"],
            error=row["error"],
            hmmm=row["hmmm"],
        )

    @staticmethod
    def _row_to_attempt(row: sqlite3.Row) -> Attempt:
        return Attempt(
            id=row["id"], job_id=row["job_id"], ordinal=int(row["ordinal"]),
            executor=row["executor"], state=row["state"], lease_owner=row["lease_owner"],
            created_at=row["created_at"], started_at=row["started_at"],
            finished_at=row["finished_at"], error=row["error"], hmmm=row["hmmm"],
        )

    def enqueue(self, *, kind: str, target: str, freshness_key: str,
                payload: dict[str, Any], executor: str = "local",
                hmmm: str | None = None) -> Job:
        if not freshness_key or len(freshness_key) != 64:
            raise ValueError("freshness_key must be a 64-character SHA-256 hex digest")
        dedupe_key = self._dedupe_key(kind=kind, target=target, freshness_key=freshness_key)
        job_id = f"job_{dedupe_key[:24]}"
        now = _now()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO fresh_jobs (
                    id, dedupe_key, kind, target, freshness_key, preferred_executor,
                    state, attempts, payload_json, created_at, updated_at, hmmm
                ) VALUES (?, ?, ?, ?, ?, ?, 'queued', 0, ?, ?, ?, ?)
                """,
                (job_id, dedupe_key, kind, target, freshness_key, executor,
                 _canonical_json(payload), now, now, hmmm),
            )
            row = conn.execute("SELECT * FROM fresh_jobs WHERE dedupe_key = ?", (dedupe_key,)).fetchone()
        assert row is not None
        return self._row_to_job(row)

    def get(self, job_id: str) -> Job:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM fresh_jobs WHERE id = ?", (job_id,)).fetchone()
        if row is None:
            raise KeyError(job_id)
        return self._row_to_job(row)

    def list(self, *, limit: int = 100, target: str | None = None) -> list[Job]:
        with self._connect() as conn:
            if target is None:
                rows = conn.execute(
                    "SELECT * FROM fresh_jobs ORDER BY created_at DESC LIMIT ?", (limit,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM fresh_jobs WHERE target = ? ORDER BY created_at DESC LIMIT ?",
                    (target, limit),
                ).fetchall()
        return [self._row_to_job(row) for row in rows]

    def attempts_for(self, job_id: str) -> list[Attempt]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM fresh_attempts WHERE job_id = ? ORDER BY ordinal", (job_id,)
            ).fetchall()
        return [self._row_to_attempt(row) for row in rows]

    def active_job_for_target(self, target: str) -> Job | None:
        with self._connect() as conn:
            row = conn.execute(
                """SELECT * FROM fresh_jobs
                   WHERE target = ? AND state IN ('queued','leased','running','verifying')
                   ORDER BY created_at DESC LIMIT 1""",
                (target,),
            ).fetchone()
        return self._row_to_job(row) if row is not None else None

    def _transition(self, conn: sqlite3.Connection, job_id: str, to_state: str,
                    *, error: str | None = None, hmmm: str | None = None,
                    receipt_path: str | None = None,
                    clear_lease: bool = False) -> sqlite3.Row:
        if to_state not in JOB_STATES:
            raise ValueError(f"unknown job state: {to_state}")
        row = conn.execute("SELECT * FROM fresh_jobs WHERE id = ?", (job_id,)).fetchone()
        if row is None:
            raise KeyError(job_id)
        current = str(row["state"])
        if to_state not in _ALLOWED_TRANSITIONS[current]:
            raise ValueError(f"invalid job transition: {current} -> {to_state}")
        lease_owner = None if clear_lease else row["lease_owner"]
        lease_expires_at = None if clear_lease else row["lease_expires_at"]
        active_attempt_id = None if clear_lease else row["active_attempt_id"]
        conn.execute(
            """
            UPDATE fresh_jobs SET state = ?, updated_at = ?, error = ?, hmmm = ?,
                receipt_path = COALESCE(?, receipt_path), lease_owner = ?,
                lease_expires_at = ?, active_attempt_id = ? WHERE id = ?
            """,
            (to_state, _now(), error, hmmm, receipt_path, lease_owner,
             lease_expires_at, active_attempt_id, job_id),
        )
        updated = conn.execute("SELECT * FROM fresh_jobs WHERE id = ?", (job_id,)).fetchone()
        assert updated is not None
        return updated

    def acquire_lease(self, job_id: str, *, owner: str, executor: str | None = None,
                      ttl_seconds: int = 300) -> Job:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self.recover_expired_leases()
        now_dt = _now_dt()
        now = now_dt.isoformat()
        expires = (now_dt + timedelta(seconds=ttl_seconds)).isoformat()
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            row = conn.execute("SELECT * FROM fresh_jobs WHERE id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            if row["state"] != "queued":
                raise ValueError(f"job must be queued before lease: {row['state']}")
            ordinal = int(row["attempts"]) + 1
            attempt_id = f"attempt_{job_id[4:16]}_{ordinal}"
            selected_executor = executor or str(row["preferred_executor"])
            conn.execute(
                """INSERT INTO fresh_attempts
                   (id, job_id, ordinal, executor, state, lease_owner, created_at)
                   VALUES (?, ?, ?, ?, 'leased', ?, ?)""",
                (attempt_id, job_id, ordinal, selected_executor, owner, now),
            )
            conn.execute(
                """UPDATE fresh_jobs SET state='leased', attempts=?, preferred_executor=?,
                   updated_at=?, lease_owner=?, lease_expires_at=?, active_attempt_id=?,
                   error=NULL, hmmm=NULL WHERE id=?""",
                (ordinal, selected_executor, now, owner, expires, attempt_id, job_id),
            )
            updated = conn.execute("SELECT * FROM fresh_jobs WHERE id = ?", (job_id,)).fetchone()
        assert updated is not None
        return self._row_to_job(updated)

    def heartbeat(self, job_id: str, *, owner: str, ttl_seconds: int = 300) -> Job:
        expires = (_now_dt() + timedelta(seconds=ttl_seconds)).isoformat()
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM fresh_jobs WHERE id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            if row["state"] not in _ACTIVE_STATES or row["lease_owner"] != owner:
                raise ValueError("heartbeat requires the active lease owner")
            conn.execute(
                "UPDATE fresh_jobs SET lease_expires_at=?, updated_at=? WHERE id=?",
                (expires, _now(), job_id),
            )
        return self.get(job_id)

    def start(self, job_id: str, *, owner: str) -> Job:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM fresh_jobs WHERE id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            if row["state"] != "leased" or row["lease_owner"] != owner:
                raise ValueError("start requires a lease owned by the caller")
            updated = self._transition(conn, job_id, "running")
            conn.execute(
                "UPDATE fresh_attempts SET state='running', started_at=? WHERE id=?",
                (_now(), row["active_attempt_id"]),
            )
        return self._row_to_job(updated)

    def mark_verifying(self, job_id: str, *, owner: str) -> Job:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM fresh_jobs WHERE id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            if row["lease_owner"] != owner:
                raise ValueError("verification requires the active lease owner")
            updated = self._transition(conn, job_id, "verifying")
            conn.execute(
                "UPDATE fresh_attempts SET state='verifying' WHERE id=?",
                (row["active_attempt_id"],),
            )
        return self._row_to_job(updated)

    def _finish(self, job_id: str, to_state: str, *, error: str | None = None,
                hmmm: str | None = None, receipt_path: str | None = None) -> Job:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM fresh_jobs WHERE id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            attempt_id = row["active_attempt_id"]
            updated = self._transition(
                conn, job_id, to_state, error=error, hmmm=hmmm,
                receipt_path=receipt_path, clear_lease=True,
            )
            if attempt_id:
                conn.execute(
                    """UPDATE fresh_attempts SET state=?, finished_at=?, error=?, hmmm=?
                       WHERE id=?""",
                    (to_state, _now(), error, hmmm, attempt_id),
                )
        return self._row_to_job(updated)

    def succeed(self, job_id: str, *, receipt_path: str) -> Job:
        return self._finish(job_id, "succeeded", receipt_path=receipt_path)

    def fail(self, job_id: str, *, error: str, hmmm: str | None = None) -> Job:
        return self._finish(job_id, "failed", error=error, hmmm=hmmm)

    def mark_hmmm(self, job_id: str, *, hmmm: str) -> Job:
        return self._finish(job_id, "hmmm", hmmm=hmmm)

    def retry(self, job_id: str, *, executor: str | None = None) -> Job:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM fresh_jobs WHERE id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            if row["state"] not in {"failed", "cancelled", "hmmm", "succeeded"}:
                raise ValueError(f"only terminal jobs can be requeued: {row['state']}")
            selected = executor or row["preferred_executor"]
            conn.execute(
                """UPDATE fresh_jobs SET state='queued', preferred_executor=?, updated_at=?,
                   lease_owner=NULL, lease_expires_at=NULL, active_attempt_id=NULL,
                   error=NULL, hmmm=NULL WHERE id=?""",
                (selected, _now(), job_id),
            )
        return self.get(job_id)

    def cancel(self, job_id: str) -> Job:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM fresh_jobs WHERE id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            if row["state"] not in {"queued", "leased", "running", "verifying", "failed", "hmmm"}:
                raise ValueError(f"job cannot be cancelled from {row['state']}")
            attempt_id = row["active_attempt_id"]
            current = row["state"]
            if current == "queued":
                updated = self._transition(conn, job_id, "cancelled", clear_lease=True)
            elif current in {"leased", "running", "verifying"}:
                updated = self._transition(conn, job_id, "cancelled", clear_lease=True)
                if attempt_id:
                    conn.execute(
                        "UPDATE fresh_attempts SET state='cancelled', finished_at=? WHERE id=?",
                        (_now(), attempt_id),
                    )
            else:
                updated = self._transition(conn, job_id, "cancelled", clear_lease=True)
        return self._row_to_job(updated)

    def recover_expired_leases(self, *, now: datetime | None = None) -> list[Job]:
        cutoff = (now or _now_dt()).isoformat()
        recovered: list[Job] = []
        with self._connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            rows = conn.execute(
                """SELECT * FROM fresh_jobs
                   WHERE state IN ('leased','running','verifying')
                     AND lease_expires_at IS NOT NULL AND lease_expires_at <= ?""",
                (cutoff,),
            ).fetchall()
            for row in rows:
                attempt_id = row["active_attempt_id"]
                if attempt_id:
                    conn.execute(
                        """UPDATE fresh_attempts SET state='failed', finished_at=?,
                           error='lease expired' WHERE id=?""",
                        (_now(), attempt_id),
                    )
                conn.execute(
                    """UPDATE fresh_jobs SET state='queued', updated_at=?,
                       lease_owner=NULL, lease_expires_at=NULL, active_attempt_id=NULL,
                       error='lease expired; recovered for retry', hmmm=NULL WHERE id=?""",
                    (_now(), row["id"]),
                )
                updated = conn.execute(
                    "SELECT * FROM fresh_jobs WHERE id=?", (row["id"],)
                ).fetchone()
                assert updated is not None
                recovered.append(self._row_to_job(updated))
        return recovered

    def accept_target(self, *, target: str, freshness_key: str, receipt_path: str) -> Acceptance:
        accepted_at = _now()
        with self._connect() as conn:
            conn.execute(
                """INSERT INTO fresh_acceptance(target, freshness_key, receipt_path, accepted_at)
                   VALUES (?, ?, ?, ?)
                   ON CONFLICT(target) DO UPDATE SET
                     freshness_key=excluded.freshness_key,
                     receipt_path=excluded.receipt_path,
                     accepted_at=excluded.accepted_at""",
                (target, freshness_key, receipt_path, accepted_at),
            )
        return Acceptance(target, freshness_key, receipt_path, accepted_at)

    def get_acceptance(self, target: str) -> Acceptance | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM fresh_acceptance WHERE target=?", (target,)
            ).fetchone()
        if row is None:
            return None
        return Acceptance(
            target=row["target"], freshness_key=row["freshness_key"],
            receipt_path=row["receipt_path"], accepted_at=row["accepted_at"],
        )
