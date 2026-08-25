"""DeepSeek AHBG realization — controlled world state.

Independent implementation of the AHBG environment. It consumes the same
event-kind envelope as the shared protocol (``plane.init``, ``turn.begin``,
``move``, ``turn.end``) but is written from scratch: no import or copy from
``ahbg/engine`` or ``ahbg/presentation``.

A world is a controlled plane: tiles at axial ``(q, r)`` centerpoints and units
standing on tiles. The builder must declare the initial board explicitly; the
DeepSeek environment never invents a substitute board (UCNS remains the board
geometry authority).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

WORLD_SCHEMA = "interdependency.ahbg.deepseek.world/1.0.0"

_TILE_KEYS = ("tile_id", "q", "r")
_UNIT_KEYS = ("unit_id", "tile_id")


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


@dataclass(frozen=True)
class Tile:
    tile_id: str
    q: int
    r: int

    def __post_init__(self) -> None:
        if not isinstance(self.tile_id, str) or not self.tile_id:
            raise ValueError("tile_id must be non-empty text")
        if not _plain_int(self.q) or not _plain_int(self.r):
            raise ValueError(f"tile {self.tile_id!r} q,r must be integers")

    def to_dict(self) -> dict[str, Any]:
        return {"tile_id": self.tile_id, "q": self.q, "r": self.r}

    @classmethod
    def from_dict(cls, data: Any) -> "Tile":
        if not isinstance(data, dict):
            raise ValueError("tile must be an object")
        _reject_unknown(data, _TILE_KEYS, "tile")
        _require_keys(data, _TILE_KEYS, "tile")
        return cls(tile_id=data["tile_id"], q=data["q"], r=data["r"])


@dataclass(frozen=True)
class Unit:
    unit_id: str
    tile_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.unit_id, str) or not self.unit_id:
            raise ValueError("unit_id must be non-empty text")
        if not isinstance(self.tile_id, str) or not self.tile_id:
            raise ValueError("unit tile_id must be non-empty text")

    def to_dict(self) -> dict[str, Any]:
        return {"unit_id": self.unit_id, "tile_id": self.tile_id}

    @classmethod
    def from_dict(cls, data: Any) -> "Unit":
        if not isinstance(data, dict):
            raise ValueError("unit must be an object")
        _reject_unknown(data, _UNIT_KEYS, "unit")
        _require_keys(data, _UNIT_KEYS, "unit")
        return cls(unit_id=data["unit_id"], tile_id=data["tile_id"])


def _reject_unknown(data: dict[str, Any], keys: tuple[str, ...], label: str) -> None:
    unknown = sorted(set(data) - set(keys))
    if unknown:
        raise ValueError(f"{label} has unknown fields: {unknown}")


def _require_keys(data: dict[str, Any], keys: tuple[str, ...], label: str) -> None:
    missing = sorted(set(keys) - set(data))
    if missing:
        raise ValueError(f"{label} is missing fields: {missing}")


@dataclass
class World:
    """Mutable controlled world plus its deterministic seed."""

    seed: int
    turn: int = 0
    tiles: dict[str, Tile] = field(default_factory=dict)
    units: dict[str, Unit] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not _plain_int(self.seed) or self.seed < 0:
            raise ValueError("world seed must be a non-negative integer")
        if not _plain_int(self.turn) or self.turn < 0:
            raise ValueError("world turn must be a non-negative integer")

    @classmethod
    def bootstrap(cls, seed: int, tiles: list[dict[str, Any]], units: list[dict[str, Any]]) -> "World":
        if not tiles or not units:
            raise ValueError("a world must declare at least one tile and one unit")
        world = cls(seed=seed, turn=0)
        for raw in tiles:
            world.add_tile(Tile.from_dict(raw))
        for raw in units:
            world.add_unit(Unit.from_dict(raw))
        world.validate()
        return world

    def add_tile(self, tile: Tile) -> None:
        if tile.tile_id in self.tiles:
            raise ValueError(f"duplicate tile id {tile.tile_id!r}")
        for existing in self.tiles.values():
            if (existing.q, existing.r) == (tile.q, tile.r):
                raise ValueError(f"duplicate axial coordinate ({tile.q},{tile.r})")
        self.tiles[tile.tile_id] = tile

    def add_unit(self, unit: Unit) -> None:
        if unit.unit_id in self.units:
            raise ValueError(f"duplicate unit id {unit.unit_id!r}")
        if unit.tile_id not in self.tiles:
            raise ValueError(f"unit {unit.unit_id!r} references missing tile {unit.tile_id!r}")
        self.units[unit.unit_id] = unit

    def validate(self) -> None:
        for tile in self.tiles.values():
            tile.__post_init__()
        for unit in self.units.values():
            unit.__post_init__()
            if unit.tile_id not in self.tiles:
                raise ValueError(f"unit {unit.unit_id!r} references missing tile {unit.tile_id!r}")

    def canonical_dict(self) -> dict[str, Any]:
        self.validate()
        return {
            "schema": WORLD_SCHEMA,
            "seed": self.seed,
            "turn": self.turn,
            "tiles": sorted((t.to_dict() for t in self.tiles.values()), key=lambda d: d["tile_id"]),
            "units": sorted((u.to_dict() for u in self.units.values()), key=lambda d: d["unit_id"]),
        }

    def canonical_json(self) -> str:
        return canonical_json(self.canonical_dict())

    def digest(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()

    @classmethod
    def from_dict(cls, data: Any) -> "World":
        if not isinstance(data, dict):
            raise ValueError("world state must be an object")
        if data.get("schema") != WORLD_SCHEMA:
            raise ValueError(f"world schema must be {WORLD_SCHEMA!r}")
        _reject_unknown(data, ("schema", "seed", "turn", "tiles", "units"), "world")
        world = cls(seed=data.get("seed"), turn=data.get("turn"))
        for raw in data.get("tiles", []):
            world.add_tile(Tile.from_dict(raw))
        for raw in data.get("units", []):
            world.add_unit(Unit.from_dict(raw))
        if not world.tiles or not world.units:
            raise ValueError("a world must declare at least one tile and one unit")
        world.validate()
        return world

    @classmethod
    def from_json(cls, text: str) -> "World":
        return cls.from_dict(json.loads(text))

    # -- legal observation surface -----------------------------------------
    def legal_observation(self) -> dict[str, Any]:
        """The only view A0 may legally receive: turn, tiles, units."""
        self.validate()
        return {
            "turn": self.turn,
            "tiles": [t.to_dict() for t in sorted(self.tiles.values(), key=lambda t: t.tile_id)],
            "units": [u.to_dict() for u in sorted(self.units.values(), key=lambda u: u.unit_id)],
        }
