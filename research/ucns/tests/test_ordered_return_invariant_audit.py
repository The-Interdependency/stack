"""Executable witnesses for the ordered return invariant audit."""

# === CHECKS ===
# id: check_ordered_return_fox_derivative_is_exact
#   proves: ordered_return_fox_derivative_is_exact
#   call: self::test_exact_fox_derivatives_and_fundamental_identity
#   mutates: none
#   cleanup: none
#
# id: check_ordered_return_magnus_preserves_order
#   proves: ordered_return_magnus_preserves_order
#   call: self::test_degree_two_magnus_keeps_order_before_degree_one_projection
#   mutates: none
#   cleanup: none
#
# id: check_ordered_return_invariants_distinguish_triadic_words
#   proves: ordered_return_invariants_distinguish_triadic_words
#   call: self::test_all_six_triadic_based_words_have_distinct_fingerprints
#   mutates: none
#   cleanup: none
#
# id: check_ordered_return_homology_underdetermines_monodromy
#   proves: ordered_return_homology_underdetermines_monodromy
#   call: self::test_nonidentity_automorphisms_replay_with_identity_h1_action
#   mutates: none
#   cleanup: none
#
# id: check_ordered_return_authority_gap_is_provenance_bound
#   proves: ordered_return_authority_gap_is_provenance_bound
#   call: self::test_existing_order_surfaces_do_not_claim_recursive_monodromy
#   mutates: none
#   cleanup: none
#
# id: check_ordered_return_presentation_gate_fails_closed
#   proves: ordered_return_presentation_gate_fails_closed
#   call: self::test_missing_relators_prevent_integer_and_factor_readout
#   mutates: none
#   cleanup: none
#
# id: check_ordered_return_invariant_audit_is_target_free
#   proves: ordered_return_invariant_audit_is_target_free
#   call: self::test_invariant_source_contains_no_observation_inputs
#   mutates: none
#   cleanup: none
#
# id: check_ordered_return_invariant_receipt_replays
#   proves: ordered_return_invariant_receipt_replays
#   call: self::test_receipt_replays_byte_identically
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import sys
import unittest


UCNS_RESEARCH_ROOT = Path(__file__).resolve().parents[1]
COMMITTED_RECEIPT = UCNS_RESEARCH_ROOT / "receipts" / "ordered-return-invariant-audit-v0.json"
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import ordered_complete_return_groupoid as groupoid_module
import ordered_return_invariant_audit as m


class OrderedReturnInvariantAuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.groupoid = groupoid_module.build_ordered_return_groupoid(3)
        cls.x, cls.y, cls.z = cls.groupoid.generators

    def test_exact_fox_derivatives_and_fundamental_identity(self) -> None:
        xyz = self.groupoid.word_from_ordinals((1, 2, 3))
        dx = m.fox_derivative(self.groupoid, xyz, self.x.relation_id)
        dy = m.fox_derivative(self.groupoid, xyz, self.y.relation_id)
        dz = m.fox_derivative(self.groupoid, xyz, self.z.relation_id)
        self.assertEqual(dx.to_payload(self.groupoid), [{"coefficient": 1, "word": []}])
        self.assertEqual(dy.to_payload(self.groupoid), [{"coefficient": 1, "word": ["g1"]}])
        self.assertEqual(dz.to_payload(self.groupoid), [{"coefficient": 1, "word": ["g1", "g2"]}])
        self.assertTrue(m.fox_fundamental_identity_holds(self.groupoid, xyz))

        mixed = self.groupoid.word_from_ordinals((-1, 2, 3, -2, 1))
        self.assertTrue(m.fox_fundamental_identity_holds(self.groupoid, mixed))
        self.assertTrue(m.fox_fundamental_identity_holds(self.groupoid, mixed.inverse()))

    def test_degree_two_magnus_keeps_order_before_degree_one_projection(self) -> None:
        xyz = self.groupoid.word_from_ordinals((1, 2, 3))
        yxz = self.groupoid.word_from_ordinals((2, 1, 3))
        xyz_expansion = m.magnus_expansion(self.groupoid, xyz)
        yxz_expansion = m.magnus_expansion(self.groupoid, yxz)
        self.assertNotEqual(xyz_expansion, yxz_expansion)
        self.assertEqual(
            xyz_expansion.coefficient((self.x.relation_id, self.y.relation_id)),
            1,
        )
        self.assertEqual(
            xyz_expansion.coefficient((self.y.relation_id, self.x.relation_id)),
            0,
        )
        self.assertEqual(
            yxz_expansion.coefficient((self.y.relation_id, self.x.relation_id)),
            1,
        )
        for word in (xyz, yxz, self.groupoid.word_from_ordinals((-1, 2, 1))):
            expansion = m.magnus_expansion(self.groupoid, word)
            degree_one = tuple(
                expansion.coefficient((generator.relation_id,))
                for generator in self.groupoid.generators
            )
            self.assertEqual(degree_one, self.groupoid.abelianize(word))

    def test_all_six_triadic_based_words_have_distinct_fingerprints(self) -> None:
        words = tuple(
            self.groupoid.word(
                groupoid_module.WordLetter(generator.relation_id)
                for generator in ordering
            )
            for ordering in permutations(self.groupoid.generators)
        )
        invariants = tuple(m.ordered_word_invariant(self.groupoid, word) for word in words)
        self.assertEqual(len({item.word for item in invariants}), 6)
        self.assertEqual(len({item.fox_fingerprint_sha256 for item in invariants}), 6)
        self.assertEqual(len({item.magnus_fingerprint_sha256 for item in invariants}), 6)
        self.assertEqual(len({item.abelianization for item in invariants}), 1)
        self.assertTrue(all(item.fox_fundamental_identity for item in invariants))

    def test_nonidentity_automorphisms_replay_with_identity_h1_action(self) -> None:
        witnesses = m.monodromy_witnesses()
        self.assertEqual(
            tuple(item.witness_id for item in witnesses),
            (
                "rank-two-inner-basepoint-transport",
                "rank-three-commutator-ia-shear",
            ),
        )
        for witness in witnesses:
            identity = tuple(
                tuple(1 if row == column else 0 for column in range(witness.rank))
                for row in range(witness.rank)
            )
            self.assertEqual(witness.abelianization_matrix, identity)
            self.assertTrue(witness.inverse_replay)
            self.assertTrue(witness.nonidentity_before_abelianization)
        triadic = witnesses[1]
        triadic_groupoid = groupoid_module.build_ordered_return_groupoid(3)
        self.assertEqual(
            triadic_groupoid.word_symbols(triadic.images[0]),
            ("g1", "g2", "g3", "g2^-1", "g3^-1"),
        )

    def test_existing_order_surfaces_do_not_claim_recursive_monodromy(self) -> None:
        evidence = m.authority_gap_evidence()
        self.assertEqual(len(evidence), 6)
        self.assertEqual(
            {item.surface for item in evidence},
            {
                "canonical Public Gonol carrier",
                "canonical native Mobius return",
                "stack-local Public Gonol operations",
                "stack-local affinization coupling",
                "stack-local recursive promotion",
                "canonical Mobius seed candidate",
            },
        )
        for item in evidence:
            source_path = m._stack_root() / item.source_path
            self.assertEqual(sha256(source_path.read_bytes()).hexdigest(), item.source_sha256)
            self.assertIn(
                item.required_source_marker,
                source_path.read_text(encoding="utf-8"),
            )
            self.assertTrue(item.existing_ordered_data)
            self.assertTrue(item.missing_recursive_geometry)

    def test_missing_relators_prevent_integer_and_factor_readout(self) -> None:
        result = m.audit()
        self.assertEqual(result.status, m.STATUS)
        self.assertEqual(result.current_relators, ())
        self.assertIsNone(result.current_global_monodromy)
        self.assertIsNone(result.current_integer_presentation)
        self.assertIsNone(result.current_canonical_integer_invariant)
        self.assertIsNone(result.current_factorization)
        self.assertIsNone(result.observation_comparison)
        self.assertIsNone(result.numerical_next_gonol)
        gate = result.to_payload()["presentation_gate"]
        self.assertEqual(gate["relator_count"], 0)
        self.assertEqual(
            gate["gate_result"],
            "NOT_REACHED_MISSING_GEOMETRY_DERIVED_RELATORS_AND_MONODROMY",
        )

    def test_invariant_source_contains_no_observation_inputs(self) -> None:
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
        self.assertIsNone(payload["result"]["presentation_gate"]["observation_comparison"])

    def test_receipt_replays_byte_identically(self) -> None:
        committed = json.loads(COMMITTED_RECEIPT.read_text(encoding="utf-8"))
        committed_digest = committed.pop("receipt_sha256")
        self.assertEqual(committed, m.receipt_payload())
        self.assertEqual(committed_digest, m.receipt_digest())
        self.assertEqual(committed_digest, sha256(m.receipt_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
