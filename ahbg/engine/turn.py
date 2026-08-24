"""Turn envelope and the fail-closed action-resolution guard.

The success loop from the AHBG README is:

    load plane -> A0 observes -> plan phase -> subordinate decision trees ->
    simultaneous resolution -> movement/construction/tile effects/collision ->
    diary/event persistence -> next turn

This module owns the envelope: beginning a turn, submitting plans, and ending
a turn with a persisted state digest. The *resolution* of plans into plane
mutations is mechanics. Movement, construction, War, and tile modification
rules are not canonical yet, so resolution fails closed instead of inventing
replacements.
"""

from __future__ import annotations

from dataclasses import dataclass

from .adapter import Plan
from .errors import UnresolvedHmmm
from .events import KIND_TURN_BEGIN, KIND_TURN_END, Event, EventLog
from .plane import Plane


@dataclass
class TurnEngine:
    """Drives turn boundaries over one plane and its event log."""

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

    def resolve(self, plans: list[Plan]) -> None:
        """Resolve submitted plans into plane mutations.

        Resolution is the simultaneous-execution kernel: movement,
        construction, spawning, absence, control/loyalty transitions, War
        collisions, and local seven-tile modification rules. None of those
        rules are canonical yet, so the engine fails closed rather than
        inventing replacements for unresolved ``hmmm`` rules.
        """
        raise UnresolvedHmmm(
            "plan resolution is not yet canonical: movement, construction, "
            "War, and tile-modification rules are unresolved hmmm"
        )
