# Weave: byte-scoped whole-plus-seven repair

Status: **structural repair implemented; native positional cipher not implemented**.
This replaces the incorrect active constructions from Stack PRs #73 and #74.
The next proposed answers are in [QUESTIONS.md](QUESTIONS.md); none is silently enabled.

## Settled construction

Each raw-byte message is an origin. Each byte occurrence participates at that origin
as one eight-bit unit, with one big circle G0 and seven small circles G1 through G7.
One source bit participates through each circle. The big circle is both a bit-bearing
member and the retained whole; its dynamic role must not be replaced by metadata,
a fixed reference, or a checksum.

Every public two-circle view contains G0 and exactly one Gi, with 1 <= i <= 7.
There are seven possible whole-part views, not four disjoint pairs. This does not
require emitting all seven views, fix a visitation order, or assign one pair per bit.

Every circle has the complete 720-degree return. Its relationship to space is
instantiated by the key set, not fixed by a universal placement formula. The full
key retains the eight-circle configuration; the public object exposes two circles
at a time. Deriving the actual cryptographic public object is distinct from enforcing
that pair shape.

The stated expansion remains **8 source bits -> 16 ciphertext bits per byte**. It is
a requirement, not an implemented serializer and not a consequence of the number of
circles alone. The removed per-bit duplication did not implement this requirement
for the correct reason.

## Executable repair

`stages/eight_circle.py` now has byte-level construction records:

- `Circle` stores a key-set circle binding and exact space coordinate. It is not a
  replacement UCNS Gonol constructor. One scalar coordinate is not the complete
  native relationship to space.
- `FullKeySet` accepts eight bindings and an explicit source-bit/circle assignment.
  `degenerate(i)` can produce only `(G0, Gi)`; direct `PublicPair` construction also
  rejects a missing whole, repeated whole, extra member, or malformed circle.
- `construct_byte` accepts a complete byte and eight caller-supplied exact positions,
  preserving each source bit once. It emits a plaintext-bearing construction record,
  **not ciphertext**. `source_value` reads that retained source, not a private inverse.
- Positions are stored as exact rational turns modulo two: a 360-degree displacement
  stays distinct, while the complete 720-degree return agrees. No sheet threshold
  converts bit values into public output codes.

`stages/message_origin.py` now contains one ordered participant per **byte**.
`construct_at` attaches that complete byte's eight placements at its message-origin
occurrence. Repeated values preserve their separate occurrence indices. The supplied
origin name is a namespace, not content hashing, nonce generation, or a secrecy claim.

The invented `CouplingKey`, public-feedback recurrence, per-bit `MessageAxis`,
`CoupledWitness`, bitwise `encode`/`decode`, and `public_recover` have been removed.
Their supported replacement is the corrected byte/star structure, not another cipher
substitute. The existing transport experiment and full-profile missing-operation
refusal remain separate and unchanged.

## What this repair does not implement

The real native origin-axis binding, full relational circle-space state, key generation,
whole-byte positional transformation, dynamic G0 evolution, cryptographic degeneration,
private reconstruction and 16-bit ciphertext layout are not implemented by these records.
No claim is made that merely requiring a `FullKeySet` argument makes its hidden circles
necessary for recovery. The next questions concern these actual operations.

UCNS retains geometry authority. UCHC origin-axis architecture remains the intended
construction dependency; this repair does **not** claim to execute UCHC by copying a
language source or relabeling occurrence metadata. Existing Stack/UCHC implementation
and migration boundaries are unchanged. No `libs/` source or source pin is changed.

## Corrected evidence scope

PR #73 encoded each individual source bit into two public sheet bits. PR #74 then
added public feedback to that wrong unit. Those programs were publicly recoverable,
but neither represented the requested byte-scoped construction. Their failures are
not falsifications of Weave, and their successful tests did not establish that the
requested geometry or message-origin construction had been implemented.

The former hidden-circle perturbation conclusion was also invalid. For a public-only
sender, encryption is a function of its public key, message and explicit public-side
inputs/randomness. Holding all those inputs fixed holds its output fixed regardless
of changes to unavailable private records. That observation cannot establish whether
private information is necessary for inversion. A correct test must examine recovery
and unauthorized inversion for the actual forward/recovery relation, accounting for
valid or equivalent keys rather than demanding arbitrary private changes alter a
public sender's output.

Historical source remains in Git at:

- PR #73 merge: `a3836f5632ed3babe1bc8c3dbebab60186c2bc78`;
- PR #74 merge and repair base: `92ccda0620c06bc46654939c061ceb2d36476cb9`.

These are provenance for removed implementations, not live capability or security
claims. Their invalid observations are not copied into the current security results.

## File plan and verification

The repair changes only `research/weave`: the two structural modules, their two test
modules, the existing full-suite receipt runner, this document, the question register,
and the specification. It removes the stale `verify.py` command from the specification.
Roll back as one transaction; restoring a deprecated encoder is not an accepted
recovery path. Other Weave layers and independent stage switches remain intact.

Focused coverage: all 256 byte values, all 40,320 source-bit/circle assignments, all
seven whole-plus-part views, direct-constructor validation, exact coordinates, source
occurrence preservation, and removal of the old callable cipher surfaces. These are
construction tests, not claims about attack resistance. Full expected test inventory:
52 existing methods plus 22 byte/star/message methods = 74.

## Usage guidance

From `research/weave/`:

```python
from fractions import Fraction
from stages.eight_circle import Circle, FullKeySet
from stages.message_origin import construct_origin, construct_at

# Explicit, nonsecret structural fixture: NOT key generation or encryption.
full = FullKeySet(
    tuple(Circle(i, f"G{i}", Fraction(i, 9)) for i in range(8)),
    (7, 2, 5, 0, 3, 1, 6, 4),
)
origin = construct_origin(b"AA", identity="example-message")
positions = tuple(Fraction(i, 7) for i in range(8))
byte_state = construct_at(origin, 0, full, positions)
assert byte_state.source_value == 65
assert full.degenerate(3).indices == (0, 3)
assert len(origin.bytesets) == 2
```

```bash
python -m unittest discover -s tests -p 'test_eight_circle.py'
python -m unittest discover -s tests -p 'test_message_origin.py'
python test.py --receipt /tmp/weave-check.json
```

The repair follows the source-preservation, native-first metadata, removal and
verification boundaries of the loaded skill-lib instructions. Skill usage-counter
persistence is not available in this runtime; no exposure count is fabricated.

## hmmm

Q11-Q14 and carried-forward Q9 await approval. The concrete forward/private-recovery
operation remains research work, not something created by approving its description.
