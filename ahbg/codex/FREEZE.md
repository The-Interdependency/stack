# Codex AHBG Freeze

Frozen implementation SHA:

```text
ffb64c274583d8539f8f4fe7e0aa77366689e910
```

Short SHA: `ffb64c2`

Commit subject: `Build Codex AHBG calibration pair`

This file is post-freeze metadata. The Codex implementation identity for
reciprocal review is the frozen SHA above, not the moving head of
`agent/ahbg-codex` after metadata or review commits.

## Verification

Before the freeze marker was added, the frozen build passed:

- A0 tests: 7 OK
- AHBG tests: 12 OK
- Python compile: 15 files OK
- Artifact checker: SURVIVED
- Calibration summary: survived 4, unresolved 2, falsified 0, blocked 0

## Review Boundary

Post-freeze commits must not modify implementation source or generated run
artifacts for the frozen build. Reciprocal reviews, when opened, belong under
`stack/ahbg/codex/reviews/` and must identify both checker and target frozen
SHAs.

## Caveat

Before this correction, the same conversation inspected sibling
DeepCode/DeepSeek files while on the wrong branch. `BUILD_MANIFEST.json` records
that contamination caveat rather than hiding it.
