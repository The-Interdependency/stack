# DeepCode calibration workspace

Builder: **DeepCode**  
Branch: `agent/ahbg-deepcode`  
Working directory: `stack/ahbg/deepseek/`

The directory name `deepseek/` is the assigned calibration workspace label. The builder assigned to it is DeepCode. Do not infer builder identity from the directory name.

Read `../README.md` and `../CALIBRATION.md` first.

Build an independent complete pair here:

```text
deepseek/
├── a0/
├── ahbg/
└── reviews/
```

## Build phase

Start from the common coordination-base commit recorded in `BUILD_MANIFEST.json`.

During the independent build phase, do not read, copy, merge, cherry-pick, or adapt implementation code from `../grok/` or `../codex/`. Shared source authority, frozen scenarios, schemas, and evaluation criteria are allowed.

Freeze the runnable build at an exact commit SHA before reciprocal review begins.

## Current build

This workspace now contains a runnable independent pair plus post-freeze
extension evidence:

- `a0/` — A0 lineage, boundary, permission field, capacity, uncertainty,
  regulatory shadow layer, telemetry, diary, deterministic decision tree,
  naming (`a0(<energy>)`), and a pluggable energy layer with DeepSeek
  default (`DEEPSEEK_API_KEY` from `.env`; openai and xai registered).
- `ahbg/` — UCNS-backed Seed-of-Life tile projection, world state (tiles
  carry `built`/`threat`), event log, turn loop with simultaneous `move`
  (v1) and `build` (v2) resolution, fail-closed unresolved mechanics,
  persistence, replay, and artifact checker.
- `run.py` — runs the sealed 35-scenario corpus, emits normalized artifacts
  under `artifacts/`, and enforces controls.
- `scenarios.py` — the `calibration-family` scenario source (digest
  `b05cba2c…e5e0`, merged to `main` via PR #5).
- `epoch2.py` — shadow-veto interpretation experiment + active candidate
  model.
- `epoch3.py` — bounded live-provider run of `a0(deepseek)`.
- `game.py` — whole-system bounded test: 30-layer board, 5-layer build,
  20% hidden threats, compact frontier observation, gameplay statistics.
- `reviews/` — both read-only reciprocal reviews plus the six-review ratio
  comparison.
- `CALIBRATION_STATUS.md` — frozen SHAs, six-check matrix, divergence
  register. `BUILD_MANIFEST.json` — provenance and change log.

## Reciprocal review phase

After all three build SHAs are frozen, DeepCode checks both other implementations read-only:

```text
DeepCode -> Grok
DeepCode -> Codex
```

Write findings only here:

```text
reviews/grok-review.md
reviews/grok-review.json
reviews/codex-review.md
reviews/codex-review.json
```

Each review records the frozen checker build SHA and frozen target build SHA. Never repair sibling code while reviewing it. Disagreement with the other checker remains `hmmm` until source authority or experiment resolves it.

## Usage

```bash
git switch agent/ahbg-deepcode
cd stack
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m unittest discover -s ahbg/deepseek/a0/tests -p 'test*.py'
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m unittest discover -s ahbg/deepseek/ahbg/tests -p 'test*.py'
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m ahbg.deepseek.run
```

## hmmm

Implementation and checker choices are local to this workspace until the shared evidence distinguishes them.
