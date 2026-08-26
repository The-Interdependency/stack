# stack

MSDMD book assembled from module-local declarations and repo collection points.

## Machine Companion

- Machine file: `docs/stack-msdmd.machine.json`
- Schema: `stack.msdmd.docs.v1`
- Source commit: `44cecb389150b31d378fd13b46fef34860142960`
- Source dirty at generation: `True`
- Regenerate: `PYTHONPATH=.:skill-lib python3 tools/stack_msdmd_docs.py --root . --repo stack`

## Summary

| Metric | Count |
|---|---:|
| Declarations | 1090 |
| Relationship edges | 1696 |
| Coverage gaps | 3 |
| Collection points | 5 |
| Source files scanned | 452 |
| Source files without direct MSDMD | 206 |

## Blocks

| Block | Count |
|---|---:|
| `BOUNDARIES` | 36 |
| `CAPABILITIES` | 26 |
| `CHECKS` | 400 |
| `CONTRACTS` | 406 |
| `DEPENDENCIES` | 5 |
| `DOCS` | 25 |
| `LLMS` | 5 |
| `MODULE_BUILD` | 181 |
| `OWNERS` | 6 |

## Chapters

## Chapter 1: Ahbg

0 declarations, 0 edges, 0 gaps, 0 collection points, 17 source files without direct MSDMD.

| Section | Declarations | Edges | Gaps | Unannotated |
|---|---:|---:|---:|---:|
| `codex` | 0 | 0 | 0 | 17 |

## Chapter 2: Backend

0 declarations, 0 edges, 0 gaps, 0 collection points, 0 source files without direct MSDMD.

## Chapter 3: Frontend

0 declarations, 0 edges, 0 gaps, 0 collection points, 0 source files without direct MSDMD.

## Chapter 4: Libs

0 declarations, 0 edges, 0 gaps, 0 collection points, 0 source files without direct MSDMD.

## Chapter 5: Research

1025 declarations, 1622 edges, 0 gaps, 4 collection points, 144 source files without direct MSDMD.

Collection points:
- `research/edcm/edcm_msdmd.ts`
- `research/metapat/metapat_msdmd.ts`
- `research/pcea/pcea_msdmd.ts`
- `research/ptcna/ptcna_msdmd.ts`

| Section | Declarations | Edges | Gaps | Unannotated |
|---|---:|---:|---:|---:|
| `edcm` | 221 | 430 | 0 | 36 |
| `epac` | 56 | 65 | 0 | 10 |
| `metapat` | 317 | 354 | 0 | 8 |
| `pcea` | 6 | 14 | 0 | 43 |
| `ptcna` | 121 | 220 | 0 | 41 |
| `ucns` | 304 | 539 | 0 | 6 |

### BOUNDARIES

- `edcm_ucns_fork_lint_boundary` in `research/edcm/edcm/ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - EDCM verifies authority-to-geometry binding but does not invent METAPAT meaning, alter UCNS algebra, or transfer proof status into measurement validity
- `generated_src_metapat_affixiation_harmonics_py_boundaries` in `research/metapat/src/metapat/affixiation_harmonics.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_affixiation_harmonics_boundary` in `research/metapat/src/metapat/affixiation_harmonics.py` (direct) - semantic question-form only; no canon amendment, UCNS topology or notation selection, EDCM measurement validation, physical-frequency claim, theorem transfer, or external truth claim
- `generated_src_metapat_application_py_boundaries` in `research/metapat/src/metapat/application.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_application_module_boundary` in `research/metapat/src/metapat/application.py` (direct) - application identity and semantic mapping only; no canon amendment, domain validation, EDCM measurement, formal proof, UCNS topology claim, or theorem-status transfer
- `generated_src_metapat_canon_py_boundaries` in `research/metapat/src/metapat/canon.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_canon_boundaries` in `research/metapat/src/metapat/canon.py` (direct) - static doctrine constants plus read-only verification of canon-bearing repository files
- `generated_src_metapat_catalog_py_boundaries` in `research/metapat/src/metapat/catalog.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_semantic_catalog_boundary` in `research/metapat/src/metapat/catalog.py` (direct) - catalog identity and semantic addressability only; no empirical state, EDCM value, formal proof, inferred UCNS containment, or consumer application meaning
- `generated_src_metapat_electromagnetic_pipe_py_boundaries` in `research/metapat/src/metapat/electromagnetic_pipe.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_electromagnetic_pipe_boundary` in `research/metapat/src/metapat/electromagnetic_pipe.py` (direct) - engineering proposal and optimization structure only; no electromagnetic, materials, insulation, thermal, fault, spacecraft, measurement, UCNS topology, or theorem-status validity claim
- `generated_src_metapat_envelope_py_boundaries` in `research/metapat/src/metapat/envelope.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_module_envelope_boundary` in `research/metapat/src/metapat/envelope.py` (direct) - semantic authority and provenance only; no UCNS algebra, EDCM measurement, theorem transfer, or empirical validation
- `generated_src_metapat_flow_plan_py_boundaries` in `research/metapat/src/metapat/flow_plan.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_flow_boundaries` in `research/metapat/src/metapat/flow_plan.py` (direct) - architecture status constants with no active external calls
- `generated_src_metapat_quantum_magnetism_py_boundaries` in `research/metapat/src/metapat/quantum_magnetism.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_quantum_magnetism_boundary` in `research/metapat/src/metapat/quantum_magnetism.py` (direct) - worked semantic mapping only; physics remains answerable to physics and no root, proof, measurement, UCNS topology, or theorem-status claim is made
- `generated_src_metapat_relations_py_boundaries` in `research/metapat/src/metapat/relations.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_semantic_relation_boundary` in `research/metapat/src/metapat/relations.py` (direct) - relation records declare semantic ancestry only; they do not prove ontology, measurement validity, UCNS topology, or constitutive containment
- `generated_src_metapat_ucns_phi_py_boundaries` in `research/metapat/src/metapat/ucns_phi.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_ucns_phi_boundary` in `research/metapat/src/metapat/ucns_phi.py` (direct) - METAPAT authorizes meaning but does not construct UCNS algebra, validate topology, or transfer proof/measurement status
- `generated_src_metapat_validation_py_boundaries` in `research/metapat/src/metapat/validation.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_contract_boundaries` in `research/metapat/src/metapat/validation.py` (direct) - pure deterministic conditions; no external effects, theorem verification, or empirical validity claim
- `ptcna_package_import_boundary` in `research/ptcna/ptcna/__init__.py` (direct, research/ptcna/ptcna_msdmd.ts) - imports local package definitions without constructing engines or performing persistence, network, authentication, user-data, or administrative effects
- `circle_composition_runtime_boundary` in `research/ptcna/ptcna/circle/compose.py` (direct, research/ptcna/ptcna_msdmd.ts) - performs deterministic in-memory structural composition without activating UCNS or touching external state
- `circle_tensor_runtime_boundary` in `research/ptcna/ptcna/circle/tensor.py` (direct, research/ptcna/ptcna_msdmd.ts) - stores caller-provided payload references in memory and performs no persistence, network, auth, or user-data operation
- `prime_core_composition_runtime_boundary` in `research/ptcna/ptcna/core/prime_core/core.py` (direct, research/ptcna/ptcna_msdmd.ts) - performs deterministic in-memory composition and creates no network, storage, auth, user-data, or external package effect
- `fiq_runtime_boundary` in `research/ptcna/ptcna/core/prime_core/fiq.py` (direct, research/ptcna/ptcna_msdmd.ts) - retains caller-provided object references in memory without inspecting content or touching external state
- `ptcna_critical_evaluation_local_receipt` in `research/ptcna/ptcna/critical_evaluation.py` (direct, research/ptcna/ptcna_msdmd.ts) - reads the repository-owned frozen plan and writes one caller-selected local JSON result without network, authentication, secrets, or user data
- `ptcna_evaluation_local_boundary` in `research/ptcna/ptcna/evaluation.py` (direct, research/ptcna/ptcna_msdmd.ts) - executes caller-supplied in-process backends and returns an in-memory receipt without persistence, network, authentication, user-data, or administrative effects
- `pcna_checkpoint_runtime_boundary` in `research/ptcna/ptcna/neural/pcna.py` (direct, research/ptcna/ptcna_msdmd.ts) - performs local numpy checkpoint reads and writes under the configured checkpoint directory
- `neural_scalar_runtime_boundary` in `research/ptcna/ptcna/neural/scalar.py` (direct, research/ptcna/ptcna_msdmd.ts) - performs in-memory scalar arithmetic without persistence, network access, or user-data handling
- `zeta_external_measurement_boundary` in `research/ptcna/ptcna/neural/zeta.py` (direct, research/ptcna/ptcna_msdmd.ts) - reads caller-supplied response text and invokes an injected callback whose network behavior is outside PTCNA authority
- `ptcna_runtime_local_boundary` in `research/ptcna/ptcna/runtime.py` (direct, research/ptcna/ptcna_msdmd.ts) - performs deterministic in-process inference and learning with no authentication, persistence, network, user-data, or administrative effect
- `ptcna_ucns_integration_runtime_boundary` in `research/ptcna/ptcna/ucns_integration.py` (direct, research/ptcna/ptcna_msdmd.ts) - validates a bundled immutable producer receipt and materializes deterministic in-memory state without network, authentication, user-data, or administrative effects
- `contract_audit_repository_boundary` in `research/ptcna/scripts/check_contracts.py` (direct, research/ptcna/ptcna_msdmd.ts) - reads repository source text and Python syntax without importing modules or mutating files

### CAPABILITIES

- `edcm_fail_closed_ucns_fork_lint` in `research/edcm/edcm/ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - validates every actual recursive UCNS payload fork against one exact METAPAT authorization and topology binding
- `generated_src_metapat_affixiation_harmonics_py_capabilities` in `research/metapat/src/metapat/affixiation_harmonics.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_affixiation_harmonics_semantics` in `research/metapat/src/metapat/affixiation_harmonics.py` (direct) - emits one deterministic catalog-bound application record for affixiation and time-agnostic harmonic relation
- `generated_src_metapat_application_py_capabilities` in `research/metapat/src/metapat/application.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_catalog_bound_application_modules` in `research/metapat/src/metapat/application.py` (direct) - binds application statements to exact catalog modules and preserves domain evidence boundaries without claim-status transfer
- `generated_src_metapat_canon_py_capabilities` in `research/metapat/src/metapat/canon.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_canon_constants` in `research/metapat/src/metapat/canon.py` (direct) - provides exact importable constants and deterministic identity for METAPAT root doctrine
- `generated_src_metapat_catalog_py_capabilities` in `research/metapat/src/metapat/catalog.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_addressable_semantic_catalog` in `research/metapat/src/metapat/catalog.py` (direct) - emits a deterministic complete catalog of current METAPAT doctrine and exact declared derivation edges
- `generated_src_metapat_electromagnetic_pipe_py_capabilities` in `research/metapat/src/metapat/electromagnetic_pipe.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_electromagnetic_pipe_fixture` in `research/metapat/src/metapat/electromagnetic_pipe.py` (direct) - emits one deterministic catalog-bound engineering application and typed device-design record for the nested three-phase pipe system
- `generated_src_metapat_envelope_py_capabilities` in `research/metapat/src/metapat/envelope.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_semantic_envelope` in `research/metapat/src/metapat/envelope.py` (direct) - emits deterministic immutable semantic constraints and provenance without calculated EDCM measurements
- `generated_src_metapat_flow_plan_py_capabilities` in `research/metapat/src/metapat/flow_plan.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_flow_status` in `research/metapat/src/metapat/flow_plan.py` (direct) - exposes distinct authority, runtime-data, and proof-status architecture declarations
- `generated_src_metapat_quantum_magnetism_py_capabilities` in `research/metapat/src/metapat/quantum_magnetism.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_quantum_magnetism_fixture` in `research/metapat/src/metapat/quantum_magnetism.py` (direct) - emits one deterministic catalog-bound application record for nuclear charge configuration and magnetic state formation
- `generated_src_metapat_relations_py_capabilities` in `research/metapat/src/metapat/relations.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_semantic_relation_records` in `research/metapat/src/metapat/relations.py` (direct) - emits deterministic semantic ancestry records with exact source provenance and no inherited proof or measurement status
- `generated_src_metapat_ucns_phi_py_capabilities` in `research/metapat/src/metapat/ucns_phi.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_constitutive_fork_authority` in `research/metapat/src/metapat/ucns_phi.py` (direct) - authorizes ordered simultaneous constitutive children of one METAPAT parent
- `generated_src_metapat_validation_py_capabilities` in `research/metapat/src/metapat/validation.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_canon_contract_checks` in `research/metapat/src/metapat/validation.py` (direct) - checks deterministic Python conditions associated with METAPAT statements without claiming proof or empirical validation

### CHECKS

- `check_goal_vector_contradiction_and_variance` in `research/edcm/tests/test_goal_vector_experiment.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_goal_vector_exact_ucns_report` in `research/edcm/tests/test_goal_vector_experiment.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_goal_vector_na_boundary` in `research/edcm/tests/test_goal_vector_experiment.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_goal_vector_same_occurrences_order` in `research/edcm/tests/test_goal_vector_experiment.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_goal_vector_sealed_evidence` in `research/edcm/tests/test_goal_vector_experiment.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `closed_gonol_atomic_at_any_scale_check` in `research/edcm/tests/test_gonol_constructor.py` (direct, research/edcm/edcm_msdmd.ts) - closed_gonol_atomic_at_any_scale
- `construction_survives_absent_ucns_geometry_check` in `research/edcm/tests/test_gonol_constructor.py` (direct, research/edcm/edcm_msdmd.ts) - construction_survives_absent_ucns_geometry
- `geometry_mismatch_fails_closed_check` in `research/edcm/tests/test_gonol_constructor.py` (direct, research/edcm/edcm_msdmd.ts) - geometry_mismatch_fails_closed
- `single_constructor_uses_scale_option_sets_check` in `research/edcm/tests/test_gonol_constructor.py` (direct, research/edcm/edcm_msdmd.ts) - single_constructor_uses_scale_option_sets
- `suffix_exception_carried_by_suffix_gonol_check` in `research/edcm/tests/test_gonol_constructor.py` (direct, research/edcm/edcm_msdmd.ts) - suffix_exception_carried_by_suffix_gonol
- `unified_candidate_does_not_select_canon_check` in `research/edcm/tests/test_gonol_constructor.py` (direct, research/edcm/edcm_msdmd.ts) - unified_candidate_does_not_select_canon
- `language_relational_branch_check` in `research/edcm/tests/test_language_relational_bridge.py` (direct, research/edcm/edcm_msdmd.ts) - lexical_branches_are_independently_constructed, english_metadata_is_external_to_ucns_carrier, lexical_ucns_producer_is_exactly_verified, lexical_relation_multiplicity_is_preserved, lexical_pre_replay_status_is_unresolved, comparison_requires_two_prior_freezes, lexical_manifest_preserves_authority_firewall
- `oewn_builder_order_check` in `research/edcm/tests/test_language_relational_bridge.py` (direct, research/edcm/edcm_msdmd.ts) - oewn_source_is_exact_pinned_and_resumable, incomplete_or_altered_lexical_resume_fails_closed, lexical_comparison_occurs_after_freeze
- `check_multiwoz_booking_outcome_calibration_precedes_test` in `research/edcm/tests/test_multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_multiwoz_booking_outcome_destinations_do_not_collide` in `research/edcm/tests/test_multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_multiwoz_booking_outcome_hypothesis_failure_is_evidence` in `research/edcm/tests/test_multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_multiwoz_booking_outcome_labelled_response_is_withheld` in `research/edcm/tests/test_multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_multiwoz_booking_outcome_repeat_requires_complete_execution` in `research/edcm/tests/test_multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_multiwoz_booking_outcome_report_is_aggregate_only` in `research/edcm/tests/test_multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_multiwoz_booking_outcome_runtime_matches_recorded_checkout` in `research/edcm/tests/test_multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_multiwoz_booking_outcome_sealed_evidence` in `research/edcm/tests/test_multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_multiwoz_booking_outcome_status_does_not_transfer` in `research/edcm/tests/test_multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_multiwoz_booking_outcome_uncertainty_is_cluster_aware` in `research/edcm/tests/test_multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_multiwoz21_admission_precedes_execution` in `research/edcm/tests/test_multiwoz21_corpus.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_multiwoz21_completion_requires_reconciliation` in `research/edcm/tests/test_multiwoz21_corpus.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_multiwoz21_every_turn_is_observed_exactly_once` in `research/edcm/tests/test_multiwoz21_corpus.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_multiwoz21_failure_is_receipted` in `research/edcm/tests/test_multiwoz21_corpus.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_multiwoz21_ucns_v0141_false_receipt_rejected` in `research/edcm/tests/test_multiwoz21_corpus.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_multiwoz21_ucns_v0141_receipt_matches_source_native_run` in `research/edcm/tests/test_multiwoz21_corpus.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_multiwoz21_written_outputs_exclude_raw_text` in `research/edcm/tests/test_multiwoz21_corpus.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_recovered_dissonance_external_evaluator_aggregate_only` in `research/edcm/tests/test_recovered_dissonance_external_evaluator.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_recovered_dissonance_external_evaluator_failure_propagation` in `research/edcm/tests/test_recovered_dissonance_external_evaluator.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_recovered_dissonance_external_evaluator_frozen` in `research/edcm/tests/test_recovered_dissonance_external_evaluator.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_recovered_dissonance_external_evaluator_nonpromotion` in `research/edcm/tests/test_recovered_dissonance_external_evaluator.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_recovered_dissonance_external_packet_identity` in `research/edcm/tests/test_recovered_dissonance_external_evaluator.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_tarot_auto_fetch_rights_gate` in `research/edcm/tests/test_tarot_corpus_acquisition.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_tarot_completed_resume_fails_closed` in `research/edcm/tests/test_tarot_corpus_acquisition.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_tarot_fetch_authority_and_metadata_only_boundary` in `research/edcm/tests/test_tarot_corpus_acquisition.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_tarot_interrupted_resume_checkpoint` in `research/edcm/tests/test_tarot_corpus_acquisition.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_tarot_manifest_preserves_preontology_boundary` in `research/edcm/tests/test_tarot_corpus_acquisition.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_tarot_ocr_v4_accuracy` in `research/edcm/tests/test_tarot_ocr_v4.py` (direct, research/edcm/edcm_msdmd.ts) - tarot_ocr_v4_applies_frozen_accuracy_rule
- `check_tarot_ocr_v4_determinism` in `research/edcm/tests/test_tarot_ocr_v4.py` (direct, research/edcm/edcm_msdmd.ts) - tarot_ocr_v4_serialization_is_deterministic
- `check_tarot_ocr_v4_identity_and_resume` in `research/edcm/tests/test_tarot_ocr_v4.py` (direct, research/edcm/edcm_msdmd.ts) - tarot_ocr_v4_verifies_every_frozen_identity, tarot_ocr_v4_resume_fails_closed
- `check_tarot_ocr_v4_raw_evidence` in `research/edcm/tests/test_tarot_ocr_v4.py` (direct, research/edcm/edcm_msdmd.ts) - tarot_ocr_v4_preserves_raw_page_evidence
- `check_tarot_ocr_v5_core_identity` in `research/edcm/tests/test_tarot_ocr_v5.py` (direct, research/edcm/edcm_msdmd.ts) - tarot_ocr_v5_retains_v4_evidence_contracts
- `check_tarot_ocr_v5_single_change` in `research/edcm/tests/test_tarot_ocr_v5.py` (direct, research/edcm/edcm_msdmd.ts) - tarot_ocr_v5_changes_only_frozen_thresholding
- `check_tarot_ocr_v6_core_identity` in `research/edcm/tests/test_tarot_ocr_v6.py` (direct, research/edcm/edcm_msdmd.ts) - tarot_ocr_v6_retains_v4_evidence_contracts
- `check_tarot_ocr_v6_model_identity` in `research/edcm/tests/test_tarot_ocr_v6.py` (direct, research/edcm/edcm_msdmd.ts) - tarot_ocr_v6_verifies_historic_model
- `check_tarot_ocr_v6_single_change` in `research/edcm/tests/test_tarot_ocr_v6.py` (direct, research/edcm/edcm_msdmd.ts) - tarot_ocr_v6_changes_only_frozen_model
- `check_tarot_ocr_v7_inherited_identity` in `research/edcm/tests/test_tarot_ocr_v7.py` (direct, research/edcm/edcm_msdmd.ts) - tarot_ocr_v7_retains_v6_instrument
- `check_tarot_ocr_v7_renderer_repair` in `research/edcm/tests/test_tarot_ocr_v7.py` (direct, research/edcm/edcm_msdmd.ts) - tarot_ocr_v7_repairs_only_renderer_activation
- `check_tarot_text_gate_frozen_thresholds` in `research/edcm/tests/test_tarot_pdf_text_layer_gate.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_tarot_discovery_complete_acquisition_and_determinism` in `research/edcm/tests/test_tarot_relation_discovery.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_tarot_discovery_documented_cli` in `research/edcm/tests/test_tarot_relation_discovery.py` (direct, research/edcm/edcm_msdmd.ts) - python3, posix_shell
- `check_tarot_discovery_exact_order_values_and_absence` in `research/edcm/tests/test_tarot_relation_discovery.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_tarot_discovery_mechanical_bounds` in `research/edcm/tests/test_tarot_relation_discovery.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_edcm_ucns_exact_profile_only` in `research/edcm/tests/test_ucns_adapter.py` (direct, research/edcm/edcm_msdmd.ts) - edcm_ucns_exact_profile_only
- `check_edcm_ucns_full_turn_observation` in `research/edcm/tests/test_ucns_adapter.py` (direct, research/edcm/edcm_msdmd.ts) - edcm_ucns_full_turn_observation
- `check_edcm_ucns_no_geometry_or_proof_transfer` in `research/edcm/tests/test_ucns_adapter.py` (direct, research/edcm/edcm_msdmd.ts) - edcm_ucns_no_geometry_or_proof_transfer
- `check_contrastive_order_multiplicity_resolution` in `research/edcm/tests/test_ucns_edcm_experiments.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_joint_runner_preserves_no_canon` in `research/edcm/tests/test_ucns_edcm_experiments.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_ucns_edcm_program_structure` in `research/edcm/tests/test_ucns_edcm_experiments.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_occurrence_coverage_candidate` in `research/edcm/tests/test_ucns_edcm_experiments_v2.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_ucns_edcm_v2_joint_report` in `research/edcm/tests/test_ucns_edcm_experiments_v2.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_ucns_edcm_v2_program` in `research/edcm/tests/test_ucns_edcm_experiments_v2.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_scope_assertion_candidate` in `research/edcm/tests/test_ucns_edcm_experiments_v3.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_ucns_edcm_v3_joint_report` in `research/edcm/tests/test_ucns_edcm_experiments_v3.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_ucns_edcm_v3_program` in `research/edcm/tests/test_ucns_edcm_experiments_v3.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_ucns_edcm_v4_joint_report` in `research/edcm/tests/test_ucns_edcm_experiments_v4.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_ucns_edcm_v4_program` in `research/edcm/tests/test_ucns_edcm_experiments_v4.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_ucns_edcm_v4_resolvers` in `research/edcm/tests/test_ucns_edcm_experiments_v4.py` (direct, research/edcm/edcm_msdmd.ts) - python3
- `check_edcm_fork_binding_exact` in `research/edcm/tests/test_ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - edcm_fork_binding_exact_topology
- `check_edcm_fork_complete_coverage` in `research/edcm/tests/test_ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - edcm_fork_lint_complete_coverage
- `check_edcm_fork_dependency` in `research/edcm/tests/test_ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - edcm_fork_lint_dependency_visible
- `check_edcm_fork_drift` in `research/edcm/tests/test_ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - edcm_fork_lint_drift_rejected
- `check_edcm_fork_missing_extra` in `research/edcm/tests/test_ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - edcm_fork_lint_missing_extra_rejected
- `check_edcm_fork_no_inference` in `research/edcm/tests/test_ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - edcm_fork_lint_no_inference
- `check_edcm_fork_roundtrip` in `research/edcm/tests/test_ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - edcm_fork_binding_roundtrip
- `check_edcm_fork_status_firewall` in `research/edcm/tests/test_ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - edcm_fork_lint_no_status_transfer
- `check_candidate_uses_only_established_ucns_surfaces` in `research/epac/subatomic/test_element_affixiation_candidate.py` (direct) - candidate_uses_only_established_ucns_surfaces
- `check_element_identity_positions_exact` in `research/epac/subatomic/test_element_affixiation_candidate.py` (direct) - element_identity_positions_exact
- `check_mobius_parameter_sequence_exact` in `research/epac/subatomic/test_element_affixiation_candidate.py` (direct) - mobius_parameter_sequence_exact
- `check_no_physics_or_canon_claim` in `research/epac/subatomic/test_element_affixiation_candidate.py` (direct) - no_physics_or_canon_claim
- `check_receipt_deterministic_and_replayable` in `research/epac/subatomic/test_element_affixiation_candidate.py` (direct) - receipt_deterministic_and_replayable
- `check_extended_atomic_preserves_z_le_18` in `research/epac/subatomic/test_extended_atomic.py` (direct) - extended_atomic_preserves_z_le_18
- `check_extended_atomic_stays_candidate` in `research/epac/subatomic/test_extended_atomic.py` (direct) - extended_atomic_stays_candidate
- `check_extended_atomic_uses_declared_configurations` in `research/epac/subatomic/test_extended_atomic.py` (direct) - extended_atomic_uses_declared_configurations
- `check_all_results_remain_cross_domain_hypothesis` in `research/epac/subatomic/test_nuclear_harmonic_candidates.py` (direct) - all_results_remain_cross_domain_hypothesis
- `check_every_harmonic_candidate_declares_six_evidence_fields` in `research/epac/subatomic/test_nuclear_harmonic_candidates.py` (direct) - every_harmonic_candidate_declares_six_evidence_fields
- `check_harmonic_parameter_is_time_agnostic` in `research/epac/subatomic/test_nuclear_harmonic_candidates.py` (direct) - harmonic_parameter_is_time_agnostic
- `check_no_public_gonol_position_operation_invented` in `research/epac/subatomic/test_nuclear_harmonic_candidates.py` (direct) - no_public_gonol_position_operation_invented
- `check_recurrence_test_is_deterministic` in `research/epac/subatomic/test_nuclear_harmonic_candidates.py` (direct) - recurrence_test_is_deterministic
- `check_subatomic_gonol_combines_three_sources` in `research/epac/subatomic/test_subatomic_gonol.py` (direct) - subatomic_gonol_combines_three_sources
- `check_subatomic_gonol_invents_no_geometry` in `research/epac/subatomic/test_subatomic_gonol.py` (direct) - subatomic_gonol_invents_no_geometry
- `check_subatomic_gonol_keeps_layers_distinct` in `research/epac/subatomic/test_subatomic_gonol.py` (direct) - subatomic_gonol_keeps_layers_distinct
- `check_subatomic_gonol_replays_byte_identical` in `research/epac/subatomic/test_subatomic_gonol.py` (direct) - subatomic_gonol_replays_byte_identical
- `check_subatomic_gonol_stays_cross_domain_hypothesis` in `research/epac/subatomic/test_subatomic_gonol.py` (direct) - subatomic_gonol_stays_cross_domain_hypothesis
- `check_letters_are_not_physics_domain` in `research/epac/subatomic/test_symbol_coupling.py` (direct) - letters_are_not_physics_domain
- `check_symbol_coupling_replays_byte_identical` in `research/epac/subatomic/test_symbol_coupling.py` (direct) - symbol_coupling_replays_byte_identical
- `check_symbol_coupling_stays_cross_domain_hypothesis` in `research/epac/subatomic/test_symbol_coupling.py` (direct) - symbol_coupling_stays_cross_domain_hypothesis
- `check_symbol_coupling_two_participants` in `research/epac/subatomic/test_symbol_coupling.py` (direct) - symbol_coupling_two_participants
- `check_symbol_gonol_preserves_exact_abbreviation` in `research/epac/subatomic/test_symbol_coupling.py` (direct) - symbol_gonol_preserves_exact_abbreviation
- `check_affixiation_harmonics_authority_firewall` in `research/metapat/tests/test_affixiation_harmonics.py` (direct) - metapat_affixiation_harmonics_authority_firewall
- `check_affixiation_harmonics_candidate_status` in `research/metapat/tests/test_affixiation_harmonics.py` (direct) - metapat_affixiation_harmonics_candidate_status
- `check_affixiation_harmonics_catalog_bound` in `research/metapat/tests/test_affixiation_harmonics.py` (direct) - metapat_affixiation_harmonics_catalog_bound
- `check_affixiation_harmonics_source_current` in `research/metapat/tests/test_affixiation_harmonics.py` (direct) - metapat_affixiation_harmonics_source_current
- `check_affixiation_identity_preserved` in `research/metapat/tests/test_affixiation_harmonics.py` (direct) - metapat_affixiation_identity_preserved
- `check_harmonics_time_agnostic` in `research/metapat/tests/test_affixiation_harmonics.py` (direct) - metapat_harmonics_time_agnostic
- `generated_tests_test_affixiation_harmonics_py_checks` in `research/metapat/tests/test_affixiation_harmonics.py` (research/metapat/metapat_msdmd.ts) - count: 6
- `check_application_binding_exact` in `research/metapat/tests/test_application.py` (direct) - metapat_application_binding_exact
- `check_application_catalog_validation` in `research/metapat/tests/test_application.py` (direct) - metapat_application_catalog_validation
- `check_application_roundtrip_strict` in `research/metapat/tests/test_application.py` (direct) - metapat_application_roundtrip_strict
- `check_application_source_exact` in `research/metapat/tests/test_application.py` (direct) - metapat_application_source_exact
- `check_application_status_firewall` in `research/metapat/tests/test_application.py` (direct) - metapat_application_status_firewall
- `check_application_tamper_rejected` in `research/metapat/tests/test_application.py` (direct) - metapat_application_tamper_rejected
- `generated_tests_test_application_py_checks` in `research/metapat/tests/test_application.py` (research/metapat/metapat_msdmd.ts) - count: 6
- `check_canon_file_drift_visible` in `research/metapat/tests/test_canon_integrity.py` (direct) - metapat_canon_file_drift_visible
- `check_canon_manifest_complete` in `research/metapat/tests/test_canon_integrity.py` (direct) - metapat_canon_manifest_complete
- `check_repository_canon_files_match` in `research/metapat/tests/test_canon_integrity.py` (direct) - metapat_canon_files_match_repository
- `generated_tests_test_canon_integrity_py_checks` in `research/metapat/tests/test_canon_integrity.py` (research/metapat/metapat_msdmd.ts) - count: 3
- `check_catalog_claim_status_bounded` in `research/metapat/tests/test_catalog.py` (direct) - metapat_catalog_claim_status_bounded
- `check_catalog_complete_ordered` in `research/metapat/tests/test_catalog.py` (direct) - metapat_catalog_complete_ordered
- `check_catalog_fixture_current` in `research/metapat/tests/test_catalog.py` (direct) - metapat_catalog_fixture_current
- `check_catalog_fixture_generated` in `research/metapat/tests/test_catalog.py` (direct) - metapat_catalog_fixture_generated
- `check_catalog_identity_unique` in `research/metapat/tests/test_catalog.py` (direct) - metapat_catalog_module_identity_unique
- `check_catalog_no_constitutive_inference` in `research/metapat/tests/test_catalog.py` (direct) - metapat_catalog_no_constitutive_inference
- `check_catalog_relations_declared` in `research/metapat/tests/test_catalog.py` (direct) - metapat_catalog_relations_declared
- `check_catalog_rotation_visible` in `research/metapat/tests/test_catalog.py` (direct) - metapat_catalog_rotation_visible
- `check_catalog_roundtrip_strict` in `research/metapat/tests/test_catalog.py` (direct) - metapat_catalog_roundtrip_strict
- `check_catalog_sources_exact` in `research/metapat/tests/test_catalog.py` (direct) - metapat_catalog_sources_exact
- `check_root_envelope_fixture_current` in `research/metapat/tests/test_catalog.py` (direct) - metapat_root_envelope_fixture_current
- `check_root_envelope_fixture_generated` in `research/metapat/tests/test_catalog.py` (direct) - metapat_root_envelope_fixture_generated
- `generated_tests_test_catalog_py_checks` in `research/metapat/tests/test_catalog.py` (research/metapat/metapat_msdmd.ts) - count: 12
- `check_contract_audit_negative_gaps` in `research/metapat/tests/test_contract_audit.py` (direct) - metapat_contract_audit_detects_gaps
- `check_repository_contract_graph_closes` in `research/metapat/tests/test_contract_audit.py` (direct) - metapat_contract_graph_closes
- `generated_tests_test_contract_audit_py_checks` in `research/metapat/tests/test_contract_audit.py` (research/metapat/metapat_msdmd.ts) - count: 2
- `check_boundary_change_changes_outcome` in `research/metapat/tests/test_contracts.py` (direct) - boundary_change_changes_outcome
- `check_consciousness_optional` in `research/metapat/tests/test_contracts.py` (direct) - consciousness_optional_observer_mode
- `check_observer_role_registration` in `research/metapat/tests/test_contracts.py` (direct) - observer_role_requires_registration
- `check_registration_not_time` in `research/metapat/tests/test_contracts.py` (direct) - registration_not_time
- `check_root_spine_exact` in `research/metapat/tests/test_contracts.py` (direct) - metapat_root_spine_exact
- `check_tensor_precedes_time` in `research/metapat/tests/test_contracts.py` (direct) - tensor_before_time
- `check_time_registration_separated` in `research/metapat/tests/test_contracts.py` (direct) - metapat_time_not_registration
- `generated_tests_test_contracts_py_checks` in `research/metapat/tests/test_contracts.py` (research/metapat/metapat_msdmd.ts) - count: 7
- `check_pipe_alloy_search` in `research/metapat/tests/test_electromagnetic_pipe.py` (direct) - metapat_pipe_alloy_search_bounded
- `check_pipe_attractors_not_bearings` in `research/metapat/tests/test_electromagnetic_pipe.py` (direct) - metapat_pipe_attractors_not_bearings
- `check_pipe_catalog_binding` in `research/metapat/tests/test_electromagnetic_pipe.py` (direct) - metapat_pipe_application_catalog_bound
- `check_pipe_control_topology` in `research/metapat/tests/test_electromagnetic_pipe.py` (direct) - metapat_pipe_control_topology_exact
- `check_pipe_fixture_current` in `research/metapat/tests/test_electromagnetic_pipe.py` (direct) - metapat_pipe_fixture_current
- `check_pipe_fixture_rendered` in `research/metapat/tests/test_electromagnetic_pipe.py` (direct) - metapat_pipe_fixture_generated
- `check_pipe_performance_firewall` in `research/metapat/tests/test_electromagnetic_pipe.py` (direct) - metapat_pipe_performance_firewall
- `check_pipe_roundtrip` in `research/metapat/tests/test_electromagnetic_pipe.py` (direct) - metapat_pipe_roundtrip_strict
- `check_pipe_source_current` in `research/metapat/tests/test_electromagnetic_pipe.py` (direct) - metapat_pipe_source_current
- `check_pipe_winding_layers` in `research/metapat/tests/test_electromagnetic_pipe.py` (direct) - metapat_pipe_winding_layers_exact
- `generated_tests_test_electromagnetic_pipe_py_checks` in `research/metapat/tests/test_electromagnetic_pipe.py` (research/metapat/metapat_msdmd.ts) - count: 10
- `check_canon_digest_deterministic` in `research/metapat/tests/test_envelope.py` (direct) - metapat_canon_digest_deterministic
- `check_envelope_canonical_json` in `research/metapat/tests/test_envelope.py` (direct) - metapat_envelope_canonical_json
- `check_envelope_exact_provenance` in `research/metapat/tests/test_envelope.py` (direct) - metapat_envelope_exact_provenance
- `check_envelope_rotation_visible` in `research/metapat/tests/test_envelope.py` (direct) - metapat_envelope_rotation_visible
- `check_envelope_roundtrip` in `research/metapat/tests/test_envelope.py` (direct) - metapat_envelope_roundtrip
- `check_envelope_scalar_types_strict` in `research/metapat/tests/test_envelope.py` (direct) - metapat_envelope_type_strict
- `check_envelope_sequence_types_strict` in `research/metapat/tests/test_envelope.py` (direct) - metapat_envelope_type_strict
- `check_envelope_tamper_rejected` in `research/metapat/tests/test_envelope.py` (direct) - metapat_envelope_tamper_rejected
- `check_labels_not_measurements` in `research/metapat/tests/test_envelope.py` (direct) - metapat_labels_not_measurements
- `check_unknown_envelope_field_rejected` in `research/metapat/tests/test_envelope.py` (direct) - metapat_envelope_unknown_field_rejected
- `generated_tests_test_envelope_py_checks` in `research/metapat/tests/test_envelope.py` (research/metapat/metapat_msdmd.ts) - count: 10
- `check_msdmd_generated_current` in `research/metapat/tests/test_msdmd_generation.py` (direct) - metapat_msdmd_generated
- `check_msdmd_scope_bounded` in `research/metapat/tests/test_msdmd_generation.py` (direct) - metapat_msdmd_scope_bounded
- `generated_tests_test_msdmd_generation_py_checks` in `research/metapat/tests/test_msdmd_generation.py` (research/metapat/metapat_msdmd.ts) - count: 2
- `check_base_import_without_ucns` in `research/metapat/tests/test_packaging.py` (direct) - metapat_base_import_without_ucns
- `check_no_public_local_ucns` in `research/metapat/tests/test_packaging.py` (direct) - metapat_no_public_local_ucns
- `check_package_version_matches_metadata` in `research/metapat/tests/test_packaging.py` (direct) - metapat_package_version_matches_metadata
- `check_pipe_fixture_packaged` in `research/metapat/tests/test_packaging.py` (direct) - metapat_pipe_fixture_packaged
- `check_root_fixture_packaged` in `research/metapat/tests/test_packaging.py` (direct) - metapat_root_fixture_packaged
- `check_typed_marker_packaged` in `research/metapat/tests/test_packaging.py` (direct) - metapat_package_typed_marker
- `generated_tests_test_packaging_py_checks` in `research/metapat/tests/test_packaging.py` (research/metapat/metapat_msdmd.ts) - count: 6
- `check_quantum_application_catalog_bound` in `research/metapat/tests/test_quantum_magnetism.py` (direct) - metapat_quantum_application_catalog_bound
- `check_quantum_application_physics_firewall` in `research/metapat/tests/test_quantum_magnetism.py` (direct) - metapat_quantum_application_physics_firewall
- `check_quantum_application_scales_distinct` in `research/metapat/tests/test_quantum_magnetism.py` (direct) - metapat_quantum_application_scales_distinct
- `check_quantum_application_source_current` in `research/metapat/tests/test_quantum_magnetism.py` (direct) - metapat_quantum_application_source_current
- `check_quantum_application_status_preserved` in `research/metapat/tests/test_quantum_magnetism.py` (direct) - metapat_quantum_application_status_preserved
- `check_quantum_fixture_current` in `research/metapat/tests/test_quantum_magnetism.py` (direct) - metapat_quantum_fixture_current
- `check_quantum_fixture_generated` in `research/metapat/tests/test_quantum_magnetism.py` (direct) - metapat_quantum_fixture_generated
- `generated_tests_test_quantum_magnetism_py_checks` in `research/metapat/tests/test_quantum_magnetism.py` (research/metapat/metapat_msdmd.ts) - count: 7
- `check_relation_no_status_transfer` in `research/metapat/tests/test_relations.py` (direct) - metapat_relation_no_status_transfer
- `check_relation_roundtrip_strict` in `research/metapat/tests/test_relations.py` (direct) - metapat_relation_roundtrip_strict
- `check_relation_tamper_rejected` in `research/metapat/tests/test_relations.py` (direct) - metapat_relation_tamper_rejected
- `check_relation_vocabulary_bounded` in `research/metapat/tests/test_relations.py` (direct) - metapat_relation_vocabulary_bounded
- `generated_tests_test_relations_py_checks` in `research/metapat/tests/test_relations.py` (research/metapat/metapat_msdmd.ts) - count: 4
- `check_metapat_base_survives_ucns_profile` in `research/metapat/tests/test_ucns_bridge.py` (direct) - metapat_ucns_ordered_occurrence_provenance
- `check_metapat_ucns_archived_operations` in `research/metapat/tests/test_ucns_bridge.py` (direct) - metapat_ucns_archived_operations_rejected
- `check_metapat_ucns_exact_identity` in `research/metapat/tests/test_ucns_bridge.py` (direct) - metapat_ucns_exact_identity_or_inactive
- `check_metapat_ucns_order_and_no_transfer` in `research/metapat/tests/test_ucns_bridge.py` (direct) - metapat_ucns_ordered_occurrence_provenance, metapat_ucns_no_authority_transfer
- `generated_tests_test_ucns_bridge_py_checks` in `research/metapat/tests/test_ucns_bridge.py` (research/metapat/metapat_msdmd.ts) - count: 4
- `check_phi_canon_order_binding` in `research/metapat/tests/test_ucns_phi.py` (direct) - metapat_phi_authorization_binds_canon_and_order
- `check_phi_default_external_provenance` in `research/metapat/tests/test_ucns_phi.py` (direct) - metapat_phi_default_external_provenance
- `check_phi_explicit_authorization` in `research/metapat/tests/test_ucns_phi.py` (direct) - metapat_phi_fork_requires_explicit_authorization
- `check_phi_negative_relations` in `research/metapat/tests/test_ucns_phi.py` (direct) - metapat_phi_negative_relations_rejected
- `check_phi_no_status_transfer` in `research/metapat/tests/test_ucns_phi.py` (direct) - metapat_phi_no_status_transfer
- `check_phi_relation_exact` in `research/metapat/tests/test_ucns_phi.py` (direct) - metapat_phi_constitutive_relation_only
- `check_phi_roundtrip` in `research/metapat/tests/test_ucns_phi.py` (direct) - metapat_phi_record_roundtrip
- `generated_tests_test_ucns_phi_py_checks` in `research/metapat/tests/test_ucns_phi.py` (research/metapat/metapat_msdmd.ts) - count: 7
- `check_circle_identity_fallback` in `research/ptcna/ptcna/circle/tests/test_circle.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_circle_non_differentiating` in `research/ptcna/ptcna/circle/tests/test_circle.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_circle_rejects_empty` in `research/ptcna/ptcna/circle/tests/test_circle.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_circle_roundtrip` in `research/ptcna/ptcna/circle/tests/test_circle.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_fiq_has_no_gradient_ownership` in `research/ptcna/ptcna/core/prime_core/tests/test_fiq_opaque.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_fiq_payload_identity` in `research/ptcna/ptcna/core/prime_core/tests/test_fiq_opaque.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_prime_core_default_profile` in `research/ptcna/ptcna/core/prime_core/tests/test_ptca_core_stratified.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_prime_core_no_gradient_ownership` in `research/ptcna/ptcna/core/prime_core/tests/test_ptca_core_stratified.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_prime_core_payload_width` in `research/ptcna/ptcna/core/prime_core/tests/test_ptca_core_stratified.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_prime_core_positive_counts` in `research/ptcna/ptcna/core/prime_core/tests/test_ptca_core_stratified.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_prime_core_shared_layer_types` in `research/ptcna/ptcna/core/prime_core/tests/test_ptca_core_stratified.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_prime_core_ucns_scope` in `research/ptcna/ptcna/core/prime_core/tests/test_ptca_core_stratified.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_pcna_checkpoint_roundtrip` in `research/ptcna/ptcna/neural/tests/test_pcna.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3, numpy
- `check_pcna_reward` in `research/ptcna/ptcna/neural/tests/test_pcna.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3, numpy
- `check_pcna_six_step_pipeline` in `research/ptcna/ptcna/neural/tests/test_pcna.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3, numpy
- `check_neural_scalar_backprop` in `research/ptcna/ptcna/neural/tests/test_scalar.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_neural_scalar_tape_ops` in `research/ptcna/ptcna/neural/tests/test_scalar.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_zeta_external_metrics` in `research/ptcna/ptcna/neural/tests/test_zeta.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3, numpy
- `check_zeta_no_shadow_edcm` in `research/ptcna/ptcna/neural/tests/test_zeta.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_zeta_suspends_without_provider` in `research/ptcna/ptcna/neural/tests/test_zeta.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3, numpy
- `check_seed_non_differentiating` in `research/ptcna/ptcna/seed/tests/test_seed_contracts.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_seed_rejects_empty` in `research/ptcna/ptcna/seed/tests/test_seed_contracts.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_seed_shared_circle_type` in `research/ptcna/ptcna/seed/tests/test_seed_contracts.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_contract_audit_broken_edges` in `research/ptcna/ptcna/tests/test_contract_audit.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_contract_audit_complete_graph` in `research/ptcna/ptcna/tests/test_contract_audit.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_ptcna_critical_plan_digest` in `research/ptcna/ptcna/tests/test_critical_evaluation.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_ptcna_critical_result_digest` in `research/ptcna/ptcna/tests/test_critical_evaluation.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_ptcna_comparator_failure_and_parity` in `research/ptcna/ptcna/tests/test_evaluation.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_ptcna_failure_propagation` in `research/ptcna/ptcna/tests/test_evaluation.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_ptcna_frozen_verdicts` in `research/ptcna/ptcna/tests/test_evaluation.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_ptcna_plan_digest` in `research/ptcna/ptcna/tests/test_evaluation.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_ptcna_explicit_failover` in `research/ptcna/ptcna/tests/test_runtime.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3, numpy
- `check_ptcna_fallback_determinism` in `research/ptcna/ptcna/tests/test_runtime.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3, numpy
- `check_ptcna_fallback_reward` in `research/ptcna/ptcna/tests/test_runtime.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3, numpy
- `check_ptcna_reward_route` in `research/ptcna/ptcna/tests/test_runtime.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3, numpy
- `check_ptcna_root_runtime_exports` in `research/ptcna/ptcna/tests/test_runtime.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3
- `check_ptcna_target_four_layers` in `research/ptcna/ptcna/tests/test_runtime.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3, numpy
- `check_ptcna_ucns_independent_state` in `research/ptcna/ptcna/tests/test_ucns_integration.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3, numpy, ucns
- `check_ptcna_ucns_producer_validation` in `research/ptcna/ptcna/tests/test_ucns_integration.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3, numpy, ucns
- `check_ptcna_ucns_shape_suspension` in `research/ptcna/ptcna/tests/test_ucns_integration.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3, numpy, ucns
- `check_ptcna_ucns_tamper_rejection` in `research/ptcna/ptcna/tests/test_ucns_integration.py` (direct, research/ptcna/ptcna_msdmd.ts) - python3, numpy, ucns
- `check_lifted_period` in `research/ucns/tests/test_carrier.py` (direct) - python3
- `check_non_null_validation_and_radius` in `research/ucns/tests/test_carrier.py` (direct) - python3
- `check_one_lap_is_deck_translation` in `research/ucns/tests/test_carrier.py` (direct) - python3
- `check_payload_zero_does_not_collapse_carrier` in `research/ucns/tests/test_carrier.py` (direct) - python3
- `check_structural_null_identity` in `research/ucns/tests/test_carrier.py` (direct) - python3
- `check_visible_projection_and_branch_law` in `research/ucns/tests/test_carrier.py` (direct) - python3
- `native_mobius_return_check` in `research/ucns/tests/test_direct_mobius.py` (direct) - python3
- `check_geometry_public_surface_exclusion` in `research/ucns/tests/test_geometry_public_surface.py` (direct) - python3
- `check_mobius_seed_center_six_phase_channels` in `research/ucns/tests/test_mobius_global_compatibility.py` (direct) - python3
- `check_mobius_seed_contact_braid_exclusivity` in `research/ucns/tests/test_mobius_global_compatibility.py` (direct) - python3
- `check_mobius_seed_direct_rotation_agreement` in `research/ucns/tests/test_mobius_global_compatibility.py` (direct) - python3
- `check_mobius_seed_global_certificate_firewall` in `research/ucns/tests/test_mobius_global_compatibility.py` (direct) - python3
- `check_mobius_seed_incident_dyad_state_incompatibility` in `research/ucns/tests/test_mobius_global_compatibility.py` (direct) - python3
- `check_mobius_seed_pr174_zero_inheritance` in `research/ucns/tests/test_mobius_global_compatibility.py` (direct) - python3
- `check_mobius_seed_rigid_rotation_transport` in `research/ucns/tests/test_mobius_global_compatibility.py` (direct) - python3
- `check_mobius_seed_single_state_capacity_three` in `research/ucns/tests/test_mobius_global_compatibility.py` (direct) - python3
- `check_mobius_seed_surface_phase_quotient` in `research/ucns/tests/test_mobius_global_compatibility.py` (direct) - python3
- `check_mobius_seed_braid_order` in `research/ucns/tests/test_mobius_seed.py` (direct) - python3
- `check_mobius_seed_dyad_phase_schedule` in `research/ucns/tests/test_mobius_seed.py` (direct) - python3
- `check_mobius_seed_null_void` in `research/ucns/tests/test_mobius_seed.py` (direct) - python3
- `check_mobius_seed_projection_pair_completion` in `research/ucns/tests/test_mobius_seed.py` (direct) - python3
- `check_mobius_seed_proof_firewall` in `research/ucns/tests/test_mobius_seed.py` (direct) - python3
- `check_mobius_seed_surface_quotient` in `research/ucns/tests/test_mobius_seed.py` (direct) - python3
- `check_mobius_vesica_alternate_branch_obstruction` in `research/ucns/tests/test_mobius_vesica_exact.py` (direct) - python3
- `check_mobius_vesica_centerline_contacts` in `research/ucns/tests/test_mobius_vesica_exact.py` (direct) - python3
- `check_mobius_vesica_contact_semantics` in `research/ucns/tests/test_mobius_vesica_exact.py` (direct) - python3
- `check_mobius_vesica_four_boundary_contacts` in `research/ucns/tests/test_mobius_vesica_exact.py` (direct) - python3
- `check_mobius_vesica_half_turn_obstruction` in `research/ucns/tests/test_mobius_vesica_exact.py` (direct) - python3
- `check_mobius_vesica_null_clearance` in `research/ucns/tests/test_mobius_vesica_exact.py` (direct) - python3
- `check_mobius_vesica_quotient_return` in `research/ucns/tests/test_mobius_vesica_exact.py` (direct) - python3
- `check_mobius_vesica_receipt_firewall` in `research/ucns/tests/test_mobius_vesica_exact.py` (direct) - python3
- `check_mobius_vesica_seed_phase_firewall` in `research/ucns/tests/test_mobius_vesica_exact.py` (direct) - python3
- `check_mobius_vesica_source_claims` in `research/ucns/tests/test_mobius_vesica_exact.py` (direct) - python3
- `check_mobius_vesica_structural_placements` in `research/ucns/tests/test_mobius_vesica_exact.py` (direct) - python3
- `check_mobius_vesica_width_continuation` in `research/ucns/tests/test_mobius_vesica_exact.py` (direct) - python3
- `check_prime_grobner_complete_accounting` in `research/ucns/tests/test_prime_determinantal_grobner.py` (direct) - python3, sympy
- `check_prime_grobner_nonclaims` in `research/ucns/tests/test_prime_determinantal_grobner.py` (direct) - python3
- `check_prime_grobner_protocol_frozen` in `research/ucns/tests/test_prime_determinantal_grobner.py` (direct) - python3
- `check_prime_grobner_reduced_bases` in `research/ucns/tests/test_prime_determinantal_grobner.py` (direct) - python3, sympy
- `check_prime_grobner_replay` in `research/ucns/tests/test_prime_determinantal_grobner.py` (direct) - python3, sympy
- `check_prime_borromean_magnus` in `research/ucns/tests/test_prime_exact_milnor_alexander.py` (direct) - python3
- `check_prime_exact_receipt_nonselecting` in `research/ucns/tests/test_prime_exact_milnor_alexander.py` (direct) - python3, mpmath
- `check_prime_fox_complete_fingerprint` in `research/ucns/tests/test_prime_exact_milnor_alexander.py` (direct) - python3, mpmath
- `check_prime_generic_diagram_fixed` in `research/ucns/tests/test_prime_exact_milnor_alexander.py` (direct) - python3, mpmath
- `check_prime_generic_pairwise_linking` in `research/ucns/tests/test_prime_exact_milnor_alexander.py` (direct) - python3, mpmath
- `check_prime_p7_exact_milnor_zero` in `research/ucns/tests/test_prime_exact_milnor_alexander.py` (direct) - python3, mpmath
- `check_prime_phase_preregistration_hash` in `research/ucns/tests/test_prime_exact_milnor_alexander.py` (direct) - python3
- `check_prime_phase_whole_link_selector` in `research/ucns/tests/test_prime_exact_milnor_alexander.py` (direct) - python3, mpmath
- `check_prime_generic_interval_atan2` in `research/ucns/tests/test_prime_generic_interval_certificate.py` (direct) - python3, system-libmpfr, mpmath
- `check_prime_generic_interval_crossing_signs` in `research/ucns/tests/test_prime_generic_interval_certificate.py` (direct) - python3, system-libmpfr, mpmath
- `check_prime_generic_interval_receipt` in `research/ucns/tests/test_prime_generic_interval_certificate.py` (direct) - python3, system-libmpfr, mpmath
- `check_prime_generic_interval_smooth_signs` in `research/ucns/tests/test_prime_generic_interval_certificate.py` (direct) - python3, system-libmpfr, mpmath
- `check_prime_independent_receipt_nonselecting` in `research/ucns/tests/test_prime_independent_phase_milnor.py` (direct) - python3
- `check_prime_milnor_borromean_benchmark` in `research/ucns/tests/test_prime_independent_phase_milnor.py` (direct) - python3, numpy
- `check_prime_milnor_exactness_boundary` in `research/ucns/tests/test_prime_independent_phase_milnor.py` (direct) - python3
- `check_prime_milnor_p7_zero_resolution` in `research/ucns/tests/test_prime_independent_phase_milnor.py` (direct) - python3, numpy
- `check_prime_mpfr_backend_independence` in `research/ucns/tests/test_prime_independent_phase_milnor.py` (direct) - python3, libmpfr
- `check_prime_mpfr_ribbon_margin` in `research/ucns/tests/test_prime_independent_phase_milnor.py` (direct) - python3, libmpfr
- `check_prime_phase_sensitivity_selection` in `research/ucns/tests/test_prime_independent_phase_milnor.py` (direct) - python3
- `check_prime_phase_torus_seven_not_forced` in `research/ucns/tests/test_prime_independent_phase_milnor.py` (direct) - python3
- `check_prime_boundary_cable_winding` in `research/ucns/tests/test_prime_interval_boundaries.py` (direct) - python3
- `check_prime_boundary_linking_fourfold` in `research/ucns/tests/test_prime_interval_boundaries.py` (direct) - python3
- `check_prime_boundary_single_two_turn_component` in `research/ucns/tests/test_prime_interval_boundaries.py` (direct) - python3
- `check_prime_higher_order_boundary` in `research/ucns/tests/test_prime_interval_boundaries.py` (direct) - python3
- `check_prime_interval_boundaries_p7_first` in `research/ucns/tests/test_prime_interval_boundaries.py` (direct) - python3, mpmath
- `check_prime_interval_boundary_compact_receipt` in `research/ucns/tests/test_prime_interval_boundaries.py` (direct) - python3, mpmath
- `check_prime_interval_replay_outward_endpoints` in `research/ucns/tests/test_prime_interval_boundaries.py` (direct) - python3, mpmath
- `check_prime_legacy_readable_adapter` in `research/ucns/tests/test_prime_interval_boundaries.py` (direct) - python3, mpmath, sympy
- `check_prime_mixed_core_boundary_matrix` in `research/ucns/tests/test_prime_interval_boundaries.py` (direct) - python3
- `check_prime_boundary_component_knot_types` in `research/ucns/tests/test_prime_interval_boundary_links.py` (direct) - python3
- `check_prime_boundary_helper_facade` in `research/ucns/tests/test_prime_interval_boundary_links.py` (direct) - python3, sympy
- `check_prime_boundary_linking_matrix` in `research/ucns/tests/test_prime_interval_boundary_links.py` (direct) - python3, sympy
- `check_prime_boundary_single_closed_component` in `research/ucns/tests/test_prime_interval_boundary_links.py` (direct) - python3
- `check_prime_generic_helper_facade` in `research/ucns/tests/test_prime_interval_boundary_links.py` (direct) - python3, mpmath
- `check_prime_interval_boundary_receipt` in `research/ucns/tests/test_prime_interval_boundary_links.py` (direct) - python3, mpmath, sympy
- `check_prime_interval_boundary_research_order` in `research/ucns/tests/test_prime_interval_boundary_links.py` (direct) - python3, mpmath, sympy
- `check_prime_interval_common_facade` in `research/ucns/tests/test_prime_interval_boundary_links.py` (direct) - python3, mpmath
- `check_prime_interval_finite_width_disjointness` in `research/ucns/tests/test_prime_interval_boundary_links.py` (direct) - python3, mpmath
- `check_prime_interval_outward_replay` in `research/ucns/tests/test_prime_interval_boundary_links.py` (direct) - python3, mpmath
- `check_prime_interval_replay_helper_facade` in `research/ucns/tests/test_prime_interval_boundary_links.py` (direct) - python3, mpmath
- `check_prime_length_three_milnor_profile` in `research/ucns/tests/test_prime_interval_boundary_links.py` (direct) - python3, mpmath
- `check_prime_milnor_helper_facade` in `research/ucns/tests/test_prime_interval_boundary_links.py` (direct) - python3, mpmath
- `check_prime_mixed_integer_invariants` in `research/ucns/tests/test_prime_interval_boundary_links.py` (direct) - python3, sympy
- `check_prime_length4_bounded_receipt` in `research/ucns/tests/test_prime_length4_milnor.py` (direct) - python3, mpmath
- `check_prime_length4_commutator_gate` in `research/ucns/tests/test_prime_length4_milnor.py` (direct) - python3
- `check_prime_length4_cyclic_receipt` in `research/ucns/tests/test_prime_length4_milnor.py` (direct) - python3, mpmath
- `check_prime_length4_lower_gates` in `research/ucns/tests/test_prime_length4_milnor.py` (direct) - python3, mpmath
- `check_nilpotent_phase_binding` in `research/ucns/tests/test_prime_nilpotent_discriminator.py` (direct) - python3
- `check_nilpotent_primary_replay` in `research/ucns/tests/test_prime_nilpotent_discriminator.py` (direct) - python3
- `check_nilpotent_protocol_identity` in `research/ucns/tests/test_prime_nilpotent_discriminator.py` (direct) - python3
- `check_nilpotent_rank_exclusion` in `research/ucns/tests/test_prime_nilpotent_discriminator.py` (direct) - python3
- `check_prime_phase_lift_data_coverage` in `research/ucns/tests/test_prime_phase_lift.py` (direct) - python3
- `check_prime_phase_lift_disjoint_centerlines` in `research/ucns/tests/test_prime_phase_lift.py` (direct) - python3
- `check_prime_phase_lift_hypernodes` in `research/ucns/tests/test_prime_phase_lift.py` (direct) - python3
- `check_prime_phase_lift_links` in `research/ucns/tests/test_prime_phase_lift.py` (direct) - python3
- `check_prime_phase_lift_model_derived_links` in `research/ucns/tests/test_prime_phase_lift.py` (direct) - python3
- `check_prime_phase_lift_model_event_semantics` in `research/ucns/tests/test_prime_phase_lift.py` (direct) - python3
- `check_prime_phase_lift_origin` in `research/ucns/tests/test_prime_phase_lift.py` (direct) - python3
- `check_prime_phase_lift_p5_second` in `research/ucns/tests/test_prime_phase_lift.py` (direct) - python3
- `check_prime_phase_lift_p7_first` in `research/ucns/tests/test_prime_phase_lift.py` (direct) - python3
- `check_prime_phase_lift_receipt` in `research/ucns/tests/test_prime_phase_lift.py` (direct) - python3
- `check_prime_phase_lift_seam` in `research/ucns/tests/test_prime_phase_lift.py` (direct) - python3
- `check_prime_arithmetic_geometry_firewall` in `research/ucns/tests/test_prime_primitives.py` (direct) - python3
- `check_prime_p5_direct_signature` in `research/ucns/tests/test_prime_primitives.py` (direct) - python3
- `check_prime_p7_direct_signature` in `research/ucns/tests/test_prime_primitives.py` (direct) - python3
- `check_prime_p7_uniform_relation` in `research/ucns/tests/test_prime_primitives.py` (direct) - python3
- `check_prime_restrictions_after_construction` in `research/ucns/tests/test_prime_primitives.py` (direct) - python3
- `check_prime_two_cycle_boundary` in `research/ucns/tests/test_prime_primitives.py` (direct) - python3
- `check_prime_replay_data_receipt` in `research/ucns/tests/test_prime_replay_phase_milnor_receipt.py` (direct) - python3
- `check_prime_replay_receipt_interval` in `research/ucns/tests/test_prime_replay_phase_milnor_receipt.py` (direct) - python3
- `check_prime_replay_receipt_milnor` in `research/ucns/tests/test_prime_replay_phase_milnor_receipt.py` (direct) - python3
- `check_prime_replay_receipt_nonselecting` in `research/ucns/tests/test_prime_replay_phase_milnor_receipt.py` (direct) - python3
- `check_prime_replay_receipt_phase` in `research/ucns/tests/test_prime_replay_phase_milnor_receipt.py` (direct) - python3
- `check_prime_smooth_ribbons_centerline_margin` in `research/ucns/tests/test_prime_smooth_ribbons.py` (direct) - python3
- `check_prime_smooth_ribbons_event_lanes` in `research/ucns/tests/test_prime_smooth_ribbons.py` (direct) - python3
- `check_prime_smooth_ribbons_finite_width_disjointness` in `research/ucns/tests/test_prime_smooth_ribbons.py` (direct) - python3
- `check_prime_smooth_ribbons_linking_matrix` in `research/ucns/tests/test_prime_smooth_ribbons.py` (direct) - python3
- `check_prime_smooth_ribbons_mobius_return` in `research/ucns/tests/test_prime_smooth_ribbons.py` (direct) - python3
- `check_prime_smooth_ribbons_p7_first` in `research/ucns/tests/test_prime_smooth_ribbons.py` (direct) - python3
- `check_prime_smooth_ribbons_receipt` in `research/ucns/tests/test_prime_smooth_ribbons.py` (direct) - python3
- `check_prime_smooth_ribbons_tangent_regularization` in `research/ucns/tests/test_prime_smooth_ribbons.py` (direct) - python3
- `check_prime_symbolic_character_replay` in `research/ucns/tests/test_prime_symbolic_alexander.py` (direct) - python3, sympy
- `check_prime_symbolic_elementary_boundary` in `research/ucns/tests/test_prime_symbolic_alexander.py` (direct) - python3, sympy
- `check_prime_symbolic_fox_exact` in `research/ucns/tests/test_prime_symbolic_alexander.py` (direct) - python3, sympy
- `check_prime_symbolic_receipt_nonselecting` in `research/ucns/tests/test_prime_symbolic_alexander.py` (direct) - python3, sympy
- `public_gonol_geometry_check` in `research/ucns/tests/test_public_gonol.py` (direct) - python3
- `check_boundary_runner_audit_gate` in `research/ucns/tests/test_skill_lib_boundary_runner.py` (direct) - python3
- `check_boundary_runner_capability_timeout_consumption` in `research/ucns/tests/test_skill_lib_boundary_runner.py` (direct) - python3
- `check_boundary_runner_nonactivation` in `research/ucns/tests/test_skill_lib_boundary_runner.py` (direct) - python3
- `check_boundary_runner_receipt_binding` in `research/ucns/tests/test_skill_lib_boundary_runner.py` (direct) - python3
- `check_boundary_runner_registered_capability_detection` in `research/ucns/tests/test_skill_lib_boundary_runner.py` (direct) - python3
- `check_boundary_runner_status_continuation` in `research/ucns/tests/test_skill_lib_boundary_runner.py` (direct) - python3
- `check_contract_audit_detects_gaps` in `research/ucns/tests/test_skill_lib_contracts.py` (direct) - python3
- `check_contract_audit_no_exec` in `research/ucns/tests/test_skill_lib_contracts.py` (direct) - python3
- `check_repository_contract_graph` in `research/ucns/tests/test_skill_lib_contracts.py` (direct) - python3

### CONTRACTS

- `multiwoz21_admission_precedes_execution` in `research/edcm/edcm/corpora/multiwoz21.py` (direct, research/edcm/edcm_msdmd.ts) - a caller supplies a local MultiWOZ 2.1 archive
- `multiwoz21_completion_requires_reconciliation` in `research/edcm/edcm/corpora/multiwoz21.py` (direct, research/edcm/edcm_msdmd.ts) - source streaming reaches valid EOF
- `multiwoz21_every_turn_is_observed_exactly_once` in `research/edcm/edcm/corpora/multiwoz21.py` (direct, research/edcm/edcm_msdmd.ts) - an admitted archive contains the complete top-level dialogue object
- `multiwoz21_failure_is_receipted` in `research/edcm/edcm/corpora/multiwoz21.py` (direct, research/edcm/edcm_msdmd.ts) - archive, schema, adapter, checkpoint, or reconciliation processing fails
- `multiwoz21_ucns_v0141_receipt_requires_matching_source_native_run` in `research/edcm/edcm/corpora/multiwoz21.py` (direct, research/edcm/edcm_msdmd.ts) - the source-native EDCM pass reconciles the admitted archive
- `multiwoz21_written_outputs_exclude_raw_text` in `research/edcm/edcm/corpora/multiwoz21.py` (direct, research/edcm/edcm_msdmd.ts) - a run succeeds or fails
- `multiwoz_booking_outcome_calibration_precedes_test` in `research/edcm/edcm/corpora/multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - admitted development, validation, and test outcome events
- `multiwoz_booking_outcome_destinations_do_not_collide` in `research/edcm/edcm/corpora/multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - a caller-held source archive plus report and receipt destinations including their atomic temporary paths and existing filesystem aliases
- `multiwoz_booking_outcome_hypothesis_failure_is_evidence` in `research/edcm/edcm/corpora/multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - a frozen sensitivity, specificity, discrimination, or calibration hypothesis is not met
- `multiwoz_booking_outcome_labelled_response_is_withheld` in `research/edcm/edcm/corpora/multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - a source dialogue-act turn contains exactly one admitted booking outcome label
- `multiwoz_booking_outcome_repeat_requires_complete_execution` in `research/edcm/edcm/corpora/multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - one holdout execution renders its aggregate report deterministically
- `multiwoz_booking_outcome_report_is_aggregate_only` in `research/edcm/edcm/corpora/multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - the holdout run completes or fails
- `multiwoz_booking_outcome_runtime_matches_recorded_checkout` in `research/edcm/edcm/corpora/multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - a caller supplies a clean EDCM repository and expected producer commit
- `multiwoz_booking_outcome_status_does_not_transfer` in `research/edcm/edcm/corpora/multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - the admitted archive, exact UCNS represented-evidence seal, and candidate EDCM report reconcile
- `multiwoz_booking_outcome_uncertainty_is_cluster_aware` in `research/edcm/edcm/corpora/multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - repeated source outcome events may share one dialogue
- `edcm_goal_vector_na_not_zero` in `research/edcm/edcm/goal_vector_experiment.py` (direct, research/edcm/edcm_msdmd.ts) - a goal component has not received an explicit fixture claim
- `edcm_goal_vector_no_status_transfer` in `research/edcm/edcm/goal_vector_experiment.py` (direct, research/edcm/edcm_msdmd.ts) - the controlled candidate emits a contradiction ledger and goal-motion variance
- `edcm_goal_vector_same_occurrences_preserve_order` in `research/edcm/edcm/goal_vector_experiment.py` (direct, research/edcm/edcm_msdmd.ts) - the fixed resolved and active-contradiction cases contain the same source occurrences in different orders
- `closed_gonol_atomic_at_any_scale` in `research/edcm/edcm/gonol.py` (direct, research/edcm/edcm_msdmd.ts) - a closed gonol participates in another construction
- `construction_survives_absent_ucns_geometry` in `research/edcm/edcm/gonol.py` (direct, research/edcm/edcm_msdmd.ts) - UCNS Public Gonol geometry authority is not explicitly supplied
- `geometry_mismatch_fails_closed` in `research/edcm/edcm/gonol.py` (direct, research/edcm/edcm_msdmd.ts) - supplied UCNS Public Gonol geometry has a digest different from the pinned identity
- `single_constructor_uses_scale_option_sets` in `research/edcm/edcm/gonol.py` (direct, research/edcm/edcm_msdmd.ts) - a caller closes source evidence or closed gonol participants
- `suffix_exception_carried_by_suffix_gonol` in `research/edcm/edcm/gonol.py` (direct, research/edcm/edcm_msdmd.ts) - suffix coupling has a final-y exception such as ing preserving y after a consonant
- `unified_candidate_does_not_select_canon` in `research/edcm/edcm/gonol.py` (direct, research/edcm/edcm_msdmd.ts) - a receipt is minted
- `lexical_manifest_preserves_authority_firewall` in `research/edcm/edcm/language/manifest.py` (direct, research/edcm/edcm_msdmd.ts) - the English lexical-floor manifest is inspected
- `comparison_requires_two_prior_freezes` in `research/edcm/edcm/language/relational_bridge.py` (direct, research/edcm/edcm_msdmd.ts) - a branch comparison is requested
- `english_metadata_is_external_to_ucns_carrier` in `research/edcm/edcm/language/relational_bridge.py` (direct, research/edcm/edcm_msdmd.ts) - either branch is frozen
- `lexical_branches_are_independently_constructed` in `research/edcm/edcm/language/relational_bridge.py` (direct, research/edcm/edcm_msdmd.ts) - direct-atomic and molecular branch builders run
- `lexical_pre_replay_status_is_unresolved` in `research/edcm/edcm/language/relational_bridge.py` (direct, research/edcm/edcm_msdmd.ts) - one branch freeze or within-run branch comparison completes
- `lexical_relation_multiplicity_is_preserved` in `research/edcm/edcm/language/relational_bridge.py` (direct, research/edcm/edcm_msdmd.ts) - direct semantic evidence or molecular alternatives contain repeated relation occurrences
- `lexical_ucns_producer_is_exactly_verified` in `research/edcm/edcm/language/relational_bridge.py` (direct, research/edcm/edcm_msdmd.ts) - EDCM opens the UCNS relational construction API
- `recovered_dissonance_gate_executes_only_frozen_candidates` in `research/edcm/edcm/recovered_dissonance_experiment.py` (direct, research/edcm/edcm_msdmd.ts) - the controlled recovered-dissonance gate runs
- `recovered_dissonance_gate_preserves_prior_falsification` in `research/edcm/edcm/recovered_dissonance_experiment.py` (direct, research/edcm/edcm_msdmd.ts) - a controlled report is emitted
- `recovered_dissonance_external_evaluator_does_not_promote` in `research/edcm/edcm/recovered_dissonance_external_evaluator.py` (direct, research/edcm/edcm_msdmd.ts) - the evaluator emits SURVIVED, FALSIFIED, or UNRESOLVED candidate evidence
- `recovered_dissonance_external_evaluator_fails_closed` in `research/edcm/edcm/recovered_dissonance_external_evaluator.py` (direct, research/edcm/edcm_msdmd.ts) - structure, identity, custody, disclosure, limits, protocol, or metric admission disagrees with the frozen packet
- `recovered_dissonance_external_evaluator_is_aggregate_only` in `research/edcm/edcm/recovered_dissonance_external_evaluator.py` (direct, research/edcm/edcm_msdmd.ts) - the frozen batch is evaluated
- `recovered_dissonance_external_evaluator_is_frozen` in `research/edcm/edcm/recovered_dissonance_external_evaluator.py` (direct, research/edcm/edcm_msdmd.ts) - the external evaluator receives a UCNS PR 196 request
- `edcm_ucns_exact_profile_only` in `research/edcm/edcm/ucns_adapter.py` (direct, research/edcm/edcm_msdmd.ts) - an importable UCNS package is considered for activation
- `edcm_ucns_full_turn_observation` in `research/edcm/edcm/ucns_adapter.py` (direct, research/edcm/edcm_msdmd.ts) - ordered ucns_turns enter the active adapter
- `edcm_ucns_no_geometry_or_proof_transfer` in `research/edcm/edcm/ucns_adapter.py` (direct, research/edcm/edcm_msdmd.ts) - exact profile observations are attached
- `edcm_fork_binding_exact_topology` in `research/edcm/edcm/ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - a METAPAT authorization is bound to an actual UCNS fork
- `edcm_fork_binding_roundtrip` in `research/edcm/edcm/ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - a topology binding is serialized and reconstructed
- `edcm_fork_lint_complete_coverage` in `research/edcm/edcm/ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - a recursive UCNS object is linted
- `edcm_fork_lint_dependency_visible` in `research/edcm/edcm/ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - UCNS or METAPAT is directly absent or transitively broken
- `edcm_fork_lint_drift_rejected` in `research/edcm/edcm/ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - payload order, cell indices, object hashes, canon, policy, or producer authorization changes
- `edcm_fork_lint_missing_extra_rejected` in `research/edcm/edcm/ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - a declaration is missing, duplicated, or targets a non-fork path
- `edcm_fork_lint_no_inference` in `research/edcm/edcm/ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - geometry has fewer than two payload children or no declaration
- `edcm_fork_lint_no_status_transfer` in `research/edcm/edcm/ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - a valid binding and lint report
- `tarot_acquisition_fetches_only_authorized_public_domain_bytes` in `research/edcm/tools/acquire_tarot_corpus.py` (direct, research/edcm/edcm_msdmd.ts) - a source requests automatic byte acquisition
- `tarot_acquisition_preserves_source_identity` in `research/edcm/tools/acquire_tarot_corpus.py` (direct, research/edcm/edcm_msdmd.ts) - a Tarot source is admitted to an acquisition run
- `tarot_acquisition_resume_fails_closed` in `research/edcm/tools/acquire_tarot_corpus.py` (direct, research/edcm/edcm_msdmd.ts) - a completed or interrupted Tarot acquisition is resumed
- `tarot_manifest_preserves_preontology_boundary` in `research/edcm/tools/acquire_tarot_corpus.py` (direct, research/edcm/edcm_msdmd.ts) - a Tarot corpus manifest is loaded
- `tarot_metadata_only_sources_are_not_downloaded` in `research/edcm/tools/acquire_tarot_corpus.py` (direct, research/edcm/edcm_msdmd.ts) - a source is metadata_only or manual_review
- `incomplete_or_altered_lexical_resume_fails_closed` in `research/edcm/tools/build_oewn2025_embeddings.py` (direct, research/edcm/edcm_msdmd.ts) - resume state is partial, noncanonical, stale, producer-mismatched, status-promoted, missing, or digest-altered
- `lexical_comparison_occurs_after_freeze` in `research/edcm/tools/build_oewn2025_embeddings.py` (direct, research/edcm/edcm_msdmd.ts) - a complete lexical-floor build runs
- `oewn_source_is_exact_pinned_and_resumable` in `research/edcm/tools/build_oewn2025_embeddings.py` (direct, research/edcm/edcm_msdmd.ts) - the lexical-floor builder consumes or acquires OEWN
- `tarot_discovery_consumes_only_complete_sealed_acquisition` in `research/edcm/tools/discover_tarot_relations.py` (direct, research/edcm/edcm_msdmd.ts) - Tarot relation discovery is requested
- `tarot_discovery_is_byte_deterministic` in `research/edcm/tools/discover_tarot_relations.py` (direct, research/edcm/edcm_msdmd.ts) - the same validated acquisition and frozen algorithm identity are processed twice
- `tarot_discovery_preserves_exact_source_order_and_values` in `research/edcm/tools/discover_tarot_relations.py` (direct, research/edcm/edcm_msdmd.ts) - a validated evidence index is discovered
- `tarot_discovery_preserves_typed_absence_and_nonclaims` in `research/edcm/tools/discover_tarot_relations.py` (direct, research/edcm/edcm_msdmd.ts) - a source field is absent or the report completes
- `tarot_discovery_relations_are_mechanical_and_bounded` in `research/edcm/tools/discover_tarot_relations.py` (direct, research/edcm/edcm_msdmd.ts) - source-envelope relations are emitted
- `tarot_text_gate_applies_frozen_adequacy_rule` in `research/edcm/tools/evaluate_tarot_pdf_text_layer.py` (direct, research/edcm/edcm_msdmd.ts) - exact per-page text bytes are extracted
- `tarot_text_gate_retains_nonclaims_and_failure` in `research/edcm/tools/evaluate_tarot_pdf_text_layer.py` (direct, research/edcm/edcm_msdmd.ts) - the gate completes or fails
- `tarot_text_gate_uses_exact_frozen_inputs_and_backend` in `research/edcm/tools/evaluate_tarot_pdf_text_layer.py` (direct, research/edcm/edcm_msdmd.ts) - the embedded-text gate runs
- `tarot_ocr_v4_applies_frozen_accuracy_rule` in `research/edcm/tools/run_tarot_ocr_v4.py` (direct, research/edcm/edcm_msdmd.ts) - the sealed independent reference and complete OCR outputs
- `tarot_ocr_v4_preserves_raw_page_evidence` in `research/edcm/tools/run_tarot_ocr_v4.py` (direct, research/edcm/edcm_msdmd.ts) - an admitted PDF page
- `tarot_ocr_v4_resume_fails_closed` in `research/edcm/tools/run_tarot_ocr_v4.py` (direct, research/edcm/edcm_msdmd.ts) - an interrupted or completed output directory
- `tarot_ocr_v4_serialization_is_deterministic` in `research/edcm/tools/run_tarot_ocr_v4.py` (direct, research/edcm/edcm_msdmd.ts) - identical producer outputs and inputs
- `tarot_ocr_v4_verifies_every_frozen_identity` in `research/edcm/tools/run_tarot_ocr_v4.py` (direct, research/edcm/edcm_msdmd.ts) - a protocol execution request
- `tarot_ocr_v5_changes_only_frozen_thresholding` in `research/edcm/tools/run_tarot_ocr_v5.py` (direct, research/edcm/edcm_msdmd.ts) - a v5 page OCR request
- `tarot_ocr_v5_retains_v4_evidence_contracts` in `research/edcm/tools/run_tarot_ocr_v5.py` (direct, research/edcm/edcm_msdmd.ts) - a complete or resumed v5 run
- `tarot_ocr_v6_changes_only_frozen_model` in `research/edcm/tools/run_tarot_ocr_v6.py` (direct, research/edcm/edcm_msdmd.ts) - a v6 page OCR request
- `tarot_ocr_v6_retains_v4_evidence_contracts` in `research/edcm/tools/run_tarot_ocr_v6.py` (direct, research/edcm/edcm_msdmd.ts) - a complete or resumed v6 run
- `tarot_ocr_v6_verifies_historic_model` in `research/edcm/tools/run_tarot_ocr_v6.py` (direct, research/edcm/edcm_msdmd.ts) - a v6 execution request
- `tarot_ocr_v7_repairs_only_renderer_activation` in `research/edcm/tools/run_tarot_ocr_v7.py` (direct, research/edcm/edcm_msdmd.ts) - a v7 page OCR request
- `tarot_ocr_v7_retains_v6_instrument` in `research/edcm/tools/run_tarot_ocr_v7.py` (direct, research/edcm/edcm_msdmd.ts) - a complete or resumed v7 run
- `charged_oriented_couplings_are_the_structure` in `research/epac/epac_public_gonol.py` (direct) - declared oriented couplings with per-slot charges
- `epac_public_gonol_binds_ucns_carrier_identity` in `research/epac/epac_public_gonol.py` (direct) - identity_glyph is an admitted Public Gonol glyph
- `epac_public_gonol_is_not_edcm_gonol` in `research/epac/epac_public_gonol.py` (direct) - an EPAC gonol is constructed
- `epac_public_gonol_replays_byte_identical` in `research/epac/epac_public_gonol.py` (direct) - a PublicGonolReceipt
- `candidate_uses_only_established_ucns_surfaces` in `research/epac/subatomic/element_affixiation_candidate.py` (direct) - the candidate module is imported and executed
- `element_identity_positions_exact` in `research/epac/subatomic/element_affixiation_candidate.py` (direct) - an element symbol with default isotope (Z, A)
- `mobius_parameter_sequence_exact` in `research/epac/subatomic/element_affixiation_candidate.py` (direct) - the Möbius turn index t in {0, 1, 2} is traversed
- `no_physics_or_canon_claim` in `research/epac/subatomic/element_affixiation_candidate.py` (direct) - any constructed candidate
- `receipt_deterministic_and_replayable` in `research/epac/subatomic/element_affixiation_candidate.py` (direct) - the same element and the same pinned source identities
- `extended_atomic_preserves_z_le_18` in `research/epac/subatomic/extended_atomic.py` (direct) - atomic_record(Z) for 1 <= Z <= 18
- `extended_atomic_stays_candidate` in `research/epac/subatomic/extended_atomic.py` (direct) - any extended record
- `extended_atomic_uses_declared_configurations` in `research/epac/subatomic/extended_atomic.py` (direct) - atomic_record(Z) for 19 <= Z <= 26
- `all_results_remain_cross_domain_hypothesis` in `research/epac/subatomic/nuclear_harmonic_candidates.py` (direct) - any candidate or recurrence result
- `every_harmonic_candidate_declares_six_evidence_fields` in `research/epac/subatomic/nuclear_harmonic_candidates.py` (direct) - any harmonic candidate record
- `harmonic_parameter_is_time_agnostic` in `research/epac/subatomic/nuclear_harmonic_candidates.py` (direct) - any harmonic candidate ordered parameter
- `no_public_gonol_position_operation_invented` in `research/epac/subatomic/nuclear_harmonic_candidates.py` (direct) - the harmonic candidate module is imported
- `recurrence_test_is_deterministic` in `research/epac/subatomic/nuclear_harmonic_candidates.py` (direct) - the same candidate record and the same declared equivalence condition
- `subatomic_gonol_combines_three_sources` in `research/epac/subatomic/subatomic_gonol.py` (direct) - a subatomic gonol is constructed for a supported symbol
- `subatomic_gonol_invents_no_geometry` in `research/epac/subatomic/subatomic_gonol.py` (direct) - construction
- `subatomic_gonol_keeps_layers_distinct` in `research/epac/subatomic/subatomic_gonol.py` (direct) - constructed gonol participants
- `subatomic_gonol_replays_byte_identical` in `research/epac/subatomic/subatomic_gonol.py` (direct) - a subatomic gonol receipt
- `subatomic_gonol_stays_cross_domain_hypothesis` in `research/epac/subatomic/subatomic_gonol.py` (direct) - any receipt
- `letters_are_not_physics_domain` in `research/epac/subatomic/symbol_coupling.py` (direct) - symbol_coupling source and any constructed symbol gonol
- `symbol_coupling_replays_byte_identical` in `research/epac/subatomic/symbol_coupling.py` (direct) - a symbol-coupled receipt
- `symbol_coupling_stays_cross_domain_hypothesis` in `research/epac/subatomic/symbol_coupling.py` (direct) - any symbol-coupled receipt
- `symbol_coupling_two_participants` in `research/epac/subatomic/symbol_coupling.py` (direct) - a nomenclature-coupled gonol
- `symbol_gonol_preserves_exact_abbreviation` in `research/epac/subatomic/symbol_coupling.py` (direct) - a symbol gonol for element symbol S
- `generated_src_metapat___init___py_contracts` in `research/metapat/src/metapat/__init__.py` (research/metapat/metapat_msdmd.ts) - count: 6
- `metapat_base_import_without_ucns` in `research/metapat/src/metapat/__init__.py` (direct) - the base package is imported without invoking the optional adapter
- `metapat_no_public_local_ucns` in `research/metapat/src/metapat/__init__.py` (direct) - the public package surface is inspected
- `metapat_package_typed_marker` in `research/metapat/src/metapat/__init__.py` (direct) - the installed package resources are inspected
- `metapat_package_version_matches_metadata` in `research/metapat/src/metapat/__init__.py` (direct) - the installed package and distribution metadata are inspected
- `metapat_pipe_fixture_packaged` in `research/metapat/src/metapat/__init__.py` (direct) - the installed package resources are inspected
- `metapat_root_fixture_packaged` in `research/metapat/src/metapat/__init__.py` (direct) - the installed package resources are inspected
- `generated_src_metapat_affixiation_harmonics_py_contracts` in `research/metapat/src/metapat/affixiation_harmonics.py` (research/metapat/metapat_msdmd.ts) - count: 6
- `metapat_affixiation_harmonics_authority_firewall` in `research/metapat/src/metapat/affixiation_harmonics.py` (direct) - the application evidence and transfer boundaries are inspected
- `metapat_affixiation_harmonics_candidate_status` in `research/metapat/src/metapat/affixiation_harmonics.py` (direct) - application status and unresolved fields are inspected
- `metapat_affixiation_harmonics_catalog_bound` in `research/metapat/src/metapat/affixiation_harmonics.py` (direct) - the affixiation-harmonics application module is constructed
- `metapat_affixiation_harmonics_source_current` in `research/metapat/src/metapat/affixiation_harmonics.py` (direct) - the application constructor and source document are checked together
- `metapat_affixiation_identity_preserved` in `research/metapat/src/metapat/affixiation_harmonics.py` (direct) - affixiation semantics are inspected
- `metapat_harmonics_time_agnostic` in `research/metapat/src/metapat/affixiation_harmonics.py` (direct) - recurrence, oscillation, and harmonic semantics are inspected
- `generated_src_metapat_application_py_contracts` in `research/metapat/src/metapat/application.py` (research/metapat/metapat_msdmd.ts) - count: 6
- `metapat_application_binding_exact` in `research/metapat/src/metapat/application.py` (direct) - an application binds a catalog module
- `metapat_application_catalog_validation` in `research/metapat/src/metapat/application.py` (direct) - an application is checked against a canonical catalog
- `metapat_application_roundtrip_strict` in `research/metapat/src/metapat/application.py` (direct) - a valid application module is serialized and reconstructed
- `metapat_application_source_exact` in `research/metapat/src/metapat/application.py` (direct) - application source references are resolved against repository Markdown
- `metapat_application_status_firewall` in `research/metapat/src/metapat/application.py` (direct) - an application module or binding is constructed
- `metapat_application_tamper_rejected` in `research/metapat/src/metapat/application.py` (direct) - application content, binding content, catalog identity, or evidence boundary changes without digest rotation
- `generated_src_metapat_canon_py_contracts` in `research/metapat/src/metapat/canon.py` (research/metapat/metapat_msdmd.ts) - count: 6
- `metapat_canon_digest_deterministic` in `research/metapat/src/metapat/canon.py` (direct) - the same exact canon constants and file manifest are serialized repeatedly
- `metapat_canon_file_drift_visible` in `research/metapat/src/metapat/canon.py` (direct) - one canon-bearing file changes by one or more bytes
- `metapat_canon_files_match_repository` in `research/metapat/src/metapat/canon.py` (direct) - the repository canon files are read without modification
- `metapat_canon_manifest_complete` in `research/metapat/src/metapat/canon.py` (direct) - the public canon file manifest is inspected
- `metapat_root_spine_exact` in `research/metapat/src/metapat/canon.py` (direct) - canon definitions are imported
- `metapat_time_not_registration` in `research/metapat/src/metapat/canon.py` (direct) - canon definitions are inspected
- `generated_src_metapat_catalog_py_contracts` in `research/metapat/src/metapat/catalog.py` (research/metapat/metapat_msdmd.ts) - count: 8
- `metapat_catalog_claim_status_bounded` in `research/metapat/src/metapat/catalog.py` (direct) - doctrine classes and claim statuses are inspected
- `metapat_catalog_complete_ordered` in `research/metapat/src/metapat/catalog.py` (direct) - the canonical semantic catalog is constructed
- `metapat_catalog_module_identity_unique` in `research/metapat/src/metapat/catalog.py` (direct) - catalog modules are inspected
- `metapat_catalog_no_constitutive_inference` in `research/metapat/src/metapat/catalog.py` (direct) - a catalog is constructed without a UCNS fork authorization
- `metapat_catalog_relations_declared` in `research/metapat/src/metapat/catalog.py` (direct) - catalog relation records are inspected
- `metapat_catalog_rotation_visible` in `research/metapat/src/metapat/catalog.py` (direct) - a module statement, claim status, relation, constraint, canon identity, or unresolved field changes
- `metapat_catalog_roundtrip_strict` in `research/metapat/src/metapat/catalog.py` (direct) - the complete catalog is serialized and reconstructed
- `metapat_catalog_sources_exact` in `research/metapat/src/metapat/catalog.py` (direct) - catalog references are resolved against repository canon files
- `generated_src_metapat_electromagnetic_pipe_py_contracts` in `research/metapat/src/metapat/electromagnetic_pipe.py` (research/metapat/metapat_msdmd.ts) - count: 8
- `metapat_pipe_alloy_search_bounded` in `research/metapat/src/metapat/electromagnetic_pipe.py` (direct) - the alloy candidates are inspected
- `metapat_pipe_application_catalog_bound` in `research/metapat/src/metapat/electromagnetic_pipe.py` (direct) - the pipe application is constructed
- `metapat_pipe_attractors_not_bearings` in `research/metapat/src/metapat/electromagnetic_pipe.py` (direct) - the mobile-element fields are inspected
- `metapat_pipe_control_topology_exact` in `research/metapat/src/metapat/electromagnetic_pipe.py` (direct) - the electromagnetic-pipe design record is constructed
- `metapat_pipe_performance_firewall` in `research/metapat/src/metapat/electromagnetic_pipe.py` (direct) - the design record and application are inspected
- `metapat_pipe_roundtrip_strict` in `research/metapat/src/metapat/electromagnetic_pipe.py` (direct) - a valid design record is serialized and reconstructed
- `metapat_pipe_source_current` in `research/metapat/src/metapat/electromagnetic_pipe.py` (direct) - the constructor and handoff source are checked together
- `metapat_pipe_winding_layers_exact` in `research/metapat/src/metapat/electromagnetic_pipe.py` (direct) - the winding layers are inspected
- `generated_src_metapat_envelope_py_contracts` in `research/metapat/src/metapat/envelope.py` (research/metapat/metapat_msdmd.ts) - count: 8
- `metapat_envelope_canonical_json` in `research/metapat/src/metapat/envelope.py` (direct) - the same envelope is serialized repeatedly
- `metapat_envelope_exact_provenance` in `research/metapat/src/metapat/envelope.py` (direct) - the canonical root-spine envelope is constructed
- `metapat_envelope_rotation_visible` in `research/metapat/src/metapat/envelope.py` (direct) - otherwise identical envelopes with different canon digest or semantic constraints
- `metapat_envelope_roundtrip` in `research/metapat/src/metapat/envelope.py` (direct) - a valid immutable module envelope including unresolved hmmm fields
- `metapat_envelope_tamper_rejected` in `research/metapat/src/metapat/envelope.py` (direct) - serialized envelope content changes without a matching provenance digest
- `metapat_envelope_type_strict` in `research/metapat/src/metapat/envelope.py` (direct) - serialized envelope fields have incorrect scalar or sequence types
- `metapat_envelope_unknown_field_rejected` in `research/metapat/src/metapat/envelope.py` (direct) - serialized envelope data contains an undeclared field
- `metapat_labels_not_measurements` in `research/metapat/src/metapat/envelope.py` (direct) - a semantic envelope is constructed
- `generated_src_metapat_quantum_magnetism_py_contracts` in `research/metapat/src/metapat/quantum_magnetism.py` (research/metapat/metapat_msdmd.ts) - count: 5
- `metapat_quantum_application_catalog_bound` in `research/metapat/src/metapat/quantum_magnetism.py` (direct) - the quantum-magnetism application module is constructed
- `metapat_quantum_application_physics_firewall` in `research/metapat/src/metapat/quantum_magnetism.py` (direct) - the application evidence fields are inspected
- `metapat_quantum_application_scales_distinct` in `research/metapat/src/metapat/quantum_magnetism.py` (direct) - selected physical scales and transfer limits are inspected
- `metapat_quantum_application_source_current` in `research/metapat/src/metapat/quantum_magnetism.py` (direct) - the application constructor and source document are checked together
- `metapat_quantum_application_status_preserved` in `research/metapat/src/metapat/quantum_magnetism.py` (direct) - the application module and its catalog bindings are inspected
- `generated_src_metapat_relations_py_contracts` in `research/metapat/src/metapat/relations.py` (research/metapat/metapat_msdmd.ts) - count: 4
- `metapat_relation_no_status_transfer` in `research/metapat/src/metapat/relations.py` (direct) - a semantic ancestry record is constructed
- `metapat_relation_roundtrip_strict` in `research/metapat/src/metapat/relations.py` (direct) - a valid semantic relation is serialized and reconstructed
- `metapat_relation_tamper_rejected` in `research/metapat/src/metapat/relations.py` (direct) - relation endpoints, source provenance, evidence status, or unresolved constraints change without digest rotation
- `metapat_relation_vocabulary_bounded` in `research/metapat/src/metapat/relations.py` (direct) - semantic relation and claim-status vocabularies are inspected
- `generated_src_metapat_ucns_py_contracts` in `research/metapat/src/metapat/ucns.py` (research/metapat/metapat_msdmd.ts) - count: 4
- `metapat_ucns_archived_operations_rejected` in `research/metapat/src/metapat/ucns.py` (direct) - archived face-bit or universal composition behavior is requested
- `metapat_ucns_exact_identity_or_inactive` in `research/metapat/src/metapat/ucns.py` (direct) - an installed package named ucns is inspected
- `metapat_ucns_no_authority_transfer` in `research/metapat/src/metapat/ucns.py` (direct) - an adaptation succeeds
- `metapat_ucns_ordered_occurrence_provenance` in `research/metapat/src/metapat/ucns.py` (direct) - a METAPAT envelope is adapted through the exact profile
- `generated_src_metapat_ucns_phi_py_contracts` in `research/metapat/src/metapat/ucns_phi.py` (research/metapat/metapat_msdmd.ts) - count: 7
- `metapat_phi_authorization_binds_canon_and_order` in `research/metapat/src/metapat/ucns_phi.py` (direct) - authorization is checked against an envelope and child order
- `metapat_phi_constitutive_relation_only` in `research/metapat/src/metapat/ucns_phi.py` (direct) - an authorization is constructed or decoded
- `metapat_phi_default_external_provenance` in `research/metapat/src/metapat/ucns_phi.py` (direct) - the default Phi policy is inspected
- `metapat_phi_fork_requires_explicit_authorization` in `research/metapat/src/metapat/ucns_phi.py` (direct) - a fork is authorized from a canonical envelope
- `metapat_phi_negative_relations_rejected` in `research/metapat/src/metapat/ucns_phi.py` (direct) - time, adjacency, provenance, alternatives, fiq connectivity, or external action is presented as containment
- `metapat_phi_no_status_transfer` in `research/metapat/src/metapat/ucns_phi.py` (direct) - any Phi policy or authorization
- `metapat_phi_record_roundtrip` in `research/metapat/src/metapat/ucns_phi.py` (direct) - authorization is serialized and reconstructed
- `boundary_change_changes_outcome` in `research/metapat/src/metapat/validation.py` (direct) - source and target are fixed while boundary state changes
- `consciousness_optional_observer_mode` in `research/metapat/src/metapat/validation.py` (direct) - non-conscious registration with or without a separate conscious story
- `generated_src_metapat_validation_py_contracts` in `research/metapat/src/metapat/validation.py` (research/metapat/metapat_msdmd.ts) - count: 5
- `observer_role_requires_registration` in `research/metapat/src/metapat/validation.py` (direct) - a simplex and a tensor alteration sequence
- `registration_not_time` in `research/metapat/src/metapat/validation.py` (direct) - a tensor alteration sequence and an optional registration
- `tensor_before_time` in `research/metapat/src/metapat/validation.py` (direct) - one tensor state and then an ordered pair of tensor states
- `generated_tools_check_contract_graph_py_contracts` in `research/metapat/tools/check_contract_graph.py` (research/metapat/metapat_msdmd.ts) - count: 2
- `metapat_contract_audit_detects_gaps` in `research/metapat/tools/check_contract_graph.py` (direct) - orphan contracts, phantom proves targets, unresolvable calls, or undeclared executable tests are planted
- `metapat_contract_graph_closes` in `research/metapat/tools/check_contract_graph.py` (direct) - current METAPAT source promises and test evidence are audited without imports
- `generated_tools_generate_application_fixtures_py_contracts` in `research/metapat/tools/generate_application_fixtures.py` (research/metapat/metapat_msdmd.ts) - count: 4
- `metapat_pipe_fixture_current` in `research/metapat/tools/generate_application_fixtures.py` (direct) - the generator runs in check mode against the packaged electromagnetic-pipe fixture
- `metapat_pipe_fixture_generated` in `research/metapat/tools/generate_application_fixtures.py` (direct) - the electromagnetic-pipe design constructor runs
- `metapat_quantum_fixture_current` in `research/metapat/tools/generate_application_fixtures.py` (direct) - the generator runs in check mode against the packaged quantum-magnetism fixture
- `metapat_quantum_fixture_generated` in `research/metapat/tools/generate_application_fixtures.py` (direct) - the quantum-magnetism application constructor runs
- `generated_tools_generate_catalog_py_contracts` in `research/metapat/tools/generate_catalog.py` (research/metapat/metapat_msdmd.ts) - count: 4
- `metapat_catalog_fixture_current` in `research/metapat/tools/generate_catalog.py` (direct) - the generator runs in check mode against the packaged fixture
- `metapat_catalog_fixture_generated` in `research/metapat/tools/generate_catalog.py` (direct) - the canonical semantic catalog constructor runs
- `metapat_root_envelope_fixture_current` in `research/metapat/tools/generate_catalog.py` (direct) - the generator runs in check mode against the packaged root-spine envelope fixture
- `metapat_root_envelope_fixture_generated` in `research/metapat/tools/generate_catalog.py` (direct) - the canonical root-spine envelope constructor runs
- `generated_tools_generate_msdmd_py_contracts` in `research/metapat/tools/generate_msdmd.py` (research/metapat/metapat_msdmd.ts) - count: 2
- `metapat_msdmd_generated` in `research/metapat/tools/generate_msdmd.py` (direct) - the pinned collector runs over the bounded METAPAT product surfaces
- `metapat_msdmd_scope_bounded` in `research/metapat/tools/generate_msdmd.py` (direct) - the collection is generated
- `ptcna_root_exports_runtime_boundary` in `research/ptcna/ptcna/__init__.py` (direct, research/ptcna/ptcna_msdmd.ts) - a caller imports ptcna
- `circle_composition_preserves_order_and_identity` in `research/ptcna/ptcna/circle/compose.py` (direct, research/ptcna/ptcna_msdmd.ts) - one or more ordered payload objects and a routing step
- `circle_composition_rejects_empty_input` in `research/ptcna/ptcna/circle/compose.py` (direct, research/ptcna/ptcna_msdmd.ts) - zero neural payloads
- `circle_tensor_is_non_differentiating` in `research/ptcna/ptcna/circle/tensor.py` (direct, research/ptcna/ptcna_msdmd.ts) - a circle hosting payloads that may themselves be neural-owned differentiable objects
- `circle_tensor_round_trips_payloads` in `research/ptcna/ptcna/circle/tensor.py` (direct, research/ptcna/ptcna_msdmd.ts) - payloads composed into a circle under a star-polygon anchor order
- `prime_core_counts_are_positive` in `research/ptcna/ptcna/core/prime_core/core.py` (direct, research/ptcna/ptcna_msdmd.ts) - any CoreSpec composition count is zero or negative
- `prime_core_default_profile_is_stable` in `research/ptcna/ptcna/core/prime_core/core.py` (direct, research/ptcna/ptcna_msdmd.ts) - build_core is called with the default CoreSpec
- `prime_core_is_non_differentiating` in `research/ptcna/ptcna/core/prime_core/core.py` (direct, research/ptcna/ptcna_msdmd.ts) - a core hosts payloads including neural-owned differentiable objects
- `prime_core_payload_width_matches_spec` in `research/ptcna/ptcna/core/prime_core/core.py` (direct, research/ptcna/ptcna_msdmd.ts) - a payload factory returns a vector whose length differs from tensor_dim
- `prime_core_ucns_receipt_scope_is_exact` in `research/ptcna/ptcna/core/prime_core/core.py` (direct, research/ptcna/ptcna_msdmd.ts) - a core is built with the exact 157x7x7x53 receipt-covered shape or a different shape
- `prime_core_uses_shared_layer_types` in `research/ptcna/ptcna/core/prime_core/core.py` (direct, research/ptcna/ptcna_msdmd.ts) - a core is built from a CoreSpec
- `fiq_never_owns_gradients` in `research/ptcna/ptcna/core/prime_core/fiq.py` (direct, research/ptcna/ptcna_msdmd.ts) - a fiq carries neural-owned differentiable objects
- `fiq_payload_is_opaque_and_lossless` in `research/ptcna/ptcna/core/prime_core/fiq.py` (direct, research/ptcna/ptcna_msdmd.ts) - arbitrary payload objects are wrapped in a fiq
- `ptcna_critical_plan_digest_locked` in `research/ptcna/ptcna/critical_evaluation.py` (direct, research/ptcna/ptcna_msdmd.ts) - the checked-in critical evaluation plan is loaded
- `ptcna_critical_result_content_addressed` in `research/ptcna/ptcna/critical_evaluation.py` (direct, research/ptcna/ptcna_msdmd.ts) - the frozen plan completes or reaches a frozen failure rule
- `ptcna_evaluation_plan_freezes_verdict_inputs` in `research/ptcna/ptcna/evaluation.py` (direct, research/ptcna/ptcna_msdmd.ts) - an EvaluationPlan is constructed
- `ptcna_evaluation_propagates_backend_failure` in `research/ptcna/ptcna/evaluation.py` (direct, research/ptcna/ptcna_msdmd.ts) - either backend errors before completing the frozen workload
- `ptcna_evaluation_verdict_uses_frozen_thresholds` in `research/ptcna/ptcna/evaluation.py` (direct, research/ptcna/ptcna_msdmd.ts) - target and fallback complete the frozen workload
- `pcna_checkpoint_round_trips_ring_state` in `research/ptcna/ptcna/neural/pcna.py` (direct, research/ptcna/ptcna_msdmd.ts) - an engine saves a checkpoint and a compatible engine loads it
- `pcna_infer_reports_complete_six_step_pipeline` in `research/ptcna/ptcna/neural/pcna.py` (direct, research/ptcna/ptcna_msdmd.ts) - non-empty input text is passed to PCNAEngine.infer
- `pcna_reward_updates_neural_and_timing_state` in `research/ptcna/ptcna/neural/pcna.py` (direct, research/ptcna/ptcna_msdmd.ts) - a bounded outcome is passed to PCNAEngine.reward
- `neural_scalar_owns_backprop` in `research/ptcna/ptcna/neural/scalar.py` (direct, research/ptcna/ptcna_msdmd.ts) - a loss graph composed from NeuralScalar addition and multiplication
- `neural_scalar_uses_no_structural_operator` in `research/ptcna/ptcna/neural/scalar.py` (direct, research/ptcna/ptcna_msdmd.ts) - a NeuralScalar computation graph
- `zeta_consumes_explicit_metrics` in `research/ptcna/ptcna/neural/zeta.py` (direct, research/ptcna/ptcna_msdmd.ts) - an injected provider returns the required bounded metric mapping
- `zeta_never_imports_shadow_edcm` in `research/ptcna/ptcna/neural/zeta.py` (direct, research/ptcna/ptcna_msdmd.ts) - evaluation runs with or without an injected provider
- `zeta_requires_external_measurement_provider` in `research/ptcna/ptcna/neural/zeta.py` (direct, research/ptcna/ptcna_msdmd.ts) - evaluate is called without an injected measurement provider
- `ptcna_failover_is_explicit_and_attributed` in `research/ptcna/ptcna/runtime.py` (direct, research/ptcna/ptcna_msdmd.ts) - the target raises during inference
- `ptcna_fallback_is_distinct_and_deterministic` in `research/ptcna/ptcna/runtime.py` (direct, research/ptcna/ptcna_msdmd.ts) - identical text and fresh HashedLinearFallback instances
- `ptcna_fallback_reward_changes_selected_score` in `research/ptcna/ptcna/runtime.py` (direct, research/ptcna/ptcna_msdmd.ts) - the fallback infers text and receives a positive bounded reward for the selected winner
- `ptcna_reward_follows_backend_receipt` in `research/ptcna/ptcna/runtime.py` (direct, research/ptcna/ptcna_msdmd.ts) - a reward is applied to an inference receipt
- `ptcna_target_reports_four_live_layers` in `research/ptcna/ptcna/runtime.py` (direct, research/ptcna/ptcna_msdmd.ts) - non-empty text is inferred through PTCNAEngine
- `seed_composition_is_non_differentiating` in `research/ptcna/ptcna/seed/compose.py` (direct, research/ptcna/ptcna_msdmd.ts) - opaque payloads including neural scalars
- `seed_composition_rejects_empty` in `research/ptcna/ptcna/seed/compose.py` (direct, research/ptcna/ptcna_msdmd.ts) - an empty circle sequence
- `seed_composition_uses_shared_circle_type` in `research/ptcna/ptcna/seed/compose.py` (direct, research/ptcna/ptcna_msdmd.ts) - a non-empty sequence of ptcna.circle.CircleTensor objects
- `seed_hosts_shared_circle_type` in `research/ptcna/ptcna/seed/tensor.py` (direct, research/ptcna/ptcna_msdmd.ts) - a sequence of ptcna.circle.CircleTensor objects
- `seed_is_non_differentiating` in `research/ptcna/ptcna/seed/tensor.py` (direct, research/ptcna/ptcna_msdmd.ts) - any valid Seed
- `seed_payload_roundtrip` in `research/ptcna/ptcna/seed/tensor.py` (direct, research/ptcna/ptcna_msdmd.ts) - hosted circles with opaque payloads
- `ptcna_ucns_receipt_is_producer_validated` in `research/ptcna/ptcna/ucns_integration.py` (direct, research/ptcna/ptcna_msdmd.ts) - PTCNA consumes a UCNS candidate-state receipt
- `ptcna_ucns_state_is_independently_verified` in `research/ptcna/ptcna/ucns_integration.py` (direct, research/ptcna/ptcna_msdmd.ts) - the producer receipt passes UCNS validation
- `ptcna_ucns_tampering_fails_closed` in `research/ptcna/ptcna/ucns_integration.py` (direct, research/ptcna/ptcna_msdmd.ts) - receipt content or expected state shape differs
- `contract_audit_closes_complete_graph` in `research/ptcna/scripts/check_contracts.py` (direct, research/ptcna/ptcna_msdmd.ts) - unique contracts and checks whose proves targets and self calls all resolve
- `contract_audit_exposes_broken_edges` in `research/ptcna/scripts/check_contracts.py` (direct, research/ptcna/ptcna_msdmd.ts) - an orphan contract, unknown proves target, unresolved self call, or undeclared executable test
- `geometry_public_surface_excludes_nongeometric_domains` in `research/ucns/src/ucns/__init__.py` (direct) - the active ucns package facade is imported
- `algebraic_zero_is_not_structural_null` in `research/ucns/src/ucns/carrier.py` (direct) - a non-null carrier retains structure while an external payload value is numerically zero
- `lifted_period_is_720_degrees` in `research/ucns/src/ucns/carrier.py` (direct) - any finite angular coordinate on a non-null carrier
- `non_null_carrier_has_positive_breadth` in `research/ucns/src/ucns/carrier.py` (direct) - a non-null lifted carrier point is constructed
- `one_visible_lap_is_deck_translation_only` in `research/ucns/src/ucns/carrier.py` (direct) - a non-null lifted carrier point translated by two pi
- `structural_null_is_unique_and_coordinate_free` in `research/ucns/src/ucns/carrier.py` (direct) - the carrier is constructed with zero faithful breadth
- `topology_does_not_invent_orientation_algebra` in `research/ucns/src/ucns/carrier.py` (direct) - a 360-degree deck translation
- `two_visible_laps_complete_return` in `research/ucns/src/ucns/carrier.py` (direct) - a non-null lifted carrier point translated twice by two pi
- `visible_projection_is_360_degrees` in `research/ucns/src/ucns/carrier.py` (direct) - a non-null lifted carrier point
- `native_mobius_motion_is_exactly_invertible` in `research/ucns/src/ucns/direct_mobius.py` (direct) - an exact rational turn displacement is applied and then negated
- `native_mobius_one_turn_reverses_frame` in `research/ucns/src/ucns/direct_mobius.py` (direct) - any framed Mobius state advances one full visible turn
- `native_mobius_two_turns_restore_complete_state` in `research/ucns/src/ucns/direct_mobius.py` (direct) - any framed Mobius state advances two full visible turns
- `mobius_vesica_alternate_height_branch_is_obstructed` in `research/ucns/src/ucns/mobius_certificates.py` (direct) - the exact quarter-turn height equation is split into its two trigonometric branches
- `mobius_vesica_certificate_is_nonselecting_and_zeta_firewalled` in `research/ucns/src/ucns/mobius_certificates.py` (direct) - a machine receipt is serialized
- `mobius_vesica_contact_semantics_are_not_flattened` in `research/ucns/src/ucns/mobius_certificates.py` (direct) - a certificate is emitted
- `mobius_vesica_sturm_proves_four_physical_boundary_contacts` in `research/ucns/src/ucns/mobius_certificates.py` (direct) - the normalized radius-one, separation-one, half-width-one-hundredth, opposite-chirality, quarter-turn dyad is constructed
- `mobius_vesica_half_turn_phase_has_exact_contact_obstruction` in `research/ucns/src/ucns/mobius_continuation.py` (direct) - the standard circular family has opposite chirality, phase pair zero and one half, and width below one half
- `mobius_vesica_rigid_placements_cover_seed_structural_pairs` in `research/ucns/src/ucns/mobius_continuation.py` (direct) - the Seed-of-Life wheel relation graph is requested
- `mobius_vesica_seed_phase_mismatch_blocks_certificate_inheritance` in `research/ucns/src/ucns/mobius_continuation.py` (direct) - the exact quarter-turn dyad is compared with the current PR-174 half-turn first dyad
- `mobius_vesica_width_continuation_recertifies_each_stage` in `research/ucns/src/ucns/mobius_continuation.py` (direct) - a sequence of rational widths strictly between zero and one half is requested at quarter-turn phase
- `mobius_seed_center_needs_six_phase_channels_for_six_spokes` in `research/ucns/src/ucns/mobius_global_compatibility.py` (direct) - all six spokes are rigid copies while the center retains one chirality
- `mobius_seed_global_compatibility_certificate_is_nonselecting` in `research/ucns/src/ucns/mobius_global_compatibility.py` (direct) - the certificate is serialized
- `mobius_seed_incident_certified_dyads_are_state_incompatible` in `research/ucns/src/ucns/mobius_global_compatibility.py` (direct) - two wheel-W7 structural pairs share a band and each is a rigid copy of the certified quarter-turn anti-chiral vesica
- `mobius_seed_physical_contact_and_strict_braid_are_event_exclusive` in `research/ucns/src/ucns/mobius_global_compatibility.py` (direct) - the same occurrences at one event are declared both physically equal and strictly height-separated
- `mobius_seed_pr174_inherits_no_exact_rigid_vesica_pairs` in `research/ucns/src/ucns/mobius_global_compatibility.py` (direct) - the pinned PR-174 phase/chirality schedule is compared with both exact rigid-copy orientations
- `mobius_seed_single_state_certified_capacity_is_three` in `research/ucns/src/ucns/mobius_global_compatibility.py` (direct) - each band has one chirality and one constant surface phase modulo one half turn
- `mobius_seed_candidate_is_nonselecting_and_proof_firewalled` in `research/ucns/src/ucns/mobius_seed.py` (direct) - a receipt or OBJ realization is emitted
- `mobius_seed_dyad_is_anti_aligned_and_outer_phase_is_incremental` in `research/ucns/src/ucns/mobius_seed.py` (direct) - the default seven-band schedule is inspected
- `mobius_seed_lift_preserves_null_as_nonvertex_void` in `research/ucns/src/ucns/mobius_seed.py` (direct) - coincident projected occurrences are lifted into three dimensions
- `mobius_seed_projection_is_exact_and_pair_complete` in `research/ucns/src/ucns/mobius_seed.py` (direct) - the default Mobius Seed of Life candidate is constructed
- `mobius_seed_structural_pairs_have_alternating_braid_order` in `research/ucns/src/ucns/mobius_seed.py` (direct) - either projected crossing of each structural vesica is inspected
- `mobius_seed_surface_obeys_360_seam_and_720_return` in `research/ucns/src/ucns/mobius_seed.py` (direct) - any default band surface point is advanced one or two carrier turns
- `mobius_vesica_has_exact_two_centerline_contacts` in `research/ucns/src/ucns/mobius_vesica.py` (direct) - the canonical equal-radius vesica embedding is constructed
- `mobius_vesica_null_origin_has_positive_clearance` in `research/ucns/src/ucns/mobius_vesica.py` (direct) - radius one, center separation one, and half width one hundredth
- `mobius_vesica_obeys_one_turn_seam_and_two_turn_return` in `research/ucns/src/ucns/mobius_vesica.py` (direct) - either band is evaluated at any admissible breadth
- `mobius_vesica_preserves_source_claims_as_testable_geometry` in `research/ucns/src/ucns/mobius_vesica.py` (direct) - the source note is used to define the dyad research target
- `prime_mpfr_replay_is_backend_independent` in `research/ucns/src/ucns/mpfr_interval.py` (direct) - the frozen P7/P5 partition is replayed
- `prime_mpfr_replay_recertifies_ribbon_margin` in `research/ucns/src/ucns/mpfr_interval.py` (direct) - every frozen pair box is replayed with directed MPFR endpoints
- `prime_boundary_helper_is_facade_witnessed` in `research/ucns/src/ucns/prime_boundary_link_invariants.py` (direct) - the owning facade invokes this readable helper
- `prime_grobner_basis_is_complete_reduced_and_saturated` in `research/ucns/src/ucns/prime_determinantal_grobner.py` (direct) - the complete rational-Laurent determinantal generator family is accepted
- `prime_grobner_generators_cover_every_maximal_minor` in `research/ucns/src/ucns/prime_determinantal_grobner.py` (direct) - P7 E1 or P5 E3 generators are constructed
- `prime_grobner_independent_replay_agrees` in `research/ucns/src/ucns/prime_determinantal_grobner.py` (direct) - primary and independent computations finish within frozen bounds
- `prime_grobner_protocol_identity_is_frozen` in `research/ucns/src/ucns/prime_determinantal_grobner.py` (direct) - a determinantal basis computation begins
- `prime_grobner_receipt_preserves_nonclaims` in `research/ucns/src/ucns/prime_determinantal_grobner.py` (direct) - the family receipt is serialized
- `prime_exact_milnor_alexander_receipt_is_nonselecting` in `research/ucns/src/ucns/prime_exact_milnor_alexander.py` (direct) - the family certificate is serialized
- `prime_fox_fingerprint_covers_all_prime_characters` in `research/ucns/src/ucns/prime_exact_milnor_alexander.py` (direct) - a P7 or P5 whole-link fingerprint is issued
- `prime_generic_diagram_is_fixed_before_invariants` in `research/ucns/src/ucns/prime_exact_milnor_alexander.py` (direct) - the P7 or P5 diagram is constructed
- `prime_generic_diagram_preserves_pairwise_linking` in `research/ucns/src/ucns/prime_exact_milnor_alexander.py` (direct) - all generic double crossings are signed
- `prime_magnus_benchmark_recovers_borromean_integer` in `research/ucns/src/ucns/prime_exact_milnor_alexander.py` (direct) - the closure of the braid sigma-one sigma-two-inverse cubed is evaluated
- `prime_p7_five_milnor_candidates_are_exact_zero_in_diagram` in `research/ucns/src/ucns/prime_exact_milnor_alexander.py` (direct) - the five pairwise-zero P7 triples are evaluated in the fixed generic diagram
- `prime_phase_selector_matches_frozen_preregistration` in `research/ucns/src/ucns/prime_exact_milnor_alexander.py` (direct) - the phase selector is evaluated
- `prime_phase_selector_uses_whole_link_character` in `research/ucns/src/ucns/prime_exact_milnor_alexander.py` (direct) - an admissible phase law is scored
- `prime_generic_helper_is_facade_witnessed` in `research/ucns/src/ucns/prime_generic_diagram.py` (direct) - the owning facade invokes this readable helper
- `prime_generic_crossing_signs_are_interval_certified` in `research/ucns/src/ucns/prime_generic_interval_certificate.py` (direct) - every reconstructed crossing has interval-certified height ordering and tangent determinant
- `prime_generic_interval_receipt_is_nonselecting` in `research/ucns/src/ucns/prime_generic_interval_certificate.py` (direct) - the family certificate is serialized
- `prime_generic_smooth_signs_are_interval_certified` in `research/ucns/src/ucns/prime_generic_interval_certificate.py` (direct) - each incident turn interval lies within one declared smooth-field segment
- `prime_generic_turns_are_outward_atan2_enclosed` in `research/ucns/src/ucns/prime_generic_interval_certificate.py` (direct) - every frozen P7/P5 generic equal-circle crossing is reconstructed
- `prime_independent_phase_milnor_receipt_is_nonselecting` in `research/ucns/src/ucns/prime_independent_phase_milnor.py` (direct) - independent replay findings are summarized
- `prime_milnor_exactness_boundary_is_preserved` in `research/ucns/src/ucns/prime_independent_phase_milnor.py` (direct) - numerical estimates resolve near integers
- `prime_milnor_fourier_benchmark_recovers_borromean` in `research/ucns/src/ucns/prime_independent_phase_milnor.py` (direct) - the numerical Fourier extractor is benchmarked
- `prime_milnor_p7_split_triples_resolve_numerically_to_zero` in `research/ucns/src/ucns/prime_independent_phase_milnor.py` (direct) - the five split P7 triples are evaluated across increasing resolutions
- `prime_phase_sensitivity_separates_selection_from_emergence` in `research/ucns/src/ucns/prime_independent_phase_milnor.py` (direct) - every equal-gap phase alternative is enumerated
- `prime_phase_sensitivity_torus_seven_is_not_forced` in `research/ucns/src/ucns/prime_independent_phase_milnor.py` (direct) - P7 and P5 maximum-gap candidates are compared
- `prime_boundary_cable_winding_is_derived_from_phase` in `research/ucns/src/ucns/prime_interval_boundaries.py` (direct) - the selected phase law is evaluated over the two-turn boundary traversal
- `prime_boundary_curve_is_single_two_turn_component` in `research/ucns/src/ucns/prime_interval_boundaries.py` (direct) - one finite-width Möbius ribbon is restricted to positive half-width
- `prime_boundary_linking_scales_by_four` in `research/ucns/src/ucns/prime_interval_boundaries.py` (direct) - boundary components retract to degree-two traversals of their cores inside pairwise-disjoint ribbons
- `prime_higher_order_boundary_is_explicit` in `research/ucns/src/ucns/prime_interval_boundaries.py` (direct) - triples of boundary components are classified by pairwise support
- `prime_interval_boundaries_p7_precedes_p5` in `research/ucns/src/ucns/prime_interval_boundaries.py` (direct) - the family certificate is built
- `prime_interval_boundary_compact_receipt_is_nonselecting` in `research/ucns/src/ucns/prime_interval_boundaries.py` (direct) - the family receipt is serialized
- `prime_interval_replay_uses_outward_endpoints` in `research/ucns/src/ucns/prime_interval_boundaries.py` (direct) - every complete pair-parameter torus is recursively covered
- `prime_mixed_core_boundary_matrix_is_complete` in `research/ucns/src/ucns/prime_interval_boundaries.py` (direct) - core-core, core-boundary, and boundary-boundary linking laws are combined
- `prime_boundary_component_knot_types_are_derived` in `research/ucns/src/ucns/prime_interval_boundary_links.py` (direct) - each centerline is a vertical graph over a circle and hence an unknot
- `prime_boundary_curve_is_single_and_closed` in `research/ucns/src/ucns/prime_interval_boundary_links.py` (direct) - one Möbius ribbon is evaluated at positive boundary breadth over two carrier turns
- `prime_boundary_linking_matrix_follows_cable_homology` in `research/ucns/src/ucns/prime_interval_boundary_links.py` (direct) - distinct boundary components each carry longitudinal coefficient two
- `prime_interval_boundary_p7_precedes_p5` in `research/ucns/src/ucns/prime_interval_boundary_links.py` (direct) - the family certificate is built
- `prime_interval_boundary_receipt_is_nonselecting` in `research/ucns/src/ucns/prime_interval_boundary_links.py` (direct) - the family receipt is serialized
- `prime_interval_replay_is_outward_rounded` in `research/ucns/src/ucns/prime_interval_boundary_links.py` (direct) - every complete P7 or P5 pair-parameter torus is replayed
- `prime_interval_replay_preserves_finite_width_disjointness` in `research/ucns/src/ucns/prime_interval_boundary_links.py` (direct) - interval centerline clearance exceeds nine hundredths and half width is one hundredth
- `prime_length_three_milnor_profile_is_computed_after_global_lift` in `research/ucns/src/ucns/prime_interval_boundary_links.py` (direct) - a clearance-preserving simultaneous generic projection is constructed
- `prime_mixed_linking_matrix_has_exact_integer_invariants` in `research/ucns/src/ucns/prime_interval_boundary_links.py` (direct) - core, boundary, and own-core boundary linkings are combined
- `prime_interval_common_is_facade_witnessed` in `research/ucns/src/ucns/prime_interval_common.py` (direct) - the owning facade invokes this readable helper
- `prime_interval_replay_helper_is_facade_witnessed` in `research/ucns/src/ucns/prime_interval_replay.py` (direct) - the owning facade invokes this readable helper
- `prime_length4_magnus_gate_matches_frozen_commutator` in `research/ucns/src/ucns/prime_length4_milnor.py` (direct) - the degree-three Magnus engine evaluates [[x1,x2],x3]
- `prime_p7_length4_receipt_is_bounded` in `research/ucns/src/ucns/prime_length4_milnor.py` (direct) - the result is serialized
- `prime_p7_length4_result_records_cyclic_conventions` in `research/ucns/src/ucns/prime_length4_milnor.py` (direct) - the frozen target passes its lower-order gates
- `prime_p7_length4_target_is_frozen_and_lower_gated` in `research/ucns/src/ucns/prime_length4_milnor.py` (direct) - the minimal P7 length-four experiment is evaluated
- `prime_milnor_helper_is_facade_witnessed` in `research/ucns/src/ucns/prime_milnor_invariants.py` (direct) - the owning facade invokes this readable helper
- `prime_nilpotent_comparison_excludes_known_rank` in `research/ucns/src/ucns/prime_nilpotent_discriminator.py` (direct) - P7 and P5 higher signatures are compared
- `prime_nilpotent_phase_binding_is_topological` in `research/ucns/src/ucns/prime_nilpotent_discriminator.py` (direct) - substantive phase co-winners bind identical group and peripheral inputs
- `prime_nilpotent_primary_and_replay_agree` in `research/ucns/src/ucns/prime_nilpotent_discriminator.py` (direct) - GAP/NQ emits a class-four marked quotient
- `prime_nilpotent_protocol_identity_is_frozen` in `research/ucns/src/ucns/prime_nilpotent_discriminator.py` (direct) - a quotient computation starts
- `prime_phase_lift_centerlines_are_disjoint` in `research/ucns/src/ucns/prime_phase_lift.py` (direct) - the complete projected pair-event ledger
- `prime_phase_lift_constructs_p7_before_restrictions` in `research/ucns/src/ucns/prime_phase_lift.py` (direct) - the phase-lift family is built
- `prime_phase_lift_is_seam_compatible` in `research/ucns/src/ucns/prime_phase_lift.py` (direct) - a carrier surface is evaluated
- `prime_phase_lift_link_numbers_are_derived` in `research/ucns/src/ucns/prime_phase_lift.py` (direct) - a pair has a regular two-crossing projection
- `prime_phase_lift_p5_follows_same_protocol` in `research/ucns/src/ucns/prime_phase_lift.py` (direct) - P7 is complete
- `prime_phase_lift_preserves_nary_origin` in `research/ucns/src/ucns/prime_phase_lift.py` (direct) - the P7 origin is evaluated
- `prime_phase_lift_receipt_is_nonselecting` in `research/ucns/src/ucns/prime_phase_lift.py` (direct) - the family receipt is serialized
- `prime_phase_lift_resolves_every_hypernode` in `research/ucns/src/ucns/prime_phase_lift.py` (direct) - any P7 or P5 hypernode
- `prime_phase_lift_data_covers_every_p7_p5_hypernode` in `research/ucns/src/ucns/prime_phase_lift_data.py` (direct) - the P7 and P5 phase-and-lift candidates consume their frozen ledgers
- `prime_phase_lift_model_derives_links_after_global_lift` in `research/ucns/src/ucns/prime_phase_lift_model.py` (direct) - pair readouts are requested from a complete phase-and-lift candidate
- `prime_phase_lift_model_preserves_event_semantics` in `research/ucns/src/ucns/prime_phase_lift_model.py` (direct) - a lifted projected event is represented
- `prime_arithmetic_geometry_firewall` in `research/ucns/src/ucns/prime_primitives.py` (direct) - arithmetic primality and UCNS primitive standing are evaluated
- `prime_p5_direct_exact_signature` in `research/ucns/src/ucns/prime_primitives.py` (direct) - P5 is constructed directly from one center plus four outer carriers
- `prime_p7_direct_exact_signature` in `research/ucns/src/ucns/prime_primitives.py` (direct) - P7 is constructed directly from one center plus six outer carriers
- `prime_p7_uniform_structural_relation` in `research/ucns/src/ucns/prime_primitives.py` (direct) - P7 spoke and adjacent-rim separations are measured
- `prime_restrictions_follow_construction` in `research/ucns/src/ucns/prime_primitives.py` (direct) - dyadic and triadic readouts are reported
- `prime_two_cycle_boundary` in `research/ucns/src/ucns/prime_primitives.py` (direct) - K2 is tested under a closure axiom requiring a nontrivial relational cycle
- `prime_replay_data_is_receipt_witnessed` in `research/ucns/src/ucns/prime_replay_phase_milnor_data.py` (direct) - the owning facade invokes this readable helper
- `prime_replay_receipt_exposes_phase_imposition` in `research/ucns/src/ucns/prime_replay_phase_milnor_receipt.py` (direct) - P7 and P5 selected phase laws are compared
- `prime_replay_receipt_freezes_p7_milnor_values` in `research/ucns/src/ucns/prime_replay_phase_milnor_receipt.py` (direct) - the five algebraically split outer triples are audited
- `prime_replay_receipt_is_nonselecting` in `research/ucns/src/ucns/prime_replay_phase_milnor_receipt.py` (direct) - the compact receipt is serialized
- `prime_replay_receipt_preserves_independent_interval_result` in `research/ucns/src/ucns/prime_replay_phase_milnor_receipt.py` (direct) - the compact receipt is loaded
- `prime_smooth_ribbons_are_globally_disjoint_at_declared_width` in `research/ucns/src/ucns/prime_smooth_ribbons.py` (direct) - centerline separation exceeds nine hundredths and ribbon half-width is one hundredth
- `prime_smooth_ribbons_have_global_centerline_margin` in `research/ucns/src/ucns/prime_smooth_ribbons.py` (direct) - every unordered pair of P7 or P5 carriers is subdivided over the complete parameter torus
- `prime_smooth_ribbons_issue_complete_linking_matrix` in `research/ucns/src/ucns/prime_smooth_ribbons.py` (direct) - regular secant readouts and tangent regularizations are combined
- `prime_smooth_ribbons_obey_mobius_return` in `research/ucns/src/ucns/prime_smooth_ribbons.py` (direct) - any carrier and admissible breadth
- `prime_smooth_ribbons_p7_precedes_p5` in `research/ucns/src/ucns/prime_smooth_ribbons.py` (direct) - the family certificate is built
- `prime_smooth_ribbons_preserve_all_event_lanes` in `research/ucns/src/ucns/prime_smooth_ribbons.py` (direct) - the piecewise-linear P7 or P5 lift knots are replaced
- `prime_smooth_ribbons_receipt_is_nonselecting` in `research/ucns/src/ucns/prime_smooth_ribbons.py` (direct) - the family receipt is serialized
- `prime_smooth_ribbons_regularize_tangent_pairs` in `research/ucns/src/ucns/prime_smooth_ribbons.py` (direct) - a projected pair is externally tangent
- `prime_symbolic_alexander_receipt_is_nonselecting` in `research/ucns/src/ucns/prime_symbolic_alexander.py` (direct) - the family certificate is serialized
- `prime_symbolic_certificate_replays_finite_characters` in `research/ucns/src/ucns/prime_symbolic_alexander.py` (direct) - the symbolic matrix is specialized at every previously frozen prime-order character
- `prime_symbolic_elementary_boundary_is_exact` in `research/ucns/src/ucns/prime_symbolic_alexander.py` (direct) - the exact symbolic presentation is evaluated over its Laurent-polynomial fraction field
- `prime_symbolic_fox_presentation_is_exact` in `research/ucns/src/ucns/prime_symbolic_alexander.py` (direct) - the frozen P7 or P5 Wirtinger diagram is abelianized over one Laurent variable per component
- `every_public_gonol_glyph_is_a_function_position` in `research/ucns/src/ucns/public_gonol.py` (direct) - any admitted Public Gonol glyph or index
- `public_gonol_has_exactly_157_unique_positions` in `research/ucns/src/ucns/public_gonol.py` (direct) - the Public Gonol carrier is imported
- `boundary_runner_audits_before_execution` in `research/ucns/tools/run_skill_lib_boundaries.py` (direct) - declared skill-lib checks are requested for execution
- `boundary_runner_classifies_and_continues` in `research/ucns/tools/run_skill_lib_boundaries.py` (direct) - one declared check passes, fails an assertion, raises unexpectedly, or times out
- `boundary_runner_consumes_capabilities_and_timeouts` in `research/ucns/tools/run_skill_lib_boundaries.py` (direct) - a CHECKS declaration names requires and timeout fields
- `boundary_runner_has_no_activation_effect` in `research/ucns/tools/run_skill_lib_boundaries.py` (direct) - every selected check passes
- `boundary_runner_receipt_is_bounded_and_bound` in `research/ucns/tools/run_skill_lib_boundaries.py` (direct) - a boundary run completes
- `contract_audit_accepts_closed_graph` in `research/ucns/tools/verify_skill_lib_contracts.py` (direct) - every declared contract has a resolving check and every check names known contracts
- `contract_audit_is_no_exec` in `research/ucns/tools/verify_skill_lib_contracts.py` (direct) - the repository contract graph is audited
- `contract_audit_reports_graph_gaps` in `research/ucns/tools/verify_skill_lib_contracts.py` (direct) - a contract, check target, or self call is missing or unknown

### DEPENDENCIES

- `generated_src_metapat___init___py_dependencies` in `research/metapat/src/metapat/__init__.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_package_dependency_edges` in `research/metapat/src/metapat/__init__.py` (direct) - base exports depend on canon, catalog, application and engineering schemas, relations, envelopes, checks, flow declarations, Phi policy, and a lazy optional UCNS adapter
- `generated_src_metapat_flow_plan_py_dependencies` in `research/metapat/src/metapat/flow_plan.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_flow_edges` in `research/metapat/src/metapat/flow_plan.py` (direct) - METAPAT constrains interpretation while actual UCNS carries geometry and EDCM measures source evidence

### DOCS

- `edcm_ucns_fork_lint_docs` in `research/edcm/edcm/ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - documents exact topology binding, complete recursive coverage, negative fixtures, and authority boundaries
- `generated_src_metapat_affixiation_harmonics_py_docs` in `research/metapat/src/metapat/affixiation_harmonics.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_affixiation_harmonics_docs` in `research/metapat/src/metapat/affixiation_harmonics.py` (direct) - defines affixiation, time-agnostic recurrence and oscillation, harmonic relation, resonance, and the METAPAT/UCNS/EDCM authority firewall
- `generated_src_metapat_application_py_docs` in `research/metapat/src/metapat/application.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_application_module_docs` in `research/metapat/src/metapat/application.py` (direct) - documents catalog-bound application identity, source integrity, evidence firewalls, and downstream limits
- `generated_src_metapat_canon_py_docs` in `research/metapat/src/metapat/canon.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_canon_docs` in `research/metapat/src/metapat/canon.py` (direct) - documents METAPAT root doctrine and byte-complete canon identity
- `generated_src_metapat_catalog_py_docs` in `research/metapat/src/metapat/catalog.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_semantic_catalog_docs` in `research/metapat/src/metapat/catalog.py` (direct) - documents catalog completeness, source resolution, claim classification, relation ancestry, and downstream limits
- `generated_src_metapat_electromagnetic_pipe_py_docs` in `research/metapat/src/metapat/electromagnetic_pipe.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_electromagnetic_pipe_docs` in `research/metapat/src/metapat/electromagnetic_pipe.py` (direct) - preserves geometry, six-vector control topology, mobile-attractor distinction, alloy search, instrumentation, fault objectives, and empirical boundaries
- `generated_src_metapat_envelope_py_docs` in `research/metapat/src/metapat/envelope.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_module_envelope_docs` in `research/metapat/src/metapat/envelope.py` (direct) - defines the METAPAT-to-consumer semantic authority boundary
- `generated_src_metapat_quantum_magnetism_py_docs` in `research/metapat/src/metapat/quantum_magnetism.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_quantum_magnetism_docs` in `research/metapat/src/metapat/quantum_magnetism.py` (direct) - binds the worked quantum-magnetism application to exact catalog modules while preserving scale, transfer, non-transfer, and physics evidence boundaries
- `generated_src_metapat_relations_py_docs` in `research/metapat/src/metapat/relations.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_semantic_relations_docs` in `research/metapat/src/metapat/relations.py` (direct) - documents relation vocabulary, evidence status, strict identity, and the prohibition on inferred constitutive containment
- `generated_src_metapat_ucns_phi_py_docs` in `research/metapat/src/metapat/ucns_phi.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_ucns_phi_docs` in `research/metapat/src/metapat/ucns_phi.py` (direct) - documents constitutive-fork authorization and downstream fail-closed enforcement
- `generated_src_metapat_validation_py_docs` in `research/metapat/src/metapat/validation.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_canon_contract_docs` in `research/metapat/src/metapat/validation.py` (direct) - documents deterministic encoded conditions and their non-validation boundary

### MODULE_BUILD

- `interdependent_work_graph_portfolio_plan` in `research/edcm/.agents/skills/interdependent-work-graph/portfolio_plan.py` (direct, research/edcm/edcm_msdmd.ts) - validates repo-owned plan reports and derives a deterministic cross-repository portfolio projection without transferring authority
- `edcm_package` in `research/edcm/edcm/__init__.py` (direct, research/edcm/edcm_msdmd.ts) - EDCM package root — declares package identity and re-exports provenance-bearing shared-stack layers, canonical METAPAT consumer surfaces, the exact EDCM UCNS word-gonol observation profile consumer, historical fork-topology research surfaces, result contracts, integrity gates, energy audit, EDCM objects, edcmucns architecture, and canonical maintained measurement.
- `edcm_corpora_package` in `research/edcm/edcm/corpora/__init__.py` (direct, research/edcm/edcm_msdmd.ts) - source-native full-corpus execution surfaces with admission, reconciliation, and completion or incompletion receipts
- `edcm_multiwoz21_corpus` in `research/edcm/edcm/corpora/multiwoz21.py` (direct, research/edcm/edcm_msdmd.ts) - verifies, streams, and reconciles every exact MultiWOZ 2.1 speaker turn through the pinned EDCM UCNS word-gonol profile and v0.14.1 completion gate from the merged v0.19 producer with final integrity repairs without committing raw text
- `edcm_multiwoz21_booking_outcome_holdout` in `research/edcm/edcm/corpora/multiwoz21_booking_holdout.py` (direct, research/edcm/edcm_msdmd.ts) - evaluates the maintained EDCM terminal-progress candidate against externally authored MultiWOZ 2.1 booking outcome events after development calibration and validation threshold freeze
- `edcm_multiwoz21_seal_launcher` in `research/edcm/edcm/corpora/run_multiwoz21_seal.py` (direct, research/edcm/edcm_msdmd.ts) - establishes a cache-independent replacement-disabled Git snapshot before importing the sealed MultiWOZ runner
- `edcmucns_package` in `research/edcm/edcm/edcmucns/__init__.py` (direct, research/edcm/edcm_msdmd.ts) - edcmucns v0.3.1 — EDCM on UCNS mathematics, provenance as the recurring theme; architecture-only implementation surface (identity layer), empirical claims remain frontier gates
- `edcmucns_composer` in `research/edcm/edcm/edcmucns/composer.py` (direct, research/edcm/edcm_msdmd.ts) - SeqAppend window composition (chronological append; lengths add; F concatenates; carrier = lcm), reserved interaction product, payload flat reduction, kappa ledger placeholders
- `edcmucns_encoder` in `research/edcm/edcm/edcmucns/encoder.py` (direct, research/edcm/edcm_msdmd.ts) - v0.3.1 turn encoder — bone events to origin-anchored windows with provenance witnesses; no-bone turns emit AbsentOperatorGeometry; cadence admission from text is a reserved frontier gate
- `edcmucns_epochs` in `research/edcm/edcm/edcmucns/epochs.py` (direct, research/edcm/edcm_msdmd.ts) - Epoch chain for edcmucns v0.3.1 — manifest rotation seals the segment and opens a new epoch; cross-epoch comparisons are Bridge lensing events, not raw deltas
- `edcmucns_equivalence` in `research/edcm/edcm/edcmucns/equivalence.py` (direct, research/edcm/edcm_msdmd.ts) - v0.3.1 equivalence tiers — ucns_carrier_equivalent (geometry only) and edcm_measurement_equivalent (geometry + in-scope witness + manifest); contact convergence is a frontier gate
- `edcmucns_field_reader` in `research/edcm/edcm/edcmucns/field_reader.py` (direct, research/edcm/edcm_msdmd.ts) - field reader — build the ConstraintField/FieldMotion hash chain for a window's field_scope; NA-safe motion/state readouts; no empirical claim
- `edcmucns_geometry` in `research/edcm/edcm/edcmucns/geometry.py` (direct, research/edcm/edcm_msdmd.ts) - v0.3.1 non-origin residue rule, anchor angles, mass helpers (L_geo/L_op), carriers (n_host_total/n_family/n_cadence/n_payload), operator shares, lambda_field
- `edcmucns_manifest` in `research/edcm/edcm/edcmucns/manifest.py` (direct, research/edcm/edcm_msdmd.ts) - PolicyManifest — the measurement-identity manifest for edcmucns v0.3.1; stable-serializable, hashable; hash changes create epoch breaks
- `edcmucns_provenance` in `research/edcm/edcm/edcmucns/provenance.py` (direct, research/edcm/edcm_msdmd.ts) - ProvenanceWitness — anchor-level testimony for edcmucns v0.3.1; provenance is measurement material, not decorative metadata
- `edcmucns_scopes` in `research/edcm/edcm/edcmucns/scopes.py` (direct, research/edcm/edcm_msdmd.ts) - Closed readout_scope registry for edcmucns v0.3.1 — edcm_measurement_equivalent must not accept arbitrary strings
- `edcmucns_types` in `research/edcm/edcm/edcmucns/types.py` (direct, research/edcm/edcm_msdmd.ts) - Core edcmucns v0.3.1 value objects — Anchor (origin/bone/cadence), Payload, Window, OperatorTurn (Present | AbsentOperatorGeometry), BridgeDiagnostic
- `edcmucns_validation` in `research/edcm/edcm/edcmucns/validation.py` (direct, research/edcm/edcm_msdmd.ts) - witness_geometry_consistent validator + polarity gauge audit — mismatches emit Bridge diagnostics, never silent alternate readings
- `edcm_energy_claims` in `research/edcm/edcm/energy_claims.py` (direct, research/edcm/edcm_msdmd.ts) - stdlib-only energy-theory falsifiability audit with explicit UCNS package/adapter/evidence status and no physics validation or proof-status transfer
- `edcm_falsifiability_bridge` in `research/edcm/edcm/falsifiability_bridge.py` (direct, research/edcm/edcm_msdmd.ts) - audits whether falsifiability-bearing claims survive input->output using the stdlib energy audit; optional edcmbone structural-density as auxiliary metadata only
- `edcm_goal_vector_experiment` in `research/edcm/edcm/goal_vector_experiment.py` (direct, research/edcm/edcm_msdmd.ts) - runs a controlled same-occurrences/different-order contradiction experiment through the exact current UCNS observation profile and an inspectable EDCM goal-state candidate
- `edcm_gonol` in `research/edcm/edcm/gonol.py` (direct, research/edcm/edcm_msdmd.ts) - unified EDCM candidate constructor that closes gonols through declared scale option sets while preserving closed-gonol atomicity, carried suffix options, deterministic replay, and UCNS/METAPAT authority boundaries
- `edcm_integrity` in `research/edcm/edcm/integrity.py` (direct, research/edcm/edcm_msdmd.ts) - non-tautological frozen-canon byte manifest and measurement source-of-truth drift gate with installed-package CLI
- `edcm_language_package` in `research/edcm/edcm/language/__init__.py` (direct, research/edcm/edcm_msdmd.ts) - exposes exact OEWN evidence, reversible lexical candidates, and independent EDCM-to-UCNS relational branch construction without EDCM-owned geometry
- `edcm_language_affixes` in `research/edcm/edcm/language/affixes.py` (direct, research/edcm/edcm_msdmd.ts) - expands every canonical EDCM affix and allomorph into a deterministic universally applicable inventory for the OEWN 2025 run
- `edcm_language_glyph_floor` in `research/edcm/edcm/language/glyph_floor.py` (direct, research/edcm/edcm_msdmd.ts) - lazily consumes the UCNS-owned public gonol without retaining a competing EDCM arrangement authority
- `edcm_language_manifest` in `research/edcm/edcm/language/manifest.py` (direct, research/edcm/edcm_msdmd.ts) - pins OEWN evidence and the exact UCNS relational producer while forbidding geometry and status transfer
- `edcm_language_model` in `research/edcm/edcm/language/model.py` (direct, research/edcm/edcm_msdmd.ts) - defines explicit composition trees, evidence states, and direct/generated atomic comparison records without placing linguistic metadata inside gonols
- `edcm_language_morphology` in `research/edcm/edcm/language/morphology.py` (direct, research/edcm/edcm_msdmd.ts) - derives the run root set and the complete affix/compound decomposition DAG for every OEWN surface while preserving all valid alternatives
- `edcm_language_relational_bridge` in `research/edcm/edcm/language/relational_bridge.py` (direct, research/edcm/edcm_msdmd.ts) - independently constructs direct-atomic and molecular OEWN relation inputs for the UCNS metadata-free relational carrier and freezes external identity bindings before comparison
- `edcm_language_rendering` in `research/edcm/edcm/language/rendering.py` (direct, research/edcm/edcm_msdmd.ts) - codifies reversible English orthographic and compounding transformations without using them as composition gates
- `edcm_language_oewn_source` in `research/edcm/edcm/language/source.py` (direct, research/edcm/edcm_msdmd.ts) - loads the exact Open English WordNet 2025 YAML release into deterministic lemma, sense, synset, and relation records and computes a source-tree digest
- `edcm_layers` in `research/edcm/edcm/layers.py` (direct, research/edcm/edcm_msdmd.ts) - Provenance-bearing EDCM stack with independently selected METAPAT semantic authority, exact UCNS word-gonol observation profile or typed absence, canonical local measurement, shared-stack composition, and final result-contract delivery.
- `edcmbone_canon_loader` in `research/edcm/edcm/measurement/canon/loader.py` (direct, research/edcm/edcm_msdmd.ts) - loads the v1 canon data files (bones/affixes/punct/markers) and exposes a lookup API
- `edcmbone_compress` in `research/edcm/edcm/measurement/compress.py` (direct, research/edcm/edcm_msdmd.ts) - lossless EDCM-aware codec for ParsedTranscript + RoundMetrics (separate bone/flesh streams, zlib entropy coding)
- `edcmbone_metrics_compute` in `research/edcm/edcm/measurement/metrics/compute.py` (direct, research/edcm/edcm_msdmd.ts) - computes the EDCM metric vector M_t and dissonance energy for a parsed round/transcript
- `edcmbone_metrics_matrix` in `research/edcm/edcm/measurement/metrics/matrix.py` (direct, research/edcm/edcm_msdmd.ts) - explicit freezable A matrix (Layer0->Layer1) and PROJECTION_MAP (Layer1->Layer3) as versioned, diffable dicts
- `edcmbone_metrics_projection` in `research/edcm/edcm/measurement/metrics/projection.py` (direct, research/edcm/edcm_msdmd.ts) - projects the 11 Layer-1 Arc-Style metrics to the 6 agent-facing metrics (CM, DA, DRIFT, DVG, INT, TBF)
- `edcmbone_metrics_risk` in `research/edcm/edcm/measurement/metrics/risk.py` (direct, research/edcm/edcm_msdmd.ts) - the EDCM risk proxies (fixation, broken-return, escalation, stagnation, loop), all clamped to [0,1]
- `edcmbone_metrics_stats` in `research/edcm/edcm/measurement/metrics/stats.py` (direct, research/edcm/edcm_msdmd.ts) - stdlib-only text statistics (TTR, entropy, novelty, cosine, n-gram density) feeding the EDCM metric vector
- `edcmbone_parser_turns_rounds` in `research/edcm/edcm/measurement/parser/turns_rounds.py` (direct, research/edcm/edcm_msdmd.ts) - embedded rule-based transcript parser (canon-driven, no ML deps) producing bones/flesh tokens, turns, and rounds
- `edcmbone_ucns_closed_tokens` in `research/edcm/edcm/measurement/ucns/closed_tokens.py` (direct, research/edcm/edcm_msdmd.ts) - encodes English closed-class tokens, whitespace, punctuation, and small numerals to UCNS objects on a 16-gon host carrier
- `edcmbone_ucns_v04` in `research/edcm/edcm/measurement/ucns/ucns_v04.py` (direct, research/edcm/edcm_msdmd.ts) - local UCNS engine using the turn-fraction angle convention on the doubled cover of the unit circle
- `edcm_metapat_adapter` in `research/edcm/edcm/metapat_adapter.py` (direct, research/edcm/edcm_msdmd.ts) - EDCM-owned consumer for actual versioned immutable METAPAT semantic-authority envelopes; preserves canon identity, exact source references, constraints, permitted interpretations, hmmm, and provenance without creating metric values.
- `recovered_dissonance_controlled_gate` in `research/edcm/edcm/recovered_dissonance_experiment.py` (direct, research/edcm/edcm_msdmd.ts) - executes the frozen absolute-recovery scale falsifier and its sole normalized-positive-pressure escalation without external labels
- `recovered_dissonance_external_evaluator` in `research/edcm/edcm/recovered_dissonance_external_evaluator.py` (direct, research/edcm/edcm_msdmd.ts) - evaluates one frozen aggregate MultiWOZ booking batch with normalized recovered dissonance through the UCNS PR 196 external protocol
- `edcm_shared_stack` in `research/edcm/edcm/shared_stack.py` (direct, research/edcm/edcm_msdmd.ts) - deterministic final EDCM result contract separating source evidence, METAPAT semantic authority, exact UCNS word-gonol observations, typed UCNS geometry and factorization absence, EDCM policy identity, implementation provenance, readouts/NA, unresolved constraints, and attachment states.
- `edcm_ucns_adapter` in `research/edcm/edcm/ucns_adapter.py` (direct, research/edcm/edcm_msdmd.ts) - fail-closed consumer for the exact EDCM-only UCNS word-gonol profile from the merged v0.19 producer with final integrity repairs, preserving full-corpus speaker-turn observations without coordinate, geometry, or proof transfer
- `edcm_ucns_dependency` in `research/edcm/edcm/ucns_dependency.py` (direct, research/edcm/edcm_msdmd.ts) - diagnostics and fail-closed loading for the optional exact EDCM UCNS word-gonol profile
- `edcm_ucns_edcm_experiments` in `research/edcm/edcm/ucns_edcm_experiments.py` (direct, research/edcm/edcm_msdmd.ts) - runs fixed contrastive EDCM cases through the maintained EDCM baseline, a transparent candidate, explicit event-to-UCNS encodings, and noncanonical UCNS equivalence/M/B candidates
- `edcm_ucns_edcm_experiments_v2` in `research/edcm/edcm/ucns_edcm_experiments_v2.py` (direct, research/edcm/edcm_msdmd.ts) - expands the joint UCNS-EDCM falsifier program across refusal dose, constraint paraphrase coverage, resolution latency, and explicit support-assignment stability
- `edcm_ucns_edcm_experiments_v3` in `research/edcm/edcm/ucns_edcm_experiments_v3.py` (direct, research/edcm/edcm_msdmd.ts) - tests assertion, negation, quotation, hypotheticals, attribution, retraction, and repair order through scope-bearing EDCM events and UCNS structural projections
- `edcm_ucns_edcm_experiments_v4` in `research/edcm/edcm/ucns_edcm_experiments_v4.py` (direct, research/edcm/edcm_msdmd.ts) - tests cross-turn reference resolution, correction targets, anaphora, nested quotation, suspension, conditional activation, contradiction ownership, and competing discourse graphs
- `edcm_ucns_fork_lint` in `research/edcm/edcm/ucns_fork_lint.py` (direct, research/edcm/edcm_msdmd.ts) - binds METAPAT constitutive-fork authorizations to exact UCNS payload paths, indices, and stable hashes and fails closed over the complete recursive object
- `edcm_ucns_objects` in `research/edcm/edcm/ucns_objects.py` (direct, research/edcm/edcm_msdmd.ts) - dependency-free mirror of edcmbone's UCNS metric construction layer (v0.2 signed-axis orthogonality)
- `edcm_tarot_corpus_acquirer` in `research/edcm/tools/acquire_tarot_corpus.py` (direct, research/edcm/edcm_msdmd.ts) - validates a provenance-only Tarot source manifest, acquires only explicitly authorized public-domain bytes, and seals deterministic evidence receipts without defining Tarot ontology
- `edcm_oewn2025_lexical_floor_builder` in `research/edcm/tools/build_oewn2025_embeddings.py` (direct, research/edcm/edcm_msdmd.ts) - acquires or verifies the pinned OEWN source and independently freezes direct-atomic and molecular UCNS relational artifacts before comparison
- `edcm_tarot_relation_discovery` in `research/edcm/tools/discover_tarot_relations.py` (direct, research/edcm/edcm_msdmd.ts) - validates a sealed Tarot acquisition and discovers only ordered source-envelope assertions and exact-value agreements without selecting Tarot ontology
- `edcm_tarot_pdf_text_layer_gate` in `research/edcm/tools/evaluate_tarot_pdf_text_layer.py` (direct, research/edcm/edcm_msdmd.ts) - executes the frozen MuPDF embedded-text adequacy gate over the two exact acquired Wellcome PDFs without OCR or semantic inspection
- `edcm_tarot_ocr_v4_runner` in `research/edcm/tools/run_tarot_ocr_v4.py` (direct, research/edcm/edcm_msdmd.ts) - executes the frozen Tarot OCR v4 protocol with exact producer identities, resumable raw outputs, deterministic manifests, and independent-reference scoring
- `edcm_tarot_ocr_v5_runner` in `research/edcm/tools/run_tarot_ocr_v5.py` (direct, research/edcm/edcm_msdmd.ts) - executes the frozen Tarot OCR v5 adaptive-threshold protocol through the v4 evidence-preserving core
- `edcm_tarot_ocr_v6_runner` in `research/edcm/tools/run_tarot_ocr_v6.py` (direct, research/edcm/edcm_msdmd.ts) - executes the frozen Tarot OCR v6 historic-print model protocol through the v4 evidence-preserving core
- `edcm_tarot_ocr_v7_runner` in `research/edcm/tools/run_tarot_ocr_v7.py` (direct, research/edcm/edcm_msdmd.ts) - executes the frozen Tarot OCR v7 renderer-flag repair with the unchanged historic-print instrument
- `epac_public_gonol` in `research/epac/epac_public_gonol.py` (direct) - EPAC candidate constructor that closes gonols on the UCNS Public Gonol carrier with oriented couplings and arity charge states; not the EDCM text-domain constructor
- `epac_subatomic_element_affixiation_candidate` in `research/epac/subatomic/element_affixiation_candidate.py` (direct) - identity-only H/He/Li/C element-gonol candidates over established UCNS carrier identity and native Möbius framing; no position operation invented
- `epac_subatomic_extended_atomic` in `research/epac/subatomic/extended_atomic.py` (direct) - atomic quantum-layer records Z=1..26 for subatomic gonols; Z<=18 delegates to epac_atomic, Z=19..26 from declared ground-state configurations with Aufbau/Slater extension
- `epac_subatomic_nuclear_harmonic_candidates` in `research/epac/subatomic/nuclear_harmonic_candidates.py` (direct) - physically sourced H/He/Li/C nuclear harmonic-relation candidates over METAPAT harmonic semantics with declared recurrence mappings and provenance
- `epac_subatomic_gonol` in `research/epac/subatomic/subatomic_gonol.py` (direct) - closes one subatomic element gonol per symbol from subatomic nucleus identity, nuclear harmonic relations, and quantum-layer electron shells via the EPAC Public Gonol constructor
- `epac_subatomic_symbol_coupling` in `research/epac/subatomic/symbol_coupling.py` (direct) - nomenclature-only coupling of a closed subatomic element gonol to its abbreviation; letters are not physics and do not enter dimensional 3-structure
- `generated_src_metapat___init___py_module_build` in `research/metapat/src/metapat/__init__.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_package_exports` in `research/metapat/src/metapat/__init__.py` (direct) - re-exports byte-complete canon identity, the semantic catalog, strict catalog-bound applications and engineering records, immutable envelopes and relations, deterministic checks, explicit UCNS Phi authority, and the optional actual-UCNS adapter
- `generated_src_metapat_affixiation_harmonics_py_module_build` in `research/metapat/src/metapat/affixiation_harmonics.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_affixiation_harmonics_application` in `research/metapat/src/metapat/affixiation_harmonics.py` (direct) - defines catalog-bound conceptual semantics for identity-preserving affixiation and time-agnostic harmonic relation while leaving UCNS implementation and EDCM measurement authority downstream
- `generated_src_metapat_application_py_module_build` in `research/metapat/src/metapat/application.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_application_module_schema` in `research/metapat/src/metapat/application.py` (direct) - defines strict application modules and catalog bindings that preserve source, claim status, evidence boundaries, and unresolved hmmm without promoting applications into canon or proof
- `generated_src_metapat_canon_py_module_build` in `research/metapat/src/metapat/canon.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_canon_core` in `research/metapat/src/metapat/canon.py` (direct) - exposes exact Meta Energy Theory root constants and a deterministic identity that includes every canon-bearing Markdown file
- `generated_src_metapat_catalog_py_module_build` in `research/metapat/src/metapat/catalog.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_semantic_catalog` in `research/metapat/src/metapat/catalog.py` (direct) - materializes the complete current METAPAT root, axiom, postulate, theorem, and theory surfaces as addressable provenance-bearing modules
- `generated_src_metapat_catalog_build_py_module_build` in `research/metapat/src/metapat/catalog_build.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_semantic_catalog_builder` in `research/metapat/src/metapat/catalog_build.py` (direct) - constructs the canonical semantic catalog from static declarations and verifies completeness and exact Markdown source resolution
- `generated_src_metapat_catalog_data_py_module_build` in `research/metapat/src/metapat/catalog_data.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_semantic_catalog_declarations` in `research/metapat/src/metapat/catalog_data.py` (direct) - combines stable doctrine and theory declarations for canonical catalog construction
- `generated_src_metapat_catalog_doctrine_data_py_module_build` in `research/metapat/src/metapat/catalog_doctrine_data.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_semantic_doctrine_declarations` in `research/metapat/src/metapat/catalog_doctrine_data.py` (direct) - declares stable axiom, postulate, and theorem module identities, classes, source sections, and exact statements
- `generated_src_metapat_catalog_theory_data_py_module_build` in `research/metapat/src/metapat/catalog_theory_data.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_semantic_theory_declarations` in `research/metapat/src/metapat/catalog_theory_data.py` (direct) - declares stable theory module identities, exact claim statements, and source-declared derivation ancestry
- `generated_src_metapat_electromagnetic_pipe_py_module_build` in `research/metapat/src/metapat/electromagnetic_pipe.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_electromagnetic_pipe_application` in `research/metapat/src/metapat/electromagnetic_pipe.py` (direct) - preserves the three-phase nested electromagnetic-pipe handoff as a strict catalog-bound engineering application and design record without claiming device performance
- `generated_src_metapat_envelope_py_module_build` in `research/metapat/src/metapat/envelope.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_module_envelope` in `research/metapat/src/metapat/envelope.py` (direct) - versioned immutable semantic-authority and provenance envelope for UCNS adapters and EDCM consumers
- `generated_src_metapat_flow_plan_py_module_build` in `research/metapat/src/metapat/flow_plan.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_flow_plan` in `research/metapat/src/metapat/flow_plan.py` (direct) - separates METAPAT semantic authority flow, EDCM/UCNS runtime data flow, and proof-status non-transfer
- `generated_src_metapat_quantum_magnetism_py_module_build` in `research/metapat/src/metapat/quantum_magnetism.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_quantum_magnetism_application` in `research/metapat/src/metapat/quantum_magnetism.py` (direct) - materializes the quantum-magnetism worked note as a strict cross-domain application module bound to exact catalog module identities and evidence limits
- `generated_src_metapat_relations_py_module_build` in `research/metapat/src/metapat/relations.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_semantic_relations` in `research/metapat/src/metapat/relations.py` (direct) - defines strict digest-bound semantic relation records and bounded claim-status vocabulary for the canonical module catalog
- `generated_src_metapat_ucns_py_module_build` in `research/metapat/src/metapat/ucns.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_exact_ucns_profile_consumer` in `research/metapat/src/metapat/ucns.py` (direct) - consumes only the exact post-reset UCNS ordered-occurrence profile while retaining METAPAT semantic authority externally
- `generated_src_metapat_ucns_phi_py_module_build` in `research/metapat/src/metapat/ucns_phi.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_ucns_phi_policy` in `research/metapat/src/metapat/ucns_phi.py` (direct) - issues strict canon-bound constitutive-simultaneous authorization records before semantic UCNS payload forks
- `generated_src_metapat_validation_py_module_build` in `research/metapat/src/metapat/validation.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_canon_contract_checks` in `research/metapat/src/metapat/validation.py` (direct) - deterministic canon contract checks retained at the compatibility module path; not theorem verification or empirical validation
- `generated_tools_check_contract_graph_py_module_build` in `research/metapat/tools/check_contract_graph.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_contract_graph_audit` in `research/metapat/tools/check_contract_graph.py` (direct) - reconciles source-owned CONTRACTS against test-owned CHECKS without importing product or test modules
- `generated_tools_generate_application_fixtures_py_module_build` in `research/metapat/tools/generate_application_fixtures.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_application_fixture_generator` in `research/metapat/tools/generate_application_fixtures.py` (direct) - generates or verifies deterministic packaged application and engineering-design fixtures from canonical constructors
- `generated_tools_generate_catalog_py_module_build` in `research/metapat/tools/generate_catalog.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_catalog_generator` in `research/metapat/tools/generate_catalog.py` (direct) - generates or verifies byte-current root-spine-envelope-v2 and semantic-module-catalog-v2 fixtures from their live constructors
- `generated_tools_generate_msdmd_py_module_build` in `research/metapat/tools/generate_msdmd.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_msdmd_generator` in `research/metapat/tools/generate_msdmd.py` (direct) - invokes the pinned skill-lib collector over METAPAT source, tests, and repository tools while excluding vendored skill declarations
- `pcea_cipher` in `research/pcea/pcea/cipher.py` (direct, research/pcea/pcea_msdmd.ts) - prime-circular Mobius disk cipher: fixed-width base-p digit encode with SHA-256 keyed additive shift
- `pcea_codec` in `research/pcea/pcea/codec.py` (direct, research/pcea/pcea_msdmd.ts) - Mobius disk codec: signed<->unsigned position mapping and fixed-width base-p digit encoding
- `pcea_contract` in `research/pcea/pcea/contract.py` (direct, research/pcea/pcea_msdmd.ts) - PCEA<->UCNS interface-contract constants and guardrails (single source of truth)
- `pcea_instance` in `research/pcea/pcea/instance.py` (direct, research/pcea/pcea_msdmd.ts) - stateful PCEA session that auto-advances last_state so sender/receiver stay synchronized
- `pcea_kdf` in `research/pcea/pcea/kdf.py` (direct, research/pcea/pcea_msdmd.ts) - hash-based key-stream derivation keyed by hierarchical address plus heptagram neighbors
- `pcea_primes` in `research/pcea/pcea/primes.py` (direct, research/pcea/pcea_msdmd.ts) - fixed 53-prime circle used as the circular bases for prime-circular base encryption
- `interdependent_work_graph_portfolio_plan` in `research/ptcna/.agents/skills/interdependent-work-graph/portfolio_plan.py` (direct, research/ptcna/ptcna_msdmd.ts) - validates repo-owned plan reports and derives a deterministic cross-repository portfolio projection without transferring authority
- `ptcna_package_surface` in `research/ptcna/ptcna/__init__.py` (direct, research/ptcna/ptcna_msdmd.ts) - exposes the four layers, explicit runtime boundary, dependable fallback, and frozen evaluation types from the package root
- `ptcna_circle_composition` in `research/ptcna/ptcna/circle/compose.py` (direct, research/ptcna/ptcna_msdmd.ts) - composes ordered neural payloads into a standalone non-differentiating circle tensor
- `ptcna_circle_tensor` in `research/ptcna/ptcna/circle/tensor.py` (direct, research/ptcna/ptcna_msdmd.ts) - represents the non-differentiating circle-layer output that structurally hosts ordered neural payloads
- `prime_core_constants` in `research/ptcna/ptcna/core/prime_core/constants.py` (direct, research/ptcna/ptcna_msdmd.ts) - frozen PTCA composition counts plus the recursive coherence-prime guard
- `ptcna_prime_core_composition` in `research/ptcna/ptcna/core/prime_core/core.py` (direct, research/ptcna/ptcna_msdmd.ts) - composes opaque fiqs through the shared circle and seed types into a non-differentiating core
- `ptcna_fiq_host` in `research/ptcna/ptcna/core/prime_core/fiq.py` (direct, research/ptcna/ptcna_msdmd.ts) - preserves opaque payload vectors inside a non-differentiating core timing host
- `ptcna_critical_evaluation` in `research/ptcna/ptcna/critical_evaluation.py` (direct, research/ptcna/ptcna_msdmd.ts) - loads the immutable representative role-acquisition plan and seals its separate usefulness and superiority verdicts
- `ptcna_frozen_evaluation` in `research/ptcna/ptcna/evaluation.py` (direct, research/ptcna/ptcna_msdmd.ts) - freezes the workload, training schedule, comparator, metric, thresholds, limits, stopping rule, failure propagation, and evidence receipt before target-versus-fallback execution
- `pcna_helix_vis` in `research/ptcna/ptcna/neural/helix_vis.py` (direct, research/ptcna/ptcna_msdmd.ts) - Visualizes the spectral state of a 7-seed Meta Router by plotting the complex descriptor Z over a simulated trajectory and saving an animation.
- `pcna_memory_core` in `research/ptcna/ptcna/neural/memory_core.py` (direct, research/ptcna/ptcna_msdmd.ts) - Parameterized in-memory ring (long-term N=19/seed=19, short-term N=17/seed=17) with round-robin write, content-addressed query, and flush_to() transfer on positive reward.
- `pcna_merge` in `research/ptcna/ptcna/neural/merge.py` (direct, research/ptcna/ptcna_msdmd.ts) - Stateless multi-instance merge operator for PCNAEngine meshes with three modes (absorb, fork, converge) via federated averaging; all output dicts use theta_* keys.
- `pcna_pcna` in `research/ptcna/ptcna/neural/pcna.py` (direct, research/ptcna/ptcna_msdmd.ts) - Six-ring PCNA inference engine (phi/psi/omega/theta/memory_l/memory_s) running project->inject->propagate->seed-audit->circle-audit->coherence, with RING_WEIGHTS scoring and numpy checkpointing.
- `pcna_ring_core` in `research/ptcna/ptcna/neural/ring_core.py` (direct, research/ptcna/ptcna_msdmd.ts) - Base prime-ring tensor (shape [N,DIMS=4,PHASES=7,HEPT_SITES=7]) with heptagram Euler-step propagation and coherence = 1 - |ring - hub|_mean; substrate for Phi/Psi/Omega/Sigma.
- `pcna_routing_loop` in `research/ptcna/ptcna/neural/routing_loop.py` (direct, research/ptcna/ptcna_msdmd.ts) - Intended GlobalRouterZero routing loop worker — currently only a print stub that announces initialization.
- `ptcna_neural_scalar` in `research/ptcna/ptcna/neural/scalar.py` (direct, research/ptcna/ptcna_msdmd.ts) - owns PTCNA reverse-mode scalar operations and back-propagation exclusively inside the neural layer
- `pcna_sigma` in `research/ptcna/ptcna/neural/sigma.py` (direct, research/ptcna/ptcna_msdmd.ts) - N=41 filesystem observer ring wrapping RingCore; tracks watched file mtimes and drains content-changed events on a content_interval cadence, injecting coherence into Psi.
- `pcna_tensor_engine` in `research/ptcna/ptcna/neural/tensor_engine.py` (direct, research/ptcna/ptcna_msdmd.ts) - Tensor engine primitives — TensorState (E[a,t,m,c]) with spectral descriptor Z = Sum E.e^(i*theta), and a MarkovRecursion updater that enforces approximate mass conservation.
- `pcna_theta` in `research/ptcna/ptcna/neural/theta.py` (direct, research/ptcna/ptcna_msdmd.ts) - N=29 standalone microkernel gate ring with ragged per-node circle counts, SHA-256 blueprint sharding, and gate control via GATE_THRESHOLD=0.45.
- `pcna_topology` in `research/ptcna/ptcna/neural/topology.py` (direct, research/ptcna/ptcna_msdmd.ts) - Stable seed-id topology — maps compute-shard neighbors to global seed IDs, computes heptagram neighbors and sentinel scan paths, and serializes to JSON for HTTP responses.
- `pcna_zeta` in `research/ptcna/ptcna/neural/zeta.py` (direct, research/ptcna/ptcna_msdmd.ts) - ZFAE evaluator that consumes explicitly injected external metrics and nudges PCNAEngine.phi without implementing or importing EDCM.
- `ptcna_runtime_boundary` in `research/ptcna/ptcna/runtime.py` (direct, research/ptcna/ptcna_msdmd.ts) - exposes the intended four-layer PTCNA path and a distinct dependable fallback behind one attributed task interface
- `seed_constants` in `research/ptcna/ptcna/seed/constants.py` (direct, research/ptcna/ptcna_msdmd.ts) - seed-layer heptagram routing motif and the recursive coherence-prime guard (composition counts are variable)
- `ptcna_ucns_integration` in `research/ptcna/ptcna/ucns_integration.py` (direct, research/ptcna/ptcna_msdmd.ts) - consumes the exactly pinned UCNS 157x7x7x53 candidate receipt and independently verifies the target state bytes
- `ptcna_contract_audit` in `research/ptcna/scripts/check_contracts.py` (direct, research/ptcna/ptcna_msdmd.ts) - reconciles source CONTRACTS with test CHECKS using syntax-only call resolution
- `interdependent_work_graph_portfolio_plan` in `research/ucns/.agents/skills/interdependent-work-graph/portfolio_plan.py` (direct) - validates repo-owned plan reports and derives a deterministic cross-repository portfolio projection without transferring authority
- `ucns_geometry_public_surface` in `research/ucns/src/ucns/__init__.py` (direct) - geometry-only UCNS public surface
- `directed_carrier_floor` in `research/ucns/src/ucns/carrier.py` (direct) - represents the directed twofold branched angular carrier without defining full UCNS object semantics
- `ucns_native_mobius_geometry` in `research/ucns/src/ucns/direct_mobius.py` (direct) - exact framed Mobius root-loop quotient with 360-degree visible return and 720-degree complete return
- `ucns_mobius_vesica_certificates` in `research/ucns/src/ucns/mobius_certificates.py` (direct) - certifies the canonical Mobius Vesica centerline count, physical boundary-contact count, quotient return, null clearance, and proof firewall using exact rational Sturm arithmetic plus residual witnesses
- `ucns_mobius_vesica_continuation` in `research/ucns/src/ucns/mobius_continuation.py` (direct) - continues the exact Mobius Vesica across rational widths, replicates it into the twelve rigid Seed-of-Life pair placements, and firewalls the quarter-turn certificate from the current half-turn seed phase
- `ucns_mobius_seed_global_compatibility` in `research/ucns/src/ucns/mobius_global_compatibility.py` (direct) - proves the single-state phase/chirality capacity and contact-versus-braid boundary for assembling the certified Mobius Vesica across the twelve structural Seed-of-Life pairs
- `ucns_mobius_seed_of_life_candidate` in `research/ucns/src/ucns/mobius_seed.py` (direct) - constructs the seven-band Mobius Seed of Life as an exact projection ledger plus a deterministic nonselecting three-dimensional braid-lift candidate
- `ucns_mobius_vesica_exact_embedding` in `research/ucns/src/ucns/mobius_vesica.py` (direct) - defines the canonical two-band Mobius Vesica Piscis embedding whose centerlines meet twice and whose single continuous boundaries admit an exact four-contact certificate
- `ucns_mpfr_interval` in `research/ucns/src/ucns/mpfr_interval.py` (direct) - provides direct system-MPFR outward-rounded interval primitives for an independent P7/P5 separation replay
- `ucns_prime_boundary_link_invariants` in `research/ucns/src/ucns/prime_boundary_link_invariants.py` (direct) - readable exact boundary-component and integer linking invariant implementation
- `ucns_prime_determinantal_grobner_p7_p5` in `research/ucns/src/ucns/prime_determinantal_grobner.py` (direct) - executes the preregistered complete rational-Laurent determinantal-ideal Groebner protocol for the frozen P7 and P5 Fox matrices
- `ucns_prime_exact_milnor_alexander_p7_p5` in `research/ucns/src/ucns/prime_exact_milnor_alexander.py` (direct) - generically resolves the P7/P5 centerline diagrams, replaces the five numerical Milnor-zero candidates with exact degree-two Magnus coefficients, freezes and evaluates a prime-character Fox-Alexander phase selector, and issues whole-link rank fingerprints
- `ucns_prime_generic_diagram` in `research/ucns/src/ucns/prime_generic_diagram.py` (direct) - readable clearance-preserving generic diagram implementation
- `ucns_prime_generic_interval_certificate` in `research/ucns/src/ucns/prime_generic_interval_certificate.py` (direct) - independently replays the frozen P7/P5 generic crossing diagram with outward-rounded MPFR atan2 and smooth-field intervals
- `ucns_prime_independent_phase_milnor` in `research/ucns/src/ucns/prime_independent_phase_milnor.py` (direct) - compact executable representation of the independent interval replay, phase sensitivity, and numerical Milnor extraction
- `ucns_prime_interval_boundaries_p7_p5` in `research/ucns/src/ucns/prime_interval_boundaries.py` (direct) - replays the P7-first smooth-ribbon separation certificate with outward interval endpoints, extracts each Möbius strip's single two-turn boundary curve, and derives exact boundary-cable and mixed core-boundary invariants before P5 comparison
- `ucns_prime_interval_boundary_links_p7_p5` in `research/ucns/src/ucns/prime_interval_boundary_links.py` (direct) - replays P7-first smooth-ribbon separation with outward-rounded interval arithmetic, extracts each Möbius ribbon's single continuous boundary, and computes boundary, mixed, component-knot, and length-three Milnor readouts before any spectral construction
- `ucns_prime_interval_common` in `research/ucns/src/ucns/prime_interval_common.py` (direct) - shared constants and dependency guards for readable interval and boundary research
- `ucns_prime_interval_replay` in `research/ucns/src/ucns/prime_interval_replay.py` (direct) - readable outward-directed interval replay implementation
- `ucns_prime_length4_milnor_p7` in `research/ucns/src/ucns/prime_length4_milnor.py` (direct) - evaluates the frozen minimal P7 length-four Milnor experiment with exact degree-three Magnus arithmetic
- `ucns_prime_milnor_invariants` in `research/ucns/src/ucns/prime_milnor_invariants.py` (direct) - readable length-three Milnor extraction and benchmark implementation
- `ucns_prime_nilpotent_discriminator_p7_p5` in `research/ucns/src/ucns/prime_nilpotent_discriminator.py` (direct) - computes the frozen class-four marked peripheral nilpotent quotients for the complete P7 and P5 core links
- `ucns_prime_phase_lift_p7_p5` in `research/ucns/src/ucns/prime_phase_lift.py` (direct) - solves P7 globally with an exact seam-compatible phase law and finite-field lift over all thirteen hypernodes, then applies the same protocol independently to P5
- `ucns_prime_phase_lift_data` in `research/ucns/src/ucns/prime_phase_lift_data.py` (direct) - stores the exact P7 and P5 occurrence-turn, carrier-residue, node-generator, and projected-center ledgers consumed by the phase-and-lift witness
- `ucns_prime_phase_lift_model` in `research/ucns/src/ucns/prime_phase_lift_model.py` (direct) - defines the typed exact phase, lift, event-semantic, geometric, and derived pair-link readouts for the P7-first witness
- `ucns_prime_primitives_p7_p5` in `research/ucns/src/ucns/prime_primitives.py` (direct) - constructs P7 first and P5 second as direct exact projected carrier complexes, preserves n-ary hypernodes, and separates arithmetic primality from UCNS closed-primitive standing
- `ucns_prime_replay_phase_milnor_data` in `research/ucns/src/ucns/prime_replay_phase_milnor_data.py` (direct) - immutable independent replay, phase-sensitivity, and numerical Milnor receipt data
- `ucns_prime_replay_phase_milnor_receipt` in `research/ucns/src/ucns/prime_replay_phase_milnor_receipt.py` (direct) - freezes the independent P7/P5 interval replay, phase-winding sensitivity, and length-three P7 Milnor audit while preserving the executable reference packet as the producing evidence
- `ucns_prime_smooth_ribbons_p7_p5` in `research/ucns/src/ucns/prime_smooth_ribbons.py` (direct) - replaces the P7-first piecewise-linear lift by a C-infinity event-preserving field, certifies global finite-width ribbon separation by deterministic Lipschitz subdivision, regularizes tangent projections, and applies the same protocol to P5 second
- `ucns_prime_symbolic_alexander_p7_p5` in `research/ucns/src/ucns/prime_symbolic_alexander.py` (direct) - derives the exact multivariable Fox-Alexander presentations and certifies their first nonzero elementary-ideal boundaries for the frozen P7 and P5 diagrams
- `ucns_public_gonol_geometry` in `research/ucns/src/ucns/public_gonol.py` (direct) - exact 157-position Public Gonol carrier; every glyph position is a Public Gonol function position without linguistic subclassing
- `skill_lib_boundary_runner` in `research/ucns/tools/run_skill_lib_boundaries.py` (direct) - audits and executes declared skill-lib CHECKS as isolated pytest boundaries with capability, timeout, and receipt enforcement
- `skill_lib_contract_audit` in `research/ucns/tools/verify_skill_lib_contracts.py` (direct) - performs a no-exec reconciliation of skill-lib MODULE_BUILD, CONTRACTS, and CHECKS declarations

### OWNERS

- `generated_src_metapat_canon_py_owners` in `research/metapat/src/metapat/canon.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_canon_owner` in `research/metapat/src/metapat/canon.py` (direct) - The Interdependency
- `generated_src_metapat_flow_plan_py_owners` in `research/metapat/src/metapat/flow_plan.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_flow_owner` in `research/metapat/src/metapat/flow_plan.py` (direct) - The Interdependency
- `generated_src_metapat_validation_py_owners` in `research/metapat/src/metapat/validation.py` (research/metapat/metapat_msdmd.ts) - count: 1
- `metapat_contract_owner` in `research/metapat/src/metapat/validation.py` (direct) - The Interdependency

## Chapter 6: Skill Lib

61 declarations, 74 edges, 3 gaps, 1 collection points, 44 source files without direct MSDMD.

Collection points:
- `skill-lib/skill-lib_msdmd.ts`

| Section | Declarations | Edges | Gaps | Unannotated |
|---|---:|---:|---:|---:|
| `.` | 1 | 1 | 3 | 0 |
| `data-visualization` | 0 | 0 | 0 | 1 |
| `doctrine` | 1 | 0 | 0 | 0 |
| `interdependent-work-graph` | 1 | 1 | 0 | 0 |
| `llms` | 5 | 0 | 0 | 2 |
| `manifest` | 0 | 0 | 0 | 1 |
| `msdmd` | 4 | 2 | 0 | 6 |
| `ratios` | 1 | 0 | 0 | 2 |
| `skill_lib` | 8 | 2 | 0 | 0 |
| `tests` | 11 | 36 | 0 | 24 |
| `tools` | 2 | 1 | 0 | 7 |
| `vm-mcp` | 27 | 31 | 0 | 1 |

### CAPABILITIES

- `repo_collection_generator` in `skill-lib/msdmd/collect.py` (skill-lib/skill-lib_msdmd.ts) - Generates <reponame>_msdmd.ts collection points from module-local blocks including CHECKS
- `repo_collection_types` in `skill-lib/msdmd/collection.ts` (skill-lib/skill-lib_msdmd.ts) - Shared TypeScript shape for collection points and visualizers, including the CHECKS block name
- `collection_visualizer` in `skill-lib/msdmd/visualize.py` (skill-lib/skill-lib_msdmd.ts) - exposes: minimal Mermaid rendering for collection edges and gaps

### CHECKS

- `check_clear_is_empty_commit` in `skill-lib/tests/test_repo_loto.py` (direct) - git, python3, posix_shell
- `check_close_deletes_tag` in `skill-lib/tests/test_repo_loto.py` (direct) - git, python3, posix_shell
- `check_latest_test_wins` in `skill-lib/tests/test_repo_loto.py` (direct) - git, python3, posix_shell
- `check_one_commit_per_session` in `skill-lib/tests/test_repo_loto.py` (direct) - git, python3, posix_shell
- `check_open_never_dirties` in `skill-lib/tests/test_repo_loto.py` (direct) - git, python3, posix_shell
- `check_scar_blocks_work` in `skill-lib/tests/test_repo_loto.py` (direct) - git, python3, posix_shell
- `check_scope_enforced` in `skill-lib/tests/test_repo_loto.py` (direct, skill-lib/skill-lib_msdmd.ts) - git, python3, posix_shell
- `check_vm_mcp_current_sdk_surface` in `skill-lib/vm-mcp/tests/test_assets.py` (direct) - vm_mcp_current_sdk_surface
- `check_vm_mcp_loopback_config` in `skill-lib/vm-mcp/tests/test_assets.py` (direct) - vm_mcp_loopback_only
- `check_vm_mcp_metadata_denial` in `skill-lib/vm-mcp/tests/test_assets.py` (direct) - vm_mcp_metadata_credentials_blocked
- `check_vm_mcp_systemd_write_boundary` in `skill-lib/vm-mcp/tests/test_assets.py` (direct) - vm_mcp_host_write_confined
- `check_vm_mcp_background_cleanup` in `skill-lib/vm-mcp/tests/test_policy.py` (direct) - vm_mcp_shell_execution_bounded
- `check_vm_mcp_directory_bounded` in `skill-lib/vm-mcp/tests/test_policy.py` (direct) - vm_mcp_read_output_bounded
- `check_vm_mcp_environment_sanitized` in `skill-lib/vm-mcp/tests/test_policy.py` (direct) - vm_mcp_credentials_not_inherited
- `check_vm_mcp_listing_symlink_not_followed` in `skill-lib/vm-mcp/tests/test_policy.py` (direct) - vm_mcp_listing_symlinks_not_followed
- `check_vm_mcp_parent_escape_rejected` in `skill-lib/vm-mcp/tests/test_policy.py` (direct) - vm_mcp_read_paths_confined
- `check_vm_mcp_read_bounded` in `skill-lib/vm-mcp/tests/test_policy.py` (direct) - vm_mcp_read_output_bounded
- `check_vm_mcp_shell_cwd_escape_rejected` in `skill-lib/vm-mcp/tests/test_policy.py` (direct) - vm_mcp_shell_cwd_confined
- `check_vm_mcp_shell_default_disabled` in `skill-lib/vm-mcp/tests/test_policy.py` (direct) - vm_mcp_shell_default_disabled
- `check_vm_mcp_shell_output_bounded` in `skill-lib/vm-mcp/tests/test_policy.py` (direct) - vm_mcp_shell_execution_bounded
- `check_vm_mcp_shell_timeout` in `skill-lib/vm-mcp/tests/test_policy.py` (direct) - vm_mcp_shell_execution_bounded
- `check_vm_mcp_symlink_escape_rejected` in `skill-lib/vm-mcp/tests/test_policy.py` (direct) - vm_mcp_read_paths_confined

### CONTRACTS

- `llms_build_drift_gate` in `skill-lib/llms/build.py` (skill-lib/skill-lib_msdmd.ts) - Checks generated llms.txt against source LLMS blocks
- `ratios_strict_gate` in `skill-lib/ratios/ratios_check.py` (skill-lib/skill-lib_msdmd.ts) - Verifies first/last ratios seals for covered executable source files
- `loto_clear_is_empty_commit` in `skill-lib/skill_lib/safety/repo_loto.py` (direct) - `loto clear` on a scar
- `loto_close_deletes_tag` in `skill-lib/skill_lib/safety/repo_loto.py` (direct) - one in-scope mutation commit and passing test evidence; `loto close`
- `loto_latest_test_wins` in `skill-lib/skill_lib/safety/repo_loto.py` (direct) - a failing run of a test command followed by a passing run of the identical command
- `loto_one_commit_per_session` in `skill-lib/skill_lib/safety/repo_loto.py` (direct) - more than one commit between base and HEAD at close
- `loto_open_never_dirties` in `skill-lib/skill_lib/safety/repo_loto.py` (direct) - clean working tree; `loto open` succeeds
- `loto_scar_blocks_work` in `skill-lib/skill_lib/safety/repo_loto.py` (direct) - an unacknowledged SCAR-*.json in .loto/
- `loto_scope_enforced` in `skill-lib/skill_lib/safety/repo_loto.py` (direct, skill-lib/skill-lib_msdmd.ts) - files touched outside the declared --files globs
- `skill_spec_compliance_gate` in `skill-lib/tools/check_skill_compliance.py` (skill-lib/skill-lib_msdmd.ts) - Checks SKILL.md frontmatter, triggers, hmmm boundaries, and index registration
- `skill_index_drift_gate` in `skill-lib/tools/check_skill_lib_drift.py` (skill-lib/skill-lib_msdmd.ts) - Checks README, AGENTS, CLAUDE, ORG_DISTRIBUTION, skills.json, and generated llms.txt drift
- `vm_mcp_credentials_not_inherited` in `skill-lib/vm-mcp/policy.py` (direct) - the MCP service process has unrelated environment variables or host credentials
- `vm_mcp_listing_symlinks_not_followed` in `skill-lib/vm-mcp/policy.py` (direct) - a directory listing encounters a symlink whose target is outside VM_MCP_ROOT
- `vm_mcp_read_output_bounded` in `skill-lib/vm-mcp/policy.py` (direct) - a requested text file or directory is larger than the configured response limit
- `vm_mcp_read_paths_confined` in `skill-lib/vm-mcp/policy.py` (direct) - a file or directory tool receives a relative path, absolute path, parent traversal, or symlink target
- `vm_mcp_shell_cwd_confined` in `skill-lib/vm-mcp/policy.py` (direct) - shell execution receives a working directory outside VM_MCP_ROOT or through an escaping symlink
- `vm_mcp_shell_default_disabled` in `skill-lib/vm-mcp/policy.py` (direct) - the service starts without explicit VM_MCP_SHELL_ENABLED opt-in
- `vm_mcp_shell_execution_bounded` in `skill-lib/vm-mcp/policy.py` (direct) - shell execution emits excessive output, exceeds its timeout, or tries to leave background descendants running
- `vm_mcp_current_sdk_surface` in `skill-lib/vm-mcp/server.py` (direct) - the runtime requirements are installed for production use
- `vm_mcp_host_write_confined` in `skill-lib/vm-mcp/server.py` (direct) - the shipped systemd service starts the MCP runtime
- `vm_mcp_loopback_only` in `skill-lib/vm-mcp/server.py` (direct) - the MCP server starts with its shipped runtime configuration
- `vm_mcp_metadata_credentials_blocked` in `skill-lib/vm-mcp/server.py` (direct) - a shell command attempts to reach the standard cloud metadata-service address

### DEPENDENCIES

- `org_target_repositories` in `skill-lib/ORG_DISTRIBUTION.md` (skill-lib/skill-lib_msdmd.ts) - target repos listed in ORG_DISTRIBUTION.md

### DOCS

- `msdmd_checks_doctrine` in `skill-lib/doctrine/msdmd-checks.md` (skill-lib/skill-lib_msdmd.ts) - CONTRACTS are obligations, CHECKS are accountable witnesses, audit reconciles the witness list against the obligation list
- `msdmd_foundational_contract` in `skill-lib/msdmd/SKILL.md` (skill-lib/skill-lib_msdmd.ts) - Module Self-Declared Metadata in Markdown block syntax, parser contract, visible gap doctrine, and collection-point shape
- `module_docs` in `skill-lib/tests/test_collect.py` (direct) - module docs
- `second_docs` in `skill-lib/tests/test_universal_parser.py` (direct) - second

### LLMS

- `architecture_summary` in `skill-lib/llms/metadata.py` (direct) - content: - Skills live as root directories with SKILL.md files and optional helpers.
- `key_definitions` in `skill-lib/llms/metadata.py` (direct) - msdmd: Module Self-Declared Metadata in Markdown — the foundational convention where each source module declares its own structured metadata in a fenced comment block.
- `project_overview` in `skill-lib/llms/metadata.py` (direct) - content: skill-lib is the canonical organization-wide source for reusable agent skills in The Interdependency.
- `usage_rules` in `skill-lib/llms/metadata.py` (direct) - content: - Read AGENTS.md, skills.json, and the relevant skill file before changing a skill.
- `project_overview` in `skill-lib/tests/test_llms_build.py` (direct) - content: example only

### MODULE_BUILD

- `interdependent_work_graph_portfolio_plan` in `skill-lib/interdependent-work-graph/portfolio_plan.py` (direct) - validates repo-owned plan reports and derives a deterministic cross-repository portfolio projection without transferring authority
- `repo_mutation_gate` in `skill-lib/skill_lib/safety/repo_loto.py` (direct, skill-lib/skill-lib_msdmd.ts) - delete-on-completion session gate for repo mutation; presence of state means open work, absence means clean
- `repo_loto_evidence` in `skill-lib/tests/test_repo_loto.py` (direct) - evidentiary procedures for repo_loto CONTRACTS; standalone or pytest; --audit reconciles the declared graph without execution
- `vm_mcp_control_plane` in `skill-lib/vm-mcp/server.py` (direct) - exposes a loopback-only MCP control plane for bounded VM inspection and gated workspace shell execution

### Visible Gaps

- `skill-lib/MSDMD_COMPLIANCE_AUDIT.md` missing `executor validity`
- `skill-lib/ORG_DISTRIBUTION.md` missing `per-target source_commit audit`
- `skill-lib/skill-lib_msdmd.ts` missing `local generated refresh`

## Chapter 7: Tests

0 declarations, 0 edges, 0 gaps, 0 collection points, 1 source files without direct MSDMD.

| Section | Declarations | Edges | Gaps | Unannotated |
|---|---:|---:|---:|---:|
| `.` | 0 | 0 | 0 | 1 |

## Chapter 8: Tools

4 declarations, 0 edges, 0 gaps, 0 collection points, 0 source files without direct MSDMD.

| Section | Declarations | Edges | Gaps | Unannotated |
|---|---:|---:|---:|---:|
| `.` | 4 | 0 | 0 | 0 |

### CONTRACTS

- `stack_msdmd_docs_collection_points` in `tools/stack_msdmd_docs.py` (direct) - generated or hand-authored *_msdmd.ts collection files
- `stack_msdmd_docs_deduplicates_sources` in `tools/stack_msdmd_docs.py` (direct) - the same declaration or edge appears through multiple input sources
- `stack_msdmd_docs_directory_chapters` in `tools/stack_msdmd_docs.py` (direct) - stack MSDMD data with files under top-level directories

### MODULE_BUILD

- `stack_msdmd_docs_runner` in `tools/stack_msdmd_docs.py` (direct) - assembles stack MSDMD blocks and collection points into machine and human docs
