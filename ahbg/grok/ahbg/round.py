"""Turn cycle for the Grok field. Only relocate intents resolve."""

from __future__ import annotations

from dataclasses import dataclass

from .chain import KIND_MOVE, KIND_TURN_BEGIN, KIND_TURN_END, KIND_WAR, Chain
from .patch import Field


@dataclass
class Cycle:
    field: Field
    chain: Chain

    def open_turn(self) -> None:
        self.chain.append(KIND_TURN_BEGIN, self.field.turn, {"turn": self.field.turn})

    def resolve(self, intents: list[tuple[str, str, str]]) -> list[dict[str, str]]:
        applied, war_events = self.field.apply_moves(intents)
        emitted: list[dict[str, str]] = []
        for unit_id, source, dest in applied:
            data = {"unit_id": unit_id, "from_tile_id": source, "to_tile_id": dest}
            self.chain.append(KIND_MOVE, self.field.turn, data)
            emitted.append(data)
        for event in war_events:
            self.chain.append(KIND_WAR, self.field.turn, event)
        return emitted

    def close_turn(self) -> str:
        digest = _field_digest(self.field)
        self.chain.append(
            KIND_TURN_END,
            self.field.turn,
            {"turn": self.field.turn, "state_digest": digest},
        )
        self.field.turn += 1
        return digest


def _field_digest(opened: Field) -> str:
    from .chain import _digest, _dump

    return _digest(_dump(opened.snapshot()))
