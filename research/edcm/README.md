# EDCM epicycle measurement research

**Area:** EDCM (third in the Stack delivery sequence).
**Standing:** Stack-local candidate measurement research.

The installed UCHC `0.2.0a3` release closes the eleven EDCM metric origins and retains ordinal placement and the exact additive resultant at every closed epicycle. The instrument below consumes those two load-bearing results, all nested occurrences, and the maintained independent EDCM transcript readouts. Canonical EDCM remains in its owning repository; the imported view in `../../libs/edcm/` is unchanged.

## Decision and evidence

The frozen [projection protocol](EPICYCLE_PROTOCOL.json) tests the largest shared decision available after UCHC graduation: determine which geometric fields preserve the distinctions required by the existing measurements, and test the proposed origin axes and proximity rules. [BASE](BASE.json) and the [work graph](EPICYCLE_WORK_GRAPH.json) pin the exact EDCM, UCHC, UCNS, METAPAT, and doctrine identities. The pass/failure conditions are the protocol's acceptance rules. A native record must admit exact source recovery and both vector results before any comparison; a counterexample falsifies the specified candidate at its declared grain. All eleven targeted baseline readout changes occurred.

The comparison retains native graphs and extracts four fields: additive resultant, ordinal endpoint, their pair, and the recursive field of both vectors plus every parent-local ray at each occurrence. The recursive coordinates compare equal parent-local ordinal-depth addresses and roles. Zero-extension for comparisons records differing supports separately. Numeric values use UCNS's native display; exact expressions remain the retained evidence.

## Results

| Geometric field | Origin dimensions | Numeric rank | Same-round changed readouts distinguished | Full-prefix changed readouts distinguished |
|---|---:|---:|---:|---:|
| Additive | 2 | 2 | 0/11 | 5/11 |
| Ordinal | 2 | 2 | 6/11 | 11/11 |
| Paired | 4 | 4 | 6/11 | 11/11 |
| Recursive | 118 | 11 | 6/11 | 11/11 |

- All eleven origin records close and replay. All eleven order reversals preserve the exact additive result and change the placed endpoint. A doubled outer frame scales both results exactly. The cancellation control has zero additive resultant and a nonzero placed endpoint.
- All 55 distinct origin pairs have nonzero numeric cosine in each field. The recursive field has eleven independent numerical directions at the frozen rank tolerance, but those axes are not mutually orthogonal.
- Five order-only contrasts exercise C, R, E, O, I, and N. Exact additive equality falsifies additive-only sufficiency for those six baseline readout changes.
- The same terminal round paired with different histories changes F, D, L, P, and κ. All four terminal-round fields are exactly equal. Full-prefix retention distinguishes all five.
- The formatting control changes the geometry while leaving every baseline readout equal. Distinction alone is not measurement calibration.
- Every tested uniform monotonic hypothesis (smaller distance, larger signed projection, or larger cosine for a larger unsigned readout) has counterexamples. Even the full-prefix recursive signed projection agrees with only six out of the ten unsigned contrasts. The signed O direction is unresolved.

The [summary](evidence/epicycle-projection-v1-summary.json) and [complete compressed receipt](evidence/epicycle-projection-v1.json.gz) retain all eight fixture pairs, eleven origin analyses, controls, raw readouts, native graphs, and unrounded numeric comparisons. Receipt digest: `7777f5f30bff69778053dccffddd27ae3b6a45def57f2f929c7b8bb6a7e5602d`. The two-second local generation and independent replay used Python 3.12.14, NumPy 2.2.6, Linux x86-64, and one OpenBLAS thread. Sixteen focused tests and 38 existing digital-metrics tests passed. The shared digital-metrics receipt was replayed against the changed root manifest; its only evidence-input change is the manifest-source digest. Prior receipts retain their historical identities.

## Run and reuse

From the Stack root, use a fresh Python 3.12.14 environment:

```sh
python3.12 -m venv /tmp/edcm-epicycle
. /tmp/edcm-epicycle/bin/activate
python -m pip download --no-deps --require-hashes \
  -r integration/uchc/halving-requirements.txt -d /tmp/edcm-wheel
python -m pip install --no-deps -r research/edcm/requirements.txt /tmp/edcm-wheel/*.whl
python -m pip install pytest==8.3.5
python -m pip check
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python -m pytest -q research/edcm/tests
python -m research.edcm.epicycle_projection \
  --output /tmp/epicycle-receipt.json --summary /tmp/epicycle-summary.json
python -m research.edcm.epicycle_projection --verify /tmp/epicycle-receipt.json
```

For new observations, give `--rounds` a JSON array of consecutive exact raw round strings (one EDCM parser cycle per string):

```sh
python -m research.edcm.epicycle_projection \
  --rounds /tmp/rounds.json --output /tmp/observation.json
python -m research.edcm.epicycle_projection \
  --rounds /tmp/rounds.json --verify /tmp/observation.json
```

Python consumers can call `observe_rounds(raw_rounds)` to receive the same bound native graphs, field records, all eleven origin comparisons, independent baseline vectors, and receipt digest. The CI workflow generates and replays a current complete receipt. To replay the committed historical receipt, decompress it with `gzip -dc`, then use `--verify` with its recorded source and numeric runtime; binary64 comparisons do not promise byte identity across different numeric runtimes.

## hmmm

The next decision is lawful metric-specific comparison, not whether more dimensions exist. Freeze a role- and window-aware observation/frame convention, then test a declared metric-specific comparison on new contrasts that separate order, context, formatting and paraphrase. Use independent holdout dialogue and assess the existing proxy semantics separately before proposing a calibrated EDCM measurement adapter. The current complete graphs and failed comparison receipts provide the controls for that decision. Authority, measurement validity, and proof standing remain separate.

GPT generated from context and prompt by Erin Spencer.
