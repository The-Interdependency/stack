# === MODULE_BUILD ===
# id: ucns_mobius_standing_wave_root_loop
#   module_name: mobius_standing_wave
#   module_kind: experiment
#   summary: explicit scalar standing-wave continuum model on the native two-turn Mobius root loop, with derived boundary trace and capacity-channel falsifier
#   owner: Erin Spencer
#   public_surface: BoundaryCapacityInduction, BoundaryTrace, StandingWaveBasisFunction, StandingWaveModel, build_native_mobius_standing_wave, evaluate_capacity_channel_induction, run_all
#   internal_surface: _matrix_rank, _positive_int, _validate_basis
#   auth_boundary: none
#   storage_boundary: immutable model records only
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_mobius_standing_wave.py
#   rollout: geometry-only candidate; no PCEA promotion and no spectral/zeta claim
#   rollback: remove module, facade exports, tests, and README note
#   requires: ucns_native_mobius_geometry
#   since: 2026-09-06
#   unresolved: higher-dimensional UCNS domain, physical boundary beyond quotient seam, PCEA boundary-capacity channel map
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: mobius_standing_wave_declares_operator_domain_bc_trace
#   given: the native Mobius root-loop quotient supplies a complete two-turn continuum coordinate
#   then:  the model declares the wave equation, spatial operator, domain, boundary conditions, admissible basis, and boundary trace object
#   class: evidence
#   since: 2026-09-06
#
# id: mobius_standing_wave_modes_satisfy_operator_and_boundary_conditions
#   given: a finite admissible standing-wave basis is generated on the two-turn root loop
#   then:  every basis function satisfies -X'' = lambda X and the complete-return endpoint conditions X(0)=X(2), X'(0)=X'(2)
#   class: correctness
#   since: 2026-09-06
#
# id: mobius_standing_wave_boundary_trace_is_derived_not_assigned
#   given: a basis function is traced at the quotient seam
#   then:  trace values and derivatives are computed from the function endpoints and their rank is derived from those vectors
#   class: safety
#   since: 2026-09-06
#
# id: mobius_standing_wave_falsifies_pcea_capacity_channel_induction
#   given: PCEA-style boundary capacity asks for more independent channels than the native root-loop trace rank
#   then:  the induction report is FALSIFIED rather than assigning extra channels or treating discrete spectra as a PDE derivation
#   class: safety
#   since: 2026-09-06
# === END CONTRACTS ===

"""Standing-wave continuum model on the native Mobius root loop.

The only continuum coordinate used here is the one UCNS already exposes: the
native two-turn Mobius root loop. Let ``t`` be visible turns on ``[0, 2]``.
For a scalar displacement field ``psi(t, tau)``, the smallest standing-wave
model is

    d2 psi / d tau2 = c^2 d2 psi / d t2

with spatial operator ``L X = -d2 X / dt2`` and complete-return boundary
conditions

    X(0) = X(2),    X'(0) = X'(2).

The admissible spatial basis is ``1``, ``cos(n*pi*t)``, and ``sin(n*pi*t)`` for
positive integer ``n``. One visible turn multiplies each positive mode by
``(-1)^n``; two visible turns restore it.

This is not a spectral/zeta theorem, not a physical field theory, and not a
PCEA result. It gives PCEA a concrete UCNS trace to inspect; in this smallest
model, that trace has rank at most two and therefore does not induce an
arbitrary boundary-measure-indexed capacity channel family.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from math import cos, isfinite, pi, sin
from typing import Iterable, Literal

from .direct_mobius import NATIVE_MOBIUS_LAW_ID, NATIVE_MOBIUS_LAW_VERSION

MOBIUS_STANDING_WAVE_SCHEMA_ID = "ucns.mobius-standing-wave-root-loop"
MOBIUS_STANDING_WAVE_SCHEMA_VERSION = "0.1.0"
SPATIAL_OPERATOR = "L X = -d2 X / dt2"
WAVE_EQUATION = "d2 psi / d tau2 = c^2 d2 psi / d t2"
DOMAIN = (Fraction(0), Fraction(2))
BOUNDARY_CONDITIONS = ("X(0)=X(2)", "X'(0)=X'(2)")
ADMISSIBLE_SOLUTION_FAMILY = "span{1, cos(n*pi*t), sin(n*pi*t) for n >= 1}"
STATUS_SURVIVED = "SURVIVED"
STATUS_FALSIFIED = "FALSIFIED"
STATUS_UNRESOLVED = "UNRESOLVED"
STATUS_BLOCKED = "BLOCKED"

BasisKind = Literal["constant", "cos", "sin"]


class MobiusStandingWaveError(ValueError):
    """Raised when a standing-wave request leaves the declared model."""


@dataclass(frozen=True, slots=True)
class BoundaryTrace:
    """Endpoint value/derivative trace on the quotient seam."""

    mode_index: int
    basis_kind: BasisKind
    value_at_zero: float
    value_at_two: float
    derivative_at_zero: float
    derivative_at_two: float

    @property
    def value_residual(self) -> float:
        return abs(self.value_at_zero - self.value_at_two)

    @property
    def derivative_residual(self) -> float:
        return abs(self.derivative_at_zero - self.derivative_at_two)

    @property
    def vector(self) -> tuple[float, float, float, float]:
        return (
            self.value_at_zero,
            self.value_at_two,
            self.derivative_at_zero,
            self.derivative_at_two,
        )

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class StandingWaveBasisFunction:
    """One admissible spatial basis function on the two-turn root loop."""

    mode_index: int
    basis_kind: BasisKind

    def __post_init__(self) -> None:
        _validate_basis(self.mode_index, self.basis_kind)

    @property
    def eigenvalue(self) -> float:
        return (self.mode_index * pi) ** 2

    @property
    def one_turn_character(self) -> int:
        if self.mode_index == 0:
            return 1
        return 1 if self.mode_index % 2 == 0 else -1

    @property
    def formula(self) -> str:
        if self.basis_kind == "constant":
            return "1"
        return f"{self.basis_kind}({self.mode_index}*pi*t)"

    def value(self, turn: float | Fraction | int) -> float:
        t = _finite_turn(turn)
        if self.basis_kind == "constant":
            return 1.0
        angle = self.mode_index * pi * t
        return cos(angle) if self.basis_kind == "cos" else sin(angle)

    def first_derivative(self, turn: float | Fraction | int) -> float:
        t = _finite_turn(turn)
        if self.basis_kind == "constant":
            return 0.0
        npi = self.mode_index * pi
        angle = npi * t
        return -npi * sin(angle) if self.basis_kind == "cos" else npi * cos(angle)

    def second_derivative(self, turn: float | Fraction | int) -> float:
        t = _finite_turn(turn)
        if self.basis_kind == "constant":
            return 0.0
        npi = self.mode_index * pi
        angle = npi * t
        return -(npi**2) * (cos(angle) if self.basis_kind == "cos" else sin(angle))

    def spatial_operator_residual(self, turn: float | Fraction | int) -> float:
        return abs(-self.second_derivative(turn) - self.eigenvalue * self.value(turn))

    def boundary_trace(self) -> BoundaryTrace:
        if self.basis_kind == "constant":
            vector = (1.0, 1.0, 0.0, 0.0)
        elif self.basis_kind == "cos":
            vector = (1.0, 1.0, 0.0, 0.0)
        else:
            derivative = self.mode_index * pi
            vector = (0.0, 0.0, derivative, derivative)
        return BoundaryTrace(
            mode_index=self.mode_index,
            basis_kind=self.basis_kind,
            value_at_zero=vector[0],
            value_at_two=vector[1],
            derivative_at_zero=vector[2],
            derivative_at_two=vector[3],
        )

    def boundary_condition_residuals(self) -> tuple[float, float]:
        trace = self.boundary_trace()
        return trace.value_residual, trace.derivative_residual

    def as_dict(self) -> dict[str, object]:
        return {
            "mode_index": self.mode_index,
            "basis_kind": self.basis_kind,
            "formula": self.formula,
            "eigenvalue": self.eigenvalue,
            "one_turn_character": self.one_turn_character,
            "boundary_trace": self.boundary_trace().as_dict(),
        }


@dataclass(frozen=True, slots=True)
class StandingWaveModel:
    """Declared continuum standing-wave model derived from the root-loop law."""

    schema_id: str = MOBIUS_STANDING_WAVE_SCHEMA_ID
    schema_version: str = MOBIUS_STANDING_WAVE_SCHEMA_VERSION
    source_law_id: str = NATIVE_MOBIUS_LAW_ID
    source_law_version: str = NATIVE_MOBIUS_LAW_VERSION
    wave_equation: str = WAVE_EQUATION
    spatial_operator: str = SPATIAL_OPERATOR
    domain: tuple[Fraction, Fraction] = DOMAIN
    boundary_conditions: tuple[str, str] = BOUNDARY_CONDITIONS
    admissible_solution_family: str = ADMISSIBLE_SOLUTION_FAMILY

    def basis_functions(self, max_mode_index: int) -> tuple[StandingWaveBasisFunction, ...]:
        count = _positive_int(max_mode_index, "max_mode_index", allow_zero=True)
        basis: list[StandingWaveBasisFunction] = [StandingWaveBasisFunction(0, "constant")]
        for mode_index in range(1, count + 1):
            basis.append(StandingWaveBasisFunction(mode_index, "cos"))
            basis.append(StandingWaveBasisFunction(mode_index, "sin"))
        return tuple(basis)

    def interior_basis_dimension(self, max_mode_index: int) -> int:
        return len(self.basis_functions(max_mode_index))

    def boundary_traces(self, max_mode_index: int) -> tuple[BoundaryTrace, ...]:
        return tuple(mode.boundary_trace() for mode in self.basis_functions(max_mode_index))

    def boundary_trace_rank(self, max_mode_index: int, *, tolerance: float = 1e-10) -> int:
        return _matrix_rank(
            (trace.vector for trace in self.boundary_traces(max_mode_index)),
            tolerance=tolerance,
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "source_law_id": self.source_law_id,
            "source_law_version": self.source_law_version,
            "wave_equation": self.wave_equation,
            "spatial_operator": self.spatial_operator,
            "domain": [str(value) for value in self.domain],
            "boundary_conditions": self.boundary_conditions,
            "admissible_solution_family": self.admissible_solution_family,
            "nonclaims": (
                "not a spectral or zeta-function theorem",
                "not a physical field theory",
                "not a PCEA boundary-capacity promotion",
            ),
        }


@dataclass(frozen=True, slots=True)
class BoundaryCapacityInduction:
    """Verdict for whether the root-loop trace supplies requested channels."""

    required_capacity_channels: int
    max_mode_index: int
    interior_basis_dimension: int
    boundary_trace_rank: int
    status: str
    reason: str

    @property
    def induces_required_channels(self) -> bool:
        return self.status == STATUS_SURVIVED

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def _finite_turn(value: float | Fraction | int) -> float:
    if isinstance(value, bool):
        raise MobiusStandingWaveError("turn cannot be boolean")
    result = float(value)
    if not isfinite(result):
        raise MobiusStandingWaveError("turn must be finite")
    return result


def _positive_int(value: int, name: str, *, allow_zero: bool = False) -> int:
    if type(value) is not int:
        raise MobiusStandingWaveError(f"{name} must be an integer")
    minimum = 0 if allow_zero else 1
    if value < minimum:
        raise MobiusStandingWaveError(f"{name} must be at least {minimum}")
    return value


def _validate_basis(mode_index: int, basis_kind: BasisKind) -> None:
    _positive_int(mode_index, "mode_index", allow_zero=True)
    if basis_kind not in ("constant", "cos", "sin"):
        raise MobiusStandingWaveError("basis_kind must be constant, cos, or sin")
    if mode_index == 0 and basis_kind != "constant":
        raise MobiusStandingWaveError("mode zero admits only the constant basis")
    if mode_index > 0 and basis_kind == "constant":
        raise MobiusStandingWaveError("positive modes admit only cos or sin basis functions")


def _matrix_rank(rows: Iterable[Iterable[float]], *, tolerance: float = 1e-10) -> int:
    matrix = [[float(value) for value in row] for row in rows]
    if not matrix:
        return 0
    width = len(matrix[0])
    rank = 0
    for column in range(width):
        pivot = max(range(rank, len(matrix)), key=lambda row: abs(matrix[row][column]))
        if abs(matrix[pivot][column]) <= tolerance:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [value / pivot_value for value in matrix[rank]]
        for row_index in range(len(matrix)):
            if row_index == rank:
                continue
            factor = matrix[row_index][column]
            if abs(factor) <= tolerance:
                continue
            matrix[row_index] = [
                value - factor * pivot_entry
                for value, pivot_entry in zip(matrix[row_index], matrix[rank])
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def build_native_mobius_standing_wave() -> StandingWaveModel:
    """Return the smallest continuum model justified by the native root loop."""

    return StandingWaveModel()


def evaluate_capacity_channel_induction(
    required_capacity_channels: int,
    *,
    max_mode_index: int = 4,
) -> BoundaryCapacityInduction:
    """Test whether the root-loop boundary trace supplies requested channels."""

    required = _positive_int(required_capacity_channels, "required_capacity_channels")
    model = build_native_mobius_standing_wave()
    trace_rank = model.boundary_trace_rank(max_mode_index)
    interior_dimension = model.interior_basis_dimension(max_mode_index)
    if required <= trace_rank:
        status = STATUS_SURVIVED
        reason = (
            "the requested finite channel count fits the derived root-loop "
            "trace rank; this does not establish boundary-measure scaling"
        )
    else:
        status = STATUS_FALSIFIED
        reason = (
            "the derived root-loop trace rank is smaller than the requested "
            "capacity channels; extra channels are not assigned"
        )
    return BoundaryCapacityInduction(
        required_capacity_channels=required,
        max_mode_index=max_mode_index,
        interior_basis_dimension=interior_dimension,
        boundary_trace_rank=trace_rank,
        status=status,
        reason=reason,
    )


def run_all() -> dict[str, object]:
    """Return a compact construction and falsification report."""

    model = build_native_mobius_standing_wave()
    sample_modes = [mode.as_dict() for mode in model.basis_functions(3)]
    induction = evaluate_capacity_channel_induction(3, max_mode_index=3)
    return {
        "schema": MOBIUS_STANDING_WAVE_SCHEMA_ID,
        "schema_version": MOBIUS_STANDING_WAVE_SCHEMA_VERSION,
        "construction_status": STATUS_SURVIVED,
        "model": model.as_dict(),
        "sample_modes": sample_modes,
        "trace_rank_through_mode_3": model.boundary_trace_rank(3),
        "interior_dimension_through_mode_3": model.interior_basis_dimension(3),
        "pcea_capacity_channel_induction": induction.as_dict(),
        "overall_status_for_pcea_promotion": induction.status,
        "hmmm": (
            "higher-dimensional UCNS domain",
            "physical boundary beyond quotient seam",
            "boundary-measure-indexed capacity channel map",
        ),
    }


__all__ = [
    "ADMISSIBLE_SOLUTION_FAMILY",
    "BOUNDARY_CONDITIONS",
    "DOMAIN",
    "MOBIUS_STANDING_WAVE_SCHEMA_ID",
    "MOBIUS_STANDING_WAVE_SCHEMA_VERSION",
    "SPATIAL_OPERATOR",
    "STATUS_BLOCKED",
    "STATUS_FALSIFIED",
    "STATUS_SURVIVED",
    "STATUS_UNRESOLVED",
    "WAVE_EQUATION",
    "BoundaryCapacityInduction",
    "BoundaryTrace",
    "MobiusStandingWaveError",
    "StandingWaveBasisFunction",
    "StandingWaveModel",
    "build_native_mobius_standing_wave",
    "evaluate_capacity_channel_induction",
    "run_all",
]
