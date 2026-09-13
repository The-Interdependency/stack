# Continuum wave equation → gonal boundary trace → modular action

Standing: **candidate UCNS representation** with an exact geometric derivation on the visible circle boundary. The equations and trace identities below are exact within the declared model; that does not by itself ratify this representation as selected UCNS geometry. This is not a physical-selection claim and does not yet lift the trace into the complete native Möbius state.

## 1. Continuum circle wave equation

Let a circle of radius `R` carry angular coordinate `θ ∈ R / 2πZ`. For scalar propagation speed `c`, the one-dimensional continuum wave equation on the circle is

```text
∂²u/∂t² = (c²/R²) ∂²u/∂θ².
```

Set `κ = c/R`. Separation `u(θ,t)=Θ(θ)T(t)` gives

```text
Θ'' + n² Θ = 0,
T'' + (κ n)² T = 0,
```

with integer `n` forced by periodicity `Θ(θ+2π)=Θ(θ)`. A complex traveling basis mode is

```text
u_n(θ,t) = A exp(i(nθ - |n|κt)).
```

Real sine/cosine modes are the real and imaginary combinations of the same basis. UCNS needs only the exact spatial phase relation below; it does not store floating-point complex amplitudes.

## 2. Positive-degree continuum covering

For any positive integer continuum covering degree `d`, define

```text
D_d(θ,t) = (dθ, dt).
```

If `u` solves the circle wave equation, then `v(θ,t)=u(dθ,dt)` also solves it because

```text
v_tt = d² u_tt,
v_θθ = d² u_θθ,
therefore v_tt = κ² v_θθ.
```

For a basis mode,

```text
u_n(D_d(θ,t)) = u_n(dθ,dt) = u_(dn)(θ,t).
```

Thus the continuum equation admits a degree-`d` solution endomorphism that multiplies spatial harmonic number by `d` while scaling time by the same factor.

Important boundary: for `d>1`, `θ ↦ dθ` is a degree-`d` covering of the circle, not a globally invertible circle isometry. The continuum equation therefore does **not** make `d` a symmetry-group generator or select one preferred `d`.

## 3. Exact candidate UCNS/gonal boundary trace

For an `m`-gonal visible boundary, place canonical residue `r ∈ Z/mZ` at the exact normalized turn

```text
τ_m(r) = r/m,
θ_r = 2πr/m.
```

Define the boundary trace of harmonic `n` by sampling the continuum phase at those positions:

```text
Γ_(m,n)(r) = n r / m   (mod 1).
```

The executable candidate record stores the canonical exact phase turn

```text
phase_(m,n)(r) = (n*r mod m)/m
```

as a rational `Fraction`. No trigonometric approximation is needed.

This is the explicit mapping:

```text
continuum boundary point θ_r = 2πr/m
        ↓ sample
UCNS candidate gonal position r at exact turn r/m
        ↓ harmonic n
exact phase turn (n*r mod m)/m.
```

The map is to the generic `m`-gonal boundary carrier. It does not automatically identify an arbitrary `m` with the 157-position Public Gonol arrangement; that identification requires its own geometric authority.

## 4. Modular multiplication is the finite trace of the continuum covering

Apply `D_d` to a gonal sample position:

```text
θ_r ↦ d θ_r = 2π (d r)/m.
```

Modulo one visible turn, this lands at

```text
r ↦ d r (mod m).
```

Let the finite modular multiplier be

```text
a = d mod m.
```

Then the induced finite action is exactly

```text
T_(a,m)(r) = a*r mod m = d*r mod m.
```

For the phase trace,

```text
Γ_(m,n)(d r)
  = n d r / m           (mod 1)
  = Γ_(m,dn)(r).
```

So the following square commutes exactly at the spatial boundary-trace level:

```text
continuum harmonic n  --D_d-->  continuum harmonic dn
       | Γ_m                         | Γ_m
       v                             v
gonal trace n         --T_a*-->  gonal trace dn
```

where `a = d mod m` and `T_a*` is pullback along `r ↦ a r mod m`.

### The finite trace forgets the continuum degree

The residue action sees only `d mod m`. Therefore

```text
d,
d + m,
d + 2m,
...
```

all induce the same finite modular action while producing different continuum harmonic multiplication and time scaling.

This means a `ModularOrbitGeometry(multiplier=a)` does **not** uniquely determine a continuum covering degree. The covering lift must be explicit:

```python
from ucns import (
    build_circle_wave_mode_trace,
    build_modular_orbit_geometry,
    pullback_circle_wave_trace,
)

geometry = build_modular_orbit_geometry(9, 2, range(1, 9))
source = build_circle_wave_mode_trace(9, 1, range(1, 9))

covering_2 = pullback_circle_wave_trace(source, geometry, 2)
covering_11 = pullback_circle_wave_trace(source, geometry, 11)

assert covering_2.action == covering_11.action == geometry.action
assert covering_2.target.harmonic == 2
assert covering_11.target.harmonic == 11
assert covering_2.time_scale == 2
assert covering_11.time_scale == 11
```

The modular-orbit candidate requires the declared finite carrier to be closed and bijective under `T_(a,m)` before calling its components disjoint cycles. That is a **finite trace boundary**, not a claim that the degree-`d` continuum covering is globally invertible.

## 5. What this derives, and what it does not

Derived exactly within the candidate model:

- the continuum circle wave equation and its integer harmonic basis;
- positive-degree spacetime coverings `(θ,t) ↦ (dθ,dt)` preserving the equation;
- exact `m`-gonal sampling at `r/m` visible turns;
- exact phase trace `(n*r mod m)/m`;
- the induced finite action `r ↦ d*r mod m`;
- the reduction `a = d mod m` linking continuum covering to modular multiplier;
- exact equivariance between modular reindexing and harmonic multiplication;
- the many-to-one nature of continuum degree → finite multiplier;
- the condition under which the finite action is a disjoint-cycle permutation.

Not derived:

- ratification of this candidate representation as selected UCNS geometry;
- which continuum lift `d ≡ a (mod m)` should be privileged;
- why a physical system should select one modulus `m`, one carrier subset, or one covering degree `d`;
- that modular cycles themselves are energy states, particles, primes, Fibonacci structure, or EPAC semantics;
- that the visible 360° trace already contains the complete 720° native Möbius state;
- that the generic `m`-gonal carrier is identical to the Public Gonol without a separate geometric identification.

Those nonclaims matter. The continuum derivation establishes the **candidate representation bridge** that was missing; it does not smuggle downstream meaning into UCNS or bypass the repository's selection protocol.

## hmmm

The candidate still requires its own ratification path. The next geometric load-bearing step is the exact lift of this visible-circle trace into the native Möbius carrier: what state must accompany `r/m` so that one visible turn reverses local frame and two visible turns restore complete local state? A second unresolved is any law that would select one continuum covering lift `d` from the congruence class `d ≡ a (mod m)`. Until those are constructed, the continuum/gonal trace is exact within its visible-boundary candidate model but not selected as complete UCNS geometry.
