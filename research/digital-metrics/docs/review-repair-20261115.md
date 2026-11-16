# Digital-metrics review repair

Area: EDCM workstream, priority 3. This is structural transport and replay;
it invokes no EDCM measurement or projection.

Starting PR #46 head: `28647b5b29e839626b8cba294b47b0b715c23c24`.
Integrated Stack main: `3032238fc8549b58721c9baf2753c53844eb8d96`.
Current semantic consultation: METAPAT
`af17dae458a806b5a0d607cbaa61be8f68b85a5e`, Chapter Zero, axioms and domain
restraint. Registration, declaration, execution and verification remain
different evidence; no authority, proof or measurement status transfers.

## Defects and repair

| Finding | Observed starting behavior | Repair and failure witness |
|---|---|---|
| Witness report-channel forgery | Stack-frame access obtains the report descriptor and shutdown marker; a failing witness returns `(true, "", 1)`. | Remove the executable-witness attestation mechanism. Audit only source-linked declarations; a failing test's top-level side effect never runs, execution is `NOT_RUN`, verified contracts are zero. |
| Transient result callback replacement | Cleanup replaces and restores result callbacks; the failing cleanup returns clean one-test completion. | Same owning trust-boundary repair. No witness interpreter can produce an accepted execution report because the audit launches none. Reviewed repository tests run separately. |
| Raw HTML projection | Wrapping the exact projection in `<pre>` hides headings/tables while consistency reports no finding. | Exclude raw HTML/code blocks while retaining line boundaries. Raw-block fixtures fail projection admission. |
| Coherent authority reassignment | Assigning EDCM semantic/geometry/proof authority consistently across graph, JSON and Markdown passes. | Both graph loader and structural checker enforce the frozen v0 authority split, even after matching edits and recomputed digests. |
| Duplicate JSON identities | A prior all-zero `commit` followed by the selected commit is silently collapsed and admitted. | Generator, structural checker and audit reject duplicate members, including repeated identical values. |

The superseded runtime and its fixtures remain recoverable at the starting
commit. They are historical evidence, not a supported fallback. Static audit
wire version 0.2.0 removes the ambiguous `passed` field; callers use
`linkage_passed` and must retain the explicit non-execution fields.

## Integration and provenance

Current-main operational skills remain pinned as current main declares.
The historical experiment keeps skill-lib
`fb3b53a7629f7f03ecf255167d52c13abef1a979`; its exact parser is isolated under
`vendor/` and declared on that research participant, with source license and
byte identity preserved. It does not replace current Stack doctrine.

Existing producer commits and the original receipt remain unchanged. The new
receipt binds repaired execution bytes and the integrated Stack manifest.
Successful replay establishes that bounded structural result, not an independent
verifier, empirical calibration, secure cipher or unforgeable Python sandbox.

## Usage and acceptance

From Stack, with clean checkouts at the exact commits in `WORK_GRAPH.json`:

```bash
python research/digital-metrics/audit_contracts_cli.py --skill-lib-root ../skill-lib-input
STACK_DIGITAL_METRICS_SKILL_LIB_ROOT=../skill-lib-input python research/digital-metrics/run_tests.py
python tools/check_stack_consistency.py
python research/digital-metrics/verify_receipt_cli.py \
  research/digital-metrics/receipts/native-mobius-v0-review-repair-20261115.json \
  --metapat-root ../metapat-input --ucns-root ../ucns-input --edcm-root ../edcm-input
```

Require clean linkage, a nonempty entirely passing reviewed suite, structural
consistency and byte-identical new-receipt replay. Hosted checks and current-head
review remain separate from local verification. Roll back by reverting this
repair; do not replace the preserved historical receipt with a new result.

Local result: 34 reviewed tests pass without skips; linkage closes 30 obligations
and 34 declarations with zero behavioral credit; Stack consistency admits seven
repositories and 66 participant identities. The repaired receipt replays with
payload digest `456f16a7b6348209f9399ffa8723105d7959dac73f862b99083a1d2315517a19`.
The [machine record](review-repair-20261115.json) preserves baseline outcomes and
the exact repaired source digests. Changed-source ratio checks and portfolio
provenance validation also pass.

hmmm: EDCM projection selection, calibration, independent implementation replay
and producer signatures remain separate research obligations. Hostile Python
execution is deliberately unsupported and receives no attestation.

GPT generated; context, prompt Erin Spencer.
