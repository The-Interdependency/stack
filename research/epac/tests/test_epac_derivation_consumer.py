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
    assert report["epac_source_commit"].startswith("db3e158")
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
    assert gate["missing_state_variable"] == "bond-context active-orbital set (may include (n-1)d)"
    assert gate["decision"] == "RETAIN-BOUNDED"
    assert gate["standing"] == "bounded constitutive carrier"
    assert gate["supported_domain"] == [
        "bare atoms",
        "ions",
        "diatomics",
        "singleton-center star topologies",
    ]
    # symmetric multi-center held-out molecules are outside the supported domain
    assert "outside-supported-domain" in gate["held_out_statuses"]["C2H2"]
    # NH4+ counts ligand K only and evaluates to (3,5,4), not 7
    assert gate["held_out_statuses"]["NH4+"] == "evaluation-only"
    # active-orbital set derived for supplied transition-metal topologies
    assert gate["active_orbital_set_derived_for_supplied_topologies"] is True
    assert gate["topology_formation"] == "downstream, not tested here"
    by_topology = {
        entry["topology"]: entry
        for entry in gate["transition_metal_topology_evaluations"]
    }
    assert by_topology["ScCl3"]["b_value"] == [3, 4, 3]
    assert by_topology["ScCl3"]["center_active_orbital_set"]["subshells"] == ["4s", "3d"]


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
