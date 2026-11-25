# ratios: loc_comments=93:12 imports_exports=6:5 calls_definitions=32:5
"""Focused native-equivalence, evidence, and no-leakage checks for corpus projection."""

import json
import math
import numpy as np
import pytest

# === CHECKS ===
# id: multiwoz_native_cache_equivalence
#   contract: multiwoz_native_exact_display
#   method: exact native endpoint/display and full recursive field norm comparison
# id: multiwoz_future_context_rejection
#   contract: multiwoz_before_response_only
#   method: source response and label substitution leaves all preceding scores identical
# id: multiwoz_checkpoint_identity
#   contract: multiwoz_source_and_checkpoint_reconciliation
#   method: resume exact row and reject mismatched source or checkpoint identity
# === END CHECKS ===
from research.edcm import epicycle_projection as e
from research.edcm import multiwoz_projection as m


@pytest.fixture(scope="module", autouse=True)
def native():
    m.initialize()


@pytest.mark.parametrize(
    "raw",
    [
        [
            "USER: repeat repeat.\nSYSTEM: try again.",
            "USER: café.\nSYSTEM: cafe\u0301.",
        ],
        ["USER: one two.\nSYSTEM: will not.", "USER: x\ny\nSYSTEM:  z."],
    ],
)
def test_cached_display_and_complete_norm_match_native(raw):
    members = []
    for value in raw:
        if members:
            members.append(m.SEPARATOR)
        members.append(m.close_round(value))
    root, _ = m.replay(m.close_prefix(members), "\n".join(raw))
    cache = m.DisplayCache()
    values, present = cache.addressed(root, verify=True)
    packet = e.geometry.closed_record(root)
    public = e.validate_record(packet, expected_text="\n".join(raw))
    field = e.build_views(public)["recursive"]
    expected = np.array(
        [
            c
            for key in m.SUPPORT
            for z in [field[key].value if key in field else 0j]
            for c in (z.real, z.imag)
        ]
    )
    assert np.array_equal(values, expected)
    assert present == sum(key in field for key in m.SUPPORT)
    assert cache.norm_squared(root) == pytest.approx(
        math.fsum(abs(v.value) ** 2 for v in field.values()), rel=1e-12
    )
    projection = cache.measure(root)
    assert len(projection["coordinates"]) == 11
    assert 0 <= projection["energy_fraction"] <= 1


def test_no_labeled_response_or_future_text_enters_event():
    first = (
        0,
        "sample",
        "development",
        "source-a",
        ("Need a room.", "Where?", "In Cambridge.", "Booked."),
        ((3, 1),),
    )
    second = (
        0,
        "sample",
        "development",
        "source-b",
        ("Need a room.", "Where?", "In Cambridge.", "Not available."),
        ((3, 0),),
    )
    a, b = m.observe_dialogue(first), m.observe_dialogue(second)
    assert a["rows"][0] == b["rows"][0]
    assert a["events"][0]["native_digest"] == b["events"][0]["native_digest"]
    assert a["events"][0]["scores"] == b["events"][0]["scores"]
    assert a["events"][0]["context_sha256"] == b["events"][0]["context_sha256"]
    assert a["events"][0]["label"] != b["events"][0]["label"]
    assert a["graph_digest"] != b["graph_digest"]
    assert "Need a room." not in json.dumps(a)


def test_correlation_retains_absence_and_ties():
    assert m.correlation([1, 1, 1], [1, 2, 3]) is None
    assert m.correlation([1, 2, 3], [3, 2, 1]) == pytest.approx(-1)
    assert m.ranks([4, 4, 5, 1]).tolist() == [1.5, 1.5, 3.0, 0.0]


def test_checkpoint_requires_same_source_and_digest(tmp_path):
    path = tmp_path / "cp.jsonl"
    identity = {"archive": "a"}
    task = (0, "sample", "development", "source-a", ("hi", "bye"), ())
    row = m.observe_dialogue(task)
    assert m.checkpoint_rows(path, identity, [task]) == []
    with path.open("ab") as handle:
        handle.write(e.canonical({"row": row, "digest": e.digest(row)}) + b"\n")
    assert m.checkpoint_rows(path, identity, [task]) == [row]
    with pytest.raises(ValueError):
        m.checkpoint_rows(path, {"archive": "b"}, [task])
    with pytest.raises(ValueError):
        m.checkpoint_rows(
            path,
            identity,
            [(0, "sample", "development", "source-b", ("hi", "bye"), ())],
        )

# ratios: loc_comments=93:12 imports_exports=6:5 calls_definitions=32:5
