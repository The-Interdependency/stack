# URPCS v1 public-contract repair

**Classification:** `REPAIRED_AWAITING_INDEPENDENT_REPLAY`

The frozen independent-decoder audit correctly found that the public sheet at
commit `db5635c7d48652d6506c3bd343f8ead0bb53872e` named Laws 1 and 3–12 without
publishing their executable rules. This repair changes the public specification,
not that historical audit.

## Repaired surface

`docs/urpcs-v1-spec.md` now states:

1. the complete `URPCS001` bootstrap header and witness/body boundary;
2. Laws 3–8 for identifiers, occurrence selection, keyed pairing, gonol
   formation, attachment, displacement, and phase;
3. the `URGON001` layer schema, canonical parsing, and reverse-layer algorithm;
4. the exact-depth halt rule;
5. the complete `URPCF001` header and URPCS KMAC256 authentication transcript;
6. the receipt transcript and deterministic derivation of all successor-state
   fields, including the concrete v1 `Avoid` rule;
7. complete forward and reverse compositions and fail-before-advance ordering.

The `Avoid` text exposes the behavior already shipped by v1: interpret the
32-byte candidate as a big-endian integer and choose the first value among
`candidate+i mod 2^256`, for `i=0..|F|`, that is absent from the forbidden set.
Publishing that rule changes no reference bytes or committed vectors.

## Repair identities

These identities were measured after the normative repair and before commit:

| artifact | bytes | SHA-256 |
|---|---:|---|
| `docs/urpcs-v1-spec.md` | 20,265 | `295cd721a19475e683b1831f1a15b3c7eed521cec551d68cd031bfed4757423e` |
| `tests/test_public_contract.py` | 2,123 | `f13355f15e244f26f6ceef5a815280a0164e2acfef4d31bbe0ef7f98bcdba55f` |
| frozen independent audit | 9,853 | `92a2b4311d788fc5d03c4738e7b8a234c4c21b3c0f76384d0ba8081451341bd2` |
| reference implementation | 42,390 | `3cdd63a60bc0740b059015f3f442e495ac8ff6a2a6be27f0d54b4eed2eaf9d3b` |
| committed vectors | 904,545 | `1d96299a016feed6f2e0881a5d4d21c20229714dab5eaa9338008d5282c2dfe6` |

The reference and vector paths have no diff from repair base
`0131f6476148866ea8a53b6c12871d8754193de5`.

## Preservation

- `URPCS-v1-independent-decoder-audit.md` remains byte-for-byte historical
  evidence for its frozen input.
- The reference implementation and vector JSON are unchanged by this repair.
- The source receipt remains the immutable PR #44 integration snapshot.
- Confidentiality, production suitability, and independent interoperability
  remain unclaimed.

## Verification gate

The next decisive test is a clean implementation that reads the repaired public
specification before reading any reference source or expected outputs. It should
consume only each fixture's ciphertext, initial state, and associated data, then
compare recovered plaintext, receipt, successor state, and negative rejection
after its implementation is frozen.

Until that replay succeeds, this repair establishes contract completeness as a
reviewed documentation result, not decoder interoperability.

## hmmm

The blocker was a missing public road, not a failed vehicle. The road is now
drawn; a driver who has never seen the reference engine must still traverse it.
