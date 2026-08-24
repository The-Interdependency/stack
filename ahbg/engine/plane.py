"""Plane state: tiles, units, and the canonical serialization used for
persistence and replay digests.

The engine models tiles as axial ``(q, r)`` centerpoints. A tile is the
centerpoint; any circle drawn around it belongs to presentation, not to plane
state. Units must reference existing tiles. The engine does not invent an
initial board: a plane is bootstrapped from an explicit tile/unit declaration
and validates it fail-closed.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from .errors import ValidationError

PLANE_SCHEMA = "ahbg.plane.state/1"

_TILE_KEYS = ("tile_id", "q", "r")
_UNIT_KEYS = ("unit_id", "tile_id", "label")


def canonical_json(obj: Any) -> str:
    """Deterministic single-line JSON with sorted keys.

    This is the one serialization used for digests and persistence, so replay
    is stable across processes and Python versions.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _is_plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


@dataclass(frozen=True)
class Tile:
    """A tile at an axial ``(q, r)`` centerpoint."""

    tile_id: str
    q: int
    r: int

    def __post_init__(self) -> None:
        if not isinstance(self.tile_id, str) or not self.tile_id:
            raise ValidationError("tile_id must be a non-empty string")
        if not _is_plain_int(self.q) or not _is_plain_int(self.r):
            raise ValidationError(f"tile {self.tile_id!r} has non-integer axial coordinates")

    def to_dict(self) -> dict[str, Any]:
        return {"tile_id": self.tile_id, "q": self.q, "r": self.r}

    @classmethod
    def from_dict(cls, data: Any) -> "Tile":
        if not isinstance(data, dict):
            raise ValidationError("tile declaration must be an object")
        unknown = sorted(set(data) - set(_TILE_KEYS))
        if unknown:
            raise ValidationError(f"tile has unknown fields: {unknown}")
        missing = sorted(set(_TILE_KEYS) - set(data))
        if missing:
            raise ValidationError(f"tile is missing fields: {missing}")
        return cls(tile_id=data["tile_id"], q=data["q"], r=data["r"])


@dataclass(frozen=True)
class Unit:
    """A unit standing on an existing tile."""

    unit_id: str
    tile_id: str
    label: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.unit_id, str) or not self.unit_id:
            raise ValidationError("unit_id must be a non-empty string")
        if not isinstance(self.tile_id, str) or not self.tile_id:
            raise ValidationError("unit tile_id must be a non-empty string")
        if not isinstance(self.label, str):
            raise ValidationError("unit label must be a string")

    def to_dict(self) -> dict[str, Any]:
        return {"unit_id": self.unit_id, "tile_id": self.tile_id, "label": self.label}

    @classmethod
    def from_dict(cls, data: Any) -> "Unit":
        if not isinstance(data, dict):
            raise ValidationError("unit declaration must be an object")
        unknown = sorted(set(data) - set(_UNIT_KEYS))
        if unknown:
            raise ValidationError(f"unit has unknown fields: {unknown}")
        missing = sorted(set(_UNIT_KEYS) - set(data))
        if missing:
            raise ValidationError(f"unit is missing fields: {missing}")
        return cls(
            unit_id=data["unit_id"],
            tile_id=data["tile_id"],
            label=data["label"],
        )


@dataclass
class Plane:
    """Mutable plane state plus the seed that deterministically drives it."""

    seed: int
    turn: int = 0
    tiles: dict[str, Tile] = field(default_factory=dict)
    units: dict[str, Unit] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not _is_plain_int(self.seed) or self.seed < 0:
            raise ValidationError("plane seed must be a non-negative integer")
        if not _is_plain_int(self.turn) or self.turn < 0:
            raise ValidationError("plane turn must be a non-negative integer")

    @classmethod
    def bootstrap(
        cls,
        seed: int,
        tiles: list[dict[str, Any]],
        units: list[dict[str, Any]],
    ) -> "Plane":
        """Build a new plane (turn 0) from explicit declarations.

        ``tiles`` and ``units`` must be non-empty: the engine never invents
        initial geometry, it only validates and loads what the host declares.
        """
        if not tiles:
            raise ValidationError("a plane must declare at least one tile")
        if not units:
            raise ValidationError("a plane must declare at least one unit")
        plane = cls(seed=seed, turn=0)
        for raw in tiles:
            tile = Tile.from_dict(raw)
            plane.add_tile(tile)
        for raw in units:
            unit = Unit.from_dict(raw)
            plane.add_unit(unit)
        plane.validate()
        return plane

    def add_tile(self, tile: Tile) -> None:
        if tile.tile_id in self.tiles:
            raise ValidationError(f"duplicate tile id: {tile.tile_id!r}")
        for existing in self.tiles.values():
            if (existing.q, existing.r) == (tile.q, tile.r):
                raise ValidationError(
                    f"duplicate axial coordinate ({tile.q}, {tile.r}) "
                    f"for tiles {existing.tile_id!r} and {tile.tile_id!r}"
                )
        self.tiles[tile.tile_id] = tile

    def add_unit(self, unit: Unit) -> None:
        if unit.unit_id in self.units:
            raise ValidationError(f"duplicate unit id: {unit.unit_id!r}")
        if unit.tile_id not in self.tiles:
            raise ValidationError(
                f"unit {unit.unit_id!r} references missing tile {unit.tile_id!r}"
            )
        self.units[unit.unit_id] = unit

    def validate(self) -> None:
        """Re-run structural checks over the whole plane."""
        for tile in self.tiles.values():
            tile.__post_init__()
        for unit in self.units.values():
            unit.__post_init__()
            if unit.tile_id not in self.tiles:
                raise ValidationError(
                    f"unit {unit.unit_id!r} references missing tile {unit.tile_id!r}"
                )
        seen_coords: set[tuple[int, int]] = set()
        for tile in self.tiles.values():
            coord = (tile.q, tile.r)
            if coord in seen_coords:
                raise ValidationError(f"duplicate axial coordinate {coord}")
            seen_coords.add(coord)

    def canonical_dict(self) -> dict[str, Any]:
        """Deterministic, digestable plane representation."""
        self.validate()
        return {
            "schema": PLANE_SCHEMA,
            "seed": self.seed,
            "turn": self.turn,
            "tiles": sorted(
                (tile.to_dict() for tile in self.tiles.values()),
                key=lambda item: item["tile_id"],
            ),
            "units": sorted(
                (unit.to_dict() for unit in self.units.values()),
                key=lambda item: item["unit_id"],
            ),
        }

    def canonical_json(self) -> str:
        return canonical_json(self.canonical_dict())

    def digest(self) -> str:
        """SHA-256 hex digest of the canonical plane representation."""
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()

    @classmethod
    def from_dict(cls, data: Any) -> "Plane":
        if not isinstance(data, dict):
            raise ValidationError("plane state must be an object")
        if data.get("schema") != PLANE_SCHEMA:
            raise ValidationError(
                f"plane schema must be {PLANE_SCHEMA!r}, got {data.get('schema')!r}"
            )
        unknown = sorted(set(data) - {"schema", "seed", "turn", "tiles", "units"})
        if unknown:
            raise ValidationError(f"plane state has unknown fields: {unknown}")
        plane = cls(
            seed=data.get("seed"),
            turn=data.get("turn"),
        )
        for raw in data.get("tiles", []):
            tile = Tile.from_dict(raw)
            plane.add_tile(tile)
        for raw in data.get("units", []):
            unit = Unit.from_dict(raw)
            plane.add_unit(unit)
        if not plane.tiles:
            raise ValidationError("a plane must declare at least one tile")
        if not plane.units:
            raise ValidationError("a plane must declare at least one unit")
        plane.validate()
        return plane

    @classmethod
    def from_json(cls, text: str) -> "Plane":
        return cls.from_dict(json.loads(text))
