# EPAC carrier research

This workspace owns Stack's bounded carrier construction and falsification
experiments. [BASE.json](BASE.json) records their Stack origin and the exact
independent EPAC source consumed by the derivation experiment.

| Surface | Responsibility |
|---|---|
| [Independent EPAC](https://github.com/The-Interdependency/epac) | EPAC implementation and public contracts |
| [Release integration](../../integration/epac/) | Hash-pinned public `v0.1.0` consumption |
| [Historical forge](../epac/) | Preserved documents, data and receipts; no Python implementation |
| This workspace | Stack-local carrier experiments and tests; no EPAC release authority |

The three experimental modules are:

- `epac_lattice_carrier.py`: frozen constitutive carrier and comparison embedding.
- `epac_carrier_falsification.py`: collision, minimality and derivation audits.
- `epac_derivation_consumer.py`: consumption and replay of verified upstream
  atomic derivations at `7b3d99af9a456d2587e0489d7400e6f8b58c8a82`.

The last module verifies the pinned commit's ancestry and SHA-256 of the three
consumed source modules before loading them. The commands and CI below use the
exact commit. This research source pin is separate from the released artifact
consumed under `integration/epac/`; changing one does not update the other.

## Historical inputs and relocation

The six Python implementation/test files were relocated from `research/epac/`.
[relocation-provenance.json](relocation-provenance.json) records the original
paths, Git blobs, file hashes and baseline report hashes. Historical fixtures
remain in place under their graduation inventory and are read relative to the
module location. The `data/` and `subatomic/` source labels inside existing
reports are relative to **`research/epac/`**, their historical origin.

The move preserves the complete constitutive, Minkowski comparison,
falsification and derived-carrier report bytes under their declared canonical
JSON encoding. It does not promote their scientific standing. The rejected
Minkowski candidate remains only as a comparison in the falsification audit.

## Usage guidance

From the Stack root, install the test dependency in your Python environment and
prepare a separate EPAC checkout at the declared source identity:

```bash
python -m pip install pytest==8.4.2
export EPAC_SOURCE_ROOT="$(mktemp -d)/epac"
git clone https://github.com/The-Interdependency/epac.git "$EPAC_SOURCE_ROOT"
git -C "$EPAC_SOURCE_ROOT" checkout --detach 7b3d99af9a456d2587e0489d7400e6f8b58c8a82
cd research/epac-carrier
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests
```

`EPAC_SOURCE_ROOT` must be explicit; the source-consumer tests fail when it is
absent or the source identity does not verify. They do not silently skip.
From this workspace, a report can be built without changing import paths:

```python
import os
from pathlib import Path
from epac_derivation_consumer import build_derived_carrier

report = build_derived_carrier(Path(os.environ["EPAC_SOURCE_ROOT"]))
```

From the Stack root, run `python tools/check_stack_consistency.py` to verify the
manifest projections, historical retirement and preserved evidence. The EPAC
workflow runs the research suite and public-release consumption as separate jobs.

## hmmm

- The source-derived carrier remains bounded; general chemical coverage is unproved.
- Coordination capacity remains `UNRESOLVED`; the rejected capacity rule remains
  `FALSIFIED` and the generative gate remains `RETAIN-BOUNDED`.
- Geometry ratification, empirical validity and operation effects do not follow
  from relocation, report replay or test success.
