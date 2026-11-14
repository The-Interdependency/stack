# ratios: loc_comments=43:31 imports_exports=5:5 calls_definitions=18:5
# === CHECKS ===
# id: uchc_unicode_projection_check
#   proves: uchc_unicode_graph_is_projected
#   call: self::test_scoped_graph_is_projected
#   requires: python3, pytest
#   timeout: 60
#   mutates: none
#   cleanup: none
# id: uchc_unicode_projection_omission_check
#   proves: uchc_unicode_graph_is_projected
#   call: self::test_checker_rejects_omitted_participant
#   requires: python3, pytest
#   timeout: 60
#   mutates: none
#   cleanup: none
# id: uchc_unicode_projection_drift_check
#   proves: uchc_unicode_graph_is_projected
#   call: self::test_checker_rejects_divergent_participant
#   requires: python3, pytest
#   timeout: 60
#   mutates: none
#   cleanup: none
# id: uchc_unicode_human_projection_check
#   proves: uchc_unicode_graph_is_projected
#   call: self::test_checker_rejects_missing_human_row
#   requires: python3, pytest
#   timeout: 60
#   mutates: none
#   cleanup: none
# === END CHECKS ===
"""Exercise the production consistency gate against lost Unicode provenance."""
from copy import deepcopy
import json
from pathlib import Path
import runpy

import pytest

ROOT = Path(__file__).resolve().parents[3]
CHECK = runpy.run_path(str(ROOT / "tools/check_stack_consistency.py"))[
    "check_unicode_bit_radius_graph"
]
MANIFEST = json.loads((ROOT / "stack-manifest.json").read_text(encoding="utf-8"))
HUMAN = (ROOT / "STACK_MANIFEST.md").read_text(encoding="utf-8")
SOURCES = json.loads((ROOT / "research/english-gonol/docs/unicode-bit-radius-work-graph.json")
                     .read_text(encoding="utf-8"))["repositories"]


def findings(manifest=MANIFEST, human=HUMAN):
    result = []
    CHECK(manifest, human, result)
    return result


def test_scoped_graph_is_projected():
    assert findings() == []


@pytest.mark.parametrize("source", SOURCES, ids=lambda source: source["repository"])
def test_checker_rejects_omitted_participant(source):
    manifest = deepcopy(MANIFEST)
    manifest["research_participants"] = [
        entry for entry in manifest["research_participants"]
        if not (entry["repository"] == source["repository"]
                and entry["commit"] == source["commit"])
    ]
    assert any(item.startswith("unicode_graph.participant:") for item in findings(manifest))


@pytest.mark.parametrize("field,value", [
    ("commit", "0" * 40), ("authority", "changed authority"),
    ("relation", "changed relation"), ("canonical_release", True),
    ("authority_transfer", True),
])
def test_checker_rejects_divergent_participant(field, value):
    manifest = deepcopy(MANIFEST)
    entry = next(entry for entry in manifest["research_participants"]
                 if entry["participant_id"] == "unicode-bit-radius-ucns")
    entry[field] = value
    assert any(item.startswith("unicode_graph.participant:") for item in findings(manifest))


@pytest.mark.parametrize("source", SOURCES, ids=lambda source: source["repository"])
def test_checker_rejects_missing_human_row(source):
    human = "\n".join(line for line in HUMAN.splitlines() if source["commit"] not in line)
    assert any(item.startswith("unicode_graph.human_drift:") for item in findings(human=human))
# ratios: loc_comments=43:31 imports_exports=5:5 calls_definitions=18:5
