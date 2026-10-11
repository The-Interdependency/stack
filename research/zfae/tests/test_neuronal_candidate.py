# === MODULE_BUILD ===
# id: zfae_neuronal_candidate_regressions
#   module_name: test_neuronal_candidate
#   module_kind: verification-tool
#   summary: mutation witnesses for candidate authority and neural-readiness boundaries
#   owner: The-Interdependency/stack
#   public_surface: unittest discovery
#   internal_surface: isolated documentation and source-lock fixtures
#   auth_boundary: none
#   storage_boundary: temporary local fixture files
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: self
#   rollout: existing zfae-research workflow
#   rollback: replace only with equivalent boundary witnesses
# === END MODULE_BUILD ===
"""Usage: python -m unittest discover -s research/zfae/tests -p test_neuronal_candidate.py -v

These guards check explicit documentation and pinned standing, not inference.
Fixtures copy current evidence and plant the two review regressions separately.
"""
from pathlib import Path
import json
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from check_stack_consistency import check_zfae_neuronal_candidate

# === CHECKS ===
# id: zfae_candidate_current_boundary_witness
#   proves: zfae_candidate_preserves_current_authority
#   call: self::test_current_candidate_boundaries
#   mutates: none
#   cleanup: none
# id: zfae_candidate_projection_mutation_witness
#   proves: zfae_candidate_preserves_current_authority
#   call: self::test_candidate_projection_mutations
#   mutates: filesystem
#   cleanup: tempdir_teardown
# id: zfae_candidate_source_promotion_mutation_witness
#   proves: zfae_candidate_preserves_current_authority
#   call: self::test_source_promotion_mutations
#   mutates: filesystem
#   cleanup: tempdir_teardown
# === END CHECKS ===


def test_current_candidate_boundaries():
    findings = []
    check_zfae_neuronal_candidate(findings, ROOT)
    assert findings == [], findings


def _fixture(root):
    workspace = root / "research" / "zfae"
    workspace.mkdir(parents=True)
    for name in ("README.md", "UCNS_NEURONAL_INFERENCE.md", "BASE.json", "UCHC_INPUT.json"):
        shutil.copyfile(ROOT / "research" / "zfae" / name, workspace / name)
    return workspace


def test_candidate_projection_mutations():
    for name in ("README.md", "UCNS_NEURONAL_INFERENCE.md"):
        for boundary in (
            "Proposed inference authority: **unassigned**.",
            "Axis construction is not an inference-node witness.",
        ):
            with tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                path = _fixture(root) / name
                original = path.read_text(encoding="utf-8")
                assert boundary in original
                path.write_text(original.replace(boundary, ""), encoding="utf-8")
                findings = []
                check_zfae_neuronal_candidate(findings, root)
                assert any(row.startswith("zfae.candidate_boundary:") for row in findings), findings


def test_source_promotion_mutations():
    cases = (
        ("BASE.json", "authority", "UCNS/UCHC owns neural construction", "zfae.candidate_authority:"),
        ("BASE.json", "authority_transfer", True, "zfae.candidate_authority:"),
        ("UCHC_INPUT.json", "neural_readiness", "established", "zfae.candidate_readiness:"),
        ("UCHC_INPUT.json", "authority_transfer", True, "zfae.candidate_readiness:"),
    )
    for name, key, value, expected in cases:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = _fixture(root) / name
            data = json.loads(path.read_text(encoding="utf-8"))
            data[key] = value
            path.write_text(json.dumps(data), encoding="utf-8")
            findings = []
            check_zfae_neuronal_candidate(findings, root)
            assert any(row.startswith(expected) for row in findings), findings


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(unittest.FunctionTestCase(fn) for fn in (
        test_current_candidate_boundaries,
        test_candidate_projection_mutations,
        test_source_promotion_mutations,
    ))
