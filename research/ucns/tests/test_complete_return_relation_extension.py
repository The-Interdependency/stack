"""Executable witnesses for the complete-return relation extension."""

# === CHECKS ===
# id: check_complete_return_extension_binds_native_geometry
#   proves: complete_return_extension_binds_native_geometry
#   call: self::test_exact_native_zero_one_two_turn_trace
#   mutates: none
#   cleanup: none
#
# id: check_complete_return_extension_closes_only_complete_state
#   proves: complete_return_extension_closes_only_complete_state
#   call: self::test_quotient_identifies_only_restored_complete_state
#   mutates: none
#   cleanup: none
#
# id: check_complete_return_extension_adds_one_cycle
#   proves: complete_return_extension_adds_one_cycle
#   call: self::test_boundary_witness_has_exact_h1_rank_one
#   mutates: none
#   cleanup: none
#
# id: check_complete_return_extension_preserves_prior_relations
#   proves: complete_return_extension_preserves_prior_relations
#   call: self::test_iteration_preserves_basis_and_adds_one_per_scale
#   mutates: none
#   cleanup: none
#
# id: check_complete_return_extension_promotes_closed_whole
#   proves: complete_return_extension_promotes_closed_whole
#   call: self::test_extension_closes_and_promotes_with_provenance
#   mutates: none
#   cleanup: none
#
# id: check_complete_return_extension_is_target_free
#   proves: complete_return_extension_is_target_free
#   call: self::test_candidate_source_contains_no_successor_or_factor_targets
#   mutates: none
#   cleanup: none
#
# id: check_complete_return_extension_receipt_replays
#   proves: complete_return_extension_receipt_replays
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
COMMITTED_RECEIPT = UCNS_RESEARCH_ROOT / "receipts" / "complete-return-relation-extension-v0.json"
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import complete_return_relation_extension as m


class CompleteReturnRelationExtensionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.trace = m.complete_return_trace()
        cls.initial = m.bootstrap_public_gonol_state()
        cls.first = m.extend_complete_return(
            cls.initial,
            target_scale="test-complete-return-scale-1",
            occurrence_id="test.complete-return-1",
        )

    def test_exact_native_zero_one_two_turn_trace(self) -> None:
        occurrences = self.trace.occurrences
        self.assertEqual(tuple(item.turns for item in occurrences), (0, 1, 2))
        self.assertEqual(tuple(item.phase_turns for item in occurrences), ("0", "0", "0"))
        self.assertEqual(
            tuple(item.frame for item in occurrences),
            ("positive-local-frame", "reversed-local-frame", "positive-local-frame"),
        )
        self.assertEqual(occurrences[0].visible_key, occurrences[1].visible_key)
        self.assertEqual(occurrences[0].visible_key, occurrences[2].visible_key)
        self.assertNotEqual(occurrences[0].complete_key, occurrences[1].complete_key)
        self.assertEqual(occurrences[0].complete_key, occurrences[2].complete_key)

    def test_quotient_identifies_only_restored_complete_state(self) -> None:
        occurrences = self.trace.occurrences
        self.assertEqual(occurrences[0].quotient_vertex, occurrences[2].quotient_vertex)
        self.assertNotEqual(occurrences[0].quotient_vertex, occurrences[1].quotient_vertex)
        self.assertEqual(len(self.trace.quotient_vertices), 2)
        self.assertEqual(
            self.trace.directed_edges,
            (
                (occurrences[0].quotient_vertex, occurrences[1].quotient_vertex),
                (occurrences[1].quotient_vertex, occurrences[2].quotient_vertex),
            ),
        )

    def test_boundary_witness_has_exact_h1_rank_one(self) -> None:
        self.assertEqual(self.trace.boundary_matrix_c1_to_c0, ((-1, 1), (1, -1)))
        self.assertEqual(self.trace.boundary_rank, 1)
        self.assertEqual(self.trace.filling_two_cell_count, 0)
        self.assertEqual(self.trace.first_homology_rank, 1)
        self.assertEqual(m._matrix_rank(((1, 0), (0, 1))), 2)
        with self.assertRaises(m.CompleteReturnExtensionError):
            m._matrix_rank(((1, 2), (3,)))

    def test_iteration_preserves_basis_and_adds_one_per_scale(self) -> None:
        results = m.iterate_complete_return(4, scale_prefix="test-iterated-return")
        self.assertEqual(tuple(item.source.relation_rank for item in results), (0, 1, 2, 3))
        self.assertEqual(tuple(item.output.relation_rank for item in results), (1, 2, 3, 4))
        self.assertEqual(tuple(item.rank_delta for item in results), (1, 1, 1, 1))
        for item in results:
            self.assertEqual(item.output.relation_basis[:-1], item.source.relation_basis)
            self.assertEqual(item.output.relation_basis[-1], item.new_relation_id)
        all_ids = tuple(item.new_relation_id for item in results)
        self.assertEqual(len(set(all_ids)), len(all_ids))

    def test_extension_closes_and_promotes_with_provenance(self) -> None:
        carrier = m.pgfo.load_carrier()
        self.assertEqual(self.initial.source_digest, carrier.public_gonol_sha256)
        self.assertEqual(self.initial.relation_rank, 0)
        self.assertEqual(self.first.closed_affinization.coupling.arity, 2)
        roles = tuple(
            participant.role
            for participant in self.first.closed_affinization.coupling.participants
        )
        self.assertEqual(
            roles,
            (
                "complete-return-start-positive-frame",
                "complete-return-midpoint-reversed-frame",
            ),
        )
        self.assertTrue(self.first.transition.atomic_participant.constituents_recoverable)
        self.assertNotEqual(self.first.output.atomic_id, self.initial.atomic_id)
        self.assertEqual(self.first.output.relation_rank, 1)
        self.assertTrue(self.first.new_relation_id.startswith("ucns.relation.complete-return:"))
        self.assertIn(self.first.new_relation_id, self.first.closed_affinization.coupling.source_refs)
        self.assertIn(
            f"ordered-relation-basis-sha256:{self.first.relation_basis_digest}",
            self.first.closed_affinization.coupling.source_refs,
        )
        self.assertEqual(
            self.first.transition.atomic_participant.coupling_digest,
            self.first.closed_affinization.coupling.coupling_digest,
        )
        with self.assertRaises(m.CompleteReturnExtensionError):
            m.extend_complete_return(
                self.initial,
                target_scale=self.initial.scale_id,
                occurrence_id="test.same-scale",
            )

    def test_candidate_source_contains_no_successor_or_factor_targets(self) -> None:
        source = Path(m.__file__).read_text(encoding="utf-8")
        prohibited = (
            "2881",
            "54837698421",
            "164513086777",
            "B_4",
            "observed_witnesses",
            "omega=4",
        )
        for text in prohibited:
            self.assertNotIn(text, source)
        payload = m.receipt_payload()
        candidate = payload["candidate"]
        self.assertIsNone(candidate["successor_cardinality_input"])
        self.assertIsNone(candidate["arithmetic_factor_input"])
        self.assertIsNone(candidate["desired_relation_rank_input"])
        self.assertEqual(payload["validation_state"], "NOT_COMPARED_WITH_OBSERVED_SCALES")

    def test_receipt_replays_byte_identically(self) -> None:
        first = m.receipt_bytes()
        second = m.receipt_bytes()
        self.assertEqual(first, second)
        self.assertEqual(m.receipt_digest(), sha256(first).hexdigest())
        payload = json.loads(first)
        self.assertEqual(payload["sample_extension"]["rank_delta"], 1)
        self.assertEqual(payload["sample_extension"]["trace"]["chain_witness"]["first_homology_rank"], 1)

        committed = json.loads(COMMITTED_RECEIPT.read_text(encoding="utf-8"))
        committed_digest = committed.pop("receipt_sha256")
        self.assertEqual(committed_digest, m.receipt_digest())
        self.assertEqual(committed, payload)


if __name__ == "__main__":
    unittest.main()
