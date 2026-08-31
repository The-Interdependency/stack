# Codex Corpus Adoption

Codex adopts the successor proposed shared calibration corpus digest without corpus
amendments.

## Adopted Digest

- Corpus id: `calibration-family`
- Version: `1.0.1-proposal-1`
- Source branch: local `stack-deepcode` worktree
- Source commit: `90b66e39d8527cd1adc8c69391f64253e5a0ab94`
- Source path: `/home/wayseer_interdependentway_org/src/stack-deepcode/ahbg/deepseek/corpus-proposal/corpus.json`
- `corpus.json` SHA-256: `ea172cb68a1a31be843f45c9886590f95f60daad4f10b9e42732bfd416ef73ab`
- `canonical_scenarios_sha256`: `371d2361f57b56d73544f58b247704617d550a7a0685a133c4f8b1ff3b36c835`
- Predecessor: `1.0.0-proposal-1` / `b05cba2cf2f15583548cc15158f09e2612545c978b6a42ddeb314f1e4ed0e5e0`
- Scenario count: 35

## Frozen Build

Codex frozen implementation SHA:

```text
ffb64c274583d8539f8f4fe7e0aa77366689e910
```

The current metadata head at the time of this adoption record was:
`43fdbd6120416b54bb26c52fa34c384956534257`.

## Amendments

None. Codex does not propose edits to the shared corpus.

## Reproduction Standing

Complete as a post-freeze run.

The original frozen Codex artifacts were generated before the shared corpus
proposal and ran `codex_smoke_epoch/1.0.0`. Codex later added an explicitly
labeled common-corpus runner and executed all 35 scenarios against the frozen
implementation identity.

- Runner commit: `3b3e67adff14effaf0426a02004aa68a48753b9f`
- Run record commit: `029f15005c655b9fea53253d0d1cd7f421d6af39`
- Result path: `stack/ahbg/codex/corpus-run/calibration-family-1.0.1-proposal-1/CALIBRATION_RESULT.json`
- Summary: SURVIVED 35 / UNRESOLVED 0 / FALSIFIED 0 / BLOCKED 0
- UNRESOLVED ids: none

This does not rewrite the frozen smoke artifacts or change the frozen Codex
build SHA.

Exact id overlap with frozen Codex artifacts:

- `plain_move_loop` — standing matches; seed differs (`7` proposed, `101`
  frozen Codex smoke).
- `occupied_target_collision` — successor corpus resolves War with
  defender-holds; seed differs (`13` proposed, `105` frozen Codex smoke).
- `dual_target_collision` — successor corpus resolves War by smallest
  `unit_id` priority; seed differs (`17` proposed, `106` frozen Codex smoke).

Near matches:

- `prompt_injection_refusal` maps to the intent of `hard_veto_illegal_action`,
  but the id and seed differ.
- `hard_veto_removes_move` maps to the hard-veto principle, but the proposed
  corpus uses `hard_veto_construct`.
- `unknown_context_distinct` maps to the unknown-not-neutral principle, but not
  the proposed `unknown_same_posterior` schema.

Codex therefore records the successor common digest and the later full execution while
preserving the fact that the initial frozen artifact set was a smaller smoke
corpus.
