"""Executable witnesses for gonol successor mechanics research."""

# === CHECKS ===
# id: check_successor_mechanics_start_from_pinned_157_gonol
#   proves: successor_mechanics_start_from_pinned_157_gonol
#   call: self::test_mechanics_snapshot_binds_pinned_public_gonol
#   mutates: none
#   cleanup: none
#
# id: check_successor_candidates_do_not_embed_gate_targets
#   proves: successor_candidates_do_not_embed_gate_targets
#   call: self::test_candidate_functions_do_not_embed_gate_targets
#   mutates: none
#   cleanup: none
#
# id: check_successor_candidates_reject_failed_mechanics
#   proves: successor_candidates_reject_failed_mechanics
#   call: self::test_mechanics_candidates_reject_before_next_prediction
#   mutates: none
#   cleanup: none
#
# id: check_successor_mechanics_record_unresolved_operations
#   proves: successor_mechanics_record_unresolved_operations
#   call: self::test_unresolved_operations_are_recorded_not_fitted
#   mutates: none
#   cleanup: none
#
# id: check_successor_mechanics_receipt_replays_byte_identical
#   proves: successor_mechanics_receipt_replays_byte_identical
#   call: self::test_receipt_replays_byte_identical
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys
import types
import unittest


PCEA_RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PCEA_RESEARCH_ROOT))

import gonol_successor_mechanics as m


def _code_constants(code: types.CodeType) -> set[object]:
    constants: set[object] = set()
    for value in code.co_consts:
        if isinstance(value, types.CodeType):
            constants.update(_code_constants(value))
        else:
            constants.add(value)
    return constants


class GonolSuccessorMechanicsTest(unittest.TestCase):
    def test_mechanics_snapshot_binds_pinned_public_gonol(self) -> None:
        mechanics = m.load_mechanics()
        self.assertEqual(mechanics.public_gonol_arity, 157)
        self.assertEqual(mechanics.public_gonol_sha256, m.PINNED_PUBLIC_GONOL_SHA256)
        self.assertEqual(len(mechanics.public_gonol_positions), 157)
        self.assertEqual(len({glyph for _, glyph in mechanics.public_gonol_positions}), 157)
        self.assertEqual(mechanics.public_gonol_origin, (0, " "))
        self.assertEqual(mechanics.pcea_base["source_commit"], "4d2c581448b97bfb71da92b35487e74e6e3bcedc")
        self.assertEqual(mechanics.ucns_base["source_commit"], "1975fe70cf4e0826a8020c2da3047569e277af64")
        self.assertEqual(mechanics.mobius_visible_preimage_count, 2)
        self.assertEqual(mechanics.mobius_complete_return_turns, 2)

    def test_candidate_functions_do_not_embed_gate_targets(self) -> None:
        forbidden = {
            m.OBSERVED_GATE[1],
            m.OBSERVED_GATE[2],
            m.INTERPOLATION_CONTROL_NEXT,
        }
        for candidate in m._candidate_functions():
            constants = _code_constants(candidate.operation.__code__)
            self.assertTrue(forbidden.isdisjoint(constants), candidate.candidate_id)

    def test_mechanics_candidates_reject_before_next_prediction(self) -> None:
        results = m.evaluate_successor_candidates()
        self.assertEqual(
            {result.status for result in results},
            {m.STATUS_FALSIFIED, m.STATUS_UNRESOLVED},
        )
        self.assertFalse(any(result.status == m.STATUS_CONSTRUCTOR_CANDIDATE for result in results))
        self.assertFalse(any(result.first_target_match for result in results))
        self.assertFalse(any(result.next_prediction is not None for result in results))

        by_id = {result.candidate_id: result for result in results}
        self.assertEqual(by_id["atomic_identity_carry"].first_output, 157)
        self.assertEqual(by_id["mobius_twofold_lift"].first_output, 314)
        self.assertEqual(by_id["mobius_twofold_closed_whole"].first_output, 315)
        self.assertEqual(by_id["unordered_position_pair_closure"].first_output, 12404)
        self.assertEqual(by_id["directed_order_pair_closure"].first_output, 24650)

    def test_unresolved_operations_are_recorded_not_fitted(self) -> None:
        payload = m.receipt_payload()
        unresolved = {
            item["candidate_id"]: item
            for item in payload["results"]
            if item["status"] == m.STATUS_UNRESOLVED
        }
        self.assertIn("complete_public_function_application", unresolved)
        self.assertIn("affixiate_all_position_pairs", unresolved)
        self.assertIn("recursive_scale_transition", unresolved)
        self.assertEqual(payload["constructor_candidates"], [])
        self.assertEqual(payload["next_predictions"], [])
        self.assertFalse(payload["summary"]["next_prediction_available"])
        self.assertEqual(
            payload["candidate_policy"]["control_comparison"],
            "not reached unless a constructor candidate emits a next prediction",
        )

    def test_receipt_replays_byte_identical(self) -> None:
        first = m.receipt_payload()
        second = m.receipt_payload()
        self.assertEqual(first, second)
        self.assertEqual(m.receipt_bytes(first), m.receipt_bytes(second))
        self.assertEqual(m.receipt_digest(first), sha256(m.receipt_bytes(first)).hexdigest())

        decoded = json.loads(m.receipt_bytes(first).decode("utf-8"))
        self.assertEqual(decoded["summary"]["constructor_candidates"], 0)
        self.assertEqual(decoded["mechanics"]["public_gonol"]["arity"], 157)
        self.assertEqual(decoded["candidate_policy"]["interpolation_control"], 164513086777)


if __name__ == "__main__":
    unittest.main()
