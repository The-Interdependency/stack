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
    ) -> None:
        self._unit_id = unit_id
        self._from_naming = "deepcode"
        self._to_naming = "grok"

        default_tiles = tiles or [
            {"tile_id": "c", "q": 0, "r": 0, "built": True},
            {"tile_id": "e", "q": 1, "r": 0},
            {"tile_id": "se", "q": 0, "r": 1},
            {"tile_id": "sw", "q": -1, "r": 1},
            {"tile_id": "w", "q": -1, "r": 0},
            {"tile_id": "nw", "q": 0, "r": -1},
            {"tile_id": "ne", "q": 1, "r": -1},
        ]
        default_units = units or [{"unit_id": unit_id, "tile_id": "c"}]

        world, log = new_game(seed, tiles=default_tiles, units=default_units)
        self._world = world
        self._log = log
        self._loop = TurnLoop(world, log)
        self._last_obs: dict[str, Any] | None = None

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
        from bridges.common import translate_choice
        if choice.get("kind") != "relocate":
            return []
        foreign_choice = translate_choice(choice, from_naming=self._to_naming, to_naming=self._from_naming)
        plan = {
            "turn": self._world.turn,
            "actions": [{"kind": "move", "data": {"unit_id": foreign_choice["unit_id"], "to_tile_id": foreign_choice["to_tile_id"]}}],
        }
        try:
            self._loop.begin_turn()
            events = self._loop.resolve([plan])
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
