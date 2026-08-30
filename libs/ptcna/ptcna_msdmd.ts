import { defineMsdmdCollection } from "./.agents/skills/msdmd/collection";

export default defineMsdmdCollection({
  "declarations": [
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "validate_report, canonical_bytes, digest",
        "module_kind": "instrument",
        "module_name": "portfolio_plan",
        "network_boundary": "none",
        "owner": "The-Interdependency/skill-lib maintainers",
        "public_surface": "load_report, build_portfolio, main",
        "rollback": "remove the aggregator, schemas, companion docs, and portfolio projection section without changing repo-owned source claims",
        "rollout": "explicit CLI or library invocation after repo reports are supplied",
        "storage_boundary": "none",
        "summary": "validates repo-owned plan reports and derives a deterministic cross-repository portfolio projection without transferring authority",
        "tests": "tests/test_interdependent_work_graph_portfolio_plan.py",
        "unresolved": "automatic portfolio membership discovery, persistent live service, cryptographic producer authentication",
        "user_data_boundary": "none"
      },
      "file": ".agents/skills/interdependent-work-graph/portfolio_plan.py",
      "id": "interdependent_work_graph_portfolio_plan"
    },
    {
      "block": "BOUNDARIES",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "pii": "none",
        "secrets": "none",
        "since": "unreleased",
        "storage_boundary": "none",
        "summary": "imports local package definitions without constructing engines or performing persistence, network, authentication, user-data, or administrative effects",
        "user_data_boundary": "none"
      },
      "file": "ptcna/__init__.py",
      "id": "ptcna_package_import_boundary"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "compatibility",
        "given": "a caller imports ptcna",
        "then": "the experimental engine, distinct fallback, attributed runtime, frozen evaluation types, and evaluator are available without importing deprecated service surfaces"
      },
      "file": "ptcna/__init__.py",
      "id": "ptcna_root_exports_runtime_boundary"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "adapter",
        "module_name": "package surface",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "neural, circle, seed, core, PTCNAEngine, HashedLinearFallback, PTCNARuntime, EvaluationCase, EvaluationPlan, EvaluationReceipt, evaluate, UCNS integration status types",
        "requires": "ptcna_runtime_boundary, ptcna_frozen_evaluation, ptcna_ucns_integration",
        "rollback": "remove root re-exports while retaining module-qualified imports",
        "rollout": "imported through ptcna",
        "since": "unreleased",
        "storage_boundary": "none",
        "summary": "exposes the four layers, explicit runtime boundary, dependable fallback, and frozen evaluation types from the package root",
        "tests": "ptcna/tests/test_runtime.py",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ptcna/__init__.py",
      "id": "ptcna_package_surface"
    },
    {
      "block": "BOUNDARIES",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "pii": "none",
        "secrets": "none",
        "since": "0.1.1",
        "storage_boundary": "none",
        "summary": "performs deterministic in-memory structural composition without activating UCNS or touching external state",
        "user_data_boundary": "none"
      },
      "file": "ptcna/circle/compose.py",
      "id": "circle_composition_runtime_boundary"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "one or more ordered payload objects and a routing step",
        "then": "composition assigns a deterministic complete anchor cycle or identity fallback and preserves every payload object"
      },
      "file": "ptcna/circle/compose.py",
      "id": "circle_composition_preserves_order_and_identity"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "zero neural payloads",
        "then": "compose_circle raises ValueError instead of inventing an empty circle"
      },
      "file": "ptcna/circle/compose.py",
      "id": "circle_composition_rejects_empty_input"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "circle composition",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "star_polygon_order, compose_circle",
        "requires": "ptcna_circle_tensor, ptcna_ucns_integration",
        "rollback": "remove exports and restore audit-only circle behavior",
        "rollout": "default enabled as the neural-to-circle structural boundary",
        "since": "0.1.1",
        "storage_boundary": "none",
        "summary": "composes ordered neural payloads into a standalone non-differentiating circle tensor",
        "tests": "ptcna/circle/tests/test_circle.py",
        "unresolved": "exact future UCNS carrier and higher-gonol composition profile",
        "user_data_boundary": "none"
      },
      "file": "ptcna/circle/compose.py",
      "id": "ptcna_circle_composition"
    },
    {
      "block": "BOUNDARIES",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "pii": "none",
        "secrets": "none",
        "since": "0.1.1",
        "storage_boundary": "none",
        "summary": "stores caller-provided payload references in memory and performs no persistence, network, auth, or user-data operation",
        "user_data_boundary": "none"
      },
      "file": "ptcna/circle/tensor.py",
      "id": "circle_tensor_runtime_boundary"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a circle hosting payloads that may themselves be neural-owned differentiable objects",
        "then": "the circle reports requires_grad false and never creates or executes gradient operations"
      },
      "file": "ptcna/circle/tensor.py",
      "id": "circle_tensor_is_non_differentiating"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "payloads composed into a circle under a star-polygon anchor order",
        "then": "each payload is recoverable by its assigned inner anchor as the identical object"
      },
      "file": "ptcna/circle/tensor.py",
      "id": "circle_tensor_round_trips_payloads"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "schema",
        "module_name": "circle tensor",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "CircleTensor",
        "requires": "none",
        "rollback": "remove circle composition and restore seed-local opaque circle wrappers",
        "rollout": "constructed through ptcna.circle.compose_circle",
        "since": "0.1.1",
        "storage_boundary": "none",
        "summary": "represents the non-differentiating circle-layer output that structurally hosts ordered neural payloads",
        "tests": "ptcna/circle/tests/test_circle.py",
        "unresolved": "exact future UCNS carrier profile",
        "user_data_boundary": "none"
      },
      "file": "ptcna/circle/tensor.py",
      "id": "ptcna_circle_tensor"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_non_coprime_count_uses_identity_fallback",
        "cleanup": "none",
        "mutates": "none",
        "proves": "circle_composition_preserves_order_and_identity",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "ptcna/circle/tests/test_circle.py",
      "id": "check_circle_identity_fallback"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_circle_does_not_own_neural_payload_gradients",
        "cleanup": "none",
        "mutates": "none",
        "proves": "circle_tensor_is_non_differentiating",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "ptcna/circle/tests/test_circle.py",
      "id": "check_circle_non_differentiating"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_empty_circle_is_rejected",
        "cleanup": "none",
        "mutates": "none",
        "proves": "circle_composition_rejects_empty_input",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "ptcna/circle/tests/test_circle.py",
      "id": "check_circle_rejects_empty"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_circle_preserves_exact_payload_objects",
        "cleanup": "none",
        "mutates": "none",
        "proves": "circle_tensor_round_trips_payloads, circle_composition_preserves_order_and_identity",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "ptcna/circle/tests/test_circle.py",
      "id": "check_circle_roundtrip"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_build_coherence_up_to, _is_prime, _prime_factors",
        "module_kind": "engine",
        "module_name": "constants",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "SEED_COUNT, CIRCLES_PER_SEED, TENSORS_PER_CIRCLE, TENSOR_DIM, TENSOR_LEAVES, PARAM_COUNT, CIRCLE_ROUTING_STEP, SEED_ROUTING_STEP, is_coherence_prime",
        "requires": "coherence_primes (mirrored from interdependent_lib, not imported \u2014 would invert the dependency graph)",
        "rollback": "revert is_coherence_prime to the prior frozen-universe implementation",
        "rollout": "default_enabled (imported by prime_core.core via prime_core.__init__)",
        "since": "2026-06-02 (manifest added; module predates the doctrine)",
        "storage_boundary": "none",
        "summary": "frozen PTCA composition counts plus the recursive coherence-prime guard",
        "tests": "prime_core.tests.test_constants_coherence_prime",
        "unresolved": "composition counts SEED_COUNT/TENSOR_DIM remain provisional pending the absent canon documents",
        "user_data_boundary": "none"
      },
      "file": "ptcna/core/prime_core/constants.py",
      "id": "prime_core_constants"
    },
    {
      "block": "BOUNDARIES",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "pii": "none",
        "secrets": "none",
        "since": "0.1.1",
        "storage_boundary": "none",
        "summary": "performs deterministic in-memory composition and creates no network, storage, auth, user-data, or external package effect",
        "user_data_boundary": "none"
      },
      "file": "ptcna/core/prime_core/core.py",
      "id": "prime_core_composition_runtime_boundary"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "any CoreSpec composition count is zero or negative",
        "then": "CoreSpec raises ValueError naming the invalid field"
      },
      "file": "ptcna/core/prime_core/core.py",
      "id": "prime_core_counts_are_positive"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "compatibility",
        "given": "build_core is called with the default CoreSpec",
        "then": "the historical default profile contains 157 seeds, 7693 fiqs, and 407729 opaque payload values"
      },
      "file": "ptcna/core/prime_core/core.py",
      "id": "prime_core_default_profile_is_stable"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a core hosts payloads including neural-owned differentiable objects",
        "then": "core, seed, circle, and fiq hosts report requires_grad false and core exposes no backward operation"
      },
      "file": "ptcna/core/prime_core/core.py",
      "id": "prime_core_is_non_differentiating"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a payload factory returns a vector whose length differs from tensor_dim",
        "then": "build_core raises ValueError before constructing an invalid fiq"
      },
      "file": "ptcna/core/prime_core/core.py",
      "id": "prime_core_payload_width_matches_spec"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a core is built with the exact 157x7x7x53 receipt-covered shape or a different shape",
        "then": "only the exact shape carries active UCNS state provenance while every different shape remains suspended and locally attributed"
      },
      "file": "ptcna/core/prime_core/core.py",
      "id": "prime_core_ucns_receipt_scope_is_exact"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "a core is built from a CoreSpec",
        "then": "every circle is ptcna.circle.CircleTensor and every seed is ptcna.seed.Seed with no duplicate core-local layer types"
      },
      "file": "ptcna/core/prime_core/core.py",
      "id": "prime_core_uses_shared_layer_types"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_local_fiq_identity",
        "module_kind": "engine",
        "module_name": "prime core composition",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "CoreSpec, Core, build_core, compose_circle, compose_seed, heptagram_order",
        "requires": "ptcna_fiq_host, ptcna_circle_composition, ptcna_seed_composition, ptcna_ucns_integration",
        "rollback": "remove prime-core exports; shared circle and seed layers remain available",
        "rollout": "exact default shape consumes the pinned UCNS candidate receipt; all other shapes remain locally attributed",
        "since": "0.1.1",
        "storage_boundary": "none",
        "summary": "composes opaque fiqs through the shared circle and seed types into a non-differentiating core",
        "tests": "ptcna/core/prime_core/tests/test_ptca_core_stratified.py",
        "unresolved": "continuous seven-fold geometry, representative efficacy, production privacy, and sustained-load behavior",
        "user_data_boundary": "none"
      },
      "file": "ptcna/core/prime_core/core.py",
      "id": "ptcna_prime_core_composition"
    },
    {
      "block": "BOUNDARIES",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "pii": "none",
        "secrets": "none",
        "since": "0.1.1",
        "storage_boundary": "none",
        "summary": "retains caller-provided object references in memory without inspecting content or touching external state",
        "user_data_boundary": "none"
      },
      "file": "ptcna/core/prime_core/fiq.py",
      "id": "fiq_runtime_boundary"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a fiq carries neural-owned differentiable objects",
        "then": "the fiq reports requires_grad false and exposes no backward operation or gradient state"
      },
      "file": "ptcna/core/prime_core/fiq.py",
      "id": "fiq_never_owns_gradients"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "arbitrary payload objects are wrapped in a fiq",
        "then": "each retrieved payload element is the identical object supplied by the caller"
      },
      "file": "ptcna/core/prime_core/fiq.py",
      "id": "fiq_payload_is_opaque_and_lossless"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "Fiq._payload",
        "module_kind": "schema",
        "module_name": "fiq",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "Fiq, wrap_tensor_fiq",
        "requires": "none",
        "rollback": "remove prime-core construction and fiq exports",
        "rollout": "default enabled for prime-core construction",
        "since": "0.1.1",
        "storage_boundary": "none",
        "summary": "preserves opaque payload vectors inside a non-differentiating core timing host",
        "tests": "ptcna/core/prime_core/tests/test_fiq_opaque.py",
        "unresolved": "exact future UCNS carrier attachment",
        "user_data_boundary": "none"
      },
      "file": "ptcna/core/prime_core/fiq.py",
      "id": "ptcna_fiq_host"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_fiq_is_non_differentiating_with_neural_payload",
        "cleanup": "none",
        "mutates": "none",
        "proves": "fiq_never_owns_gradients",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "ptcna/core/prime_core/tests/test_fiq_opaque.py",
      "id": "check_fiq_has_no_gradient_ownership"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_payload_roundtrip_identity",
        "cleanup": "none",
        "mutates": "none",
        "proves": "fiq_payload_is_opaque_and_lossless",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "ptcna/core/prime_core/tests/test_fiq_opaque.py",
      "id": "check_fiq_payload_identity"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_canon_structure_counts",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_core_default_profile_is_stable",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "ptcna/core/prime_core/tests/test_ptca_core_stratified.py",
      "id": "check_prime_core_default_profile"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_neural_payload_gradients_remain_neural_owned",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_core_is_non_differentiating",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "ptcna/core/prime_core/tests/test_ptca_core_stratified.py",
      "id": "check_prime_core_no_gradient_ownership"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_payload_factory_width_is_checked",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_core_payload_width_matches_spec",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "ptcna/core/prime_core/tests/test_ptca_core_stratified.py",
      "id": "check_prime_core_payload_width"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_core_spec_rejects_nonpositive_counts",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_core_counts_are_positive",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "ptcna/core/prime_core/tests/test_ptca_core_stratified.py",
      "id": "check_prime_core_positive_counts"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_core_uses_circle_and_seed_owned_types",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_core_uses_shared_layer_types",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "ptcna/core/prime_core/tests/test_ptca_core_stratified.py",
      "id": "check_prime_core_shared_layer_types"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_ucns_attribution_is_exactly_shape_scoped",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_core_ucns_receipt_scope_is_exact",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "ptcna/core/prime_core/tests/test_ptca_core_stratified.py",
      "id": "check_prime_core_ucns_scope"
    },
    {
      "block": "BOUNDARIES",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "pii": "none",
        "secrets": "none",
        "since": "unreleased",
        "storage_boundary": "write",
        "summary": "reads the repository-owned frozen plan and writes one caller-selected local JSON result without network, authentication, secrets, or user data",
        "user_data_boundary": "none"
      },
      "file": "ptcna/critical_evaluation.py",
      "id": "ptcna_critical_evaluation_local_receipt"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the checked-in critical evaluation plan is loaded",
        "then": "its canonical EvaluationPlan digest must equal the independently stored frozen digest"
      },
      "file": "ptcna/critical_evaluation.py",
      "id": "ptcna_critical_plan_digest_locked"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the frozen plan completes or reaches a frozen failure rule",
        "then": "the serialized result names the plan digest, separate claim verdicts, and its own canonical result digest"
      },
      "file": "ptcna/critical_evaluation.py",
      "id": "ptcna_critical_result_content_addressed"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_artifact_path, _canonical_digest",
        "module_kind": "experiment",
        "module_name": "critical_evaluation",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "load_frozen_plan, execute_frozen_plan, main",
        "requires": "ptcna_frozen_evaluation",
        "rollback": "preserve plan and result receipts; remove executable wrapper without changing runtime",
        "rollout": "execute only after the preregistration commit is merged",
        "since": "unreleased",
        "storage_boundary": "write",
        "summary": "loads the immutable representative role-acquisition plan and seals its separate usefulness and superiority verdicts",
        "tests": "ptcna/tests/test_critical_evaluation.py",
        "unresolved": "outcome until the merged frozen plan is executed",
        "user_data_boundary": "none"
      },
      "file": "ptcna/critical_evaluation.py",
      "id": "ptcna_critical_evaluation"
    },
    {
      "block": "BOUNDARIES",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "pii": "none",
        "secrets": "none",
        "since": "unreleased",
        "storage_boundary": "none",
        "summary": "executes caller-supplied in-process backends and returns an in-memory receipt without persistence, network, authentication, user-data, or administrative effects",
        "user_data_boundary": "none"
      },
      "file": "ptcna/evaluation.py",
      "id": "ptcna_evaluation_local_boundary"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "an EvaluationPlan is constructed",
        "then": "workload, training schedule, comparator identities, metric, aggregation, thresholds, resource bounds, stopping rule, and failure propagation are immutable and covered by one deterministic digest"
      },
      "file": "ptcna/evaluation.py",
      "id": "ptcna_evaluation_plan_freezes_verdict_inputs"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "either backend errors before completing the frozen workload",
        "then": "evaluation stops and records the plan's preselected target/comparator failure propagation before any repair or criterion change"
      },
      "file": "ptcna/evaluation.py",
      "id": "ptcna_evaluation_propagates_backend_failure"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "target and fallback complete the frozen workload",
        "then": "training occurs before scoring and separate usefulness and superiority verdicts use only the frozen target-accuracy and target-advantage thresholds"
      },
      "file": "ptcna/evaluation.py",
      "id": "ptcna_evaluation_verdict_uses_frozen_thresholds"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_receipt",
        "module_kind": "experiment",
        "module_name": "evaluation",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "EvaluationCase, EvaluationPlan, EvaluationReceipt, evaluate, FALSIFIED, SURVIVED_NOT_PROVED, UNRESOLVED",
        "requires": "ptcna_runtime_boundary",
        "rollback": "remove evaluation exports without changing target or fallback runtime behavior",
        "rollout": "caller supplies a preserved representative EvaluationPlan before execution",
        "since": "unreleased",
        "storage_boundary": "none",
        "summary": "freezes the workload, training schedule, comparator, metric, thresholds, limits, stopping rule, failure propagation, and evidence receipt before target-versus-fallback execution",
        "tests": "ptcna/tests/test_evaluation.py",
        "unresolved": "representative workload identity and externally justified thresholds",
        "user_data_boundary": "none"
      },
      "file": "ptcna/evaluation.py",
      "id": "ptcna_frozen_evaluation"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "instrument",
        "module_name": "helix_vis",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "generate_helix_data, visualize",
        "requires": "none",
        "rollback": "remove import and call sites",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "write",
        "summary": "Visualizes the spectral state of a 7-seed Meta Router by plotting the complex descriptor Z over a simulated trajectory and saving an animation.",
        "tests": "hmmm",
        "unresolved": "saves to hardcoded pcna_helix.gif with no config (Known Issues)",
        "user_data_boundary": "none"
      },
      "file": "ptcna/neural/helix_vis.py",
      "id": "pcna_helix_vis"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_recompute_hub_avg, _reset",
        "module_kind": "engine",
        "module_name": "memory_core",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "MemoryCore",
        "requires": "none",
        "rollback": "remove import and call sites",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Parameterized in-memory ring (long-term N=19/seed=19, short-term N=17/seed=17) with round-robin write, content-addressed query, and flush_to() transfer on positive reward.",
        "tests": "hmmm",
        "unresolved": "query() is defined but never called anywhere (Known Issues)",
        "user_data_boundary": "none"
      },
      "file": "ptcna/neural/memory_core.py",
      "id": "pcna_memory_core"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_fed_avg, _blend_core",
        "module_kind": "engine",
        "module_name": "merge",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "InstanceMerge",
        "requires": "pcna_ring_core, pcna_pcna",
        "rollback": "remove import and call sites",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Stateless multi-instance merge operator for PCNAEngine meshes with three modes (absorb, fork, converge) via federated averaging; all output dicts use theta_* keys.",
        "tests": "hmmm",
        "unresolved": "fork() time-seeds its RNG \u2014 rapid calls may collide (Known Issues)",
        "user_data_boundary": "none"
      },
      "file": "ptcna/neural/merge.py",
      "id": "pcna_merge"
    },
    {
      "block": "BOUNDARIES",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "pii": "none",
        "secrets": "none",
        "since": "0.1.1",
        "storage_boundary": "write",
        "summary": "performs local numpy checkpoint reads and writes under the configured checkpoint directory",
        "user_data_boundary": "none"
      },
      "file": "ptcna/neural/pcna.py",
      "id": "pcna_checkpoint_runtime_boundary"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "an engine saves a checkpoint and a compatible engine loads it",
        "then": "all five persisted ring tensors are restored with the saved shapes and values"
      },
      "file": "ptcna/neural/pcna.py",
      "id": "pcna_checkpoint_round_trips_ring_state"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "non-empty input text is passed to PCNAEngine.infer",
        "then": "the result reports project, inject, propagate, seed audit, circle audit, and coherence steps with a bounded confidence"
      },
      "file": "ptcna/neural/pcna.py",
      "id": "pcna_infer_reports_complete_six_step_pipeline"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "a bounded outcome is passed to PCNAEngine.reward",
        "then": "the neural rings and theta timing state are updated and one unambiguous memory flush result is reported"
      },
      "file": "ptcna/neural/pcna.py",
      "id": "pcna_reward_updates_neural_and_timing_state"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_tensor_to_b64, _b64_to_tensor, _CHECKPOINT_DIR, PCNAEngine._project, PCNAEngine._inject, PCNAEngine._propagate, PCNAEngine._seed_audit, PCNAEngine._circle_audit, PCNAEngine._coherence_score",
        "module_kind": "engine",
        "module_name": "pcna",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "PCNAEngine, RING_WEIGHTS, WINNER_RINGS",
        "requires": "pcna_ring_core, pcna_memory_core, pcna_theta",
        "rollback": "remove import and call sites; checkpoints under .checkpoints/ can be deleted",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "write",
        "summary": "Six-ring PCNA inference engine (phi/psi/omega/theta/memory_l/memory_s) running project->inject->propagate->seed-audit->circle-audit->coherence, with RING_WEIGHTS scoring and numpy checkpointing.",
        "tests": "ptcna/neural/tests/test_pcna.py",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ptcna/neural/pcna.py",
      "id": "pcna_pcna"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_adj_distances, RingCore._adjacents, _propagate_node, _recompute_coherence",
        "module_kind": "engine",
        "module_name": "ring_core",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "RingCore, DIMS, PHASES, HEPT_SITES",
        "requires": "none",
        "rollback": "remove import and call sites",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Base prime-ring tensor (shape [N,DIMS=4,PHASES=7,HEPT_SITES=7]) with heptagram Euler-step propagation and coherence = 1 - |ring - hub|_mean; substrate for Phi/Psi/Omega/Sigma.",
        "tests": "hmmm",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ptcna/neural/ring_core.py",
      "id": "pcna_ring_core"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "worker",
        "module_name": "routing_loop",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "GlobalRouterZero",
        "requires": "none",
        "rollback": "remove import and call sites",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Intended GlobalRouterZero routing loop worker \u2014 currently only a print stub that announces initialization.",
        "tests": "hmmm",
        "unresolved": "only a print stub \u2014 GlobalRouterZero not implemented (Known Stubs)",
        "user_data_boundary": "none"
      },
      "file": "ptcna/neural/routing_loop.py",
      "id": "pcna_routing_loop"
    },
    {
      "block": "BOUNDARIES",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "pii": "none",
        "secrets": "none",
        "since": "0.1.1",
        "storage_boundary": "none",
        "summary": "performs in-memory scalar arithmetic without persistence, network access, or user-data handling",
        "user_data_boundary": "none"
      },
      "file": "ptcna/neural/scalar.py",
      "id": "neural_scalar_runtime_boundary"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "a loss graph composed from NeuralScalar addition and multiplication",
        "then": "backward accumulates gradients only on NeuralScalar nodes"
      },
      "file": "ptcna/neural/scalar.py",
      "id": "neural_scalar_owns_backprop"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a NeuralScalar computation graph",
        "then": "every recorded operation is scalar addition, scalar multiplication, or a leaf; structural composition never enters the tape"
      },
      "file": "ptcna/neural/scalar.py",
      "id": "neural_scalar_uses_no_structural_operator"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "NeuralScalar._backward, NeuralScalar._prev, NeuralScalar._op",
        "module_kind": "engine",
        "module_name": "neural scalar",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "NeuralScalar",
        "requires": "none",
        "rollback": "remove neural scalar exports and all neural call sites",
        "rollout": "default enabled as the sole PTCNA differentiable leaf type",
        "since": "0.1.1",
        "storage_boundary": "none",
        "summary": "owns PTCNA reverse-mode scalar operations and back-propagation exclusively inside the neural layer",
        "tests": "ptcna/neural/tests/test_scalar.py",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ptcna/neural/scalar.py",
      "id": "ptcna_neural_scalar"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_sigma, SigmaRing._core, SigmaRing._watched, SigmaRing._pending, SigmaRing._last_check",
        "module_kind": "engine",
        "module_name": "sigma",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "SigmaRing, get_sigma, N, SEED",
        "requires": "pcna_ring_core",
        "rollback": "remove import and call sites; callers already degrade gracefully if it raises",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "read",
        "summary": "N=41 filesystem observer ring wrapping RingCore; tracks watched file mtimes and drains content-changed events on a content_interval cadence, injecting coherence into Psi.",
        "tests": "hmmm",
        "unresolved": "structural_interval is stored but never acted on (Known Issues)",
        "user_data_boundary": "none"
      },
      "file": "ptcna/neural/sigma.py",
      "id": "pcna_sigma"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "tensor_engine",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "TensorState, MarkovRecursion",
        "requires": "none",
        "rollback": "remove import and call sites",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Tensor engine primitives \u2014 TensorState (E[a,t,m,c]) with spectral descriptor Z = Sum E.e^(i*theta), and a MarkovRecursion updater that enforces approximate mass conservation.",
        "tests": "tests/test_tensor_engine.py",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ptcna/neural/tensor_engine.py",
      "id": "pcna_tensor_engine"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_checkpoint_roundtrip",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "pcna_checkpoint_round_trips_ring_state",
        "requires": "python3, numpy",
        "timeout": "30"
      },
      "file": "ptcna/neural/tests/test_pcna.py",
      "id": "check_pcna_checkpoint_roundtrip"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_reward_reports_one_memory_flush_result",
        "cleanup": "none",
        "mutates": "none",
        "proves": "pcna_reward_updates_neural_and_timing_state",
        "requires": "python3, numpy",
        "timeout": "30"
      },
      "file": "ptcna/neural/tests/test_pcna.py",
      "id": "check_pcna_reward"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_infer_reports_all_six_steps",
        "cleanup": "none",
        "mutates": "none",
        "proves": "pcna_infer_reports_complete_six_step_pipeline",
        "requires": "python3, numpy",
        "timeout": "30"
      },
      "file": "ptcna/neural/tests/test_pcna.py",
      "id": "check_pcna_six_step_pipeline"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_backward_accumulates_expected_gradient",
        "cleanup": "none",
        "mutates": "none",
        "proves": "neural_scalar_owns_backprop",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "ptcna/neural/tests/test_scalar.py",
      "id": "check_neural_scalar_backprop"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_tape_contains_only_neural_scalar_ops",
        "cleanup": "none",
        "mutates": "none",
        "proves": "neural_scalar_uses_no_structural_operator",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "ptcna/neural/tests/test_scalar.py",
      "id": "check_neural_scalar_tape_ops"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_external_provider_drives_phi_nudge",
        "cleanup": "none",
        "mutates": "none",
        "proves": "zeta_consumes_explicit_metrics",
        "requires": "python3, numpy",
        "timeout": "10"
      },
      "file": "ptcna/neural/tests/test_zeta.py",
      "id": "check_zeta_external_metrics"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_removed_shadow_edcm_module_is_absent",
        "cleanup": "none",
        "mutates": "none",
        "proves": "zeta_never_imports_shadow_edcm",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "ptcna/neural/tests/test_zeta.py",
      "id": "check_zeta_no_shadow_edcm"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_evaluate_suspends_without_provider",
        "cleanup": "none",
        "mutates": "none",
        "proves": "zeta_requires_external_measurement_provider",
        "requires": "python3, numpy",
        "timeout": "10"
      },
      "file": "ptcna/neural/tests/test_zeta.py",
      "id": "check_zeta_suspends_without_provider"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_gen_instance_id, _derive_key_id, _compute_blueprint_hash, _shard_blueprint, ThetaTensor._recompute_coherence",
        "module_kind": "engine",
        "module_name": "theta",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "ThetaTensor, GATE_THRESHOLD, N",
        "requires": "none",
        "rollback": "remove import and call sites",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "N=29 standalone microkernel gate ring with ragged per-node circle counts, SHA-256 blueprint sharding, and gate control via GATE_THRESHOLD=0.45.",
        "tests": "hmmm",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ptcna/neural/theta.py",
      "id": "pcna_theta"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_initialize_topology, _heptagram_neighbors",
        "module_kind": "engine",
        "module_name": "topology",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "PCNATopology, Seed, SeedRole",
        "requires": "none",
        "rollback": "remove import and call sites",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Stable seed-id topology \u2014 maps compute-shard neighbors to global seed IDs, computes heptagram neighbors and sentinel scan paths, and serializes to JSON for HTTP responses.",
        "tests": "tests/tests_topology.py",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "ptcna/neural/topology.py",
      "id": "pcna_topology"
    },
    {
      "block": "BOUNDARIES",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "network_boundary": "hmmm",
        "owner": "Erin Spencer",
        "pii": "possible",
        "secrets": "none",
        "since": "0.1.1",
        "storage_boundary": "none",
        "summary": "reads caller-supplied response text and invokes an injected callback whose network behavior is outside PTCNA authority",
        "user_data_boundary": "read"
      },
      "file": "ptcna/neural/zeta.py",
      "id": "zeta_external_measurement_boundary"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "an injected provider returns the required bounded metric mapping",
        "then": "Zeta computes coherence, nudges Phi, and records an external_measurement event"
      },
      "file": "ptcna/neural/zeta.py",
      "id": "zeta_consumes_explicit_metrics"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "evaluation runs with or without an injected provider",
        "then": "PTCNA does not import or call ptcna.neural.edcm and treats supplied metrics as external evidence"
      },
      "file": "ptcna/neural/zeta.py",
      "id": "zeta_never_imports_shadow_edcm"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "evaluate is called without an injected measurement provider",
        "then": "a measurement_suspended event is returned and no neural nudge occurs"
      },
      "file": "ptcna/neural/zeta.py",
      "id": "zeta_requires_external_measurement_provider"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_get_default_pcna, ZetaEngine._coherence_from_metrics, ZetaEngine._sigma_nudge_factors, ZetaEngine._theta_gate_factor",
        "module_kind": "engine",
        "module_name": "zeta",
        "network_boundary": "hmmm",
        "owner": "Erin Spencer",
        "public_surface": "ZetaEngine, _zeta_engine",
        "requires": "pcna_pcna, pcna_sigma",
        "rollback": "remove import and call sites",
        "rollout": "default_enabled",
        "since": "0.1.1",
        "storage_boundary": "none",
        "summary": "ZFAE evaluator that consumes explicitly injected external metrics and nudges PCNAEngine.phi without implementing or importing EDCM.",
        "tests": "ptcna/neural/tests/test_zeta.py",
        "unresolved": "callback network behavior belongs to the caller and is not introspectable by PTCNA",
        "user_data_boundary": "read"
      },
      "file": "ptcna/neural/zeta.py",
      "id": "pcna_zeta"
    },
    {
      "block": "BOUNDARIES",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "pii": "none",
        "secrets": "none",
        "since": "unreleased",
        "storage_boundary": "none",
        "summary": "performs deterministic in-process inference and learning with no authentication, persistence, network, user-data, or administrative effect",
        "user_data_boundary": "none"
      },
      "file": "ptcna/runtime.py",
      "id": "ptcna_runtime_local_boundary"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "the target raises during inference",
        "then": "PTCNARuntime raises by default and uses the fallback only when explicitly enabled while recording the target failure and actual backend"
      },
      "file": "ptcna/runtime.py",
      "id": "ptcna_failover_is_explicit_and_attributed"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "identical text and fresh HashedLinearFallback instances",
        "then": "both produce the same bounded prediction under a fallback identity that is never labeled PTCNA"
      },
      "file": "ptcna/runtime.py",
      "id": "ptcna_fallback_is_distinct_and_deterministic"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "the fallback infers text and receives a positive bounded reward for the selected winner",
        "then": "a second inference of the same text gives that winner a strictly greater linear score"
      },
      "file": "ptcna/runtime.py",
      "id": "ptcna_fallback_reward_changes_selected_score"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a reward is applied to an inference receipt",
        "then": "only the backend named by backend_used receives the reward"
      },
      "file": "ptcna/runtime.py",
      "id": "ptcna_reward_follows_backend_receipt"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "non-empty text is inferred through PTCNAEngine",
        "then": "the receipt identifies the experimental PTCNA backend and reports neural, circle, seed, and core layer state without transferring gradients to structural layers"
      },
      "file": "ptcna/runtime.py",
      "id": "ptcna_target_reports_four_live_layers"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_validate_text, _validate_reward, _attach_route",
        "module_kind": "engine",
        "module_name": "runtime",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "PTCNAEngine, HashedLinearFallback, PTCNARuntime, InferenceBackend, PTCNA_BACKEND, FALLBACK_BACKEND",
        "requires": "pcna_pcna, ptcna_prime_core_composition",
        "rollback": "remove runtime exports while preserving the existing layer modules and PCNAEngine",
        "rollout": "explicit public API; target selected by default and fallback selected or enabled by the caller",
        "since": "unreleased",
        "storage_boundary": "none",
        "summary": "exposes the intended four-layer PTCNA path and a distinct dependable fallback behind one attributed task interface",
        "tests": "ptcna/tests/test_runtime.py",
        "unresolved": "representative task workload and whether either backend is useful under it",
        "user_data_boundary": "none"
      },
      "file": "ptcna/runtime.py",
      "id": "ptcna_runtime_boundary"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "given": "opaque payloads including neural scalars",
        "then": "composition creates no gradient node and preserves payload references"
      },
      "file": "ptcna/seed/compose.py",
      "id": "seed_composition_is_non_differentiating"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "given": "an empty circle sequence",
        "then": "compose_seed raises ValueError"
      },
      "file": "ptcna/seed/compose.py",
      "id": "seed_composition_rejects_empty"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "given": "a non-empty sequence of ptcna.circle.CircleTensor objects",
        "then": "compose_seed returns a Seed whose circles remain that shared type"
      },
      "file": "ptcna/seed/compose.py",
      "id": "seed_composition_uses_shared_circle_type"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_build_coherence_up_to, _is_prime, _prime_factors",
        "module_kind": "engine",
        "module_name": "constants",
        "network_boundary": "none",
        "owner": "Erin Patrick Spencer",
        "public_surface": "NOMINAL_CIRCLES_PER_SEED, SEED_ROUTING_STEP, HEPTAGRAM_VERTICES, is_coherence_prime, coherence_primes_up_to, nth_coherence_prime",
        "requires": "coherence_primes (mirrored from interdependent_lib, NOT imported \u2014 importing the aggregator would invert the dependency graph)",
        "rollback": "none (greenfield module; revert the file)",
        "rollout": "default_enabled (imported by seed.compose via ptcna.seed.__init__)",
        "since": "2026-06-05 (greenfield scaffold of the seed package, pre-consolidation `pcta`)",
        "storage_boundary": "none",
        "summary": "seed-layer heptagram routing motif and the recursive coherence-prime guard (composition counts are variable)",
        "tests": "tests.test_constants",
        "unresolved": "none (PCTA acronym, variable-count rule, and \"motion\" = Fickian flux J = \u2212D \u2207\u03c6 all resolved by maintainer)",
        "user_data_boundary": "none"
      },
      "file": "ptcna/seed/constants.py",
      "id": "seed_constants"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "given": "a sequence of ptcna.circle.CircleTensor objects",
        "then": "Seed stores and returns those shared circle values without a duplicate circle class"
      },
      "file": "ptcna/seed/tensor.py",
      "id": "seed_hosts_shared_circle_type"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "given": "any valid Seed",
        "then": "requires_grad is false and the seed owns no backward operation"
      },
      "file": "ptcna/seed/tensor.py",
      "id": "seed_is_non_differentiating"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "given": "hosted circles with opaque payloads",
        "then": "tensor_payloads returns the exact payload objects in structural anchor order"
      },
      "file": "ptcna/seed/tensor.py",
      "id": "seed_payload_roundtrip"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_seed_preserves_neural_scalar_without_owning_gradient",
        "cleanup": "none",
        "mutates": "none",
        "proves": "seed_composition_is_non_differentiating, seed_is_non_differentiating",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "ptcna/seed/tests/test_seed_contracts.py",
      "id": "check_seed_non_differentiating"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_seed_rejects_empty_input",
        "cleanup": "none",
        "mutates": "none",
        "proves": "seed_composition_rejects_empty",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "ptcna/seed/tests/test_seed_contracts.py",
      "id": "check_seed_rejects_empty"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_seed_uses_shared_circle_type",
        "cleanup": "none",
        "mutates": "none",
        "proves": "seed_composition_uses_shared_circle_type, seed_hosts_shared_circle_type, seed_payload_roundtrip",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "ptcna/seed/tests/test_seed_contracts.py",
      "id": "check_seed_shared_circle_type"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_broken_graph_exposes_each_required_gap",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "contract_audit_exposes_broken_edges",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "ptcna/tests/test_contract_audit.py",
      "id": "check_contract_audit_broken_edges"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_complete_graph_closes",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "contract_audit_closes_complete_graph",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "ptcna/tests/test_contract_audit.py",
      "id": "check_contract_audit_complete_graph"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_critical_plan_is_balanced_and_digest_locked",
        "cleanup": "none",
        "mutates": "none",
        "proves": "ptcna_critical_plan_digest_locked",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "ptcna/tests/test_critical_evaluation.py",
      "id": "check_ptcna_critical_plan_digest"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_sealed_result_digest_and_independent_verdict_replay",
        "cleanup": "none",
        "mutates": "none",
        "proves": "ptcna_critical_result_content_addressed",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "ptcna/tests/test_critical_evaluation.py",
      "id": "check_ptcna_critical_result_digest"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_comparator_failure_is_unresolved_and_parity_is_not_superiority",
        "cleanup": "none",
        "mutates": "none",
        "proves": "ptcna_evaluation_propagates_backend_failure, ptcna_evaluation_verdict_uses_frozen_thresholds",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "ptcna/tests/test_evaluation.py",
      "id": "check_ptcna_comparator_failure_and_parity"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_backend_failure_stops_with_preselected_status",
        "cleanup": "none",
        "mutates": "none",
        "proves": "ptcna_evaluation_propagates_backend_failure",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "ptcna/tests/test_evaluation.py",
      "id": "check_ptcna_failure_propagation"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_frozen_thresholds_produce_survival_and_falsification",
        "cleanup": "none",
        "mutates": "none",
        "proves": "ptcna_evaluation_verdict_uses_frozen_thresholds",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "ptcna/tests/test_evaluation.py",
      "id": "check_ptcna_frozen_verdicts"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_plan_digest_is_stable_and_criteria_sensitive",
        "cleanup": "none",
        "mutates": "none",
        "proves": "ptcna_evaluation_plan_freezes_verdict_inputs",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "ptcna/tests/test_evaluation.py",
      "id": "check_ptcna_plan_digest"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_target_failure_requires_explicit_attributed_failover",
        "cleanup": "none",
        "mutates": "none",
        "proves": "ptcna_failover_is_explicit_and_attributed",
        "requires": "python3, numpy",
        "timeout": "30"
      },
      "file": "ptcna/tests/test_runtime.py",
      "id": "check_ptcna_explicit_failover"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_fallback_is_deterministic_bounded_and_distinct",
        "cleanup": "none",
        "mutates": "none",
        "proves": "ptcna_fallback_is_distinct_and_deterministic",
        "requires": "python3, numpy",
        "timeout": "30"
      },
      "file": "ptcna/tests/test_runtime.py",
      "id": "check_ptcna_fallback_determinism"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_fallback_positive_reward_increases_selected_score",
        "cleanup": "none",
        "mutates": "none",
        "proves": "ptcna_fallback_reward_changes_selected_score",
        "requires": "python3, numpy",
        "timeout": "30"
      },
      "file": "ptcna/tests/test_runtime.py",
      "id": "check_ptcna_fallback_reward"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_reward_follows_the_recorded_backend",
        "cleanup": "none",
        "mutates": "none",
        "proves": "ptcna_reward_follows_backend_receipt",
        "requires": "python3, numpy",
        "timeout": "30"
      },
      "file": "ptcna/tests/test_runtime.py",
      "id": "check_ptcna_reward_route"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_root_exports_runtime_and_evaluation_surface",
        "cleanup": "none",
        "mutates": "none",
        "proves": "ptcna_root_exports_runtime_boundary",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "ptcna/tests/test_runtime.py",
      "id": "check_ptcna_root_runtime_exports"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_target_reports_all_four_live_layers",
        "cleanup": "none",
        "mutates": "none",
        "proves": "ptcna_target_reports_four_live_layers",
        "requires": "python3, numpy",
        "timeout": "30"
      },
      "file": "ptcna/tests/test_runtime.py",
      "id": "check_ptcna_target_four_layers"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_materialized_state_identity_is_reported",
        "cleanup": "none",
        "mutates": "none",
        "proves": "ptcna_ucns_state_is_independently_verified",
        "requires": "python3, numpy, ucns",
        "timeout": "10"
      },
      "file": "ptcna/tests/test_ucns_integration.py",
      "id": "check_ptcna_ucns_independent_state"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_bundled_receipt_activates_exact_pinned_producer",
        "cleanup": "none",
        "mutates": "none",
        "proves": "ptcna_ucns_receipt_is_producer_validated",
        "requires": "python3, numpy, ucns",
        "timeout": "10"
      },
      "file": "ptcna/tests/test_ucns_integration.py",
      "id": "check_ptcna_ucns_producer_validation"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_uncovered_shape_is_explicitly_suspended",
        "cleanup": "none",
        "mutates": "none",
        "proves": "ptcna_ucns_tampering_fails_closed",
        "requires": "python3, numpy, ucns",
        "timeout": "10"
      },
      "file": "ptcna/tests/test_ucns_integration.py",
      "id": "check_ptcna_ucns_shape_suspension"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_tampered_receipt_is_rejected",
        "cleanup": "none",
        "mutates": "none",
        "proves": "ptcna_ucns_tampering_fails_closed",
        "requires": "python3, numpy, ucns",
        "timeout": "10"
      },
      "file": "ptcna/tests/test_ucns_integration.py",
      "id": "check_ptcna_ucns_tamper_rejection"
    },
    {
      "block": "BOUNDARIES",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "pii": "none",
        "secrets": "none",
        "since": "unreleased",
        "storage_boundary": "read bundled immutable receipt",
        "summary": "validates a bundled immutable producer receipt and materializes deterministic in-memory state without network, authentication, user-data, or administrative effects",
        "user_data_boundary": "none"
      },
      "file": "ptcna/ucns_integration.py",
      "id": "ptcna_ucns_integration_runtime_boundary"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "PTCNA consumes a UCNS candidate-state receipt",
        "then": "the exact pinned UCNS validator accepts every authority-bearing field before PTCNA materializes state"
      },
      "file": "ptcna/ucns_integration.py",
      "id": "ptcna_ucns_receipt_is_producer_validated"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "the producer receipt passes UCNS validation",
        "then": "PTCNA independently materializes C-order little-endian float64 positive-zero state and matches its shape, byte count, and digest"
      },
      "file": "ptcna/ucns_integration.py",
      "id": "ptcna_ucns_state_is_independently_verified"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "receipt content or expected state shape differs",
        "then": "consumption raises or returns an explicit suspended status without substituting PTCNA-local provenance"
      },
      "file": "ptcna/ucns_integration.py",
      "id": "ptcna_ucns_tampering_fails_closed"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_receipt_status, _suspended_status",
        "module_kind": "adapter",
        "module_name": "ucns_integration",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "UCNSIntegrationState, UCNSIntegrationStatus, UCNSReceiptError, consume_ucns_receipt, load_bundled_ucns_receipt, ucns_integration_status, require_ucns_integration",
        "requires": "ucns_ptcna_candidate_state",
        "rollback": "restore typed suspension while retaining PTCNA-local composition and fallback",
        "rollout": "active only for the exact bundled producer receipt and matching state contract",
        "since": "unreleased",
        "storage_boundary": "read bundled immutable receipt",
        "summary": "consumes the exactly pinned UCNS 157x7x7x53 candidate receipt and independently verifies the target state bytes",
        "tests": "ptcna/tests/test_ucns_integration.py",
        "unresolved": "continuous seven-fold geometry, representative efficacy, and production privacy",
        "user_data_boundary": "none"
      },
      "file": "ptcna/ucns_integration.py",
      "id": "ptcna_ucns_integration"
    },
    {
      "block": "BOUNDARIES",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "pii": "none",
        "secrets": "none",
        "since": "0.1.1",
        "storage_boundary": "read repository source",
        "summary": "reads repository source text and Python syntax without importing modules or mutating files",
        "user_data_boundary": "none"
      },
      "file": "scripts/check_contracts.py",
      "id": "contract_audit_repository_boundary"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "unique contracts and checks whose proves targets and self calls all resolve",
        "then": "audit returns no gaps"
      },
      "file": "scripts/check_contracts.py",
      "id": "contract_audit_closes_complete_graph"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "an orphan contract, unknown proves target, unresolved self call, or undeclared executable test",
        "then": "audit returns a visible GAP for every broken edge"
      },
      "file": "scripts/check_contracts.py",
      "id": "contract_audit_exposes_broken_edges"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_definitions, _split",
        "module_kind": "verification",
        "module_name": "contract audit",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "audit, main",
        "requires": "vendored msdmd parser",
        "rollback": "remove the gate without changing runtime code",
        "rollout": "release gate",
        "since": "0.1.1",
        "storage_boundary": "read repository source",
        "summary": "reconciles source CONTRACTS with test CHECKS using syntax-only call resolution",
        "tests": "ptcna/tests/test_contract_audit.py",
        "unresolved": "mutation sensitivity remains outside this syntax-only audit",
        "user_data_boundary": "none"
      },
      "file": "scripts/check_contracts.py",
      "id": "ptcna_contract_audit"
    }
  ],
  "edges": [
    {
      "from": "circle_composition_runtime_boundary",
      "kind": "owns",
      "source_block": "BOUNDARIES",
      "source_id": "circle_composition_runtime_boundary",
      "to": "Erin Spencer"
    },
    {
      "from": "circle_tensor_runtime_boundary",
      "kind": "owns",
      "source_block": "BOUNDARIES",
      "source_id": "circle_tensor_runtime_boundary",
      "to": "Erin Spencer"
    },
    {
      "from": "contract_audit_repository_boundary",
      "kind": "owns",
      "source_block": "BOUNDARIES",
      "source_id": "contract_audit_repository_boundary",
      "to": "Erin Spencer"
    },
    {
      "from": "fiq_runtime_boundary",
      "kind": "owns",
      "source_block": "BOUNDARIES",
      "source_id": "fiq_runtime_boundary",
      "to": "Erin Spencer"
    },
    {
      "from": "neural_scalar_runtime_boundary",
      "kind": "owns",
      "source_block": "BOUNDARIES",
      "source_id": "neural_scalar_runtime_boundary",
      "to": "Erin Spencer"
    },
    {
      "from": "pcna_checkpoint_runtime_boundary",
      "kind": "owns",
      "source_block": "BOUNDARIES",
      "source_id": "pcna_checkpoint_runtime_boundary",
      "to": "Erin Spencer"
    },
    {
      "from": "prime_core_composition_runtime_boundary",
      "kind": "owns",
      "source_block": "BOUNDARIES",
      "source_id": "prime_core_composition_runtime_boundary",
      "to": "Erin Spencer"
    },
    {
      "from": "ptcna_critical_evaluation_local_receipt",
      "kind": "owns",
      "source_block": "BOUNDARIES",
      "source_id": "ptcna_critical_evaluation_local_receipt",
      "to": "Erin Spencer"
    },
    {
      "from": "ptcna_evaluation_local_boundary",
      "kind": "owns",
      "source_block": "BOUNDARIES",
      "source_id": "ptcna_evaluation_local_boundary",
      "to": "Erin Spencer"
    },
    {
      "from": "ptcna_package_import_boundary",
      "kind": "owns",
      "source_block": "BOUNDARIES",
      "source_id": "ptcna_package_import_boundary",
      "to": "Erin Spencer"
    },
    {
      "from": "ptcna_runtime_local_boundary",
      "kind": "owns",
      "source_block": "BOUNDARIES",
      "source_id": "ptcna_runtime_local_boundary",
      "to": "Erin Spencer"
    },
    {
      "from": "ptcna_ucns_integration_runtime_boundary",
      "kind": "owns",
      "source_block": "BOUNDARIES",
      "source_id": "ptcna_ucns_integration_runtime_boundary",
      "to": "Erin Spencer"
    },
    {
      "from": "zeta_external_measurement_boundary",
      "kind": "owns",
      "source_block": "BOUNDARIES",
      "source_id": "zeta_external_measurement_boundary",
      "to": "Erin Spencer"
    },
    {
      "from": "check_circle_identity_fallback",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_circle_identity_fallback",
      "to": "self::test_non_coprime_count_uses_identity_fallback"
    },
    {
      "from": "check_circle_identity_fallback",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_circle_identity_fallback",
      "to": "circle_composition_preserves_order_and_identity"
    },
    {
      "from": "check_circle_identity_fallback",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_circle_identity_fallback",
      "to": "python3"
    },
    {
      "from": "check_circle_non_differentiating",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_circle_non_differentiating",
      "to": "self::test_circle_does_not_own_neural_payload_gradients"
    },
    {
      "from": "check_circle_non_differentiating",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_circle_non_differentiating",
      "to": "circle_tensor_is_non_differentiating"
    },
    {
      "from": "check_circle_non_differentiating",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_circle_non_differentiating",
      "to": "python3"
    },
    {
      "from": "check_circle_rejects_empty",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_circle_rejects_empty",
      "to": "self::test_empty_circle_is_rejected"
    },
    {
      "from": "check_circle_rejects_empty",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_circle_rejects_empty",
      "to": "circle_composition_rejects_empty_input"
    },
    {
      "from": "check_circle_rejects_empty",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_circle_rejects_empty",
      "to": "python3"
    },
    {
      "from": "check_circle_roundtrip",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_circle_roundtrip",
      "to": "self::test_circle_preserves_exact_payload_objects"
    },
    {
      "from": "check_circle_roundtrip",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_circle_roundtrip",
      "to": "circle_composition_preserves_order_and_identity"
    },
    {
      "from": "check_circle_roundtrip",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_circle_roundtrip",
      "to": "circle_tensor_round_trips_payloads"
    },
    {
      "from": "check_circle_roundtrip",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_circle_roundtrip",
      "to": "python3"
    },
    {
      "from": "check_contract_audit_broken_edges",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_broken_edges",
      "to": "self::test_broken_graph_exposes_each_required_gap"
    },
    {
      "from": "check_contract_audit_broken_edges",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_broken_edges",
      "to": "contract_audit_exposes_broken_edges"
    },
    {
      "from": "check_contract_audit_broken_edges",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_broken_edges",
      "to": "python3"
    },
    {
      "from": "check_contract_audit_complete_graph",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_complete_graph",
      "to": "self::test_complete_graph_closes"
    },
    {
      "from": "check_contract_audit_complete_graph",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_complete_graph",
      "to": "contract_audit_closes_complete_graph"
    },
    {
      "from": "check_contract_audit_complete_graph",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_complete_graph",
      "to": "python3"
    },
    {
      "from": "check_fiq_has_no_gradient_ownership",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_fiq_has_no_gradient_ownership",
      "to": "self::test_fiq_is_non_differentiating_with_neural_payload"
    },
    {
      "from": "check_fiq_has_no_gradient_ownership",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_fiq_has_no_gradient_ownership",
      "to": "fiq_never_owns_gradients"
    },
    {
      "from": "check_fiq_has_no_gradient_ownership",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_fiq_has_no_gradient_ownership",
      "to": "python3"
    },
    {
      "from": "check_fiq_payload_identity",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_fiq_payload_identity",
      "to": "self::test_payload_roundtrip_identity"
    },
    {
      "from": "check_fiq_payload_identity",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_fiq_payload_identity",
      "to": "fiq_payload_is_opaque_and_lossless"
    },
    {
      "from": "check_fiq_payload_identity",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_fiq_payload_identity",
      "to": "python3"
    },
    {
      "from": "check_neural_scalar_backprop",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_neural_scalar_backprop",
      "to": "self::test_backward_accumulates_expected_gradient"
    },
    {
      "from": "check_neural_scalar_backprop",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_neural_scalar_backprop",
      "to": "neural_scalar_owns_backprop"
    },
    {
      "from": "check_neural_scalar_backprop",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_neural_scalar_backprop",
      "to": "python3"
    },
    {
      "from": "check_neural_scalar_tape_ops",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_neural_scalar_tape_ops",
      "to": "self::test_tape_contains_only_neural_scalar_ops"
    },
    {
      "from": "check_neural_scalar_tape_ops",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_neural_scalar_tape_ops",
      "to": "neural_scalar_uses_no_structural_operator"
    },
    {
      "from": "check_neural_scalar_tape_ops",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_neural_scalar_tape_ops",
      "to": "python3"
    },
    {
      "from": "check_pcna_checkpoint_roundtrip",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_pcna_checkpoint_roundtrip",
      "to": "self::test_checkpoint_roundtrip"
    },
    {
      "from": "check_pcna_checkpoint_roundtrip",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_pcna_checkpoint_roundtrip",
      "to": "pcna_checkpoint_round_trips_ring_state"
    },
    {
      "from": "check_pcna_checkpoint_roundtrip",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_pcna_checkpoint_roundtrip",
      "to": "numpy"
    },
    {
      "from": "check_pcna_checkpoint_roundtrip",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_pcna_checkpoint_roundtrip",
      "to": "python3"
    },
    {
      "from": "check_pcna_reward",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_pcna_reward",
      "to": "self::test_reward_reports_one_memory_flush_result"
    },
    {
      "from": "check_pcna_reward",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_pcna_reward",
      "to": "pcna_reward_updates_neural_and_timing_state"
    },
    {
      "from": "check_pcna_reward",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_pcna_reward",
      "to": "numpy"
    },
    {
      "from": "check_pcna_reward",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_pcna_reward",
      "to": "python3"
    },
    {
      "from": "check_pcna_six_step_pipeline",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_pcna_six_step_pipeline",
      "to": "self::test_infer_reports_all_six_steps"
    },
    {
      "from": "check_pcna_six_step_pipeline",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_pcna_six_step_pipeline",
      "to": "pcna_infer_reports_complete_six_step_pipeline"
    },
    {
      "from": "check_pcna_six_step_pipeline",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_pcna_six_step_pipeline",
      "to": "numpy"
    },
    {
      "from": "check_pcna_six_step_pipeline",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_pcna_six_step_pipeline",
      "to": "python3"
    },
    {
      "from": "check_prime_core_default_profile",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_default_profile",
      "to": "self::test_canon_structure_counts"
    },
    {
      "from": "check_prime_core_default_profile",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_default_profile",
      "to": "prime_core_default_profile_is_stable"
    },
    {
      "from": "check_prime_core_default_profile",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_default_profile",
      "to": "python3"
    },
    {
      "from": "check_prime_core_no_gradient_ownership",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_no_gradient_ownership",
      "to": "self::test_neural_payload_gradients_remain_neural_owned"
    },
    {
      "from": "check_prime_core_no_gradient_ownership",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_no_gradient_ownership",
      "to": "prime_core_is_non_differentiating"
    },
    {
      "from": "check_prime_core_no_gradient_ownership",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_no_gradient_ownership",
      "to": "python3"
    },
    {
      "from": "check_prime_core_payload_width",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_payload_width",
      "to": "self::test_payload_factory_width_is_checked"
    },
    {
      "from": "check_prime_core_payload_width",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_payload_width",
      "to": "prime_core_payload_width_matches_spec"
    },
    {
      "from": "check_prime_core_payload_width",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_payload_width",
      "to": "python3"
    },
    {
      "from": "check_prime_core_positive_counts",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_positive_counts",
      "to": "self::test_core_spec_rejects_nonpositive_counts"
    },
    {
      "from": "check_prime_core_positive_counts",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_positive_counts",
      "to": "prime_core_counts_are_positive"
    },
    {
      "from": "check_prime_core_positive_counts",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_positive_counts",
      "to": "python3"
    },
    {
      "from": "check_prime_core_shared_layer_types",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_shared_layer_types",
      "to": "self::test_core_uses_circle_and_seed_owned_types"
    },
    {
      "from": "check_prime_core_shared_layer_types",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_shared_layer_types",
      "to": "prime_core_uses_shared_layer_types"
    },
    {
      "from": "check_prime_core_shared_layer_types",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_shared_layer_types",
      "to": "python3"
    },
    {
      "from": "check_prime_core_ucns_scope",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_ucns_scope",
      "to": "self::test_ucns_attribution_is_exactly_shape_scoped"
    },
    {
      "from": "check_prime_core_ucns_scope",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_ucns_scope",
      "to": "prime_core_ucns_receipt_scope_is_exact"
    },
    {
      "from": "check_prime_core_ucns_scope",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_core_ucns_scope",
      "to": "python3"
    },
    {
      "from": "check_ptcna_comparator_failure_and_parity",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_comparator_failure_and_parity",
      "to": "self::test_comparator_failure_is_unresolved_and_parity_is_not_superiority"
    },
    {
      "from": "check_ptcna_comparator_failure_and_parity",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_comparator_failure_and_parity",
      "to": "ptcna_evaluation_propagates_backend_failure"
    },
    {
      "from": "check_ptcna_comparator_failure_and_parity",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_comparator_failure_and_parity",
      "to": "ptcna_evaluation_verdict_uses_frozen_thresholds"
    },
    {
      "from": "check_ptcna_comparator_failure_and_parity",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_comparator_failure_and_parity",
      "to": "python3"
    },
    {
      "from": "check_ptcna_critical_plan_digest",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_critical_plan_digest",
      "to": "self::test_critical_plan_is_balanced_and_digest_locked"
    },
    {
      "from": "check_ptcna_critical_plan_digest",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_critical_plan_digest",
      "to": "ptcna_critical_plan_digest_locked"
    },
    {
      "from": "check_ptcna_critical_plan_digest",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_critical_plan_digest",
      "to": "python3"
    },
    {
      "from": "check_ptcna_critical_result_digest",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_critical_result_digest",
      "to": "self::test_sealed_result_digest_and_independent_verdict_replay"
    },
    {
      "from": "check_ptcna_critical_result_digest",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_critical_result_digest",
      "to": "ptcna_critical_result_content_addressed"
    },
    {
      "from": "check_ptcna_critical_result_digest",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_critical_result_digest",
      "to": "python3"
    },
    {
      "from": "check_ptcna_explicit_failover",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_explicit_failover",
      "to": "self::test_target_failure_requires_explicit_attributed_failover"
    },
    {
      "from": "check_ptcna_explicit_failover",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_explicit_failover",
      "to": "ptcna_failover_is_explicit_and_attributed"
    },
    {
      "from": "check_ptcna_explicit_failover",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_explicit_failover",
      "to": "numpy"
    },
    {
      "from": "check_ptcna_explicit_failover",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_explicit_failover",
      "to": "python3"
    },
    {
      "from": "check_ptcna_failure_propagation",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_failure_propagation",
      "to": "self::test_backend_failure_stops_with_preselected_status"
    },
    {
      "from": "check_ptcna_failure_propagation",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_failure_propagation",
      "to": "ptcna_evaluation_propagates_backend_failure"
    },
    {
      "from": "check_ptcna_failure_propagation",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_failure_propagation",
      "to": "python3"
    },
    {
      "from": "check_ptcna_fallback_determinism",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_fallback_determinism",
      "to": "self::test_fallback_is_deterministic_bounded_and_distinct"
    },
    {
      "from": "check_ptcna_fallback_determinism",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_fallback_determinism",
      "to": "ptcna_fallback_is_distinct_and_deterministic"
    },
    {
      "from": "check_ptcna_fallback_determinism",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_fallback_determinism",
      "to": "numpy"
    },
    {
      "from": "check_ptcna_fallback_determinism",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_fallback_determinism",
      "to": "python3"
    },
    {
      "from": "check_ptcna_fallback_reward",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_fallback_reward",
      "to": "self::test_fallback_positive_reward_increases_selected_score"
    },
    {
      "from": "check_ptcna_fallback_reward",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_fallback_reward",
      "to": "ptcna_fallback_reward_changes_selected_score"
    },
    {
      "from": "check_ptcna_fallback_reward",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_fallback_reward",
      "to": "numpy"
    },
    {
      "from": "check_ptcna_fallback_reward",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_fallback_reward",
      "to": "python3"
    },
    {
      "from": "check_ptcna_frozen_verdicts",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_frozen_verdicts",
      "to": "self::test_frozen_thresholds_produce_survival_and_falsification"
    },
    {
      "from": "check_ptcna_frozen_verdicts",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_frozen_verdicts",
      "to": "ptcna_evaluation_verdict_uses_frozen_thresholds"
    },
    {
      "from": "check_ptcna_frozen_verdicts",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_frozen_verdicts",
      "to": "python3"
    },
    {
      "from": "check_ptcna_plan_digest",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_plan_digest",
      "to": "self::test_plan_digest_is_stable_and_criteria_sensitive"
    },
    {
      "from": "check_ptcna_plan_digest",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_plan_digest",
      "to": "ptcna_evaluation_plan_freezes_verdict_inputs"
    },
    {
      "from": "check_ptcna_plan_digest",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_plan_digest",
      "to": "python3"
    },
    {
      "from": "check_ptcna_reward_route",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_reward_route",
      "to": "self::test_reward_follows_the_recorded_backend"
    },
    {
      "from": "check_ptcna_reward_route",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_reward_route",
      "to": "ptcna_reward_follows_backend_receipt"
    },
    {
      "from": "check_ptcna_reward_route",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_reward_route",
      "to": "numpy"
    },
    {
      "from": "check_ptcna_reward_route",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_reward_route",
      "to": "python3"
    },
    {
      "from": "check_ptcna_root_runtime_exports",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_root_runtime_exports",
      "to": "self::test_root_exports_runtime_and_evaluation_surface"
    },
    {
      "from": "check_ptcna_root_runtime_exports",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_root_runtime_exports",
      "to": "ptcna_root_exports_runtime_boundary"
    },
    {
      "from": "check_ptcna_root_runtime_exports",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_root_runtime_exports",
      "to": "python3"
    },
    {
      "from": "check_ptcna_target_four_layers",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_target_four_layers",
      "to": "self::test_target_reports_all_four_live_layers"
    },
    {
      "from": "check_ptcna_target_four_layers",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_target_four_layers",
      "to": "ptcna_target_reports_four_live_layers"
    },
    {
      "from": "check_ptcna_target_four_layers",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_target_four_layers",
      "to": "numpy"
    },
    {
      "from": "check_ptcna_target_four_layers",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_target_four_layers",
      "to": "python3"
    },
    {
      "from": "check_ptcna_ucns_independent_state",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_independent_state",
      "to": "self::test_materialized_state_identity_is_reported"
    },
    {
      "from": "check_ptcna_ucns_independent_state",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_independent_state",
      "to": "ptcna_ucns_state_is_independently_verified"
    },
    {
      "from": "check_ptcna_ucns_independent_state",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_independent_state",
      "to": "numpy"
    },
    {
      "from": "check_ptcna_ucns_independent_state",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_independent_state",
      "to": "python3"
    },
    {
      "from": "check_ptcna_ucns_independent_state",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_independent_state",
      "to": "ucns"
    },
    {
      "from": "check_ptcna_ucns_producer_validation",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_producer_validation",
      "to": "self::test_bundled_receipt_activates_exact_pinned_producer"
    },
    {
      "from": "check_ptcna_ucns_producer_validation",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_producer_validation",
      "to": "ptcna_ucns_receipt_is_producer_validated"
    },
    {
      "from": "check_ptcna_ucns_producer_validation",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_producer_validation",
      "to": "numpy"
    },
    {
      "from": "check_ptcna_ucns_producer_validation",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_producer_validation",
      "to": "python3"
    },
    {
      "from": "check_ptcna_ucns_producer_validation",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_producer_validation",
      "to": "ucns"
    },
    {
      "from": "check_ptcna_ucns_shape_suspension",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_shape_suspension",
      "to": "self::test_uncovered_shape_is_explicitly_suspended"
    },
    {
      "from": "check_ptcna_ucns_shape_suspension",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_shape_suspension",
      "to": "ptcna_ucns_tampering_fails_closed"
    },
    {
      "from": "check_ptcna_ucns_shape_suspension",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_shape_suspension",
      "to": "numpy"
    },
    {
      "from": "check_ptcna_ucns_shape_suspension",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_shape_suspension",
      "to": "python3"
    },
    {
      "from": "check_ptcna_ucns_shape_suspension",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_shape_suspension",
      "to": "ucns"
    },
    {
      "from": "check_ptcna_ucns_tamper_rejection",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_tamper_rejection",
      "to": "self::test_tampered_receipt_is_rejected"
    },
    {
      "from": "check_ptcna_ucns_tamper_rejection",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_tamper_rejection",
      "to": "ptcna_ucns_tampering_fails_closed"
    },
    {
      "from": "check_ptcna_ucns_tamper_rejection",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_tamper_rejection",
      "to": "numpy"
    },
    {
      "from": "check_ptcna_ucns_tamper_rejection",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_tamper_rejection",
      "to": "python3"
    },
    {
      "from": "check_ptcna_ucns_tamper_rejection",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_ptcna_ucns_tamper_rejection",
      "to": "ucns"
    },
    {
      "from": "check_seed_non_differentiating",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_seed_non_differentiating",
      "to": "self::test_seed_preserves_neural_scalar_without_owning_gradient"
    },
    {
      "from": "check_seed_non_differentiating",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_seed_non_differentiating",
      "to": "seed_composition_is_non_differentiating"
    },
    {
      "from": "check_seed_non_differentiating",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_seed_non_differentiating",
      "to": "seed_is_non_differentiating"
    },
    {
      "from": "check_seed_non_differentiating",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_seed_non_differentiating",
      "to": "python3"
    },
    {
      "from": "check_seed_rejects_empty",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_seed_rejects_empty",
      "to": "self::test_seed_rejects_empty_input"
    },
    {
      "from": "check_seed_rejects_empty",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_seed_rejects_empty",
      "to": "seed_composition_rejects_empty"
    },
    {
      "from": "check_seed_rejects_empty",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_seed_rejects_empty",
      "to": "python3"
    },
    {
      "from": "check_seed_shared_circle_type",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_seed_shared_circle_type",
      "to": "self::test_seed_uses_shared_circle_type"
    },
    {
      "from": "check_seed_shared_circle_type",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_seed_shared_circle_type",
      "to": "seed_composition_uses_shared_circle_type"
    },
    {
      "from": "check_seed_shared_circle_type",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_seed_shared_circle_type",
      "to": "seed_hosts_shared_circle_type"
    },
    {
      "from": "check_seed_shared_circle_type",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_seed_shared_circle_type",
      "to": "seed_payload_roundtrip"
    },
    {
      "from": "check_seed_shared_circle_type",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_seed_shared_circle_type",
      "to": "python3"
    },
    {
      "from": "check_zeta_external_metrics",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_zeta_external_metrics",
      "to": "self::test_external_provider_drives_phi_nudge"
    },
    {
      "from": "check_zeta_external_metrics",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_zeta_external_metrics",
      "to": "zeta_consumes_explicit_metrics"
    },
    {
      "from": "check_zeta_external_metrics",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_zeta_external_metrics",
      "to": "numpy"
    },
    {
      "from": "check_zeta_external_metrics",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_zeta_external_metrics",
      "to": "python3"
    },
    {
      "from": "check_zeta_no_shadow_edcm",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_zeta_no_shadow_edcm",
      "to": "self::test_removed_shadow_edcm_module_is_absent"
    },
    {
      "from": "check_zeta_no_shadow_edcm",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_zeta_no_shadow_edcm",
      "to": "zeta_never_imports_shadow_edcm"
    },
    {
      "from": "check_zeta_no_shadow_edcm",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_zeta_no_shadow_edcm",
      "to": "python3"
    },
    {
      "from": "check_zeta_suspends_without_provider",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_zeta_suspends_without_provider",
      "to": "self::test_evaluate_suspends_without_provider"
    },
    {
      "from": "check_zeta_suspends_without_provider",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_zeta_suspends_without_provider",
      "to": "zeta_requires_external_measurement_provider"
    },
    {
      "from": "check_zeta_suspends_without_provider",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_zeta_suspends_without_provider",
      "to": "numpy"
    },
    {
      "from": "check_zeta_suspends_without_provider",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_zeta_suspends_without_provider",
      "to": "python3"
    },
    {
      "from": "interdependent_work_graph_portfolio_plan",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "interdependent_work_graph_portfolio_plan",
      "to": "The-Interdependency/skill-lib maintainers"
    },
    {
      "from": "pcna_helix_vis",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_helix_vis",
      "to": "Erin Spencer"
    },
    {
      "from": "pcna_helix_vis",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_helix_vis",
      "to": "none"
    },
    {
      "from": "pcna_memory_core",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_memory_core",
      "to": "Erin Spencer"
    },
    {
      "from": "pcna_memory_core",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_memory_core",
      "to": "none"
    },
    {
      "from": "pcna_merge",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_merge",
      "to": "Erin Spencer"
    },
    {
      "from": "pcna_merge",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_merge",
      "to": "pcna_pcna"
    },
    {
      "from": "pcna_merge",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_merge",
      "to": "pcna_ring_core"
    },
    {
      "from": "pcna_pcna",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_pcna",
      "to": "Erin Spencer"
    },
    {
      "from": "pcna_pcna",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_pcna",
      "to": "pcna_memory_core"
    },
    {
      "from": "pcna_pcna",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_pcna",
      "to": "pcna_ring_core"
    },
    {
      "from": "pcna_pcna",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_pcna",
      "to": "pcna_theta"
    },
    {
      "from": "pcna_ring_core",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_ring_core",
      "to": "Erin Spencer"
    },
    {
      "from": "pcna_ring_core",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_ring_core",
      "to": "none"
    },
    {
      "from": "pcna_routing_loop",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_routing_loop",
      "to": "Erin Spencer"
    },
    {
      "from": "pcna_routing_loop",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_routing_loop",
      "to": "none"
    },
    {
      "from": "pcna_sigma",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_sigma",
      "to": "Erin Spencer"
    },
    {
      "from": "pcna_sigma",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_sigma",
      "to": "pcna_ring_core"
    },
    {
      "from": "pcna_tensor_engine",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_tensor_engine",
      "to": "Erin Spencer"
    },
    {
      "from": "pcna_tensor_engine",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_tensor_engine",
      "to": "none"
    },
    {
      "from": "pcna_theta",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_theta",
      "to": "Erin Spencer"
    },
    {
      "from": "pcna_theta",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_theta",
      "to": "none"
    },
    {
      "from": "pcna_topology",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_topology",
      "to": "Erin Spencer"
    },
    {
      "from": "pcna_topology",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_topology",
      "to": "none"
    },
    {
      "from": "pcna_zeta",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_zeta",
      "to": "Erin Spencer"
    },
    {
      "from": "pcna_zeta",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_zeta",
      "to": "pcna_pcna"
    },
    {
      "from": "pcna_zeta",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcna_zeta",
      "to": "pcna_sigma"
    },
    {
      "from": "prime_core_constants",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "prime_core_constants",
      "to": "Erin Spencer"
    },
    {
      "from": "prime_core_constants",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "prime_core_constants",
      "to": "coherence_primes (mirrored from interdependent_lib"
    },
    {
      "from": "prime_core_constants",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "prime_core_constants",
      "to": "not imported \u2014 would invert the dependency graph)"
    },
    {
      "from": "ptcna_circle_composition",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_circle_composition",
      "to": "Erin Spencer"
    },
    {
      "from": "ptcna_circle_composition",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_circle_composition",
      "to": "ptcna_circle_tensor"
    },
    {
      "from": "ptcna_circle_composition",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_circle_composition",
      "to": "ptcna_ucns_integration"
    },
    {
      "from": "ptcna_circle_tensor",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_circle_tensor",
      "to": "Erin Spencer"
    },
    {
      "from": "ptcna_circle_tensor",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_circle_tensor",
      "to": "none"
    },
    {
      "from": "ptcna_contract_audit",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_contract_audit",
      "to": "Erin Spencer"
    },
    {
      "from": "ptcna_contract_audit",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_contract_audit",
      "to": "vendored msdmd parser"
    },
    {
      "from": "ptcna_critical_evaluation",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_critical_evaluation",
      "to": "Erin Spencer"
    },
    {
      "from": "ptcna_critical_evaluation",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_critical_evaluation",
      "to": "ptcna_frozen_evaluation"
    },
    {
      "from": "ptcna_fiq_host",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_fiq_host",
      "to": "Erin Spencer"
    },
    {
      "from": "ptcna_fiq_host",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_fiq_host",
      "to": "none"
    },
    {
      "from": "ptcna_frozen_evaluation",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_frozen_evaluation",
      "to": "Erin Spencer"
    },
    {
      "from": "ptcna_frozen_evaluation",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_frozen_evaluation",
      "to": "ptcna_runtime_boundary"
    },
    {
      "from": "ptcna_neural_scalar",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_neural_scalar",
      "to": "Erin Spencer"
    },
    {
      "from": "ptcna_neural_scalar",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_neural_scalar",
      "to": "none"
    },
    {
      "from": "ptcna_package_surface",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_package_surface",
      "to": "Erin Spencer"
    },
    {
      "from": "ptcna_package_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_package_surface",
      "to": "ptcna_frozen_evaluation"
    },
    {
      "from": "ptcna_package_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_package_surface",
      "to": "ptcna_runtime_boundary"
    },
    {
      "from": "ptcna_package_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_package_surface",
      "to": "ptcna_ucns_integration"
    },
    {
      "from": "ptcna_prime_core_composition",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_prime_core_composition",
      "to": "Erin Spencer"
    },
    {
      "from": "ptcna_prime_core_composition",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_prime_core_composition",
      "to": "ptcna_circle_composition"
    },
    {
      "from": "ptcna_prime_core_composition",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_prime_core_composition",
      "to": "ptcna_fiq_host"
    },
    {
      "from": "ptcna_prime_core_composition",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_prime_core_composition",
      "to": "ptcna_seed_composition"
    },
    {
      "from": "ptcna_prime_core_composition",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_prime_core_composition",
      "to": "ptcna_ucns_integration"
    },
    {
      "from": "ptcna_runtime_boundary",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_runtime_boundary",
      "to": "Erin Spencer"
    },
    {
      "from": "ptcna_runtime_boundary",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_runtime_boundary",
      "to": "pcna_pcna"
    },
    {
      "from": "ptcna_runtime_boundary",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_runtime_boundary",
      "to": "ptcna_prime_core_composition"
    },
    {
      "from": "ptcna_ucns_integration",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_ucns_integration",
      "to": "Erin Spencer"
    },
    {
      "from": "ptcna_ucns_integration",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ptcna_ucns_integration",
      "to": "ucns_ptcna_candidate_state"
    },
    {
      "from": "seed_constants",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "seed_constants",
      "to": "Erin Patrick Spencer"
    },
    {
      "from": "seed_constants",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "seed_constants",
      "to": "NOT imported \u2014 importing the aggregator would invert the dependency graph)"
    },
    {
      "from": "seed_constants",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "seed_constants",
      "to": "coherence_primes (mirrored from interdependent_lib"
    }
  ],
  "gaps": [],
  "repo": "ptcna"
});
