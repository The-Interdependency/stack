# === MODULE_BUILD ===
# id: ucns_prime_boundary_link_invariants
#   module_name: prime_boundary_link_invariants
#   module_kind: experiment
#   summary: readable exact boundary-component and integer linking invariant implementation
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
# id: prime_boundary_helper_is_facade_witnessed
#   given: the owning facade invokes this readable helper
#   then: the helper behavior is exercised through the named facade test without becoming a separate certificate
#   class: evidence
#   since: 2026-08-11
#
# === END CONTRACTS ===

"""Exact Möbius boundary-component and integer linking invariants."""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping, Sequence

from .prime_interval_common import (
    IntervalBoundaryError,
    fraction_text,
    require_sympy as _require_sympy,
)
from .prime_smooth_ribbons import (
    SmoothPrimeRibbon,
    certify_smooth_prime_five,
    certify_smooth_prime_seven,
)

def _alexander_laurent(meridional_winding: int) -> dict[str, int]:
    winding = abs(meridional_winding)
    if winding % 2 != 1 or winding < 1:
        raise IntervalBoundaryError('two-strand Möbius boundary requires a positive odd winding')
    genus = (winding - 1) // 2
    return {str(exponent): (-1) ** (genus - exponent) for exponent in range(-genus, genus + 1)}

@dataclass(frozen=True, slots=True)
class BoundaryComponentInvariant:
    carrier: str
    phase_winding: int
    longitudinal_winding: int
    meridional_winding: int
    core_boundary_linking: int
    knot_type: str
    genus: int
    determinant: int
    crossing_number: int
    alexander_laurent: Mapping[str, int]

    @property
    def component_id(self) -> str:
        return f'd{self.carrier}'

    def as_dict(self) -> dict[str, object]:
        return {'boundary_component': self.component_id, 'carrier': self.carrier, 'parameter_domain': '0 <= t < 2 turns at breadth +w', 'one_continuous_component': math.gcd(self.longitudinal_winding, self.meridional_winding) == 1, 'tubular_slope': {'longitude': self.longitudinal_winding, 'meridian': self.meridional_winding}, 'phase_winding': self.phase_winding, 'core_boundary_linking': self.core_boundary_linking, 'component_knot_type': self.knot_type, 'Seifert_genus': self.genus, 'knot_determinant': self.determinant, 'minimal_crossing_number': self.crossing_number, 'normalized_Alexander_polynomial_Laurent_coefficients': dict(self.alexander_laurent), 'embedding_reason': 'the carrier centerline is a vertical graph over a circle and the boundary is a primitive two-by-odd cable in its embedded tubular neighborhood'}

def extract_boundary_components(ribbon: SmoothPrimeRibbon) -> tuple[BoundaryComponentInvariant, ...]:
    result: list[BoundaryComponentInvariant] = []
    for carrier in ribbon.carriers:
        phase_winding = ribbon.base.phase_law.center_winding if carrier == 'C' else 0
        meridional = 1 + 2 * phase_winding
        absolute = abs(meridional)
        genus = (absolute - 1) // 2
        knot_type = 'unknot (T(2,1))' if absolute == 1 else f'torus knot T(2,{absolute})'
        result.append(BoundaryComponentInvariant(carrier=carrier, phase_winding=phase_winding, longitudinal_winding=2, meridional_winding=meridional, core_boundary_linking=meridional, knot_type=knot_type, genus=genus, determinant=absolute, crossing_number=0 if absolute == 1 else absolute, alexander_laurent=_alexander_laurent(meridional)))
    return tuple(result)

def _matrix_rank_determinant_smith(matrix: Sequence[Sequence[int]]) -> tuple[int, int, tuple[int, ...]]:
    sp, smith_normal_form, ZZ = _require_sympy()
    sympy_matrix = sp.Matrix(matrix)
    rank = int(sympy_matrix.rank())
    determinant = int(sympy_matrix.det()) if sympy_matrix.rows == sympy_matrix.cols else 0
    smith = smith_normal_form(sympy_matrix, domain=ZZ)
    factors = tuple((abs(int(smith[index, index])) for index in range(min(smith.rows, smith.cols)) if smith[index, index] != 0))
    return (rank, determinant, factors)

def _factor_integer(value: int) -> dict[str, int]:
    remaining = abs(value)
    if remaining in {0, 1}:
        return {str(remaining): 1}
    factors: dict[str, int] = {}
    divisor = 2
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            factors[str(divisor)] = factors.get(str(divisor), 0) + 1
            remaining //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors[str(remaining)] = factors.get(str(remaining), 0) + 1
    return factors

@dataclass(frozen=True, slots=True)
class IntegerMatrixInvariant:
    component_order: tuple[str, ...]
    matrix: tuple[tuple[int, ...], ...]
    rank: int
    nullity: int
    determinant: int
    smith_nonzero_invariant_factors: tuple[int, ...]

    def as_dict(self) -> dict[str, object]:
        return {'component_order': list(self.component_order), 'matrix': [list(row) for row in self.matrix], 'rank_over_Q': self.rank, 'nullity_over_Q': self.nullity, 'determinant': self.determinant, 'absolute_determinant_factorization': _factor_integer(self.determinant), 'Smith_nonzero_invariant_factors': list(self.smith_nonzero_invariant_factors)}

def _integer_matrix_invariant(order: Sequence[str], matrix: Sequence[Sequence[int]]) -> IntegerMatrixInvariant:
    rank, determinant, smith = _matrix_rank_determinant_smith(matrix)
    return IntegerMatrixInvariant(component_order=tuple(order), matrix=tuple((tuple((int(value) for value in row)) for row in matrix)), rank=rank, nullity=len(order) - rank, determinant=determinant, smith_nonzero_invariant_factors=smith)

@dataclass(frozen=True, slots=True)
class BoundaryLinkCertificate:
    prime: int
    components: tuple[BoundaryComponentInvariant, ...]
    core_matrix: IntegerMatrixInvariant
    boundary_matrix: IntegerMatrixInvariant
    mixed_core_boundary_block: tuple[tuple[int, ...], ...]
    full_core_boundary_matrix: IntegerMatrixInvariant

    def as_dict(self) -> dict[str, object]:
        return {'terminology': 'ribbon-boundary component link; not automatically a boundary link in the knot-theoretic sense because the spanning Möbius surfaces are nonorientable', 'components': [item.as_dict() for item in self.components], 'core_pairwise_linking': self.core_matrix.as_dict(), 'boundary_pairwise_linking': {**self.boundary_matrix.as_dict(), 'homology_law': 'lk(dMi,dMj)=4*lk(Ci,Cj) for i!=j'}, 'mixed_core_boundary_block': {'rows': list(self.core_matrix.component_order), 'columns': [item.component_id for item in self.components], 'matrix': [list(row) for row in self.mixed_core_boundary_block], 'off_diagonal_law': 'lk(Ci,dMj)=2*lk(Ci,Cj)', 'diagonal_law': 'lk(Ci,dMi)=1+2*phase_winding_i'}, 'full_core_boundary_pairwise_linking': self.full_core_boundary_matrix.as_dict(), 'orientation_boundary': 'component reorientation conjugates the matrix by a diagonal sign matrix; absolute determinant and Smith factors are preserved'}

def build_boundary_link_certificate(ribbon: SmoothPrimeRibbon) -> BoundaryLinkCertificate:
    smooth = certify_smooth_prime_seven() if ribbon.prime == 7 else certify_smooth_prime_five()
    carriers = ribbon.carriers
    core = [list(row) for row in smooth.linking_matrix.matrix]
    components = extract_boundary_components(ribbon)
    size = len(carriers)
    boundary = [[4 * core[row][column] for column in range(size)] for row in range(size)]
    mixed = [[0] * size for _ in range(size)]
    for row in range(size):
        for column in range(size):
            mixed[row][column] = components[row].core_boundary_linking if row == column else 2 * core[row][column]
    full = [core[row] + mixed[row] for row in range(size)] + [[mixed[column][row] for column in range(size)] + boundary[row] for row in range(size)]
    core_order = tuple(carriers)
    boundary_order = tuple((item.component_id for item in components))
    return BoundaryLinkCertificate(prime=ribbon.prime, components=components, core_matrix=_integer_matrix_invariant(core_order, core), boundary_matrix=_integer_matrix_invariant(boundary_order, boundary), mixed_core_boundary_block=tuple((tuple(row) for row in mixed)), full_core_boundary_matrix=_integer_matrix_invariant(core_order + boundary_order, full))
