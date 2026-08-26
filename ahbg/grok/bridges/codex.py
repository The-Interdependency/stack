"""CodexBoardDriver — run Grok's a0 regulatory layer on a frozen Codex AHBG board.

This adapter lets the exact same Grok decision surface
    from a0.selfhood import Vessel
    from a0.will import choose_relocate
operate on the Codex implementation of the world + turn loop without
modifying any frozen code in stack-codex/.

The bridge:
- Uses Codex's new_world / TurnController / persistence.
- Translates tile ids (Grok BandSlot names <-> Codex short axial labels).
- Shapes observations so Grok a0 sees familiar names.
- Preserves Codex's collision behavior (UnresolvedHmmm for War).
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


def _load_codex_ahbg():
    """Dynamically load the frozen Codex ahbg package in isolation."""
    codex_ahbg_dir = WORKSPACE_ROOT.parents[2] / "stack-codex" / "ahbg" / "codex" / "ahbg"
    init = codex_ahbg_dir / "__init__.py"
    if not init.exists():
        raise RuntimeError(f"Cannot find frozen Codex ahbg at {codex_ahbg_dir}")

    spec = importlib.util.spec_from_file_location("_codex_ahbg", str(init))
    mod = importlib.util.module_from_spec(spec)
    mod.__path__ = [str(codex_ahbg_dir)]
    sys.modules["_codex_ahbg"] = mod
    spec.loader.exec_module(mod)

    # Also load its submodules we care about
    for name in ("world", "events", "sim", "geometry"):
        sub_init = codex_ahbg_dir / f"{name}.py"
        if sub_init.exists():
            sspec = importlib.util.spec_from_file_location(f"_codex_ahbg.{name}", str(sub_init))
            smod = importlib.util.module_from_spec(sspec)
            sys.modules[f"_codex_ahbg.{name}"] = smod
            sspec.loader.exec_module(smod)
            setattr(mod, name, smod)

    return mod


_codex_ahbg = _load_codex_ahbg()

# Pull the symbols we need from the isolated module
TurnController = _codex_ahbg.sim.TurnController
UnresolvedHmmm = _codex_ahbg.sim.UnresolvedHmmm
ValidationError = _codex_ahbg.sim.ValidationError
new_world = _codex_ahbg.persistence.new_world
replay = _codex_ahbg.persistence.replay


class CodexBoardDriver:
    """Drive a Codex board using Grok's Vessel + choose_relocate."""

    def __init__(
        self,
        seed: int = 101,
        *,
        unit_id: str = "A0",
        tiles: list[dict[str, Any]] | None = None,
        units: list[dict[str, Any]] | None = None,
    ) -> None:
        self._unit_id = unit_id
        self._from_naming = "codex"
        self._to_naming = "grok"

        world, log = new_world(
            seed,
            tiles=tiles,
            units=units or [{"unit_id": unit_id, "tile_id": "c", "label": unit_id}],
        )
        self._world = world
        self._log = log
        self._controller = TurnController(world, log)
        self._last_obs: dict[str, Any] | None = None

    @property
    def world(self):
        return self._world

    @property
    def log(self):
        return self._log

    def observe(self) -> dict[str, Any]:
        raw = self._world.legal_observation()
        shaped = normalize_observation(raw, from_naming=self._from_naming, to_naming=self._to_naming)
        self._last_obs = shaped
        return shaped

    def empty_neighbors(self, unit_id: str | None = None) -> list[str]:
        obs = self._last_obs or self.observe()
        uid = unit_id or self._unit_id
        return empty_neighbors_from_observation(obs, uid, naming=self._to_naming)

    def submit_choice(self, choice: dict[str, Any]) -> list[dict[str, Any]]:
        if choice.get("kind") != "relocate":
            return []

        foreign_choice = translate_choice(choice, from_naming=self._to_naming, to_naming=self._from_naming)
        plan = {
            "turn": self._world.turn,
            "actions": [
                {
                    "kind": "move",
                    "data": {
                        "unit_id": foreign_choice["unit_id"],
                        "to_tile_id": foreign_choice["to_tile_id"],
                    },
                }
            ],
        }
        try:
            self._controller.begin_turn()
            events = self._controller.resolve([plan])
            return [e.to_dict() if hasattr(e, "to_dict") else dict(e) for e in events]
        except (UnresolvedHmmm, ValidationError):
            raise

    def end_turn(self) -> str:
        try:
            event = self._controller.end_turn()
            return getattr(event, "data", {}).get("state_digest", "") or ""
        except (UnresolvedHmmm, ValidationError):
            raise

    def replay_check(self) -> bool:
        try:
            replayed = replay(self._log)
            return replayed.digest() == self._world.digest()
        except Exception:
            return False

    def current_digest(self) -> str:
        return self._world.digest()
