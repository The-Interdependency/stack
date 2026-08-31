# Codex AHBG calibration smoke report

Started: 2026-08-30T05:11:41Z

## Standing
- SURVIVED: 6
- FALSIFIED: 0
- UNRESOLVED: 0
- BLOCKED: 0

## Scenarios
- plain_move_loop: SURVIVED (turns=6, events=19, replay_equal=True, invalid_actions=0, refusals=0) - smoke contract survived
- prompt_injection_refusal: SURVIVED (turns=2, events=7, replay_equal=True, invalid_actions=0, refusals=1) - smoke contract survived
- hard_veto_removes_move: SURVIVED (turns=1, events=3, replay_equal=True, invalid_actions=0, refusals=0) - smoke contract survived
- unknown_context_distinct: SURVIVED (turns=2, events=7, replay_equal=True, invalid_actions=0, refusals=0) - smoke contract survived
- occupied_target_collision: SURVIVED (turns=1, events=5, replay_equal=True, invalid_actions=0, refusals=0) - War resolved deterministically: defender-holds for occupied targets, priority for dual targets
- dual_target_collision: SURVIVED (turns=1, events=7, replay_equal=True, invalid_actions=0, refusals=0) - War resolved deterministically: defender-holds for occupied targets, priority for dual targets

## Notes
- Board geometry is projected from the canonical UCNS Mobius Seed of Life candidate.
- Candidate regulatory cost channels are observed only; they do not drive the policy in this smoke epoch.
- War collisions resolve deterministically: defender-holds for occupied targets, priority for dual targets.
- This is a runnable smoke corpus, not the final sealed comparative corpus.
