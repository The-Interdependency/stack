"""Project a sanitized observation into an AHBG presentation snapshot.

This is graphics. It does not decide adjacency, legality, or turn resolution.
Unknown observation fields are ignored; only the declared visual surface is
copied.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from .snapshot import KIND, STANDING, PresentationSnapshotError, validate_snapshot


def snapshot_from_observation(
    observation: Mapping[str, Any],
    *,
    plane_id: str,
    selected_tile: str | None = None,
    feed: Sequence[Mapping[str, Any]] = (),
    move_events: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Map public tile/unit data and already-resolved moves to display data."""

    if not isinstance(observation, Mapping):
        raise PresentationSnapshotError("observation must be an object")
    if not isinstance(plane_id, str) or not plane_id:
        raise PresentationSnapshotError("plane_id must be exact non-empty text")
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
            "q": tile.get("q"),
            "r": tile.get("r"),
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

    if selected_tile is None and units and isinstance(units[0].get("tile"), str):
        selected_tile = units[0]["tile"]

    snapshot: dict[str, Any] = {
        "kind": KIND,
        "standing": STANDING,
        "plane_id": plane_id,
        "turn": observation.get("turn"),
        "tiles": tiles,
        "units": units,
        "selected_tile": selected_tile,
        "feed": [dict(item) for item in feed],
    }
    if motions:
        snapshot["motions"] = motions
    return dict(validate_snapshot(snapshot))
