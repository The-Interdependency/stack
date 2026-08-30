"""Catalog-bound quantum-magnetism application-module vertical slice."""

# === MODULE_BUILD ===
# id: metapat_quantum_magnetism_application
#   module_name: metapat.quantum_magnetism
#   module_kind: schema
#   summary: materializes the quantum-magnetism worked note as a strict cross-domain application module bound to exact catalog module identities and evidence limits
#   owner: The Interdependency
#   public_surface: QUANTUM_MAGNETISM_APPLICATION_VERSION, QUANTUM_MAGNETISM_BINDING_SPECS, quantum_magnetism_application_module, quantum_magnetism_application_digest
#   internal_surface: source declarations and application mapping constants
#   auth_boundary: none
#   storage_boundary: serialization-only and read-only source verification
#   network_boundary: none
#   user_data_boundary: public worked physics application text only
#   admin_only: false
#   tests: tests.test_application, tests.test_quantum_magnetism
#   rollout: importable package constructor and packaged fixture
#   rollback: remove application exports and fixture while preserving generic application schema and canonical catalog
#   requires: metapat_application_module_schema, metapat_semantic_catalog
#   since: 2026-07-21
#   unresolved: field-space remains ambiguous among physical field, configuration space, and general potential-state landscape
# === END MODULE_BUILD ===

# === DOCS ===
# id: metapat_quantum_magnetism_docs
#   summary: binds the worked quantum-magnetism application to exact catalog modules while preserving scale, transfer, non-transfer, and physics evidence boundaries
#   audience: developer, physicist, domain reviewer, agent
#   source: docs/applications/quantum-magnetism.md
#   covers: quantum_magnetism_application_module, catalog bindings, source integrity, evidence boundary
#   status: current
# === END DOCS ===

# === CAPABILITIES ===
# id: metapat_quantum_magnetism_fixture
#   summary: emits one deterministic catalog-bound application record for nuclear charge configuration and magnetic state formation
#   exposes: metapat.quantum_magnetism_application_module
#   inputs: canonical semantic catalog v2
#   outputs: strict cross-domain application module and deterministic digest
#   boundaries: auth:none, storage:serialization-only, network:none, user_data:public application text only
# === END CAPABILITIES ===

# === BOUNDARIES ===
# id: metapat_quantum_magnetism_boundary
#   summary: worked semantic mapping only; physics remains answerable to physics and no root, proof, measurement, UCNS topology, or theorem-status claim is made
#   auth_boundary: none
#   storage_boundary: serialization-only and read-only source verification
#   network_boundary: none
#   user_data_boundary: public application text only
#   admin_only: false
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: metapat_quantum_application_catalog_bound
#   given: the quantum-magnetism application module is constructed
#   then: every applied METAPAT term is bound to an exact catalog module digest and declared claim status
#   class: integration_contract
#
# id: metapat_quantum_application_status_preserved
#   given: the application module and its catalog bindings are inspected
#   then: application status remains CROSS-DOMAIN-HYPOTHESIS, root impact remains none, and theory 10 is not imported
#   class: boundary_contract
#
# id: metapat_quantum_application_scales_distinct
#   given: selected physical scales and transfer limits are inspected
#   then: nuclear, atomic, crystalline, and magnetic-domain scales remain distinct and component identity is not inferred across scales
#   class: domain_boundary
#
# id: metapat_quantum_application_physics_firewall
#   given: the application evidence fields are inspected
#   then: physics claims remain answerable to physics and all METAPAT, domain, measurement, theorem-transfer, and UCNS-topology validation claims remain false
#   class: boundary_contract
#
# id: metapat_quantum_application_source_current
#   given: the application constructor and source document are checked together
#   then: exact identity, catalog-binding, mapping, transfer, evidence, and hmmm statements remain source-current
#   class: provenance_contract
# === END CONTRACTS ===

from __future__ import annotations

from .application import (
    MetapatApplicationModule,
    bind_catalog_module,
    validate_application_against_catalog,
)
from .catalog import MetapatSemanticCatalog, canonical_semantic_catalog, semantic_module_by_id

QUANTUM_MAGNETISM_APPLICATION_VERSION = "quantum-magnetism-application-v2"
SOURCE_DOCUMENT = "docs/applications/quantum-magnetism.md"

QUANTUM_MAGNETISM_BINDING_SPECS = (
    (
        "metapat.axiom.0.root_untouchable",
        "domain-restraint",
        "METAPAT supplies a bounded question-form and does not replace physical theory.",
    ),
    (
        "metapat.postulate.1.domain_similarity",
        "shared-question-form",
        "Similarly shaped transformations may be compared while the physical scales and domains remain distinct.",
    ),
    (
        "metapat.postulate.2.explicationary_use",
        "explicationary-restraint",
        "METAPAT terminology clarifies the application and does not replace equations, measurements, or physics evidence.",
    ),
    (
        "metapat.axiom.4.tensor",
        "tensor",
        "The simultaneous nuclear, electronic, lattice, and field-state arrangement at the selected scale.",
    ),
    (
        "metapat.axiom.6.relation",
        "relation",
        "Configured charge, position, spin, coupling, and material context within that tensor.",
    ),
    (
        "metapat.axiom.7.gradient",
        "gradient",
        "Readable potential difference within those relations.",
    ),
    (
        "metapat.axiom.2.boundary",
        "boundary-simplex",
        "A nuclear, atomic, crystalline, or magnetic-domain configuration that modifies passage, state selection, or transformation outcome.",
    ),
    (
        "metapat.axiom.5.energy_state",
        "energy-state",
        "An allowed electronic state or collective magnetic state within the application model.",
    ),
    (
        "metapat.axiom.8.transformation",
        "transformation",
        "Alteration of electronic occupation, spin organization, or magnetic-domain configuration.",
    ),
    (
        "metapat.theory.2.boundary_mediated_transformation",
        "boundary-mediated-transformation",
        "Changing a modeled boundary state may change passage, permitted state selection, delay, filtering, propagation, or transformation outcome.",
    ),
    (
        "metapat.theory.5.relational_gradient_selection",
        "relational-gradient-selection",
        "Direction and state selection are asked through the complete relation, boundary state, and tensor arrangement rather than difference alone.",
    ),
    (
        "metapat.theory.11.cross_domain_question_forms",
        "cross-domain-question-form",
        "The application asks one shared question-form across nuclear, atomic, crystalline, and magnetic-domain scales without making those scales identical.",
    ),
)

DOMAINS = (
    "atomic physics",
    "quantum mechanics",
    "condensed-matter physics",
    "magnetism",
)
SELECTED_SCALES = ("nuclear", "atomic", "crystalline", "magnetic-domain")
DOMAIN_STATEMENTS = (
    "A nucleus's proton charge distribution contributes to the electrostatic potential-energy term within the Hamiltonian that constrains permitted electronic quantum states.",
    "At ordinary atomic scales, total proton number \\(Z\\) is the dominant nuclear fact: it determines the element and strongly structures its electronic states. Most atomic electrons do not resolve individual proton positions. Detailed nuclear size, shape, spin, and magnetic moment produce smaller finite-size and hyperfine effects.",
    "For iron, nuclear charge establishes the atomic species and makes its electronic structure possible. Ferromagnetism in solid iron arises farther downstream through the collective electronic and material configuration, including electronic band structure, exchange interaction, crystal geometry, spin-orbit coupling, and magnetic-domain organization.",
    "The nucleus therefore does not mechanically lock an electron into a classical orbit. An electron occupies a quantum state permitted by the complete physical Hamiltonian.",
)
SHARED_QUESTION_FORM = (
    "configured source",
    "-> relational potential",
    "-> constrained permitted states",
    "-> collective state selection",
    "-> transformation",
)
TRANSFERS = (
    "Source configuration can affect the relational potential experienced downstream.",
    "A potential gradient constrains possible direction, transition, and state occupation.",
    "Larger tensor and boundary configurations can select collective behavior not attributable to one component alone.",
    "The same question-form can be asked at nuclear, atomic, crystalline, and domain scales while preserving their differences.",
)
DOES_NOT_TRANSFER = (
    "Electrons are classical particles traveling in fixed circular orbits.",
    "Detailed proton geometry alone explains ordinary electronic structure or iron ferromagnetism.",
    "A one-to-one identity exists between a METAPAT simplex and a fundamental particle.",
    "Structural resonance between METAPAT and quantum mechanics proves either framework.",
    "METAPAT terminology replaces the equations, measurements, or evidentiary standards of physics.",
)
WORKING_QUESTION = "What configured relations and boundary states determine which electronic and collective magnetic transformations are permitted at the selected scale?"
EVIDENCE_BOUNDARY = "The physics claims remain answerable to atomic physics, quantum mechanics, and condensed-matter evidence. METAPAT supplies a bounded cross-domain question-form and semantic mapping, not independent empirical proof."
EVIDENCE_REQUIREMENTS = (
    "A precise definition of each selected physical scale and modeled boundary.",
    "An explicit mapping from the physical Hamiltonian and material variables to the proposed METAPAT relations and gradients.",
    "Predictions that distinguish this mapping from a restatement of established physics.",
    "Comparison with experimental or computational results under declared uncertainty.",
)
UNRESOLVED = (
    "hmmm: “Field-space” remains unresolved among physical spatial field, quantum configuration space, and a general potential-state landscape; the intended physical quantity must be named rather than silently joining those meanings.",
)


def _catalog_binding_rows() -> tuple[str, ...]:
    return tuple(
        f"| `{module_id}` | {role} | {statement} |"
        for module_id, role, statement in QUANTUM_MAGNETISM_BINDING_SPECS
    )


def _source_pairs() -> tuple[tuple[str, str], ...]:
    pairs: list[tuple[str, str]] = [
        ("application-identity", "Status: **CROSS-DOMAIN-HYPOTHESIS / worked physics application**"),
        ("application-identity", "Root impact: **none**"),
    ]
    pairs.extend(("catalog-bindings", row) for row in _catalog_binding_rows())
    pairs.extend(("domain-statement", statement) for statement in DOMAIN_STATEMENTS)
    pairs.extend(("shared-question-form", line) for line in SHARED_QUESTION_FORM)
    pairs.extend(
        (
            "metapat-mapping",
            f"- **{role.replace('-', ' ').title()}:** {statement}",
        )
        for _module_id, role, statement in QUANTUM_MAGNETISM_BINDING_SPECS[3:9]
    )
    pairs.extend(("transfers", f"- {statement}") for statement in TRANSFERS)
    pairs.extend(("does-not-transfer", f"- {statement}") for statement in DOES_NOT_TRANSFER)
    pairs.append(("working-question", WORKING_QUESTION))
    pairs.append(("evidence-boundary", EVIDENCE_BOUNDARY))
    pairs.extend(
        ("evidence-boundary", f"{index}. {statement}")
        for index, statement in enumerate(EVIDENCE_REQUIREMENTS, start=1)
    )
    pairs.append(("hmmm", UNRESOLVED[0].removeprefix("hmmm: ")))
    return tuple(pairs)


def quantum_magnetism_application_module(
    catalog: MetapatSemanticCatalog | None = None,
) -> MetapatApplicationModule:
    selected = catalog or canonical_semantic_catalog()
    bindings = tuple(
        bind_catalog_module(
            semantic_module_by_id(module_id, selected),
            application_role=role,
            application_statement=statement,
        )
        for module_id, role, statement in QUANTUM_MAGNETISM_BINDING_SPECS
    )
    source_pairs = _source_pairs()
    refs = tuple(
        f"{SOURCE_DOCUMENT}#{anchor}::statement-{index}"
        for index, (anchor, _statement) in enumerate(source_pairs, start=1)
    )
    application = MetapatApplicationModule(
        application_id="metapat.application.quantum_magnetism",
        application_version=QUANTUM_MAGNETISM_APPLICATION_VERSION,
        title="Nuclear Charge Configuration and Magnetic State Formation",
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


def quantum_magnetism_application_digest() -> str:
    return quantum_magnetism_application_module().application_digest


__all__ = [
    "QUANTUM_MAGNETISM_APPLICATION_VERSION",
    "QUANTUM_MAGNETISM_BINDING_SPECS",
    "quantum_magnetism_application_digest",
    "quantum_magnetism_application_module",
]
