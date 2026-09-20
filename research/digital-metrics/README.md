# Digital metrics protocol v0

Standing: **INCUBATING / TEST-BACKED STACK RESEARCH**.

This workspace provides the first strict cross-repository metric transport and
receipt slice for METAPAT, UCNS, EDCM, and Stack. It is not canon and does not
validate a scientific or semantic metric.

## Authority and flow

```text
METAPAT semantic constraint
  -> UCNS exact structural producer
  -> Stack strict observation + integrity projection + receipt
  -> future EDCM projection and calibration (hmmm; not invoked here)
```

- METAPAT owns definitions, question forms, interpretation constraints, and
  claim status. No METAPAT label is converted into a numerical value.
- UCNS owns geometry and its own proof status. The first slice executes its
  native Möbius state transition directly from the exact pinned checkout.
- EDCM owns future measurement projections. The v0 receipt invokes no EDCM
  decoder or measurement function. Its fail-closed missing-metric repair is
  pinned as a prerequisite only.
- Stack owns this noncanonical protocol, integrity metrics, work graph,
  deterministic receipt, and replay verifier. A passing Stack receipt transfers
  no authority, proof, measurement, or empirical status.

Exact participants and remaining boundaries are in [`WORK_GRAPH.json`](WORK_GRAPH.json).

## Wire guarantees

`metric_protocol.py` defines strict records for:

- metric definitions;
- typed observations;
- retained structures with participant identity, provenance, ordered relations,
  and multiplicity;
- deterministic receipts.

The protocol rejects missing and unknown fields, floating-point values, boolean
and integer aliasing, noncanonical rationals, stale digests, and status transfer.
Every observation carries `value`. A non-observed status requires explicit
`null`, a reason, and `not_quantified` uncertainty; absence never becomes zero.
Committed producers use typed `git-commit` revisions. A pre-commit Stack
artifact uses `candidate-content`, whose revision digest must equal its artifact
digest; it never claims to exist at the baseline commit.

## Frozen first slice

Semantic binding:

```text
metapat.application.affixiation_harmonics
affixiation-harmonics-application-v4
```

Geometric producer:

```text
ucns.native-mobius-root-loop@1.0.0
```

The committed receipt records:

- one visible turn preserves the visible key: `true`;
- one visible turn preserves the complete framed key: `false`;
- two visible turns restore the complete framed state: `true`;
- the exact `7/3` then `-7/3` displacement restores complete state: `true`;
- participant identity retention: `1/1`;
- ordered relation retention: `1/1`;
- provenance binding complete: `true`.

These are structural observations and transport-integrity readouts. They are not
EDCM measurements and do not independently prove UCNS mathematics.

Receipt:

```text
receipts/native-mobius-v0.json
Receipt payload digest (`receipt_sha256`): fcc1d049105ba46b055c28e8ab3428bd3cb40a68791b860fe2f5f20817fa2e3e
File SHA-256: 29734a8c78e2e41a0acac69d356fe795df7f710bfc4a1e4fd71fc114b7685c66
```

## Usage guidance

Run adversarial protocol tests:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=skill-lib \
python3 research/digital-metrics/audit_contracts.py
```

Then run the adversarial witnesses:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -m unittest discover \
  -s research/digital-metrics/tests -p 'test*.py' -v
```

Generate a candidate receipt from clean checkouts at the exact commits in
`WORK_GRAPH.json`:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/digital-metrics/generate_receipt.py \
  --metapat-root /path/to/exact/metapat \
  --ucns-root /path/to/exact/ucns \
  --output /tmp/native-mobius-v0.pending.json
```

The generator always records verification as `pending`. Replay that candidate
and write a `pass` receipt only after the named verifier obtains the identical
candidate from the pinned producers:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/digital-metrics/verify_receipt.py \
  /tmp/native-mobius-v0.pending.json \
  --metapat-root /path/to/exact/metapat \
  --ucns-root /path/to/exact/ucns \
  --attest-output /tmp/native-mobius-v0.attested.json
```

Replay an already attested receipt byte-for-byte:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/digital-metrics/verify_receipt.py \
  research/digital-metrics/receipts/native-mobius-v0.json \
  --metapat-root /path/to/exact/metapat \
  --ucns-root /path/to/exact/ucns
```

The generator fails before importing producer code when a required producer
checkout has the wrong commit or any tracked changes.

The METAPAT import is isolated from the ambient module cache, its resolved file
must be inside the verified checkout at the expected path, and the prior cache
is restored afterward. METAPAT and UCNS producer loaders compile the verified
source bytes directly; the regression suite proves that same-size,
same-timestamp poisoned bytecode is not executed.

## Promotion gates

1. Write an independent verifier that does not import this protocol module.
2. Define an EDCM projection separately, with its observable, falsifier,
   uncertainty, missingness, and calibration protocol preregistered.
3. Use development/validation/held-out evidence with no target-informed changes.
4. Demonstrate predictive or discriminative value against matched controls.
5. Register the resulting derivation in Stack fresh-making only after its
   producer, verifier, and output identities are stable.
6. Promote repo-owned pieces only through their owning repositories; Stack
   placement alone creates no authority.

## hmmm

- No EDCM projection is selected or calibrated.
- The verifier shares protocol code with the generator; replay is deterministic
  but not yet independent implementation agreement.
- Git/content identities are not cryptographic producer signatures.
- The correct empirical targets and external holdout custody remain unresolved.
