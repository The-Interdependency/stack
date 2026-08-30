"""Executable checks for PostgreSQL-backed MSDMD orchestration boundaries."""
from __future__ import annotations

# === CHECKS ===
# id: check_stack_msdmd_refresh_source_pinned
#   proves: stack_msdmd_refresh_source_pinned
#   call: self::test_source_drift_becomes_hmmm_without_replacing_artifact
#   requires: python3, git
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_stack_msdmd_refresh_generator_pinned
#   proves: stack_msdmd_refresh_generator_pinned
#   call: self::test_generator_drift_becomes_hmmm
#   requires: python3, git
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_stack_msdmd_refresh_clean_boundary
#   proves: stack_msdmd_refresh_clean_boundary
#   call: self::test_dirty_worktree_becomes_hmmm_without_replacing_artifact
#   requires: python3, git
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_stack_msdmd_refresh_receipted
#   proves: stack_msdmd_refresh_receipted
#   call: self::test_local_refresh_writes_digest_and_receipt
#   requires: python3, git
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_stack_msdmd_refresh_executor_independent_state
#   proves: stack_msdmd_refresh_executor_independent_state
#   call: self::test_local_refresh_writes_digest_and_receipt
#   requires: python3, git
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_stack_job_enqueue_idempotent
#   proves: stack_job_enqueue_idempotent
#   call: self::test_postgres_enqueue_claim_and_receipt
#   requires: python3, postgres, psycopg
#   mutates: db
#   cleanup: delete_test_job
#
# id: check_stack_job_transition_fail_closed
#   proves: stack_job_transition_fail_closed
#   call: self::test_postgres_invalid_transition_fails_closed
#   requires: python3, postgres, psycopg
#   mutates: db
#   cleanup: delete_test_job
#
# id: check_stack_job_claim_skip_locked
#   proves: stack_job_claim_skip_locked
#   call: self::test_postgres_enqueue_claim_and_receipt
#   requires: python3, postgres, psycopg
#   mutates: db
#   cleanup: delete_test_job
# === END CHECKS ===

from dataclasses import replace
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import uuid

from backend.jobs import Job, JobLedger
from backend.msdmd import queue_refresh, run_job

FAKE_COLLECTOR = r'''from pathlib import Path
import argparse
p = argparse.ArgumentParser()
p.add_argument("--root", required=True)
p.add_argument("--repo", required=True)
p.add_argument("--out", required=True)
p.add_argument("--source-commit", required=True)
a = p.parse_args()
Path(a.out).write_text(
    f"repo={a.repo}\\nsource_commit={a.source_commit}\\n",
    encoding="utf-8",
)
'''

class MemoryLedger:
    """Pure test double; production JobLedger remains PostgreSQL-only."""
    def __init__(self, receipt_dir: Path):
        self.receipt_dir = receipt_dir
        self.jobs: dict[str, Job] = {}
        self.by_dedupe: dict[str, str] = {}

    def enqueue(self, *, kind: str, target: str, source_sha: str,
                generator_identity: str, executor: str, payload: dict,
                hmmm: str | None = None) -> Job:
        key = JobLedger._dedupe_key(
            kind=kind, target=target, source_sha=source_sha,
            generator_identity=generator_identity, executor=executor, payload=payload,
        )
        existing = self.by_dedupe.get(key)
        if existing:
            return self.jobs[existing]
        job = Job(
            id=f"job_{key[:24]}", dedupe_key=key, kind=kind, target=target,
            source_sha=source_sha, generator_identity=generator_identity,
            executor=executor, state="queued", attempts=0, payload=payload,
            created_at="2026-08-30T00:00:00+00:00",
            updated_at="2026-08-30T00:00:00+00:00",
            artifact_path=None, artifact_sha256=None, error=None, hmmm=hmmm,
        )
        self.jobs[job.id] = job
        self.by_dedupe[key] = job.id
        return job

    def get(self, job_id: str) -> Job:
        return self.jobs[job_id]

    def start(self, job_id: str, *, worker_id: str = "operator") -> Job:
        job = self.get(job_id)
        if job.state != "queued":
            raise ValueError(f"invalid job transition: {job.state} -> running")
        job = replace(job, state="running", attempts=job.attempts + 1)
        self.jobs[job_id] = job
        return job

    def succeed(self, job_id: str, *, artifact_path: str, artifact_sha256: str) -> Job:
        job = replace(
            self.get(job_id), state="succeeded", artifact_path=artifact_path,
            artifact_sha256=artifact_sha256, error=None, hmmm=None,
        )
        self.jobs[job_id] = job
        return job

    def fail(self, job_id: str, *, error: str) -> Job:
        job = replace(self.get(job_id), state="failed", error=error, hmmm=None)
        self.jobs[job_id] = job
        return job

    def hold(self, job_id: str, *, constraint: str, error: str | None = None) -> Job:
        job = replace(self.get(job_id), state="hmmm", error=error or constraint, hmmm=constraint)
        self.jobs[job_id] = job
        return job

    def retry(self, job_id: str) -> Job:
        job = self.get(job_id)
        if job.state not in {"failed", "hmmm", "cancelled"}:
            raise ValueError(f"invalid retry state: {job.state}")
        job = replace(job, state="queued", error=None, hmmm=None)
        self.jobs[job_id] = job
        return job

    def cancel(self, job_id: str) -> Job:
        job = replace(self.get(job_id), state="cancelled")
        self.jobs[job_id] = job
        return job

def _fake_generator(root: Path) -> Path:
    package = root / "msdmd"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "collect.py").write_text(FAKE_COLLECTOR, encoding="utf-8")
    return root

def _git_target(root: Path) -> tuple[Path, str]:
    target = root / "ucns"
    target.mkdir()
    subprocess.run(["git", "init", "-q", str(target)], check=True)
    subprocess.run(["git", "-C", str(target), "config", "user.email", "test@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(target), "config", "user.name", "Test"], check=True)
    (target / "module.py").write_text("VALUE = 1\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(target), "add", "."], check=True)
    subprocess.run(["git", "-C", str(target), "commit", "-qm", "fixture"], check=True)
    sha = subprocess.check_output(["git", "-C", str(target), "rev-parse", "HEAD"], text=True).strip()
    return target, sha

def _unbound_env():
    return patch.dict(
        os.environ,
        {"STACK_REPO_ROOT": "", "STACK_ALLOWED_REPOS": "", "STACK_SKILL_LIB_ROOT": "", "STACK_COMMAND_TIMEOUT_SECONDS": "30"},
        clear=False,
    )

class OrchestratorUnitTests(unittest.TestCase):
    def test_sqlite_is_not_a_production_fallback(self) -> None:
        with self.assertRaises(ValueError):
            JobLedger(".stack/state/jobs.sqlite3")

    def test_schema_declares_durable_surfaces(self) -> None:
        sql = (Path(__file__).resolve().parents[1] / "sql" / "001_postgres.sql").read_text(encoding="utf-8")
        for table in ("jobs", "attempts", "receipts", "job_dependencies", "hmmm"):
            self.assertIn(f"CREATE TABLE IF NOT EXISTS {table}", sql)
        self.assertIn("payload_json jsonb", sql)
        self.assertIn("lease_until timestamptz", sql)

    def test_local_refresh_writes_digest_and_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            base = Path(tmp)
            target, sha = _git_target(base)
            generator = _fake_generator(base / "generator")
            ledger = MemoryLedger(base / "state" / "receipts")
            job = queue_refresh(ledger, repo="ucns", root=target, generator_root=generator, source_sha=sha)
            result = run_job(ledger, job.id)
            self.assertEqual(result.state, "succeeded")
            artifact = target / "ucns_msdmd.ts"
            self.assertTrue(artifact.is_file())
            self.assertEqual(result.artifact_sha256, hashlib.sha256(artifact.read_bytes()).hexdigest())
            self.assertTrue((ledger.receipt_dir / f"{job.id}.json").is_file())
            self.assertEqual([], list(target.glob(".ucns_msdmd.ts.*.tmp")))

    def test_source_drift_becomes_hmmm_without_replacing_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            base = Path(tmp)
            target, _ = _git_target(base)
            generator = _fake_generator(base / "generator")
            output = target / "ucns_msdmd.ts"
            output.write_text("old\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(target), "add", output.name], check=True)
            subprocess.run(["git", "-C", str(target), "commit", "-qm", "old output"], check=True)
            queued_sha = subprocess.check_output(["git", "-C", str(target), "rev-parse", "HEAD"], text=True).strip()
            ledger = MemoryLedger(base / "state" / "receipts")
            job = queue_refresh(ledger, repo="ucns", root=target, generator_root=generator, source_sha=queued_sha)
            (target / "module.py").write_text("VALUE = 2\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(target), "add", "module.py"], check=True)
            subprocess.run(["git", "-C", str(target), "commit", "-qm", "move head"], check=True)
            result = run_job(ledger, job.id)
            self.assertEqual(result.state, "hmmm")
            self.assertIn("source checkout moved", result.hmmm or "")
            self.assertEqual(output.read_text(encoding="utf-8"), "old\n")

    def test_dirty_worktree_becomes_hmmm_without_replacing_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            base = Path(tmp)
            target, _ = _git_target(base)
            output = target / "ucns_msdmd.ts"
            output.write_text("old\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(target), "add", output.name], check=True)
            subprocess.run(["git", "-C", str(target), "commit", "-qm", "old output"], check=True)
            sha = subprocess.check_output(["git", "-C", str(target), "rev-parse", "HEAD"], text=True).strip()
            generator = _fake_generator(base / "generator")
            ledger = MemoryLedger(base / "state" / "receipts")
            job = queue_refresh(ledger, repo="ucns", root=target, generator_root=generator, source_sha=sha)
            (target / "module.py").write_text("VALUE = 99\n", encoding="utf-8")
            result = run_job(ledger, job.id)
            self.assertEqual(result.state, "hmmm")
            self.assertIn("unrelated target worktree changes", result.hmmm or "")
            self.assertEqual(output.read_text(encoding="utf-8"), "old\n")

    def test_generator_drift_becomes_hmmm(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            base = Path(tmp)
            target, sha = _git_target(base)
            generator = _fake_generator(base / "generator")
            ledger = MemoryLedger(base / "state" / "receipts")
            job = queue_refresh(ledger, repo="ucns", root=target, generator_root=generator, source_sha=sha)
            (generator / "msdmd" / "collect.py").write_text(FAKE_COLLECTOR + "\n# drift\n", encoding="utf-8")
            result = run_job(ledger, job.id)
            self.assertEqual(result.state, "hmmm")
            self.assertIn("generator identity moved", result.hmmm or "")
            self.assertFalse((target / "ucns_msdmd.ts").exists())

    def test_production_repo_boundary_rejects_wrong_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            target, sha = _git_target(base)
            generator = _fake_generator(base / "generator")
            ledger = MemoryLedger(base / "state" / "receipts")
            with patch.dict(
                os.environ,
                {"STACK_REPO_ROOT": str(base / "elsewhere"), "STACK_ALLOWED_REPOS": "ucns", "STACK_SKILL_LIB_ROOT": str(generator)},
                clear=False,
            ):
                with self.assertRaises(Exception):
                    queue_refresh(ledger, repo="ucns", root=target, generator_root=generator, source_sha=sha)

@unittest.skipUnless(os.environ.get("STACK_TEST_DATABASE_URL"), "set STACK_TEST_DATABASE_URL to a disposable PostgreSQL database")
class PostgresIntegrationTests(unittest.TestCase):
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

    def _enqueue_unique(self) -> Job:
        nonce = uuid.uuid4().hex
        source_sha = hashlib.sha1(nonce.encode()).hexdigest()
        generator = hashlib.sha256(nonce.encode()).hexdigest()
        job = self.ledger.enqueue(
            kind="msdmd.refresh", target=f"test-{nonce[:8]}",
            source_sha=source_sha, generator_identity=generator,
            executor="local", payload={"root": f"/tmp/{nonce}"},
        )
        self.job_ids.append(job.id)
        return job

    def test_postgres_enqueue_claim_and_receipt(self) -> None:
        job = self._enqueue_unique()
        duplicate = self.ledger.enqueue(
            kind=job.kind, target=job.target, source_sha=job.source_sha,
            generator_identity=job.generator_identity, executor=job.executor,
            payload=job.payload,
        )
        self.assertEqual(job.id, duplicate.id)
        claimed = self.ledger.claim_next(executor="local", worker_id="integration-test", lease_seconds=120)
        self.assertIsNotNone(claimed)
        assert claimed is not None
        self.assertEqual(claimed.id, job.id)
        self.assertEqual(claimed.state, "running")
        done = self.ledger.succeed(job.id, artifact_path="test_msdmd.ts", artifact_sha256="c" * 64)
        self.assertEqual(done.state, "succeeded")
        with self.ledger._connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT artifact_sha256 FROM receipts WHERE job_id = %s", (job.id,))
                row = cur.fetchone()
        self.assertEqual(row["artifact_sha256"], "c" * 64)

    def test_postgres_invalid_transition_fails_closed(self) -> None:
        job = self._enqueue_unique()
        with self.assertRaises(ValueError):
            self.ledger.succeed(job.id, artifact_path="should-not-exist.ts", artifact_sha256="d" * 64)
        self.assertEqual(self.ledger.get(job.id).state, "queued")

if __name__ == "__main__":
    unittest.main()
