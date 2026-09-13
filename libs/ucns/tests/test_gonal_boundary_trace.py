# ratios: loc_comments=101:51 imports_exports=7:6 calls_definitions=55:7
# === CHECKS ===
# id: check_gonal_boundary_trace_samples_circle_wave_mode_exactly
#   proves: gonal_boundary_trace_samples_circle_wave_mode_exactly
#   call: self::test_circle_wave_mode_trace_is_exact
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_gonal_boundary_trace_matches_modular_covering_pullback
#   proves: gonal_boundary_trace_matches_modular_covering_pullback
#   call: self::test_modular_action_is_exact_wave_covering_trace
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_gonal_boundary_trace_requires_explicit_continuum_lift
#   proves: gonal_boundary_trace_requires_explicit_continuum_lift
#   call: self::test_same_finite_action_admits_distinct_continuum_lifts
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_gonal_boundary_trace_fails_closed_on_incompatible_geometry
#   proves: gonal_boundary_trace_fails_closed_on_incompatible_geometry
#   call: self::test_trace_bridge_fails_closed
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_gonal_boundary_trace_does_not_select_downstream_physics
#   proves: gonal_boundary_trace_does_not_select_downstream_physics
#   call: self::test_trace_surface_is_geometry_only
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_gonal_boundary_trace_candidate_standing
#   proves: gonal_boundary_trace_remains_candidate_until_ratified
#   call: self::test_trace_is_candidate_scoped_in_canon
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from ucns.gonal_boundary_trace import (
    CircleWaveModeTrace,
    GonalBoundaryTraceError,
    build_circle_wave_mode_trace,
    pullback_circle_wave_trace,
)
from ucns.modular_orbit import build_modular_orbit_geometry


def test_circle_wave_mode_trace_is_exact() -> None:
    trace = build_circle_wave_mode_trace(9, 2, range(1, 9))

    assert trace.positions == tuple(range(1, 9))
    assert trace.samples[0].boundary_turn == Fraction(1, 9)
    assert trace.phase_at(1) == Fraction(2, 9)
    assert trace.phase_at(5) == Fraction(1, 9)
    assert trace.phase_at(8) == Fraction(7, 9)


def test_modular_action_is_exact_wave_covering_trace(monkeypatch: pytest.MonkeyPatch) -> None:
    geometry = build_modular_orbit_geometry(9, 2, range(1, 9))
    source = build_circle_wave_mode_trace(9, 1, range(1, 9))

    # Covering validation must use one indexed phase pass rather than invoking
    # the trace's linear phase_at lookup once per action edge.
    def _unexpected_phase_lookup(self: CircleWaveModeTrace, residue: int) -> Fraction:
        raise AssertionError(f"covering validation used phase_at({residue})")

    monkeypatch.setattr(CircleWaveModeTrace, "phase_at", _unexpected_phase_lookup)
    covering = pullback_circle_wave_trace(source, geometry, 2)

    assert covering.covering_degree == 2
    assert covering.finite_multiplier == 2
    assert covering.time_scale == 2
    assert covering.target.harmonic == 2
    assert covering.action == geometry.action
    source_phases = {sample.residue: sample.phase_turn for sample in source.samples}
    target_phases = {sample.residue: sample.phase_turn for sample in covering.target.samples}
    for source_residue, target_residue in geometry.action:
        assert source_phases[target_residue] == target_phases[source_residue]


def test_same_finite_action_admits_distinct_continuum_lifts() -> None:
    geometry = build_modular_orbit_geometry(9, 2, range(1, 9))
    source = build_circle_wave_mode_trace(9, 1, range(1, 9))

    degree_2 = pullback_circle_wave_trace(source, geometry, 2)
    degree_11 = pullback_circle_wave_trace(source, geometry, 11)

    assert degree_2.action == degree_11.action == geometry.action
    assert degree_2.finite_multiplier == degree_11.finite_multiplier == 2
    assert degree_2.target.harmonic == 2
    assert degree_11.target.harmonic == 11
    assert degree_2.time_scale == 2
    assert degree_11.time_scale == 11

    zero_mod_geometry = build_modular_orbit_geometry(9, 0, (0,))
    zero_trace = build_circle_wave_mode_trace(9, 1, (0,))
    degree_9 = pullback_circle_wave_trace(zero_trace, zero_mod_geometry, 9)
    assert degree_9.covering_degree == 9
    assert degree_9.finite_multiplier == 0
    assert degree_9.target.harmonic == 9


def test_trace_bridge_fails_closed() -> None:
    source = build_circle_wave_mode_trace(9, 1, range(1, 9))
    wrong_modulus = build_modular_orbit_geometry(7, 2, range(1, 7))
    with pytest.raises(GonalBoundaryTraceError, match="moduli must match"):
        pullback_circle_wave_trace(source, wrong_modulus, 2)

    wrong_carrier = build_modular_orbit_geometry(9, 2, (1, 2, 4, 5, 7, 8))
    with pytest.raises(GonalBoundaryTraceError, match="carriers must match"):
        pullback_circle_wave_trace(source, wrong_carrier, 2)

    geometry = build_modular_orbit_geometry(9, 2, range(1, 9))
    with pytest.raises(GonalBoundaryTraceError, match="positive integer"):
        pullback_circle_wave_trace(source, geometry, 0)
    with pytest.raises(GonalBoundaryTraceError, match="congruent"):
        pullback_circle_wave_trace(source, geometry, 3)

    valid = pullback_circle_wave_trace(source, geometry, 2)
    with pytest.raises(GonalBoundaryTraceError, match="time scale must be a positive integer"):
        replace(valid, time_scale=True)
    with pytest.raises(GonalBoundaryTraceError, match="time scale must be a positive integer"):
        replace(valid, time_scale=2.0)  # type: ignore[arg-type]

    identity = build_modular_orbit_geometry(3, 1)
    trace = build_circle_wave_mode_trace(3, 1)
    covering = pullback_circle_wave_trace(trace, identity, 1)
    for action in (((False, False), (True, True), (2.0, 2.0)), None, [[0, 0], [1, 1], [2, 2]]):
        with pytest.raises(GonalBoundaryTraceError):
            replace(covering, action=action)
    for query in (True, False, 1.0, Fraction(1), "1", []):
        with pytest.raises(GonalBoundaryTraceError):
            trace.phase_at(query)
    with pytest.raises(GonalBoundaryTraceError):
        replace(covering, source=None)
    with pytest.raises(GonalBoundaryTraceError):
        pullback_circle_wave_trace(trace, None, 1)


def test_trace_surface_is_geometry_only() -> None:
    geometry = build_modular_orbit_geometry(9, 7, range(1, 9))
    source = build_circle_wave_mode_trace(9, 2, range(1, 9))
    payload = pullback_circle_wave_trace(source, geometry, 7).as_dict()
    text = repr(payload).lower()

    assert payload["covering_degree"] == 7
    assert payload["finite_multiplier"] == 7
    assert payload["time_scale"] == 7
    assert payload["target"]["harmonic"] == 14
    for forbidden in ("epac", "pcea", "fibonacci", "prime", "particle", "energy"):
        assert forbidden not in text


def test_trace_is_candidate_scoped_in_canon() -> None:
    canon = (Path(__file__).resolve().parents[1] / "CANON.md").read_text(encoding="utf-8")
    section = canon.split("## Continuum wave / gonal boundary trace", 1)[1].split(
        "## Retained research", 1
    )[0]

    assert "candidate" in section.lower()
    assert "not ratified" in section.lower()
# ratios: loc_comments=101:51 imports_exports=7:6 calls_definitions=55:7
