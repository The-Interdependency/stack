# === MODULE_BUILD ===
# id: ucns_prime_interval_boundary_links_p7_p5
#   module_name: prime_interval_boundary_links
#   module_kind: experiment
#   summary: replays P7-first smooth-ribbon separation with outward-rounded interval arithmetic, extracts each Möbius ribbon's single continuous boundary, and computes boundary, mixed, component-knot, and length-three Milnor readouts before any spectral construction
#   owner: Erin Spencer
#   public_surface: IntervalPairCertificate, IntervalSeparationCertificate, BoundaryComponentInvariant, IntegerMatrixInvariant, BoundaryLinkCertificate, DiagramCrossing, GenericCoreDiagram, MilnorTripleInvariant, MilnorProfile, IntervalBoundaryCertificate, replay_interval_separation, extract_boundary_components, build_boundary_link_certificate, build_generic_core_diagram, compute_milnor_profile, certify_interval_boundary_prime_seven, certify_interval_boundary_prime_five, interval_boundary_family_certificate, interval_boundary_family_summary, write_interval_boundary_family_certificate, write_interval_boundary_family_summary, render_boundary_curve_obj
#   internal_surface: prime_interval_common, prime_interval_replay, prime_boundary_link_invariants, prime_generic_diagram, prime_milnor_invariants
#   auth_boundary: none
#   storage_boundary: caller-supplied local paths only through writer and renderer functions
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_interval_boundary_links.py
#   rollout: P7 first, P5 same-protocol comparison second; selection effect none; does not alter prior smooth-ribbon receipts
#   rollback: remove this facade and its five helper modules, test, documentation, generated certificate, and boundary models; revert the research/test optional dependencies
#   requires: ucns_prime_smooth_ribbons_p7_p5
#   since: 2026-08-11
#   unresolved: proof-assistant replay, simultaneous global projection regularization, length-four-and-higher Milnor invariants, whole-link ambient isotopy, multivariable Alexander or HOMFLYPT invariants, spectral operator, prime-power law, zeta correspondence
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: prime_interval_replay_is_outward_rounded
#   given: every complete P7 or P5 pair-parameter torus is replayed
#   then: elementary evaluations use directed interval endpoints and every accepted leaf has a rigorous lower endpoint strictly above nine hundredths at the declared precision
#   class: evidence
#   since: 2026-08-11
#
# id: prime_interval_replay_preserves_finite_width_disjointness
#   given: interval centerline clearance exceeds nine hundredths and half width is one hundredth
#   then: all distinct complete ribbons remain separated by more than seven hundredths
#   class: correctness
#   since: 2026-08-11
#
# id: prime_boundary_curve_is_single_and_closed
#   given: one Möbius ribbon is evaluated at positive boundary breadth over two carrier turns
#   then: it yields one closed boundary component with longitudinal winding two and odd meridional winding one plus twice the phase winding
#   class: correctness
#   since: 2026-08-11
#
# id: prime_boundary_component_knot_types_are_derived
#   given: each centerline is a vertical graph over a circle and hence an unknot
#   then: each boundary component is assigned its exact two-by-odd torus-cable type and Alexander, genus, determinant, and crossing-number readouts
#   class: evidence
#   since: 2026-08-11
#
# id: prime_boundary_linking_matrix_follows_cable_homology
#   given: distinct boundary components each carry longitudinal coefficient two
#   then: their pairwise linking matrix equals four times the core linking matrix and the mixed core-boundary off-diagonal block equals twice the core matrix
#   class: correctness
#   since: 2026-08-11
#
# id: prime_mixed_linking_matrix_has_exact_integer_invariants
#   given: core, boundary, and own-core boundary linkings are combined
#   then: rank, nullity, determinant, factorization, and Smith invariant factors are computed over the integers
#   class: evidence
#   since: 2026-08-11
#
# id: prime_length_three_milnor_profile_is_computed_after_global_lift
#   given: a clearance-preserving simultaneous generic projection is constructed
#   then: pairwise linking is unchanged and every integer-valued length-three Milnor invariant is computed by a truncated Magnus expansion validated on the Borromean braid
#   class: evidence
#   since: 2026-08-11
#
# id: prime_interval_boundary_p7_precedes_p5
#   given: the family certificate is built
#   then: P7 is interval-certified and analyzed first and P5 is independently processed second
#   class: doctrine
#   since: 2026-08-11
#
# id: prime_interval_boundary_receipt_is_nonselecting
#   given: the family receipt is serialized
#   then: it records dependency, precision, generic-projection, and invariant boundaries and claims no arithmetic redefinition, electron ontology, zeta theorem, or Riemann-hypothesis proof
#   class: doctrine
#   since: 2026-08-11
# === END CONTRACTS ===

"""P7-first interval, Möbius-boundary, and higher-link certificate."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
from pathlib import Path

from .prime_interval_common import (
    CENTERLINE_SEPARATION_TARGET,
    GENERIC_ISOTOPY_CLEARANCE,
    INTERVAL_DPS,
    RIBBON_SEPARATION_LOWER_BOUND,
    SCHEMA_ID,
    SCHEMA_VERSION,
    SOURCE_LINES,
    SOURCE_NAME,
    SOURCE_SHA256,
    IntervalBoundaryError,
    fraction_text,
)
from .prime_interval_replay import (
    IntervalPairCertificate,
    IntervalSeparationCertificate,
    replay_interval_separation,
)
from .prime_boundary_link_invariants import (
    BoundaryComponentInvariant,
    IntegerMatrixInvariant,
    BoundaryLinkCertificate,
    extract_boundary_components,
    build_boundary_link_certificate,
)
from .prime_generic_diagram import (
    DiagramCrossing,
    GenericCoreDiagram,
    build_generic_core_diagram,
)
from .prime_milnor_invariants import (
    MilnorTripleInvariant,
    MilnorProfile,
    compute_milnor_profile,
)
from .prime_smooth_ribbons import (
    SmoothPrimeRibbon,
    build_smooth_prime_five,
    build_smooth_prime_seven,
    certify_smooth_prime_five,
    certify_smooth_prime_seven,
)

@dataclass(frozen=True, slots=True)
class IntervalBoundaryCertificate:
    ribbon: SmoothPrimeRibbon
    interval_separation: IntervalSeparationCertificate
    boundary_link: BoundaryLinkCertificate
    milnor_profile: MilnorProfile

    @property
    def payload(self) -> dict[str, object]:
        payload: dict[str, object] = {'schema_id': SCHEMA_ID, 'schema_version': SCHEMA_VERSION, 'authority': 'Erin Spencer', 'recorded_on': '2026-08-11', 'selection_effect': 'none', 'prime': self.ribbon.prime, 'source': {'name': SOURCE_NAME, 'sha256': SOURCE_SHA256, 'line_basis': list(SOURCE_LINES)}, 'construction_lineage': 'global prime primitive, phase, lift, and smooth ribbon first; boundary and higher-link readouts derived afterward', 'interval_separation': self.interval_separation.as_dict(), 'ribbon_boundary_link': self.boundary_link.as_dict(), 'length_three_Milnor_profile': self.milnor_profile.as_dict(), 'findings': {'complete_distinct_ribbons_interval_separated': True, 'one_boundary_component_per_Mobius_ribbon': True, 'P7_center_boundary_type' if self.ribbon.prime == 7 else 'P5_center_boundary_type': self.boundary_link.components[0].knot_type, 'all_informative_core_length_three_Milnor_values_zero': not self.milnor_profile.nonzero_integer_values}, 'unresolved': ['proof-assistant replay of mpmath interval endpoint semantics and every leaf', 'one simultaneous projection regularization for every optional diagram readout', 'length-four and higher Milnor invariants', 'whole multi-component ambient-isotopy classification', 'multivariable Alexander, HOMFLYPT, and boundary-surface complement invariants', 'spectral operator and prime-power law', 'zeta-zero correspondence'], 'nonclaims': ['not a redefinition of arithmetic primality', 'not an established electron ontology or Pauli-exclusion derivation', 'not a complete link classification', 'not a zeta-function theorem or proof of the Riemann hypothesis', 'not EDCM or METAPAT validity']}
        canonical = json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
        payload['payload_sha256'] = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
        return payload

    def json_text(self, *, indent: int=2) -> str:
        return json.dumps(self.payload, indent=indent, sort_keys=True, ensure_ascii=False) + '\n'

def _certify_interval_boundary(ribbon: SmoothPrimeRibbon) -> IntervalBoundaryCertificate:
    interval = replay_interval_separation(ribbon)
    boundary = build_boundary_link_certificate(ribbon)
    diagram = build_generic_core_diagram(ribbon)
    milnor = compute_milnor_profile(ribbon, diagram)
    return IntervalBoundaryCertificate(ribbon, interval, boundary, milnor)

@lru_cache(maxsize=1)
def certify_interval_boundary_prime_seven() -> IntervalBoundaryCertificate:
    return _certify_interval_boundary(certify_smooth_prime_seven().ribbon)

@lru_cache(maxsize=1)
def certify_interval_boundary_prime_five() -> IntervalBoundaryCertificate:
    return _certify_interval_boundary(certify_smooth_prime_five().ribbon)

def interval_boundary_family_certificate() -> dict[str, object]:
    p7 = certify_interval_boundary_prime_seven()
    p5 = certify_interval_boundary_prime_five()
    payload: dict[str, object] = {'schema_id': f'{SCHEMA_ID}.family', 'schema_version': SCHEMA_VERSION, 'authority': 'Erin Spencer', 'recorded_on': '2026-08-11', 'selection_effect': 'none', 'research_order': [7, 5], 'source': {'name': SOURCE_NAME, 'sha256': SOURCE_SHA256, 'line_basis': list(SOURCE_LINES)}, 'dependencies': {'mpmath': '>=1.3,<2 for directed interval endpoints', 'sympy': '>=1.12,<2 for exact Smith normal form'}, 'p7': p7.payload, 'p5': p5.payload, 'comparison': {'interval_centerline_target': fraction_text(CENTERLINE_SEPARATION_TARGET), 'finite_width_ribbon_lower_bound': fraction_text(RIBBON_SEPARATION_LOWER_BOUND), 'P7_full_mixed_matrix_determinant': p7.boundary_link.full_core_boundary_matrix.determinant, 'P5_full_mixed_matrix_determinant': p5.boundary_link.full_core_boundary_matrix.determinant, 'P7_full_mixed_Smith_factors': list(p7.boundary_link.full_core_boundary_matrix.smith_nonzero_invariant_factors), 'P5_full_mixed_Smith_factors': list(p5.boundary_link.full_core_boundary_matrix.smith_nonzero_invariant_factors), 'P7_informative_length_three_Milnor_values': [item.value for item in p7.milnor_profile.integer_valued_triples], 'P5_informative_length_three_Milnor_values': [item.value for item in p5.milnor_profile.integer_valued_triples], 'phase_law_warning': 'both selected candidates have center phase winding three and therefore the same T(2,7) center-boundary component; this boundary knot type alone does not encode the prime label'}, 'next': 'compute length-four Milnor and multivariable Alexander-type invariants, then seek a proof-assistant replay before any spectral object', 'nonclaims': ['no arithmetic redefinition', 'no electron ontology', 'no complete ambient-isotopy classification', 'no zeta theorem', 'no proof of the Riemann hypothesis']}
    canonical = json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    payload['payload_sha256'] = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    return payload

def interval_boundary_family_summary() -> dict[str, object]:
    """Return a compact deterministic publication summary of the expanded receipt."""
    expanded = interval_boundary_family_certificate()

    def prime_summary(key: str) -> dict[str, object]:
        item = expanded[key]
        interval = item['interval_separation']
        boundary = item['ribbon_boundary_link']
        milnor = item['length_three_Milnor_profile']
        full = boundary['full_core_boundary_pairwise_linking']
        boundary_matrix = boundary['boundary_pairwise_linking']
        informative = [{'triple': triple['ordered_triple'], 'value': triple['mu_bar_123']} for triple in milnor['triples'] if triple['integer_valued']]
        return {'prime': item['prime'], 'interval_replay': {'method': interval['method'], 'decimal_precision': interval['decimal_precision'], 'pair_count': interval['pair_count'], 'boxes_evaluated': interval['total_boxes_evaluated'], 'maximum_depth': interval['maximum_depth'], 'minimum_leaf_lower_bound_decimal': interval['minimum_leaf_lower_bound_decimal'], 'centerline_target': interval['centerline_target'], 'finite_width_ribbon_separation_lower_bound': interval['finite_width_ribbon_separation_lower_bound'], 'all_pairs_certified': interval['all_pairs_certified']}, 'boundary_components': [{'component': component['boundary_component'], 'slope': component['tubular_slope'], 'knot_type': component['component_knot_type'], 'core_boundary_linking': component['core_boundary_linking']} for component in boundary['components']], 'boundary_linking_matrix': {'rank_over_Q': boundary_matrix['rank_over_Q'], 'nullity_over_Q': boundary_matrix['nullity_over_Q'], 'Smith_nonzero_invariant_factors': boundary_matrix['Smith_nonzero_invariant_factors']}, 'full_core_boundary_matrix': {'rank_over_Q': full['rank_over_Q'], 'nullity_over_Q': full['nullity_over_Q'], 'determinant': full['determinant'], 'absolute_determinant_factorization': full['absolute_determinant_factorization'], 'Smith_nonzero_invariant_factors': full['Smith_nonzero_invariant_factors']}, 'generic_core_diagram': {'crossing_count': milnor['generic_core_diagram']['crossing_count'], 'minimum_turn_gap_decimal': milnor['generic_core_diagram']['minimum_distinct_crossing_turn_gap_decimal'], 'minimum_height_gap_decimal': milnor['generic_core_diagram']['minimum_crossing_height_gap_decimal'], 'residual_ribbon_clearance': milnor['generic_core_diagram']['residual_complete_ribbon_clearance']}, 'length_three_Milnor': {'total_component_triples': milnor['total_component_triples'], 'integer_valued_algebraically_split_triples': milnor['integer_valued_algebraically_split_triples'], 'nonzero_integer_values': milnor['nonzero_integer_length_three_invariants'], 'informative_triples': informative, 'Borromean_regression': milnor['Borromean_regression']}, 'expanded_prime_payload_sha256': item['payload_sha256']}
    payload: dict[str, object] = {'schema_id': f'{SCHEMA_ID}.family.summary', 'schema_version': SCHEMA_VERSION, 'authority': expanded['authority'], 'recorded_on': expanded['recorded_on'], 'selection_effect': 'none', 'research_order': [7, 5], 'source': expanded['source'], 'dependencies': expanded['dependencies'], 'p7': prime_summary('p7'), 'p5': prime_summary('p5'), 'comparison': expanded['comparison'], 'next': expanded['next'], 'nonclaims': expanded['nonclaims'], 'expanded_family_payload_sha256': expanded['payload_sha256']}
    canonical = json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    payload['payload_sha256'] = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    return payload

def write_interval_boundary_family_summary(path: str | Path, *, indent: int=2) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(interval_boundary_family_summary(), indent=indent, sort_keys=True, ensure_ascii=False) + '\n', encoding='utf-8')
    return output

def write_interval_boundary_family_certificate(path: str | Path, *, indent: int=2) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(interval_boundary_family_certificate(), indent=indent, sort_keys=True, ensure_ascii=False) + '\n', encoding='utf-8')
    return output

def render_boundary_curve_obj(ribbon: SmoothPrimeRibbon, *, longitudinal_samples: int=2048) -> str:
    if isinstance(longitudinal_samples, bool) or not isinstance(longitudinal_samples, int) or longitudinal_samples < 64:
        raise IntervalBoundaryError('boundary OBJ requires at least 64 samples')
    lines = [f'# UCNS P{ribbon.prime} single continuous Mobius ribbon boundaries', '# Each group traverses breadth +w over two carrier turns.']
    vertex_offset = 1
    for carrier in ribbon.carriers:
        lines.append(f'o P{ribbon.prime}_boundary_{carrier}')
        indices: list[int] = []
        for sample in range(longitudinal_samples):
            turn = Fraction(2 * sample, longitudinal_samples)
            x, y, z = ribbon.surface_point(carrier, turn, ribbon.half_width)
            lines.append(f'v {x:.17g} {y:.17g} {z:.17g}')
            indices.append(vertex_offset + sample)
        indices.append(indices[0])
        lines.append('l ' + ' '.join(map(str, indices)))
        vertex_offset += longitudinal_samples
    return '\n'.join(lines) + '\n'
