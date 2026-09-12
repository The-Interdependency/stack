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
- [`docs/boundary_capacity_principle.md`](docs/boundary_capacity_principle.md) — internal boundary-capacity result for the current molecule construction.
- [`docs/cross_scale_compositional_closure.md`](docs/cross_scale_compositional_closure.md) — bounded closure audit for the implemented subatomic -> element -> molecule stack across the locked nine formulas: H2, H2O, NH3, CH4, CO2, H2S, BF3, PH3, and SiH4.
- [`docs/boundary_descriptor_nondegeneracy.md`](docs/boundary_descriptor_nondegeneracy.md) — bounded first-order control audit showing the current boundary descriptor is label/order invariant, path invariant over implemented equivalent paths, and sensitive to declared boundary dimension and coupling-count changes without claiming complete incidence-topology sufficiency.
- [`docs/boundary_capacity_quotient.md`](docs/boundary_capacity_quotient.md) — quotient audit showing equality of `B=(3,d_boundary,c_boundary)` matches equality of the presently observable boundary-capacity probe behavior while preserving the falsification of `B` as a complete state descriptor.
- [`docs/boundary_probe_completeness.md`](docs/boundary_probe_completeness.md) — probe-inventory audit showing the quotient probe set is incomplete for the full presently declared EPAC boundary-relevant operation surface because existing coupling-structure observers refine the 16-class B quotient.
- [`docs/boundary_minimal_refinement.md`](docs/boundary_minimal_refinement.md) — minimal-refinement audit showing that one existing structural observable is enough to reproduce the 21-class partition, but the singleton minimum is not unique and no canonical compositional descriptor component is promoted.

## Usage

From this directory:

```bash
PYTHONPATH=".:subatomic:../../libs/ucns/src" python3 -m unittest discover -s tests -q
```

Do not open `data/sealed_known_molecular_geometry.json` during construction. After construction:

```bash
PYTHONPATH=".:subatomic:../../libs/ucns/src" python3 - <<'PY'
from epac_comparison import compare_after_construction
print(compare_after_construction()["standings"])
PY
```

Cross-scale closure report:

```bash
PYTHONPATH=".:subatomic:../../libs/ucns/src" python3 - <<'PY'
from epac_cross_scale_closure import cross_scale_compositional_closure
print(cross_scale_compositional_closure()["statuses"])
PY
```

Boundary-descriptor non-degeneracy report:

```bash
PYTHONPATH=".:subatomic:../../libs/ucns/src" python3 - <<'PY'
from epac_boundary_nondegeneracy import boundary_descriptor_nondegeneracy_report
print(boundary_descriptor_nondegeneracy_report()["statuses"])
PY
```

Boundary-capacity quotient report:

```bash
PYTHONPATH=".:subatomic:../../libs/ucns/src" python3 - <<'PY'
from epac_boundary_quotient import boundary_capacity_quotient_report
print(boundary_capacity_quotient_report()["statuses"])
PY
```

Boundary-probe completeness report:

```bash
PYTHONPATH=".:subatomic:../../libs/ucns/src" python3 - <<'PY'
from epac_boundary_probe_completeness import boundary_probe_completeness_report
print(boundary_probe_completeness_report()["statuses"])
PY
```

Boundary minimal-refinement report:

```bash
PYTHONPATH=".:subatomic:../../libs/ucns/src" python3 - <<'PY'
from epac_boundary_minimal_refinement import boundary_minimal_refinement_report
print(boundary_minimal_refinement_report()["statuses"])
PY
```

## hmmm

This forge workspace remains live only as the pre-graduation research side of the transition. The exact handoff point is the eventual verified release + downstream reconsumption + authority-transition receipt, not repository creation alone.
