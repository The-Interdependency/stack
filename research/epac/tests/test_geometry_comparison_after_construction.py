from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

EPAC_ROOT = Path(__file__).resolve().parents[1]
STACK_ROOT = EPAC_ROOT.parents[1]
sys.path.insert(0, str(EPAC_ROOT))
sys.path.insert(0, str(STACK_ROOT / "research" / "edcm"))
sys.path.insert(0, str(STACK_ROOT / "research" / "ucns" / "src"))

from epac_molecular import construct_declared_molecules, matched_information_control


SEALED = EPAC_ROOT / "data" / "sealed_known_molecular_geometry.json"


class GeometryComparisonAfterConstructionTest(unittest.TestCase):
    def test_ucns_coupling_does_not_predict_sealed_shapes(self) -> None:
        constructions = construct_declared_molecules()
        sealed = json.loads(SEALED.read_text(encoding="utf-8"))["molecules"]

        ucns_signatures = {
            formula: item.invariants["ucns_coupling_signature"]
            for formula, item in constructions.items()
        }
        controls = {
            formula: matched_information_control(item.invariants)
            for formula, item in constructions.items()
        }
        known_shapes = {formula: sealed[formula]["known_shape"] for formula in constructions}

        # Construction finished. Comparison opens sealed labels only now.
        distinct_shapes = set(known_shapes.values())
        distinct_ucns = set(ucns_signatures.values())
        distinct_controls = set(controls.values())

        water_co2_same_ucns = ucns_signatures["H2O"] == ucns_signatures["CO2"]
        water_co2_same_shape = known_shapes["H2O"] == known_shapes["CO2"]
        water_co2_same_control = controls["H2O"] == controls["CO2"]

        self.assertGreater(len(distinct_shapes), 1)
        self.assertEqual(len(distinct_ucns), 1)
        self.assertTrue(water_co2_same_ucns)
        self.assertFalse(water_co2_same_shape)
        self.assertFalse(water_co2_same_control)
        self.assertGreater(len(distinct_controls), 1)

        standing = (
            "FALSIFIED-as-prediction"
            if len(distinct_ucns) == 1 and len(distinct_shapes) > 1
            else "UNRESOLVED"
        )
        self.assertEqual(standing, "FALSIFIED-as-prediction")
        self.assertEqual(len(distinct_controls), len(constructions))


if __name__ == "__main__":
    unittest.main()
