# Codex calibration workspace

Builder: **Codex**  
Branch: `agent/ahbg-codex`  
Working directory: `stack/ahbg/codex/`

Read `../README.md` and `../CALIBRATION.md` first.

Build an independent complete pair here:

```text
codex/
├── a0/
├── ahbg/
└── reviews/
```

## Current build

This branch now contains a runnable Codex smoke implementation:

- `a0/` — A0 lineage, boundary, permission field, perspective, capacity,
  history, uncertainty, deterministic policy, and telemetry.
- `ahbg/` — UCNS-backed Seed-of-Life tile projection, world state, event log,
  turn controller, fail-closed unresolved mechanics, persistence, replay, and a
  read-only artifact checker.
- `run.py` — runs the Codex smoke corpus and emits normalized artifacts under
  `artifacts/`.
- `run_common_corpus.py` — runs the adopted successor corpus and emits a
  checkable aggregate artifact root under `corpus-run/<corpus-id>/`.
- `BUILD_MANIFEST.json` — records the coordination base, source authorities,
  and independence caveat for this corrected build.

The smoke corpus is not the final sealed calibration corpus. It proves that the
Codex pair is executable, replayable, and ready to be frozen or replaced by the
shared sealed corpus when that corpus lands.

The read-only artifact checker accepts the live AHBG evidence layouts now in
use: aggregate run files under `corpus-run/<corpus-id>/`, aggregate run files
under `artifacts/`, aggregate run files at workspace root, and DeepCode-style
per-scenario `*/events.jsonl` under `artifacts/`.

## Build phase

Start from the common coordination-base commit recorded in `BUILD_MANIFEST.json`.

During the independent build phase, do not read, copy, merge, cherry-pick, or adapt implementation code from `../grok/` or `../deepseek/`. Shared source authority, frozen scenarios, schemas, and evaluation criteria are allowed.

Freeze the runnable build at an exact commit SHA before reciprocal review begins.

## Reciprocal review phase

After all three build SHAs are frozen, Codex checks both other implementations read-only:

```text
Codex -> Grok
Codex -> DeepCode
```

DeepCode's calibration implementation lives in `../deepseek/`; the directory name is not builder identity.

Write findings only here:

```text
reviews/grok-review.md
reviews/grok-review.json
reviews/deepcode-review.md
reviews/deepcode-review.json
```

Each review records the frozen checker build SHA and frozen target build SHA. Never repair sibling code while reviewing it. Disagreement with the other checker remains `hmmm` until source authority or experiment resolves it.

## Usage

```bash
git switch agent/ahbg-codex
cd stack/ahbg/codex
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s a0/tests -p 'test*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ahbg/tests -p 'test*.py'
cd ../..
PYTHONDONTWRITEBYTECODE=1 python3 -m ahbg.codex.run
```

## hmmm

Implementation and checker choices are local to this workspace until the shared evidence distinguishes them.

This corrected build records a contamination caveat: the current Codex
conversation inspected sibling DeepCode/DeepSeek workspace files before moving
to `agent/ahbg-codex`. The implementation in this directory does not import or
copy sibling code, but the caveat is part of the evidence record.
