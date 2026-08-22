# Dimensional arity

Status: **CROSS-DOMAIN-HYPOTHESIS / provisional**. Not org canon.

Dimension tells where. Arity tells what intersects at once. Degree tells how a
dimension is incident on declared couplings.

```text
(z, x) ≠ (x, z)
(x, z) and (y, z) ↛ (x, y, z)   without an explicit proof
```

Degree is required. For ambient `{x,y,z}` with couplings `(z,x)` and `(z,y)`:

```text
deg(z) = 2 at slot 0
deg(x) = 1 at slot 1
deg(y) = 1 at slot 1
```

That incidence structure is the geometry of two binary couplings sharing `z`.
It is not a ternary coupling and not `(x,y)`.

Overlap of members is not a proof. Forbidden inference rules include
`overlap-closure`, `permutation-identity`, and `ambient-power-set`.

See `epac_dimensional_arity.py`.
