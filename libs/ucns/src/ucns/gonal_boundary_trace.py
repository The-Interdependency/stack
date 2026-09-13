# ratios: loc_comments=226:108 imports_exports=5:7 calls_definitions=76:18
# === MODULE_BUILD ===
# id: ucns_gonal_boundary_trace
#   module_name: gonal_boundary_trace
#   module_kind: instrument
#   summary: exact visible-circle wave-mode trace onto a finite gonal boundary with explicit continuum covering lift candidate
#   owner: Erin Spencer
#   public_surface: GonalBoundaryTraceError, GonalBoundarySample, CircleWaveModeTrace, CircleWaveCoveringTrace, build_circle_wave_mode_trace, pullback_circle_wave_trace
#   internal_surface: canonical residue validation, exact phase-turn construction, covering congruence and equivariance audit
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_gonal_boundary_trace.py
#   rollout: executable candidate geometric bridge on the visible circle boundary; no UCNS ratification or downstream physical selection semantics
#   rollback: remove this module, facade exports, tests, and continuum trace documentation
#   requires: ucns_modular_orbit_geometry
#   since: 2026-09-05
#   unresolved: candidate ratification; lift from visible-circle wave trace into complete native Mobius state; any law selecting a privileged continuum covering lift
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: gonal_boundary_trace_samples_circle_wave_mode_exactly
#   given: modulus m > 1, integer harmonic n, and a nonempty canonical residue carrier
#   then: residue r is placed at exactly r/m visible turns and carries exact spatial wave phase (n*r mod m)/m turns, all as Fraction values
#   class: correctness
#   since: 2026-09-05
#
# id: gonal_boundary_trace_matches_modular_covering_pullback
#   given: a circle-wave trace, modular orbit geometry with the same modulus/carrier, and positive continuum covering degree d congruent to the geometry multiplier modulo m
#   then: pulling the trace through r -> d*r mod m equals the exact trace of harmonic d*n and records matched continuum time scaling t -> d*t
#   class: correctness
#   requires: modular_orbit_action_decomposes_exact_permutation
#   since: 2026-09-05
#
# id: gonal_boundary_trace_requires_explicit_continuum_lift
#   given: one finite modular multiplier a modulo m
#   then: the caller must supply a positive continuum covering degree d with d mod m = a, because d and d+k*m induce the same finite action but distinct harmonic and time scaling
#   class: correctness
#   since: 2026-09-05
#
# id: gonal_boundary_trace_fails_closed_on_incompatible_geometry
#   given: malformed residues, mismatched modulus/carrier, nonpositive covering degree, noninteger time scale, incongruent covering degree, or inconsistent direct record construction
#   then: construction raises GonalBoundaryTraceError rather than inventing a continuum-to-gonal correspondence
#   class: safety
#   since: 2026-09-05
#
# id: gonal_boundary_trace_does_not_select_downstream_physics
#   given: an exact wave trace or covering trace is serialized or consumed
#   then: it records only visible-circle harmonic, gonal sample geometry, explicit continuum covering degree, induced finite multiplier/action, and matched time scaling; it does not assign EPAC, prime, Fibonacci, or other physical significance
#   class: doctrine
#   since: 2026-09-05
#
# id: gonal_boundary_trace_remains_candidate_until_ratified
#   given: the exact executable trace exists without a declared falsifier/replay/ratification receipt selecting it as active UCNS geometry
#   then: repository standing remains candidate even though the represented equations and finite trace identities are exact within their declared model
#   class: doctrine
#   since: 2026-09-06
# === END CONTRACTS ===

"""Exact visible-circle wave-equation trace onto a finite gonal boundary candidate.

Continuum geometry
------------------
On a circle of radius ``R``, with angular coordinate ``theta``, the scalar wave
equation is::

    u_tt = (c^2 / R^2) u_theta_theta

Its periodic spatial harmonics are indexed by integers ``n``. A complex
traveling mode has spatial factor ``exp(i*n*theta)``. This module does not
store floating-point complex amplitudes; it records the exact boundary phase
at finite gonal sample positions.

For an ``m``-gonal visible boundary, residue ``r`` lies at::

    theta_r / (2*pi) = r / m

and harmonic ``n`` has exact spatial phase::

    phase_r / (2*pi) = (n*r mod m) / m.

A positive integer continuum covering degree ``d`` acts on solutions by::

    D_d(theta, t) = (d*theta, d*t)

so ``u(D_d(theta,t))`` is again a solution and harmonic ``n`` maps to harmonic
``d*n``. On the finite gonal trace this becomes::

    r -> d*r mod m.

Only ``d mod m`` is visible in the finite residue action. Therefore a modular
multiplier does not uniquely recover the continuum covering degree: ``d`` and
``d + k*m`` induce the same finite action while carrying different harmonic and
time scaling. The continuum lift is consequently an explicit input, never an
inferred physical selection.

When the finite action is bijective on a declared carrier, the existing
``ModularOrbitGeometry`` records its cycle decomposition. This establishes an
exact candidate continuum-boundary-to-modular-action representation relation
without assigning downstream meaning. Executability and algebraic exactness do
not by themselves ratify the representation as selected UCNS geometry.

The trace is on the visible 360-degree circle boundary only. Its lift into the
complete 720-degree native Mobius state remains ``hmmm``.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable

from .modular_orbit import ModularOrbitGeometry


class GonalBoundaryTraceError(ValueError):
    """Raised when an exact continuum-to-gonal trace cannot be constructed."""


def _validate_modulus(modulus: int) -> None:
    if isinstance(modulus, bool) or not isinstance(modulus, int) or modulus <= 1:
        raise GonalBoundaryTraceError("modulus must be an integer greater than 1")


def _canonical_positions(modulus: int, positions: Iterable[int] | None) -> tuple[int, ...]:
    if positions is None:
        return tuple(range(modulus))
    raw = tuple(positions)
    if not raw:
        raise GonalBoundaryTraceError("positions must be nonempty")
    if any(isinstance(value, bool) or not isinstance(value, int) for value in raw):
        raise GonalBoundaryTraceError("positions must contain integers only")
    if any(value < 0 or value >= modulus for value in raw):
        raise GonalBoundaryTraceError(
            f"positions must be canonical residues in [0, {modulus - 1}]"
        )
    if len(set(raw)) != len(raw):
        raise GonalBoundaryTraceError("positions must not contain duplicate residues")
    return tuple(sorted(raw))


def _phase_turn(harmonic: int, residue: int, modulus: int) -> Fraction:
    return Fraction((harmonic * residue) % modulus, modulus)


def _validate_covering_degree(covering_degree: int) -> None:
    if (
        isinstance(covering_degree, bool)
        or not isinstance(covering_degree, int)
        or covering_degree <= 0
    ):
        raise GonalBoundaryTraceError("covering degree must be a positive integer")


def _validate_time_scale(time_scale: int) -> None:
    if isinstance(time_scale, bool) or not isinstance(time_scale, int) or time_scale <= 0:
        raise GonalBoundaryTraceError("time scale must be a positive integer")


@dataclass(frozen=True, slots=True)
class GonalBoundarySample:
    """One exact visible-circle boundary sample."""

    residue: int
    boundary_turn: Fraction
    phase_turn: Fraction

    def __post_init__(self) -> None:
        if isinstance(self.residue, bool) or not isinstance(self.residue, int):
            raise GonalBoundaryTraceError("sample residue must be an integer")
        for name, value in (
            ("boundary_turn", self.boundary_turn),
            ("phase_turn", self.phase_turn),
        ):
            if not isinstance(value, Fraction) or not 0 <= value < 1:
                raise GonalBoundaryTraceError(
                    f"sample {name} must be an exact Fraction in [0, 1)"
                )


@dataclass(frozen=True, slots=True)
class CircleWaveModeTrace:
    """Exact spatial trace of one integer harmonic on an m-gonal boundary."""

    modulus: int
    harmonic: int
    positions: tuple[int, ...]
    samples: tuple[GonalBoundarySample, ...]

    def __post_init__(self) -> None:
        _validate_modulus(self.modulus)
        if isinstance(self.harmonic, bool) or not isinstance(self.harmonic, int):
            raise GonalBoundaryTraceError("harmonic must be an integer")
        canonical = _canonical_positions(self.modulus, self.positions)
        if canonical != self.positions:
            raise GonalBoundaryTraceError("positions must be sorted canonical residues")
        expected = tuple(
            GonalBoundarySample(
                residue=residue,
                boundary_turn=Fraction(residue, self.modulus),
                phase_turn=_phase_turn(self.harmonic, residue, self.modulus),
            )
            for residue in self.positions
        )
        if self.samples != expected:
            raise GonalBoundaryTraceError(
                "samples must equal the exact harmonic phase trace on the declared carrier"
            )

    def phase_at(self, residue: int) -> Fraction:
        """Return exact spatial phase in normalized turns at one declared position."""

        if isinstance(residue, bool) or not isinstance(residue, int):
            raise GonalBoundaryTraceError("residue must be a nonboolean integer")
        for sample in self.samples:
            if sample.residue == residue:
                return sample.phase_turn
        raise GonalBoundaryTraceError(f"residue {residue!r} is not in this trace")

    def as_dict(self) -> dict[str, object]:
        """Serialize the exact visible-circle trace without physical interpretation."""

        return {
            "modulus": self.modulus,
            "harmonic": self.harmonic,
            "positions": list(self.positions),
            "samples": [
                {
                    "residue": sample.residue,
                    "boundary_turn": {
                        "numerator": sample.boundary_turn.numerator,
                        "denominator": sample.boundary_turn.denominator,
                    },
                    "phase_turn": {
                        "numerator": sample.phase_turn.numerator,
                        "denominator": sample.phase_turn.denominator,
                    },
                }
                for sample in self.samples
            ],
        }


@dataclass(frozen=True, slots=True)
class CircleWaveCoveringTrace:
    """Exact trace-level witness of a continuum degree-d spacetime pullback.

    Direct restoration requires validated trace records and immutable integer
    action pairs. Use ``pullback_circle_wave_trace`` to construct a witness.
    """

    source: CircleWaveModeTrace
    target: CircleWaveModeTrace
    covering_degree: int
    time_scale: int
    action: tuple[tuple[int, int], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.source, CircleWaveModeTrace) or not isinstance(self.target, CircleWaveModeTrace):
            raise GonalBoundaryTraceError("source and target must be CircleWaveModeTrace records")
        if not isinstance(self.action, tuple) or any(
            not isinstance(pair, tuple) or len(pair) != 2
            or any(isinstance(value, bool) or not isinstance(value, int) for value in pair)
            for pair in self.action
        ):
            raise GonalBoundaryTraceError("action must contain immutable nonboolean integer pairs")
        _validate_covering_degree(self.covering_degree)
        _validate_time_scale(self.time_scale)
        if self.time_scale != self.covering_degree:
            raise GonalBoundaryTraceError(
                "wave-equation covering requires matched time scale t -> d*t"
            )
        if self.source.modulus != self.target.modulus:
            raise GonalBoundaryTraceError("source and target moduli must match")
        if self.source.positions != self.target.positions:
            raise GonalBoundaryTraceError("source and target carriers must match")
        if self.target.harmonic != self.source.harmonic * self.covering_degree:
            raise GonalBoundaryTraceError(
                "target harmonic must equal source harmonic times covering degree"
            )
        expected_action = tuple(
            (
                residue,
                (self.covering_degree * residue) % self.source.modulus,
            )
            for residue in self.source.positions
        )
        if self.action != expected_action:
            raise GonalBoundaryTraceError(
                "action must be the exact gonal trace of theta -> d*theta"
            )
        source_positions = set(self.source.positions)
        if any(target not in source_positions for _, target in self.action):
            raise GonalBoundaryTraceError("covering action leaves the declared carrier")

        source_phases = {sample.residue: sample.phase_turn for sample in self.source.samples}
        target_phases = {sample.residue: sample.phase_turn for sample in self.target.samples}
        for source_residue, target_residue in self.action:
            if source_phases[target_residue] != target_phases[source_residue]:
                raise GonalBoundaryTraceError(
                    "trace pullback is not equivariant with harmonic multiplication"
                )

    @property
    def finite_multiplier(self) -> int:
        """Canonical modular multiplier retained by the finite m-gonal trace."""

        return self.covering_degree % self.source.modulus

    def as_dict(self) -> dict[str, object]:
        """Serialize the exact covering witness."""

        return {
            "covering_degree": self.covering_degree,
            "finite_multiplier": self.finite_multiplier,
            "time_scale": self.time_scale,
            "action": [[source, target] for source, target in self.action],
            "source": self.source.as_dict(),
            "target": self.target.as_dict(),
        }


def build_circle_wave_mode_trace(
    modulus: int,
    harmonic: int,
    positions: Iterable[int] | None = None,
) -> CircleWaveModeTrace:
    """Build the exact spatial trace of harmonic ``n`` on an m-gonal boundary."""

    _validate_modulus(modulus)
    if isinstance(harmonic, bool) or not isinstance(harmonic, int):
        raise GonalBoundaryTraceError("harmonic must be an integer")
    resolved_positions = _canonical_positions(modulus, positions)
    samples = tuple(
        GonalBoundarySample(
            residue=residue,
            boundary_turn=Fraction(residue, modulus),
            phase_turn=_phase_turn(harmonic, residue, modulus),
        )
        for residue in resolved_positions
    )
    return CircleWaveModeTrace(
        modulus=modulus,
        harmonic=harmonic,
        positions=resolved_positions,
        samples=samples,
    )


def pullback_circle_wave_trace(
    trace: CircleWaveModeTrace,
    geometry: ModularOrbitGeometry,
    covering_degree: int,
) -> CircleWaveCoveringTrace:
    """Witness one explicit continuum covering above a finite modular action.

    For positive integer ``d``, the circle-wave equation is preserved by
    ``(theta, t) -> (d*theta, d*t)``. On an ``m``-gonal trace, only ``d mod m``
    remains in the residue action. The caller therefore supplies ``d``
    explicitly, and this function requires ``d % m == geometry.multiplier``.
    """

    if not isinstance(trace, CircleWaveModeTrace) or not isinstance(geometry, ModularOrbitGeometry):
        raise GonalBoundaryTraceError("pullback requires validated trace and modular geometry records")
    if trace.modulus != geometry.modulus:
        raise GonalBoundaryTraceError("trace and modular geometry moduli must match")
    if trace.positions != geometry.positions:
        raise GonalBoundaryTraceError("trace and modular geometry carriers must match")
    _validate_covering_degree(covering_degree)
    if covering_degree % trace.modulus != geometry.multiplier:
        raise GonalBoundaryTraceError(
            "covering degree must be congruent to the modular multiplier modulo modulus"
        )

    target = build_circle_wave_mode_trace(
        modulus=trace.modulus,
        harmonic=trace.harmonic * covering_degree,
        positions=trace.positions,
    )
    return CircleWaveCoveringTrace(
        source=trace,
        target=target,
        covering_degree=covering_degree,
        time_scale=covering_degree,
        action=geometry.action,
    )


__all__ = [
    "CircleWaveCoveringTrace",
    "CircleWaveModeTrace",
    "GonalBoundarySample",
    "GonalBoundaryTraceError",
    "build_circle_wave_mode_trace",
    "pullback_circle_wave_trace",
]
# ratios: loc_comments=226:108 imports_exports=5:7 calls_definitions=76:18
