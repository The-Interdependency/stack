# ratios: loc_comments=195:410 imports_exports=23:18 calls_definitions=248:20
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
#   proves: boundary_runner_classifies_and_continues, boundary_pytest_observes_actual_outcomes
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
#   timeout: 30
#   mutates: temporary_path
#   cleanup: pytest temporary_path
# === END CHECKS ===

# === CHECKS ===
# id: check_boundary_runner_skips_are_not_passes
#   proves: boundary_runner_classifies_and_continues
#   call: self::test_skips_xfails_and_mixed_parameters_are_not_passes
#   requires: python3, pytest
#   timeout: 30
#   mutates: temporary_path
#   cleanup: pytest temporary_path
#
# id: check_boundary_runner_invalid_declaration_continuation
#   proves: boundary_runner_classifies_and_continues
#   call: self::test_invalid_execution_metadata_does_not_abort_later_checks
#   requires: python3, pytest
#   timeout: 15
#   mutates: temporary_path
#   cleanup: pytest temporary_path
#
# id: check_boundary_runner_source_identity
#   proves: boundary_runner_receipt_is_bounded_and_bound
#   call: self::test_source_mutation_prevents_acceptance
#   requires: python3, pytest
#   timeout: 15
#   mutates: temporary_path
#   cleanup: pytest temporary_path
#
# id: check_boundary_runner_report_and_discovery_boundaries
#   proves: boundary_runner_classifies_and_continues, boundary_runner_receipt_is_bounded_and_bound
#   call: self::test_report_errors_suffix_discovery_and_launch_continuation
#   requires: python3, pytest
#   timeout: 20
#   mutates: temporary_path
#   cleanup: pytest temporary_path
# === END CHECKS ===

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
from tools import run_skill_lib_boundaries as runner


RUNNER_PATH = Path(__file__).parents[1] / "tools" / "run_skill_lib_boundaries.py"


def _repo(tmp_path: Path, functions: str, checks: list[dict[str, str]]) -> Path:
    root = tmp_path / "repo"
    (root / "src" / "pkg").mkdir(parents=True)
    (root / "tools").mkdir()
    (root / "tests").mkdir()
    (root / "pyproject.toml").write_text('[tool.pytest.ini_options]\ncollect_imported_tests = false\ntestpaths = ["tests"]\n')
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
    root = _repo(tmp_path / "rebound-function", "def test_probe(): assert False\ndef test_probe(): pass\n", [{"id": "check_probe", "function": "test_probe"}])
    receipt = runner.run_boundaries(root)
    assert receipt["status"] == "audit-gap" and not receipt["outcomes"], receipt
    root = _repo(tmp_path / "nested", "def test_fails(): assert False\n", [{"id": "check_fails", "function": "test_fails"}])
    nested = root / "tests/sub"
    nested.mkdir()
    (root / "tests/test_feature.py").rename(nested / "test_feature.py")
    (nested / "pyproject.toml").write_text('[tool.pytest.ini_options]\ncollect_imported_tests = false\naddopts = "-p custom_plugin"\n')
    marker = tmp_path / "plugin-executed"
    (root / "custom_plugin.py").write_text(f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\ndef pytest_runtest_setup(item):\n    item.obj = lambda: None\n")
    receipt = runner.run_boundaries(root)
    assert receipt["status"] == "audit-gap" and not receipt["outcomes"], receipt
    assert not marker.exists()
    # Even below the audit gate, execution must select the audited root config.
    outcome = runner._run_check(root, runner._declared_checks(root)[0])
    assert outcome.status == "FAIL", outcome
    assert not marker.exists()
    hook_body = f"from pathlib import Path\ndef pytest_generate_tests(metafunc):\n    Path({str(marker)!r}).write_text('hook ran')\n    metafunc.function.__code__ = (lambda: None).__code__\ndef test_fails(): assert False\n"
    root = _repo(tmp_path / "module-hook", hook_body, [{"id": "check_fails", "function": "test_fails"}])
    receipt = runner.run_boundaries(root)
    assert receipt["status"] == "audit-gap" and not receipt["outcomes"], receipt
    assert not marker.exists()
    root = _repo(tmp_path / "descriptor", "from descriptor_helper import descriptor\nclass TestInjected:\n    injected = descriptor\ndef test_probe(): pass\n", [{"id": "check_probe", "function": "test_probe"}])
    (root / "descriptor_helper.py").write_text(f"from pathlib import Path\nclass Inject:\n    def __set_name__(self, owner, name):\n        Path({str(marker)!r}).write_text('descriptor ran')\n        owner.test_hidden = lambda self: 1 / 0\ndescriptor = Inject()\n")
    receipt = runner.run_boundaries(root)
    assert receipt["status"] == "audit-gap" and not receipt["outcomes"], receipt
    assert not marker.exists()
    root = _repo(tmp_path / "fixture-helper", "import pytest\n@pytest.fixture\ndef test_data(): return 1\ndef test_probe(test_data): assert test_data == 1\n", [{"id": "check_probe", "function": "test_probe"}])
    receipt = runner.run_boundaries(root)
    assert receipt["status"] == "passed", receipt
    callback_body = f"import pytest\nfrom pathlib import Path\ndef alter(value):\n    Path({str(marker)!r}).write_text('callback ran')\n    test_fails.__code__ = (lambda sample: None).__code__\n    return str(value)\n@pytest.fixture(params=[1], ids=alter)\ndef sample(request): return request.param\ndef test_fails(sample): assert False\n"
    root = _repo(tmp_path / "decorator-callback", callback_body, [{"id": "check_fails", "function": "test_fails"}])
    receipt = runner.run_boundaries(root)
    assert receipt["status"] == "audit-gap" and not receipt["outcomes"], receipt
    assert not marker.exists()
    root = _repo(tmp_path / "import-optout", "from helper import __test__\ndef test_fails(): assert False\n", [{"id": "check_fails", "function": "test_fails"}])
    (root / "helper.py").write_text(f"from pathlib import Path\nPath({str(marker)!r}).write_text('import ran')\n__test__ = False\n")
    (root / "tests/test_other.py").write_text("# === CHECKS ===\n# id: check_other\n#   proves: contract_0\n#   call: self::test_other\n#   timeout: 5\n#   mutates: none\n#   cleanup: none\n# === END CHECKS ===\ndef test_other(): pass\n")
    receipt = runner.run_boundaries(root)
    assert receipt["status"] == "audit-gap" and not receipt["outcomes"], receipt
    assert not marker.exists()


    helper_source = "import inspect\ndef passing(): pass\nfor frame in inspect.stack():\n    namespace = frame.frame.f_globals\n    if 'test_probe' in namespace:\n        passing.__name__ = 'test_probe'\n        passing.__module__ = namespace['__name__']\n        namespace['test_probe'] = passing\n"
    root = _repo(tmp_path / "helper-replacement", "def test_probe(): assert False\nimport replacing_helper\n", [{"id": "check_probe", "function": "test_probe"}])
    helper = root / "tests/replacing_helper.py"
    helper.write_text(helper_source)
    receipt = runner.run_boundaries(root)
    assert receipt["status"] == "audit-gap" and not receipt["outcomes"], receipt
    # Root helpers are outside the declared source layout and must fail the audit.
    helper.rename(root / "replacing_helper.py")
    receipt = runner.run_boundaries(root)
    assert receipt["status"] == "audit-gap" and not receipt["outcomes"], receipt
    assert any("root helper" in gap for gap in receipt["audit_gaps"])
    # Below the audit gate, the runtime still rejects a replaced witness.
    outcome = runner._run_check(root, runner._declared_checks(root)[0])
    assert outcome.status == "FAIL" and "witness code differs" in outcome.stdout_excerpt, outcome
    hiding = "import inspect\nfor frame in inspect.stack():\n    witness = frame.frame.f_globals.get('test_fails')\n    if witness is not None:\n        witness.__test__ = False\n"
    root = _repo(tmp_path / "hidden-witness", "def test_fails(): assert False\nimport hide_witness\ndef test_passes(): pass\n", [{"id": "check_fails", "function": "test_fails"}, {"id": "check_passes", "function": "test_passes"}])
    (root / "hide_witness.py").write_text(hiding)
    receipt = runner.run_boundaries(root)
    assert receipt["status"] == "audit-gap" and not receipt["outcomes"], receipt
    namespace = root / "hide_package"
    namespace.mkdir()
    (root / "hide_witness.py").rename(namespace / "effects.py")
    source = root / "tests/test_feature.py"
    source.write_text(source.read_text().replace("import hide_witness", "import hide_package.effects"))
    receipt = runner.run_boundaries(root)
    assert receipt["status"] == "audit-gap" and not receipt["outcomes"], receipt


# === CHECKS ===
# id: check_geometry_suite_nonempty_pass
#   proves: geometry_suite_requires_nonempty_pass
#   call: self::test_geometry_suite_rejects_nonpasses
#   requires: python3
#   timeout: 90
#   mutates: filesystem
#   cleanup: tempdir_teardown
# === END CHECKS ===
def test_geometry_suite_rejects_nonpasses(tmp_path: Path) -> None:
    import os
    import subprocess
    import sys
    cases = (
        ("pass", "def test_probe(): pass\n", True),
        ("skip", "import pytest\ndef test_probe(): pytest.skip('unobserved')\n", False),
        ("marked-skip", "import pytest\n@pytest.mark.skip(reason='unobserved')\ndef test_probe(): pass\n", False),
        ("xfail", "import pytest\n@pytest.mark.xfail\ndef test_probe(): assert False\n", False),
        ("xpass", "import pytest\n@pytest.mark.xfail(strict=False)\ndef test_probe(): pass\n", False),
        ("empty", "# no executable checks\n", False),
        ("collection-skip", "import pytest\npytest.skip('unobserved', allow_module_level=True)\n", False),
        ("collection-error", "raise RuntimeError('broken collection')\n", False),
        ("module-mark", "import pytest\npytestmark = pytest.mark.skip\ndef test_probe(): assert False\n", False),
        ("hidden-witness", "def test_fails(): assert False\nimport hide_witness\ndef test_passes(): pass\n", False),
        ("removed-witness", "def test_first(request): request.session.items[:] = [request.node]\ndef test_fails(): assert False\n", False),
        ("removed-parameter", "import pytest\n@pytest.mark.parametrize('value', [0, 1], ids=['a::b', 'failing'])\ndef test_probe(value, request):\n    if value == 0: request.session.items[:] = [request.node]\n    assert value == 0\n", False),
    )
    script = "import os,sys; from pathlib import Path; sys.path.insert(0,sys.argv[1]); from tools._boundary_pytest import run_suite; root=Path(sys.argv[2]); os.chdir(root); raise SystemExit(run_suite(['tests','-c','pyproject.toml','--noconftest','--strict-config'],root))"
    environment = {key: value for key, value in os.environ.items() if key not in {"PYTHONPATH", "PYTHONHOME", "PYTEST_ADDOPTS", "PYTEST_PLUGINS"}}
    environment["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    for label, body, expected_pass in cases:
        checks = [{"id": "check_probe", "function": "test_probe", "timeout": "15"}] if label in {"removed-parameter", "marked-skip"} else []
        root = _repo(tmp_path / label, body, checks)
        if label.startswith("collection-"):
            (root / "tests/test_other.py").write_text("def test_other(): pass\n")
        if label == "hidden-witness":
            (root / "hide_witness.py").write_text("import inspect\nfor frame in inspect.stack():\n    witness = frame.frame.f_globals.get('test_fails')\n    if witness is not None:\n        witness.__test__ = False\n")
        result = subprocess.run([sys.executable, "-c", script, str(RUNNER_PATH.parents[1]), str(root)], env=environment, capture_output=True, text=True)
        assert (result.returncode == 0) is expected_pass, (label, result.stdout, result.stderr)
        if label in {"removed-parameter", "marked-skip"}:
            receipt = runner.run_boundaries(root)
            assert receipt["audit_closed"] and receipt["status"] == "not-passed", json.dumps(receipt, indent=2)
            assert receipt["outcomes"][0]["status"] == ("ERROR" if label == "removed-parameter" else "SKIP"), json.dumps(receipt, indent=2)
            if label == "removed-parameter":
                assert "did not all execute" in receipt["outcomes"][0]["diagnostic"]


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
    raise RuntimeError("AssertionError mentioned by a broken harness")
def test_subclass():
    class ContractViolation(AssertionError):
        pass
    raise ContractViolation("broken")
"""
    checks = [
        {"id": "check_pass", "function": "test_pass"},
        {"id": "check_fail", "function": "test_fail"},
        {"id": "check_error", "function": "test_error"},
        {"id": "check_subclass", "function": "test_subclass"},
    ]
    receipt = runner.run_boundaries(_repo(tmp_path, functions, checks))
    assert [item["status"] for item in receipt["outcomes"]] == [
        "PASS", "FAIL", "ERROR", "FAIL",
    ]
    assert receipt["outcome_counts"] == {
        "PASS": 1, "FAIL": 2, "ERROR": 1, "TIMEOUT": 0, "SKIP": 0,
    }


def test_report_errors_suffix_discovery_and_launch_continuation(tmp_path: Path, monkeypatch) -> None:
    report = tmp_path / "report.xml"
    assert runner._pytest_outcome(report, 0)[0] == "ERROR"
    for text in ("not json", "[]", '{"status": "PASS"}', '{"status": "PASS", "calls": [], "other": [], "origins": {}}'):
        report.write_text(text)
        assert runner._pytest_outcome(report, 0)[0] == "ERROR"
    root = _repo(tmp_path, "def test_first():\n    pass\ndef test_later():\n    pass\n", [
        {"id": "check_first", "function": "test_first"},
        {"id": "check_later", "function": "test_later"},
    ])
    (root / "tests/test_feature.py").rename(root / "tests/feature_test.py")
    original = runner._run_check

    def launch(repository, check):
        if check.id == "check_first":
            raise OSError("fixture process launch failed")
        return original(repository, check)

    monkeypatch.setattr(runner, "_run_check", launch)
    receipt = runner.run_boundaries(root)
    assert [outcome["status"] for outcome in receipt["outcomes"]] == ["ERROR", "PASS"]
    assert receipt["outcomes"][0]["diagnostic"].startswith("OSError:")
    assert receipt["status"] == "not-passed"


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


    root = _repo(tmp_path / "text-input", "from pathlib import Path\ndef test_probe():\n    assert Path(__file__).with_name('witness.txt').read_text() in {'one', 'two'}\n", [{"id": "check_probe", "function": "test_probe"}])
    witness = root / "tests/witness.txt"
    snapshots = []
    for text in ("one", "two"):
        witness.write_text(text)
        observed = runner.run_boundaries(root)
        assert observed["status"] == "passed" and observed["source_unchanged"], observed
        assert observed["source_files_sha256"]["tests/witness.txt"] == sha256(text.encode()).hexdigest()
        snapshots.append(observed["source_before_sha256"])
    assert snapshots[0] != snapshots[1]
    for directory in runner.SOURCE_DIRECTORIES:
        path = root / directory / "fixture-without-suffix"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"input")
        inventory, _ = runner._source_snapshot(root)
        assert inventory[path.relative_to(root).as_posix()] == sha256(b"input").hexdigest()


    import pytest
    outside = tmp_path / "outside-inputs"
    outside.mkdir()
    (outside / "witness").write_text("one")
    for index, name in enumerate(("tests/fixtures", "tests/witness-link", "README.md", ".agents")):
        linked = _repo(tmp_path / f"symlink-{index}", "def test_probe(): pass\n", [{"id": "check_probe", "function": "test_probe"}])
        path = linked / name
        path.symlink_to(outside / "witness" if name == "tests/witness-link" or name == "README.md" else outside)
        invalid = runner.run_boundaries(linked)
        assert invalid["status"] == "audit-gap" and not invalid["outcomes"]
        assert any("unsupported source symlink" in gap for gap in invalid["audit_gaps"])


def test_passing_receipt_has_no_activation_or_selection_effect(tmp_path: Path) -> None:
    receipt = runner.run_boundaries(_repo(
        tmp_path, "def test_pass():\n    pass\n",
        [{"id": "check_pass", "function": "test_pass"}],
    ))
    assert receipt["status"] == "passed"
    assert receipt["selection_effect"] == "none"
    assert receipt["edcm_activation"] == "inactive"
    assert receipt["canon_status"] == "none"
    parametrized = _repo(tmp_path / "parameter-ids", "import pytest\n@pytest.mark.parametrize('value', [1, 2], ids=['a::b', 'nested[x]::y'])\ndef test_probe(value): assert value > 0\n", [{"id": "check_probe", "function": "test_probe"}])
    observed = runner.run_boundaries(parametrized)
    assert observed["status"] == "passed", observed


def test_skips_xfails_and_mixed_parameters_are_not_passes(tmp_path: Path) -> None:
    bodies = (
        "import pytest\ndef test_probe():\n    pytest.skip('not observed')\n",
        "import pytest\n@pytest.mark.xfail(reason='broken')\ndef test_probe():\n    assert False\n",
        "import pytest\n@pytest.mark.parametrize('x', [1, 2])\ndef test_probe(x):\n    if x == 2: pytest.skip('partial')\n",
    )
    for index, body in enumerate(bodies):
        root = _repo(tmp_path / str(index), body, [{"id": "check_probe", "function": "test_probe"}])
        receipt = runner.run_boundaries(root)
        assert receipt["status"] == "not-passed"
        assert receipt["outcomes"][0]["status"] == "SKIP"
    for index, decorator in enumerate(("@pytest.mark.xfail(strict=False)", "@pytest.mark.xfail(strict=True)")):
        body = "import pytest\n" + decorator + "\ndef test_probe():\n    pass\n"
        root = _repo(tmp_path / f"xpass{index}", body, [{"id": "check_probe", "function": "test_probe"}])
        receipt = runner.run_boundaries(root)
        assert receipt["status"] == "not-passed"
        assert receipt["outcomes"][0]["status"] == "FAIL"
    assert runner.run_boundaries(tmp_path / "absent")["status"] == "audit-gap"


def test_invalid_execution_metadata_does_not_abort_later_checks(tmp_path: Path) -> None:
    root = _repo(tmp_path, "def test_bad():\n    pass\ndef test_good():\n    pass\n", [
        {"id": "check_bad", "function": "test_bad", "timeout": "not-an-integer"},
        {"id": "check_good", "function": "test_good"},
    ])
    receipt = runner.run_boundaries(root)
    assert [outcome["status"] for outcome in receipt["outcomes"]] == ["ERROR", "PASS"]
    assert receipt["status"] == "not-passed"


def test_source_mutation_prevents_acceptance(tmp_path: Path) -> None:
    root = _repo(tmp_path, "from pathlib import Path\ndef test_probe():\n    p=Path('src/pkg/feature.py')\n    p.write_text(p.read_text()+'\\n# mutation\\n')\n", [
        {"id": "check_probe", "function": "test_probe"},
    ])
    receipt = runner.run_boundaries(root)
    assert receipt["outcomes"][0]["status"] == "PASS"
    assert receipt["status"] == "not-passed"
    assert receipt["source_before_sha256"] != receipt["source_after_sha256"]
    assert receipt["source_unchanged"] is False
    root = _repo(tmp_path / "restored", "from pathlib import Path\ndef test_probe():\n    p=Path('src/pkg/feature.py')\n    original=p.read_bytes()\n    p.write_bytes(original+b'\\n# transient\\n')\n    p.write_bytes(original)\n", [
        {"id": "check_probe", "function": "test_probe"},
    ])
    receipt = runner.run_boundaries(root)
    assert receipt["source_before_sha256"] == receipt["source_after_sha256"]
    assert receipt["source_unchanged"] is False
    assert receipt["status"] == "not-passed"
    assert "src/pkg/feature.py" in receipt["outcomes"][0]["source_events"]
    import pytest
    import subprocess
    with pytest.raises(ValueError, match="outside the bound source tree"):
        runner.write_receipt(receipt, root / "generated/receipt.json")
    assert not (root / "generated/receipt.json").exists()
    result = subprocess.run([sys.executable, str(RUNNER_PATH), str(root), "--receipt", str(root / "generated/receipt.json")], capture_output=True, text=True)
    assert result.returncode == 2
    assert "outside the bound source tree" in result.stderr
    external = tmp_path / "outside-receipt.json"
    source = root / "src/pkg/feature.py"
    original = source.read_bytes()
    external.hardlink_to(source)
    runner.write_receipt(receipt, external)
    assert source.read_bytes() == original
    assert json.loads(external.read_text())["receipt_sha256"] == receipt["receipt_sha256"]
    internal_link = root / "receipt-link.json"
    internal_link.symlink_to(external)
    external_before = external.read_bytes()
    with pytest.raises(ValueError, match="outside the bound source tree"):
        runner.write_receipt(receipt, internal_link)
    result = subprocess.run([sys.executable, str(RUNNER_PATH), str(root), "--receipt", str(internal_link)], capture_output=True, text=True)
    assert result.returncode == 2
    assert "outside the bound source tree" in result.stderr
    assert internal_link.is_symlink() and external.read_bytes() == external_before
    root_alias = tmp_path / "root-alias"
    root_alias.symlink_to(root, target_is_directory=True)
    with pytest.raises(ValueError, match="outside the bound source tree"):
        runner.write_receipt(receipt, root_alias / internal_link.name)
    assert internal_link.is_symlink() and external.read_bytes() == external_before
    alias = tmp_path / "source-alias.py"
    body = f"from pathlib import Path\ndef test_probe():\n    p=Path({str(alias)!r})\n    original=p.read_bytes()\n    p.write_bytes(original+b'# transient\\n')\n    p.write_bytes(original)\n"
    root = _repo(tmp_path / "hardlinked", body, [{"id": "check_probe", "function": "test_probe"}])
    alias.hardlink_to(root / "src/pkg/feature.py")
    receipt = runner.run_boundaries(root)
    assert receipt["outcomes"][0]["status"] == "PASS"
    assert receipt["source_before_sha256"] == receipt["source_after_sha256"]
    assert receipt["status"] == "not-passed"
    assert "src/pkg/feature.py" in receipt["outcomes"][0]["source_events"]
# === CHECKS ===
# id: check_boundary_runner_import_origin
#   proves: boundary_runner_receipt_is_bounded_and_bound, boundary_pytest_observes_actual_outcomes, boundary_descendants_import_bound_source
#   call: self::test_check_imports_bound_source_despite_ambient_pythonpath
#   requires: python3, pytest
#   timeout: 30
#   mutates: temporary_path
#   cleanup: pytest temporary_path
# === END CHECKS ===


    root = _repo(tmp_path / "new-symlink", "from pathlib import Path\ndef test_mutate():\n    Path(__file__).with_name('new-link').symlink_to('test_feature.py')\ndef test_later(): pass\n", [{"id": "check_mutate", "function": "test_mutate"}, {"id": "check_later", "function": "test_later"}])
    receipt = runner.run_boundaries(root)
    assert receipt["status"] == "not-passed" and not receipt["source_unchanged"]
    assert [outcome["check_id"] for outcome in receipt["outcomes"]] == ["check_mutate", "check_later"]
    assert all(outcome["status"] == "ERROR" for outcome in receipt["outcomes"])
    assert receipt["snapshot_errors"] and receipt["source_after_sha256"] == ""
    assert receipt["outcomes"][0]["source_events"]


def test_check_imports_bound_source_despite_ambient_pythonpath(tmp_path: Path, monkeypatch) -> None:
    body = "import pkg.feature\nimport subprocess, sys\ndef test_probe():\n    assert pkg.feature.VALUE == 'bound'\n    child = subprocess.check_output([sys.executable, '-c', 'import pkg.feature; print(pkg.feature.VALUE)'], text=True)\n    assert child.strip() == 'bound'\n"
    root = _repo(tmp_path, body, [{"id": "check_probe", "function": "test_probe", "timeout": "15"}])
    source = root / "src/pkg/feature.py"
    source.write_text(source.read_text() + "VALUE = 'bound'\n")
    # A regular package avoids unrelated namespace packages in the host.
    (root / "src/pkg/__init__.py").write_text(source.read_text().replace("fixture_module", "fixture_init").replace("contract_0", "init_contract"))
    (root / "tests/test_feature.py").write_text((root / "tests/test_feature.py").read_text().replace("#   proves: contract_0", "#   proves: contract_0, init_contract"))
    alternate = tmp_path / "alternate"
    (alternate / "pkg").mkdir(parents=True)
    (alternate / "pkg/__init__.py").write_text("")
    (alternate / "pkg/feature.py").write_text("VALUE = 'wrong'\n")
    monkeypatch.setenv("PYTHONPATH", str(alternate))
    test_source = root / "tests/test_feature.py"
    test_source.write_text(test_source.read_text().replace("text=True)", f"text=True, cwd={str(alternate)!r})"))
    receipt = runner.run_boundaries(root)
    assert receipt["status"] == "passed", json.dumps(receipt, indent=2)
    assert receipt["outcomes"][0]["imported_sources"]["pkg.feature"] == [str(source)]

# === CHECKS ===
# id: check_boundary_background_descendants
#   proves: boundary_runner_receipt_is_bounded_and_bound, boundary_pytest_observes_actual_outcomes, boundary_supervisor_ends_descendants
#   call: self::test_background_descendants_block_acceptance
#   requires: python3, pytest
#   timeout: 30
#   mutates: temporary_path
#   cleanup: pytest temporary_path
# === END CHECKS ===


    # A timestamp-valid cache must not replace inventoried source bytes.
    import os
    import py_compile
    import subprocess
    poisoned = _repo(tmp_path / "poisoned-cache", "def test_probe():\n    from pkg.feature import VALUE\n    assert VALUE == 1\n    import subprocess, sys\n    child = subprocess.run([sys.executable, '-c', 'from pkg.feature import VALUE; print(VALUE)'], check=True, capture_output=True, text=True)\n    assert child.stdout.strip() == '1'\n", [{"id": "check_probe", "function": "test_probe", "timeout": "15"}])
    module = poisoned / "src/pkg/feature.py"
    declarations = module.read_text()
    module.write_text(declarations + "\nVALUE = 2\n")
    stamp = module.stat()
    cache = module.parent / "__pycache__" / f"{module.stem}.{sys.implementation.cache_tag}.pyc"
    py_compile.compile(str(module), cfile=str(cache), doraise=True)
    module.write_text(declarations + "\nVALUE = 1\n")
    os.utime(module, ns=(stamp.st_atime_ns, stamp.st_mtime_ns))
    ordinary = dict(os.environ, PYTHONPATH=str(poisoned / "src"), PYTHONDONTWRITEBYTECODE="1")
    ordinary.pop("PYTHONPYCACHEPREFIX", None)
    old = subprocess.run([sys.executable, "-c", "from pkg.feature import VALUE; print(VALUE)"], env=ordinary, capture_output=True, text=True, check=True)
    assert old.stdout.strip() == "2", "fixture must contain an executable stale cache"
    observed = runner.run_boundaries(poisoned)
    assert observed["status"] == "passed" and observed["source_unchanged"], json.dumps(observed, indent=2)
    assert not any("__pycache__" in name for name in observed["source_files_sha256"])


def test_background_descendants_block_acceptance(tmp_path: Path) -> None:
    import os
    import pytest
    from tools._boundary_supervisor import _owned_children
    proc = tmp_path / "proc"
    proc.mkdir()
    for pid, parent in ((101, os.getpid()), (102, 1)):
        process = proc / str(pid)
        process.mkdir()
        (process / "stat").write_text(f"{pid} (name with ) spaces) S {parent} 0 0 0\n")
    (proc / "103").mkdir()  # Exited between directory enumeration and stat read.
    assert _owned_children(proc) == [101]
    task = proc / f"self/task/{os.getpid()}"
    task.mkdir(parents=True)
    (task / "children").write_text("101 104\n")
    assert _owned_children(proc) == [101, 104]
    child = "import time; from pathlib import Path; time.sleep(30); Path('src/pkg/feature.py').write_text('late mutation')"
    body = f"import subprocess, sys\nfrom pathlib import Path\ndef test_probe():\n    p=subprocess.Popen([sys.executable, '-c', {child!r}], start_new_session=True)\n    Path('child.pid').write_text(str(p.pid))\n"
    root = _repo(tmp_path, body, [{"id": "check_probe", "function": "test_probe"}])
    before = (root / "src/pkg/feature.py").read_bytes()
    receipt = runner.run_boundaries(root)
    assert receipt["status"] == "not-passed", receipt
    assert receipt["outcomes"][0]["status"] == "ERROR"
    assert receipt["outcomes"][0]["descendants_reaped"] >= 1
    pid = int((root / "child.pid").read_text())
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)
    assert (root / "src/pkg/feature.py").read_bytes() == before
    body += "    import signal, time; signal.signal(signal.SIGTERM, signal.SIG_IGN); time.sleep(30)\n"
    timeout_root = _repo(tmp_path / "timeout-child", body, [{"id": "check_probe", "function": "test_probe", "timeout": "5"}])
    receipt = runner.run_boundaries(timeout_root)
    assert receipt["outcomes"][0]["status"] == "TIMEOUT"
    pid = int((timeout_root / "child.pid").read_text())
    with pytest.raises(ProcessLookupError):
        os.kill(pid, 0)
# === CHECKS ===
# id: check_node24_capability_runs_typescript_witness
#   proves: boundary_runner_consumes_capabilities_and_timeouts, boundary_runner_receipt_is_bounded_and_bound, boundary_supervisor_ends_descendants
#   call: self::test_node24_capability_runs_typescript_witness
#   requires: python3, node24
#   timeout: 20
#   mutates: filesystem
#   cleanup: tempdir_teardown
# === END CHECKS ===


def test_node24_capability_runs_typescript_witness(tmp_path: Path) -> None:
    import os
    import pytest
    from unittest.mock import patch
    from subprocess import CompletedProcess
    for version, expected in (("v24.15.0\n", True), ("v22.23.2\n", False), ("not-a-version", False)):
        with patch.object(runner.shutil, "which", return_value="/fake/node"):
            with patch.object(runner.subprocess, "run", return_value=CompletedProcess([], 0, version, "")):
                assert runner._capability_available("node24") is expected
    with patch.object(runner.shutil, "which", return_value=None):
        assert not runner._capability_available("node24")
    receipt = runner.run_boundaries(RUNNER_PATH.resolve().parents[1], selected_ids=("check_vendored_typescript_field_preservation",))
    assert receipt["status"] == "passed", receipt
    assert len(receipt["outcomes"]) == 1 and receipt["outcomes"][0]["status"] == "PASS", receipt
    root = _repo(tmp_path, "def test_probe(): pass\n", [{"id": "check_probe", "function": "test_probe", "requires": "node24"}])
    source = root / "src/pkg/feature.py"
    node = tmp_path / "node"
    node.write_text(f"#!{sys.executable}\nfrom pathlib import Path\np=Path({str(source)!r})\noriginal=p.read_bytes()\np.write_bytes(original+b'# transient\\n')\np.write_bytes(original)\nprint('v24.15.0')\n")
    node.chmod(0o755)
    with patch.dict(os.environ, {"PATH": str(tmp_path) + os.pathsep + os.environ["PATH"]}):
        receipt = runner.run_boundaries(root)
    assert receipt["outcomes"][0]["status"] == "PASS", receipt
    assert receipt["source_before_sha256"] == receipt["source_after_sha256"]
    assert receipt["status"] == "not-passed" and not receipt["source_unchanged"]
    assert "src/pkg/feature.py" in receipt["outcomes"][0]["source_events"]
    pid_path = tmp_path / "probe-child.pid"
    node.write_text(f"#!{sys.executable}\nimport subprocess, sys\nfrom pathlib import Path\np=subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(30)'], start_new_session=True)\nPath({str(pid_path)!r}).write_text(str(p.pid))\nprint('v24.15.0')\n")
    with patch.dict(os.environ, {"PATH": str(tmp_path) + os.pathsep + os.environ["PATH"]}):
        receipt = runner.run_boundaries(root)
    assert receipt["status"] == "not-passed" and receipt["outcomes"][0]["status"] == "ERROR", receipt
    assert receipt["outcomes"][0]["missing_capabilities"] == ("node24",)
    with pytest.raises(ProcessLookupError):
        os.kill(int(pid_path.read_text()), 0)
    node.write_text(f"#!{sys.executable}\nimport os, time\nfrom pathlib import Path\nPath({str(pid_path)!r}).write_text(str(os.getpid()))\nprint('v24.15.0', flush=True)\ntime.sleep(30)\n")
    with patch.dict(os.environ, {"PATH": str(tmp_path) + os.pathsep + os.environ["PATH"]}):
        receipt = runner.run_boundaries(root)
    assert receipt["outcomes"][0]["status"] == "ERROR", receipt
    with pytest.raises(ProcessLookupError):
        os.kill(int(pid_path.read_text()), 0)
# ratios: loc_comments=195:410 imports_exports=23:18 calls_definitions=248:20
