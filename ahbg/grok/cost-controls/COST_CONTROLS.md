# Grok cost-control comparison

Frozen build SHA: `cce9cec7dae61304118efcd47bc0d7461200d335`
Corpus run: `corpus-run/calibration-family-1.0.1-proposal-1`

Shadow epoch: C_lambda is logged and does not select actions.

## Standing
- SURVIVED: 5
- FALSIFIED: 1
- UNRESOLVED: 6
- BLOCKED: 1

## Action-model scores (non-forced scenarios)

| model | n | accuracy | false_positive | false_negative |
|---|---:|---:|---:|---:|
| null_never_defer | 33 | 0.758 | 0 | 8 |
| wanted_axes_deficit | 33 | 0.788 | 2 | 5 |
| additive_shadow_cost_positive | 33 | 0.939 | 2 | 0 |
| binary_occupancy_veto | 33 | 1.000 | 0 | 0 |

## Components

- `runtime_burden_observables` — **UNRESOLVED**. Scenario-level numeric resource telemetry is present. Mapping C_lambda onto runtime burden still needs a fitted comparator.
- `binary_occupancy_veto_vs_null` — **SURVIVED**. On 33 non-forced scenarios, defer-all is exactly allowed_to_be<=0 or allowed_to_do<=0 (accuracy 1.000 vs null 0.758). This recovers frozen will.py; it is not a fitted cost law.
- `additive_shadow_cost_vs_binary_veto` — **FALSIFIED**. C_structural+C_transition>0 predicts defer worse than the binary veto (0.939 vs 1.000). wanted_here=0 and wanted_to_do=0 raise shadow cost but do not remove relocate.
- `wanted_axes_as_action_price` — **UNRESOLVED**. wanted_here/wanted_to_do as a defer rule accuracy 0.788 vs null 0.758. The small lift is hostility rows that also zero a wanted axis. wanted-only gradients still relocate, so those axes are logged, not gates.
- `hierarchical_coupling_vs_additive` — **BLOCKED**. Frozen shadow_cost is additive occupancy deficits only. Corpus impedance fields were not computed into C_lambda, so hierarchical coupling cannot be compared.
- `path_history_held_out_value` — **UNRESOLVED**. Occupancy is constant inside each run. repeated_hostility and sudden_hostility have identical selected_actions and refusals. Path history has no identifying variation.
- `scope_contraction_changes_admitted_surface` — **UNRESOLVED**. scope_contraction/support_removed/scope_avoidance relabel scope but keep selected_actions=3, same as affirmed_baseline. Neighbor geometry is unchanged.
- `capacity_margins_predict_transitions` — **UNRESOLVED**. high_capacity and low_capacity both selected_actions=3, refusals=0. Capacity does not change the frozen policy.
- `voluntary_disengagement_capacity_preserving` — **UNRESOLVED**. voluntary_disengagement still relocates three times. Resource telemetry is numeric, but capacity preservation is not linked to transitions.
- `known_neutral_vs_unknown_action` — **SURVIVED**. known_neutral and unknown_same_posterior both relocate three times with refusals=0. Epistemic labels do not collapse into action in the shadow epoch.
- `task_value_separate_from_regulatory_burden` — **SURVIVED**. task_value is recorded as 0.0 beside C_lambda and does not enter choose_relocate. It is separate, not a measured task quantity.
- `hard_veto_removes_relocate` — **SURVIVED**. When allowed_to_be or allowed_to_do is 0, selected_actions=0 on non-forced rows. Relocate is removed, not priced.
- `candidate_cost_feeds_action_selection` — **SURVIVED**. Destinations remain lexicographic over empty neighbors. Shadow cost is logged after the fact. wanted-axis cost does not change destination choice.

## Notes
- Do not treat binary occupancy veto as a discovered cost functional. It is the frozen policy.
- Additive shadow cost is a restatement of occupancy; it loses to the veto rule because wanted-axis deficits are priced but not gated.
- Runtime-burden mapping is unresolved; hierarchical coupling remains blocked until comparable coupling observables exist.
