# Weave eight-circle / two-circle candidate

Status: **implemented candidate; asymmetric security not established.**

This construction records the current user-specified boundary without adding a
selection law that has not been supplied.

## Preserved construction

For each raw byte:

- the byte is eight bits;
- one whole circle plus seven derived circles form the full eight-circle key-set state;
- every circle has an exact 720-degree return;
- every circle has its own relationship to space, and that relationship belongs to the
  concrete key set rather than to a universal law;
- the full/private key set contains all eight circles;
- a degenerate public view exposes exactly two circles at a time;
- the two public circles produce two transmitted witness bits for each source bit,
  therefore one eight-bit byte produces sixteen transmitted bits.

The implementation uses exact rational turns: 0 <= phase < 2, with 1 turn equal to
360 degrees and 2 turns equal to the complete 720-degree return. This is an executable
representation of positions, not a claim that the mathematical circle has finitely
many possible positions.

No rule is imposed for how key sets choose their circle positions, their relations to
space, or which two circles are exposed. Those are construction-instance data.

## Executable object

`stages/eight_circle.py` provides:

- `Circle`: exact 720-degree position, zero/one positions, and key-set-specific space relation;
- `FullKeySet`: exactly eight distinct circles;
- `FullKeySet.degenerate(i, j)`: exactly two-circle public projection;
- `encode_byte`: eight source bits -> sixteen positional witness bits;
- `decode_byte`: full-key-set recovery API;
- raw-byte `encode` / `decode` helpers.

The candidate is deliberately separate from the older transport profile and is not
silently installed as the complete Weave `bind` law.

## Falsification already obtained

The first independent-bit implementation fails the intended asymmetric property.

Because each source bit is independently mapped to one of two public two-bit witnesses,
a holder of the public pair can evaluate the public forward image of 0 and 1 and recover
every source bit by comparison. The test
`test_independent_bit_baseline_is_publicly_bruteforceable` preserves that attack as
required evidence.

Therefore:

[
8 \to 2
]

is implemented as a geometric degeneration, but **independent per-bit projection is
falsified as the cryptographic relation**.

This does not falsify the eight-circle construction. It identifies what the next
construction must actually use: the message-scoped UCHC origin/axis relational state
must couple the eight circles so that the six omitted circles change the recoverable
trajectory rather than merely sitting unused in the private object.

## hmmm

The remaining construction is the coupled UCHC relation itself. No additional policy
decision is introduced here. The next candidate must make the full eight-circle state
causally necessary for inversion and then be attacked.
