# Event-pair quotient candidate v0

**Standing:** stack-local post-observation candidate, falsified at the second
gate. Not UCNS canon and not a recursive gonol law.

## Candidate

The pinned Mobius Seed supplies exact counts independently of the observed
successor values:

```text
pairwise projection events = 39
all band-pair relations     = 21
boundary multiplicity       = 4
origin                      = 1
```

The candidate treats event states as generators of an exterior pair space and
assigns one independent rank-one quotient constraint to each band-pair
relation:

```text
Q(x) = C(x, 2) - 21
L(x) = 1 + 4*x
```

UCNS does not currently declare this exterior space or constraint
independence. They are explicit candidate assumptions, introduced after the
observations were known.

## First gate

```text
C(39, 2) = 741
Q(39)    = 741 - 21 = 720
L(720)   = 2881
```

This is an exact relationship among the pinned geometry counts and the first
observed successor. Its standing is `RETRODICTIVE_MATCH_ONLY`.

## Unchanged second gate

The same operator and the same constraint rank are then applied without target
constants or tuning:

```text
C(720, 2) = 258840
Q(720)    = 258840 - 21 = 258819
L(258819) = 1035277
```

The observed second successor is `54837698421`, so:

```text
EVENT_PAIR_QUOTIENT = FALSIFIED
CONSTRUCTOR_SURVIVORS = 0
NEXT_PREDICTION = hmmm
```

Changing the quotient rank after seeing this mismatch would define a different
candidate and would require an independently constructed `2881` relation
ledger.

## Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/ucns/event_pair_quotient_candidate.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research/ucns/tests/test_event_pair_quotient_candidate.py -v
```

Frozen identities:

```text
event_pair_quotient_candidate.py sha256 = 42289230971ec3d47081b22254d19a1cf26b12537b3ed0f241702ec3057b71bc
test module sha256                       = f94880ecdfb7c00930f7452b28876401078889e59ab890816364189a80242d09
canonical receipt payload sha256         = 209eccd83f6aa280a76a5f38700ee760e13e754568dc25c79f9f05e2ffd92d91
formatted receipt file sha256            = 680bac02213f032cbb18251e4be0484ffa0c61ee9597b4d131daa0f622c806b5
```

## hmmm

- The identity `720 = C(39,2)-21` is structurally sharper than interpolation,
  but one matched gate cannot establish its invented quotient semantics.
- The failed unchanged second gate rules it out as the recursive law.
- Actual relation rank must come from the completed object at each scale; it
  cannot be solved backward from the target.
