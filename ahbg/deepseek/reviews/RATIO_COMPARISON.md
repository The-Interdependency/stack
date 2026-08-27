# DeepCode AHBG calibration — ratio comparisons across all six reviews

## Per-direction ratios (shared 13-check framework)

| direction | standing | checks | PASS | UNRESOLVED | FAILED | pass ratio |
|---|---|---|---|---|---|---|
| grok->codex | SURVIVED | 13 | 8 | 5 | 0 | 0.615 |
| grok->deepcode | SURVIVED | 13 | 6 | 7 | 0 | 0.462 |
| codex->grok | SURVIVED | 13 | 7 | 6 | 0 | 0.538 |
| codex->deepcode | SURVIVED | 13 | 6 | 7 | 0 | 0.462 |
| deepcode->grok | SURVIVED | 13 | 8 | 5 | 0 | 0.615 |
| deepcode->codex | SURVIVED | 13 | 9 | 4 | 0 | 0.692 |

## Per-subject checker agreement

| subject | checkers | agreement ratio | standing agreement | disagreements |
|---|---|---|---|---|
| grok | codex->grok, deepcode->grok | 0.923 | True | 1 |
| codex | grok->codex, deepcode->codex | 0.923 | True | 1 |
| deepcode | grok->deepcode, codex->deepcode | 1.0 | True | 0 |

## Per-check consensus (PASS / UNRESOLVED across six reviews)

| check id | PASS | UNRESOLVED | consensus |
|---|---|---|---|
| deterministic_scenario_validation | 6 | 0 | PASS |
| event_ordering_and_lineage_integrity | 6 | 0 | PASS |
| replay_equivalence | 6 | 0 | PASS |
| no_silent_cross_instance_state_leakage | 2 | 4 | MIXED |
| known_neutral_vs_unknown | 4 | 2 | MIXED |
| hard_veto_removes_action | 4 | 2 | MIXED |
| task_value_separate_from_regulatory_burden | 4 | 2 | MIXED |
| voluntary_disengagement_capacity_preserving | 0 | 6 | UNRESOLVED |
| scope_contraction_changes_admitted_surface | 0 | 6 | UNRESOLVED |
| apparent_decoupling_delayed_cost | 0 | 6 | UNRESOLVED |
| hierarchical_models_vs_simpler_controls | 0 | 6 | UNRESOLVED |
| provider_identity_is_relation | 6 | 0 | PASS |
| unit_tests | 6 | 0 | PASS |

## Overall

- Six-review standing agreement (all SURVIVED): True
- Survived directions: 6/6
- Shared checks: 78 (PASS 44, UNRESOLVED 34)
- Overall shared pass ratio: 0.564

Agreement is replication evidence, not truth by vote. Disagreements remain
`hmmm` and are preserved in each checker's divergence register.
