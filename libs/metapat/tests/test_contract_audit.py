from __future__ import annotations

# === CHECKS ===
# id: check_repository_contract_graph_closes
#   proves: metapat_contract_graph_closes
#   call: self::test_repository_contract_graph_closes
#   mutates: filesystem_read
#   cleanup: none
#
# id: check_contract_audit_negative_gaps
#   proves: metapat_contract_audit_detects_gaps
#   call: self::test_audit_reports_required_negative_gaps
#   mutates: tempdir
#   cleanup: tempdir_teardown
# === END CHECKS ===

import shutil
from pathlib import Path

from tools.check_contract_graph import audit_repository

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_repository_contract_graph_closes() -> None:
    result = audit_repository(REPO_ROOT)
    assert result.closed, "\n".join(result.gaps)
    assert result.contracts > 0
    assert result.checks > 0
    assert result.executable_tests == result.checks


def test_audit_reports_required_negative_gaps(tmp_path: Path) -> None:
    parser_source = REPO_ROOT / ".agents/skills/msdmd/parsers/universal.py"
    parser_target = tmp_path / ".agents/skills/msdmd/parsers/universal.py"
    parser_target.parent.mkdir(parents=True)
    shutil.copy2(parser_source, parser_target)

    source = tmp_path / "src/metapat/sample.py"
    source.parent.mkdir(parents=True)
    source.write_text(
        "# === CONTRACTS ===\n"
        "# id: orphan_contract\n"
        "#   given: a planted orphan exists\n"
        "#   then: the audit reports it\n"
        "#   class: safety\n"
        "# === END CONTRACTS ===\n",
        encoding="utf-8",
    )

    test_file = tmp_path / "tests/test_sample.py"
    test_file.parent.mkdir(parents=True)
    test_file.write_text(
        "# === CHECKS ===\n"
        "# id: check_phantom\n"
        "#   proves: unknown_contract\n"
        "#   call: self::missing\n"
        "#   mutates: none\n"
        "#   cleanup: none\n"
        "# === END CHECKS ===\n\n"
        "def test_undeclared():\n"
        "    pass\n",
        encoding="utf-8",
    )

    result = audit_repository(tmp_path)
    text = "\n".join(result.gaps)
    assert "orphan_contract has no CHECKS entry" in text
    assert "check_phantom claims unknown contract: unknown_contract" in text
    assert "check_phantom call does not resolve" in text
    assert "executable check test_undeclared has no resolving CHECKS declaration" in text
    assert not result.closed
