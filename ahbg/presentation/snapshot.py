# === MODULE_BUILD ===
# id: ahbg_presentation_snapshot_contract
#   module_name: snapshot
#   module_kind: schema
#   summary: validates the presentation-only AHBG snapshot envelope, including UCNS-derived display positions and exact geometry source identity
#   owner: AHBG presentation
#   public_surface: KIND, STANDING, PresentationSnapshotError, load_snapshot, validate_snapshot
#   internal_surface: _plain_int, _finite_number, _reject_unknown
#   auth_boundary: none
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: ahbg/presentation/tests/test_presentation.py
#   rollout: consumed by presentation projector and browser sample
#   rollback: remove presentation package without changing AHBG mechanics or UCNS
#   requires: pinned UCNS geometry identity supplied in snapshot.geometry_source
#   since: 2026-08-31
#   unresolved: live engine-to-observation geometry adapter remains owned outside presentation
# === END MODULE_BUILD ===

"""AHBG presentation snapshot — visual fields only.

This is not plane state and not a mechanics contract. Tile ``x``/``y`` values
must already be derived from the declared UCNS geometry source; this module does
not reconstruct geometry from AHBG-local coordinates. Optional motions are
traces of already-resolved unit relocation between presented tiles.

Usage guidance:
    ``python -m unittest ahbg.presentation.tests.test_presentation``
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Mapping

KIND = "ahbg.presentation.snapshot"
STANDING = "not-mechanics"
SAMPLE_PATH = Path(__file__).resolve().parent / "sample_snapshot.json"

_ROOT_FIELDS = {"kind", "standing", "plane_id", "turn", "geometry_source", "tiles", "units", "selected_tile", "feed", "motions"}
_GEOMETRY_FIELDS = {"repository", "commit", "module", "schema_id", "schema_version", "projection_id", "selection_effect"}
_TILE_FIELDS = {"id", "label", "source_slot", "x", "y"}
_UNIT_FIELDS = {"id", "tile", "label"}
_FEED_FIELDS = {"turn", "text"}
_MOTION_FIELDS = {"unit", "from", "to"}


class PresentationSnapshotError(ValueError):
    """Fail-closed presentation snapshot error."""


def load_snapshot(path: Path | None = None) -> Mapping[str, Any]:
    target = SAMPLE_PATH if path is None else path
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PresentationSnapshotError(f"cannot load snapshot: {exc}") from exc
    return validate_snapshot(payload)


def _plain_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _finite_number(value: object) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(float(value))
    except (OverflowError, ValueError):
        return False


def _reject_unknown(mapping: Mapping[str, Any], allowed: set[str], surface: str) -> None:
    unknown = sorted(set(mapping) - allowed)
    if unknown:
        raise PresentationSnapshotError(f"{surface} has undeclared fields: {', '.join(unknown)}")


def validate_snapshot(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    if not isinstance(payload, Mapping):
        raise PresentationSnapshotError("snapshot must be an object")
    _reject_unknown(payload, _ROOT_FIELDS, "snapshot")
    if payload.get("kind") != KIND:
        raise PresentationSnapshotError(f"kind must be {KIND}")
    if payload.get("standing") != STANDING:
        raise PresentationSnapshotError(f"standing must be {STANDING}")
    if not isinstance(payload.get("plane_id"), str) or not payload["plane_id"]:
        raise PresentationSnapshotError("plane_id must be exact non-empty text")
    if not _plain_int(payload.get("turn")) or payload["turn"] < 0:
        raise PresentationSnapshotError("turn must be a non-negative int")

    geometry_source = payload.get("geometry_source")
    if not isinstance(geometry_source, Mapping):
        raise PresentationSnapshotError("geometry_source must be an object")
    _reject_unknown(geometry_source, _GEOMETRY_FIELDS, "geometry_source")
    for field in _GEOMETRY_FIELDS:
        value = geometry_source.get(field)
        if not isinstance(value, str) or not value:
            raise PresentationSnapshotError(f"geometry_source.{field} must be exact non-empty text")
    commit = geometry_source["commit"]
    if len(commit) != 40 or any(ch not in "0123456789abcdef" for ch in commit):
        raise PresentationSnapshotError("geometry_source.commit must be a lowercase 40-hex commit")

    tiles = payload.get("tiles")
    if not isinstance(tiles, list) or not tiles:
        raise PresentationSnapshotError("tiles must be a non-empty list")
    ids: set[str] = set()
    source_slots: set[str] = set()
    positions: set[tuple[float, float]] = set()
    for tile in tiles:
        if not isinstance(tile, Mapping):
            raise PresentationSnapshotError("each tile must be an object")
        _reject_unknown(tile, _TILE_FIELDS, "tile")
        tile_id = tile.get("id")
        source_slot = tile.get("source_slot")
        x, y = tile.get("x"), tile.get("y")
        if not isinstance(tile_id, str) or not tile_id:
            raise PresentationSnapshotError("tile id must be exact non-empty text")
        if tile_id in ids:
            raise PresentationSnapshotError(f"tile id repeats: {tile_id}")
        if not isinstance(source_slot, str) or not source_slot:
            raise PresentationSnapshotError(f"tile {tile_id} source_slot must be exact non-empty text")
        if source_slot in source_slots:
            raise PresentationSnapshotError(f"UCNS source slot repeats: {source_slot}")
        if not _finite_number(x) or not _finite_number(y):
            raise PresentationSnapshotError(f"tile {tile_id} x,y must be finite numeric and nonboolean")
        position = (float(x), float(y))
        if position in positions:
            raise PresentationSnapshotError(f"tile source position repeats: {position}")
        if "label" in tile and (not isinstance(tile["label"], str) or not tile["label"]):
            raise PresentationSnapshotError(f"tile {tile_id} label must be exact non-empty text when present")
        ids.add(tile_id)
        source_slots.add(source_slot)
        positions.add(position)

    units = payload.get("units")
    if not isinstance(units, list):
        raise PresentationSnapshotError("units must be a list")
    unit_ids: set[str] = set()
    unit_tiles: dict[str, str] = {}
    for unit in units:
        if not isinstance(unit, Mapping):
            raise PresentationSnapshotError("each unit must be an object")
        _reject_unknown(unit, _UNIT_FIELDS, "unit")
        unit_id = unit.get("id")
        tile_id = unit.get("tile")
        if not isinstance(unit_id, str) or not unit_id:
            raise PresentationSnapshotError("unit id must be exact non-empty text")
        if unit_id in unit_ids:
            raise PresentationSnapshotError(f"unit id repeats: {unit_id}")
        if not isinstance(tile_id, str) or not tile_id:
            raise PresentationSnapshotError(f"unit {unit_id} tile must be exact non-empty text")
        if tile_id not in ids:
            raise PresentationSnapshotError(f"unit {unit_id} tile {tile_id!r} is not a presented tile")
        if "label" in unit and (not isinstance(unit["label"], str) or not unit["label"]):
            raise PresentationSnapshotError(f"unit {unit_id} label must be exact non-empty text when present")
        unit_ids.add(unit_id)
        unit_tiles[unit_id] = tile_id

    selected = payload.get("selected_tile")
    if selected is not None:
        if not isinstance(selected, str) or not selected:
            raise PresentationSnapshotError("selected_tile must be exact non-empty text")
        if selected not in ids:
            raise PresentationSnapshotError("selected_tile must name a presented tile")

    feed = payload.get("feed")
    if not isinstance(feed, list):
        raise PresentationSnapshotError("feed must be a list")
    for item in feed:
        if not isinstance(item, Mapping):
            raise PresentationSnapshotError("each feed item must be an object")
        _reject_unknown(item, _FEED_FIELDS, "feed item")
        if not isinstance(item.get("text"), str) or not item["text"]:
            raise PresentationSnapshotError("each feed item must have exact non-empty text")
        if "turn" in item and (not _plain_int(item["turn"]) or item["turn"] < 0):
            raise PresentationSnapshotError("feed turn must be a non-negative int when present")

    if "motions" not in payload:
        return payload
    motions = payload["motions"]
    if not isinstance(motions, list):
        raise PresentationSnapshotError("motions must be a list when present")
    seen_motion_units: set[str] = set()
    for motion in motions:
        if not isinstance(motion, Mapping):
            raise PresentationSnapshotError("each motion must be an object")
        _reject_unknown(motion, _MOTION_FIELDS, "motion")
        unit_id = motion.get("unit")
        from_tile = motion.get("from")
        to_tile = motion.get("to")
        for name, value in (("unit", unit_id), ("from", from_tile), ("to", to_tile)):
            if not isinstance(value, str) or not value:
                raise PresentationSnapshotError(f"motion {name} must be exact non-empty text")
        if unit_id not in unit_ids:
            raise PresentationSnapshotError(f"motion unit {unit_id!r} is not a presented unit")
        if unit_id in seen_motion_units:
            raise PresentationSnapshotError(f"motion repeats unit {unit_id}")
        if from_tile not in ids:
            raise PresentationSnapshotError(f"motion from {from_tile!r} is not a presented tile")
        if to_tile not in ids:
            raise PresentationSnapshotError(f"motion to {to_tile!r} is not a presented tile")
        if from_tile == to_tile:
            raise PresentationSnapshotError(f"motion for {unit_id} must change tiles")
        if unit_tiles[unit_id] != to_tile:
            raise PresentationSnapshotError(f"motion destination {to_tile!r} does not match unit {unit_id} tile {unit_tiles[unit_id]!r}")
        seen_motion_units.add(unit_id)
    return payload
