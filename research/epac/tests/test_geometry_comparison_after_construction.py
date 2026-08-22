from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

EPAC_ROOT = Path(__file__).resolve().parents[1]
STACK_ROOT = EPAC_ROOT.parents[1]
sys.path.insert(0, str(EPAC_ROOT))
sys.path.insert(0, str(STACK_ROOT / "research" / "ucns" / "src"))

from epac_molecular import construct_declared_molecules, matched_information_control


SEALED = EPAC_ROOT / "data" / "sealed_known_molecular_geometry.json"


class GeometryComparisonAfterConstructionTest(unittest.TestCase):
    def test_what_atomic_shells_add_versus_ucns_coupling(self) -> None:
        constructions = construct_declared_molecules()
        sealed = json.loads(SEALED.read_text(encoding="utf-8"))["molecules"]
        known_shapes = {formula: sealed[formula]["known_shape"] for formula in constructions}

        ucns = {f: c.invariants["ucns_coupling_signature"] for f, c in constructions.items()}
        atomic = {f: c.invariants["atomic_coupling_signature"] for f, c in constructions.items()}
        control = {f: matched_information_control(c.invariants) for f, c in constructions.items()}

        self.assertGreater(len(set(known_shapes.values())), 1)
        self.assertEqual(len(set(ucns.values())), 1)
        self.assertNotEqual(known_shapes["H2O"], known_shapes["CO2"])
        self.assertNotEqual(control["H2O"], control["CO2"])
        self.assertNotEqual(atomic["H2O"], atomic["CO2"])
        self.assertTrue(constructions["CO2"].invariants["ligand_has_p"])
        self.assertFalse(constructions["H2O"].invariants["ligand_has_p"])

        # UCNS Möbius is identical across sealed shape classes.
        ucns_predicts_shape = len(set(ucns.values())) == len(set(known_shapes.values()))
        self.assertFalse(ucns_predicts_shape)

        # Atomic shell/unpaired-(l,m) signatures distinguish the formulas, but
        # they are functions of the atoms already named in the formula.
        atomic_equals_control = set(atomic.values()) == set(control.values())
        self.assertFalse(atomic_equals_control)
        self.assertEqual(len(set(atomic.values())), len(constructions))
        self.assertEqual(len(set(control.values())), len(constructions))


if __name__ == "__main__":
    unittest.main()
