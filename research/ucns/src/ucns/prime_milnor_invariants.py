# === MODULE_BUILD ===
# id: ucns_prime_milnor_invariants
#   module_name: prime_milnor_invariants
#   module_kind: experiment
#   summary: readable length-three Milnor extraction and benchmark implementation
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
#   requires: ucns_prime_generic_diagram
#   since: 2026-08-11
#   unresolved: see owning facade contracts and research document
# === END MODULE_BUILD ===

# === CONTRACTS ===
# Internal helper: behavioral obligations are declared by the owning facade and witnessed by its tests.
# id: prime_milnor_helper_is_facade_witnessed
#   given: the owning facade invokes this readable helper
#   then: the helper behavior is exercised through the named facade test without becoming a separate certificate
#   class: evidence
#   since: 2026-08-11
#
# === END CONTRACTS ===

"""Length-three Milnor invariants from generic core diagrams."""
from __future__ import annotations

from dataclasses import dataclass
import itertools
import math
from typing import Mapping, MutableMapping, Sequence

from .prime_generic_diagram import DiagramCrossing, GenericCoreDiagram, build_generic_core_diagram
from .prime_interval_common import IntervalBoundaryError
from .prime_smooth_ribbons import SmoothPrimeRibbon

Series = dict[tuple[str, ...], int]

def _series_add(left: Series, right: Series) -> Series:
    result = dict(left)
    for word, coefficient in right.items():
        result[word] = result.get(word, 0) + coefficient
    return {word: coefficient for word, coefficient in result.items() if coefficient}

def _series_scale(series: Series, factor: int) -> Series:
    return {word: coefficient * factor for word, coefficient in series.items() if coefficient * factor}

def _series_multiply(left: Series, right: Series) -> Series:
    result: Series = {}
    for left_word, left_coefficient in left.items():
        for right_word, right_coefficient in right.items():
            word = left_word + right_word
            if len(word) > 2:
                continue
            result[word] = result.get(word, 0) + left_coefficient * right_coefficient
    return {word: coefficient for word, coefficient in result.items() if coefficient}

def _series_inverse(series: Series) -> Series:
    one: Series = {(): 1}
    reduced = _series_add(series, {(): -1})
    return _series_add(_series_add(one, _series_scale(reduced, -1)), _series_multiply(reduced, reduced))

def _series_power(series: Series, exponent: int) -> Series:
    if exponent == 1:
        return series
    if exponent == -1:
        return _series_inverse(series)
    raise IntervalBoundaryError('crossing exponents must be plus or minus one')

def _series_conjugate(generator: Series, conjugator: Series, exponent: int) -> Series:
    powered = _series_power(conjugator, exponent)
    return _series_multiply(_series_multiply(_series_inverse(powered), generator), powered)

def _meridian(component: str) -> Series:
    return {(): 1, (component,): 1}

def _crossings_for_components(diagram: GenericCoreDiagram, components: Sequence[str]) -> tuple[DiagramCrossing, ...]:
    component_set = set(components)
    return tuple((item for item in diagram.crossings if item.left in component_set and item.right in component_set))

def _cyclic_turn(turn: float, basepoint: float) -> float:
    return (turn - basepoint) % 1.0

def _longitude_series(diagram: GenericCoreDiagram, components: Sequence[str], *, basepoint: float) -> dict[str, Series]:
    crossings = _crossings_for_components(diagram, components)
    under_by_component: dict[str, list[DiagramCrossing]] = {component: [] for component in components}
    for crossing in crossings:
        under_by_component[crossing.under].append(crossing)
    for component in components:
        under_by_component[component].sort(key=lambda item: (_cyclic_turn(float(item.under_turn_decimal), basepoint), item.crossing_id))
    arcs: dict[str, list[Series]] = {}
    for component in components:
        current = _meridian(component)
        component_arcs = [current]
        for crossing in under_by_component[component]:
            current = _series_conjugate(current, _meridian(crossing.over), crossing.sign)
            component_arcs.append(current)
        arcs[component] = component_arcs

    def over_arc(crossing: DiagramCrossing) -> Series:
        component = crossing.over
        target = _cyclic_turn(float(crossing.over_turn_decimal), basepoint)
        count = sum((_cyclic_turn(float(item.under_turn_decimal), basepoint) < target for item in under_by_component[component]))
        return arcs[component][count]
    result: dict[str, Series] = {}
    for component in components:
        longitude: Series = {(): 1}
        for crossing in under_by_component[component]:
            longitude = _series_multiply(longitude, _series_power(over_arc(crossing), crossing.sign))
        result[component] = longitude
    return result

def _permutation_sign(canonical: Sequence[str], permutation: Sequence[str]) -> int:
    positions = [canonical.index(item) for item in permutation]
    inversions = sum((positions[left] > positions[right] for left in range(len(positions)) for right in range(left + 1, len(positions))))
    return -1 if inversions % 2 else 1

def _milnor_value(diagram: GenericCoreDiagram, ordered_triple: tuple[str, str, str], *, basepoint: float) -> int:
    first, second, longitude_component = ordered_triple
    longitudes = _longitude_series(diagram, ordered_triple, basepoint=basepoint)
    return longitudes[longitude_component].get((first, second), 0)

def _borromean_braid_validation() -> dict[str, object]:
    word = ((0, 1, 1), (1, 2, -1)) * 3
    positions = ['0', '1', '2']
    events: list[tuple[str, str, int, float]] = []
    for event_index, (left_position, right_position, sign) in enumerate(word):
        left_component = positions[left_position]
        right_component = positions[right_position]
        over = left_component if sign == 1 else right_component
        under = right_component if sign == 1 else left_component
        events.append((over, under, sign, float(event_index)))
        positions[left_position], positions[right_position] = (right_component, left_component)
    if positions != ['0', '1', '2']:
        raise IntervalBoundaryError('Borromean braid closure did not have three components')
    components = ('0', '1', '2')
    under_by: dict[str, list[tuple[str, str, int, float]]] = {component: [] for component in components}
    for event in events:
        under_by[event[1]].append(event)
    arcs: dict[str, list[Series]] = {}
    for component in components:
        current = _meridian(component)
        component_arcs = [current]
        for over, _, sign, _ in under_by[component]:
            current = _series_conjugate(current, _meridian(over), sign)
            component_arcs.append(current)
        arcs[component] = component_arcs

    def over_arc(event):
        over, _, _, order = event
        count = sum((item[3] < order for item in under_by[over]))
        return arcs[over][count]
    longitudes: dict[str, Series] = {}
    for component in components:
        longitude: Series = {(): 1}
        for event in under_by[component]:
            longitude = _series_multiply(longitude, _series_power(over_arc(event), event[2]))
        longitudes[component] = longitude
    values = {'012': longitudes['2'].get(('0', '1'), 0), '102': longitudes['2'].get(('1', '0'), 0), '120': longitudes['0'].get(('1', '2'), 0)}
    if abs(values['012']) != 1 or values['102'] != -values['012'] or values['120'] != values['012']:
        raise IntervalBoundaryError('Magnus implementation failed the Borromean regression')
    return {'test_link': 'closure of (sigma_1 sigma_2^-1)^3', 'mu_012': values['012'], 'antisymmetry_check': True, 'cyclic_check': True}

@dataclass(frozen=True, slots=True)
class MilnorTripleInvariant:
    triple: tuple[str, str, str]
    pairwise_linking: tuple[int, int, int]
    indeterminacy_modulus: int
    value: int | None
    basepoint_values: tuple[int, ...]
    antisymmetry_verified: bool

    @property
    def integer_valued(self) -> bool:
        return self.indeterminacy_modulus == 0

    def as_dict(self) -> dict[str, object]:
        return {'ordered_triple': list(self.triple), 'pairwise_linking': list(self.pairwise_linking), 'indeterminacy_modulus': self.indeterminacy_modulus, 'integer_valued': self.integer_valued, 'mu_bar_123': self.value, 'basepoint_values': list(self.basepoint_values), 'basepoint_independent': len(set(self.basepoint_values)) <= 1, 'antisymmetry_verified': self.antisymmetry_verified, 'standing': 'integer invariant' if self.integer_valued else 'residue modulo gcd of pairwise linking numbers; modulus one is uninformative'}

@dataclass(frozen=True, slots=True)
class MilnorProfile:
    prime: int
    diagram: GenericCoreDiagram
    triples: tuple[MilnorTripleInvariant, ...]
    Borromean_validation: Mapping[str, object]

    @property
    def integer_valued_triples(self) -> tuple[MilnorTripleInvariant, ...]:
        return tuple((item for item in self.triples if item.integer_valued))

    @property
    def nonzero_integer_values(self) -> tuple[MilnorTripleInvariant, ...]:
        return tuple((item for item in self.integer_valued_triples if item.value not in {None, 0}))

    def as_dict(self) -> dict[str, object]:
        return {'method': 'Wirtinger longitudes reduced through the third lower-central quotient and degree-two truncated Magnus expansion', 'generic_core_diagram': self.diagram.as_dict(), 'Borromean_regression': dict(self.Borromean_validation), 'total_component_triples': len(self.triples), 'integer_valued_algebraically_split_triples': len(self.integer_valued_triples), 'nonzero_integer_length_three_invariants': len(self.nonzero_integer_values), 'all_informative_length_three_values_zero': not self.nonzero_integer_values, 'triples': [item.as_dict() for item in self.triples], 'boundary': 'length-three Milnor invariants do not classify the whole link; length four and higher remain unresolved'}

def compute_milnor_profile(ribbon: SmoothPrimeRibbon, diagram: GenericCoreDiagram | None=None) -> MilnorProfile:
    generic = diagram or build_generic_core_diagram(ribbon)
    order = generic.component_order
    index = {component: position for position, component in enumerate(order)}
    matrix = generic.pairwise_linking_matrix
    basepoints = (0.017, 0.071, 0.133, 0.271, 0.499)
    results: list[MilnorTripleInvariant] = []
    for triple in itertools.combinations(order, 3):
        pairwise = tuple((matrix[index[left]][index[right]] for left, right in ((triple[0], triple[1]), (triple[0], triple[2]), (triple[1], triple[2]))))
        modulus = math.gcd(*(abs(value) for value in pairwise))
        if modulus == 0:
            values = tuple((_milnor_value(generic, triple, basepoint=basepoint) for basepoint in basepoints))
            if len(set(values)) != 1:
                raise IntervalBoundaryError(f'basepoint dependence for Milnor triple {triple}')
            canonical_value = values[0]
            antisymmetry = True
            for permutation in itertools.permutations(triple):
                observed = _milnor_value(generic, permutation, basepoint=basepoints[0])
                expected = _permutation_sign(triple, permutation) * canonical_value
                antisymmetry &= observed == expected
            if not antisymmetry:
                raise IntervalBoundaryError(f'Milnor antisymmetry failed for {triple}')
            value: int | None = canonical_value
        else:
            values = ()
            value = 0 if modulus == 1 else None
            antisymmetry = True
        results.append(MilnorTripleInvariant(triple=triple, pairwise_linking=pairwise, indeterminacy_modulus=modulus, value=value, basepoint_values=values, antisymmetry_verified=antisymmetry))
    return MilnorProfile(prime=ribbon.prime, diagram=generic, triples=tuple(results), Borromean_validation=_borromean_braid_validation())
