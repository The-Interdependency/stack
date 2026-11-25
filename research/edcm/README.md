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


## MultiWOZ 2.1 full-corpus projection

The [frozen corpus protocol](MULTIWOZ_PROJECTION_PROTOCOL.json) exercises the same native recursive origin directions jointly, rather than treating overlapping axes as independent proximity scores. It consumes the previously [admitted Cambridge archive](https://www.repository.cam.ac.uk/items/74e8d468-9442-424a-bb3b-1bb88dcb8673/full) (DOI `10.17863/CAM.41572`, CC BY 4.0). The [aggregate receipt](evidence/multiwoz-epicycle-projection-v1.json) binds exact Stack, EDCM, UCHC and UCNS sources, the admitted archive, the coordinate rule and a chain of all dialogue results. Raw corpus text and per-dialogue checkpoints remain outside Git.

### Corpus result

All 10,438 dialogue graphs replayed; all 143,048 source turns (including 1,607 containing CR/LF) and 71,524 complete rounds reconciled. Every round and full-prefix state has all eleven joint coefficients and the independent maintained readout. Every unambiguous pre-response booking event was measured: 5,214 development, 656 validation and 661 test; the 19 ambiguous development annotations remain counted exclusions.

The fixed, eleven-column recursive origin matrix has numerical rank 11 but condition number **25,414**. The median test-prefix field energy projected onto the origin span is 85.2%. Yet the median absolute per-axis Spearman association with the maintained test readouts is only 0.084 (round-only 0.038; prefix differences 0.071). Test-prefix associations include E +0.452, F −0.363, P +0.247 and L +0.229. The test partition barely exercises several maintained readouts: C is nonzero in 1/7,372 rounds, I in 6, κ in 17, O in 40, and R in 52. This corpus cannot by itself settle all eleven intended measurement semantics.

### External outcome comparison

Each score uses only the exact preceding turns; the labelled system response is withheld. Calibration uses development, threshold selection uses validation, and test evaluation follows both freezes. The maintained progress point estimate exactly reproduces the previous EDCM booking test; no score improves on it here.

| Fixed score | Test balanced accuracy | 95% dialogue-cluster interval |
|---|---:|---:|
| Maintained P | 52.1% | 46.6–57.5% |
| Joint geometric P | 48.9% | 45.1–52.7% |
| Joint geometric ΔP | 48.8% | 47.5–50.2% |
| Context length control | 48.4% | 45.4–51.6% |

**Disposition:** native full-corpus construction and replay SURVIVED. The proposed geometric progress scores do not establish above-chance discrimination; the point estimates are below chance. The high origin condition number and weak correspondence with the maintained measurements identify a poorly separated candidate coordinate system, not a failure of native source construction. This experiment does not establish a causal explanation for the weak discrimination.

### Replay

Use the released-producer environment above. Obtain the exact source archive using EDCM's existing admission record. The runner independently verifies archive bytes, every logical member, the partition inventory and all source-native outcome counts before execution.

```sh
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python -m pytest -q research/edcm/tests
python -m research.edcm.multiwoz_projection   --archive /path/to/MULTIWOZ2.1.zip   --checkpoint /tmp/multiwoz-epicycle-checkpoint.jsonl   --output /tmp/multiwoz-epicycle-report.json --workers 8
```

Use the same command and source-bound checkpoint to resume. The native numerical evaluator caches exact Point evaluation and child endpoint units; focused tests compare it to the released native display, including exact endpoint records, full recursive norms, Unicode and future-response exclusion. The local resource preflight estimated 0.113 s/dialogue on one worker, and eight workers completed the corpus in approximately five minutes. All 21 focused and inherited tests passed. A separate full source-to-checkpoint reconciliation confirmed every dialogue, turn, round and eligible event; re-aggregating the verified checkpoint produced a byte-identical report (without repeating the native execution). The aggregate receipt SHA-256 is `7e896f6062eabc08d8cc5c68e46caf7e25042dddf987e201da6ab67dc41197e0`.

## hmmm

The next measurement question is how to compare role-aligned and window-local structures against a particular metric origin, rather than simply resolve eleven nearly collinear directions over entire histories. Freeze that relation and its falsifier using development evidence, then test it on separately admitted source-native labels. EDCM's existing corpus queue after MultiWOZ lists Molweni, PRISM, ICSI, AMI, WildChat-1M, and LMSYS-Chat-1M; these each still require admission and adapters. Prioritize adequate representation of contradiction, refusal, integration and scope before claiming broader metric validity. Do not tune the MultiWOZ test partition or transfer its task-success labels to other semantics.

GPT generated from context and prompt by Erin Spencer.
