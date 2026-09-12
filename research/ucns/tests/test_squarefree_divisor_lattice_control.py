"""Executable witnesses for the squarefree divisor-lattice control."""

# === CHECKS ===
# id: check_squarefree_control_factors_observations_exactly
#   proves: squarefree_control_factors_observations_exactly
#   call: self::test_observed_factorizations_are_exact
#   mutates: none
#   cleanup: none
#
# id: check_squarefree_control_witnesses_boolean_divisor_lattices
#   proves: squarefree_control_witnesses_boolean_divisor_lattices
#   call: self::test_observed_divisor_lattices_are_b1_b2_b3
#   mutates: none
#   cleanup: none
#
# id: check_squarefree_control_preregisters_structure_not_number
#   proves: squarefree_control_preregisters_structure_not_number
#   call: self::test_fourth_control_freezes_invariants_without_number
#   mutates: none
#   cleanup: none
#
# id: check_squarefree_control_has_out_of_sample_falsification_gate
#   proves: squarefree_control_has_out_of_sample_falsification_gate
#   call: self::test_comparison_requires_full_invariant_tuple
#   mutates: none
#   cleanup: none
#
# id: check_squarefree_control_does_not_upgrade_arithmetic_to_ucns_mechanics
#   proves: squarefree_control_does_not_upgrade_arithmetic_to_ucns_mechanics
#   call: self::test_mechanics_audit_leaves_factor_mapping_unresolved
#   mutates: none
#   cleanup: none
#
# id: check_squarefree_control_retains_failed_local_mechanism
#   proves: squarefree_control_retains_failed_local_mechanism
#   call: self::test_receipt_retains_event_pair_failure
#   mutates: none
#   cleanup: none
#
# id: check_squarefree_control_receipt_replays
#   proves: squarefree_control_receipt_replays
#   call: self::test_receipt_replays_byte_identically
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest


UCNS_RESEARCH_ROOT = Path(__file__).resolve().parents[1]
COMMITTED_RECEIPT = UCNS_RESEARCH_ROOT / "receipts" / "squarefree-divisor-lattice-control-v0.json"
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import squarefree_divisor_lattice_control as m


class SquarefreeDivisorLatticeControlTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.witnesses = m.observed_witnesses()
        cls.control = m.structural_control()
        cls.audit = m.audit_ucns_mechanics()

    def test_observed_factorizations_are_exact(self) -> None:
        expected = (
            ((157, 1),),
            ((43, 1), (67, 1)),
            ((3, 1), (11, 1), (1661748437, 1)),
        )
        self.assertEqual(tuple(item.factorization for item in self.witnesses), expected)
        for value, witness in zip(m.OBSERVED_GONOLS, self.witnesses, strict=True):
            reconstructed = 1
            for prime, exponent in witness.factorization:
                reconstructed *= prime**exponent
            self.assertEqual(reconstructed, value)
            self.assertEqual(m.factor_integer(value), witness.factorization)

        repeated = m.analyze_integer(12)
        self.assertEqual(repeated.factorization, ((2, 2), (3, 1)))
        self.assertFalse(repeated.squarefree)
        self.assertEqual(repeated.tau, 6)
        self.assertEqual(repeated.mobius_mu, 0)
        self.assertIsNone(repeated.lattice_name)
        with self.assertRaises(m.SquarefreeControlError):
            m.factor_integer(True)
        with self.assertRaises(m.SquarefreeControlError):
            m.factor_integer(0)

    def test_observed_divisor_lattices_are_b1_b2_b3(self) -> None:
        self.assertEqual(tuple(item.squarefree for item in self.witnesses), (True, True, True))
        self.assertEqual(tuple(item.omega for item in self.witnesses), (1, 2, 3))
        self.assertEqual(tuple(item.tau for item in self.witnesses), (2, 4, 8))
        self.assertEqual(tuple(item.mobius_mu for item in self.witnesses), (-1, 1, -1))
        self.assertEqual(tuple(item.lattice_name for item in self.witnesses), ("B_1", "B_2", "B_3"))
        self.assertEqual(
            tuple(item.lattice_rank_counts for item in self.witnesses),
            (
                ((0, 1), (1, 1)),
                ((0, 1), (1, 2), (2, 1)),
                ((0, 1), (1, 3), (2, 3), (3, 1)),
            ),
        )
        for witness in self.witnesses:
            subset_divisors = tuple(sorted(row[1] for row in witness.subset_products))
            self.assertEqual(subset_divisors, witness.divisors)

    def test_fourth_control_freezes_invariants_without_number(self) -> None:
        control = self.control
        self.assertEqual(control.observation_index, 4)
        self.assertIsNone(control.numerical_value)
        self.assertTrue(control.squarefree)
        self.assertEqual(control.omega, 4)
        self.assertEqual(control.tau, 16)
        self.assertEqual(control.mobius_mu, 1)
        self.assertEqual(control.lattice_name, "B_4")
        self.assertEqual(control.standing, m.STANDING)

    def test_comparison_requires_full_invariant_tuple(self) -> None:
        synthetic_match = m.compare_actual_next(2 * 3 * 5 * 7)
        self.assertEqual(synthetic_match.status, m.STATUS_SURVIVED_ONE)
        self.assertEqual(synthetic_match.mismatches, ())
        self.assertIn("does not validate a gonol constructor", synthetic_match.to_payload()["claim_boundary"])

        synthetic_failure = m.compare_actual_next(2 * 3 * 5)
        self.assertEqual(synthetic_failure.status, m.STATUS_FALSIFIED)
        self.assertIn("omega", synthetic_failure.mismatches)
        self.assertIn("tau", synthetic_failure.mismatches)
        self.assertIn("mobius_mu", synthetic_failure.mismatches)
        self.assertIn("divisor_lattice", synthetic_failure.mismatches)

    def test_mechanics_audit_leaves_factor_mapping_unresolved(self) -> None:
        audit = self.audit
        self.assertEqual(audit.public_gonol_arity, 157)
        self.assertEqual(audit.mechanic1_identity_output_arity, 157)
        self.assertEqual(audit.mechanic1_cyclic_output_arity, 157)
        self.assertTrue(audit.mechanic1_preserves_fixed_carrier)
        self.assertEqual(audit.mechanic2_sample_coupling_arity, 2)
        self.assertEqual(audit.mechanic2_explicit_three_participant_arity, 3)
        self.assertEqual(audit.mechanic3_promoted_atomic_participants, 1)
        self.assertIsNone(audit.mechanic3_next_carrier_cardinality)
        self.assertEqual(audit.composed_first_output, 629)
        self.assertEqual(audit.composed_status, m.composed.STATUS_FALSIFIED)
        self.assertFalse(audit.declared_product_decomposition_operation)
        self.assertFalse(audit.declared_arithmetic_factor_to_geometry_operation)
        self.assertFalse(audit.declared_add_one_prime_dimension_transition)
        self.assertEqual(audit.explanation_status, m.MECHANICS_STATUS)

    def test_receipt_retains_event_pair_failure(self) -> None:
        retained = m.receipt_payload()["retained_falsified_local_mechanism"]
        self.assertEqual(retained["first_local_state"], 39)
        self.assertEqual(retained["first_relation_constraint_rank"], 21)
        self.assertEqual(retained["first_output_state"], 720)
        self.assertEqual(retained["first_lifted_gonol"], 2881)
        self.assertEqual(retained["unchanged_second_output_state"], 258819)
        self.assertEqual(retained["unchanged_second_lifted_gonol"], 1035277)
        self.assertEqual(retained["status"], m.event_pair.STATUS_FALSIFIED)

    def test_receipt_replays_byte_identically(self) -> None:
        first = m.receipt_bytes()
        second = m.receipt_bytes()
        self.assertEqual(first, second)
        self.assertEqual(m.receipt_digest(), sha256(first).hexdigest())
        payload = json.loads(first)
        self.assertEqual(payload["comparison"]["status"], m.STATUS_PENDING)
        self.assertIsNone(payload["comparison"]["actual_fourth_value"])
        self.assertIsNone(payload["structural_control"]["numerical_value"])
        self.assertEqual(payload["mechanics_audit"]["explanation_status"], m.MECHANICS_STATUS)

        committed = json.loads(COMMITTED_RECEIPT.read_text(encoding="utf-8"))
        committed_digest = committed.pop("receipt_sha256")
        self.assertEqual(committed_digest, m.receipt_digest())
        self.assertEqual(committed, payload)


if __name__ == "__main__":
    unittest.main()
