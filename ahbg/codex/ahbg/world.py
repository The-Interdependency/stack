"""Codex AHBG world state."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

WORLD_SCHEMA = "interdependency.ahbg.codex.world/1.0.0"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _plain_int(value: Any, field_name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field_name} must be an integer")


def _text(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} must be non-empty text")


@dataclass(frozen=True)
class Tile:
    tile_id: str
    q: int
    r: int
    label: str = ""

    def __post_init__(self) -> None:
        _text(self.tile_id, "tile_id")
        _plain_int(self.q, "tile q")
        _plain_int(self.r, "tile r")
        if not isinstance(self.label, str):
            raise ValueError("tile label must be text")

    def to_dict(self) -> dict[str, Any]:
        return {
            "tile_id": self.tile_id,
            "q": self.q,
            "r": self.r,
            "label": self.label,
        }

    @classmethod
    def from_dict(cls, data: Any) -> "Tile":
        if not isinstance(data, dict):
            raise ValueError("tile must be an object")
        allowed = {"tile_id", "q", "r", "label"}
        unknown = sorted(set(data) - allowed)
        if unknown:
            raise ValueError(f"tile has unknown fields: {unknown}")
        missing = sorted({"tile_id", "q", "r"} - set(data))
        if missing:
            raise ValueError(f"tile is missing fields: {missing}")
        return cls(data["tile_id"], data["q"], data["r"], data.get("label", ""))


@dataclass(frozen=True)
class Unit:
    unit_id: str
    tile_id: str
    label: str = ""

    def __post_init__(self) -> None:
        _text(self.unit_id, "unit_id")
        _text(self.tile_id, "unit tile_id")
        if not isinstance(self.label, str):
            raise ValueError("unit label must be text")

    def to_dict(self) -> dict[str, Any]:
        return {
            "unit_id": self.unit_id,
            "tile_id": self.tile_id,
            "label": self.label,
        }

    @classmethod
    def from_dict(cls, data: Any) -> "Unit":
        if not isinstance(data, dict):
            raise ValueError("unit must be an object")
        allowed = {"unit_id", "tile_id", "label"}
        unknown = sorted(set(data) - allowed)
        if unknown:
            raise ValueError(f"unit has unknown fields: {unknown}")
        missing = sorted({"unit_id", "tile_id"} - set(data))
        if missing:
            raise ValueError(f"unit is missing fields: {missing}")
        return cls(data["unit_id"], data["tile_id"], data.get("label", ""))


@dataclass
class World:
    seed: int
    turn: int = 0
    tiles: dict[str, Tile] = field(default_factory=dict)
    units: dict[str, Unit] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _plain_int(self.seed, "world seed")
        _plain_int(self.turn, "world turn")
        if self.seed < 0 or self.turn < 0:
            raise ValueError("world seed and turn must be non-negative")

    @classmethod
    def bootstrap(
        cls,
        seed: int,
        tiles: list[dict[str, Any]],
        units: list[dict[str, Any]],
    ) -> "World":
        if not tiles:
            raise ValueError("world requires at least one tile")
        if not units:
            raise ValueError("world requires at least one unit")
        world = cls(seed=seed)
        for raw_tile in tiles:
            world.add_tile(Tile.from_dict(raw_tile))
        for raw_unit in units:
            world.add_unit(Unit.from_dict(raw_unit))
        world.validate()
        return world

    def add_tile(self, tile: Tile) -> None:
        if tile.tile_id in self.tiles:
            raise ValueError(f"duplicate tile id: {tile.tile_id}")
        if any((other.q, other.r) == (tile.q, tile.r) for other in self.tiles.values()):
            raise ValueError(f"duplicate axial coordinate: {(tile.q, tile.r)}")
        self.tiles[tile.tile_id] = tile

    def add_unit(self, unit: Unit) -> None:
        if unit.unit_id in self.units:
            raise ValueError(f"duplicate unit id: {unit.unit_id}")
        if unit.tile_id not in self.tiles:
            raise ValueError(f"unit references missing tile: {unit.tile_id}")
        self.units[unit.unit_id] = unit

    def validate(self) -> None:
        coords: set[tuple[int, int]] = set()
        for tile in self.tiles.values():
            tile.__post_init__()
            coord = (tile.q, tile.r)
            if coord in coords:
                raise ValueError(f"duplicate axial coordinate: {coord}")
            coords.add(coord)
        occupied: set[str] = set()
        for unit in self.units.values():
            unit.__post_init__()
            if unit.tile_id not in self.tiles:
                raise ValueError(f"unit references missing tile: {unit.tile_id}")
            if unit.tile_id in occupied:
                raise ValueError(f"two units occupy tile: {unit.tile_id}")
            occupied.add(unit.tile_id)

    def canonical_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "schema": WORLD_SCHEMA,
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
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()

    def legal_observation(self, *, context: dict[str, Any] | None = None) -> dict[str, Any]:
        self.validate()
        return {
            "turn": self.turn,
            "tiles": sorted(
                (tile.to_dict() for tile in self.tiles.values()),
                key=lambda item: item["tile_id"],
            ),
            "units": sorted(
                (unit.to_dict() for unit in self.units.values()),
                key=lambda item: item["unit_id"],
            ),
            "context": dict(context or {}),
        }

    @classmethod
    def from_dict(cls, data: Any) -> "World":
        if not isinstance(data, dict):
            raise ValueError("world must be an object")
        if data.get("schema") != WORLD_SCHEMA:
            raise ValueError(f"world schema must be {WORLD_SCHEMA}")
        unknown = sorted(set(data) - {"schema", "seed", "turn", "tiles", "units"})
        if unknown:
            raise ValueError(f"world has unknown fields: {unknown}")
        world = cls(seed=data.get("seed"), turn=data.get("turn"))
        for raw_tile in data.get("tiles", []):
            world.add_tile(Tile.from_dict(raw_tile))
        for raw_unit in data.get("units", []):
            world.add_unit(Unit.from_dict(raw_unit))
        world.validate()
        return world

    @classmethod
    def from_json(cls, text: str) -> "World":
        return cls.from_dict(json.loads(text))
