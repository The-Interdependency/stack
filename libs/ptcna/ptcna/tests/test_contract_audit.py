"""Mutation-style evidence for the no-exec contract graph auditor."""

import importlib.util
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_contracts.py"
SPEC = importlib.util.spec_from_file_location("ptcna_check_contracts", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
AUDITOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDITOR)

# === CHECKS ===
# id: check_contract_audit_complete_graph
#   proves: contract_audit_closes_complete_graph
#   call: self::test_complete_graph_closes
#   requires: python3
#   timeout: 10
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_contract_audit_broken_edges
#   proves: contract_audit_exposes_broken_edges
#   call: self::test_broken_graph_exposes_each_required_gap
#   requires: python3
#   timeout: 10
#   mutates: filesystem
#   cleanup: tempdir_teardown
# === END CHECKS ===


def test_complete_graph_closes() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / "source.py").write_text(
            "# === CONTRACTS ===\n"
            "# id: example_contract\n"
            "#   given: valid input\n"
            "#   then: valid output\n"
            "# === END CONTRACTS ===\n",
            encoding="utf-8",
        )
        (root / "test_source.py").write_text(
            "# === CHECKS ===\n"
            "# id: check_example\n"
            "#   proves: example_contract\n"
            "#   call: self::test_example\n"
            "#   mutates: none\n"
            "#   cleanup: none\n"
            "# === END CHECKS ===\n"
            "def test_example():\n"
            "    return None\n",
            encoding="utf-8",
        )
        assert AUDITOR.audit(root) == []


def test_broken_graph_exposes_each_required_gap() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        (root / "source.py").write_text(
            "# === CONTRACTS ===\n"
            "# id: orphan_contract\n"
            "#   given: valid input\n"
            "#   then: visible evidence\n"
            "# === END CONTRACTS ===\n",
            encoding="utf-8",
        )
        (root / "test_source.py").write_text(
            "# === CHECKS ===\n"
            "# id: check_phantom\n"
            "#   proves: phantom_contract\n"
            "#   call: self::test_missing\n"
            "#   mutates: none\n"
            "#   cleanup: none\n"
            "# === END CHECKS ===\n"
            "def test_orphan():\n"
            "    return None\n",
            encoding="utf-8",
        )
        gaps = "\n".join(AUDITOR.audit(root))
        assert "orphan_contract has no CHECKS entry" in gaps
        assert "claims unknown contract: phantom_contract" in gaps
        assert "call does not resolve: self::test_missing" in gaps
        assert "test_orphan has no resolving CHECKS declaration" in gaps
