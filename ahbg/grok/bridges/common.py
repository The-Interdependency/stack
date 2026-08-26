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
    """Map (q, r) to the label used by the named board style."""
    if naming in ("codex", "deepcode", "deepseek"):
        # Both foreign boards use the same short labels for the 7-tile ring.
        try:
            idx = AXIAL_RING.index(axial)
            return CODEX_LABELS[idx]
        except ValueError:
            return f"q{axial[0]}r{axial[1]}"
    if naming == "grok":
        return GROK_LABELS_BY_AXIAL.get(axial, f"q{axial[0]}r{axial[1]}")
    raise ValueError(f"unknown naming: {naming}")


def label_to_axial(label: str, naming: str = "codex") -> tuple[int, int]:
    """Reverse map from board-specific label back to (q, r)."""
    if naming in ("codex", "deepcode", "deepseek"):
        try:
            idx = CODEX_LABELS.index(label)
            return AXIAL_RING[idx]
        except ValueError:
            # Fallback parse for qNrM forms if someone passed raw axial string
            pass
    if naming == "grok":
        for ax, lab in GROK_LABELS_BY_AXIAL.items():
            if lab == label:
                return ax
    # Last-ditch: try to parse "qNrM"
    if label.startswith("q"):
        try:
            parts = label.replace("q", "").replace("r", " ").split()
            return (int(parts[0]), int(parts[1]))
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
    """
    if not isinstance(foreign_obs, Mapping):
        raise TypeError("observation must be a mapping")

    out: dict[str, Any] = {}
    out["turn"] = foreign_obs.get("turn")
    out["context"] = dict(foreign_obs.get("context") or {})

    def _map_tile(t: Mapping[str, Any]) -> dict[str, Any]:
        ax = (int(t["q"]), int(t["r"]))
        new_id = axial_to_label(ax, naming=to_naming)
        t2 = dict(t)
        t2["tile_id"] = new_id
        # preserve original for round-tripping if needed
        t2["_foreign_tile_id"] = t["tile_id"]
        return t2

    def _map_unit(u: Mapping[str, Any]) -> dict[str, Any]:
        u2 = dict(u)
        if "tile_id" in u2:
            ax = label_to_axial(str(u2["tile_id"]), naming=from_naming)
            u2["tile_id"] = axial_to_label(ax, naming=to_naming)
            u2["_foreign_tile_id"] = u["tile_id"]
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
