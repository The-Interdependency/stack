# Grok calibration workspace

Builder: **Grok**  
Branch: `agent/ahbg-grok`  
Working directory: `stack/ahbg/grok/`

Read `../README.md` and `../CALIBRATION.md` first.

Build an independent complete pair here:

```text
grok/
├── a0/
├── ahbg/
└── reviews/
```

## Build phase

Start from the common coordination-base commit recorded in `BUILD_MANIFEST.json`.

During the independent build phase, do not read, copy, merge, cherry-pick, or adapt implementation code from `../codex/` or `../deepseek/`. Shared source authority, frozen scenarios, schemas, and evaluation criteria are allowed.

Freeze the runnable build at an exact commit SHA before reciprocal review begins.

## Reciprocal review phase

After all three build SHAs are frozen, Grok checks both other implementations read-only:

```text
Grok -> Codex
Grok -> DeepCode
```

DeepCode's calibration implementation lives in `../deepseek/`; the directory name is not builder identity.

Write findings only here:

```text
reviews/codex-review.md
reviews/codex-review.json
reviews/deepcode-review.md
reviews/deepcode-review.json
```

Each review records the frozen checker build SHA and frozen target build SHA. Never repair sibling code while reviewing it. Disagreement with the other checker remains `hmmm` until source authority or experiment resolves it.

## Usage

```bash
git switch agent/ahbg-grok
cd stack/ahbg/grok
```

## Usage

```bash
cd stack/ahbg/grok
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s a0/tests -p 'test*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ahbg/tests -p 'test*.py'
PYTHONDONTWRITEBYTECODE=1 python3 run.py
python3 checker.py
```

Frozen implementation SHA: `cce9cec7dae61304118efcd47bc0d7461200d335`
(see `FREEZE.md`). Reciprocal reviews use that SHA, not later metadata commits.

Smoke epoch writes `CALIBRATION_RESULT.json`, `RUN_MANIFEST.json`, `EVENTS.jsonl`,
and per-scenario files under `artifacts/`. Grok adopts the shared corpus digest
`b05cba2cf2f15583548cc15158f09e2612545c978b6a42ddeb314f1e4ed0e5e0` with no
amendments; frozen-build reproduction of the full 35-scenario family remains
`hmmm` (see `corpus-adoption/`).

## hmmm

Implementation and checker choices are local to this workspace until the shared evidence distinguishes them.
The adopted digest is recorded; the frozen build did not run the full common corpus. War remains fail-closed.
