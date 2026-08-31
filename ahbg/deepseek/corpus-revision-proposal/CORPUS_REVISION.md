# DeepCode shared corpus revision proposal — war_v3

- Corpus id: `calibration-family`
- Revision: `1.0.1-proposal-1` (successor to `1.0.0-proposal-1`)
- Predecessor canonical scenarios digest: `b05cba2c…e5e0` (sealed, merged to main via PR #5)
- Proposed canonical scenarios digest: `371d2361f57b56d73544f58b247704617d550a7a0685a133c4f8b1ff3b36c835`
- Corpus file SHA-256: `15dff076460ccd297b96843dcfa30c38de6d39f6ca725d65a7b1af6a8e54ea24`

## Change

- Adds the canonical deterministic War resolver (war_v3):
  occupied target -> defender holds; dual target -> smallest `unit_id`
  wins priority; outcomes emit explicit `war` events and replay equal.
- Re-grades exactly two scenarios: `occupied_target_collision` and
  `dual_target_collision` set `standing_override` to null;
  their standing is now determined by the run.
- All other 33 scenarios are unchanged.

## Adoption procedure

- Frozen calibration SHAs are not touched.
- The sealed `1.0.0-proposal-1` corpus is not edited in place.
- This revision is sealed only when the other builders record the new
  canonical digest or reject it explicitly.

## hmmm

- Refreshed Grok/Codex current runs adopt war_v3; local successor adoption is recorded.
- Remote/branch merge of the successor corpus remains open.
- Whether build_v2 and hidden threat terrain enter a later revision.
