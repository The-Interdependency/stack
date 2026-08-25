"""AHBG presentation snapshot — visual fields only.

This is not plane state and not a mechanics contract. Optional motions are
traces of already-resolved unit relocation between presented tiles.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


KIND = "ahbg.presentation.snapshot"
STANDING = "not-mechanics"
SAMPLE_PATH = Path(__file__).resolve().parent / "sample_snapshot.json"


class PresentationSnapshotError(ValueError):
    """Fail-closed presentation snapshot error."""


def load_snapshot(path: Path | None = None) -> Mapping[str, Any]:
    target = SAMPLE_PATH if path is None else path
    return validate_snapshot(json.loads(target.read_text(encoding="utf-8")))


def validate_snapshot(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if not isinstance(payload, Mapping):
        raise PresentationSnapshotError("snapshot must be an object")
    if payload.get("kind") != KIND:
        raise PresentationSnapshotError(f"kind must be {KIND}")
    if payload.get("standing") != STANDING:
        raise PresentationSnapshotError(f"standing must be {STANDING}")
    if not isinstance(payload.get("plane_id"), str) or not payload["plane_id"]:
        raise PresentationSnapshotError("plane_id must be exact non-empty text")
    if isinstance(payload.get("turn"), bool) or not isinstance(payload.get("turn"), int) or payload["turn"] < 0:
        raise PresentationSnapshotError("turn must be a non-negative int")
    tiles = payload.get("tiles")
    if not isinstance(tiles, list) or not tiles:
        raise PresentationSnapshotError("tiles must be a non-empty list")
    ids: set[str] = set()
    coords: set[tuple[int, int]] = set()
    for tile in tiles:
        if not isinstance(tile, Mapping):
            raise PresentationSnapshotError("each tile must be an object")
        tile_id = tile.get("id")
        q, r = tile.get("q"), tile.get("r")
        if not isinstance(tile_id, str) or not tile_id:
            raise PresentationSnapshotError("tile id must be exact non-empty text")
        if tile_id in ids:
            raise PresentationSnapshotError(f"tile id repeats: {tile_id}")
        if isinstance(q, bool) or isinstance(r, bool) or not isinstance(q, int) or not isinstance(r, int):
            raise PresentationSnapshotError(f"tile {tile_id} q,r must be ints")
        if (q, r) in coords:
            raise PresentationSnapshotError(f"tile axial coordinate repeats: {(q, r)}")
        ids.add(tile_id)
        coords.add((q, r))
        label = tile.get("label")
        if label is not None and (not isinstance(label, str) or not label):
            raise PresentationSnapshotError(f"tile {tile_id} label must be exact non-empty text when present")
    units = payload.get("units")
    if not isinstance(units, list):
        raise PresentationSnapshotError("units must be a list")
    unit_ids: set[str] = set()
    for unit in units:
        if not isinstance(unit, Mapping):
            raise PresentationSnapshotError("each unit must be an object")
        unit_id = unit.get("id")
        tile_id = unit.get("tile")
        if not isinstance(unit_id, str) or not unit_id:
            raise PresentationSnapshotError("unit id must be exact non-empty text")
        if unit_id in unit_ids:
            raise PresentationSnapshotError(f"unit id repeats: {unit_id}")
        if tile_id not in ids:
            raise PresentationSnapshotError(f"unit {unit_id} tile {tile_id!r} is not a presented tile")
        unit_ids.add(unit_id)
    selected = payload.get("selected_tile")
    if selected is not None and selected not in ids:
        raise PresentationSnapshotError("selected_tile must name a presented tile")
    feed = payload.get("feed")
    if not isinstance(feed, list):
        raise PresentationSnapshotError("feed must be a list")
    for item in feed:
        if not isinstance(item, Mapping) or not isinstance(item.get("text"), str) or not item["text"]:
            raise PresentationSnapshotError("each feed item must have exact non-empty text")
    motions = payload.get("motions")
    if motions is None:
        return payload
    if not isinstance(motions, list):
        raise PresentationSnapshotError("motions must be a list when present")
    for motion in motions:
        if not isinstance(motion, Mapping):
            raise PresentationSnapshotError("each motion must be an object")
        unit_id = motion.get("unit")
        from_tile = motion.get("from")
        to_tile = motion.get("to")
        if unit_id not in unit_ids:
            raise PresentationSnapshotError(f"motion unit {unit_id!r} is not a presented unit")
        if from_tile not in ids:
            raise PresentationSnapshotError(f"motion from {from_tile!r} is not a presented tile")
        if to_tile not in ids:
            raise PresentationSnapshotError(f"motion to {to_tile!r} is not a presented tile")
        if from_tile == to_tile:
            raise PresentationSnapshotError(f"motion for {unit_id} must change tiles")
    return payload
