# === MODULE_BUILD ===
# id: ucns_prime_generic_diagram
#   module_name: prime_generic_diagram
#   module_kind: experiment
#   summary: readable clearance-preserving generic diagram implementation
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
#   requires: ucns_prime_interval_boundary_links_p7_p5
#   since: 2026-08-11
#   unresolved: see owning facade contracts and research document
# === END MODULE_BUILD ===

# === CONTRACTS ===
# Internal helper: behavioral obligations are declared by the owning facade and witnessed by its tests.
# id: prime_generic_helper_is_facade_witnessed
#   given: the owning facade invokes this readable helper
#   then: the helper behavior is exercised through the named facade test without becoming a separate certificate
#   class: evidence
#   since: 2026-08-11
#
# === END CONTRACTS ===

"""Clearance-preserving generic diagrams of prime core links."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import itertools

from .prime_interval_common import (
    GENERIC_CENTER_X,
    GENERIC_CENTER_Y,
    GENERIC_ISOTOPY_CLEARANCE,
    GENERIC_PROJECTION_DPS,
    GENERIC_TRANSLATION_BOUND,
    IntervalBoundaryError,
    fraction_text,
    require_mpmath as _require_mpmath,
)
from .prime_smooth_ribbons import (
    SmoothPrimeRibbon,
    certify_smooth_prime_five,
    certify_smooth_prime_seven,
)

def _generic_translation_coefficients(carrier: str) -> tuple[Fraction, Fraction]:
    if carrier == 'C':
        return (Fraction(0), Fraction(0))
    index = int(carrier[1:])
    radial = Fraction(100 + 7 * index, 100000)
    tangential = Fraction((index * index + 3 * index + 1) % 7 - 3, 10000)
    return (radial, tangential)

def _mp_exact_centers(ribbon: SmoothPrimeRibbon, dps: int):
    mp = _require_mpmath()
    mp.mp.dps = dps
    if ribbon.prime == 7:
        root3_half = mp.sqrt(3) / 2
        base = {'C': (mp.mpf(0), mp.mpf(0)), 'R0': (mp.mpf(1), mp.mpf(0)), 'R1': (mp.mpf(1) / 2, root3_half), 'R2': (-mp.mpf(1) / 2, root3_half), 'R3': (-mp.mpf(1), mp.mpf(0)), 'R4': (-mp.mpf(1) / 2, -root3_half), 'R5': (mp.mpf(1) / 2, -root3_half)}
    else:
        base = {'C': (mp.mpf(0), mp.mpf(0)), 'R0': (mp.mpf(1), mp.mpf(0)), 'R1': (mp.mpf(0), mp.mpf(1)), 'R2': (-mp.mpf(1), mp.mpf(0)), 'R3': (mp.mpf(0), -mp.mpf(1))}
    result = {}
    for carrier, (center_x, center_y) in base.items():
        if carrier == 'C':
            result[carrier] = (center_x + mp.mpf(GENERIC_CENTER_X.numerator) / GENERIC_CENTER_X.denominator, center_y + mp.mpf(GENERIC_CENTER_Y.numerator) / GENERIC_CENTER_Y.denominator)
            continue
        radial, tangential = _generic_translation_coefficients(carrier)
        radius = mp.sqrt(center_x * center_x + center_y * center_y)
        radial_x, radial_y = (center_x / radius, center_y / radius)
        tangent_x, tangent_y = (-radial_y, radial_x)
        result[carrier] = (center_x + mp.mpf(radial.numerator) / radial.denominator * radial_x + mp.mpf(tangential.numerator) / tangential.denominator * tangent_x, center_y + mp.mpf(radial.numerator) / radial.denominator * radial_y + mp.mpf(tangential.numerator) / tangential.denominator * tangent_y)
    translation_bound = mp.mpf(GENERIC_TRANSLATION_BOUND.numerator) / GENERIC_TRANSLATION_BOUND.denominator
    for carrier in ribbon.carriers:
        base_x, base_y = base[carrier]
        moved_x, moved_y = result[carrier]
        displacement = mp.sqrt((moved_x - base_x) ** 2 + (moved_y - base_y) ** 2)
        if displacement > translation_bound:
            raise IntervalBoundaryError(f'generic projection translation bound exceeded for {carrier}')
    return result

def _flat_step_mp(mp, value):
    if value <= 0:
        return mp.mpf(0)
    if value >= 1:
        return mp.mpf(1)
    left = mp.exp(-1 / value)
    right = mp.exp(-1 / (1 - value))
    return left / (left + right)

def _smooth_field_mp(mp, ribbon: SmoothPrimeRibbon, carrier: str, turn):
    target = turn % 1
    for index, segment in enumerate(ribbon.field(carrier).segments):
        left_turn = mp.mpf(segment.left_turn.numerator) / segment.left_turn.denominator
        right_turn = mp.mpf(segment.right_turn.numerator) / segment.right_turn.denominator
        adjusted = target
        if index == len(ribbon.field(carrier).segments) - 1 and adjusted < left_turn:
            adjusted += 1
        if left_turn <= adjusted <= right_turn:
            left_value = mp.mpf(segment.left_value.numerator) / segment.left_value.denominator
            right_value = mp.mpf(segment.right_value.numerator) / segment.right_value.denominator
            if adjusted == left_turn:
                return left_value
            if adjusted == right_turn:
                return right_value
            local = (adjusted - left_turn) / (right_turn - left_turn)
            return left_value + (right_value - left_value) * _flat_step_mp(mp, local)
    raise AssertionError('high-precision smooth field lookup failed')

def _circle_intersections(mp, left_center, right_center):
    delta_x = right_center[0] - left_center[0]
    delta_y = right_center[1] - left_center[1]
    distance = mp.sqrt(delta_x * delta_x + delta_y * delta_y)
    if distance > 2:
        return ()
    if distance == 2:
        raise IntervalBoundaryError('generic projection retained a tangency')
    if distance <= 0:
        raise IntervalBoundaryError('generic projection collapsed two centers')
    half_distance = distance / 2
    height = mp.sqrt(1 - half_distance * half_distance)
    unit_x, unit_y = (delta_x / distance, delta_y / distance)
    midpoint_x = left_center[0] + half_distance * unit_x
    midpoint_y = left_center[1] + half_distance * unit_y
    perpendicular_x, perpendicular_y = (-unit_y, unit_x)
    return ((midpoint_x + height * perpendicular_x, midpoint_y + height * perpendicular_y), (midpoint_x - height * perpendicular_x, midpoint_y - height * perpendicular_y))

@dataclass(frozen=True, slots=True)
class DiagramCrossing:
    crossing_id: str
    left: str
    right: str
    over: str
    under: str
    left_turn_decimal: str
    right_turn_decimal: str
    over_turn_decimal: str
    under_turn_decimal: str
    sign: int
    height_gap_decimal: str

    def turn_for(self, carrier: str) -> float:
        if carrier == self.left:
            return float(self.left_turn_decimal)
        if carrier == self.right:
            return float(self.right_turn_decimal)
        raise IntervalBoundaryError(f'{carrier} is not incident to {self.crossing_id}')

    def as_dict(self) -> dict[str, object]:
        return {'crossing_id': self.crossing_id, 'pair': [self.left, self.right], 'over': self.over, 'under': self.under, 'left_turn_decimal': self.left_turn_decimal, 'right_turn_decimal': self.right_turn_decimal, 'sign': self.sign, 'height_gap_decimal': self.height_gap_decimal}

@dataclass(frozen=True, slots=True)
class GenericCoreDiagram:
    prime: int
    component_order: tuple[str, ...]
    crossings: tuple[DiagramCrossing, ...]
    pairwise_linking_matrix: tuple[tuple[int, ...], ...]
    minimum_turn_gap_decimal: str
    minimum_height_gap_decimal: str
    maximum_translation_bound: Fraction
    residual_ribbon_clearance: Fraction
    precision_dps: int

    def crossing_turn(self, crossing: DiagramCrossing, carrier: str) -> float:
        return crossing.turn_for(carrier)

    def as_dict(self) -> dict[str, object]:
        return {'method': 'simultaneous deterministic in-plane carrier translations followed by exact equal-circle intersections at high precision', 'precision_dps': self.precision_dps, 'component_order': list(self.component_order), 'crossing_count': len(self.crossings), 'pairwise_linking_matrix': [list(row) for row in self.pairwise_linking_matrix], 'minimum_distinct_crossing_turn_gap_decimal': self.minimum_turn_gap_decimal, 'minimum_crossing_height_gap_decimal': self.minimum_height_gap_decimal, 'maximum_component_translation_bound': fraction_text(self.maximum_translation_bound), 'residual_complete_ribbon_clearance': fraction_text(self.residual_ribbon_clearance), 'crossings': [item.as_dict() for item in self.crossings]}

def build_generic_core_diagram(ribbon: SmoothPrimeRibbon, *, dps: int=GENERIC_PROJECTION_DPS) -> GenericCoreDiagram:
    mp = _require_mpmath()
    mp.mp.dps = dps
    centers = _mp_exact_centers(ribbon, dps)
    crossings: list[DiagramCrossing] = []
    order = ribbon.carriers
    for left, right in itertools.combinations(order, 2):
        for crossing_index, point in enumerate(_circle_intersections(mp, centers[left], centers[right])):
            left_turn = mp.atan2(point[1] - centers[left][1], point[0] - centers[left][0]) / (2 * mp.pi) % 1
            right_turn = mp.atan2(point[1] - centers[right][1], point[0] - centers[right][0]) / (2 * mp.pi) % 1
            left_height = _smooth_field_mp(mp, ribbon, left, left_turn)
            right_height = _smooth_field_mp(mp, ribbon, right, right_turn)
            height_difference = left_height - right_height
            if height_difference == 0:
                raise IntervalBoundaryError('generic projection produced an unresolved height tie')
            orientation_value = mp.sin(2 * mp.pi * (right_turn - left_turn))
            if orientation_value == 0:
                raise IntervalBoundaryError('generic projection produced a tangent crossing')
            orientation = 1 if orientation_value > 0 else -1
            if height_difference > 0:
                over, under = (left, right)
                over_turn, under_turn = (left_turn, right_turn)
                sign = orientation
            else:
                over, under = (right, left)
                over_turn, under_turn = (right_turn, left_turn)
                sign = -orientation
            crossings.append(DiagramCrossing(crossing_id=f'{left}::{right}::{crossing_index}', left=left, right=right, over=over, under=under, left_turn_decimal=mp.nstr(left_turn, 50), right_turn_decimal=mp.nstr(right_turn, 50), over_turn_decimal=mp.nstr(over_turn, 50), under_turn_decimal=mp.nstr(under_turn, 50), sign=sign, height_gap_decimal=mp.nstr(abs(height_difference), 50)))
    crossings.sort(key=lambda item: item.crossing_id)
    matrix = [[0] * len(order) for _ in order]
    index = {carrier: position for position, carrier in enumerate(order)}
    for left, right in itertools.combinations(order, 2):
        total = sum((crossing.sign for crossing in crossings if crossing.left == left and crossing.right == right))
        if total % 2:
            raise IntervalBoundaryError(f'odd crossing-sign sum for {left}::{right}')
        value = total // 2
        matrix[index[left]][index[right]] = value
        matrix[index[right]][index[left]] = value
    minimum_turn_gap = mp.inf
    for carrier in order:
        turns = sorted((mp.mpf(crossing.left_turn_decimal) if crossing.left == carrier else mp.mpf(crossing.right_turn_decimal) for crossing in crossings if carrier in {crossing.left, crossing.right}))
        if not turns:
            continue
        gaps = [right - left for left, right in zip(turns, turns[1:])]
        gaps.append(turns[0] + 1 - turns[-1])
        minimum_turn_gap = min(minimum_turn_gap, min(gaps))
    minimum_height_gap = min((mp.mpf(item.height_gap_decimal) for item in crossings))
    expected_crossings = 36 if ribbon.prime == 7 else 16
    if len(crossings) != expected_crossings:
        raise IntervalBoundaryError(f'generic projection crossing count mismatch: expected {expected_crossings}, observed {len(crossings)}')
    if minimum_turn_gap <= mp.mpf('1e-6'):
        raise IntervalBoundaryError('generic projection does not separate crossing turns sufficiently for deterministic ordering')
    if minimum_height_gap <= mp.mpf('0.09'):
        raise IntervalBoundaryError('generic projection consumed the certified event-height separation')
    smooth = certify_smooth_prime_seven() if ribbon.prime == 7 else certify_smooth_prime_five()
    expected = tuple((tuple(row) for row in smooth.linking_matrix.matrix))
    observed = tuple((tuple(row) for row in matrix))
    if observed != expected:
        raise IntervalBoundaryError('generic projection changed the core linking matrix')
    if GENERIC_ISOTOPY_CLEARANCE <= 0:
        raise IntervalBoundaryError('generic projection translations consumed ribbon clearance')
    return GenericCoreDiagram(prime=ribbon.prime, component_order=order, crossings=tuple(crossings), pairwise_linking_matrix=observed, minimum_turn_gap_decimal=mp.nstr(minimum_turn_gap, 30), minimum_height_gap_decimal=mp.nstr(minimum_height_gap, 30), maximum_translation_bound=GENERIC_TRANSLATION_BOUND, residual_ribbon_clearance=GENERIC_ISOTOPY_CLEARANCE, precision_dps=dps)
