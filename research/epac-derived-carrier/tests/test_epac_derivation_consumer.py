# Stack-local EPAC-derived-carrier checks; not EPAC implementation tests.
# === CHECKS ===
# id: check_derived_carrier_binds_exact_epac_source
#   proves: derived_carrier_binds_exact_epac_source
#   call: self::test_binds_exact_epac_source
#   requires: python3, git
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_derived_carrier_uses_construction_not_lookup
#   proves: derived_carrier_uses_construction_not_lookup
#   call: self::test_uses_construction_not_lookup
#   requires: python3, git
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_derived_carrier_reruns_collision_transition_provenance_generalization
#   proves: derived_carrier_reruns_collision_transition_provenance_generalization
#   call: self::test_reruns_collision_transition_provenance_generalization
#   requires: python3, git
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_derived_carrier_preserves_bounded_ligand_field_energy_selection
#   proves: derived_carrier_preserves_bounded_ligand_field_energy_selection
#   call: self::test_generative_gate_retains_bounded
#   requires: python3, git
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from epac_derivation_consumer import (
    SCHEMA,
    DerivedCarrierError,
    build_derived_carrier,
    replay_derived_carrier,
)

EPAC_SOURCE_ROOT = Path(
    os.environ.get("EPAC_SOURCE_ROOT", "/tmp/epac-quantum")
)


def test_binds_exact_epac_source() -> None:
    report = build_derived_carrier(EPAC_SOURCE_ROOT)
    assert report["epac_source_commit"] == "efa2079db4a431092808b21643654ebe56140348"
    assert report["source_bytes_verified"] is True

    data = json.dumps(report, sort_keys=True, separators=(",", ":")).encode("utf-8")
    replayed = replay_derived_carrier(data, EPAC_SOURCE_ROOT)
    assert replayed["receipt_sha256"] == report["receipt_sha256"]

    tampered = bytearray(data)
    tampered[40] ^= 0x01
    with pytest.raises(DerivedCarrierError):
        replay_derived_carrier(bytes(tampered), EPAC_SOURCE_ROOT)


def test_generative_gate_retains_bounded() -> None:
    report = build_derived_carrier(EPAC_SOURCE_ROOT)
    gate = report["generative_gate"]
    assert gate["frozen_rule_reproduces_nine"] is True
    assert gate["transition_metal_failure_recorded"] is True
    assert gate["decision"] == "RETAIN-BOUNDED"
    assert gate["standing"] == "bounded constitutive carrier"
    assert gate["supported_domain"] == [
        "bare atoms",
        "ions",
        "diatomics",
        "singleton-center star topologies",
    ]
    # Multi-center topologies outside the declared domain remain declined.
    assert "outside-supported-domain" in gate["held_out_statuses"]["C2H2"]
    # NH4+ counts ligand K only and evaluates to (3,5,4), not 7
    assert gate["held_out_statuses"]["NH4+"] == "evaluation-only"
    # The construction supplies a 4s/3d/4p basis, but bond-context
    # participation and coordination capacity remain explicitly unresolved.
    assert gate["active_orbital_basis_constructed_for_supplied_topologies"] is True
    assert gate["bond_context_orbital_participation"] == "UNRESOLVED"
    assert gate["coordination_capacity"] == "UNRESOLVED"
    assert gate["capacity_rule_status"] == "FALSIFIED"
    assert gate["topology_formation"] == "downstream, not tested here"
    by_topology = {
        entry["topology"]: entry
        for entry in gate["transition_metal_topology_evaluations"]
    }
    assert by_topology["ScCl3"]["b_value"] == [3, 4, 3]
    sc_active = by_topology["ScCl3"]["center_active_orbital_set"]
    assert [sub["subshell"] for sub in sc_active["subshells"]] == ["4s", "3d", "4p"]
    assert sc_active["coordination_capacity"] == "UNRESOLVED"
    # Zn2+ regression: d10 has zero unpaired electrons
    zn_active = by_topology["ZnCl2"]["center_active_orbital_set"]
    assert zn_active["unpaired_electrons"] == 0
    zn_subshells = {sub["subshell"]: sub for sub in zn_active["subshells"]}
    assert zn_subshells["3d"]["electrons"] == 10
    assert zn_subshells["4p"]["electrons"] == 0

    # High/low-spin behavior now follows exact model-energy minimization,
    # while equal-energy distinct candidates fail closed as unresolved.
    controls = {
        (entry["delta_o_input"], entry["pairing_energy_input"]): entry
        for entry in gate["ligand_field_energy_controls"]
    }
    assert controls[("1", "2")]["selected_regime"] == "high"
    assert controls[("1", "2")]["unpaired_electrons"] == 5
    assert controls[("2", "1")]["selected_regime"] == "low"
    assert controls[("2", "1")]["unpaired_electrons"] == 1
    assert (
        controls[("1", "1")]["ligand_field_regime_derivation"]
        == "UNRESOLVED_DEGENERATE"
    )
    assert controls[("1", "1")]["unpaired_electrons"] is None
    assert gate["ligand_field_regime_derivation"] == "CONDITIONAL_ON_SUPPLIED_ENERGIES"
    assert gate["ligand_field_energy_inputs_derivation"] == "UNRESOLVED"
    assert gate["spin_regime_input_used"] is False
    assert "not an empirical ground-state predictor" in gate["ligand_field_model_scope"]
    assert gate["spectrochemical_lookup_used"] is False
    assert gate["topology_formation_derived"] is False
    assert gate["remaining_unresolved"] == [
        "bond-context orbital participation (including 4p)",
        "delta_o and pairing-energy derivation from bond context",
        "coordination capacity",
        "topology formation",
    ]


def test_uses_construction_not_lookup() -> None:
    report = build_derived_carrier(EPAC_SOURCE_ROOT)
    assert report["lookup_used"] is False
    for symbol, entry in report["derived_period_valence"].items():
        assert entry["lookup_used"] is False
        assert entry["period"] > 0
        assert entry["valence_electrons"] > 0


def test_reruns_collision_transition_provenance_generalization() -> None:
    report = build_derived_carrier(EPAC_SOURCE_ROOT)
    assert report["schema"] == SCHEMA
    assert report["b_classes"] == 16
    assert report["collisions_separated"] is True
    assert report["transitions_preserved"] is True
    assert len(report["locked_transitions"]) == 9
    for transition in report["locked_transitions"]:
        assert transition["provenance_preserved"] is True
    # Generalization: all 18 symbols get derived period and valence; the
    # nine required symbols are carrier-admitted, the rest remain
    # B-declined.
    generalization = report["generalization"]
    assert len(generalization) == 18
    admitted = {entry["symbol"] for entry in generalization if entry["carrier_status"] == "derived"}
    assert admitted == {"H", "B", "C", "F", "N", "O", "P", "S", "Si"}
    for entry in generalization:
        if entry["carrier_status"] != "derived":
            assert entry["carrier_status"] == "period-valence-derived-B-declined"
    # Promotion gate: period and valence derive from epac_atomic and all
    # carrier tests survive, so the carrier promotes.
    gate = report["promotion_gate"]
    assert gate["decision"] == "PROMOTE"
    assert gate["standing"] == "EPAC-derived constitutive carrier"
    assert gate["remaining_unresolved"] == "B for unseen states is not yet derived"
