"""Turn envelope and plan resolution.

The success loop from the AHBG README is:

    load plane -> A0 observes -> plan phase -> subordinate decision trees ->
    simultaneous resolution -> movement/construction/tile effects/collision ->
    diary/event persistence -> next turn

This module owns the envelope: beginning a turn, resolving submitted plans
into plane mutations, and ending a turn with a persisted state digest.

Canonical mechanics so far:
- ``move`` — one-tile axial move onto an empty adjacent tile, resolved
  simultaneously against the pre-turn plane (see ``movement.py``).

Everything else (construction, spawning, absence, control/loyalty
transitions, War collisions, local seven-tile modification rules) still
fails closed with :class:`UnresolvedHmmm`.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import movement
from .adapter import Plan
from .errors import UnresolvedHmmm
from .events import KIND_MOVE, KIND_TURN_BEGIN, KIND_TURN_END, Event, EventLog
from .plane import Plane


@dataclass
class TurnEngine:
    """Drives turn boundaries and plan resolution over one plane and log."""

    plane: Plane
    log: EventLog

    def begin_turn(self) -> Event:
        """Open the current turn for the plan phase."""
        self.plane.validate()
        return self.log.append(
            KIND_TURN_BEGIN,
            turn=self.plane.turn,
            data={"turn": self.plane.turn},
        )

    def resolve(self, plans: list[Plan]) -> list[Event]:
        """Resolve submitted plans into plane mutations and move events.

        Resolution is simultaneous: every move is validated against the
        pre-turn plane, then all moves apply atomically. Returns the emitted
        events in canonical (unit_id-sorted) order.
        """
        specs = movement.specs_from_plans(self.plane, plans)
        movement.apply_moves_simultaneously(self.plane, specs)
        events: list[Event] = []
        for spec in sorted(specs, key=lambda item: item.unit_id):
            events.append(
                self.log.append(
                    KIND_MOVE,
                    turn=self.plane.turn,
                    data=movement.move_event_data(spec),
                )
            )
        return events

    def end_turn(self) -> Event:
        """Close the current turn with a state digest, then advance.

        The digest is recorded *before* the turn counter advances so replay
        can verify each turn boundary against the same canonical state.
        """
        self.plane.validate()
        digest = self.plane.digest()
        event = self.log.append(
            KIND_TURN_END,
            turn=self.plane.turn,
            data={"turn": self.plane.turn, "state_digest": digest},
        )
        self.plane.turn += 1
        return event
