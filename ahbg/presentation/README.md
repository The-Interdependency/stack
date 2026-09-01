# AHBG presentation

Grok-owned graphics surface. It renders validated presentation snapshots and
already-resolved motion traces. It does **not** define game mechanics or derive
UCNS geometry.

## Boundary

- Included: Seed-of-Life circle rendering, UCNS-supplied tile centerpoints,
  unit markers, selection/inspection, public feed text, and visual traces of
  already-resolved moves.
- Excluded: legal movement, adjacency authority, turns, War resolution,
  construction, permissions, RNG, DM state, private prompt state, or agent policy.
- Snapshot standing is `ahbg.presentation.snapshot` / `not-mechanics`.
- Every snapshot carries an exact `geometry_source` identity plus each tile's
  UCNS-derived `x`, `y`, and `source_slot`. The renderer only scales those
  coordinates for SVG display; it never rebuilds centers from local axial rules.
- The current sample pins `The-Interdependency/ucns@1975fe70cf4e0826a8020c2da3047569e277af64`,
  the canonical `libs/ucns/` identity in the stack manifest when this surface was
  authored. Its `mobius_seed` module remains an explicit nonselecting UCNS
  candidate; presentation consumption does not promote its standing.
- `project.py` accepts already-sanitized observation data, source-backed display
  coordinates, and resolved move events. It never decides whether those moves
  were legal and copies only declared browser-facing fields.
- `geometry.py` scales supplied source coordinates into display pixels only.

## Usage guidance

Validate the package:

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

Project a sanitized observation only after the owning adapter has attached the
UCNS-derived centers and exact source identity:

```python
from ahbg.presentation.project import snapshot_from_observation

geometry_source = {
    "repository": "The-Interdependency/ucns",
    "commit": "1975fe70cf4e0826a8020c2da3047569e277af64",
    "module": "src/ucns/mobius_seed.py",
    "schema_id": "ucns.mobius-seed-of-life",
    "schema_version": "0.1.0",
    "projection_id": "seed-of-life-seven-equal-circles",
    "selection_effect": "none",
}
observation = {
    "turn": 1,
    "geometry_source": geometry_source,
    "tiles": [
        {"tile_id": "CENTER", "ucns_slot": "CENTER", "x": 0.0, "y": 0.0},
        {"tile_id": "RING_0", "ucns_slot": "RING_0", "x": 1.0, "y": 0.0},
    ],
    "units": [{"unit_id": "A0", "tile_id": "RING_0", "label": "A0"}],
}
move = {
    "kind": "move",
    "data": {"unit_id": "A0", "from_tile_id": "CENTER", "to_tile_id": "RING_0"},
}
snapshot = snapshot_from_observation(
    observation,
    plane_id="plane-0",
    move_events=[move],
    feed=[{"turn": 1, "text": "public display text only"}],
)
```

The snapshot validator is allowlist-based. Unknown root, geometry, tile, unit,
feed, or motion fields fail closed. The projector drops undeclared observation,
move-event, and feed metadata before validation, preventing a visual snapshot
from becoming a transport for private/internal fields.

The browser exposes tile inspection to pointer and keyboard input, permits
interactive descendants under an SVG `group` role, scales unit-marker spread by
occupant count, and renders the selection ring above the unit layer.

## hmmm

- whether later Flower-of-Life rings belong on this presentation surface;
- the exact live engine-to-observation adapter that attaches UCNS positions is
  owned by the eventual engine integration, not by this graphics package;
- construction animation remains unavailable until an owning mechanics layer
  emits an already-resolved construction event contract.
