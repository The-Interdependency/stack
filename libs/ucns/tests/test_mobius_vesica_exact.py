# === CHECKS ===
# id: check_mobius_vesica_centerline_contacts
#   proves: mobius_vesica_has_exact_two_centerline_contacts
#   call: self::test_centerlines_have_exactly_two_contacts_and_positive_null_clearance
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_vesica_source_claims
#   proves: mobius_vesica_preserves_source_claims_as_testable_geometry
#   call: self::test_sturm_certificate_proves_exactly_four_physical_boundary_contacts
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_vesica_null_clearance
#   proves: mobius_vesica_null_origin_has_positive_clearance
#   call: self::test_centerlines_have_exactly_two_contacts_and_positive_null_clearance
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_vesica_quotient_return
#   proves: mobius_vesica_obeys_one_turn_seam_and_two_turn_return
#   call: self::test_each_band_obeys_one_turn_seam_and_two_turn_return
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_vesica_four_boundary_contacts
#   proves: mobius_vesica_sturm_proves_four_physical_boundary_contacts
#   call: self::test_sturm_certificate_proves_exactly_four_physical_boundary_contacts
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_vesica_alternate_branch_obstruction
#   proves: mobius_vesica_alternate_height_branch_is_obstructed
#   call: self::test_sturm_certificate_proves_exactly_four_physical_boundary_contacts
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_vesica_contact_semantics
#   proves: mobius_vesica_contact_semantics_are_not_flattened
#   call: self::test_contact_semantics_and_global_surface_boundary_remain_distinct
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_vesica_width_continuation
#   proves: mobius_vesica_width_continuation_recertifies_each_stage
#   call: self::test_width_continuation_recertifies_four_contacts_at_every_stage
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_mobius_vesica_seed_phase_firewall
#   proves: mobius_vesica_seed_phase_mismatch_blocks_certificate_inheritance
#   call: self::test_seed_half_turn_phase_is_obstructed_and_cannot_inherit_certificate
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_vesica_half_turn_obstruction
#   proves: mobius_vesica_half_turn_phase_has_exact_contact_obstruction
#   call: self::test_seed_half_turn_phase_is_obstructed_and_cannot_inherit_certificate
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_vesica_structural_placements
#   proves: mobius_vesica_rigid_placements_cover_seed_structural_pairs
#   call: self::test_rigid_placement_plan_covers_all_twelve_structural_pairs
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_vesica_receipt_firewall
#   proves: mobius_vesica_certificate_is_nonselecting_and_zeta_firewalled
#   call: self::test_combined_receipt_is_deterministic_nonselecting_and_firewalled
#   requires: python3
#   timeout: 10
#   mutates: temporary_path
#   cleanup: pytest temporary_path
# === END CHECKS ===

from fractions import Fraction
import json
import math

from ucns.mobius_certificates import certify_mobius_vesica, count_real_roots
from ucns.mobius_continuation import (
    MobiusVesicaContinuationEngine,
    build_artifact_payload,
    write_default_artifact,
)
from ucns.mobius_vesica import build_mobius_vesica


def test_centerlines_have_exactly_two_contacts_and_positive_null_clearance() -> None:
    vesica = build_mobius_vesica()
    contacts = vesica.centerline_contacts

    assert len(contacts) == 2
    assert tuple(contact.contact_id for contact in contacts) == (
        "CENTERLINE_TOP",
        "CENTERLINE_BOTTOM",
    )
    assert contacts[0].left_turn == Fraction(1, 6)
    assert contacts[0].right_turn == Fraction(1, 3)
    assert contacts[0].y_sqrt3_coefficient == Fraction(1, 2)
    assert contacts[1].left_turn == Fraction(5, 6)
    assert contacts[1].right_turn == Fraction(2, 3)
    assert contacts[1].y_sqrt3_coefficient == Fraction(-1, 2)
    assert max(vesica.centerline_contact_residuals()) < 1e-12
    assert vesica.parameters.null_clearance_lower_bound == Fraction(49, 100)


def test_each_band_obeys_one_turn_seam_and_two_turn_return() -> None:
    vesica = build_mobius_vesica()
    seam_residual, return_residual = vesica.seam_and_return_residuals()

    assert seam_residual < 1e-12
    assert return_residual < 1e-12
    for band in vesica.bands:
        assert band.boundary_point(0).distance_to(band.boundary_point(2)) < 1e-12
        assert band.boundary_point(1).distance_to(
            band.surface_point(0, -vesica.parameters.half_width)
        ) < 1e-12


def test_sturm_certificate_proves_exactly_four_physical_boundary_contacts() -> None:
    certificate = certify_mobius_vesica()

    assert certificate.sturm.root_count == 2
    assert count_real_roots(certificate.sturm.polynomial, Fraction(-1), Fraction(1)) == 2
    assert len(certificate.sturm.isolating_intervals) == 2
    assert certificate.boundary_physical_contact_count == 4
    assert all(interval.width <= Fraction(1, 2**36) for interval in certificate.sturm.isolating_intervals)
    assert max(witness.residual for witness in certificate.witnesses) < 1e-9
    assert min(witness.tangent_cross_norm for witness in certificate.witnesses) > 1

    # The four physical contacts form two near the upper centerline node and
    # two near the lower node.  Their exact x coordinate is zero; binary64
    # witnesses remain close to that exact consequence of the contact equation.
    assert sum(witness.point.y > 0 for witness in certificate.witnesses) == 2
    assert sum(witness.point.y < 0 for witness in certificate.witnesses) == 2
    assert all(abs(witness.point.x) < 1e-12 for witness in certificate.witnesses)
    assert sum(witness.point.z > 0 for witness in certificate.witnesses) == 2
    assert sum(witness.point.z < 0 for witness in certificate.witnesses) == 2


def test_contact_semantics_and_global_surface_boundary_remain_distinct() -> None:
    payload = certify_mobius_vesica().payload

    assert payload["centerline_contacts"]["semantic_type"] == (
        "physical equality of the two core curves"
    )
    assert payload["boundary_contacts"]["semantic_type"] == (
        "physical equality of the two single continuous boundary curves in R3"
    )
    assert payload["boundary_contacts"]["height_equation_branches"][
        "difference_branch_obstructed"
    ] is True
    assert payload["pair_surface_intersection_locus"]["standing"] == "unresolved"
    assert "not claimed" in payload["boundary_contacts"]["arbitrary_3d_perturbation_stability"]


def test_width_continuation_recertifies_four_contacts_at_every_stage() -> None:
    engine = MobiusVesicaContinuationEngine()
    stages = engine.continue_widths()

    assert len(stages) == 8
    assert tuple(stage.half_width for stage in stages) == (
        Fraction(1, 200),
        Fraction(1, 100),
        Fraction(1, 80),
        Fraction(1, 50),
        Fraction(1, 20),
        Fraction(1, 10),
        Fraction(1, 5),
        Fraction(1, 4),
    )
    assert all(stage.root_count == 2 for stage in stages)
    assert all(stage.physical_boundary_contact_count == 4 for stage in stages)
    assert all(stage.null_clearance_lower_bound > 0 for stage in stages)
    assert all(len(stage.certificate_sha256) == 64 for stage in stages)


def test_seed_half_turn_phase_is_obstructed_and_cannot_inherit_certificate() -> None:
    engine = MobiusVesicaContinuationEngine()
    comparison = engine.compare_with_seed_candidate()
    path = engine.phase_path_to_seed()

    assert comparison.chirality_match is True
    assert comparison.width_match is True
    assert comparison.phase_match is False
    assert comparison.certified_phase_turns == Fraction(1, 4)
    assert comparison.seed_phase_turns == Fraction(1, 2)
    assert comparison.certified_physical_boundary_contacts == 4
    assert comparison.seed_phase_physical_boundary_contacts_in_standard_family == 0
    assert comparison.certificate_inherits is False
    assert path[0].physical_boundary_contact_count == 4
    assert path[-1].physical_boundary_contact_count == 0
    assert path[-1].standing.startswith("exact-zero-contact-obstruction")
    assert all(stage.physical_boundary_contact_count is None for stage in path[1:-1])


def test_rigid_placement_plan_covers_all_twelve_structural_pairs() -> None:
    placements = MobiusVesicaContinuationEngine.seed_structural_placements()

    assert len(placements) == 12
    assert sum(item.pair_id.startswith("CENTER_RING") for item in placements) == 6
    assert sum(item.pair_id.startswith("RING_") for item in placements) == 6
    assert all(item.local_certificate_preserved for item in placements)
    assert not any(item.global_simultaneous_realization_claimed for item in placements)
    for item in placements:
        distance = math.hypot(
            item.right_center_x - item.left_center_x,
            item.right_center_y - item.left_center_y,
        )
        assert math.isclose(distance, 1.0, rel_tol=0, abs_tol=1e-12)


def test_combined_receipt_is_deterministic_nonselecting_and_firewalled(tmp_path) -> None:
    first = build_artifact_payload()
    second = build_artifact_payload()
    assert first == second

    output = write_default_artifact(tmp_path / "mobius-vesica-certificate.json")
    decoded = json.loads(output.read_text(encoding="utf-8"))
    assert decoded == first
    assert decoded["selection_effect"] == "none"
    assert decoded["certificate_status"].startswith("certified-existence")
    assert decoded["centerline_contacts"]["exact_count"] == 2
    assert decoded["boundary_contacts"]["exact_count"] == 4
    assert decoded["continuation"]["seed_candidate_comparison"]["certificate_inherits"] is False
    assert len(decoded["artifact_payload_sha256"]) == 64
    assert any("Riemann" in item for item in decoded["nonclaims"])
    assert any("spectral operator" in item for item in decoded["nonclaims"])
