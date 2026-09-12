# Complete-return relation-rank experiment v0

**Standing:** stack-local post-observation rank comparison. The geometric
candidate was frozen first, but the candidate class was selected after the
observed factor-lattice pattern was known. Matches are therefore retrodictive,
not out-of-sample validation.

## Frozen candidate

Before opening any arithmetic comparison gate, the experiment binds:

```text
candidate code sha256    = 7c09ee73fe18ea0489f1a7cee5738b140d761dab6d09fcba6104d7ff4a8b5f53
candidate receipt sha256 = f1ebfed99730b338a8b716ae4f7e2984c243ee294d7806f54182c24c849ceaea
candidate validation     = NOT_COMPARED_WITH_OBSERVED_SCALES
```

The same complete-return operation is then run four times. All relation
outputs and their aggregate digest are frozen before reading the observed
arithmetic ranks.

## Generated ranks

```text
scale 1: 0 -> 1
scale 2: 1 -> 2
scale 3: 2 -> 3
scale 4: 3 -> 4
```

Every step uses the same native return trace, preserves all prior relation ids,
and appends one distinct geometry-derived relation id.

## Observation gates

Only after generation, the first three outputs are compared with the frozen
squarefree witnesses:

| scale | generated complete-return relation rank | observed arithmetic omega | result |
|---:|---:|---:|---|
| 1 | 1 | 1 | match |
| 2 | 2 | 2 | match |
| 3 | 3 | 3 | match |

Result:

```text
RELATION_RANK_GATE = TARGET_FREE_RETRODICTIVE_RELATION_RANK_MATCH
NEXT_RELATION_RANK = 4
NEXT_FACTOR_CARDINALITIES = hmmm
NUMERICAL_NEXT_GONOL = hmmm
FACTOR_MAPPING = UNRESOLVED_NO_CYCLE_TO_ARITHMETIC_FACTOR_MAP
```

The generated fourth relation rank agrees with the already-preregistered
structural `omega=4` control. It is not a new independent prediction because
that control and the motivating pattern predate this candidate.

## What advanced

UCNS now has an executable geometric candidate that creates one new
independent **topological relation** dimension at recursive closure. The prior
mechanics audit had no such operation.

What remains missing is equally precise: no executable UCNS operation assigns
an arithmetic-prime cardinality to the new return-cycle generator or proves
that gonol cardinalities multiply over these generators. Consequently this
candidate cannot derive `2881`, `54837698421`, or a numerical fourth gonol.

## Next falsifiable construction

The next research target is no longer "find an operation that adds one
dimension." One bounded candidate now exists. The target is:

1. Construct the return-loop attachment in full higher-dimensional UCNS
   geometry and test whether the cycle survives closure.
2. Derive any monodromy action on retained inner relation generators.
3. Define a geometric component-cardinality readout for each surviving
   generator without using observed factors.
4. Test whether those independently derived cardinalities multiply to the
   three observed gonols.

Failure at steps 1 or 2 falsifies the relation-extension candidate. Failure at
steps 3 or 4 leaves the topological rank mechanism intact but falsifies its
interpretation as the source of the Boolean factor-lattice progression.

## Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/ucns/complete_return_relation_rank_experiment.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research/ucns/tests/test_complete_return_relation_rank_experiment.py -v
```

Frozen identities:

```text
complete_return_relation_rank_experiment.py sha256 = 248001fd757faa8d88f02c6453fe039b4b09d65d9fd2f3c60911e3d6ea8ebbb6
test module sha256                              = 592276739717c00d0b250857d01097a3a4989e6065d6917f634a2d4ff9789c61
canonical receipt payload sha256                = 5b35e5ccfcdc253161a5a34dc99a3652c81c77f898df02d3e8d527c784dcc8f7
formatted receipt file sha256                   = 92b72bc946946c48a31966b6ca80cc7edb48dc7051fce598cbd8dae3d919d8d0
```

## hmmm

- The rank matches are retrodictive and need the independently observed fourth
  gonol for an out-of-sample structural gate.
- Full UCNS closure may fill the return loop or act nontrivially on inner
  relations.
- A relation generator has no currently derived prime cardinality.
- Numerical `n4` remains premature.
