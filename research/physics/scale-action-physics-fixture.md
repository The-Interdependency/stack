# Physics scale-action fixture

Standing: **conditional external-domain fixture; not UCNS canon; not physics validation**.

This file records a domain-consumer use of the UCNS multiplicative scale-action candidate from UCNS PR #232. UCNS owns only the exact domain-agnostic action. Stack owns this conditional physics interpretation and its unresolved evidence boundary.

## Source and authority

- UCNS candidate action: `T_q(x)_i = q^w_i x_i`
- UCNS PR at time of extraction: `https://github.com/The-Interdependency/ucns/pull/232`
- Former UCNS misplaced fixture path: `docs/scale-transform-physics-fixture.md`
- Status of this Stack record: external physics fixture, candidate only
- Non-transfer boundary: no physics premise, trapped-field claim, varying-constants claim, or cosmological claim transfers into UCNS.

## Confinement relation

A cavity-like confined mode with characteristic size `L` may be written

```text
omega ~ kappa*c/L
E ~ hbar*omega
E = m*c^2
```

which gives

```text
L ~ kappa*hbar/(m*c).
```

The quantity `hbar/(m*c)` is the reduced Compton wavelength. Its appearance here is an algebraic consequence of the assumed light-speed mode, one-quantum energy relation, and mass-energy equivalence. It is therefore a useful target for a confinement theory, not independent evidence that matter is confined electromagnetic radiation.

The stronger test is whether a theory derives the dimensionless geometric factor `kappa`, confinement, stability, and particle observables without fitting the particle mass or inserting another dimensional scale.

## Six-axis conditional action

For the external-domain ordering

```text
(epsilon, mu, c, hbar, m, L)
```

the hypothesis

```text
epsilon -> q*epsilon
mu      -> q*mu
c       -> c/q
hbar    -> q*hbar
m       -> q^2*m
L       -> L
```

maps to the UCNS weight vector

```text
w = (1, 1, -1, 1, 2, 0).
```

UCNS stores only the ordered integer vector and exact scale factor. The names and physical interpretation remain in this Stack fixture.

For a monomial with exponent vector `a`, invariance is the exact kernel test

```text
a dot w = 0.
```

Under the stated weights, the following external expressions lie in that kernel:

| external expression | exponent vector in the ordering above |
|---|---|
| `mu/epsilon` | `(-1, 1, 0, 0, 0, 0)` |
| `hbar*c` | `(0, 0, 1, 1, 0, 0)` |
| `m*c^2` | `(0, 0, 2, 0, 1, 0)` |
| `hbar/(m*c)` | `(0, 0, -1, 1, -1, 0)` |
| `L*m*c/hbar` | `(0, 0, 1, -1, 1, 1)` |

The last row is the dimensionless confinement factor

```text
kappa = L*m*c/hbar.
```

Thus the conditional hypothesis preserves both the reduced Compton scale and the ratio `L / (hbar/(m*c))`.

By contrast, `epsilon*mu` has exponent vector `(1, 1, 0, 0, 0, 0)` and scale weight `2`; it is not invariant.

## UCNS usage

```python
from fractions import Fraction
from ucns import build_scale_action

action = build_scale_action(
    weights=(1, 1, -1, 1, 2, 0),
    factor=Fraction(3, 2),
)

assert action.is_invariant((-1, 1, 0, 0, 0, 0))
assert action.is_invariant((0, 0, 1, 1, 0, 0))
assert action.is_invariant((0, 0, -1, 1, -1, 0))
assert action.is_invariant((0, 0, 1, -1, 1, 1))
assert not action.is_invariant((1, 1, 0, 0, 0, 0))
```

Composition and inversion are exact:

```text
T_p o T_q = T_(p*q)
T_1 = identity
T_q^-1 = T_(1/q)
```

These are properties of the UCNS mathematical action. They do not validate a varying-constants cosmology, a trapped-field model of matter, or any claim that the six external quantities actually transform with these weights.

## Falsification use

This fixture becomes scientifically useful only when an external physics consumer supplies independent evidence for the bindings and predictions.

A strong confinement test would require the geometry to derive an admissible `kappa` before using the observed particle mass. If `kappa` is chosen after the mass is known, the construction has only repackaged the Compton relation.

## hmmm

No result here supplies charge, spin, statistics, magnetic moment, spectroscopy, scattering, self-confinement, or stability. This fixture tests an exact transformation structure conditional on external physical premises; it does not promote those premises into UCNS or into established physics.
