"""Normalized agent-adapter boundary.

A0 (and later benchmark agents) may legally see only the public plane state:
tiles, units, and the current turn. The seed, RNG streams, event log, and DM
state are engine-internal and are never exposed through an observation.

Actions are declared here as an envelope only. Resolving an action into
plane mutations is mechanics; until canonical rules land, the turn engine
fails closed for any submitted plan.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

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


@dataclass(frozen=True)
class Plan:
    """A turn plan: zero or more actions for the declared turn."""

    turn: int
    actions: tuple[Action, ...] = ()


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
