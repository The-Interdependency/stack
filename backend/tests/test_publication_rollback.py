"""Regression check for filesystem/SQL fresh-making acceptance rollback."""
from __future__ import annotations

# === CHECKS ===
# id: check_stack_msdmd_publish_rollback
#   proves: stack_msdmd_publish_after_verify
#   call: self::test_acceptance_failure_restores_previous_artifact
#   requires: python3, git
#   mutates: filesystem
#   cleanup: tempdir_teardown
# === END CHECKS ===

from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from backend.msdmd import make
import backend.tests.test_orchestrator as fixtures


class PublicationRollbackTests(unittest.TestCase):
    def test_acceptance_failure_restores_previous_artifact(self):
        with tempfile.TemporaryDirectory() as tmp, fixtures._unbound_env():
            target, _, ledger, spec = fixtures.FreshMakingTests()._runtime(Path(tmp))
            _, first = make(ledger, spec["target"])
            self.assertEqual(first.state, "fresh")
            output = target / "ucns_msdmd.ts"
            previous = output.read_bytes()

            (target / "x.py").write_text("x = 4\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(target), "add", "x.py"], check=True)
            subprocess.run(["git", "-C", str(target), "commit", "-qm", "new desired key"], check=True)

            with patch.object(ledger, "accept_success", side_effect=RuntimeError("postgres unavailable")):
                with self.assertRaises(RuntimeError):
                    make(ledger, spec["target"])

            self.assertEqual(output.read_bytes(), previous)


if __name__ == "__main__":
    unittest.main()
