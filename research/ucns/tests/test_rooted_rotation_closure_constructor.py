"""Adversarial witnesses for rooted rotation/closure and successor gating."""

# === CHECKS ===
# id: check_rooted_constructor_preserves_retained_structure
#   proves: rooted_constructor_preserves_retained_structure
#   call: self::test_retained_structure_preserves_coefficients_order_multiplicity_and_provenance
#   mutates: none
#   cleanup: none
#
# id: check_rooted_constructor_names_every_added_assumption
#   proves: rooted_constructor_names_every_added_assumption
#   call: self::test_five_fields_are_explicit_assumptions
#   mutates: none
#   cleanup: none
#
# id: check_rooted_constructor_uses_actual_complete_return_geometry
#   proves: rooted_constructor_uses_actual_complete_return_geometry
#   call: self::test_role_bindings_are_exact_complete_return_loops
#   mutates: none
#   cleanup: none
#
# id: check_rooted_constructor_closes_by_face_permutation
#   proves: rooted_constructor_closes_by_face_permutation
#   call: self::test_face_successor_closes_every_dart_once
#   mutates: none
#   cleanup: none
#
# id: check_rooted_constructor_exposes_rotation_ambiguity
#   proves: rooted_constructor_exposes_rotation_ambiguity
#   call: self::test_two_coherent_rotations_disagree_exactly
#   mutates: none
#   cleanup: none
#
# id: check_rooted_constructor_does_not_manufacture_prime_selector
#   proves: rooted_constructor_does_not_manufacture_prime_selector
#   call: self::test_cellular_readout_has_no_prime_selector
#   mutates: none
#   cleanup: none
#
# id: check_rooted_constructor_replays_byte_identically
#   proves: rooted_constructor_replays_byte_identically
#   call: self::test_constructor_receipt_replays_byte_identically
#   mutates: none
#   cleanup: none
#
# id: check_rooted_successor_gate_freezes_before_observations
#   proves: rooted_successor_gate_freezes_before_observations
#   call: self::test_constructor_freeze_contains_no_observed_targets
#   mutates: none
#   cleanup: none
#
# id: check_rooted_successor_gate_preserves_observed_R
#   proves: rooted_successor_gate_preserves_observed_R
#   call: self::test_observed_retained_records_are_complete
#   mutates: none
#   cleanup: none
#
# id: check_rooted_successor_gate_stops_failed_recursion
#   proves: rooted_successor_gate_stops_failed_recursion
#   call: self::test_frozen_successor_candidates_falsify_and_stop
#   mutates: none
#   cleanup: none
#
# id: check_rooted_successor_gate_separates_geometry_from_security
#   proves: rooted_successor_gate_separates_geometry_from_security
#   call: self::test_security_standing_remains_separate
#   mutates: none
#   cleanup: none
#
# id: check_rooted_successor_gate_receipts_replay
#   proves: rooted_successor_gate_receipts_replay
#   call: self::test_gate_receipts_replay_byte_identically
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys
import unittest


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH_ROOT))

import ordered_complete_return_groupoid as return_groupoid
import rooted_rotation_closure_constructor as constructor
import rooted_rotation_successor_gate as gate


class RootedRotationClosureConstructorTest(unittest.TestCase):
    def _rank_two(self, primes: tuple[int, int] = (5, 7)) -> constructor.RetainedStructure:
        return constructor.retained_structure(
            "test-rank-two",
            primes,
            provenance=("unit-test-retained-provenance",),
        )

    def _certificates(self) -> tuple[constructor.RootedRibbonCertificate, ...]:
        state = self._rank_two()
        return tuple(
            constructor.construct(
                state,
                assumption,
                rotation_relation_id=state.relations[0].relation_id,
            )
            for assumption in constructor.frozen_assumptions()
        )

    def test_retained_structure_preserves_coefficients_order_multiplicity_and_provenance(self) -> None:
        repeated = self._rank_two((5, 5))
        self.assertEqual(repeated.coefficients, (1, 10, 25))
        self.assertEqual(tuple(role.prime for role in repeated.roles), (5, 5))
        self.assertNotEqual(repeated.roles[0].occurrence_id, repeated.roles[1].occurrence_id)
        self.assertEqual(
            repeated.relations[0].participant_occurrences,
            tuple(role.occurrence_id for role in repeated.roles),
        )
        self.assertIn("unit-test-retained-provenance", repeated.provenance)

        left = self._rank_two((3, 11))
        right = self._rank_two((5, 7))
        self.assertEqual(left.c_at_one, right.c_at_one)
        self.assertNotEqual(left.coefficients, right.coefficients)
        self.assertNotEqual(left.digest, right.digest)

    def test_five_fields_are_explicit_assumptions(self) -> None:
        certificate = self._certificates()[0]
        fields = certificate.to_payload()["five_field_audit"]
        self.assertEqual(tuple(fields), (
            "origin_attachment",
            "directed_tangent_or_chirality",
            "rotation_system",
            "marked_outgoing_dart",
            "closure_rule",
        ))
        self.assertIn("ASSUMPTION", fields["origin_attachment"]["status"])
        self.assertIn("ASSUMPTION", fields["marked_outgoing_dart"]["status"])
        self.assertEqual(
            fields["directed_tangent_or_chirality"]["native_transition_law"],
            constructor.NATIVE_TRANSITION_LAW,
        )

    def test_role_bindings_are_exact_complete_return_loops(self) -> None:
        state = self._rank_two()
        groupoid = return_groupoid.build_ordered_return_groupoid(2)
        self.assertEqual(
            {role.geometry_relation_id for role in state.roles},
            {generator.relation_id for generator in groupoid.generators},
        )
        for role in state.roles:
            path = groupoid.complete_loop_path(role.geometry_relation_id)
            self.assertTrue(path.is_loop)
            self.assertEqual(len(path.steps), 2)

    def test_face_successor_closes_every_dart_once(self) -> None:
        for certificate in self._certificates():
            visited = [dart for cycle in certificate.face_cycles for dart in cycle]
            self.assertEqual(len(visited), 4)
            self.assertEqual(len(set(visited)), 4)
            self.assertEqual(set(visited), set(certificate.rotation_cycle))
            self.assertEqual(certificate.traversal_word[0], certificate.marked_dart)

    def test_two_coherent_rotations_disagree_exactly(self) -> None:
        paired, blocked = self._certificates()
        self.assertEqual(paired.structure.digest, blocked.structure.digest)
        self.assertEqual(paired.assumptions.chirality, blocked.assumptions.chirality)
        self.assertNotEqual(paired.face_cycles, blocked.face_cycles)
        self.assertEqual((len(paired.face_cycles), paired.genus), (3, 0))
        self.assertEqual((len(blocked.face_cycles), blocked.genus), (1, 1))
        self.assertEqual(paired.finite_cokernel_order, 1)
        self.assertIsNone(blocked.finite_cokernel_order)

        reversed_assumption = replace(paired.assumptions, assumption_id="test-reversed", chirality=-1)
        reversed_certificate = constructor.construct(
            paired.structure,
            reversed_assumption,
            rotation_relation_id=paired.relation_id,
        )
        self.assertNotEqual(paired.face_successor, reversed_certificate.face_successor)
        self.assertNotEqual(paired.digest, reversed_certificate.digest)

    def test_shuffled_storage_alternative_primes_and_ordered_relation_controls(self) -> None:
        state = self._rank_two()
        assumption = constructor.frozen_assumptions()[0]
        baseline = constructor.construct(
            state,
            assumption,
            rotation_relation_id=state.relations[0].relation_id,
        )

        storage_shuffled = replace(state, roles=tuple(reversed(state.roles)))
        storage_result = constructor.construct(
            storage_shuffled,
            assumption,
            rotation_relation_id=storage_shuffled.relations[0].relation_id,
        )
        self.assertEqual(baseline.rotation_cycle, storage_result.rotation_cycle)
        self.assertEqual(baseline.face_cycles, storage_result.face_cycles)
        self.assertEqual(baseline.genus, storage_result.genus)
        self.assertEqual(
            storage_result.cellular_boundary_matrix,
            tuple(tuple(reversed(row)) for row in baseline.cellular_boundary_matrix),
        )

        alternative_primes = self._rank_two((13, 17))
        alternative_result = constructor.construct(
            alternative_primes,
            assumption,
            rotation_relation_id=alternative_primes.relations[0].relation_id,
        )
        self.assertEqual(baseline.face_cycles, alternative_result.face_cycles)
        self.assertEqual(baseline.finite_cokernel_order, alternative_result.finite_cokernel_order)
        self.assertNotEqual(baseline.structure.coefficients, alternative_result.structure.coefficients)

        reversed_relation = replace(
            state.relations[0],
            participant_occurrences=tuple(reversed(state.relations[0].participant_occurrences)),
        )
        relation_shuffled = replace(state, relations=(reversed_relation,))
        relation_result = constructor.construct(
            relation_shuffled,
            assumption,
            rotation_relation_id=reversed_relation.relation_id,
        )
        self.assertNotEqual(baseline.rotation_cycle, relation_result.rotation_cycle)
        self.assertNotEqual(baseline.digest, relation_result.digest)

    def test_cellular_readout_has_no_prime_selector(self) -> None:
        for certificate in self._certificates():
            readout = certificate.to_payload()["cellular_readout"]
            self.assertIsNone(readout["successor_selector"])
            self.assertIsNone(readout["supplied_next_prime"])
            self.assertIn(readout["finite_cokernel_order"], (None, 1))
            self.assertEqual(readout["factorization"], [])

    def test_constructor_receipt_replays_byte_identically(self) -> None:
        first = constructor.receipt_payload()
        second = constructor.receipt_payload()
        self.assertEqual(first, second)
        self.assertEqual(constructor.receipt_bytes(first), constructor.receipt_bytes(second))
        self.assertEqual(constructor.receipt_digest(first), constructor.receipt_digest(second))
        self.assertTrue(first["rotation_ambiguity"]["different_face_cycles"])
        self.assertTrue(first["rotation_ambiguity"]["different_genus"])

    def test_constructor_freeze_contains_no_observed_targets(self) -> None:
        frozen = gate.freeze_payload()
        self.assertIsNone(frozen["observed_values"])
        self.assertIsNone(frozen["observed_factors"])
        self.assertNotIn("157", Path(constructor.__file__).read_text(encoding="utf-8"))
        self.assertNotIn("2881", Path(constructor.__file__).read_text(encoding="utf-8"))
        self.assertNotIn("54837698421", Path(constructor.__file__).read_text(encoding="utf-8"))
        self.assertEqual(gate.freeze_digest(), gate.freeze_digest())

    def test_observed_retained_records_are_complete(self) -> None:
        payload = gate.audit_payload()
        by_candidate = payload["candidate_diagnostics"]
        for candidate in by_candidate:
            diagnostics = candidate["scale_diagnostics_not_recursive_predictions"]
            self.assertEqual([item["complete_product"] for item in diagnostics], [
                observation.cardinality for observation in gate.OBSERVATIONS
            ])
            self.assertEqual([len(item["coefficients"]) - 1 for item in diagnostics], [1, 2, 3])
            self.assertTrue(all(item["retained_structure_sha256"] for item in diagnostics))

    def test_frozen_successor_candidates_falsify_and_stop(self) -> None:
        payload = gate.audit_payload()
        for result in payload["recursive_successor_gate"]:
            self.assertEqual(result["derived_cellular_order"], 1)
            self.assertEqual(result["verdict"], "FALSIFIED")
            self.assertFalse(result["second_recursive_transition_executed"])
            self.assertIsNone(result["next_prediction"])
        self.assertEqual(payload["verdicts"]["canonical_ucns_based_traversal"], "UNRESOLVED")
        self.assertEqual(payload["verdicts"]["ucns_prime_successor_selector"], "UNRESOLVED")

    def test_security_standing_remains_separate(self) -> None:
        verdicts = gate.audit_payload()["verdicts"]
        self.assertEqual(verdicts["explicit_assumption_ribbon_constructor"], "SURVIVED_LOCALLY")
        self.assertEqual(verdicts["minimal_fourth_power_trapdoor"], "FALSIFIED")
        self.assertEqual(verdicts["pcea_cryptographic_security"], "FALSIFIED")

    def test_gate_receipts_replay_byte_identically(self) -> None:
        first = gate.audit_payload()
        second = gate.audit_payload()
        self.assertEqual(first, second)
        self.assertEqual(gate.receipt_bytes(first), gate.receipt_bytes(second))
        self.assertEqual(gate.receipt_digest(first), gate.receipt_digest(second))
        self.assertEqual(gate.render_markdown(first), gate.render_markdown(second))

    def test_adversarial_missing_or_malformed_structure_fails_closed(self) -> None:
        state = self._rank_two()
        assumption = constructor.frozen_assumptions()[0]
        with self.assertRaises(constructor.ConstructorError):
            constructor.construct(state, assumption, rotation_relation_id="missing")
        with self.assertRaises(constructor.ConstructorError):
            replace(assumption, assumption_id="bad-chirality", chirality=0)
        with self.assertRaises(constructor.ConstructorError):
            replace(state, provenance=())
        with self.assertRaises(constructor.ConstructorError):
            replace(state, roles=(state.roles[0], state.roles[0]))


if __name__ == "__main__":
    unittest.main()
