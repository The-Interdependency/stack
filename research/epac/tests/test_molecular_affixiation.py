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
            self.assertEqual(construction.receipt.gonol.participants[0].scale, "word")

    def test_valence_occupancy_from_inputs_only(self) -> None:
        molecules = construct_declared_molecules()
        self.assertEqual(molecules["H2"].invariants["center_symbol"], None)
        self.assertEqual(molecules["H2O"].invariants["center_symbol"], "O")
        self.assertEqual(molecules["H2O"].invariants["slot_occupancy"], [1, 1])
        self.assertEqual(molecules["NH3"].invariants["slot_occupancy"], [1, 1, 1])
        self.assertEqual(molecules["CH4"].invariants["slot_occupancy"], [1, 1, 1, 1])
        self.assertEqual(molecules["CO2"].invariants["slot_occupancy"], [2, 2])

    def test_ucns_coupling_is_the_same_mobius_loop(self) -> None:
        molecules = construct_declared_molecules()
        signatures = {formula: item.invariants["ucns_coupling_signature"] for formula, item in molecules.items()}
        unique = set(signatures.values())
        self.assertEqual(len(unique), 1)
        law, turns, _frames, restored = next(iter(unique))
        self.assertEqual(law, "ucns.native-mobius-root-loop")
        self.assertEqual(turns, (0, 1, 2))
        self.assertTrue(restored)

    def test_construction_text_avoids_sealed_labels(self) -> None:
        source = (EPAC_ROOT / "epac_molecular.py").read_text(encoding="utf-8").lower()
        for term in ("bent", "tetrahedral", "trigonal-pyramidal", "vsepr"):
            self.assertNotIn(term, source)


if __name__ == "__main__":
    unittest.main()
