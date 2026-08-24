# AHBG engine

Codex-owned executable shell for AHBG. This package implements the
*infrastructure* of the plane — state, provenance, randomness, persistence,
replay — plus the first canonical mechanic, and deliberately stops at the
edge of the remaining unresolved mechanics.

## Boundary

- **Included**: plane state (axial `q,r` tiles, units on tiles), append-only
  event log with a hash chain, deterministic splitmix64 RNG with named
  substreams, save/load with replay equivalence, the turn envelope, the
  normalized agent observation boundary, and canonical v1 movement.
- **Excluded (unresolved `hmmm`)**: construction, spawning, absence,
  control/loyalty transitions, War collision resolution, local seven-tile
  modification rules, DM terrain/world effects, and prompt-injection rolls.
  Any surface that would touch these fails closed with `UnresolvedHmmm`.

## Canonical mechanics

### Movement (v1)

`move` is the first canonical mechanic: a unit may move one step along axial
hex adjacency onto an empty tile. Semantics are simultaneous — every move in
a turn is validated against the pre-turn plane, then all moves apply
atomically.

Still fail-closed:

- moving onto an occupied tile (`UnresolvedHmmm` — War collision resolver),
- two moves targeting the same tile (`UnresolvedHmmm` — War collision
  resolver),
- any action kind other than `move` (`UnresolvedHmmm`).

## Canonical event envelope

| kind | data | meaning |
|---|---|---|
| `plane.init` | `plane` (canonical plane dict) | bootstrap; must be the first event, turn 0 |
| `turn.begin` | `turn` | plan phase opened for that turn |
| `move` | `unit_id`, `from_tile_id`, `to_tile_id` | one resolved move, inside an open turn |
| `turn.end` | `turn`, `state_digest` | turn closed; digest of the plane after resolution, before advancing |

`replay()` folds moves simultaneously at `turn.end` before verifying the
state digest, so a replayed plane always matches the original resolution
kernel. Unknown kinds fail closed.

## Determinism

- Canonical JSON is `json.dumps(..., sort_keys=True, separators=(",", ":"))`
  and never uses process-randomized constructs.
- The RNG is splitmix64 seeded from `sha256(f"{seed}:{domain}")`, so streams
  and substreams (`war`, `prompt-injection`, `dm`) are pure functions of the
  plane seed.
- The event log is a SHA-256 hash chain; truncation or tampering breaks
  `verify()`.

## Persistence

A save directory holds `plane.json` (snapshot) and `events.jsonl` (log).
`save_plane` refuses to write unless the snapshot equals `replay(log)`;
`load_plane` re-verifies both before returning.

## Initial board

The engine does not invent initial geometry. `new_game(seed, tiles, units)`
bootstraps a plane from an explicit declaration and validates it fail-closed.
The canonical starting board is still an open question; until it lands,
callers must declare tiles and units explicitly.
