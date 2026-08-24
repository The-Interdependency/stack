# AHBG — Agent Harness Benchmark Game

AHBG is the single-player-first agentic sacred-geometry game and benchmark workspace.

Immediate target: one functional persistent plane in which A0 can perceive, plan, communicate, move, build, modify tiles, encounter adversarial context, resolve collisions, record diaries, and begin the next turn.

Do not block this target on multiplayer, federation, blockchain, ascension, monetization, or other deferred architecture.

## Tool responsibilities

### Grok — graphics / game presentation

Owns visual implementation:
- sacred-geometry board rendering;
- tile, unit, control, vision, construction, and selection visuals;
- motion / construction animation;
- human feed and tile-inspection surfaces;
- visual asset generation and presentation-layer polish.

Grok does not define game mechanics.

Current Grok surface: [`presentation/`](presentation/) renders a
`ahbg.presentation.snapshot` (seven-tile hex neighborhood, A0 marker, feed,
tile inspect). That snapshot is not plane state.

### Codex — game engine / runtime

Owns executable game semantics:
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

Codex implements canonical mechanics; it does not invent replacements for unresolved `hmmm` rules.

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
- cannot bypass engine legality, provenance, or information boundaries.

The first implementation may keep the DM deterministic/seeded so runs are replayable.

## Minimum supporting infrastructure

These are required capabilities, not separate products:

1. **Agent adapter** — normalized observe / plan / act interface for A0 and later benchmark agents.
2. **Event log + persistence** — append-only game events sufficient to restore and replay a plane.
3. **Deterministic seed/replay** — captures randomness for War, prompt-injection rolls, and DM events.
4. **CI gate** — runs engine tests, replay equivalence, harness invariants, and build checks on every change.

## Initial build boundary

The first success condition is intentionally small:

`load plane -> A0 observes -> plan phase -> subordinate decision trees -> simultaneous resolution -> movement/construction/tile effects/collision -> diary/event persistence -> next turn`

If that loop repeats correctly from persisted state, AHBG has a functional single-player foundation.
