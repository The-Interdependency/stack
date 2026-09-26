# ratios: loc_comments=54:1 imports_exports=5:5 calls_definitions=25:5
"""Negative controls for the qualification gate; run with pytest."""
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("language_qualification", Path(__file__).parents[1] / "qualify_language_gonols.py")
qualification = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qualification)


@pytest.mark.parametrize("body", ["", "<testcase><skipped/></testcase>", "<testcase><failure/></testcase>", "<testcase><error/></testcase>"])
def test_test_gate_rejects_incomplete_evidence(tmp_path, body):
    path = tmp_path / "outcome.xml"
    path.write_text("<testsuites><testsuite>" + body + "</testsuite></testsuites>")
    with pytest.raises(ValueError):
        qualification.check_tests([path])


def test_test_gate_accepts_passed_cases(tmp_path):
    path = tmp_path / "outcome.xml"
    path.write_text('<testsuites><testsuite tests="1" skipped="0" failures="0" errors="0"><testcase name="passed"/></testsuite></testsuites>')
    qualification.check_tests([path])
@pytest.mark.parametrize("attribute,value", [("tests", "2"), ("failures", "1"), ("errors", "1"), ("skipped", "1")])
def test_junit_aggregate_must_agree(tmp_path, attribute, value):
    report = '<testsuite tests="1" skipped="0" failures="0" errors="0"><testcase name="a"/></testsuite>'
    before = 'tests="1"' if attribute == "tests" else f'{attribute}="0"'
    path = tmp_path / "results.xml"
    path.write_text(report.replace(before, f'{attribute}="{value}"'))
    with pytest.raises(ValueError):
        qualification.check_tests([path])


def test_alias_cannot_claim_two_executions(tmp_path):
    (tmp_path / "receipt.json").write_text("{}")
    with pytest.raises(ValueError, match="distinct"):
        qualification.distinct_outputs(tmp_path, tmp_path / ".", ("receipt.json",))


def test_compare_rejects_corrupted_provenance_and_counts(tmp_path):
    import json
    from hashlib import sha256
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir(); b.mkdir()
    inputs = [{"path": "x.py", "git_blob": "a" * 40, "sha256": "b" * 64, "bytes": 1}]
    outcome = {**inputs[0], "outcome": "REJECTED_ENCODING", "reason": "SyntaxError"}
    data = qualification.canonical(outcome) + b"\n"
    receipt = {"schema": "language-gonol.python-qualification", "version": 1,
               "cpython": qualification.CPYTHON, "ucns": qualification.UCNS_PYTHON,
               "python": "3.12.14", "sqlite_runtime": qualification.sqlite3.sqlite_version, "implementation_sha256": qualification.implementation_hashes(),
               "input_files": 1, "input_bytes": 1, "counts": {"rejected_encoding": 1},
               "inventory_sha256": sha256(qualification.canonical(inputs)).hexdigest(),
               "outcomes_sha256": sha256(data).hexdigest()}
    for root in (a, b):
        (root / "inventory.json").write_bytes(qualification.canonical(inputs))
        (root / "outcomes.jsonl").write_bytes(data)
        (root / "receipt.json").write_bytes(qualification.canonical(receipt))
    qualification.compare(a, b)
    for key, value in (("schema", "wrong"), ("version", 2), ("cpython", "wrong"), ("ucns", "wrong"),
                       ("python", "wrong"), ("implementation_sha256", {}), ("input_bytes", 2), ("counts", {})):
        bad = {**receipt, key: value}
        for root in (a, b):
            (root / "receipt.json").write_bytes(qualification.canonical(bad))
        with pytest.raises(ValueError):
            qualification.compare(a, b)

# ratios: loc_comments=54:1 imports_exports=5:5 calls_definitions=25:5
