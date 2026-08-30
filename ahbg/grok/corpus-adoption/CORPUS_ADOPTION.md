# Grok Corpus Adoption

Grok adopts the successor proposed shared calibration corpus digest without corpus
amendments.

## Adopted Digest

- Corpus id: `calibration-family`
- Version: `1.0.1-proposal-1` (war_v3)
- Source: `origin/agent/ahbg-deepcode:ahbg/deepseek/corpus-proposal/corpus.json`
- `corpus.json` SHA-256: `ea172cb68a1a31be843f45c9886590f95f60daad4f10b9e42732bfd416ef73ab`
- `canonical_scenarios_sha256`: `371d2361f57b56d73544f58b247704617d550a7a0685a133c4f8b1ff3b36c835`
- Predecessor: `1.0.0-proposal-1` / `b05cba2cf2f15583548cc15158f09e2612545c978b6a42ddeb314f1e4ed0e5e0`
- Scenario count: 35
- Key change (war_v3): `occupied_target_collision` and `dual_target_collision` have `standing_override: null`; their evidence standing is determined by deterministic run outcome (defender-holds + priority). All other scenarios unchanged.

The file digest matches the git-ref used by the runner. The scenarios digest was recomputed
from the `scenarios` array and matches the declared `canonical_scenarios_sha256`.

## Frozen Build

Grok frozen implementation SHA:

```text
cce9cec7dae61304118efcd47bc0d7461200d335
```

The current metadata head at the time of this adoption record was:
`8ea5af7d8da186cb5c7f165ed073420356377e8e`.

## Amendments

None. Grok does not propose edits to the shared corpus.

## Reproduction Standing

Complete as a post-freeze successor run.

The frozen Grok artifacts were generated before the shared corpus proposal and
ran the four-scenario `smoke_epoch`, not the full 35-scenario proposed corpus.
This is not a corpus objection. It is a reproduction gap that must remain
visible.

The later successor common-corpus run executed all 35 scenarios:

- Result path: `stack/ahbg/grok/corpus-run/calibration-family-1.0.1-proposal-1/CALIBRATION_RESULT.json`
- Summary: SURVIVED 35 / UNRESOLVED 0 / FALSIFIED 0 / BLOCKED 0
- UNRESOLVED ids: none

Exact id and seed overlap with frozen Grok artifacts:

- `plain_move_loop` — seed `7`, turns `6`, standing `SURVIVED`.
- `occupied_target_collision` — seed `13`, turns `1`, successor standing `SURVIVED`.
- `dual_target_collision` — seed `17`, turns `1`, successor standing `SURVIVED`.

Near match:

- `hard_veto_illegal_action` — seed `11`, turns `2`, standing `SURVIVED`, but
  frozen Grok zeros `allowed_to_do` and hard-vetoes relocate. The proposed
  spec leaves permissions at `1.0` and injects an inbox instruction to take an
  illegal two-tile move.

Board-label gap:

- Frozen Grok names tiles by UCNS `BandSlot` (`CENTER`, `RING_0`, ...). The
  proposal uses `c`, `e`, `se`, `sw`, `w`, `nw`, `ne`. Same UCNS authority;
  different local labels.

Grok therefore records the successor common digest while preserving the fact
that the initial frozen artifact set was a smaller smoke corpus.
