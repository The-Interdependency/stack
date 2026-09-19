# ratios: loc_comments=16:1 imports_exports=3:2 calls_definitions=9:2
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
    path.write_text('<testsuites><testsuite><testcase name="passed"/></testsuite></testsuites>')
    qualification.check_tests([path])
# ratios: loc_comments=16:1 imports_exports=3:2 calls_definitions=9:2
