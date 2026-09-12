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
canonical receipt payload sha256         = 330581ff3edbb3b3b99021e9c026e585dc4619c0ae60e9f1d1425c350c834482
formatted receipt file sha256            = 12e3355220d843ba3ae67422b06921f0468709721d8b56738d8b0c540e7ca2a0
```

## hmmm

- The identity `720 = C(39,2)-21` is structurally sharper than interpolation,
  but one matched gate cannot establish its invented quotient semantics.
- The failed unchanged second gate rules it out as the recursive law.
- Actual relation rank must come from the completed object at each scale; it
  cannot be solved backward from the target.
