# AHBG presentation

Grok-owned graphics surface. It renders a presentation snapshot. It does not
define game mechanics.

AHBG is a despecified handle. This folder uses the instance expansion
"Agent Harness Benchmark Game" only for this workspace README. That expansion
is not identity.

## Boundary

- Included: Seed of Life circle rendering, tile-as-centerpoint, unit marker, selection, human feed, visual traces of already-resolved unit motion
- Excluded: turns, legal movement, construction, War, loyalty, DM rolls, legal observation
- Codex owns engine state. This snapshot is `ahbg.presentation.snapshot`, not plane state.
- A tile is the centerpoint. The circle around it is geometry, not the tile.
- Optional `motions` are graphics of engine-emitted `move` events. They do not decide adjacency or legality.
- `project.py` maps sanitized legal observations for presentation-local tools
  and tests.
- Engine-owned live snapshots should come through
  `ahbg.engine.snapshot_from_plane()`, which verifies replay equivalence before
  emitting display data.

## Usage

Validate the sample snapshot:

```bash
cd ahbg/presentation
python3 -m unittest discover -s tests -q
```

Open the board:

```bash
python3 -m http.server 8765 --bind 127.0.0.1
# then visit http://127.0.0.1:8765/board.html
```

`board.html` also runs from a file URL by embedding the sample snapshot.

Project a live engine plane (does not decide legality):

```bash
cd ahbg/presentation
python3 - <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, str(Path("../..").resolve()))
from ahbg.engine import Action, Plan, TurnEngine, new_game, snapshot_from_plane

tiles = [
    {"tile_id": "c", "q": 0, "r": 0},
    {"tile_id": "ne", "q": 1, "r": -1},
    {"tile_id": "e", "q": 1, "r": 0},
    {"tile_id": "se", "q": 0, "r": 1},
    {"tile_id": "sw", "q": -1, "r": 1},
    {"tile_id": "w", "q": -1, "r": 0},
    {"tile_id": "nw", "q": 0, "r": -1},
]
plane, log = new_game(seed=7, tiles=tiles, units=[{"unit_id": "A0", "tile_id": "c", "label": "A0"}])
engine = TurnEngine(plane=plane, log=log)
engine.begin_turn()
engine.resolve([Plan(turn=0, actions=(Action("move", {"unit_id": "A0", "to_tile_id": "ne"}),))])
engine.end_turn()
print(snapshot_from_plane(plane, log, plane_id="plane-0")["motions"])
PY
```

## Snapshot contract

A presentation snapshot must include:

- `kind` equal to `ahbg.presentation.snapshot`
- `standing` equal to `not-mechanics`
- unique tile ids with axial `q`,`r`
- units whose `tile` ids exist
- a feed list (may be empty)
- optional `motions` whose `unit`, `from`, and `to` name presented units and tiles

Unknown mechanic fields are ignored. Missing required visual fields fail closed. `motions` do not validate adjacency; that is engine law.

## hmmm

- whether later Flower-of-Life rings are presentation-only extensions of this Seed
- whether later Codex plane state fields will map 1:1 onto this snapshot
- animation of construction once the engine emits construction events
