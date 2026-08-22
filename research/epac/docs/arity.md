# Dimensional arity

Status: **CROSS-DOMAIN-HYPOTHESIS / provisional**. Not org canon.

Dimension tells where. Arity tells what intersects at once.

```text
ambient_dimensions: declared independent axes
couplings: only explicitly declared intersections
Coupling.arity = number of dimensions in that one coupling
```

Ambient size and arity are independent. Three ambient dimensions do not create
a ternary coupling. `{z,x}` and `{z,y}` remain two arity-2 declarations that
share `z`. They do not declare `{x,y}` or `{x,y,z}`.

Geometry is generated from declared couplings, not from the power set of
available axes. The same ambient space may hold mixed arities. There is no
x/y/z special case; ids may be `d1…dk`.

`hmmm`: whether `{x,z}` and `{z,x}` are the same coupling or oriented
declarations is undeclared. The implementation stores declaration sequence
only.

See `epac_dimensional_arity.py`.
