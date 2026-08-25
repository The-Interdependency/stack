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
```

## hmmm

Implementation and checker choices are local to this workspace until the shared evidence distinguishes them.
