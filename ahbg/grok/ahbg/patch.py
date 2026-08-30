"""Grok field: UCNS Seed-of-Life centers as tiles.

Tiles are named by UCNS band slots. Axial (q, r) is a game projection of those
centers, not a substitute board. Movement adjacency uses that projection.
War collisions remain ClosedUnknown.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

_UCNS = Path(__file__).resolve().parents[3] / "research" / "ucns" / "src"
if str(_UCNS) not in sys.path:
    sys.path.insert(0, str(_UCNS))

from ucns.mobius_seed import build_mobius_seed_of_life  # noqa: E402


SCHEMA = "interdependency.ahbg.grok.field/1"


class ClosedUnknown(RuntimeError):
    """Fail-closed surface whose governing rule is still hmmm."""


def _axial_of(x: float, y: float) -> tuple[int, int]:
    r = int(round((2.0 * y) / math.sqrt(3.0)))
    q = int(round(x - (r / 2.0)))
    return q, r


def tile_from_ucns() -> list[dict[str, Any]]:
    """Seven tiles from UCNS Möbius Seed of Life band centers."""

    seed = build_mobius_seed_of_life()
    tiles: list[dict[str, Any]] = []
    for band in seed.bands:
        x, y = band.center.to_float()
        q, r = _axial_of(x, y)
        tiles.append({"tile_id": band.slot.value, "q": q, "r": r, "ucns_slot": band.slot.value})
    if len(tiles) != 7:
        raise ValueError("UCNS seed must yield seven band centers")
    return tiles


def _steps() -> tuple[tuple[int, int], ...]:
    # Clockwise from +x. Independent of sibling direction lists.
    return ((1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1))


@dataclass(frozen=True)
class Cell:
    tile_id: str
    q: int
    r: int
    ucns_slot: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {"tile_id": self.tile_id, "q": self.q, "r": self.r, "ucns_slot": self.ucns_slot or self.tile_id}


@dataclass(frozen=True)
class Occupant:
    unit_id: str
    tile_id: str
    label: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {"unit_id": self.unit_id, "tile_id": self.tile_id, "label": self.label or self.unit_id}


@dataclass
class Field:
    seed: int
    turn: int = 0
    cells: dict[str, Cell] = field(default_factory=dict)
    occupants: dict[str, Occupant] = field(default_factory=dict)

    @classmethod
    def open(cls, seed: int, tiles: list[Mapping[str, Any]], units: list[Mapping[str, Any]]) -> "Field":
        opened = cls(seed=seed, turn=0)
        for raw in tiles:
            cell = Cell(str(raw["tile_id"]), int(raw["q"]), int(raw["r"]), str(raw.get("ucns_slot") or raw["tile_id"]))
            if cell.tile_id in opened.cells:
                raise ValueError(f"duplicate tile {cell.tile_id}")
            opened.cells[cell.tile_id] = cell
        for raw in units:
            unit = Occupant(str(raw["unit_id"]), str(raw["tile_id"]), str(raw.get("label") or raw["unit_id"]))
            if unit.unit_id in opened.occupants:
                raise ValueError(f"duplicate unit {unit.unit_id}")
            if unit.tile_id not in opened.cells:
                raise ValueError(f"unit {unit.unit_id} has no tile {unit.tile_id}")
            opened.occupants[unit.unit_id] = unit
        if not opened.cells or not opened.occupants:
            raise ValueError("field needs tiles and units")
        return opened

    def occupant_on(self, tile_id: str) -> str | None:
        for unit in self.occupants.values():
            if unit.tile_id == tile_id:
                return unit.unit_id
        return None

    def neighbors(self, tile_id: str) -> list[str]:
        cell = self.cells[tile_id]
        wanted = {(cell.q + dq, cell.r + dr) for dq, dr in _steps()}
        found = [other.tile_id for other in self.cells.values() if (other.q, other.r) in wanted]
        return sorted(found)

    def snapshot(self) -> dict[str, Any]:
        return {
            "schema": SCHEMA,
            "seed": self.seed,
            "turn": self.turn,
            "tiles": sorted((c.as_dict() for c in self.cells.values()), key=lambda item: item["tile_id"]),
            "units": sorted((u.as_dict() for u in self.occupants.values()), key=lambda item: item["unit_id"]),
        }

    def apply_moves(self, intents: list[tuple[str, str, str]]) -> None:
        """Simultaneous relocate. Occupied or shared destinations stay ClosedUnknown."""

        if len({unit for unit, _src, _dst in intents}) != len(intents):
            raise ValueError("one intent per unit per turn")
        destinations: dict[str, str] = {}
        for unit_id, source, dest in intents:
            unit = self.occupants.get(unit_id)
            if unit is None or unit.tile_id != source:
                raise ValueError(f"{unit_id} is not on {source}")
            if dest not in self.cells:
                raise ValueError(f"unknown destination {dest}")
            if dest not in self.neighbors(source):
                raise ValueError(f"{source} is not adjacent to {dest}")
            sitting = self.occupant_on(dest)
            if sitting is not None:
                raise ClosedUnknown(
                    f"War collision resolver is hmmm: {unit_id} onto occupied {dest}"
                )
            if dest in destinations:
                raise ClosedUnknown(
                    f"War collision resolver is hmmm: two intents target {dest}"
                )
            destinations[dest] = unit_id
        for unit_id, _source, dest in sorted(intents, key=lambda item: item[0]):
            current = self.occupants[unit_id]
            self.occupants[unit_id] = Occupant(current.unit_id, dest, current.label)
