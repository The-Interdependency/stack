# Weave: full modular assembly v1

Status: ASSEMBLY IMPLEMENTED; COMPLETE ENCRYPTION NOT IMPLEMENTED.

This is a source-bound composition contract and switchable runner, not a replacement
cipher. The native key, binding, thread, corpus and join laws remain explicit missing
operators. No dummy implementation is enabled, and a missing operator never acts as
an identity. All-on encryption refuses before touching input until those operators
are supplied. Existing interleave code is reused without changing its findings.

Source: The-Interdependency/stack@2f1a70948fb90f340613c49d27dfeb1b4e1b650f,
research/weave/SPECIFICATION.md. This specification preserves the full architecture.
The order below is an ASSISTANT PROPOSAL, not an additional user requirement.

## Module plan and complete composition

Key setup is separate from the reversible data path. `stages/key.py` owns KeyGen
and the public/private operation contract. The sender-side context has no private-key
field. This API separation does not prove that a public key reveals no private data.

Proposed forward order:

1. `stages/gonol.py`: construct the complete native nested plaintext object.
2. `stages/bind.py`: apply the public-side native relation whose recovery uses the
   private gonol. This is a mathematical operation, not a password check.
3. `stages/split.py`: form the mutually required logical thread streams.
4. `stages/corpus.py`: apply the actual corpus/material relationship to each thread.
5. `stages/inter.py`: execute the exact supplied section partitions, last/first inward,
   in supplied stage order, independently for each thread.
6. `stages/join.py`: interlace the transformed threads under the selected relation.
7. `stages/whole.py`: apply the last/first inward operation to the resulting whole.
8. `stages/auth.py`: optional integrity/replay contract; no authentication law has
   been selected or implemented. Off by default; never a substitute for encryption.

Inverse: undo the enabled data stages in the exact reverse order, using the recipient
context and the same explicitly selected profile. Key generation is not inverted.
A key-derived plan may govern any of these stages; it is not deferred until the end.
If inverse planning depends on data that is still hidden by a later inverse stage,
that dependency must be resolved by the native law, not circularly read from plaintext.

## Switch semantics

All seven required data stages and key setup default ON. Auth defaults OFF because
it has not been made a requirement of this design. Each has an independent Boolean.
OFF skips exactly that stage and its inverse, without changing any other switch.
Key OFF bypasses KeyGen and withholds both key objects from stage contexts.
A missing enabled implementation is BLOCKED, not skipped. A type/dependency that cannot
survive a bypass is an incompatible ablation, not a falsification of the full system.

Every run carries its profile, stage order, switch mask, operator identities and
classification. The runner retains no plaintext, private key, corpus bytes or per-stage
payloads in its trace. It never serializes a plan or secret into ciphertext on its own.
Disabling a required stage creates ABLATION_ONLY output. An all-on experiment is still
FULL_PROFILE_EXPERIMENT, never a proof of security. Whole-system observations require
whole-system operators; test fixtures cannot authorize full-profile execution.

## Questions and proposed answers

The short IDs below let Erin change answers without retyping the project. None of
these proposed answers is presented as a previously supplied law.

| ID | Question necessary to complete the binding | Proposed answer / research position |
|---|---|---|
| Q1 | Does the plaintext construction use a lossless binary admission into native gonols, a language-domain construction, or both? | Support the entire raw input without lossy normalization. Use a native binary admission for arbitrary files and explicitly selected language constructors for language-aware profiles. Do not relabel a JSON tree or an input dossier as a new gonol. The binary and whole-message constructors still need an owning native implementation. |
| Q2 | Is the private gonol a missing origin/attachment relation, an omitted member, or something else; what public operation corresponds to it? | Investigate a public projection of the full native relation with a private origin/attachment supplying the lift during recovery. This is a candidate target, not an established algebra. Deriving its forward operation and testing unauthorized inversion is the research job; Erin need not supply a security proof. |
| Q3 | Are threads different necessary parts/projections of one plaintext construction, or separate full constructions? | Different required parts of one construction, preserving cross-thread relations and occurrence identity. No independent plaintext copy in each lane. Whether every lane is mathematically necessary must be measured, not enforced by an artificial missing-file check. Exact routing/projection remains to be defined. |
| Q4 | Does corpus material supply axes/origins, traversal instructions, transformed values, or a combination? | Keep two explicit candidates: corpus-derived native axes/origin attachments; and corpus-derived traversal/arity choices. Use actual content in either case. Evaluate both within the complete composition; do not replace either with a filename hash, XOR mask or unrelated cipher. |
| Q5 | How do thread streams interlace, and is final whole-stream interleaving after that join? | Use a declared key/context-derived thread route, followed by the final last/first interleave over the joined stream. This is one proposed order. A per-thread final pass is a separate alternative, not an invisible extra pass. |
| Q6 | Do successive arities consume the previous stage's output, and how are remainders handled? | Proposed sequential composition. Supply exact partition lengths for every stage/lane now; balanced quotient/remainder partitioning is one selectable future policy, not an assumed rule. Keep arity distinct from level count: no invented three-stage minimum. |
| Q7 | What may an independent sender know: just public key/material, or any private corpus selections and schedules? | Sender gets public key, allowed public material and message randomness only. Private gonol and secret selections remain recipient-side. Any secret-dependent stage must offer a public forward operation. Giving encryption the private plan would be a symmetric test, not the requested asymmetric system. |
| Q8 | Are thread count, partitions, corpus locations and join route message-dependent, key-dependent or explicitly supplied? | Keep them key-and-message-context dependent candidates. The public/native forward law must make encryption possible without disclosing the private inverse. Do not publish them as convenient ciphertext headers before deciding which are intended to remain hidden. |
| Q9 | Should equal plaintext under the same public key produce different outputs? | Proposed yes: explicit fresh sender randomness, reproducible only in test fixtures. Derive its role through the native relation; a public nonce alone does not create secrecy or prevent key recovery. No automatic randomization mechanism is inserted here. |
| Q10 | Which ciphertext structure is public, and must altered or incomplete messages be rejected? | Specify version, profile negotiation, length policy, integrity and replay policy before a wire format is frozen. Keep experimental switch masks in the lab receipt; do not silently disclose secret structure. There is no selected authentication construction. |

Q2, Q4 and Q8 require mathematical candidate derivation as well as intent. A label such
as 'private projection' is not an implementation. Operators remain unbound until that
actual transformation exists. The original pre-substitution conversation remains
unrecovered; this does not establish that Erin never specified these relations.

## Usage

From `research/weave/`:

```bash
python run.py                         # full proposed profile: explicit BLOCKED list
python run.py --off corpus            # one-stage ablation; no cascading skips
python run.py --on auth               # also requires a real authentication law
python -m unittest discover -s tests -p 'test_assembly.py'
```

`assembly.Pipeline` accepts explicitly supplied `Operator` bindings. Nothing is loaded
from ciphertext or dynamic module names. Native objects pass through without conversion
into a generic replacement tree. `stages/inter.py` expects a `Streams` object plus
explicit per-thread partitions; `stages/whole.py` expects exactly one joined stream.
KeyGen is explicitly supplied through `stages/key.py`, not invented by the runner.

## Verification and remaining work

Tests cover assembly control flow, inverse order, independent switches, missing-law
refusal, public/private API separation, and the two existing literal bit operations.
They do not simulate missing native operators and call that encryption. Test-marker
operators are labelled wiring fixtures and cannot run as full-profile evidence.
A valid decryption API returning original data is not by itself security evidence.

Deployment: manual local research only; no service, scheduled work or network calls.
Rollback: remove this new assembly and its tests; preserve the original source/spec
and sealed interleave evidence. No imported `libs/`, upstream producer or lifecycle
standing changes in this transaction.

## hmmm

The assembled interface is executable. The complete cipher is not: native message
admission/composition, private/public binding, thread/corpus coupling and join/key
planning are not filled with pretend implementations. These are the next exact
research/intent decisions exposed by this assembly.

## Native source inspection

UCHC `hyperspace_construct.py` blob `8b55823805c87ad8c4cc9d7451dc2eb90bdedd3a`
supplies real glyph/word/definition construction and recovery. UCHC
`inference_input.py` blob `0959342f9526e8c0b35cc7e1a2a448b0961977b9` explicitly
calls `InferenceFrame` an input dossier, not a new gonol. That dossier is not silently
substituted for a native whole-message encryption gonol. The full construct database
was not available in this runtime, and no reduced fabricated corpus was generated.

Skill application record (one unit of work): `the-interdependency`,
`meta-module-build`, `msdmd`; source preservation, explicit native boundaries and
fail-closed module wiring applied. Outcome: assembly tested, full cipher unresolved.
METAPAT README consulted for domain-owned mechanisms/non-transfer; no cryptographic
conclusion is inferred from that semantic source.

## Review repair: provenance and inverse controls

Usage: a supplied native key law returns
`KeyPair(public, private, law_identity, relation_identity)` through `keygen`.
Export `pair.public_context(parameters=...)` for the sender and
`pair.private_context(parameters=...)` for the recipient. Both declarations are
validated and their law/relation identities are bound into the recipe. Sender
contexts contain no private-side reference. Fixture pairs must set `fixture=True`
and require explicit fixture permission; they remain `WIRING_ONLY`.
These checks verify declared provenance and matching sides, not the mathematical
truth or secrecy of a still-unimplemented asymmetric relation.

Each enabled stage records a type-preserving digest of its effective parameters
before execution. Inverse execution checks it before that stage runs. If forward
operators derive different controls through `Transition`, callers may supply
`decrypt(run, private_context, inverse_plans={stage: independently_derived_controls})`.
That mapping must cover exactly the enabled stages. The Run never contains the
controls and cannot reconstruct them for the recipient; missing native derivation
still blocks. Unserializable controls require an explicit representation, never repr.

The transport lab record is now `weave.lab-record/v2`, carrying plan identities.
Version 1 is refused because it cannot bind inverse plans; regenerate experimental
records from the declared profile and original input. These comparison digests are
neither authentication nor a secrecy mechanism and may disclose plan guesses. They
belong to the lab, not a proposed native cipher wire format.

The source verifier requires both `probe.py` and `PLAN.md` at their frozen hashes,
plus the exact declared Stack and inspected UCHC identities. Receipt location does
not choose executable sources. Run `python probe.py > /tmp/weave-probe.json` and
`python verify.py /tmp/weave-probe.json`; omission and substitution must fail.
