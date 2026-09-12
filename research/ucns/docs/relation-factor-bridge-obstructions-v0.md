# Relation-to-factor bridge obstructions v0

**Standing:** stack-local post-observation obstruction audit. Not UCNS canon
and not a factor-cardinality constructor.

**Later refinement:** the [ordered return invariant audit](ordered-return-invariant-audit-v0.md)
shows that an integer presentation matrix is a downstream acceptance gate, not
the primary next research object. `H_1 = Z^r` has already erased traversal
order. UCNS must first derive noncommutative traversal, attaching, and
monodromy words from geometry; only a frozen presentation and specialization
may later feed this document's integer readout.

## Question

The complete-return candidate supplies nested relation bases of ranks:

```text
G1 subset G2 subset G3 subset G4
rank: 1, 2, 3, 4
```

Can each relation generator receive a target-free arithmetic-prime cardinality
whose product is the gonol cardinality?

The audit now eliminates two natural interpretations and identifies the extra
geometry required by any survivor.

## Obstruction 1: stable generator labels

Assume one stable map `p(g)` assigns a fixed prime to every persistent
generator and:

```text
n_s = product of p(g) for g in G_s
```

Because `G_s` is retained inside `G_(s+1)`, this requires:

```text
n_s divides n_(s+1)
factor_set(n_s) subset factor_set(n_(s+1))
```

The observations give:

```text
factor_set(157)         = {157}
factor_set(2881)        = {43, 67}
factor_set(54837698421) = {3, 11, 1661748437}

gcd(157, 2881)                 = 1
gcd(157, 54837698421)          = 1
gcd(2881, 54837698421)         = 1
```

No factor set is nested. The three gonol cardinalities are pairwise coprime.
Therefore:

```text
STABLE_PERSISTENT_GENERATOR_PRIME_PRODUCT = FALSIFIED
```

If the relation-rank correspondence is real, prime identities must be a global
readout recomputed at each scale rather than permanent labels carried by the
retained generators.

## Obstruction 2: local trace maps

Every generated relation uses the same exact native complete-return trace. All
four trace payloads replay with one digest. Any isomorphism-invariant map from
that local trace alone must assign the same value `p` to every generator.

At rank two the product would be:

```text
p * p = p^2
```

That is not squarefree, while the second observed gonol is squarefree with two
distinct prime factors. Therefore:

```text
LOCAL_COMPLETE_RETURN_TRACE_TO_PRIME_MAP = FALSIFIED
```

Different generator hashes or scale indices can distinguish occurrences, but
they are addresses rather than geometric measurements. Hash-to-prime and
index-to-prime rules are rejected even when deterministic and target-free.

## Obstruction 3: free homology has no finite order

The current return loop has no filling two-cell. One loop contributes `Z`, and
the retained rank-`r` relation module is:

```text
H_1 = Z^r
torsion invariants = none
finite order = none
```

A free generator does not contain a canonical finite prime cardinality. A
finite prime order requires additional geometric relations, such as
degree-two attachment, linking, intersection, or monodromy coefficients.

## Remaining bridge class

The surviving class is global rather than generator-local. Let geometry derive
a square integer presentation matrix `R_s` over the complete relation basis.
If `det(R_s)` is nonzero, its cokernel is finite and:

```text
cardinality = abs(det(R_s))
prime identities = exact factorization of abs(det(R_s))
```

Smith normal form must be retained to distinguish the full finite-group
structure. Because `R_s` can change globally when a new relation enters, this
class does not require factor-set nesting.

The generic exact readout is now executable and requires provenance for every
matrix entry. The geometric matrix itself is not available:

```text
complete-return linking matrix       = hmmm
complete-return intersection matrix  = hmmm
degree-two boundary matrix           = hmmm
monodromy presentation matrix        = hmmm
factor cardinalities                 = hmmm
numerical n4                         = hmmm
```

UCNS prime primitives do not fill this gap. Their direction is arithmetic
prime label to constructed geometry; they do not invert recursive return
geometry to derive a prime label.

## Result

```text
STABLE GENERATOR MAP = FALSIFIED
LOCAL TRACE MAP = FALSIFIED
HASH OR SCALE MAP = REJECTED_NON_GEOMETRIC
FREE-HOMOLOGY ORDER MAP = FALSIFIED
GLOBAL INTEGER PRESENTATION = BLOCKED_MISSING_GEOMETRIC_PRESENTATION
EXECUTABLE FACTOR MAPS = 0
NUMERICAL N4 = hmmm
```

The next experiment must derive matrix entries from exact interactions among
all retained return generators. Factoring a matrix chosen after seeing the
targets would be another interpolation and is prohibited.

## Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/ucns/relation_factor_bridge_obstructions.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research/ucns/tests/test_relation_factor_bridge_obstructions.py -v
```

Frozen identities:

```text
relation_factor_bridge_obstructions.py sha256 = 03f615131e74a2b1b7ef53e1d645eef01572d8b78ffaf2d77daa6e41fd07f466
test module sha256                           = b25a45fa4e2b5eaeb32a6e87b3bfc109c264951fb7f8d130746a922ba664dc57
canonical receipt payload sha256             = 2d3f06ce4eedc80ab030177b1dee79b8d6a109b4477ba7f7e0836ab4afad699c
formatted receipt file sha256                = ee494d0ab622748856f8be301d5b7dc39ba6fb51eff3c2f8b388f5e12b6ad6c3
```

## hmmm

- What exact higher-dimensional interaction pairs distinct complete-return
  generators?
- Does recursive monodromy supply an integer presentation, and can its entries
  be replayed without target arithmetic?
- Can one matrix-construction law recover all three observed factor multisets?
- Until then, relation rank four does not identify four primes.
