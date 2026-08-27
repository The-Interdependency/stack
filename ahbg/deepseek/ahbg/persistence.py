# ratios: loc_comments=115:15 imports_exports=7:4 calls_definitions=53:4
"""DeepSeek AHBG realization — persistence and deterministic replay.

A persisted world is two files in one directory:

- ``world.json``  — canonical world snapshot at the last turn boundary.
- ``events.jsonl`` — append-only event log, one canonical event per line.

Saving verifies that the snapshot equals a replay of the log; loading
re-verifies the hash chain and the replay before returning anything.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .events import KIND_BUILD, KIND_MOVE, KIND_PLANE_INIT, KIND_TURN_BEGIN, KIND_TURN_END, EventLog
from .turns import (
    BuildSpec,
    MoveSpec,
    ReplayMismatch,
    UnresolvedHmmm,
    ValidationError,
    _apply_builds_simultaneously,
    _apply_moves_simultaneously,
    build_spec_from_event_data,
    move_spec_from_event_data,
)
from .world import World

WORLD_FILE = "world.json"
EVENTS_FILE = "events.jsonl"


def new_game(seed: int, tiles: list[dict[str, Any]], units: list[dict[str, Any]]) -> tuple[World, EventLog]:
    """Bootstrap a fresh world and log it with a ``plane.init`` event."""
    world = World.bootstrap(seed=seed, tiles=tiles, units=units)
    log = EventLog()
    log.append(KIND_PLANE_INIT, turn=0, data={"world": world.canonical_dict()})
    return world, log


def replay(log: EventLog) -> World:
    """Reconstruct a world by folding the event log from its init event.

    Moves inside a turn are buffered and applied simultaneously at
    ``turn.end``, mirroring the resolution kernel, before the state digest is
    verified. Unknown event kinds fail closed.
    """
    log.verify()
    events = log.events
    if not events:
        raise ReplayMismatch("cannot replay an empty event log")

    first = events[0]
    if first.kind != KIND_PLANE_INIT:
        raise ReplayMismatch(f"first event must be {KIND_PLANE_INIT!r}")
    if first.turn != 0:
        raise ReplayMismatch("plane.init must carry turn 0")
    if not isinstance(first.data.get("world"), dict):
        raise ReplayMismatch("plane.init is missing its world declaration")
    world = World.from_dict(first.data["world"])
    if world.turn != 0:
        raise ReplayMismatch("initial world must have turn 0")

    phase = "awaiting_begin"
    buffered_moves: list[MoveSpec] = []
    buffered_builds: list[BuildSpec] = []
    for event in events[1:]:
        if event.kind == KIND_TURN_BEGIN:
            if phase != "awaiting_begin":
                raise ReplayMismatch(f"turn.begin seq {event.seq} arrived while {phase}")
            if event.turn != world.turn or event.data.get("turn") != world.turn:
                raise ReplayMismatch(f"turn.begin seq {event.seq} turn mismatch")
            phase = "awaiting_end"
        elif event.kind == KIND_MOVE:
            if phase != "awaiting_end":
                raise ReplayMismatch(f"move seq {event.seq} arrived outside an open turn")
            if event.turn != world.turn:
                raise ReplayMismatch(f"move seq {event.seq} turn mismatch")
            buffered_moves.append(move_spec_from_event_data(event.data))
        elif event.kind == KIND_BUILD:
            if phase != "awaiting_end":
                raise ReplayMismatch(f"build seq {event.seq} arrived outside an open turn")
            if event.turn != world.turn:
                raise ReplayMismatch(f"build seq {event.seq} turn mismatch")
            buffered_builds.append(build_spec_from_event_data(event.data))
        elif event.kind == KIND_TURN_END:
            if phase != "awaiting_end":
                raise ReplayMismatch(f"turn.end seq {event.seq} arrived while {phase}")
            if event.turn != world.turn or event.data.get("turn") != world.turn:
                raise ReplayMismatch(f"turn.end seq {event.seq} turn mismatch")
            _apply_moves_simultaneously(world, buffered_moves)
            _apply_builds_simultaneously(world, buffered_builds)
            expected = world.digest()
            if event.data.get("state_digest") != expected:
                raise ReplayMismatch(f"turn.end seq {event.seq} state digest mismatch")
            world.turn += 1
            phase = "awaiting_begin"
            buffered_moves = []
            buffered_builds = []
        else:
            raise ReplayMismatch(f"event kind {event.kind!r} is not canonical")
    return world


def save_world(directory: str | os.PathLike, world: World, log: EventLog) -> Path:
    """Persist a world and its log, verifying replay equivalence first."""
    world.validate()
    log.verify()
    replayed = replay(log)
    if replayed.canonical_dict() != world.canonical_dict():
        raise ReplayMismatch("refusing to save: world snapshot does not match event log replay")

    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    world_path = target / WORLD_FILE
    events_path = target / EVENTS_FILE
    world_tmp = target / f".{WORLD_FILE}.tmp"
    events_tmp = target / f".{EVENTS_FILE}.tmp"
    try:
        world_tmp.write_text(world.canonical_json() + "\n", encoding="utf-8")
        events_tmp.write_text(log.to_jsonl(), encoding="utf-8")
        os.replace(world_tmp, world_path)
        os.replace(events_tmp, events_path)
    finally:
        for tmp in (world_tmp, events_tmp):
            if tmp.exists():
                tmp.unlink()
    return target


def load_world(directory: str | os.PathLike) -> tuple[World, EventLog]:
    """Load a persisted world and verify log integrity plus replay equality."""
    target = Path(directory)
    world_path = target / WORLD_FILE
    events_path = target / EVENTS_FILE
    if not world_path.is_file():
        raise ValidationError(f"missing {world_path}")
    if not events_path.is_file():
        raise ValidationError(f"missing {events_path}")

    world = World.from_json(world_path.read_text(encoding="utf-8"))
    log = EventLog.from_jsonl(events_path.read_text(encoding="utf-8"))
    log.verify()
    replayed = replay(log)
    if replayed.canonical_dict() != world.canonical_dict():
        raise ReplayMismatch("persisted world does not match the replay of its event log")
    return world, log
# ratios: loc_comments=115:15 imports_exports=7:4 calls_definitions=53:4
