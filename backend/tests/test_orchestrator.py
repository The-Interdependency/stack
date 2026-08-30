"""Executable checks for PostgreSQL-backed fresh-making semantics."""
from __future__ import annotations

# === CHECKS ===
# id: check_stack_freshness_identity_not_time
#   proves: stack_freshness_identity_not_time
#   call: self::test_freshness_key_excludes_runtime_state
#   requires: python3
#   mutates: none
#
# id: check_stack_freshness_hmmm_fail_closed
#   proves: stack_freshness_hmmm_fail_closed
#   call: self::test_unresolved_identity_is_hmmm
#   requires: python3
#   mutates: none
#
# id: check_stack_freshness_affected_closure_minimal
#   proves: stack_freshness_affected_closure_minimal
#   call: self::test_affected_closure_is_minimal_and_ordered
#   requires: python3
#   mutates: none
#
# id: check_stack_fresh_job_identity_executor_independent
#   proves: stack_fresh_job_identity_executor_independent
#   call: self::test_executor_is_not_logical_job_identity
#   requires: python3
#   mutates: none
#
# id: check_stack_msdmd_fresh_exact_identity
#   proves: stack_msdmd_fresh_exact_identity
#   call: self::test_queued_job_refuses_moved_identity
#   requires: python3, git
#   mutates: filesystem
#
# id: check_stack_msdmd_false_green_rejected
#   proves: stack_msdmd_false_green_rejected
#   call: self::test_false_green_nondeterminism_never_accepts
#   requires: python3, git
#   mutates: filesystem
#
# id: check_stack_msdmd_publish_after_verify
#   proves: stack_msdmd_publish_after_verify
#   call: self::test_make_then_noop_is_idempotent
#   requires: python3, git
#   mutates: filesystem
# === END CHECKS ===

from dataclasses import replace
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import uuid

from backend.freshness import (
    SPEC_SCHEMA, SPEC_VERSION, affected_closure, base_report, freshness_key,
)
from backend.jobs import Acceptance, Job, JobLedger, Receipt
from backend.msdmd import build_spec, evaluate, make, queue_make, run_job

FAKE_COLLECTOR = r'''from pathlib import Path
import argparse
p = argparse.ArgumentParser()
p.add_argument("--root", required=True)
p.add_argument("--repo", required=True)
p.add_argument("--out", required=True)
p.add_argument("--source-commit", required=True)
a = p.parse_args()
Path(a.out).write_text(f"repo={a.repo}\nsource_commit={a.source_commit}\n", encoding="utf-8")
'''

NONDETERMINISTIC_COLLECTOR = r'''from pathlib import Path
import argparse, uuid
p = argparse.ArgumentParser()
p.add_argument("--root", required=True)
p.add_argument("--repo", required=True)
p.add_argument("--out", required=True)
p.add_argument("--source-commit", required=True)
a = p.parse_args()
Path(a.out).write_text(str(uuid.uuid4()) + "\n", encoding="utf-8")
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
    subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
    (root / "x.py").write_text("x = 1\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "one"], check=True)
    return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()


def _unbound_env():
    return patch.dict(
        os.environ,
        {
            "STACK_REPO_ROOT": "", "STACK_ALLOWED_REPOS": "",
            "STACK_SKILL_LIB_ROOT": "", "STACK_COMMAND_TIMEOUT_SECONDS": "30",
            "STACK_VERIFY_TIMEOUT_SECONDS": "30", "STACK_LEASE_SECONDS": "120",
        },
        clear=False,
    )


class MemoryLedger:
    """Test double matching production semantics without becoming a production fallback."""

    def __init__(self, receipt_dir: Path):
        self.receipt_dir = receipt_dir
        self.derivations: dict[str, dict] = {}
        self.jobs: dict[str, Job] = {}
        self.attempts: dict[str, list] = {}
        self.acceptance: dict[str, Acceptance] = {}
        self.receipts: dict[str, Receipt] = {}

    def upsert_derivation(self, spec, key):
        self.derivations[spec["target"]] = json.loads(json.dumps(spec))

    def get_derivation(self, target):
        if target not in self.derivations:
            raise KeyError(target)
        return json.loads(json.dumps(self.derivations[target]))

    def list_derivations(self):
        return [self.get_derivation(k) for k in sorted(self.derivations)]

    def enqueue(self, *, kind, target, freshness_key, payload, executor="local"):
        key = JobLedger._dedupe_key(kind=kind, target=target, freshness_key=freshness_key)
        job_id = f"job_{key[:24]}"
        if job_id in self.jobs:
            return self.jobs[job_id]
        job = Job(
            id=job_id, dedupe_key=key, kind=kind, target=target,
            freshness_key=freshness_key, preferred_executor=executor,
            state="queued", attempts=0, payload=dict(payload),
            created_at="2026-08-30T00:00:00+00:00", updated_at="2026-08-30T00:00:00+00:00",
            lease_owner=None, lease_until=None, active_attempt_id=None, receipt_id=None,
            error=None, hmmm=None,
        )
        self.jobs[job_id] = job
        self.attempts[job_id] = []
        return job

    def get(self, job_id):
        return self.jobs[job_id]

    def list(self, *, limit=100, target=None):
        rows = list(self.jobs.values())
        if target:
            rows = [j for j in rows if j.target == target]
        return rows[-limit:]

    def attempts_for(self, job_id):
        return list(self.attempts[job_id])

    def active_job_for_target(self, target):
        active = [j for j in self.jobs.values() if j.target == target and j.state in {"queued","leased","running","verifying"}]
        return active[-1] if active else None

    def acquire_lease(self, job_id, *, worker_id, executor="local", lease_seconds=1800):
        job = self.jobs[job_id]
        if job.state != "queued":
            raise ValueError("job must be queued before lease")
        attempt_id = f"attempt_{job_id}_{job.attempts + 1}"
        job = replace(
            job, state="leased", attempts=job.attempts + 1,
            preferred_executor=executor, lease_owner=worker_id,
            lease_until="2099-01-01T00:00:00+00:00", active_attempt_id=attempt_id,
            error=None, hmmm=None,
        )
        self.jobs[job_id] = job
        self.attempts[job_id].append({"id": attempt_id, "state": "leased", "executor": executor})
        return job

    def start(self, job_id, *, worker_id):
        job = self.jobs[job_id]
        if job.state != "leased" or job.lease_owner != worker_id:
            raise ValueError("start requires lease")
        job = replace(job, state="running")
        self.jobs[job_id] = job
        self.attempts[job_id][-1]["state"] = "running"
        return job

    def heartbeat(self, job_id, *, worker_id, lease_seconds):
        job = self.jobs[job_id]
        if job.lease_owner != worker_id or job.state not in {"leased","running","verifying"}:
            raise ValueError("heartbeat requires lease")
        return job

    def mark_verifying(self, job_id, *, worker_id):
        job = self.jobs[job_id]
        if job.state != "running" or job.lease_owner != worker_id:
            raise ValueError("verify requires lease")
        job = replace(job, state="verifying")
        self.jobs[job_id] = job
        self.attempts[job_id][-1]["state"] = "verifying"
        return job

    def _terminal(self, job_id, state, *, error=None, hmmm=None):
        job = self.jobs[job_id]
        if job.active_attempt_id:
            self.attempts[job_id][-1]["state"] = state
        job = replace(
            job, state=state, error=error, hmmm=hmmm,
            lease_owner=None, lease_until=None, active_attempt_id=None,
        )
        self.jobs[job_id] = job
        return job

    def fail(self, job_id, *, error, hmmm=None):
        return self._terminal(job_id, "failed", error=error, hmmm=hmmm)

    def hold(self, job_id, *, constraint, error=None):
        return self._terminal(job_id, "hmmm", error=error or constraint, hmmm=constraint)

    def cancel(self, job_id):
        return self._terminal(job_id, "cancelled")

    def retry(self, job_id, *, executor=None):
        job = self.jobs[job_id]
        if job.state not in {"succeeded","failed","hmmm","cancelled"}:
            raise ValueError("only terminal jobs retry")
        job = replace(job, state="queued", preferred_executor=executor or job.preferred_executor,
                      error=None, hmmm=None, lease_owner=None, lease_until=None,
                      active_attempt_id=None)
        self.jobs[job_id] = job
        return job

    def accept_success(self, job_id, *, receipt, output_path, output_sha256):
        job = self.jobs[job_id]
        if job.state != "verifying" or not job.active_attempt_id:
            raise ValueError("success requires verifying")
        attempt_id = job.active_attempt_id
        receipt_id = f"receipt_{uuid.uuid4().hex}"
        rec = Receipt(
            id=receipt_id, job_id=job_id, target=job.target,
            freshness_key=job.freshness_key, output_path=output_path,
            output_sha256=output_sha256, receipt=dict(receipt),
            verified_at=datetime.now(timezone.utc).isoformat(),
        )
        self.receipts[receipt_id] = rec
        self.acceptance[job.target] = Acceptance(
            target=job.target, freshness_key=job.freshness_key,
            receipt_id=receipt_id, accepted_at=rec.verified_at,
        )
        self.attempts[job_id][-1]["state"] = "succeeded"
        job = replace(
            job, state="succeeded", receipt_id=receipt_id,
            lease_owner=None, lease_until=None, active_attempt_id=None,
            error=None, hmmm=None,
        )
        self.jobs[job_id] = job
        return job

    def get_acceptance(self, target):
        return self.acceptance.get(target)

    def get_receipt(self, receipt_id):
        return self.receipts[receipt_id]


class FreshMakingTests(unittest.TestCase):
    def _runtime(self, base: Path, *, collector: str = FAKE_COLLECTOR):
        target = base / "target"
        _git_repo(target)
        generator = _fake_generator(base / "generator", collector)
        ledger = MemoryLedger(base / "receipts")
        spec = build_spec(repo="ucns", root=target, generator_root=generator)
        ledger.upsert_derivation(spec, freshness_key(spec))
        return target, generator, ledger, spec

    def test_freshness_key_excludes_runtime_state(self):
        spec = {
            "schema": SPEC_SCHEMA, "version": SPEC_VERSION, "target": "x", "kind": "test",
            "inputs": [{"name":"i","identity":"sha256:" + "a"*64}],
            "generator": {"identity":"sha256:" + "b"*64, "command":"gen"},
            "outputs": [{"path":"x"}],
            "verifier": {"identity":"builtin:v1", "command":"verify"},
            "depends_on": [], "runtime": {"executor":"local", "timestamp":"now"},
        }
        other = json.loads(json.dumps(spec))
        other["runtime"] = {"executor":"github-actions", "timestamp":"later"}
        self.assertEqual(freshness_key(spec), freshness_key(other))

    def test_unresolved_identity_is_hmmm(self):
        class L:
            def get_acceptance(self, target): return None
            def active_job_for_target(self, target): return None
        spec = {
            "schema": SPEC_SCHEMA, "version": SPEC_VERSION, "target":"x", "kind":"test",
            "inputs":[{"name":"source","identity":"hmmm"}],
            "generator":{"identity":"builtin:g","command":"g"}, "outputs":[{"path":"x"}],
            "verifier":{"identity":"builtin:v","command":"v"}, "depends_on":[],
        }
        self.assertEqual(base_report(L(), spec).state, "hmmm")

    def test_affected_closure_is_minimal_and_ordered(self):
        def s(target, deps):
            return {"schema":SPEC_SCHEMA,"version":SPEC_VERSION,"target":target,"kind":"t",
                    "inputs":[{"name":"i","identity":"builtin:i"}],
                    "generator":{"identity":"builtin:g","command":"g"},
                    "outputs":[{"path":target}],"verifier":{"identity":"builtin:v","command":"v"},
                    "depends_on":deps}
        self.assertEqual(affected_closure([s("a",[]),s("b",["a"]),s("c",["b"]),s("d",[])],["a"]), ["a","b","c"])

    def test_make_then_noop_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            _, _, ledger, spec = self._runtime(Path(tmp))
            job, report = make(ledger, spec["target"])
            self.assertIsNotNone(job)
            self.assertEqual(report.state, "fresh")
            second, report2 = make(ledger, spec["target"])
            self.assertIsNone(second)
            self.assertEqual(report2.state, "fresh")
            self.assertEqual(len(ledger.jobs), 1)

    def test_executor_is_not_logical_job_identity(self):
        ledger = MemoryLedger(Path("/tmp/receipts"))
        a = ledger.enqueue(kind="fresh.make", target="x", freshness_key="a"*64, payload={}, executor="local")
        b = ledger.enqueue(kind="fresh.make", target="x", freshness_key="a"*64, payload={}, executor="github-actions")
        self.assertEqual(a.id, b.id)

    def test_source_change_moves_key_and_rebuilds(self):
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            target, _, ledger, spec = self._runtime(Path(tmp))
            _, first = make(ledger, spec["target"])
            old = first.desired_freshness_key
            (target / "x.py").write_text("x = 2\n", encoding="utf-8")
            subprocess.run(["git","-C",str(target),"add","x.py"], check=True)
            subprocess.run(["git","-C",str(target),"commit","-qm","two"], check=True)
            changed = evaluate(ledger, spec["target"])
            self.assertEqual(changed.diagnosis, "identity-changed")
            self.assertNotEqual(changed.desired_freshness_key, old)
            _, final = make(ledger, spec["target"])
            self.assertEqual(final.state, "fresh")
            self.assertEqual(len(ledger.jobs), 2)

    def test_generator_change_invalidates(self):
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            _, generator, ledger, spec = self._runtime(Path(tmp))
            _, first = make(ledger, spec["target"])
            old = first.desired_freshness_key
            p = generator / "msdmd" / "collect.py"
            p.write_text(p.read_text() + "\n# change\n")
            changed = evaluate(ledger, spec["target"])
            self.assertEqual(changed.state, "making-fresh")
            self.assertNotEqual(changed.desired_freshness_key, old)

    def test_tamper_repairs_same_key_as_second_attempt(self):
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            target, _, ledger, spec = self._runtime(Path(tmp))
            job, first = make(ledger, spec["target"])
            self.assertEqual(first.state, "fresh")
            (target / "ucns_msdmd.ts").write_text("tampered\n", encoding="utf-8")
            self.assertEqual(evaluate(ledger, spec["target"]).diagnosis, "output-tampered")
            repaired_job, repaired = make(ledger, spec["target"])
            self.assertEqual(repaired.state, "fresh")
            self.assertEqual(repaired_job.id, job.id)
            self.assertEqual(repaired_job.attempts, 2)

    def test_false_green_nondeterminism_never_accepts(self):
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            target, _, ledger, spec = self._runtime(Path(tmp), collector=NONDETERMINISTIC_COLLECTOR)
            job, _ = queue_make(ledger, spec["target"])
            self.assertIsNotNone(job)
            result = run_job(ledger, job.id)
            self.assertEqual(result.state, "failed")
            self.assertIn("differ", result.error or "")
            self.assertFalse((target / "ucns_msdmd.ts").exists())
            self.assertIsNone(ledger.get_acceptance(spec["target"]))

    def test_queued_job_refuses_moved_identity(self):
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            target, _, ledger, spec = self._runtime(Path(tmp))
            job, _ = queue_make(ledger, spec["target"])
            self.assertIsNotNone(job)
            (target / "x.py").write_text("x = 3\n", encoding="utf-8")
            subprocess.run(["git","-C",str(target),"add","x.py"], check=True)
            subprocess.run(["git","-C",str(target),"commit","-qm","move"], check=True)
            result = run_job(ledger, job.id)
            self.assertEqual(result.state, "failed")
            self.assertIn("freshness key moved", result.error or "")

    def test_production_repo_boundary_rejects_wrong_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            target = base / "target"
            _git_repo(target)
            generator = _fake_generator(base / "generator")
            with patch.dict(os.environ, {"STACK_REPO_ROOT": str(base / "elsewhere"), "STACK_ALLOWED_REPOS":"ucns", "STACK_SKILL_LIB_ROOT":str(generator)}, clear=False):
                with self.assertRaises(Exception):
                    build_spec(repo="ucns", root=target, generator_root=generator)

    def test_sql_schema_declares_single_fresh_state_authority(self):
        sql = (Path(__file__).resolve().parents[1] / "sql" / "001_postgres.sql").read_text()
        for table in ("derivations","jobs","attempts","receipts","target_acceptance","hmmm"):
            self.assertIn(f"CREATE TABLE IF NOT EXISTS {table}", sql)
        self.assertIn("FOR UPDATE", Path(__file__).resolve().parents[1].joinpath("jobs.py").read_text())
        self.assertNotIn("sqlite", Path(__file__).resolve().parents[1].joinpath("jobs.py").read_text().lower())


@unittest.skipUnless(os.environ.get("STACK_TEST_DATABASE_URL"), "set STACK_TEST_DATABASE_URL to a disposable PostgreSQL database")
class PostgresIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import psycopg  # noqa: F401
        except ImportError as exc:
            raise unittest.SkipTest("psycopg is not installed") from exc
        cls.ledger = JobLedger(os.environ["STACK_TEST_DATABASE_URL"], receipt_dir=Path(tempfile.gettempdir())/"stack-fresh-test-receipts")
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
                    cur.execute("DELETE FROM derivations WHERE target=%s", (target,))
            conn.commit()

    def test_executor_independent_enqueue_and_skip_locked_claim(self):
        target = f"test:{uuid.uuid4().hex[:8]}"
        self.targets.append(target)
        first = self.ledger.enqueue(kind="fresh.make", target=target, freshness_key="a"*64, payload={}, executor="local")
        second = self.ledger.enqueue(kind="fresh.make", target=target, freshness_key="a"*64, payload={}, executor="github-actions")
        self.assertEqual(first.id, second.id)
        claimed = self.ledger.claim_next(executor="local", worker_id="integration", lease_seconds=120)
        self.assertIsNotNone(claimed)
        self.assertEqual(claimed.id, first.id)
        self.assertEqual(claimed.state, "leased")


if __name__ == "__main__":
    unittest.main()
