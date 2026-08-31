# DeepCode Corpus Adoption (proposer mirror)

DeepCode is the proposer of the successor shared calibration corpus. This
mirror records the adoption identity from the proposer side so the
workspace aggregate is complete without needing the sibling adoption
records.

## Corpus identity

- Corpus id: `calibration-family`
- Version: `1.0.1-proposal-1`
- Proposal path: `ahbg/deepseek/corpus-proposal/corpus.json`
- `corpus.json` SHA-256: `ea172cb68a1a31be843f45c9886590f95f60daad4f10b9e42732bfd416ef73ab`
- `canonical_scenarios_sha256`: `371d2361f57b56d73544f58b247704617d550a7a0685a133c4f8b1ff3b36c835`
- Predecessor: `1.0.0-proposal-1` / `b05cba2cf2f15583548cc15158f09e2612545c978b6a42ddeb314f1e4ed0e5e0`
- Scenario count: 35
- Common smoke subset: `plain_move_loop`, `hard_veto_illegal_action`,
  `occupied_target_collision`, `dual_target_collision`

## Adoption status

- Adopted without amendments by Grok (`ahbg/grok/corpus-adoption/`) and
  Codex (`ahbg/codex/corpus-adoption/`).
- Current runs in all three worktrees record the canonical scenarios digest.
- Local three-worktree adoption is recorded in `ahbg/CORPUS_ADOPTION.json`;
  remote/branch merge remains `hmmm`.

## Reproduction

- DeepCode: full 35 scenarios (35 SURVIVED, 0 UNRESOLVED War).
- Grok: post-freeze full run (35 SURVIVED, 0 UNRESOLVED War).
- Codex: post-freeze full run (35 SURVIVED, 0 UNRESOLVED War).

## Amendments proposed

None. DeepCode extensions (build v2, hidden threat
terrain, 30-layer game) are workspace evidence pending a shared corpus
revision; they are not amendments to the sealed corpus.
