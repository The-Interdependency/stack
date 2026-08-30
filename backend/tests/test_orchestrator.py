"""Executable checks for stack fresh-making and MSDMD regeneration."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
import subprocess
import tempfile
import unittest

from backend.freshness import SpecStore
from backend.jobs import JobLedger
from backend.msdmd import build_spec, evaluate, make, queue_make, run_job


FAKE_COLLECTOR = r'''from pathlib import Path
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--root", required=True)
parser.add_argument("--repo", required=True)
parser.add_argument("--out", required=True)
parser.add_argument("--source-commit", required=True)
args = parser.parse_args()
Path(args.out).write_text(
    f"repo={args.repo}\nsource_commit={args.source_commit}\n",
    encoding="utf-8",
)
'''

NONDETERMINISTIC_COLLECTOR = r'''from pathlib import Path
import argparse, uuid
parser = argparse.ArgumentParser()
parser.add_argument("--root", required=True)
parser.add_argument("--repo", required=True)
parser.add_argument("--out", required=True)
parser.add_argument("--source-commit", required=True)
args = parser.parse_args()
Path(args.out).write_text(str(uuid.uuid4()) + "\n", encoding="utf-8")
'''


def _fake_generator(root: Path, content: str = FAKE_COLLECTOR) -> Path:
    package = root / "msdmd"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "collect.py").write_text(content, encoding="utf-8")
    return root


def _git_repo(root: Path) -> str:
    root.mkdir()
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
    (root / "x.py").write_text("x = 1\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "x.py"], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "one"], check=True)
    return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()


class OrchestratorTests(unittest.TestCase):
    def _runtime(self, base: Path, *, collector: str = FAKE_COLLECTOR):
        target = base / "target"
        _git_repo(target)
        generator = _fake_generator(base / "generator", collector)
        ledger = JobLedger(base / "state" / "jobs.sqlite3")
        store = SpecStore(base / "state")
        spec = build_spec(repo="ucns", root=target, generator_root=generator)
        store.put(spec)
        return target, generator, ledger, store, spec

    def test_make_then_noop_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _, _, ledger, store, spec = self._runtime(Path(tmp))
            job, report = make(ledger, store, spec["target"])
            self.assertIsNotNone(job)
            self.assertEqual(report.state, "fresh")
            attempts = job.attempts if job else 0
            second_job, second_report = make(ledger, store, spec["target"])
            self.assertIsNone(second_job)
            self.assertEqual(second_report.state, "fresh")
            self.assertEqual(len(ledger.list()), 1)
            self.assertEqual(ledger.list()[0].attempts, attempts)

    def test_executor_not_part_of_job_identity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _, _, ledger, store, spec = self._runtime(Path(tmp))
            key = __import__("backend.freshness", fromlist=["freshness_key"]).freshness_key(spec)
            first = ledger.enqueue(kind="fresh.make", target=spec["target"], freshness_key=key,
                                   payload={"spec_target": spec["target"]}, executor="local")
            second = ledger.enqueue(kind="fresh.make", target=spec["target"], freshness_key=key,
                                    payload={"spec_target": spec["target"]}, executor="other")
            self.assertEqual(first.id, second.id)
            self.assertEqual(len(ledger.list()), 1)

    def test_source_change_moves_desired_key_and_rebuilds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target, _, ledger, store, spec = self._runtime(Path(tmp))
            _, first_report = make(ledger, store, spec["target"])
            self.assertEqual(first_report.state, "fresh")
            old_key = first_report.desired_freshness_key
            (target / "x.py").write_text("x = 2\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(target), "add", "x.py"], check=True)
            subprocess.run(["git", "-C", str(target), "commit", "-qm", "two"], check=True)
            changed = evaluate(ledger, store, spec["target"])
            self.assertEqual(changed.state, "making-fresh")
            self.assertEqual(changed.diagnosis, "identity-changed")
            self.assertNotEqual(changed.desired_freshness_key, old_key)
            second, final = make(ledger, store, spec["target"])
            self.assertIsNotNone(second)
            self.assertEqual(final.state, "fresh")
            self.assertEqual(len(ledger.list()), 2)

    def test_generator_change_invalidates_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _, generator, ledger, store, spec = self._runtime(Path(tmp))
            _, first = make(ledger, store, spec["target"])
            old_key = first.desired_freshness_key
            collector = generator / "msdmd" / "collect.py"
            collector.write_text(collector.read_text(encoding="utf-8") + "\n# changed\n", encoding="utf-8")
            changed = evaluate(ledger, store, spec["target"])
            self.assertEqual(changed.state, "making-fresh")
            self.assertNotEqual(changed.desired_freshness_key, old_key)

    def test_tamper_is_not_fresh(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target, _, ledger, store, spec = self._runtime(Path(tmp))
            _, first = make(ledger, store, spec["target"])
            self.assertEqual(first.state, "fresh")
            (target / "ucns_msdmd.ts").write_text("tampered\n", encoding="utf-8")
            report = evaluate(ledger, store, spec["target"])
            self.assertEqual(report.state, "making-fresh")
            self.assertEqual(report.diagnosis, "output-tampered")
            repaired_job, repaired = make(ledger, store, spec["target"])
            self.assertIsNotNone(repaired_job)
            self.assertEqual(repaired.state, "fresh")
            self.assertEqual(len(ledger.list()), 1)
            self.assertEqual(ledger.list()[0].attempts, 2)

    def test_false_green_nondeterminism_fails_before_publish(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target, _, ledger, store, spec = self._runtime(
                Path(tmp), collector=NONDETERMINISTIC_COLLECTOR
            )
            job, _ = queue_make(ledger, store, spec["target"])
            self.assertIsNotNone(job)
            result = run_job(ledger, store, job.id if job else "")
            self.assertEqual(result.state, "failed")
            self.assertIn("differ", result.error or "")
            self.assertFalse((target / "ucns_msdmd.ts").exists())
            self.assertIsNone(ledger.get_acceptance(spec["target"]))

    def test_expired_lease_recovers_without_losing_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _, _, ledger, store, spec = self._runtime(Path(tmp))
            job, _ = queue_make(ledger, store, spec["target"])
            assert job is not None
            leased = ledger.acquire_lease(job.id, owner="dead", ttl_seconds=1)
            self.assertEqual(leased.state, "leased")
            recovered = ledger.recover_expired_leases(
                now=datetime.now(timezone.utc) + timedelta(seconds=10)
            )
            self.assertEqual([item.id for item in recovered], [job.id])
            self.assertEqual(ledger.get(job.id).state, "queued")
            attempts = ledger.attempts_for(job.id)
            self.assertEqual(len(attempts), 1)
            self.assertEqual(attempts[0].state, "failed")
            self.assertEqual(attempts[0].error, "lease expired")

    def test_queued_job_refuses_if_identity_moves_before_execution(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target, _, ledger, store, spec = self._runtime(Path(tmp))
            job, _ = queue_make(ledger, store, spec["target"])
            assert job is not None
            (target / "x.py").write_text("x = 3\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(target), "add", "x.py"], check=True)
            subprocess.run(["git", "-C", str(target), "commit", "-qm", "move"], check=True)
            result = run_job(ledger, store, job.id)
            self.assertEqual(result.state, "failed")
            self.assertIn("freshness key moved", result.error or "")
            self.assertFalse((target / "ucns_msdmd.ts").exists())

    def test_affected_closure_is_minimal_and_ordered(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = SpecStore(Path(tmp) / "state")
            def spec(target: str, deps: list[str]):
                return {
                    "schema": "the-interdependency.fresh-making-spec", "version": "1.0.0",
                    "target": target, "kind": "test", "inputs": [{"name":"x","identity":"sha256:" + "a"*64}],
                    "generator": {"identity":"sha256:" + "b"*64, "command":"x"},
                    "outputs": [{"path": target}],
                    "verifier": {"identity":"builtin:test", "command":"x"},
                    "depends_on": deps, "runtime": {},
                }
            for item in (spec("a", []), spec("b", ["a"]), spec("c", ["b"]), spec("d", [])):
                store.put(item)
            self.assertEqual(store.affected_closure(["a"]), ["a", "b", "c"])

    def test_receipt_replay_survives_new_store_and_ledger_instances(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            _, _, ledger, store, spec = self._runtime(base)
            _, first = make(ledger, store, spec["target"])
            self.assertEqual(first.state, "fresh")
            new_ledger = JobLedger(base / "state" / "jobs.sqlite3")
            new_store = SpecStore(base / "state")
            replay = evaluate(new_ledger, new_store, spec["target"])
            self.assertEqual(replay.state, "fresh")
            receipt = json.loads(Path(replay.receipt_path or "").read_text(encoding="utf-8"))
            self.assertEqual(receipt["freshness_key_sha256"], replay.desired_freshness_key)


if __name__ == "__main__":
    unittest.main()
