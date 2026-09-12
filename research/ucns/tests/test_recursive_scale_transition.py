"""Executable witnesses for recursive-scale transition research."""

# === CHECKS ===
# id: check_recursive_scale_transition_binds_prior_mechanics
#   proves: recursive_scale_transition_binds_prior_mechanics
#   call: self::test_transition_authority_binds_prior_mechanics
#   mutates: none
#   cleanup: none
#
# id: check_recursive_scale_transition_promotes_closed_whole_only
#   proves: recursive_scale_transition_promotes_closed_whole_only
#   call: self::test_promotion_requires_closed_recoverable_affinization
#   mutates: none
#   cleanup: none
#
# id: check_recursive_scale_transition_atomic_identity_is_deterministic
#   proves: recursive_scale_transition_atomic_identity_is_deterministic
#   call: self::test_atomic_identity_stable_and_occurrences_separate
#   mutates: none
#   cleanup: none
#
# id: check_recursive_scale_transition_preserves_recoverable_constituents
#   proves: recursive_scale_transition_preserves_recoverable_constituents
#   call: self::test_constituent_references_remain_recoverable
#   mutates: none
#   cleanup: none
#
# id: check_recursive_scale_transition_receipts_are_deterministic
#   proves: recursive_scale_transition_receipts_are_deterministic
#   call: self::test_receipts_replay_byte_identically
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

import affinization_coupling_geometry as acg
import public_gonol_functional_operations as pgfo
import recursive_scale_transition as m


class RecursiveScaleTransitionTest(unittest.TestCase):
    def test_transition_authority_binds_prior_mechanics(self) -> None:
        authority = m.load_transition_authority()
        self.assertEqual(authority.ucns_base["source_commit"], m.PINNED_UCNS_COMMIT)
        self.assertEqual(authority.metapat_base["source_commit"], m.PINNED_METAPAT_COMMIT)
        self.assertEqual(authority.mechanic1_receipt_sha256, pgfo.receipt_digest(pgfo.receipt_payload()))
        self.assertEqual(authority.mechanic2_receipt_sha256, acg.receipt_digest(acg.receipt_payload()))
        paths = {path for path, _digest in authority.source_file_digests}
        self.assertIn("research/ucns/public_gonol_functional_operations.py", paths)
        self.assertIn("research/ucns/affinization_coupling_geometry.py", paths)

    def test_promotion_requires_closed_recoverable_affinization(self) -> None:
        source = Path(m.__file__).read_text(encoding="utf-8")
        for value in {"28" + "81", "548" + "37698421"}:
            self.assertNotIn(value, source)

        closed = acg.sample_public_operation_affinization()
        promoted = m.promote_closed_affinization(
            closed,
            source_scale="source",
            target_scale="target",
            occurrence_id="occurrence-0",
        )
        self.assertTrue(promoted.atomic_participant.atomic_id.startswith("ucns.atomic:"))
        self.assertEqual(promoted.atomic_participant.source_whole_id, closed.whole_id)
        self.assertEqual(promoted.atomic_participant.source_digest, closed.digest)

        bad_receipt = dict(closed.receipt)
        bad_receipt["closure"] = {**bad_receipt["closure"], "participants_recoverable": False}
        bad = acg.ClosedAffinization(closed.whole_id, closed.coupling, bad_receipt)
        with self.assertRaises(m.RecursiveScaleTransitionError):
            m.promote_closed_affinization(
                bad,
                source_scale="source",
                target_scale="target",
                occurrence_id="occurrence-0",
            )
        with self.assertRaises(m.RecursiveScaleTransitionError):
            m.promote_closed_affinization(
                closed,
                source_scale="source",
                target_scale="",
                occurrence_id="occurrence-0",
            )

    def test_atomic_identity_stable_and_occurrences_separate(self) -> None:
        closed = acg.sample_public_operation_affinization()
        first = m.promote_closed_affinization(
            closed,
            source_scale="source",
            target_scale="target",
            occurrence_id="occurrence-0",
        )
        second = m.promote_closed_affinization(
            closed,
            source_scale="source",
            target_scale="target",
            occurrence_id="occurrence-1",
        )
        other_scale = m.promote_closed_affinization(
            closed,
            source_scale="source",
            target_scale="other-target",
            occurrence_id="occurrence-0",
        )
        self.assertEqual(first.atomic_participant.atomic_id, second.atomic_participant.atomic_id)
        self.assertNotEqual(first.digest, second.digest)
        self.assertNotEqual(first.occurrence_id, second.occurrence_id)
        self.assertNotEqual(first.atomic_participant.atomic_id, other_scale.atomic_participant.atomic_id)

    def test_constituent_references_remain_recoverable(self) -> None:
        transition = m.sample_recursive_transition()
        constituents = m.recover_constituent_references(transition)
        self.assertEqual(len(constituents), 2)
        self.assertEqual(constituents[0]["participant_id"], "mechanic1.closed-operation.identity")
        self.assertEqual(constituents[1]["participant_id"], "mechanic1.closed-operation.cyclic-step-one")
        self.assertFalse(transition.receipt["transition"]["reopen_constituents_by_default"])
        self.assertTrue(transition.receipt["transition"]["atomic_at_consuming_scale"])
        self.assertEqual(
            transition.receipt["source_closed_affinization"]["coupling_digest"],
            transition.atomic_participant.coupling_digest,
        )

    def test_receipts_replay_byte_identically(self) -> None:
        first = m.sample_recursive_transition()
        second = m.sample_recursive_transition()
        self.assertEqual(first.receipt, second.receipt)
        self.assertEqual(first.digest, second.digest)

        payload = m.receipt_payload()
        self.assertEqual(m.receipt_bytes(payload), m.receipt_bytes(m.receipt_payload()))
        self.assertEqual(m.receipt_digest(payload), sha256(m.receipt_bytes(payload)).hexdigest())
        self.assertEqual(payload["definition"]["successor_validation"], "paused")


if __name__ == "__main__":
    unittest.main()
