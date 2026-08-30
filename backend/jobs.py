"""Durable job ledger for stack-level orchestration.

Usage:
    from backend.jobs import JobLedger
    ledger = JobLedger(".stack/state/jobs.sqlite3")
    job = ledger.enqueue(
        kind="msdmd.refresh",
        target="ucns",
        source_sha="<40-hex>",
        generator_identity="<sha256>",
        executor="local",
        payload={"root": "/srv/repos/ucns"},
    )
"""
from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_durable_job_ledger
#   module_name: durable_job_ledger
#   module_kind: engine
#   summary: persists idempotent stack orchestration jobs and explicit state transitions in SQLite
#   owner: stack
#   public_surface: Job, JobLedger
#   internal_surface: schema initialization, canonical dedupe key, row conversion
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: backend.tests.test_orchestrator
#   rollout: imported by frontend.cli.stackctl and backend.msdmd
#   rollback: remove callers and delete the untracked .stack state directory
# === END MODULE_BUILD ===

# === BOUNDARIES ===
# id: stack_durable_job_ledger_storage
#   summary: creates and updates a local SQLite orchestration ledger under the configured state directory
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   side_effects: job
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
#   then: the ledger raises ValueError and leaves the persisted state unchanged
#   class: correctness
# === END CONTRACTS ===

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any


JOB_STATES = ("queued", "running", "succeeded", "failed", "cancelled")
_ALLOWED_TRANSITIONS = {
    "queued": {"running", "cancelled"},
    "running": {"succeeded", "failed"},
    "succeeded": set(),
    "failed": {"queued", "cancelled"},
    "cancelled": {"queued"},
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


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
    """Small SQLite-backed orchestration ledger."""

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id TEXT PRIMARY KEY,
                    dedupe_key TEXT NOT NULL UNIQUE,
                    kind TEXT NOT NULL,
                    target TEXT NOT NULL,
                    source_sha TEXT NOT NULL,
                    generator_identity TEXT NOT NULL,
                    executor TEXT NOT NULL,
                    state TEXT NOT NULL,
                    attempts INTEGER NOT NULL DEFAULT 0,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    artifact_path TEXT,
                    artifact_sha256 TEXT,
                    error TEXT,
                    hmmm TEXT,
                    CHECK (state IN ('queued','running','succeeded','failed','cancelled'))
                )
                """
            )

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
    def _row_to_job(row: sqlite3.Row) -> Job:
        return Job(
            id=row["id"], dedupe_key=row["dedupe_key"], kind=row["kind"],
            target=row["target"], source_sha=row["source_sha"],
            generator_identity=row["generator_identity"], executor=row["executor"],
            state=row["state"], attempts=int(row["attempts"]),
            payload=json.loads(row["payload_json"]), created_at=row["created_at"],
            updated_at=row["updated_at"], artifact_path=row["artifact_path"],
            artifact_sha256=row["artifact_sha256"], error=row["error"], hmmm=row["hmmm"],
        )

    def enqueue(self, *, kind: str, target: str, source_sha: str,
                generator_identity: str, executor: str, payload: dict[str, Any],
                hmmm: str | None = None) -> Job:
        dedupe_key = self._dedupe_key(
            kind=kind, target=target, source_sha=source_sha,
            generator_identity=generator_identity, executor=executor, payload=payload,
        )
        job_id = f"job_{dedupe_key[:24]}"
        now = _now()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO jobs (
                    id, dedupe_key, kind, target, source_sha, generator_identity,
                    executor, state, attempts, payload_json, created_at, updated_at, hmmm
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'queued', 0, ?, ?, ?, ?)
                """,
                (job_id, dedupe_key, kind, target, source_sha, generator_identity,
                 executor, _canonical_json(payload), now, now, hmmm),
            )
            row = conn.execute("SELECT * FROM jobs WHERE dedupe_key = ?", (dedupe_key,)).fetchone()
        assert row is not None
        return self._row_to_job(row)

    def get(self, job_id: str) -> Job:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        if row is None:
            raise KeyError(job_id)
        return self._row_to_job(row)

    def list(self, *, limit: int = 100) -> list[Job]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [self._row_to_job(row) for row in rows]

    def transition(self, job_id: str, to_state: str, *,
                   artifact_path: str | None = None,
                   artifact_sha256: str | None = None,
                   error: str | None = None, hmmm: str | None = None,
                   increment_attempt: bool = False) -> Job:
        if to_state not in JOB_STATES:
            raise ValueError(f"unknown job state: {to_state}")
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
            if row is None:
                raise KeyError(job_id)
            current = str(row["state"])
            if to_state not in _ALLOWED_TRANSITIONS[current]:
                raise ValueError(f"invalid job transition: {current} -> {to_state}")
            attempts = int(row["attempts"]) + (1 if increment_attempt else 0)
            conn.execute(
                """
                UPDATE jobs SET state = ?, attempts = ?, updated_at = ?,
                    artifact_path = COALESCE(?, artifact_path),
                    artifact_sha256 = COALESCE(?, artifact_sha256),
                    error = ?, hmmm = ? WHERE id = ?
                """,
                (to_state, attempts, _now(), artifact_path, artifact_sha256,
                 error, hmmm, job_id),
            )
            updated = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        assert updated is not None
        return self._row_to_job(updated)

    def start(self, job_id: str) -> Job:
        return self.transition(job_id, "running", error=None, increment_attempt=True)

    def succeed(self, job_id: str, *, artifact_path: str, artifact_sha256: str) -> Job:
        return self.transition(job_id, "succeeded", artifact_path=artifact_path,
                               artifact_sha256=artifact_sha256, error=None, hmmm=None)

    def fail(self, job_id: str, *, error: str, hmmm: str | None = None) -> Job:
        return self.transition(job_id, "failed", error=error, hmmm=hmmm)

    def retry(self, job_id: str) -> Job:
        return self.transition(job_id, "queued", error=None)

    def cancel(self, job_id: str) -> Job:
        return self.transition(job_id, "cancelled")
