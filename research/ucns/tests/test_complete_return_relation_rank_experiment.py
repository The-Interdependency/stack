"""Executable witnesses for the complete-return relation-rank gate."""

# === CHECKS ===
# id: check_complete_return_rank_gate_freezes_candidate_first
#   proves: complete_return_rank_gate_freezes_candidate_first
#   call: self::test_candidate_identity_is_frozen_before_gate
#   mutates: none
#   cleanup: none
#
# id: check_complete_return_rank_gate_runs_unchanged_operation
#   proves: complete_return_rank_gate_runs_unchanged_operation
#   call: self::test_four_extensions_use_one_trace_and_add_one_rank
#   mutates: none
#   cleanup: none
#
# id: check_complete_return_rank_gate_compares_only_after_generation
#   proves: complete_return_rank_gate_compares_only_after_generation
#   call: self::test_first_three_generated_ranks_match_external_omega_retrodictively
#   mutates: none
#   cleanup: none
#
# id: check_complete_return_rank_gate_freezes_nonnumeric_next_rank
#   proves: complete_return_rank_gate_freezes_nonnumeric_next_rank
#   call: self::test_next_relation_rank_is_four_but_no_integer_is_emitted
#   mutates: none
#   cleanup: none
#
# id: check_complete_return_rank_gate_preserves_factor_boundary
#   proves: complete_return_rank_gate_preserves_factor_boundary
#   call: self::test_factor_interpretation_remains_unresolved
#   mutates: none
#   cleanup: none
#
# id: check_complete_return_rank_gate_receipt_replays
#   proves: complete_return_rank_gate_receipt_replays
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
COMMITTED_RECEIPT = UCNS_RESEARCH_ROOT / "receipts" / "complete-return-relation-rank-experiment-v0.json"
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import complete_return_relation_rank_experiment as m


class CompleteReturnRelationRankExperimentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = m.evaluate()

    def test_candidate_identity_is_frozen_before_gate(self) -> None:
        frozen = self.result.frozen_candidate
        candidate_path = m._stack_root() / frozen.module_path
        self.assertEqual(frozen.code_sha256, sha256(candidate_path.read_bytes()).hexdigest())
        self.assertEqual(frozen.receipt_sha256, m.extension.receipt_digest())
        self.assertEqual(frozen.producer_code_reference, "sha256:" + frozen.code_sha256)
        self.assertEqual(frozen.validation_state, "NOT_COMPARED_WITH_OBSERVED_SCALES")
        candidate_source = candidate_path.read_text(encoding="utf-8")
        for prohibited in ("2881", "54837698421", "164513086777", "B_4", "omega=4"):
            self.assertNotIn(prohibited, candidate_source)

    def test_four_extensions_use_one_trace_and_add_one_rank(self) -> None:
        generated = self.result.generated_extensions
        self.assertEqual(len(generated), 4)
        self.assertEqual(tuple(item.source.relation_rank for item in generated), (0, 1, 2, 3))
        self.assertEqual(tuple(item.output.relation_rank for item in generated), (1, 2, 3, 4))
        self.assertEqual(tuple(item.rank_delta for item in generated), (1, 1, 1, 1))
        trace_digests = {
            sha256(m._canonical_bytes(item.trace.to_payload())).hexdigest()
            for item in generated
        }
        self.assertEqual(len(trace_digests), 1)
        relation_ids = tuple(item.new_relation_id for item in generated)
        self.assertEqual(len(set(relation_ids)), 4)
        for item in generated:
            self.assertEqual(item.output.relation_basis[:-1], item.source.relation_basis)

    def test_first_three_generated_ranks_match_external_omega_retrodictively(self) -> None:
        comparisons = self.result.comparisons
        self.assertEqual(tuple(item.generated_relation_rank for item in comparisons), (1, 2, 3))
        self.assertEqual(tuple(item.observed_arithmetic_omega for item in comparisons), (1, 2, 3))
        self.assertTrue(all(item.match for item in comparisons))
        self.assertTrue(all(item.standing == m.STATUS_MATCH for item in comparisons))
        self.assertEqual(self.result.status, m.STATUS_MATCH)
        self.assertIn("RETRODICTIVE", self.result.status)

    def test_next_relation_rank_is_four_but_no_integer_is_emitted(self) -> None:
        self.assertEqual(self.result.next_relation_rank, 4)
        self.assertIsNotNone(self.result.next_relation_output_sha256)
        self.assertEqual(self.result.preregistered_structural_omega, 4)
        self.assertTrue(self.result.next_rank_matches_preregistered_omega)
        self.assertIsNone(self.result.new_factor_cardinalities)
        self.assertIsNone(self.result.numerical_next_gonol)

    def test_factor_interpretation_remains_unresolved(self) -> None:
        self.assertEqual(self.result.arithmetic_factor_mapping_status, m.FACTOR_MAPPING_STATUS)
        self.assertIn("UNRESOLVED", self.result.arithmetic_factor_mapping_status)
        payload = self.result.to_payload()
        self.assertIn("no arithmetic factor", payload["claim_boundary"])
        self.assertIsNone(payload["next"]["new_factor_cardinalities"])
        self.assertIsNone(payload["next"]["numerical_gonol"])

    def test_receipt_replays_byte_identically(self) -> None:
        first = m.receipt_bytes()
        second = m.receipt_bytes()
        self.assertEqual(first, second)
        self.assertEqual(m.receipt_digest(), sha256(first).hexdigest())
        payload = json.loads(first)
        self.assertEqual(payload["experiment"]["status"], m.STATUS_MATCH)
        self.assertEqual(payload["experiment"]["next"]["relation_rank"], 4)
        self.assertIsNone(payload["experiment"]["next"]["numerical_gonol"])

        committed = json.loads(COMMITTED_RECEIPT.read_text(encoding="utf-8"))
        committed_digest = committed.pop("receipt_sha256")
        self.assertEqual(committed_digest, m.receipt_digest())
        self.assertEqual(committed, payload)


if __name__ == "__main__":
    unittest.main()
