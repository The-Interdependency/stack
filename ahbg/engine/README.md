# AHBG engine

Codex-owned executable shell for AHBG. This package implements the
*infrastructure* of the plane — state, provenance, randomness, persistence,
replay — and deliberately stops at the edge of canonical mechanics.

## Boundary

- **Included**: plane state (axial `q,r` tiles, units on tiles), append-only
  event log with a hash chain, deterministic splitmix64 RNG with named
  substreams, save/load with replay equivalence, the turn envelope, and the
  normalized agent observation boundary.
- **Excluded (unresolved `hmmm`)**: movement, construction, spawning,
  absence, control/loyalty transitions, War collision resolution, local
  seven-tile modification rules, DM terrain/world effects, and prompt-injection
  rolls. Any surface that would touch these fails closed with
  `UnresolvedHmmm`.

## Canonical event envelope

| kind | data | meaning |
|---|---|---|
| `plane.init` | `plane` (canonical plane dict) | bootstrap; must be the first event, turn 0 |
| `turn.begin` | `turn` | plan phase opened for that turn |
| `turn.end` | `turn`, `state_digest` | turn closed; digest of the plane before advancing |

Mechanic events do not exist yet. `replay()` rejects any other kind.

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
