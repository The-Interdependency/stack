# Codex calibration workspace

Working directory: `stack/ahbg/codex/`

Read `../CALIBRATION.md` first.

Build an independent complete pair here:

```text
codex/
├── a0/
├── ahbg/
└── reviews/
```

Do not edit or copy implementation code from `../grok/` or `../deepseek/` during the calibration epoch. Consume the same frozen protocol, scenarios, source authorities, and evaluation contract; independently realize the implementation.

Before building, resolve and record exact source commits and applicable skill-lib instructions in `BUILD_MANIFEST.json`.

The build is complete only when its a0 instance and AHBG environment run the shared sealed calibration corpus and emit the normalized artifacts required by `../CALIBRATION.md`.

After all three builds are frozen, Codex must independently check both sibling implementations read-only:

```text
Codex -> Grok
Codex -> DeepSeek
```

Write those findings under this workspace only:

```text
reviews/grok/
reviews/deepseek/
```

Do not repair sibling code while checking it. Preserve disagreements with the sibling's other checker as `hmmm`; do not resolve them by vote.

## hmmm

Implementation and checker choices are local to this workspace until the shared evidence distinguishes them.