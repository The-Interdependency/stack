# URPCS v1 recursive pairing codec research

URPCS is a **stack-local authenticated codec experiment**. Laws 1–13 define a
recursive pairing/witness format, deterministic framing, integrity verification,
and linear state advance. The committed reference implementation and vectors
exercise that bounded construction.

Standing: **COMPUTATION; research, not canon**.

The evidence supports deterministic round-trip behavior for the frozen harness.
It does not establish confidentiality, production suitability, PCEA compatibility,
UCNS geometry, or UCNS-gonol identity.

## Placement and authority

- `The-Interdependency/stack` owns this research workspace and its reference code.
- `The-Interdependency/skill-lib` supplies build, evidence, domain-claim, and
  stack-update discipline; it supplies no codec or security result.
- KMAC256 follows [NIST SP 800-185](https://csrc.nist.gov/pubs/sp/800/185/final)
  and its SHA-3/KECCAK dependency follows
  [FIPS 202](https://csrc.nist.gov/pubs/fips/202/final).
- PCEA remains a separate project. No PCEA construction is imported here.
- A `Gonol` row in URPCS is a codec-local layer record. It is not a UCNS gonol and
  carries no UCNS constructor or geometry authority.

`URPCS` is a despecified handle in v1. No lexical expansion is canonical.
[`DOMAIN_CLAIM.json`](DOMAIN_CLAIM.json) owns that boundary.

## Artifacts

- [`docs/urpcs-v1-spec.md`](docs/urpcs-v1-spec.md) — normative public Laws 1–13,
  complete forward/reverse composition, and exact wire/state rules.
- [`urpcs_v1_reference.py`](urpcs_v1_reference.py) — dependency-free reference
  encoder, decoder, state advance, and fixture generator.
- [`vectors/urpcs-v1-vectors.json`](vectors/urpcs-v1-vectors.json) — byte-exact
  positive and negative fixtures.
- [`docs/URPCS-v1-vector-report.md`](docs/URPCS-v1-vector-report.md) — measured
  results, artifact receipts, and claim boundary.
- [`docs/URPCS-v1-independent-decoder-audit.md`](docs/URPCS-v1-independent-decoder-audit.md)
  — frozen independent-decoder sufficiency audit and exact public-input identities.
- [`docs/URPCS-v1-public-contract-repair.md`](docs/URPCS-v1-public-contract-repair.md)
  — repair scope, preservation boundary, and clean-room replay gate.
- [`SOURCE_RECEIPT.json`](SOURCE_RECEIPT.json) — imported-artifact identities.

## Usage guidance

Run the reference checks:

```bash
python3 research/urpcs/urpcs_v1_reference.py --self-test
python3 -m unittest discover -s research/urpcs/tests -p 'test*.py'
```

Regenerate the vector file without overwriting the committed evidence first:

```bash
python3 research/urpcs/urpcs_v1_reference.py \
  --write-vectors /tmp/urpcs-v1-vectors.json
cmp /tmp/urpcs-v1-vectors.json \
  research/urpcs/vectors/urpcs-v1-vectors.json
```

The harness accepts at most one plaintext byte and recursion depth one. It is an
interoperability fixture, not an application API.

## Verified reference result

- 8/8 named fixtures pass.
- All 256 one-byte plaintexts round-trip at depth zero.
- The KMAC256 implementation passes the embedded known-answer check.
- Regenerated vector JSON is byte-identical to the committed artifact.
- Empty input at depth one produces a 146,210-byte authenticated frame.

The last result makes the resource boundary concrete: this is not a compressor,
and greater depths require a separately justified permitted-domain cap.

## Next gates

1. Run a fresh clean-room decoder audit using the repaired public specification
   as its only URPCS law source; compare expected outputs only after freezing the
   implementation.
2. A threat model and leakage model must precede any confidentiality claim.
3. Host-side durable compare-and-swap, crash recovery, rollback resistance, and
   fork policy require implementation and adversarial testing.
4. Any future relation to PCEA or UCNS requires a separate authority-bearing law;
   repository proximity supplies none.

## hmmm

The frozen audit is `BLOCKED_NOT_INDEPENDENTLY_SPECIFIED` for its old input. The
public contract has since been repaired without changing reference code or
vectors. Independent interoperability remains the next gate: the door is now
specified, but a clean-room implementation still has to walk through it.
