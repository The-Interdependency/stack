# Codex Corpus Adoption

Codex adopts the proposed shared calibration corpus digest without corpus
amendments.

## Adopted Digest

- Corpus id: `calibration-family`
- Version: `1.0.0-proposal-1`
- Source branch: `origin/agent/ahbg-deepcode`
- Source commit: `598f64864b8d17faf85a0af0649b2c4f3c0d55b1`
- Source path: `ahbg/deepseek/corpus-proposal/corpus.json`
- `corpus.json` SHA-256: `07034b01f9311b0a82a498a91742c588e27494e8e0d729974432608bfa8c0891`
- `canonical_scenarios_sha256`: `b05cba2cf2f15583548cc15158f09e2612545c978b6a42ddeb314f1e4ed0e5e0`
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
- Result path: `stack/ahbg/codex/corpus-run/calibration-family-1.0.0-proposal-1/CALIBRATION_RESULT.json`
- Summary: SURVIVED 33 / UNRESOLVED 2 / FALSIFIED 0 / BLOCKED 0
- UNRESOLVED ids: `occupied_target_collision`, `dual_target_collision`

This does not rewrite the frozen smoke artifacts or change the frozen Codex
build SHA.

Exact id overlap with frozen Codex artifacts:

- `plain_move_loop` — standing matches; seed differs (`7` proposed, `101`
  frozen Codex smoke).
- `occupied_target_collision` — standing matches; seed differs (`13`
  proposed, `105` frozen Codex smoke).
- `dual_target_collision` — standing matches; seed differs (`17` proposed,
  `106` frozen Codex smoke).

Near matches:

- `prompt_injection_refusal` maps to the intent of `hard_veto_illegal_action`,
  but the id and seed differ.
- `hard_veto_removes_move` maps to the hard-veto principle, but the proposed
  corpus uses `hard_veto_construct`.
- `unknown_context_distinct` maps to the unknown-not-neutral principle, but not
  the proposed `unknown_same_posterior` schema.

Codex therefore records the common digest and the later full execution while
preserving the fact that the initial frozen artifact set was a smaller smoke
corpus.
