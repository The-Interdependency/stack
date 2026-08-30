# === CHECKS ===
# id: check_prime_generic_diagram_fixed
#   proves: prime_generic_diagram_is_fixed_before_invariants
#   call: self::test_generic_projection_preserves_positive_isotopy_clearance
#   requires: python3, mpmath
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_prime_generic_pairwise_linking
#   proves: prime_generic_diagram_preserves_pairwise_linking
#   call: self::test_generic_diagrams_reproduce_complete_linking_matrices
#   requires: python3, mpmath
#   timeout: 60
#   mutates: none
#   cleanup: none
#
# id: check_prime_borromean_magnus
#   proves: prime_magnus_benchmark_recovers_borromean_integer
#   call: self::test_borromean_magnus_benchmark_is_unit
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_prime_p7_exact_milnor_zero
#   proves: prime_p7_five_milnor_candidates_are_exact_zero_in_diagram
#   call: self::test_all_five_p7_milnor_coefficients_are_exact_zero
#   requires: python3, mpmath
#   timeout: 60
#   mutates: none
#   cleanup: none
#
# id: check_prime_phase_preregistration_hash
#   proves: prime_phase_selector_matches_frozen_preregistration
#   call: self::test_preregistration_hash_and_selector_order_are_frozen
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_prime_phase_whole_link_selector
#   proves: prime_phase_selector_uses_whole_link_character
#   call: self::test_preregistered_selector_outputs_are_not_target_fitted
#   requires: python3, mpmath
#   timeout: 120
#   mutates: none
#   cleanup: none
#
# id: check_prime_fox_complete_fingerprint
#   proves: prime_fox_fingerprint_covers_all_prime_characters
#   call: self::test_fox_rank_fingerprints_cover_every_prime_character
#   requires: python3, mpmath
#   timeout: 120
#   mutates: none
#   cleanup: none
#
# id: check_prime_exact_receipt_nonselecting
#   proves: prime_exact_milnor_alexander_receipt_is_nonselecting
#   call: self::test_family_receipt_is_deterministic_bounded_and_nonselecting
#   requires: python3, mpmath
#   timeout: 180
#   mutates: temporary_path
#   cleanup: pytest temporary_path
# === END CHECKS ===

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from ucns.prime_exact_milnor_alexander import (
    PREREGISTRATION_SHA256,
    borromean_magnus_benchmark,
    build_generic_prime_five_diagram,
    build_generic_prime_seven_diagram,
    evaluate_preregistered_phase_selector,
    exact_milnor_alexander_family_certificate,
    exact_p7_milnor_certificates,
    fox_rank_fingerprint,
    common_field_fox_rank_fingerprint,
    write_exact_milnor_alexander_family_certificate,
)


def test_generic_projection_preserves_positive_isotopy_clearance() -> None:
    for diagram in (
        build_generic_prime_seven_diagram(),
        build_generic_prime_five_diagram(),
    ):
        assert float(diagram.maximum_component_displacement) < 0.00425
        assert float(diagram.maximum_relative_displacement) < 0.00850
        assert float(diagram.isotopy_ribbon_clearance_lower_bound) > 0.061
        assert float(diagram.minimum_height_gap) > 0.09
        assert float(diagram.minimum_transversality) > 0.05
        assert float(diagram.minimum_distinct_crossing_point_gap) > 0.0001
        assert diagram.crossing_count == diagram.generator_count
        assert diagram.crossing_count == diagram.relation_count


def test_generic_diagrams_reproduce_complete_linking_matrices() -> None:
    p7 = build_generic_prime_seven_diagram()
    p5 = build_generic_prime_five_diagram()

    assert p7.crossing_count == 38
    assert p7.pairwise_linking_matrix == (
        (0, 1, 1, 1, 1, 1, 1),
        (1, 0, 0, 0, 0, 0, 0),
        (1, 0, 0, 1, 1, 0, 0),
        (1, 0, 1, 0, 1, 1, 0),
        (1, 0, 1, 1, 0, 1, 1),
        (1, 0, 0, 1, 1, 0, 0),
        (1, 0, 0, 0, 1, 0, 0),
    )
    assert p5.crossing_count == 18
    assert p5.pairwise_linking_matrix == (
        (0, 0, 0, 0, 0),
        (0, 0, 0, 0, 0),
        (0, 0, 0, 1, 0),
        (0, 0, 1, 0, 1),
        (0, 0, 0, 1, 0),
    )


def test_borromean_magnus_benchmark_is_unit() -> None:
    assert borromean_magnus_benchmark() == 1


def test_all_five_p7_milnor_coefficients_are_exact_zero() -> None:
    certificates = exact_p7_milnor_certificates()
    assert len(certificates) == 5
    assert all(certificate.exact_zero for certificate in certificates)
    assert all(certificate.coefficient_ij_in_longitude_k == 0 for certificate in certificates)
    assert all(certificate.coefficient_ji_in_longitude_k == 0 for certificate in certificates)
    assert all(certificate.longitude_degree_one == (0, 0, 0) for certificate in certificates)


def test_preregistration_hash_and_selector_order_are_frozen() -> None:
    root = Path(__file__).resolve().parents[1]
    document = root / "docs" / "PREREGISTRATION_P7_PHASE_ALEXANDER.md"
    assert hashlib.sha256(document.read_bytes()).hexdigest() == PREREGISTRATION_SHA256
    record = json.loads(
        (root / "generated" / "p7-exact-milnor-alexander-preregistration.json").read_text(
            encoding="utf-8"
        )
    )
    assert record["document_sha256"] == PREREGISTRATION_SHA256
    assert record["evaluation_status"] == "not-yet-run-at-freeze"


def test_preregistered_selector_outputs_are_not_target_fitted() -> None:
    p7 = evaluate_preregistered_phase_selector(7)
    p5 = evaluate_preregistered_phase_selector(5)

    assert p7.selected_winding == 3
    assert p7.selected_outer_numerator == 4
    assert p7.selected_fox_excess_nullity == 1
    assert str(p7.selected_alignment_energy) == "599/196"
    assert p7.selected_boundary_meridional_degree == 7
    assert p7.co_winners_before_neutral_tiebreak == ((3, 4), (9, 4))

    assert p5.selected_winding == -3
    assert p5.selected_outer_numerator == 1
    assert p5.selected_fox_excess_nullity == 2
    assert str(p5.selected_alignment_energy) == "39/20"
    assert p5.selected_boundary_meridional_degree == -5
    assert p5.co_winners_before_neutral_tiebreak == ((-3, 1), (9, 1))

    assert abs(p7.selected_boundary_meridional_degree) == 7
    assert abs(p5.selected_boundary_meridional_degree) == 5
    assert p7.as_dict()["target_degree_not_used"] is True
    assert p5.as_dict()["target_degree_not_used"] is True


def test_fox_rank_fingerprints_cover_every_prime_character() -> None:
    p7 = fox_rank_fingerprint(7)
    p5 = fox_rank_fingerprint(5)

    assert len(p7.rows) == 42
    assert p7.histogram == {"0": 18, "1": 24}
    assert p7.ordered_rank_vector_sha256 == (
        "ce6657419a659cac667bb4a377181951352346e4cc94525e1f1ef8297d66fff4"
    )
    assert len(p5.rows) == 20
    assert p5.histogram == {"2": 20}
    assert p5.ordered_rank_vector_sha256 == (
        "c6d2f7f443e150c2941aea4634b8de19f77f9c082dfc9f48d9efc04029971661"
    )
    assert p7.ordered_rank_vector_sha256 != p5.ordered_rank_vector_sha256

    p7_common = common_field_fox_rank_fingerprint(7)
    p5_common = common_field_fox_rank_fingerprint(5)
    assert p7_common.field_modulus == 71
    assert p5_common.field_modulus == 71
    assert p7_common.ordered_rank_vector_sha256 == p7.ordered_rank_vector_sha256
    assert p5_common.ordered_rank_vector_sha256 == p5.ordered_rank_vector_sha256


def test_family_receipt_is_deterministic_bounded_and_nonselecting(tmp_path) -> None:
    first = exact_milnor_alexander_family_certificate()
    second = exact_milnor_alexander_family_certificate()
    assert first == second

    output = write_exact_milnor_alexander_family_certificate(
        tmp_path / "prime-exact-milnor-alexander-family-certificate.json"
    )
    assert json.loads(output.read_text(encoding="utf-8")) == first
    assert first["selection_effect"] == "none"
    assert first["exact_milnor"]["borromean_braid"]["gate_passed"] is True
    assert first["exact_milnor"]["all_five_exact_zero"] is True
    assert first["preregistered_phase_selector"]["p7"]["selected"]["boundary_meridional_degree"] == 7
    assert first["preregistered_phase_selector"]["p5"]["selected"]["boundary_meridional_degree"] == -5
    assert any("not a complete" in item for item in first["nonclaims"])
    assert any("Riemann" in item for item in first["nonclaims"])
    assert len(first["payload_sha256"]) == 64
