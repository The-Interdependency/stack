"""Catalog-bound affixiation and time-agnostic harmonic-relation application."""

# === MODULE_BUILD ===
# id: metapat_affixiation_harmonics_application
#   module_name: metapat.affixiation_harmonics
#   module_kind: schema
#   summary: defines catalog-bound conceptual semantics for identity-preserving affixiation and time-agnostic harmonic relation while leaving UCNS implementation and EDCM measurement authority downstream
#   owner: The Interdependency
#   public_surface: AFFIXIATION_HARMONICS_APPLICATION_VERSION, AFFIXIATION_HARMONICS_BINDING_SPECS, affixiation_harmonics_application_module, affixiation_harmonics_application_digest
#   internal_surface: source declarations and application mapping constants
#   auth_boundary: none
#   storage_boundary: serialization-only and read-only source verification
#   network_boundary: none
#   user_data_boundary: public conceptual application text only
#   admin_only: false
#   tests: tests.test_affixiation_harmonics
#   rollout: importable catalog-bound application module
#   rollback: remove application module and documentation while preserving canon and the generic application schema
#   requires: metapat_application_module_schema, metapat_semantic_catalog
#   since: 2026-08-20
#   unresolved: UCNS harmonic notation and EDCM measurement validity remain downstream; promotion into postulate or theory remains unresolved
# === END MODULE_BUILD ===

# === DOCS ===
# id: metapat_affixiation_harmonics_docs
#   summary: defines affixiation, time-agnostic recurrence and oscillation, harmonic relation, resonance, and the METAPAT/UCNS/EDCM authority firewall
#   audience: developer, agent, UCNS consumer, EDCM consumer
#   source: docs/applications/affixiation-harmonics.md
#   covers: affixiation_harmonics_application_module, semantic definitions, authority boundaries, downstream evidence requirements
#   status: current
# === END DOCS ===

# === CAPABILITIES ===
# id: metapat_affixiation_harmonics_semantics
#   summary: emits one deterministic catalog-bound application record for affixiation and time-agnostic harmonic relation
#   exposes: metapat.affixiation_harmonics.affixiation_harmonics_application_module
#   inputs: canonical semantic catalog v2
#   outputs: strict cross-domain application module and deterministic digest
#   boundaries: auth:none, storage:serialization-only, network:none, user_data:public conceptual text only
# === END CAPABILITIES ===

# === BOUNDARIES ===
# id: metapat_affixiation_harmonics_boundary
#   summary: semantic question-form only; no canon amendment, UCNS topology or notation selection, EDCM measurement validation, physical-frequency claim, theorem transfer, or external truth claim
#   auth_boundary: none
#   storage_boundary: serialization-only and read-only source verification
#   network_boundary: none
#   user_data_boundary: public conceptual text only
#   admin_only: false
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: metapat_affixiation_harmonics_catalog_bound
#   given: the affixiation-harmonics application module is constructed
#   then: every applied METAPAT concept is bound to an exact catalog module identity, digest, and claim status
#   class: integration_contract
#
# id: metapat_affixiation_identity_preserved
#   given: affixiation semantics are inspected
#   then: participants remain individually addressable with identity and provenance preserved and no flattening or topology is implied
#   class: boundary_contract
#
# id: metapat_harmonics_time_agnostic
#   given: recurrence, oscillation, and harmonic semantics are inspected
#   then: an ordered non-temporal relational parameter is permitted without redefining time or implying physical frequency
#   class: boundary_contract
#
# id: metapat_affixiation_harmonics_authority_firewall
#   given: the application evidence and transfer boundaries are inspected
#   then: METAPAT owns semantic meaning, UCNS owns implementation, EDCM owns measurement, and no status transfers automatically
#   class: boundary_contract
#
# id: metapat_affixiation_harmonics_candidate_status
#   given: application status and unresolved fields are inspected
#   then: the application remains a cross-domain hypothesis with no root impact and no promotion into postulate or theory
#   class: canon_contract
#
# id: metapat_affixiation_harmonics_source_current
#   given: the application constructor and source document are checked together
#   then: exact definitions, catalog bindings, transfer limits, evidence boundaries, and hmmm statements remain source-current
#   class: provenance_contract
# === END CONTRACTS ===

from __future__ import annotations

from .application import (
    MetapatApplicationModule,
    bind_catalog_module,
    validate_application_against_catalog,
)
from .catalog import MetapatSemanticCatalog, canonical_semantic_catalog, semantic_module_by_id

AFFIXIATION_HARMONICS_APPLICATION_VERSION = "affixiation-harmonics-application-v1"
SOURCE_DOCUMENT = "docs/applications/affixiation-harmonics.md"

AFFIXIATION_HARMONICS_BINDING_SPECS = (
    (
        "metapat.axiom.0.root_untouchable",
        "domain-restraint",
        "Affixiation and harmonic terminology may organize a relational application without redefining the METAPAT root.",
    ),
    (
        "metapat.postulate.1.domain_similarity",
        "shared-question-form",
        "Recurrent relational structures may be compared across domains while the participating domains remain distinct.",
    ),
    (
        "metapat.postulate.2.explicationary_use",
        "explicationary-restraint",
        "Harmonic, oscillation, phase, and resonance are explicationary terms here and do not import physics or signal processing as root ontology.",
    ),
    (
        "metapat.axiom.4.tensor",
        "simultaneous-arrangement",
        "Affixiation begins from participants already addressable within a simultaneous tensor arrangement; temporal succession is not required for their relation to exist.",
    ),
    (
        "metapat.axiom.6.relation",
        "relation",
        "Affixiation and harmonic correspondence are readable configurations within tensor rather than identity claims about their participants.",
    ),
    (
        "metapat.axiom.9.time",
        "time-boundary",
        "Time remains sequential tensor alteration; a harmonic structure may be parameterized over a non-temporal ordered relation without thereby becoming time.",
    ),
    (
        "metapat.postulate.3.formed_objects",
        "formed-object",
        "A relation among already-bounded participants may become object-whole only at a declared native scale rather than merely because the participants are associated.",
    ),
    (
        "metapat.postulate.4.integration",
        "integration",
        "Affixiation may integrate a declared relation as a higher-scale object-whole while retaining the addressable identities of its participants.",
    ),
    (
        "metapat.theory.3.tensor_first_arrangement",
        "tensor-first",
        "Simultaneous arrangement permits relational structure before sequential alteration and therefore before a temporal interpretation is required.",
    ),
    (
        "metapat.theory.5.relational_gradient_selection",
        "relational-structure",
        "Harmonic correspondence is interpreted through the complete declared relation rather than through one scalar difference alone.",
    ),
    (
        "metapat.theory.6.time_as_sequential_tensor_alteration",
        "time-separation",
        "Traversal of an ordered relational parameter must not be silently equated with physical or experiential time.",
    ),
    (
        "metapat.theory.9.native_scale_object_integration",
        "recursive-scale",
        "An affixiated whole may become a bounded participant in a later relation only after its own native-scale integration remains explicit.",
    ),
    (
        "metapat.theory.11.cross_domain_question_forms",
        "cross-domain-question-form",
        "Time-agnostic harmonic language may compare recurrent relation-shapes across modalities while preserving what remains modality-specific.",
    ),
)

DOMAINS = (
    "relational systems",
    "multimodal representation",
    "computation",
    "harmonic analysis",
)
SELECTED_SCALES = (
    "participant",
    "declared-relation",
    "integrated-whole",
    "recursive-higher-scale",
)
DOMAIN_STATEMENTS = (
    "Affixiation is the application-layer name for a declared relation in which already-bounded participants remain individually addressable, with their identities and provenance preserved, while the relation may integrate as a higher-scale object-whole.",
    "An affixiated whole may itself become a bounded participant in a later declared relation. Recursive participation does not erase the identities or provenance of the constituents from which the higher-scale whole was constructed.",
    "A recurrent relation is one in which equivalent relational states or configurations reappear under traversal of a declared ordered parameter.",
    "Oscillation is recurrence among distinguishable relational states under such a traversal.",
    "A harmonic relation is a proposed correspondence among recurrent structures whose declared parameterizations admit a repeatable commensurability, phase relation, ratio, symmetry, inversion, or other explicitly stated recurrence mapping.",
    "Resonance names a proposed stable coupling among such recurrent relational structures under declared boundary and scale conditions.",
)
SHARED_QUESTION_FORM = (
    "addressable participants",
    "-> declared relation",
    "-> declared ordered parameter or parameters",
    "-> recurrent structure",
    "-> harmonic correspondence or non-correspondence",
    "-> possible native-scale integration",
    "-> recursively addressable whole",
)
TRANSFERS = (
    "Participants may preserve identity and provenance while entering a higher-order declared relation.",
    "A higher-order relation may become object-whole at a declared native scale without requiring its constituents to become identical.",
    "Recurrence and oscillation may be expressed over a declared ordered parameter other than time.",
    "Harmonic language may compare recurrence, phase, ratio, inversion, symmetry, and coupling across modalities when the mapping is explicit.",
    "A successfully integrated affixiated whole may itself participate recursively at another scale.",
)
DOES_NOT_TRANSFER = (
    "Affixiation does not by itself select a UCNS carrier, containment rule, geometry, coordinate law, or harmonic notation.",
    "Harmonic relation does not imply a physical frequency or a signal evolving through time.",
    "Resonance does not mean identity, consensus, truth, causal influence, consciousness, or empirical validity.",
    "Multimodal relation does not permit flattening distinct modalities into an undeclared common representation.",
    "METAPAT semantic declaration does not establish UCNS theorem status, construction correctness, EDCM measurement validity, or external domain truth.",
)
WORKING_QUESTION = "What identities remain, what declared relation binds them, over what ordered parameter does recurrence occur, what harmonic correspondence is actually specified, and under what condition—if any—does that relation integrate as a new object-whole at its native scale?"
EVIDENCE_BOUNDARY = "This application defines semantic distinctions and question-forms only. UCNS owns any exact representation or executable construction of affixiation and harmonic relation. EDCM owns any explicit measurement projection used to interpret whether those constructions exhibit useful coherence, dissonance, recurrence, resonance, or multimodal behavior. Neither downstream surface may silently promote this application into METAPAT root or canon validity."
EVIDENCE_REQUIREMENTS = (
    "A UCNS candidate must preserve exact participant identity, provenance, relation identity, scale, and unresolved state rather than treating association as closure.",
    "Any harmonic candidate must declare the ordered parameter, recurrence mapping, equivalence condition, and information loss; time may not be inserted when the parameter is non-temporal.",
    "Multimodal construction must preserve modality-specific identity while making the cross-modal relation explicit and independently replayable.",
    "Any EDCM interpretation must preregister the observable or measurement projection and distinguish represented structure from measured evidence.",
    "Independent reconstruction or replay must be possible before a claimed relation is promoted beyond candidate standing.",
)
UNRESOLVED = (
    "hmmm: No UCNS harmonic-resonance notation is selected. Phase, ratio, orientation, recurrence, scale, and coupling fields remain implementation candidates rather than METAPAT-mandated coordinates.",
    "hmmm: No EDCM measurement validity is established for coherence, dissonance, recurrence, resonance, or multimodal usefulness merely because the semantic distinctions are now addressable.",
    "hmmm: Whether affixiation and time-agnostic harmonic relation should later be promoted from application terminology into METAPAT postulates or theories remains unresolved and should depend on downstream construction, falsification, and independent recovery rather than naming preference.",
)


def _catalog_binding_rows() -> tuple[str, ...]:
    return tuple(
        f"| `{module_id}` | {role} | {statement} |"
        for module_id, role, statement in AFFIXIATION_HARMONICS_BINDING_SPECS
    )


def _source_pairs() -> tuple[tuple[str, str], ...]:
    pairs: list[tuple[str, str]] = [
        ("application-identity", "Status: **CROSS-DOMAIN-HYPOTHESIS / relational application**"),
        ("application-identity", "Root impact: **none**"),
        (
            "application-identity",
            "METAPAT owns the conceptual meaning declared here. UCNS may implement exact construction, geometry, notation, and provenance for these relations. EDCM may define and test explicit observational or measurement projections over those constructions. No UCNS implementation status or EDCM measurement status transfers into METAPAT validity, and METAPAT semantic authority does not validate UCNS mathematics or EDCM measurement.",
        ),
    ]
    pairs.extend(("catalog-bindings", row) for row in _catalog_binding_rows())
    pairs.extend(("affixiation", statement) for statement in DOMAIN_STATEMENTS[:2])
    pairs.extend(
        ("time-agnostic-recurrence-and-oscillation", statement)
        for statement in DOMAIN_STATEMENTS[2:4]
    )
    pairs.extend(
        ("harmonic-relation-and-resonance", statement)
        for statement in DOMAIN_STATEMENTS[4:]
    )
    pairs.extend(("shared-question-form", line) for line in SHARED_QUESTION_FORM)
    pairs.extend(("transfers", f"- {statement}") for statement in TRANSFERS)
    pairs.extend(("does-not-transfer", f"- {statement}") for statement in DOES_NOT_TRANSFER)
    pairs.append(("working-question", WORKING_QUESTION))
    pairs.append(("evidence-boundary", EVIDENCE_BOUNDARY))
    pairs.extend(
        ("evidence-boundary", f"{index}. {statement}")
        for index, statement in enumerate(EVIDENCE_REQUIREMENTS, start=1)
    )
    pairs.extend(("hmmm", item.removeprefix("hmmm: ")) for item in UNRESOLVED)
    return tuple(pairs)


def affixiation_harmonics_application_module(
    catalog: MetapatSemanticCatalog | None = None,
) -> MetapatApplicationModule:
    selected = catalog or canonical_semantic_catalog()
    bindings = tuple(
        bind_catalog_module(
            semantic_module_by_id(module_id, selected),
            application_role=role,
            application_statement=statement,
        )
        for module_id, role, statement in AFFIXIATION_HARMONICS_BINDING_SPECS
    )
    source_pairs = _source_pairs()
    refs = tuple(
        f"{SOURCE_DOCUMENT}#{anchor}::statement-{index}"
        for index, (anchor, _statement) in enumerate(source_pairs, start=1)
    )
    application = MetapatApplicationModule(
        application_id="metapat.application.affixiation_harmonics",
        application_version=AFFIXIATION_HARMONICS_APPLICATION_VERSION,
        title="Affixiation and Time-Agnostic Harmonic Relation",
        claim_status="CROSS-DOMAIN-HYPOTHESIS",
        domains=DOMAINS,
        selected_scales=SELECTED_SCALES,
        source_document=SOURCE_DOCUMENT,
        source_statement_refs=refs,
        source_statements=tuple(statement for _anchor, statement in source_pairs),
        catalog_version=selected.catalog_version,
        catalog_digest=selected.catalog_digest,
        catalog_bindings=bindings,
        domain_statements=DOMAIN_STATEMENTS,
        shared_question_form=SHARED_QUESTION_FORM,
        transfers=TRANSFERS,
        does_not_transfer=DOES_NOT_TRANSFER,
        working_question=WORKING_QUESTION,
        evidence_boundary=EVIDENCE_BOUNDARY,
        evidence_requirements=EVIDENCE_REQUIREMENTS,
        unresolved_constraints=UNRESOLVED,
    )
    validate_application_against_catalog(application, selected)
    return application


def affixiation_harmonics_application_digest() -> str:
    return affixiation_harmonics_application_module().application_digest


__all__ = [
    "AFFIXIATION_HARMONICS_APPLICATION_VERSION",
    "AFFIXIATION_HARMONICS_BINDING_SPECS",
    "affixiation_harmonics_application_digest",
    "affixiation_harmonics_application_module",
]
