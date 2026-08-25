"""Engine-owned projection into the AHBG presentation snapshot contract.

This module converts already-resolved engine state into
``ahbg.presentation.snapshot`` data. It does not validate or decide mechanics;
movement legality has already been settled by the engine before a ``move``
event exists.
"""

from __future__ import annotations

from typing import Any

from ahbg.presentation.snapshot import (
    KIND as PRESENTATION_KIND,
    STANDING as PRESENTATION_STANDING,
    validate_snapshot,
)

from .errors import ReplayMismatch, ValidationError
from .events import KIND_MOVE, KIND_PLANE_INIT, EventLog
from .movement import spec_from_event_data
from .persistence import replay
from .plane import Plane


def motion_traces_from_log(log: EventLog, turn: int | None = None) -> list[dict[str, str]]:
    """Return presentation traces for canonical ``move`` events.

    If ``turn`` is supplied, only move events from that engine turn are
    returned. The trace fields name already-presented unit and tile ids; they
    do not re-check adjacency or War conditions.
    """
    log.verify()
    traces: list[dict[str, str]] = []
    for event in log.events:
        if event.kind != KIND_MOVE:
            continue
        if turn is not None and event.turn != turn:
            continue
        spec = spec_from_event_data(event.data)
        traces.append(
            {
                "unit": spec.unit_id,
                "from": spec.from_tile_id,
                "to": spec.to_tile_id,
            }
        )
    return traces


def feed_from_log(log: EventLog) -> list[dict[str, Any]]:
    """Build a compact human feed from engine provenance events."""
    log.verify()
    feed: list[dict[str, Any]] = []
    for event in log.events:
        if event.kind == KIND_PLANE_INIT:
            units = event.data.get("plane", {}).get("units", [])
            if units:
                placements = ", ".join(
                    f"{unit.get('label') or unit.get('unit_id')} at {unit.get('tile_id')}"
                    for unit in units
                )
                feed.append(
                    {"turn": event.turn, "text": f"plane loaded; {placements}"}
                )
            else:
                feed.append({"turn": event.turn, "text": "plane loaded"})
        elif event.kind == KIND_MOVE:
            spec = spec_from_event_data(event.data)
            feed.append(
                {
                    "turn": event.turn,
                    "text": (
                        f"{spec.unit_id} move "
                        f"{spec.from_tile_id} to {spec.to_tile_id}"
                    ),
                }
            )
    return feed


def snapshot_from_plane(
    plane: Plane,
    log: EventLog | None = None,
    *,
    plane_id: str = "plane-0",
    selected_tile_id: str | None = None,
) -> dict[str, Any]:
    """Project an engine plane into the presentation snapshot format.

    When a log is supplied, it must replay exactly to ``plane`` before any
    presentation data is emitted. Default motion traces are the moves from the
    last completed turn, matching the current visual transition into the
    presented plane state.
    """
    plane.validate()
    if not isinstance(plane_id, str) or not plane_id:
        raise ValidationError("presentation plane_id must be exact non-empty text")
    if log is not None:
        replayed = replay(log)
        if replayed.canonical_dict() != plane.canonical_dict():
            raise ReplayMismatch("presentation snapshot source log does not replay to plane")

    tiles = [
        {"id": tile.tile_id, "q": tile.q, "r": tile.r, "label": tile.tile_id}
        for tile in sorted(plane.tiles.values(), key=lambda item: item.tile_id)
    ]
    units = [
        {
            "id": unit.unit_id,
            "tile": unit.tile_id,
            "label": unit.label or unit.unit_id,
        }
        for unit in sorted(plane.units.values(), key=lambda item: item.unit_id)
    ]
    tile_ids = {tile["id"] for tile in tiles}
    if selected_tile_id is None and units:
        selected_tile_id = units[0]["tile"]
    if selected_tile_id is not None and selected_tile_id not in tile_ids:
        raise ValidationError("selected_tile_id must name a plane tile")

    payload: dict[str, Any] = {
        "kind": PRESENTATION_KIND,
        "standing": PRESENTATION_STANDING,
        "plane_id": plane_id,
        "turn": plane.turn,
        "tiles": tiles,
        "units": units,
        "selected_tile": selected_tile_id,
        "feed": feed_from_log(log) if log is not None else [],
    }
    if log is not None:
        payload["motions"] = motion_traces_from_log(
            log,
            turn=plane.turn - 1 if plane.turn > 0 else None,
        )
    return dict(validate_snapshot(payload))
