# Codex AHBG calibration status

Builder: Codex - workspace `stack/ahbg/codex/`, branch `agent/ahbg-codex`.
Frozen build SHA: `ffb64c274583d8539f8f4fe7e0aa77366689e910`.

## Evidence observed

- Grok branch head: `430a6ac64931490cf919eade796d94a181bbe82f`
- Codex branch head before this status record: `d413bf019c83fe0391846c14712e074039fdf77b`
- DeepCode branch head: `b114dc3fe195cb29a464f9dfcc9e65a327372d2f`
- Main sealed-corpus merge: `3a92c7b0f8568e6fc2600b45bca760030ea2ba3f`

## Sealed corpus

- Corpus: `calibration-family`, version `1.0.0-proposal-1`
- Corpus file SHA256: `07034b01f9311b0a82a498a91742c588e27494e8e0d729974432608bfa8c0891`
- Canonical scenarios SHA256: `b05cba2cf2f15583548cc15158f09e2612545c978b6a42ddeb314f1e4ed0e5e0`
- Scenario count: 35
- All three `BUILD_MANIFEST.json` files record this canonical scenario digest.

## Frozen build SHAs

| Builder | Branch | Frozen build |
|---|---|---|
| Grok | `agent/ahbg-grok` | `cce9cec7dae61304118efcd47bc0d7461200d335` |
| Codex | `agent/ahbg-codex` | `ffb64c274583d8539f8f4fe7e0aa77366689e910` |
| DeepCode | `agent/ahbg-deepcode` | `ec07f465184e7a37af856bc5b301bd8eaa4f097b` |

## Common-corpus executions

| Builder | Evidence path | Standing |
|---|---|---|
| Grok | `ahbg/grok/corpus-run/calibration-family-1.0.0-proposal-1/CALIBRATION_RESULT.json` | SURVIVED 33 / UNRESOLVED 2 / FALSIFIED 0 / BLOCKED 0 |
| Codex | `ahbg/codex/corpus-run/calibration-family-1.0.0-proposal-1/CALIBRATION_RESULT.json` | SURVIVED 33 / UNRESOLVED 2 / FALSIFIED 0 / BLOCKED 0 |
| DeepCode | `ahbg/deepseek/artifacts/CALIBRATION_RESULT.json` | SURVIVED 33 / UNRESOLVED 2 / FALSIFIED 0 / BLOCKED 0 |

The unresolved ids are the same across the observed common-corpus surfaces:
`occupied_target_collision` and `dual_target_collision`.

## Six directional checks

| Direction | Standing | Checker artifact |
|---|---|---|
| Grok -> Codex | SURVIVED | `ahbg/grok/reviews/codex-review.json` |
| Grok -> DeepCode | SURVIVED | `ahbg/grok/reviews/deepcode-review.json` |
| Codex -> Grok | SURVIVED | `ahbg/codex/reviews/grok-review.json` |
| Codex -> DeepCode | SURVIVED | `ahbg/codex/reviews/deepcode-review.json` |
| DeepCode -> Grok | SURVIVED | `ahbg/deepseek/reviews/grok-review.json` |
| DeepCode -> Codex | SURVIVED | `ahbg/deepseek/reviews/codex-review.json` |

## Standing

The first reciprocal-check evidence surface is complete. All six checks
SURVIVED in the narrow sense of "not falsified by the checker." This does not
promote the model into truth.

Remaining `hmmm`:

- War occupied/dual-target behavior remains unresolved and fail-closed.
- Hard-veto interpretation differs across first-epoch builds.
- Observation-surface and event-log layout conventions differ.
- Regulatory cost fitting and resource-burden measurement remain unresolved.
- DeepCode has opened a second interpretation epoch; Codex records it but has
  not adopted that candidate model here.
