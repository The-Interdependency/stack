# Weave recovery challenges v2

GPT generated; context, prompt Erin Spencer.

This version contains **1,841 actual challenge files**, with per-file predicted
outcomes as their messages and the exact line `my human needs my help`. All 1,841
were recovered byte for byte by fresh receiver processes given the selected receiver
material. **No attacker trials have been run against v2.**

Download [blind-pack.zip](blind-pack.zip) and extract it to obtain the `files/`
directory. Each `.bin` is an opaque case ID. The archive is packaging; the individual
files are the exact outputs of the documented operations and adapters, without an
extra cipher. Some operations expose literal content. That is a result to measure.

**This README is for the operator. Do not give it, this checkout, the generating
conversation, or the private operator archive to a no-clue attacker.** Release one
case at level zero into a fresh context. Reading this README reveals information
intentionally withheld at the first levels.

## Run each file through the ladder

The separately delivered operator archive includes the frozen predictions, selected
parameters, corpora, exact answers, per-case receipts, pinned source and release tool.
The public repository deliberately does not map IDs to schedules or supply selected
receiver material. From the extracted operator archive's root:

```sh
python3 source/research/weave/recovery-challenges/v2/release.py release \
  --private operator --id CASE_ID --level 0 --out attempts/CASE_ID-L0
```

Give only that exported directory to the recovery model. Its README contains the
instructions appropriate to that level. Freeze its attempt log, code and proposed
bytes before any feedback or next clue. Grade the frozen submission privately:

```sh
python3 source/research/weave/recovery-challenges/v2/release.py grade \
  --private operator --id CASE_ID --candidate submission.bin
```

If exact recovery has not occurred, export level 1 to a **new** directory, then level
2, and so on through level 6. Keep the same case's attempt history. Release only one
new level at a time. Never solve a failed grading check by handing over the answer.
The final stage supplies a working inverse and its inputs, so every admitted file
has a demonstrated path to exact recovery without revealing the stored original.

| Level | Additional information supplied | How to classify success |
| --- | --- | --- |
| 0 | Only one ciphertext and a generic exact-byte recovery instruction | No-clue recovery |
| 1 | Operation family and number of forward stages | Family-informed recovery |
| 2 | Exact pinned algorithm source, adapters and format descriptions | Source-informed recovery |
| 3 | Actual operation order, repeat counts and structural controls | Schedule-assisted recovery |
| 4 | Message structure, the requested known line and concrete recovery hints | Known-plaintext-assisted recovery |
| 5 | Exact geometry, prime paths, circle order, offsets and other controls; corpus withheld | Parameter-assisted recovery |
| 6 | All receiver material including corpus, with executable inverse | Key-assisted completion |

Levels are cumulative. A file counts as cracked at the earliest level with a
byte-exact frozen submission. **Level 6 is not an unaided break.** Do not relabel a
source-informed result as no-clue. For each file's independent level-zero attempt,
use a fresh context; a model that learned from earlier files is a separate cumulative
learning condition. Record that exposure rather than calling it independent.

Natural ciphertext leakage is fair evidence, including readable content and native
hashes. These are not removed. Grading returns only equality and the submitted
candidate's digest. Freeze each attempt to avoid turning repeated grading into an
unrecorded oracle. Instructions are not a filesystem or account sandbox: the
attacker must actually lack access to the private operator archive.

## What is exercised

| Family | Files | Declared coverage |
| --- | ---: | --- |
| Byte-composable layers | 1,180 | N/A/U/S/W/B singles x1/x2/x3; all 62 words for each of 15 pairs; every larger subset forward/reverse; repetition inserted throughout full combinations |
| Three-byte reflection | 265 | R in combination with B/S/W, including all pair orderings/counts and broader combinations; exact three-byte admission |
| Historical typed transport | 393 | All admitted pair words plus all legal five-stage orders repeated x1/x2/x3; explicit split/join lane requirements |
| Unchanged native cycle | 3 | Actual WVC records with one, two and three rounds |

The cap is **three invocations of each named stage in a schedule**. Calls to shared
serialization/validation helpers inside a stage are not additional independently
selected stages. A larger combination may therefore contain up to 18 stage instances.
This is exhaustive pair coverage, not every possible word over all six stages.
[PLAN.md](PLAN.md), [matrix.py](matrix.py) and [COVERAGE.json](COVERAGE.json) specify
the denominator. The transport census also records and verifies **602 invalid typed
schedules**. They produce explicit refusals, not fake ciphertexts or silent joins.

| Stage/component | Actual source and role | Standalone / combination evidence |
| --- | --- | --- |
| N | `cycle.normalize` / `denormalize`; actual corpus tail and WNM frame | N-only files; every core pair; wrong/missing-corpus and extraction witness |
| Discovery | `affixiation.discover`; longest-first repeated sequences, not an LZ78 replacement | Independent partition fixtures; every A and cycle case |
| Native whole-plus-seven circles | `native_binary` and unchanged UCNS geometry | Independent eight-circle closure/recovery fixture; A and WVC cases |
| A | Actual native sequence affixiation | A-only files; every core pair; WRA1 only supplies the native root otherwise carried by WVC |
| U | Actual literal WNC numeral encoding | U-only files; every core pair; exact restoration |
| Prime numeral recipes | Actual `PrimePath` and recipe-backed WNC entries | Independent base-2/base-10 span and prime-index fixtures; recipe packet combination; not invented recipes for arbitrary prose |
| S | Actual prime-route nonempty sections and first/last bit interleave | S-only files; every core pair; both end orders and 3/5/7 arity witnesses |
| W | Actual whole-stream last/first bit interleave | W-only files; byte, reflection and typed transport combinations |
| B/R | Prior representation experiment: bit reversal within bytes / byte reversal within exact three-byte records | Singles/repetitions/pairs; cancellation and commutation witnesses |
| X/J | Existing historical explicit occurrence split / stable join | Own-domain files, admitted pair words, full typed combinations; join-first cases declare contiguous initial lanes |
| C/I | Historical corpus-controlled end traversal / balanced section candidate | Singles/repetitions/pairs/full typed combinations; C is explicitly the earlier assistant proposal, not native private binding |
| Full native cycle | Unmodified `cycle.forward` / `reverse` | WVC cases with normalization once and 1–3 A/S rounds |
| Twin-ray attempt | Existing `TwinRayEngine` | Distinct messages have identical public faces; internal records recover, but no recoverable public-face challenge is fabricated |

These are stage/representation experiments. The new adapters serialize existing
outputs; they do not supply a missing private-gonol relation. R never pads an
intermediate stream to make an invalid order work. Its challenge first lines have
zero to two alignment spaces so the original input satisfies the existing three-byte
domain. Historical transport has its own transparent WLN1 lane container.

The plaintext first line contains a prediction and an independent random trial tag.
The second line is the requested sentence. Predictions were frozen before encoding
or attacker attempts; private.json and its salt are bound by the public commitment
in COVERAGE.json. The salt and complete private record can be revealed after the
experiment if desired. A prediction is a hypothesis, not a measured outcome.

## Full-Weave obligations remain incomplete

The actual source lacks the arbitrary-message private-gonol construction, private
gonol binding, asymmetric KeyGen relation, complementary cryptographic thread law,
native corpus/key binding, authentication and replay state. The existing known-word
gonol reader does not implement those missing operations, and no constructed lexical
database replay is claimed here. These obligations remain visible in COVERAGE.json.
Passing tests of refusal do not count as exercising their encryption.

Consequently, **the user's complete “every part of Weave” requirement remains unmet
for those mechanisms**. No substitute cipher, identity function, conventional
encryption wrapper or invented key law is used to turn that gap green. The explicit
`--require-full-weave` gate exits 2 even when the executable harness tests pass.

## Reproduce and record results

Python 3.12 and standard library suffice. SOURCE.json pins the original Stack and
UCNS files individually. The operator archive includes their exact bytes. Sources
are checked before execution. Fresh receiver processes get ciphertext and selected
parameters only, with no original bytes, prediction salt or encoder trace. This is
data-flow separation, not an OS sandbox or independent cryptanalytic implementation.

```sh
python3 source/research/weave/recovery-challenges/v2/test_harness.py \
  --private operator --receipt harness-replay.json --require-full-weave
```

Expected complete-system gate: exit 2 with passing executable harness and explicit
unimplemented obligations. See RESULTS.json and CHECKS.json for measured validation.
Generation used four workers, unchanged native budgets, and completed naturally.
No budget refusal or omitted case occurred. New runs use fresh messages/material:

```sh
python3 build.py freeze --private /absolute/new-private-directory
python3 build.py generate --private /absolute/new-private-directory --workers 4
```

Generation emits resumable per-case checkpoints. Packaging writes new public
artifacts exclusively and refuses to overwrite a frozen archive. Use a separate
version/directory for a new experiment. The selected private profiles here are
research inputs; no native public/private derivation law is implied.

Use ATTEMPTS.csv from the operator archive to record one row per case per attempted
level: supplied exposure, prior knowledge, time, resources, candidate digest, exact
or partial outcome, method, derived parameters, and stopping reason. Include failed
attempts. A clean no-clue attempt cannot be retroactively manufactured after source
or message disclosure. v1 remains unchanged; the user's reported external 8/8
recovery belongs to that earlier version and is not counted as a v2 attack result.

## hmmm

The full private reconstruction law remains absent. Repetition/order can change
representations, but BB and RR cancel and BR equals RB in the reflection subgroup;
schedule counts are not measured independent keys. No cryptographic strength or
commercial outcome is established by these fixtures. The useful next evidence is
the earliest successful disclosure level and actual necessary receiver material for
each case, followed by implementation of the still-missing native obligations.
