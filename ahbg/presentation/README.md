# AHBG presentation

Grok-owned graphics surface. It renders validated presentation snapshots and
already-resolved motion traces. It does **not** define game mechanics.

## Boundary

- Included: Seed-of-Life circle rendering, tile centerpoints, unit markers,
  selection/inspection, feed text, and visual traces of already-resolved moves.
- Excluded: legal movement, adjacency authority, turns, War resolution,
  construction, permissions, RNG, DM state, or agent policy.
- Snapshot standing is `ahbg.presentation.snapshot` / `not-mechanics`.
- `project.py` accepts already-sanitized observation data and resolved move
  events. It never decides whether those moves were legal.
- `geometry.py` maps supplied coordinates into display positions only; visual
  one-radius relations are not exported as game-law adjacency.

## Usage guidance

Validate the sample and projector:

```bash
python -m unittest discover -s ahbg/presentation/tests -p 'test*.py'
node --check ahbg/presentation/board.js
```

Serve the board locally:

```bash
cd ahbg/presentation
python -m http.server 8765 --bind 127.0.0.1
# open http://127.0.0.1:8765/board.html
```

Project a sanitized observation:

```python
from ahbg.presentation.project import snapshot_from_observation

observation = {
    "turn": 1,
    "tiles": [
        {"tile_id": "c", "q": 0, "r": 0},
        {"tile_id": "ne", "q": 1, "r": -1},
    ],
    "units": [{"unit_id": "A0", "tile_id": "ne", "label": "A0"}],
}
move = {
    "kind": "move",
    "data": {"unit_id": "A0", "from_tile_id": "c", "to_tile_id": "ne"},
}
snapshot = snapshot_from_observation(
    observation,
    plane_id="plane-0",
    move_events=[move],
)
```

The validator fails closed on malformed/duplicate tile IDs or coordinates,
invalid unit references/labels, duplicate unit IDs, and motion destinations that
do not match the unit's presented final tile.

The browser exposes tile inspection to pointer and keyboard input, separates
multiple unit markers sharing one tile, and renders the selection ring above the
unit layer so selection remains visible on occupied tiles.

## hmmm

- whether later Flower-of-Life rings belong on this presentation surface;
- the exact live engine-to-observation adapter is owned by the eventual engine
  integration, not by this graphics package;
- construction animation remains unavailable until an owning mechanics layer
  emits an already-resolved construction event contract.
