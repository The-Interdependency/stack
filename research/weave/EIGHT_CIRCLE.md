# Weave eight-circle / two-circle candidate

Status: **implemented construction research; asymmetric security not established.**

This workspace preserves the current Weave geometry and records candidate failures
instead of silently promoting them into a cipher.

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

## Executable geometry

`stages/eight_circle.py` provides:

- `Circle`: exact 720-degree position, zero/one positions, and key-set-specific space relation;
- `FullKeySet`: exactly eight distinct circles;
- `FullKeySet.degenerate(i, j)`: exactly two-circle public projection;
- `encode_byte`: eight source bits -> sixteen positional witness bits;
- `decode_byte`: full-key-set recovery API;
- raw-byte `encode` / `decode` helpers.

The candidate remains separate from the older transport profile and is not silently
installed as the complete Weave `bind` law.

## Message origin / UCHC-axis candidate

`stages/message_origin.py` consumes the UCHC architectural distinction currently
implemented in `The-Interdependency/uchc`:

- participants are individually addressable axes at one declared origin;
- axis identity follows construction/admission order;
- occurrence identity is preserved;
- attachment happens at the participation point;
- unresolved cross-origin geometry is not silently promoted.

For Weave, one raw-byte message constructs one origin `O_M`. Every source-bit
occurrence participates as its own ordered axis at that origin. The candidate then
uses exact key-set-specific phase/feedback parameters to couple successive axes before
the same two-circle public degeneration is applied.

Usage:

```python
origin = construct_origin(raw_bytes)
witness = encode(raw_bytes, public_pair, coupling_key)
```

The phase recurrence is deliberately a bounded Weave candidate, not UCNS or UCHC
canon. It is present so the message-origin construction can be executed and attacked.

## Falsifications obtained

### Independent-bit projection

The first independent-bit implementation fails the intended asymmetric property.
A public holder can evaluate the two public forward images for 0 and 1 and recover
every source bit directly.

Therefore the bare geometry

```text
8 full circles -> 2 public circles
```

survives, while independent per-bit projection is falsified as the cryptographic
relation.

### Message-origin coupling

The second candidate adds the message-scoped origin and ordered axis trajectory.
That preserves the requested topology, but it still fails the asymmetric requirement:
the sender's public coupling parameters and public two-circle state are sufficient to
replay the trajectory and recover the message.

The tests additionally perturb all six omitted circles while holding the two public
circles fixed. The ciphertext is unchanged. Therefore the six private circles are
**not causal** in this candidate.

This is a useful narrowing result:

```text
message origin + ordered axes + public feedback
!=
trapdoor degeneration/lift
```

The UCHC architecture supplies the origin/axis topology. It does not, by itself,
supply the missing asymmetric mathematical relation.

## Authority and provenance

UCHC source inspected for this candidate:
`human/english/english_gonol/hyperspace_construct.py`,
Git blob `8b55823805c87ad8c4cc9d7451dc2eb90bdedd3a`.

The source explicitly keeps carrier position and axis participation distinct and
leaves cross-origin angles / continuum lift-selection as `hmmm`. Weave therefore
does not invent those as UCNS/UCHC laws.

Relevant construction discipline was read from
`The-Interdependency/skill-lib` `gonol-build/SKILL.md` and
`the-interdependency/SKILL.md`. Current METAPAT was consulted before selecting the
candidate relation; its boundary-state guidance permits a domain boundary/state to
alter a transformation only where the domain evidence supplies the mechanism. No
METAPAT security claim is inferred.

## Usage guidance

Run all Weave evidence:

```bash
cd research/weave
python test.py --receipt /tmp/weave-check.json
```

Run only the message-origin candidate:

```bash
python -m unittest tests.test_message_origin
```

Interpret a passing run as reproducibility of the candidate and its falsification
witnesses, not evidence of cryptographic strength.

## hmmm

The remaining construction is now narrower than "couple the message."

We need a **native degeneration/lift relation** in which:

- the public two-circle object permits the forward operation;
- the six omitted circles materially alter the full lift;
- the full eight-circle key can recover the lift efficiently;
- the public two-circle holder cannot replay the same inverse efficiently.

No additional circle-selection or space-placement policy is required before that
relation is constructed. The relation itself is the unresolved work.
