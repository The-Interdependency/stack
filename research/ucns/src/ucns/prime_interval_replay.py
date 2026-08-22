# === MODULE_BUILD ===
# id: ucns_prime_interval_replay
#   module_name: prime_interval_replay
#   module_kind: experiment
#   summary: readable outward-directed interval replay implementation
#   owner: Erin Spencer
#   public_surface: internal readable implementation used through the declared facade
#   internal_surface: module implementation
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_interval_boundary_links.py
#   rollout: readable implementation; authority remains with the facade contracts
#   rollback: remove only with the owning consolidated research layer
#   requires: ucns_prime_interval_common
#   since: 2026-08-11
#   unresolved: see owning facade contracts and research document
# === END MODULE_BUILD ===

# === CONTRACTS ===
# Internal helper: behavioral obligations are declared by the owning facade and witnessed by its tests.
# id: prime_interval_replay_helper_is_facade_witnessed
#   given: the owning facade invokes this readable helper
#   then: the helper behavior is exercised through the named facade test without becoming a separate certificate
#   class: evidence
#   since: 2026-08-11
#
# === END CONTRACTS ===

"""Directed interval replay of complete carrier-pair parameter tori."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import itertools
from typing import Mapping, Sequence

from .prime_interval_common import (
    CENTERLINE_SEPARATION_TARGET,
    INTERVAL_DPS,
    INTERVAL_MAX_BOXES_PER_PAIR,
    INTERVAL_MAX_DEPTH,
    RIBBON_SEPARATION_LOWER_BOUND,
    IntervalBoundaryError,
    fraction_text,
    require_mpmath as _require_mpmath,
)
from .prime_smooth_ribbons import SmoothPrimeRibbon

def _mp_interval_endpoint_text(interval, *, upper: bool, digits: int=80) -> str:
    from mpmath.libmp import to_str
    endpoint = interval._mpi_[1 if upper else 0]
    return to_str(endpoint, digits)

def _mp_interval_endpoint(interval, *, upper: bool):
    mp = _require_mpmath()
    return mp.mpf(_mp_interval_endpoint_text(interval, upper=upper))

def _iv_fraction(context, value: Fraction | int):
    if isinstance(value, int):
        return context.mpf(value)
    return context.mpf(value.numerator) / value.denominator

def _exact_interval_centers(prime: int, context) -> dict[str, tuple[object, object]]:
    zero = _iv_fraction(context, 0)
    one = _iv_fraction(context, 1)
    half = _iv_fraction(context, Fraction(1, 2))
    if prime == 7:
        root3_half = context.sqrt(_iv_fraction(context, 3)) / 2
        return {'C': (zero, zero), 'R0': (one, zero), 'R1': (half, root3_half), 'R2': (-half, root3_half), 'R3': (-one, zero), 'R4': (-half, -root3_half), 'R5': (half, -root3_half)}
    if prime == 5:
        return {'C': (zero, zero), 'R0': (one, zero), 'R1': (zero, one), 'R2': (-one, zero), 'R3': (zero, -one)}
    raise IntervalBoundaryError('only P7 and P5 are supported')

def _flat_step_interval_point(context, value: Fraction):
    if value <= 0:
        return _iv_fraction(context, 0)
    if value >= 1:
        return _iv_fraction(context, 1)
    x = _iv_fraction(context, value)
    left = context.exp(-1 / x)
    right = context.exp(-1 / (1 - x))
    return left / (left + right)

def _smooth_field_interval_point(context, ribbon: SmoothPrimeRibbon, carrier: str, turn: Fraction):
    field = ribbon.field(carrier)
    target = turn % 1
    for index, segment in enumerate(field.segments):
        adjusted = target
        if index == len(field.segments) - 1 and adjusted < segment.left_turn:
            adjusted += 1
        if not segment.contains(adjusted):
            continue
        if adjusted == segment.left_turn:
            return _iv_fraction(context, segment.left_value)
        if adjusted == segment.right_turn:
            return _iv_fraction(context, segment.right_value)
        local = (adjusted - segment.left_turn) / segment.turn_width
        return _iv_fraction(context, segment.left_value) + _iv_fraction(context, segment.right_value - segment.left_value) * _flat_step_interval_point(context, local)
    raise AssertionError('interval field lookup failed')

def _centerline_interval_point(context, ribbon: SmoothPrimeRibbon, carrier: str, turn: Fraction, centers: Mapping[str, tuple[object, object]]) -> tuple[object, object, object]:
    angle = 2 * context.pi * _iv_fraction(context, turn)
    center_x, center_y = centers[carrier]
    return (center_x + context.cos(angle), center_y + context.sin(angle), _smooth_field_interval_point(context, ribbon, carrier, turn))

def _interval_square(context, value):
    lower = _mp_interval_endpoint(value, upper=False)
    upper = _mp_interval_endpoint(value, upper=True)
    if lower <= 0 <= upper:
        high = max(lower * lower, upper * upper)
        return context.mpf([0, high])
    values = (lower * lower, upper * upper)
    return context.mpf([min(values), max(values)])

def _interval_distance_lower(context, left: Sequence[object], right: Sequence[object]):
    total = _iv_fraction(context, 0)
    for left_value, right_value in zip(left, right):
        total += _interval_square(context, left_value - right_value)
    return _mp_interval_endpoint(context.sqrt(total), upper=False)

def _interval_speed_upper(context, ribbon: SmoothPrimeRibbon, carrier: str):
    lift_bound = _iv_fraction(context, ribbon.field(carrier).maximum_derivative_bound)
    speed = context.sqrt((2 * context.pi) ** 2 + lift_bound ** 2)
    return _mp_interval_endpoint(speed, upper=True)

@dataclass(frozen=True, slots=True)
class IntervalPairCertificate:
    left: str
    right: str
    target: Fraction
    boxes_evaluated: int
    certified_leaf_boxes: int
    maximum_depth: int
    minimum_leaf_lower_bound_decimal: str
    left_speed_upper_decimal: str
    right_speed_upper_decimal: str

    @property
    def pair_id(self) -> str:
        return f'{self.left}::{self.right}'

    @property
    def minimum_leaf_lower_bound(self) -> float:
        return float(self.minimum_leaf_lower_bound_decimal)

    @property
    def certified(self) -> bool:
        return self.minimum_leaf_lower_bound > float(self.target)

    def as_dict(self) -> dict[str, object]:
        return {'pair_id': self.pair_id, 'target': fraction_text(self.target), 'boxes_evaluated': self.boxes_evaluated, 'certified_leaf_boxes': self.certified_leaf_boxes, 'maximum_depth': self.maximum_depth, 'minimum_leaf_lower_bound_decimal': self.minimum_leaf_lower_bound_decimal, 'left_speed_upper_decimal': self.left_speed_upper_decimal, 'right_speed_upper_decimal': self.right_speed_upper_decimal, 'certified': self.certified}

@dataclass(frozen=True, slots=True)
class IntervalSeparationCertificate:
    prime: int
    dps: int
    mpmath_version: str
    pair_certificates: tuple[IntervalPairCertificate, ...]

    @property
    def pair_count(self) -> int:
        return len(self.pair_certificates)

    @property
    def total_boxes_evaluated(self) -> int:
        return sum((item.boxes_evaluated for item in self.pair_certificates))

    @property
    def maximum_depth(self) -> int:
        return max((item.maximum_depth for item in self.pair_certificates))

    @property
    def minimum_leaf_lower_bound_decimal(self) -> str:
        return min((item.minimum_leaf_lower_bound_decimal for item in self.pair_certificates), key=lambda value: float(value))

    @property
    def all_pairs_certified(self) -> bool:
        return all((item.certified for item in self.pair_certificates))

    def as_dict(self) -> dict[str, object]:
        return {'method': 'mpmath.iv directed interval endpoints plus exact dyadic Lipschitz subdivision', 'mpmath_version': self.mpmath_version, 'decimal_precision': self.dps, 'parameter_domain_per_pair': '[0,1] x [0,1]', 'centerline_target': fraction_text(CENTERLINE_SEPARATION_TARGET), 'pair_count': self.pair_count, 'all_pairs_certified': self.all_pairs_certified, 'total_boxes_evaluated': self.total_boxes_evaluated, 'maximum_depth': self.maximum_depth, 'minimum_leaf_lower_bound_decimal': self.minimum_leaf_lower_bound_decimal, 'ad_hoc_roundoff_buffer': None, 'finite_width_ribbon_separation_lower_bound': fraction_text(RIBBON_SEPARATION_LOWER_BOUND), 'pairs': [item.as_dict() for item in self.pair_certificates]}

def _replay_interval_pair(ribbon: SmoothPrimeRibbon, left: str, right: str, *, dps: int) -> IntervalPairCertificate:
    mp = _require_mpmath()
    context = mp.iv
    context.dps = dps
    centers = _exact_interval_centers(ribbon.prime, context)
    left_speed = _interval_speed_upper(context, ribbon, left)
    right_speed = _interval_speed_upper(context, ribbon, right)
    target = mp.mpf(CENTERLINE_SEPARATION_TARGET.numerator) / CENTERLINE_SEPARATION_TARGET.denominator
    pending: list[tuple[Fraction, Fraction, Fraction, Fraction, int]] = [(Fraction(0), Fraction(1), Fraction(0), Fraction(1), 0)]
    evaluated = 0
    leaves = 0
    maximum_depth = 0
    minimum_lower = mp.inf
    while pending:
        left_a, left_b, right_a, right_b, depth = pending.pop()
        evaluated += 1
        if evaluated > INTERVAL_MAX_BOXES_PER_PAIR:
            raise IntervalBoundaryError(f'interval box budget exceeded for {left}::{right}')
        maximum_depth = max(maximum_depth, depth)
        left_mid = (left_a + left_b) / 2
        right_mid = (right_a + right_b) / 2
        center_distance_lower = _interval_distance_lower(context, _centerline_interval_point(context, ribbon, left, left_mid, centers), _centerline_interval_point(context, ribbon, right, right_mid, centers))
        left_radius = left_speed * mp.mpf((left_b - left_a).numerator) / ((left_b - left_a).denominator * 2)
        right_radius = right_speed * mp.mpf((right_b - right_a).numerator) / ((right_b - right_a).denominator * 2)
        lower = center_distance_lower - left_radius - right_radius
        if lower > target:
            leaves += 1
            minimum_lower = min(minimum_lower, lower)
            continue
        if depth >= INTERVAL_MAX_DEPTH:
            raise IntervalBoundaryError(f'interval separation unresolved at depth {depth} for {left}::{right}; lower={lower}')
        if left_radius >= right_radius:
            midpoint = (left_a + left_b) / 2
            pending.append((midpoint, left_b, right_a, right_b, depth + 1))
            pending.append((left_a, midpoint, right_a, right_b, depth + 1))
        else:
            midpoint = (right_a + right_b) / 2
            pending.append((left_a, left_b, midpoint, right_b, depth + 1))
            pending.append((left_a, left_b, right_a, midpoint, depth + 1))
    result = IntervalPairCertificate(left=left, right=right, target=CENTERLINE_SEPARATION_TARGET, boxes_evaluated=evaluated, certified_leaf_boxes=leaves, maximum_depth=maximum_depth, minimum_leaf_lower_bound_decimal=mp.nstr(minimum_lower, 30), left_speed_upper_decimal=mp.nstr(left_speed, 30), right_speed_upper_decimal=mp.nstr(right_speed, 30))
    if not result.certified:
        raise IntervalBoundaryError(f'outward interval replay failed for {result.pair_id}')
    return result

def replay_interval_separation(ribbon: SmoothPrimeRibbon, *, dps: int=INTERVAL_DPS) -> IntervalSeparationCertificate:
    if isinstance(dps, bool) or not isinstance(dps, int) or dps < 40:
        raise IntervalBoundaryError('interval decimal precision must be an integer >= 40')
    mp = _require_mpmath()
    pairs = tuple((_replay_interval_pair(ribbon, left, right, dps=dps) for left, right in itertools.combinations(ribbon.carriers, 2)))
    result = IntervalSeparationCertificate(prime=ribbon.prime, dps=dps, mpmath_version=str(mp.__version__), pair_certificates=pairs)
    if not result.all_pairs_certified:
        raise IntervalBoundaryError('not every pair passed the interval replay')
    return result
