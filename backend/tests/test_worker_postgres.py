"""Checks for VM worker ordering and PostgreSQL stale-lease recovery."""
from __future__ import annotations

# === CHECKS ===
# id: check_stack_job_stale_lease_visible
#   proves: stack_job_stale_lease_visible
#   call: self::test_postgres_stale_lease_requeues_with_hmmm
#   requires: python3, postgres, psycopg
#   mutates: db
#   cleanup: delete_test_job
#
# id: check_stack_worker_recovers_stale_lease
#   proves: stack_worker_recovers_stale_lease
#   call: self::test_worker_recovers_before_claim
#   requires: python3
#   mutates: none
#   cleanup: none
#
# id: check_stack_worker_claims_one_job
#   proves: stack_worker_claims_one_job
#   call: self::test_worker_claims_and_runs_one_job
#   requires: python3
#   mutates: none
#   cleanup: none
# === END CHECKS ===

import hashlib
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import uuid

from backend.jobs import Job, JobLedger
from backend.worker import run_once

class WorkerLedger:
    def __init__(self, job: Job | None):
        self.job = job
        self.recovered = False
        self.claims = 0

    def requeue_stale(self) -> int:
        self.recovered = True
        return 1

    def claim_next(self, *, executor: str, worker_id: str, lease_seconds: int):
        if not self.recovered:
            raise AssertionError("claim occurred before stale-lease recovery")
        self.claims += 1
        return self.job if self.claims == 1 else None

class WorkerUnitTests(unittest.TestCase):
    def test_worker_recovers_before_claim(self) -> None:
        ledger = WorkerLedger(None)
        with patch.dict(os.environ, {"STACK_COMMAND_TIMEOUT_SECONDS": "30"}, clear=False):
            did_work = run_once(ledger, worker_id="test", lease_seconds=120)
        self.assertFalse(did_work)
        self.assertTrue(ledger.recovered)
        self.assertEqual(ledger.claims, 1)

    def test_worker_claims_and_runs_one_job(self) -> None:
        job = Job(
            id="job_test", dedupe_key="a" * 64, kind="msdmd.refresh", target="ucns",
            source_sha="b" * 40, generator_identity="c" * 64, executor="local",
            state="running", attempts=1, payload={},
            created_at="2026-08-30T00:00:00+00:00",
            updated_at="2026-08-30T00:00:00+00:00",
            artifact_path=None, artifact_sha256=None, error=None, hmmm=None,
        )
        ledger = WorkerLedger(job)
        with patch.dict(os.environ, {"STACK_COMMAND_TIMEOUT_SECONDS": "30"}, clear=False), \
             patch("backend.worker.run_job") as mocked_run:
            did_work = run_once(ledger, worker_id="test", lease_seconds=120)
        self.assertTrue(did_work)
        mocked_run.assert_called_once_with(ledger, "job_test", worker_id="test")

@unittest.skipUnless(
    os.environ.get("STACK_TEST_DATABASE_URL"),
    "set STACK_TEST_DATABASE_URL to a disposable PostgreSQL database",
)
class PostgresStaleLeaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        try:
            import psycopg  # noqa: F401
        except ImportError as exc:
            raise unittest.SkipTest("psycopg is not installed") from exc
        cls.ledger = JobLedger(
            os.environ["STACK_TEST_DATABASE_URL"],
            receipt_dir=Path(tempfile.gettempdir()) / "stack-test-receipts",
        )
        cls.ledger.migrate()
        cls.job_ids: list[str] = []

    @classmethod
    def tearDownClass(cls) -> None:
        if not hasattr(cls, "ledger"):
            return
        with cls.ledger._connect() as conn:
            with conn.cursor() as cur:
                for job_id in cls.job_ids:
                    cur.execute("DELETE FROM jobs WHERE id = %s", (job_id,))
            conn.commit()

    def test_postgres_stale_lease_requeues_with_hmmm(self) -> None:
        nonce = uuid.uuid4().hex
        job = self.ledger.enqueue(
            kind="msdmd.refresh", target=f"stale-{nonce[:8]}",
            source_sha=hashlib.sha1(nonce.encode()).hexdigest(),
            generator_identity=hashlib.sha256(nonce.encode()).hexdigest(),
            executor="local", payload={"root": f"/tmp/{nonce}"},
        )
        self.job_ids.append(job.id)
        claimed = self.ledger.claim_next(
            executor="local", worker_id="stale-test", lease_seconds=120
        )
        self.assertIsNotNone(claimed)
        with self.ledger._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE jobs SET lease_until = CURRENT_TIMESTAMP - INTERVAL '1 second' WHERE id = %s",
                    (job.id,),
                )
            conn.commit()
        self.assertEqual(self.ledger.requeue_stale(), 1)
        recovered = self.ledger.get(job.id)
        self.assertEqual(recovered.state, "queued")
        self.assertIn("lease expired", recovered.hmmm or "")
        with self.ledger._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT constraint FROM hmmm WHERE job_id = %s AND resolved_at IS NULL",
                    (job.id,),
                )
                row = cur.fetchone()
        self.assertIn("lease expired", row["constraint"])

if __name__ == "__main__":
    unittest.main()
