from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ahbg.chain import KIND_PLANE_INIT, Chain
from ahbg.keep import replay
from ahbg.patch import ClosedUnknown, Field, tile_from_ucns
from ahbg.round import Cycle


class FieldTests(unittest.TestCase):
    def test_ucns_yields_seven_named_slots(self) -> None:
        tiles = tile_from_ucns()
        ids = {item["tile_id"] for item in tiles}
        self.assertEqual(len(tiles), 7)
        self.assertIn("CENTER", ids)
        self.assertIn("RING_0", ids)

    def test_plain_relocate_replays(self) -> None:
        tiles = tile_from_ucns()
        opened = Field.open(7, tiles, [{"unit_id": "A0", "tile_id": "CENTER"}])
        chain = Chain()
        chain.append(KIND_PLANE_INIT, 0, {"field": opened.snapshot()})
        cycle = Cycle(opened, chain)
        cycle.open_turn()
        dest = sorted(_empty(opened, "A0"))[0]
        cycle.resolve([("A0", "CENTER", dest)])
        cycle.close_turn()
        self.assertEqual(opened.occupants["A0"].tile_id, dest)
        self.assertEqual(replay(chain).snapshot(), opened.snapshot())

    def test_occupied_is_closed_unknown(self) -> None:
        tiles = tile_from_ucns()
        opened = Field.open(
            13,
            tiles,
            [
                {"unit_id": "A0", "tile_id": "CENTER"},
                {"unit_id": "B0", "tile_id": "RING_0"},
            ],
        )
        with self.assertRaises(ClosedUnknown):
            opened.apply_moves([("A0", "CENTER", "RING_0")])


def _empty(opened: Field, unit_id: str) -> list[str]:
    at = opened.occupants[unit_id].tile_id
    return [tile for tile in opened.neighbors(at) if opened.occupant_on(tile) is None]


if __name__ == "__main__":
    unittest.main()
