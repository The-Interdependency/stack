# epac — placeholder scaffold

Reserved for **energy particle affixiation coupling**.

Status: `hmmm` — no source repository exists yet. This directory carries no doctrine
until a canonical `The-Interdependency/epac` source is created and pinned in
`STACK_MANIFEST.md`.

## Current content

- [`subatomic/subatomic-affixiation-baseline.md`](subatomic/subatomic-affixiation-baseline.md) —
  provisional research candidate: hydrogen → helium baseline and the lithium/carbon
  construction form over current METAPAT affixiation semantics and UCNS carrier identity.
  Status: CROSS-DOMAIN-HYPOTHESIS / proposed. Not org canon.
- [`epac_public_gonol.py`](epac_public_gonol.py) — EPAC Public Gonol constructor
  on the UCNS carrier. Not the EDCM text-domain constructor.
- [`docs/arity.md`](docs/arity.md) — arity is declared dimensional coupling,
  not ambient dimension count. Charged oriented couplings plus degree are the
  three-dimensional structure.
- [`docs/constraints.md`](docs/constraints.md) — standing constraints and
  resolved contradictions for this candidate.
- [`docs/preregistration-molecular-geometry-from-element-gonols.md`](docs/preregistration-molecular-geometry-from-element-gonols.md) —
  provisional candidate: carbon is the primary research atom. Z=1–18 element
  gonols from nucleons, nucleus–electron couplings, occupancy-2 pairing, and
  leftover unpaired `(nucleus, e_i)` bonding surfaces, then affixiation of
  one-carbon inorganic molecules (`CO`, `CO2`, `CS2`, `COS`, `CF4`, `CCl4`,
  `COF2`, `COCl2`, `HCN`) plus `CH4` and non-carbon regression formulas by
  matching those surfaces. Known chemistry is sealed until after construction.

## Usage

From this directory:

```bash
PYTHONPATH=".:../ucns/src" python3 -m unittest discover -s tests -q
```

Do not open `data/sealed_known_molecular_geometry.json` during construction.
After construction:

```bash
PYTHONPATH=".:../ucns/src" python3 - <<'PY'
from epac_comparison import compare_after_construction
print(compare_after_construction()["standings"])
PY
```
