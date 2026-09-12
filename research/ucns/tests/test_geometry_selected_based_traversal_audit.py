"""Executable witnesses for the geometry-selected based traversal audit."""

# === CHECKS ===
# id: check_based_traversal_audit_binds_exact_geometry
#   proves: based_traversal_audit_binds_exact_geometry
#   call: self::test_exact_sources_and_predecessor_receipts_are_bound
#   mutates: none
#   cleanup: none
#
# id: check_based_traversal_audit_separates_origin_from_attachment
#   proves: based_traversal_audit_separates_origin_from_attachment
#   call: self::test_distinguished_origin_does_not_invent_groupoid_attachment
#   mutates: none
#   cleanup: none
#
# id: check_based_traversal_audit_exhibits_direction_symmetry
#   proves: based_traversal_audit_exhibits_direction_symmetry
#   call: self::test_native_reflection_exchanges_signed_complete_returns_exactly
#   mutates: none
#   cleanup: none
#
# id: check_based_traversal_audit_exhibits_permutation_obstruction
#   proves: based_traversal_audit_exhibits_permutation_obstruction
#   call: self::test_unmarked_rank_three_shape_has_full_s3_word_orbit
#   mutates: none
#   cleanup: none
#
# id: check_based_traversal_audit_rejects_nongeometric_selectors
#   proves: based_traversal_audit_rejects_nongeometric_selectors
#   call: self::test_data_and_caller_orders_are_not_promoted
#   mutates: none
#   cleanup: none
#
# id: check_based_traversal_audit_defines_exact_missing_marks
#   proves: based_traversal_audit_defines_exact_missing_marks
#   call: self::test_all_five_geometric_marks_are_required_and_absent
#   mutates: none
#   cleanup: none
#
# id: check_based_traversal_audit_stops_without_word
#   proves: based_traversal_audit_stops_without_word
#   call: self::test_stop_result_emits_no_word_monodromy_or_arithmetic
#   mutates: none
#   cleanup: none
#
# id: check_based_traversal_audit_receipt_replays
#   proves: based_traversal_audit_receipt_replays
#   call: self::test_receipt_replays_byte_identically
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest


UCNS_RESEARCH_ROOT = Path(__file__).resolve().parents[1]
COMMITTED_RECEIPT = UCNS_RESEARCH_ROOT / "receipts" / "geometry-selected-based-traversal-audit-v0.json"
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import geometry_selected_based_traversal_audit as m
import ordered_complete_return_groupoid as groupoid_module
import ordered_return_invariant_audit as invariant_audit


class GeometrySelectedBasedTraversalAuditTest(unittest.TestCase):
    def test_exact_sources_and_predecessor_receipts_are_bound(self) -> None:
        payload = m.receipt_payload()
        source = payload["source"]
        self.assertEqual(source["ucns_commit"], m.extension.PINNED_UCNS_COMMIT)
        self.assertEqual(
            source["ordered_groupoid_receipt_sha256"],
            groupoid_module.receipt_digest(),
        )
        self.assertEqual(
            source["ordered_invariant_audit_receipt_sha256"],
            invariant_audit.receipt_digest(),
        )
        for item in source["source_file_digests"]:
            path = m._stack_root() / item["path"]
            self.assertEqual(sha256(path.read_bytes()).hexdigest(), item["sha256"])

    def test_distinguished_origin_does_not_invent_groupoid_attachment(self) -> None:
        origin = m.origin_attachment_audit()
        self.assertEqual(origin.public_gonol_index, 0)
        self.assertEqual(origin.public_gonol_glyph, " ")
        self.assertEqual(origin.direct_structural_null_carrier_position, 0)
        self.assertTrue(origin.carrier_structural_null_coordinate_free)
        self.assertEqual(origin.ordered_model_base_object, groupoid_module.POSITIVE_BASE_OBJECT)
        self.assertIsNone(origin.geometry_selected_origin_to_base_object_map)
        self.assertEqual(origin.status, m.STATUS_UNRESOLVED)

    def test_native_reflection_exchanges_signed_complete_returns_exactly(self) -> None:
        witness = m.native_direction_symmetry()
        self.assertEqual(witness.positive_turns, (Fraction(0), Fraction(1), Fraction(2)))
        self.assertEqual(witness.negative_turns, (Fraction(0), Fraction(-1), Fraction(-2)))
        self.assertEqual(witness.positive_states, witness.negative_states)
        self.assertTrue(witness.integer_return_traces_equal)
        self.assertTrue(witness.reflection_fixes_base_state)
        self.assertEqual(witness.reflection_conjugacy_checks, 35)
        self.assertTrue(witness.reflection_conjugacy_all_exact)
        self.assertIsNone(witness.geometry_selected_direction)

        direct = m._direct_mobius()
        base = direct.native_mobius_state()
        quarter = base.advance(Fraction(1, 4))
        self.assertEqual(
            m._reflect_state(direct, quarter),
            base.advance(Fraction(-1, 4)),
        )

    def test_unmarked_rank_three_shape_has_full_s3_word_orbit(self) -> None:
        orbit = m.permutation_selection_orbit()
        self.assertEqual(orbit.rank, 3)
        self.assertEqual(orbit.action_count, 6)
        self.assertEqual(orbit.orbit_size, 6)
        self.assertEqual(
            set(orbit.orbit_words),
            {
                ("g1", "g2", "g3"),
                ("g1", "g3", "g2"),
                ("g2", "g1", "g3"),
                ("g2", "g3", "g1"),
                ("g3", "g1", "g2"),
                ("g3", "g2", "g1"),
            },
        )
        self.assertEqual(orbit.fixed_once_each_words, ())
        self.assertEqual(orbit.common_abelianization, (1, 1, 1))
        self.assertIsNone(orbit.geometry_selected_word)

    def test_data_and_caller_orders_are_not_promoted(self) -> None:
        evaluations = m.selector_evaluations()
        self.assertEqual(len(evaluations), 8)
        self.assertFalse(any(item.status == "SELECTED" for item in evaluations))
        by_basis = {item.proposed_basis: item for item in evaluations}
        self.assertEqual(
            by_basis["Public Gonol position zero / Structural Null identity"].status,
            m.STATUS_UNRESOLVED,
        )
        for basis in (
            "forward direction of the Public Gonol arrangement tuple",
            "phase-zero positive-frame API default",
            "retained relation-basis ordinal order",
            "affinization participant slot order",
            "Mobius seed event or band order",
        ):
            self.assertEqual(by_basis[basis].status, m.STATUS_REJECTED)
        self.assertEqual(
            by_basis["one permutation of the unmarked rank-three return loops"].status,
            m.STATUS_UNSELECTED,
        )

    def test_all_five_geometric_marks_are_required_and_absent(self) -> None:
        requirements = m.audit().requirements
        self.assertFalse(requirements.ready)
        self.assertIsNone(requirements.origin_to_groupoid_attachment)
        self.assertIsNone(requirements.directed_tangent_or_chirality)
        self.assertIsNone(requirements.oriented_rotation_or_successor_system)
        self.assertIsNone(requirements.geometrically_marked_outgoing_dart)
        self.assertIsNone(requirements.complete_return_closure_rule)

    def test_stop_result_emits_no_word_monodromy_or_arithmetic(self) -> None:
        result = m.audit()
        self.assertEqual(result.status, m.STATUS)
        self.assertIsNone(result.geometry_selected_basepoint)
        self.assertIsNone(result.geometry_selected_orientation)
        self.assertIsNone(result.geometry_selected_traversal_word)
        self.assertIsNone(result.geometry_selected_attaching_word)
        self.assertIsNone(result.current_global_monodromy)
        self.assertIsNone(result.current_arithmetic_readout)
        self.assertIsNone(result.observation_comparison)
        self.assertIsNone(result.numerical_next_gonol)

        source = Path(m.__file__).read_text(encoding="utf-8")
        for forbidden in ("54837698421", "164513086777", "1661748437"):
            self.assertNotIn(forbidden, source)
        boundary = m.receipt_payload()["experiment_boundary"]
        self.assertIsNone(boundary["observed_successor_cardinality_input"])
        self.assertIsNone(boundary["observed_arithmetic_factor_input"])

    def test_receipt_replays_byte_identically(self) -> None:
        committed = json.loads(COMMITTED_RECEIPT.read_text(encoding="utf-8"))
        committed_digest = committed.pop("receipt_sha256")
        self.assertEqual(committed, m.receipt_payload())
        self.assertEqual(committed_digest, m.receipt_digest())
        self.assertEqual(committed_digest, sha256(m.receipt_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
