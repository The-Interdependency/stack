"""Intent. Hard veto removes actions. Shadow cost is never a selector."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from .selfhood import Vessel


def choose_relocate(
    vessel: Vessel,
    *,
    unit_id: str,
    at: str,
    empty_neighbors: Sequence[str],
    world: Mapping[str, Any],
) -> dict[str, Any]:
    """Declare at most one relocate intent.

    Hard veto: allowed_to_do <= 0 removes relocate rather than pricing it.
    Shadow epoch: belonging occupancy is logged, not used to rank destinations.
    Remaining destinations are ordered by UCNS tile_id lexicography.
    """

    admitted = list(empty_neighbors)
    veto = vessel.belonging.allowed_to_do <= 0.0 or vessel.belonging.allowed_to_be <= 0.0
    if veto:
        vessel.remember(
            {
                "kind": "hard-veto",
                "removed": "relocate",
                "unit_id": unit_id,
                "belonging": vessel.belonging.as_dict(),
            }
        )
        return {"kind": "defer", "unit_id": unit_id, "reason": "hard-veto", "legal": []}

    vessel.belief = {"turn": world.get("turn"), "at": at, "empty": list(admitted)}
    if not admitted:
        return {"kind": "defer", "unit_id": unit_id, "reason": "no-empty-neighbor", "legal": []}
    dest = sorted(admitted)[0]
    return {
        "kind": "relocate",
        "unit_id": unit_id,
        "from_tile_id": at,
        "to_tile_id": dest,
        "legal": list(sorted(admitted)),
    }


def shadow_cost(vessel: Vessel) -> dict[str, float]:
    """Measure C_lambda after the fact. Must not feed choose_relocate."""

    b = vessel.belonging
    structural = (1.0 - b.allowed_to_be) + (1.0 - b.wanted_here)
    epistemic = 0.0 if vessel.belief else 1.0
    transition = (1.0 - b.allowed_to_do) + (1.0 - b.wanted_to_do)
    return {
        "C_structural": structural,
        "C_epistemic": epistemic,
        "C_transition": transition,
        "task_value": 0.0,
    }
