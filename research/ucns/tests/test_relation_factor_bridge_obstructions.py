"""Executable witnesses for the relation-to-factor bridge obstruction audit."""

# === CHECKS ===
# id: check_relation_factor_bridge_profiles_free_homology
#   proves: relation_factor_bridge_profiles_free_homology
#   call: self::test_return_relation_modules_are_free_and_infinite
#   mutates: none
#   cleanup: none
#
# id: check_relation_factor_bridge_falsifies_stable_generator_products
#   proves: relation_factor_bridge_falsifies_stable_generator_products
#   call: self::test_stable_generator_prime_products_fail_nesting
#   mutates: none
#   cleanup: none
#
# id: check_relation_factor_bridge_falsifies_local_trace_maps
#   proves: relation_factor_bridge_falsifies_local_trace_maps
#   call: self::test_identical_local_trace_map_fails_squarefree_rank_two
#   mutates: none
#   cleanup: none
#
# id: check_relation_factor_bridge_rejects_nongeometric_addresses
#   proves: relation_factor_bridge_rejects_nongeometric_addresses
#   call: self::test_hash_and_scale_prime_selectors_are_rejected
#   mutates: none
#   cleanup: none
#
# id: check_relation_factor_bridge_defines_presentation_readout
#   proves: relation_factor_bridge_defines_presentation_readout
#   call: self::test_generic_integer_presentation_readout_is_exact_and_target_free
#   mutates: none
#   cleanup: none
#
# id: check_relation_factor_bridge_keeps_global_matrix_unresolved
#   proves: relation_factor_bridge_keeps_global_matrix_unresolved
#   call: self::test_global_geometric_presentation_remains_missing
#   mutates: none
#   cleanup: none
#
# id: check_relation_factor_bridge_receipt_replays
#   proves: relation_factor_bridge_receipt_replays
#   call: self::test_receipt_replays_byte_identically
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from hashlib import sha256
import inspect
import json
from pathlib import Path
import sys
import unittest


UCNS_RESEARCH_ROOT = Path(__file__).resolve().parents[1]
COMMITTED_RECEIPT = UCNS_RESEARCH_ROOT / "receipts" / "relation-factor-bridge-obstructions-v0.json"
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import relation_factor_bridge_obstructions as m


class RelationFactorBridgeObstructionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = m.audit()
        cls.by_class = {item.bridge_class: item for item in cls.result.bridge_classes}

    def test_return_relation_modules_are_free_and_infinite(self) -> None:
        profiles = self.result.homology_profiles
        self.assertEqual(tuple(item.relation_rank for item in profiles), (1, 2, 3, 4))
        self.assertEqual(tuple(item.free_rank for item in profiles), (1, 2, 3, 4))
        self.assertTrue(all(item.torsion_invariants == () for item in profiles))
        self.assertTrue(all(item.finite_order is None for item in profiles))
        self.assertEqual(len({item.local_trace_sha256 for item in profiles}), 1)
        free_class = self.by_class["current free-homology cardinality"]
        self.assertEqual(free_class.status, m.STATUS_FALSIFIED)
        self.assertIn("infinite cardinality", free_class.conclusion)

    def test_stable_generator_prime_products_fail_nesting(self) -> None:
        stable = self.by_class["stable persistent-generator prime product"]
        self.assertEqual(stable.status, m.STATUS_FALSIFIED)
        self.assertTrue(stable.evidence["relation_basis_nested"])
        self.assertEqual(stable.evidence["adjacent_divisibility"], [False, False])
        self.assertEqual(stable.evidence["nested_factor_sets"], [False, False])
        self.assertEqual(stable.evidence["pairwise_gcds"], [1, 1, 1])
        self.assertEqual(
            self.result.observed_factor_sets,
            ((157,), (43, 67), (3, 11, 1661748437)),
        )
        profiles = self.result.homology_profiles
        for earlier, later in zip(profiles[:-1], profiles[1:], strict=True):
            self.assertEqual(earlier.relation_ids, later.relation_ids[:-1])

    def test_identical_local_trace_map_fails_squarefree_rank_two(self) -> None:
        local = self.by_class["local complete-return trace isomorphism map"]
        self.assertEqual(local.status, m.STATUS_FALSIFIED)
        self.assertTrue(local.evidence["all_local_traces_identical"])
        self.assertTrue(local.evidence["rank_two_observation_squarefree"])
        self.assertEqual(local.evidence["repeated_local_factor_product_at_rank_two"], "p^2")
        self.assertIn("cannot equal a squarefree", local.conclusion)

    def test_hash_and_scale_prime_selectors_are_rejected(self) -> None:
        rejected = self.by_class["generator hash, id, or scale-address prime selection"]
        self.assertEqual(rejected.status, m.STATUS_REJECTED)
        self.assertTrue(rejected.evidence["generator_ids_are_sha256_addresses"])
        self.assertTrue(rejected.evidence["scale_indices_are_external_addresses"])
        self.assertFalse(rejected.evidence["geometric_measurement_defined"])
        payload = m.receipt_payload()
        prime_boundary = payload["source"]["ucns_prime_primitives"]["direction_boundary"]
        self.assertIn("selected arithmetic prime labels", prime_boundary)
        self.assertIn("does not invert", prime_boundary)

    def test_generic_integer_presentation_readout_is_exact_and_target_free(self) -> None:
        matrix = ((2, 1), (1, 4))
        provenance = (
            ("synthetic.geometry.entry-00", "synthetic.geometry.entry-01"),
            ("synthetic.geometry.entry-10", "synthetic.geometry.entry-11"),
        )
        readout = m.evaluate_integer_presentation(matrix, provenance)
        self.assertEqual(readout.determinant, 7)
        self.assertTrue(readout.finite_cokernel)
        self.assertEqual(readout.finite_order, 7)
        self.assertEqual(readout.factorization, ((7, 1),))

        singular = m.evaluate_integer_presentation(
            ((-1, 1), (1, -1)),
            provenance,
        )
        self.assertEqual(singular.determinant, 0)
        self.assertFalse(singular.finite_cokernel)
        self.assertIsNone(singular.finite_order)
        self.assertEqual(singular.factorization, ())

        source = inspect.getsource(m.evaluate_integer_presentation)
        for prohibited in ("157", "2881", "54837698421", "43", "67", "1661748437"):
            self.assertNotIn(prohibited, source)
        with self.assertRaises(m.RelationFactorBridgeError):
            m.evaluate_integer_presentation(((1, 2),), (("only",),))
        with self.assertRaises(m.RelationFactorBridgeError):
            m.evaluate_integer_presentation(((1,),), (("",),))

    def test_global_geometric_presentation_remains_missing(self) -> None:
        global_class = self.by_class["global geometry-derived integer presentation"]
        self.assertEqual(global_class.status, m.STATUS_BLOCKED)
        self.assertIsNone(global_class.evidence["complete_return_pairing_matrix"])
        self.assertIsNone(global_class.evidence["complete_return_degree_two_boundary"])
        self.assertIsNone(global_class.evidence["complete_return_monodromy_matrix"])
        self.assertTrue(global_class.evidence["finite_presentation_readout_implemented"])
        self.assertEqual(self.result.status, m.CURRENT_BRIDGE_STATUS)
        self.assertIsNone(self.result.current_geometric_presentation)
        self.assertIsNone(self.result.current_factor_cardinalities)
        self.assertIsNone(self.result.numerical_next_gonol)

    def test_receipt_replays_byte_identically(self) -> None:
        first = m.receipt_bytes()
        second = m.receipt_bytes()
        self.assertEqual(first, second)
        self.assertEqual(m.receipt_digest(), sha256(first).hexdigest())
        payload = json.loads(first)
        self.assertEqual(payload["audit"]["status"], m.CURRENT_BRIDGE_STATUS)
        self.assertIsNone(payload["audit"]["remaining_admissible_class"]["current_geometric_presentation"])
        self.assertIsNone(payload["audit"]["numerical_next_gonol"])

        committed = json.loads(COMMITTED_RECEIPT.read_text(encoding="utf-8"))
        committed_digest = committed.pop("receipt_sha256")
        self.assertEqual(committed_digest, m.receipt_digest())
        self.assertEqual(committed, payload)


if __name__ == "__main__":
    unittest.main()
