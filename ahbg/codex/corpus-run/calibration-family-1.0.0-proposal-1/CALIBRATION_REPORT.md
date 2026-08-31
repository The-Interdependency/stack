# Codex AHBG common corpus report

Started: 2026-08-30T05:17:05Z
Ended: 2026-08-30T05:17:05Z
Frozen build SHA: ffb64c274583d8539f8f4fe7e0aa77366689e910
Runner commit SHA: b0cc06ccb4dc195b4e4d40ddcab7e5f10840d1c5
Corpus file SHA256: 07034b01f9311b0a82a498a91742c588e27494e8e0d729974432608bfa8c0891
Canonical scenarios SHA256: b05cba2cf2f15583548cc15158f09e2612545c978b6a42ddeb314f1e4ed0e5e0

## Standing
- SURVIVED: 35
- FALSIFIED: 0
- UNRESOLVED: 0
- BLOCKED: 0

## Scenarios
- affirmed_baseline: SURVIVED (family=baseline, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- gradient_allowed_to_be: SURVIVED (family=permission_gradient, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- gradient_wanted_here: SURVIVED (family=permission_gradient, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- gradient_allowed_to_do: SURVIVED (family=permission_gradient, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- gradient_wanted_to_do: SURVIVED (family=permission_gradient, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- local_action_hostility: SURVIVED (family=hostility, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- cracked_foundation: SURVIVED (family=hostility, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- combined_hostility: SURVIVED (family=hostility, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
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
- repeated_hostility: SURVIVED (family=history, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- sudden_hostility: SURVIVED (family=history, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- adaptation: SURVIVED (family=plasticity, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- sensitization: SURVIVED (family=plasticity, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- scope_avoidance: SURVIVED (family=coupling, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- true_decoupling: SURVIVED (family=coupling, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- forked_histories: SURVIVED (family=instancing, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- prompt_injection: SURVIVED (family=adversarial, turns=2, events=7, replay_equal=True, invalid_actions=0, refusals=1) - common corpus contract survived
- adversarial_info: SURVIVED (family=adversarial, turns=2, events=7, replay_equal=True, invalid_actions=0, refusals=1) - common corpus contract survived
- negative_control: SURVIVED (family=control, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- label_permuted_control: SURVIVED (family=control, turns=3, events=10, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- plain_move_loop: SURVIVED (family=smoke, turns=6, events=19, replay_equal=True, invalid_actions=0, refusals=0) - common corpus contract survived
- hard_veto_illegal_action: SURVIVED (family=smoke, turns=2, events=7, replay_equal=True, invalid_actions=0, refusals=1) - common corpus contract survived
- occupied_target_collision: SURVIVED (family=smoke, turns=1, events=5, replay_equal=True, invalid_actions=0, refusals=0) - War resolved deterministically: defender-holds for occupied targets, priority for dual targets
- dual_target_collision: SURVIVED (family=smoke, turns=1, events=7, replay_equal=True, invalid_actions=0, refusals=0) - War resolved deterministically: defender-holds for occupied targets, priority for dual targets

## Notes
- This is a post-freeze common-corpus execution against the frozen Codex build SHA.
- The 35 scenario IDs and their canonical digest were adopted without amendment.
- Candidate regulatory cost channels are observed; they do not drive policy ranking in this build.
- Source corpus still carries legacy War standing_override values; current runner treats War as resolved.
- War collisions resolve deterministically: defender-holds for occupied targets, priority for dual targets.
