"""Executable witnesses for the event/trace lift candidate."""

# === CHECKS ===
# id: check_event_trace_lift_binds_pinned_seed_geometry
#   proves: event_trace_lift_binds_pinned_seed_geometry
#   call: self::test_source_geometry_is_exact_and_pinned
#   mutates: none
#   cleanup: none
#
# id: check_event_trace_lift_recovers_seed_build_orders
#   proves: event_trace_lift_recovers_seed_build_orders
#   call: self::test_seed_graph_has_exactly_six_factorial_build_orders
#   mutates: none
#   cleanup: none
#
# id: check_event_trace_lift_matches_are_retrodictive_only
#   proves: event_trace_lift_matches_are_retrodictive_only
#   call: self::test_first_two_identities_are_retrodictive_not_survivors
#   mutates: none
#   cleanup: none
#
# id: check_event_trace_lift_continuations_are_unchanged_and_falsifiable
#   proves: event_trace_lift_continuations_are_unchanged_and_falsifiable
#   call: self::test_unchanged_continuations_have_frozen_outputs_and_no_target_constants
#   mutates: none
#   cleanup: none
#
# id: check_event_trace_lift_has_no_survivor_without_second_geometry
#   proves: event_trace_lift_has_no_survivor_without_second_geometry
#   call: self::test_no_continuation_survives_or_predicts
#   mutates: none
#   cleanup: none
#
# id: check_event_trace_lift_receipt_replays_byte_identical
#   proves: event_trace_lift_receipt_replays_byte_identical
#   call: self::test_receipt_replays_byte_identical
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from hashlib import sha256
import inspect
import json
from pathlib import Path
import sys
import types
import unittest


UCNS_RESEARCH_ROOT = Path(__file__).resolve().parents[1]
COMMITTED_RECEIPT = UCNS_RESEARCH_ROOT / "receipts" / "event-trace-lift-candidate-v0.json"
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import event_trace_lift_candidate as m


def _constants(code: types.CodeType) -> set[object]:
    values: set[object] = set()
    for value in code.co_consts:
        if isinstance(value, types.CodeType):
            values.update(_constants(value))
        else:
            values.add(value)
    return values


class EventTraceLiftCandidateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.geometry = m.load_seed_geometry()
        cls.result = m.evaluate()

    def test_source_geometry_is_exact_and_pinned(self) -> None:
        geometry = self.geometry
        self.assertEqual(geometry.base_commit, m.PINNED_UCNS_COMMIT)
        self.assertEqual(geometry.public_gonol_arity, 157)
        self.assertEqual(geometry.public_gonol_sha256, m.PINNED_PUBLIC_GONOL_SHA256)
        self.assertEqual(len(geometry.bands), 7)
        self.assertEqual(geometry.pair_relation_count, 21)
        self.assertEqual(geometry.structural_relation_count, 12)
        self.assertEqual(len(geometry.projection_node_incidence), 13)
        self.assertEqual(geometry.pairwise_projection_event_count, 39)
        self.assertEqual(geometry.boundary_multiplicity, 4)
        self.assertEqual(geometry.total_declared_structural_boundary_events, 48)
        self.assertTrue(all(len(digest) == 64 for _, digest in geometry.source_file_digests))

    def test_seed_graph_has_exactly_six_factorial_build_orders(self) -> None:
        vertices, edges, root = m._seed_graph(self.geometry)
        self.assertEqual(len(vertices), 7)
        self.assertEqual(len(edges), 12)
        self.assertEqual(root, "CENTER")
        self.assertEqual(m.count_connected_build_orders(vertices, edges, root), 720)

    def test_first_two_identities_are_retrodictive_not_survivors(self) -> None:
        result = self.result
        self.assertEqual(result.status, m.STATUS_RETRODICTIVE_MATCH)
        self.assertEqual(result.event_state_count, 39)
        self.assertEqual(result.event_lifted_cardinality, 157)
        self.assertTrue(result.public_arity_match)
        self.assertEqual(result.seed_construction_trace_count, 720)
        self.assertEqual(result.trace_lifted_cardinality, 2881)
        self.assertTrue(result.first_successor_match)
        self.assertIn("post-observation", m.STANDING)

    def test_unchanged_continuations_have_frozen_outputs_and_no_target_constants(self) -> None:
        by_id = {result.candidate_id: result for result in self.result.continuations}
        self.assertEqual(
            by_id["radius_two_hex_disk"].construction_trace_count,
            97934946851520,
        )
        self.assertEqual(
            by_id["radius_two_hex_disk"].lifted_cardinality,
            391739787406081,
        )
        self.assertEqual(
            by_id["structural_relation_incidence"].construction_trace_count,
            3625881589440,
        )
        self.assertEqual(
            by_id["structural_relation_incidence"].lifted_cardinality,
            14503526357761,
        )
        self.assertEqual(
            by_id["projection_node_incidence"].construction_trace_count,
            648016379781120,
        )
        self.assertEqual(
            by_id["projection_node_incidence"].lifted_cardinality,
            2592065519124481,
        )

        forbidden = set(m.OBSERVED_GONOLS[1:])
        for operation in (
            m.count_connected_build_orders,
            m.fourfold_origin_lift,
            m._radius_two_hex_graph,
            m._structural_incidence_graph,
            m._projection_incidence_graph,
        ):
            unwrapped = inspect.unwrap(operation)
            self.assertTrue(forbidden.isdisjoint(_constants(unwrapped.__code__)), operation.__name__)

    def test_no_continuation_survives_or_predicts(self) -> None:
        result = self.result
        self.assertEqual(result.third_observation_state_quotient, 13709424605)
        self.assertEqual(result.constructor_survivor_count, 0)
        self.assertFalse(any(item.target_match for item in result.continuations))
        self.assertTrue(all(item.standing == m.STATUS_FALSIFIED for item in result.continuations))
        self.assertIsNone(result.next_prediction)
        self.assertTrue(any("completed 2881-gonol" in item for item in result.hmmm))

    def test_receipt_replays_byte_identical(self) -> None:
        first = m.receipt_bytes()
        second = m.receipt_bytes()
        self.assertEqual(first, second)
        self.assertEqual(m.receipt_digest(), sha256(first).hexdigest())
        payload = json.loads(first)
        self.assertEqual(payload["comparison"]["constructor_survivor_count"], 0)
        self.assertIsNone(payload["comparison"]["next_prediction"])
        self.assertEqual(payload["comparison"]["status"], m.STATUS_RETRODICTIVE_MATCH)

        committed = json.loads(COMMITTED_RECEIPT.read_text(encoding="utf-8"))
        committed_digest = committed.pop("receipt_sha256")
        self.assertEqual(committed_digest, m.receipt_digest())
        self.assertEqual(committed, payload)


if __name__ == "__main__":
    unittest.main()
