"""Static axiom, postulate, and theorem declarations for the semantic catalog."""

# === MODULE_BUILD ===
# id: metapat_semantic_doctrine_declarations
#   module_name: metapat.catalog_doctrine_data
#   module_kind: schema
#   summary: declares stable axiom, postulate, and theorem module identities, classes, source sections, and exact statements
#   owner: The Interdependency
#   public_surface: none
#   internal_surface: DOCTRINE_SPECS
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
#   unresolved: none
# === END MODULE_BUILD ===

DOCTRINE_SPECS = (
    ("metapat.axiom.0.root_untouchable", "canon-module", "axiom", "ROOT-STIPULATION", "AXIOMS.md", "0-root-is-untouchable", (
        "Domains may influence the exploratory tools of Energy Theory.",
        "Domains may not redefine the root.",
        "No domain owns Energy Theory.",
    ), ()),
    ("metapat.axiom.1.legible_difference", "distinction", "axiom", "ROOT-STIPULATION", "AXIOMS.md", "1-legible-difference", (
        "Legible difference is distinction.",
        "Without legible difference, no boundary can be defined.",
    ), ()),
    ("metapat.axiom.2.boundary", "boundary-simplex", "axiom", "ROOT-STIPULATION", "AXIOMS.md", "2-boundary", (
        "Distinction defines boundaries.",
        "Boundary is simplex of distinction.",
        "A boundary is a state-bearing simplex whose configuration may affect transformation.",
    ), ()),
    ("metapat.axiom.3.simplex", "simplex", "axiom", "ROOT-STIPULATION", "AXIOMS.md", "3-simplex", (
        "Boundaries define simplex.",
        "A simplex is a bounded state-bearing object.",
        "Simplex holds or modifies energy in a state of being.",
    ), ()),
    ("metapat.axiom.4.tensor", "tensor", "axiom", "DEFINITION", "AXIOMS.md", "4-tensor", (
        "Tensor is primitive.",
        "Tensor is simultaneous arrangement of energy-states.",
        "Without sequence, there is tensor.",
    ), ()),
    ("metapat.axiom.5.energy_state", "energy-state", "axiom", "DEFINITION", "AXIOMS.md", "5-energy-state", (
        "Energy appears as state of being.",
        "Energy-state held is scalar.",
        "Energy-state motioned is vector.",
        "Energy-state vectors alter energy-state scalars.",
    ), ()),
    ("metapat.axiom.6.relation", "relation", "axiom", "DEFINITION", "AXIOMS.md", "6-relation", (
        "Relation is readable configuration within tensor.",
        "Relation includes configured possibility of alteration among simplexes, including boundary-simplexes.",
    ), ()),
    ("metapat.axiom.7.gradient", "gradient", "axiom", "DEFINITION", "AXIOMS.md", "7-gradient", (
        "Gradient is readable difference within relation.",
        "Gradient dynamics are how vectors select direction.",
        "Gradient dynamics include tensor arrangement, simplex relations, and boundary-simplex states.",
    ), ()),
    ("metapat.axiom.8.transformation", "transformation", "axiom", "DEFINITION", "AXIOMS.md", "8-transformation", (
        "Transformation is vector-compelled alteration of energy-state.",
        "A simplex may hold energy-state.",
        "A simplex may modify energy-state.",
        "A boundary-simplex may modify how alteration occurs.",
    ), ()),
    ("metapat.axiom.9.time", "time", "axiom", "DEFINITION", "AXIOMS.md", "9-time", (
        "Time is sequential tensor alteration.",
        "Registration is not the parent of time.",
    ), ()),
    ("metapat.axiom.10.registration", "registration", "axiom", "DEFINITION", "AXIOMS.md", "10-registration", (
        "Registration is the capacity of a simplex to preserve, express, or transmit sequential tensor alteration.",
        "An observer is a simplex performing registration.",
        "An observer need not be conscious.",
        "Consciousness is one possible observer-mode.",
        "Story is conscious registration of time.",
    ), ()),
    ("metapat.axiom.11.question", "question", "axiom", "DEFINITION", "AXIOMS.md", "11-question", (
        "A question is a bounded unresolved energy-state.",
        "Energy Theory answers: What questions do I ask?",
    ), ()),
    ("metapat.postulate.1.domain_similarity", "postulate", "postulate", "WORKING-POSTULATE", "POSTULATES.md", "first-postulate-domain-similarity", (
        "When different domains show similarly shaped transformations, Energy Theory may compare them.",
        "The comparison does not make the domains identical.",
        "The comparison reveals shared question-forms.",
    ), ()),
    ("metapat.postulate.2.explicationary_use", "postulate", "postulate", "WORKING-POSTULATE", "POSTULATES.md", "second-postulate-explicationary-use", (
        "A domain term may be used as an explicationary tool if it clarifies the root.",
        "A domain term must be rejected or demoted if it attempts to redefine the root.",
    ), ()),
    ("metapat.postulate.3.formed_objects", "postulate", "postulate", "WORKING-POSTULATE", "POSTULATES.md", "third-postulate-formed-objects", (
        "A formed object is a tensor of simplexes integrated at a scale.",
        "Object-instantiation requires integration at its native scale, not consciousness.",
        "A physical object may require physical and spatial simplexes.",
        "A mental object may require archetype, concept, idea, and gestalt simplexes.",
        "Gestalt simplex is cognitive registration of integrated object-whole. It is not the source of physical object existence.",
    ), ()),
    ("metapat.postulate.4.integration", "postulate", "postulate", "WORKING-POSTULATE", "POSTULATES.md", "fourth-postulate-integration", (
        "Integration is a tensor configuration becoming object-whole at a native scale.",
        "An integration simplex may instantiate object-whole at that scale.",
        "A cognitive gestalt may register that integration when a mind encounters or constructs it.",
    ), ()),
    ("metapat.postulate.5.registration_plurality", "postulate", "postulate", "WORKING-POSTULATE", "POSTULATES.md", "fifth-postulate-registration-plurality", (
        "Registration may be performed by any simplex capable of preserving, expressing, or transmitting sequential tensor alteration.",
        "A sedimentary layer, a log file, a sensor stream, a memory trace, a written mark, a downstream code module, a trained model state, or a human mind may all register according to their native structures.",
        "Consciousness is one registration mode, not the parent ontology.",
    ), ()),
    ("metapat.postulate.6.validation_by_boundary_change", "postulate", "postulate", "WORKING-POSTULATE", "POSTULATES.md", "sixth-postulate-validation-by-boundary-change", (
        "A boundary-simplex earns ontology only if changing its state changes vector direction, propagation, delay, filtering, or transformation outcome while source and target energy-states are held constant.",
    ), ()),
    ("metapat.postulate.7.discovery_before_recovery", "postulate", "postulate", "WORKING-POSTULATE", "POSTULATES.md", "seventh-postulate-discovery-before-recovery", (
        "Interest may select what to explore.",
        "Discovery may precede explanation.",
        "Freeze a result before independent recovery.",
        "Independent recovery tests the result, not the legitimacy of the discovery path.",
        "A simpler recovery method does not invalidate a more complex discovery method.",
    ), ()),
    ("metapat.theorem.1.boundary_earns_its_keep", "theorem", "theorem", "INTERNAL-DERIVATION", "THEOREMS.md", "first-theorem-boundary-earns-its-keep", (
        "If boundary is simplex, then boundary can modify transformation.",
        "If boundary can modify transformation, then gradient dynamics cannot be reduced to simple distance values or difference alone.",
        "Therefore, vector direction is selected through gradient dynamics that explicitly include the current state of the boundary-simplex.",
    ), ()),
    ("metapat.theorem.2.tensor_precedes_time", "theorem", "theorem", "INTERNAL-DERIVATION", "THEOREMS.md", "second-theorem-tensor-precedes-time", (
        "If tensor is simultaneous arrangement of energy-states, and time is sequential tensor alteration, then tensor precedes time in Energy Theory.",
        "Therefore, without sequence there is not nothingness.",
        "Without sequence, there is tensor.",
    ), ()),
    ("metapat.theorem.3.question_as_energy_state", "theorem", "theorem", "INTERNAL-DERIVATION", "THEOREMS.md", "third-theorem-question-as-energy-state", (
        "If a question is bounded and unresolved, and simplex holds energy in a state of being, then a question is a simplex holding unresolved energy-state.",
        "Therefore, questions are Energy Theory.",
    ), ()),
    ("metapat.theorem.4.object_instantiation", "theorem", "theorem", "INTERNAL-DERIVATION", "THEOREMS.md", "fourth-theorem-object-instantiation", (
        "If a formed object is a tensor of simplexes integrated at a scale, then object-instantiation does not require a human mind.",
        "Therefore, the physical cup is not created by cognition.",
        "Cognition may register cup-whole as a gestalt simplex.",
    ), ()),
    ("metapat.theorem.5.root_and_tool_separation", "theorem", "theorem", "INTERNAL-DERIVATION", "THEOREMS.md", "fifth-theorem-root-and-tool-separation", (
        "If domains influence tools but cannot alter the root, then Energy Theory can grow without root-drift.",
        "Therefore, Energy Theory is a magpie, not a mimic.",
        "It may take the shiny shape of a question from any domain.",
        "It may not surrender its root to any domain.",
    ), ()),
    ("metapat.theorem.6.registration_is_not_time", "theorem", "theorem", "INTERNAL-DERIVATION", "THEOREMS.md", "sixth-theorem-registration-is-not-time", (
        "If time is sequential tensor alteration, and registration is the capacity of a simplex to preserve, express, or transmit sequential tensor alteration, then registration is not the parent of time.",
        "Therefore, time can occur without being consciously narrated, and registration can occur without consciousness.",
        "Story is one conscious registration of time, not time itself.",
    ), ()),
    ("metapat.theorem.7.observer_role_earned_by_registration", "theorem", "theorem", "INTERNAL-DERIVATION", "THEOREMS.md", "seventh-theorem-observer-role-is-earned-by-registration", (
        "If observer is a simplex performing registration, then a simplex is not an observer merely by being present in a tensor.",
        "Therefore, observer is a role performed by a simplex when it preserves, expresses, or transmits sequential tensor alteration.",
    ), ()),
    ("metapat.theorem.8.consciousness_is_optional", "theorem", "theorem", "INTERNAL-DERIVATION", "THEOREMS.md", "eighth-theorem-consciousness-is-optional", (
        "If observer is any simplex performing registration, and consciousness is one observer-mode, then consciousness is not required for registration.",
        "Therefore, non-conscious registration and conscious story can both be observer-mode expressions, but only story is conscious registration of time.",
    ), ()),
)
