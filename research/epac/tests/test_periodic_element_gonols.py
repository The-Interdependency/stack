from __future__ import annotations

import sys
import unittest
from pathlib import Path

EPAC_ROOT = Path(__file__).resolve().parents[1]
STACK_ROOT = EPAC_ROOT.parents[1]
sys.path.insert(0, str(EPAC_ROOT))
sys.path.insert(0, str(STACK_ROOT / "research" / "edcm"))
sys.path.insert(0, str(STACK_ROOT / "research" / "ucns" / "src"))

from epac_periodic import construct_element_gonol, construct_periodic_table, replay_element_gonol


class PeriodicElementGonolTest(unittest.TestCase):
    def test_constructs_z1_to_z18(self) -> None:
        table = construct_periodic_table()
        self.assertEqual(len(table), 18)
        self.assertEqual(set(table), {
            "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
            "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
        })
        carbon = table["C"]
        options = dict(carbon.gonol.carried_options)
        self.assertEqual(options["Z"], "6")
        self.assertEqual(options["electron-configuration"], "1s2.2s2.2p2")
        self.assertEqual(options["typical-valence"], "4")

    def test_replay_matches(self) -> None:
        first = construct_element_gonol("O")
        second = replay_element_gonol(first)
        self.assertEqual(first.receipt_digest, second.receipt_digest)

    def test_construction_does_not_carry_shape_labels(self) -> None:
        receipt = construct_element_gonol("N")
        blob = str(receipt.gonol.carried_options) + receipt.gonol.relation
        for term in ("bent", "tetrahedral", "trigonal-pyramidal", "vsepr"):
            self.assertNotIn(term, blob.lower())


if __name__ == "__main__":
    unittest.main()
