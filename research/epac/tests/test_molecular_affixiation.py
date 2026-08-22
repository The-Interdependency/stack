from __future__ import annotations

import sys
import unittest
from pathlib import Path

EPAC_ROOT = Path(__file__).resolve().parents[1]
STACK_ROOT = EPAC_ROOT.parents[1]
sys.path.insert(0, str(EPAC_ROOT))
sys.path.insert(0, str(STACK_ROOT / "research" / "edcm"))
sys.path.insert(0, str(STACK_ROOT / "research" / "ucns" / "src"))

from epac_molecular import construct_declared_molecules, replay_molecule


class MolecularAffixiationTest(unittest.TestCase):
    def test_declared_formulas_close_and_replay(self) -> None:
        molecules = construct_declared_molecules()
        self.assertEqual(set(molecules), {"H2", "H2O", "NH3", "CH4", "CO2"})
        for formula, construction in molecules.items():
            replayed = replay_molecule(construction)
            self.assertEqual(construction.receipt.receipt_digest, replayed.receipt_digest, formula)

    def test_unpaired_valence_and_shells_are_used(self) -> None:
        molecules = construct_declared_molecules()
        water = molecules["H2O"].invariants
        methane = molecules["CH4"].invariants
        carbon_dioxide = molecules["CO2"].invariants
        self.assertEqual(water["center_symbol"], "O")
        self.assertEqual(water["center_configuration"], "1s2.2s2.2p4")
        self.assertEqual(water["center_unpaired_lm"], ["1:0", "1:-1"])
        self.assertFalse(water["ligand_has_p"])
        self.assertEqual(water["center_used_atomic_promotion"], False)
        self.assertEqual(methane["center_used_atomic_promotion"], True)
        self.assertEqual(methane["center_unpaired_lm"], ["0:0", "1:-1", "1:1", "1:0"])
        self.assertTrue(carbon_dioxide["ligand_has_p"])
        self.assertEqual(carbon_dioxide["center_unpaired_lm"], ["1:1", "1:0"])

    def test_declared_couplings_are_binary_and_do_not_fill_ambient(self) -> None:
        molecules = construct_declared_molecules()
        water = molecules["H2O"].invariants["dimensional_geometry"]
        self.assertEqual(water["ambient_count"], 3)
        self.assertEqual([c["arity"] for c in water["couplings"]], [2, 2])
        ids = [c["declared_ids"] for c in water["couplings"]]
        self.assertEqual(len(ids), 2)
        self.assertTrue(all(len(item) == 2 for item in ids))
        methane = molecules["CH4"].invariants["dimensional_geometry"]
        self.assertEqual(methane["ambient_count"], 5)
        self.assertEqual([c["arity"] for c in methane["couplings"]], [2, 2, 2, 2])
        self.assertFalse(any(c["arity"] == 5 for c in methane["couplings"]))
        self.assertFalse(methane["inferred_from_ambient"])
        self.assertFalse(methane["inferred_higher_arity_from_overlap"])

    def test_ucns_coupling_is_the_same_mobius_loop(self) -> None:
        molecules = construct_declared_molecules()
        signatures = {formula: item.invariants["ucns_coupling_signature"] for formula, item in molecules.items()}
        self.assertEqual(len(set(signatures.values())), 1)

    def test_construction_text_avoids_sealed_labels(self) -> None:
        source = (EPAC_ROOT / "epac_molecular.py").read_text(encoding="utf-8").lower()
        for term in ("bent", "tetrahedral", "trigonal-pyramidal", "vsepr"):
            self.assertNotIn(term, source)


if __name__ == "__main__":
    unittest.main()
