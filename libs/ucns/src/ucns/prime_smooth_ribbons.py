# === MODULE_BUILD ===
# id: ucns_prime_smooth_ribbons_p7_p5
#   module_name: prime_smooth_ribbons
#   module_kind: experiment
#   summary: replaces the P7-first piecewise-linear lift by a C-infinity event-preserving field, certifies global finite-width ribbon separation by deterministic Lipschitz subdivision, regularizes tangent projections, and applies the same protocol to P5 second
#   owner: Erin Spencer
#   public_surface: SmoothPeriodicField, SmoothPrimeRibbon, PairSeparationCertificate, TangentRegularization, LinkingMatrixCertificate, SmoothRibbonCertificate, flat_step, flat_step_derivative, build_smooth_prime_seven, build_smooth_prime_five, certify_smooth_prime_seven, certify_smooth_prime_five, smooth_ribbon_family_certificate, write_smooth_ribbon_family_certificate, render_smooth_centerline_obj, render_smooth_ribbon_obj
#   internal_surface: flat C-infinity interpolation, exact derivative majorant, binary64 Lipschitz subdivision, pair-specific tangent isotopy, rational matrix rank
#   auth_boundary: none
#   storage_boundary: caller-supplied local paths only through writer functions
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_smooth_ribbons.py
#   rollout: P7 first, P5 same-protocol comparison second; selection effect none; does not alter prior phase or lift receipts
#   rollback: remove this module, its test, documentation, generated certificate, and generated meshes
#   requires: ucns_prime_phase_lift_p7_p5
#   since: 2026-08-11
#   unresolved: formal interval or proof-assistant replay, whole-link ambient isotopy, higher-order link invariants, boundary-link invariants, spectral operator, prime-power law, zeta correspondence
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: prime_smooth_ribbons_preserve_all_event_lanes
#   given: the piecewise-linear P7 or P5 lift knots are replaced
#   then: one periodic C-infinity field per carrier reproduces every exact event height without overshoot
#   class: correctness
#   since: 2026-08-11
#
# id: prime_smooth_ribbons_obey_mobius_return
#   given: any carrier and admissible breadth
#   then: the smoothed surface obeys one-turn breadth reversal and two-turn return
#   class: correctness
#   since: 2026-08-11
#
# id: prime_smooth_ribbons_have_global_centerline_margin
#   given: every unordered pair of P7 or P5 carriers is subdivided over the complete parameter torus
#   then: a deterministic Lipschitz certificate establishes centerline separation greater than nine hundredths under the declared binary64 roundoff boundary
#   class: evidence
#   since: 2026-08-11
#
# id: prime_smooth_ribbons_are_globally_disjoint_at_declared_width
#   given: centerline separation exceeds nine hundredths and ribbon half-width is one hundredth
#   then: the complete finite-width ribbons have pairwise separation greater than seven hundredths by the triangle inequality
#   class: correctness
#   since: 2026-08-11
#
# id: prime_smooth_ribbons_regularize_tangent_pairs
#   given: a projected pair is externally tangent
#   then: a one-hundredth outward pair-specific isotopy remains inside the global clearance, makes the projected circles disjoint, and certifies linking number zero
#   class: evidence
#   since: 2026-08-11
#
# id: prime_smooth_ribbons_issue_complete_linking_matrix
#   given: regular secant readouts and tangent regularizations are combined
#   then: every pair receives an integer linking number and matrix rank, nullity, determinant, and nonzero-link graph readouts are derived
#   class: evidence
#   since: 2026-08-11
#
# id: prime_smooth_ribbons_p7_precedes_p5
#   given: the family certificate is built
#   then: P7 is certified first and P5 is independently processed second under the same smoothing and separation protocol
#   class: doctrine
#   since: 2026-08-11
#
# id: prime_smooth_ribbons_receipt_is_nonselecting
#   given: the family receipt is serialized
#   then: it records the numerical proof boundary and claims no arithmetic redefinition, electron ontology, zeta theorem, or Riemann-hypothesis proof
#   class: doctrine
#   since: 2026-08-11
# === END CONTRACTS ===

"""Smooth finite-width ribbon certificate for the P7-first lift.

The lift knots from :mod:`ucns.prime_phase_lift` are interpolated with the
standard flat C-infinity step

    S(x) = exp(-1/x) / (exp(-1/x) + exp(-1/(1-x)))

on each knot interval. All derivatives vanish at interval endpoints, so the
periodic pieces join smoothly while preserving every event height exactly.

Global centerline separation is checked by a deterministic branch-and-bound
cover of each parameter torus. Each box uses a center sample and the analytic
curve-speed majorants. The calculation includes a declared 1e-12 binary64
roundoff buffer. It is strong computer-assisted evidence, not formal interval
arithmetic or a proof-assistant replay.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Mapping, Sequence

from .prime_phase_lift import build_prime_five_phase_lift, build_prime_seven_phase_lift
from .prime_phase_lift_data import P5_CENTERS, P7_CENTERS
from .prime_phase_lift_model import HALF_WIDTH, PrimePhaseLiftCandidate

SCHEMA_ID = "ucns.prime-smooth-ribbons"
SCHEMA_VERSION = "0.1.0"
SOURCE_NAME = "Möbius Strips and Quantum Geometry.txt"
SOURCE_SHA256 = "dc3a94ca5070ffff8f2a246f48db77192b08f521e721bc7c2a011aa05ddeb9a1"
SOURCE_LINES = (5, 6, 13, 14, 15, 16, 17)
CENTERLINE_SEPARATION_TARGET = Fraction(9, 100)
RIBBON_SEPARATION_LOWER_BOUND = CENTERLINE_SEPARATION_TARGET - 2 * HALF_WIDTH
ROUND_OFF_BUFFER = 1e-12
TANGENT_REGULARIZATION_EPSILON = Fraction(1, 100)
MAX_CERTIFICATE_BOXES_PER_PAIR = 100_000


class SmoothRibbonError(ValueError):
    pass


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def flat_step(value: float) -> float:
    x = float(value)
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    exponent = 1.0 / x - 1.0 / (1.0 - x)
    if exponent >= 0.0:
        small = math.exp(-exponent)
        return small / (1.0 + small)
    small = math.exp(exponent)
    return 1.0 / (1.0 + small)


def flat_step_derivative(value: float) -> float:
    x = float(value)
    if x <= 0.0 or x >= 1.0:
        return 0.0
    step = flat_step(x)
    return step * (1.0 - step) * (1.0 / (x * x) + 1.0 / ((1.0 - x) ** 2))


@dataclass(frozen=True, slots=True)
class SmoothSegment:
    left_turn: Fraction
    right_turn: Fraction
    left_value: Fraction
    right_value: Fraction

    def __post_init__(self) -> None:
        if self.right_turn <= self.left_turn:
            raise SmoothRibbonError("smooth segment requires positive turn width")

    @property
    def turn_width(self) -> Fraction:
        return self.right_turn - self.left_turn

    @property
    def derivative_bound(self) -> Fraction:
        return 2 * abs(self.right_value - self.left_value) / self.turn_width

    def contains(self, turn: Fraction) -> bool:
        return self.left_turn <= turn <= self.right_turn

    def evaluate(self, turn: Fraction) -> float:
        if turn == self.left_turn:
            return float(self.left_value)
        if turn == self.right_turn:
            return float(self.right_value)
        local = float((turn - self.left_turn) / self.turn_width)
        return float(self.left_value) + float(self.right_value - self.left_value) * flat_step(local)

    def derivative(self, turn: Fraction) -> float:
        if turn <= self.left_turn or turn >= self.right_turn:
            return 0.0
        local = float((turn - self.left_turn) / self.turn_width)
        return float(self.right_value - self.left_value) / float(self.turn_width) * flat_step_derivative(local)


@dataclass(frozen=True, slots=True)
class SmoothPeriodicField:
    carrier: str
    knots: tuple[tuple[Fraction, Fraction], ...]
    segments: tuple[SmoothSegment, ...]

    @classmethod
    def from_candidate(cls, candidate: PrimePhaseLiftCandidate, carrier: str) -> "SmoothPeriodicField":
        knots = tuple(sorted((item.turn, item.height) for node in candidate.hypernodes for item in node.occurrences if item.carrier == carrier))
        if not knots or len({turn for turn, _ in knots}) != len(knots):
            raise SmoothRibbonError(f"invalid lift knots for {carrier}")
        segments = []
        for index, (left_turn, left_value) in enumerate(knots):
            right_turn, right_value = knots[(index + 1) % len(knots)]
            if index == len(knots) - 1:
                right_turn += 1
            segments.append(SmoothSegment(left_turn, right_turn, left_value, right_value))
        return cls(carrier, knots, tuple(segments))

    @property
    def maximum_derivative_bound(self) -> Fraction:
        return max(segment.derivative_bound for segment in self.segments)

    @property
    def minimum_value(self) -> Fraction:
        return min(value for _, value in self.knots)

    @property
    def maximum_value(self) -> Fraction:
        return max(value for _, value in self.knots)

    def _canonical_target(self, turn: int | float | Fraction) -> Fraction:
        if isinstance(turn, bool):
            raise SmoothRibbonError("turn cannot be boolean")
        if isinstance(turn, Fraction):
            return turn % 1
        if isinstance(turn, int):
            return Fraction(turn) % 1
        number = float(turn)
        if not math.isfinite(number):
            raise SmoothRibbonError("turn must be finite")
        return Fraction.from_float(number % 1.0)

    def _segment_and_target(self, turn: int | float | Fraction) -> tuple[SmoothSegment, Fraction]:
        target = self._canonical_target(turn)
        for index, segment in enumerate(self.segments):
            adjusted = target
            if index == len(self.segments) - 1 and adjusted < segment.left_turn:
                adjusted += 1
            if segment.contains(adjusted):
                return segment, adjusted
        raise AssertionError("periodic smooth interval search failed")

    def evaluate(self, turn: int | float | Fraction) -> float:
        segment, target = self._segment_and_target(turn)
        return segment.evaluate(target)

    def derivative(self, turn: int | float | Fraction) -> float:
        segment, target = self._segment_and_target(turn)
        return segment.derivative(target)

    @property
    def maximum_event_residual(self) -> float:
        return max(abs(self.evaluate(turn) - float(value)) for turn, value in self.knots)

    def as_dict(self) -> dict[str, object]:
        return {
            "carrier": self.carrier,
            "kind": "periodic-C-infinity-flat-step",
            "period": "1 turn",
            "event_knots": [{"turn": fraction_text(turn), "height": fraction_text(value)} for turn, value in self.knots],
            "event_values_preserved": self.maximum_event_residual == 0.0,
            "value_range": [fraction_text(self.minimum_value), fraction_text(self.maximum_value)],
            "maximum_derivative_bound": fraction_text(self.maximum_derivative_bound),
            "derivative_bound_proof": "flat step S has 0<=S'<=2; each interval scales the bound by |delta_z|/delta_t",
        }


@dataclass(frozen=True, slots=True)
class SmoothPrimeRibbon:
    base: PrimePhaseLiftCandidate
    fields: tuple[SmoothPeriodicField, ...]

    @property
    def prime(self) -> int:
        return self.base.prime

    @property
    def carriers(self) -> tuple[str, ...]:
        return self.base.carriers

    @property
    def half_width(self) -> Fraction:
        return HALF_WIDTH

    def field(self, carrier: str) -> SmoothPeriodicField:
        return next(item for item in self.fields if item.carrier == carrier)

    def centers(self) -> Mapping[str, tuple[float, float]]:
        return P7_CENTERS if self.prime == 7 else P5_CENTERS

    def lift(self, carrier: str, turn: int | float | Fraction) -> float:
        return self.field(carrier).evaluate(turn)

    def centerline_point(self, carrier: str, turn: int | float | Fraction) -> tuple[float, float, float]:
        t = float(turn) % 1.0
        center_x, center_y = self.centers()[carrier]
        angle = math.tau * t
        return center_x + math.cos(angle), center_y + math.sin(angle), self.lift(carrier, turn)

    def surface_point(self, carrier: str, turn: int | float | Fraction, breadth: int | float | Fraction) -> tuple[float, float, float]:
        u = float(breadth)
        if not math.isfinite(u) or abs(u) > float(self.half_width) + 1e-15:
            raise SmoothRibbonError("breadth exceeds declared half-width")
        t_fraction = turn if isinstance(turn, Fraction) else Fraction.from_float(float(turn))
        t = float(t_fraction)
        center_x, center_y = self.centers()[carrier]
        radial_x, radial_y = math.cos(math.tau * t), math.sin(math.tau * t)
        frame_turns = Fraction(1, 2) * t_fraction + self.base.phase_law.unwrapped(carrier, t_fraction)
        frame = math.tau * float(frame_turns)
        radial_offset = u * math.cos(frame)
        vertical_offset = u * math.sin(frame)
        return center_x + (1.0 + radial_offset) * radial_x, center_y + (1.0 + radial_offset) * radial_y, self.lift(carrier, t_fraction) + vertical_offset

    def speed_upper_bound(self, carrier: str) -> float:
        return math.nextafter(math.hypot(math.tau, float(self.field(carrier).maximum_derivative_bound)), math.inf)

    @property
    def maximum_event_height_residual(self) -> float:
        return max(field.maximum_event_residual for field in self.fields)

    def seam_residuals(self) -> tuple[float, float]:
        one_turn = two_turn = 0.0
        turns = (Fraction(0), Fraction(1, 13), Fraction(5, 17), Fraction(11, 19))
        breadths = (-self.half_width, Fraction(0), self.half_width)
        for carrier in self.carriers:
            for turn in turns:
                for breadth in breadths:
                    one_turn = max(one_turn, math.dist(self.surface_point(carrier, turn + 1, breadth), self.surface_point(carrier, turn, -breadth)))
                    two_turn = max(two_turn, math.dist(self.surface_point(carrier, turn + 2, breadth), self.surface_point(carrier, turn, breadth)))
        return one_turn, two_turn

    def as_dict(self) -> dict[str, object]:
        one_turn, two_turn = self.seam_residuals()
        return {
            "prime": self.prime,
            "construction_lineage": "global prime phase-and-lift candidate first; smooth fields replace its lift interpolation only",
            "smoothness": {"class": "C-infinity", "field": "flat-step interpolation on every periodic knot interval", "maximum_event_height_residual_binary64": self.maximum_event_height_residual, "no_overshoot": True},
            "mobius_return": {"one_turn": "X(t+1,u)=X(t,-u)", "two_turn": "X(t+2,u)=X(t,u)", "maximum_sampled_one_turn_residual_binary64": one_turn, "maximum_sampled_two_turn_residual_binary64": two_turn},
            "fields": [field.as_dict() for field in self.fields],
        }


@dataclass(frozen=True, slots=True)
class PairSeparationCertificate:
    left: str
    right: str
    target: Fraction
    left_speed_upper_bound: float
    right_speed_upper_bound: float
    boxes_evaluated: int
    certified_leaf_boxes: int
    maximum_depth: int
    minimum_leaf_lower_bound: float
    minimum_sample_distance: float
    roundoff_buffer: float

    @property
    def pair_id(self) -> str:
        return f"{self.left}::{self.right}"

    @property
    def certified(self) -> bool:
        return self.minimum_leaf_lower_bound > float(self.target)

    def as_dict(self) -> dict[str, object]:
        return {"pair_id": self.pair_id, "target": fraction_text(self.target), "certified": self.certified, "left_speed_upper_bound_binary64": self.left_speed_upper_bound, "right_speed_upper_bound_binary64": self.right_speed_upper_bound, "boxes_evaluated": self.boxes_evaluated, "certified_leaf_boxes": self.certified_leaf_boxes, "maximum_depth": self.maximum_depth, "minimum_leaf_lower_bound_binary64": self.minimum_leaf_lower_bound, "minimum_sample_distance_binary64": self.minimum_sample_distance, "roundoff_buffer": self.roundoff_buffer}


def _distance3(left: Sequence[float], right: Sequence[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


def _certify_pair_separation(ribbon: SmoothPrimeRibbon, left: str, right: str, *, target: Fraction = CENTERLINE_SEPARATION_TARGET) -> PairSeparationCertificate:
    left_speed = ribbon.speed_upper_bound(left)
    right_speed = ribbon.speed_upper_bound(right)
    pending = [(0.0, 1.0, 0.0, 1.0, 0)]
    evaluated = leaves = maximum_depth = 0
    minimum_leaf_lower = minimum_sample = math.inf
    while pending:
        left_a, left_b, right_a, right_b, depth = pending.pop()
        evaluated += 1
        if evaluated > MAX_CERTIFICATE_BOXES_PER_PAIR:
            raise SmoothRibbonError(f"separation subdivision exceeded box limit for {left}::{right}")
        maximum_depth = max(maximum_depth, depth)
        left_center = (left_a + left_b) / 2.0
        right_center = (right_a + right_b) / 2.0
        sample = _distance3(ribbon.centerline_point(left, left_center), ribbon.centerline_point(right, right_center))
        minimum_sample = min(minimum_sample, sample)
        lower = sample - left_speed * (left_b - left_a) / 2.0 - right_speed * (right_b - right_a) / 2.0 - ROUND_OFF_BUFFER
        if lower > float(target):
            leaves += 1
            minimum_leaf_lower = min(minimum_leaf_lower, lower)
            continue
        if left_speed * (left_b - left_a) >= right_speed * (right_b - right_a):
            midpoint = (left_a + left_b) / 2.0
            pending.extend([(midpoint, left_b, right_a, right_b, depth + 1), (left_a, midpoint, right_a, right_b, depth + 1)])
        else:
            midpoint = (right_a + right_b) / 2.0
            pending.extend([(left_a, left_b, midpoint, right_b, depth + 1), (left_a, left_b, right_a, midpoint, depth + 1)])
    certificate = PairSeparationCertificate(left, right, target, left_speed, right_speed, evaluated, leaves, maximum_depth, minimum_leaf_lower, minimum_sample, ROUND_OFF_BUFFER)
    if not certificate.certified:
        raise SmoothRibbonError(f"pair separation not certified: {certificate.pair_id}")
    return certificate


@dataclass(frozen=True, slots=True)
class TangentRegularization:
    left: str
    right: str
    moved_carrier: str
    translation_unit_vector: tuple[float, float]
    epsilon: Fraction
    post_translation_projected_center_distance: Fraction
    minimum_ribbon_clearance_during_isotopy: Fraction
    linking_number: int = 0

    @property
    def pair_id(self) -> str:
        return f"{self.left}::{self.right}"

    def as_dict(self) -> dict[str, object]:
        return {"pair_id": self.pair_id, "moved_carrier": self.moved_carrier, "translation_unit_vector_binary64": list(self.translation_unit_vector), "translation_epsilon": fraction_text(self.epsilon), "post_translation_projected_center_distance": fraction_text(self.post_translation_projected_center_distance), "minimum_ribbon_clearance_during_isotopy": fraction_text(self.minimum_ribbon_clearance_during_isotopy), "regularized_projection_crossings": 0, "linking_number": self.linking_number, "standing": "pair-specific outward translation; linking number is invariant because the complete ribbon remains disjoint throughout"}


def _tangent_regularizations(ribbon: SmoothPrimeRibbon) -> tuple[TangentRegularization, ...]:
    centers = ribbon.centers()
    result = []
    for left, right, distance_squared in ribbon.base.primitive.pair_distance_squared:
        if distance_squared != 4:
            continue
        vector_x = (centers[left][0] - centers[right][0]) / 2.0
        vector_y = (centers[left][1] - centers[right][1]) / 2.0
        norm = math.hypot(vector_x, vector_y)
        if abs(norm - 1.0) > 1e-12:
            raise SmoothRibbonError("tangent center vector is not unit after halving")
        clearance = RIBBON_SEPARATION_LOWER_BOUND - TANGENT_REGULARIZATION_EPSILON
        result.append(TangentRegularization(left, right, left, (vector_x / norm, vector_y / norm), TANGENT_REGULARIZATION_EPSILON, Fraction(2) + TANGENT_REGULARIZATION_EPSILON, clearance))
    return tuple(result)


def _integer_rank(matrix: Sequence[Sequence[int]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    rank = 0
    for column in range(columns):
        pivot = next((index for index in range(rank, rows) if work[index][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for index in range(rows):
            if index == rank or not work[index][column]:
                continue
            factor = work[index][column]
            work[index] = [value - factor * pivot_entry for value, pivot_entry in zip(work[index], work[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def _bareiss_determinant(matrix: Sequence[Sequence[int]]) -> int:
    size = len(matrix)
    if not size:
        return 1
    work = [list(map(int, row)) for row in matrix]
    sign = previous = 1
    for pivot_index in range(size - 1):
        if work[pivot_index][pivot_index] == 0:
            swap = next((index for index in range(pivot_index + 1, size) if work[index][pivot_index]), None)
            if swap is None:
                return 0
            work[pivot_index], work[swap] = work[swap], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                work[row][column] = (work[row][column] * pivot - work[row][pivot_index] * work[pivot_index][column]) // previous
        previous = pivot
    return sign * work[-1][-1]


def _component_count(vertices: Sequence[str], edges: Sequence[tuple[str, str]]) -> int:
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = set()
    components = 0
    for start in vertices:
        if start in seen:
            continue
        components += 1
        pending = [start]
        while pending:
            vertex = pending.pop()
            if vertex in seen:
                continue
            seen.add(vertex)
            pending.extend(adjacency[vertex] - seen)
    return components


@dataclass(frozen=True, slots=True)
class LinkingMatrixCertificate:
    carrier_order: tuple[str, ...]
    matrix: tuple[tuple[int, ...], ...]
    regularized_tangent_pairs: tuple[str, ...]
    rank: int
    nullity: int
    determinant: int
    value_counts: Mapping[str, int]
    nonzero_edge_count: int
    nonzero_component_count: int
    nonzero_cycle_rank: int

    def as_dict(self) -> dict[str, object]:
        return {"carrier_order": list(self.carrier_order), "matrix": [list(row) for row in self.matrix], "regularized_tangent_pairs": list(self.regularized_tangent_pairs), "pair_value_counts": dict(self.value_counts), "rank_over_Q": self.rank, "nullity_over_Q": self.nullity, "determinant": self.determinant, "nonzero_link_graph": {"edge_count": self.nonzero_edge_count, "component_count": self.nonzero_component_count, "cycle_rank": self.nonzero_cycle_rank}, "orientation_boundary": "reorienting a component conjugates the matrix by a diagonal sign matrix; rank, nullity, determinant, and zero pattern remain invariant"}


def _linking_matrix(ribbon: SmoothPrimeRibbon, tangent_regularizations: Sequence[TangentRegularization]) -> LinkingMatrixCertificate:
    carriers = ribbon.carriers
    index = {carrier: position for position, carrier in enumerate(carriers)}
    tangent_ids = {item.pair_id for item in tangent_regularizations}
    matrix = [[0] * len(carriers) for _ in carriers]
    values = []
    for readout in ribbon.base.pair_readouts:
        pair_id = f"{readout.left}::{readout.right}"
        value = 0 if readout.linking_number is None and pair_id in tangent_ids else readout.linking_number
        if value is None:
            raise SmoothRibbonError(f"unregularized tangent pair {pair_id}")
        left_index, right_index = index[readout.left], index[readout.right]
        matrix[left_index][right_index] = matrix[right_index][left_index] = value
        values.append(value)
    rank = _integer_rank(matrix)
    nonzero_edges = [(carriers[left], carriers[right]) for left in range(len(carriers)) for right in range(left + 1, len(carriers)) if matrix[left][right]]
    components = _component_count(carriers, nonzero_edges)
    return LinkingMatrixCertificate(carriers, tuple(tuple(row) for row in matrix), tuple(sorted(tangent_ids)), rank, len(carriers) - rank, _bareiss_determinant(matrix), {str(value): values.count(value) for value in sorted(set(values))}, len(nonzero_edges), components, len(nonzero_edges) - len(carriers) + components)


@dataclass(frozen=True, slots=True)
class SmoothRibbonCertificate:
    ribbon: SmoothPrimeRibbon
    pair_certificates: tuple[PairSeparationCertificate, ...]
    tangent_regularizations: tuple[TangentRegularization, ...]
    linking_matrix: LinkingMatrixCertificate

    @property
    def minimum_leaf_lower_bound(self) -> float:
        return min(item.minimum_leaf_lower_bound for item in self.pair_certificates)

    @property
    def total_boxes_evaluated(self) -> int:
        return sum(item.boxes_evaluated for item in self.pair_certificates)

    @property
    def maximum_subdivision_depth(self) -> int:
        return max(item.maximum_depth for item in self.pair_certificates)

    @property
    def payload(self) -> dict[str, object]:
        payload = {
            "schema_id": SCHEMA_ID,
            "schema_version": SCHEMA_VERSION,
            "authority": "Erin Spencer",
            "recorded_on": "2026-08-11",
            "selection_effect": "none",
            "prime": self.ribbon.prime,
            "source": {"name": SOURCE_NAME, "sha256": SOURCE_SHA256, "line_basis": list(SOURCE_LINES)},
            "smooth_realization": self.ribbon.as_dict(),
            "global_separation": {"standing": "deterministic binary64 Lipschitz subdivision with declared roundoff buffer; not formal interval arithmetic", "parameter_domain_per_pair": "[0,1] x [0,1]", "pair_count": len(self.pair_certificates), "centerline_separation_target": fraction_text(CENTERLINE_SEPARATION_TARGET), "all_pairs_certified": all(item.certified for item in self.pair_certificates), "minimum_leaf_lower_bound_binary64": self.minimum_leaf_lower_bound, "total_boxes_evaluated": self.total_boxes_evaluated, "maximum_subdivision_depth": self.maximum_subdivision_depth, "roundoff_buffer": ROUND_OFF_BUFFER, "ribbon_half_width": fraction_text(HALF_WIDTH), "global_finite_width_ribbon_separation_lower_bound": fraction_text(RIBBON_SEPARATION_LOWER_BOUND), "triangle_inequality": "d(ribbon_i,ribbon_j) >= d(centerline_i,centerline_j)-2*w", "pair_certificates": [item.as_dict() for item in self.pair_certificates]},
            "tangent_regularization": {"epsilon": fraction_text(TANGENT_REGULARIZATION_EPSILON), "pair_count": len(self.tangent_regularizations), "pairs": [item.as_dict() for item in self.tangent_regularizations]},
            "complete_pairwise_linking_matrix": self.linking_matrix.as_dict(),
            "event_semantics": {"projected_coincidences": "retained", "strict_braid_order": "retained", "physical_centerline_contacts_claimed": 0, "physical_boundary_contacts_claimed": 0},
            "unresolved": ["formal interval or proof-assistant replay of the global separation certificate", "ambient-isotopy classification of the whole multi-ribbon link", "higher-order invariants not determined by pairwise linking numbers", "boundary-component link invariants", "spectral operator and prime-power law", "zeta-zero correspondence"],
            "nonclaims": ["not a redefinition of arithmetic primality", "not an established electron ontology or Pauli-exclusion derivation", "not a complete link classification", "not a zeta-function theorem or proof of the Riemann hypothesis", "not EDCM or METAPAT validity"],
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        payload["payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return payload

    def json_text(self, *, indent: int = 2) -> str:
        return json.dumps(self.payload, indent=indent, sort_keys=True, ensure_ascii=False) + "\n"


def _build_smooth(base: PrimePhaseLiftCandidate) -> SmoothPrimeRibbon:
    ribbon = SmoothPrimeRibbon(base, tuple(SmoothPeriodicField.from_candidate(base, carrier) for carrier in base.carriers))
    if ribbon.maximum_event_height_residual != 0.0:
        raise SmoothRibbonError("smooth field did not preserve event heights")
    one_turn, two_turn = ribbon.seam_residuals()
    if one_turn > 3e-12 or two_turn > 3e-12:
        raise SmoothRibbonError("smoothed Möbius return residual exceeded tolerance")
    return ribbon


@lru_cache(maxsize=None)
def build_smooth_prime_seven() -> SmoothPrimeRibbon:
    return _build_smooth(build_prime_seven_phase_lift())


@lru_cache(maxsize=None)
def build_smooth_prime_five() -> SmoothPrimeRibbon:
    return _build_smooth(build_prime_five_phase_lift())


def _certify(ribbon: SmoothPrimeRibbon) -> SmoothRibbonCertificate:
    pair_certificates = tuple(_certify_pair_separation(ribbon, left, right) for left, right in itertools.combinations(ribbon.carriers, 2))
    tangent_regularizations = _tangent_regularizations(ribbon)
    certificate = SmoothRibbonCertificate(ribbon, pair_certificates, tangent_regularizations, _linking_matrix(ribbon, tangent_regularizations))
    if certificate.minimum_leaf_lower_bound <= float(CENTERLINE_SEPARATION_TARGET):
        raise SmoothRibbonError("global centerline target not certified")
    return certificate


@lru_cache(maxsize=None)
def certify_smooth_prime_seven() -> SmoothRibbonCertificate:
    return _certify(build_smooth_prime_seven())


@lru_cache(maxsize=None)
def certify_smooth_prime_five() -> SmoothRibbonCertificate:
    certify_smooth_prime_seven()
    return _certify(build_smooth_prime_five())


def smooth_ribbon_family_certificate() -> dict[str, object]:
    p7 = certify_smooth_prime_seven()
    p5 = certify_smooth_prime_five()
    payload = {
        "schema_id": f"{SCHEMA_ID}.family",
        "schema_version": SCHEMA_VERSION,
        "authority": "Erin Spencer",
        "recorded_on": "2026-08-11",
        "selection_effect": "none",
        "research_order": [7, 5],
        "source": {"name": SOURCE_NAME, "sha256": SOURCE_SHA256, "line_basis": list(SOURCE_LINES)},
        "p7": p7.payload,
        "p5": p5.payload,
        "comparison": {"same_protocol": True, "centerline_target": fraction_text(CENTERLINE_SEPARATION_TARGET), "finite_width_ribbon_lower_bound": fraction_text(RIBBON_SEPARATION_LOWER_BOUND), "p7_linking_matrix_rank": p7.linking_matrix.rank, "p5_linking_matrix_rank": p5.linking_matrix.rank, "p7_nonzero_link_pairs": p7.linking_matrix.nonzero_edge_count, "p5_nonzero_link_pairs": p5.linking_matrix.nonzero_edge_count, "standing": "two independently constructed prime candidates; P5 is not obtained by deleting P7 carriers"},
        "next": ["replay the separation proof with rigorous interval arithmetic or a proof assistant", "compute higher-order link invariants beyond the complete pairwise linking matrix", "derive boundary-component link invariants and whole-link ambient isotopy", "only then define a spectral operator"],
        "nonclaims": ["no arithmetic redefinition", "no electron ontology", "no complete link classification", "no zeta theorem", "no proof of the Riemann hypothesis"],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    payload["payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload


def write_smooth_ribbon_family_certificate(path: str | Path, *, indent: int = 2) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(smooth_ribbon_family_certificate(), indent=indent, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return output


def render_smooth_centerline_obj(ribbon: SmoothPrimeRibbon, *, samples_per_carrier: int = 720) -> str:
    if isinstance(samples_per_carrier, bool) or samples_per_carrier < 24:
        raise SmoothRibbonError("samples_per_carrier must be an integer >= 24")
    certificate = certify_smooth_prime_seven() if ribbon.prime == 7 else certify_smooth_prime_five()
    lines = [f"# UCNS P{ribbon.prime} C-infinity lifted centerlines", f"# smooth_payload_sha256 {certificate.payload['payload_sha256']}"]
    vertex_index = 1
    for carrier in ribbon.carriers:
        start = vertex_index
        for index in range(samples_per_carrier):
            point = ribbon.centerline_point(carrier, Fraction(index, samples_per_carrier))
            lines.append("v " + " ".join(f"{coordinate:.12f}" for coordinate in point))
            vertex_index += 1
        lines.append("l " + " ".join(map(str, list(range(start, vertex_index)) + [start])))
    return "\n".join(lines) + "\n"


def render_smooth_ribbon_obj(ribbon: SmoothPrimeRibbon, *, turn_samples: int = 360, breadth_segments: int = 6) -> str:
    if isinstance(turn_samples, bool) or turn_samples < 24:
        raise SmoothRibbonError("turn_samples must be an integer >= 24")
    if isinstance(breadth_segments, bool) or breadth_segments < 1:
        raise SmoothRibbonError("breadth_segments must be an integer >= 1")
    certificate = certify_smooth_prime_seven() if ribbon.prime == 7 else certify_smooth_prime_five()
    lines = [f"# UCNS P{ribbon.prime} globally separated C-infinity Möbius ribbons", f"# certified ribbon separation lower bound {fraction_text(RIBBON_SEPARATION_LOWER_BOUND)}", f"# smooth_payload_sha256 {certificate.payload['payload_sha256']}"]
    columns = breadth_segments + 1
    vertex_base = 1
    for carrier in ribbon.carriers:
        lines.append(f"o P{ribbon.prime}_{carrier}")
        for turn_index in range(turn_samples):
            turn = Fraction(turn_index, turn_samples)
            for breadth_index in range(columns):
                breadth = -ribbon.half_width + 2 * ribbon.half_width * Fraction(breadth_index, breadth_segments)
                lines.append("v " + " ".join(f"{coordinate:.12f}" for coordinate in ribbon.surface_point(carrier, turn, breadth)))
        for turn_index in range(turn_samples):
            next_turn = (turn_index + 1) % turn_samples
            for breadth_index in range(breadth_segments):
                left_a = vertex_base + turn_index * columns + breadth_index
                left_b = left_a + 1
                if next_turn == 0:
                    right_a = vertex_base + breadth_segments - breadth_index
                    right_b = right_a - 1
                else:
                    right_a = vertex_base + next_turn * columns + breadth_index
                    right_b = right_a + 1
                lines.append(f"f {left_a} {right_a} {right_b} {left_b}")
        vertex_base += turn_samples * columns
    return "\n".join(lines) + "\n"
