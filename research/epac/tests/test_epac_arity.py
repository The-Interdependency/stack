from __future__ import annotations

import sys
import unittest
from pathlib import Path

EPAC_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EPAC_ROOT))

from epac_dimensional_arity import (
    DimensionalArityError,
    coupling,
    geometry_from_declared_couplings,
    has_declared_coupling,
    observed_shared_ids,
    space,
)


class DimensionalArityTest(unittest.TestCase):
    def test_unary_in_one_ambient_dimension(self) -> None:
        declared = space(["x"], [["x"]])
        geometry = geometry_from_declared_couplings(declared)
        self.assertEqual(geometry["ambient_count"], 1)
        self.assertEqual(geometry["couplings"], ({"declared_ids": ("x",), "arity": 1},))

    def test_binary_in_two_ambient_dimensions(self) -> None:
        declared = space(["x", "y"], [["x", "y"]])
        self.assertEqual(declared.couplings[0].arity, 2)

    def test_ternary_only_when_declared(self) -> None:
        declared = space(["x", "y", "z"], [["x", "y", "z"]])
        self.assertEqual(declared.couplings[0].arity, 3)

    def test_two_binaries_in_three_dimensions_do_not_create_xy_or_xyz(self) -> None:
        declared = space(["x", "y", "z"], [["z", "x"], ["z", "y"]])
        geometry = geometry_from_declared_couplings(declared)
        self.assertEqual(len(declared.ambient_dimensions), 3)
        self.assertEqual(tuple(item.arity for item in declared.couplings), (2, 2))
        self.assertTrue(has_declared_coupling(declared, ["z", "x"]))
        self.assertTrue(has_declared_coupling(declared, ["z", "y"]))
        self.assertFalse(has_declared_coupling(declared, ["x", "y"]))
        self.assertFalse(has_declared_coupling(declared, ["x", "y", "z"]))
        self.assertFalse(has_declared_coupling(declared, ["z", "x", "y"]))
        shares = geometry["observed_shares"]
        self.assertEqual(len(shares), 1)
        self.assertEqual(shares[0]["shared_ids"], ("z",))
        self.assertFalse(shares[0]["creates_higher_arity_coupling"])
        self.assertFalse(geometry["inferred_from_ambient"])
        self.assertFalse(geometry["inferred_higher_arity_from_overlap"])

    def test_ambient_size_does_not_infer_couplings(self) -> None:
        declared = space(["d1", "d2", "d3", "d4", "d5"], [])
        geometry = geometry_from_declared_couplings(declared)
        self.assertEqual(geometry["ambient_count"], 5)
        self.assertEqual(geometry["couplings"], ())

    def test_arity_five_in_seven_dimensions(self) -> None:
        ambient = [f"d{i}" for i in range(1, 8)]
        declared = space(ambient, [["d1", "d2", "d3", "d4", "d5"]])
        self.assertEqual(declared.couplings[0].arity, 5)
        self.assertEqual(len(declared.ambient_dimensions), 7)

    def test_mixed_arities_in_one_ambient_space(self) -> None:
        declared = space(
            ["d1", "d2", "d3", "d4"],
            [["d1"], ["d2", "d3"], ["d1", "d2", "d3", "d4"]],
        )
        self.assertEqual(tuple(item.arity for item in declared.couplings), (1, 2, 4))

    def test_coupling_must_be_subset_of_ambient(self) -> None:
        with self.assertRaisesRegex(DimensionalArityError, "undeclared dimensions"):
            space(["d1"], [["d1", "d2"]])

    def test_coupling_cannot_repeat_a_dimension(self) -> None:
        with self.assertRaisesRegex(DimensionalArityError, "cannot repeat"):
            coupling(["d1", "d1"])

    def test_declaration_sequence_is_preserved_without_order_semantics(self) -> None:
        declared = space(["x", "z"], [["z", "x"], ["x", "z"]])
        self.assertEqual(declared.couplings[0].declared_ids, ("z", "x"))
        self.assertEqual(declared.couplings[1].declared_ids, ("x", "z"))
        self.assertNotEqual(declared.couplings[0].declared_ids, declared.couplings[1].declared_ids)
        self.assertEqual(declared.couplings[0].member_ids, declared.couplings[1].member_ids)
        geometry = geometry_from_declared_couplings(declared)
        self.assertEqual(geometry["order_identity"], "hmmm")

    def test_overlap_observation_is_not_a_coupling(self) -> None:
        zx = coupling(["z", "x"])
        zy = coupling(["z", "y"])
        self.assertEqual(observed_shared_ids(zx, zy), frozenset({"z"}))
        self.assertEqual(zx.arity, 2)
        self.assertEqual(zy.arity, 2)


if __name__ == "__main__":
    unittest.main()
