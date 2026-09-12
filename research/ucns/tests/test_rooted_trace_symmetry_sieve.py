"""Executable witnesses for the rooted trace symmetry sieve."""

# === CHECKS ===
# id: check_rooted_trace_symmetry_binds_predecessor_evidence
#   proves: rooted_trace_symmetry_binds_predecessor_evidence
#   call: self::test_predecessor_and_target_are_exact
#   mutates: none
#   cleanup: none
#
# id: check_rooted_trace_automorphisms_act_freely
#   proves: rooted_trace_automorphisms_act_freely
#   call: self::test_nonidentity_seed_automorphisms_move_every_complete_order
#   mutates: none
#   cleanup: none
#
# id: check_rooted_trace_seed_symmetry_replays
#   proves: rooted_trace_seed_symmetry_replays
#   call: self::test_seed_trace_count_splits_into_twelve_element_orbits
#   mutates: none
#   cleanup: none
#
# id: check_rooted_trace_symmetric_continuations_are_falsified
#   proves: rooted_trace_symmetric_continuations_are_falsified
#   call: self::test_radius_two_and_two_face_symmetries_fail_divisibility
#   mutates: none
#   cleanup: none
#
# id: check_rooted_trace_symmetry_sieve_does_not_predict
#   proves: rooted_trace_symmetry_sieve_does_not_predict
#   call: self::test_no_constructor_survives_or_predicts
#   mutates: none
#   cleanup: none
#
# id: check_rooted_trace_symmetry_receipt_replays
#   proves: rooted_trace_symmetry_receipt_replays
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
COMMITTED_RECEIPT = UCNS_RESEARCH_ROOT / "receipts" / "rooted-trace-symmetry-sieve-v0.json"
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import rooted_trace_symmetry_sieve as m


class RootedTraceSymmetrySieveTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.seed = m.seed_structural_graph()
        cls.seed_group = m.rooted_automorphisms(cls.seed)
        cls.result = m.evaluate()

    def test_predecessor_and_target_are_exact(self) -> None:
        payload = m.receipt_payload()
        self.assertEqual(payload["source"]["ucns_base_commit"], m.lift.PINNED_UCNS_COMMIT)
        self.assertEqual(payload["source"]["event_trace_receipt_sha256"], m.lift.receipt_digest())
        self.assertEqual(payload["comparison"]["observed"], list(m.OBSERVED_GONOLS))
        self.assertEqual(self.result.state_target, 13709424605)
        self.assertEqual(self.result.state_target_factorization, ((5, 1), (2741884921, 1)))

    def test_nonidentity_seed_automorphisms_move_every_complete_order(self) -> None:
        order = tuple(vertex for vertex in self.seed.vertices if vertex != self.seed.root)
        identity = tuple(range(len(self.seed.vertices)))
        for automorphism in self.seed_group:
            mapped = m.apply_automorphism(self.seed, automorphism, order)
            if automorphism == identity:
                self.assertEqual(mapped, order)
            else:
                self.assertNotEqual(mapped, order)

    def test_seed_trace_count_splits_into_twelve_element_orbits(self) -> None:
        self.assertEqual(len(self.seed_group), 12)
        self.assertEqual(self.result.seed_automorphism_order, 12)
        self.assertEqual(self.result.seed_trace_count, 720)
        self.assertEqual(self.result.seed_orbit_count, 60)

    def test_radius_two_and_two_face_symmetries_fail_divisibility(self) -> None:
        result = self.result
        self.assertEqual(result.radius_two_symmetry_order, 12)
        self.assertEqual(result.radius_two_trace_count, 97934946851520)
        self.assertEqual(result.radius_two_trace_count % 12, 0)
        self.assertNotEqual(result.state_target % 12, 0)
        self.assertTrue(result.two_face_has_layer_swap)
        self.assertEqual(result.two_face_trace_count, 1779148800)
        self.assertEqual(result.two_face_trace_count % 2, 0)
        self.assertEqual(result.state_target % 2, 1)
        self.assertEqual(result.radius_two_standing, m.STATUS_FALSIFIED)
        self.assertEqual(result.two_face_standing, m.STATUS_FALSIFIED)

    def test_no_constructor_survives_or_predicts(self) -> None:
        self.assertEqual(self.result.falsified_class_count, 2)
        self.assertEqual(self.result.constructor_survivor_count, 0)
        self.assertIsNone(self.result.next_prediction)
        self.assertTrue(any("phase" in item for item in self.result.hmmm))

    def test_receipt_replays_byte_identically(self) -> None:
        first = m.receipt_bytes()
        second = m.receipt_bytes()
        self.assertEqual(first, second)
        self.assertEqual(m.receipt_digest(), sha256(first).hexdigest())
        payload = json.loads(first)
        self.assertEqual(payload["comparison"]["falsified_class_count"], 2)
        self.assertEqual(payload["comparison"]["constructor_survivor_count"], 0)
        self.assertIsNone(payload["comparison"]["next_prediction"])

        committed = json.loads(COMMITTED_RECEIPT.read_text(encoding="utf-8"))
        committed_digest = committed.pop("receipt_sha256")
        self.assertEqual(committed_digest, m.receipt_digest())
        self.assertEqual(committed, payload)


if __name__ == "__main__":
    unittest.main()
