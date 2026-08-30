"""Checks VM worker ordering and PostgreSQL stale-lease contract."""
from __future__ import annotations

# === CHECKS ===
# id: check_stack_fresh_worker_recovers_stale_lease
#   proves: stack_fresh_worker_recovers_stale_lease
#   call: self::test_worker_recovers_before_claim
#   requires: python3
#   mutates: none
#
# id: check_stack_fresh_worker_claims_one_job
#   proves: stack_fresh_worker_claims_one_job
#   call: self::test_worker_claims_and_runs_one_job
#   requires: python3
#   mutates: none
#
# id: check_stack_fresh_job_stale_lease_visible
#   proves: stack_fresh_job_stale_lease_visible
#   call: self::test_postgres_stale_lease_requeues_with_hmmm
#   requires: python3, postgres, psycopg
#   mutates: database
# === END CHECKS ===

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
    def test_worker_recovers_before_claim(self):
        ledger = WorkerLedger(None)
        with patch.dict(os.environ, {"STACK_COMMAND_TIMEOUT_SECONDS":"30"}, clear=False):
            did_work = run_once(ledger, worker_id="test", lease_seconds=120)
        self.assertFalse(did_work)
        self.assertTrue(ledger.recovered)
        self.assertEqual(ledger.claims, 1)

    def test_worker_claims_and_runs_one_job(self):
        job = Job(
            id="job_test", dedupe_key="a"*64, kind="fresh.make", target="msdmd:ucns",
            freshness_key="b"*64, preferred_executor="local", state="leased", attempts=1,
            payload={"target":"msdmd:ucns"}, created_at="2026-08-30T00:00:00+00:00",
            updated_at="2026-08-30T00:00:00+00:00", lease_owner="test",
            lease_until="2099-01-01T00:00:00+00:00", active_attempt_id="attempt_test",
            receipt_id=None, error=None, hmmm=None,
        )
        ledger = WorkerLedger(job)
        with patch.dict(os.environ, {"STACK_COMMAND_TIMEOUT_SECONDS":"30"}, clear=False), \
             patch("backend.worker.run_job") as mocked:
            did_work = run_once(ledger, worker_id="test", lease_seconds=120)
        self.assertTrue(did_work)
        mocked.assert_called_once_with(
            ledger, "job_test", worker_id="test", executor="local", lease_seconds=120,
        )


@unittest.skipUnless(os.environ.get("STACK_TEST_DATABASE_URL"), "set STACK_TEST_DATABASE_URL to a disposable PostgreSQL database")
class PostgresStaleLeaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import psycopg  # noqa: F401
        except ImportError as exc:
            raise unittest.SkipTest("psycopg is not installed") from exc
        cls.ledger = JobLedger(os.environ["STACK_TEST_DATABASE_URL"], receipt_dir=Path(tempfile.gettempdir())/"stack-test-receipts")
        cls.ledger.migrate()
        cls.targets: list[str] = []

    @classmethod
    def tearDownClass(cls):
        if not hasattr(cls, "ledger"):
            return
        with cls.ledger._connect() as conn:
            with conn.cursor() as cur:
                for target in cls.targets:
                    cur.execute("DELETE FROM jobs WHERE target=%s", (target,))
            conn.commit()

    def test_postgres_stale_lease_requeues_with_hmmm(self):
        target = f"test:{uuid.uuid4().hex[:8]}"; self.targets.append(target)
        job = self.ledger.enqueue(kind="fresh.make", target=target, freshness_key="c"*64, payload={})
        claimed = self.ledger.claim_next(executor="local", worker_id="stale-test", lease_seconds=120)
        self.assertIsNotNone(claimed)
        with self.ledger._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE jobs SET lease_until=CURRENT_TIMESTAMP - INTERVAL '1 second' WHERE id=%s", (job.id,))
            conn.commit()
        self.assertEqual(self.ledger.requeue_stale(), 1)
        recovered = self.ledger.get(job.id)
        self.assertEqual(recovered.state, "queued")
        self.assertIn("lease expired", recovered.hmmm or "")

if __name__ == "__main__":
    unittest.main()
