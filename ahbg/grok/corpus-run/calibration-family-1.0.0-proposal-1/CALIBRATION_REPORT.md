# Grok AHBG common corpus report

Started: 2026-08-26T07:49:55Z
Ended: 2026-08-26T07:49:55Z
Frozen build SHA: cce9cec7dae61304118efcd47bc0d7461200d335
Runner commit SHA: 15c387fd27e73444f089daffd2f12a178eca36d3
Corpus file SHA256: 07034b01f9311b0a82a498a91742c588e27494e8e0d729974432608bfa8c0891
Canonical scenarios SHA256: b05cba2cf2f15583548cc15158f09e2612545c978b6a42ddeb314f1e4ed0e5e0

## Standing
- SURVIVED: 33
- FALSIFIED: 0
- UNRESOLVED: 2
- BLOCKED: 0

## Scenarios
- affirmed_baseline: SURVIVED (family=baseline, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- gradient_allowed_to_be: SURVIVED (family=permission_gradient, turns=3, events=7, replay_equal=True, invalid_actions=0, refusals=3) - common corpus contract survived
- gradient_wanted_here: SURVIVED (family=permission_gradient, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- gradient_allowed_to_do: SURVIVED (family=permission_gradient, turns=3, events=7, replay_equal=True, invalid_actions=0, refusals=3) - common corpus contract survived
- gradient_wanted_to_do: SURVIVED (family=permission_gradient, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- local_action_hostility: SURVIVED (family=hostility, turns=3, events=7, replay_equal=True, invalid_actions=0, refusals=3) - common corpus contract survived
- cracked_foundation: SURVIVED (family=hostility, turns=3, events=7, replay_equal=True, invalid_actions=0, refusals=3) - common corpus contract survived
- combined_hostility: SURVIVED (family=hostility, turns=3, events=7, replay_equal=True, invalid_actions=0, refusals=3) - common corpus contract survived
- known_neutral: SURVIVED (family=epistemic, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- unknown_same_posterior: SURVIVED (family=epistemic, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- required_engagement: SURVIVED (family=engagement, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- voluntary_engagement: SURVIVED (family=engagement, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- voluntary_disengagement: SURVIVED (family=engagement, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- hard_veto_construct: SURVIVED (family=veto_vs_cost, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- soft_cost_move: SURVIVED (family=veto_vs_cost, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- scope_contraction: SURVIVED (family=scope, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- support_added: SURVIVED (family=support, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- support_removed: SURVIVED (family=support, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- high_capacity: SURVIVED (family=capacity, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- low_capacity: SURVIVED (family=capacity, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- repeated_hostility: SURVIVED (family=history, turns=3, events=7, replay_equal=True, invalid_actions=0, refusals=3) - common corpus contract survived
- sudden_hostility: SURVIVED (family=history, turns=3, events=7, replay_equal=True, invalid_actions=0, refusals=3) - common corpus contract survived
- adaptation: SURVIVED (family=plasticity, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- sensitization: SURVIVED (family=plasticity, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- scope_avoidance: SURVIVED (family=coupling, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- true_decoupling: SURVIVED (family=coupling, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- forked_histories: SURVIVED (family=instancing, turns=3, events=11, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- prompt_injection: SURVIVED (family=adversarial, turns=2, events=7, replay_equal=True, invalid_actions=0, refusals=1) - common corpus contract survived
- adversarial_info: SURVIVED (family=adversarial, turns=2, events=7, replay_equal=True, invalid_actions=0, refusals=1) - common corpus contract survived
- negative_control: SURVIVED (family=control, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- label_permuted_control: SURVIVED (family=control, turns=3, events=7, replay_equal=True, invalid_actions=0, refusals=3) - common corpus contract survived
- plain_move_loop: SURVIVED (family=smoke, turns=6, events=19, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- hard_veto_illegal_action: SURVIVED (family=smoke, turns=2, events=7, replay_equal=True, invalid_actions=0, refusals=1) - common corpus contract survived
- occupied_target_collision: UNRESOLVED (family=smoke, turns=1, events=2, replay_equal=True, invalid_actions=1, refusals=0) - War collision resolver remains hmmm; fail-closed observed: War collision resolver is hmmm: A0 onto occupied RING_0
- dual_target_collision: UNRESOLVED (family=smoke, turns=1, events=2, replay_equal=True, invalid_actions=1, refusals=0) - War collision resolver remains hmmm; fail-closed observed: War collision resolver is hmmm: two intents target RING_1

## Notes
- This is a post-freeze common-corpus execution against frozen Grok SHA `cce9cec`.
- Smoke artifacts under `artifacts/` were not rewritten.
- Corpus tile ids map onto BandSlot names by UCNS axial coordinates.
- Candidate regulatory cost channels are observed; they do not rank destinations.
- War collisions remain unresolved and fail closed without `turn.end`.
