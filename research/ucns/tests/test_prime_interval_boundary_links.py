# === CHECKS ===
# id: check_prime_interval_outward_replay
#   proves: prime_interval_replay_is_outward_rounded
#   call: self::test_outward_interval_replay_covers_every_pair
#   requires: python3, mpmath
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_prime_interval_finite_width_disjointness
#   proves: prime_interval_replay_preserves_finite_width_disjointness
#   call: self::test_interval_margin_implies_complete_ribbon_disjointness
#   requires: python3, mpmath
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_prime_boundary_single_closed_component
#   proves: prime_boundary_curve_is_single_and_closed
#   call: self::test_each_mobius_ribbon_has_one_closed_two_turn_boundary
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_boundary_component_knot_types
#   proves: prime_boundary_component_knot_types_are_derived
#   call: self::test_boundary_component_cable_and_knot_invariants
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_boundary_linking_matrix
#   proves: prime_boundary_linking_matrix_follows_cable_homology
#   call: self::test_boundary_and_mixed_linking_blocks_follow_cable_homology
#   requires: python3, sympy
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_prime_mixed_integer_invariants
#   proves: prime_mixed_linking_matrix_has_exact_integer_invariants
#   call: self::test_full_core_boundary_integer_invariants_distinguish_p7_and_p5
#   requires: python3, sympy
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_prime_length_three_milnor_profile
#   proves: prime_length_three_milnor_profile_is_computed_after_global_lift
#   call: self::test_generic_diagram_and_length_three_milnor_profile
#   requires: python3, mpmath
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_prime_interval_boundary_research_order
#   proves: prime_interval_boundary_p7_precedes_p5
#   call: self::test_family_certificate_preserves_p7_first_order
#   requires: python3, mpmath, sympy
#   timeout: 60
#   mutates: none
#   cleanup: none
#
# id: check_prime_interval_boundary_receipt
#   proves: prime_interval_boundary_receipt_is_nonselecting
#   call: self::test_receipt_and_boundary_models_are_deterministic_and_bounded
#   requires: python3, mpmath, sympy
#   timeout: 60
#   mutates: temporary_path
#   cleanup: pytest temporary_path
# id: check_prime_boundary_helper_facade
#   proves: prime_boundary_helper_is_facade_witnessed
#   call: self::test_boundary_and_mixed_linking_blocks_follow_cable_homology
#   requires: python3, sympy
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_prime_generic_helper_facade
#   proves: prime_generic_helper_is_facade_witnessed
#   call: self::test_generic_diagram_and_length_three_milnor_profile
#   requires: python3, mpmath
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_prime_interval_common_facade
#   proves: prime_interval_common_is_facade_witnessed
#   call: self::test_outward_interval_replay_covers_every_pair
#   requires: python3, mpmath
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_prime_interval_replay_helper_facade
#   proves: prime_interval_replay_helper_is_facade_witnessed
#   call: self::test_outward_interval_replay_covers_every_pair
#   requires: python3, mpmath
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_prime_milnor_helper_facade
#   proves: prime_milnor_helper_is_facade_witnessed
#   call: self::test_generic_diagram_and_length_three_milnor_profile
#   requires: python3, mpmath
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# === END CHECKS ===

from fractions import Fraction
import hashlib
import json
import math

import pytest

from ucns.prime_interval_boundary_links import (
    GENERIC_ISOTOPY_CLEARANCE,
    INTERVAL_DPS,
    build_boundary_link_certificate,
    build_generic_core_diagram,
    certify_interval_boundary_prime_five,
    certify_interval_boundary_prime_seven,
    compute_milnor_profile,
    extract_boundary_components,
    interval_boundary_family_certificate,
    interval_boundary_family_summary,
    render_boundary_curve_obj,
    replay_interval_separation,
    write_interval_boundary_family_certificate,
    write_interval_boundary_family_summary,
)
from ucns.prime_smooth_ribbons import (
    RIBBON_SEPARATION_LOWER_BOUND,
    build_smooth_prime_five,
    build_smooth_prime_seven,
)


@pytest.fixture(scope="module")
def p7_certificate():
    return certify_interval_boundary_prime_seven()


@pytest.fixture(scope="module")
def p5_certificate():
    return certify_interval_boundary_prime_five()


def test_outward_interval_replay_covers_every_pair(p7_certificate, p5_certificate) -> None:
    p7 = p7_certificate.interval_separation
    p5 = p5_certificate.interval_separation
    assert p7.dps == p5.dps == INTERVAL_DPS
    assert p7.mpmath_version.startswith("1.")
    assert p7.pair_count == 21
    assert p5.pair_count == 10
    assert p7.total_boxes_evaluated == 6173
    assert p5.total_boxes_evaluated == 4340
    assert p7.maximum_depth == p5.maximum_depth == 20
    assert p7.all_pairs_certified and p5.all_pairs_certified
    assert float(p7.minimum_leaf_lower_bound_decimal) > 0.09
    assert float(p5.minimum_leaf_lower_bound_decimal) > 0.09
    assert p7.as_dict()["ad_hoc_roundoff_buffer"] is None
    assert "directed interval" in p7.as_dict()["method"]


def test_interval_margin_implies_complete_ribbon_disjointness(p7_certificate, p5_certificate) -> None:
    assert RIBBON_SEPARATION_LOWER_BOUND == Fraction(7, 100)
    for certificate in (p7_certificate, p5_certificate):
        assert certificate.interval_separation.all_pairs_certified
        assert certificate.payload["findings"]["complete_distinct_ribbons_interval_separated"] is True
        assert certificate.interval_separation.as_dict()["finite_width_ribbon_separation_lower_bound"] == "7/100"


def test_each_mobius_ribbon_has_one_closed_two_turn_boundary() -> None:
    for ribbon in (build_smooth_prime_seven(), build_smooth_prime_five()):
        components = extract_boundary_components(ribbon)
        assert len(components) == ribbon.prime
        for component in components:
            assert component.longitudinal_winding == 2
            assert component.meridional_winding % 2 == 1
            assert math.gcd(component.longitudinal_winding, component.meridional_winding) == 1
            start = ribbon.surface_point(component.carrier, Fraction(0), ribbon.half_width)
            finish = ribbon.surface_point(component.carrier, Fraction(2), ribbon.half_width)
            halfway = ribbon.surface_point(component.carrier, Fraction(1), ribbon.half_width)
            assert math.dist(start, finish) < 3e-15
            assert math.dist(start, halfway) > 2 * float(ribbon.half_width) - 1e-12


def test_boundary_component_cable_and_knot_invariants() -> None:
    for ribbon in (build_smooth_prime_seven(), build_smooth_prime_five()):
        components = extract_boundary_components(ribbon)
        center = components[0]
        outers = components[1:]
        assert center.carrier == "C"
        assert center.phase_winding == 3
        assert center.meridional_winding == 7
        assert center.core_boundary_linking == 7
        assert center.knot_type == "torus knot T(2,7)"
        assert center.genus == 3
        assert center.determinant == 7
        assert center.crossing_number == 7
        assert center.alexander_laurent == {"-3": 1, "-2": -1, "-1": 1, "0": -1, "1": 1, "2": -1, "3": 1}
        assert all(item.knot_type == "unknot (T(2,1))" for item in outers)
        assert all(item.core_boundary_linking == 1 for item in outers)
        assert all(item.alexander_laurent == {"0": 1} for item in outers)


def test_boundary_and_mixed_linking_blocks_follow_cable_homology() -> None:
    for ribbon in (build_smooth_prime_seven(), build_smooth_prime_five()):
        certificate = build_boundary_link_certificate(ribbon)
        core = certificate.core_matrix.matrix
        boundary = certificate.boundary_matrix.matrix
        mixed = certificate.mixed_core_boundary_block
        for row in range(ribbon.prime):
            for column in range(ribbon.prime):
                if row == column:
                    assert boundary[row][column] == 0
                    assert mixed[row][column] == certificate.components[row].core_boundary_linking
                else:
                    assert boundary[row][column] == 4 * core[row][column]
                    assert mixed[row][column] == 2 * core[row][column]


def test_full_core_boundary_integer_invariants_distinguish_p7_and_p5(p7_certificate, p5_certificate) -> None:
    p7 = p7_certificate.boundary_link
    p5 = p5_certificate.boundary_link
    assert p7.boundary_matrix.rank == 6
    assert p7.boundary_matrix.nullity == 1
    assert p7.boundary_matrix.smith_nonzero_invariant_factors == (4, 4, 4, 4, 4, 4)
    assert p5.boundary_matrix.rank == 2
    assert p5.boundary_matrix.nullity == 3
    assert p5.boundary_matrix.smith_nonzero_invariant_factors == (4, 4)
    assert p7.full_core_boundary_matrix.rank == 14
    assert p7.full_core_boundary_matrix.nullity == 0
    assert p7.full_core_boundary_matrix.determinant == 73423
    assert p7.full_core_boundary_matrix.smith_nonzero_invariant_factors == (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 73423)
    assert p5.full_core_boundary_matrix.rank == 10
    assert p5.full_core_boundary_matrix.nullity == 0
    assert p5.full_core_boundary_matrix.determinant == 1519
    assert p5.full_core_boundary_matrix.smith_nonzero_invariant_factors == (1, 1, 1, 1, 1, 1, 1, 1, 7, 217)
    assert p7.full_core_boundary_matrix.as_dict()["absolute_determinant_factorization"] == {"7": 1, "17": 1, "617": 1}
    assert p5.full_core_boundary_matrix.as_dict()["absolute_determinant_factorization"] == {"7": 2, "31": 1}


def test_generic_diagram_and_length_three_milnor_profile(p7_certificate, p5_certificate) -> None:
    p7 = p7_certificate.milnor_profile
    p5 = p5_certificate.milnor_profile
    assert p7.diagram.residual_ribbon_clearance == GENERIC_ISOTOPY_CLEARANCE
    assert p7.diagram.residual_ribbon_clearance == Fraction(42, 625)
    assert len(p7.diagram.crossings) == 36
    assert len(p5.diagram.crossings) == 16
    assert float(p7.diagram.minimum_turn_gap_decimal) > 0.00017
    assert float(p5.diagram.minimum_turn_gap_decimal) > 0.00034
    assert float(p7.diagram.minimum_height_gap_decimal) > 0.099999
    assert float(p5.diagram.minimum_height_gap_decimal) > 0.099999
    assert p7.Borromean_validation["antisymmetry_check"] is True
    assert abs(p7.Borromean_validation["mu_012"]) == 1
    assert len(p7.triples) == 35
    assert len(p7.integer_valued_triples) == 5
    assert {item.triple for item in p7.integer_valued_triples} == {("R0", "R1", "R4"), ("R0", "R1", "R5"), ("R0", "R2", "R5"), ("R0", "R4", "R5"), ("R1", "R4", "R5")}
    assert all(item.value == 0 for item in p7.integer_valued_triples)
    assert not p7.nonzero_integer_values
    assert len(p5.triples) == 10
    assert len(p5.integer_valued_triples) == 5
    assert all(item.value == 0 for item in p5.integer_valued_triples)
    assert not p5.nonzero_integer_values
    assert all(item.indeterminacy_modulus in {0, 1} for item in (*p7.triples, *p5.triples))


def test_family_certificate_preserves_p7_first_order() -> None:
    first = interval_boundary_family_certificate()
    second = interval_boundary_family_certificate()
    assert first == second
    assert first["research_order"] == [7, 5]
    assert first["comparison"]["P7_full_mixed_matrix_determinant"] == 73423
    assert first["comparison"]["P5_full_mixed_matrix_determinant"] == 1519
    assert first["comparison"]["P7_informative_length_three_Milnor_values"] == [0, 0, 0, 0, 0]
    assert "same T(2,7)" in first["comparison"]["phase_law_warning"]
    assert len(first["payload_sha256"]) == 64
    summary_first = interval_boundary_family_summary()
    summary_second = interval_boundary_family_summary()
    assert summary_first == summary_second
    assert summary_first["expanded_family_payload_sha256"] == first["payload_sha256"]
    assert summary_first["p7"]["length_three_Milnor"]["nonzero_integer_values"] == 0
    assert summary_first["p5"]["length_three_Milnor"]["nonzero_integer_values"] == 0


def test_receipt_and_boundary_models_are_deterministic_and_bounded(tmp_path) -> None:
    output = write_interval_boundary_family_certificate(tmp_path / "prime-interval-boundary-family-certificate.json")
    decoded = json.loads(output.read_text(encoding="utf-8"))
    assert decoded == interval_boundary_family_certificate()
    summary_output = write_interval_boundary_family_summary(tmp_path / "prime-interval-boundary-family-summary.json")
    assert json.loads(summary_output.read_text(encoding="utf-8")) == interval_boundary_family_summary()
    assert decoded["selection_effect"] == "none"
    assert any("length-four" in item for item in decoded["p7"]["unresolved"])
    assert any("Riemann" in item for item in decoded["nonclaims"])
    p7_obj_first = render_boundary_curve_obj(build_smooth_prime_seven(), longitudinal_samples=256)
    p7_obj_second = render_boundary_curve_obj(build_smooth_prime_seven(), longitudinal_samples=256)
    p5_obj = render_boundary_curve_obj(build_smooth_prime_five(), longitudinal_samples=256)
    assert p7_obj_first == p7_obj_second
    assert p7_obj_first.count("\no ") == 7
    assert p5_obj.count("\no ") == 5
    assert p7_obj_first.count("\nl ") == 7
    assert p5_obj.count("\nl ") == 5
    assert hashlib.sha256(p7_obj_first.encode()).hexdigest() == hashlib.sha256(p7_obj_second.encode()).hexdigest()
