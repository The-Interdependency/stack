# AHBG presentation

Grok-owned graphics surface. It renders a presentation snapshot. It does not
define game mechanics.

AHBG is a despecified handle. This folder uses the instance expansion
"Agent Harness Benchmark Game" only for this workspace README. That expansion
is not identity.

## Boundary

- Included: hex neighborhood rendering, unit marker, selection highlight, human feed
- Excluded: turns, movement, construction, War, loyalty, DM rolls, legal observation
- Codex owns engine state. This snapshot is `ahbg.presentation.snapshot`, not plane state.

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

## Snapshot contract

A presentation snapshot must include:

- `kind` equal to `ahbg.presentation.snapshot`
- `standing` equal to `not-mechanics`
- unique tile ids with axial `q`,`r`
- units whose `tile` ids exist
- a feed list (may be empty)

Unknown mechanic fields are ignored. Missing required visual fields fail closed.

## hmmm

- exact sacred-geometry vocabulary of the board (hex is a presentation choice)
- whether Codex plane state will map 1:1 onto this snapshot
- animation of motion/construction once the engine emits events
