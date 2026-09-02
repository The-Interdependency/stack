"""Bind AHBG construct to the UCNS construction state.

UCNS now supplies the authoritative build state for the seven-band Mobius
Seed of Life (``ucns.mobius_seed_construction``). AHBG maps that state onto
its UCNS-derived tiles by ``ucns_slot`` and persists it beside the engine
field. This module adds no geometry: buildable-next is read from UCNS
structural-vesica relations only.

Usage guidance:
    The runtime constructs the ledger automatically inside ``run_plane`` and
    the HTTP bridge. Direct use is also supported::

        ledger = ConstructionLedger.open(field)
        for tile_id in ledger.legal_build_tiles(field):
            ledger, event = ledger.apply_build(field, tile_id, unit_id="A0")
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

_UCNS = Path(__file__).resolve().parents[2] / "libs" / "ucns" / "src"
if str(_UCNS) not in sys.path:
    sys.path.insert(0, str(_UCNS))

from ucns.mobius_seed_construction import (  # noqa: E402
    ConstructionState,
    buildable_slots,
    construct,
    from_built,
    initial_construction_state,
)

LEDGER_SCHEMA = "interdependency.ahbg.construction-ledger/1"


class ConstructionError(ValueError):
    """A construct intent violates the UCNS construction boundary."""


def _slot_for_tile(field: Any, tile_id: str) -> str:
    for tile in field.snapshot()["tiles"]:
        if tile["tile_id"] == tile_id:
            return str(tile.get("ucns_slot") or tile["tile_id"])
    raise ConstructionError(f"unknown tile {tile_id}")


def _tile_for_slot(field: Any, slot: str) -> str:
    for tile in field.snapshot()["tiles"]:
        if str(tile.get("ucns_slot") or tile["tile_id"]) == slot:
            return str(tile["tile_id"])
    raise ConstructionError(f"no tile for UCNS slot {slot}")


@dataclass(frozen=True)
class ConstructionLedger:
    state: ConstructionState

    @classmethod
    def open(cls, field: Any) -> "ConstructionLedger":
        return cls(initial_construction_state())

    @classmethod
    def load(cls, field: Any, directory: Path) -> "ConstructionLedger":
        path = directory / "construction.json"
        if not path.exists():
            return cls.open(field)
        raw = json.loads(path.read_text(encoding="utf-8"))
        if raw.get("schema") != LEDGER_SCHEMA:
            raise ConstructionError("unknown construction ledger schema")
        built = [str(slot) for slot in raw.get("built", [])]
        from ucns.mobius_seed import BandSlot

        slots = [BandSlot(slot) for slot in built if slot in {item.value for item in BandSlot}]
        return cls(from_built(slots))

    def dump(self, directory: Path) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "construction.json").write_text(
            json.dumps(
                {
                    "schema": LEDGER_SCHEMA,
                    "built": [slot.value for slot in sorted(self.state.built, key=lambda item: item.value)],
                    "buildable": [slot.value for slot in buildable_slots(self.state)],
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

    def legal_build_tiles(self, field: Any) -> tuple[str, ...]:
        slots = buildable_slots(self.state)
        return tuple(_tile_for_slot(field, slot.value) for slot in slots)

    def apply_build(
        self,
        field: Any,
        *,
        unit_id: str,
        from_tile_id: str,
        to_tile_id: str,
    ) -> tuple["ConstructionLedger", dict[str, Any]]:
        unit = field.occupants.get(unit_id)
        if unit is None or unit.tile_id != from_tile_id:
            raise ConstructionError(f"{unit_id} is not on {from_tile_id}")
        slot = _slot_for_tile(field, to_tile_id)
        from ucns.mobius_seed import BandSlot

        band = BandSlot(slot)
        try:
            next_state = construct(self.state, band)
        except Exception as exc:
            raise ConstructionError(f"construct {slot} violates UCNS construction boundary: {exc}") from exc
        event = {
            "kind": "construct",
            "unit_id": unit_id,
            "from_tile_id": from_tile_id,
            "to_tile_id": to_tile_id,
            "ucns_slot": slot,
            "built_count": len(next_state.built),
        }
        return ConstructionLedger(next_state), event

    def as_dict(self) -> Mapping[str, Any]:
        return {
            "schema": LEDGER_SCHEMA,
            "built": [slot.value for slot in sorted(self.state.built, key=lambda item: item.value)],
            "buildable": [slot.value for slot in buildable_slots(self.state)],
        }
