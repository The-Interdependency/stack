# === MODULE_BUILD ===
# id: ahbg_presentation_observation_projector
#   module_name: project
#   module_kind: adapter
#   summary: projects a sanitized public observation plus UCNS-derived display coordinates into the strict presentation snapshot schema
#   owner: AHBG presentation
#   public_surface: snapshot_from_observation
#   internal_surface: declared-field projection for geometry source, tiles, units, feed, and resolved motion events
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   tests: ahbg/presentation/tests/test_presentation.py
#   rollout: explicit caller use only
#   rollback: remove projector while retaining snapshot schema and static sample
#   requires: ahbg_presentation_snapshot_contract; caller-supplied UCNS-derived x/y positions and exact geometry source identity
#   since: 2026-08-31
#   unresolved: live engine adapter that supplies UCNS positions is outside presentation ownership
# === END MODULE_BUILD ===

"""Project a sanitized observation into an AHBG presentation snapshot.

This is graphics. It does not decide adjacency, legality, turn resolution, or
UCNS geometry. Callers must supply UCNS-derived display ``x``/``y`` positions
and exact geometry source identity. Unknown observation/feed fields are dropped
rather than copied into the browser-facing envelope.

Usage guidance:
    Call ``snapshot_from_observation`` only after the owning engine/adapter has
    attached source-backed UCNS positions to the public observation.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from .snapshot import KIND, STANDING, PresentationSnapshotError, validate_snapshot


_GEOMETRY_FIELDS = (
    "repository",
    "commit",
    "module",
    "schema_id",
    "schema_version",
    "projection_id",
    "selection_effect",
)


def snapshot_from_observation(
    observation: Mapping[str, Any],
    *,
    plane_id: str,
    selected_tile: str | None = None,
    feed: Sequence[Mapping[str, Any]] = (),
    move_events: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Map declared public visual data and already-resolved moves to display data."""

    if not isinstance(observation, Mapping):
        raise PresentationSnapshotError("observation must be an object")
    if not isinstance(plane_id, str) or not plane_id:
        raise PresentationSnapshotError("plane_id must be exact non-empty text")

    raw_geometry = observation.get("geometry_source")
    if not isinstance(raw_geometry, Mapping):
        raise PresentationSnapshotError("observation geometry_source must be an object")
    geometry_source = {field: raw_geometry.get(field) for field in _GEOMETRY_FIELDS}

    raw_tiles = observation.get("tiles")
    raw_units = observation.get("units")
    if not isinstance(raw_tiles, list) or not raw_tiles:
        raise PresentationSnapshotError("observation tiles must be a non-empty list")
    if not isinstance(raw_units, list):
        raise PresentationSnapshotError("observation units must be a list")

    tiles: list[dict[str, Any]] = []
    for tile in raw_tiles:
        if not isinstance(tile, Mapping):
            raise PresentationSnapshotError("each observation tile must be an object")
        tile_id = tile.get("tile_id", tile.get("id"))
        presented: dict[str, Any] = {
            "id": tile_id,
            "source_slot": tile.get("source_slot", tile.get("ucns_slot")),
            "x": tile.get("x"),
            "y": tile.get("y"),
        }
        if tile.get("label") is not None:
            presented["label"] = tile.get("label")
        tiles.append(presented)

    units: list[dict[str, Any]] = []
    for unit in raw_units:
        if not isinstance(unit, Mapping):
            raise PresentationSnapshotError("each observation unit must be an object")
        presented_unit: dict[str, Any] = {
            "id": unit.get("unit_id", unit.get("id")),
            "tile": unit.get("tile_id", unit.get("tile")),
        }
        if unit.get("label") is not None:
            presented_unit["label"] = unit.get("label")
        units.append(presented_unit)

    motions: list[dict[str, Any]] = []
    for event in move_events:
        if not isinstance(event, Mapping):
            raise PresentationSnapshotError("each move event must be an object")
        kind = event.get("kind")
        if kind not in (None, "move"):
            continue
        data = event.get("data", event)
        if not isinstance(data, Mapping):
            raise PresentationSnapshotError("move event data must be an object")
        motions.append(
            {
                "unit": data.get("unit_id"),
                "from": data.get("from_tile_id"),
                "to": data.get("to_tile_id"),
            }
        )

    presented_feed: list[dict[str, Any]] = []
    for item in feed:
        if not isinstance(item, Mapping):
            raise PresentationSnapshotError("each feed item must be an object")
        row: dict[str, Any] = {"text": item.get("text")}
        if "turn" in item:
            row["turn"] = item.get("turn")
        presented_feed.append(row)

    if selected_tile is None and units and isinstance(units[0].get("tile"), str):
        selected_tile = units[0]["tile"]

    snapshot: dict[str, Any] = {
        "kind": KIND,
        "standing": STANDING,
        "plane_id": plane_id,
        "turn": observation.get("turn"),
        "geometry_source": geometry_source,
        "tiles": tiles,
        "units": units,
        "selected_tile": selected_tile,
        "feed": presented_feed,
    }
    if motions:
        snapshot["motions"] = motions
    return dict(validate_snapshot(snapshot))
