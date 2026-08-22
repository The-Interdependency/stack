# Dimensional arity

Status: **CROSS-DOMAIN-HYPOTHESIS / provisional**. Not org canon.

Dimension tells where. Arity tells what intersects at once. Degree tells how a
dimension is incident on declared couplings.

```text
(z, x) ≠ (x, z)
(x, z) and (y, z) ↛ (x, y, z)   without an explicit proof

every instance of x has its own (z, x_i)
every instance of y has its own (z, y_j)
```

A second occurrence is a second instance. `(z, x_0)` does not cover `x_1`.
`(x_i, z)` does not satisfy `(z, x_i)`.

Degree is required. For ambient `{x,y,z}` with couplings `(z,x)` and `(z,y)`:

```text
deg(z) = 2 at slot 0
deg(x) = 1 at slot 1
deg(y) = 1 at slot 1
```

That incidence structure is the geometry of two binary couplings sharing `z`.
It is not a ternary coupling and not `(x,y)`.

Charge state rides on each coupling from the math already present: per-slot
dimension charges (nuclear `Z` when the axis is an atom) and Möbius `ε` at
`t=0`. `(z,x)` with charges `(q_z, q_x, ε)` is not `(x,z)` with
`(q_x, q_z, ε)`. The three-dimensional structure **is** that combination —
oriented couplings, each arity's charge state, and degree. Two charged
arity-2 couplings on a degree-2 hub already occupy three participating axes.
It still does not declare `(x,y,z)`.

Construction is `epac.public_gonol` on the UCNS Public Gonol carrier, not
`edcm.gonol`.

Overlap of members is not a proof. Forbidden inference rules include
`overlap-closure`, `permutation-identity`, and `ambient-power-set`.

See `epac_dimensional_arity.py`. After construction, `epac_comparison.py` reads
that 3-structure against sealed known chemistry. Sealed shape names stay out
of construction.
