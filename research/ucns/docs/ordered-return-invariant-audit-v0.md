# Ordered return invariant audit v0

**Standing:** stack-local target-free noncommutative invariant audit. Not UCNS
canon, not an arithmetic bridge, and not a next-gonol prediction.

**Next gate result:** the later
[geometry-selected based traversal audit](geometry-selected-based-traversal-audit-v0.md)
finds no current Public Gonol attachment, orientation, marked rotation system,
or closure rule that selects one of the representable words. Its status is
`STOP_NO_GEOMETRY_SELECTED_BASED_TRAVERSAL`.

## Exact ordered invariants

The audit consumes the frozen ordered path-groupoid candidate and follows the
same ordering boundary already present in canonical UCNS prime analysis:

```text
geometry-derived words
-> noncommutative Fox/Magnus data
-> explicit later abelian specialization
```

Only that architecture transfers. Canonical prime-selected P7/P5 diagrams do
not define recursive return words or arithmetic factors.

### Fox derivative

For a freely reduced word in `F_r`, the audit computes exact derivatives in
the integral group ring `Z[F_r]` using:

```text
d(xj)/d(xi)     = delta_ij
d(uv)/d(xi)     = d(u)/d(xi) + u d(v)/d(xi)
d(xj^-1)/d(xi) = -xj^-1 delta_ij
```

Every result is checked against the noncommutative fundamental identity:

```text
sum_i d(w)/d(gi) (gi - 1) = w - 1
```

For `w = g1 g2 g3`, the exact derivatives are:

```text
d(w)/d(g1) = 1
d(w)/d(g2) = g1
d(w)/d(g3) = g1 g2
```

The prefixes retain order.

### Magnus expansion

The audit also applies `gi -> 1 + Xi` in a noncommuting power-series ring,
truncated through degree two. Degree one is exactly the exponent-vector
projection to `H_1`; degree two records ordered pairs.

For all six positive permutations of three generators:

```text
based words                         = 6
distinct Fox fingerprints           = 6
distinct degree-two Magnus records  = 6
distinct H_1 vectors                = 1
```

This is executable evidence that order survives below homology and is erased
by abelianization.

## Monodromy obstruction

The audit constructs two exact automorphism witnesses with explicit inverses:

```text
rank 2: g1 -> g2 g1 g2^-1, g2 -> g2
rank 3: g1 -> g1 [g2,g3],  g2 -> g2, g3 -> g3
```

Both are nonidentity on based words and identity on `H_1`. The rank-two case
is inner and may become a basepoint change if only outer monodromy matters.
The rank-three commutator shear demonstrates the stronger obstruction: once
three generators exist, commutator information can change while every
homology coordinate remains fixed.

Therefore the prior statement that relation ids persist in `Z^r` does not
authorize identity monodromy in `F_r`.

## Authority surface audit

The receipt binds six exact source surfaces and distinguishes the order each
one actually owns from the recursive geometry it does not own:

- Public Gonol canon owns position order, but declares position operations
  unresolved.
- Native Mobius canon owns local frame order, but declares higher attachment
  unresolved.
- The functional-operation research layer owns candidate total carrier
  permutations, but does not canonically select one.
- Affinization owns caller-supplied participant slot order, but has no
  coordinate or topological rule that derives that order.
- Recursive promotion preserves constituent records, but supplies no
  next-scale placement or free-group transport.
- The Mobius seed owns exact event turns and over-under changes, but has no
  authorized map from those events to Public Gonol recursive relation words.

This rules out treating ordered source data as if it were already a derived
recursive traversal or monodromy.

## Presentation gate

Fox derivatives of a traversal word are fingerprints, not matrix rows unless
geometry declares that word to be a relator. Current recursive return geometry
provides:

```text
generators                       = g1, g2, g3, g4
geometry-derived relators        = none
global based monodromy           = unresolved
crossings/linking/intersections  = unresolved
```

The current candidate is consequently the free group `F_4`, not a finite
presentation with a determinant. The audit fails closed with:

```text
ORDERED_LAYER_EXECUTABLE__MONODROMY_PRESENTATION_AND_FACTOR_BRIDGE_UNRESOLVED
```

No Fox presentation matrix, canonical finite integer invariant,
factorization, observation comparison, or numerical successor is emitted.
This is not another determinant search. The next required object is an exact
geometry-selected attaching or monodromy word.

## Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/ucns/ordered_return_invariant_audit.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research/ucns/tests/test_ordered_return_invariant_audit.py -v
```

Frozen identities:

```text
ordered_return_invariant_audit.py sha256 = fb33b5b7ab7a5053c75389c11378c4e31b67fb2b9b1dfaae089bdb2056df05d4
test module sha256                       = b166d06239b9efedacaefc3a6b567fa03785b2b2b6488bbdac97f10dd9dc08ba
canonical receipt payload sha256         = 18a2ddffd70aef891a4fab6d1a202642faf10f1f4ee8ae11aeabeeb3163df2d1
formatted receipt file sha256             = 0bfba647fcea7765eea624b5f4c3a7137ffec8b7581034d5bb4defbadd46420f
```

## hmmm

- What exact recursive UCNS path chooses a word among the representable
  permutations?
- What based free-group automorphism does one full recursive return induce?
- Which geometric crossings or attachments turn words into relators?
- What target-free representation or specialization, if any, turns that
  frozen presentation into a finite arithmetic readout?
