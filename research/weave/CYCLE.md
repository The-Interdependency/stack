# Weave iterative sequence cycle v1

Status: executable construction and exact recovery. Public/private asymmetric
key generation and cryptographic security are not implemented by this profile.

## The complete implemented path

1. Normalize once using actual corpus bits. Preserve the exact original byte
   length inside the normalized frame.
2. Discover repeated multi-byte sequences in the current byte stream. Select
   nonoverlapping occurrences, retaining every residual byte.
3. Close the sequences through the Stack binary-domain candidate. The eighth/whole
   circle holds native sequence attachments; seven occurrence circles hold count,
   order and native positions. Sequential byte occurrences remain addressable axes.
4. Bind definitions through the existing length-bearing integer/Unicode numeral
   layer. Emit the seven native occurrence-circle streams and the positions needed
   to reconstruct source order. Include every definition and relation in accounting.
5. Execute the configured prime-index and embedded-prime-span route. Derive the
   section arity and exact nonempty bit boundaries from that route and current size.
6. First/last interleave the bits within each section. Feed those actual rearranged
   bytes into step 2 of the next round.

Reverse performs the last bit permutation's inverse, native sequence-position
recovery, preceding rounds in reverse order, and corpus denormalization. The only
inputs are the final record, the same supplied profile/material, and pinned producer
sources. Original plaintext and an untransmitted encoder trace are not accepted.

This implements the corrected normalization/affixiation/interleave cycle, not all
historical proposals or a disguised replacement cryptosystem. There is no
one-bit-per-circle mapping, two-bit substitution, fixed 16-bit byte codeword,
conventional cipher fallback, or inferred twofold expansion.

## Explicit implementation profiles

The following choices make the construction executable and are named/versioned,
not attributed to the user as universal laws:

- **corpus-tail bucket normalization:** frame the original byte length and a corpus
  source digest with the message, then fill the next strictly larger configured
  bucket with actual cyclic corpus bits starting at the configured bit offset.
  At least one filler byte is used. The source digest is not the corpus substitute:
  the actual filler is checked during recovery. The public format is research only.
- **maximal-lcp-longest-first-v1:** suffix-array/LCP discovery, longest candidates
  first, with earliest-source tie breaking and leftmost nonoverlapping selection.
  Counts mean selected partition occurrences, not all overlapping substring matches.
  No fixed chunk length or silent candidate truncation is introduced. This is not
  a globally optimal compression claim.
- **native binary attachment:** The Stack candidate attaches each saved sequence at its first
  selected occurrence's native byte axis. UCNS owns the exact `r/N` axis position
  and complete 720-degree state. Source data, occurrences and native objects remain
  inside the construction; hashes merely identify it.
- **circle assignment:** definition admission order indexes the profile's explicit
  permutation of circles 1..7. Eight configured exact fractions govern native
  circle-space displacement, including the whole circle at index 0.
- **prime-route-compositions-v1:** execute the full prime path, including every
  source/span position and returned value. A prefix-bearing radix numeral of those
  route tokens selects among explicit candidate arities and ranks an ordered
  composition of the actual bit length. Different routes may select the same map;
  no secret entropy is inferred from the size of the determinant.
- **end order:** `first-last` is explicit in the sample profile, matching the latest
  clarified cycle. `last-first` remains supported and separate. Historical transport
  ordering is not silently changed.

All choices are visible in `profiles/cycle-v1.json`, the named implementation
profiles, or the native producer documentation. They can be replaced under a new
profile identity without redefining UCNS or UCHC geometry.

## Native dependency boundary

`CYCLE_NATIVE.json` v2 binds the exact local `native_binary.py` blob and its two
unchanged UCNS producer modules at `905e66964a495d7596a577bb64e4158db9465864`.
`cycle_native.py` executes a fresh copy of each verified buffer on every load;
mutable `sys.modules` cache slots are never accepted as source evidence.

The binary-origin/sequence implementation remains in its owning Stack forge.
UCHC `4ad94e92be10d2c4c875a848addfda46f3c7cfdb` supplies the architecture and
migration boundary, not a graduated binary runtime. The premature UCHC #7 code
is retained as provenance in `NATIVE_BINARY_PROVENANCE.json` and replaced by the
repaired forge-owned candidate. No English/Python migration or UCNS authority moves.

Actual UCNS `AxisCirclePosition` and `NativeMobiusState` objects construct and
recover positions. The eighth remains the whole/origin; seven circle streams
preserve sequence occurrence order. `SequenceTable` validates source, order,
definitions, every occurrence, and native positions including space offsets on
construction and before exporting a receipt or reconstruction. A frozen record
with a forged relation is rejected, including through `dataclasses.replace`.

The v2 lock and binary-domain identity deliberately reject records from the old
ungraduated candidate. Rebuild research records using this exact profile/source.
Native representation is not authentication, a trapdoor, or a security claim.

## Framing and full size accounting

`WVC` + version byte 1 identifies the outer cycle record. It binds native-source lock,
profile identity, retained message-origin receipt, round count and final payload.
The original-length/corpus frame is inside the repeated transformations, not an
unreported external reconstruction file.

Each `WAF` + version byte 1 affixiation record contains source byte length, a complete
numeral packet, seven occurrence counts and exact native source-position fractions.
The numeral occurrence stream is in native circle order, NOT plaintext order.
The next round consumes the entire preceding permuted record, including information
that will be needed to undo earlier rounds. No hidden sidecar or overwritten history.

An attached Unicode symbol is a scoped reference, not one byte containing arbitrary
information. All its definitions and actual UTF-8 bytes are counted. Research
source/profile digests and structural rejection are not authentication.

The three-round nonsecret demo measured 784 original bytes, normalized to 1,024:

| Round | Input bytes | Definitions | Selected occurrences | Complete output bytes |
|---|---:|---:|---:|---:|
| 0 | 1,024 | 8 | 11 | 910 |
| 1 | 910 | 41 | 56 | 1,669 |
| 2 | 1,669 | 231 | 321 | 6,632 |

The outer frame adds 103 bytes: total **6,735 bytes**, with exact recovery.
This example expands overall. Later rounds can create metadata cost larger than
any repeated-sequence saving. No claim that additional rounds always compress,
strengthen secrecy, or produce independent transformations is made.

## Usage

Python 3.12+; the consumer and native operations require only the standard library.
The source root contains the locked `ucns/` checkout. No UCHC runtime checkout is required. The runnable
bundle supplies exact, read-only minimal snapshots under `sources/`.

```sh
cd research/weave
python cycle.py demo --sources /checkouts
python cycle.py forward input.bin output.wvc --corpus corpus.bin \
  --profile profiles/cycle-v1.json --sources /checkouts
python cycle.py reverse output.wvc recovered.bin --corpus corpus.bin \
  --profile profiles/cycle-v1.json --sources /checkouts
WEAVE_SOURCES=/checkouts python -m unittest discover -s tests -p test_cycle.py -v
WEAVE_SOURCES=/checkouts python test.py --receipt /tmp/weave-cycle-check.json
```

`--sources` defaults to `WEAVE_SOURCES`, then the local `sources/` folder. Output
files use exclusive creation; existing files are never overwritten. Actual corpus
bytes and the same profile are required for recovery. Neither should be mistaken
for an asymmetric private/public key pair. Do not use this research format for secrets.

Default execution budgets: 256 KiB source message, 1 MiB intermediate records and
corpus, 32 rounds, 16 million candidate-occurrence visits, 131,072 native occurrences
per round, and 16 million aggregate scheduler prime-work units. Library callers
can supply `CycleLimits`. Guards produce visible refusal before exceeding the
admitted scope; no mid-run truncation is returned as success. These are operational
profiles, not mathematical limits or cryptographic security parameters.

## Tests, integration, and rollback

Thirty cycle tests cover all 8,191 binary-alphabet byte strings of lengths 0..12;
competing overlaps/residuals; all 4,083 small ranked compositions in the declared
range; all byte values; both end orders; effective native spaces; exact prime paths;
empty/random/multiround messages; a 65,536-byte roundtrip; malformed records/configs;
resource guards; and a fresh recovery process after original-file deletion.

The numeral dependency's four live review findings are repaired: conflicting active
circle documentation, reset decode prime budgets, zero-denominator CLI handling,
and malformed-input versus resource-limit classification. Three new regressions
bring its suite to 18. The obsolete bit-per-circle modules and their 22 tests are
removed, with these sequence/native operations as replacement. Fifty-two original
transport/assembly tests retain their original limited scope. Full Weave inventory:
52 + 18 + 30 + 13 native-origin + 12 repair + 18 review-closure + 9 follow-up + 9 terminal-record + 3 header-admission + 4 numeral-replay regressions = 168. The original
13 native producer tests are retained in Stack as `tests/test_binary_origin.py`.
The repair regressions exercise forged closed records, fresh verified module
loading, atomic failed-write cleanup, empty-input attachments and manifest edges.

The cycle is opt-in. The original transport experiment and the all-on native cipher
refusal remain separate; no missing asymmetric operator is silently filled.
Rollback removes the cycle modules/profile/dependency locks/workflow additions as
one change. Historical discarded encoders remain in Git, not in active imports.

## hmmm

Automatic discovery of short prime recipes for arbitrary literal sequences, an
actual private/public degeneration and recovery advantage, authentication/replay,
and security analysis of the completed cipher remain open. The named normalization,
selection, attachment and determinant profiles are implemented candidates, not
universal rules. This cycle now executes those choices and reports their real cost.

## Output failure boundary

Both `cycle.py` and `numeral.py` write a private temporary sibling, flush, fsync
and close it, then install it with an atomic no-clobber hard link. Write, flush,
fsync or close failure leaves no partial destination. Existing files and symlinks
are never overwritten. A filesystem without the required hard-link semantics
refuses explicitly. Abrupt process-crash cleanup and directory durability are
not guaranteed. Empty numeral input still validates its required attachments.

## Final-review closure repairs

The four later PR #77 findings are covered by `tests/test_review_closure.py`.
Accounting reuses its validated bit count; numeral CLI operations share one charged
prime-work engine through parsing, accounting, and recovery. Budget failure occurs
before publishing output. Native closure comparison checks the exact UCNS classes
from the origin's Geometry instance and compares only typed canonical fields, never
arbitrary object equality. This also rejects equality-spoofing scalar subclasses.
Validation calls the trusted record classes directly; per-instance methods cannot
replace the validation of a supplied record.

The inverse rediscovers sequences under the declared selection profile and requires
both definitions and source order to match. Its rediscovery obeys the same explicit
per-round byte and candidate-visit limits as forward discovery. A different valid
partition is not silently attributed to the selected deterministic profile.

Usage: `WEAVE_SOURCES=/checkouts python -m unittest discover -s tests -p test_review_closure.py -v`.
The profile, forward operations, UCNS producers, ownership and cryptographic standing
are unchanged. The local candidate source lock changes with the repaired source;
records bound to the previous lock must be regenerated rather than accepted under
false source provenance. This is stricter validation, not authentication.

## Record-owned dispatch boundary

Sequence-table exports call the trusted class validator rather than `self.validate`.
The numeral layer likewise invokes trusted Packet, Entry, BitBlock and PrimePath
operations while handling supplied records. Altered block fields are revalidated;
record-owned `validate`, `replay`, and `to_bytes` overrides cannot authorize or
change serialized content. Prime opcodes require exact string values.

Six additional regressions cover the table/Entry follow-up findings and the same
pattern in enclosing packets, bit blocks and recipes. This boundary concerns
supplied data records; it does not sandbox hostile Python code that replaces the
trusted runtime classes or producer modules themselves. Runtime code is trusted.

## Follow-up discovery and dispatch repairs

`tests/test_final_findings.py` covers the five subsequent review findings. A capped
LCP candidate now expands to the full matching suffix interval before selection;
duplicate intervals are merged before applying the existing longest-first and
leftmost-nonoverlapping rules. For `00 01 00 01 00 01 01`, all three disjoint
`00 01` occurrences are retained, followed by the residual `01`. The selected
profile is unchanged; the earlier implementation omitted a qualifying occurrence.
The regression suite compares the LCP-derived candidate family against explicit
prefix matches on all 1,022 nonempty binary-alphabet strings of lengths 1..9.

Native closure uses the trusted ByteOrigin byte-axis constructor and trusted
geometry/axis export methods, so a record-owned method cannot replace the origin
under validation. Profile identity revalidates scalar and nested round fields
and uses trusted serializers. The scheduler invokes trusted PrimePath replay,
including its aggregate budget, rather than a method on the supplied path.

This cycle profile emits literal sequence definitions. Recovery now rejects a
recipe-backed substitute even when the recipe produces the same bytes. The
standalone numeral layer retains its explicit prime-recipe support; it has not
been removed or silently disabled there. Supporting such definitions in a cycle
requires a profile that actually emits them. The existing native-source lock
rotation refuses old records instead of attributing them to the repaired code.

Run the added regressions with:

```sh
WEAVE_SOURCES=/checkouts python -m unittest discover -s tests -p test_final_findings.py -v
```

The earlier follow-up checkpoint passed its then-current 152-test suite. The
three-round demo still costs 6,735 total bytes and recovers exactly. These repairs
change neither the UCNS producer pins nor the ownership or cryptographic standing of the construction.

## Canonical rational, route and inverse validation

The three terminal-review findings at `76508332f353` are exercised by
`tests/test_terminal_records.py`. Numeral attachments validate the exact integer
numerator and positive denominator and compare them with a newly normalized
Fraction before serialization. Altering an exact Fraction object's internals no
longer produces a record the canonical decoder would reject. Native coordinate
and space inputs receive the same canonical-field check before geometric work.

`plan` validates a supplied Route by re-executing its PrimePath with trusted
methods and comparing the typed trace and determinant. Direct construction and
mutation do not create an evaluated route merely through the record's class.
Its optional `limits` and `engine` parameters account for this actual replay.
Both cycle directions share one scheduler engine across initial evaluation and
all subsequent route validations. The aggregate work allowance is not reset;
a workload that formerly fit only because revalidation was omitted may now
refuse within its declared budget. The split formula and valid results are unchanged.

Native inverse recovery, its axis construction and coordinate replay call trusted
Geometry methods. The cycle's corresponding geometric exports do so as well.
Supplying replacement instance methods cannot license arbitrary coordinates. This
remains a data-record validation boundary, not protection against modification of
trusted Python classes or producer modules.

Run the terminal-record and header-admission regressions with:

```sh
WEAVE_SOURCES=/checkouts python -m unittest discover -s tests -p test_terminal_records.py -v
```

The native source lock rotates with this repair. Regenerate records tied to the
previous lock rather than treating them as evidence for the new source. UCNS
producer source, UCHC architectural reference and Stack ownership are unchanged.

## Outer-header admission before expensive recovery

Recovery parses the complete outer frame first: magic, fixed identity fields,
root, canonical round count, bounded payload length, and absence of trailing
bytes. It then validates the supplied profile and matches the source/profile
identities and round count. Only admitted framing reaches prime-route replay
or loading and execution of the pinned native producers. Valid records retain
the same single scheduler budget and reverse operations; no wire field, split
formula, producer pin, ownership or security claim changes.

Three added tests in `tests/test_terminal_records.py` check every truncated
prefix, wrong magic, identity/count/length mismatches, noncanonical integers
and trailing bytes without invoking either expensive step. A complete header
still reaches real scheduler evaluation and its existing budget refusal.

Usage: `WEAVE_SOURCES=/checkouts python -m unittest discover -s tests -p test_terminal_records.py -k HeaderAdmissionTests -v`.

The outer-header repair passed its then-current **164-test** local suite with
zero failures, errors or skips. The current result is recorded below; neither the
152-test nor 164-test checkpoint is presented as the latest inventory.


## Single recipe replay during numeral decoding

The review of `8bc5e1f7ce7f` found that a shared counter still charged decoding
for a redundant second recipe evaluation. A recipe needing five work units could
encode under `prime_work=5` but fail to decode under those identical limits.

The decoder now reconstructs each recipe-backed block once using the trusted
PrimePath implementation and one aggregate engine. It then checks the packet's
complete typed structure, angular attachments, definition uniqueness, occurrences
and declared length without replaying those same definitions. No caller-supplied
bypass or reusable validation flag is introduced. Public validation, encoding,
accounting, occurrence export and restoration continue to revalidate supplied
objects and recipes; mutation after decoding is not trusted.

Four regressions in `tests/test_numeral_replay.py` verify the exact same-budget
roundtrip, one replay per definition and true aggregate refusal, malformed recipe
record rejection, and revalidation after a decoded record is changed. The prior
budget tests now count necessary actual work rather than mandating duplicate work.
CLI inspect/recover still share one counter across their distinct operations.

Usage: `python -m unittest discover -s tests -p test_numeral_replay.py -v`.

Current repaired local result: **168 tests passed, zero failures, errors or skips**,
with unchanged sources during execution. The native source lock, profile, wire
format, UCNS producers and 6,735-byte exact-recovery demo are unchanged. This
numeral resource repair does not change Weave's cryptographic standing. Hosted
checks and current-head terminal review remain separate acceptance gates.
