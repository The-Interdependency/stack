"""Lints the bash blocks in backend/deploy/VM_CONTACT.md.

Usage: python -m unittest backend.tests.test_vm_contact_runbook
The runbook is pasted block by block into an interactive SSH shell, so a block
must parse, and must not leave `set -e`, an EXIT trap or a umask behind in that
shell: they would end the session at the next expected-nonzero command.
"""
from __future__ import annotations

from pathlib import Path
import re
import subprocess
import unittest

RUNBOOK = Path(__file__).resolve().parents[1] / "deploy" / "VM_CONTACT.md"
# Shell state that must never persist in the operator's interactive shell.
PERSISTENT = re.compile(r"^\s*(set\s+-[A-Za-z]*e|set\s+-o\s+errexit|trap\s.*\bEXIT\b|umask\s)")


def bash_blocks(text: str) -> list[tuple[int, str]]:
    blocks, current, start = [], None, 0
    for number, line in enumerate(text.splitlines(), 1):
        if current is None and line.strip() == "```bash":
            current, start = [], number + 1
        elif current is not None and line.strip() == "```":
            blocks.append((start, "\n".join(current) + "\n"))
            current = None
        elif current is not None:
            current.append(line)
    return blocks


def _wrapped(block: str) -> bool:
    lines = [line for line in block.splitlines() if line.strip()]
    return bool(lines) and lines[0].strip() == "(" and lines[-1].strip() == ")"


def _parses(script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["bash", "-n"], input=script, text=True, capture_output=True, check=False)


class VmContactRunbookTests(unittest.TestCase):
    def setUp(self):
        self.blocks = bash_blocks(RUNBOOK.read_text(encoding="utf-8"))

    def test_runbook_has_bash_blocks(self):
        self.assertGreaterEqual(len(self.blocks), 8)

    def test_every_bash_block_parses(self):
        for line, block in self.blocks:
            with self.subTest(line=line):
                result = _parses(block)
                self.assertEqual(0, result.returncode, result.stderr)

    def test_no_block_sets_shell_state_at_top_level(self):
        for line, block in self.blocks:
            with self.subTest(line=line):
                if not any(PERSISTENT.match(text) for text in block.splitlines()):
                    continue
                # Such a block must be one ( ... ) subshell, and the subshell
                # must not close early: the inner text must parse on its own.
                self.assertTrue(_wrapped(block), f"block at line {line} sets -e/trap/umask outside a subshell")
                lines = block.splitlines()
                first = next(i for i, text in enumerate(lines) if text.strip())
                last = max(i for i, text in enumerate(lines) if text.strip())
                inner = "\n".join(lines[first + 1:last]) + "\n"
                self.assertEqual(0, _parses(inner).returncode, f"block at line {line} closes its subshell early")
                self.assertEqual(0, _parses("f() {\n" + inner + "}\n").returncode)

    def test_blocks_define_the_http_variables_they_use(self):
        for line, block in self.blocks:
            uses = {name for name in ("H", "U", "LIST", "INIT") if re.search(r"\$\{?%s(\b|\[)" % name, block)}
            for name in uses:
                with self.subTest(line=line, name=name):
                    self.assertRegex(block, r"(?m)^\s*%s=" % name, f"block at line {line} uses ${name} without defining it")

    def test_expected_empty_checks_cannot_fail_the_block(self):
        # A bare `grep -c` (exit 1 on zero matches) must be guarded by `|| true`.
        for line, block in self.blocks:
            for text in block.splitlines():
                if "grep -c" in text:
                    with self.subTest(line=line, text=text):
                        self.assertIn("|| true", text)


if __name__ == "__main__":
    unittest.main()
