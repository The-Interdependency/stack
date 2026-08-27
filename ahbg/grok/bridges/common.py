"""Shared bridge utilities for cross-board operation.

Normalizes tile naming and observation shapes between:
- Grok: BandSlot names (CENTER, RING_0, ...) derived from UCNS axial centers.
- Codex / DeepCode: short axial labels ("c", "e", "se", "sw", "w", "nw", "ne").

The bridge treats axial (q, r) as the common coordinate system.
Grok's Field already projects UCNS to axial; the foreign boards use axial directly.

This module provides:
- AXIAL_TO_CODEx / AXIAL_TO_GROK label maps (seeded from the known 7-tile ring).
- Observation shaping helpers.
- Choice translation helpers.
"""

from __future__ import annotations

import math
from typing import Any, Mapping, Sequence

# Canonical 7-tile ring using short axial labels (shared by Codex and DeepCode workspaces).
# Order is conventional "c, e, se, sw, w, nw, ne".
AXIAL_CENTRAL = (0, 0)
AXIAL_RING: list[tuple[int, int]] = [
    (0, 0),   # c
    (1, 0),   # e
    (0, 1),   # se
    (-1, 1),  # sw
    (-1, 0),  # w
    (0, -1),  # nw
    (1, -1),  # ne
]

CODEX_LABELS = ["c", "e", "se", "sw", "w", "nw", "ne"]

# Grok BandSlot names (derived from ucns.mobius_seed band centers projected to axial).
# We map by (q, r) so that bridges can round-trip without depending on the UCNS package.
GROK_LABELS_BY_AXIAL: dict[tuple[int, int], str] = {
    (0, 0): "CENTER",
    (1, 0): "RING_0",
    (0, 1): "RING_1",
    (-1, 1): "RING_2",
    (-1, 0): "RING_3",
    (0, -1): "RING_4",
    (1, -1): "RING_5",
}

GROK_LABELS = list(GROK_LABELS_BY_AXIAL.values())


def axial_to_label(axial: tuple[int, int], naming: str = "codex") -> str:
    """Map (q, r) to the label used by the named board style.

    For generated larger boards (construction), DeepCode/DeepSeek use "t{q},{r}" ids.
    We preserve that form for axials outside the classic 7-tile ring.
    """
    if naming in ("codex", "deepcode", "deepseek"):
        try:
            idx = AXIAL_RING.index(axial)
            return CODEX_LABELS[idx]
        except ValueError:
            q, r = axial
            return f"t{q},{r}"          # match board generation in game.py and viewer
    if naming == "grok":
        return GROK_LABELS_BY_AXIAL.get(axial, f"t{axial[0]},{axial[1]}")
    raise ValueError(f"unknown naming: {naming}")


def label_to_axial(label: str, naming: str = "codex") -> tuple[int, int]:
    """Reverse map from board-specific label back to (q, r).

    Supports:
    - Grok BandSlot names (CENTER, RING_*)
    - 7-tile short labels used by Codex/DeepCode smoke (c, e, se, ...)
    - Arbitrary DeepCode-style "t{q},{r}" or "q{r}" forms for large boards
    """
    s = str(label).strip()

    # Grok names first
    if naming == "grok":
        for ax, lab in GROK_LABELS_BY_AXIAL.items():
            if lab == s:
                return ax
        # also accept t-forms even if naming says grok (defensive)
        s2 = s.lower()
        if s2.startswith("t"):
            s2 = s2[1:]
        try:
            if "," in s2:
                q, r = s2.split(",", 1)
                return int(q), int(r)
            if "r" in s2:
                qp, rp = s2.replace("q", " ").replace("r", " ").split()
                return int(qp), int(rp)
        except Exception:
            pass

    # Short 7-tile labels (Codex/DeepCode smoke boards)
    if naming in ("codex", "deepcode", "deepseek"):
        try:
            idx = CODEX_LABELS.index(s.lower())
            return AXIAL_RING[idx]
        except ValueError:
            pass

    # t{q},{r} or bare axial forms (used by generated larger boards)
    s2 = s.lower()
    if s2.startswith("t"):
        s2 = s2[1:]
    try:
        if "," in s2:
            q, r = s2.split(",", 1)
            return int(q), int(r)
        if "r" in s2:
            qp, rp = s2.replace("q", " ").replace("r", " ").split()
            return int(qp), int(rp)
        parts = [p for p in s2.replace(",", " ").split() if p]
        if len(parts) == 2:
            return int(parts[0]), int(parts[1])
    except Exception:
        pass

    raise ValueError(f"cannot map label {label!r} under naming {naming}")


def normalize_observation(
    foreign_obs: Mapping[str, Any],
    *,
    from_naming: str,
    to_naming: str = "grok",
) -> dict[str, Any]:
    """Shape a foreign board observation into the target naming.

    The output keeps the same structure (turn, tiles, units, context) but
    rewrites tile_id / from_tile_id / to_tile_id fields using the target labels.
    This lets Grok's choose_relocate see names it understands while the
    underlying board keeps its own identity for replay.

    For generated construction boards (tile ids like "t{q},{r}"), we try hard
    to preserve the original generated ids in the normalized view so that
    submit_build / submit_plan receive ids that actually exist in the world.
    """
    if not isinstance(foreign_obs, Mapping):
        raise TypeError("observation must be a mapping")

    out: dict[str, Any] = {}
    out["turn"] = foreign_obs.get("turn")
    out["context"] = dict(foreign_obs.get("context") or {})

    def _looks_generated(tid: str) -> bool:
        return isinstance(tid, str) and (tid.startswith("t") or "," in tid)

    def _map_tile(t: Mapping[str, Any]) -> dict[str, Any]:
        orig_id = str(t["tile_id"])
        ax = (int(t["q"]), int(t["r"]))
        if _looks_generated(orig_id):
            # Keep generated form for construction boards
            new_id = orig_id
        else:
            new_id = axial_to_label(ax, naming=to_naming)
        t2 = dict(t)
        t2["tile_id"] = new_id
        t2["_foreign_tile_id"] = orig_id
        return t2

    def _map_unit(u: Mapping[str, Any]) -> dict[str, Any]:
        u2 = dict(u)
        if "tile_id" in u2:
            orig = str(u2["tile_id"])
            ax = label_to_axial(orig, naming=from_naming)
            if _looks_generated(orig):
                new_id = orig
            else:
                new_id = axial_to_label(ax, naming=to_naming)
            u2["tile_id"] = new_id
            u2["_foreign_tile_id"] = orig
        return u2

    tiles = foreign_obs.get("tiles") or []
    units = foreign_obs.get("units") or []

    out["tiles"] = [_map_tile(t) for t in tiles]
    out["units"] = [_map_unit(u) for u in units]
    return out


def translate_choice(
    choice: Mapping[str, Any],
    *,
    from_naming: str,
    to_naming: str,
) -> dict[str, Any]:
    """Translate a choice (from choose_relocate or equivalent) between namings.

    Only relocates have tile ids that need mapping. Defer / other choices pass through.
    """
    ch = dict(choice)
    if ch.get("kind") == "relocate":
        for key in ("from_tile_id", "to_tile_id"):
            if key in ch:
                ax = label_to_axial(str(ch[key]), naming=from_naming)
                ch[key] = axial_to_label(ax, naming=to_naming)
                ch[f"_foreign_{key}"] = choice[key]
    return ch


def empty_neighbors_from_observation(
    obs: Mapping[str, Any],
    unit_id: str,
    naming: str = "codex",
) -> list[str]:
    """Given a normalized observation, return tile labels (in that naming) that are empty neighbors of the unit."""
    units = {u["unit_id"]: u for u in obs.get("units", [])}
    tiles_by_id = {t["tile_id"]: t for t in obs.get("tiles", [])}

    unit = units.get(unit_id)
    if not unit:
        return []

    at = unit.get("tile_id")
    if not at or at not in tiles_by_id:
        return []

    at_tile = tiles_by_id[at]
    ax = (int(at_tile["q"]), int(at_tile["r"]))

    occupied = {u["tile_id"] for u in obs.get("units", [])}

    neighbors: list[str] = []
    for dq, dr in ((1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)):
        nax = (ax[0] + dq, ax[1] + dr)
        # find a tile with that axial in the current observation
        for t in obs.get("tiles", []):
            if (int(t["q"]), int(t["r"])) == nax and t["tile_id"] not in occupied:
                neighbors.append(t["tile_id"])
    return sorted(neighbors)


def unbuilt_adjacent_from_observation(
    obs: Mapping[str, Any],
    unit_id: str,
    naming: str = "codex",
) -> list[str]:
    """Return tiles that are adjacent to the unit and not yet built (for construction).

    Tiles are expected to carry a "built" boolean when construction is in play.
    If no "built" key is present, all adjacent tiles are considered buildable.
    """
    units = {u["unit_id"]: u for u in obs.get("units", [])}
    tiles_by_id = {t["tile_id"]: t for t in obs.get("tiles", [])}

    unit = units.get(unit_id)
    if not unit:
        return []

    at = unit.get("tile_id")
    if not at or at not in tiles_by_id:
        return []

    at_tile = tiles_by_id[at]
    ax = (int(at_tile["q"]), int(at_tile["r"]))

    candidates: list[str] = []
    for dq, dr in ((1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)):
        nax = (ax[0] + dq, ax[1] + dr)
        for t in obs.get("tiles", []):
            if (int(t["q"]), int(t["r"])) == nax:
                is_built = bool(t.get("built", False))
                if not is_built:
                    candidates.append(t["tile_id"])
    return sorted(set(candidates))


# ------------------------------------------------------------------
# Hex layout helpers (for viewers). All use flat-top axial layout.
# ------------------------------------------------------------------

def hex_center(q: int, r: int, size: float = 20.0) -> tuple[float, float]:
    """Pixel center for axial (q, r) using flat-top hexes."""
    x = size * (3.0 / 2.0 * q)
    y = size * (math.sqrt(3) / 2.0 * q + math.sqrt(3) * r)
    return x, y


def hex_corners(cx: float, cy: float, size: float = 20.0) -> list[tuple[float, float]]:
    """Return 6 corner points for a flat-top hex centered at (cx, cy)."""
    import math as _m
    pts = []
    for i in range(6):
        angle = _m.pi / 180 * (60 * i)
        x = cx + size * _m.cos(angle)
        y = cy + size * _m.sin(angle)
        pts.append((x, y))
    return pts
