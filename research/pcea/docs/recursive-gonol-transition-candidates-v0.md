# Recursive gonol transition candidates v0

Status: stack-local research, not canon.

Actor lane: A.

## Source identity

This candidate run is bound to `research/pcea/BASE.json`:

```text
source_repository = The-Interdependency/pcea
source_commit = 4d2c581448b97bfb71da92b35487e74e6e3bcedc
canon_path = ../../libs/pcea
standing = stack-local-research
```

UCNS canon is not modified. PCEA runtime and `../../libs/pcea/` are not
modified.

## Observed data

```text
157 -> 2881 -> 54837698421
```

This document treats those values as observations. It does not claim that an
existing UCNS recursive constructor has been recovered. It does not use a
withheld PCEA prediction as an input.

## Falsification policy

Candidate families must:

- replay both observed transitions exactly;
- emit a positive integer next gonol;
- declare their free assumptions;
- retain `hmmm` for unresolved UCNS geometry and authenticity receipts;
- remain stack-local research unless a later authority promotes them.

## Candidate outcomes

| Candidate | Outcome | Reason |
|---|---|---|
| `constant_delta` | `FALSIFIED` | observed deltas differ |
| `constant_ratio` | `FALSIFIED` | observed ratios differ |
| `integer_affine` | `FALSIFIED` | no integer slope replays both observed transitions |
| `rational_affine_integer_output` | `FALSIFIED` | exact affine replay predicts a non-integer next gonol |
| `constant_square_offset` | `FALSIFIED` | square offsets differ |
| `quadratic_forward_difference_baseline` | `CONTROL` | the unique quadratic through three indexed observations predicts one next value |

## Frozen control

```text
candidate_id = quadratic_forward_difference_baseline
standing = interpolation-control-only
rule = scale indices are consecutive and second finite difference is constant
delta_0_to_1 = 2724
delta_1_to_2 = 54837695540
constant_second_difference = 54837692816
next_delta = 109675388356
next_gonol_prediction = 164513086777
```

Equivalent indexed polynomial for consecutive scale indices `n = 0, 1, 2`:

```text
g(n) = 27418846408*n^2 - 27418843684*n + 157
g(3) = 164513086777
```

This is not a derived UCNS law. Every three indexed observations admit a
quadratic interpolation, so `CONTROL` means only that this is the naive
mathematically sufficient prediction.

It becomes empirical evidence only if an independently executed gonol
construction, derived from gonol relations/closure rather than from fitting
these integers, also produces `164513086777`.

## First actual constructor test

The next research gate must start from the 157-gonol itself:

```text
1. freeze the constituent relations/closure of the 157-gonol;
2. determine an operation on those constituents that produces 2881;
3. apply the same operation to 2881 without using 54837698421 as a target;
4. compare the produced value to 54837698421 only after the operation is frozen.
```

If the operation lands on `54837698421`, then that operation becomes the first
real recursive constructor candidate. If it does not, the candidate operation is
falsified. In either case, `164513086777` remains the dumb interpolation control
for the later next-gonol comparison, not a discovered recursion.

## Replay command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/pcea/gonol_transition_candidates.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest research.pcea.tests.test_gonol_transition_candidates
```

## Deterministic receipt

```text
receipt_schema = the-interdependency.stack-research.pcea.gonol-transition-candidates
receipt_version = 0.1.0
producer_code_reference = sha256:d11a9aad73364fb29e43a3be306a85fea99876c5f7b90ee1b9083657f6cadf11
receipt_sha256 = 9dfa6fbffeecacde1e94a6949dc0036aa42260ff350aa79fb87a266552a01905
```

## Non-claims

This research note does not establish:

- a recovered UCNS recursive constructor;
- PCEA runtime behavior;
- stack `libs/pcea/` canon;
- cryptographic security;
- entropy or hardness from gonol size or geometry;
- public authenticity receipts;
- proof that the candidate will match a future observed gonol.

## hmmm

- The actual UCNS recursive geometry that should own gonol construction remains
  unresolved.
- The right independent variable may not be consecutive scale index.
- Public authenticity receipts require a separate signature, transparency, or
  verifier layer.
- A future actual gonol construction is required before `164513086777` has
  empirical meaning.
