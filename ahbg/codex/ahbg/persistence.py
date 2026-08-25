"""Persistence and deterministic replay for the Codex AHBG build."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .events import (
    KIND_MOVE,
    KIND_PLANE_INIT,
    KIND_TURN_BEGIN,
    KIND_TURN_END,
    EventLog,
)
from .geometry import seed_of_life_tiles
from .sim import ReplayError, apply_motions, motion_from_event_data
from .world import World

WORLD_FILE = "world.json"
EVENTS_FILE = "events.jsonl"


def new_world(
    seed: int,
    *,
    tiles: list[dict[str, Any]] | None = None,
    units: list[dict[str, Any]] | None = None,
) -> tuple[World, EventLog]:
    """Create a world from explicit units and UCNS-derived default geometry."""
    world = World.bootstrap(
        seed=seed,
        tiles=seed_of_life_tiles() if tiles is None else tiles,
        units=[{"unit_id": "A0", "tile_id": "c", "label": "A0"}] if units is None else units,
    )
    log = EventLog()
    log.append(KIND_PLANE_INIT, 0, {"world": world.canonical_dict()})
    return world, log


def replay(log: EventLog) -> World:
    """Fold a canonical event log back into a world snapshot."""
    log.verify()
    events = log.events
    if not events:
        raise ReplayError("cannot replay empty log")
    first = events[0]
    if first.kind != KIND_PLANE_INIT:
        raise ReplayError("first event must be plane.init")
    if first.turn != 0:
        raise ReplayError("plane.init must be turn 0")
    world_data = first.data.get("world")
    if not isinstance(world_data, dict):
        raise ReplayError("plane.init missing world data")
    world = World.from_dict(world_data)
    if world.turn != 0:
        raise ReplayError("initial world must start at turn 0")

    phase = "awaiting-begin"
    buffered = []
    for event in events[1:]:
        if event.kind == KIND_TURN_BEGIN:
            if phase != "awaiting-begin":
                raise ReplayError(f"turn.begin while {phase}")
            if event.turn != world.turn or event.data.get("turn") != world.turn:
                raise ReplayError("turn.begin turn mismatch")
            phase = "awaiting-end"
        elif event.kind == KIND_MOVE:
            if phase != "awaiting-end":
                raise ReplayError("move outside open turn")
            if event.turn != world.turn:
                raise ReplayError("move turn mismatch")
            buffered.append(motion_from_event_data(event.data))
        elif event.kind == KIND_TURN_END:
            if phase != "awaiting-end":
                raise ReplayError(f"turn.end while {phase}")
            if event.turn != world.turn or event.data.get("turn") != world.turn:
                raise ReplayError("turn.end turn mismatch")
            apply_motions(world, buffered)
            if event.data.get("state_digest") != world.digest():
                raise ReplayError("turn.end state digest mismatch")
            world.turn += 1
            buffered = []
            phase = "awaiting-begin"
        else:
            raise ReplayError(f"unknown canonical event kind: {event.kind}")
    if phase != "awaiting-begin":
        raise ReplayError("event log ended before turn.end")
    return world


def save_world(directory: str | os.PathLike, world: World, log: EventLog) -> Path:
    """Write a replay-verified world snapshot and event log."""
    log.verify()
    replayed = replay(log)
    if replayed.canonical_dict() != world.canonical_dict():
        raise ReplayError("world does not match replayed log")
    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)
    (target / WORLD_FILE).write_text(world.canonical_json() + "\n", encoding="utf-8")
    (target / EVENTS_FILE).write_text(log.to_jsonl(), encoding="utf-8")
    return target


def load_world(directory: str | os.PathLike) -> tuple[World, EventLog]:
    target = Path(directory)
    world_path = target / WORLD_FILE
    events_path = target / EVENTS_FILE
    if not world_path.is_file() or not events_path.is_file():
        raise ReplayError(f"missing persisted world files in {target}")
    world = World.from_json(world_path.read_text(encoding="utf-8"))
    log = EventLog.from_jsonl(events_path.read_text(encoding="utf-8"))
    if replay(log).canonical_dict() != world.canonical_dict():
        raise ReplayError("persisted world does not match replay")
    return world, log
