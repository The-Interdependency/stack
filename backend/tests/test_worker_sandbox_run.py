"""Checks backend/ops/worker_sandbox_run.sh against stubbed systemctl/systemd-run.

Usage: python -m unittest backend.tests.test_worker_sandbox_run
The stub systemctl prints a chosen `systemctl show` result (the loaded unit
with drop-ins already merged); the stub systemd-run prints its arguments.
"""
from __future__ import annotations

# === CHECKS ===
# id: check_stack_worker_sandbox_run_fails_closed
#   proves: stack_msdmd_identity_observed_where_executed
#   call: self::test_missing_or_relaxed_hardening_fails_closed
#   requires: python3, bash
#   mutates: filesystem
#   cleanup: tempdir_teardown
# === END CHECKS ===

import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "ops" / "worker_sandbox_run.sh"
SHOWN = """LoadState=loaded
User=stackorchestrator
Group=stackorchestrator
WorkingDirectory=/srv/stack
EnvironmentFiles=/etc/stack-orchestrator.env (ignore_errors=no)
EnvironmentFiles=/etc/stack-orchestrator.d/extra.env (ignore_errors=yes)
Environment=STACK_POLL_SECONDS=5 PYTHONDONTWRITEBYTECODE=1
UMask=0077
NoNewPrivileges=yes
PrivateTmp=yes
ProtectHome=yes
ProtectSystem=strict
ReadWritePaths=/srv/stack-repos /var/lib/stack-orchestrator
ReadOnlyPaths=
InaccessiblePaths=
RestrictAddressFamilies=AF_UNIX
LockPersonality=yes
MemoryDenyWriteExecute=yes
"""


class WorkerSandboxRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.bin = Path(self.tmp.name)
        self.shown = self.bin / "shown.txt"
        (self.bin / "systemctl").write_text(f'#!/bin/sh\necho "$*" > {self.bin}/systemctl.args\ncat {self.shown}\n')
        (self.bin / "systemd-run").write_text('#!/bin/sh\nfor a in "$@"; do echo "ARG:$a"; done\n')
        for name in ("systemctl", "systemd-run"):
            (self.bin / name).chmod(0o755)

    def tearDown(self):
        self.tmp.cleanup()

    def run_wrapper(self, shown: str, *args: str) -> subprocess.CompletedProcess:
        self.shown.write_text(shown, encoding="utf-8")
        env = dict(os.environ, PATH=os.pathsep.join([str(self.bin), os.environ["PATH"]]))
        env.pop("STACK_WORKER_USER", None)
        env.pop("STACK_WORKER_UNIT", None)
        return subprocess.run(["bash", str(SCRIPT), *args], env=env, capture_output=True, text=True)

    def test_properties_come_from_systemctl_show(self):
        result = self.run_wrapper(SHOWN, "--chdir", "/srv/stack/skill-lib", "--setenv", "PYTHONPATH=/srv/stack/skill-lib",
                                  "--", "/srv/stack/.venv/bin/python", "-P", "-m", "msdmd.collect", "--print-generator-identity")
        self.assertEqual(0, result.returncode, result.stderr)
        args = [line[4:] for line in result.stdout.splitlines()]
        for expected in ("--property=User=stackorchestrator", "--property=MemoryDenyWriteExecute=yes",
                         "--property=ProtectSystem=strict",
                         "--property=ReadWritePaths=/srv/stack-repos /var/lib/stack-orchestrator",
                         "--property=Environment=STACK_POLL_SECONDS=5 PYTHONDONTWRITEBYTECODE=1",
                         "--property=EnvironmentFile=/etc/stack-orchestrator.env",
                         "--property=EnvironmentFile=-/etc/stack-orchestrator.d/extra.env",
                         "--working-directory=/srv/stack/skill-lib", "--setenv=PYTHONPATH=/srv/stack/skill-lib"):
            self.assertIn(expected, args)
        self.assertNotIn("--property=WorkingDirectory=/srv/stack", args)  # --chdir wins
        self.assertFalse([a for a in args if a.startswith("--property=ReadOnlyPaths")])  # empty values dropped
        self.assertEqual(["--", "/srv/stack/.venv/bin/python", "-P"], args[args.index("--"):args.index("--") + 3])
        queried = (self.bin / "systemctl.args").read_text()
        self.assertIn("show", queried)
        self.assertIn("-p MemoryDenyWriteExecute", queried)
        self.assertIn("stack-orchestrator-worker.service", queried)

    def test_missing_or_relaxed_hardening_fails_closed(self):
        cases = {
            "MemoryDenyWriteExecute=no": SHOWN.replace("MemoryDenyWriteExecute=yes", "MemoryDenyWriteExecute=no"),
            "MemoryDenyWriteExecute=missing": SHOWN.replace("MemoryDenyWriteExecute=yes\n", ""),
            "User=root": SHOWN.replace("User=stackorchestrator", "User=root"),
            "User=missing": SHOWN.replace("User=stackorchestrator\n", "User=\n"),
            "LoadState=not-found": SHOWN.replace("LoadState=loaded", "LoadState=not-found"),
        }
        for expected, shown in cases.items():
            with self.subTest(expected):
                result = self.run_wrapper(shown, "--", "true")
                self.assertEqual(2, result.returncode, result.stdout)
                self.assertIn(expected, result.stderr)
                self.assertNotIn("ARG:", result.stdout)


if __name__ == "__main__":
    unittest.main()
