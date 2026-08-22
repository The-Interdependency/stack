# === CHECKS ===
# id: check_contract_audit_no_exec
#   proves: contract_audit_is_no_exec
#   call: self::test_contract_audit_no_exec
#   requires: python3
#   timeout: 5
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_contract_audit_detects_gaps
#   proves: contract_audit_reports_graph_gaps
#   call: self::test_contract_audit_detects_gaps
#   requires: python3
#   timeout: 5
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_repository_contract_graph
#   proves: contract_audit_accepts_closed_graph
#   call: self::test_repository_contract_graph
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from pathlib import Path
from tempfile import TemporaryDirectory

from tools.verify_skill_lib_contracts import audit_repository

ROOT = Path(__file__).resolve().parents[1]


def test_contract_audit_no_exec() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "src").mkdir()
        marker = root / "executed.txt"
        (root / "src" / "module.py").write_text(
            "# === CONTRACTS ===\n"
            "# id: safe_import\n"
            "#   given: source is audited\n"
            "#   then: top-level code is not executed\n"
            "# === END CONTRACTS ===\n"
            f"open({str(marker)!r}, 'w').write('executed')\n",
            encoding="utf-8",
        )
        ok, problems = audit_repository(root)
        assert not ok
        assert problems
        assert not marker.exists()


def test_contract_audit_detects_gaps() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "tests").mkdir()
        (root / "src").mkdir()
        (root / "src" / "bare.py").write_text(
            "def behavior():\n"
            "    return 1\n",
            encoding="utf-8",
        )
        (root / "tests" / "test_orphan.py").write_text(
            "# === CHECKS ===\n"
            "# id: orphan_check\n"
            "#   proves: absent_contract\n"
            "#   call: self::missing_function\n"
            "#   mutates: none\n"
            "#   cleanup: none\n"
            "# === END CHECKS ===\n"
            "def missing_function():\n"
            "    return None\n",
            encoding="utf-8",
        )
        ok, problems = audit_repository(root)
        assert not ok
        assert any("unknown contract" in problem for problem in problems)
        assert any("missing MODULE_BUILD" in problem for problem in problems)
        assert any("missing CONTRACTS" in problem for problem in problems)
        assert any("orphan_check missing fields: timeout" in problem for problem in problems)
        assert any("does not target an executable pytest test" in problem for problem in problems)


def test_repository_contract_graph() -> None:
    ok, problems = audit_repository(ROOT)
    assert ok, "\n".join(problems)
