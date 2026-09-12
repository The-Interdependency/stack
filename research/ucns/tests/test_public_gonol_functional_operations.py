"""Executable witnesses for Public Gonol functional operations research."""

# === CHECKS ===
# id: check_public_gonol_operations_bind_pinned_carrier
#   proves: public_gonol_operations_bind_pinned_carrier
#   call: self::test_carrier_binds_pinned_ucns_public_gonol
#   mutates: none
#   cleanup: none
#
# id: check_public_gonol_operations_are_position_relations_not_glyph_semantics
#   proves: public_gonol_operations_are_position_relations_not_glyph_semantics
#   call: self::test_operations_use_position_maps_without_successor_or_semantic_inputs
#   mutates: none
#   cleanup: none
#
# id: check_public_gonol_operations_compose_as_total_carrier_functions
#   proves: public_gonol_operations_compose_as_total_carrier_functions
#   call: self::test_composition_identity_and_associativity
#   mutates: none
#   cleanup: none
#
# id: check_public_gonol_admissible_transformations_are_bijective
#   proves: public_gonol_admissible_transformations_are_bijective
#   call: self::test_admissible_transformations_require_bijection_and_shape
#   mutates: none
#   cleanup: none
#
# id: check_public_gonol_closure_receipts_are_deterministic
#   proves: public_gonol_closure_receipts_are_deterministic
#   call: self::test_closure_receipts_replay_byte_identically
#   mutates: none
#   cleanup: none
#
# id: check_public_gonol_participation_records_preserve_occurrence_identity
#   proves: public_gonol_participation_records_preserve_occurrence_identity
#   call: self::test_participation_record_preserves_occurrence_and_addresses
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import sys
import unittest


UCNS_RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import public_gonol_functional_operations as m


class PublicGonolFunctionalOperationsTest(unittest.TestCase):
    def test_carrier_binds_pinned_ucns_public_gonol(self) -> None:
        carrier = m.load_carrier()
        self.assertEqual(carrier.source_commit, m.PINNED_UCNS_COMMIT)
        self.assertEqual(carrier.source_repository, "The-Interdependency/ucns")
        self.assertEqual(carrier.public_gonol_sha256, m.PINNED_PUBLIC_GONOL_SHA256)
        self.assertEqual(carrier.arity, 157)
        self.assertEqual(carrier.origin, m.PublicGonolAddress(0, " "))
        self.assertEqual(len(carrier.addresses()), 157)
        self.assertEqual(len({address.glyph for address in carrier.addresses()}), 157)
        self.assertIn(
            "libs/ucns/src/ucns/public_gonol.py",
            {path for path, _digest in carrier.source_file_digests},
        )

    def test_operations_use_position_maps_without_successor_or_semantic_inputs(self) -> None:
        source = Path(m.__file__).read_text(encoding="utf-8")
        forbidden_observation = {"28" + "81", "548" + "37698421"}
        for value in forbidden_observation:
            self.assertNotIn(value, source)

        carrier = m.load_carrier()
        identity = m.identity_operation(carrier)
        shift = m.cyclic_order_motion(1, carrier)
        self.assertEqual(identity.apply("A"), carrier.address("A"))
        self.assertEqual(shift.apply(carrier.origin), carrier.address(1))
        self.assertEqual(shift.apply(carrier.address(156)), carrier.origin)
        self.assertEqual(shift.apply("A"), carrier.address(2))
        self.assertFalse(any("unicode_name" in key for key in m._operation_payload(shift)))

    def test_composition_identity_and_associativity(self) -> None:
        carrier = m.load_carrier()
        identity = m.identity_operation(carrier)
        one = m.cyclic_order_motion(1, carrier)
        two = m.cyclic_order_motion(2, carrier)
        five = m.cyclic_order_motion(5, carrier)

        self.assertEqual(m.compose_operations(identity, one).transform, one.transform)
        self.assertEqual(m.compose_operations(one, identity).transform, one.transform)
        self.assertEqual(m.compose_operations(one, two).transform, m.cyclic_order_motion(3, carrier).transform)

        left = m.compose_operations(m.compose_operations(one, two), five)
        right = m.compose_operations(one, m.compose_operations(two, five))
        self.assertEqual(left.transform, right.transform)
        for index in (0, 1, 80, 156):
            self.assertEqual(left.apply(index), right.apply(index))

    def test_admissible_transformations_require_bijection_and_shape(self) -> None:
        carrier = m.load_carrier()
        shift = m.cyclic_order_motion(-1, carrier)
        self.assertTrue(shift.is_bijective)
        self.assertTrue(shift.is_admissible_transformation)
        self.assertEqual(shift.apply(0), carrier.address(156))

        duplicate_zero = tuple(0 for _ in range(carrier.arity))
        explicit = m.PublicGonolOperation(
            operation_id="research.non_bijective_total_function",
            basis="explicit_total_carrier_function",
            standing="stack-local-candidate",
            carrier=carrier,
            transform=duplicate_zero,
        )
        self.assertFalse(explicit.is_bijective)
        self.assertFalse(explicit.is_admissible_transformation)
        with self.assertRaises(m.PublicGonolOperationError):
            m.close_operation(explicit)
        with self.assertRaises(m.PublicGonolOperationError):
            m.PublicGonolOperation(
                operation_id="bad.cyclic",
                basis="cyclic_order_motion",
                standing="stack-local-candidate",
                carrier=carrier,
                transform=duplicate_zero,
            )
        with self.assertRaises(m.PublicGonolOperationError):
            m.PublicGonolOperation(
                operation_id="bad.out_of_carrier",
                basis="explicit_total_carrier_function",
                standing="stack-local-candidate",
                carrier=carrier,
                transform=tuple(range(carrier.arity - 1)) + (carrier.arity,),
            )

    def test_closure_receipts_replay_byte_identically(self) -> None:
        carrier = m.load_carrier()
        operation = m.cyclic_order_motion(7, carrier)
        first = m.close_operation(operation)
        second = m.close_operation(m.cyclic_order_motion(7, carrier))
        self.assertEqual(first.receipt, second.receipt)
        self.assertEqual(first.digest, second.digest)
        self.assertEqual(first.receipt["closure"]["closed_over_positions"], 157)
        self.assertEqual(first.receipt["operation"]["mapping_sha256"], operation.mapping_sha256)
        self.assertTrue(any(
            item.startswith("later UCNS authority rejects cyclic order motion")
            for item in first.receipt["falsification_conditions"]
        ))

        payload = m.receipt_payload()
        self.assertEqual(m.receipt_bytes(payload), m.receipt_bytes(m.receipt_payload()))
        self.assertEqual(m.receipt_digest(payload), sha256(m.receipt_bytes(payload)).hexdigest())

    def test_participation_record_preserves_occurrence_and_addresses(self) -> None:
        carrier = m.load_carrier()
        operation = m.cyclic_order_motion(1, carrier)
        record = m.participation_record(
            operation,
            "A",
            "occurrence-A-0",
            "public-gonol-functional-operation-test",
        )
        payload = record.as_payload()
        self.assertEqual(payload["occurrence_id"], "occurrence-A-0")
        self.assertEqual(payload["relation_context"], "public-gonol-functional-operation-test")
        self.assertEqual(payload["input"], {"index": 1, "glyph": "A"})
        self.assertEqual(payload["output"], {"index": 2, "glyph": "!"})
        self.assertEqual(payload["carrier_digest"], m.PINNED_PUBLIC_GONOL_SHA256)
        self.assertEqual(record.digest, sha256(m._canonical_bytes(payload)).hexdigest())

        with self.assertRaises(m.PublicGonolOperationError):
            m.participation_record(operation, "A", "", "context")
        with self.assertRaises(m.PublicGonolOperationError):
            m.participation_record(operation, "A", "occurrence-A-0", "")


if __name__ == "__main__":
    unittest.main()
