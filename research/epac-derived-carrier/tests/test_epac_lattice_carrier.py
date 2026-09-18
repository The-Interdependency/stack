# Stack-local EPAC-derived-carrier checks; not EPAC implementation tests.
# === CHECKS ===
# id: check_epac_carrier_is_constitutive_discrete
#   proves: epac_carrier_is_constitutive_discrete
#   call: self::test_is_constitutive_discrete
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_epac_carrier_b_is_projection
#   proves: epac_carrier_b_is_projection
#   call: self::test_b_is_projection
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_epac_carrier_separates_known_collisions
#   proves: epac_carrier_separates_known_collisions
#   call: self::test_separates_known_collisions
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_epac_carrier_preserves_transitions_and_provenance
#   proves: epac_carrier_preserves_transitions_and_provenance
#   call: self::test_preserves_transitions_and_provenance
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_epac_carrier_does_not_invent_unseen_states
#   proves: epac_carrier_does_not_invent_unseen_states
#   call: self::test_does_not_invent_unseen_states
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_epac_carrier_remains_candidate
#   proves: epac_carrier_remains_candidate
#   call: self::test_remains_candidate
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from epac_lattice_carrier import (
    SCHEMA,
    SCHEMA_MINKOWSKI,
    LOCKED_FORMULAS,
    build_constitutive_discrete_carrier,
    build_minkowski_backend,
)


def test_is_constitutive_discrete() -> None:
    report = build_constitutive_discrete_carrier()
    assert report["schema"] == SCHEMA
    for state in report["states"]:
        assert len(state["coordinates"]) == 5, state


def test_b_is_projection() -> None:
    report = build_constitutive_discrete_carrier()
    documented_b = {
        "subatomic:H": [3, 2, 0],
        "subatomic:B": [3, 3, 0],
        "subatomic:C": [3, 3, 0],
        "subatomic:F": [3, 3, 0],
        "subatomic:N": [3, 3, 0],
        "subatomic:O": [3, 3, 0],
        "subatomic:P": [3, 4, 0],
        "subatomic:S": [3, 4, 0],
        "subatomic:Si": [3, 4, 0],
        "element:H": [3, 2, 0],
        "element:B": [3, 6, 0],
        "element:C": [3, 7, 0],
        "element:N": [3, 8, 0],
        "element:O": [3, 9, 0],
        "element:F": [3, 10, 0],
        "element:Si": [3, 15, 0],
        "element:P": [3, 16, 0],
        "element:S": [3, 17, 0],
        "molecule:H2": [3, 2, 2],
        "molecule:H2O": [3, 3, 2],
        "molecule:NH3": [3, 4, 3],
        "molecule:CH4": [3, 5, 4],
        "molecule:CO2": [3, 3, 4],
        "molecule:H2S": [3, 3, 2],
        "molecule:BF3": [3, 4, 3],
        "molecule:PH3": [3, 4, 3],
        "molecule:SiH4": [3, 5, 4],
    }
    by_state = {state["state"]: state for state in report["states"]}
    assert len(by_state) == 27
    for state, b in documented_b.items():
        assert by_state[state]["B"] == b, state


def test_separates_known_collisions() -> None:
    report = build_constitutive_discrete_carrier()
    assert report["collisions_separated"] is True
    assert report["b_classes"] == 16
    for group in report["collision_groups"].values():
        coordinates = [tuple(point["coordinates"]) for point in group]
        assert len(set(coordinates)) == len(coordinates)


def test_preserves_transitions_and_provenance() -> None:
    report = build_constitutive_discrete_carrier()
    assert report["transitions_preserved"] is True
    assert len(report["locked_transitions"]) == 9
    by_state = {state["state"]: state for state in report["states"]}
    for transition in report["locked_transitions"]:
        constituent_sum = [0] * 5
        for symbol in transition["constituents"]:
            element = by_state[f"element:{symbol}"]
            constituent_sum = [
                a + b for a, b in zip(constituent_sum, element["coordinates"])
            ]
        assert constituent_sum == transition["constituent_sum"]
        molecule = by_state[transition["molecule"]["state"]]
        rebuilt = [
            a + b
            for a, b in zip(constituent_sum, transition["formula_vector"])
        ]
        assert rebuilt == molecule["coordinates"]
        assert transition["provenance_preserved"] is True


def test_does_not_invent_unseen_states() -> None:
    report = build_constitutive_discrete_carrier()
    generalization = report["generalization_audit"]
    assert generalization["unseen_states_declined"] == 18
    for entry in generalization["declined"]:
        assert entry["declined"] is True
    sigma = report["sigma_audit"]
    assert sigma["epac_internal"] is True
    assert sigma["bare_scale_is_name"] is True
    assert sigma["molecule_scale_is_compositional"] is True


def test_remains_candidate() -> None:
    report = build_constitutive_discrete_carrier()
    assert "hmmm" in report["hmmm"]
    backend = build_minkowski_backend()
    assert backend["schema"] == SCHEMA_MINKOWSKI
    assert backend["separation_relevance"] == "none; field structure contributes nothing"
    assert report["receipt_sha256"]
