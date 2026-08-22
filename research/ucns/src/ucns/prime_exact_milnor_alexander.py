# === MODULE_BUILD ===
# id: ucns_prime_exact_milnor_alexander_p7_p5
#   module_name: prime_exact_milnor_alexander
#   module_kind: experiment
#   summary: generically resolves the P7/P5 centerline diagrams, replaces the five numerical Milnor-zero candidates with exact degree-two Magnus coefficients, freezes and evaluates a prime-character Fox-Alexander phase selector, and issues whole-link rank fingerprints
#   owner: Erin Spencer
#   public_surface: DiagramCrossing, GenericLinkDiagram, MilnorIntegerCertificate, FoxRankFingerprint, PhaseSelectorResult, build_generic_prime_seven_diagram, build_generic_prime_five_diagram, exact_p7_milnor_certificates, fox_rank_fingerprint, common_field_fox_rank_fingerprint, evaluate_preregistered_phase_selector, exact_milnor_alexander_family_certificate, write_exact_milnor_alexander_family_certificate
#   internal_surface: fixed planar translations, high-precision circle intersections, Wirtinger arcs, degree-two Magnus algebra, finite-field Fox derivatives, exact rational phase-lift energy
#   auth_boundary: none
#   storage_boundary: caller-supplied local paths only through writer functions
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_exact_milnor_alexander.py
#   rollout: P7 first, P5 same-protocol comparison second; preregistration SHA-256 frozen before evaluation; selection effect none
#   rollback: remove this module, its tests, documentation, preregistration, and generated certificate
#   requires: ucns_prime_independent_phase_milnor_p7_p5, mpmath>=1.3
#   since: 2026-08-11
#   unresolved: proof-assistant replay of diagram signs, full multivariable Alexander polynomial, ambient-isotopy classification, higher Milnor invariants, spectral operator, prime-power law, zeta correspondence
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: prime_generic_diagram_is_fixed_before_invariants
#   given: the P7 or P5 diagram is constructed
#   then: every component uses the preregistered rational planar translation and the straight-line isotopy remains inside the prior seven-hundredths ribbon clearance
#   class: doctrine
#   since: 2026-08-11
#
# id: prime_generic_diagram_preserves_pairwise_linking
#   given: all generic double crossings are signed
#   then: their half-sums reproduce the previously certified complete P7 and P5 pairwise linking matrices
#   class: correctness
#   since: 2026-08-11
#
# id: prime_magnus_benchmark_recovers_borromean_integer
#   given: the closure of the braid sigma-one sigma-two-inverse cubed is evaluated
#   then: the degree-two preferred-longitude Magnus coefficient has absolute value one
#   class: correctness
#   since: 2026-08-11
#
# id: prime_p7_five_milnor_candidates_are_exact_zero_in_diagram
#   given: the five pairwise-zero P7 triples are evaluated in the fixed generic diagram
#   then: every degree-two Magnus coefficient is exactly the integer zero
#   class: evidence
#   since: 2026-08-11
#
# id: prime_phase_selector_matches_frozen_preregistration
#   given: the phase selector is evaluated
#   then: its document hash equals the preregistered hash and no post-evaluation criterion is added
#   class: doctrine
#   since: 2026-08-11
#
# id: prime_phase_selector_uses_whole_link_character
#   given: an admissible phase law is scored
#   then: the score uses maximum phase gap, finite-field Fox-Alexander excess nullity, and exact phase-lift alignment energy before neutral tie breakers
#   class: correctness
#   since: 2026-08-11
#
# id: prime_fox_fingerprint_covers_all_prime_characters
#   given: a P7 or P5 whole-link fingerprint is issued
#   then: every distinct phase-induced prime character has a rank and excess-nullity value committed by SHA-256
#   class: evidence
#   since: 2026-08-11
#
# id: prime_exact_milnor_alexander_receipt_is_nonselecting
#   given: the family certificate is serialized
#   then: it claims no arithmetic redefinition, electron ontology, zeta theorem, or Riemann-hypothesis proof
#   class: doctrine
#   since: 2026-08-11
# === END CONTRACTS ===

"""Exact diagram-level Milnor and finite-character Fox-Alexander experiment.

The P7 and P5 lifted centerlines are first moved by fixed, preregistered small
translations in the projection plane.  The earlier finite-width certificate
leaves enough clearance for the simultaneous straight-line translation, so the
new generic diagrams represent the same centerline links.  Circle intersections
are evaluated at 100 decimal digits; all accepted crossing signs have explicit
nonzero height and transversality margins.

For pairwise-zero triples, preferred longitudes are constructed from Wirtinger
arcs.  Their noncommutative Magnus expansions are evaluated exactly through
degree two with :class:`fractions.Fraction`.  The implementation is blocked
unless it recovers ``|mu|=1`` for the closure of ``(sigma_1 sigma_2^-1)^3``.

The phase selector was frozen in ``docs/PREREGISTRATION_P7_PHASE_ALEXANDER.md``
before evaluation.  Its whole-link term is the excess nullity of a Fox matrix
specialized at a prime-order character over F_29 for P7 and F_11 for P5.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
from functools import lru_cache
from fractions import Fraction
import bisect
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Iterable, Mapping, Sequence

import mpmath as mp

from .prime_independent_phase_milnor import P7_SPLIT_TRIPLES
from .prime_phase_lift import _dataset, build_prime_five_phase_lift, build_prime_seven_phase_lift
from .prime_phase_lift_model import PhaseLaw, _min_gap, _mod1, _outer
from .prime_smooth_ribbons import (
    SmoothPrimeRibbon,
    build_smooth_prime_five,
    build_smooth_prime_seven,
    certify_smooth_prime_five,
    certify_smooth_prime_seven,
)

SCHEMA_ID = "ucns.prime-exact-milnor-alexander"
SCHEMA_VERSION = "0.1.0"
SOURCE_NAME = "Möbius Strips and Quantum Geometry.txt"
SOURCE_SHA256 = "dc3a94ca5070ffff8f2a246f48db77192b08f521e721bc7c2a011aa05ddeb9a1"
SOURCE_LINES = (5, 6, 13, 14, 15, 16, 17)
PREREGISTRATION_DOCUMENT = "docs/PREREGISTRATION_P7_PHASE_ALEXANDER.md"
PREREGISTRATION_SHA256 = "f8f1a6eae5de2c8235a576266a140c93492554248c2756d838845a19240b23cc"
PROJECTION_EPSILON = Fraction(1, 1000)
PRIOR_RIBBON_CLEARANCE = Fraction(7, 100)
MP_DECIMAL_DIGITS = 100
MINIMUM_ACCEPTED_HEIGHT_GAP = mp.mpf("0.09")
MINIMUM_ACCEPTED_TRANSVERSALITY = mp.mpf("0.05")
MINIMUM_ACCEPTED_CROSSING_POINT_GAP = mp.mpf("0.0001")
FIELD_MODULUS = {7: 29, 5: 11}
FIELD_PRIMITIVE_ROOT = {7: 2, 5: 2}
COMMON_FIELD_MODULUS = 71
COMMON_FIELD_PRIMITIVE_ROOT = 7

SHIFT_VECTORS: Mapping[str, tuple[int, int]] = {
    "C": (0, 0),
    "R0": (1, 2),
    "R1": (-2, 1),
    "R2": (3, -1),
    "R3": (-1, -3),
    "R4": (2, -2),
    "R5": (-3, 3),
}


class ExactMilnorAlexanderError(ValueError):
    """Raised when a frozen experiment boundary is violated."""


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _mp_fraction(value: Fraction) -> mp.mpf:
    return mp.mpf(value.numerator) / value.denominator


def _sign(value: mp.mpf) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def _canonical_json_sha256(payload: object) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _center_coordinates(prime: int) -> dict[str, tuple[mp.mpf, mp.mpf]]:
    zero = mp.mpf("0")
    one = mp.mpf("1")
    if prime == 5:
        base = {
            "C": (zero, zero),
            "R0": (one, zero),
            "R1": (zero, one),
            "R2": (-one, zero),
            "R3": (zero, -one),
        }
    elif prime == 7:
        half = mp.mpf("0.5")
        root_three_half = mp.sqrt(3) / 2
        base = {
            "C": (zero, zero),
            "R0": (one, zero),
            "R1": (half, root_three_half),
            "R2": (-half, root_three_half),
            "R3": (-one, zero),
            "R4": (-half, -root_three_half),
            "R5": (half, -root_three_half),
        }
    else:
        raise ExactMilnorAlexanderError("only P7 and P5 are supported")
    epsilon = _mp_fraction(PROJECTION_EPSILON)
    return {
        carrier: (
            point[0] + epsilon * SHIFT_VECTORS[carrier][0],
            point[1] + epsilon * SHIFT_VECTORS[carrier][1],
        )
        for carrier, point in base.items()
    }


def _smooth_lift_mp(ribbon: SmoothPrimeRibbon, carrier: str, turn: mp.mpf) -> mp.mpf:
    target = mp.fmod(turn, 1)
    if target < 0:
        target += 1
    field = ribbon.field(carrier)
    for index, segment in enumerate(field.segments):
        left_turn = _mp_fraction(segment.left_turn)
        right_turn = _mp_fraction(segment.right_turn)
        adjusted = target
        if index == len(field.segments) - 1 and adjusted < left_turn:
            adjusted += 1
        if left_turn <= adjusted <= right_turn:
            left_value = _mp_fraction(segment.left_value)
            right_value = _mp_fraction(segment.right_value)
            if adjusted == left_turn:
                return left_value
            if adjusted == right_turn:
                return right_value
            local = (adjusted - left_turn) / (right_turn - left_turn)
            a = mp.e ** (-1 / local)
            b = mp.e ** (-1 / (1 - local))
            step = a / (a + b)
            return left_value + (right_value - left_value) * step
    raise AssertionError("high-precision smooth-field interval search failed")


def _circle_intersections(
    left_center: tuple[mp.mpf, mp.mpf],
    right_center: tuple[mp.mpf, mp.mpf],
) -> tuple[tuple[mp.mpf, mp.mpf], ...]:
    dx = right_center[0] - left_center[0]
    dy = right_center[1] - left_center[1]
    distance = mp.sqrt(dx * dx + dy * dy)
    if distance >= 2:
        return ()
    if distance <= 0:
        raise ExactMilnorAlexanderError("coincident projected carrier centers")
    height_squared = 1 - distance * distance / 4
    if height_squared <= 0:
        raise ExactMilnorAlexanderError("generic projection retained a tangency")
    height = mp.sqrt(height_squared)
    midpoint = (
        (left_center[0] + right_center[0]) / 2,
        (left_center[1] + right_center[1]) / 2,
    )
    perpendicular = (-dy / distance, dx / distance)
    return (
        (
            midpoint[0] + height * perpendicular[0],
            midpoint[1] + height * perpendicular[1],
        ),
        (
            midpoint[0] - height * perpendicular[0],
            midpoint[1] - height * perpendicular[1],
        ),
    )


def _turn_at(
    point: tuple[mp.mpf, mp.mpf],
    center: tuple[mp.mpf, mp.mpf],
) -> mp.mpf:
    angle = mp.atan2(point[1] - center[1], point[0] - center[0])
    turn = angle / (2 * mp.pi)
    return turn if turn >= 0 else turn + 1


@dataclass(frozen=True, slots=True)
class DiagramCrossing:
    crossing_id: str
    left: str
    right: str
    left_turn: str
    right_turn: str
    point_x: str
    point_y: str
    left_height: str
    right_height: str
    over: str
    under: str
    over_turn: str
    under_turn: str
    sign: int
    absolute_height_gap: str
    absolute_transversality: str

    @property
    def left_turn_mpf(self) -> mp.mpf:
        return mp.mpf(self.left_turn)

    @property
    def right_turn_mpf(self) -> mp.mpf:
        return mp.mpf(self.right_turn)

    @property
    def over_turn_mpf(self) -> mp.mpf:
        return mp.mpf(self.over_turn)

    @property
    def under_turn_mpf(self) -> mp.mpf:
        return mp.mpf(self.under_turn)

    @property
    def point(self) -> tuple[mp.mpf, mp.mpf]:
        return mp.mpf(self.point_x), mp.mpf(self.point_y)

    def turn_for(self, carrier: str) -> mp.mpf:
        if carrier == self.left:
            return self.left_turn_mpf
        if carrier == self.right:
            return self.right_turn_mpf
        raise ExactMilnorAlexanderError(f"{carrier} is not incident to {self.crossing_id}")

    def as_dict(self) -> dict[str, object]:
        return {
            "crossing_id": self.crossing_id,
            "components": [self.left, self.right],
            "turns": {self.left: self.left_turn, self.right: self.right_turn},
            "projected_point": [self.point_x, self.point_y],
            "heights": {self.left: self.left_height, self.right: self.right_height},
            "over": self.over,
            "under": self.under,
            "sign": self.sign,
            "absolute_height_gap": self.absolute_height_gap,
            "absolute_transversality": self.absolute_transversality,
        }


@dataclass(frozen=True, slots=True)
class ArcGenerator:
    index: int
    component: str
    local_index: int

    @property
    def label(self) -> str:
        return f"{self.component}:a{self.local_index}"


@dataclass(frozen=True, slots=True)
class WirtingerRelation:
    crossing_id: str
    sign: int
    over_arc: int
    incoming_under_arc: int
    outgoing_under_arc: int

    @property
    def word(self) -> tuple[tuple[int, int], ...]:
        return (
            (self.over_arc, self.sign),
            (self.incoming_under_arc, 1),
            (self.over_arc, -self.sign),
            (self.outgoing_under_arc, -1),
        )


@dataclass(frozen=True, slots=True)
class GenericLinkDiagram:
    prime: int
    carriers: tuple[str, ...]
    crossings: tuple[DiagramCrossing, ...]
    arcs: tuple[ArcGenerator, ...]
    relations: tuple[WirtingerRelation, ...]
    maximum_component_displacement: str
    maximum_relative_displacement: str
    isotopy_ribbon_clearance_lower_bound: str
    minimum_height_gap: str
    minimum_transversality: str
    minimum_distinct_crossing_point_gap: str
    pairwise_linking_matrix: tuple[tuple[int, ...], ...]

    @property
    def crossing_count(self) -> int:
        return len(self.crossings)

    @property
    def generator_count(self) -> int:
        return len(self.arcs)

    @property
    def relation_count(self) -> int:
        return len(self.relations)

    def component_index(self) -> dict[str, int]:
        return {carrier: index for index, carrier in enumerate(self.carriers)}

    def subdiagram_crossings(self, components: Sequence[str]) -> tuple[DiagramCrossing, ...]:
        selected = set(components)
        return tuple(
            crossing
            for crossing in self.crossings
            if crossing.left in selected and crossing.right in selected
        )

    def as_dict(self, *, include_crossings: bool = False) -> dict[str, object]:
        payload: dict[str, object] = {
            "prime": self.prime,
            "carriers": list(self.carriers),
            "fixed_translation_epsilon": fraction_text(PROJECTION_EPSILON),
            "shift_vectors": {
                carrier: list(SHIFT_VECTORS[carrier]) for carrier in self.carriers
            },
            "crossing_count": self.crossing_count,
            "generator_count": self.generator_count,
            "relation_count": self.relation_count,
            "maximum_component_displacement": self.maximum_component_displacement,
            "maximum_relative_displacement": self.maximum_relative_displacement,
            "prior_ribbon_clearance": fraction_text(PRIOR_RIBBON_CLEARANCE),
            "isotopy_ribbon_clearance_lower_bound": self.isotopy_ribbon_clearance_lower_bound,
            "minimum_height_gap": self.minimum_height_gap,
            "minimum_transversality": self.minimum_transversality,
            "minimum_distinct_crossing_point_gap": self.minimum_distinct_crossing_point_gap,
            "pairwise_linking_matrix": [list(row) for row in self.pairwise_linking_matrix],
            "standing": (
                "fixed generic projection with high-precision nonzero margins; "
                "integer invariants are exact for this certified crossing combinatorics"
            ),
        }
        if include_crossings:
            payload["crossings"] = [crossing.as_dict() for crossing in self.crossings]
            payload["arcs"] = [
                {
                    "index": arc.index,
                    "label": arc.label,
                    "component": arc.component,
                }
                for arc in self.arcs
            ]
            payload["relations"] = [
                {
                    "crossing_id": relation.crossing_id,
                    "sign": relation.sign,
                    "over_arc": relation.over_arc,
                    "incoming_under_arc": relation.incoming_under_arc,
                    "outgoing_under_arc": relation.outgoing_under_arc,
                    "word": [list(letter) for letter in relation.word],
                }
                for relation in self.relations
            ]
        return payload


def _mp_text(value: mp.mpf, digits: int = 60) -> str:
    return mp.nstr(value, n=digits, strip_zeros=False)


def _crossing_rows(ribbon: SmoothPrimeRibbon) -> tuple[DiagramCrossing, ...]:
    mp.mp.dps = MP_DECIMAL_DIGITS
    centers = _center_coordinates(ribbon.prime)
    rows: list[DiagramCrossing] = []
    for left, right in itertools.combinations(ribbon.carriers, 2):
        points = _circle_intersections(centers[left], centers[right])
        local: list[tuple[mp.mpf, DiagramCrossing]] = []
        for point in points:
            left_turn = _turn_at(point, centers[left])
            right_turn = _turn_at(point, centers[right])
            left_height = _smooth_lift_mp(ribbon, left, left_turn)
            right_height = _smooth_lift_mp(ribbon, right, right_turn)
            left_tangent = (
                -mp.sin(2 * mp.pi * left_turn),
                mp.cos(2 * mp.pi * left_turn),
            )
            right_tangent = (
                -mp.sin(2 * mp.pi * right_turn),
                mp.cos(2 * mp.pi * right_turn),
            )
            determinant = (
                left_tangent[0] * right_tangent[1]
                - left_tangent[1] * right_tangent[0]
            )
            height_difference = left_height - right_height
            sign = _sign(height_difference * determinant)
            if sign == 0:
                raise ExactMilnorAlexanderError(f"zero crossing sign for {left},{right}")
            over, under = (
                (left, right) if height_difference > 0 else (right, left)
            )
            over_turn, under_turn = (
                (left_turn, right_turn)
                if over == left
                else (right_turn, left_turn)
            )
            crossing = DiagramCrossing(
                crossing_id="pending",
                left=left,
                right=right,
                left_turn=_mp_text(left_turn),
                right_turn=_mp_text(right_turn),
                point_x=_mp_text(point[0]),
                point_y=_mp_text(point[1]),
                left_height=_mp_text(left_height),
                right_height=_mp_text(right_height),
                over=over,
                under=under,
                over_turn=_mp_text(over_turn),
                under_turn=_mp_text(under_turn),
                sign=sign,
                absolute_height_gap=_mp_text(abs(height_difference)),
                absolute_transversality=_mp_text(abs(determinant)),
            )
            local.append((left_turn, crossing))
        for index, (_, crossing) in enumerate(sorted(local, key=lambda item: item[0])):
            rows.append(
                replace(
                    crossing,
                    crossing_id=f"{left}::{right}::{index}",
                )
            )
    return tuple(rows)


def _under_crossings(
    crossings: Sequence[DiagramCrossing],
    carrier: str,
) -> tuple[DiagramCrossing, ...]:
    return tuple(
        sorted(
            (crossing for crossing in crossings if crossing.under == carrier),
            key=lambda crossing: crossing.under_turn_mpf,
        )
    )


def _arc_index_at_turn(
    carrier: str,
    turn: mp.mpf,
    under_events: Mapping[str, tuple[DiagramCrossing, ...]],
    arc_lookup: Mapping[tuple[str, int], int],
) -> int:
    events = under_events[carrier]
    if not events:
        return arc_lookup[(carrier, 0)]
    turns = [event.under_turn_mpf for event in events]
    position = bisect.bisect_left(turns, turn) - 1
    return arc_lookup[(carrier, position % len(events))]


def _wirtinger_structure(
    carriers: Sequence[str],
    crossings: Sequence[DiagramCrossing],
) -> tuple[tuple[ArcGenerator, ...], tuple[WirtingerRelation, ...]]:
    under_events = {
        carrier: _under_crossings(crossings, carrier) for carrier in carriers
    }
    arcs: list[ArcGenerator] = []
    arc_lookup: dict[tuple[str, int], int] = {}
    for carrier in carriers:
        count = max(1, len(under_events[carrier]))
        for local_index in range(count):
            index = len(arcs)
            arcs.append(ArcGenerator(index, carrier, local_index))
            arc_lookup[(carrier, local_index)] = index
    relations: list[WirtingerRelation] = []
    for crossing in crossings:
        events = under_events[crossing.under]
        local_index = next(
            index
            for index, event in enumerate(events)
            if event.crossing_id == crossing.crossing_id
        )
        outgoing = arc_lookup[(crossing.under, local_index)]
        incoming = arc_lookup[(crossing.under, (local_index - 1) % len(events))]
        over_arc = _arc_index_at_turn(
            crossing.over,
            crossing.over_turn_mpf,
            under_events,
            arc_lookup,
        )
        relations.append(
            WirtingerRelation(
                crossing.crossing_id,
                crossing.sign,
                over_arc,
                incoming,
                outgoing,
            )
        )
    return tuple(arcs), tuple(relations)


def _linking_matrix(
    carriers: Sequence[str],
    crossings: Sequence[DiagramCrossing],
) -> tuple[tuple[int, ...], ...]:
    index = {carrier: position for position, carrier in enumerate(carriers)}
    matrix = [[0] * len(carriers) for _ in carriers]
    for left, right in itertools.combinations(carriers, 2):
        signs = [
            crossing.sign
            for crossing in crossings
            if {crossing.left, crossing.right} == {left, right}
        ]
        if sum(signs) % 2:
            raise ExactMilnorAlexanderError(f"odd crossing-sign sum for {left},{right}")
        value = sum(signs) // 2
        matrix[index[left]][index[right]] = value
        matrix[index[right]][index[left]] = value
    return tuple(tuple(row) for row in matrix)


def _expected_linking_matrix(prime: int) -> tuple[tuple[int, ...], ...]:
    certificate = (
        certify_smooth_prime_seven() if prime == 7 else certify_smooth_prime_five()
    )
    return certificate.linking_matrix.matrix


def _projection_displacement_bounds(carriers: Sequence[str]) -> tuple[mp.mpf, mp.mpf, mp.mpf]:
    epsilon = _mp_fraction(PROJECTION_EPSILON)
    displacements = {
        carrier: (
            epsilon * SHIFT_VECTORS[carrier][0],
            epsilon * SHIFT_VECTORS[carrier][1],
        )
        for carrier in carriers
    }
    maximum_component = max(
        mp.sqrt(dx * dx + dy * dy) for dx, dy in displacements.values()
    )
    maximum_relative = max(
        mp.sqrt(
            (displacements[left][0] - displacements[right][0]) ** 2
            + (displacements[left][1] - displacements[right][1]) ** 2
        )
        for left, right in itertools.combinations(carriers, 2)
    )
    clearance = _mp_fraction(PRIOR_RIBBON_CLEARANCE) - maximum_relative
    return maximum_component, maximum_relative, clearance


def _minimum_crossing_point_gap(crossings: Sequence[DiagramCrossing]) -> mp.mpf:
    distances = []
    for left, right in itertools.combinations(crossings, 2):
        distances.append(
            mp.sqrt(
                (left.point[0] - right.point[0]) ** 2
                + (left.point[1] - right.point[1]) ** 2
            )
        )
    return min(distances) if distances else mp.inf


def _build_generic_diagram(prime: int) -> GenericLinkDiagram:
    ribbon = build_smooth_prime_seven() if prime == 7 else build_smooth_prime_five()
    crossings = _crossing_rows(ribbon)
    arcs, relations = _wirtinger_structure(ribbon.carriers, crossings)
    linking = _linking_matrix(ribbon.carriers, crossings)
    if linking != _expected_linking_matrix(prime):
        raise ExactMilnorAlexanderError("generic projection changed the pairwise linking matrix")
    minimum_height = min(mp.mpf(crossing.absolute_height_gap) for crossing in crossings)
    minimum_transversality = min(
        mp.mpf(crossing.absolute_transversality) for crossing in crossings
    )
    minimum_point_gap = _minimum_crossing_point_gap(crossings)
    maximum_component, maximum_relative, clearance = _projection_displacement_bounds(
        ribbon.carriers
    )
    if minimum_height <= MINIMUM_ACCEPTED_HEIGHT_GAP:
        raise ExactMilnorAlexanderError("generic crossing height margin is too small")
    if minimum_transversality <= MINIMUM_ACCEPTED_TRANSVERSALITY:
        raise ExactMilnorAlexanderError("generic crossing transversality margin is too small")
    if minimum_point_gap <= MINIMUM_ACCEPTED_CROSSING_POINT_GAP:
        raise ExactMilnorAlexanderError("generic crossing points are not sufficiently separated")
    if clearance <= 0:
        raise ExactMilnorAlexanderError("generic projection translation consumes ribbon clearance")
    return GenericLinkDiagram(
        prime=prime,
        carriers=ribbon.carriers,
        crossings=crossings,
        arcs=arcs,
        relations=relations,
        maximum_component_displacement=_mp_text(maximum_component),
        maximum_relative_displacement=_mp_text(maximum_relative),
        isotopy_ribbon_clearance_lower_bound=_mp_text(clearance),
        minimum_height_gap=_mp_text(minimum_height),
        minimum_transversality=_mp_text(minimum_transversality),
        minimum_distinct_crossing_point_gap=_mp_text(minimum_point_gap),
        pairwise_linking_matrix=linking,
    )


def build_generic_prime_seven_diagram() -> GenericLinkDiagram:
    return _build_generic_diagram(7)


def build_generic_prime_five_diagram() -> GenericLinkDiagram:
    return _build_generic_diagram(5)


class MagnusSeries:
    """Noncommutative power series truncated above total degree two."""

    __slots__ = ("coefficients",)

    def __init__(self, coefficients: Mapping[tuple[int, ...], Fraction] | None = None):
        self.coefficients = {
            word: Fraction(value)
            for word, value in (coefficients or {}).items()
            if value and len(word) <= 2
        }

    @classmethod
    def one(cls) -> "MagnusSeries":
        return cls({(): Fraction(1)})

    @classmethod
    def generator(cls, index: int) -> "MagnusSeries":
        return cls({(): Fraction(1), (index,): Fraction(1)})

    def __mul__(self, other: "MagnusSeries") -> "MagnusSeries":
        result: dict[tuple[int, ...], Fraction] = {}
        for left_word, left_value in self.coefficients.items():
            for right_word, right_value in other.coefficients.items():
                word = left_word + right_word
                if len(word) <= 2:
                    result[word] = result.get(word, Fraction(0)) + left_value * right_value
        return MagnusSeries(result)

    def inverse(self) -> "MagnusSeries":
        if self.coefficients.get((), Fraction(0)) != 1:
            raise ExactMilnorAlexanderError("Magnus inverse requires constant coefficient one")
        degree_one = {
            word: value for word, value in self.coefficients.items() if len(word) == 1
        }
        degree_two = {
            word: value for word, value in self.coefficients.items() if len(word) == 2
        }
        result: dict[tuple[int, ...], Fraction] = {(): Fraction(1)}
        for word, value in degree_one.items():
            result[word] = -value
        for word, value in degree_two.items():
            result[word] = result.get(word, Fraction(0)) - value
        for left_word, left_value in degree_one.items():
            for right_word, right_value in degree_one.items():
                word = left_word + right_word
                result[word] = result.get(word, Fraction(0)) + left_value * right_value
        return MagnusSeries(result)

    def power(self, exponent: int) -> "MagnusSeries":
        if exponent == 1:
            return self
        if exponent == -1:
            return self.inverse()
        raise ExactMilnorAlexanderError("only exponents plus or minus one are supported")

    def coefficient(self, word: Sequence[int]) -> Fraction:
        return self.coefficients.get(tuple(word), Fraction(0))

    def degree_one_coefficients(self, size: int) -> tuple[Fraction, ...]:
        return tuple(self.coefficient((index,)) for index in range(size))


def _triple_crossing_records(
    diagram: GenericLinkDiagram,
    components: Sequence[str],
) -> tuple[dict[str, object], ...]:
    selected = set(components)
    rows: list[dict[str, object]] = []
    for crossing in diagram.crossings:
        if crossing.left not in selected or crossing.right not in selected:
            continue
        rows.append(
            {
                "crossing_id": crossing.crossing_id,
                "sign": crossing.sign,
                "over": crossing.over,
                "under": crossing.under,
                "over_turn": crossing.over_turn_mpf,
                "under_turn": crossing.under_turn_mpf,
            }
        )
    return tuple(rows)


def _milnor_longitudes(
    components: Sequence[str],
    crossing_rows: Sequence[Mapping[str, object]],
) -> dict[str, MagnusSeries]:
    component_index = {component: index for index, component in enumerate(components)}
    meridians = {
        component: MagnusSeries.generator(component_index[component])
        for component in components
    }
    under_events = {
        component: tuple(
            sorted(
                (row for row in crossing_rows if row["under"] == component),
                key=lambda row: row["under_turn"],
            )
        )
        for component in components
    }
    after_states: dict[str, tuple[MagnusSeries, ...]] = {}
    for component in components:
        current = meridians[component]
        states: list[MagnusSeries] = []
        for row in under_events[component]:
            over_meridian = meridians[str(row["over"])]
            sign = int(row["sign"])
            current = (
                over_meridian.power(sign)
                * current
                * over_meridian.power(-sign)
            )
            states.append(current)
        after_states[component] = tuple(states)

    def arc_at(component: str, turn: mp.mpf) -> MagnusSeries:
        events = under_events[component]
        if not events:
            return meridians[component]
        first_turn = mp.mpf(events[0]["under_turn"])
        relative = [
            mp.fmod(mp.mpf(row["under_turn"]) - first_turn, 1) for row in events
        ]
        relative = [value if value >= 0 else value + 1 for value in relative]
        target = mp.fmod(turn - first_turn, 1)
        if target < 0:
            target += 1
        position = bisect.bisect_left(relative, target) - 1
        return (
            meridians[component]
            if position < 0
            else after_states[component][position]
        )

    longitudes: dict[str, MagnusSeries] = {}
    for component in components:
        longitude = MagnusSeries.one()
        for row in under_events[component]:
            over_arc = arc_at(str(row["over"]), mp.mpf(row["over_turn"]))
            # Prepending is load-bearing: repeated conjugations produce the
            # reverse product as the preferred longitude conjugator.
            longitude = over_arc.power(int(row["sign"])) * longitude
        longitudes[component] = longitude
    return longitudes


@dataclass(frozen=True, slots=True)
class MilnorIntegerCertificate:
    components: tuple[str, str, str]
    coefficient_ij_in_longitude_k: int
    coefficient_ji_in_longitude_k: int
    longitude_degree_one: tuple[int, int, int]
    crossing_ids: tuple[str, ...]

    @property
    def exact_zero(self) -> bool:
        return (
            self.coefficient_ij_in_longitude_k == 0
            and self.coefficient_ji_in_longitude_k == 0
            and self.longitude_degree_one == (0, 0, 0)
        )

    def as_dict(self) -> dict[str, object]:
        return {
            "components": list(self.components),
            "pairwise_linking_numbers": [0, 0, 0],
            "crossing_ids": list(self.crossing_ids),
            "preferred_longitude_degree_one": list(self.longitude_degree_one),
            "mu_ijk": self.coefficient_ij_in_longitude_k,
            "opposite_word_coefficient": self.coefficient_ji_in_longitude_k,
            "exact_zero": self.exact_zero,
            "standing": (
                "exact integer Magnus coefficient for the fixed generic diagram; "
                "diagram signs are guarded by recorded nonzero high-precision margins"
            ),
        }


def _milnor_certificate(
    diagram: GenericLinkDiagram,
    components: tuple[str, str, str],
) -> MilnorIntegerCertificate:
    index = {component: position for position, component in enumerate(components)}
    crossing_rows = _triple_crossing_records(diagram, components)
    longitudes = _milnor_longitudes(components, crossing_rows)
    longitude = longitudes[components[2]]
    degree_one = tuple(int(value) for value in longitude.degree_one_coefficients(3))
    coefficient = longitude.coefficient((index[components[0]], index[components[1]]))
    opposite = longitude.coefficient((index[components[1]], index[components[0]]))
    if coefficient.denominator != 1 or opposite.denominator != 1:
        raise ExactMilnorAlexanderError("Milnor Magnus coefficient is nonintegral")
    return MilnorIntegerCertificate(
        components=components,
        coefficient_ij_in_longitude_k=coefficient.numerator,
        coefficient_ji_in_longitude_k=opposite.numerator,
        longitude_degree_one=degree_one,
        crossing_ids=tuple(str(row["crossing_id"]) for row in crossing_rows),
    )


def _borromean_braid_crossings() -> tuple[dict[str, object], ...]:
    word = ((0, 1), (1, -1)) * 3
    positions = ["B0", "B1", "B2"]
    rows: list[dict[str, object]] = []
    for index, (generator, sign) in enumerate(word):
        left = positions[generator]
        right = positions[generator + 1]
        over, under = (left, right) if sign == 1 else (right, left)
        turn = mp.mpf(index * 2 + 1) / (2 * len(word))
        rows.append(
            {
                "crossing_id": f"BORROMEAN_{index}",
                "sign": sign,
                "over": over,
                "under": under,
                "over_turn": turn,
                "under_turn": turn,
            }
        )
        positions[generator], positions[generator + 1] = (
            positions[generator + 1],
            positions[generator],
        )
    if positions != ["B0", "B1", "B2"]:
        raise ExactMilnorAlexanderError("Borromean braid closure did not return each strand")
    return tuple(rows)


def borromean_magnus_benchmark() -> int:
    components = ("B0", "B1", "B2")
    longitudes = _milnor_longitudes(components, _borromean_braid_crossings())
    coefficient = longitudes["B2"].coefficient((0, 1))
    if coefficient.denominator != 1 or abs(coefficient.numerator) != 1:
        raise ExactMilnorAlexanderError("Borromean Magnus benchmark failed")
    return coefficient.numerator


def exact_p7_milnor_certificates() -> tuple[MilnorIntegerCertificate, ...]:
    if abs(borromean_magnus_benchmark()) != 1:
        raise ExactMilnorAlexanderError("Borromean benchmark gate failed")
    diagram = build_generic_prime_seven_diagram()
    certificates = tuple(
        _milnor_certificate(diagram, tuple(triple)) for triple in P7_SPLIT_TRIPLES
    )
    if not all(certificate.exact_zero for certificate in certificates):
        raise ExactMilnorAlexanderError("one or more P7 Milnor candidates are nonzero")
    return certificates


def _modular_inverse(value: int, modulus: int) -> int:
    value %= modulus
    if not value:
        raise ExactMilnorAlexanderError("zero has no modular inverse")
    return pow(value, -1, modulus)


def _matrix_rank_mod(matrix: Sequence[Sequence[int]], modulus: int) -> int:
    work = [[value % modulus for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column] % modulus),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = _modular_inverse(work[rank][column], modulus)
        work[rank] = [(value * inverse) % modulus for value in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (value - factor * pivot_value) % modulus
                for value, pivot_value in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def _fox_matrix(
    diagram: GenericLinkDiagram,
    component_values: Mapping[str, int],
    modulus: int,
) -> tuple[tuple[int, ...], ...]:
    generator_values = {
        arc.index: component_values[arc.component] % modulus for arc in diagram.arcs
    }
    rows: list[tuple[int, ...]] = []
    for relation in diagram.relations:
        derivatives = [0] * diagram.generator_count
        prefix = 1
        for generator, exponent in relation.word:
            value = generator_values[generator]
            if exponent == 1:
                derivatives[generator] = (derivatives[generator] + prefix) % modulus
                prefix = (prefix * value) % modulus
            elif exponent == -1:
                inverse = _modular_inverse(value, modulus)
                derivatives[generator] = (
                    derivatives[generator] - prefix * inverse
                ) % modulus
                prefix = (prefix * inverse) % modulus
            else:
                raise ExactMilnorAlexanderError("Fox word contains unsupported exponent")
        if prefix % modulus != 1:
            raise ExactMilnorAlexanderError("Wirtinger relator did not abelianize to one")
        rows.append(tuple(derivatives))
    return tuple(rows)


def _primitive_order_element(prime: int) -> tuple[int, int, int]:
    modulus = FIELD_MODULUS[prime]
    root = FIELD_PRIMITIVE_ROOT[prime]
    if pow(root, modulus - 1, modulus) != 1:
        raise ExactMilnorAlexanderError("declared finite-field root is invalid")
    for divisor in range(1, modulus - 1):
        if (modulus - 1) % divisor == 0 and divisor < modulus - 1:
            if pow(root, divisor, modulus) == 1:
                raise ExactMilnorAlexanderError("declared finite-field root is not primitive")
    zeta = pow(root, (modulus - 1) // prime, modulus)
    if pow(zeta, prime, modulus) != 1 or zeta == 1:
        raise ExactMilnorAlexanderError("failed to construct prime-order character")
    return modulus, root, zeta


def _component_character(
    prime: int,
    winding: int,
    numerator: int,
) -> dict[str, int]:
    modulus, _, zeta = _primitive_order_element(prime)
    values = {"C": pow(zeta, winding % prime, modulus)}
    values.update(
        {
            f"R{index}": pow(zeta, (index * numerator) % prime, modulus)
            for index in range(prime - 1)
        }
    )
    return values


def _fox_rank_for_candidate(
    diagram: GenericLinkDiagram,
    winding: int,
    numerator: int,
) -> tuple[int, int]:
    modulus = FIELD_MODULUS[diagram.prime]
    matrix = _fox_matrix(
        diagram,
        _component_character(diagram.prime, winding, numerator),
        modulus,
    )
    rank = _matrix_rank_mod(matrix, modulus)
    excess_nullity = diagram.generator_count - rank - 1
    if excess_nullity < 0:
        raise ExactMilnorAlexanderError("Fox excess nullity became negative")
    return rank, excess_nullity


@dataclass(frozen=True, slots=True)
class FoxCharacterRow:
    winding_residue: int
    outer_numerator: int
    rank: int
    excess_nullity: int

    def as_dict(self) -> dict[str, int]:
        return {
            "winding_residue": self.winding_residue,
            "outer_numerator": self.outer_numerator,
            "rank": self.rank,
            "excess_nullity": self.excess_nullity,
        }


@dataclass(frozen=True, slots=True)
class FoxRankFingerprint:
    prime: int
    field_modulus: int
    primitive_root: int
    prime_order_element: int
    generator_count: int
    relation_count: int
    rows: tuple[FoxCharacterRow, ...]

    @property
    def histogram(self) -> dict[str, int]:
        counts = Counter(row.excess_nullity for row in self.rows)
        return {str(key): counts[key] for key in sorted(counts)}

    @property
    def ordered_rank_vector_sha256(self) -> str:
        return _canonical_json_sha256(
            [
                [
                    row.winding_residue,
                    row.outer_numerator,
                    row.rank,
                    row.excess_nullity,
                ]
                for row in self.rows
            ]
        )

    def as_dict(self, *, include_rows: bool = True) -> dict[str, object]:
        payload: dict[str, object] = {
            "prime": self.prime,
            "field_modulus": self.field_modulus,
            "primitive_root": self.primitive_root,
            "prime_order_element": self.prime_order_element,
            "generator_count": self.generator_count,
            "relation_count": self.relation_count,
            "character_count": len(self.rows),
            "excess_nullity_histogram": self.histogram,
            "ordered_rank_vector_sha256": self.ordered_rank_vector_sha256,
            "standing": (
                "finite-character specialization fingerprint of the multivariable Fox-Alexander presentation; "
                "not the full multivariable Alexander polynomial"
            ),
        }
        if include_rows:
            payload["characters"] = [row.as_dict() for row in self.rows]
        return payload


def _fingerprint_in_field(
    prime: int,
    modulus: int,
    root: int,
) -> FoxRankFingerprint:
    diagram = (
        build_generic_prime_seven_diagram()
        if prime == 7
        else build_generic_prime_five_diagram()
    )
    if (modulus - 1) % prime:
        raise ExactMilnorAlexanderError("field multiplicative order is not divisible by the prime")
    zeta = pow(root, (modulus - 1) // prime, modulus)
    if pow(zeta, prime, modulus) != 1 or zeta == 1:
        raise ExactMilnorAlexanderError("field does not supply the requested prime-order character")
    rows = []
    for winding_residue in range(prime):
        for numerator in range(1, prime):
            values = {"C": pow(zeta, winding_residue, modulus)}
            values.update(
                {
                    f"R{index}": pow(zeta, (index * numerator) % prime, modulus)
                    for index in range(prime - 1)
                }
            )
            matrix = _fox_matrix(diagram, values, modulus)
            rank = _matrix_rank_mod(matrix, modulus)
            rows.append(
                FoxCharacterRow(
                    winding_residue,
                    numerator,
                    rank,
                    diagram.generator_count - rank - 1,
                )
            )
    return FoxRankFingerprint(
        prime=prime,
        field_modulus=modulus,
        primitive_root=root,
        prime_order_element=zeta,
        generator_count=diagram.generator_count,
        relation_count=diagram.relation_count,
        rows=tuple(rows),
    )


def fox_rank_fingerprint(prime: int) -> FoxRankFingerprint:
    modulus, root, _ = _primitive_order_element(prime)
    return _fingerprint_in_field(prime, modulus, root)


def common_field_fox_rank_fingerprint(prime: int) -> FoxRankFingerprint:
    return _fingerprint_in_field(
        prime, COMMON_FIELD_MODULUS, COMMON_FIELD_PRIMITIVE_ROOT
    )


@lru_cache(maxsize=2)
def _phase_lift_candidate(prime: int):
    return (
        build_prime_seven_phase_lift()
        if prime == 7
        else build_prime_five_phase_lift()
    )


def _phase_lift_alignment_energy(
    prime: int,
    winding: int,
    numerator: int,
) -> Fraction:
    candidate = _phase_lift_candidate(prime)
    step = Fraction(numerator, prime)
    total = Fraction(0)
    for node in candidate.hypernodes:
        for occurrence in node.occurrences:
            phase = _mod1(
                winding * occurrence.turn
                if occurrence.carrier == "C"
                else _outer(occurrence.carrier) * step
            )
            target = Fraction(occurrence.residue, prime)
            difference = abs(phase - target)
            distance = min(difference, 1 - difference)
            total += distance * distance
    return total


def _enumerate_phase_candidates(prime: int) -> tuple[dict[str, object], ...]:
    primitive, turns, _, _, _ = _dataset(prime)
    diagram = (
        build_generic_prime_seven_diagram()
        if prime == 7
        else build_generic_prime_five_diagram()
    )
    rows: list[dict[str, object]] = []
    for winding in range(-2 * prime, 2 * prime + 1):
        for numerator in range(1, prime):
            step = Fraction(numerator, prime)
            gaps: list[Fraction] = []
            for node in primitive.hypernodes:
                phases = [
                    _mod1(
                        winding * turns[carrier][node.node_id]
                        if carrier == "C"
                        else _outer(carrier) * step
                    )
                    for carrier in node.carriers
                ]
                gap = _min_gap(phases)
                if gap == 0:
                    break
                gaps.append(gap)
            else:
                rank, excess = _fox_rank_for_candidate(
                    diagram, winding, numerator
                )
                energy = _phase_lift_alignment_energy(
                    prime, winding, numerator
                )
                rows.append(
                    {
                        "winding": winding,
                        "outer_numerator": numerator,
                        "outer_step": step,
                        "minimum_gap": min(gaps),
                        "fox_rank": rank,
                        "fox_excess_nullity": excess,
                        "alignment_energy": energy,
                        "boundary_meridional_degree": 1 + 2 * winding,
                    }
                )
    return tuple(rows)


@dataclass(frozen=True, slots=True)
class PhaseSelectorResult:
    prime: int
    preregistration_sha256: str
    candidate_count: int
    admissible_count: int
    maximum_gap_candidate_count: int
    maximum_gap: Fraction
    selected_winding: int
    selected_outer_numerator: int
    selected_fox_rank: int
    selected_fox_excess_nullity: int
    selected_alignment_energy: Fraction
    selected_boundary_meridional_degree: int
    co_winners_before_neutral_tiebreak: tuple[tuple[int, int], ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "prime": self.prime,
            "preregistration_sha256": self.preregistration_sha256,
            "candidate_count": self.candidate_count,
            "admissible_count": self.admissible_count,
            "maximum_gap_candidate_count": self.maximum_gap_candidate_count,
            "maximum_gap": fraction_text(self.maximum_gap),
            "selected": {
                "center_winding": self.selected_winding,
                "outer_numerator": self.selected_outer_numerator,
                "outer_step": f"{self.selected_outer_numerator}/{self.prime}",
                "fox_rank": self.selected_fox_rank,
                "fox_excess_nullity": self.selected_fox_excess_nullity,
                "alignment_energy": fraction_text(self.selected_alignment_energy),
                "boundary_meridional_degree": self.selected_boundary_meridional_degree,
            },
            "co_winners_before_neutral_tiebreak": [
                {"center_winding": winding, "outer_numerator": numerator}
                for winding, numerator in self.co_winners_before_neutral_tiebreak
            ],
            "frozen_selector_order": [
                "maximum minimum phase gap",
                "maximum Fox-Alexander excess nullity",
                "minimum exact phase-lift alignment energy",
                "minimum absolute center winding",
                "positive before negative winding",
                "smallest outer numerator",
            ],
            "target_degree_not_used": True,
        }


def evaluate_preregistered_phase_selector(prime: int) -> PhaseSelectorResult:
    rows = _enumerate_phase_candidates(prime)
    if not rows:
        raise ExactMilnorAlexanderError("no admissible phase candidates")
    maximum_gap = max(row["minimum_gap"] for row in rows)
    maximum_gap_rows = [row for row in rows if row["minimum_gap"] == maximum_gap]
    maximum_nullity = max(row["fox_excess_nullity"] for row in maximum_gap_rows)
    nullity_rows = [
        row for row in maximum_gap_rows
        if row["fox_excess_nullity"] == maximum_nullity
    ]
    minimum_energy = min(row["alignment_energy"] for row in nullity_rows)
    substantive_winners = [
        row for row in nullity_rows if row["alignment_energy"] == minimum_energy
    ]

    def neutral_key(row: Mapping[str, object]) -> tuple[int, int, int]:
        winding = int(row["winding"])
        sign_preference = 2 if winding > 0 else 1 if winding == 0 else 0
        return (-abs(winding), sign_preference, -int(row["outer_numerator"]))

    selected = max(substantive_winners, key=neutral_key)
    return PhaseSelectorResult(
        prime=prime,
        preregistration_sha256=PREREGISTRATION_SHA256,
        candidate_count=(4 * prime + 1) * (prime - 1),
        admissible_count=len(rows),
        maximum_gap_candidate_count=len(maximum_gap_rows),
        maximum_gap=maximum_gap,
        selected_winding=int(selected["winding"]),
        selected_outer_numerator=int(selected["outer_numerator"]),
        selected_fox_rank=int(selected["fox_rank"]),
        selected_fox_excess_nullity=int(selected["fox_excess_nullity"]),
        selected_alignment_energy=Fraction(selected["alignment_energy"]),
        selected_boundary_meridional_degree=int(selected["boundary_meridional_degree"]),
        co_winners_before_neutral_tiebreak=tuple(
            sorted(
                (
                    int(row["winding"]),
                    int(row["outer_numerator"]),
                )
                for row in substantive_winners
            )
        ),
    )


def exact_milnor_alexander_family_certificate() -> dict[str, object]:
    p7_diagram = build_generic_prime_seven_diagram()
    p5_diagram = build_generic_prime_five_diagram()
    p7_milnor = exact_p7_milnor_certificates()
    p7_fingerprint = fox_rank_fingerprint(7)
    p5_fingerprint = fox_rank_fingerprint(5)
    p7_common_fingerprint = common_field_fox_rank_fingerprint(7)
    p5_common_fingerprint = common_field_fox_rank_fingerprint(5)
    p7_selector = evaluate_preregistered_phase_selector(7)
    p5_selector = evaluate_preregistered_phase_selector(5)
    payload: dict[str, object] = {
        "schema_id": f"{SCHEMA_ID}.family",
        "schema_version": SCHEMA_VERSION,
        "authority": "Erin Spencer",
        "recorded_on": "2026-08-11",
        "selection_effect": "none",
        "research_order": [7, 5],
        "source": {
            "name": SOURCE_NAME,
            "sha256": SOURCE_SHA256,
            "line_basis": list(SOURCE_LINES),
        },
        "preregistration": {
            "document": PREREGISTRATION_DOCUMENT,
            "document_sha256": PREREGISTRATION_SHA256,
            "frozen_before_evaluation": True,
        },
        "generic_diagrams": {
            "p7": p7_diagram.as_dict(include_crossings=False),
            "p5": p5_diagram.as_dict(include_crossings=False),
        },
        "exact_milnor": {
            "method": (
                "Wirtinger preferred longitudes with exact noncommutative Magnus expansion through degree two"
            ),
            "borromean_braid": {
                "word": "(sigma_1 sigma_2^-1)^3",
                "mu_012": borromean_magnus_benchmark(),
                "gate_passed": abs(borromean_magnus_benchmark()) == 1,
            },
            "p7_pairwise_zero_triples": [
                certificate.as_dict() for certificate in p7_milnor
            ],
            "all_five_exact_zero": all(
                certificate.exact_zero for certificate in p7_milnor
            ),
            "numerical_fourier_result_superseded": (
                "the prior convergence-to-zero evidence is retained as an independent check; "
                "the fixed generic diagram now supplies integer degree-two coefficients"
            ),
        },
        "prime_character_fox_alexander": {
            "p7": p7_fingerprint.as_dict(include_rows=True),
            "p5": p5_fingerprint.as_dict(include_rows=True),
            "common_field_replay": {
                "field_modulus": COMMON_FIELD_MODULUS,
                "primitive_root": COMMON_FIELD_PRIMITIVE_ROOT,
                "p7": p7_common_fingerprint.as_dict(include_rows=False),
                "p5": p5_common_fingerprint.as_dict(include_rows=False),
                "p7_matches_prime_specific_rank_vector": (
                    p7_common_fingerprint.ordered_rank_vector_sha256
                    == p7_fingerprint.ordered_rank_vector_sha256
                ),
                "p5_matches_prime_specific_rank_vector": (
                    p5_common_fingerprint.ordered_rank_vector_sha256
                    == p5_fingerprint.ordered_rank_vector_sha256
                ),
                "selector_effect": "none; this replay was not used to choose a phase law",
            },
            "comparison": {
                "rank_vector_hashes_differ": (
                    p7_fingerprint.ordered_rank_vector_sha256
                    != p5_fingerprint.ordered_rank_vector_sha256
                ),
                "standing": (
                    "stronger than pairwise linking as a link-group-module readout, "
                    "but not a complete link invariant"
                ),
            },
        },
        "preregistered_phase_selector": {
            "p7": p7_selector.as_dict(),
            "p5": p5_selector.as_dict(),
            "conclusion": (
                "the selected boundary degree is an observed output of the frozen selector; "
                "no target degree was included in the score"
            ),
        },
        "next": [
            "replay the generic crossing-sign margins with outward-rounded interval atan2 and smooth-field evaluation",
            "compute a symbolic or multivariable Alexander presentation from the same Wirtinger diagram",
            "test higher Milnor invariants and finite nilpotent quotients of the complete P7 link group",
            "only after phase selection and whole-link invariants stabilize, define a spectral object",
        ],
        "nonclaims": [
            "not a proof-assistant verification of the generic diagram",
            "not a complete ambient-isotopy classification",
            "not the full multivariable Alexander polynomial",
            "not an arithmetic redefinition of primality",
            "not an electron ontology or Pauli-exclusion derivation",
            "not a spectral operator, prime-power law, zeta-zero correspondence, or proof of the Riemann hypothesis",
        ],
    }
    payload["payload_sha256"] = _canonical_json_sha256(payload)
    return payload


def write_exact_milnor_alexander_family_certificate(
    path: str | Path,
    *,
    indent: int = 2,
) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            exact_milnor_alexander_family_certificate(),
            indent=indent,
            sort_keys=True,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return output
