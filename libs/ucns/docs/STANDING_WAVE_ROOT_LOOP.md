# UCNS Mobius Standing-Wave Root Loop

Status: SURVIVED as the smallest explicit UCNS continuum standing-wave
construction; FALSIFIED as a direct source of PCEA-style boundary-measure
capacity channels.

## Domain Claim

Surface form: standing-wave boundary trace.

Term id: `ucns.mobius_standing_wave.boundary_trace`.

Claiming domain: UCNS geometry.

Claimed sense: endpoint value/derivative trace induced by the scalar
second-order standing-wave operator on the native two-turn Mobius root loop.

Scope: `src/ucns/mobius_standing_wave.py` and tests that consume that exact
root-loop model.

Excluded uses: physical field theory, spectral/zeta theorem, PCEA runtime
capacity, FFT/discrete spectral tooling, and Möbius band or higher-dimensional
domains.

Status: provisional candidate.

## Construction

The native UCNS Mobius root loop supplies the continuum coordinate:

```text
t in [0, 2]
```

The spatial operator is:

```text
L X = -d2 X / dt2
```

The standing-wave equation is:

```text
d2 psi / d tau2 = c^2 d2 psi / d t2
```

The complete-return boundary conditions are:

```text
X(0) = X(2)
X'(0) = X'(2)
```

The admissible spatial basis is:

```text
1
cos(n*pi*t), n >= 1
sin(n*pi*t), n >= 1
```

Each positive mode changes sign under one visible turn when `n` is odd and
returns after two visible turns.

## Boundary Trace

For each basis function, the trace is derived from endpoints:

```text
(X(0), X(2), X'(0), X'(2))
```

The trace image has rank `1` for only the constant mode and rank `2` once any
positive sine/cosine mode is admitted. Increasing the interior mode cutoff adds
more interior basis functions, but it does not add independent trace channels in
this one-dimensional root-loop model.

## PCEA Capacity Induction

This model does not induce the capacity channels required by PCEA's
boundary-capacity hypothesis. The derived trace rank is at most `2`, while
PCEA-style boundary capacity asks for a boundary-measure-indexed family of
independent coupling channels.

No channels are assigned by fiat. Discrete FFT/epicycle tooling is not used as a
PDE derivation.

The next larger construction is `src/ucns/mobius_band_standing_wave.py`, which
adds the canonical Mobius band coordinate domain and its continuous physical
boundary. That construction does not retroactively change this root-loop
falsifier.

## hmmm

- embedded Laplace-Beltrami operator on the realized ribbon;
- exact continuum boundary-measure capacity theorem;
- derived map from continuum trace functions into PCEA capacity channels.
