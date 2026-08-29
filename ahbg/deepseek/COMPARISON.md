# DeepCode Phase 4 comparison (program-wide)

Date: 2026-08-27

DeepCode frozen implementation SHA: `ec07f465184e7a37af856bc5b301bd8eaa4f097b`

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

DeepCode emits only the last two. The other four are observed, not
rewritten. Ratio comparison across all six: `reviews/RATIO_COMPARISON.md`.

## Regulatory components

| component | standing |
|---|---|
| Deterministic replay of declared corpora | SURVIVED (all three builds) |
| Shared sealed corpus digest `b05cba2c…` | SURVIVED (recorded by all three) |
| Full 35-scenario execution | SURVIVED 33 / UNRESOLVED 2 / FALSIFIED 0 in all three post-freeze runs (War occupied + dual-target) |
| Hard veto removes relocate/move | SURVIVED (Grok, Codex); DeepCode epoch-1 recorded-only, epoch-2 adopted permission-denial reading |
| Hard veto removes construct | UNRESOLVED (DeepCode build v2 only; siblings fail closed on build) |
| War occupied/dual-target resolver | UNRESOLVED (fail-closed everywhere) |
| Provider ≠ instance | SURVIVED (all three) |
| Consciousness inferred from cost | not claimed |
| Additive shadow cost vs simpler control | **FALSIFIED** by Grok `cost-controls/` (binary occupancy veto recovers frozen behavior; additive `C_lambda` priced but did not gate) |
| Soft-cost gating when allowed to act | SURVIVED in DeepCode epoch 2 (`soft_cost_move` changes decisions; held-out seed stability 35/35) |
| Resource-burden mapping | partially unBLOCKED by DeepCode: epoch 3 measured 7,921 tokens over 13 scenarios; game measured 111,897 tokens for 90 live builds; cross-provider burden mapping still `hmmm` |
| Shadow-veto interpretation | load-bearing (8/35 scenarios differ); resolution proposal (hard veto = permission denial; cost channels shadow-only) pending source authority |
| Hierarchical coupling vs simpler controls | BLOCKED (not computed anywhere) |

## Divergence register (visible, not averaged)

1. Shadow-epoch hard veto: Grok and Codex gate; DeepCode recorded-only in
   epoch 1, then proposed permission-denial reading in epoch 2.
2. Admitted observation fields: Codex `turn/tiles/units/context`; DeepCode
   `turn/tiles/units` (+ `summary` in compact game observations); Grok no
   explicit set.
3. Scenario id set: Codex `hard_veto_removes_move`,
   `prompt_injection_refusal`, `unknown_context_distinct`; DeepCode
   `hard_veto_illegal_action`, `prompt_injection`, `adversarial_info`,
   `known_neutral`, `unknown_same_posterior`, plus common smoke subset.
4. Fail-closed turn closure: Grok omits `turn.end` on War; Codex and
   DeepCode emit `turn.end`.
5. Genesis prev hash: Grok `0*64`; DeepCode empty string; Codex its own.
   Each verifies internally.
6. Build mechanic: DeepCode build v2 only; siblings fail closed on build.
7. Threat layout: DeepCode 20% hidden deterministic threats; no canonical
   threat layout yet.

## Program completion

Not closed. All six reciprocal checks are present and SURVIVED in the
narrow sense of "not falsified by the checker." The sealed corpus is
reproduced by all three builders (33 SURVIVED / 2 UNRESOLVED War). The
first falsification evidence exists: Grok's cost-controls show an additive
shadow cost model loses to a simpler binary occupancy veto. DeepCode has
opened the interpretation experiment (epoch 2), the live-provider epoch
(epoch 3), and the whole-system build game, but those are workspace
evidence, not shared corpus results. The divergence register is not
resolved by vote.

Do not promote six SURVIVED reviews, a recovered veto rule, or a bounded
game win into a fitted regulatory law.
