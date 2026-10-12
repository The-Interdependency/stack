# Pi radix structure

Standing: **Stack-local bounded computation; no base-independent law established.**

This workspace measures prime-valued symbols and contiguous prime-valued blocks in
radix representations of \(\pi\). It also gives every radix symbol an exact point on
the unit circle:

\[
d\longmapsto e^{2\pi i d/b},\qquad 0\le d<b.
\]

The stored identity is the integer pair `(base, digit)`. Turns, degrees and radians
are exact derived fractions; floating-point coordinates never define a symbol.
Decoded integer primality is independent of notation. The selection and position of
a block in a radix expansion remain base-dependent. The experiment preserves that
distinction rather than promoting recurrence into invariance.

## Usage

From the Stack root, regenerate both committed artifacts:

```bash
python research/pi-radix/pi_radix.py scan
```

Run the workspace tests:

```bash
python -m unittest discover -s research/pi-radix/tests -v
```

Run the structural Stack gate after any placement or provenance edit:

```bash
python tools/check_stack_consistency.py
```

The scan uses only the Python standard library. It generates \(\pi\) twice at
different decimal precision and fails before analysis if any requested radix symbol
differs. Prime testing is deterministic for the bounded unsigned-64-bit block domain.

## Artifacts

- `EXPERIMENT.json` freezes the compared bases and questions.
- `receipts/pi-radix-scan-v1.json` contains complete digit streams, prime hits,
  cross-base recurrences and exact angular coincidences.
- `docs/pi-radix-scan-v1.md` is the human-readable result projection.

## Boundaries

- This workspace owns the experiment and its receipts, not prime-number canon.
- METAPAT supplied domain-restraint guidance only; root impact is none.
- The unit-circle projection is ordinary exact mathematics implemented locally. It
  neither consumes nor redefines UCNS geometry.
- Fixed 500-symbol samples have different information depths across bases. The receipt
  also evaluates the longest prefix of every stream that stays within a common
  2,400-bit horizon. Counts are reported per eligible window; neither profile is
  treated as proof of an invariant.

## hmmm

Whether a useful invariant survives continued-fraction indexing or another
base-independent segmentation remains open.
The wheel is exact; the law allegedly riding it has not yet shown identification.

## Recurrence controls

The exploratory follow-up is frozen in `CONTROL_PLAN.md`. It compares the pi
recurrence count to 199 same-number cross-radix controls and 199 conditional
histogram shuffles. All samples use identical block selection rules. Read
`docs/recurrence-controls-v1.md` for the results and limits; the matching JSON
receipt records every replicate count, interval numerator, and source hashes.

```bash
python research/pi-radix/recurrence_controls.py
```

The 2400-bit horizon describes resolution, not entropy. SHAKE256 draws are a
reproducible simulation model, not evidence that pi is random. The exact eight
primes were selected after inspecting pi; the comparison tests the COUNT of
recurring prime values, not a post-selected list of identities.

Scanner review repair: oversized horizons and bases now fail before analysis;
reports use configured lengths and labels; angular comparisons retain pairwise
prefix overlap after a shorter third stream ends. Artifact hashes changed when
regenerated; pi's 12/8 recurrence counts did not. The former receipt is retained
in Git history at b4791f2bebf8218201d22e07131c8cbe74ddf4d8.

## Admission limits and independent verification

The seven bases, 500-symbol streams, block lengths 1–4, and 2400-bit comparison
remain unchanged. Custom scans admit bases 2–100000 and decoded values through
`2^64 - 1` inclusive. Before generation, the validator enforces:

- at most 100000 retained symbols across all bases per precision run;
- at most 2000000 block-digit work units across both profiles, conservatively
  counted as `2 * number_of_bases * symbol_count * sum(block_lengths)`;
- at most 2000000 alphabet entries scanned across both profiles, counted as
  `2 * sum(bases)`; the sieve also rejects oversized direct calls before allocation;
- at most 10000 required decimal digits before guard digits, bounding the two
  Chudnovsky calculations; and at most 50000000 generation digit-work units,
  `2 * number_of_bases * symbol_count * (required_decimal_digits + 180)`,
  bounding aggregate high-precision extraction as well as retained symbol count.

Version 1 accepts only `constant: pi` and its implemented canonical-block,
angular-symbol, and precision-verification rule strings from `EXPERIMENT.json`.
Changing those labels cannot select a different algorithm. Unsupported or missing
rules fail before generation, so receipts cannot claim behavior that was not run.

Each evidence generator snapshots its source files before computing, uses those
bytes for receipt hashes, and rejects sources changed before completion. Scanner
and control modules also reject disk bytes that differ from the source captured
when they loaded. Mid-run edits leave existing output files untouched. Apply the
same unchanged-input requirement when regenerating independent verification.

These resource limits reject infeasible requests rather than truncating evidence.
Impossible horizons are rejected using the smallest radix and the admitted
symbol count before any horizon-sized exact exponentiation. Phase summaries
count distinct positions separately from `(position, reduced phase)` groups;
multiple groups at one position do not create additional positions.
The terminal gcd sieve retains `[1, 0]`, whose decoded value is the radix itself:
it can be prime. Correcting this omission raises shared-number trial 192's
fixed-500 recurrence count from 8 to 9, and the control mean from 11.111 to
11.116. Pi's 12/8 counts and the primary matched-horizon comparison are unchanged.

To independently verify all canonical scan blocks and all 796 control counts,
including the complete 199-replicate replay, install GNU coreutils (`factor`)
and run:

```bash
python research/pi-radix/verify_evidence.py
```

The verifier uses direct place-value decoding, GNU factorization, a separate
recurrence counter, and pairwise phase comparisons. It reuses the control draw,
interval, and shuffle generation; it does not claim an independent implementation
of those generators. The dedicated `pi-radix-research` workflow runs this gate.
After intentional source changes, regenerate the scan and control artifacts
with the commands above, then write the verification receipt with
`python research/pi-radix/verify_evidence.py --write`. Verification failure leaves
that receipt untouched. Counts remain finite-prefix computational evidence.
