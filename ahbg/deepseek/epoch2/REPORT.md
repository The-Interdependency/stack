# DeepCode AHBG calibration — second epoch report

## Interpretation experiment (decisive)
- Scenarios where shadow-only and veto-gating decision sequences differ: 8/35
- Delta ids: ['gradient_allowed_to_be', 'gradient_allowed_to_do', 'local_action_hostility', 'cracked_foundation', 'combined_hostility', 'repeated_hostility', 'sudden_hostility', 'label_permuted_control']
- Load-bearing: True

## Resolution proposed from the protocol text
- CALIBRATION.md requires hard vetoes to *remove actions rather than price them*
  and separately requires the candidate *cost model* not to alter first-epoch decisions.
- The `forbidden != expensive` distinction resolves the tension: hard veto is a
  permission denial (embodiment state) and gates; soft costs and other cost
  channels are the candidate cost model and remain shadow-only in the first epoch.
- DeepCode adopts this reading for epoch 2; it is recorded as a proposal, not a vote.

## Second epoch (candidate model active)
- Soft-cost gating changes decisions on: ['soft_cost_move']
- Held-out seed stability: 35/35 scenarios

## Evidence standing
- Hard-veto gating: SURVIVED (removes actions, never prices them)
- Soft-cost gating: SURVIVED (changes decisions when allowed to act)
- Interpretation resolution: SURVIVED (proposed from source text)
- Resource-burden mapping: BLOCKED (deterministic sandbox cannot measure token/tool/retry burden)

## hmmm
- Whether source authority confirms the veto/reading disambiguation.
- Whether the other two builders adopt the same resolution.
- Live-provider epoch required to map cost channels to measured runtime burden.
