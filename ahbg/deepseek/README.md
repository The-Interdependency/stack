# DeepSeek calibration workspace

Working directory: `stack/ahbg/deepseek/`

Read `../CALIBRATION.md` first.

Build an independent complete pair here:

```text
deepseek/
├── a0/
├── ahbg/
└── reviews/
```

Do not edit or copy implementation code from `../grok/` or `../codex/` during the calibration epoch. Consume the same frozen protocol, scenarios, source authorities, and evaluation contract; independently realize the implementation.

Before building, resolve and record exact source commits and applicable skill-lib instructions in `BUILD_MANIFEST.json`.

The build is complete only when its a0 instance and AHBG environment run the shared sealed calibration corpus and emit the normalized artifacts required by `../CALIBRATION.md`.

After all three builds are frozen, DeepSeek must independently check both sibling implementations read-only:

```text
DeepSeek -> Grok
DeepSeek -> Codex
```

Write those findings under this workspace only:

```text
reviews/grok/
reviews/codex/
```

Do not repair sibling code while checking it. Preserve disagreements with the sibling's other checker as `hmmm`; do not resolve them by vote.

## hmmm

Implementation and checker choices are local to this workspace until the shared evidence distinguishes them.