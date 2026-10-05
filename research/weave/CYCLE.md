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
52 + 18 + 30 + 13 native-origin + 12 repair regressions = 125. The original
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
