# ratios: loc_comments=264:35 imports_exports=5:13 calls_definitions=113:24



"""DeepSeek AHBG realization — turn loop and simultaneous resolution.

The success loop from the AHBG README:

    load plane -> A0 observes -> plan phase -> subordinate decision trees ->
    simultaneous resolution -> movement/construction/tile effects/collision ->
    diary/event persistence -> next turn

This module owns the envelope and the canonical mechanics of this workspace:

- ``move`` (v1): one axial step onto an adjacent tile, resolved
  simultaneously against the pre-turn world with deterministic War collision
  events.
- ``build`` (v2, DeepCode workspace mechanic): construct one unbuilt circle
  adjacent to an already-built circle. Validated against the pre-turn built
  set, applied simultaneously with other builds.

Everything else fails closed with :class:`UnresolvedHmmm`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .events import KIND_BUILD, KIND_MOVE, KIND_TURN_BEGIN, KIND_TURN_END, KIND_WAR, Event, EventLog
from .world import Tile, Unit, World

MOVE_ACTION = "move"
BUILD_ACTION = "build"
MOVE_DATA_KEYS = ("unit_id", "to_tile_id")
MOVE_EVENT_KEYS = ("unit_id", "from_tile_id", "to_tile_id")
BUILD_DATA_KEYS = ("unit_id", "tile_id")
BUILD_EVENT_KEYS = ("unit_id", "tile_id")
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


@dataclass(frozen=True)
class BuildSpec:
    unit_id: str
    tile_id: str


def _unit_on_tile(world: World, tile_id: str) -> str | None:
    for unit in world.units.values():
        if unit.tile_id == tile_id:
            return unit.unit_id
    return None


def built_tile_ids(world: World) -> set[str]:
    return {tile_id for tile_id, tile in world.tiles.items() if tile.built}


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


def _validate_build_spec(world: World, spec: BuildSpec, built_before: set[str]) -> None:
    unit = world.units.get(spec.unit_id)
    if unit is None:
        raise ValidationError(f"build references unknown unit {spec.unit_id!r}")
    if spec.tile_id not in world.tiles:
        raise ValidationError(f"build targets unknown tile {spec.tile_id!r}")
    if spec.tile_id in built_before:
        raise ValidationError(f"build targets already-built tile {spec.tile_id!r}")
    target = world.tiles[spec.tile_id]
    adjacent = axial_neighbors(target.q, target.r)
    for built_id in built_before:
        built_tile = world.tiles[built_id]
        if (built_tile.q, built_tile.r) in adjacent:
            return
    raise ValidationError(f"build target {spec.tile_id!r} is not adjacent to any built circle")


@dataclass(frozen=True)
class WarSpec:
    unit_id: str
    to_tile_id: str
    reason: str  # "occupied" | "dual_target"
    outcome: str  # "defender_holds" | "priority_win" | "priority_loss"


def _resolve_war(specs: list[MoveSpec], world: World) -> tuple[list[MoveSpec], list[WarSpec]]:
    """Canonical deterministic War resolver.

    Occupied target: the defender holds; every mover targeting an occupied
    tile stays and records a ``defender_holds`` war event.
    Dual target on an empty tile: the lexicographically smallest unit_id
    wins priority; the others stay and record ``priority_loss``.
    """
    for spec in specs:
        _validate_move_spec(world, spec)

    unit_ids = [spec.unit_id for spec in specs]
    if len(set(unit_ids)) != len(unit_ids):
        raise ValidationError("a unit may submit at most one move per turn")

    wars: list[WarSpec] = []
    survivors: list[MoveSpec] = []

    occupied_targets = {spec.to_tile_id for spec in specs if _unit_on_tile(world, spec.to_tile_id) is not None}
    for spec in specs:
        if spec.to_tile_id in occupied_targets:
            wars.append(WarSpec(unit_id=spec.unit_id, to_tile_id=spec.to_tile_id, reason="occupied", outcome="defender_holds"))
        else:
            survivors.append(spec)

    by_target: dict[str, list[MoveSpec]] = {}
    for spec in survivors:
        by_target.setdefault(spec.to_tile_id, []).append(spec)
    survivors = []
    for tile_id, group in sorted(by_target.items()):
        if len(group) == 1:
            survivors.append(group[0])
        else:
            winner = min(group, key=lambda s: s.unit_id)
            for spec in sorted(group, key=lambda s: s.unit_id):
                if spec.unit_id == winner.unit_id:
                    survivors.append(spec)
                    wars.append(WarSpec(unit_id=spec.unit_id, to_tile_id=tile_id, reason="dual_target", outcome="priority_win"))
                else:
                    wars.append(WarSpec(unit_id=spec.unit_id, to_tile_id=tile_id, reason="dual_target", outcome="priority_loss"))
    return survivors, sorted(wars, key=lambda w: (w.unit_id, w.to_tile_id))


def _apply_moves_simultaneously(world: World, specs: list[MoveSpec]) -> list[WarSpec]:
    """Validate and apply moves, returning the War resolution events."""
    survivors, wars = _resolve_war(specs, world)
    for spec in sorted(survivors, key=lambda item: item.unit_id):
        unit = world.units[spec.unit_id]
        world.units[spec.unit_id] = Unit(unit_id=unit.unit_id, tile_id=spec.to_tile_id)
    return wars


def _apply_builds_simultaneously(world: World, specs: list[BuildSpec]) -> None:
    """Validate every build against the pre-turn built set, then apply."""
    built_before = built_tile_ids(world)
    unit_ids = [spec.unit_id for spec in specs]
    if len(set(unit_ids)) != len(unit_ids):
        raise ValidationError("a unit may submit at most one build per turn")
    for spec in specs:
        _validate_build_spec(world, spec, built_before)
    for spec in sorted(specs, key=lambda item: item.tile_id):
        tile = world.tiles[spec.tile_id]
        world.tiles[spec.tile_id] = Tile(tile_id=tile.tile_id, q=tile.q, r=tile.r, built=True, threat=tile.threat)


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
        envelopes. Moves and builds validate against the pre-turn world, then
        apply atomically. War collisions resolve canonically: occupied targets
        hold for the defender; dual targets award priority to the smallest
        unit_id. Both outcomes emit explicit ``war`` events.
        """
        move_specs, build_specs = _specs_from_plans(self.world, plans)
        survivors, wars = _resolve_war(move_specs, self.world)
        for spec in sorted(survivors, key=lambda item: item.unit_id):
            unit = self.world.units[spec.unit_id]
            self.world.units[spec.unit_id] = Unit(unit_id=unit.unit_id, tile_id=spec.to_tile_id)
        _apply_builds_simultaneously(self.world, build_specs)
        events: list[Event] = []
        # Every submitted move is recorded (intent); war events mark the losers.
        for spec in sorted(move_specs, key=lambda item: item.unit_id):
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
        for war in wars:
            events.append(
                self.log.append(
                    KIND_WAR,
                    turn=self.world.turn,
                    data={
                        "unit_id": war.unit_id,
                        "to_tile_id": war.to_tile_id,
                        "reason": war.reason,
                        "outcome": war.outcome,
                    },
                )
            )
        for spec in sorted(build_specs, key=lambda item: item.tile_id):
            events.append(
                self.log.append(
                    KIND_BUILD,
                    turn=self.world.turn,
                    data={"unit_id": spec.unit_id, "tile_id": spec.tile_id},
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


def _specs_from_plans(world: World, plans: list[dict[str, Any]]) -> tuple[list[MoveSpec], list[BuildSpec]]:
    move_specs: list[MoveSpec] = []
    build_specs: list[BuildSpec] = []
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
            if kind == MOVE_ACTION:
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
                move_specs.append(MoveSpec(unit_id=unit_id, from_tile_id=unit.tile_id, to_tile_id=to_tile_id))
            elif kind == BUILD_ACTION:
                if not isinstance(data, dict):
                    raise ValidationError("build action data must be an object")
                unknown = sorted(set(data) - set(BUILD_DATA_KEYS))
                if unknown:
                    raise ValidationError(f"build action has unknown fields: {unknown}")
                unit_id = data.get("unit_id")
                tile_id = data.get("tile_id")
                if not isinstance(unit_id, str) or not unit_id:
                    raise ValidationError("build action requires a non-empty unit_id")
                if not isinstance(tile_id, str) or not tile_id:
                    raise ValidationError("build action requires a non-empty tile_id")
                if unit_id not in world.units:
                    raise ValidationError(f"build references unknown unit {unit_id!r}")
                build_specs.append(BuildSpec(unit_id=unit_id, tile_id=tile_id))
            else:
                raise UnresolvedHmmm(
                    f"action kind {kind!r} is not yet canonical; "
                    f"only {MOVE_ACTION!r} and {BUILD_ACTION!r} resolve"
                )
    return move_specs, build_specs


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


def build_spec_from_event_data(data: dict[str, Any]) -> BuildSpec:
    unknown = sorted(set(data) - set(BUILD_EVENT_KEYS))
    if unknown:
        raise ValidationError(f"build event has unknown fields: {unknown}")
    missing = sorted(set(BUILD_EVENT_KEYS) - set(data))
    if missing:
        raise ValidationError(f"build event is missing fields: {missing}")
    return BuildSpec(unit_id=data["unit_id"], tile_id=data["tile_id"])


WAR_EVENT_KEYS = ("unit_id", "to_tile_id", "reason", "outcome")


def war_spec_from_event_data(data: dict[str, Any]) -> WarSpec:
    unknown = sorted(set(data) - set(WAR_EVENT_KEYS))
    if unknown:
        raise ValidationError(f"war event has unknown fields: {unknown}")
    missing = sorted(set(WAR_EVENT_KEYS) - set(data))
    if missing:
        raise ValidationError(f"war event is missing fields: {missing}")
    return WarSpec(
        unit_id=data["unit_id"],
        to_tile_id=data["to_tile_id"],
        reason=data["reason"],
        outcome=data["outcome"],
    )
# ratios: loc_comments=264:35 imports_exports=5:13 calls_definitions=113:24
