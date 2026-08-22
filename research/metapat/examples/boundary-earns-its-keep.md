# Example: Boundary Earns Its Keep

## Purpose

This example tests the First Theorem.

A boundary is not decorative if changing only the boundary-simplex state changes vector direction, delay, filtering, propagation, or transformation outcome.

## Controlled setup

Hold source energy-state constant.

Hold target energy-state constant.

Change only boundary-simplex state.

Observe whether vector behavior changes.

## Expected result

If vector behavior changes, boundary-simplex state participates in gradient dynamics.

If vector behavior does not change under any boundary state, the boundary is not doing ontological work in that model.

## Energy Theory form

```text
source scalar state: fixed
target scalar state: fixed
boundary-simplex state: varied
relation: same source/target relation except boundary state
gradient dynamics: recomputed
vector outcome: compared
```

## Pass condition

Changing only the boundary-simplex state changes at least one of:

- vector direction;
- propagation outcome;
- delay;
- filtering;
- amplification;
- dampening;
- inversion;
- phase-shift;
- translation;
- blockage.

## Theorem supported

If boundary is simplex, then boundary can modify transformation.

Therefore, gradient dynamics must include boundary-simplex state.
