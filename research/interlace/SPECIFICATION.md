# Interlace — specification floor

Status: **PRE-SPECIFICATION / PRESERVED MECHANISM**.

This document records what is fixed, what is forbidden to substitute, and what remains
`hmmm`. It is deliberately smaller than an implementation specification.

## 1. Objects

- `B`: the input plaintext represented as an ordered bit sequence.
- `A = (a_1, ..., a_k)`: an ordered sequence of division arities.
- `k >= 3`: minimum declared number of arity levels.
- `I(S)`: end-interleave of one finite bit sequence `S`.

For a sequence

```text
S = s_0, s_1, ..., s_(n-1)
```

the preserved end-interleave order begins

```text
s_(n-1), s_0, s_(n-2), s_1, ...
```

and continues inward until every bit appears exactly once.

## 2. Declared transform skeleton

For each arity level `a_i`:

1. partition the working bit sequence into `a_i` ordered sections;
2. apply `I` independently to every section;
3. preserve all bits exactly once.

After all declared arity levels, apply `I` once to the entire working sequence.

Example arity sequence already specified in discussion:

```text
(5, 7, 3)
```

The example is evidence of the mechanism, not a declaration that `(5,7,3)` is the
only or preferred schedule.

## 3. Required invariants

Any implementation claiming conformance must preserve all of these:

- **bit conservation** — no bit is added, removed, duplicated, or changed by the core
  interleaving transform;
- **order-sensitive arity schedule** — changing arity order is a different transform;
- **level-count sensitivity** — omitting or adding a level is a different transform;
- **section-local end interleave** — each section uses the declared last/first inward
  operation;
- **whole-sequence final interleave** — the final operation acts across the resulting
  complete bit sequence;
- **exact invertibility** — given all required reconstruction information, the original
  bit sequence must be recovered exactly.

## 4. Forbidden substitutions

The following do not implement this specification merely because they are reversible or
cryptographic:

- recursive pairing codecs;
- authenticated framing;
- substitution with AES, ChaCha, a Feistel network, XOR stream masking, or another
  standard primitive;
- hashing the plaintext and treating the digest as the transform;
- replacing section interleaving with generic permutation generation;
- reducing the arity schedule to a conventional integer key without preserving its
  specified structural role;
- importing URPCS Laws 1–13.

Conventional primitives may later be composed around the construction only when their
role is separately declared. They may not replace the construction being tested.

## 5. Falsification targets

The first implementation must make it cheap to test:

1. exhaustive inversion across small bit lengths and multiple schedules;
2. whether different schedules collide on the same permutation;
3. how much of the schedule can be recovered from known plaintext/ciphertext pairs;
4. whether the transform leaks bit-position relations or periodic structure;
5. whether repeated or highly structured plaintext remains visibly structured;
6. whether the effective permutation family grows meaningfully with arity depth;
7. whether thread, corpus, or hyperspace layers add independent security properties or
   merely obscure the same permutation.

Failure on these tests is useful evidence. It must not trigger replacement of the
mechanism with a familiar cipher.

## 6. Later-layer boundary

Potential later layers already contemplated:

- three/five/seven-or-more interlaced streams or threads;
- caller-selected corpus/material per thread;
- plaintext-to-hyperspace/gonol preprocessing;
- a private gonol participating in recovery.

None is part of the executable core until its own input, output, inverse, and security
claim are explicitly specified.

## Usage guidance

An implementer must read this document before writing transform code. For every
unresolved choice below, implementation should raise/refuse rather than select a
default. Tests should identify the exact specification revision they exercise.

## hmmm

1. **Uneven partition rule:** how `n mod a_i` bits are distributed when a bit length
   is not divisible by the arity.
2. **Stage input rule:** whether level `i+1` partitions the output of level `i` or
   independently partitions the original/raw bit sequence before a later composition.
3. **Schedule encoding:** how arities, order, and level count are represented and bound
   to recovery.
4. **Thread construction:** exact relationship between sections, threads, and corpus
   material.
5. **Hyperspace binding:** exact reversible relation among plaintext, gonol construction,
   private gonol, and the core transform.
6. **Authentication/state:** whether integrity, nonces, state evolution, or replay
   protection belong to the eventual system and at which layer.
7. **Threat model:** attacker capabilities and the minimum security properties the
   construction is intended to provide.
