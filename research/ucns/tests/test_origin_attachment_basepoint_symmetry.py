"""Executable witnesses for the origin-attachment basepoint symmetry audit."""

# === CHECKS ===
# id: check_basepoint_symmetry_binds_exact_authority
#   proves: basepoint_symmetry_binds_exact_authority
#   call: self::test_exact_authority_and_predecessor_receipts_are_bound
#   mutates: none
#   cleanup: none
#
# id: check_basepoint_symmetry_defines_candidate
#   proves: basepoint_symmetry_defines_exact_candidate
#   call: self::test_candidate_is_exact_unframed_visible_action_groupoid
#   mutates: none
#   cleanup: none
#
# id: check_basepoint_symmetry_enumerates_objects
#   proves: basepoint_symmetry_enumerates_unframed_objects
#   call: self::test_unframed_object_enumeration_is_exact_and_unmarked
#   mutates: none
#   cleanup: none
#
# id: check_basepoint_symmetry_automorphism_group
#   proves: basepoint_symmetry_derives_exact_automorphism_group
#   call: self::test_translations_form_exact_label_preserving_action
#   mutates: none
#   cleanup: none
#
# id: check_basepoint_symmetry_orbit_partition
#   proves: basepoint_symmetry_partitions_one_transitive_orbit
#   call: self::test_all_objects_form_one_simply_transitive_orbit
#   mutates: none
#   cleanup: none
#
# id: check_basepoint_symmetry_rejects_phase_zero
#   proves: basepoint_symmetry_rejects_phase_zero_default
#   call: self::test_half_turn_moves_phase_zero_and_every_replay_object
#   mutates: none
#   cleanup: none
#
# id: check_basepoint_symmetry_rejects_bouquet
#   proves: basepoint_symmetry_rejects_circular_bouquet_base
#   call: self::test_bouquet_degree_witness_is_circular_and_not_canon
#   mutates: none
#   cleanup: none
#
# id: check_basepoint_symmetry_minimum_structure
#   proves: basepoint_symmetry_identifies_minimum_new_structure
#   call: self::test_one_geometric_zero_cell_mark_breaks_translation_group
#   mutates: none
#   cleanup: none
#
# id: check_basepoint_symmetry_stops_without_iota
#   proves: basepoint_symmetry_stops_without_iota
#   call: self::test_transitive_outcome_emits_no_iota_or_downstream_evaluation
#   mutates: none
#   cleanup: none
#
# id: check_basepoint_symmetry_receipt_replays
#   proves: basepoint_symmetry_receipt_replays
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
COMMITTED_RECEIPT = (
    UCNS_RESEARCH_ROOT
    / "receipts"
    / "origin-attachment-basepoint-symmetry-v0.json"
)
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import origin_attachment_basepoint_symmetry as m


class OriginAttachmentBasepointSymmetryTest(unittest.TestCase):
    def test_exact_authority_and_predecessor_receipts_are_bound(self) -> None:
        source = m.receipt_payload()["source"]
        self.assertEqual(source["ucns_commit"], m.PINNED_UCNS_COMMIT)
        self.assertEqual(source["ucns_tree"], m.PINNED_UCNS_TREE)
        self.assertEqual(
            source["origin_attachment_canon_gap_receipt_sha256"],
            m.ORIGIN_GAP_RECEIPT_SHA256,
        )
        self.assertEqual(
            source["ordered_groupoid_candidate_receipt_sha256"],
            m.ORDERED_GROUPOID_RECEIPT_SHA256,
        )
        self.assertFalse(source["network_used"])
        for item in source["source_file_digests"]:
            path = m._stack_root() / item["path"]
            self.assertEqual(sha256(path.read_bytes()).hexdigest(), item["sha256"])

    def test_candidate_is_exact_unframed_visible_action_groupoid(self) -> None:
        structure = m.candidate_traversable_structure()
        self.assertEqual(structure.structure_id, m.STRUCTURE_ID)
        self.assertEqual(structure.object_set, "V(T) = Q/Z")
        self.assertIn("d in Q", structure.morphism_set)
        self.assertTrue(structure.unframed)
        self.assertFalse(structure.structural_null_is_object)
        self.assertFalse(structure.phase_zero_intrinsically_marked)

        start = m.UnframedBaseObject.from_phase(Fraction(5, 6))
        first = m.UnframedPath.from_displacement(start, Fraction(1, 2))
        second = m.UnframedPath.from_displacement(first.target, Fraction(-1, 3))
        composite = first.then(second)
        self.assertEqual(composite.source, start)
        self.assertEqual(composite.displacement, Fraction(1, 6))
        self.assertEqual(composite.target, second.target)

    def test_unframed_object_enumeration_is_exact_and_unmarked(self) -> None:
        objects = m.enumerate_unframed_base_objects(8)
        self.assertEqual(len(objects), 22)
        self.assertEqual(len(set(objects)), len(objects))
        self.assertIn(m.UnframedBaseObject.from_phase(0), objects)
        self.assertTrue(all(Fraction(0) <= item.phase < Fraction(1) for item in objects))
        self.assertEqual(
            m.UnframedBaseObject.from_phase(Fraction(17, 6)),
            m.UnframedBaseObject.from_phase(Fraction(5, 6)),
        )
        structure = m.candidate_traversable_structure().to_payload()
        self.assertTrue(structure["objects"]["all_objects_admissible"])
        self.assertIsNone(structure["objects"]["excluded_or_marked_phase"])

    def test_translations_form_exact_label_preserving_action(self) -> None:
        objects = m.enumerate_unframed_base_objects(6)
        identity = m.TranslationAutomorphism.from_offset(0)
        for source in objects:
            self.assertEqual(identity.apply_object(source), source)
            for target in objects:
                move = m.transporter(source, target)
                self.assertEqual(move.apply_object(source), target)
                self.assertEqual(
                    move.then(move.inverse()).apply_object(source),
                    source,
                )
                path = m.UnframedPath.from_displacement(source, Fraction(7, 5))
                moved = move.apply_path(path)
                self.assertEqual(moved.displacement, path.displacement)
                self.assertEqual(moved.target, move.apply_object(path.target))

        witness = m.automorphism_group_witness()
        self.assertEqual(witness.exact_group, "Q/Z under addition")
        self.assertTrue(witness.action_free)
        self.assertTrue(witness.action_transitive)

    def test_all_objects_form_one_simply_transitive_orbit(self) -> None:
        partition = m.orbit_partition()
        self.assertEqual(partition.orbit_count, 1)
        self.assertEqual(partition.orbits, ("Q/Z",))
        self.assertTrue(partition.unique_orbit)
        self.assertFalse(partition.unique_object_within_orbit)
        self.assertEqual(partition.globally_fixed_objects, ())
        self.assertIsNone(partition.canonical_orbit_section)
        self.assertEqual(partition.outcome, m.STATUS)

    def test_half_turn_moves_phase_zero_and_every_replay_object(self) -> None:
        phase_zero = m.UnframedBaseObject.from_phase(0)
        half_turn = m.TranslationAutomorphism.from_offset(Fraction(1, 2))
        self.assertEqual(
            half_turn.apply_object(phase_zero),
            m.UnframedBaseObject.from_phase(Fraction(1, 2)),
        )
        self.assertNotEqual(half_turn.apply_object(phase_zero), phase_zero)
        replay = m.finite_replay_witness()
        self.assertEqual(replay.object_count, 22)
        self.assertEqual(replay.transporter_checks, replay.object_pair_count)
        self.assertEqual(replay.half_turn_fixed_object_count, 0)
        self.assertTrue(replay.all_checks_passed)

    def test_bouquet_degree_witness_is_circular_and_not_canon(self) -> None:
        boundaries = {item.candidate_id: item for item in m.candidate_boundaries()}
        public = boundaries["public-gonol-157-position-carrier"]
        self.assertFalse(public.qualifies_as_t)
        self.assertIn("no canonical traversal", public.orbit_information)

        carrier = boundaries["non-null-directed-carrier"]
        self.assertFalse(carrier.qualifies_as_t)
        self.assertIn("translation-transitive", carrier.orbit_information)

        bouquet = boundaries["stack-local-subdivided-return-bouquet"]
        self.assertFalse(bouquet.qualifies_as_t)
        self.assertIn("uniquely distinguished by degree", bouquet.orbit_information)
        self.assertIn("attachment", bouquet.reason)
        self.assertNotEqual(bouquet.standing, "UCNS canon")

    def test_one_geometric_zero_cell_mark_breaks_translation_group(self) -> None:
        requirement = m.additional_structure_requirement()
        self.assertIn("distinguished unframed zero-cell", requirement.required_kind)
        self.assertIn("only tau_0 remains", requirement.exact_effect)
        self.assertFalse(requirement.current_canon_supplies)
        self.assertIsNone(requirement.selected_object)

    def test_transitive_outcome_emits_no_iota_or_downstream_evaluation(self) -> None:
        result = m.audit()
        self.assertEqual(result.status, "TRANSITIVE_SYMMETRY")
        self.assertEqual(result.secondary_classification, "UNIQUE_ORBIT_NOT_OBJECT")
        self.assertTrue(result.existing_canon_distinguishes_exactly_one_orbit)
        self.assertFalse(result.existing_canon_distinguishes_exactly_one_object)
        self.assertIsNone(result.iota)
        self.assertFalse(result.tangent_or_chirality_evaluated)
        self.assertFalse(result.downstream_constructor_fields_evaluated)

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
