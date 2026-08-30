# === CHECKS ===
# id: check_boundary_runner_audit_gate
#   proves: boundary_runner_audits_before_execution
#   call: self::test_audit_gap_prevents_execution
#   requires: python3
#   timeout: 10
#   mutates: temporary_path
#   cleanup: pytest temporary_path
#
# id: check_boundary_runner_capability_timeout_consumption
#   proves: boundary_runner_consumes_capabilities_and_timeouts
#   call: self::test_missing_capability_and_timeout_are_enforced
#   requires: python3
#   timeout: 15
#   mutates: temporary_path
#   cleanup: pytest temporary_path
#
# id: check_boundary_runner_registered_capability_detection
#   proves: boundary_runner_consumes_capabilities_and_timeouts
#   call: self::test_registered_posix_capabilities_are_detected
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_boundary_runner_status_continuation
#   proves: boundary_runner_classifies_and_continues
#   call: self::test_runner_classifies_all_outcomes_and_continues
#   requires: python3
#   timeout: 20
#   mutates: temporary_path
#   cleanup: pytest temporary_path
#
# id: check_boundary_runner_receipt_binding
#   proves: boundary_runner_receipt_is_bounded_and_bound
#   call: self::test_receipt_binds_declarations_outputs_and_identity
#   requires: python3
#   timeout: 10
#   mutates: temporary_path
#   cleanup: pytest temporary_path
#
# id: check_boundary_runner_nonactivation
#   proves: boundary_runner_has_no_activation_effect
#   call: self::test_passing_receipt_has_no_activation_or_selection_effect
#   requires: python3
#   timeout: 10
#   mutates: temporary_path
#   cleanup: pytest temporary_path
# === END CHECKS ===

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


RUNNER_PATH = Path(__file__).parents[1] / "tools" / "run_skill_lib_boundaries.py"
SPEC = importlib.util.spec_from_file_location("run_skill_lib_boundaries", RUNNER_PATH)
assert SPEC is not None and SPEC.loader is not None
runner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = runner
SPEC.loader.exec_module(runner)


def _repo(tmp_path: Path, functions: str, checks: list[dict[str, str]]) -> Path:
    root = tmp_path / "repo"
    (root / "src" / "pkg").mkdir(parents=True)
    (root / "tools").mkdir()
    (root / "tests").mkdir()
    contracts: list[str] = []
    check_lines: list[str] = []
    for index, check in enumerate(checks):
        contract_id = f"contract_{index}"
        contracts.extend([
            f"# id: {contract_id}", "#   given: fixture input",
            "#   then: fixture outcome", "#   class: evidence", "#",
        ])
        check_lines.extend([
            f"# id: {check['id']}", f"#   proves: {contract_id}",
            f"#   call: self::{check['function']}",
            f"#   requires: {check.get('requires', 'python3')}",
            f"#   timeout: {check.get('timeout', '5')}",
            "#   mutates: none", "#   cleanup: none", "#",
        ])
    (root / "src" / "pkg" / "feature.py").write_text(
        "\n".join([
            "# === MODULE_BUILD ===", "# id: fixture_module",
            "#   module_name: feature", "#   module_kind: instrument",
            "#   summary: fixture", "#   owner: fixture", "#   public_surface: none",
            "#   internal_surface: none", "#   auth_boundary: none",
            "#   storage_boundary: none", "#   network_boundary: none",
            "#   user_data_boundary: none", "#   admin_only: false",
            "#   tests: tests/test_feature.py", "#   rollout: fixture",
            "#   rollback: remove", "# === END MODULE_BUILD ===",
            "# === CONTRACTS ===", *contracts, "# === END CONTRACTS ===", "",
        ]), encoding="utf-8"
    )
    (root / "tests" / "test_feature.py").write_text(
        "\n".join(["# === CHECKS ===", *check_lines, "# === END CHECKS ===", "", functions]),
        encoding="utf-8",
    )
    return root


def test_audit_gap_prevents_execution(tmp_path: Path) -> None:
    root = _repo(tmp_path, "def test_never():\n    raise AssertionError('ran')\n", [{"id": "check_never", "function": "test_never"}])
    source = root / "src" / "pkg" / "feature.py"
    source.write_text(source.read_text().replace(
        "# === END CONTRACTS ===",
        "# id: orphan\n#   given: x\n#   then: y\n# === END CONTRACTS ===",
    ))
    receipt = runner.run_boundaries(root)
    assert receipt["status"] == "audit-gap"
    assert receipt["outcomes"] == []
    assert len(receipt["receipt_sha256"]) == 64


def test_missing_capability_and_timeout_are_enforced(tmp_path: Path) -> None:
    root = _repo(tmp_path, "def test_missing():\n    pass\n", [{
        "id": "check_missing", "function": "test_missing",
        "requires": "capability-that-cannot-exist",
    }])
    receipt = runner.run_boundaries(root)
    assert receipt["outcomes"][0]["status"] == "ERROR"
    assert receipt["outcomes"][0]["missing_capabilities"] == (
        "capability-that-cannot-exist",
    )

    root = _repo(tmp_path / "timeout", "import time\ndef test_slow():\n    time.sleep(5)\n", [{
        "id": "check_slow", "function": "test_slow", "timeout": "1",
    }])
    receipt = runner.run_boundaries(root)
    assert receipt["outcomes"][0]["status"] == "TIMEOUT"
    assert receipt["outcomes"][0]["duration_seconds"] < 4


def test_registered_posix_capabilities_are_detected() -> None:
    assert runner._capability_available("posix_resource") == (
        runner.os.name == "posix"
        and importlib.util.find_spec("resource") is not None
    )
    assert runner._capability_available("sched_affinity") == (
        hasattr(runner.os, "sched_getaffinity")
        and hasattr(runner.os, "sched_setaffinity")
    )


def test_runner_classifies_all_outcomes_and_continues(tmp_path: Path) -> None:
    functions = """
def test_pass():
    pass
def test_fail():
    assert False
def test_error():
    raise RuntimeError("broken harness")
"""
    checks = [
        {"id": "check_pass", "function": "test_pass"},
        {"id": "check_fail", "function": "test_fail"},
        {"id": "check_error", "function": "test_error"},
    ]
    receipt = runner.run_boundaries(_repo(tmp_path, functions, checks))
    assert [item["status"] for item in receipt["outcomes"]] == [
        "PASS", "FAIL", "ERROR",
    ]
    assert receipt["outcome_counts"] == {
        "PASS": 1, "FAIL": 1, "ERROR": 1, "TIMEOUT": 0,
    }


def test_receipt_binds_declarations_outputs_and_identity(tmp_path: Path) -> None:
    root = _repo(tmp_path, "def test_output():\n    print('evidence')\n", [{
        "id": "check_output", "function": "test_output",
    }])
    receipt = runner.run_boundaries(root)
    outcome = receipt["outcomes"][0]
    assert outcome["contract_ids"] == ("contract_0",)
    assert outcome["mutates"] == outcome["cleanup"] == "none"
    assert outcome["stdout_bytes"] > 0
    assert len(outcome["stdout_sha256"]) == 64
    identity = receipt.pop("receipt_sha256")
    encoded = json.dumps(
        receipt, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    assert identity == sha256(encoded).hexdigest()


def test_passing_receipt_has_no_activation_or_selection_effect(tmp_path: Path) -> None:
    receipt = runner.run_boundaries(_repo(
        tmp_path, "def test_pass():\n    pass\n",
        [{"id": "check_pass", "function": "test_pass"}],
    ))
    assert receipt["status"] == "passed"
    assert receipt["selection_effect"] == "none"
    assert receipt["edcm_activation"] == "inactive"
    assert receipt["canon_status"] == "none"
