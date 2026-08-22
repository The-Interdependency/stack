# Test Spec: Theorem 01 — Boundary Earns Its Keep

## Claim

Changing only the boundary-simplex state changes vector direction, delay, filtering, propagation, or transformation outcome while source and target energy-states remain constant.

## Fixed inputs

- source energy-state: fixed
- target energy-state: fixed
- source/target relation class: fixed
- tensor membership: fixed

## Variable input

- boundary-simplex state

## Procedure

1. Build a tensor containing source simplex, target simplex, and boundary-simplex.
2. Set source and target energy-states.
3. Set boundary-simplex state A.
4. Compute or describe gradient dynamics.
5. Record vector outcome.
6. Change only boundary-simplex state to B.
7. Recompute or redescribe gradient dynamics.
8. Record vector outcome.
9. Compare outcomes.

## Passing outcomes

The test passes when boundary state B changes at least one of:

- vector direction;
- vector magnitude;
- propagation path;
- propagation success/failure;
- delay;
- filtering;
- amplification;
- dampening;
- inversion;
- phase-shift;
- translation;
- transformation result.

## Failing outcomes

The test fails when boundary-simplex state is changed and no vector behavior changes under conditions where the model claims the boundary is ontologically active.

## Hmmm cases

Mark `hmmm` when outcome changes but it is unclear whether the change came from boundary-simplex state or an untracked source/target relation change.

## Minimal assertion

```text
same source + same target + changed boundary-simplex state => changed vector outcome
```

This proves boundary is not decorative.
