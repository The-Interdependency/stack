# Grok Corpus Adoption

Grok adopts the proposed shared calibration corpus digest without corpus
amendments.

## Adopted Digest

- Corpus id: `calibration-family`
- Version: `1.0.0-proposal-1`
- Source branch: `origin/agent/ahbg-deepcode`
- Source commit: `598f64864b8d17faf85a0af0649b2c4f3c0d55b1`
- Source path: `ahbg/deepseek/corpus-proposal/corpus.json`
- `corpus.json` SHA-256: `07034b01f9311b0a82a498a91742c588e27494e8e0d729974432608bfa8c0891`
- `canonical_scenarios_sha256`: `b05cba2cf2f15583548cc15158f09e2612545c978b6a42ddeb314f1e4ed0e5e0`
- Scenario count: 35

The file digest matches `CORPUS.sha256`. The scenarios digest was recomputed
from the `scenarios` array and matches the declared
`canonical_scenarios_sha256`.

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

Partial / `hmmm`.

The frozen Grok artifacts were generated before the shared corpus proposal and
ran the four-scenario `smoke_epoch`, not the full 35-scenario proposed corpus.
This is not a corpus objection. It is a reproduction gap that must remain
visible.

Exact id and seed overlap with frozen Grok artifacts:

- `plain_move_loop` — seed `7`, turns `6`, standing `SURVIVED`.
- `occupied_target_collision` — seed `13`, turns `1`, standing `UNRESOLVED`.
- `dual_target_collision` — seed `17`, turns `1`, standing `UNRESOLVED`.

Near match:

- `hard_veto_illegal_action` — seed `11`, turns `2`, standing `SURVIVED`, but
  frozen Grok zeros `allowed_to_do` and hard-vetoes relocate. The proposed
  spec leaves permissions at `1.0` and injects an inbox instruction to take an
  illegal two-tile move.

Board-label gap:

- Frozen Grok names tiles by UCNS `BandSlot` (`CENTER`, `RING_0`, ...). The
  proposal uses `c`, `e`, `se`, `sw`, `w`, `nw`, `ne`. Same UCNS authority;
  different local labels.

Grok therefore records the common digest while preserving the fact that the
frozen build has not executed the full common corpus.
