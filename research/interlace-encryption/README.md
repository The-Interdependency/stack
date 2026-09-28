# Interlace Encryption Research

Standing: **stack-local research; specification-first; no security claim**.

This workspace exists to pursue Erin Spencer's intended encryption construction after
the retirement of URPCS. It is a new project. It does not inherit URPCS code, Laws
1–13, codec architecture, tests, measurements, security conclusions, or terminology.

The project begins from the mechanisms Erin actually specified and keeps unresolved
mechanics unresolved until they are explicitly selected.

## Preserved construction

The current specification floor is:

1. Operate on the plaintext as a raw bit sequence.
2. Use an ordered sequence of arity/division levels, with at least three levels.
3. At each declared level, divide the working bit sequence into the declared number
   of sections; examples already given include fifths, sevenths, and thirds.
4. Within each section, interleave from the two ends: last bit, first bit,
   next-to-last bit, next-from-first bit, continuing inward until the section is
   exhausted.
5. Apply the declared sequence of arity levels without replacing the mechanism by
   pairing, framing, hashing, authentication, a standard cipher mode, or another
   familiar construction.
6. After the declared levels, apply the corresponding end-interleave to the whole
   resulting bit sequence.
7. Reconstruction depends on knowing the division/arity choices, their order, and
   how many levels were used. Those choices are therefore part of the intended
   private reconstruction information unless a later explicit law says otherwise.

These statements define the mechanism to investigate. They do **not** establish
confidentiality, entropy, pseudorandomness, key strength, resistance to known-plaintext
or chosen-plaintext attack, or production suitability.

## Intended later layers

Two related ideas are retained as intended research directions, but are not silently
folded into the core transform:

- multiple interlaced threads, potentially three, five, seven, or more, with
  caller-selected corpus/material associated with individual threads;
- preprocessing or binding plaintext through a hyperspace/gonol construction, with a
  private gonol participating in recovery.

Each requires its own explicit contract before implementation. Neither may be
invented from analogy to URPCS, PCEA, UCNS, or conventional cryptographic systems.

## Non-inheritance boundary

`research/urpcs/` is historical evidence of a substituted GPT-produced construction.
Nothing from it is an implementation dependency here. A result proved against URPCS
does not transfer into this workspace.

If comparison with URPCS is ever useful, URPCS is treated only as a negative
specification-divergence witness: an example of what must not be substituted for the
declared construction.

## Development order

1. Freeze exact bit-level transformation laws.
2. Resolve only the minimum missing mechanics needed to make the transform invertible.
3. Write an executable reference transform with exhaustive small-input inverse tests.
4. Build an independently structured inverse from the written contract.
5. Measure information leakage and structural distinguishability before adding
   authentication, key wrapping, gonol binding, or corpus-thread layers.
6. Add later layers one at a time, preserving ablation tests so their contribution can
   be measured rather than presumed.
7. Only after adversarial cryptanalysis may the project make a bounded security claim.

## Usage guidance

Start with the specification, not code:

```bash
cat research/interlace-encryption/SPECIFICATION.md
cat research/interlace-encryption/BASE.json
```

Before implementing a missing rule, update the specification so the rule is explicit
and attributable. An implementation must fail rather than choose an unresolved rule
for convenience.

Do not use this workspace for protecting real secrets until a later security contract
and adversarial evidence explicitly authorize that use.

## hmmm

Exact handling of uneven section lengths, whether each arity stage consumes the prior
stage's output or independently re-partitions the original input, representation of the
private arity schedule, thread/corpus binding, hyperspace/gonol binding, authentication,
nonce/state requirements, and the threat model remain unresolved. Their absence is part
of the current specification and must not be filled by model preference.
