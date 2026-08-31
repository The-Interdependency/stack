"""Turn execution for the Codex AHBG build."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from .events import KIND_MOVE, KIND_TURN_BEGIN, KIND_TURN_END, KIND_WAR, Event, EventLog
from .geometry import axial_neighbors
from .world import Unit, World

MOVE = "move"


class AHBGError(Exception):
    """Base error for the Codex AHBG runtime."""


class ValidationError(AHBGError):
    """Input violated a declared structural contract."""


class UnresolvedHmmm(AHBGError):
    """Requested behavior touches a deliberately unresolved rule."""


class ReplayError(AHBGError):
    """Event replay failed closed."""


@dataclass(frozen=True)
class Action:
    kind: str
    data: dict[str, Any]


@dataclass(frozen=True)
class Plan:
    turn: int
    actions: tuple[Action, ...]


@dataclass(frozen=True)
class Motion:
    unit_id: str
    from_tile_id: str
    to_tile_id: str

    def event_data(self) -> dict[str, str]:
        return {
            "unit_id": self.unit_id,
            "from_tile_id": self.from_tile_id,
            "to_tile_id": self.to_tile_id,
        }


@dataclass(frozen=True)
class WarSpec:
    unit_id: str
    to_tile_id: str
    reason: str
    outcome: str

    def event_data(self) -> dict[str, str]:
        return {
            "unit_id": self.unit_id,
            "to_tile_id": self.to_tile_id,
            "reason": self.reason,
            "outcome": self.outcome,
        }


def plan_from_mapping(data: Mapping[str, Any]) -> Plan:
    if not isinstance(data, Mapping):
        raise ValidationError("plan must be an object")
    turn = data.get("turn")
    if isinstance(turn, bool) or not isinstance(turn, int) or turn < 0:
        raise ValidationError("plan turn must be a non-negative integer")
    raw_actions = data.get("actions", [])
    if not isinstance(raw_actions, list):
        raise ValidationError("plan actions must be a list")
    actions: list[Action] = []
    for raw_action in raw_actions:
        if not isinstance(raw_action, Mapping):
            raise ValidationError("action must be an object")
        kind = raw_action.get("kind")
        action_data = raw_action.get("data")
        if not isinstance(kind, str) or not kind:
            raise ValidationError("action kind must be non-empty text")
        if not isinstance(action_data, dict):
            raise ValidationError("action data must be an object")
        actions.append(Action(kind=kind, data=dict(action_data)))
    return Plan(turn=turn, actions=tuple(actions))


def motion_from_event_data(data: Mapping[str, Any]) -> Motion:
    allowed = {"unit_id", "from_tile_id", "to_tile_id"}
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ReplayError(f"move event has unknown fields: {unknown}")
    missing = sorted(allowed - set(data))
    if missing:
        raise ReplayError(f"move event is missing fields: {missing}")
    unit_id = data["unit_id"]
    from_tile_id = data["from_tile_id"]
    to_tile_id = data["to_tile_id"]
    if not all(isinstance(value, str) and value for value in (unit_id, from_tile_id, to_tile_id)):
        raise ReplayError("move event ids must be non-empty text")
    return Motion(unit_id, from_tile_id, to_tile_id)


def war_spec_from_event_data(data: Mapping[str, Any]) -> WarSpec:
    allowed = {"unit_id", "to_tile_id", "reason", "outcome"}
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise ReplayError(f"war event has unknown fields: {unknown}")
    missing = sorted(allowed - set(data))
    if missing:
        raise ReplayError(f"war event is missing fields: {missing}")
    unit_id = data["unit_id"]
    to_tile_id = data["to_tile_id"]
    reason = data["reason"]
    outcome = data["outcome"]
    if not all(isinstance(value, str) and value for value in (unit_id, to_tile_id, reason, outcome)):
        raise ReplayError("war event fields must be non-empty text")
    if reason not in {"occupied", "dual_target"}:
        raise ReplayError(f"unknown war reason: {reason}")
    if outcome not in {"defender_holds", "priority_win", "priority_loss"}:
        raise ReplayError(f"unknown war outcome: {outcome}")
    return WarSpec(unit_id, to_tile_id, reason, outcome)


def motions_from_plans(world: World, plans: Sequence[Plan]) -> list[Motion]:
    motions: list[Motion] = []
    for plan in plans:
        if plan.turn != world.turn:
            raise ValidationError(f"plan turn {plan.turn} does not match world turn {world.turn}")
        for action in plan.actions:
            if action.kind != MOVE:
                raise UnresolvedHmmm(f"action {action.kind!r} is not canonical in this smoke build")
            allowed = {"unit_id", "to_tile_id"}
            unknown = sorted(set(action.data) - allowed)
            if unknown:
                raise ValidationError(f"move action has unknown fields: {unknown}")
            unit_id = action.data.get("unit_id")
            to_tile_id = action.data.get("to_tile_id")
            if not isinstance(unit_id, str) or not unit_id:
                raise ValidationError("move requires unit_id")
            if not isinstance(to_tile_id, str) or not to_tile_id:
                raise ValidationError("move requires to_tile_id")
            unit = world.units.get(unit_id)
            if unit is None:
                raise ValidationError(f"unknown unit: {unit_id}")
            motions.append(Motion(unit_id, unit.tile_id, to_tile_id))
    return motions


def _unit_on_tile(world: World, tile_id: str) -> str | None:
    for unit in world.units.values():
        if unit.tile_id == tile_id:
            return unit.unit_id
    return None


def _resolve_war(world: World, motions: Sequence[Motion]) -> tuple[list[Motion], list[WarSpec]]:
    """Resolve simultaneous move collisions against the pre-turn world."""
    seen_units: set[str] = set()
    targets: dict[str, list[Motion]] = {}
    for motion in motions:
        if motion.unit_id in seen_units:
            raise ValidationError(f"unit {motion.unit_id} moved more than once")
        seen_units.add(motion.unit_id)
        unit = world.units.get(motion.unit_id)
        if unit is None:
            raise ValidationError(f"unknown unit: {motion.unit_id}")
        if unit.tile_id != motion.from_tile_id:
            raise ValidationError(f"unit {motion.unit_id} is not on {motion.from_tile_id}")
        if motion.from_tile_id == motion.to_tile_id:
            raise ValidationError("move must change tiles")
        if motion.to_tile_id not in world.tiles:
            raise ValidationError(f"unknown target tile: {motion.to_tile_id}")
        from_tile = world.tiles[motion.from_tile_id]
        to_tile = world.tiles[motion.to_tile_id]
        if (to_tile.q, to_tile.r) not in axial_neighbors(from_tile.q, from_tile.r):
            raise ValidationError(f"non-adjacent move: {motion.from_tile_id}->{motion.to_tile_id}")
        targets.setdefault(motion.to_tile_id, []).append(motion)

    wars: list[WarSpec] = []
    candidates: list[Motion] = []
    occupied_targets = {
        motion.to_tile_id
        for motion in motions
        if _unit_on_tile(world, motion.to_tile_id) is not None
    }
    for motion in sorted(motions, key=lambda item: item.unit_id):
        if motion.to_tile_id in occupied_targets:
            wars.append(WarSpec(motion.unit_id, motion.to_tile_id, "occupied", "defender_holds"))
        else:
            candidates.append(motion)

    survivors: list[Motion] = []
    by_target: dict[str, list[Motion]] = {}
    for motion in candidates:
        by_target.setdefault(motion.to_tile_id, []).append(motion)
    for target, group in sorted(by_target.items()):
        if len(group) == 1:
            survivors.append(group[0])
            continue
        winner = min(group, key=lambda item: item.unit_id)
        for motion in sorted(group, key=lambda item: item.unit_id):
            outcome = "priority_win" if motion.unit_id == winner.unit_id else "priority_loss"
            wars.append(WarSpec(motion.unit_id, target, "dual_target", outcome))
        survivors.append(winner)
    return (
        sorted(survivors, key=lambda item: item.unit_id),
        sorted(wars, key=lambda item: (item.unit_id, item.to_tile_id)),
    )


def apply_motions(world: World, motions: Sequence[Motion]) -> list[WarSpec]:
    """Validate against the pre-turn world, resolve War, then mutate atomically."""
    survivors, wars = _resolve_war(world, motions)
    for motion in survivors:
        current = world.units[motion.unit_id]
        world.units[motion.unit_id] = Unit(
            unit_id=current.unit_id,
            tile_id=motion.to_tile_id,
            label=current.label,
        )
    return wars


class TurnController:
    """Open, resolve, and close a turn against one world and event log."""

    def __init__(self, world: World, log: EventLog) -> None:
        self.world = world
        self.log = log
        self._open = False

    def begin_turn(self) -> Event:
        if self._open:
            raise ValidationError("turn is already open")
        self.world.validate()
        self._open = True
        return self.log.append(KIND_TURN_BEGIN, self.world.turn, {"turn": self.world.turn})

    def resolve(self, plans: Sequence[Plan | Mapping[str, Any]]) -> list[Event]:
        if not self._open:
            raise ValidationError("turn is not open")
        normalized = [
            plan if isinstance(plan, Plan) else plan_from_mapping(plan)
            for plan in plans
        ]
        motions = motions_from_plans(self.world, normalized)
        wars = apply_motions(self.world, motions)
        events = [
            self.log.append(KIND_MOVE, self.world.turn, motion.event_data())
            for motion in sorted(motions, key=lambda item: item.unit_id)
        ]
        events.extend(self.log.append(KIND_WAR, self.world.turn, war.event_data()) for war in wars)
        return events

    def end_turn(self) -> Event:
        if not self._open:
            raise ValidationError("turn is not open")
        self.world.validate()
        event = self.log.append(
            KIND_TURN_END,
            self.world.turn,
            {"turn": self.world.turn, "state_digest": self.world.digest()},
        )
        self.world.turn += 1
        self._open = False
        return event
