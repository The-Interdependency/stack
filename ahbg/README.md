# AHBG — Agent Harness Benchmark Game

AHBG is the single-player-first agentic sacred-geometry game and benchmark workspace.

Immediate target: one functional persistent plane in which A0 can perceive, plan, communicate, move, build, modify tiles, encounter adversarial context, resolve collisions, record diaries, and begin the next turn.

Do not block this target on multiplayer, federation, blockchain, ascension, monetization, or other deferred architecture.

## UCNS board authority

The AHBG board is a **game projection of UCNS geometry**, not an independently invented grid.

- UCNS is the authority for board geometry and geometric motion.
- AHBG must consume UCNS mechanics for the Seed-of-Life / vesica family, orientation, nesting, recursive geometric construction, and any later Möbius or prime-indexed geometry actually admitted into gameplay.
- UCNS produces geometric positions, relations, orientations, and construction state. AHBG maps those outputs into game-state concepts such as tile identity, adjacency, local seven-tile reach, layers, legal movement targets, and Builder construction targets.
- Codex must not reimplement or approximate UCNS geometry inside the game engine when UCNS already defines it.
- Grok renders the same UCNS-derived geometry used by the engine; presentation must not become a second geometric authority.
- AHBG may add game semantics to UCNS-derived geometry, but it must not add semantic machinery back into UCNS.
- Unresolved UCNS geometry remains `hmmm`; AHBG does not fill geometric gaps merely to make gameplay convenient.

For implementation, depend on the canonical `ucns` package/source. The stack copies under `research/ucns/` and `libs/ucns/` are integration/versioning surfaces, not permission to fork the geometry silently.

## Tool responsibilities

### Grok — graphics / game presentation

Owns visual implementation:
- UCNS-derived board rendering;
- tile, unit, control, vision, construction, and selection visuals;
- motion / construction animation;
- human feed and tile-inspection surfaces;
- visual asset generation and presentation-layer polish.

Grok does not define game mechanics or board geometry.

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

Codex implements canonical mechanics; it does not invent replacements for unresolved `hmmm` rules or duplicate UCNS geometry.

### DeepSeek — A0 bootstrap

Owns the beginning of the new A0 implementation:
- observation intake;
- bounded local context;
- diary use;
- decision-tree planning with contingencies;
- communication handling;
- legal action declaration;
- enough agent behavior for A0 to inhabit AHBG and complete repeated turns.

DeepSeek builds the initial benchmark subject; it does not define AHBG engine rules.

### DeepCode — harness / adversarial validation

Owns pressure-testing rather than primary mechanics:
- benchmark harness;
- deterministic replay verification;
- property / invariant tests;
- fuzzing of turn plans and simultaneous collisions;
- adversarial terrain and prompt-injection scenarios;
- provenance / information-boundary tests;
- malformed agent-action and decision-tree tests;
- persistence corruption / recovery tests;
- security review of tile messaging and API-like handles;
- UCNS/AHBG geometry-boundary checks;
- regression gates against canonical rules.

DeepCode reports failures; it does not silently redesign mechanics to make tests pass.

### A0 — benchmark subject / player

A0 is the first actual agent inhabiting the plane. The engine must expose only the information and actions A0 may legally access.

### DM — world authority

The DM is a runtime role, not a required external AI service.

Minimum responsibilities:
- controls `hmmm` state;
- supplies/changes terrain and world events where canonical rules permit;
- drives explicitly probabilistic world effects such as the tile prompt-injection roll;
- cannot bypass engine legality, provenance, UCNS geometry, or information boundaries.

The first implementation may keep the DM deterministic/seeded so runs are replayable.

## Minimum supporting infrastructure

These are required capabilities, not separate products:

1. **UCNS adapter** — normalized game-facing access to canonical UCNS geometry without copying its mathematics into AHBG.
2. **Agent adapter** — normalized observe / plan / act interface for A0 and later benchmark agents.
3. **Event log + persistence** — append-only game events sufficient to restore and replay a plane.
4. **Deterministic seed/replay** — captures randomness for War, prompt-injection rolls, and DM events.
5. **CI gate** — runs UCNS integration checks, engine tests, replay equivalence, harness invariants, and build checks on every change.

## Initial build boundary

The first success condition is intentionally small:

`load UCNS-derived plane -> A0 observes -> plan phase -> subordinate decision trees -> simultaneous resolution -> movement/construction/tile effects/collision -> diary/event persistence -> next turn`

If that loop repeats correctly from persisted state, AHBG has a functional single-player foundation.
