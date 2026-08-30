"""Executable checks for the first durable MSDMD orchestration vertical slice."""
from __future__ import annotations

# === CHECKS ===
# id: check_stack_job_enqueue_idempotent
#   proves: stack_job_enqueue_idempotent
#   call: self::test_enqueue_is_idempotent
#   requires: python3
#   mutates: filesystem, db
#   cleanup: tempdir_teardown
#
# id: check_stack_job_transition_fail_closed
#   proves: stack_job_transition_fail_closed
#   call: self::test_invalid_transition_fails_closed
#   requires: python3
#   mutates: filesystem, db
#   cleanup: tempdir_teardown
#
# id: check_stack_msdmd_refresh_source_pinned
#   proves: stack_msdmd_refresh_source_pinned
#   call: self::test_source_drift_fails_before_generator_execution
#   requires: python3, git
#   mutates: filesystem, db
#   cleanup: tempdir_teardown
#
# id: check_stack_msdmd_refresh_receipted
#   proves: stack_msdmd_refresh_receipted
#   call: self::test_local_refresh_writes_artifact_digest_and_receipt
#   requires: python3
#   mutates: filesystem, db
#   cleanup: tempdir_teardown
#
# id: check_stack_msdmd_refresh_executor_independent_state
#   proves: stack_msdmd_refresh_executor_independent_state
#   call: self::test_local_refresh_writes_artifact_digest_and_receipt
#   requires: python3
#   mutates: filesystem, db
#   cleanup: tempdir_teardown
# === END CHECKS ===

from pathlib import Path
import subprocess
import tempfile
import unittest

from backend.jobs import JobLedger
from backend.msdmd import queue_refresh, run_job


FAKE_COLLECTOR = r'''from pathlib import Path
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--root", required=True)
parser.add_argument("--repo", required=True)
parser.add_argument("--out", required=True)
parser.add_argument("--source-commit", required=True)
args = parser.parse_args()
Path(args.out).write_text(
    f"repo={args.repo}\\nsource_commit={args.source_commit}\\n",
    encoding="utf-8",
)
'''


def _fake_generator(root: Path) -> Path:
    package = root / "msdmd"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "collect.py").write_text(FAKE_COLLECTOR, encoding="utf-8")
    return root


class OrchestratorTests(unittest.TestCase):
    def test_enqueue_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = JobLedger(Path(tmp) / "jobs.sqlite3")
            kwargs = dict(
                kind="msdmd.refresh", target="ucns", source_sha="a" * 40,
                generator_identity="b" * 64, executor="local",
                payload={"root": "/tmp/ucns"},
            )
            first = ledger.enqueue(**kwargs)
            second = ledger.enqueue(**kwargs)
            self.assertEqual(first.id, second.id)
            self.assertEqual(len(ledger.list()), 1)

    def test_invalid_transition_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = JobLedger(Path(tmp) / "jobs.sqlite3")
            job = ledger.enqueue(
                kind="msdmd.refresh", target="ucns", source_sha="a" * 40,
                generator_identity="b" * 64, executor="local",
                payload={"root": "/tmp/ucns"},
            )
            with self.assertRaises(ValueError):
                ledger.succeed(job.id, artifact_path="x", artifact_sha256="c" * 64)
            self.assertEqual(ledger.get(job.id).state, "queued")

    def test_local_refresh_writes_artifact_digest_and_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            target = base / "target"
            target.mkdir()
            generator = _fake_generator(base / "generator")
            ledger = JobLedger(base / "state" / "jobs.sqlite3")
            job = queue_refresh(
                ledger, repo="ucns", root=target, generator_root=generator,
                source_sha="a" * 40,
            )
            result = run_job(ledger, job.id)
            self.assertEqual(result.state, "succeeded")
            self.assertTrue(Path(result.artifact_path or "").is_file())
            self.assertEqual(len(result.artifact_sha256 or ""), 64)
            receipt = base / "state" / "receipts" / f"{job.id}.json"
            self.assertTrue(receipt.is_file())

    def test_source_drift_fails_before_generator_execution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            target = base / "target"
            target.mkdir()
            subprocess.run(["git", "init", "-q", str(target)], check=True)
            subprocess.run(["git", "-C", str(target), "config", "user.email", "test@example.com"], check=True)
            subprocess.run(["git", "-C", str(target), "config", "user.name", "Test"], check=True)
            (target / "x.py").write_text("x = 1\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(target), "add", "x.py"], check=True)
            subprocess.run(["git", "-C", str(target), "commit", "-qm", "one"], check=True)
            first_sha = subprocess.check_output(
                ["git", "-C", str(target), "rev-parse", "HEAD"], text=True
            ).strip()

            generator = _fake_generator(base / "generator")
            ledger = JobLedger(base / "state" / "jobs.sqlite3")
            job = queue_refresh(
                ledger, repo="ucns", root=target, generator_root=generator,
                source_sha=first_sha,
            )

            (target / "x.py").write_text("x = 2\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(target), "add", "x.py"], check=True)
            subprocess.run(["git", "-C", str(target), "commit", "-qm", "two"], check=True)

            result = run_job(ledger, job.id)
            self.assertEqual(result.state, "failed")
            self.assertIn("source checkout moved", result.error or "")
            self.assertFalse((target / "ucns_msdmd.ts").exists())


if __name__ == "__main__":
    unittest.main()
