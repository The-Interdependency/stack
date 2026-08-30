# === MODULE_BUILD ===
# id: directed_carrier_floor
#   module_name: carrier
#   module_kind: schema
#   summary: represents the directed twofold branched angular carrier without defining full UCNS object semantics
#   owner: Erin Spencer
#   public_surface: STRUCTURAL_NULL, LiftedCarrierPoint, VisibleCarrierPoint, radius_from_breadth, carrier_from_breadth, project, deck_translate, lifted_preimages, same_lifted_position, same_visible_position
#   internal_surface: _StructuralNull, _normalize_angle
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_carrier.py
#   rollout: importable prototype only; no arithmetic or theorem promotion
#   rollback: remove public exports and this module
#   requires: canonical_chapter_one
#   since: 2026-07-21
#   unresolved: canonical evaluators for mu, W, M, and B; complete UCNS object schema
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: structural_null_is_unique_and_coordinate_free
#   given: the carrier is constructed with zero faithful breadth
#   then: the result is the unique Structural Null and exposes no angular coordinate
#   class: doctrine
#   since: 2026-07-21
#
# id: non_null_carrier_has_positive_breadth
#   given: a non-null lifted carrier point is constructed
#   then: breadth is finite and strictly positive and radius lies strictly between zero and one
#   class: correctness
#   since: 2026-07-21
#
# id: lifted_period_is_720_degrees
#   given: any finite angular coordinate on a non-null carrier
#   then: the coordinate is normalized modulo four pi and returns only after two visible laps
#   class: doctrine
#   since: 2026-07-21
#
# id: visible_projection_is_360_degrees
#   given: a non-null lifted carrier point
#   then: projection is normalized modulo two pi and has exactly two lifted representatives
#   class: doctrine
#   since: 2026-07-21
#
# id: one_visible_lap_is_deck_translation_only
#   given: a non-null lifted carrier point translated by two pi
#   then: its visible projection is unchanged while its lifted representative is distinct
#   class: doctrine
#   since: 2026-07-21
#
# id: two_visible_laps_complete_return
#   given: a non-null lifted carrier point translated twice by two pi
#   then: the original lifted representative is restored
#   class: doctrine
#   since: 2026-07-21
#
# id: topology_does_not_invent_orientation_algebra
#   given: a 360-degree deck translation
#   then: no negation, reflection, parity, chirality, frame inversion, or payload operation is inferred by the carrier API
#   class: safety
#   since: 2026-07-21
#
# id: algebraic_zero_is_not_structural_null
#   given: a non-null carrier retains structure while an external payload value is numerically zero
#   then: carrier identity remains non-null because payload algebra is outside the carrier floor
#   class: doctrine
#   since: 2026-07-21
# === END CONTRACTS ===

"""The definition-first UCNS carrier floor.

This module implements only the topology fixed by Chapter 1:

* one unique coordinate-free Structural Null;
* non-null points on a directed angular period of ``4*pi``;
* visible projection modulo ``2*pi``;
* a half-period deck translation that changes the lifted representative without
  inventing negation, parity, chirality, or frame inversion.

It deliberately does not define ``UCNSObject``, payload algebra, carrier pairing,
faithful-breadth evaluation, support weights, product character, factorization,
encoding, or theorem status.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import expm1, isclose, isfinite, nextafter, pi
from typing import Tuple, Union

VISIBLE_PERIOD = 2.0 * pi
LIFTED_PERIOD = 4.0 * pi


class _StructuralNull:
    """Unique complete absence of structural distinction.

    Structural Null has no coordinate. The singleton is intentionally not a
    numeric zero and must not be used as an algebraic additive identity.
    """

    __slots__ = ()

    def __repr__(self) -> str:
        return "STRUCTURAL_NULL"

    def __reduce__(self):
        return (_structural_null, ())


def _structural_null() -> "_StructuralNull":
    return STRUCTURAL_NULL


STRUCTURAL_NULL = _StructuralNull()


def _normalize_angle(angle: float, period: float) -> float:
    angle = float(angle)
    if not isfinite(angle):
        raise ValueError("angle must be finite")
    normalized = angle % period
    return 0.0 if normalized == 0.0 else normalized


def radius_from_breadth(breadth: float) -> float:
    """Return ``a = 1 - exp(-B)`` for an already-supplied breadth value.

    This is the canonical radial map, not an evaluator for faithful breadth.
    """

    breadth = float(breadth)
    if not isfinite(breadth) or breadth < 0.0:
        raise ValueError("breadth must be finite and nonnegative")
    radius = -expm1(-breadth)
    # Binary float rounds the mathematical value to 1.0 for large but
    # finite breadth. Preserve the canonical open rim in the finite
    # representation rather than making valid points unprojectable.
    return nextafter(1.0, 0.0) if radius >= 1.0 else radius


@dataclass(frozen=True, eq=False)
class VisibleCarrierPoint:
    """A non-null point in the visible 360-degree projection.

    Breadth is retained directly so finite values beyond binary-float radial
    resolution do not collapse into one another at the visible boundary.
    """

    breadth: float
    angle: float

    def __post_init__(self) -> None:
        breadth = float(self.breadth)
        if not isfinite(breadth) or breadth <= 0.0:
            raise ValueError("a non-null visible point requires finite positive breadth")
        object.__setattr__(self, "breadth", breadth)
        object.__setattr__(self, "angle", _normalize_angle(self.angle, VISIBLE_PERIOD))

    @property
    def radius(self) -> float:
        return radius_from_breadth(self.breadth)


@dataclass(frozen=True, eq=False)
class LiftedCarrierPoint:
    """A non-null point on the directed 720-degree lifted carrier."""

    breadth: float
    angle: float = 0.0

    def __post_init__(self) -> None:
        breadth = float(self.breadth)
        if not isfinite(breadth) or breadth <= 0.0:
            raise ValueError("a non-null carrier point requires finite positive breadth")
        object.__setattr__(self, "breadth", breadth)
        object.__setattr__(self, "angle", _normalize_angle(self.angle, LIFTED_PERIOD))

    @property
    def radius(self) -> float:
        return radius_from_breadth(self.breadth)

    def rotate(self, displacement: float) -> "LiftedCarrierPoint":
        displacement = float(displacement)
        if not isfinite(displacement):
            raise ValueError("displacement must be finite")
        return LiftedCarrierPoint(self.breadth, self.angle + displacement)

    def deck_translate(self) -> "LiftedCarrierPoint":
        """Advance one visible lap without inventing an orientation operation."""

        return self.rotate(VISIBLE_PERIOD)

    def project(self) -> VisibleCarrierPoint:
        return VisibleCarrierPoint(self.breadth, self.angle)


CarrierPoint = Union[_StructuralNull, LiftedCarrierPoint]
VisiblePoint = Union[_StructuralNull, VisibleCarrierPoint]


def carrier_from_breadth(breadth: float, angle: float = 0.0) -> CarrierPoint:
    """Construct Structural Null at ``B=0`` or a non-null lifted point at ``B>0``."""

    breadth = float(breadth)
    if not isfinite(breadth) or breadth < 0.0:
        raise ValueError("breadth must be finite and nonnegative")
    if breadth == 0.0:
        return STRUCTURAL_NULL
    return LiftedCarrierPoint(breadth, angle)


def project(point: CarrierPoint) -> VisiblePoint:
    if point is STRUCTURAL_NULL:
        return STRUCTURAL_NULL
    if not isinstance(point, LiftedCarrierPoint):
        raise TypeError("point must be STRUCTURAL_NULL or LiftedCarrierPoint")
    return point.project()


def deck_translate(point: CarrierPoint) -> CarrierPoint:
    if point is STRUCTURAL_NULL:
        return STRUCTURAL_NULL
    if not isinstance(point, LiftedCarrierPoint):
        raise TypeError("point must be STRUCTURAL_NULL or LiftedCarrierPoint")
    return point.deck_translate()


def lifted_preimages(point: VisiblePoint) -> Tuple[CarrierPoint, ...]:
    """Return the branch-law preimages: one at null, two everywhere else."""

    if point is STRUCTURAL_NULL:
        return (STRUCTURAL_NULL,)
    if not isinstance(point, VisibleCarrierPoint):
        raise TypeError("point must be STRUCTURAL_NULL or VisibleCarrierPoint")
    first = LiftedCarrierPoint(point.breadth, point.angle)
    return (first, first.deck_translate())


def _angles_match(first: float, second: float, period: float, tolerance: float) -> bool:
    delta = abs((first - second) % period)
    circular_distance = min(delta, period - delta)
    return circular_distance <= tolerance


def same_lifted_position(
    first: CarrierPoint, second: CarrierPoint, *, tolerance: float = 1e-12
) -> bool:
    """Compare carrier coordinates without claiming full structural equivalence."""

    if first is STRUCTURAL_NULL or second is STRUCTURAL_NULL:
        return first is STRUCTURAL_NULL and second is STRUCTURAL_NULL
    if not isinstance(first, LiftedCarrierPoint) or not isinstance(second, LiftedCarrierPoint):
        raise TypeError("points must be carrier points")
    return isclose(first.breadth, second.breadth, rel_tol=tolerance, abs_tol=tolerance) and _angles_match(
        first.angle, second.angle, LIFTED_PERIOD, tolerance
    )


def same_visible_position(
    first: VisiblePoint, second: VisiblePoint, *, tolerance: float = 1e-12
) -> bool:
    """Compare visible coordinates without claiming full structural equivalence."""

    if first is STRUCTURAL_NULL or second is STRUCTURAL_NULL:
        return first is STRUCTURAL_NULL and second is STRUCTURAL_NULL
    if not isinstance(first, VisibleCarrierPoint) or not isinstance(second, VisibleCarrierPoint):
        raise TypeError("points must be visible carrier points")
    return isclose(first.breadth, second.breadth, rel_tol=tolerance, abs_tol=tolerance) and _angles_match(
        first.angle, second.angle, VISIBLE_PERIOD, tolerance
    )
