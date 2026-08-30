"""Checks for the catalog-bound three-phase electromagnetic-pipe release surface."""

# === CHECKS ===
# id: check_pipe_control_topology
#   proves: metapat_pipe_control_topology_exact
#   call: self::test_pipe_control_topology_exact
#   mutates: none
#   cleanup: none
#
# id: check_pipe_winding_layers
#   proves: metapat_pipe_winding_layers_exact
#   call: self::test_pipe_winding_layers_exact
#   mutates: none
#   cleanup: none
#
# id: check_pipe_attractors_not_bearings
#   proves: metapat_pipe_attractors_not_bearings
#   call: self::test_pipe_attractors_not_bearings
#   mutates: none
#   cleanup: none
#
# id: check_pipe_alloy_search
#   proves: metapat_pipe_alloy_search_bounded
#   call: self::test_pipe_alloy_search_bounded
#   mutates: none
#   cleanup: none
#
# id: check_pipe_catalog_binding
#   proves: metapat_pipe_application_catalog_bound
#   call: self::test_pipe_application_catalog_bound
#   mutates: none
#   cleanup: none
#
# id: check_pipe_source_current
#   proves: metapat_pipe_source_current
#   call: self::test_pipe_source_current
#   mutates: filesystem_read
#   cleanup: none
#
# id: check_pipe_performance_firewall
#   proves: metapat_pipe_performance_firewall
#   call: self::test_pipe_performance_firewall
#   mutates: none
#   cleanup: none
#
# id: check_pipe_roundtrip
#   proves: metapat_pipe_roundtrip_strict
#   call: self::test_pipe_roundtrip_strict
#   mutates: none
#   cleanup: none
#
# id: check_pipe_fixture_rendered
#   proves: metapat_pipe_fixture_generated
#   call: self::test_pipe_fixture_renderer_is_deterministic
#   mutates: none
#   cleanup: none
#
# id: check_pipe_fixture_current
#   proves: metapat_pipe_fixture_current
#   call: self::test_packaged_pipe_fixture_matches_live_constructor
#   mutates: filesystem_read
#   cleanup: none
# === END CHECKS ===

import json
from importlib.resources import files
from pathlib import Path

import pytest

import metapat
from metapat.electromagnetic_pipe import AlloyCandidate, ElectromagneticPipeDesign
from tools.generate_application_fixtures import render_electromagnetic_pipe_fixture


def test_pipe_control_topology_exact() -> None:
    design = metapat.electromagnetic_pipe_design()
    assert design.assembly_length_m == 3.0
    assert design.outer_pipe_diameter_in == 3.0
    assert design.radial_layer_count == 3
    assert design.handednesses == ("clockwise", "widdershins")
    assert design.phases_per_handedness == 3
    assert design.phase_circuit_count == 18
    assert design.three_phase_system_count == 6
    assert design.control_object == "one three-phase vector per handedness per radial layer"
    assert design.current_command_variable == "phase current"
    assert design.voltage_role == "compliance"


def test_pipe_winding_layers_exact() -> None:
    design = metapat.electromagnetic_pipe_design()
    assert tuple(
        (layer.layer_name, layer.wire_awg, layer.turns_per_inch)
        for layer in design.winding_layers
    ) == (("outer", 12, 6), ("middle", 16, 12), ("inner", 20, 18))
    assert all(layer.clockwise_phase_count == 3 for layer in design.winding_layers)
    assert all(layer.widdershins_phase_count == 3 for layer in design.winding_layers)
    assert sum(layer.phase_circuit_count for layer in design.winding_layers) == 18
    assert sum(layer.three_phase_system_count for layer in design.winding_layers) == 6


def test_pipe_attractors_not_bearings() -> None:
    design = metapat.electromagnetic_pipe_design()
    assert design.mobile_element_designation == "ceramic-coated magnetic eddy-current attractors"
    assert design.prohibited_mobile_element_designation == "bearings"
    assert "bearing" not in design.mobile_element_designation.lower()
    assert "field-history response" in design.mobile_element_effects
    assert "cluster" in design.mobile_element_behaviors


def test_pipe_alloy_search_bounded() -> None:
    design = metapat.electromagnetic_pipe_design()
    assert len(design.alloy_candidates) == 5
    for candidate in design.alloy_candidates:
        assert candidate.basis == "atomic percent"
        assert candidate.iron + candidate.cobalt + candidate.nickel == 75.0
        assert candidate.chromium == 15.0
        assert candidate.manganese == 10.0
        assert (
            candidate.iron
            + candidate.cobalt
            + candidate.nickel
            + candidate.chromium
            + candidate.manganese
        ) == 100.0
    with pytest.raises(ValueError, match=r"Fe \+ Co \+ Ni"):
        AlloyCandidate("invalid", 40, 20, 10, 20, 10)


def test_pipe_application_catalog_bound() -> None:
    catalog = metapat.canonical_semantic_catalog()
    application = metapat.electromagnetic_pipe_application_module(catalog)
    metapat.validate_application_against_catalog(application, catalog)
    assert application.claim_status == "EMPIRICAL-FRONTIER"
    assert application.root_impact == "none"
    assert len(application.catalog_bindings) == 20
    assert len({binding.module_id for binding in application.catalog_bindings}) == 20
    assert "metapat.theory.10.symbolic_and_memetic_transfer" not in {
        binding.module_id for binding in application.catalog_bindings
    }


def test_pipe_source_current() -> None:
    application = metapat.electromagnetic_pipe_application_module()
    metapat.assert_application_sources_match(Path(__file__).resolve().parents[1], application)
    assert any("six three-phase systems" in text for text in application.source_statements)
    assert any("not bearings" in text for text in application.source_statements)
    assert any("No fixed protection distance" in text for text in application.source_statements)


def test_pipe_performance_firewall() -> None:
    design = metapat.electromagnetic_pipe_design()
    application = design.application
    assert application.metapat_validity_claim is False
    assert application.domain_validity_claim is False
    assert application.measurement_validity_claim is False
    assert application.ucns_theorem_status_transfer is False
    assert application.ucns_topology_claim is False
    assert design.electromagnetic_validity_claim is False
    assert design.alloy_validity_claim is False
    assert design.insulation_validity_claim is False
    assert design.fault_containment_validity_claim is False
    assert design.spacecraft_safety_validity_claim is False
    assert design.protection_distance_status.startswith("No fixed protection distance")


def test_pipe_roundtrip_strict() -> None:
    design = metapat.electromagnetic_pipe_design()
    reconstructed = ElectromagneticPipeDesign.from_json(design.to_json())
    assert reconstructed == design
    assert json.loads(reconstructed.to_json()) == json.loads(design.to_json())

    unknown = design.to_dict()
    unknown["ideal_alloy"] = "claimed"
    with pytest.raises(ValueError, match="unknown pipe-design fields"):
        ElectromagneticPipeDesign.from_dict(unknown)

    tampered = design.to_dict()
    tampered["phase_circuit_count"] = 17
    with pytest.raises(ValueError, match="phase_circuit_count"):
        ElectromagneticPipeDesign.from_dict(tampered)

    changed = design.to_dict()
    changed["protection_distance_status"] = "known"
    with pytest.raises(ValueError, match="design_digest"):
        ElectromagneticPipeDesign.from_dict(changed)


def test_pipe_fixture_renderer_is_deterministic() -> None:
    rendered = render_electromagnetic_pipe_fixture()
    assert rendered.endswith("\n")
    assert rendered.count("\n") == 1
    assert rendered == render_electromagnetic_pipe_fixture()
    assert ElectromagneticPipeDesign.from_json(rendered.strip()) == metapat.electromagnetic_pipe_design()


def test_packaged_pipe_fixture_matches_live_constructor() -> None:
    fixture = files("metapat").joinpath("fixtures/three-phase-electromagnetic-pipe-v2.json")
    assert fixture.is_file()
    assert fixture.read_text(encoding="utf-8") == render_electromagnetic_pipe_fixture()
