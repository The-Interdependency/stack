from __future__ import annotations

import sys
import unittest
from pathlib import Path

EPAC_ROOT = Path(__file__).resolve().parents[1]
STACK_ROOT = EPAC_ROOT.parents[1]
sys.path.insert(0, str(EPAC_ROOT))
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
        self.assertEqual(options["valence-electrons"], "4")
        self.assertEqual(options["unpaired-valence-count"], "2")
        self.assertEqual(options["promoted-unpaired-count"], "4")
        self.assertEqual(carbon.constructor_id, "epac.public_gonol")
        self.assertEqual(len(carbon.gonol.participants), 3)
        shells = [item for item in carbon.gonol.participants if item.relation == "epac.atomic.shell"]
        electrons = [e for shell in shells for e in shell.participants]
        self.assertEqual(len(electrons), 6)
        quantum = {(dict(e.carried_options)["n"], dict(e.carried_options)["l"], dict(e.carried_options)["m_l"], dict(e.carried_options)["m_s"]) for e in electrons}
        self.assertEqual(len(quantum), 6)
        oxygen = table["O"]
        self.assertEqual(dict(oxygen.gonol.carried_options)["unpaired-valence-lm"], "1:0,1:-1")

    def test_replay_matches(self) -> None:
        first = construct_element_gonol("O")
        second = replay_element_gonol(first)
        self.assertEqual(first.receipt_digest, second.receipt_digest)

    def test_hund_unpaired_and_shells(self) -> None:
        from epac_atomic import atomic_record

        carbon = atomic_record(6)
        oxygen = atomic_record(8)
        nitrogen = atomic_record(7)
        self.assertEqual(len(carbon.electrons), 6)
        self.assertEqual(tuple((e.l, e.m_l) for e in carbon.unpaired_valence), ((1, 1), (1, 0)))
        self.assertEqual(len(carbon.promoted_unpaired_valence), 4)
        self.assertEqual(tuple((e.l, e.m_l) for e in oxygen.unpaired_valence), ((1, 0), (1, -1)))
        self.assertEqual(len(nitrogen.unpaired_valence), 3)
        self.assertEqual({e.m_l for e in nitrogen.unpaired_valence}, {1, 0, -1})

    def test_construction_does_not_carry_shape_labels(self) -> None:
        receipt = construct_element_gonol("N")
        blob = str(receipt.gonol.carried_options) + receipt.gonol.relation
        for term in ("bent", "tetrahedral", "trigonal-pyramidal", "vsepr"):
            self.assertNotIn(term, blob.lower())


if __name__ == "__main__":
    unittest.main()
