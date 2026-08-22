# === MODULE_BUILD ===
# id: ucns_prime_interval_boundaries_p7_p5
#   module_name: prime_interval_boundaries
#   module_kind: experiment
#   summary: replays the P7-first smooth-ribbon separation certificate with outward interval endpoints, extracts each Möbius strip's single two-turn boundary curve, and derives exact boundary-cable and mixed core-boundary invariants before P5 comparison
#   owner: Erin Spencer
#   public_surface: IntervalPairReplay, IntervalReplayCertificate, BoundaryComponentCertificate, BoundaryInvariantCertificate, replay_prime_seven_intervals, replay_prime_five_intervals, certify_prime_seven_boundaries, certify_prime_five_boundaries, interval_boundary_family_certificate, write_interval_boundary_family_certificate, render_boundary_obj, render_core_boundary_obj
#   internal_surface: recovered legacy types and payloads over readable PR 181 interval and boundary certificates
#   auth_boundary: none
#   storage_boundary: caller-supplied local paths only through writer functions
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_interval_boundaries.py
#   rollout: P7 first, P5 same-protocol comparison second; selection effect none; does not alter prior smooth-ribbon receipts
#   rollback: remove this module, its test, documentation, generated certificate, and boundary exports
#   requires: ucns_prime_smooth_ribbons_p7_p5, mpmath>=1.3
#   since: 2026-08-11
#   unresolved: independently verified interval kernel, proof-assistant replay, Milnor invariants of algebraically split triples, multivariable Alexander polynomial of the complete boundary link, ambient isotopy, spectral operator, prime-power law, zeta correspondence
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: prime_interval_replay_uses_outward_endpoints
#   given: every complete pair-parameter torus is recursively covered
#   then: high-precision interval point values and interval speed majorants certify the same nine-hundredths centerline target without a binary64 subtraction heuristic
#   class: evidence
#   since: 2026-08-11
#
# id: prime_boundary_curve_is_single_two_turn_component
#   given: one finite-width Möbius ribbon is restricted to positive half-width
#   then: its boundary closes only after two carrier turns and retracts with longitudinal degree two
#   class: correctness
#   since: 2026-08-11
#
# id: prime_boundary_cable_winding_is_derived_from_phase
#   given: the selected phase law is evaluated over the two-turn boundary traversal
#   then: the center boundary has cable class two-seven and each outer boundary has cable class two-one in the declared framing
#   class: correctness
#   since: 2026-08-11
#
# id: prime_boundary_linking_scales_by_four
#   given: boundary components retract to degree-two traversals of their cores inside pairwise-disjoint ribbons
#   then: every inter-ribbon boundary linking number is four times the corresponding core linking number
#   class: correctness
#   since: 2026-08-11
#
# id: prime_mixed_core_boundary_matrix_is_complete
#   given: core-core, core-boundary, and boundary-boundary linking laws are combined
#   then: a complete two-p by two-p integer matrix and exact rank and determinant are issued
#   class: evidence
#   since: 2026-08-11
#
# id: prime_higher_order_boundary_is_explicit
#   given: triples of boundary components are classified by pairwise support
#   then: algebraically split triples are enumerated while Milnor and complete-link invariants remain explicitly unresolved
#   class: doctrine
#   since: 2026-08-11
#
# id: prime_interval_boundaries_p7_precedes_p5
#   given: the family certificate is built
#   then: P7 interval and boundary invariants are completed before the same protocol is applied independently to P5
#   class: doctrine
#   since: 2026-08-11
#
# id: prime_interval_boundary_compact_receipt_is_nonselecting
#   given: the family receipt is serialized
#   then: it records the interval-kernel boundary and claims no arithmetic redefinition, electron ontology, zeta theorem, or Riemann-hypothesis proof
#   class: doctrine
#   since: 2026-08-11
# === END CONTRACTS ===

"""Outward interval replay and Möbius-boundary invariants for P7 first.

The preceding smooth-ribbon artifact used deterministic binary64 Lipschitz
subdivision with a declared guard.  This module replays the same subdivision
using ``mpmath.iv`` point intervals and interval speed majorants at 80 decimal
digits.  Exact rational boxes drive the recursion; accepted lower endpoints are
outward interval endpoints rather than guarded binary64 samples.

Each Möbius strip has one boundary component.  In the declared parameterization
that boundary is ``B_i(t)=X_i(t,w)`` for ``0<=t<2``.  Retraction to the core has
longitudinal degree two.  The meridional winding is ``1+2*omega_i`` where
``omega_i`` is the integer phase winding.  Hence the selected center boundary
is a ``(2,7)`` cable and each outer boundary is a ``(2,1)`` cable.

The interval backend is computer-assisted evidence.  It is not an independently
verified interval kernel or proof-assistant replay.
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
from typing import Iterable, Mapping, Sequence

import mpmath
from mpmath import iv

from .prime_smooth_ribbons import (
    CENTERLINE_SEPARATION_TARGET,
    HALF_WIDTH,
    RIBBON_SEPARATION_LOWER_BOUND,
    SmoothPrimeRibbon,
    build_smooth_prime_five,
    build_smooth_prime_seven,
    certify_smooth_prime_five,
    certify_smooth_prime_seven,
)
from .prime_interval_replay import (
    IntervalPairCertificate as ReadableIntervalPairCertificate,
    IntervalSeparationCertificate as ReadableIntervalSeparationCertificate,
    replay_interval_separation,
)
from .prime_boundary_link_invariants import (
    BoundaryComponentInvariant as ReadableBoundaryComponentInvariant,
    build_boundary_link_certificate,
)

SCHEMA_ID = "ucns.prime-interval-boundaries"
SCHEMA_VERSION = "0.1.0"
SOURCE_NAME = "Möbius Strips and Quantum Geometry.txt"
SOURCE_SHA256 = "dc3a94ca5070ffff8f2a246f48db77192b08f521e721bc7c2a011aa05ddeb9a1"
SOURCE_LINES = (5, 6, 13, 14, 15, 16, 17)
INTERVAL_DPS = 80
INTERVAL_BACKEND = "mpmath.iv"
INTERVAL_MAX_DEPTH = 28
INTERVAL_MAX_BOXES_PER_PAIR = 100_000
BOUNDARY_PERIOD_TURNS = Fraction(2)
RECOVERED_LEGACY_SOURCE_SHA256 = "6a79463856ea0171d7d29881fdb7e66780fab29779ff1c5fd1b71eaae7f9fc3c"


class IntervalBoundaryError(ValueError):
    """Raised when interval replay or boundary extraction leaves its boundary."""


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _iv_fraction(value: Fraction | int) -> object:
    item = value if isinstance(value, Fraction) else Fraction(value)
    return iv.mpf(item.numerator) / item.denominator


def _point_endpoint_text(value: object, *, lower: bool = True) -> str:
    endpoint = value.a if lower else value.b
    text = str(endpoint)
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1].split(",", 1)[0 if lower else -1].strip()
    return text


def _point_endpoint_float(value: object, *, lower: bool = True) -> float:
    return float(value.a if lower else value.b)


def _flat_step_point_interval(value: Fraction) -> object:
    if value <= 0:
        return iv.mpf(0)
    if value >= 1:
        return iv.mpf(1)
    x = _iv_fraction(value)
    left = iv.exp(-1 / x)
    right = iv.exp(-1 / (1 - x))
    return left / (left + right)


def _field_point_interval(ribbon: SmoothPrimeRibbon, carrier: str, turn: Fraction) -> object:
    field = ribbon.field(carrier)
    target = turn % 1
    for index, segment in enumerate(field.segments):
        adjusted = target
        if index == len(field.segments) - 1 and adjusted < segment.left_turn:
            adjusted += 1
        if segment.left_turn <= adjusted <= segment.right_turn:
            if adjusted == segment.left_turn:
                return _iv_fraction(segment.left_value)
            if adjusted == segment.right_turn:
                return _iv_fraction(segment.right_value)
            local = (adjusted - segment.left_turn) / segment.turn_width
            return (
                _iv_fraction(segment.left_value)
                + _iv_fraction(segment.right_value - segment.left_value)
                * _flat_step_point_interval(local)
            )
    raise AssertionError("interval field segment search failed")


def _exact_center(prime: int, carrier: str) -> tuple[object, object]:
    zero = _iv_fraction(0)
    one = _iv_fraction(1)
    half = _iv_fraction(Fraction(1, 2))
    if prime == 5:
        centers = {
            "C": (zero, zero),
            "R0": (one, zero),
            "R1": (zero, one),
            "R2": (-one, zero),
            "R3": (zero, -one),
        }
        return centers[carrier]
    if prime != 7:
        raise IntervalBoundaryError("only P7 and P5 are currently supported")
    root_three_half = iv.sqrt(_iv_fraction(3)) / 2
    centers = {
        "C": (zero, zero),
        "R0": (one, zero),
        "R1": (half, root_three_half),
        "R2": (-half, root_three_half),
        "R3": (-one, zero),
        "R4": (-half, -root_three_half),
        "R5": (half, -root_three_half),
    }
    return centers[carrier]


def _centerline_point_interval(
    ribbon: SmoothPrimeRibbon,
    carrier: str,
    turn: Fraction,
) -> tuple[object, object, object]:
    center_x, center_y = _exact_center(ribbon.prime, carrier)
    angle = 2 * iv.pi * _iv_fraction(turn)
    return (
        center_x + iv.cos(angle),
        center_y + iv.sin(angle),
        _field_point_interval(ribbon, carrier, turn),
    )


def _speed_interval(ribbon: SmoothPrimeRibbon, carrier: str) -> object:
    derivative = _iv_fraction(ribbon.field(carrier).maximum_derivative_bound)
    return iv.sqrt((2 * iv.pi) ** 2 + derivative**2)


def _distance_interval(
    left: Sequence[object],
    right: Sequence[object],
) -> object:
    return iv.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)))


@dataclass(frozen=True, slots=True)
class IntervalPairReplay:
    left: str
    right: str
    target: Fraction
    boxes_evaluated: int
    accepted_leaf_boxes: int
    maximum_depth: int
    minimum_lower_endpoint: str
    minimum_lower_endpoint_binary64: float
    leaf_ledger_sha256: str

    @property
    def pair_id(self) -> str:
        return f"{self.left}::{self.right}"

    @property
    def certified(self) -> bool:
        return self.minimum_lower_endpoint_binary64 > float(self.target)

    def as_dict(self) -> dict[str, object]:
        return {
            "pair_id": self.pair_id,
            "target": fraction_text(self.target),
            "certified": self.certified,
            "boxes_evaluated": self.boxes_evaluated,
            "accepted_leaf_boxes": self.accepted_leaf_boxes,
            "maximum_depth": self.maximum_depth,
            "minimum_outward_lower_endpoint": self.minimum_lower_endpoint,
            "minimum_outward_lower_endpoint_binary64_for_display": self.minimum_lower_endpoint_binary64,
            "accepted_leaf_ledger_sha256": self.leaf_ledger_sha256,
        }


def _replay_pair(
    ribbon: SmoothPrimeRibbon,
    left: str,
    right: str,
    *,
    target: Fraction = CENTERLINE_SEPARATION_TARGET,
) -> IntervalPairReplay:
    left_speed = _speed_interval(ribbon, left)
    right_speed = _speed_interval(ribbon, right)
    target_interval = _iv_fraction(target)
    pending: list[tuple[Fraction, Fraction, Fraction, Fraction, int]] = [
        (Fraction(0), Fraction(1), Fraction(0), Fraction(1), 0)
    ]
    boxes = 0
    leaves = 0
    maximum_depth = 0
    minimum_value: object | None = None
    digest = hashlib.sha256()

    while pending:
        left_a, left_b, right_a, right_b, depth = pending.pop()
        boxes += 1
        maximum_depth = max(maximum_depth, depth)
        if boxes > INTERVAL_MAX_BOXES_PER_PAIR:
            raise IntervalBoundaryError(f"interval replay exceeded box budget for {left}::{right}")
        left_mid = (left_a + left_b) / 2
        right_mid = (right_a + right_b) / 2
        sample_distance = _distance_interval(
            _centerline_point_interval(ribbon, left, left_mid),
            _centerline_point_interval(ribbon, right, right_mid),
        )
        radius = (
            left_speed * _iv_fraction((left_b - left_a) / 2)
            + right_speed * _iv_fraction((right_b - right_a) / 2)
        )
        lower_bound = sample_distance - radius
        if lower_bound.a > target_interval.b:
            leaves += 1
            if minimum_value is None or lower_bound.a < minimum_value.a:
                minimum_value = lower_bound
            row = "|".join(
                (
                    fraction_text(left_a),
                    fraction_text(left_b),
                    fraction_text(right_a),
                    fraction_text(right_b),
                    str(depth),
                    _point_endpoint_text(lower_bound),
                )
            )
            digest.update((row + "\n").encode("ascii"))
            continue
        if depth >= INTERVAL_MAX_DEPTH:
            raise IntervalBoundaryError(
                f"interval replay failed at depth {depth} for {left}::{right}"
            )
        left_contribution = left_speed.b * _iv_fraction(left_b - left_a)
        right_contribution = right_speed.b * _iv_fraction(right_b - right_a)
        if left_contribution >= right_contribution:
            midpoint = (left_a + left_b) / 2
            pending.append((left_a, midpoint, right_a, right_b, depth + 1))
            pending.append((midpoint, left_b, right_a, right_b, depth + 1))
        else:
            midpoint = (right_a + right_b) / 2
            pending.append((left_a, left_b, right_a, midpoint, depth + 1))
            pending.append((left_a, left_b, midpoint, right_b, depth + 1))

    if minimum_value is None:
        raise IntervalBoundaryError("interval replay produced no accepted leaves")
    return IntervalPairReplay(
        left=left,
        right=right,
        target=target,
        boxes_evaluated=boxes,
        accepted_leaf_boxes=leaves,
        maximum_depth=maximum_depth,
        minimum_lower_endpoint=_point_endpoint_text(minimum_value),
        minimum_lower_endpoint_binary64=_point_endpoint_float(minimum_value),
        leaf_ledger_sha256=digest.hexdigest(),
    )


@dataclass(frozen=True, slots=True)
class IntervalReplayCertificate:
    prime: int
    pair_replays: tuple[IntervalPairReplay, ...]

    @property
    def all_pairs_certified(self) -> bool:
        return all(item.certified for item in self.pair_replays)

    @property
    def total_boxes_evaluated(self) -> int:
        return sum(item.boxes_evaluated for item in self.pair_replays)

    @property
    def maximum_depth(self) -> int:
        return max(item.maximum_depth for item in self.pair_replays)

    @property
    def minimum_lower_endpoint_binary64(self) -> float:
        return min(item.minimum_lower_endpoint_binary64 for item in self.pair_replays)

    @property
    def global_leaf_ledger_sha256(self) -> str:
        digest = hashlib.sha256()
        for item in self.pair_replays:
            digest.update(f"{item.pair_id}:{item.leaf_ledger_sha256}\n".encode("ascii"))
        return digest.hexdigest()

    def as_dict(self) -> dict[str, object]:
        return {
            "prime": self.prime,
            "backend": {
                "name": INTERVAL_BACKEND,
                "mpmath_version": mpmath.__version__,
                "decimal_digits": INTERVAL_DPS,
                "standing": "outward interval endpoints; software kernel not independently verified",
            },
            "target": fraction_text(CENTERLINE_SEPARATION_TARGET),
            "all_pairs_certified": self.all_pairs_certified,
            "pair_count": len(self.pair_replays),
            "total_boxes_evaluated": self.total_boxes_evaluated,
            "maximum_depth": self.maximum_depth,
            "minimum_outward_lower_endpoint_binary64_for_display": self.minimum_lower_endpoint_binary64,
            "global_accepted_leaf_ledger_sha256": self.global_leaf_ledger_sha256,
            "pair_replays": [item.as_dict() for item in self.pair_replays],
            "finite_width_consequence": {
                "ribbon_half_width": fraction_text(HALF_WIDTH),
                "ribbon_separation_lower_bound": fraction_text(RIBBON_SEPARATION_LOWER_BOUND),
                "derivation": "centerline target minus two ribbon half-widths",
            },
            "compatibility": {
                "implementation": "readable PR #181 interval replay",
                "legacy_source_sha256": RECOVERED_LEGACY_SOURCE_SHA256,
                "ledger_digest": "adapter digest over readable pair certificates; not the legacy leaf ledger",
            },
        }


def _adapt_pair(item: ReadableIntervalPairCertificate) -> IntervalPairReplay:
    evidence = json.dumps(item.as_dict(), sort_keys=True, separators=(",", ":"))
    return IntervalPairReplay(
        left=item.left,
        right=item.right,
        target=item.target,
        boxes_evaluated=item.boxes_evaluated,
        accepted_leaf_boxes=item.certified_leaf_boxes,
        maximum_depth=item.maximum_depth,
        minimum_lower_endpoint=item.minimum_leaf_lower_bound_decimal,
        minimum_lower_endpoint_binary64=item.minimum_leaf_lower_bound,
        leaf_ledger_sha256=hashlib.sha256(("pr181-adapter:" + evidence).encode("utf-8")).hexdigest(),
    )


def _adapt_replay(readable: ReadableIntervalSeparationCertificate) -> IntervalReplayCertificate:
    certificate = IntervalReplayCertificate(
        readable.prime,
        tuple(_adapt_pair(item) for item in readable.pair_certificates),
    )
    if not certificate.all_pairs_certified:
        raise IntervalBoundaryError("not every pair was interval-certified")
    return certificate


@lru_cache(maxsize=1)
def replay_prime_seven_intervals() -> IntervalReplayCertificate:
    return _adapt_replay(replay_interval_separation(build_smooth_prime_seven()))


@lru_cache(maxsize=1)
def replay_prime_five_intervals() -> IntervalReplayCertificate:
    return _adapt_replay(replay_interval_separation(build_smooth_prime_five()))


def _integer_rank(matrix: Sequence[Sequence[int]]) -> int:
    rows = [[Fraction(value) for value in row] for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    column_count = len(rows[0])
    rank = 0
    for column in range(column_count):
        pivot = next((index for index in range(rank, row_count) if rows[index][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [value / pivot_value for value in rows[rank]]
        for index in range(row_count):
            if index == rank or rows[index][column] == 0:
                continue
            factor = rows[index][column]
            rows[index] = [a - factor * b for a, b in zip(rows[index], rows[rank])]
        rank += 1
        if rank == row_count:
            break
    return rank


def _bareiss_determinant(matrix: Sequence[Sequence[int]]) -> int:
    values = [list(map(int, row)) for row in matrix]
    size = len(values)
    if any(len(row) != size for row in values):
        raise IntervalBoundaryError("determinant requires a square matrix")
    if size == 0:
        return 1
    sign = 1
    denominator = 1
    for pivot_index in range(size - 1):
        pivot_row = next(
            (row for row in range(pivot_index, size) if values[row][pivot_index]),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            values[pivot_index], values[pivot_row] = values[pivot_row], values[pivot_index]
            sign *= -1
        pivot = values[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = values[row][column] * pivot - values[row][pivot_index] * values[pivot_index][column]
                if numerator % denominator:
                    raise IntervalBoundaryError("Bareiss division was not exact")
                values[row][column] = numerator // denominator
        denominator = pivot
        for row in range(pivot_index + 1, size):
            values[row][pivot_index] = 0
    return sign * values[-1][-1]


def _factor_integer(value: int) -> dict[str, int]:
    number = abs(int(value))
    factors: dict[str, int] = {}
    divisor = 2
    while divisor * divisor <= number:
        while number % divisor == 0:
            factors[str(divisor)] = factors.get(str(divisor), 0) + 1
            number //= divisor
        divisor += 1 if divisor == 2 else 2
    if number > 1:
        factors[str(number)] = factors.get(str(number), 0) + 1
    return factors


def _matrix_value_counts(matrix: Sequence[Sequence[int]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row_index, row in enumerate(matrix):
        for column_index in range(row_index + 1, len(row)):
            key = str(row[column_index])
            counts[key] = counts.get(key, 0) + 1
    return {key: counts[key] for key in sorted(counts, key=int)}


def _alexander_torus_two_q(q: int) -> str:
    q = abs(int(q))
    if q == 1:
        return "1"
    genus = (q - 1) // 2
    pieces: list[str] = []
    sign = 1
    for exponent in range(genus, -genus - 1, -1):
        term = (
            "1"
            if exponent == 0
            else "t"
            if exponent == 1
            else "t^-1"
            if exponent == -1
            else f"t^{exponent}"
        )
        if not pieces:
            pieces.append(term if sign > 0 else f"-{term}")
        else:
            pieces.append((" + " if sign > 0 else " - ") + term)
        sign *= -1
    return "".join(pieces)


@dataclass(frozen=True, slots=True)
class BoundaryComponentCertificate:
    carrier: str
    longitudinal_degree: int
    meridional_degree: int
    natural_core_boundary_linking: int
    knot_type: str
    alexander_polynomial: str
    determinant: int
    seifert_genus: int
    crossing_number: int
    is_unknot: bool

    def as_dict(self) -> dict[str, object]:
        return {
            "carrier": self.carrier,
            "boundary_period_turns": fraction_text(BOUNDARY_PERIOD_TURNS),
            "cable_class": [self.longitudinal_degree, self.meridional_degree],
            "natural_orientation_core_boundary_linking": self.natural_core_boundary_linking,
            "knot_type_in_declared_ribbon_framing": self.knot_type,
            "is_unknot": self.is_unknot,
            "alexander_polynomial": self.alexander_polynomial,
            "determinant": self.determinant,
            "seifert_genus": self.seifert_genus,
            "crossing_number": self.crossing_number,
        }


def _boundary_component(ribbon: SmoothPrimeRibbon, carrier: str) -> BoundaryComponentCertificate:
    winding = ribbon.base.phase_law.center_winding if carrier == "C" else 0
    meridional = 1 + 2 * winding
    is_unknot = abs(meridional) == 1
    return BoundaryComponentCertificate(
        carrier=carrier,
        longitudinal_degree=2,
        meridional_degree=meridional,
        natural_core_boundary_linking=-meridional,
        knot_type=f"T(2,{meridional})",
        alexander_polynomial=_alexander_torus_two_q(meridional),
        determinant=abs(meridional),
        seifert_genus=(abs(meridional) - 1) // 2,
        crossing_number=0 if is_unknot else abs(meridional),
        is_unknot=is_unknot,
    )


def _adapt_boundary_component(
    item: ReadableBoundaryComponentInvariant,
) -> BoundaryComponentCertificate:
    """Translate the recovered legacy orientation and field names explicitly."""
    return BoundaryComponentCertificate(
        carrier=item.carrier,
        longitudinal_degree=item.longitudinal_winding,
        meridional_degree=item.meridional_winding,
        natural_core_boundary_linking=-item.core_boundary_linking,
        knot_type=f"T(2,{item.meridional_winding})",
        alexander_polynomial=_alexander_torus_two_q(item.meridional_winding),
        determinant=item.determinant,
        seifert_genus=item.genus,
        crossing_number=item.crossing_number,
        is_unknot=abs(item.meridional_winding) == 1,
    )


def _scaled_matrix(matrix: Sequence[Sequence[int]], scale: int) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(scale * int(value) for value in row) for row in matrix)


def _mixed_matrix(
    core_matrix: Sequence[Sequence[int]],
    components: Sequence[BoundaryComponentCertificate],
) -> tuple[tuple[int, ...], ...]:
    size = len(core_matrix)
    cross = []
    for row in range(size):
        cross.append(
            [
                components[row].natural_core_boundary_linking
                if row == column
                else 2 * int(core_matrix[row][column])
                for column in range(size)
            ]
        )
    boundary = _scaled_matrix(core_matrix, 4)
    full = []
    for row in range(size):
        full.append(tuple(int(value) for value in core_matrix[row]) + tuple(cross[row]))
    for row in range(size):
        full.append(tuple(cross[column][row] for column in range(size)) + tuple(boundary[row]))
    return tuple(full)


def _triple_census(
    order: Sequence[str],
    matrix: Sequence[Sequence[int]],
) -> dict[str, object]:
    support_counts = {0: 0, 1: 0, 2: 0, 3: 0}
    algebraically_split: list[tuple[str, str, str]] = []
    for indices in itertools.combinations(range(len(order)), 3):
        support = sum(
            matrix[left][right] != 0
            for left, right in itertools.combinations(indices, 2)
        )
        support_counts[support] += 1
        if support == 0:
            algebraically_split.append(tuple(order[index] for index in indices))
    return {
        "pairwise_nonzero_edge_count_distribution": {
            str(key): support_counts[key] for key in sorted(support_counts)
        },
        "algebraically_split_triple_count": len(algebraically_split),
        "algebraically_split_triples": [list(item) for item in algebraically_split],
        "milnor_mu123_standing": (
            "not computed; these triples are the exact candidates for a link-group or C-complex calculation"
        ),
    }


@dataclass(frozen=True, slots=True)
class BoundaryInvariantCertificate:
    prime: int
    carrier_order: tuple[str, ...]
    components: tuple[BoundaryComponentCertificate, ...]
    core_linking_matrix: tuple[tuple[int, ...], ...]
    boundary_linking_matrix: tuple[tuple[int, ...], ...]
    mixed_core_boundary_matrix: tuple[tuple[int, ...], ...]
    interval_replay: IntervalReplayCertificate

    @property
    def boundary_rank(self) -> int:
        return _integer_rank(self.boundary_linking_matrix)

    @property
    def boundary_nullity(self) -> int:
        return len(self.boundary_linking_matrix) - self.boundary_rank

    @property
    def boundary_determinant(self) -> int:
        return _bareiss_determinant(self.boundary_linking_matrix)

    @property
    def mixed_rank(self) -> int:
        return _integer_rank(self.mixed_core_boundary_matrix)

    @property
    def mixed_nullity(self) -> int:
        return len(self.mixed_core_boundary_matrix) - self.mixed_rank

    @property
    def mixed_determinant(self) -> int:
        return _bareiss_determinant(self.mixed_core_boundary_matrix)

    @property
    def payload(self) -> dict[str, object]:
        result: dict[str, object] = {
            "prime": self.prime,
            "carrier_order": list(self.carrier_order),
            "interval_replay": self.interval_replay.as_dict(),
            "boundary_extraction": {
                "boundary_components": self.prime,
                "one_component_per_mobius_ribbon": True,
                "parameterization": "B_i(t)=X_i(t,+w), 0<=t<2",
                "one_turn_relation": "B_i(t+1)=X_i(t,-w)",
                "two_turn_closure": "B_i(t+2)=B_i(t)",
                "components": [item.as_dict() for item in self.components],
            },
            "boundary_linking": {
                "theorem": "[B_i]=2[C_i] in the complement of every other disjoint ribbon, so lk(B_i,B_j)=4*lk(C_i,C_j)",
                "matrix": [list(row) for row in self.boundary_linking_matrix],
                "value_counts": _matrix_value_counts(self.boundary_linking_matrix),
                "rank_over_Q": self.boundary_rank,
                "nullity_over_Q": self.boundary_nullity,
                "determinant": self.boundary_determinant,
                "technical_boundary_link_status": (
                    "not a boundary link in the knot-theoretic sense because some pairwise linking numbers are nonzero"
                ),
            },
            "mixed_core_boundary_link": {
                "component_order": [
                    *(f"core:{item}" for item in self.carrier_order),
                    *(f"boundary:{item}" for item in self.carrier_order),
                ],
                "orientation_convention": (
                    "core and boundary parameters increase; self core-boundary links are -(1+2*phase winding)"
                ),
                "off_diagonal_laws": {
                    "core_i_boundary_j": "2*lk(core_i,core_j), i!=j",
                    "boundary_i_boundary_j": "4*lk(core_i,core_j), i!=j",
                },
                "matrix": [list(row) for row in self.mixed_core_boundary_matrix],
                "rank_over_Q": self.mixed_rank,
                "nullity_over_Q": self.mixed_nullity,
                "determinant": self.mixed_determinant,
                "absolute_determinant_factorization": _factor_integer(self.mixed_determinant),
            },
            "higher_order_boundary": _triple_census(
                self.carrier_order,
                self.boundary_linking_matrix,
            ),
            "compatibility": {
                "implementation": "readable PR #181 boundary-link certificate",
                "legacy_source_sha256": RECOVERED_LEGACY_SOURCE_SHA256,
                "orientation_adapter": "legacy own-core linking is the negative of the readable certificate convention",
            },
            "nonclaims": [
                "not an independently verified interval kernel or proof-assistant replay",
                "not a computation of Milnor triple invariants",
                "not a multivariable Alexander polynomial of the complete boundary link",
                "not a complete ambient-isotopy classification",
                "not an arithmetic redefinition of primality",
                "not an electron ontology or Pauli-exclusion derivation",
                "not a spectral operator, prime-power law, zeta-zero correspondence, or proof of the Riemann hypothesis",
            ],
        }
        canonical = json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        result["payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return result


def _certify_boundaries(
    ribbon: SmoothPrimeRibbon,
    interval_replay: IntervalReplayCertificate,
) -> BoundaryInvariantCertificate:
    readable = build_boundary_link_certificate(ribbon)
    core = readable.core_matrix.matrix
    components = tuple(_adapt_boundary_component(item) for item in readable.components)
    boundary = readable.boundary_matrix.matrix
    mixed = _mixed_matrix(core, components)
    certificate = BoundaryInvariantCertificate(
        prime=ribbon.prime,
        carrier_order=ribbon.carriers,
        components=components,
        core_linking_matrix=core,
        boundary_linking_matrix=boundary,
        mixed_core_boundary_matrix=mixed,
        interval_replay=interval_replay,
    )
    if certificate.mixed_rank != 2 * ribbon.prime:
        raise IntervalBoundaryError("mixed core-boundary matrix unexpectedly singular")
    return certificate


@lru_cache(maxsize=1)
def certify_prime_seven_boundaries() -> BoundaryInvariantCertificate:
    return _certify_boundaries(
        build_smooth_prime_seven(),
        replay_prime_seven_intervals(),
    )


@lru_cache(maxsize=1)
def certify_prime_five_boundaries() -> BoundaryInvariantCertificate:
    return _certify_boundaries(
        build_smooth_prime_five(),
        replay_prime_five_intervals(),
    )


@lru_cache(maxsize=1)
def interval_boundary_family_certificate() -> dict[str, object]:
    p7 = certify_prime_seven_boundaries()
    p5 = certify_prime_five_boundaries()
    result: dict[str, object] = {
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
        "p7": p7.payload,
        "p5": p5.payload,
        "comparison": {
            "same_protocol": True,
            "p7_center_boundary_knot": p7.components[0].knot_type,
            "p5_center_boundary_knot": p5.components[0].knot_type,
            "p7_boundary_link_rank": p7.boundary_rank,
            "p5_boundary_link_rank": p5.boundary_rank,
            "p7_mixed_absolute_determinant": abs(p7.mixed_determinant),
            "p5_mixed_absolute_determinant": abs(p5.mixed_determinant),
            "standing": "P5 is independently reconstructed and processed only after P7",
        },
        "next": [
            "replay the interval certificate in an independently verified kernel or proof assistant",
            "compute Milnor invariants for the enumerated algebraically split triples",
            "compute a multivariable Alexander or equivalent complete-link invariant",
            "only then define a spectral object",
        ],
        "nonclaims": [
            "no arithmetic redefinition",
            "no complete ambient-isotopy classification",
            "no zeta theorem",
            "no proof of the Riemann hypothesis",
        ],
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    result["payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return result


def write_interval_boundary_family_certificate(
    path: str | Path,
    *,
    indent: int = 2,
) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            interval_boundary_family_certificate(),
            indent=indent,
            sort_keys=True,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return output


def render_boundary_obj(
    ribbon: SmoothPrimeRibbon,
    *,
    samples_per_boundary: int = 512,
) -> str:
    if isinstance(samples_per_boundary, bool) or samples_per_boundary < 32:
        raise IntervalBoundaryError("samples_per_boundary must be an integer >= 32")
    lines = [
        f"# P{ribbon.prime} continuous Möbius boundary curves",
        "# one boundary component per ribbon; each uses a two-turn parameter domain",
        f"# interval-derived ribbon separation lower bound {fraction_text(RIBBON_SEPARATION_LOWER_BOUND)}",
    ]
    vertex_offset = 1
    for carrier in ribbon.carriers:
        component = _boundary_component(ribbon, carrier)
        lines.append(
            f"# {carrier} cable T(2,{component.meridional_degree}) core-boundary linking {component.natural_core_boundary_linking}"
        )
        indices = []
        for index in range(samples_per_boundary):
            turn = Fraction(2 * index, samples_per_boundary)
            x, y, z = ribbon.surface_point(carrier, turn, ribbon.half_width)
            lines.append(f"v {x:.17g} {y:.17g} {z:.17g}")
            indices.append(vertex_offset + index)
        lines.append("l " + " ".join(map(str, (*indices, indices[0]))))
        vertex_offset += samples_per_boundary
    return "\n".join(lines) + "\n"


def render_core_boundary_obj(
    ribbon: SmoothPrimeRibbon,
    *,
    core_samples: int = 256,
    boundary_samples: int = 512,
) -> str:
    if min(core_samples, boundary_samples) < 32:
        raise IntervalBoundaryError("core and boundary samples must be >= 32")
    lines = [
        f"# P{ribbon.prime} cores and one-component Möbius boundaries",
        "# core objects precede boundary objects",
    ]
    vertex_offset = 1
    for carrier in ribbon.carriers:
        indices = []
        for index in range(core_samples):
            turn = Fraction(index, core_samples)
            x, y, z = ribbon.centerline_point(carrier, turn)
            lines.append(f"v {x:.17g} {y:.17g} {z:.17g}")
            indices.append(vertex_offset + index)
        lines.append("l " + " ".join(map(str, (*indices, indices[0]))))
        vertex_offset += core_samples
    boundary_text = render_boundary_obj(
        ribbon,
        samples_per_boundary=boundary_samples,
    ).splitlines()
    boundary_vertices = [line for line in boundary_text if line.startswith("v ")]
    boundary_groups = [line for line in boundary_text if line.startswith("l ")]
    for line in boundary_vertices:
        lines.append(line)
    for group in boundary_groups:
        raw = [int(value) for value in group.split()[1:]]
        adjusted = [value + vertex_offset - 1 for value in raw]
        lines.append("l " + " ".join(map(str, adjusted)))
    return "\n".join(lines) + "\n"
