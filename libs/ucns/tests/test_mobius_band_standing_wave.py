# === CHECKS ===
# id: check_mobius_band_standing_wave_declares_operator_domain_bc_trace
#   proves: mobius_band_standing_wave_declares_operator_domain_bc_trace
#   call: self::test_band_model_declares_operator_domain_boundary_and_trace
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_mobius_band_standing_wave_modes_satisfy_equations
#   proves: mobius_band_standing_wave_modes_satisfy_operator_and_boundary_conditions
#   call: self::test_band_modes_satisfy_operator_mobius_seam_return_and_edge_conditions
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_mobius_band_boundary_trace_rank_derivation
#   proves: mobius_band_boundary_trace_rank_is_derived_not_assigned
#   call: self::test_boundary_trace_rank_is_limited_by_boundary_harmonics_not_bulk_modes
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_mobius_band_capacity_falsifies_bulk_counting
#   proves: mobius_band_boundary_capacity_falsifies_bulk_only_counting
#   call: self::test_capacity_report_survives_finite_trace_and_falsifies_bulk_overadmission
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_mobius_band_invalid_requests_rejected
#   proves: mobius_band_standing_wave_declares_operator_domain_bc_trace
#   call: self::test_invalid_band_requests_are_rejected
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from fractions import Fraction

import pytest

from ucns.mobius_band_standing_wave import (
    BOUNDARY_CONDITIONS,
    MOBIUS_QUOTIENT,
    PHYSICAL_BOUNDARY,
    SPATIAL_OPERATOR,
    STATUS_FALSIFIED,
    STATUS_SURVIVED,
    STATUS_UNRESOLVED,
    TURN_DOMAIN,
    WAVE_EQUATION,
    MobiusBandBasisFunction,
    MobiusBandStandingWaveError,
    build_mobius_band_standing_wave,
    evaluate_band_capacity_channel_induction,
    run_all_mobius_band,
)


def test_band_model_declares_operator_domain_boundary_and_trace() -> None:
    model = build_mobius_band_standing_wave()

    assert model.schema_id == "ucns.mobius-band-standing-wave"
    assert model.domain.turn_domain == TURN_DOMAIN
    assert model.domain.breadth_domain == (-Fraction(1, 100), Fraction(1, 100))
    assert model.domain.mobius_quotient == MOBIUS_QUOTIENT
    assert model.domain.physical_boundary == PHYSICAL_BOUNDARY
    assert model.spatial_operator == SPATIAL_OPERATOR
    assert model.wave_equation == WAVE_EQUATION
    assert "dX/du(t,+w)=0" in BOUNDARY_CONDITIONS

    mode = model.basis_functions(1, 0)[1]
    trace = mode.boundary_trace(8)
    assert trace.sample_count == 8
    assert len(trace.values) == 8
    assert trace.vector == trace.values


def test_band_modes_satisfy_operator_mobius_seam_return_and_edge_conditions() -> None:
    model = build_mobius_band_standing_wave()

    for mode in model.basis_functions(4, 2):
        for turn in (Fraction(0), Fraction(1, 9), Fraction(5, 8)):
            for breadth in (
                -model.domain.half_width / 2,
                Fraction(0),
                model.domain.half_width / 3,
            ):
                assert mode.spatial_operator_residual(turn, breadth) < 2e-8
                assert mode.mobius_seam_residual(turn, breadth) < 2e-8
                assert mode.two_turn_return_residual(turn, breadth) < 2e-8
        assert mode.physical_boundary_residual() < 2e-8


def test_boundary_trace_rank_is_limited_by_boundary_harmonics_not_bulk_modes() -> None:
    model = build_mobius_band_standing_wave()

    assert model.interior_basis_dimension(3, 0) == 7
    assert model.boundary_trace_rank(16, 3, 0) == 7
    assert model.interior_basis_dimension(3, 4) == 35
    assert model.boundary_trace_rank(16, 3, 4) == 7

    with_derivative = model.boundary_trace_rank(
        16,
        3,
        4,
        include_normal_derivative=True,
    )
    assert with_derivative == 7


def test_capacity_report_survives_finite_trace_and_falsifies_bulk_overadmission() -> None:
    survived = evaluate_band_capacity_channel_induction(
        8,
        boundary_sample_count=16,
        max_longitudinal_index=7,
        max_transverse_index=3,
    )
    falsified = evaluate_band_capacity_channel_induction(
        16,
        boundary_sample_count=16,
        max_longitudinal_index=7,
        max_transverse_index=3,
    )

    assert survived.status == STATUS_SURVIVED
    assert survived.induces_required_channels
    assert survived.boundary_trace_rank == 15
    assert survived.pcea_generalization_status == STATUS_UNRESOLVED

    assert falsified.status == STATUS_FALSIFIED
    assert falsified.bulk_only_accepts is True
    assert falsified.boundary_accepts is False
    assert falsified.boundary_trace_rank == 15
    assert falsified.interior_basis_dimension == 60

    report = run_all_mobius_band()
    assert report["construction_status"] == STATUS_SURVIVED
    assert report["overall_status_for_pcea_promotion"] == STATUS_UNRESOLVED


def test_invalid_band_requests_are_rejected() -> None:
    with pytest.raises(MobiusBandStandingWaveError):
        build_mobius_band_standing_wave(Fraction(0))
    with pytest.raises(MobiusBandStandingWaveError):
        MobiusBandBasisFunction(1, "cos", 0, "even_neumann")
    with pytest.raises(MobiusBandStandingWaveError):
        evaluate_band_capacity_channel_induction(0)
