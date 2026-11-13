"""The backend workflow pins every third-party action to a full commit SHA."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

WORKFLOW = Path(__file__).resolve().parents[2] / ".github" / "workflows" / "backend.yml"
USES = re.compile(r"^\s*(?:-\s*)?uses:\s*(\S+)(.*)$")
PINNED = re.compile(r"^[\w.-]+/[\w./-]+@[0-9a-f]{40}$")


class BackendWorkflowPinTests(unittest.TestCase):
    def test_every_action_is_pinned_by_commit_sha_with_a_version_comment(self):
        lines = WORKFLOW.read_text(encoding="utf-8").splitlines()
        uses = [m for m in map(USES.match, lines) if m]
        self.assertGreaterEqual(len(uses), 2)  # checkout and setup-python at least
        for match in uses:
            action, rest = match.group(1), match.group(2)
            if action.startswith("./"):
                continue  # local actions are part of this commit already
            with self.subTest(action=action):
                self.assertRegex(action, PINNED, "pin by 40-hex commit SHA, not a tag")
                self.assertRegex(rest, r"#\s*v\d", "keep the human-readable version as a comment")


if __name__ == "__main__":
    unittest.main()
