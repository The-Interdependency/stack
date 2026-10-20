# Weave

Standing: **Stack-owned construction research; no established encryption security.**

Weave preserves the intended system: native gonol/origin construction, private-gonol
recovery, reconstruction-related streams, selected corpus material, ordered
multi-arity bit interleaving, and an eventual asymmetric public/private relation.
The interleave is one operation, not the project identity. URPCS remains retired;
its substituted codec, implementation and security findings are not inherited.

## Research abstract

Description dated 2026-10-14; published 2026-10-18. This is a research description, not a new verification, release, or promotion of claim status.

### Weave: A Reversible Gonol Construction for Cryptographic Research

**Weave** investigates whether cryptographic recovery can depend on private structural relations among nested geometric representations, multiple reconstruction-dependent streams, and user-selected corpus material. Its intended architecture combines a message-origin construction with private-gonol participation, ordered multi-arity bit interleaving, and an asymmetric public/private recovery relation. The interleave is one operation within this architecture, not the cryptosystem itself; the intended asymmetry must arise from the construction rather than a substituted conventional cipher.

The implemented cycle normalizes message length using actual corpus bits, identifies repeated multi-byte sequences, attaches those sequences to an eighth whole/origin circle, and records their ordered occurrences across seven companion-circle streams. Exact length-bearing numeral references preserve reconstructable values, while executed prime routes determine bit partitions. Sequence construction and first/last interleaving repeat across successive rounds. Recovery reverses the resulting record using the declared corpus, profile, and source dependencies, without requiring the original plaintext or an undisclosed encoder trace.

The merged cycle’s published validation reports **176 passing tests** and exact reconstruction. Its recorded demonstration expands 784 input bytes to 6,735 encoded bytes; compact references therefore do not establish net compression or a fixed expansion ratio. A separate public/private polynomial candidate supports public-only encoding and private inversion, but its published coefficients also permit an equivalent public inverse. This result falsifies that candidate’s requirement for private state, not the broader intended architecture.

Weave’s present contribution is an executable reversible construction and a falsification program that distinguishes reconstruction correctness from confidentiality. The central research question is whether the combined private-gonol, stream, and corpus relations impose an independently necessary recovery constraint that remains unavailable from public information.

**hmmm:** Native asymmetry, cryptographic stream/corpus dependence, authentication, and replay resistance remain unresolved. The current implementation supports construction experiments, not confidential storage.

**Usage guidance:** Read this abstract for the research question and intended contribution. Use the scope, evidence, commands, and limitations in the rest of this README before relying on the work; retain the unresolved conditions above when quoting the description.

Public repository context: [Preserved specification](https://github.com/The-Interdependency/stack/blob/3d74cf118e14cc3839d7426d90ca9791567a7005/research/weave/SPECIFICATION.md) · [Executable cycle and limits](https://github.com/The-Interdependency/stack/blob/3d74cf118e14cc3839d7426d90ca9791567a7005/research/weave/CYCLE.md).

## Current executable cycle

Normalize once with actual corpus bits. Discover repeated multi-byte sequences,
retain each sequence at an attachment on the eighth/whole circle and its ordered
occurrences among the other seven. Serialize exact numeral references and native
positions, derive bit divisions from executed prime-index and embedded-span paths,
first/last interleave, and repeat. Reverse from the final record, corpus, profile
and exact source dependencies without the original input or encoder trace.

[The cycle contract](CYCLE.md) records the explicit candidate choices, all-cost
accounting, budgets and exact source lock. These choices are not universal laws.
[The numeral layer](NUMERAL_CONSTRUCTION.md) separately records length-bearing
integers, Unicode references and exact prime recipes.

`native_binary.py` is the Stack-owned binary-origin/sequence candidate, consuming
actual source-verified UCNS `AxisCirclePosition` and `NativeMobiusState` objects.
UCHC supplies the origin/axis architecture reference; the premature UCHC #7
implementation is retained only as provenance. Domain graduation has not occurred.
The eighth remains the whole/origin, not one bit of a byte. Old bit-per-circle
records and their misleading attack interpretations remain removed.

## Usage

Python 3.12+ and the standard library, with the exact UCNS source in `/checkouts/ucns`:

```sh
cd research/weave
WEAVE_SOURCES=/checkouts python cycle.py demo
python cycle.py forward input.bin output.wvc --corpus corpus.bin --sources /checkouts
python cycle.py reverse output.wvc recovered.bin --corpus corpus.bin --sources /checkouts
WEAVE_SOURCES=/checkouts python test.py --receipt /tmp/weave-check.json
```

`CYCLE_NATIVE.json` binds the actual source blobs. The runnable bundle includes the
minimal exact UCNS files under `sources/`. Existing files are never overwritten;
ordinary write/flush/close failures leave no partial destination. The output is
an experimental representation, not safe storage for secrets.

## Evidence boundaries

`SPECIFICATION.md` preserves the full intended system and latest clarification.
`QUESTIONS.md` preserves question identities and distinguishes implemented candidate
answers from unfinished cryptography. `EIGHT_CIRCLE.md` is historical correction.
`ASSEMBLY.md`, `IMPLEMENTED.md`, `PLAN.md` and `REPORT.md` retain the earlier transport
experiment under its original scope. Its fixed-map attacks are not full-system verdicts.

## hmmm

Actual private/public key derivation and recovery advantage, authentication/replay,
secret-key-space analysis, automatic compact prime-recipe discovery, and security
of the completed cryptosystem remain unfinished. Exact reconstruction and real
geometry do not themselves establish confidentiality or a fixed expansion ratio.
