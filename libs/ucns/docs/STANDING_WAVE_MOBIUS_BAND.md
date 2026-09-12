# UCNS Mobius Band Standing-Wave Continuum

Status: SURVIVED as an explicit UCNS continuum standing-wave construction on
the canonical Mobius band coordinate domain; SURVIVED for finite capacity
requests that fit the derived sampled boundary trace rank; FALSIFIED for
bulk-only capacity counts that exceed that trace rank; UNRESOLVED for PCEA
promotion.

## Domain Claim

Surface form: standing-wave continuous-boundary trace.

Term id: `ucns.mobius_band_standing_wave.boundary_trace`.

Claiming domain: UCNS geometry.

Claimed sense: finite value samples, with optional normal derivative slots, on
the single continuous physical boundary induced by a scalar coordinate-domain
standing-wave operator on the canonical Mobius band.

Scope: `src/ucns/mobius_band_standing_wave.py` and tests that consume that
exact coordinate-domain band model.

Excluded uses: embedded Laplace-Beltrami theorem, physical field theory,
spectral/zeta theorem, PCEA runtime capacity, FFT/discrete spectral tooling,
and arbitrary boundary-measure promotion.

Status: provisional candidate.

## Construction

The canonical Mobius ribbon supplies the coordinate domain:

```text
(t, u) in [0, 2] x [-w, w]
(t + 1, u) ~ (t, -u)
```

The spatial operator is:

```text
L X = -(d2 X / dt2 + d2 X / du2)
```

The standing-wave equation is:

```text
d2 psi / d tau2 = c^2 * (d2 psi / d t2 + d2 psi / d u2)
```

The boundary conditions are:

```text
X(t+1,u) = X(t,-u)
dX/dt(t+1,u) = dX/dt(t,-u)
dX/du(t+1,u) = -dX/du(t,-u)
dX/du(t,+w) = 0
dX/du(t,-w) = 0
```

The admissible basis is separable. The one-turn longitudinal character must
match the transverse parity:

```text
n even: longitudinal cos/sin(n*pi*t) or constant, transverse cos(k*pi*u/w)
n odd:  longitudinal cos/sin(n*pi*t), transverse sin((k+1/2)*pi*u/w)
```

## Boundary Trace

The Mobius strip has one continuous physical boundary. The executable trace
uses `u=+w` over the complete two-turn boundary traversal:

```text
X(2*i/sample_count, w), 0 <= i < sample_count
```

Optional normal-derivative trace slots are present, but the declared Neumann
condition makes them zero for admissible modes. They therefore do not increase
rank.

For longitudinal cutoff `N` and transverse cutoff `K`, the interior basis
dimension is:

```text
(K + 1) * (1 + 2*N)
```

The sampled boundary value trace rank is bounded by the boundary harmonics and
the sample count:

```text
rank <= min(sample_count, 1 + 2*N)
```

Increasing `K` adds transverse bulk modes but does not add independent boundary
trace channels at the same longitudinal cutoff.

## Boundary-Capacity Result

The boundary-capacity principle survives in this finite tested form:

- finite channel requests that fit the derived sampled boundary trace rank are
  `SURVIVED`;
- channel requests that fit the interior basis dimension but exceed the
  boundary trace rank are `FALSIFIED`;
- arbitrary promotion from this sampled trace to PCEA runtime capacity remains
  `UNRESOLVED`.

No capacity channel is assigned by fiat. Discrete FFT/epicycle tooling is not
used as a PDE derivation.

## hmmm

- embedded Laplace-Beltrami operator on the realized three-dimensional ribbon;
- exact continuum boundary-measure capacity theorem rather than finite sampled
  rank;
- derived encoding from continuum trace functions into PCEA runtime channels.
