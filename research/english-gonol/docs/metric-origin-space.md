# EDCM metric-origin construction — usage guidance

Stack consumes the merged EDCM producer
`0873c105799681ea1f7ccb3e619d1f7aebbd85e0`. EDCM owns the metric meanings,
scalar computations, canonical metric identities, and proxy limitations. Stack constructs their
declared ordered English terms. Construction closure does not establish
measurement validity. Bare `O` and `L` remain compatibility carriers only:
`O -> edcm.behavioral.O_scope` and `L -> edcm.behavioral.L_loss`; sibling
`O_confidence`, `L_load`, and `L_resistance` axes remain distinct.

`BASE.json`, the local metric work graph, the Stack manifests, the source fixture,
and CI register this same producer. The loader binds the fixture's complete bytes
to `FIXTURE_SHA256`; `fixture_path` accepts an exact copy, not alternate semantic
definitions or unregistered producer labels. Update the owning EDCM source first
and replay the cross-source check before changing this pin.

## Reproduce the authoritative checks

From `research/english-gonol`, install `pytest` and `PyYAML`. Use clean checkouts:

| Input | Commit | Path passed to the checks |
|---|---|---|
| EDCM | `0873c105799681ea1f7ccb3e619d1f7aebbd85e0` | checkout root |
| OEWN 2025 | `dc343f2683279ecbb13fab4e2fd778d7b162d287` | checkout `src/yaml` |
| UCNS full-construct carrier | `4f863ad37096b7baab8f62820ad5cb937b62a3a7` | checkout root |

Set the three absolute paths for your checkouts and a new output directory:

```bash
export OEWN_SOURCE_ROOT=/path/to/oewn/src/yaml
export EDCM_METRIC_ORIGIN_ROOT=/path/to/edcm
export ENGLISH_GONOL_FULL_CONSTRUCT_ROOT=/path/to/generated/english-full-construct
export REQUIRE_METRIC_ORIGIN_SOURCES=1
python -m english_gonol.full_construct_run \
  --source-root "$OEWN_SOURCE_ROOT" \
  --ucns-source-root /path/to/ucns-carrier \
  --out-dir "$ENGLISH_GONOL_FULL_CONSTRUCT_ROOT"
python -m pytest -q tests/test_edcm_metric_origins.py
```

Preflight enough disk and memory before starting the full construction; CI
requires 8 GiB free disk and 5 GiB RAM. Let an admitted run finish naturally.
The complete workflow also sets the motion and relational UCNS source paths
needed by the rest of the English suite.

The tests verify the actual EDCM checkout, compare all consumed semantic fields,
check exact term admission against the complete pinned corpus, replay the full
construct receipt, construct every metric origin, and bind the emitted records
through the exact merged EDCM adapter. Required missing sources fail instead of
skipping. `metric-origin-replay.json` contains all 11 origin records and a clearly
synthetic transcript measurement used only to test adapter compatibility.

## Export for independent observations

With the environment above, this writes an ordered JSON object ready for
EDCM's `build_semantic_metric_space`:

```bash
python - <<'PY'
import json, os
from pathlib import Path
from english_gonol.edcm_metric_origins import (
    build_metric_origin_set, load_metric_origin_specs,
)
state = Path(os.environ["ENGLISH_GONOL_FULL_CONSTRUCT_ROOT"])
records = {metric: build_metric_origin_set(state, metric).to_dict()
           for metric in load_metric_origin_specs()["specs"]}
(state / "metric-origins.json").write_text(json.dumps(records, indent=2) + "\n")
PY
```

Load that JSON object in the pinned EDCM environment, build the space, and call
`bind_round_metrics` with maintained `RoundMetrics` and the separate observation's
evidence receipt. See EDCM's `docs/semantic-metric-space.md` for the runnable
measurement example and adapter input contract. Keep vector order; do not sort
the exported metric keys.

## hmmm

The O/L naming collision is resolved by canonical separation rather than aliasing.
The observed-construct-to-origin projection remains unestablished. Receipts establish content identity, not cryptographic producer
authentication, empirical validity, or canon selection.
