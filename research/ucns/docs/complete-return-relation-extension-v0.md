# Complete-return relation extension v0

**Standing:** stack-local target-free geometric candidate. Not UCNS canon, not
a successor-cardinality constructor, and not an arithmetic factor operation.

## Geometric derivation

Pinned UCNS native Mobius geometry defines exact framed states under:

```text
(t, frame) ~ (t + n, (-1)^n frame)
```

The candidate uses only the exact integer-turn trace:

```text
turn 0: phase 0, positive frame
turn 1: phase 0, reversed frame
turn 2: phase 0, positive frame
```

All three occurrences have the same visible phase. The one-turn state is not
the same complete state because its frame is reversed. Only the two-turn state
can be identified with the start.

The resulting quotient has two vertices and two directed edges:

```text
positive -> reversed -> positive
```

Its integer boundary map from edge chains to vertex chains is:

```text
[ -1  1 ]
[  1 -1 ]
```

The matrix has rank one. With two edge generators and no filling two-cell in
the declared root-loop boundary:

```text
rank H_1 = dim C_1 - rank boundary_1 - rank image(boundary_2)
         = 2 - 1 - 0
         = 1
```

This is the independently derived operation: one exact complete-return loop
contributes one topological relation generator.

## Recursive composition

The pinned Public Gonol carrier supplies the starting atomic identity. For one
extension:

1. Create separately addressed zero-turn and one-turn occurrences of the same
   source atom.
2. Close their ordered coupling under the exact two-turn return trace.
3. Append the trace's one `H_1` generator to the retained prior relation basis
   and bind the complete ordered basis digest into the coupling closure.
4. Promote that basis-bound closed whole through the recursive-scale research
   mechanic.

Repeated execution preserves every prior relation id and adds exactly one new
id per scale:

```text
source relation ranks: 0, 1, 2, 3
output relation ranks: 1, 2, 3, 4
rank delta:            1, 1, 1, 1
```

The candidate source and frozen receipt contain no observed successor
cardinality, arithmetic factorization, omega sequence, or requested next rank.

## Boundary

The root-loop calculation is exact. Its recursive interpretation remains a
candidate because UCNS authority has not yet constructed the attachment to the
higher circle, epicycle, disk, sphere, or full gonol geometry.

The candidate is falsified if:

- a required higher-dimensional two-cell fills the return loop and kills its
  `H_1` generator;
- later geometry applies nontrivial monodromy to retained inner relations;
- atomic promotion drops or identifies an existing relation generator;
- complete closure occurs at one visible turn despite the reversed frame; or
- target arithmetic enters the operation definition.

A topological cycle generator is not automatically an arithmetic prime-factor
axis. That mapping requires a separate geometric construction.

## Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/ucns/complete_return_relation_extension.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research/ucns/tests/test_complete_return_relation_extension.py -v
```

Frozen identities:

```text
complete_return_relation_extension.py sha256 = 7c09ee73fe18ea0489f1a7cee5738b140d761dab6d09fcba6104d7ff4a8b5f53
test module sha256                         = 0827dfd52da3d880efe5f3c61d60c2fcd920fa4b45ffc02dcdc2d71cf5a532c9
canonical receipt payload sha256           = f1ebfed99730b338a8b716ae4f7e2984c243ee294d7806f54182c24c849ceaea
formatted receipt file sha256              = 5475b0839b80ddc892d94256dd5e138838ff7f71e4d5eda6901584b614b60e03
```

## hmmm

- Does full gonol closure retain the root-loop generator, or does a disk or
  sphere attachment fill it?
- Is the outer return loop independent of all retained inner relations under
  the actual recursive monodromy?
- What UCNS geometry, if any, turns this relation generator into a component
  with independently derived arithmetic-prime cardinality?
