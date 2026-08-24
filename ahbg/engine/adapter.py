"""Normalized agent-adapter boundary.

A0 (and later benchmark agents) may legally see only the public plane state:
tiles, units, and the current turn. The seed, RNG streams, event log, and DM
state are engine-internal and are never exposed through an observation.

Actions are declared as an envelope. Resolving an action into plane
mutations is mechanics; the first canonical action is ``move``, and every
other kind still fails closed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from .errors import ValidationError
from .plane import Plane


@dataclass(frozen=True)
class Observation:
    """The legal view of the plane for an agent."""

    turn: int
    tiles: tuple[dict[str, Any], ...]
    units: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "turn": self.turn,
            "tiles": [dict(tile) for tile in self.tiles],
            "units": [dict(unit) for unit in self.units],
        }


@dataclass(frozen=True)
class Action:
    """One declared intent. ``kind`` and ``data`` are validated by the engine."""

    kind: str
    data: dict[str, Any]

    def __post_init__(self) -> None:
        if not isinstance(self.kind, str) or not self.kind:
            raise ValidationError("action kind must be a non-empty string")
        if not isinstance(self.data, dict):
            raise ValidationError("action data must be an object")


@dataclass(frozen=True)
class Plan:
    """A turn plan: zero or more actions for the declared turn."""

    turn: int
    actions: tuple[Action, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.turn, int) or isinstance(self.turn, bool) or self.turn < 0:
            raise ValidationError("plan turn must be a non-negative integer")
        object.__setattr__(self, "actions", tuple(self.actions))
        for action in self.actions:
            if not isinstance(action, Action):
                raise ValidationError("plan actions must be Action instances")


class AgentAdapter(Protocol):
    """The normalized observe / plan interface for benchmark agents."""

    def observe(self, observation: Observation) -> None: ...

    def plan(self, observation: Observation) -> Plan: ...


def legal_observation(plane: Plane) -> Observation:
    """Build the observation A0 may legally receive from a plane."""
    plane.validate()
    return Observation(
        turn=plane.turn,
        tiles=tuple(tile.to_dict() for tile in plane.tiles.values()),
        units=tuple(unit.to_dict() for unit in plane.units.values()),
    )
