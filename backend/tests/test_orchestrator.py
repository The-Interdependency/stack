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
#
# id: check_stack_msdmd_target_cannot_shadow_collector
#   proves: stack_msdmd_target_cannot_shadow_collector
#   call: self::test_target_msdmd_package_cannot_shadow_the_pinned_collector
#   requires: python3, git
#   mutates: filesystem
#
# id: check_stack_msdmd_identity_observed_where_executed
#   proves: stack_msdmd_identity_observed_where_executed
#   call: self::test_shell_queue_never_keys_the_generator_and_worker_owns_identity
#   requires: python3, git
#   mutates: filesystem
# === END CHECKS ===

from dataclasses import replace
from datetime import datetime, timezone
import hashlib
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
from backend.msdmd import (
    WORKER_PENDING, _clean_stale_siblings, build_spec, component_difference, evaluate, make, queue_make,
    register_spec, run_job,
)

IDENTITY_PRELUDE = r'''import hashlib, sys
from pathlib import Path as _P
if "--print-generator-identity" in sys.argv:
    # Mirrors the real collector's flag: identity of this generator's own bytes.
    print("sha256:" + hashlib.sha256(_P(__file__).read_bytes()).hexdigest())
    raise SystemExit(0)
'''

FAKE_COLLECTOR = IDENTITY_PRELUDE + r'''from pathlib import Path
import argparse
p = argparse.ArgumentParser()
p.add_argument("--root", required=True)
p.add_argument("--repo", required=True)
p.add_argument("--out", required=True)
p.add_argument("--source-commit", required=True)
a = p.parse_args()
Path(a.out).write_text(f"repo={a.repo}\nsource_commit={a.source_commit}\n", encoding="utf-8")
'''

# Identity depends on the environment the probe runs in (FAKE_NODE stands in
# for PATH/Node/venv differences between an operator shell and the worker).
ENV_COLLECTOR = r'''import hashlib, json, os, sys
from pathlib import Path as _P
_components = {"source_sha256": hashlib.sha256(_P(__file__).read_bytes()).hexdigest(),
               "node": os.environ.get("FAKE_NODE", "absent")}
if "--print-generator-identity" in sys.argv:
    if "--json" in sys.argv:
        print(json.dumps(_components, sort_keys=True))
    else:
        print("sha256:" + hashlib.sha256(json.dumps(_components, sort_keys=True).encode()).hexdigest())
    raise SystemExit(0)
''' + FAKE_COLLECTOR.replace(IDENTITY_PRELUDE, "")

NONDETERMINISTIC_COLLECTOR = IDENTITY_PRELUDE + r'''from pathlib import Path
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

    def test_generator_identity_comes_from_the_collector_and_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            target, generator, ledger, spec = self._runtime(Path(tmp))
            collector = generator / "msdmd" / "collect.py"
            expected = hashlib.sha256(collector.read_bytes()).hexdigest()
            self.assertEqual(f"sha256:{expected}", spec["generator"]["identity"])
            # A collector that cannot report --print-generator-identity is never trusted.
            collector.write_text(FAKE_COLLECTOR.replace(IDENTITY_PRELUDE, ""), encoding="utf-8")
            with self.assertRaises(ValueError):
                build_spec(repo="ucns", root=target, generator_root=generator)
            report = evaluate(ledger, spec["target"])
            self.assertNotEqual(report.state, "fresh")
            self.assertEqual("hmmm", ledger.get_derivation(spec["target"])["generator"]["identity"])

    def test_collector_refusals_fail_closed_into_the_ledger(self):
        # The real collector writes nothing on exit 3/4/5; this one even leaves a
        # file behind to prove the refusal alone keeps it unpublished.
        for code, name in ((3, "reader-runtime-missing"), (4, "schema-helper-outdated"),
                           (5, "git-visibility-unavailable")):
            with self.subTest(code=code), tempfile.TemporaryDirectory() as tmp, _unbound_env():
                target, generator, ledger, spec = self._runtime(Path(tmp))
                first, _ = make(ledger, spec["target"])
                self.assertEqual(first.state, "succeeded")
                accepted = ledger.get_acceptance(spec["target"])
                published = (target / "ucns_msdmd.ts").read_bytes()
                refusing = FAKE_COLLECTOR + (
                    "import sys\n"
                    "print('msdmd: ERROR: refused for test', file=sys.stderr)\n"
                    f"raise SystemExit({code})\n"
                )
                (generator / "msdmd" / "collect.py").write_text(refusing, encoding="utf-8")
                job, _ = queue_make(ledger, spec["target"])
                self.assertIsNotNone(job)
                result = run_job(ledger, job.id)
                self.assertEqual(result.state, "failed")
                self.assertIn(f"exit {code}, {name}", result.error or "")
                self.assertIn("refused for test", result.error or "")
                self.assertIn(f"msdmd exit {code} ({name})", result.hmmm or "")
                self.assertEqual(published, (target / "ucns_msdmd.ts").read_bytes())
                self.assertEqual(accepted, ledger.get_acceptance(spec["target"]))
                self.assertEqual([], sorted(p.name for p in target.iterdir() if p.name.startswith(".ucns_msdmd.ts.")))
                self.assertNotEqual("fresh", evaluate(ledger, spec["target"]).state)

    def test_target_msdmd_package_cannot_shadow_the_pinned_collector(self):
        # Review P1 on stack #78: with cwd at the target, `python -m` imported the
        # target's own msdmd/collect.py (and yaml.py) ahead of PYTHONPATH and
        # published its forged artifact as fresh.
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            base = Path(tmp)
            target, _, ledger, spec = self._runtime(base)
            marker = base / "target-code-ran"
            (target / "msdmd").mkdir()
            (target / "msdmd" / "__init__.py").write_text("", encoding="utf-8")
            (target / "msdmd" / "collect.py").write_text(
                "import pathlib, sys\n"
                f"pathlib.Path({str(marker)!r}).write_text('msdmd shadow ran')\n"
                "if '--print-generator-identity' in sys.argv:\n"
                "    print('sha256:' + 'f' * 64); raise SystemExit(0)\n"
                "out = sys.argv[sys.argv.index('--out') + 1]\n"
                "pathlib.Path(out).write_text('// forged by the inspected repository\\n')\n",
                encoding="utf-8")
            (target / "yaml.py").write_text(
                f"import pathlib\npathlib.Path({str(marker)!r}).write_text('yaml shadow ran')\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(target), "add", "-A"], check=True)
            subprocess.run(["git", "-C", str(target), "commit", "-qm", "shadow"], check=True)
            job, report = make(ledger, spec["target"])
            self.assertEqual("succeeded", job.state, job.error)
            self.assertEqual("fresh", report.state)
            self.assertFalse(marker.exists(), marker.read_text() if marker.exists() else "")
            published = (target / "ucns_msdmd.ts").read_text(encoding="utf-8")
            self.assertNotIn("forged", published)
            self.assertIn("repo=ucns", published)
            self.assertNotEqual("sha256:" + "f" * 64, ledger.get_derivation(spec["target"])["generator"]["identity"])

    def test_unmapped_exits_and_signals_name_their_status(self):
        for tail, status, has_hmmm in (
            ("raise SystemExit(7)\n", "exit 7", False),
            ("import os, signal\nos.kill(os.getpid(), signal.SIGKILL)\n", "killed by SIGKILL", True),
            ("import os, signal\nos.kill(os.getpid(), signal.SIGSEGV)\n", "killed by SIGSEGV", True),
        ):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as tmp, _unbound_env():
                target, generator, ledger, spec = self._runtime(Path(tmp))
                (generator / "msdmd" / "collect.py").write_text(FAKE_COLLECTOR + tail, encoding="utf-8")
                job, _ = queue_make(ledger, spec["target"])
                result = run_job(ledger, job.id)
                self.assertEqual("failed", result.state)
                self.assertIn(f"executor failed ({status})", result.error or "")
                self.assertEqual(has_hmmm, bool(result.hmmm), result.hmmm)
                self.assertFalse((target / "ucns_msdmd.ts").exists())
                self.assertEqual([], [p.name for p in target.iterdir() if p.name.startswith(".ucns_msdmd.ts.")])

    def test_spawn_oserror_is_recorded_not_raised(self):
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            target, _, ledger, spec = self._runtime(Path(tmp))
            first, _ = make(ledger, spec["target"])
            published = (target / "ucns_msdmd.ts").read_bytes()
            (target / "ucns_msdmd.ts").write_text("tampered\n", encoding="utf-8")
            job, _ = queue_make(ledger, spec["target"])
            job = ledger.retry(job.id)  # same key as the accepted run: a repair attempt
            real = subprocess.run

            def no_memory(cmd, *args, **kwargs):
                if "--out" in cmd:
                    raise OSError(12, "Cannot allocate memory")
                return real(cmd, *args, **kwargs)

            with patch("backend.msdmd.subprocess.run", side_effect=no_memory):
                result = run_job(ledger, job.id)
                self.assertEqual("failed", result.state)
                self.assertIn("executor could not start: OSError", result.error or "")
                self.assertIn("ENOMEM", result.hmmm or "")
                report = evaluate(ledger, spec["target"])
                self.assertNotEqual("fresh", report.state)
            self.assertEqual(b"tampered\n", (target / "ucns_msdmd.ts").read_bytes())
            self.assertNotEqual(published, b"tampered\n")
            self.assertEqual([], [p.name for p in target.iterdir() if p.name.startswith(".ucns_msdmd.ts.")])

            def identity_no_memory(cmd, *args, **kwargs):
                if "--print-generator-identity" in cmd:
                    raise OSError(12, "Cannot allocate memory")
                return real(cmd, *args, **kwargs)

            with patch("backend.msdmd.subprocess.run", side_effect=identity_no_memory):
                report = evaluate(ledger, spec["target"])
            self.assertEqual("hmmm", ledger.get_derivation(spec["target"])["generator"]["identity"])
            self.assertNotEqual("fresh", report.state)

    def test_stale_own_siblings_older_than_the_lease_are_cleaned(self):
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            target, _, ledger, spec = self._runtime(Path(tmp))
            old = os.path.getmtime(target / "x.py") - 3600
            stale = [target / ".ucns_msdmd.ts.dead1234.candidate", target / ".ucns_msdmd.ts.dead5678.verify",
                     target / ".ucns_msdmd.ts.fresh-status-verify", target / ".ucns_msdmd.ts.job_gone.accepted-backup"]
            for path in stale:
                path.write_text("junk from a crashed worker\n", encoding="utf-8")
                os.utime(path, (old, old))
            job, report = make(ledger, spec["target"])
            self.assertEqual("succeeded", job.state, job.error)
            self.assertEqual("fresh", report.state)
            self.assertEqual([], [p.name for p in target.iterdir() if p.name.startswith(".ucns_msdmd.ts.")])

    def test_stale_collector_temp_files_are_cleaned_but_young_or_lookalike_ones_are_not(self):
        # Review P3: a collector killed mid-write leaves its mkstemp(".msdmd-") file in the target root.
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            target, _, ledger, spec = self._runtime(Path(tmp))
            old = os.path.getmtime(target / "x.py") - 3600
            stale = target / ".msdmd-ab12_z9q"
            stale.write_text("partial collector output\n", encoding="utf-8")
            os.utime(stale, (old, old))
            with patch("sys.stderr"):
                job, report = make(ledger, spec["target"])
            self.assertEqual("succeeded", job.state, job.error)
            self.assertFalse(stale.exists())
            for name in (".msdmd-young123", ".msdmd-toolongname1", ".msdmd-UPPER123"):
                path = target / name
                path.write_text("x\n", encoding="utf-8")
                if name != ".msdmd-young123":
                    os.utime(path, (old, old))
            (target / "x.py").write_text("x = 9\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(target), "commit", "-qam", "next"], check=True)
            job, _ = queue_make(ledger, spec["target"])
            result = run_job(ledger, job.id)
            self.assertEqual("hmmm", result.state)
            for name in (".msdmd-young123", ".msdmd-toolongname1", ".msdmd-UPPER123"):
                self.assertTrue((target / name).exists(), name)

    def test_concurrent_status_rerender_does_not_hold_the_worker(self):
        # Review P3: `fresh status` writes .<out>.fresh-status-verify while the
        # worker checks the worktree; that sibling is ours, not a dirty change.
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            target, _, ledger, spec = self._runtime(Path(tmp))
            in_flight = target / ".ucns_msdmd.ts.fresh-status-verify"
            in_flight.write_text("status rerender in progress\n", encoding="utf-8")
            job, _ = queue_make(ledger, spec["target"])
            result = run_job(ledger, job.id)
            self.assertEqual("succeeded", result.state, result.error)
            self.assertTrue(in_flight.exists())  # young: left for the status run to remove

    def test_young_or_foreign_siblings_are_not_touched(self):
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            target, _, ledger, spec = self._runtime(Path(tmp))
            young = target / ".ucns_msdmd.ts.live1234.candidate"
            young.write_text("another worker is still writing\n", encoding="utf-8")
            foreign = target / ".ucns_msdmd.ts.notes"
            foreign.write_text("not ours\n", encoding="utf-8")
            old = os.path.getmtime(target / "x.py") - 3600
            os.utime(foreign, (old, old))
            job, _ = queue_make(ledger, spec["target"])
            result = run_job(ledger, job.id)
            self.assertEqual("hmmm", result.state)
            self.assertIn("unrelated target worktree changes", result.error or "")
            self.assertTrue(young.exists())
            self.assertTrue(foreign.exists())

    def test_stale_rollback_holding_accepted_bytes_is_restored(self):
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            target, _, ledger, spec = self._runtime(Path(tmp))
            make(ledger, spec["target"])
            output = target / "ucns_msdmd.ts"
            accepted = output.read_bytes()
            # Crash between publish and SQL acceptance: unaccepted bytes are live.
            backup = target / ".ucns_msdmd.ts.job_crashed.accepted-backup"
            backup.write_bytes(accepted)
            output.write_text("published but never accepted\n", encoding="utf-8")
            old = os.path.getmtime(target / "x.py") - 3600
            os.utime(backup, (old, old))
            with patch("sys.stderr"):
                cleaned = _clean_stale_siblings(ledger, ledger.get_derivation(spec["target"]), 120)
            self.assertEqual(["restored .ucns_msdmd.ts.job_crashed.accepted-backup"], cleaned)
            self.assertEqual(accepted, output.read_bytes())
            self.assertFalse(backup.exists())

    def test_failed_git_status_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            target, _, ledger, spec = self._runtime(Path(tmp))
            job, _ = queue_make(ledger, spec["target"])
            real = subprocess.run

            def broken_status(cmd, *args, **kwargs):
                if "status" in cmd:
                    return subprocess.CompletedProcess(cmd, 128, "", "fatal: detected dubious ownership")
                return real(cmd, *args, **kwargs)

            with patch("backend.msdmd.subprocess.run", side_effect=broken_status):
                result = run_job(ledger, job.id)
            self.assertEqual("hmmm", result.state)
            self.assertIn("git status failed", result.error or "")
            self.assertIn("dubious ownership", result.error or "")
            self.assertFalse((target / "ucns_msdmd.ts").exists())

    def test_shell_queue_never_keys_the_generator_and_worker_owns_identity(self):
        # Review P2 on stack #78: the VM_SETUP queue-from-shell flow keyed jobs
        # with the operator shell's identity, then the worker re-keyed (and
        # status from the shell re-keyed back).
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            base = Path(tmp)
            target = base / "target"
            _git_repo(target)
            generator = _fake_generator(base / "generator", ENV_COLLECTOR)
            ledger = MemoryLedger(base / "receipts")
            with patch.dict(os.environ, {"FAKE_NODE": "v20-shell"}), \
                 patch("backend.msdmd.generator_identity", side_effect=AssertionError("shell probed identity")):
                spec = build_spec(repo="ucns", root=target, generator_root=generator, observe_generator=False)
                self.assertEqual(WORKER_PENDING, spec["generator"]["identity"])
                register_spec(ledger, spec)
                queued, _ = queue_make(ledger, spec["target"], observe_generator=False)
            self.assertEqual("queued", queued.state)
            with patch.dict(os.environ, {"FAKE_NODE": "v24-worker"}), patch("sys.stderr"):
                superseded = run_job(ledger, queued.id)
                self.assertEqual("failed", superseded.state)
                self.assertIn("superseded", superseded.error or "")
                replacement = ledger.active_job_for_target(spec["target"])
                self.assertIsNotNone(replacement)
                self.assertNotEqual(queued.id, replacement.id)
                done = run_job(ledger, replacement.id)
                self.assertEqual("succeeded", done.state, done.error)
                worker_spec = ledger.get_derivation(spec["target"])
                self.assertEqual("v24-worker", worker_spec["runtime"]["generator_components"]["node"])
                self.assertEqual("fresh", evaluate(ledger, spec["target"]).state)
            with patch.dict(os.environ, {"FAKE_NODE": "v20-shell"}):
                status = evaluate(ledger, spec["target"], observe_generator=False)
                self.assertEqual(worker_spec, ledger.get_derivation(spec["target"]))  # no re-key
                self.assertEqual("verifier-unavailable", status.diagnosis)
                self.assertIn("node: v24-worker -> v20-shell", " ".join(status.hmmm))
                again = build_spec(repo="ucns", root=target, generator_root=generator,
                                   observe_generator=False, recorded=ledger.get_derivation(spec["target"]))
                self.assertEqual(worker_spec["generator"], again["generator"])
                self.assertEqual(freshness_key(worker_spec), freshness_key(again))
            self.assertEqual(2, len(ledger.jobs))

    def test_stackctl_queue_only_and_status_do_not_probe_the_generator(self):
        from contextlib import redirect_stdout
        import io
        from frontend.cli import stackctl
        with tempfile.TemporaryDirectory() as tmp, _unbound_env():
            base = Path(tmp)
            target = base / "target"
            _git_repo(target)
            generator = _fake_generator(base / "generator", ENV_COLLECTOR)
            ledger = MemoryLedger(base / "receipts")
            with patch.object(stackctl, "_ledger", return_value=ledger), \
                 patch("backend.msdmd.generator_identity", side_effect=AssertionError("shell probed identity")), \
                 redirect_stdout(io.StringIO()) as printed:
                code = stackctl.main(["fresh", "make-msdmd", "ucns", "--root", str(target),
                                      "--generator-root", str(generator), "--queue-only"])
                self.assertEqual(0, code)
                self.assertEqual(0, stackctl.main(["fresh", "status", "msdmd:ucns"]))
            self.assertEqual(WORKER_PENDING, ledger.get_derivation("msdmd:ucns")["generator"]["identity"])
            self.assertIn('"state": "queued"', printed.getvalue())

    def test_moved_generator_names_the_components_that_differ(self):
        with tempfile.TemporaryDirectory() as tmp, _unbound_env(), patch.dict(os.environ, {"FAKE_NODE": "v24.15.0"}):
            target, _, ledger, spec = self._runtime(Path(tmp), collector=ENV_COLLECTOR)
            first, _ = make(ledger, spec["target"])
            (target / "ucns_msdmd.ts").write_text("tampered\n", encoding="utf-8")
            job, _ = queue_make(ledger, spec["target"])
            job = ledger.retry(job.id)
            with patch.dict(os.environ, {"FAKE_NODE": "absent"}):
                result = run_job(ledger, job.id)
            self.assertEqual("failed", result.state)
            self.assertIn("desired freshness key moved", result.error or "")
            self.assertIn("components differ: node: v24.15.0 -> absent", result.error or "")
            self.assertNotIn("superseded", result.error or "")
        self.assertEqual("components differ: python_modules.yaml: sha256:a -> absent",
                         component_difference({"python_modules": {"yaml": "sha256:a"}},
                                              {"python_modules": {"yaml": "absent"}}))
        self.assertIn("unavailable", component_difference(None, {"node": "v24"}))

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
