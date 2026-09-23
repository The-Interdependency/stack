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
- [`urpcs_v1_independent.js`](urpcs_v1_independent.js) — independently structured,
  dependency-free decoder built from the public contract.
- [`vectors/urpcs-v1-vectors.json`](vectors/urpcs-v1-vectors.json) — byte-exact
  positive and negative fixtures.
- [`docs/URPCS-v1-vector-report.md`](docs/URPCS-v1-vector-report.md) — measured
  results, artifact receipts, and claim boundary.
- [`docs/URPCS-v1-independent-decoder-audit.md`](docs/URPCS-v1-independent-decoder-audit.md)
  — frozen independent-decoder sufficiency audit and exact public-input identities.
- [`docs/URPCS-v1-public-contract-repair.md`](docs/URPCS-v1-public-contract-repair.md)
  — repair scope, preservation boundary, and clean-room replay gate.
- [`docs/URPCS-v1-independent-replay.md`](docs/URPCS-v1-independent-replay.md)
  — frozen clean-room replay identities and `SURVIVED_INDEPENDENTLY` result.
- [`urpcs_mobius_projection.py`](urpcs_mobius_projection.py) — read-only adapter
  from authenticated v1 witness displacement rows to the exact UCNS native
  Möbius state.
- [`receipts/urpcs-mobius-projection-v0.json`](receipts/urpcs-mobius-projection-v0.json)
  — canonical deterministic 514-case measurement receipt.
- [`docs/URPCS-mobius-projection-v0.md`](docs/URPCS-mobius-projection-v0.md)
  — generated human-readable summary of that canonical JSON.
- [`SOURCE_RECEIPT.json`](SOURCE_RECEIPT.json) — imported-artifact identities.

The measurement receipt lives in the new `receipts/` evidence directory while
its Markdown projection remains with the existing human-readable reports in
`docs/`. A duplicate Markdown file is intentionally not stored in `receipts/`.

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

Run the independent decoder checks:

```bash
node research/urpcs/urpcs_v1_independent.js --kat
node research/urpcs/tests/test_independent_decoder.js
```

Run the bounded Möbius projection tests:

```bash
python3 -m unittest -v research/urpcs/tests/test_mobius_projection.py
```

The complete receipt was generated against detached source worktrees at UCNS
`4086ab82399c4d142b0eacfbc09e0a69ed151aa5` and skill-lib
`abd259b4722901317e4388d774a20d6819d959c2`. The canonical run used Python
3.12 and PyCryptodome 3.23.0 after matching its KMAC256 output to the embedded
NIST SP 800-185 known-answer vector and the dependency-free URPCS
implementation. PyCryptodome is an execution accelerator, not a protocol
dependency; the tests use the frozen dependency-free implementation.

```bash
python3 research/urpcs/urpcs_mobius_projection.py \
  --stack-root . \
  --ucns-root /path/to/ucns-at-4086ab8 \
  --skill-lib-root /path/to/skill-lib-at-abd259b \
  --jobs 2 \
  --kmac-backend pycryptodome \
  --write-receipt research/urpcs/receipts/urpcs-mobius-projection-v0.json \
  --write-report research/urpcs/docs/URPCS-mobius-projection-v0.md
```

## Verified reference result

- 8/8 named fixtures pass.
- All 256 one-byte plaintexts round-trip at depth zero.
- The KMAC256 implementation passes the embedded known-answer check.
- Regenerated vector JSON is byte-identical to the committed artifact.
- Empty input at depth one produces a 146,210-byte authenticated frame.

The last result makes the resource boundary concrete: this is not a compressor,
and greater depths require a separately justified permitted-domain cap.

## Verified independent result

- `empty_r0`, `empty_r1`, and `odd_09_r0` reproduce the committed plaintext,
  deterministic receipt, and complete successor state.
- Wrong associated data and an authenticated-body mutation are rejected at tag
  verification before state advance.
- The independent KMAC256 implementation matches NIST SP 800-185 Sample #4 and
  an external OpenSSL `KMAC-256` result.
- The decoder was frozen before the first ciphertext comparison and required no
  correction afterward.

## Verified bounded Möbius measurement

- All 514 declared plaintext/depth cases completed under the frozen harness.
- 288,615 gonol states and 546,956 member states were projected with exact
  integer/rational arithmetic and checked against UCNS
  `native_mobius_state(Fraction(S, M))`.
- Gonol/member maximum unreduced displacements were 2/6; both maximum Euclidean
  quotients were zero.
- No phase bucket contained both local frames. The result is
  `DISTINCTION_ABSENT_IN_BOUNDED_DOMAIN`.
- This zero result ends integration for the bounded profile. No traversal path,
  frame field, protocol profile, or inactive semantic stub was added.

## Next gates

1. A threat model and leakage model must precede any confidentiality claim.
2. Host-side durable compare-and-swap, crash recovery, rollback resistance, and
   fork policy require implementation and adversarial testing.
3. Any future relation to PCEA or UCNS requires a separate authority-bearing law;
   repository proximity supplies none.
4. A Möbius-frame-sensitive traversal experiment is not authorized by the
   completed bounded measurement because no opposite-frame phase split occurred.

## hmmm

The frozen audit remains `BLOCKED_NOT_INDEPENDENTLY_SPECIFIED` for its old input.
After the public contract repair, the clean-room replay is
`SURVIVED_INDEPENDENTLY` for the committed bounded profile. Confidentiality,
durable host state, production security, and release authority remain open.
The complete Möbius scan found no opposite-frame phase split in this fixed
harness; whether one occurs outside the bounded domain remains unresolved and
does not authorize integration.
