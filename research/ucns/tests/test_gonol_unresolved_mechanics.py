"""Executable witnesses for UCNS unresolved-mechanics research."""

# === CHECKS ===
# id: check_ucns_unresolved_mechanics_start_from_pinned_public_gonol
#   proves: ucns_unresolved_mechanics_start_from_pinned_public_gonol
#   call: self::test_snapshot_binds_pinned_public_gonol_and_ucns_commit
#   mutates: none
#   cleanup: none
#
# id: check_ucns_observations_are_falsification_gates_only
#   proves: ucns_observations_are_falsification_gates_only
#   call: self::test_candidate_operations_do_not_embed_observed_targets
#   mutates: none
#   cleanup: none
#
# id: check_ucns_candidate_mechanics_are_structure_derived
#   proves: ucns_candidate_mechanics_are_structure_derived
#   call: self::test_candidates_cover_the_three_ucns_mechanics
#   mutates: none
#   cleanup: none
#
# id: check_ucns_candidates_must_pass_two_transition_gate
#   proves: ucns_candidates_must_pass_two_transition_gate
#   call: self::test_completed_candidates_are_falsified_before_second_gate
#   mutates: none
#   cleanup: none
#
# id: check_ucns_unresolved_operations_remain_hmmm
#   proves: ucns_unresolved_operations_remain_hmmm
#   call: self::test_exact_unresolved_mechanics_are_blocked
#   mutates: none
#   cleanup: none
#
# id: check_ucns_unresolved_mechanics_receipt_replays_byte_identical
#   proves: ucns_unresolved_mechanics_receipt_replays_byte_identical
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


UCNS_RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import gonol_unresolved_mechanics as m


def _code_constants(code: types.CodeType) -> set[object]:
    constants: set[object] = set()
    for value in code.co_consts:
        if isinstance(value, types.CodeType):
            constants.update(_code_constants(value))
        else:
            constants.add(value)
    return constants


class GonolUnresolvedMechanicsTest(unittest.TestCase):
    def test_snapshot_binds_pinned_public_gonol_and_ucns_commit(self) -> None:
        mechanics = m.load_mechanics()
        self.assertEqual(mechanics.ucns_base["source_commit"], m.PINNED_UCNS_COMMIT)
        self.assertEqual(mechanics.public_gonol_arity, 157)
        self.assertEqual(mechanics.public_gonol_sha256, m.PINNED_PUBLIC_GONOL_SHA256)
        self.assertEqual(mechanics.public_gonol_origin, (0, " "))
        self.assertEqual(len(mechanics.public_gonol_positions), 157)
        self.assertEqual(len({glyph for _, glyph in mechanics.public_gonol_positions}), 157)
        self.assertEqual(mechanics.mobius_visible_preimage_count, 2)
        self.assertEqual(mechanics.mobius_complete_return_turns, 2)
        self.assertEqual(mechanics.mobius_seed_bands, 7)
        self.assertEqual(mechanics.mobius_seed_structural_relations, 12)
        self.assertEqual(mechanics.mobius_seed_pair_relations, 21)
        self.assertEqual(mechanics.mobius_seed_pairwise_projection_events, 39)
        self.assertEqual(mechanics.mobius_seed_declared_structural_boundary_events, 48)

    def test_candidate_operations_do_not_embed_observed_targets(self) -> None:
        forbidden = set(m.OBSERVED_TRANSITIONS[1:])
        for candidate in m._candidate_functions():
            constants = _code_constants(candidate.operation.__code__)
            self.assertTrue(forbidden.isdisjoint(constants), candidate.candidate_id)

    def test_candidates_cover_the_three_ucns_mechanics(self) -> None:
        candidates = m._candidate_functions()
        mechanics = {candidate.mechanic for candidate in candidates}
        self.assertEqual(
            mechanics,
            {
                "Public Gonol functional operations",
                "affinization/coupling geometry",
                "recursive-scale transition",
            },
        )
        self.assertTrue(all(candidate.basis for candidate in candidates))

    def test_completed_candidates_are_falsified_before_second_gate(self) -> None:
        by_id = {result.candidate_id: result for result in m.evaluate_candidates()}
        self.assertEqual(by_id["public_identity_carry"].first_output, 157)
        self.assertEqual(by_id["public_cyclic_order_closure"].first_output, 315)
        self.assertEqual(by_id["unordered_position_pair_closure"].first_output, 12404)
        self.assertEqual(by_id["directed_position_pair_closure"].first_output, 24650)
        self.assertEqual(by_id["seed_w7_structural_relations_per_position"].first_output, 2042)
        self.assertEqual(by_id["seed_pair_projection_events_per_position"].first_output, 6281)
        self.assertEqual(by_id["mobius_visible_preimage_promotion"].first_output, 315)
        self.assertEqual(by_id["seed_seven_band_scale_promotion"].first_output, 1100)

        completed = [
            result
            for result in by_id.values()
            if result.status == m.STATUS_FALSIFIED
        ]
        self.assertEqual(len(completed), 8)
        self.assertFalse(any(result.first_target_match for result in completed))
        self.assertFalse(any(result.second_input is not None for result in completed))
        self.assertFalse(any(result.next_prediction is not None for result in completed))

    def test_exact_unresolved_mechanics_are_blocked(self) -> None:
        payload = m.receipt_payload()
        unresolved = {
            item["candidate_id"]: item
            for item in payload["results"]
            if item["status"] == m.STATUS_UNRESOLVED
        }
        self.assertEqual(
            set(unresolved),
            {
                "complete_public_function_application",
                "exact_affinization_coupling_geometry",
                "recursive_scale_transition_law",
            },
        )
        self.assertEqual(payload["survivors"], [])
        self.assertFalse(payload["summary"]["next_prediction_available"])
        self.assertIn("not loaded or compared", payload["withheld_comparison_policy"])
        hmmm_text = "\n".join(payload["hmmm"]).lower()
        self.assertIn("public gonol functional operations", hmmm_text)
        self.assertIn("coupling geometry", hmmm_text)
        self.assertIn("recursive-scale transition", hmmm_text)

    def test_receipt_replays_byte_identical(self) -> None:
        first = m.receipt_payload()
        second = m.receipt_payload()
        self.assertEqual(first, second)
        self.assertEqual(m.receipt_bytes(first), m.receipt_bytes(second))
        self.assertEqual(m.receipt_digest(first), sha256(m.receipt_bytes(first)).hexdigest())

        decoded = json.loads(m.receipt_bytes(first).decode("utf-8"))
        self.assertEqual(decoded["summary"]["falsified"], 8)
        self.assertEqual(decoded["summary"]["unresolved"], 3)
        self.assertEqual(decoded["summary"]["survivors"], 0)
        self.assertEqual(decoded["construction_identity"]["selection_effect"], "none")


if __name__ == "__main__":
    unittest.main()
