"""Project a legal plane view into an AHBG presentation snapshot.

This is graphics. It does not decide adjacency, legality, or turn resolution.
Unknown observation fields are ignored. Seed, RNG, and event-log internals
are not copied into the snapshot.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

try:
    from .snapshot import KIND, STANDING, PresentationSnapshotError, validate_snapshot
except ImportError:  # pragma: no cover - supports direct execution from this folder.
    from snapshot import KIND, STANDING, PresentationSnapshotError, validate_snapshot


def snapshot_from_observation(
    observation: Mapping[str, Any],
    *,
    plane_id: str,
    selected_tile: str | None = None,
    feed: Sequence[Mapping[str, Any]] = (),
    move_events: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Map a public observation (and optional resolved move events) to a snapshot.

    ``observation`` is the legal view: ``turn``, ``tiles``, ``units``. A full
    plane dict is also accepted; ``seed`` and ``schema`` are dropped.
    ``move_events`` are already-resolved ``move`` payloads with ``unit_id``,
    ``from_tile_id``, and ``to_tile_id``.
    """

    if not isinstance(observation, Mapping):
        raise PresentationSnapshotError("observation must be an object")
    if not isinstance(plane_id, str) or not plane_id:
        raise PresentationSnapshotError("plane_id must be exact non-empty text")
    turn = observation.get("turn")
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
        if not isinstance(tile_id, str) or not tile_id:
            raise PresentationSnapshotError("observation tile id must be exact non-empty text")
        presented: dict[str, Any] = {"id": tile_id, "q": tile.get("q"), "r": tile.get("r")}
        label = tile.get("label")
        if isinstance(label, str) and label:
            presented["label"] = label
        tiles.append(presented)

    units: list[dict[str, Any]] = []
    for unit in raw_units:
        if not isinstance(unit, Mapping):
            raise PresentationSnapshotError("each observation unit must be an object")
        unit_id = unit.get("unit_id", unit.get("id"))
        tile_id = unit.get("tile_id", unit.get("tile"))
        if not isinstance(unit_id, str) or not unit_id:
            raise PresentationSnapshotError("observation unit id must be exact non-empty text")
        presented_unit: dict[str, Any] = {"id": unit_id, "tile": tile_id}
        label = unit.get("label")
        if isinstance(label, str) and label:
            presented_unit["label"] = label
        units.append(presented_unit)

    motions: list[dict[str, str]] = []
    for event in move_events:
        if not isinstance(event, Mapping):
            raise PresentationSnapshotError("each move event must be an object")
        kind = event.get("kind")
        data = event.get("data", event)
        if kind not in (None, "move"):
            continue
        if not isinstance(data, Mapping):
            raise PresentationSnapshotError("move event data must be an object")
        motions.append(
            {
                "unit": str(data.get("unit_id", "")),
                "from": str(data.get("from_tile_id", "")),
                "to": str(data.get("to_tile_id", "")),
            }
        )

    if selected_tile is None and units:
        selected_tile = units[0].get("tile") if isinstance(units[0].get("tile"), str) else None

    snapshot = {
        "kind": KIND,
        "standing": STANDING,
        "plane_id": plane_id,
        "turn": turn,
        "tiles": tiles,
        "units": units,
        "selected_tile": selected_tile,
        "feed": [dict(item) for item in feed],
        "motions": motions,
    }
    if not motions:
        snapshot.pop("motions")
    return dict(validate_snapshot(snapshot))
