# === CHECKS ===
# id: check_mobius_standing_wave_declares_operator_domain_bc_trace
#   proves: mobius_standing_wave_declares_operator_domain_bc_trace
#   call: self::test_model_declares_operator_domain_boundary_conditions_and_trace
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_mobius_standing_wave_modes_satisfy_operator_and_boundary_conditions
#   proves: mobius_standing_wave_modes_satisfy_operator_and_boundary_conditions
#   call: self::test_modes_satisfy_operator_and_complete_return_conditions
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_mobius_standing_wave_boundary_trace_is_derived_not_assigned
#   proves: mobius_standing_wave_boundary_trace_is_derived_not_assigned
#   call: self::test_boundary_trace_rank_is_derived_from_endpoint_vectors
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_mobius_standing_wave_falsifies_pcea_capacity_channel_induction
#   proves: mobius_standing_wave_falsifies_pcea_capacity_channel_induction
#   call: self::test_pcea_capacity_channel_induction_is_falsified_when_trace_rank_is_insufficient
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_mobius_standing_wave_rejects_invalid_requests
#   proves: mobius_standing_wave_declares_operator_domain_bc_trace
#   call: self::test_invalid_standing_wave_requests_raise
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from fractions import Fraction

import pytest

from ucns.mobius_standing_wave import (
    DOMAIN,
    MOBIUS_STANDING_WAVE_SCHEMA_ID,
    STATUS_FALSIFIED,
    STATUS_SURVIVED,
    MobiusStandingWaveError,
    StandingWaveBasisFunction,
    build_native_mobius_standing_wave,
    evaluate_capacity_channel_induction,
    run_all,
)


def test_model_declares_operator_domain_boundary_conditions_and_trace() -> None:
    model = build_native_mobius_standing_wave()
    traces = model.boundary_traces(1)

    assert model.wave_equation == "d2 psi / d tau2 = c^2 d2 psi / d t2"
    assert model.spatial_operator == "L X = -d2 X / dt2"
    assert model.domain == (Fraction(0), Fraction(2)) == DOMAIN
    assert model.boundary_conditions == ("X(0)=X(2)", "X'(0)=X'(2)")
    assert "not a PCEA boundary-capacity promotion" in model.as_dict()["nonclaims"]
    assert len(traces) == 3
    assert traces[0].vector == (1.0, 1.0, 0.0, 0.0)


def test_modes_satisfy_operator_and_complete_return_conditions() -> None:
    model = build_native_mobius_standing_wave()

    for mode in model.basis_functions(6):
        for turn in (0, 0.25, 0.5, 1, 1.75, 2):
            assert mode.spatial_operator_residual(turn) < 1e-12

        value_residual, derivative_residual = mode.boundary_condition_residuals()
        assert value_residual < 1e-12
        assert derivative_residual < 1e-12

        if mode.mode_index:
            assert mode.value(Fraction(1, 3) + 1) == pytest.approx(
                mode.one_turn_character * mode.value(Fraction(1, 3))
            )
            assert mode.value(Fraction(1, 3) + 2) == pytest.approx(
                mode.value(Fraction(1, 3))
            )


def test_boundary_trace_rank_is_derived_from_endpoint_vectors() -> None:
    model = build_native_mobius_standing_wave()
    mode_one_cos = StandingWaveBasisFunction(1, "cos").boundary_trace()
    mode_three_cos = StandingWaveBasisFunction(3, "cos").boundary_trace()
    mode_one_sin = StandingWaveBasisFunction(1, "sin").boundary_trace()
    mode_three_sin = StandingWaveBasisFunction(3, "sin").boundary_trace()

    assert mode_one_cos.vector == pytest.approx(mode_three_cos.vector)
    assert mode_three_sin.vector[2] == pytest.approx(3 * mode_one_sin.vector[2])
    assert mode_three_sin.vector[3] == pytest.approx(3 * mode_one_sin.vector[3])
    assert model.boundary_trace_rank(0) == 1
    assert model.boundary_trace_rank(1) == 2
    assert model.boundary_trace_rank(8) == 2
    assert model.interior_basis_dimension(8) == 17


def test_pcea_capacity_channel_induction_is_falsified_when_trace_rank_is_insufficient() -> None:
    survived = evaluate_capacity_channel_induction(2, max_mode_index=8)
    falsified = evaluate_capacity_channel_induction(3, max_mode_index=8)
    report = run_all()

    assert survived.status == STATUS_SURVIVED
    assert survived.boundary_trace_rank == 2
    assert falsified.status == STATUS_FALSIFIED
    assert not falsified.induces_required_channels
    assert falsified.boundary_trace_rank == 2
    assert falsified.interior_basis_dimension == 17
    assert report["schema"] == MOBIUS_STANDING_WAVE_SCHEMA_ID
    assert report["construction_status"] == STATUS_SURVIVED
    assert report["overall_status_for_pcea_promotion"] == STATUS_FALSIFIED


def test_invalid_standing_wave_requests_raise() -> None:
    with pytest.raises(MobiusStandingWaveError):
        StandingWaveBasisFunction(0, "cos")
    with pytest.raises(MobiusStandingWaveError):
        StandingWaveBasisFunction(1, "constant")
    with pytest.raises(MobiusStandingWaveError):
        evaluate_capacity_channel_induction(0)
