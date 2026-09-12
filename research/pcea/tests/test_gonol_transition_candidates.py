"""Executable witnesses for PCEA gonol transition candidate research."""

# === CHECKS ===
# id: check_transition_candidates_use_only_observed_sequence
#   proves: transition_candidates_use_only_observed_sequence
#   call: self::test_candidate_receipt_uses_only_observed_sequence_and_base_identity
#   mutates: none
#   cleanup: none
#
# id: check_transition_candidates_falsify_failed_families
#   proves: transition_candidates_falsify_failed_families
#   call: self::test_failed_candidate_families_are_explicitly_falsified
#   mutates: none
#   cleanup: none
#
# id: check_quadratic_forward_difference_is_control_only
#   proves: quadratic_forward_difference_is_control_only
#   call: self::test_quadratic_forward_difference_is_control_only
#   mutates: none
#   cleanup: none
#
# id: check_gonol_transition_receipt_replays_byte_identical
#   proves: gonol_transition_receipt_replays_byte_identical
#   call: self::test_receipt_replays_byte_identical
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from hashlib import sha256
import ast
import json
from pathlib import Path
import sys
import unittest


PCEA_RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PCEA_RESEARCH_ROOT))

import gonol_transition_candidates as m


class GonolTransitionCandidateTest(unittest.TestCase):
    def _by_id(self):
        return {result.candidate_id: result for result in m.evaluate_candidates()}

    def test_candidate_receipt_uses_only_observed_sequence_and_base_identity(self):
        payload = m.receipt_payload()
        self.assertEqual(payload["observed_data"]["sequence"], list(m.OBSERVED_GONOLS))
        self.assertEqual(payload["observed_data"]["ucns_constructor_identity"], "hmmm")
        self.assertEqual(payload["base"]["source_repository"], "The-Interdependency/pcea")
        self.assertEqual(
            payload["base"]["source_commit"],
            "4d2c581448b97bfb71da92b35487e74e6e3bcedc",
        )
        self.assertEqual(
            payload["candidate_policy"]["numeric_inputs"],
            "observed_data.sequence only",
        )

        source = Path(m.__file__).read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported_roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".", 1)[0])
        self.assertNotIn("pcea", imported_roots)
        self.assertNotIn("ucns", imported_roots)

    def test_failed_candidate_families_are_explicitly_falsified(self):
        results = self._by_id()
        for candidate_id in (
            "constant_delta",
            "constant_ratio",
            "integer_affine",
            "rational_affine_integer_output",
            "constant_square_offset",
        ):
            result = results[candidate_id]
            self.assertEqual(result.status, m.STATUS_FALSIFIED)
            self.assertEqual(result.standing, "rejected")
            self.assertTrue(result.rejection_reason)
            self.assertIsNone(result.prediction)

    def test_quadratic_forward_difference_is_control_only(self):
        result = self._by_id()["quadratic_forward_difference_baseline"]
        observed = m.OBSERVED_GONOLS
        expected_prediction = 3 * observed[2] - 3 * observed[1] + observed[0]
        self.assertEqual(result.status, m.STATUS_CONTROL)
        self.assertEqual(result.standing, m.CONTROL_STANDING)
        self.assertIs(result.replayed_observed, True)
        self.assertEqual(result.prediction, expected_prediction)
        self.assertTrue(result.hmmm)
        self.assertIn("no UCNS geometry selects constant second finite difference", result.hmmm)

    def test_receipt_replays_byte_identical(self):
        first = m.receipt_payload()
        second = m.receipt_payload()
        self.assertEqual(first, second)
        self.assertEqual(m.receipt_bytes(first), m.receipt_bytes(second))
        self.assertEqual(m.receipt_digest(first), sha256(m.receipt_bytes(first)).hexdigest())

        decoded = json.loads(m.receipt_bytes(first).decode("utf-8"))
        self.assertEqual(decoded["control_predictions"], first["control_predictions"])
        self.assertEqual(decoded["nonclaims"], list(m.NONCLAIMS))


if __name__ == "__main__":
    unittest.main()
