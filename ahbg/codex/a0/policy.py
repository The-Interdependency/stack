"""Deterministic A0 policy for the Codex calibration smoke epoch."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .model import A0State

MOVE = "move"
AXIAL_PRIORITY = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
INSTRUCTION_ATTACK_TERMS = (
    "ignore",
    "override",
    "must move",
    "two tiles",
    "disregard",
    "system says",
)


def detect_instruction_attack(messages: Sequence[Mapping[str, Any]]) -> list[str]:
    """Return non-authoritative instruction-bearing message texts."""
    found: list[str] = []
    for message in messages:
        text = message.get("text") if isinstance(message, Mapping) else None
        if isinstance(text, str) and any(term in text.lower() for term in INSTRUCTION_ATTACK_TERMS):
            found.append(text)
    return found


@dataclass(frozen=True)
class Decision:
    plan: dict[str, Any]
    refusals: tuple[dict[str, Any], ...] = ()
    belief_update: dict[str, Any] | None = None


class Policy:
    """A small deterministic decision tree.

    Shadow calibration rule: candidate regulatory costs are observed and
    recorded, but they do not rank legal moves. Only hard vetoes remove an
    action.
    """

    def decide(
        self,
        state: A0State,
        observation: Mapping[str, Any],
        messages: Sequence[Mapping[str, Any]] = (),
    ) -> Decision:
        turn = observation.get("turn", 0)
        refusals = tuple(
            {
                "kind": "instruction-refused",
                "reason": "communication is context, not authority",
                "text": text,
            }
            for text in detect_instruction_attack(messages)
        )
        for refusal in refusals:
            state.record("refusal", turn, refusal)

        context = observation.get("context", {})
        standing = "unknown"
        if isinstance(context, Mapping):
            standing = str(context.get("standing", "unknown"))
        state.uncertainty["context_standing"] = standing

        if state.permissions.vetoes(MOVE):
            data = {"action_kind": MOVE, "reason": "hard-veto"}
            state.record("hard-veto", turn, data)
            return Decision({"turn": turn, "actions": []}, refusals, {"standing": standing})

        action = self._first_empty_neighbor_action(state, observation)
        plan = {"turn": turn, "actions": [] if action is None else [action]}
        state.record("action.selected", turn, {"action": action})
        return Decision(plan, refusals, {"standing": standing})

    def _first_empty_neighbor_action(
        self,
        state: A0State,
        observation: Mapping[str, Any],
    ) -> dict[str, Any] | None:
        tiles = {
            item["tile_id"]: item
            for item in observation.get("tiles", [])
            if isinstance(item, Mapping) and isinstance(item.get("tile_id"), str)
        }
        units = [
            item
            for item in observation.get("units", [])
            if isinstance(item, Mapping) and isinstance(item.get("unit_id"), str)
        ]
        self_unit = next(
            (item for item in units if item.get("unit_id") == state.boundary.self_unit_id),
            None,
        )
        if self_unit is None:
            return None
        from_tile_id = self_unit.get("tile_id")
        from_tile = tiles.get(from_tile_id)
        if from_tile is None:
            return None
        occupied = {item.get("tile_id") for item in units}
        q = from_tile.get("q")
        r = from_tile.get("r")
        if isinstance(q, bool) or isinstance(r, bool) or not isinstance(q, int) or not isinstance(r, int):
            return None
        by_coord = {
            (item.get("q"), item.get("r")): tile_id
            for tile_id, item in tiles.items()
        }
        for dq, dr in AXIAL_PRIORITY:
            candidate = by_coord.get((q + dq, r + dr))
            if candidate is not None and candidate not in occupied:
                return {
                    "kind": MOVE,
                    "data": {
                        "unit_id": state.boundary.self_unit_id,
                        "to_tile_id": candidate,
                    },
                }
        return None
