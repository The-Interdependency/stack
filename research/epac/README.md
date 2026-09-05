# EPAC forge workspace

EPAC now exists independently at `The-Interdependency/epac`.

This directory is the **stack forge candidate** from which the independent repository was extracted. It remains noncanonical stack-local research until the graduation sequence is complete. Do not treat continued work here as authority over the independent repository, and do not populate `libs/epac/` merely because extraction occurred.

`EPAC` is the stable project handle; historical expansions are provenance, not a fixed canonical expansion.

## Transition standing

- independent extracted repository: `The-Interdependency/epac@d8868858b2e455381ce670797bdbe47189bdc496`
- extraction source: `The-Interdependency/stack@ef51f2e8f32ccfd5394525dad72475a61a505bc1:research/epac/`
- implementation/public-contract authority transfer: incomplete
- independent tests: passed in EPAC
- clean build/install: unresolved/failed as a graduation gate
- license/distribution rights: unresolved
- immutable release: `hmmm`
- downstream stack reconsumption: `hmmm`
- molecular-shape prediction: **FALSIFIED** and preserved

## Current content

- [`subatomic/subatomic-affixiation-baseline.md`](subatomic/subatomic-affixiation-baseline.md) — historical/provisional subatomic research record.
- [`epac_public_gonol.py`](epac_public_gonol.py) — EPAC Public Gonol constructor on the UCNS carrier; not the EDCM text-domain constructor.
- [`docs/arity.md`](docs/arity.md) — provisional dimensional-arity construction.
- [`docs/preregistration-molecular-geometry-from-element-gonols.md`](docs/preregistration-molecular-geometry-from-element-gonols.md) — frozen preregistration and falsification boundary.

## Usage

From this directory:

```bash
PYTHONPATH=".:../../libs/ucns/src" python3 -m unittest discover -s tests -q
```

Do not open `data/sealed_known_molecular_geometry.json` during construction. After construction:

```bash
PYTHONPATH=".:../../libs/ucns/src" python3 - <<'PY'
from epac_comparison import compare_after_construction
print(compare_after_construction()["standings"])
PY
```

## hmmm

This forge workspace remains live only as the pre-graduation research side of the transition. The exact handoff point is the eventual verified release + downstream reconsumption + authority-transition receipt, not repository creation alone.
