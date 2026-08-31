from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from ahbg.chain import KIND_PLANE_INIT, KIND_TURN_BEGIN, KIND_TURN_END, KIND_WAR, Chain
from ahbg.keep import replay
from ahbg.patch import Field, tile_from_ucns
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

    def test_occupied_target_defender_holds(self) -> None:
        tiles = tile_from_ucns()
        opened = Field.open(
            13,
            tiles,
            [
                {"unit_id": "A0", "tile_id": "CENTER"},
                {"unit_id": "B0", "tile_id": "RING_0"},
            ],
        )
        applied, war_events = opened.apply_moves([("A0", "CENTER", "RING_0")])
        self.assertEqual(applied, [])
        self.assertEqual(len(war_events), 1)
        self.assertEqual(war_events[0]["resolution"], "defender_holds")
        self.assertEqual(opened.occupants["A0"].tile_id, "CENTER")
        self.assertEqual(opened.occupants["B0"].tile_id, "RING_0")

    def test_targeted_defender_cannot_vacate_contested_origin(self) -> None:
        tiles = tile_from_ucns()
        opened = Field.open(
            14,
            tiles,
            [
                {"unit_id": "A0", "tile_id": "CENTER"},
                {"unit_id": "B0", "tile_id": "RING_0"},
            ],
        )
        b_dest = sorted(_empty(opened, "B0"))[0]
        applied, war_events = opened.apply_moves(
            [
                ("A0", "CENTER", "RING_0"),
                ("B0", "RING_0", b_dest),
            ]
        )
        self.assertEqual(applied, [])
        by_unit = {event["unit_id"]: event for event in war_events}
        self.assertEqual(by_unit["A0"]["resolution"], "defender_holds")
        self.assertEqual(by_unit["B0"]["resolution"], "defender_holds_origin")
        self.assertEqual(opened.occupants["A0"].tile_id, "CENTER")
        self.assertEqual(opened.occupants["B0"].tile_id, "RING_0")

    def test_dual_target_smallest_unit_wins_priority(self) -> None:
        tiles = tile_from_ucns()
        opened = Field.open(
            17,
            tiles,
            [
                {"unit_id": "A0", "tile_id": "CENTER"},
                {"unit_id": "B0", "tile_id": "RING_0"},
            ],
        )
        shared = sorted(set(opened.neighbors("CENTER")) & set(opened.neighbors("RING_0")))[0]
        applied, war_events = opened.apply_moves(
            [
                ("B0", "RING_0", shared),
                ("A0", "CENTER", shared),
            ]
        )
        self.assertEqual(applied, [("A0", "CENTER", shared)])
        self.assertEqual(len(war_events), 1)
        self.assertEqual(war_events[0]["unit_id"], "B0")
        self.assertEqual(war_events[0]["resolution"], "priority_loser")
        self.assertEqual(opened.occupants["A0"].tile_id, shared)
        self.assertEqual(opened.occupants["B0"].tile_id, "RING_0")

    def test_war_evidence_replays_exactly(self) -> None:
        tiles = tile_from_ucns()
        opened = Field.open(
            19,
            tiles,
            [
                {"unit_id": "A0", "tile_id": "CENTER"},
                {"unit_id": "B0", "tile_id": "RING_0"},
            ],
        )
        chain = Chain()
        chain.append(KIND_PLANE_INIT, 0, {"field": opened.snapshot()})
        cycle = Cycle(opened, chain)
        cycle.open_turn()
        cycle.resolve([("A0", "CENTER", "RING_0")])
        cycle.close_turn()
        self.assertEqual(replay(chain).snapshot(), opened.snapshot())

    def test_tampered_war_evidence_is_rejected_even_with_valid_hash_chain(self) -> None:
        tiles = tile_from_ucns()
        initial = Field.open(
            23,
            tiles,
            [
                {"unit_id": "A0", "tile_id": "CENTER"},
                {"unit_id": "B0", "tile_id": "RING_0"},
            ],
        )
        expected = Field.open(23, tiles, initial.snapshot()["units"])
        expected.apply_moves([("A0", "CENTER", "RING_0")])

        from ahbg.chain import _digest, _dump

        malicious = Chain()
        malicious.append(KIND_PLANE_INIT, 0, {"field": initial.snapshot()})
        malicious.append(KIND_TURN_BEGIN, 0, {"turn": 0})
        malicious.append(
            KIND_WAR,
            0,
            {
                "unit_id": "A0",
                "from_tile_id": "CENTER",
                "to_tile_id": "RING_0",
                "resolution": "defender_holds",
                "winner_unit_id": "A0",
            },
        )
        malicious.append(
            KIND_TURN_END,
            0,
            {"turn": 0, "state_digest": _digest(_dump(expected.snapshot()))},
        )
        malicious.verify()
        with self.assertRaisesRegex(ValueError, "war evidence mismatch"):
            replay(malicious)


def _empty(opened: Field, unit_id: str) -> list[str]:
    at = opened.occupants[unit_id].tile_id
    return [tile for tile in opened.neighbors(at) if opened.occupant_on(tile) is None]


if __name__ == "__main__":
    unittest.main()
