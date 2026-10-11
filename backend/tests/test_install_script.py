"""Checks backend/ops/install_msdmd_runtime.sh with stubbed pip, npm and collector.

Usage: python -m unittest backend.tests.test_install_script
Nothing is installed: the venv interpreter stubs ``pip`` and the collector
prints identity components chosen by the test. The sandboxed systemd probe is
exercised on the VM (it needs root and systemd-run).
"""
from __future__ import annotations

# === CHECKS ===
# id: check_stack_msdmd_runtime_install_fails_without_node_runtimes
#   proves: stack_msdmd_runtime_install
#   call: self::test_absent_node_or_typescript_fails
#   requires: python3, bash
#   mutates: filesystem
#   cleanup: tempdir_teardown
# === END CHECKS ===

import getpass
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "ops" / "install_msdmd_runtime.sh"


class InstallScriptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.venv = base / "venv"
        (self.venv / "bin").mkdir(parents=True)
        python = self.venv / "bin" / "python"
        python.write_text(
            "#!/bin/sh\n"
            'if [ "$1" = "-m" ] && [ "$2" = "pip" ]; then echo "stub pip $*"; exit 0; fi\n'
            f'exec {sys.executable} "$@"\n', encoding="utf-8")
        python.chmod(0o755)
        self.skill = base / "skill-lib"
        msdmd = self.skill / "msdmd"
        msdmd.mkdir(parents=True)
        (msdmd / "__init__.py").write_text("", encoding="utf-8")
        (msdmd / "requirements.txt").write_text("docstring-parser==0.18.0\n", encoding="utf-8")
        (msdmd / "package-lock.json").write_text("{}\n", encoding="utf-8")
        (msdmd / "collect.py").write_text(
            "import json, os\n"
            "print(json.dumps({'node': os.environ.get('FAKE_NODE', 'absent'),"
            " 'typescript': os.environ.get('FAKE_TS', 'absent')}))\n", encoding="utf-8")
        self.bin = base / "bin"
        self.bin.mkdir()
        for name, body in (("node", "exit 0\n"),
                           ("npm", 'mkdir -p "$4/node_modules" && echo installed > "$4/node_modules/marker"\n')):
            tool = self.bin / name
            tool.write_text("#!/bin/sh\n" + body, encoding="utf-8")
            tool.chmod(0o755)

    def tearDown(self):
        self.tmp.cleanup()

    def run_script(self, **env) -> subprocess.CompletedProcess:
        full = dict(os.environ, PATH=os.pathsep.join([str(self.bin), os.environ["PATH"]]),
                    STACK_VENV=str(self.venv), STACK_SKILL_LIB_ROOT=str(self.skill))
        full.update({"STACK_WORKER_USER": getpass.getuser(), "STACK_SANDBOX_PROBE": "skip", **env})
        # A restrictive caller umask must not leak into the installed trees.
        return subprocess.run(["bash", "-c", 'umask 077; exec bash "$0"', str(SCRIPT)],
                              env=full, capture_output=True, text=True)

    def test_installs_world_readable_and_reports_runtimes(self):
        result = self.run_script(FAKE_NODE="v24.15.0", FAKE_TS="5.8.3")
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('"typescript": "5.8.3"', result.stdout)
        self.assertIn("sandboxed probe skipped", result.stderr)
        marker = self.skill / "msdmd" / "node_modules" / "marker"
        self.assertEqual(0o644, marker.stat().st_mode & 0o777)

    def test_absent_node_or_typescript_fails(self):
        for env, missing in (({"FAKE_NODE": "v24.15.0"}, "typescript absent"),
                             ({"FAKE_TS": "5.8.3"}, "node absent")):
            with self.subTest(missing=missing):
                result = self.run_script(**env)
                self.assertEqual(3, result.returncode, result.stdout + result.stderr)
                self.assertIn(missing, result.stderr)

    def test_unknown_worker_user_and_unprobed_sandbox_fail(self):
        result = self.run_script(FAKE_NODE="v24.15.0", FAKE_TS="5.8.3", STACK_WORKER_USER="no-such-user-xyz")
        self.assertEqual(2, result.returncode)
        self.assertIn("worker user no-such-user-xyz does not exist", result.stderr)
        if os.geteuid() != 0:
            result = self.run_script(FAKE_NODE="v24.15.0", FAKE_TS="5.8.3", STACK_SANDBOX_PROBE="")
            self.assertEqual(4, result.returncode, result.stderr)
            self.assertIn("sandboxed probe needs root", result.stderr)


if __name__ == "__main__":
    unittest.main()
