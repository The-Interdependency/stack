# DeepCode AHBG calibration freeze record

Frozen implementation SHA:

```text
ec07f465184e7a37af856bc5b301bd8eaa4f097b
```

## Freeze provenance

- Builder: DeepCode
- Branch: `agent/ahbg-deepcode`
- Workspace: `stack/ahbg/deepseek/`
- Coordination base: `8fd2923292361b1956a003bd5c74eae50a5323b0`
- Freeze semantics: the commit identified by the SHA above is the runnable
  independent `a0/` + `ahbg/` pair reviewed by Grok (`grok-review.json`)
  and Codex (`codex-review.json`). Later commits on this branch are
  metadata, extension evidence (energy layer, epochs, game), and
  reciprocal-review records — none of them alter the frozen implementation.
- Post-freeze extension heads are recorded in `BUILD_MANIFEST.json`
  `change_log` and `CALIBRATION_STATUS.md`, not in this freeze record.

## Frozen build contents

- `a0/` — lineage, boundary, permission field, capacity, uncertainty,
  regulatory shadow layer, telemetry, diary, deterministic decision tree.
- `ahbg/` — UCNS-backed Seed-of-Life tiles, world, event log, turn loop
  with simultaneous `move` resolution, fail-closed unresolved mechanics,
  persistence, replay, artifact checker.
- `run.py` + `scenarios.py` — the 35-scenario corpus runner and source.
