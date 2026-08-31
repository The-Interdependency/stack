# AHBG Successor Corpus Adoption

Recorded: `2026-08-30T07:19:36Z`

This packet records local three-worktree adoption of the successor calibration
corpus. It does not claim a remote merge, branch merge, or release.

## Corpus

- Corpus id: `calibration-family`
- Version: `1.0.1-proposal-1`
- Proposer: DeepCode
- Source path: `/home/wayseer_interdependentway_org/src/stack-deepcode/ahbg/deepseek/corpus-proposal/corpus.json`
- `corpus.json` SHA-256: `ea172cb68a1a31be843f45c9886590f95f60daad4f10b9e42732bfd416ef73ab`
- `canonical_scenarios_sha256`: `371d2361f57b56d73544f58b247704617d550a7a0685a133c4f8b1ff3b36c835`
- Predecessor: `1.0.0-proposal-1`
- Scenario count: 35

## Adoption Evidence

| Builder | Decision | Run standing | Artifact layout |
|---|---|---|---|
| Grok | adopted without amendments | 35 SURVIVED / 0 UNRESOLVED / 0 FALSIFIED / 0 BLOCKED | `corpus-run/calibration-family-1.0.1-proposal-1:aggregate-events` |
| Codex | adopted without amendments | 35 SURVIVED / 0 UNRESOLVED / 0 FALSIFIED / 0 BLOCKED | `corpus-run/calibration-family-1.0.1-proposal-1:aggregate-events` |
| DeepCode | proposer mirror, no amendments | 35 SURVIVED / 0 UNRESOLVED / 0 FALSIFIED / 0 BLOCKED | `artifacts:per-scenario-events` |

The Codex artifact checker `interdependency.ahbg.codex.artifact-check/1.1.0`
validated all three artifact roots after artifact-layout normalization.

## Boundary

Local adoption is complete for the three current worktrees. Formal upstream
merge, branch deletion, release tagging, and any change of canonical repository
authority remain outside this packet.

## hmmm

- Remote GitHub/PR merge state was not changed.
- Historical reciprocal-review files still preserve earlier path assumptions.
- DeepCode-only extensions remain outside this adopted shared corpus.
