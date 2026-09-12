# Ordered complete-return groupoid v0

**Standing:** stack-local target-free noncommutative geometric candidate. Not
UCNS canon, not an arithmetic factor map, and not a successor constructor.

## Why this layer exists

The complete-return relation candidate retained only a free abelian basis:

```text
H_1 = Z^r
```

That representation necessarily identifies every ordering with the same
exponent vector. For example, all positive permutations of three generators
map to `(1, 1, 1)`. It cannot express a requirement such as:

```text
g1 g2 g3 != g2 g3 g1 != g1 g3 g2
```

This candidate lifts the same complete-return traces before abelianization.

## Minimal path-groupoid lift

At retained rank `r`, the candidate uses:

- one shared based positive-frame object;
- one relation-specific reversed-frame midpoint for each retained loop;
- one positive-to-reversed edge and one reversed-to-positive edge per loop;
- no filling two-cells and no cross-generator relators.

Each generator therefore has an exact subdivided path:

```text
              ui                         vi
positive base ----> reversed midpoint i ----> positive base
```

The relation-specific midpoint is load-bearing. Identifying every reversed
midpoint without additional relations would create unsupported mixed
half-edge cycles and change the previously declared rank.

The graph has:

```text
vertices = r + 1
edges    = 2r
rank d1  = r
rank H_1 = 2r - r = r
pi_1     = free-group candidate F_r
```

This is the smallest graph lift consistent with the retained rank. It assumes
prior loops include at the promoted positive basepoint unchanged. Actual UCNS
recursive transport could falsify that assumption by supplying nontrivial
monodromy or attaching relations.

## Basepoint and closure

For one relation, the complete loop `ui vi` is based at the positive object.
The one-turn-shifted loop `vi ui` is based at its reversed midpoint. They are
not equal as typed paths. Explicit transport recovers the based loop:

```text
ui (vi ui) ui^-1  ->  ui vi
```

For words using distinct generators, the implementation cancels adjacent
inverse pairs only. It never commutes generators.

There are three separate information levels:

1. Based words preserve every permutation.
2. Oriented unbased closure identifies cyclic rotations by conjugacy.
3. Abelianization retains only signed generator counts.

The exact once-each counts are:

| rank | based words `r!` | oriented cyclic classes `(r-1)!` | H1 vectors |
|---:|---:|---:|---:|
| 1 | 1 | 1 | 1 |
| 2 | 2 | 1 | 1 |
| 3 | 6 | 2 | 1 |
| 4 | 24 | 6 | 1 |

Thus all six triadic permutations remain distinct as based paths. If a later
closure forgets the basepoint, they split into two oriented cyclic classes:

```text
{g1 g2 g3, g2 g3 g1, g3 g1 g2}
{g1 g3 g2, g3 g2 g1, g2 g1 g3}
```

Orientation reversal is not identified. UCNS geometry must authorize that
additional quotient if it is required.

## Boundary

This candidate establishes representation capacity, not geometric word
selection. Current recursive geometry does not yet say:

- which cross-generator traversal word occurs;
- how a full recursive return acts on retained inner loops;
- whether closure keeps a basepoint or takes conjugacy classes;
- whether generators cross, link, intersect, or satisfy attaching relators.

No arithmetic observation, observed factor, or desired rank enters the
constructor.

## Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/ucns/ordered_complete_return_groupoid.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research/ucns/tests/test_ordered_complete_return_groupoid.py -v
```

Frozen identities:

```text
ordered_complete_return_groupoid.py sha256 = d1c83252371bbe50fbc7d514bba43de6685d8eb5045060037941d38a5914b6e5
test module sha256                          = 8a7e274fc0ade6d9979b5116add27665d3dfcf1168632392ae52ba4ff47fea49
canonical receipt payload sha256            = cf61151f9e9ce1479b6d7eb95ff51bb2a683045de292243e1f14a9b3dd050f69
formatted receipt file sha256                = 741495c16f3d1b439663aa1710e89175c3f1ee67d5b6c0336d8ecf4cf854d002
```

## hmmm

- Is recursive promotion actually a basepoint-preserving inclusion of prior
  loops, or does it transport them through a nontrivial automorphism?
- Which based or cyclic traversal does full UCNS closure select?
- What cross-generator geometry supplies relators without fitting arithmetic
  observations?

