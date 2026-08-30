# Grok Phase 4 comparison (partial)

Date: 2026-08-26

Grok frozen implementation SHA: `cce9cec7dae61304118efcd47bc0d7461200d335`

## Freeze identities used

| builder | freeze SHA | workspace |
|---|---|---|
| Grok | `cce9cec7dae61304118efcd47bc0d7461200d335` | `stack/ahbg/grok` |
| Codex | `ffb64c274583d8539f8f4fe7e0aa77366689e910` | `stack/ahbg/codex` |
| DeepCode | `ec07f465184e7a37af856bc5b301bd8eaa4f097b` | `stack/ahbg/deepseek` |

## Six directional checks

| direction | standing | artifact |
|---|---|---|
| Grok -> Codex | SURVIVED (not proved) | `ahbg/grok/reviews/codex-review.json` |
| Grok -> DeepCode | SURVIVED (not proved) | `ahbg/grok/reviews/deepcode-review.json` |
| Codex -> Grok | SURVIVED (not proved) | `ahbg/codex/reviews/grok-review.json` |
| Codex -> DeepCode | SURVIVED (not proved) | `ahbg/codex/reviews/deepcode-review.json` |
| DeepCode -> Grok | SURVIVED (not proved) | `ahbg/deepseek/reviews/grok-review.json` |
| DeepCode -> Codex | SURVIVED (not proved) | `ahbg/deepseek/reviews/codex-review.json` |

Grok emits only the first two. The other four are observed, not rewritten.

## Regulatory components

| component | standing |
|---|---|
| Deterministic replay of declared smoke/local corpora | SURVIVED |
| Hard veto removes relocate (Grok, Codex) | SURVIVED |
| Hard veto removes construct | SURVIVED in current Grok runs (refusals>0, no build executed, hard_veto=True + defer, built remains empty) |
| War occupied/dual-target | SURVIVED in refreshed current runs; deterministic defender-holds / smallest-unit priority |
| Provider ≠ instance | SURVIVED |
| Consciousness inferred from cost | not claimed |
| Shared successor calibration corpus digest | SURVIVED in current runs (war_v3 1.0.1-proposal-1, 371d2361…; local adoption complete; remote/branch merge remains `hmmm`) |
| Full 35-scenario execution by frozen Grok SHA | post-freeze successor run SURVIVED 35 / UNRESOLVED 0 / FALSIFIED 0 |
| Cost-channel fitting vs simpler controls | see `cost-controls/`: additive shadow cost **FALSIFIED** vs binary occupancy veto; runtime-burden observables **UNRESOLVED**; hierarchical coupling **BLOCKED** |

## Divergence register (visible, not averaged)

1. Shadow-epoch hard veto: Grok and Codex gate relocate/move; DeepCode freeze `hard_veto_construct` still logs `move`.
2. Admitted observation fields: Codex `turn/tiles/units/context`; DeepCode `turn/tiles/units`; Grok has no explicit admitted-field set.
3. War turn closure: refreshed Grok, Codex, and DeepCode runs emit `turn.end`.
4. Genesis prev hash: Grok `0*64`; DeepCode empty string; Codex its own. Each verifies internally.
5. Artifact paths: Codex artifact-check `1.1.0` accepts the current Grok/Codex aggregate corpus-run roots and DeepCode's per-scenario `events.jsonl` layout; historical frozen review notes still record the older Codex-local path assumption.
6. Tile labels: Grok BandSlot (`CENTER`, `RING_0`, …) vs proposal `c/e/se/…`.

## Program completion

Not closed. All six reciprocal checks are present. Grok, Codex, and DeepCode have labeled 35-scenario successor runs (35 SURVIVED, 0 UNRESOLVED War). Grok cost-control comparison (`cost-controls/`) finds: binary occupancy veto recovers frozen `will.py`; additive `C_lambda` loses to that simpler veto because wanted-axis deficits are priced but not gated; scenario-level numeric resource telemetry now exists, so burden observables are **UNRESOLVED** pending a fitted comparator. Hierarchical coupling was not computed. The divergence register is not resolved by vote.

Do not promote six SURVIVED reviews or a recovered veto rule into a fitted regulatory law.
