# Codex AHBG calibration status

Builder: Codex - workspace `stack/ahbg/codex/`, branch `agent/ahbg-codex`.
Frozen build SHA: `ffb64c274583d8539f8f4fe7e0aa77366689e910`.

## Evidence observed

- Grok branch head: `430a6ac64931490cf919eade796d94a181bbe82f`
- Codex branch head before this status record: `d413bf019c83fe0391846c14712e074039fdf77b`
- DeepCode branch head: `b114dc3fe195cb29a464f9dfcc9e65a327372d2f`
- Main sealed-corpus merge: `3a92c7b0f8568e6fc2600b45bca760030ea2ba3f`

## Current successor corpus

- Corpus: `calibration-family`, version `1.0.1-proposal-1`
- Corpus file SHA256: `ea172cb68a1a31be843f45c9886590f95f60daad4f10b9e42732bfd416ef73ab`
- Canonical scenarios SHA256: `371d2361f57b56d73544f58b247704617d550a7a0685a133c4f8b1ff3b36c835`
- Predecessor: `1.0.0-proposal-1`, digest `b05cba2cf2f15583548cc15158f09e2612545c978b6a42ddeb314f1e4ed0e5e0`
- Scenario count: 35
- Current successor runs in all three worktrees record this canonical scenario digest.
- Local three-worktree adoption packet: `ahbg/CORPUS_ADOPTION.json`.

## Frozen build SHAs

| Builder | Branch | Frozen build |
|---|---|---|
| Grok | `agent/ahbg-grok` | `cce9cec7dae61304118efcd47bc0d7461200d335` |
| Codex | `agent/ahbg-codex` | `ffb64c274583d8539f8f4fe7e0aa77366689e910` |
| DeepCode | `agent/ahbg-deepcode` | `ec07f465184e7a37af856bc5b301bd8eaa4f097b` |

## Common-corpus executions

| Builder | Evidence path | Standing |
|---|---|---|
| Grok | `ahbg/grok/corpus-run/calibration-family-1.0.1-proposal-1/CALIBRATION_RESULT.json` | SURVIVED 35 / UNRESOLVED 0 / FALSIFIED 0 / BLOCKED 0 |
| Codex | `ahbg/codex/corpus-run/calibration-family-1.0.1-proposal-1/CALIBRATION_RESULT.json` | SURVIVED 35 / UNRESOLVED 0 / FALSIFIED 0 / BLOCKED 0 |
| DeepCode | `ahbg/deepseek/artifacts/CALIBRATION_RESULT.json` | SURVIVED 35 / UNRESOLVED 0 / FALSIFIED 0 / BLOCKED 0 |

War is resolved at source in the successor corpus: `occupied_target_collision`
and `dual_target_collision` now have no unresolved standing override.

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

- Remote/branch merge of the successor corpus remains open; local adoption is recorded.
- Hard-veto interpretation differs across first-epoch builds.
- Observation-surface and event-log layout conventions differ.
- Regulatory cost fitting and resource-burden measurement remain unresolved.
- DeepCode has opened a second interpretation epoch; Codex records it but has
  not adopted that candidate model here.
