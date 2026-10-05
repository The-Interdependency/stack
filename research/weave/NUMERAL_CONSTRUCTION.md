# Weave numeral construction v1

Status: executable representation/replay layer; not an encryption implementation.
Starting Stack revision: `d0e76d58f832a5664578af39103cdd0697c091d3`.

## Current construction and placement

The latest user clarification controls this work:

1. Normalize the message's bit length using corpus material.
2. Parse repeated multi-byte sequences. Save each selected sequence at an angle
   on the eighth/origin circle; a circle among the seven records its occurrences
   and their order.
3. First/last interleave the resulting bitstream. Repeat steps 2 and 3.

The proposed numerical extension makes a selected bit block one exact integer,
then uses a Unicode symbol to refer to its recoverable definition. Prime-index
continuation and embedded prime spans can supply executable recipes. This layer
constructs that extension, not the whole cycle or a replacement cryptosystem.

The earlier bit-per-circle interpretation does not constrain this layer. A byte
is eight bits; a selected multi-byte sequence remains an ordered sequence. Neither
one-bit-per-circle assignment nor per-bit public substitution is introduced.
No fixed total expansion follows from this representation; all wire bytes are
measured. Earlier whole-cipher length proposals require whole-cycle accounting.

## Delivered objects

`BitBlock(value, length)` holds exact bits, including leading zeros and partial
bytes. Values are arbitrary-size Python integers, never decimal floats or hashes.
`BitBlock.from_bytes` and `to_bytes` use MSB-first packing and explicit bit length.
Nonzero unused padding is rejected.

`Entry(symbol, block, angle, circle, recipe=None)` binds a private-use Unicode
scalar to a block and its caller-supplied exact angular attachment. `circle` is
one of the seven occurrence circles. The angle is a rational in [0,2) turns,
retaining the 720-degree coordinate distinction without inventing a UCNS law.
The origin/circle fields are attachment records, not native geometric objects.
This module does not claim to construct a UCNS Gonol or consume a UCHC constructor.

`Packet(origin, round_id, entries, symbols)` stores the scoped definitions and
ordered occurrences. `origin` is a caller's scope identifier, not a substitute
geometric origin. Repeated references preserve multiplicity. Their exact offsets
and per-circle order are derived from the stream and block lengths, not duplicated
in a second source of truth. The table can represent residual material as literal
entries as well. Participant selection and repeated-sequence parsing remain with
the caller; no fixed chunking rule is silently installed.

Symbols are aliases, not Unicode's standardized numeric values. All three private-
use ranges are supported. BMP aliases take three UTF-8 bytes; supplementary aliases
four. Unicode private-use semantics and ranges are defined at:
https://www.unicode.org/faq/private_use.html

## Exact prime recipes

`PrimePath(seed, steps)` supports two explicitly selected operations:

- `('next',)` replaces the current prime by the prime at that index.
- `('span', base, start, width)` selects a contiguous span from the current
  prime's canonical base-2 or base-10 numeral. Both the source and selected value
  must be prime. Start is zero-based from the left. The original span position
  and width remain in the recipe, including when the span has leading zeros.

For example:

```python
PrimePath(5381, (('span', 10, 0, 2), ('next',), ('next',)))
# Exact replay: 5381 -> 53 -> 241 -> 1523
```

Different occurrences leading to the same destination are distinct recipes. The
source prime, base, start, and width survive serialization; the destination alone
does not replace the route. The evaluator uses exact trial division and sieving,
not a probable-prime verdict or a published answer substituted for computation.
Literal blocks need not be prime. No automatic search claims every block has a
short prime recipe. A supplied recipe must reconstruct its bound integer exactly;
mismatch never silently falls back to a literal.

Default recipe limits are operational: index 100,000; prime value 2^32-1;
4,000,000 sieve bytes; 256 steps per recipe; 16,000,000 aggregate work units per
packet validation/replay. Work units conservatively count trial divisors, sieve
cells, and recipe steps. Budgets are adjustable via `Limits`. Exceeding one is
`ResourceLimit`, not evidence against the proposed prime construction. The
nineteenth prime recursion is not claimed executed by this evaluator.

## Wire and accounting

The self-contained versioned binary record starts with `WNC` followed by byte 1.
It contains origin scope, round, total reconstructed bit length, every definition,
and the actual UTF-8 occurrence stream. A definition carries its Unicode scalar,
exact angle, occurrence-circle number, bit length, and either packed literal bits
or a prime recipe. Recipes replace literal payload bytes, not their length field.
Unsigned metadata integers have canonical unsigned LEB128 encoding within 64 bits;
this limit does not constrain the size of literal integer values.

`accounting(packet)` reports source bits, packed source bytes, header bytes,
definition bytes, occurrence bytes, and total bytes. Everything necessary for this
layer's reconstruction is included. No external dictionary, original-message
copy, producer trace, or hidden corpus is needed. This is intentionally not a
choice of public/private exposure for the eventual cipher.

The decoder rejects malformed UTF-8, noncanonical integers/fractions, undefined
symbols, duplicate symbols or angles, wrong lengths, truncation, trailing data,
invalid prime steps, and over-budget operations. It sizes literal wire allocation
before producing it and checks total reconstructed length before output allocation.
A structurally valid modification can produce a different message: syntax checks
are not authentication, and private-use naming does not create secrecy.

## Usage

Python 3.11+ standard library only; no install or network dependency.

```bash
cd research/weave
python numeral.py demo
python numeral.py bind input.bin block.wnc --origin message-1 --angle 1/7 --circle 3
python numeral.py inspect block.wnc
python numeral.py recover block.wnc recovered.bin
python -m unittest discover -s tests -p test_numeral.py -v
python test.py --receipt /tmp/weave-check.json
```

`bind` treats the supplied file as one block; it is not an automatic compressor.
The symbol is U+E000 within the supplied scope. The angle/circle are required inputs.
For multiple selected blocks and repeated references, use `Entry` and `Packet`:

```python
from fractions import Fraction
from numeral import BitBlock, Entry, Packet, encode, decode, accounting

block = BitBlock.from_bytes(b'ABCD' * 256)
entry = Entry(chr(0xE000), block, Fraction(1, 7), 3)
packet = Packet('message-1', 0, (entry,), entry.symbol * 4)
wire = encode(packet)
assert decode(wire).restore().to_bytes() == b'ABCD' * 1024
print(accounting(packet))
```

Output files use exclusive creation and are never overwritten. `recover` reports
exact output bit length; a partial final byte is right-padded with zeros. Keep that
reported length when using non-byte-aligned API inputs. Default CLI input/output
budgets are finite; library callers may supply an explicit `Limits` profile.

## Evidence and interpretation

The 15 new tests include all 8,191 bit blocks of lengths 0 through 12; mixed partial-
byte concatenation; an 8,388,608-bit integer; four repeated large-block occurrences;
all seven occurrence circles; all private-use range boundaries; exact prime-index
and decimal/binary span replay; scope distinction; malformed input and aggregate
resource refusal; and new-process recovery after the source file is deleted.

The nonsecret demo measured:

| Case | Packed source bytes | All packet bytes | Exact recovery |
|---|---:|---:|---|
| One 8,388,608-bit literal block | 1,048,576 | 1,048,613 | yes |
| Four references to that block | 4,194,304 | 1,048,622 | yes |
| Prime recipe ending at 1523, length 16 | 2 | 40 | yes |

A single glyph is genuinely a short reference, not a claim that the complete
packet is that small. The small prime example expands after accounting. Repetition
produces a real saving in the large-block example. No universal compression,
asymmetric advantage, or cryptographic-strength result follows from these tests.

## File plan and rollout

- `numeral.py`: constructor, exact evaluator, codec, accounting, CLI. Main risks:
  lost bit length, unresolved aliases, recipe mismatch, and excessive decode work.
- `tests/test_numeral.py`: witnesses for those boundaries and separate-process replay.
- `test.py`: add all 15 methods to the existing workspace test gate; no skipped tests.
- `SPECIFICATION.md`: point the active clarification at sequence/occurrence semantics.
- This document: usage, source attribution, scope, and explicit construction choices.

This is opt-in research. It does not fill any missing native encryption operator,
alter the transport experiment, select key material, or modify UCNS/UCHC authority.
Rollback removes this module/tests/link and adjusts the test inventory. Existing
sealed evidence remains tied to its original sources.

## hmmm

Automatic discovery of compact prime recipes, native origin/axis attachment, and
integration with corpus normalization, repeated-sequence parsing, and the iterative
interleave cycle remain separate construction work. The numeric-reference layer
now runs end to end and exposes its actual cost; it is not the whole Weave cipher.
