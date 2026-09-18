# EPAC-derived carrier audit

This is active, stack-local carrier research. It consumes exact EPAC source
bytes and tests whether EPAC-derived coordinates preserve Stack's frozen
carrier controls. It is not an EPAC implementation, release consumer, or
authority transfer.

`research/epac/` remains sealed historical forge evidence after EPAC
graduation. EPAC implementation and public-contract authority remain in
`The-Interdependency/epac`; the immutable accepted release remains consumed
through `integration/epac/`.

## Run

Use an EPAC checkout that contains the exact commit pinned by
`epac_derivation_consumer.py`:

```bash
EPAC_SOURCE_ROOT=/path/to/epac \
PYTHONPATH=research/epac-derived-carrier \
python3 -m pytest -q research/epac-derived-carrier/tests
```

The consumer verifies the exact EPAC commit and SHA-256 digests of all three
source modules before importing them. Receipts replay byte-identically and
tampering fails closed.

## Standing

- Constitutive gate: `PROMOTE` — period and valence derive from EPAC electron
  construction and the frozen carrier controls survive.
- Generative gate: `RETAIN-BOUNDED` — bond-context orbital participation,
  ligand-field regime, coordination capacity, and topology formation remain
  unresolved.
- Explicit ligand-field controls accept high/low spin as input and use no
  spectrochemical lookup.

## hmmm

EPAC can construct a candidate 4s/3d/4p basis and evaluate supplied field
controls. It does not yet derive which orbitals participate in a bond context,
which ligand-field regime applies, how many ligands coordinate, or which
topology forms.
