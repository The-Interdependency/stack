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
cd stack/ahbg/deepseek
```

## hmmm

Implementation and checker choices are local to this workspace until the shared evidence distinguishes them.
