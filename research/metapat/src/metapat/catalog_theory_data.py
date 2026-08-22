"""Static theory and declared-derivation data for the semantic catalog."""

# === MODULE_BUILD ===
# id: metapat_semantic_theory_declarations
#   module_name: metapat.catalog_theory_data
#   module_kind: schema
#   summary: declares stable theory module identities, exact claim statements, and source-declared derivation ancestry
#   owner: The Interdependency
#   public_surface: none
#   internal_surface: THEORY_SPECS, CATALOG_DERIVATIONS, CATALOG_DERIVED_TEXT
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: exact canon statements only
#   admin_only: false
#   tests: tests.test_catalog
#   rollout: internal catalog constructor dependency
#   rollback: remove only with semantic catalog
#   requires: metapat_canon_core
#   since: 2026-07-21
#   unresolved: theory 10 remains cross-domain hypothesis and theory 11 remains domain-restraint bounded
# === END MODULE_BUILD ===

THEORY_SPECS = (
    ("metapat.theory.0.root_prior_restraint", "theory", "theory", "INTERNAL-DERIVATION", "THEORIES.md", "0-theory-of-root-prior-restraint", (
        "Energy Theory can learn from any domain without being owned by that domain.",
        "Domains may supply tools, examples, metaphors, measurements, and question-forms.",
        "Domains may not redefine the root.",
    ), ()),
    ("metapat.theory.1.distinction_formation", "theory", "theory", "INTERNAL-DERIVATION", "THEORIES.md", "1-theory-of-distinction-formation", (
        "Legible difference generates distinction.",
        "Distinction defines boundary.",
        "Boundary defines simplex.",
        "A simplex is therefore not merely an object already sitting in a domain. A simplex is the bounded state-bearing result of legible distinction.",
    ), ()),
    ("metapat.theory.2.boundary_mediated_transformation", "theory", "theory", "INTERNAL-DERIVATION", "THEORIES.md", "2-theory-of-boundary-mediated-transformation", (
        "Boundary is not passive edge.",
        "Boundary is a state-bearing simplex whose configuration may alter passage, relation, gradient dynamics, vector direction, delay, filtering, propagation, or transformation outcome.",
    ), ()),
    ("metapat.theory.3.tensor_first_arrangement", "theory", "theory", "INTERNAL-DERIVATION", "THEORIES.md", "3-theory-of-tensor-first-arrangement", (
        "Tensor is primitive simultaneous arrangement of energy-states.",
        "Time is not the first condition.",
        "Time appears when tensor alteration becomes sequential.",
        "Without sequence, there is not nothingness.",
        "Without sequence, there is tensor.",
    ), ()),
    ("metapat.theory.4.energy_state_motion", "theory", "theory", "INTERNAL-DERIVATION", "THEORIES.md", "4-theory-of-energy-state-motion", (
        "Energy appears as state of being.",
        "Energy-state held is scalar.",
        "Energy-state motioned is vector.",
        "Energy-state vectors alter energy-state scalars.",
        "Transformation is vector-compelled alteration of energy-state.",
    ), ()),
    ("metapat.theory.5.relational_gradient_selection", "theory", "theory", "INTERNAL-DERIVATION", "THEORIES.md", "5-theory-of-relational-gradient-selection", (
        "Relation is readable configuration within tensor.",
        "Gradient is readable difference within relation.",
        "Gradient dynamics select vector direction through tensor arrangement, simplex relations, and boundary-simplex states.",
        "A vector does not select direction from difference alone.",
    ), ()),
    ("metapat.theory.6.time_as_sequential_tensor_alteration", "theory", "theory", "INTERNAL-DERIVATION", "THEORIES.md", "6-theory-of-time-as-sequential-tensor-alteration", (
        "Time is sequential tensor alteration.",
        "Registration is not the parent of time.",
        "A sequence can occur without being preserved, narrated, or consciously observed.",
    ), ()),
    ("metapat.theory.7.registration_and_observer_roles", "theory", "theory", "INTERNAL-DERIVATION", "THEORIES.md", "7-theory-of-registration-and-observer-roles", (
        "Registration is the capacity of a simplex to preserve, express, or transmit sequential tensor alteration.",
        "An observer is a simplex performing registration.",
        "An observer need not be conscious.",
        "Consciousness is one possible observer-mode.",
        "Story is conscious registration of time.",
    ), ()),
    ("metapat.theory.8.questions_as_bounded_unresolved_energy_state", "theory", "theory", "INTERNAL-DERIVATION", "THEORIES.md", "8-theory-of-questions-as-bounded-unresolved-energy-state", (
        "A question is a bounded unresolved energy-state.",
        "Energy Theory is not first an answer-machine.",
        "Energy Theory is a question-finder.",
    ), ()),
    ("metapat.theory.9.native_scale_object_integration", "theory", "theory", "INTERNAL-DERIVATION", "THEORIES.md", "9-theory-of-native-scale-object-integration", (
        "A formed object is a tensor of simplexes integrated at a scale.",
        "Object-instantiation requires integration at its native scale, not consciousness.",
        "A physical object may require physical and spatial simplexes.",
        "A mental object may require archetype, concept, idea, and gestalt simplexes.",
        "A cognitive gestalt may register object-whole without creating physical objecthood.",
    ), ()),
    ("metapat.theory.10.symbolic_and_memetic_transfer", "theory", "theory", "CROSS-DOMAIN-HYPOTHESIS", "THEORIES.md", "10-theory-of-symbolic-and-memetic-transfer", (
        "Thought does not transfer thought directly.",
        "Thought emits symbolic form.",
        "Symbolic form perturbs a receiver.",
        "A reconstructed thought appears only if the receiving simplex or tensor can register, relate, and resolve the pattern.",
        "Words, marks, gestures, numerals, operators, spacing, rhythm, and silence may function as symbolic boundary-simplexes.",
    ), ("hmmm: symbolic vertex tables, receiver registration tests, and UCNS-gonol mappings are not yet specified.",)),
    ("metapat.theory.11.cross_domain_question_forms", "theory", "theory", "INTERNAL-DERIVATION", "THEORIES.md", "11-theory-of-cross-domain-question-forms", (
        "Different domains may show similarly shaped transformations.",
        "Energy Theory may compare those shapes to find shared question-forms.",
        "The comparison does not make the domains identical.",
    ), ("hmmm: this theory remains valid only while domain restraint is explicit.",)),
)

CATALOG_DERIVATIONS = {
    "metapat.theory.0.root_prior_restraint": ("metapat.axiom.0.root_untouchable", "metapat.postulate.1.domain_similarity", "metapat.postulate.2.explicationary_use", "metapat.theorem.5.root_and_tool_separation"),
    "metapat.theory.1.distinction_formation": ("metapat.axiom.1.legible_difference", "metapat.axiom.2.boundary", "metapat.axiom.3.simplex"),
    "metapat.theory.2.boundary_mediated_transformation": ("metapat.axiom.2.boundary", "metapat.axiom.3.simplex", "metapat.axiom.7.gradient", "metapat.axiom.8.transformation", "metapat.postulate.6.validation_by_boundary_change", "metapat.theorem.1.boundary_earns_its_keep"),
    "metapat.theory.3.tensor_first_arrangement": ("metapat.axiom.4.tensor", "metapat.axiom.9.time", "metapat.theorem.2.tensor_precedes_time"),
    "metapat.theory.4.energy_state_motion": ("metapat.axiom.5.energy_state", "metapat.axiom.8.transformation"),
    "metapat.theory.5.relational_gradient_selection": ("metapat.axiom.6.relation", "metapat.axiom.7.gradient", "metapat.axiom.8.transformation", "metapat.theorem.1.boundary_earns_its_keep"),
    "metapat.theory.6.time_as_sequential_tensor_alteration": ("metapat.axiom.4.tensor", "metapat.axiom.9.time", "metapat.theorem.6.registration_is_not_time"),
    "metapat.theory.7.registration_and_observer_roles": ("metapat.axiom.10.registration", "metapat.theorem.6.registration_is_not_time", "metapat.theorem.7.observer_role_earned_by_registration", "metapat.theorem.8.consciousness_is_optional", "metapat.postulate.5.registration_plurality"),
    "metapat.theory.8.questions_as_bounded_unresolved_energy_state": ("metapat.axiom.11.question", "metapat.theorem.3.question_as_energy_state"),
    "metapat.theory.9.native_scale_object_integration": ("metapat.axiom.2.boundary", "metapat.axiom.3.simplex", "metapat.axiom.4.tensor", "metapat.axiom.5.energy_state", "metapat.axiom.6.relation", "metapat.postulate.3.formed_objects", "metapat.postulate.4.integration", "metapat.theorem.4.object_instantiation"),
    "metapat.theory.10.symbolic_and_memetic_transfer": ("metapat.axiom.5.energy_state", "metapat.axiom.6.relation", "metapat.axiom.8.transformation", "metapat.axiom.10.registration", "metapat.axiom.11.question", "metapat.theory.7.registration_and_observer_roles", "metapat.theory.8.questions_as_bounded_unresolved_energy_state"),
    "metapat.theory.11.cross_domain_question_forms": ("metapat.axiom.0.root_untouchable", "metapat.axiom.11.question", "metapat.postulate.1.domain_similarity", "metapat.postulate.2.explicationary_use", "metapat.theorem.5.root_and_tool_separation"),
}

CATALOG_DERIVED_TEXT = {
    "metapat.theory.0.root_prior_restraint": "Derived from: Axiom 0; Postulates 1-2; Fifth Theorem.",
    "metapat.theory.1.distinction_formation": "Derived from: Axioms 1-3.",
    "metapat.theory.2.boundary_mediated_transformation": "Derived from: Axioms 2-3, 7-8; Postulate 6; First Theorem.",
    "metapat.theory.3.tensor_first_arrangement": "Derived from: Axiom 4; Axiom 9; Second Theorem.",
    "metapat.theory.4.energy_state_motion": "Derived from: Axiom 5; Axiom 8.",
    "metapat.theory.5.relational_gradient_selection": "Derived from: Axioms 6-8; First Theorem.",
    "metapat.theory.6.time_as_sequential_tensor_alteration": "Derived from: Axiom 4; Axiom 9; Sixth Theorem.",
    "metapat.theory.7.registration_and_observer_roles": "Derived from: Axiom 10; Theorems 6-8; Postulate 5.",
    "metapat.theory.8.questions_as_bounded_unresolved_energy_state": "Derived from: Axiom 11; Third Theorem.",
    "metapat.theory.9.native_scale_object_integration": "Derived from: Axioms 2-6; Postulates 3-4; Fourth Theorem.",
    "metapat.theory.10.symbolic_and_memetic_transfer": "Derived from: Axioms 5-6, 8, 10-11; Theory 7; Theory 8.",
    "metapat.theory.11.cross_domain_question_forms": "Derived from: Axiom 0; Axiom 11; Postulates 1-2; Fifth Theorem.",
}
