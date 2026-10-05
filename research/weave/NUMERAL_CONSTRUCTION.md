# Weave numeral construction v1

Status: executable numerical representation and replay. The complete iterative
construction using this layer is now [CYCLE.md](CYCLE.md). Neither layer establishes
public/private encryption or universal compression.

## Exact objects

`BitBlock(value, length)` represents ordered bits as an arbitrary-size integer and
its exact bit length. Leading zeros remain part of identity. Byte conversion uses
MSB-first packing; unused low bits in a partial last byte must be zero.

`Entry(symbol, block, angle, circle, recipe=None)` gives a nonempty block a scoped
Unicode private-use reference and exact supplied attachment. Angles are Fractions
in [0,2) turns and occurrence circles are 1..7. This standalone codec does not
invent native geometry. The cycle supplies attachments from real UCNS objects
through the Stack binary-origin candidate.

`Packet(origin, round_id, entries, symbols)` contains definitions and ordered
references. The same symbol may denote different blocks in different scopes.
Definitions, source positions implicit in occurrence order, multiplicity, length
and attachment data remain recoverable without the original input. In the cycle,
references are instead organized into native circle order; the surrounding WAF
record carries native coordinates used to recover source order.

Private-use scalars are aliases, not standardized Unicode numeric values. All
three private-use ranges are admitted. Their actual UTF-8 widths are counted:
three bytes in the BMP range and four in the supplementary ranges. Reference:
https://www.unicode.org/faq/private_use.html

## Prime-path replay

`PrimePath(seed, steps)` supports `('next',)` for the prime at the current prime's
index and `('span', base, start, width)` for an embedded prime-valued span in base
2 or 10. Both source and selected values must be prime. Span offsets are zero-based
from the left; source, base, start and width remain in the recipe, including leading
zero spans. Equal destinations do not erase distinct selection occurrences.

```python
PrimePath(5381, (('span', 10, 0, 2), ('next',), ('next',))).replay()
# (5381, 53, 241, 1523)
```

Literal blocks may be composite. A supplied recipe must reproduce its bound integer
exactly; mismatch never silently becomes a literal. Exact trial division and sieving
perform the admitted work. No automatic compact-recipe finder or nineteenth prime
recursion computation is claimed. The cycle scheduler separately executes these
routes to determine interleave splits.

Default adjustable `Limits`: 64 MiB output, 80 MiB wire, 137468 definitions,
1000000 references, prime index100000, prime value2^32-1, sieve4000000 cells,
256 steps per recipe, and16000000 aggregate prime-work units. Resource refusal
means the chosen execution profile cannot complete that work, not falsification.
Malformed immutable structures raise `Refused`, not `ResourceLimit`. Decode parsing
and validation now share one charged prime engine rather than resetting the budget.

## Self-contained wire and accounting

WNC plus version byte1 carries scope, round, reconstructed bit length, all
definitions and the actual UTF-8 reference stream. Each definition contains its
scalar, exact angle, circle and bit length, then either packed literal bytes or
an executable prime recipe. Canonical unsigned LEB128 metadata fields are limited
to64 bits; arbitrary-size literal values use their packed bytes instead.

`accounting(packet)` reports header, definition, occurrence and total bytes.
The decoder rejects malformed UTF-8, noncanonical integers/fractions, undefined
references, duplicate symbols/angles, wrong lengths, truncation, trailing data,
invalid recipes and exceeded budgets. These structural checks are not authentication.

Observed standalone examples, including all definitions and metadata:

| Case | Original packed bytes | Complete packet bytes |
|---|---:|---:|
| One 8,388,608-bit literal block | 1,048,576 | 1,048,613 |
| Four references to that block | 4,194,304 | 1,048,622 |
| Recipe ending at1523 in16 bits | 2 | 40 |

All recover exactly. The repeated large block saves space; the other examples expand.
A short symbol does not erase the reconstruction information it identifies.

## Usage

```sh
cd research/weave
python numeral.py demo
python numeral.py bind input.bin block.wnc --origin message-1 --angle 1/7 --circle 3
python numeral.py recover block.wnc recovered.bin
python numeral.py inspect block.wnc
python -m unittest discover -s tests -p 'test_numeral*.py' -v
```

`bind` selects the entire supplied file as one block; automatic repeated-sequence
selection belongs to `affixiation.py`. `recover` reports the exact output bit length;
a partial final byte is right-padded with zeros. Existing output files are never
overwritten. Invalid CLI angles such as1/0 now produce concise status2 refusal.

The original15 tests cover exhaustive8191 short blocks, large integers, partial-byte
concatenation, all private-use boundaries, exact prime paths, all seven circles,
malformed input, resource limits and source-deleted new-process recovery. Three
review regressions cover aggregate decode work and error classifications. The full
cycle suite retains all18 alongside its native composition tests.

## hmmm

Native attachment, automatic sequence discovery, corpus normalization and iterative
interleaving are connected in the separately named cycle profile. Automatic short
prime-recipe discovery and an asymmetric private reconstruction advantage remain
unimplemented. Reverting this codec requires retiring or rebinding its cycle consumer;
no discarded bit-per-circle implementation is a supported fallback.
