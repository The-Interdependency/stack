# Weave — preserved architecture and specification floor

Status: **PRE-SPECIFICATION / FULL-ARCHITECTURE PRESERVATION**.

This document records the construction that must survive implementation. It separates
fixed architecture from unresolved mechanics. An unresolved mechanic must remain
`hmmm`; an implementer may not replace the architecture to make the problem easier.

Executed evidence and its exact scope are recorded in [REPORT.md](REPORT.md).
That evidence is not a full-system verdict.

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

Define the preserved end-interleave ordering:

```text
I(S) = s_(n-1), s_0, s_(n-2), s_1, ...
```

continuing inward until every bit appears exactly once.

For an ordered arity schedule

```text
A = (a_1, ..., a_k)
```

each level partitions the relevant working sequence into `a_i` ordered sections and
applies `I` independently to each section. After the declared levels, `I` is applied
to the complete resulting sequence.

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

The exact split/recombination law remains unresolved.

## 4. Corpus/material participation

Each thread may consume or bind caller-selected corpus/material. Examples already
contemplated include literary, musical, technical-manual, and sound material.

The material is intended to participate in construction/recovery. Treating it as an
unused label or merely hashing its filename does not satisfy this architecture.

Exact extraction, addressing, mixing, and recovery dependence remain unresolved.

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
- dependence on the declared corpus/material relation if that layer is enabled;
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
python verify.py receipt.json
```

## hmmm

1. Uneven partition selection rule; the component runner accepts explicit positive
   section lengths without selecting a remainder policy.
2. Whether each arity stage consumes the preceding stage output or composes independent
   partitions before a later merge. The runner's sequential choice is an explicitly
   labelled experiment, not a newly inferred user law.
3. Exact thread split/recombine law.
4. Corpus/material extraction and binding law.
5. Nested gonol representation and reversible serialization.
6. Private-gonol generation and binding.
7. Public/private key derivation and the exact source of asymmetry.
8. Authentication, nonces, state evolution, truncation/replay handling.
9. Threat model and target security properties.
10. Original pre-substitution thirteen-law conversation was not recovered. Missing
    retrieved source is not evidence that the user never specified the relation.
