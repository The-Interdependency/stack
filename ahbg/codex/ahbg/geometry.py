"""UCNS-backed geometry projection for the Codex AHBG build."""

from __future__ import annotations

import importlib
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

TILE_ORDER = ("e", "se", "sw", "w", "nw", "ne")
AXIAL_DIRECTIONS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))


def _stack_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _ucns_mobius_seed() -> Any:
    try:
        return importlib.import_module("ucns.mobius_seed")
    except ModuleNotFoundError as exc:
        if exc.name != "ucns":
            raise
        source_root = _stack_root() / "research" / "ucns" / "src"
        if not source_root.is_dir():
            raise RuntimeError(f"canonical UCNS source is unavailable: {source_root}") from exc
        sys.path.insert(0, str(source_root))
        return importlib.import_module("ucns.mobius_seed")


def _fraction(value: Any, field_name: str) -> Fraction:
    if not isinstance(value, Fraction):
        raise RuntimeError(f"UCNS point {field_name} is not an exact Fraction")
    return value


def _point_to_axial(point: Any) -> tuple[int, int]:
    """Map an exact UCNS 2D point onto AHBG axial center coordinates."""
    x_rational = _fraction(point.x.rational, "x.rational")
    x_sqrt3 = _fraction(point.x.sqrt3, "x.sqrt3")
    y_rational = _fraction(point.y.rational, "y.rational")
    y_sqrt3 = _fraction(point.y.sqrt3, "y.sqrt3")
    if x_sqrt3 != 0 or y_rational != 0:
        raise RuntimeError("UCNS point is outside AHBG's axial projection plane")
    r = 2 * y_sqrt3
    q = x_rational - r / 2
    if q.denominator != 1 or r.denominator != 1:
        raise RuntimeError("UCNS point does not project to integer AHBG coordinates")
    return int(q), int(r)


def seed_of_life_tiles() -> list[dict[str, Any]]:
    """Return AHBG tiles from canonical UCNS Seed-of-Life ring centers."""
    seed = _ucns_mobius_seed().build_mobius_seed_of_life()
    tiles: list[dict[str, Any]] = [{"tile_id": "c", "q": 0, "r": 0, "label": "center"}]
    for index, tile_id in enumerate(TILE_ORDER):
        q, r = _point_to_axial(seed.node_by_id[f"RING_{index}"].point)
        tiles.append({"tile_id": tile_id, "q": q, "r": r, "label": tile_id})
    return tiles


def axial_neighbors(q: int, r: int) -> set[tuple[int, int]]:
    return {(q + dq, r + dr) for dq, dr in AXIAL_DIRECTIONS}
