"""Executable witnesses for the fail-closed based-traversal contract."""

# === CHECKS ===
# id: check_based_traversal_contract_binds_current_authority
#   proves: based_traversal_contract_binds_current_authority
#   call: self::test_exact_authority_and_predecessor_receipts_are_bound
#   mutates: none
#   cleanup: none
#
# id: check_based_traversal_contract_orders_five_fields
#   proves: based_traversal_contract_orders_five_fields
#   call: self::test_five_fields_have_exact_dependency_order
#   mutates: none
#   cleanup: none
#
# id: check_based_traversal_contract_rejects_nongeometric_derivations
#   proves: based_traversal_contract_rejects_nongeometric_derivations
#   call: self::test_source_order_derivation_is_rejected
#   mutates: none
#   cleanup: none
#
# id: check_based_traversal_contract_separates_origin_from_attachment
#   proves: based_traversal_contract_separates_origin_from_attachment
#   call: self::test_origin_primitives_do_not_become_attachment
#   mutates: none
#   cleanup: none
#
# id: check_based_traversal_contract_stops_at_first_missing_field
#   proves: based_traversal_contract_stops_at_first_missing_field
#   call: self::test_first_missing_field_stops_all_downstream_evaluation
#   mutates: none
#   cleanup: none
#
# id: check_based_traversal_contract_defines_certificate_output
#   proves: based_traversal_contract_defines_certificate_output
#   call: self::test_completed_certificate_output_contract_is_explicit
#   mutates: none
#   cleanup: none
#
# id: check_based_traversal_contract_receipt_replays
#   proves: based_traversal_contract_receipt_replays
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
    UCNS_RESEARCH_ROOT
    / "receipts"
    / "based-traversal-constructor-contract-v0.json"
)
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import based_traversal_constructor_contract as m


class BasedTraversalConstructorContractTest(unittest.TestCase):
    def test_exact_authority_and_predecessor_receipts_are_bound(self) -> None:
        source = m.receipt_payload()["source"]
        self.assertEqual(source["ucns_commit"], m.PINNED_UCNS_COMMIT)
        self.assertEqual(source["ucns_tree"], m.PINNED_UCNS_TREE)
        self.assertEqual(
            source["geometry_selection_receipt_sha256"],
            "4c4f06aae237fd4ce771dc7849738617b0cbc9ab3cc5bd6685ffec84b2921a09",
        )
        self.assertEqual(
            source["provenance_history_receipt_sha256"],
            "ed08c5315ab7dc6988985455d7226ced9151481883b7b8bbb0050ffc2bbc82e2",
        )
        for item in source["source_file_digests"]:
            path = m._stack_root() / item["path"]
            self.assertEqual(sha256(path.read_bytes()).hexdigest(), item["sha256"])

    def test_five_fields_have_exact_dependency_order(self) -> None:
        requirements = m.field_requirements()
        self.assertEqual(tuple(item.field for item in requirements), m.FIELD_ORDER)
        self.assertEqual(requirements[0].prerequisites, ())
        self.assertEqual(requirements[1].prerequisites, ("origin_attachment",))
        self.assertEqual(
            requirements[2].prerequisites,
            ("origin_attachment", "directed_tangent_or_chirality"),
        )
        self.assertEqual(requirements[3].prerequisites, ("rotation_system",))
        self.assertEqual(
            requirements[4].prerequisites,
            (
                "origin_attachment",
                "directed_tangent_or_chirality",
                "rotation_system",
                "marked_outgoing_dart",
            ),
        )
        for requirement in requirements:
            self.assertEqual(requirement.forbidden_substitutes, m.FORBIDDEN_SELECTION_BASES)

    def test_source_order_derivation_is_rejected(self) -> None:
        derivation = m.FieldDerivation(
            field="origin_attachment",
            authority="The-Interdependency/ucns",
            ucns_commit=m.PINNED_UCNS_COMMIT,
            operation_id="invented.source-order-attachment",
            source_paths=("src/ucns/public_gonol.py",),
            selection_basis="source text order",
            input_binding_sha256="0" * 64,
            output_payload={"target": "caller-selected"},
            replay_sha256="0" * 64,
        )
        with self.assertRaisesRegex(
            m.ConstructorContractError,
            "not selected by intrinsic UCNS geometry",
        ):
            m._verify_derivation(m.field_requirements()[0], derivation)
        self.assertEqual(m.registered_derivations(), ())

    def test_origin_primitives_do_not_become_attachment(self) -> None:
        origin = m.origin_primitive_evidence()
        self.assertEqual(origin.public_gonol_index, 0)
        self.assertEqual(origin.public_gonol_glyph, " ")
        self.assertEqual(origin.direct_structural_null_carrier_position, 0)
        self.assertTrue(origin.carrier_structural_null_coordinate_free)
        self.assertIsNone(origin.origin_to_groupoid_attachment)
        self.assertEqual(
            origin.status,
            "ORIGIN_PRIMITIVES_PRESENT__ATTACHMENT_ABSENT",
        )

    def test_first_missing_field_stops_all_downstream_evaluation(self) -> None:
        result = m.construct()
        self.assertEqual(result.status, "STOP_MISSING_ORIGIN_ATTACHMENT")
        self.assertEqual(result.stop_field, "origin_attachment")
        self.assertEqual(result.hmmm["field"], "origin_attachment")
        self.assertEqual(result.evaluations[0].status, m.MISSING_STATUS)
        self.assertTrue(
            all(item.status == m.BLOCKED_STATUS for item in result.evaluations[1:])
        )
        self.assertIsNone(result.constructor_certificate)
        self.assertIsNone(result.traversal_word)
        self.assertIsNone(result.attaching_word)
        self.assertIsNone(result.monodromy)
        self.assertIsNone(result.arithmetic_readout)
        self.assertIsNone(result.successor)
        self.assertFalse(result.to_payload()["pcea_handoff_permitted"])

        source = Path(m.__file__).read_text(encoding="utf-8")
        for forbidden_number in ("2881", "54837698421", "164513086777"):
            self.assertNotIn(forbidden_number, source)

    def test_completed_certificate_output_contract_is_explicit(self) -> None:
        contract = m.certificate_output_contract()
        self.assertTrue(contract["emitted_only_when_all_fields_ready"])
        self.assertEqual(tuple(contract["required_field_order"]), m.FIELD_ORDER)
        self.assertIn("traversal_word", contract["required_outputs"])
        self.assertIn("certificate_sha256", contract["required_outputs"])
        self.assertIn("replay_sha256", contract["required_field_evidence"])
        self.assertIn("ucns_commit", contract["required_authority_bindings"])

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
