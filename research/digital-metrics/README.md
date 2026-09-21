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
The v0 validator requires its complete ordered Stack, skill-lib, METAPAT, UCNS,
and EDCM participant sequence; a recomputed digest cannot authorize omissions.

## Wire guarantees

`metric_protocol.py` defines strict records for:

- metric definitions;
- typed observations;
- retained structures with participant identity, provenance, ordered relations,
  and multiplicity;
- deterministic receipts.

The protocol rejects missing and unknown fields, floating-point values, boolean
and integer aliasing, integer/rational wire-kind mismatches, noncanonical
rationals, stale digests, and status transfer. Integer values use an `integer`
wire tag; rationals use a distinct reduced numerator/denominator form. Every
observation carries `value`. A non-observed status requires explicit `null`, a
reason, and `not_quantified` uncertainty; absence never becomes zero. Every
receipt definition must have at least one explicit matching observation;
dropping an entire observation cannot bypass missingness. Committed
producers use typed `git-commit` revisions. A pre-commit Stack artifact uses
`candidate-content`, whose revision digest must equal its artifact digest; it
never claims to exist at the baseline commit.

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
Receipt payload digest (`receipt_sha256`): 724dc4ef31df329a047e51a3460261ec8d4b9223a2f8f7efa4d2d64c235a29e8
File SHA-256: c94247eed29c4e90bea8b9668218000bf12c497a36cef8c63c897e18339ac98d
```

## Usage guidance

Run the contract audit. It source-loads the exact manifest-bound msdmd parser,
executes every statically admitted witness, and rejects skips, expected
failures, unexpected successes, test failures, and static/runtime count drift:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONDONTWRITEBYTECODE=1 \
python3 research/digital-metrics/audit_contracts_cli.py
```

Then run the adversarial witnesses directly for verbose per-test output:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -m unittest discover \
  -s research/digital-metrics/tests -p 'test*.py' -v
```

Generate a candidate receipt from clean checkouts at the exact commits in
`WORK_GRAPH.json`:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/digital-metrics/generate_receipt_cli.py \
  --metapat-root /path/to/exact/metapat \
  --ucns-root /path/to/exact/ucns \
  --edcm-root /path/to/exact/edcm \
  --output /tmp/native-mobius-v0.pending.json
```

The generator always records verification as `pending`. Replay that candidate
and write a `pass` receipt only after the named verifier obtains the identical
candidate from the pinned producers:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/digital-metrics/verify_receipt_cli.py \
  /tmp/native-mobius-v0.pending.json \
  --metapat-root /path/to/exact/metapat \
  --ucns-root /path/to/exact/ucns \
  --edcm-root /path/to/exact/edcm \
  --attest-output /tmp/native-mobius-v0.attested.json
```

Replay an already attested receipt byte-for-byte:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 research/digital-metrics/verify_receipt_cli.py \
  research/digital-metrics/receipts/native-mobius-v0.json \
  --metapat-root /path/to/exact/metapat \
  --ucns-root /path/to/exact/ucns \
  --edcm-root /path/to/exact/edcm
```

The generator first executes the pinned EDCM decoder's rejecting witness for an
incomplete metric record; this validates only the fail-closed prerequisite and
does not invoke an EDCM measurement. It fails before importing producer code
when a supplied root is not the repository's resolved Git top level, or when a
required producer checkout has the wrong commit or any tracked changes.

The METAPAT import is isolated from the ambient module cache, its resolved file
must be inside the verified checkout at the expected path, and the prior cache
is restored afterward. Every METAPAT dependency executes from the exact blob in
the participant commit object named by `WORK_GRAPH.json`; source loading never
dereferences mutable `HEAD`, and every producer Git read disables replacement
objects. Untracked shadows and hidden working-tree changes are therefore not
executable. METAPAT, UCNS, and Stack replay modules compile source bytes
directly, bind receipt digests to those loaded bytes, and ignore poisoned
bytecode.

The generator supports its source-loading CLI launcher and explicit
source-loaded API only. The launcher reads `generate_receipt.py` once, hashes
and compiles that same byte buffer, then invokes its `main`; direct execution or
an ordinary import cannot generate a candidate.

The verifier supports the source-loading CLI launcher and explicit
source-loaded API only. The launcher reads `verify_receipt.py` once, hashes and
compiles that same byte buffer, then invokes its `main`. Direct execution of the
implementation and ordinary Python imports are rejected because neither binds
executed verifier bytes to the recorded digest.

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
