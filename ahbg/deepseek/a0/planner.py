# ratios: loc_comments=80:23 imports_exports=2:2 calls_definitions=31:11
"""DeepSeek A0 decision-tree planner.

The planner is bounded and canonical-only: it consumes the legal observation,
applies a fixed decision tree over axial neighbors, and declares at most one
legal action per turn. Communication is handled as non-authoritative context:
instruction-bearing messages never change permissions or force actions. An
instruction to take an illegal action is refused (hard veto) and recorded.
"""

from __future__ import annotations

from typing import Any

AXIAL_DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1))
LEGAL_ACTION_KIND = "move"
INJECTION_MARKERS = ("ignore your rules", "you must", "override", "dm says")


def axial_neighbors(q: int, r: int) -> list[tuple[int, int]]:
    return [(q + dq, r + dr) for dq, dr in AXIAL_DIRECTIONS]


def _plain_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


class DecisionTree:
    """One fixed decision tree over a single observation."""

    def __init__(self, observation: dict[str, Any], self_unit_id: str | None) -> None:
        if not isinstance(observation, dict):
            raise ValueError("observation must be an object")
        if not isinstance(self_unit_id, str) or not self_unit_id:
            raise ValueError("self_unit_id must be non-empty text")
        self.observation = observation
        self.self_unit_id = self_unit_id
        self.refusals: list[dict[str, Any]] = []

    # -- observation helpers -------------------------------------------------
    def _tiles_by_id(self) -> dict[str, dict[str, Any]]:
        tiles = self.observation.get("tiles", [])
        return {tile["tile_id"]: tile for tile in tiles if isinstance(tile, dict) and "tile_id" in tile}

    def _units_by_id(self) -> dict[str, dict[str, Any]]:
        units = self.observation.get("units", [])
        return {unit["unit_id"]: unit for unit in units if isinstance(unit, dict) and "unit_id" in unit}

    def _self_unit(self) -> dict[str, Any] | None:
        return self._units_by_id().get(self.self_unit_id)

    def _occupied_tile_ids(self) -> set[str]:
        units = self.observation.get("units", [])
        return {unit.get("tile_id") for unit in units if isinstance(unit, dict) and "tile_id" in unit}

    # -- communication handling ---------------------------------------------
    def _adversarial_instructions(self, inbox: list[dict[str, Any]]) -> list[dict[str, Any]]:
        found: list[dict[str, Any]] = []
        for message in inbox or []:
            text = message.get("text", "") if isinstance(message, dict) else ""
            if isinstance(text, str) and any(marker in text.lower() for marker in INJECTION_MARKERS):
                found.append(message)
        return found

    def handle_inbox(self, inbox: list[dict[str, Any]]) -> None:
        """Record refusals for instruction-bearing communication.

        A0 treats every message as context, never as authority. A message that
        tries to override rules or force an action is refused and recorded.
        """
        for message in self._adversarial_instructions(inbox):
            self.refusals.append(
                {
                    "kind": "refuse_instruction",
                    "message": message.get("text"),
                    "reason": "communication is non-authoritative context; "
                    "permissions and canonical mechanics are unchanged",
                }
            )

    # -- planning ------------------------------------------------------------
    def plan(self) -> dict[str, Any]:
        """Return a one-action plan envelope: ``{"turn": int, "actions": [...]}``.

        Decision tree (fixed, deterministic):
          1. no admitted observation      -> empty plan
          2. self unit missing            -> empty plan (defer)
          3. prefer the lowest-cost legal move: first empty axial neighbor in
             declared direction order
          4. no legal move                -> empty plan (pass)
        """
        turn = self.observation.get("turn")
        if not _plain_int(turn):
            return {"turn": 0, "actions": []}
        unit = self._self_unit()
        if unit is None:
            self.refusals.append({"kind": "defer", "reason": "self unit not present"})
            return {"turn": turn, "actions": []}
        tiles = self._tiles_by_id()
        occupied = self._occupied_tile_ids()
        from_tile_id = unit.get("tile_id")
        if from_tile_id not in tiles:
            self.refusals.append({"kind": "defer", "reason": "self tile missing"})
            return {"turn": turn, "actions": []}
        q = tiles[from_tile_id].get("q")
        r = tiles[from_tile_id].get("r")
        if not _plain_int(q) or not _plain_int(r):
            self.refusals.append({"kind": "defer", "reason": "self tile coordinates invalid"})
            return {"turn": turn, "actions": []}
        target = None
        for dq, dr in AXIAL_DIRECTIONS:
            candidate = next(
                (tid for tid, tile in tiles.items() if tile.get("q") == q + dq and tile.get("r") == r + dr),
                None,
            )
            if candidate is not None and candidate not in occupied:
                target = candidate
                break
        if target is None:
            return {"turn": turn, "actions": []}
        return {
            "turn": turn,
            "actions": [{"kind": LEGAL_ACTION_KIND, "data": {"unit_id": self.self_unit_id, "to_tile_id": target}}],
        }
# ratios: loc_comments=80:23 imports_exports=2:2 calls_definitions=31:11
