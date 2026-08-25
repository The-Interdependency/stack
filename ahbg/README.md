# AHBG — Agent Harness Benchmark Game

AHBG is the single-player-first agentic sacred-geometry game and benchmark workspace.

Immediate target: one functional persistent plane in which A0 can perceive, plan, communicate, move, build, modify tiles, encounter adversarial context, resolve collisions, record diaries, and begin the next turn.

Do not block this target on multiplayer, federation, blockchain, ascension, monetization, or other deferred architecture.

## UCNS board authority

The AHBG board is a **game projection of UCNS geometry**, not an independently invented grid.

- UCNS is the authority for board geometry and geometric motion.
- AHBG must consume UCNS mechanics for the Seed-of-Life / vesica family, orientation, nesting, recursive geometric construction, and any later Möbius or prime-indexed geometry actually admitted into gameplay.
- UCNS produces geometric positions, relations, orientations, and construction state. AHBG maps those outputs into game-state concepts such as tile identity, adjacency, local seven-tile reach, layers, legal movement targets, and Builder construction targets.
- No AHBG implementation may reimplement or approximate UCNS geometry when UCNS already defines it.
- Presentation must render the same UCNS-derived geometry used by the engine; presentation is not a second geometric authority.
- AHBG may add game semantics to UCNS-derived geometry, but it must not add semantic machinery back into UCNS.
- Unresolved UCNS geometry remains `hmmm`; AHBG does not fill geometric gaps merely to make gameplay convenient.

For implementation, depend on the canonical `ucns` package/source. The stack copies under `research/ucns/` and `libs/ucns/` are integration/versioning surfaces, not permission to fork the geometry silently.

## Two coordination modes — do not mix them

AHBG now has two different work modes.

### Shared canonical AHBG line

The original specialist split still applies to ordinary coordinated development of the shared AHBG implementation:

- **Grok** — graphics / game presentation.
- **Codex** — game engine / runtime.
- **DeepSeek** — A0 bootstrap.
- **DeepCode** — harness / adversarial validation.

Those are complementary roles on one shared implementation.

### Triplicate calibration line

The embodiment-calibration experiment deliberately suspends that specialist split. It requires three **independent full-stack implementations** so implementation choices themselves can be compared.

The builders are:

| builder | branch | working directory | builds | checks after freeze |
|---|---|---|---|---|
| Grok | `agent/ahbg-grok` | `stack/ahbg/grok/` | its own `a0/` + `ahbg/` | Codex + DeepCode |
| Codex | `agent/ahbg-codex` | `stack/ahbg/codex/` | its own `a0/` + `ahbg/` | Grok + DeepCode |
| DeepCode | `agent/ahbg-deepcode` | `stack/ahbg/deepseek/` | its own `a0/` + `ahbg/` | Grok + Codex |

**The directory name `deepseek/` is the assigned workspace name; the calibration builder assigned to that workspace is DeepCode. Directory name is not builder identity.**

All three calibration branches must start from the same coordination-base commit. During the build phase each builder edits only its assigned workspace and does not read or copy sibling implementation code. After each build is frozen at an exact commit SHA, every builder checks the other two read-only. Review findings are written only into the checker’s own workspace.

No builder provides comparative evidence about itself. There is no sole calibration validator.

The six directional checks are:

```text
Grok     -> Codex
Grok     -> DeepCode
Codex    -> Grok
Codex    -> DeepCode
DeepCode -> Grok
DeepCode -> Codex
```

Agreement is replication evidence, not truth by vote. Disagreement remains `hmmm` until source authority or experiment resolves it.

See [`CALIBRATION.md`](CALIBRATION.md) for the complete protocol.

## Shared-line specialist responsibilities

These responsibilities apply to the **shared canonical AHBG line only**. They are not limits on the three full-stack calibration builders above.

### Grok — graphics / game presentation

Owns visual implementation:
- UCNS-derived board rendering;
- tile, unit, control, vision, construction, and selection visuals;
- motion / construction animation;
- human feed and tile-inspection surfaces;
- visual asset generation and presentation-layer polish.

Grok does not define game mechanics or board geometry on the shared line.

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

Owns the beginning of the shared-line A0 implementation:
- observation intake;
- bounded local context;
- diary use;
- decision-tree planning with contingencies;
- communication handling;
- legal action declaration;
- enough agent behavior for A0 to inhabit AHBG and complete repeated turns.

DeepSeek builds the initial shared-line benchmark subject; it does not define AHBG engine rules.

### DeepCode — harness / adversarial validation

Owns shared-line pressure-testing:
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

DeepCode reports shared-line failures; it does not silently redesign canonical mechanics to make tests pass.

## A0 — benchmark subject / player

A0 is the first actual agent inhabiting the plane. The engine must expose only the information and actions A0 may legally access.

## DM — world authority

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

## Initial shared-line build boundary

The first success condition remains:

`load UCNS-derived plane -> A0 observes -> plan phase -> subordinate decision trees -> simultaneous resolution -> movement/construction/tile effects/collision -> diary/event persistence -> next turn`

If that loop repeats correctly from persisted state, AHBG has a functional single-player foundation.

## Calibration usage guidance

Each calibration builder checks out its own branch and starts in its assigned workspace:

```bash
# Grok
git switch agent/ahbg-grok
cd stack/ahbg/grok

# Codex
git switch agent/ahbg-codex
cd stack/ahbg/codex

# DeepCode
git switch agent/ahbg-deepcode
cd stack/ahbg/deepseek
```

Read `../CALIBRATION.md` before implementation. Record the coordination-base commit and exact source identities in `BUILD_MANIFEST.json`.

Build phase: do not inspect sibling implementation code.

Review phase: after all three build SHAs are frozen, inspect the other two read-only and write findings beneath your own `reviews/` directory. Never patch a sibling while reviewing it.

## hmmm

The exact regulatory cost function, calibration thresholds, coupling plasticity, and resource projection remain intentionally unresolved until the triplicate builds and six reciprocal checks produce evidence.
