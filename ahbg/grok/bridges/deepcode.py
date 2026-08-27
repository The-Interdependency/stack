"""DeepCodeBoardDriver — run Grok's a0 regulatory layer on a frozen DeepCode AHBG board.

This adapter lets the exact same Grok decision surface
    from a0.selfhood import Vessel
    from a0.will import choose_relocate
operate on the DeepCode implementation of the world + turn loop without
modifying any frozen code in stack-deepcode/.

The bridge:
- Uses DeepCode's new_game / TurnLoop / persistence.
- Translates tile ids (Grok BandSlot names <-> short axial labels).
- Shapes observations so Grok a0 sees familiar names.
- Preserves DeepCode's collision behavior (UnresolvedHmmm for War).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]

# Guarantee the local Grok a0 is importable as top-level "a0"
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKSPACE_ROOT))

# Local Grok regulatory surface (this is "your a0")
from a0.selfhood import Vessel  # noqa: E402
from a0.will import choose_relocate  # noqa: E402

from .common import (
    empty_neighbors_from_observation,
    normalize_observation,
    translate_choice,
)


def _load_deep_ahbg():
    """Dynamically load the frozen DeepCode (deepseek) ahbg package in isolation."""
    deep_ahbg_dir = WORKSPACE_ROOT.parents[2] / "stack-deepcode" / "ahbg" / "deepseek" / "ahbg"
    init = deep_ahbg_dir / "__init__.py"
    if not init.exists():
        raise RuntimeError(f"Cannot find frozen DeepCode ahbg at {deep_ahbg_dir}")

    spec = importlib.util.spec_from_file_location("_deep_ahbg", str(init))
    mod = importlib.util.module_from_spec(spec)
    mod.__path__ = [str(deep_ahbg_dir)]
    sys.modules["_deep_ahbg"] = mod
    spec.loader.exec_module(mod)

    for name in ("world", "events", "turns", "persistence"):
        sub = deep_ahbg_dir / f"{name}.py"
        if sub.exists():
            sspec = importlib.util.spec_from_file_location(f"_deep_ahbg.{name}", str(sub))
            smod = importlib.util.module_from_spec(sspec)
            sys.modules[f"_deep_ahbg.{name}"] = smod
            sspec.loader.exec_module(smod)
            setattr(mod, name, smod)

    return mod


_deep_ahbg = _load_deep_ahbg()

TurnLoop = _deep_ahbg.turns.TurnLoop
UnresolvedHmmm = _deep_ahbg.turns.UnresolvedHmmm
ValidationError = _deep_ahbg.turns.ValidationError
new_game = _deep_ahbg.persistence.new_game
replay = _deep_ahbg.persistence.replay


class DeepCodeBoardDriver:
    """Drive a DeepCode board using Grok's Vessel + choose_relocate."""

    def __init__(
        self,
        seed: int = 101,
        *,
        unit_id: str = "A0",
        tiles: list[dict[str, Any]] | None = None,
        units: list[dict[str, Any]] | None = None,
        layers: int | None = None,
    ) -> None:
        self._unit_id = unit_id
        self._from_naming = "deepcode"
        self._to_naming = "grok"

        if layers is not None and tiles is None:
            tiles = self._make_hex_board(layers)

        default_tiles = tiles or [
            {"tile_id": "c", "q": 0, "r": 0, "built": True},
            {"tile_id": "e", "q": 1, "r": 0},
            {"tile_id": "se", "q": 0, "r": 1},
            {"tile_id": "sw", "q": -1, "r": 1},
            {"tile_id": "w", "q": -1, "r": 0},
            {"tile_id": "nw", "q": 0, "r": -1},
            {"tile_id": "ne", "q": 1, "r": -1},
        ]
        # When we generated a hex board, the center tile uses "t0,0"
        center_tile = "t0,0" if layers is not None else "c"
        default_units = units or [{"unit_id": unit_id, "tile_id": center_tile}]

        world, log = new_game(seed, tiles=default_tiles, units=default_units)
        self._world = world
        self._log = log
        self._loop = TurnLoop(world, log)
        self._last_obs: dict[str, Any] | None = None

    def _make_hex_board(self, layers: int) -> list[dict[str, Any]]:
        """Centered hex board of given radius (layers). Center starts built."""
        tiles: list[dict[str, Any]] = []
        for q in range(-layers, layers + 1):
            for r in range(-layers, layers + 1):
                if abs(q) + abs(q + r) + abs(r) <= layers:
                    built = (q == 0 and r == 0)
                    tiles.append({"tile_id": f"t{q},{r}", "q": q, "r": r, "built": built})
        return tiles

    @property
    def world(self):
        return self._world

    @property
    def log(self):
        return self._log

    def observe(self) -> dict[str, Any]:
        from bridges.common import normalize_observation
        raw = self._world.legal_observation()
        shaped = normalize_observation(raw, from_naming=self._from_naming, to_naming=self._to_naming)
        self._last_obs = shaped
        return shaped

    def empty_neighbors(self, unit_id: str | None = None) -> list[str]:
        from bridges.common import empty_neighbors_from_observation
        obs = self._last_obs or self.observe()
        uid = unit_id or self._unit_id
        return empty_neighbors_from_observation(obs, uid, naming=self._to_naming)

    def submit_choice(self, choice: dict[str, Any]) -> list[dict[str, Any]]:
        if choice.get("kind") != "relocate":
            return []
        # Resolve using live world axial lookup so we emit the exact tile id the world uses
        # (important for generated larger boards that use "t{q},{r}" even for ring axials).
        to_wanted = choice.get("to_tile_id")
        unit = choice.get("unit_id", self._unit_id)
        foreign_to = self._resolve_tile_id(to_wanted)
        plan = {
            "turn": self._world.turn,
            "actions": [{"kind": "move", "data": {"unit_id": unit, "to_tile_id": foreign_to}}],
        }
        try:
            self._loop.begin_turn()
            events = self._loop.resolve([plan])
            return [dict(e) if isinstance(e, dict) else getattr(e, "to_dict", lambda: dict(e))() for e in events]
        except (UnresolvedHmmm, ValidationError):
            raise

    def _resolve_tile_id(self, wanted: str) -> str:
        """Map a (possibly grok-naming) label to the concrete tile id present in this world's tiles."""
        from bridges.common import label_to_axial
        try:
            ax = label_to_axial(str(wanted), naming="grok")
        except Exception:
            s = str(wanted).lower().lstrip("t")
            try:
                if "," in s:
                    q, r = s.split(",", 1)
                    ax = (int(q), int(r))
                else:
                    return wanted
            except Exception:
                return wanted
        for tid, tile in self._world.tiles.items():
            if (tile.q, tile.r) == ax:
                return tid
        return wanted

    def submit_build(self, unit_id: str, tile_id: str) -> list[dict[str, Any]]:
        """Submit a construction action on larger boards.

        Accepts either the tile id as exposed by this driver (preferred) or a
        human-friendly name. We resolve by axial coordinate against the live world.
        """
        # Resolve the requested tile by axial in the actual world (most reliable for large boards)
        target_ax = None
        try:
            from bridges.common import label_to_axial
            target_ax = label_to_axial(str(tile_id), naming="grok")
        except Exception:
            # Try to parse as tq,r directly
            s = str(tile_id).lower().lstrip("t")
            try:
                if "," in s:
                    q, r = s.split(",", 1)
                    target_ax = (int(q), int(r))
            except Exception:
                pass

        if target_ax is None:
            # last resort: use as-is (may fail in world, which is correct)
            foreign_tile = tile_id
        else:
            # Find a tile in the current world with that axial
            for tid, tile in self._world.tiles.items():
                if (tile.q, tile.r) == target_ax:
                    foreign_tile = tid
                    break
            else:
                foreign_tile = tile_id

        plan = {
            "turn": self._world.turn,
            "actions": [{"kind": "build", "data": {"unit_id": unit_id, "tile_id": foreign_tile}}],
        }
        try:
            self._loop.begin_turn()
            events = self._loop.resolve([plan])
            return [dict(e) if isinstance(e, dict) else getattr(e, "to_dict", lambda: dict(e))() for e in events]
        except (UnresolvedHmmm, ValidationError):
            raise

    def submit_plan(self, plan: dict[str, Any]) -> list[dict[str, Any]]:
        """Submit a general plan (moves and/or builds).

        Best effort translation of tile ids using axial lookup in the live world.
        """
        from bridges.common import label_to_axial

        def resolve_tile(wanted: str) -> str:
            try:
                ax = label_to_axial(str(wanted), naming="grok")
            except Exception:
                s = str(wanted).lower().lstrip("t")
                try:
                    if "," in s:
                        q, r = s.split(",", 1)
                        ax = (int(q), int(r))
                    else:
                        return wanted
                except Exception:
                    return wanted
            for tid, tile in self._world.tiles.items():
                if (tile.q, tile.r) == ax:
                    return tid
            return wanted

        foreign_plan = {"turn": plan.get("turn", self._world.turn), "actions": []}
        for action in plan.get("actions", []):
            a = dict(action)
            data = dict(a.get("data", {}))
            for k in ("tile_id", "to_tile_id", "from_tile_id"):
                if k in data:
                    data[k] = resolve_tile(data[k])
            a["data"] = data
            foreign_plan["actions"].append(a)

        try:
            self._loop.begin_turn()
            events = self._loop.resolve([foreign_plan])
            return [dict(e) if isinstance(e, dict) else getattr(e, "to_dict", lambda: dict(e))() for e in events]
        except (UnresolvedHmmm, ValidationError):
            raise

    def end_turn(self) -> str:
        try:
            digest = self._world.digest() if hasattr(self._world, "digest") else ""
            return digest
        except (UnresolvedHmmm, ValidationError):
            raise

    def replay_check(self) -> bool:
        try:
            replayed = replay(self._log)
            return replayed.digest() == self._world.digest()
        except Exception:
            return False

    def current_digest(self) -> str:
        if hasattr(self._world, "digest"):
            return self._world.digest()
        return ""
