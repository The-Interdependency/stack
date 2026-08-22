# === CHECKS ===
# id: check_prime_mpfr_backend_independence
#   proves: prime_mpfr_replay_is_backend_independent
#   call: self::test_direct_mpfr_replay_matches_frozen_partition
#   requires: python3, libmpfr
#   timeout: 120
#   mutates: none
#   cleanup: none
#
# id: check_prime_mpfr_ribbon_margin
#   proves: prime_mpfr_replay_recertifies_ribbon_margin
#   call: self::test_direct_mpfr_replay_recertifies_both_primes
#   requires: python3, libmpfr
#   timeout: 120
#   mutates: none
#   cleanup: none
#
# id: check_prime_phase_sensitivity_selection
#   proves: prime_phase_sensitivity_separates_selection_from_emergence
#   call: self::test_phase_sensitivity_enumerates_all_equal_gap_alternatives
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_prime_phase_torus_seven_not_forced
#   proves: prime_phase_sensitivity_torus_seven_is_not_forced
#   call: self::test_p7_and_p5_share_the_same_maximum_gap_knot_degrees
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_prime_milnor_borromean_benchmark
#   proves: prime_milnor_fourier_benchmark_recovers_borromean
#   call: self::test_fourier_milnor_benchmark_converges_to_minus_one
#   requires: python3, numpy
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_prime_milnor_p7_zero_resolution
#   proves: prime_milnor_p7_split_triples_resolve_numerically_to_zero
#   call: self::test_all_five_p7_triples_converge_numerically_to_zero
#   requires: python3, numpy
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_prime_milnor_exactness_boundary
#   proves: prime_milnor_exactness_boundary_is_preserved
#   call: self::test_numerical_resolution_is_not_promoted_to_exact_theorem
#   requires: python3
#   timeout: 60
#   mutates: none
#   cleanup: none
#
# id: check_prime_independent_receipt_nonselecting
#   proves: prime_independent_phase_milnor_receipt_is_nonselecting
#   call: self::test_research_boundaries_remain_explicit
#   requires: python3
#   timeout: 60
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from fractions import Fraction

from ucns.mpfr_interval import mpfr_version
from ucns.prime_independent_phase_milnor import (
    P7_SPLIT_TRIPLES,
    _borromean_curves,
    fourier_milnor_estimate,
    phase_sensitivity_report,
    replay_prime_five_mpfr,
    replay_prime_seven_mpfr,
    resolve_p7_milnor_triples,
)


def test_direct_mpfr_replay_matches_frozen_partition() -> None:
    p7 = replay_prime_seven_mpfr()
    p5 = replay_prime_five_mpfr()
    assert mpfr_version().startswith("4.")
    assert p7.total_boxes_evaluated == 6173
    assert p5.total_boxes_evaluated == 4340
    assert p7.maximum_depth == 20
    assert p5.maximum_depth == 20
    assert p7.partition_sha256 == "2ae4d1b1ef8e7d140d0feb61d6014b8bba696285c84d56b870cfeba0536168ae"
    assert p5.partition_sha256 == "0e90ce700117ef1af2e155526eef0c1338315fd556ac0fffa344d3306a07c858"


def test_direct_mpfr_replay_recertifies_both_primes() -> None:
    p7 = replay_prime_seven_mpfr()
    p5 = replay_prime_five_mpfr()
    assert p7.all_pairs_certified
    assert p5.all_pairs_certified
    assert p7.minimum_lower_endpoint_binary64 > 0.09
    assert p5.minimum_lower_endpoint_binary64 > 0.09
    assert p7.minimum_lower_endpoint_binary64 == 0.09000515000075497
    assert p5.minimum_lower_endpoint_binary64 == 0.09000862353879262


def test_phase_sensitivity_enumerates_all_equal_gap_alternatives() -> None:
    p7 = phase_sensitivity_report(7)
    assert p7.candidates == 174
    assert p7.admissible_count == 144
    assert p7.maximum_gap == Fraction(1, 7)
    assert len(p7.maximum_gap_candidates) == 8
    assert p7.selected_winding == 3
    assert p7.selected_outer_numerator == 3
    assert p7.selected_meridional_degree == 7
    assert p7.inadmissible_windings == (-12, -6, 0, 6, 12)


def test_p7_and_p5_share_the_same_maximum_gap_knot_degrees() -> None:
    p7 = phase_sensitivity_report(7)
    p5 = phase_sensitivity_report(5)
    expected = (-17, -5, 7, 19)
    assert p7.maximum_gap_meridional_degrees == expected
    assert p5.maximum_gap_meridional_degrees == expected
    assert p7.maximum_gap == Fraction(1, 7)
    assert p5.maximum_gap == Fraction(1, 5)
    assert p5.selected_winding == 3
    assert p5.selected_outer_numerator == 4


def test_fourier_milnor_benchmark_converges_to_minus_one() -> None:
    estimates = [
        fourier_milnor_estimate(_borromean_curves(), grid)
        for grid in (32, 48, 64)
    ]
    errors = [abs(item.estimate + 1) for item in estimates]
    assert errors[2] < errors[1] < errors[0]
    assert errors[-1] < 0.003
    assert max(item.coordinate_degree_residual for item in estimates) < 1e-12


def test_all_five_p7_triples_converge_numerically_to_zero() -> None:
    resolutions = resolve_p7_milnor_triples((48, 64, 80))
    assert tuple(item.components for item in resolutions) == P7_SPLIT_TRIPLES
    assert all(item.nearest_integer == 0 for item in resolutions)
    assert all(abs(item.finest.estimate) < 0.0011 for item in resolutions)
    for item in resolutions:
        magnitudes = [abs(estimate.estimate) for estimate in item.estimates]
        assert magnitudes[-1] < magnitudes[-2] < magnitudes[-3]


def test_numerical_resolution_is_not_promoted_to_exact_theorem() -> None:
    resolution = resolve_p7_milnor_triples((48, 64, 80))[0]
    payload = resolution.as_dict()
    assert payload["numerically_resolved_zero"] is True
    assert "exact Milnor value still requires" in payload["exact_standing"]


def test_research_boundaries_remain_explicit() -> None:
    p7 = phase_sensitivity_report(7).as_dict()
    assert "does not uniquely force" in p7["standing"]
    result = resolve_p7_milnor_triples((48, 64, 80))[0].as_dict()
    assert "C-complex" in result["exact_standing"]
