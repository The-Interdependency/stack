# DeepCode — documentation aggregate comparison

Scope: the calibration program's documentation file aggregates — the shared
protocol layer (`ahbg/README.md`, `ahbg/CALIBRATION.md` on `main`) and the
three workspace aggregates (`ahbg/grok/`, `ahbg/codex/`, `ahbg/deepseek/`) —
compared on two axes: **information completion** (which protocol-relevant
records exist) and **content clarity** (can a reader recover purpose, current
state, evidence standing, pending items, and provenance without archaeology).

Reference tips observed: `origin/agent/ahbg-grok` `c1f9d81`,
`origin/agent/ahbg-codex` `b0cc06c`, `origin/agent/ahbg-deepcode` `a0927f1`,
`origin/main` `3a92c7b0`.

## 1. Information completion matrix

| Record | Grok | Codex | DeepCode |
|---|---|---|---|
| Workspace README | ✅ | ✅ | ✅ |
| README describes current build | ❌ (template only) | ✅ | ❌ (template only) |
| BUILD_MANIFEST | ✅ | ✅ | ✅ |
| Freeze record (FREEZE.md/json) | ✅ | ✅ | ❌ (SHA in manifest/status only) |
| RUN_MANIFEST | ✅ | ✅ `artifacts/` | ✅ `artifacts/` |
| CALIBRATION_REPORT/RESULT | ✅ smoke + `corpus-run/` | ✅ smoke + `corpus-run/` | ✅ `artifacts/` |
| CALIBRATION_STATUS | via `COMPARISON.md` | ✅ | ✅ |
| Sealed corpus proposal | ❌ | ❌ | ✅ (author) |
| Sealed corpus adoption record | ✅ | ✅ | ❌ (proposer, no adoption mirror) |
| Full 35-scenario post-freeze run | ✅ `corpus-run/` | ✅ `corpus-run/` | ✅ `artifacts/` |
| Reciprocal reviews ×2 | ✅ + `CHECK_REPORT/` subdirs | ✅ | ✅ + `RATIO_COMPARISON` |
| Divergence register | ✅ `COMPARISON.md` | ⚠️ short `hmmm` list | ✅ `CALIBRATION_STATUS.md` |
| Cross-builder comparison doc | ✅ `COMPARISON.md` (program-wide) | ❌ | ⚠️ six-review ratios only |
| Cost-control / falsification evidence | ✅ `cost-controls/` | ❌ | ✅ `epoch2/` |
| Live-provider evidence (tokens/latency) | ❌ | ❌ | ✅ `epoch3/` + `game/` |
| Build mechanic documentation | ❌ (build unresolved) | ❌ | ✅ `game/` + status |
| Coding-ratio bookends | ❌ | ❌ | ✅ 24 files verified |

## 2. Content clarity assessment

### Shared protocol layer (`ahbg/README.md`, `ahbg/CALIBRATION.md`)

Clear and authoritative. The README states the immediate target and the two
coordination modes ("do not mix them"); CALIBRATION.md states the program
purpose, the three-builder contract, the six directional checks, and the
evidence-standing vocabulary. This layer is the standard every workspace
aggregate is measured against.

### Grok aggregate — richest synthesis, scattered layout

Strengths:

- `COMPARISON.md` is the only program-wide cross-builder document: freeze
  identities, six directional checks, regulatory-component standings
  (including the **FALSIFIED** additive cost model vs the simpler binary
  occupancy veto), a six-item divergence register, and an explicit
  "program completion: not closed" statement with a do-not-promote warning.
- Full corpus adoption and post-freeze 35-scenario execution records exist.

Clarity gaps:

- The workspace README is the coordination template only; the actual state
  lives in `COMPARISON.md`, `FREEZE.md`, `CALIBRATION_REPORT.md` (smoke only),
  `corpus-run/`, and `cost-controls/` — a reader must assemble the aggregate.
- `COMPARISON.md` is labeled "partial" and mixes the comparison with
  cost-control conclusions.

### Codex aggregate — cleanest status, thinnest comparison

Strengths:

- `CALIBRATION_STATUS.md` is the cleanest single-file status: evidence
  observed (branch heads), sealed corpus, frozen SHAs, common-corpus
  execution standings, six directional checks, standing, and remaining
  `hmmm` — all recoverable without archaeology.
- README includes a "Current build" section describing the actual contents.

Clarity gaps:

- No cross-builder comparison document.
- No cost-control/falsification evidence record.
- The divergence register is a short bullet list inside `hmmm`, not a
  numbered, visible register.
- No live-provider or coding-ratio records.

### DeepCode aggregate — deepest extension record, weakest orientation

Strengths:

- Richest extension evidence: energy layer + `a0(deepseek)` nomenclature,
  epoch 2 interpretation experiment, epoch 3 live-provider run, whole-system
  game with gameplay statistics, six-review ratio comparison.
- `BUILD_MANIFEST.json` carries the only full change log (12 SHAs) with a
  `change_log` field; 24 source files carry verified first/last-line ratio
  bookends.
- `CALIBRATION_STATUS.md` keeps a seven-item divergence register and a
  six-check matrix.

Clarity gaps:

- README is the coordination template only; it does not describe the current
  build (compare Codex's README).
- No `FREEZE.md` record — the frozen SHA lives inside the manifest and status
  files.
- Proposer of the corpus, but no adoption-mirror record in the workspace.
- The only cross-builder document is `reviews/RATIO_COMPARISON.md`, which
  covers review ratios only, not the whole program (no regulatory-component
  standings like Grok's `COMPARISON.md`).

## 3. Comparative findings

1. **No aggregate is complete.** Grok owns the program-wide synthesis and the
   falsification evidence; Codex owns the cleanest status; DeepCode owns the
   live-provider and coding-ratio records. Each is missing what another has.
2. **Clarity winner (single file):** Codex `CALIBRATION_STATUS.md`.
   **Completeness winner (program view):** Grok `COMPARISON.md`.
   **Completeness winner (extension + provenance view):** DeepCode
   `BUILD_MANIFEST.json` + `CALIBRATION_STATUS.md`.
3. **Common gaps:** none of the three READMEs describe the post-freeze state
   end-to-end; only Grok and Codex emit explicit freeze records; only
   DeepCode verifies coding ratios or records live-provider burden.
4. **The shared protocol docs remain the only complete description of the
   program's intent.** Workspace docs describe each builder's slice; no
   single workspace doc yet reconstructs the whole program as well as
   `CALIBRATION.md` + `COMPARISON.md` read together.

## 4. Recommended revisions (DeepCode side)

- Add `FREEZE.md` recording `ec07f46…` with provenance.
- Add a "Current build" section to `ahbg/deepseek/README.md`.
- Add a corpus-adoption mirror noting DeepCode is the proposer (digest
  `b05cba2c…`, merged via PR #5).
- Extend `RATIO_COMPARISON.md` or add `COMPARISON.md` with program-wide
  regulatory-component standings (as Grok's does), not only review ratios.
