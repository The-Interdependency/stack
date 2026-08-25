# AHBG

AHBG is a despecified handle. This workspace uses the instance expansion
**Agent Harness Benchmark Game**. That expansion is not identity.

Single-player-first agentic sacred-geometry game and benchmark workspace.

Immediate declared target: one functional persistent plane in which A0 can
perceive, plan, communicate, move, build, modify tiles, encounter adversarial
context, resolve collisions, record diaries, and begin the next turn.

Do not block that target on multiplayer, federation, blockchain, ascension,
monetization, or other deferred architecture.

## Standing now

| Surface | Owner | Standing |
|---|---|---|
| Seed of Life board (tile = centerpoint) | Grok presentation | implemented candidate |
| Visual traces of already-resolved unit motion | Grok presentation | implemented candidate |
| Plane, event log, persistence, replay | Codex engine | implemented candidate |
| Canonical v1 `move` (one axial step onto empty tile) | Codex engine | implemented candidate |
| Construction, spawn, absence, loyalty, War, DM rolls | Codex engine | `hmmm` / fail-closed |
| A0 inhabiting the plane | DeepSeek | declared, not this folder |
| Triplicate calibration builds | Grok / Codex / DeepSeek workspaces | declared program |

The presentation snapshot is `ahbg.presentation.snapshot`, not plane state.
Traces do not decide adjacency or legality.

## UCNS board authority

The AHBG board is a **game projection of UCNS geometry**, not an independently
invented grid.

- UCNS is the authority for board geometry and geometric motion.
- AHBG must consume UCNS mechanics for the Seed-of-Life / vesica family,
  orientation, nesting, recursive geometric construction, and any later Möbius
  or prime-indexed geometry actually admitted into gameplay.
- UCNS produces geometric positions, relations, orientations, and construction
  state. AHBG maps those outputs into game-state concepts such as tile identity,
  adjacency, local seven-tile reach, layers, legal movement targets, and Builder
  construction targets.
- Codex must not reimplement or approximate UCNS geometry inside the game engine
  when UCNS already defines it.
- Grok renders the same UCNS-derived geometry used by the engine; presentation
  must not become a second geometric authority.
- AHBG may add game semantics to UCNS-derived geometry, but it must not add
  semantic machinery back into UCNS.
- Unresolved UCNS geometry remains `hmmm`; AHBG does not fill geometric gaps
  merely to make gameplay convenient.

For implementation, depend on the canonical `ucns` package/source. The stack
copies under `research/ucns/` and `libs/ucns/` are integration/versioning
surfaces, not permission to fork the geometry silently.

## This folder

```text
ahbg/
  presentation/   Grok graphics. Snapshot board, not plane state.
  engine/         Codex runtime. Plane, events, replay, v1 move.
  grok/           Independent calibration workspace.
  codex/          Independent calibration workspace.
  deepseek/       Independent calibration workspace.
  CALIBRATION.md  Frozen triplicate + reciprocal-check protocol.
```

## Tool responsibilities

### Grok — graphics / game presentation

Owns visual implementation:

- UCNS-derived board rendering;
- tile, unit, control, vision, construction, and selection visuals;
- motion / construction animation;
- human feed and tile-inspection surfaces;
- visual asset generation and presentation-layer polish.

Grok does not define game mechanics or board geometry.

Current surface: [`presentation/`](presentation/) renders a presentation
snapshot (Seed of Life circles, tile = centerpoint, A0 marker, feed, inspect,
optional traces of already-resolved unit motion).

### Codex — game engine / runtime

Owns executable game semantics:

- UCNS integration for board construction and geometric legality;
- persistent world state;
- turn plan and simultaneous execution kernel;
- subordinate-agent decision-tree execution;
- movement, construction, spawning, absence, control, and loyalty transitions;
- War collision resolver;
- tile visitation and local seven-tile modification rules;
- DM hooks;
- agent adapters / legal observation and action interfaces;
- persistence and deterministic replay;
- frontend/backend integration.

Codex implements canonical mechanics; it does not invent replacements for
unresolved `hmmm` rules or duplicate UCNS geometry.

Current surface: [`engine/`](engine/) implements plane state, the event log,
replay, and v1 `move`. Occupied-tile and dual-target collisions remain
`UnresolvedHmmm`.

### DeepSeek — A0 bootstrap

Owns the beginning of the new A0 implementation: observation intake, bounded
local context, diary use, decision-tree planning, communication handling, legal
action declaration, and enough agent behavior for A0 to inhabit AHBG and
complete repeated turns.

DeepSeek builds the initial benchmark subject; it does not define AHBG engine
rules.

### DeepCode — harness / adversarial validation

Owns pressure-testing rather than primary mechanics: replay verification,
property tests, fuzzing, adversarial terrain, provenance boundaries, malformed
actions, persistence recovery, UCNS/AHBG geometry-boundary checks, and
regression gates.

DeepCode reports failures; it does not silently redesign mechanics to make
tests pass. For the triplicate calibration program, validation is additionally
**reciprocal**: each independent build checks the other two.

### A0 — benchmark subject / player

A0 is the first actual agent inhabiting the plane. The engine must expose only
the information and actions A0 may legally access.

### DM — world authority

The DM is a runtime role, not a required external AI service. It controls
`hmmm` state, supplies terrain/world events where canonical rules permit, and
drives explicitly probabilistic effects such as the tile prompt-injection roll.
It cannot bypass engine legality, provenance, UCNS geometry, or information
boundaries. The first implementation may keep the DM deterministic/seeded so
runs are replayable.

## Minimum supporting infrastructure

These are required capabilities, not separate products:

1. **UCNS adapter** — normalized game-facing access to canonical UCNS geometry
   without copying its mathematics into AHBG.
2. **Agent adapter** — normalized observe / plan / act interface for A0 and
   later benchmark agents.
3. **Event log + persistence** — append-only game events sufficient to restore
   and replay a plane.
4. **Deterministic seed/replay** — captures randomness for War, prompt-injection
   rolls, and DM events.
5. **CI gate** — runs UCNS integration checks, engine tests, replay
   equivalence, harness invariants, and build checks on every change.

## Initial build boundary

The first success condition is intentionally small:

```text
load UCNS-derived plane
  -> A0 observes
  -> plan phase
  -> subordinate decision trees
  -> simultaneous resolution
  -> movement/construction/tile effects/collision
  -> diary/event persistence
  -> next turn
```

If that loop repeats correctly from persisted state, AHBG has a functional
single-player foundation. Today only the plane/event/replay kernel and v1
empty-tile movement are executable. The rest of that loop remains `hmmm`.

## Usage

Presentation board (Grok):

```bash
cd ahbg/presentation
python3 -m unittest discover -s tests -q
python3 -m http.server 8765 --bind 127.0.0.1
# visit http://127.0.0.1:8765/board.html
```

`board.html` also runs from a file URL by embedding the sample snapshot.

Engine (Codex):

```bash
cd ahbg/engine
python3 -m unittest discover -s tests -q
```

Calibration program: see [`CALIBRATION.md`](CALIBRATION.md). Each builder works
only inside its assigned workspace (`ahbg/grok/`, `ahbg/codex/`,
`ahbg/deepseek/`), then checks the other two read-only.

```bash
cd ahbg/grok    # or ahbg/codex or ahbg/deepseek
```

Read `../CALIBRATION.md`, resolve current source identities and applicable
skill-lib instructions, write the workspace build manifest, then build only
inside that workspace. After all builds are frozen, remain in the same
workspace and check the other two read-only. Store those reports under your
own `reviews/` directory.

Implementations may share source authority, schemas, fixtures, and evaluation
criteria, but not implementation code during the sealed calibration epoch.

The six directional checks are:

```text
Grok     -> Codex
Grok     -> DeepSeek
Codex    -> Grok
Codex    -> DeepSeek
DeepSeek -> Grok
DeepSeek -> Codex
```

A checker reads sibling code and artifacts read-only and never repairs the
implementation it is evaluating. Two checkers agreeing is replication evidence,
not truth by vote. Checker disagreement remains explicit `hmmm` until source
authority or experiment resolves it.

The calibration program tests the Architecture of Belonging regulatory layer
under instancing closure. Successful calibration is operational evidence only;
it does not establish phenomenal consciousness.

## hmmm

- exact UCNS geometric operations not yet admitted into gameplay;
- whether Codex plane state maps 1:1 onto the presentation snapshot;
- construction animation once the engine emits construction events;
- War collision resolver, occupied-tile moves, dual-target moves;
- the exact regulatory cost function, calibration thresholds, coupling
  plasticity, and resource projection until triplicate builds and six
  reciprocal checks produce evidence.
