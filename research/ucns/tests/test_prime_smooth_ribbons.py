# === CHECKS ===
# id: check_prime_smooth_ribbons_event_lanes
#   proves: prime_smooth_ribbons_preserve_all_event_lanes
#   call: self::test_flat_step_fields_are_c_infinity_bounded_and_event_preserving
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_smooth_ribbons_mobius_return
#   proves: prime_smooth_ribbons_obey_mobius_return
#   call: self::test_smoothed_surfaces_obey_one_turn_reversal_and_two_turn_return
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_smooth_ribbons_centerline_margin
#   proves: prime_smooth_ribbons_have_global_centerline_margin
#   call: self::test_complete_parameter_tori_certify_nine_hundredths_centerline_margin
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_prime_smooth_ribbons_finite_width_disjointness
#   proves: prime_smooth_ribbons_are_globally_disjoint_at_declared_width
#   call: self::test_triangle_inequality_certifies_seven_hundredths_ribbon_margin
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_smooth_ribbons_tangent_regularization
#   proves: prime_smooth_ribbons_regularize_tangent_pairs
#   call: self::test_tangent_pairs_receive_clearance_preserving_zero_link_regularizations
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_smooth_ribbons_linking_matrix
#   proves: prime_smooth_ribbons_issue_complete_linking_matrix
#   call: self::test_complete_pairwise_linking_matrices_have_expected_invariants
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_smooth_ribbons_p7_first
#   proves: prime_smooth_ribbons_p7_precedes_p5
#   call: self::test_family_receipt_preserves_p7_first_p5_second_order
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_smooth_ribbons_receipt
#   proves: prime_smooth_ribbons_receipt_is_nonselecting
#   call: self::test_receipt_and_smooth_meshes_are_deterministic_and_firewalled
#   requires: python3
#   timeout: 30
#   mutates: temporary_path
#   cleanup: pytest temporary_path
# === END CHECKS ===

from fractions import Fraction
import json
import math

from ucns.prime_smooth_ribbons import (
    CENTERLINE_SEPARATION_TARGET,
    HALF_WIDTH,
    RIBBON_SEPARATION_LOWER_BOUND,
    TANGENT_REGULARIZATION_EPSILON,
    build_smooth_prime_five,
    build_smooth_prime_seven,
    certify_smooth_prime_five,
    certify_smooth_prime_seven,
    flat_step,
    flat_step_derivative,
    render_smooth_centerline_obj,
    render_smooth_ribbon_obj,
    smooth_ribbon_family_certificate,
    write_smooth_ribbon_family_certificate,
)


def test_flat_step_fields_are_c_infinity_bounded_and_event_preserving() -> None:
    assert flat_step(0.0) == 0.0
    assert flat_step(1.0) == 1.0
    assert flat_step_derivative(0.0) == 0.0
    assert flat_step_derivative(1.0) == 0.0
    samples = [index / 2000 for index in range(2001)]
    values = [flat_step(value) for value in samples]
    derivatives = [flat_step_derivative(value) for value in samples]
    assert all(0.0 <= value <= 1.0 for value in values)
    assert all(left <= right for left, right in zip(values, values[1:]))
    assert max(derivatives) <= 2.0 + 1e-12
    assert math.isclose(flat_step(0.5), 0.5, rel_tol=0, abs_tol=1e-15)

    for ribbon in (build_smooth_prime_seven(), build_smooth_prime_five()):
        assert ribbon.maximum_event_height_residual == 0.0
        for field in ribbon.fields:
            assert field.maximum_event_residual == 0.0
            for segment in field.segments:
                for step in range(21):
                    turn = segment.left_turn + segment.turn_width * Fraction(step, 20)
                    value = field.evaluate(turn)
                    lower = float(min(segment.left_value, segment.right_value))
                    upper = float(max(segment.left_value, segment.right_value))
                    assert lower - 1e-15 <= value <= upper + 1e-15


def test_smoothed_surfaces_obey_one_turn_reversal_and_two_turn_return() -> None:
    for ribbon in (build_smooth_prime_seven(), build_smooth_prime_five()):
        one_turn, two_turn = ribbon.seam_residuals()
        assert one_turn < 1e-12
        assert two_turn < 3e-12
        for carrier in ribbon.carriers:
            assert ribbon.field(carrier).evaluate(Fraction(1, 7)) == ribbon.field(carrier).evaluate(Fraction(8, 7))


def test_complete_parameter_tori_certify_nine_hundredths_centerline_margin() -> None:
    p7 = certify_smooth_prime_seven()
    p5 = certify_smooth_prime_five()
    assert len(p7.pair_certificates) == 21
    assert len(p5.pair_certificates) == 10
    for certificate in (p7, p5):
        assert certificate.minimum_leaf_lower_bound > float(CENTERLINE_SEPARATION_TARGET)
        assert certificate.maximum_subdivision_depth <= 24
        assert certificate.total_boxes_evaluated < 20_000
        assert all(item.certified for item in certificate.pair_certificates)
        assert all(item.target == Fraction(9, 100) for item in certificate.pair_certificates)
        assert all(item.boxes_evaluated < 2_000 for item in certificate.pair_certificates)


def test_triangle_inequality_certifies_seven_hundredths_ribbon_margin() -> None:
    assert HALF_WIDTH == Fraction(1, 100)
    assert CENTERLINE_SEPARATION_TARGET == Fraction(9, 100)
    assert RIBBON_SEPARATION_LOWER_BOUND == Fraction(7, 100)
    for certificate in (certify_smooth_prime_seven(), certify_smooth_prime_five()):
        separation = certificate.payload["global_separation"]
        assert separation["all_pairs_certified"] is True
        assert separation["global_finite_width_ribbon_separation_lower_bound"] == "7/100"


def test_tangent_pairs_receive_clearance_preserving_zero_link_regularizations() -> None:
    p7 = certify_smooth_prime_seven()
    p5 = certify_smooth_prime_five()
    assert {item.pair_id for item in p7.tangent_regularizations} == {"R0::R3", "R1::R4", "R2::R5"}
    assert {item.pair_id for item in p5.tangent_regularizations} == {"R0::R2", "R1::R3"}
    for item in (*p7.tangent_regularizations, *p5.tangent_regularizations):
        assert item.epsilon == TANGENT_REGULARIZATION_EPSILON
        assert item.post_translation_projected_center_distance == Fraction(201, 100)
        assert item.minimum_ribbon_clearance_during_isotopy == Fraction(3, 50)
        assert item.linking_number == 0
        assert math.isclose(math.hypot(*item.translation_unit_vector), 1.0, rel_tol=0, abs_tol=1e-12)


def test_complete_pairwise_linking_matrices_have_expected_invariants() -> None:
    p7 = certify_smooth_prime_seven().linking_matrix
    p5 = certify_smooth_prime_five().linking_matrix
    assert p7.value_counts == {"0": 9, "1": 12}
    assert (p7.rank, p7.nullity, p7.determinant) == (6, 1, 0)
    assert (p7.nonzero_edge_count, p7.nonzero_component_count, p7.nonzero_cycle_rank) == (12, 1, 6)
    assert len(p7.matrix) == 7
    assert all(row[index] == 0 for index, row in enumerate(p7.matrix))
    assert all(p7.matrix[i][j] == p7.matrix[j][i] for i in range(7) for j in range(7))
    assert p5.value_counts == {"0": 8, "1": 2}
    assert (p5.rank, p5.nullity, p5.determinant) == (2, 3, 0)
    assert (p5.nonzero_edge_count, p5.nonzero_component_count, p5.nonzero_cycle_rank) == (2, 3, 0)


def test_family_receipt_preserves_p7_first_p5_second_order() -> None:
    receipt = smooth_ribbon_family_certificate()
    assert receipt["research_order"] == [7, 5]
    assert receipt["p7"]["prime"] == 7
    assert receipt["p5"]["prime"] == 5
    assert receipt["comparison"]["same_protocol"] is True
    assert "not obtained" in receipt["comparison"]["standing"]
    assert receipt["comparison"]["p7_linking_matrix_rank"] == 6
    assert receipt["comparison"]["p5_linking_matrix_rank"] == 2


def test_receipt_and_smooth_meshes_are_deterministic_and_firewalled(tmp_path) -> None:
    first = smooth_ribbon_family_certificate()
    second = smooth_ribbon_family_certificate()
    assert first == second
    assert first["selection_effect"] == "none"
    assert len(first["payload_sha256"]) == 64
    assert any("Riemann" in item for item in first["nonclaims"])
    output = write_smooth_ribbon_family_certificate(tmp_path / "prime-smooth-ribbon-family-certificate.json")
    assert json.loads(output.read_text(encoding="utf-8")) == first
    p7 = build_smooth_prime_seven()
    centerline_a = render_smooth_centerline_obj(p7, samples_per_carrier=48)
    centerline_b = render_smooth_centerline_obj(p7, samples_per_carrier=48)
    ribbon_a = render_smooth_ribbon_obj(p7, turn_samples=24, breadth_segments=2)
    ribbon_b = render_smooth_ribbon_obj(p7, turn_samples=24, breadth_segments=2)
    assert centerline_a == centerline_b
    assert ribbon_a == ribbon_b
    assert centerline_a.count("\nv ") == 7 * 48
    assert centerline_a.count("\nl ") == 7
    assert ribbon_a.count("\nv ") == 7 * 24 * 3
    assert "separation lower bound 7/100" in ribbon_a
