"""Executable witnesses for the origin-attachment canon-gap record."""

# === CHECKS ===
# id: check_origin_attachment_gap_binds_exact_authority
#   proves: origin_attachment_gap_binds_exact_authority
#   call: self::test_exact_authority_sources_and_predecessors_are_bound
#   mutates: none
#   cleanup: none
#
# id: check_origin_attachment_gap_preserves_null_boundary
#   proves: origin_attachment_gap_preserves_null_boundary
#   call: self::test_null_operations_do_not_create_traversable_attachment
#   mutates: none
#   cleanup: none
#
# id: check_origin_attachment_gap_rejects_near_misses
#   proves: origin_attachment_gap_rejects_geometric_near_misses
#   call: self::test_candidate_geometries_exclude_or_fail_to_attach_origin
#   mutates: none
#   cleanup: none
#
# id: check_origin_attachment_gap_records_choices
#   proves: origin_attachment_gap_records_choice_boundary
#   call: self::test_current_attachment_set_is_empty_and_conditional_fiber_is_unselected
#   mutates: none
#   cleanup: none
#
# id: check_origin_attachment_gap_defines_axiom
#   proves: origin_attachment_gap_defines_minimal_axiom
#   call: self::test_required_axiom_is_unoriented_and_replayable
#   mutates: none
#   cleanup: none
#
# id: check_origin_attachment_gap_stops_downstream
#   proves: origin_attachment_gap_stops_before_downstream_fields
#   call: self::test_audit_stops_without_downstream_evaluation
#   mutates: none
#   cleanup: none
#
# id: check_origin_attachment_gap_receipt_replays
#   proves: origin_attachment_gap_receipt_replays
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
COMMITTED_RECEIPT = (
    UCNS_RESEARCH_ROOT / "receipts" / "origin-attachment-canon-gap-v0.json"
)
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import origin_attachment_canon_gap as m


class OriginAttachmentCanonGapTest(unittest.TestCase):
    def test_exact_authority_sources_and_predecessors_are_bound(self) -> None:
        source = m.receipt_payload()["source"]
        self.assertEqual(source["ucns_commit"], m.PINNED_UCNS_COMMIT)
        self.assertEqual(source["ucns_tree"], m.PINNED_UCNS_TREE)
        self.assertEqual(
            source["constructor_contract_receipt_sha256"],
            m.CONSTRUCTOR_RECEIPT_SHA256,
        )
        self.assertEqual(
            source["provenance_history_receipt_sha256"],
            m.PROVENANCE_RECEIPT_SHA256,
        )
        self.assertFalse(source["network_used"])
        for item in source["source_file_digests"]:
            path = m._stack_root() / item["path"]
            self.assertEqual(sha256(path.read_bytes()).hexdigest(), item["sha256"])

        inventory = m.canonical_callable_inventory()
        self.assertEqual(inventory.public_and_native_symbol_modules, ("__init__.py",))
        self.assertEqual(inventory.facade_top_level_callable_count, 0)
        self.assertEqual(inventory.typed_public_origin_consumers, ())
        self.assertEqual(inventory.typed_direct_origin_consumers, ())
        self.assertEqual(inventory.direct_state_factory_parameters, ("turns", "frame"))
        self.assertEqual(inventory.declared_origin_to_traversable_callables, ())

    def test_null_operations_do_not_create_traversable_attachment(self) -> None:
        evidence = m.canonical_geometry_evidence()
        self.assertEqual(evidence.public_origin["index"], 0)
        self.assertEqual(evidence.public_origin["glyph"], " ")
        self.assertEqual(evidence.direct_origin["carrier_position"], 0)
        self.assertTrue(evidence.carrier_structural_null_coordinate_free)
        self.assertTrue(evidence.carrier_null_preserved_by_project)
        self.assertTrue(evidence.carrier_null_preserved_by_deck_translation)
        self.assertTrue(evidence.carrier_null_has_only_null_preimage)
        self.assertIsNone(evidence.public_origin_to_structural_null_map)
        self.assertIsNone(evidence.structural_null_to_native_state_map)

    def test_candidate_geometries_exclude_or_fail_to_attach_origin(self) -> None:
        evidence = m.canonical_geometry_evidence()
        self.assertEqual(evidence.vesica["selection_effect"], "none")
        self.assertEqual(evidence.vesica["null_clearance_lower_bound"], "49/100")
        self.assertFalse(evidence.vesica["origin_incident_to_band"])

        self.assertEqual(evidence.seed["selection_effect"], "none")
        self.assertEqual(evidence.seed["projected_null_incident_slot_count"], 6)
        self.assertFalse(evidence.seed["projected_null_is_vertex"])
        self.assertFalse(evidence.seed["projected_null_is_structural_null"])
        self.assertEqual(evidence.seed["lifted_occurrence_count"], 6)
        self.assertTrue(evidence.seed["all_lifted_occurrences_nonzero"])
        self.assertTrue(evidence.seed["origin_contact_margin_positive"])

        self.assertEqual(evidence.compatibility["selection_effect"], "none")
        self.assertEqual(evidence.compatibility["compatible_incident_checks"], 0)
        self.assertEqual(evidence.prime_lifts["selection_effect"], "none")
        self.assertEqual(evidence.prime_lifts["p5_origin_void_lower_bound"], "9/100")
        self.assertEqual(evidence.prime_lifts["p7_origin_void_lower_bound"], "9/100")
        self.assertIsNone(evidence.prime_lifts["public_gonol_bridge"])

    def test_current_attachment_set_is_empty_and_conditional_fiber_is_unselected(self) -> None:
        choices = m.attachment_choice_audit()
        self.assertEqual(choices.authoritative_admissible_attachments, ())
        self.assertEqual(choices.authoritative_attachment_count, 0)
        self.assertEqual(choices.current_status, m.CURRENT_CHOICE_STATUS)
        self.assertFalse(choices.future_attachment_choice_space_determinable)
        self.assertEqual(choices.future_status, m.FUTURE_CHOICE_STATUS)

        fiber = choices.conditional_native_target_fiber
        self.assertEqual(fiber.visible_class_count, 1)
        self.assertEqual(fiber.framed_lift_count, 2)
        self.assertEqual(
            tuple(item["frame"] for item in fiber.framed_lifts),
            ("positive-local-frame", "reversed-local-frame"),
        )
        self.assertTrue(fiber.one_turn_exchanges_framed_lifts)
        self.assertIsNone(fiber.selected_framed_lift)
        self.assertEqual(
            fiber.standing,
            "CONDITIONAL_TARGET_FIBER_ONLY__NOT_ATTACHMENT_CHOICES",
        )

    def test_required_axiom_is_unoriented_and_replayable(self) -> None:
        axiom = m.required_canon_axiom()
        self.assertEqual(axiom.axiom_id, "ucns.origin-to-traversable-base-incidence")
        self.assertIn("unframed base object", axiom.relation)
        self.assertIn("replay_sha256", axiom.minimum_receipt_fields)
        self.assertEqual(
            axiom.must_not_select,
            (
                "directed tangent or chirality",
                "rotation system",
                "marked outgoing dart",
                "closure rule",
            ),
        )

    def test_audit_stops_without_downstream_evaluation(self) -> None:
        result = m.audit()
        self.assertEqual(result.status, m.STATUS)
        self.assertEqual(result.field, "origin_attachment")
        self.assertEqual(result.field_status, m.FIELD_STATUS)
        self.assertIsNone(result.origin_attachment)
        self.assertFalse(result.downstream_fields_evaluated)
        self.assertFalse(result.constructor_continuation_permitted)

        source = Path(m.__file__).read_text(encoding="utf-8")
        for forbidden_number in ("2881", "54837698421", "164513086777"):
            self.assertNotIn(forbidden_number, source)

    def test_receipt_replays_byte_identically(self) -> None:
        raw = COMMITTED_RECEIPT.read_bytes()
        committed = json.loads(raw)
        committed_digest = committed.pop("receipt_sha256")
        self.assertEqual(committed, m.receipt_payload())
        self.assertEqual(committed_digest, m.receipt_digest())
        self.assertEqual(committed_digest, sha256(m.receipt_bytes()).hexdigest())
        self.assertEqual(raw, m.formatted_receipt_bytes())


if __name__ == "__main__":
    unittest.main()
