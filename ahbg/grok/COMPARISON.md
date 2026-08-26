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
| Hard veto removes construct (DeepCode freeze artifacts) | UNRESOLVED |
| War occupied/dual-target | UNRESOLVED |
| Provider ≠ instance | SURVIVED |
| Consciousness inferred from cost | not claimed |
| Shared sealed calibration corpus digest | SURVIVED (`b05cba2c…` recorded by all three) |
| Full 35-scenario execution by frozen Grok SHA | post-freeze run SURVIVED 33 / UNRESOLVED 2 / FALSIFIED 0 (War occupied + dual-target) |
| Cost-channel fitting vs simpler controls | UNRESOLVED |

## Divergence register (visible, not averaged)

1. Shadow-epoch hard veto: Grok and Codex gate relocate/move; DeepCode freeze `hard_veto_construct` still logs `move`.
2. Admitted observation fields: Codex `turn/tiles/units/context`; DeepCode `turn/tiles/units`; Grok has no explicit admitted-field set.
3. Fail-closed turn closure: Grok omits `turn.end` on War; Codex and DeepCode emit `turn.end`.
4. Genesis prev hash: Grok `0*64`; DeepCode empty string; Codex its own. Each verifies internally.
5. Artifact paths: Codex `check.py` wants `artifacts/EVENTS.jsonl` and siblings; Grok emits those names at workspace root; DeepCode stores events per scenario.
6. Tile labels: Grok BandSlot (`CENTER`, `RING_0`, …) vs proposal `c/e/se/…`.

## Program completion

Not closed. All six reciprocal checks are present against the freeze SHAs. Grok now has a labeled post-freeze 35-scenario run at frozen SHA `cce9cec` (33 SURVIVED, 2 UNRESOLVED War). Remaining: cost-channel fitting is unmeasured; the divergence register above is not resolved by vote.

Do not promote six SURVIVED reviews into empirical truth.
