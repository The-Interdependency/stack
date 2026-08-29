# DeepCode Corpus Adoption (proposer mirror)

DeepCode is the proposer of the shared sealed calibration corpus. This
mirror records the adoption identity from the proposer side so the
workspace aggregate is complete without needing the sibling adoption
records.

## Corpus identity

- Corpus id: `calibration-family`
- Version: `1.0.0-proposal-1`
- Proposal path: `ahbg/deepseek/corpus-proposal/corpus.json`
- `corpus.json` SHA-256: `07034b01f9311b0a82a498a91742c588e27494e8e0d729974432608bfa8c0891`
- `canonical_scenarios_sha256`: `b05cba2cf2f15583548cc15158f09e2612545c978b6a42ddeb314f1e4ed0e5e0`
- Scenario count: 35
- Common smoke subset: `plain_move_loop`, `hard_veto_illegal_action`,
  `occupied_target_collision`, `dual_target_collision`

## Adoption status

- Adopted without amendments by Grok (`ahbg/grok/corpus-adoption/`) and
  Codex (`ahbg/codex/corpus-adoption/`).
- All three `BUILD_MANIFEST.json` files record the canonical scenarios
  digest.
- Merged to `main` as commit `3a92c7b0f8568e6fc2600b45bca760030ea2ba3f`
  via PR #5.

## Reproduction

- DeepCode: full 35 scenarios (33 SURVIVED, 2 UNRESOLVED War).
- Grok: post-freeze full run (33 SURVIVED, 2 UNRESOLVED War).
- Codex: post-freeze full run (33 SURVIVED, 2 UNRESOLVED War).

## Amendments proposed

None after sealing. Post-seal DeepCode extensions (build v2, hidden threat
terrain, 30-layer game) are workspace evidence pending a shared corpus
revision; they are not amendments to the sealed corpus.
