# === MODULE_BUILD ===
# id: ucns_mobius_vesica_exact_embedding
#   module_name: mobius_vesica
#   module_kind: experiment
#   summary: defines the canonical two-band Mobius Vesica Piscis embedding whose centerlines meet twice and whose single continuous boundaries admit an exact four-contact certificate
#   owner: Erin Spencer
#   public_surface: VesicaBand, TwistChirality, Point3, CenterlineContact, MobiusBandEmbedding, MobiusVesicaParameters, MobiusVesica, build_mobius_vesica
#   internal_surface: exact vesica parameters, circular ribbon frame, quotient validation, boundary-contact polynomial
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_mobius_vesica_exact.py
#   rollout: UCNS-only exact candidate; selection effect none; does not alter the seven-band candidate or select a canonical zeta operator
#   rollback: remove this module, mobius_certificates, mobius_continuation, their tests, documentation, and generated receipt
#   requires: ucns_mobius_seed_of_life_candidate
#   since: 2026-08-10
#   unresolved: full pair-surface intersection set, arbitrary-perturbation stability, linking data, ambient-isotopy class, seven-band phase reconciliation, spectral operator, zeta correspondence
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: mobius_vesica_has_exact_two_centerline_contacts
#   given: the canonical equal-radius vesica embedding is constructed
#   then: the two circular centerlines meet at exactly two exact points, zero plus or minus sqrt(3)/2 in the projection plane
#   class: correctness
#   since: 2026-08-10
#
# id: mobius_vesica_obeys_one_turn_seam_and_two_turn_return
#   given: either band is evaluated at any admissible breadth
#   then: one carrier turn reverses breadth under the quotient and two turns restore the full point
#   class: correctness
#   since: 2026-08-10
#
# id: mobius_vesica_preserves_source_claims_as_testable_geometry
#   given: the source note is used to define the dyad research target
#   then: two centerline contacts and four physical continuous-boundary contacts remain explicit hypotheses to prove or falsify without being replaced by projected or abstract events
#   class: doctrine
#   since: 2026-08-10
#
# id: mobius_vesica_null_origin_has_positive_clearance
#   given: radius one, center separation one, and half width one hundredth
#   then: the origin is excluded from both individual bands by an exact lower clearance bound of forty-nine hundredths
#   class: safety
#   since: 2026-08-10
# === END CONTRACTS ===

"""Canonical two-band Möbius Vesica Piscis geometry.

The source note states that the two Möbius centerlines meet twice and that their
single continuous boundary curves meet four times.  This module defines one
explicit standard-circular ribbon family in which those statements can be
asked exactly.  The companion :mod:`ucns.mobius_certificates` module proves the
counts for the default parameters.

The construction is geometric research infrastructure.  It does not identify
an electron with a Möbius strip, derive the Pauli exclusion principle, prove a
link type, or establish any zeta-function theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
import math
from typing import Iterable

MOBIUS_VESICA_SCHEMA_ID = "ucns.mobius-vesica"
MOBIUS_VESICA_SCHEMA_VERSION = "0.1.0"
MOBIUS_VESICA_SELECTION_EFFECT = "none"
SOURCE_DOCUMENT_NAME = "Möbius Strips and Quantum Geometry.txt"
SOURCE_DOCUMENT_SHA256 = "dc3a94ca5070ffff8f2a246f48db77192b08f521e721bc7c2a011aa05ddeb9a1"
SOURCE_CENTERLINE_CLAIM_LINE = 9
SOURCE_BOUNDARY_CLAIM_LINE = 10


class MobiusVesicaError(ValueError):
    """Raised when a requested construction leaves the declared family."""


def fraction_text(value: Fraction) -> str:
    """Return a stable exact text representation for a fraction."""

    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _as_fraction(value: int | Fraction, field: str) -> Fraction:
    if isinstance(value, bool):
        raise MobiusVesicaError(f"{field} cannot be boolean")
    if isinstance(value, int):
        return Fraction(value)
    if not isinstance(value, Fraction):
        raise MobiusVesicaError(f"{field} must be an int or exact Fraction")
    return value


def _canonical_turn(value: Fraction) -> Fraction:
    return value - value.numerator // value.denominator


def _numeric(value: int | float | Fraction, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float, Fraction)):
        raise MobiusVesicaError(f"{field} must be numeric and nonboolean")
    result = float(value)
    if not math.isfinite(result):
        raise MobiusVesicaError(f"{field} must be finite")
    return result


@dataclass(frozen=True, slots=True)
class Point3:
    """A binary64 point used only for realization and residual checks."""

    x: float
    y: float
    z: float

    def distance_to(self, other: "Point3") -> float:
        return math.sqrt(
            (self.x - other.x) ** 2
            + (self.y - other.y) ** 2
            + (self.z - other.z) ** 2
        )

    def as_dict(self) -> dict[str, float]:
        return {"x": self.x, "y": self.y, "z": self.z}


class VesicaBand(str, Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class TwistChirality(int, Enum):
    POSITIVE = 1
    NEGATIVE = -1


@dataclass(frozen=True, slots=True)
class CenterlineContact:
    """An exact centerline contact in ``Q(sqrt(3))`` coordinates."""

    contact_id: str
    left_turn: Fraction
    right_turn: Fraction
    y_sqrt3_coefficient: Fraction

    @property
    def point(self) -> Point3:
        return Point3(0.0, float(self.y_sqrt3_coefficient) * math.sqrt(3.0), 0.0)

    def as_dict(self) -> dict[str, object]:
        coefficient = fraction_text(self.y_sqrt3_coefficient)
        return {
            "contact_id": self.contact_id,
            "left_turn": fraction_text(self.left_turn),
            "right_turn": fraction_text(self.right_turn),
            "point_exact": {
                "x": "0",
                "y": f"({coefficient})*sqrt(3)",
                "z": "0",
            },
            "point_binary64": self.point.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class MobiusVesicaParameters:
    """Exact parameters for the certified standard-circular family.

    The equal circles have radius ``radius`` and center separation
    ``center_distance``.  The default separation equals the radius, which is
    the classical vesica-piscis relation.
    """

    radius: Fraction = Fraction(1)
    center_distance: Fraction = Fraction(1)
    half_width: Fraction = Fraction(1, 100)
    left_phase_turns: Fraction = Fraction(0)
    right_phase_turns: Fraction = Fraction(1, 4)
    left_chirality: TwistChirality = TwistChirality.POSITIVE
    right_chirality: TwistChirality = TwistChirality.NEGATIVE

    def __post_init__(self) -> None:
        for value, field in (
            (self.radius, "radius"),
            (self.center_distance, "center_distance"),
            (self.half_width, "half_width"),
            (self.left_phase_turns, "left_phase_turns"),
            (self.right_phase_turns, "right_phase_turns"),
        ):
            if not isinstance(value, Fraction):
                raise MobiusVesicaError(f"{field} must be an exact Fraction")
        if self.radius <= 0 or self.center_distance <= 0 or self.half_width <= 0:
            raise MobiusVesicaError("radius, center distance, and half width must be positive")
        if self.center_distance >= 2 * self.radius:
            raise MobiusVesicaError("the centerlines must be strict secants, not tangent or disjoint")
        if self.half_width >= self.radius:
            raise MobiusVesicaError("half width must be smaller than the carrier radius")
        if _canonical_turn(self.left_phase_turns) != self.left_phase_turns:
            raise MobiusVesicaError("left phase must be canonical in [0,1)")
        if _canonical_turn(self.right_phase_turns) != self.right_phase_turns:
            raise MobiusVesicaError("right phase must be canonical in [0,1)")
        if self.left_chirality is self.right_chirality:
            raise MobiusVesicaError("the certified dyad requires opposite twist chirality")

    @property
    def is_canonical_vesica(self) -> bool:
        return self.center_distance == self.radius

    @property
    def is_certified_phase_pair(self) -> bool:
        return (
            self.left_phase_turns == Fraction(0)
            and self.right_phase_turns == Fraction(1, 4)
        )

    @property
    def null_clearance_lower_bound(self) -> Fraction:
        """Triangle-inequality lower bound for distance from origin to either band."""

        return self.radius - self.center_distance / 2 - self.half_width

    def as_dict(self) -> dict[str, object]:
        return {
            "radius": fraction_text(self.radius),
            "center_distance": fraction_text(self.center_distance),
            "half_width": fraction_text(self.half_width),
            "left_phase_turns": fraction_text(self.left_phase_turns),
            "right_phase_turns": fraction_text(self.right_phase_turns),
            "left_chirality": self.left_chirality.name.lower(),
            "right_chirality": self.right_chirality.name.lower(),
        }


@dataclass(frozen=True, slots=True)
class MobiusBandEmbedding:
    """One standard circular Möbius ribbon.

    For carrier turn ``t`` and signed breadth ``u`` the surface is

    ``C(t) + u * (cos(alpha(t)) radial(t) + sin(alpha(t)) vertical)``,

    where ``alpha(t) = chirality*pi*t + 2*pi*phase``.  Because chirality is
    odd, the frame reverses after one turn and returns after two.
    """

    slot: VesicaBand
    center_x: Fraction
    radius: Fraction
    half_width: Fraction
    chirality: TwistChirality
    phase_turns: Fraction

    def __post_init__(self) -> None:
        for value, field in (
            (self.center_x, "center_x"),
            (self.radius, "radius"),
            (self.half_width, "half_width"),
            (self.phase_turns, "phase_turns"),
        ):
            if not isinstance(value, Fraction):
                raise MobiusVesicaError(f"{field} must be an exact Fraction")
        if self.radius <= 0 or self.half_width <= 0 or self.half_width >= self.radius:
            raise MobiusVesicaError("band radius and half width are inadmissible")
        if _canonical_turn(self.phase_turns) != self.phase_turns:
            raise MobiusVesicaError("band phase must be canonical in [0,1)")

    def centerline_point(self, turn: int | float | Fraction) -> Point3:
        t = _numeric(turn, "turn")
        theta = math.tau * t
        return Point3(
            float(self.center_x) + float(self.radius) * math.cos(theta),
            float(self.radius) * math.sin(theta),
            0.0,
        )

    def surface_point(
        self,
        turn: int | float | Fraction,
        breadth: int | float | Fraction,
    ) -> Point3:
        t = _numeric(turn, "turn")
        u = _numeric(breadth, "breadth")
        if abs(u) > float(self.half_width) + 1e-15:
            raise MobiusVesicaError("breadth exceeds the declared half width")
        theta = math.tau * t
        twist = self.chirality.value * math.pi * t + math.tau * float(self.phase_turns)
        core = self.centerline_point(t)
        radial_offset = u * math.cos(twist)
        vertical_offset = u * math.sin(twist)
        return Point3(
            core.x + radial_offset * math.cos(theta),
            core.y + radial_offset * math.sin(theta),
            vertical_offset,
        )

    def boundary_point(self, boundary_turn: int | float | Fraction) -> Point3:
        """Evaluate the strip's one continuous boundary over a two-turn domain."""

        return self.surface_point(boundary_turn, self.half_width)

    def boundary_tangent(self, boundary_turn: int | float | Fraction) -> Point3:
        """Analytic derivative of the continuous boundary with respect to turns."""

        t = _numeric(boundary_turn, "boundary_turn")
        theta = math.tau * t
        twist = self.chirality.value * math.pi * t + math.tau * float(self.phase_turns)
        radius = float(self.radius) + float(self.half_width) * math.cos(twist)
        radius_derivative = (
            -float(self.half_width)
            * math.sin(twist)
            * self.chirality.value
            * math.pi
        )
        return Point3(
            radius_derivative * math.cos(theta) - radius * math.tau * math.sin(theta),
            radius_derivative * math.sin(theta) + radius * math.tau * math.cos(theta),
            float(self.half_width)
            * math.cos(twist)
            * self.chirality.value
            * math.pi,
        )

    def seam_residual(
        self,
        turn: int | float | Fraction,
        breadth: int | float | Fraction,
    ) -> float:
        t = _numeric(turn, "turn")
        u = _numeric(breadth, "breadth")
        return self.surface_point(t + 1.0, u).distance_to(self.surface_point(t, -u))

    def return_residual(
        self,
        turn: int | float | Fraction,
        breadth: int | float | Fraction,
    ) -> float:
        t = _numeric(turn, "turn")
        u = _numeric(breadth, "breadth")
        return self.surface_point(t + 2.0, u).distance_to(self.surface_point(t, u))

    def as_dict(self) -> dict[str, object]:
        return {
            "slot": self.slot.value,
            "center_x": fraction_text(self.center_x),
            "radius": fraction_text(self.radius),
            "half_width": fraction_text(self.half_width),
            "chirality": self.chirality.name.lower(),
            "phase_turns": fraction_text(self.phase_turns),
        }


@dataclass(frozen=True, slots=True)
class MobiusVesica:
    parameters: MobiusVesicaParameters
    left: MobiusBandEmbedding
    right: MobiusBandEmbedding
    schema_id: str = MOBIUS_VESICA_SCHEMA_ID
    schema_version: str = MOBIUS_VESICA_SCHEMA_VERSION
    selection_effect: str = MOBIUS_VESICA_SELECTION_EFFECT

    def __post_init__(self) -> None:
        if self.left.slot is not VesicaBand.LEFT or self.right.slot is not VesicaBand.RIGHT:
            raise MobiusVesicaError("band slots are reversed")
        if self.schema_id != MOBIUS_VESICA_SCHEMA_ID or self.schema_version != MOBIUS_VESICA_SCHEMA_VERSION:
            raise MobiusVesicaError("schema identity mismatch")
        if self.selection_effect != "none":
            raise MobiusVesicaError("the research artifact cannot select UCNS canon")
        expected_left = -self.parameters.center_distance / 2
        expected_right = self.parameters.center_distance / 2
        if self.left.center_x != expected_left or self.right.center_x != expected_right:
            raise MobiusVesicaError("band centers do not match the parameter ledger")

    @property
    def bands(self) -> tuple[MobiusBandEmbedding, MobiusBandEmbedding]:
        return self.left, self.right

    @property
    def centerline_contacts(self) -> tuple[CenterlineContact, CenterlineContact]:
        if not self.parameters.is_canonical_vesica:
            raise MobiusVesicaError("exact sqrt(3)/2 contacts are specific to separation equals radius")
        scale = self.parameters.radius
        return (
            CenterlineContact(
                "CENTERLINE_TOP",
                Fraction(1, 6),
                Fraction(1, 3),
                scale / 2,
            ),
            CenterlineContact(
                "CENTERLINE_BOTTOM",
                Fraction(5, 6),
                Fraction(2, 3),
                -scale / 2,
            ),
        )

    def boundary_contact_polynomial(self) -> tuple[Fraction, ...]:
        """Return ``P_w(x)`` in ascending coefficient order.

        For the certified phase/chirality pair, equality of boundary heights
        reduces the viable branch to ``s = 1/2 - t (mod 2)``.  With
        ``x = cos(pi*t)`` the remaining planar equation is

        ``(1 + w*x) * (2*x*x - 1) = 1/2``

        for the canonical unit-radius vesica.  Equivalently,
        ``P_w(x) = 4*w*x^3 + 4*x^2 - 2*w*x - 3``.
        """

        if self.parameters.radius != 1 or self.parameters.center_distance != 1:
            raise MobiusVesicaError("the normalized contact polynomial requires radius and separation one")
        if not self.parameters.is_certified_phase_pair:
            raise MobiusVesicaError("the closed-form contact polynomial requires quarter-turn phase")
        w = self.parameters.half_width
        return (Fraction(-3), -2 * w, Fraction(4), 4 * w)

    def centerline_contact_residuals(self) -> tuple[float, float]:
        residuals: list[float] = []
        for contact in self.centerline_contacts:
            residuals.append(
                self.left.centerline_point(contact.left_turn).distance_to(
                    self.right.centerline_point(contact.right_turn)
                )
            )
        return tuple(residuals)  # type: ignore[return-value]

    def seam_and_return_residuals(
        self,
        turns: Iterable[Fraction] = (Fraction(0), Fraction(1, 7), Fraction(5, 13)),
        breadths: Iterable[Fraction] | None = None,
    ) -> tuple[float, float]:
        if breadths is None:
            breadths = (-self.parameters.half_width, Fraction(0), self.parameters.half_width)
        seam = 0.0
        full_return = 0.0
        for band in self.bands:
            for turn in turns:
                for breadth in breadths:
                    seam = max(seam, band.seam_residual(turn, breadth))
                    full_return = max(full_return, band.return_residual(turn, breadth))
        return seam, full_return

    def boundary_contact_residual(
        self,
        left_turn: float,
        right_turn: float,
    ) -> float:
        return self.left.boundary_point(left_turn).distance_to(
            self.right.boundary_point(right_turn)
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "selection_effect": self.selection_effect,
            "parameters": self.parameters.as_dict(),
            "bands": [band.as_dict() for band in self.bands],
            "centerline_contacts": [contact.as_dict() for contact in self.centerline_contacts],
            "null_clearance_lower_bound": fraction_text(
                self.parameters.null_clearance_lower_bound
            ),
        }


def build_mobius_vesica(
    parameters: MobiusVesicaParameters | None = None,
) -> MobiusVesica:
    """Construct the canonical anti-chiral Möbius Vesica Piscis candidate."""

    params = parameters or MobiusVesicaParameters()
    left = MobiusBandEmbedding(
        slot=VesicaBand.LEFT,
        center_x=-params.center_distance / 2,
        radius=params.radius,
        half_width=params.half_width,
        chirality=params.left_chirality,
        phase_turns=params.left_phase_turns,
    )
    right = MobiusBandEmbedding(
        slot=VesicaBand.RIGHT,
        center_x=params.center_distance / 2,
        radius=params.radius,
        half_width=params.half_width,
        chirality=params.right_chirality,
        phase_turns=params.right_phase_turns,
    )
    return MobiusVesica(parameters=params, left=left, right=right)


__all__ = [
    "VesicaBand",
    "TwistChirality",
    "Point3",
    "CenterlineContact",
    "MobiusBandEmbedding",
    "MobiusVesicaParameters",
    "MobiusVesica",
    "build_mobius_vesica",
]
