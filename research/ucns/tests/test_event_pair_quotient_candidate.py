"""Executable witnesses for the event-pair quotient candidate."""

# === CHECKS ===
# id: check_event_pair_quotient_binds_pinned_counts
#   proves: event_pair_quotient_binds_pinned_counts
#   call: self::test_pinned_event_relation_and_boundary_counts
#   mutates: none
#   cleanup: none
#
# id: check_event_pair_quotient_operator_is_target_free
#   proves: event_pair_quotient_operator_is_target_free
#   call: self::test_operator_is_exact_and_contains_no_observed_target
#   mutates: none
#   cleanup: none
#
# id: check_event_pair_quotient_first_match_is_retrodictive
#   proves: event_pair_quotient_first_match_is_retrodictive
#   call: self::test_first_gate_exact_identity_is_retrodictive_only
#   mutates: none
#   cleanup: none
#
# id: check_event_pair_quotient_fails_unchanged_second_gate
#   proves: event_pair_quotient_fails_unchanged_second_gate
#   call: self::test_unchanged_operator_is_falsified_at_second_gate
#   mutates: none
#   cleanup: none
#
# id: check_event_pair_quotient_does_not_predict_after_failure
#   proves: event_pair_quotient_does_not_predict_after_failure
#   call: self::test_no_survivor_or_prediction
#   mutates: none
#   cleanup: none
#
# id: check_event_pair_quotient_receipt_replays
#   proves: event_pair_quotient_receipt_replays
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
COMMITTED_RECEIPT = UCNS_RESEARCH_ROOT / "receipts" / "event-pair-quotient-candidate-v0.json"
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import event_pair_quotient_candidate as m


class EventPairQuotientCandidateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = m.evaluate()

    def test_pinned_event_relation_and_boundary_counts(self) -> None:
        geometry = m.lift.load_seed_geometry()
        self.assertEqual(geometry.base_commit, m.lift.PINNED_UCNS_COMMIT)
        self.assertEqual(geometry.pairwise_projection_event_count, 39)
        self.assertEqual(geometry.pair_relation_count, 21)
        self.assertEqual(geometry.boundary_multiplicity, 4)
        self.assertEqual(self.result.event_state_count, 39)
        self.assertEqual(self.result.relation_constraint_rank, 21)

    def test_operator_is_exact_and_contains_no_observed_target(self) -> None:
        self.assertEqual(m.exterior_pair_quotient_dimension(39, 21), 720)
        self.assertEqual(m.exterior_pair_quotient_dimension(720, 21), 258819)
        constants = set(inspect.unwrap(m.exterior_pair_quotient_dimension).__code__.co_consts)
        self.assertTrue(set(m.OBSERVED_GONOLS).isdisjoint(constants))

    def test_first_gate_exact_identity_is_retrodictive_only(self) -> None:
        result = self.result
        self.assertEqual(result.exterior_pair_dimension, 741)
        self.assertEqual(result.first_quotient_state, 720)
        self.assertEqual(result.first_lifted_gonol, 2881)
        self.assertTrue(result.first_gate_match)
        self.assertEqual(result.first_gate_standing, m.FIRST_GATE_STANDING)

    def test_unchanged_operator_is_falsified_at_second_gate(self) -> None:
        result = self.result
        self.assertEqual(result.second_pair_dimension, 258840)
        self.assertEqual(result.second_quotient_state, 258819)
        self.assertEqual(result.second_lifted_gonol, 1035277)
        self.assertFalse(result.second_gate_match)
        self.assertEqual(result.status, m.STATUS_FALSIFIED)

    def test_no_survivor_or_prediction(self) -> None:
        self.assertEqual(self.result.constructor_survivor_count, 0)
        self.assertIsNone(self.result.next_prediction)
        self.assertTrue(any("exterior algebra" in item for item in self.result.hmmm))

    def test_receipt_replays_byte_identically(self) -> None:
        first = m.receipt_bytes()
        second = m.receipt_bytes()
        self.assertEqual(first, second)
        self.assertEqual(m.receipt_digest(), sha256(first).hexdigest())
        payload = json.loads(first)
        self.assertEqual(payload["comparison"]["second_gate"]["standing"], m.STATUS_FALSIFIED)
        self.assertIsNone(payload["comparison"]["next_prediction"])

        committed = json.loads(COMMITTED_RECEIPT.read_text(encoding="utf-8"))
        committed_digest = committed.pop("receipt_sha256")
        self.assertEqual(committed_digest, m.receipt_digest())
        self.assertEqual(committed, payload)


if __name__ == "__main__":
    unittest.main()
