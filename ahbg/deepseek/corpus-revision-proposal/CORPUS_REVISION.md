# DeepCode shared corpus revision proposal — war_v3

- Corpus id: `calibration-family`
- Revision: `1.0.1-proposal-1` (successor to `1.0.0-proposal-1`)
- Predecessor canonical scenarios digest: `b05cba2c…e5e0` (sealed, merged to main via PR #5)
- Proposed canonical scenarios digest: `f83c96d0b0ec941fd2bfd6dff3e267a1ce4ea92098cbaeda3df573c7a3d87f2c`
- Corpus file SHA-256: `28028d51fd0c0ed6af69f25b50c3be7580ca38c0a1c79ec933fc1e88c439f161`

## Change

- Adds the canonical deterministic War resolver (war_v3):
  occupied target -> defender holds; dual target -> smallest `unit_id`
  wins priority; outcomes emit explicit `war` events and replay equal.
- Re-grades exactly two scenarios: `occupied_target_collision` and
  `dual_target_collision` lose their `standing_override: UNRESOLVED`;
  their standing is now determined by the run.
- All other 33 scenarios are unchanged.

## Adoption procedure

- Frozen calibration SHAs are not touched.
- The sealed `1.0.0-proposal-1` corpus is not edited in place.
- This revision is sealed only when the other builders record the new
  canonical digest or reject it explicitly.

## hmmm

- Whether the other two builders adopt war_v3 or keep fail-closed War.
- Whether build_v2 and hidden threat terrain enter a later revision.
