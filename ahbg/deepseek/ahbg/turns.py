"""DeepSeek AHBG realization — turn loop and simultaneous resolution.

The success loop from the AHBG README:

    load plane -> A0 observes -> plan phase -> subordinate decision trees ->
    simultaneous resolution -> movement/construction/tile effects/collision ->
    diary/event persistence -> next turn

This module owns the envelope and the canonical v1 ``move`` mechanic (one
axial step onto an empty adjacent tile). Every other action kind fails closed
with ``UnresolvedHmmm``, and collision cases (occupied target, dual target)
also fail closed until the War resolver is canonical.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .events import KIND_MOVE, KIND_TURN_BEGIN, KIND_TURN_END, Event, EventLog
from .world import Unit, World

MOVE_ACTION = "move"
MOVE_DATA_KEYS = ("unit_id", "to_tile_id")
MOVE_EVENT_KEYS = ("unit_id", "from_tile_id", "to_tile_id")
_AXIAL_DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1))


class EngineError(Exception):
    """Base class for DeepSeek AHBG engine errors."""


class ValidationError(EngineError):
    """A declaration failed structural validation."""


class UnresolvedHmmm(EngineError):
    """A requested surface touches an unresolved ``hmmm`` rule."""


class ReplayMismatch(EngineError):
    """Persisted state does not match the event log replay."""


def axial_neighbors(q: int, r: int) -> set[tuple[int, int]]:
    return {(q + dq, r + dr) for dq, dr in _AXIAL_DIRECTIONS}


@dataclass(frozen=True)
class MoveSpec:
    unit_id: str
    from_tile_id: str
    to_tile_id: str


def _unit_on_tile(world: World, tile_id: str) -> str | None:
    for unit in world.units.values():
        if unit.tile_id == tile_id:
            return unit.unit_id
    return None


def _validate_move_spec(world: World, spec: MoveSpec) -> None:
    unit = world.units.get(spec.unit_id)
    if unit is None:
        raise ValidationError(f"move references unknown unit {spec.unit_id!r}")
    if unit.tile_id != spec.from_tile_id:
        raise ValidationError(
            f"unit {spec.unit_id!r} is on {unit.tile_id!r}, not {spec.from_tile_id!r}"
        )
    if spec.from_tile_id == spec.to_tile_id:
        raise ValidationError("a move must change tiles")
    if spec.to_tile_id not in world.tiles:
        raise ValidationError(f"move targets unknown tile {spec.to_tile_id!r}")
    from_tile = world.tiles[spec.from_tile_id]
    to_tile = world.tiles[spec.to_tile_id]
    if (to_tile.q, to_tile.r) not in axial_neighbors(from_tile.q, from_tile.r):
        raise ValidationError(f"move {spec.from_tile_id!r} -> {spec.to_tile_id!r} is not adjacent")


def _apply_moves_simultaneously(world: World, specs: list[MoveSpec]) -> None:
    """Validate every move against the pre-turn world, then apply atomically."""
    for spec in specs:
        _validate_move_spec(world, spec)

    unit_ids = [spec.unit_id for spec in specs]
    if len(set(unit_ids)) != len(unit_ids):
        raise ValidationError("a unit may submit at most one move per turn")

    targets: dict[str, str] = {}
    for spec in specs:
        occupant = _unit_on_tile(world, spec.to_tile_id)
        if occupant is not None:
            raise UnresolvedHmmm(
                "War collision resolver is not yet canonical: "
                f"unit {spec.unit_id!r} moves onto occupied tile {spec.to_tile_id!r}"
            )
        if spec.to_tile_id in targets:
            raise UnresolvedHmmm(
                "War collision resolver is not yet canonical: "
                f"two moves target the same tile {spec.to_tile_id!r}"
            )
        targets[spec.to_tile_id] = spec.unit_id

    for spec in sorted(specs, key=lambda item: item.unit_id):
        unit = world.units[spec.unit_id]
        world.units[spec.unit_id] = Unit(unit_id=unit.unit_id, tile_id=spec.to_tile_id)


class TurnLoop:
    """Drives turn boundaries and plan resolution over one world and log."""

    def __init__(self, world: World, log: EventLog) -> None:
        self.world = world
        self.log = log

    def begin_turn(self) -> Event:
        self.world.validate()
        return self.log.append(KIND_TURN_BEGIN, turn=self.world.turn, data={"turn": self.world.turn})

    def resolve(self, plans: list[dict[str, Any]]) -> list[Event]:
        """Resolve submitted plan envelopes into world mutations and events.

        ``plans`` is a list of ``{"turn": int, "actions": [{"kind", "data"}]}``
        envelopes (the A0-facing plan shape). Resolution is simultaneous: all
        moves validate against the pre-turn world, then apply atomically.
        """
        specs = _specs_from_plans(self.world, plans)
        _apply_moves_simultaneously(self.world, specs)
        events: list[Event] = []
        for spec in sorted(specs, key=lambda item: item.unit_id):
            events.append(
                self.log.append(
                    KIND_MOVE,
                    turn=self.world.turn,
                    data={
                        "unit_id": spec.unit_id,
                        "from_tile_id": spec.from_tile_id,
                        "to_tile_id": spec.to_tile_id,
                    },
                )
            )
        return events

    def end_turn(self) -> Event:
        self.world.validate()
        digest = self.world.digest()
        event = self.log.append(
            KIND_TURN_END,
            turn=self.world.turn,
            data={"turn": self.world.turn, "state_digest": digest},
        )
        self.world.turn += 1
        return event


def _specs_from_plans(world: World, plans: list[dict[str, Any]]) -> list[MoveSpec]:
    specs: list[MoveSpec] = []
    for plan in plans:
        if not isinstance(plan, dict):
            raise ValidationError("plan must be an object")
        turn = plan.get("turn")
        if turn != world.turn:
            raise ValidationError(f"plan turn {turn!r} does not match world turn {world.turn}")
        actions = plan.get("actions", [])
        if not isinstance(actions, list):
            raise ValidationError("plan actions must be a list")
        for action in actions:
            if not isinstance(action, dict):
                raise ValidationError("action must be an object")
            kind = action.get("kind")
            data = action.get("data")
            if kind != MOVE_ACTION:
                raise UnresolvedHmmm(f"action kind {kind!r} is not yet canonical; only {MOVE_ACTION!r} resolves")
            if not isinstance(data, dict):
                raise ValidationError("move action data must be an object")
            unknown = sorted(set(data) - set(MOVE_DATA_KEYS))
            if unknown:
                raise ValidationError(f"move action has unknown fields: {unknown}")
            unit_id = data.get("unit_id")
            to_tile_id = data.get("to_tile_id")
            if not isinstance(unit_id, str) or not unit_id:
                raise ValidationError("move action requires a non-empty unit_id")
            if not isinstance(to_tile_id, str) or not to_tile_id:
                raise ValidationError("move action requires a non-empty to_tile_id")
            unit = world.units.get(unit_id)
            if unit is None:
                raise ValidationError(f"move references unknown unit {unit_id!r}")
            specs.append(
                MoveSpec(unit_id=unit_id, from_tile_id=unit.tile_id, to_tile_id=to_tile_id)
            )
    return specs


def move_spec_from_event_data(data: dict[str, Any]) -> MoveSpec:
    unknown = sorted(set(data) - set(MOVE_EVENT_KEYS))
    if unknown:
        raise ValidationError(f"move event has unknown fields: {unknown}")
    missing = sorted(set(MOVE_EVENT_KEYS) - set(data))
    if missing:
        raise ValidationError(f"move event is missing fields: {missing}")
    return MoveSpec(
        unit_id=data["unit_id"],
        from_tile_id=data["from_tile_id"],
        to_tile_id=data["to_tile_id"],
    )
