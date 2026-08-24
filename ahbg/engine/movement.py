"""Canonical v1 movement mechanic.

The first canonical mechanic is a one-tile axial move onto an empty adjacent
tile. Semantics are simultaneous: every move in a turn is validated against
the pre-turn plane, then all moves apply atomically.

Still unresolved (fails closed with :class:`UnresolvedHmmm`):
- moving onto an occupied tile (War collision resolver),
- two moves targeting the same tile (War collision resolver),
- any action kind other than ``move``.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from .adapter import Plan
from .errors import UnresolvedHmmm, ValidationError
from .plane import Plane

MOVE_ACTION = "move"
MOVE_DATA_KEYS = ("unit_id", "to_tile_id")
MOVE_EVENT_KEYS = ("unit_id", "from_tile_id", "to_tile_id")

_AXIAL_DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1))


def axial_neighbors(q: int, r: int) -> set[tuple[int, int]]:
    """The six axial hex tiles adjacent to ``(q, r)``."""
    return {(q + dq, r + dr) for dq, dr in _AXIAL_DIRECTIONS}


@dataclass(frozen=True)
class MoveSpec:
    """One validated move intent: a unit from one tile to an adjacent tile."""

    unit_id: str
    from_tile_id: str
    to_tile_id: str


def unit_on_tile(plane: Plane, tile_id: str) -> str | None:
    """Return the unit id occupying ``tile_id``, or ``None``."""
    for unit in plane.units.values():
        if unit.tile_id == tile_id:
            return unit.unit_id
    return None


def validate_move_spec(plane: Plane, spec: MoveSpec) -> None:
    """Fail closed unless ``spec`` is structurally legal on ``plane``."""
    unit = plane.units.get(spec.unit_id)
    if unit is None:
        raise ValidationError(f"move references unknown unit {spec.unit_id!r}")
    if unit.tile_id != spec.from_tile_id:
        raise ValidationError(
            f"unit {spec.unit_id!r} is on tile {unit.tile_id!r}, "
            f"not {spec.from_tile_id!r}"
        )
    if spec.from_tile_id == spec.to_tile_id:
        raise ValidationError("a move must change tiles")
    if spec.to_tile_id not in plane.tiles:
        raise ValidationError(f"move targets unknown tile {spec.to_tile_id!r}")
    from_tile = plane.tiles[spec.from_tile_id]
    to_tile = plane.tiles[spec.to_tile_id]
    if (to_tile.q, to_tile.r) not in axial_neighbors(from_tile.q, from_tile.r):
        raise ValidationError(
            f"move {spec.from_tile_id!r} -> {spec.to_tile_id!r} is not adjacent"
        )


def apply_moves_simultaneously(plane: Plane, specs: list[MoveSpec]) -> None:
    """Apply every move against the pre-turn plane, atomically.

    All validation happens before any mutation, so a rejected batch leaves
    the plane untouched.
    """
    for spec in specs:
        validate_move_spec(plane, spec)

    unit_ids = [spec.unit_id for spec in specs]
    if len(set(unit_ids)) != len(unit_ids):
        raise ValidationError("a unit may submit at most one move per turn")

    targets: dict[str, str] = {}
    for spec in specs:
        occupant = unit_on_tile(plane, spec.to_tile_id)
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
        unit = plane.units[spec.unit_id]
        plane.units[spec.unit_id] = replace(unit, tile_id=spec.to_tile_id)


def specs_from_plans(plane: Plane, plans: list[Plan]) -> list[MoveSpec]:
    """Build move specs from submitted plans, validating the action envelope.

    Every action must be a ``move``; anything else is an unresolved mechanic
    and fails closed.
    """
    specs: list[MoveSpec] = []
    for plan in plans:
        if plan.turn != plane.turn:
            raise ValidationError(
                f"plan turn {plan.turn} does not match plane turn {plane.turn}"
            )
        for action in plan.actions:
            if action.kind != MOVE_ACTION:
                raise UnresolvedHmmm(
                    f"action kind {action.kind!r} is not yet canonical; "
                    f"only {MOVE_ACTION!r} resolves"
                )
            data = action.data
            unknown = sorted(set(data) - set(MOVE_DATA_KEYS))
            if unknown:
                raise ValidationError(f"move action has unknown fields: {unknown}")
            unit_id = data.get("unit_id")
            to_tile_id = data.get("to_tile_id")
            if not isinstance(unit_id, str) or not unit_id:
                raise ValidationError("move action requires a non-empty unit_id")
            if not isinstance(to_tile_id, str) or not to_tile_id:
                raise ValidationError("move action requires a non-empty to_tile_id")
            unit = plane.units.get(unit_id)
            if unit is None:
                raise ValidationError(f"move references unknown unit {unit_id!r}")
            specs.append(
                MoveSpec(
                    unit_id=unit_id,
                    from_tile_id=unit.tile_id,
                    to_tile_id=to_tile_id,
                )
            )
    return specs


def move_event_data(spec: MoveSpec) -> dict[str, Any]:
    return {
        "unit_id": spec.unit_id,
        "from_tile_id": spec.from_tile_id,
        "to_tile_id": spec.to_tile_id,
    }


def spec_from_event_data(data: dict[str, Any]) -> MoveSpec:
    """Build a move spec from an event payload, failing closed on shape."""
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
