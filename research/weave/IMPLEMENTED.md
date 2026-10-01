# Weave — executable provisional stages

**Delivered:** a five-stage transport experiment, each stage independently switchable,
plus a source-pinned native-word adapter. **Not delivered:** a complete native asymmetric
Weave cipher. The all-on native profile remains the default and reports unresolved
operations before processing input. No native operation is silently replaced.

This work implements the instruction to act on available proposed answers and return
remaining questions for correction, improvement or approval. The concrete corpus
left/right formula, cyclic split example and cyclic join example are explicitly new
assistant-selected trial rules. They are not attributed to Erin or made canonical.

## What executes

| Module | Implemented operation | Standing |
|---|---|---|
| `stages/split.py` | Route each source bit occurrence exactly once to an explicitly assigned lane; reconstruct original order. | Transport candidate; native complementary-gonol thread law remains open. |
| `stages/corpus.py` | Use actual selected corpus bits to choose left/right consumption of each lane; recompute the inverse from the same material. | New provisional traversal variant, not native origin/axis binding. |
| `stages/inter.py` | Sequential last/first section operations, with exact supplied boundaries or balanced quotient/remainder generation. | Literal operation with an explicitly provisional partition policy. |
| `stages/join.py` | Interlace lanes in a supplied repeating visitation order; recover exact lane lengths and order. | Explicit transport route, not a native private route generator. |
| `stages/whole.py` | Last/first inward interleaving across the entire joined stream. | Existing literal operation preserved byte-for-byte. |
| `stages/gonol.py` | Verify the inspected UCHC source blob and caller-pinned database, then use actual `promote_word`/`recover_word` objects. | Adapter written; missing-input/source-refusal tested; successful native corpus replay NOT executed here. |
| `stages/key.py`, `stages/bind.py` | Existing explicit interfaces and missing-law refusal. | Native key generation and private-gonol recovery algebra unimplemented. |
| `stages/auth.py` | Independent optional switch; enabled use requires a real supplied law. | Authentication/replay unimplemented. |

The runnable profile composes **split → corpus traversal → arity interleaves → join →
whole interleave**, and reverses that composition. It acts on explicitly admitted
transport bits. It does not call those bits a gonol or relabel this profile as Weave.

## Run from a phone-oriented Python environment

Python 3.11+ and its standard library are sufficient for the transport experiment.
The local evidence here was produced with Python 3.13.5; Android execution was not
observed. From `research/weave/` or the extracted bundle:

```sh
python run.py demo
python test.py --receipt /tmp/weave-check.json
python run.py
```

The first runs a nonsecret demonstration. The second runs all local tests. The third
shows the full native profile's unresolved laws and returns exit status 2.

For actual file experiments, supply each selected material explicitly:

```sh
python run.py enc profiles/transport.json input.bin output.lab \
  --material a=book.txt --material b=manual.txt --material c=sound.bin
python run.py dec profiles/transport.json output.lab recovered.bin \
  --material a=book.txt --material b=manual.txt --material c=sound.bin
```

This is **not safe storage for real secrets**. Files are never overwritten. Output
`.lab` files are research records, not a chosen production cipher format. They carry
switch/operator identities and packed bits; they do not carry corpus content or
secret native reconstruction state. The separate profile remains necessary input.
The message and each supplied material file are capped at 64 KiB as a declared runtime
resource guard, not a cryptographic or mathematical limit. The experiment also caps
thread count at 63 and each schedule at 64 stages/arity 4096 for the same reason.

## Switches and absent dependencies

`profiles/transport.json` explicitly disables `key`, `gonol`, `bind`, and `auth`.
It is selected only by demo/enc/dec. `run.py` without that command retains full native
scope. Every switch is a literal Boolean; unknown/misspelled fields fail.

Off means that stage and its inverse do not run. Corpus off reads no supplied corpus
path, passes no corpus material to later stages and compiles no stale corpus control.
Other switches do not change automatically. Turning join off while leaving multiple
lanes and whole on is an incompatible configuration, not a result against the design.
Opaque third-party callbacks remain responsible for their declared dependencies;
this runner is not a sandbox against callbacks hiding private data in closures.

All transport operators carry `scope='transport'`. Even if combined with additional
operators, their result cannot be classified as a full-native profile experiment.
Wiring fixtures remain separately labelled and disabled unless explicitly permitted.

## Verification

The source-bound receipt is `evidence/transport-v1.json`. Tests include original assembly
regressions, 512 assembly switch combinations, all 32 transport switch combinations
(28 executable; four incompatible), all 8,191 binary inputs of lengths 0–12, unequal and
empty sections, exact byte recovery at 64 KiB, and independent-process recovery after
deleting the original input file. There are no skipped tests.

The corpus-content witness demonstrates a real effect: changing actual material changes
a declared case's output, while renaming identical material does not. Disabling corpus
removes that influence. This does not imply every material is distinct or adds entropy:
all-zero material selects left-to-right traversal, all-one selects reverse traversal,
and unused material bits have no effect. Equivalent traversals remain possible.

The test suite also records **limitations**, not hidden successes: fixed-map recovery
succeeds against this complete transport candidate at 137 bits in eight selected-input
queries; wrong material can return incorrect bytes without an integrity error. These
are observations about the explicitly chosen transport variant, not the unimplemented
native gonol/private-key/corpus relations or a verdict on Weave. No independent
researcher reviewed these tests. Fresh-process recovery is not an independent-author
implementation.

## Native source boundary

The optional reader consumes UCHC `human/english/english_gonol/hyperspace_construct.py`
at Git blob `8b55823805c87ad8c4cc9d7451dc2eb90bdedd3a`. It verifies the exact source
before execution and opens a caller-digest-bound `construct.db` read-only. It returns
an actual upstream `WordGonol`, not a generic message tree. A hash match is source
identity, not full-corpus validation. No constructed corpus database was materialized
here, so successful native replay is explicitly NOT EXECUTED. No small fabricated
corpus is presented as a full-corpus replacement.

Whole-message/binary admission, nested native serialization, private-gonol binding,
public/private key derivation and native complementary-thread construction remain
separate unfinished implementation/research work. The reader is not automatically
bound to the complete `gonol` stage because its admitted scope is narrower.

## Questions and change control

Read `QUESTIONS.md`: Q1–Q10 each pair an unresolved choice with a proposed answer,
current implementation status and the exact distinction that must survive correction.
Approving a research direction does not require Erin to supply its proof or code.

## Provenance, deployment and rollback

Starting Stack identity: `200032dba6131145ebc61b52bb4f1aee507e6f63` on existing PR #62.
No `libs/` snapshot, upstream constructor or root project lifecycle is modified.
The source file plan and non-transfer boundaries are in `IMPLEMENTATION_PLAN.json`.
The original run-1 probe and assembly test source were recovered byte-exactly and
checked against their Git blob identities before use. Old sealed receipts are not
rewritten as evidence for new code.

Rollout is manual research plus path-scoped CI. Revert this workspace-local change to
roll back; retained historical evidence remains available. Usage of `the-interdependency`,
`meta-module-build`, `msdmd`, and `gonol-build` shaped scope, source ownership, native
metadata and validation. This records their contribution, not an invented maturity
count. The canonical skill-usage runner was not available in this local checkout;
its persistent usage counter was not updated. METAPAT's domain-owned-mechanism boundary
was consulted; no cryptographic result is inferred from it.

## hmmm

The coded proposals are ready to correct, improve or approve. The complete native cipher
remains unimplemented. Transport execution, source verification and API refusal do not
replace its missing constitutive relations.

## PR #62 review repair

Retirement dependency: merged Stack #61 at
`1ba201449731337dc20c564788f4303c8910bfdd`.
The current source adds key-law/relation provenance, per-stage inverse-plan checks,
complete source verification and mandatory corpus dependence for complete profiles.
All original layers and independent switches remain. Native asymmetric derivation
is still unresolved. Prior `evidence/transport-v1.json` is historical evidence for
its exact source, not evidence for this repair. Reproduce current coverage with:

```bash
python research/weave/test.py --receipt /tmp/weave-review-repair.json
```

See `ASSEMBLY.md` for the required key-side exports, independently derived inverse
plans and replacement v2 lab-record usage. No native cipher security is established.
