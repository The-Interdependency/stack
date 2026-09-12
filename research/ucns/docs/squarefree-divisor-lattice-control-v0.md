# Squarefree divisor-lattice control v0

**Standing:** `PREREGISTERED_STRUCTURAL_CONTROL`, frozen after the first
three observations and before any fourth observation. This is an arithmetic
classification and a nonnumeric control, not UCNS canon and not a gonol
successor constructor.

## Exact observation witnesses

Deterministic trial factorization gives:

```text
157         = 157
2881        = 43 * 67
54837698421 = 3 * 11 * 1661748437
```

Every displayed factor is prime and every exponent is one. Therefore:

| observation | omega | tau | mu | divisor lattice |
|---:|---:|---:|---:|---:|
| `157` | 1 | 2 | -1 | `B_1` |
| `2881` | 2 | 4 | +1 | `B_2` |
| `54837698421` | 3 | 8 | -1 | `B_3` |

For a squarefree integer with `k` distinct prime factors, each divisor is the
product of one subset of those factors. Divisibility is subset inclusion, so
the divisor lattice is the Boolean lattice `B_k`. The receipt freezes the full
subset-product bijection and the rank counts:

```text
B_1: 1,1
B_2: 1,2,1
B_3: 1,3,3,1
```

This establishes the arithmetic structure exactly. It does not establish that
the factors are UCNS components or that Boolean-lattice independence is
geometric independence.

## Frozen structural control

The next structural observation is preregistered as:

```text
observation index = 4
numeric value     = hmmm
squarefree        = true
omega             = 4
tau               = 16
mu                = +1
divisor lattice   = B_4
```

An independently obtained fourth gonol falsifies the full control if any one
of those structural invariants fails. A full match has standing
`SURVIVED_ONE_OUT_OF_SAMPLE_TEST`; it still would not recover a constructor.

## UCNS mechanics audit

The pinned UCNS sources and all three executable research mechanics were
audited for a map from recursive geometry to independent multiplicative
factors.

```text
mechanic 1: fixed 157-position carrier transformations -> arity stays 157
mechanic 2: coupling arity -> length of caller-supplied participant tuple
mechanic 3: one closed affinization -> one atomic participant
next carrier cardinality -> undefined
declared product decomposition -> absent
declared arithmetic-factor-to-geometry map -> absent
declared add-one-prime-dimension transition -> absent
```

The smallest prior composition still produces `157 -> 629`, not `2881`.
UCNS canon also leaves the full recursive-scale transition unresolved, the
carrier floor explicitly excludes factorization and product character, and
the prime-primitive module separates arithmetic primality from UCNS primitive
standing. Prime-indexed geometry is therefore not evidence that a composite
gonol cardinality decomposes into prime-indexed geometric components.

Result:

```text
ARITHMETIC_PATTERN = EXACT
STRUCTURAL_CONTROL = FROZEN
NUMERIC_N4 = hmmm
UCNS_FACTOR_EXPLANATION = UNRESOLVED_NO_DECLARED_FACTOR_MAPPING
```

## Retained local failure

The event-pair mechanism remains useful negative evidence:

```text
39 pairwise projection events
21 band-pair relations
C(39,2) - 21 = 720
1 + 4*720 = 2881
```

Applied unchanged:

```text
C(720,2) - 21 = 258819
1 + 4*258819 = 1035277 != 54837698421
```

Thus `39 -> 720` is an exact local accounting identity and a falsified
recursive mechanism. It is retained in the new receipt rather than discarded.

## Required explanatory experiment

Before attempting a numerical `n4`, a UCNS candidate must execute all of the
following without using successor targets to define its operations:

1. Decompose each closed gonol into geometrically identified independent
   components whose carrier cardinalities multiply.
2. Derive each component's prime cardinality from geometry while preserving
   the arithmetic-prime/UCNS-standing firewall.
3. Promote the closed whole across scale while preserving existing components
   and introducing exactly one independently derived component.
4. Reconstruct all three observed cardinalities under one unchanged operation.
5. Freeze its fourth numerical output before comparison.

Until those operations exist, `B_1 -> B_2 -> B_3` is the strongest surviving
structural observation, not an explanation.

## Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/ucns/squarefree_divisor_lattice_control.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research/ucns/tests/test_squarefree_divisor_lattice_control.py -v
```

Frozen identities:

```text
squarefree_divisor_lattice_control.py sha256 = 34b4a3602f42a216bda0ffea8096fac47efd83338fc15a96bf27d79aa9914e32
test module sha256                           = 6411e5eeb5b9c1eaaffbf33eb84747fafecebf7d68d648fe733f75140b3fc180
canonical receipt payload sha256             = 1c23366a6aabc5dbd576aea07c03fc46a13c10822ada9e8c6198f6043d2933b8
formatted receipt file sha256                = 74f28753efb23e5f321d0e6b32719bf33db9107422b4cd9629afaf36a2a25ed5
```

## hmmm

- Why do the observed cardinalities add one Boolean divisor-lattice dimension
  at each scale?
- Is there a UCNS product construction whose factor axes are geometrically
  independent, or is the arithmetic pattern incidental?
- Why does the exact event-pair identity explain the first local lift but fail
  under unchanged recursion?
- Which geometric evidence would identify the next independent component
  before its cardinality is observed?
