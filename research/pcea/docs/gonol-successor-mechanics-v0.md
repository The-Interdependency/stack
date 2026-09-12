# Gonol successor mechanics v0

Status: stack-local research, not canon.

Actor lane: A.

## Purpose

This run begins the actual successor-construction research gate. It starts from
the stack-pinned UCNS 157-position Public Gonol carrier and the available
construction/closure rules. It does not fit formulas to:

```text
157 -> 2881 -> 54837698421
```

The observed targets are comparators only. Candidate operations receive the
pinned mechanics and the current gonol size; they do not receive the target as a
parameter.

## Source identities

```text
stack_work_graph_sha256 = 0760abd60f089266405aa589063a7533f485761e2bd25faa44f2eac64fb89f7d
pcea_source_commit = 4d2c581448b97bfb71da92b35487e74e6e3bcedc
ucns_source_commit = 1975fe70cf4e0826a8020c2da3047569e277af64
public_gonol_sha256 = 55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5
```

## Mechanics snapshot

Available from pinned UCNS:

```text
Public Gonol arity = 157
Public Gonol origin = index 0, glyph SPACE
Public Gonol arrangement bytes sha256 = 55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5
Public Gonol arrangement byte count = 737
Mobius visible return = 1 turn
Mobius complete return = 2 turns
visible preimage count = 2 local-frame representatives
```

Available from construction discipline:

```text
eligible completed participants
-> explicit relation or geometrically authorized function application
-> relation enters construction
-> closure with source identity and receipt
-> completed gonol
-> atomic participant at another declared scale
```

Unresolved mechanics:

```text
Public Gonol position operation = hmmm
UCNS affixiation/coupling geometry = hmmm
recursive-scale transition law = hmmm
completed 2881-gonol structure = hmmm
```

## Candidate gate

A mechanics-derived candidate must pass both gates unchanged:

```text
gate 1: f(157) = 2881
gate 2: f(2881) = 54837698421
```

Only after both gates pass may it emit:

```text
next_prediction = f(54837698421)
```

Only after that freeze may it be compared with the interpolation control:

```text
control = 164513086777
```

## Candidate outcomes

| Candidate | Basis | First output | Status |
|---|---|---:|---|
| `atomic_identity_carry` | closed gonol remains atomic at another scale | 157 | `FALSIFIED` |
| `mobius_twofold_lift` | two complete local-frame representatives per visible state | 314 | `FALSIFIED` |
| `mobius_twofold_closed_whole` | two representatives per position plus one closed whole | 315 | `FALSIFIED` |
| `cyclic_order_edges_with_positions` | exact cyclic carrier order plus one successor edge per position | 314 | `FALSIFIED` |
| `cyclic_order_edges_closed_whole` | cyclic successor edges, retained positions, and one closed whole | 315 | `FALSIFIED` |
| `unordered_position_pair_closure` | all unordered pairs, retained positions, and one closed whole | 12404 | `FALSIFIED` |
| `directed_order_pair_closure` | all direction-sensitive ordered pairs, retained positions, and one closed whole | 24650 | `FALSIFIED` |
| `canonical_arrangement_byte_count` | canonical JSON byte count of the exact 157 arrangement | 737 | `FALSIFIED` |
| `complete_public_function_application` | all function positions applied to all positions | n/a | `UNRESOLVED` |
| `affixiate_all_position_pairs` | all pairwise affixiations under UCNS coupling geometry | n/a | `UNRESOLVED` |
| `recursive_scale_transition` | the UCNS recursive-scale transition law itself | n/a | `UNRESOLVED` |

No mechanics-derived candidate produced `2881` from the pinned 157-gonol in this
run. Therefore no candidate advanced to the `2881 -> 54837698421` gate, no next
prediction was frozen, and no comparison against `164513086777` was reached.

## Research result

```text
CONSTRUCTOR_CANDIDATES = 0
NEXT_PREDICTION_AVAILABLE = false
INTERPOLATION_CONTROL_COMPARISON = not reached
```

The control remains valuable precisely because it is the dumb interpolation
prediction. The current mechanics research says only that the available pinned
mechanics do not yet expose an operation that independently reaches even the
first gate.

## Replay

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/pcea/gonol_successor_mechanics.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research.pcea.tests.test_gonol_successor_mechanics
```

## Deterministic receipt

```text
receipt_schema = the-interdependency.stack-research.pcea.gonol-successor-mechanics
receipt_version = 0.1.0
producer_code_reference = sha256:dccaddbcd54ccd13a204d56f2a36f67f08251d489a494456b7896bb8aa716ccb
receipt_sha256 = 9944ca5e4ca10be3f59d38d48b28640a21897df04a32829aebfafca72629dbd5
```

## Non-claims

This research note does not establish:

- a UCNS canon successor constructor;
- PCEA runtime behavior;
- a fitted recurrence;
- a hidden transition operator;
- cryptographic security;
- entropy or hardness from gonol size;
- public authenticity receipts.

## hmmm

- The exact operation of each Public Gonol function position remains unresolved.
- The exact UCNS affixiation/coupling geometry remains unresolved.
- The recursive-scale transition law remains unresolved.
- The completed 2881-gonol structure is not available, so structural operations
  that require its constituents cannot run a second-stage test.
- The next experiment should freeze a candidate operation over actual Public
  Gonol constituent relations/closure that reaches `2881` from `157` without
  using `2881`, then run the unchanged operation against the second gate.
