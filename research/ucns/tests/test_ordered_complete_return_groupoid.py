"""Executable witnesses for the ordered complete-return path groupoid."""

# === CHECKS ===
# id: check_ordered_return_groupoid_lifts_exact_trace
#   proves: ordered_return_groupoid_lifts_exact_trace
#   call: self::test_exact_trace_halves_and_midpoints_are_retained
#   mutates: none
#   cleanup: none
#
# id: check_ordered_return_groupoid_has_free_rank_r
#   proves: ordered_return_groupoid_has_free_rank_r
#   call: self::test_subdivided_bouquet_has_declared_free_rank
#   mutates: none
#   cleanup: none
#
# id: check_ordered_return_groupoid_preserves_composition_order
#   proves: ordered_return_groupoid_preserves_composition_order
#   call: self::test_typed_paths_reduce_inverses_without_commuting
#   mutates: none
#   cleanup: none
#
# id: check_ordered_return_groupoid_preserves_basepoint_and_orientation
#   proves: ordered_return_groupoid_preserves_basepoint_and_orientation
#   call: self::test_shifted_loop_requires_explicit_basepoint_transport
#   mutates: none
#   cleanup: none
#
# id: check_ordered_return_groupoid_abelianizes_explicitly
#   proves: ordered_return_groupoid_abelianizes_explicitly
#   call: self::test_distinct_ordered_words_collapse_only_under_abelianization
#   mutates: none
#   cleanup: none
#
# id: check_ordered_return_groupoid_quantifies_closure_order
#   proves: ordered_return_groupoid_quantifies_closure_order
#   call: self::test_based_and_oriented_cyclic_counts
#   mutates: none
#   cleanup: none
#
# id: check_ordered_return_groupoid_is_target_free
#   proves: ordered_return_groupoid_is_target_free
#   call: self::test_constructor_contains_no_observation_or_factor_inputs
#   mutates: none
#   cleanup: none
#
# id: check_ordered_return_groupoid_receipt_replays
#   proves: ordered_return_groupoid_receipt_replays
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
COMMITTED_RECEIPT = UCNS_RESEARCH_ROOT / "receipts" / "ordered-complete-return-groupoid-v0.json"
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import complete_return_relation_extension as extension
import ordered_complete_return_groupoid as m


class OrderedCompleteReturnGroupoidTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.groupoid = m.build_ordered_return_groupoid(4)

    def test_exact_trace_halves_and_midpoints_are_retained(self) -> None:
        generated = extension.iterate_complete_return(
            4,
            scale_prefix="ordered-return-groupoid-scale",
        )
        self.assertEqual(
            tuple(item.relation_id for item in self.groupoid.generators),
            tuple(item.new_relation_id for item in generated),
        )
        self.assertEqual(len({item.midpoint_object for item in self.groupoid.generators}), 4)
        self.assertEqual(len({item.trace_sha256 for item in self.groupoid.generators}), 1)
        for generator in self.groupoid.generators:
            outbound = next(edge for edge in self.groupoid.edges if edge.edge_id == generator.outbound_edge_id)
            returning = next(edge for edge in self.groupoid.edges if edge.edge_id == generator.return_edge_id)
            self.assertEqual(
                (outbound.source, outbound.target),
                (self.groupoid.base_object, generator.midpoint_object),
            )
            self.assertEqual(
                (returning.source, returning.target),
                (generator.midpoint_object, self.groupoid.base_object),
            )

    def test_subdivided_bouquet_has_declared_free_rank(self) -> None:
        for rank in range(1, 5):
            groupoid = m.build_ordered_return_groupoid(rank)
            self.assertEqual(len(groupoid.objects), rank + 1)
            self.assertEqual(len(groupoid.edges), 2 * rank)
            self.assertEqual(groupoid.boundary_rank, rank)
            self.assertEqual(groupoid.first_betti_rank, rank)
            self.assertEqual(groupoid.to_payload()["graph"]["fundamental_group_candidate"], f"F_{rank}")
            self.assertEqual(groupoid.to_payload()["graph"]["abelianization"], f"Z^{rank}")

    def test_typed_paths_reduce_inverses_without_commuting(self) -> None:
        x = self.groupoid.word_from_ordinals((1,))
        y = self.groupoid.word_from_ordinals((2,))
        xy = x.multiply(y)
        yx = y.multiply(x)
        self.assertNotEqual(xy, yx)
        self.assertNotEqual(self.groupoid.word_path(xy), self.groupoid.word_path(yx))

        identity = self.groupoid.word_from_ordinals((1, 2, -2, -1))
        self.assertTrue(identity.is_identity)
        self.assertEqual(self.groupoid.word_path(identity).steps, ())

        complete = self.groupoid.complete_loop_path(self.groupoid.generators[0].relation_id)
        shifted = self.groupoid.shifted_loop_path(self.groupoid.generators[0].relation_id)
        with self.assertRaises(m.OrderedReturnGroupoidError):
            self.groupoid.compose_paths(complete, shifted)

    def test_shifted_loop_requires_explicit_basepoint_transport(self) -> None:
        relation_id = self.groupoid.generators[0].relation_id
        complete = self.groupoid.complete_loop_path(relation_id)
        shifted = self.groupoid.shifted_loop_path(relation_id)
        self.assertNotEqual(complete.source, shifted.source)
        self.assertNotEqual(complete, shifted)
        self.assertEqual(
            self.groupoid.transported_shifted_loop_path(relation_id),
            complete,
        )

    def test_distinct_ordered_words_collapse_only_under_abelianization(self) -> None:
        xyz = self.groupoid.word_from_ordinals((1, 2, 3))
        yzx = self.groupoid.word_from_ordinals((2, 3, 1))
        xzy = self.groupoid.word_from_ordinals((1, 3, 2))
        self.assertEqual(len({xyz, yzx, xzy}), 3)
        self.assertEqual(self.groupoid.abelianize(xyz), (1, 1, 1, 0))
        self.assertEqual(self.groupoid.abelianize(yzx), (1, 1, 1, 0))
        self.assertEqual(self.groupoid.abelianize(xzy), (1, 1, 1, 0))
        self.assertEqual(xyz.oriented_cyclic_key, yzx.oriented_cyclic_key)
        self.assertNotEqual(xyz.oriented_cyclic_key, xzy.oriented_cyclic_key)

    def test_based_and_oriented_cyclic_counts(self) -> None:
        expected = {
            1: (1, 1, 1),
            2: (2, 1, 1),
            3: (6, 2, 1),
            4: (24, 6, 1),
        }
        for rank, counts in expected.items():
            profile = m.permutation_order_profile(self.groupoid, rank)
            self.assertEqual(
                (
                    profile.based_word_count,
                    profile.oriented_cyclic_class_count,
                    profile.abelianization_class_count,
                ),
                counts,
            )

    def test_constructor_contains_no_observation_or_factor_inputs(self) -> None:
        source = Path(m.__file__).read_text(encoding="utf-8")
        for forbidden in (
            "54837698421",
            "164513086777",
            "1661748437",
            "squarefree_divisor_lattice_control",
            "relation_factor_bridge_obstructions",
        ):
            self.assertNotIn(forbidden, source)
        payload = m.receipt_payload()
        self.assertIsNone(payload["candidate"]["observed_successor_cardinality_input"])
        self.assertIsNone(payload["candidate"]["observed_arithmetic_factor_input"])
        self.assertIsNone(payload["current_arithmetic_factor_map"])
        self.assertIsNone(payload["numerical_next_gonol"])

    def test_receipt_replays_byte_identically(self) -> None:
        committed = json.loads(COMMITTED_RECEIPT.read_text(encoding="utf-8"))
        committed_digest = committed.pop("receipt_sha256")
        self.assertEqual(committed, m.receipt_payload())
        self.assertEqual(committed_digest, m.receipt_digest())
        self.assertEqual(
            committed_digest,
            sha256(m.receipt_bytes()).hexdigest(),
        )


if __name__ == "__main__":
    unittest.main()
