from __future__ import annotations

import sys
import unittest
from pathlib import Path

EPAC_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EPAC_ROOT))

from epac_dimensional_arity import (
    CouplingProof,
    DimensionalArityError,
    coupling,
    degree_relations,
    geometry_from_declared_couplings,
    has_declared_coupling,
    install_proven_coupling,
    observed_common_ids,
    space,
)


class DimensionalArityTest(unittest.TestCase):
    def test_unary_in_one_ambient_dimension(self) -> None:
        declared = space(["x"], [["x"]])
        geometry = geometry_from_declared_couplings(declared)
        self.assertEqual(geometry["ambient_count"], 1)
        self.assertEqual(geometry["couplings"][0]["declared_ids"], ("x",))
        self.assertEqual(geometry["couplings"][0]["arity"], 1)
        self.assertEqual(geometry["degree_relations"][0]["degree"], 1)

    def test_zx_is_not_xz(self) -> None:
        declared = space(["x", "z"], [["z", "x"]], charges={"x": 1, "z": 8})
        self.assertTrue(has_declared_coupling(declared, ["z", "x"]))
        self.assertFalse(has_declared_coupling(declared, ["x", "z"]))
        self.assertNotEqual(coupling(["z", "x"]), coupling(["x", "z"]))
        self.assertNotEqual(declared.couplings[0].charge_state, coupling(["x", "z"], {"x": 1, "z": 8}).charge_state)
        geometry = geometry_from_declared_couplings(declared)
        self.assertFalse(geometry["zx_equals_xz"])
        self.assertEqual(geometry["couplings"][0]["slot_charges"], (8, 1))
        z_degree = next(item for item in geometry["degree_relations"] if item["dimension"] == "z")
        x_degree = next(item for item in geometry["degree_relations"] if item["dimension"] == "x")
        self.assertEqual(z_degree["slot_degrees"], ((0, 1),))
        self.assertEqual(x_degree["slot_degrees"], ((1, 1),))

    def test_xz_and_yz_do_not_give_xyz_without_proof(self) -> None:
        declared = space(["x", "y", "z"], [["x", "z"], ["y", "z"]], charges={"x": 1, "y": 1, "z": 8})
        geometry = geometry_from_declared_couplings(declared)
        self.assertEqual(tuple(item.arity for item in declared.couplings), (2, 2))
        self.assertFalse(has_declared_coupling(declared, ["x", "y", "z"]))
        self.assertFalse(has_declared_coupling(declared, ["x", "y"]))
        self.assertFalse(geometry["inferred_higher_arity_from_overlap"])
        self.assertEqual(geometry["structure"]["participating_dimension_count"], 3)
        self.assertFalse(geometry["structure"]["ternary_coupling_declared"])
        self.assertFalse(geometry["structure"]["inferred_cartesian_embedding"])
        self.assertEqual(
            geometry["structure"]["parts"],
            (
                {"coupling": ("x", "z"), "arity": 2, "charge_state": ((1, 8), 1)},
                {"coupling": ("y", "z"), "arity": 2, "charge_state": ((1, 8), 1)},
            ),
        )
        self.assertEqual(geometry["couplings"][0]["charge_state"], ((1, 8), 1))
        self.assertEqual(geometry["couplings"][1]["charge_state"], ((1, 8), 1))
        common = geometry["observed_common_ids"]
        self.assertEqual(len(common), 1)
        self.assertEqual(common[0]["common_ids"], ("z",))
        self.assertFalse(common[0]["proof_of_higher_arity"])
        degrees = {item["dimension"]: item["degree"] for item in geometry["degree_relations"]}
        self.assertEqual(degrees["z"], 2)
        self.assertEqual(degrees["x"], 1)
        self.assertEqual(degrees["y"], 1)
        z_slots = next(item for item in geometry["degree_relations"] if item["dimension"] == "z")
        self.assertEqual(z_slots["slot_degrees"], ((1, 2),))

    def test_overlap_is_not_an_installable_proof(self) -> None:
        declared = space(["x", "y", "z"], [["x", "z"], ["y", "z"]])
        with self.assertRaisesRegex(DimensionalArityError, "not a proof"):
            CouplingProof(
                conclusion=coupling(["x", "y", "z"]),
                premises=(coupling(["x", "z"]), coupling(["y", "z"])),
                rule_id="overlap-closure",
            )
        self.assertFalse(has_declared_coupling(declared, ["x", "y", "z"]))

    def test_explicit_proof_can_install_higher_arity(self) -> None:
        declared = space(["x", "y", "z"], [["x", "z"], ["y", "z"]])
        proof = CouplingProof(
            conclusion=coupling(["x", "y", "z"]),
            premises=(coupling(["x", "z"]), coupling(["y", "z"])),
            rule_id="caller-supplied-certificate",
        )
        proven = install_proven_coupling(declared, proof)
        self.assertFalse(has_declared_coupling(declared, ["x", "y", "z"]))
        self.assertTrue(has_declared_coupling(proven, ["x", "y", "z"]))
        self.assertEqual(proven.couplings[-1].arity, 3)

    def test_zx_and_zy_degree_has_z_in_slot_zero_twice(self) -> None:
        declared = space(["x", "y", "z"], [["z", "x"], ["z", "y"]])
        degrees = {item.dimension.id: item for item in degree_relations(declared)}
        self.assertEqual(degrees["z"].degree, 2)
        self.assertEqual(degrees["z"].slot_degrees, ((0, 2),))
        self.assertEqual(degrees["x"].degree, 1)
        self.assertEqual(degrees["y"].degree, 1)
        self.assertFalse(has_declared_coupling(declared, ["x", "y"]))
        self.assertFalse(has_declared_coupling(declared, ["x", "y", "z"]))

    def test_ambient_size_does_not_infer_couplings(self) -> None:
        declared = space(["d1", "d2", "d3", "d4", "d5"], [])
        geometry = geometry_from_declared_couplings(declared)
        self.assertEqual(geometry["couplings"], ())
        self.assertEqual({item["degree"] for item in geometry["degree_relations"]}, {0})

    def test_arity_five_in_seven_dimensions(self) -> None:
        ambient = [f"d{i}" for i in range(1, 8)]
        declared = space(ambient, [["d1", "d2", "d3", "d4", "d5"]])
        self.assertEqual(declared.couplings[0].arity, 5)
        degrees = degree_relations(declared)
        used = {item.dimension.id: item.degree for item in degrees if item.degree}
        unused = {item.dimension.id for item in degrees if item.degree == 0}
        self.assertEqual(set(used), {"d1", "d2", "d3", "d4", "d5"})
        self.assertEqual(unused, {"d6", "d7"})

    def test_mixed_arities_in_one_ambient_space(self) -> None:
        declared = space(
            ["d1", "d2", "d3", "d4"],
            [["d1"], ["d2", "d3"], ["d1", "d2", "d3", "d4"]],
        )
        self.assertEqual(tuple(item.arity for item in declared.couplings), (1, 2, 4))
        degrees = {item.dimension.id: item.degree for item in degree_relations(declared)}
        self.assertEqual(degrees["d1"], 2)
        self.assertEqual(degrees["d4"], 1)

    def test_coupling_must_be_subset_of_ambient(self) -> None:
        with self.assertRaisesRegex(DimensionalArityError, "undeclared dimensions"):
            space(["d1"], [["d1", "d2"]])

    def test_coupling_cannot_repeat_a_dimension(self) -> None:
        with self.assertRaisesRegex(DimensionalArityError, "cannot repeat"):
            coupling(["d1", "d1"])

    def test_common_ids_are_not_a_coupling(self) -> None:
        xz = coupling(["x", "z"])
        yz = coupling(["y", "z"])
        self.assertEqual(observed_common_ids(xz, yz), frozenset({"z"}))
        self.assertNotEqual(xz, yz)


if __name__ == "__main__":
    unittest.main()
