# === MODULE_BUILD ===
# id: ucns_mobius_band_standing_wave
#   module_name: mobius_band_standing_wave
#   module_kind: experiment
#   summary: explicit scalar standing-wave continuum model on the canonical Mobius band coordinate domain, with derived physical-boundary trace ranks and bulk-overadmission falsifier
#   owner: Erin Spencer
#   public_surface: BandBoundaryTraceSamples, BandCapacityInduction, MobiusBandBasisFunction, MobiusBandDomain, MobiusBandStandingWaveModel, build_mobius_band_standing_wave, evaluate_band_capacity_channel_induction, run_all_mobius_band
#   internal_surface: _as_positive_fraction, _finite_coordinate, _matrix_rank, _positive_int
#   auth_boundary: none
#   storage_boundary: immutable model records only
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_mobius_band_standing_wave.py
#   rollout: geometry-only candidate; no PCEA promotion, no embedded Laplace-Beltrami claim, and no spectral/zeta claim
#   rollback: remove module, facade exports, tests, README note, and standing-wave band document
#   requires: ucns_mobius_vesica_exact_embedding, ucns_mobius_standing_wave_root_loop
#   since: 2026-09-06
#   unresolved: embedded Laplace-Beltrami operator, exact continuum trace capacity theorem, PCEA boundary-channel encoding map
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: mobius_band_standing_wave_declares_operator_domain_bc_trace
#   given: the canonical Mobius ribbon supplies a two-turn coordinate domain with signed breadth
#   then:  the model declares the coordinate-domain wave equation, spatial operator, Mobius quotient, physical edge boundary conditions, admissible basis, and boundary trace object
#   class: evidence
#   since: 2026-09-06
#
# id: mobius_band_standing_wave_modes_satisfy_operator_and_boundary_conditions
#   given: admissible finite standing-wave modes are generated on the Mobius band coordinate domain
#   then:  every mode satisfies the coordinate Laplacian eigen-equation, the one-turn Mobius seam law, two-turn return, and physical-edge Neumann boundary condition
#   class: correctness
#   since: 2026-09-06
#
# id: mobius_band_boundary_trace_rank_is_derived_not_assigned
#   given: finite boundary samples are taken from the physical Mobius boundary
#   then:  capacity rank is computed from evaluated trace vectors and transverse bulk modes do not add independent boundary channels by assignment
#   class: safety
#   since: 2026-09-06
#
# id: mobius_band_boundary_capacity_falsifies_bulk_only_counting
#   given: a requested channel count is less than the interior basis dimension but greater than the derived boundary trace rank
#   then:  the capacity report is FALSIFIED rather than promoting bulk measure to boundary capacity
#   class: safety
#   since: 2026-09-06
# === END CONTRACTS ===

"""Standing-wave continuum model on the Mobius band coordinate domain.

This module is the largest continuum standing-wave construction currently
justified by the UCNS geometry already present in the package.  It lifts the
root-loop model from one coordinate to the canonical Mobius ribbon coordinate
domain

    (t, u) in [0, 2] x [-w, w],    (t + 1, u) ~ (t, -u).

The spatial operator is the coordinate-domain flat strip Laplacian

    L X = -(d2 X / dt2 + d2 X / du2)

with Neumann conditions on the physical strip edge.  The Neumann choice keeps
the boundary value trace observable while declaring an actual standing-wave
boundary condition.  The basis is separable: the one-turn longitudinal sign
``(-1)^n`` must match the transverse parity under ``u -> -u``.

This is not an embedded Laplace-Beltrami construction for the realized
three-dimensional ribbon, not a spectral/zeta theorem, and not a PCEA
promotion.  It supplies a falsifiable boundary trace: finite capacity channels
are induced only up to the rank of evaluated boundary trace vectors.  Interior
transverse modes increase bulk basis dimension without automatically increasing
boundary trace rank.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from fractions import Fraction
from math import cos, isfinite, pi, sin
from typing import Iterable, Literal

from .mobius_vesica import MobiusVesicaParameters

MOBIUS_BAND_STANDING_WAVE_SCHEMA_ID = "ucns.mobius-band-standing-wave"
MOBIUS_BAND_STANDING_WAVE_SCHEMA_VERSION = "0.1.0"
STATUS_SURVIVED = "SURVIVED"
STATUS_FALSIFIED = "FALSIFIED"
STATUS_UNRESOLVED = "UNRESOLVED"
STATUS_BLOCKED = "BLOCKED"
DEFAULT_HALF_WIDTH = MobiusVesicaParameters().half_width
TURN_DOMAIN = (Fraction(0), Fraction(2))
SPATIAL_OPERATOR = "L X = -(d2 X / dt2 + d2 X / du2)"
WAVE_EQUATION = "d2 psi / d tau2 = c^2 * (d2 psi / d t2 + d2 psi / d u2)"
MOBIUS_QUOTIENT = "(t+1, u) ~ (t, -u)"
PHYSICAL_BOUNDARY = "single continuous boundary traced as u=+w over t in [0,2)"
BOUNDARY_CONDITIONS = (
    "X(t+1,u)=X(t,-u)",
    "dX/dt(t+1,u)=dX/dt(t,-u)",
    "dX/du(t+1,u)=-dX/du(t,-u)",
    "dX/du(t,+w)=0",
    "dX/du(t,-w)=0",
)
ADMISSIBLE_SOLUTION_FAMILY = (
    "span{longitudinal n*pi modes whose one-turn character matches transverse "
    "Neumann parity on [-w,w]}"
)

LongitudinalKind = Literal["constant", "cos", "sin"]
TransverseKind = Literal["even_neumann", "odd_neumann"]


class MobiusBandStandingWaveError(ValueError):
    """Raised when a standing-wave request leaves the declared band model."""


@dataclass(frozen=True, slots=True)
class MobiusBandDomain:
    """Coordinate domain for one canonical Mobius band."""

    half_width: Fraction = DEFAULT_HALF_WIDTH
    turn_domain: tuple[Fraction, Fraction] = TURN_DOMAIN
    mobius_quotient: str = MOBIUS_QUOTIENT
    physical_boundary: str = PHYSICAL_BOUNDARY

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "half_width",
            _as_positive_fraction(self.half_width, "half_width"),
        )
        if self.turn_domain != TURN_DOMAIN:
            raise MobiusBandStandingWaveError("turn_domain must be the complete two-turn domain")

    @property
    def breadth_domain(self) -> tuple[Fraction, Fraction]:
        return -self.half_width, self.half_width

    def as_dict(self) -> dict[str, object]:
        return {
            "turn_domain": [str(value) for value in self.turn_domain],
            "breadth_domain": [str(value) for value in self.breadth_domain],
            "mobius_quotient": self.mobius_quotient,
            "physical_boundary": self.physical_boundary,
        }


@dataclass(frozen=True, slots=True)
class BandBoundaryTraceSamples:
    """Finite value/normal-derivative samples from the continuous boundary."""

    sample_count: int
    half_width: Fraction
    values: tuple[float, ...]
    normal_derivatives: tuple[float, ...]
    include_normal_derivative: bool = False

    @property
    def vector(self) -> tuple[float, ...]:
        if self.include_normal_derivative:
            return self.values + self.normal_derivatives
        return self.values

    def as_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["half_width"] = str(self.half_width)
        return payload


@dataclass(frozen=True, slots=True)
class MobiusBandBasisFunction:
    """One separable admissible basis function on the Mobius band domain."""

    longitudinal_index: int
    longitudinal_kind: LongitudinalKind
    transverse_index: int
    transverse_kind: TransverseKind
    half_width: Fraction = DEFAULT_HALF_WIDTH

    def __post_init__(self) -> None:
        _positive_int(self.longitudinal_index, "longitudinal_index", allow_zero=True)
        _positive_int(self.transverse_index, "transverse_index", allow_zero=True)
        object.__setattr__(
            self,
            "half_width",
            _as_positive_fraction(self.half_width, "half_width"),
        )
        if self.longitudinal_kind not in ("constant", "cos", "sin"):
            raise MobiusBandStandingWaveError(
                "longitudinal_kind must be constant, cos, or sin"
            )
        if self.transverse_kind not in ("even_neumann", "odd_neumann"):
            raise MobiusBandStandingWaveError(
                "transverse_kind must be even_neumann or odd_neumann"
            )
        if self.longitudinal_index == 0 and self.longitudinal_kind != "constant":
            raise MobiusBandStandingWaveError(
                "longitudinal zero admits only the constant basis"
            )
        if self.longitudinal_index > 0 and self.longitudinal_kind == "constant":
            raise MobiusBandStandingWaveError(
                "positive longitudinal modes admit only cos or sin"
            )
        if self.one_turn_character != self.transverse_parity:
            raise MobiusBandStandingWaveError(
                "Mobius quotient requires longitudinal one-turn character to match transverse parity"
            )

    @property
    def one_turn_character(self) -> int:
        return 1 if self.longitudinal_index % 2 == 0 else -1

    @property
    def transverse_parity(self) -> int:
        return 1 if self.transverse_kind == "even_neumann" else -1

    @property
    def longitudinal_wave_number(self) -> float:
        return self.longitudinal_index * pi

    @property
    def transverse_wave_number(self) -> float:
        width = float(self.half_width)
        if self.transverse_kind == "even_neumann":
            return self.transverse_index * pi / width
        return (self.transverse_index + 0.5) * pi / width

    @property
    def eigenvalue(self) -> float:
        return self.longitudinal_wave_number**2 + self.transverse_wave_number**2

    @property
    def formula(self) -> str:
        if self.longitudinal_kind == "constant":
            longitudinal = "1"
        else:
            longitudinal = f"{self.longitudinal_kind}({self.longitudinal_index}*pi*t)"
        if self.transverse_kind == "even_neumann":
            transverse = f"cos({self.transverse_index}*pi*u/w)"
        else:
            transverse = f"sin(({self.transverse_index}+1/2)*pi*u/w)"
        return f"{longitudinal} * {transverse}"

    def longitudinal_value(self, turn: float | Fraction | int) -> float:
        t = _finite_coordinate(turn, "turn")
        if self.longitudinal_kind == "constant":
            return 1.0
        angle = self.longitudinal_wave_number * t
        return cos(angle) if self.longitudinal_kind == "cos" else sin(angle)

    def longitudinal_first_derivative(self, turn: float | Fraction | int) -> float:
        t = _finite_coordinate(turn, "turn")
        if self.longitudinal_kind == "constant":
            return 0.0
        wave_number = self.longitudinal_wave_number
        angle = wave_number * t
        if self.longitudinal_kind == "cos":
            return -wave_number * sin(angle)
        return wave_number * cos(angle)

    def longitudinal_second_derivative(self, turn: float | Fraction | int) -> float:
        t = _finite_coordinate(turn, "turn")
        if self.longitudinal_kind == "constant":
            return 0.0
        return -(self.longitudinal_wave_number**2) * self.longitudinal_value(t)

    def transverse_value(self, breadth: float | Fraction | int) -> float:
        u = _finite_coordinate(breadth, "breadth")
        angle = self.transverse_wave_number * u
        if self.transverse_kind == "even_neumann":
            return cos(angle)
        return sin(angle)

    def transverse_first_derivative(self, breadth: float | Fraction | int) -> float:
        u = _finite_coordinate(breadth, "breadth")
        wave_number = self.transverse_wave_number
        angle = wave_number * u
        if self.transverse_kind == "even_neumann":
            return -wave_number * sin(angle)
        return wave_number * cos(angle)

    def transverse_second_derivative(self, breadth: float | Fraction | int) -> float:
        u = _finite_coordinate(breadth, "breadth")
        return -(self.transverse_wave_number**2) * self.transverse_value(u)

    def value(
        self,
        turn: float | Fraction | int,
        breadth: float | Fraction | int,
    ) -> float:
        return self.longitudinal_value(turn) * self.transverse_value(breadth)

    def turn_derivative(
        self,
        turn: float | Fraction | int,
        breadth: float | Fraction | int,
    ) -> float:
        return self.longitudinal_first_derivative(turn) * self.transverse_value(breadth)

    def breadth_derivative(
        self,
        turn: float | Fraction | int,
        breadth: float | Fraction | int,
    ) -> float:
        return self.longitudinal_value(turn) * self.transverse_first_derivative(breadth)

    def second_turn_derivative(
        self,
        turn: float | Fraction | int,
        breadth: float | Fraction | int,
    ) -> float:
        return self.longitudinal_second_derivative(turn) * self.transverse_value(breadth)

    def second_breadth_derivative(
        self,
        turn: float | Fraction | int,
        breadth: float | Fraction | int,
    ) -> float:
        return self.longitudinal_value(turn) * self.transverse_second_derivative(breadth)

    def spatial_operator_residual(
        self,
        turn: float | Fraction | int,
        breadth: float | Fraction | int,
    ) -> float:
        lhs = -(
            self.second_turn_derivative(turn, breadth)
            + self.second_breadth_derivative(turn, breadth)
        )
        rhs = self.eigenvalue * self.value(turn, breadth)
        return abs(lhs - rhs)

    def mobius_seam_residual(
        self,
        turn: float | Fraction | int,
        breadth: float | Fraction | int,
    ) -> float:
        t = _finite_coordinate(turn, "turn")
        u = _finite_coordinate(breadth, "breadth")
        return max(
            abs(self.value(t + 1.0, u) - self.value(t, -u)),
            abs(self.turn_derivative(t + 1.0, u) - self.turn_derivative(t, -u)),
            abs(
                self.breadth_derivative(t + 1.0, u)
                + self.breadth_derivative(t, -u)
            ),
        )

    def two_turn_return_residual(
        self,
        turn: float | Fraction | int,
        breadth: float | Fraction | int,
    ) -> float:
        t = _finite_coordinate(turn, "turn")
        u = _finite_coordinate(breadth, "breadth")
        return max(
            abs(self.value(t + 2.0, u) - self.value(t, u)),
            abs(self.turn_derivative(t + 2.0, u) - self.turn_derivative(t, u)),
            abs(self.breadth_derivative(t + 2.0, u) - self.breadth_derivative(t, u)),
        )

    def physical_boundary_residual(
        self,
        sample_turns: Iterable[float | Fraction | int] = (
            Fraction(0),
            Fraction(1, 7),
            Fraction(1, 2),
            Fraction(8, 7),
        ),
    ) -> float:
        width = self.half_width
        residual = 0.0
        for turn in sample_turns:
            residual = max(
                residual,
                abs(self.breadth_derivative(turn, width)),
                abs(self.breadth_derivative(turn, -width)),
            )
        return residual

    def boundary_trace(
        self,
        sample_count: int,
        *,
        include_normal_derivative: bool = False,
    ) -> BandBoundaryTraceSamples:
        samples = _positive_int(sample_count, "sample_count")
        width = self.half_width
        values = tuple(
            self.value(Fraction(2 * index, samples), width)
            for index in range(samples)
        )
        normal_derivatives = tuple(
            self.breadth_derivative(Fraction(2 * index, samples), width)
            for index in range(samples)
        )
        return BandBoundaryTraceSamples(
            sample_count=samples,
            half_width=width,
            values=values,
            normal_derivatives=normal_derivatives,
            include_normal_derivative=include_normal_derivative,
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "longitudinal_index": self.longitudinal_index,
            "longitudinal_kind": self.longitudinal_kind,
            "transverse_index": self.transverse_index,
            "transverse_kind": self.transverse_kind,
            "half_width": str(self.half_width),
            "formula": self.formula,
            "one_turn_character": self.one_turn_character,
            "transverse_parity": self.transverse_parity,
            "eigenvalue": self.eigenvalue,
        }


@dataclass(frozen=True, slots=True)
class MobiusBandStandingWaveModel:
    """Declared coordinate-domain standing-wave model for the Mobius band."""

    domain: MobiusBandDomain = field(default_factory=MobiusBandDomain)
    schema_id: str = MOBIUS_BAND_STANDING_WAVE_SCHEMA_ID
    schema_version: str = MOBIUS_BAND_STANDING_WAVE_SCHEMA_VERSION
    wave_equation: str = WAVE_EQUATION
    spatial_operator: str = SPATIAL_OPERATOR
    boundary_conditions: tuple[str, ...] = BOUNDARY_CONDITIONS
    admissible_solution_family: str = ADMISSIBLE_SOLUTION_FAMILY

    def basis_functions(
        self,
        max_longitudinal_index: int,
        max_transverse_index: int,
    ) -> tuple[MobiusBandBasisFunction, ...]:
        longitudinal_cutoff = _positive_int(
            max_longitudinal_index,
            "max_longitudinal_index",
            allow_zero=True,
        )
        transverse_cutoff = _positive_int(
            max_transverse_index,
            "max_transverse_index",
            allow_zero=True,
        )
        basis: list[MobiusBandBasisFunction] = []
        for longitudinal_index in range(longitudinal_cutoff + 1):
            longitudinal_kinds: tuple[LongitudinalKind, ...]
            if longitudinal_index == 0:
                longitudinal_kinds = ("constant",)
            else:
                longitudinal_kinds = ("cos", "sin")
            transverse_kind: TransverseKind = (
                "even_neumann" if longitudinal_index % 2 == 0 else "odd_neumann"
            )
            for longitudinal_kind in longitudinal_kinds:
                for transverse_index in range(transverse_cutoff + 1):
                    basis.append(
                        MobiusBandBasisFunction(
                            longitudinal_index=longitudinal_index,
                            longitudinal_kind=longitudinal_kind,
                            transverse_index=transverse_index,
                            transverse_kind=transverse_kind,
                            half_width=self.domain.half_width,
                        )
                    )
        return tuple(basis)

    def interior_basis_dimension(
        self,
        max_longitudinal_index: int,
        max_transverse_index: int,
    ) -> int:
        return len(self.basis_functions(max_longitudinal_index, max_transverse_index))

    def boundary_traces(
        self,
        sample_count: int,
        max_longitudinal_index: int,
        max_transverse_index: int,
        *,
        include_normal_derivative: bool = False,
    ) -> tuple[BandBoundaryTraceSamples, ...]:
        return tuple(
            mode.boundary_trace(
                sample_count,
                include_normal_derivative=include_normal_derivative,
            )
            for mode in self.basis_functions(max_longitudinal_index, max_transverse_index)
        )

    def boundary_trace_rank(
        self,
        sample_count: int,
        max_longitudinal_index: int,
        max_transverse_index: int,
        *,
        include_normal_derivative: bool = False,
        tolerance: float = 1e-10,
    ) -> int:
        traces = self.boundary_traces(
            sample_count,
            max_longitudinal_index,
            max_transverse_index,
            include_normal_derivative=include_normal_derivative,
        )
        return _matrix_rank((trace.vector for trace in traces), tolerance=tolerance)

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "domain": self.domain.as_dict(),
            "wave_equation": self.wave_equation,
            "spatial_operator": self.spatial_operator,
            "boundary_conditions": self.boundary_conditions,
            "admissible_solution_family": self.admissible_solution_family,
            "nonclaims": (
                "not an embedded Laplace-Beltrami construction",
                "not a spectral or zeta-function theorem",
                "not a PCEA boundary-capacity promotion",
            ),
        }


@dataclass(frozen=True, slots=True)
class BandCapacityInduction:
    """Verdict for whether the band boundary trace supplies requested channels."""

    required_capacity_channels: int
    boundary_sample_count: int
    max_longitudinal_index: int
    max_transverse_index: int
    interior_basis_dimension: int
    boundary_trace_rank: int
    bulk_only_accepts: bool
    boundary_accepts: bool
    status: str
    pcea_generalization_status: str
    reason: str

    @property
    def induces_required_channels(self) -> bool:
        return self.status == STATUS_SURVIVED

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def build_mobius_band_standing_wave(
    half_width: Fraction = DEFAULT_HALF_WIDTH,
) -> MobiusBandStandingWaveModel:
    """Return the coordinate-domain continuum model for one Mobius band."""

    return MobiusBandStandingWaveModel(domain=MobiusBandDomain(half_width=half_width))


def evaluate_band_capacity_channel_induction(
    required_capacity_channels: int,
    *,
    boundary_sample_count: int = 16,
    max_longitudinal_index: int = 7,
    max_transverse_index: int = 3,
) -> BandCapacityInduction:
    """Test whether the finite boundary trace supplies requested channels."""

    required = _positive_int(required_capacity_channels, "required_capacity_channels")
    samples = _positive_int(boundary_sample_count, "boundary_sample_count")
    model = build_mobius_band_standing_wave()
    trace_rank = model.boundary_trace_rank(
        samples,
        max_longitudinal_index,
        max_transverse_index,
    )
    interior_dimension = model.interior_basis_dimension(
        max_longitudinal_index,
        max_transverse_index,
    )
    bulk_only_accepts = required <= interior_dimension
    boundary_accepts = required <= trace_rank
    if boundary_accepts:
        status = STATUS_SURVIVED
        reason = (
            "the requested finite channel count fits the derived sampled "
            "Mobius boundary trace rank"
        )
    else:
        status = STATUS_FALSIFIED
        reason = (
            "the requested channel count exceeds the derived sampled Mobius "
            "boundary trace rank; interior bulk modes are not promoted to "
            "boundary channels"
        )
    return BandCapacityInduction(
        required_capacity_channels=required,
        boundary_sample_count=samples,
        max_longitudinal_index=max_longitudinal_index,
        max_transverse_index=max_transverse_index,
        interior_basis_dimension=interior_dimension,
        boundary_trace_rank=trace_rank,
        bulk_only_accepts=bulk_only_accepts,
        boundary_accepts=boundary_accepts,
        status=status,
        pcea_generalization_status=STATUS_UNRESOLVED,
        reason=reason,
    )


def run_all_mobius_band() -> dict[str, object]:
    """Return a compact construction, survival, and falsification report."""

    model = build_mobius_band_standing_wave()
    finite_induction = evaluate_band_capacity_channel_induction(
        8,
        boundary_sample_count=16,
        max_longitudinal_index=7,
        max_transverse_index=3,
    )
    bulk_overadmission = evaluate_band_capacity_channel_induction(
        16,
        boundary_sample_count=16,
        max_longitudinal_index=7,
        max_transverse_index=3,
    )
    return {
        "schema": MOBIUS_BAND_STANDING_WAVE_SCHEMA_ID,
        "schema_version": MOBIUS_BAND_STANDING_WAVE_SCHEMA_VERSION,
        "construction_status": STATUS_SURVIVED,
        "model": model.as_dict(),
        "interior_dimension_n7_k3": model.interior_basis_dimension(7, 3),
        "boundary_trace_rank_n7_k3_samples16": model.boundary_trace_rank(16, 7, 3),
        "finite_capacity_induction": finite_induction.as_dict(),
        "bulk_overadmission_falsifier": bulk_overadmission.as_dict(),
        "overall_status_for_pcea_promotion": STATUS_UNRESOLVED,
        "hmmm": (
            "embedded Laplace-Beltrami operator on the realized ribbon",
            "exact continuum boundary-measure capacity theorem",
            "derived encoding from continuum trace functions into PCEA runtime channels",
        ),
    }


def _as_positive_fraction(value: int | Fraction, name: str) -> Fraction:
    if isinstance(value, bool):
        raise MobiusBandStandingWaveError(f"{name} cannot be boolean")
    if isinstance(value, int):
        result = Fraction(value)
    elif isinstance(value, Fraction):
        result = value
    else:
        raise MobiusBandStandingWaveError(f"{name} must be an int or exact Fraction")
    if result <= 0:
        raise MobiusBandStandingWaveError(f"{name} must be positive")
    return result


def _finite_coordinate(value: float | Fraction | int, name: str) -> float:
    if isinstance(value, bool):
        raise MobiusBandStandingWaveError(f"{name} cannot be boolean")
    result = float(value)
    if not isfinite(result):
        raise MobiusBandStandingWaveError(f"{name} must be finite")
    return result


def _positive_int(value: int, name: str, *, allow_zero: bool = False) -> int:
    if type(value) is not int:
        raise MobiusBandStandingWaveError(f"{name} must be an integer")
    minimum = 0 if allow_zero else 1
    if value < minimum:
        raise MobiusBandStandingWaveError(f"{name} must be at least {minimum}")
    return value


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


__all__ = [
    "ADMISSIBLE_SOLUTION_FAMILY",
    "BOUNDARY_CONDITIONS",
    "DEFAULT_HALF_WIDTH",
    "MOBIUS_BAND_STANDING_WAVE_SCHEMA_ID",
    "MOBIUS_BAND_STANDING_WAVE_SCHEMA_VERSION",
    "MOBIUS_QUOTIENT",
    "PHYSICAL_BOUNDARY",
    "SPATIAL_OPERATOR",
    "STATUS_BLOCKED",
    "STATUS_FALSIFIED",
    "STATUS_SURVIVED",
    "STATUS_UNRESOLVED",
    "TURN_DOMAIN",
    "WAVE_EQUATION",
    "BandBoundaryTraceSamples",
    "BandCapacityInduction",
    "MobiusBandBasisFunction",
    "MobiusBandDomain",
    "MobiusBandStandingWaveError",
    "MobiusBandStandingWaveModel",
    "build_mobius_band_standing_wave",
    "evaluate_band_capacity_channel_induction",
    "run_all_mobius_band",
]
