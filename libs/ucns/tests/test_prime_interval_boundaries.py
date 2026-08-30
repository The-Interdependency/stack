# === CHECKS ===
# id: check_prime_interval_replay_outward_endpoints
#   proves: prime_interval_replay_uses_outward_endpoints
#   call: self::test_interval_replay_closes_every_complete_parameter_torus
#   requires: python3, mpmath
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_prime_boundary_single_two_turn_component
#   proves: prime_boundary_curve_is_single_two_turn_component
#   call: self::test_each_mobius_boundary_is_one_two_turn_component
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_boundary_cable_winding
#   proves: prime_boundary_cable_winding_is_derived_from_phase
#   call: self::test_boundary_cable_classes_and_component_knot_invariants
#   requires: python3
#   timeout: 60
#   mutates: none
#   cleanup: none
#
# id: check_prime_boundary_linking_fourfold
#   proves: prime_boundary_linking_scales_by_four
#   call: self::test_boundary_linking_matrices_are_four_times_core_matrices
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_prime_mixed_core_boundary_matrix
#   proves: prime_mixed_core_boundary_matrix_is_complete
#   call: self::test_mixed_core_boundary_matrices_are_full_rank_with_exact_determinants
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_prime_higher_order_boundary
#   proves: prime_higher_order_boundary_is_explicit
#   call: self::test_algebraically_split_triples_are_enumerated_without_fake_milnor_values
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_prime_interval_boundaries_p7_first
#   proves: prime_interval_boundaries_p7_precedes_p5
#   call: self::test_family_receipt_preserves_p7_first_order
#   requires: python3, mpmath
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_prime_interval_boundary_compact_receipt
#   proves: prime_interval_boundary_compact_receipt_is_nonselecting
#   call: self::test_receipt_and_boundary_exports_are_deterministic_and_firewalled
#   requires: python3, mpmath
#   timeout: 40
#   mutates: temporary_path
#   cleanup: pytest temporary_path
#
# id: check_prime_legacy_readable_adapter
#   proves: prime_interval_replay_uses_outward_endpoints
#   call: self::test_legacy_surface_is_an_explicit_adapter_over_readable_evidence
#   requires: python3, mpmath, sympy
#   timeout: 40
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from fractions import Fraction
import json
import math

from ucns.prime_interval_boundaries import (
    BOUNDARY_PERIOD_TURNS,
    INTERVAL_BACKEND,
    INTERVAL_DPS,
    certify_prime_five_boundaries,
    certify_prime_seven_boundaries,
    interval_boundary_family_certificate,
    render_boundary_obj,
    render_core_boundary_obj,
    replay_prime_five_intervals,
    replay_prime_seven_intervals,
    write_interval_boundary_family_certificate,
)
from ucns.prime_smooth_ribbons import (
    build_smooth_prime_five,
    build_smooth_prime_seven,
)
from ucns.prime_interval_boundary_links import certify_interval_boundary_prime_seven


def test_legacy_surface_is_an_explicit_adapter_over_readable_evidence() -> None:
    legacy = certify_prime_seven_boundaries()
    readable = certify_interval_boundary_prime_seven()

    assert legacy.interval_replay.total_boxes_evaluated == readable.interval_separation.total_boxes_evaluated
    assert legacy.core_linking_matrix == readable.boundary_link.core_matrix.matrix
    assert legacy.boundary_linking_matrix == readable.boundary_link.boundary_matrix.matrix
    assert legacy.components[0].natural_core_boundary_linking == -readable.boundary_link.components[0].core_boundary_linking
    compatibility = legacy.payload["compatibility"]
    assert compatibility["implementation"] == "readable PR #181 boundary-link certificate"
    assert compatibility["legacy_source_sha256"] == "6a79463856ea0171d7d29881fdb7e66780fab29779ff1c5fd1b71eaae7f9fc3c"


def test_interval_replay_closes_every_complete_parameter_torus() -> None:
    p7 = replay_prime_seven_intervals()
    p5 = replay_prime_five_intervals()

    assert p7.all_pairs_certified
    assert p5.all_pairs_certified
    assert len(p7.pair_replays) == 21
    assert len(p5.pair_replays) == 10
    assert p7.total_boxes_evaluated == 6173
    assert p5.total_boxes_evaluated == 4340
    assert p7.maximum_depth == 20
    assert p5.maximum_depth == 20
    assert p7.minimum_lower_endpoint_binary64 > 0.09
    assert p5.minimum_lower_endpoint_binary64 > 0.09
    assert len(p7.global_leaf_ledger_sha256) == 64
    assert len(p5.global_leaf_ledger_sha256) == 64
    payload = p7.as_dict()
    assert payload["backend"]["name"] == INTERVAL_BACKEND
    assert payload["backend"]["decimal_digits"] == INTERVAL_DPS
    assert "not independently verified" in payload["backend"]["standing"]


def test_each_mobius_boundary_is_one_two_turn_component() -> None:
    assert BOUNDARY_PERIOD_TURNS == Fraction(2)
    for ribbon in (build_smooth_prime_seven(), build_smooth_prime_five()):
        for carrier in ribbon.carriers:
            for turn in (Fraction(0), Fraction(1, 17), Fraction(5, 13)):
                boundary = ribbon.surface_point(carrier, turn, ribbon.half_width)
                second_turn = ribbon.surface_point(carrier, turn + 2, ribbon.half_width)
                opposite_edge = ribbon.surface_point(carrier, turn + 1, ribbon.half_width)
                negative_breadth = ribbon.surface_point(carrier, turn, -ribbon.half_width)
                assert math.dist(boundary, second_turn) < 3e-12
                assert math.dist(opposite_edge, negative_breadth) < 3e-12


def test_boundary_cable_classes_and_component_knot_invariants() -> None:
    for certificate in (
        certify_prime_seven_boundaries(),
        certify_prime_five_boundaries(),
    ):
        center = certificate.components[0]
        outers = certificate.components[1:]
        assert center.carrier == "C"
        assert (center.longitudinal_degree, center.meridional_degree) == (2, 7)
        assert center.natural_core_boundary_linking == -7
        assert center.knot_type == "T(2,7)"
        assert center.determinant == 7
        assert center.seifert_genus == 3
        assert center.crossing_number == 7
        assert center.is_unknot is False
        assert "t^3" in center.alexander_polynomial
        assert all((item.longitudinal_degree, item.meridional_degree) == (2, 1) for item in outers)
        assert all(item.natural_core_boundary_linking == -1 for item in outers)
        assert all(item.knot_type == "T(2,1)" for item in outers)
        assert all(item.alexander_polynomial == "1" for item in outers)
        assert all(item.is_unknot for item in outers)


def test_boundary_linking_matrices_are_four_times_core_matrices() -> None:
    p7 = certify_prime_seven_boundaries()
    p5 = certify_prime_five_boundaries()
    for certificate in (p7, p5):
        for row in range(certificate.prime):
            for column in range(certificate.prime):
                assert certificate.boundary_linking_matrix[row][column] == 4 * certificate.core_linking_matrix[row][column]
        assert certificate.boundary_rank == (6 if certificate.prime == 7 else 2)
        assert certificate.boundary_nullity == (1 if certificate.prime == 7 else 3)
        assert certificate.boundary_determinant == 0
        assert certificate.payload["boundary_linking"]["technical_boundary_link_status"].startswith("not a boundary link")
    assert p7.payload["boundary_linking"]["value_counts"] == {"0": 9, "4": 12}
    assert p5.payload["boundary_linking"]["value_counts"] == {"0": 8, "4": 2}


def test_mixed_core_boundary_matrices_are_full_rank_with_exact_determinants() -> None:
    p7 = certify_prime_seven_boundaries()
    p5 = certify_prime_five_boundaries()

    assert len(p7.mixed_core_boundary_matrix) == 14
    assert p7.mixed_rank == 14
    assert p7.mixed_nullity == 0
    assert p7.mixed_determinant == -5425
    assert p7.payload["mixed_core_boundary_link"]["absolute_determinant_factorization"] == {
        "5": 2,
        "7": 1,
        "31": 1,
    }

    assert len(p5.mixed_core_boundary_matrix) == 10
    assert p5.mixed_rank == 10
    assert p5.mixed_nullity == 0
    assert p5.mixed_determinant == 1519
    assert p5.payload["mixed_core_boundary_link"]["absolute_determinant_factorization"] == {
        "7": 2,
        "31": 1,
    }


def test_algebraically_split_triples_are_enumerated_without_fake_milnor_values() -> None:
    p7 = certify_prime_seven_boundaries().payload["higher_order_boundary"]
    p5 = certify_prime_five_boundaries().payload["higher_order_boundary"]

    assert p7["pairwise_nonzero_edge_count_distribution"] == {
        "0": 5,
        "1": 8,
        "2": 14,
        "3": 8,
    }
    assert p5["pairwise_nonzero_edge_count_distribution"] == {
        "0": 5,
        "1": 4,
        "2": 1,
        "3": 0,
    }
    assert p7["algebraically_split_triple_count"] == 5
    assert p5["algebraically_split_triple_count"] == 5
    assert "not computed" in p7["milnor_mu123_standing"]
    assert "not computed" in p5["milnor_mu123_standing"]


def test_family_receipt_preserves_p7_first_order() -> None:
    receipt = interval_boundary_family_certificate()
    assert receipt["research_order"] == [7, 5]
    assert receipt["p7"]["prime"] == 7
    assert receipt["p5"]["prime"] == 5
    assert receipt["comparison"]["same_protocol"] is True
    assert receipt["comparison"]["p7_center_boundary_knot"] == "T(2,7)"
    assert receipt["comparison"]["p5_center_boundary_knot"] == "T(2,7)"
    assert receipt["comparison"]["p7_mixed_absolute_determinant"] == 5425
    assert receipt["comparison"]["p5_mixed_absolute_determinant"] == 1519


def test_receipt_and_boundary_exports_are_deterministic_and_firewalled(tmp_path) -> None:
    first = interval_boundary_family_certificate()
    second = interval_boundary_family_certificate()
    assert first == second
    assert first["selection_effect"] == "none"
    assert len(first["payload_sha256"]) == 64
    assert any("Riemann" in item for item in first["p7"]["nonclaims"])

    output = write_interval_boundary_family_certificate(
        tmp_path / "prime-interval-boundary-family-certificate.json"
    )
    assert json.loads(output.read_text(encoding="utf-8")) == first

    p7 = build_smooth_prime_seven()
    boundary_a = render_boundary_obj(p7, samples_per_boundary=64)
    boundary_b = render_boundary_obj(p7, samples_per_boundary=64)
    combined_a = render_core_boundary_obj(p7, core_samples=32, boundary_samples=64)
    combined_b = render_core_boundary_obj(p7, core_samples=32, boundary_samples=64)
    assert boundary_a == boundary_b
    assert combined_a == combined_b
    assert boundary_a.count("\nv ") == 7 * 64
    assert boundary_a.count("\nl ") == 7
    assert combined_a.count("\nv ") == 7 * (32 + 64)
    assert combined_a.count("\nl ") == 14
    assert "T(2,7)" in boundary_a
