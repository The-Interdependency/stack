# EPAC historical forge evidence

The active implementation is owned by [The-Interdependency/epac](https://github.com/The-Interdependency/epac).
Stack has reconsumed its immutable MPL-2.0 `v0.1.0` release and retired the 37
forge Python implementation/test files. Final transition evidence is recorded
under [`integration/epac/`](../../integration/epac/).

This directory preserves historical documents, data, SVGs and receipts from
Stack `0e8384bbb60e4c2189016a212bdd0030d04aed7d`. [`BASE.json`](BASE.json)
binds that origin; it does not claim the historical findings describe today's
EPAC implementation. [`README.forge-history.md`](README.forge-history.md) preserves
the former instructions as history. Its local import commands are retired.

## Usage guidance

Run the supported release consumer from the Stack root:

```bash
python3 integration/epac/reconsume.py \
  integration/epac/release-lock.json /tmp/epac-public-consumption python3.12
```

Use a new output directory outside Stack. Make EPAC implementation changes in
the independent repository. Consult the pinned public release's own documents
and tests for current behavior; retained research here is historical evidence.

## hmmm

The release preserves all 14 FALSIFIED comparison standings. Geometry ratification,
canonical compositional descriptors, and unmeasured operation effects remain
unresolved. Packaging and implementation ownership confer no scientific standing.
