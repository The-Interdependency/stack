# English ordinal candidate in the Stack forge

Stack owns this candidate's English implementation and public-contract research.
UCNS owns its Public Gonol carrier, ordinal geometry, native objects and receipts.
UCHC may carry a verified extraction while the domain remains ungraduated.

The candidate originated in UCHC PR #10 at
`c514e1a2a3f3da5ffae9ebf76d67a1d348845842`. That proposal lacked the required
Stack source. This repair establishes the source here and preserves the proposal's
identity in [ordinal-source.json](ordinal-source.json); it does not pretend the
proposal originally came from Stack. Copied source retains FSL-1.1-ALv2 terms.
The [input graph](ordinal-work-graph.json) records exact upstream identities.

## Usage and construction

Install UCNS from the graph's exact producer and run from this workspace:

```bash
python -m english_gonol.ordinal_construction word
python -m pytest -q ordinal_tests/test_ordinal_construction.py
UCHC_STRUCTURAL_FIELD=/path/to/verified/complete/field \
  python -m pytest -q ordinal_tests/test_ordinal_corpus.py
```

The Public Gonol supplies angles relative to SPACE. Appending a glyph places it
at R/2 and halves earlier occurrences: `word` ends at R/16, R/8, R/4, R/2.
Only UCNS computes those placements. Missing bearings refuse; SPACE-spanning
queries retain word interiors and explicitly leave their parent frame unresolved.
Every returned word/interior carries the verified UCNS producer identities.

The [2026-10-27 ratified decisions](ordinal-decisions-2026-10-27.md) select
construction-derived parent bearing through SPACE, whole-lexical definition
ownership, and permission to rebase glyph bearings in a new carrier version.
The same record now fixes compound joining at the terminal glyph occurrence:
it serves as SPACE for the next component, radial distance stays unchanged,
and angular placement changes to express the join. Exact angular composition,
forward origin implementation and expanded carrier specification remain
distinct implementation boundaries.

## Extraction and verification

Make implementation changes here first. UCHC pins an exact Stack commit and
checks source/test SHA-256 values plus the existing structural import closure.
Its ordinal workflow runs Stack source tests and compares Stack, UCHC source,
and clean-wheel CLI results. Its structural workflow reuses the complete corpus
to run the same detached-interior regression against Stack and the installed
wheel, then compares the actual SPACE-seam output.

`ordinal_tests/` is a separate suite because it requires the selected UCNS
ordinal package, while historical English suites retain their own producer pins.
The dedicated Stack workflow fails on errors or skipped ordinal tests. A passed
candidate extraction does not transfer authority or publish a stable release.

Rollback removes this optional candidate and its dedicated workflow together;
retain the original proposal identity and sealed historical corpus evidence.
No AHBG lock, historical English receipt, or global `libs/ucns` pin changes.

## hmmm

- Expanded carrier inventory/order and bearings for missing Unicode scalars;
  rebasing in a new version is authorized by the linked decision.
- Exact angular composition for the compound join. Its terminal-occurrence
  SPACE reference and unchanged radial distance are settled.
- Whole-lexical-owner implementation and full-corpus replay; ownership is chosen.
- Stable publication, released-artifact reconsumption and domain graduation.
