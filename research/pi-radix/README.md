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
