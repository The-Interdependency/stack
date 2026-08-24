"""Persistence and deterministic replay for AHBG planes.

A persisted plane is two files in one directory:

- ``plane.json``   — the canonical plane snapshot at the last turn boundary.
- ``events.jsonl`` — the append-only event log, one canonical event per line.

Saving verifies that the snapshot equals a replay of the log, and loading
re-verifies the hash chain and the replay before returning anything. Any
divergence raises :class:`ReplayMismatch`; the engine fails closed rather
than trusting a torn or tampered save.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .errors import ReplayMismatch, ValidationError
from .events import KIND_PLANE_INIT, KIND_TURN_BEGIN, KIND_TURN_END, EventLog
from .plane import Plane

PLANE_FILE = "plane.json"
EVENTS_FILE = "events.jsonl"


def new_game(
    seed: int,
    tiles: list[dict[str, Any]],
    units: list[dict[str, Any]],
) -> tuple[Plane, EventLog]:
    """Bootstrap a fresh plane and log it with a ``plane.init`` event."""
    plane = Plane.bootstrap(seed=seed, tiles=tiles, units=units)
    log = EventLog()
    log.append(KIND_PLANE_INIT, turn=0, data={"plane": plane.canonical_dict()})
    return plane, log


def replay(log: EventLog) -> Plane:
    """Reconstruct a plane by folding the event log from its init event.

    Only the canonical envelope events are replayable today:
    ``plane.init``, ``turn.begin``, ``turn.end``. Mechanic events do not
    exist yet, so any other kind fails closed with :class:`ReplayMismatch`.
    """
    log.verify()
    events = log.events
    if not events:
        raise ReplayMismatch("cannot replay an empty event log")

    first = events[0]
    if first.kind != KIND_PLANE_INIT:
        raise ReplayMismatch(
            f"first event must be {KIND_PLANE_INIT!r}, got {first.kind!r}"
        )
    if first.turn != 0:
        raise ReplayMismatch("plane.init must carry turn 0")
    if not isinstance(first.data.get("plane"), dict):
        raise ReplayMismatch("plane.init is missing its plane declaration")
    plane = Plane.from_dict(first.data["plane"])
    if plane.turn != 0:
        raise ReplayMismatch("initial plane must have turn 0")

    phase = "awaiting_begin"
    for event in events[1:]:
        if event.kind == KIND_TURN_BEGIN:
            if phase != "awaiting_begin":
                raise ReplayMismatch(
                    f"turn.begin seq {event.seq} arrived while {phase}"
                )
            if event.turn != plane.turn or event.data.get("turn") != plane.turn:
                raise ReplayMismatch(
                    f"turn.begin seq {event.seq} turn {event.turn} does not "
                    f"match plane turn {plane.turn}"
                )
            phase = "awaiting_end"
        elif event.kind == KIND_TURN_END:
            if phase != "awaiting_end":
                raise ReplayMismatch(
                    f"turn.end seq {event.seq} arrived while {phase}"
                )
            if event.turn != plane.turn or event.data.get("turn") != plane.turn:
                raise ReplayMismatch(
                    f"turn.end seq {event.seq} turn {event.turn} does not "
                    f"match plane turn {plane.turn}"
                )
            expected_digest = plane.digest()
            if event.data.get("state_digest") != expected_digest:
                raise ReplayMismatch(
                    f"turn.end seq {event.seq} state digest does not match "
                    "the replayed plane"
                )
            plane.turn += 1
            phase = "awaiting_begin"
        else:
            raise ReplayMismatch(
                f"event kind {event.kind!r} is not canonical; no mechanic "
                "events exist yet"
            )
    return plane


def save_plane(directory: str | os.PathLike, plane: Plane, log: EventLog) -> Path:
    """Persist a plane and its log, verifying replay equivalence first."""
    plane.validate()
    log.verify()
    replayed = replay(log)
    if replayed.canonical_dict() != plane.canonical_dict():
        raise ReplayMismatch(
            "refusing to save: plane snapshot does not match event log replay"
        )

    target = Path(directory)
    target.mkdir(parents=True, exist_ok=True)

    plane_path = target / PLANE_FILE
    events_path = target / EVENTS_FILE

    plane_tmp = target / f".{PLANE_FILE}.tmp"
    events_tmp = target / f".{EVENTS_FILE}.tmp"
    try:
        plane_tmp.write_text(plane.canonical_json() + "\n", encoding="utf-8")
        events_tmp.write_text(log.to_jsonl(), encoding="utf-8")
        os.replace(plane_tmp, plane_path)
        os.replace(events_tmp, events_path)
    finally:
        for tmp in (plane_tmp, events_tmp):
            if tmp.exists():
                tmp.unlink()
    return target


def load_plane(directory: str | os.PathLike) -> tuple[Plane, EventLog]:
    """Load a persisted plane and verify log integrity plus replay equality."""
    target = Path(directory)
    plane_path = target / PLANE_FILE
    events_path = target / EVENTS_FILE
    if not plane_path.is_file():
        raise ValidationError(f"missing {plane_path}")
    if not events_path.is_file():
        raise ValidationError(f"missing {events_path}")

    plane = Plane.from_json(plane_path.read_text(encoding="utf-8"))
    log = EventLog.from_jsonl(events_path.read_text(encoding="utf-8"))
    log.verify()

    replayed = replay(log)
    if replayed.canonical_dict() != plane.canonical_dict():
        raise ReplayMismatch(
            "persisted plane does not match the replay of its event log"
        )
    return plane, log
