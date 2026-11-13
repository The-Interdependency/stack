# ratios: loc_comments=28:31 imports_exports=3:4 calls_definitions=16:4
"""Negative controls for the qualification gate; run with pytest."""
# === CHECKS ===
# id: english_test_test_gate_rejects_incomplete_evidence
#   proves: english_qualification_test_outcomes
#   call: self::test_test_gate_rejects_incomplete_evidence
#   requires: python3, pytest
#   timeout: 60
#   mutates: pytest temporary files
#   cleanup: pytest_tmp_path
# id: english_test_test_gate_accepts_passed_cases
#   proves: english_qualification_test_outcomes
#   call: self::test_test_gate_accepts_passed_cases
#   requires: python3, pytest
#   timeout: 60
#   mutates: pytest temporary files
#   cleanup: pytest_tmp_path
# id: english_test_junit_aggregate_must_agree
#   proves: english_qualification_test_outcomes
#   call: self::test_junit_aggregate_must_agree
#   requires: python3, pytest
#   timeout: 60
#   mutates: pytest temporary files
#   cleanup: pytest_tmp_path
# id: english_test_alias_cannot_claim_two_executions
#   proves: english_qualification_distinct_artifacts
#   call: self::test_alias_cannot_claim_two_executions
#   requires: python3, pytest
#   timeout: 60
#   mutates: pytest temporary files
#   cleanup: pytest_tmp_path
# === END CHECKS ===
import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location("english_qualification", Path(__file__).parents[1] / "qualify_english_gonols.py")
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
# ratios: loc_comments=28:31 imports_exports=3:4 calls_definitions=16:4
