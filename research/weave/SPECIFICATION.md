# Weave — preserved architecture and specification floor

Status: **CORRECTED SEQUENCE CYCLE IMPLEMENTED AS AN EXPLICIT PROFILE; ASYMMETRY UNIMPLEMENTED**.

The latest sequence/occurrence clarification in section 5.1 controls over older
bit-per-circle interpretations. [CYCLE.md](CYCLE.md) records the executable native
normalization/affixiation/interleave cycle and all candidate choices. Other historical
layers below remain preserved objectives, not automatic claims about that profile.

This document records the construction that must survive implementation. It separates
fixed architecture from unresolved mechanics. An unresolved mechanic must remain
`hmmm`; an implementer may not replace the architecture to make the problem easier.

Executed evidence and its exact scope are recorded in [REPORT.md](REPORT.md).
That evidence is not a full-system verdict.

Provenance: this preserves the reported design account, not a recovered immutable
transcript or the original thirteen laws. The merged retirement at
`1ba201449731337dc20c564788f4303c8910bfdd` records that boundary in
`research/urpcs/SOURCE_RECEIPT.json`. Exact historical attribution remains `hmmm`.

## 1. System layers

Weave currently comprises these intended layers:

1. plaintext -> nested hyperspace/gonol construction;
2. private-gonol participation in recovery/private key structure;
3. multiple reconstruction-dependent threads/data streams;
4. user-selected corpus/material associated with threads;
5. ordered multi-arity section interleaving within the thread/data transformation;
6. final whole-sequence end interleaving;
7. asymmetric public/private recovery relation.

These layers are analytically separable but belong to one intended cryptosystem.

## 2. Core bit interleave

Let `S = s_0, s_1, ..., s_(n-1)`.

The historical transport experiment retains this last-first ordering. The current
cycle selects `first-last` explicitly in its profile and also supports `last-first`:

```text
I(S) = s_(n-1), s_0, s_(n-2), s_1, ...
```

continuing inward until every bit appears exactly once.

For an ordered arity schedule

```text
A = (a_1, ..., a_k)
```

each level partitions its explicitly selected input into `a_i` ordered sections and
applies `I` independently to each section. The final whole-sequence operation likewise
requires an explicitly selected input. This skeleton does not choose between original
and prior-stage inputs; the executable experimental profiles explicitly select prior-stage
output. That proposal is not retroactive historical ratification.

Stage count and section arity are distinct. The user's phrase “arity three, minimum”
does not establish `k >= 3`. The prior minimum of three stages was an unsupported
assistant addition and is removed. Experiments must state their stage counts and
arity interpretation explicitly rather than promote them to new user requirements.

A previously stated example schedule is:

```text
(5, 7, 3)
```

This demonstrates the mechanism; it does not select one canonical schedule.

## 3. Thread structure

The design requires multiple data streams/threads, contemplated at arities such as
three, five, seven, or more.

Required architectural property:

```text
no one thread == complete recoverable plaintext
complete recovery requires the declared thread relation
```

The current cycle constructs seven native occurrence-circle streams and exactly
recombines their sequence positions. Their equivalence to every earlier
cryptographic-thread proposal is not asserted; that broader relation remains open.

## 4. Corpus/material participation

Each thread may consume or bind caller-selected corpus/material. Examples already
contemplated include literary, musical, technical-manual, and sound material.

The material is intended to participate in construction/recovery. Treating it as an
unused label or merely hashing its filename does not satisfy this architecture.

The current cycle implements actual cyclic corpus-bit extraction at a configured
bit offset, bucket normalization, and exact reverse checks. The broader private
corpus/key binding remains unimplemented.

## 5. Hyperspace / gonol layer

Plaintext is intended to be represented as a nested hyperspace gonol construction
before or within the encryption transform.

A private gonol is intended to be hidden/bound within the private-key side and required
for recovery.

The exact relation among:

```text
plaintext
nested gonol construction
private gonol
public key
private key
ciphertext
recovered plaintext
```

must be specified explicitly before implementation can claim this layer.

## 5.1. Current sequence/occurrence and numeral clarification

The latest user clarification supersedes the earlier one-bit-per-circle reading:
normalize message bit length with corpus material; parse repeated multi-byte
sequences; save each selected sequence at an angle on the eighth/origin circle;
a circle among the seven records its occurrence count and order; first/last
interleave the resulting bitstream; repeat parsing/affixiation and interleaving.
The message remains the origin and sequential byte occurrences remain individually
addressable. A saved multi-byte sequence is not reduced to a single source bit.

The current numerical extension interprets an exact selected bit block as an
integer with its bit length preserved, then gives it a scoped Unicode reference.
A reference resolves to stored literal construction or an executable prime path.
Prime-index continuation and embedded prime spans preserve route and occurrence
information. [NUMERAL_CONSTRUCTION.md](NUMERAL_CONSTRUCTION.md) records its
implemented boundary, full size accounting, exact replay, and usage.

The numeral module remains a representation layer, not replacement geometry.
The separate cycle now connects automatic repeated-sequence discovery, actual
corpus normalization, Stack-owned sequence closure using native UCNS geometry and coordinate recovery,
prime-route split derivation, and the repeated first/last bit interleave. See
[CYCLE.md](CYCLE.md) for the exact named profile, inverse, tests and byte accounting.
This implements the corrected sequence cycle, not public-key encryption.
No fixed total ciphertext expansion is inferred from a short Unicode reference.
The earlier twofold-length proposal requires accounting over the completed cycle.

The existing 720-degree return and key-set-specific space relationships remain
preserved. Earlier whole-plus-one public-view research is not promoted into an
asymmetric result by this codec. [EIGHT_CIRCLE.md](EIGHT_CIRCLE.md) records the
prior byte/star repair; its bit-per-circle interpretation is historical and its obsolete modules/tests
are removed in favor of the native sequence cycle. No discarded PR #73/#74
encoder or attack is revived. All other declared system layers remain.

## 6. Asymmetric relation

The intended system is to reach asymmetric key generation/recovery without silently
outsourcing the construction to an unrelated external cryptosystem.

The public/private derivation law is not yet fixed. Existing standard primitives may
be used later only in explicitly scoped supporting roles; they may not stand in for the
missing Weave relation.

## 7. Required invariants and measured relations

Any complete Weave profile must eventually demonstrate:

- exact plaintext recovery with the complete authorized reconstruction state;
- failure or materially incomplete recovery when required structural components are
  absent;
- bit conservation wherever a layer is specified as a permutation;
- exact preservation of supplied arity order and stage count; equivalences between
  different schedules are measured, not forbidden by an invented uniqueness law;
- dependence on the declared thread relation;
- dependence on the declared corpus/material relation, which is mandatory for every complete profile;
- dependence on the private gonol/private-key relation;
- no hidden inheritance from URPCS.

A different schedule description need not induce a different positional map.
[REPORT.md](REPORT.md) records exact counterexamples for the explicit sequential
component profile. They do not establish a verdict on the full construction.

## 8. Forbidden flattening

The following are specification failures if used as replacements rather than explicitly
declared supporting components:

- reducing Weave to only the bit interleave;
- reducing threads to one stream;
- making corpus/material decorative;
- omitting hyperspace/gonol construction;
- omitting the private gonol from recovery;
- replacing the system with recursive pairing/framing;
- importing URPCS Laws 1–13;
- replacing missing key structure with RSA, ECC, DH, a KEM, AES, ChaCha, Feistel, or
  another familiar primitive and calling the result Weave;
- treating a reduced-layer test as evidence for the complete system.

## 9. Falsification program

The research program must separately test:

1. exact inversion of the bit interleave;
2. collisions/equivalences among arity schedules;
3. schedule recovery from known/chosen plaintext;
4. thread independence and reconstruction dependence;
5. corpus/material contribution versus decorative obscurity;
6. structural leakage and distinguishability;
7. hyperspace/gonol reversibility and whether the private gonol adds a real independent
   constraint;
8. public/private asymmetry and whether public information permits unauthorized
   reconstruction;
9. complete-system behavior after all required layers are combined.

A failure is evidence about the specified mechanism. It does not authorize replacement
of the mechanism.

## Usage guidance

Implement one explicitly versioned profile at a time, but every profile must state which
Weave layers it includes and excludes. A profile omitting a required layer is a layer
test, not a Weave security result.

To reproduce the executed component evidence, run from this directory:

```bash
python probe.py > receipt.json
python probe.py --check receipt.json
```

## hmmm

1. Prime-route ranked compositions implement uneven partitions for the named cycle
   profile; other determinant profiles remain open.
2. The current cycle consumes preceding-round output, as clarified. Historical
   alternatives are not current prerequisites or silently selected rules.
3. Seven native occurrence streams reconstruct exactly in the current profile;
   broader cryptographic-thread dependence remains unestablished.
4. Corpus-tail normalization is implemented as an explicit profile; broader
   cryptographic corpus binding remains open.
5. The native binary sequence profile now supplies scoped origin/axis closure and
   reversible serialization; general nested-gonol and private-key use remain separate.
6. Private-gonol generation and binding.
7. Public/private key derivation and the exact source of asymmetry.
8. Authentication, nonces, state evolution, truncation/replay handling.
9. Threat model and target security properties.
10. Original pre-substitution thirteen-law conversation was not recovered. Missing
    retrieved source is not evidence that the user never specified the relation.
