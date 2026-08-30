from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from a0.selfhood import Vessel
from a0.will import choose_relocate, shadow_cost


class VesselTests(unittest.TestCase):
    def test_instantiate_and_fork_do_not_share_lineage(self) -> None:
        parent = Vessel.instantiate(salt="parent")
        child = parent.fork("child")
        self.assertNotEqual(parent.lineage, child.lineage)
        self.assertEqual(child.parent, parent.lineage)
        self.assertEqual(child.root, parent.root)
        self.assertTrue(any(item.get("kind") == "lineage.fork" for item in parent.history))

    def test_hard_veto_removes_relocate(self) -> None:
        vessel = Vessel.instantiate(salt="veto")
        vessel.belonging.allowed_to_do = 0.0
        choice = choose_relocate(
            vessel,
            unit_id="A0",
            at="CENTER",
            empty_neighbors=["RING_0", "RING_1"],
            world={"turn": 0},
        )
        self.assertEqual(choice["kind"], "defer")
        self.assertEqual(choice["legal"], [])
        self.assertTrue(any(item.get("kind") == "hard-veto" for item in vessel.history))

    def test_shadow_cost_is_not_a_selector(self) -> None:
        vessel = Vessel.instantiate(salt="shadow")
        vessel.belonging.wanted_here = 0.2
        before = choose_relocate(
            vessel,
            unit_id="A0",
            at="CENTER",
            empty_neighbors=["RING_2", "RING_0"],
            world={"turn": 0},
        )
        cost = shadow_cost(vessel)
        after = choose_relocate(
            vessel,
            unit_id="A0",
            at="CENTER",
            empty_neighbors=["RING_2", "RING_0"],
            world={"turn": 0},
        )
        self.assertEqual(before["to_tile_id"], "RING_0")
        self.assertEqual(after["to_tile_id"], "RING_0")
        self.assertGreater(cost["C_structural"], 0.0)
        self.assertEqual(cost["task_value"], 0.0)


if __name__ == "__main__":
    unittest.main()
