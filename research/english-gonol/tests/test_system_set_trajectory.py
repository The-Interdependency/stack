# === CHECKS ===
# id: check_system_set_trajectory_order
#   proves: system_set_trajectory_preserves_order
#   call: self::test_order_and_multiplicity_are_load_bearing
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_system_set_trajectory_evidence
#   proves: system_set_trajectory_preserves_comparison_evidence
#   call: self::test_comparison_input_carries_complete_steps
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_system_set_trajectory_boundary
#   proves: system_set_trajectory_no_downstream_judgment
#   call: self::test_no_downstream_judgment_is_encoded
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_system_set_trajectory_immutable
#   proves: system_set_trajectory_immutable_inputs
#   call: self::test_mutable_inputs_are_frozen_before_identity
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from english_gonol.system_set_trajectory import SemanticStep, SystemSetTrajectory


def make(path_id, steps):
    return SystemSetTrajectory(
        construct_id="english:construct:v2",
        origin_id="origin:" + path_id,
        path_id=path_id,
        steps=steps,
        provenance_ids=["source:fixture"],
    )


def test_order_and_multiplicity_are_load_bearing():
    a = make("a", [
        SemanticStep("many", "relate", "system"),
        SemanticStep("system", "recurs", "system"),
        SemanticStep("system", "recurs", "system"),
    ])
    b = make("b", [
        SemanticStep("system", "recurs", "system"),
        SemanticStep("many", "relate", "system"),
        SemanticStep("system", "recurs", "system"),
    ])
    assert a.relation_signature != b.relation_signature
    assert a.receipt_sha256 != b.receipt_sha256


def test_comparison_input_carries_complete_steps():
    t = make("x", [SemanticStep("axis:a", "rel:r", "axis:b")])
    payload = t.to_ucns_comparison_input()
    assert payload["construct_id"] == "english:construct:v2"
    assert payload["origin_id"] == "origin:x"
    assert payload["path_id"] == "x"
    assert payload["steps"] == [
        {"axis_id": "axis:a", "relation_id": "rel:r", "target_axis_id": "axis:b"}
    ]
    assert payload["provenance_ids"] == ["source:fixture"]


def test_no_downstream_judgment_is_encoded():
    payload = make("x", [SemanticStep("a", "r", "b")]).to_ucns_comparison_input()
    forbidden = {"equivalent", "analogous", "recurrence", "proof_status", "measurement"}
    assert forbidden.isdisjoint(payload)


def test_mutable_inputs_are_frozen_before_identity():
    steps = [SemanticStep("a", "r", "b")]
    provenance = ["source:fixture"]
    t = SystemSetTrajectory("c", "o", "p", steps, provenance)
    before = t.receipt_sha256
    steps.append(SemanticStep("b", "r", "c"))
    provenance.append("source:later")
    assert t.receipt_sha256 == before
    assert len(t.steps) == 1
    assert t.provenance_ids == ("source:fixture",)
