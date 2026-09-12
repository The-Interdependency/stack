"""Executable witnesses for affinization/coupling geometry research."""

# === CHECKS ===
# id: check_affinization_coupling_binds_ucns_and_metapat_authority
#   proves: affinization_coupling_binds_ucns_and_metapat_authority
#   call: self::test_authority_snapshot_binds_ucns_metapat_and_mechanic1
#   mutates: none
#   cleanup: none
#
# id: check_affinization_coupling_requires_explicit_ordered_relation
#   proves: affinization_coupling_requires_explicit_ordered_relation
#   call: self::test_coupling_requires_explicit_order_and_rejects_forbidden_inputs
#   mutates: none
#   cleanup: none
#
# id: check_affinization_coupling_preserves_participant_provenance
#   proves: affinization_coupling_preserves_participant_provenance
#   call: self::test_closed_affinization_preserves_recoverable_participants
#   mutates: none
#   cleanup: none
#
# id: check_affinization_coupling_degree_is_slot_sensitive
#   proves: affinization_coupling_degree_is_slot_sensitive
#   call: self::test_degree_ledger_is_slot_sensitive
#   mutates: none
#   cleanup: none
#
# id: check_affinization_coupling_closure_receipts_are_deterministic
#   proves: affinization_coupling_closure_receipts_are_deterministic
#   call: self::test_closure_receipts_replay_byte_identically
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

import affinization_coupling_geometry as m
import public_gonol_functional_operations as pgfo


def _participant(name: str, digest: str | None = None) -> m.CouplingParticipant:
    return m.CouplingParticipant(
        participant_id=f"participant.{name}",
        scale="test-scale",
        role=name,
        source_digest=digest or sha256(name.encode("utf-8")).hexdigest(),
    )


class AffinizationCouplingGeometryTest(unittest.TestCase):
    def test_authority_snapshot_binds_ucns_metapat_and_mechanic1(self) -> None:
        snapshot = m.load_authority_snapshot()
        self.assertEqual(snapshot.ucns_base["source_commit"], m.PINNED_UCNS_COMMIT)
        self.assertEqual(snapshot.metapat_base["source_commit"], m.PINNED_METAPAT_COMMIT)
        self.assertEqual(snapshot.metapat_phi_policy["allowed_relation_kind"], m.RELATION_KIND)
        self.assertFalse(snapshot.metapat_phi_policy["theorem_status_transfer"])
        self.assertFalse(snapshot.metapat_phi_policy["metapat_validity_claim"])
        self.assertEqual(snapshot.mechanic1_receipt_sha256, pgfo.receipt_digest(pgfo.receipt_payload()))
        paths = {path for path, _digest in snapshot.source_file_digests}
        self.assertIn("libs/metapat/src/metapat/ucns_phi.py", paths)
        self.assertIn("research/ucns/public_gonol_functional_operations.py", paths)

    def test_coupling_requires_explicit_order_and_rejects_forbidden_inputs(self) -> None:
        source = Path(m.__file__).read_text(encoding="utf-8")
        for value in {"28" + "81", "548" + "37698421"}:
            self.assertNotIn(value, source)

        left = _participant("left")
        right = _participant("right")
        item = m.coupling("ordered.left-right", (left, right))
        reversed_item = m.coupling("ordered.right-left", (right, left))
        self.assertNotEqual(item.coupling_digest, reversed_item.coupling_digest)
        self.assertEqual(item.to_payload()["participants"][0]["participant_id"], left.participant_id)

        with self.assertRaises(m.CouplingGeometryError):
            m.coupling("bad.temporal", (left, right), relation_kind="temporal-successor")
        with self.assertRaises(m.CouplingGeometryError):
            m.coupling("bad.duplicate", (left, left))
        with self.assertRaises(m.CouplingGeometryError):
            m.reject_inferred_overlap_coupling("shared participant id")

    def test_closed_affinization_preserves_recoverable_participants(self) -> None:
        closed = m.sample_public_operation_affinization()
        receipt = closed.receipt
        self.assertEqual(receipt["closure"]["participants_recoverable"], True)
        self.assertEqual(receipt["closure"]["relation_intrinsic_to_whole"], True)
        participants = receipt["coupling"]["participants"]
        self.assertEqual(len(participants), 2)
        self.assertEqual(participants[0]["participant_id"], "mechanic1.closed-operation.identity")
        self.assertEqual(participants[0]["slot"], 0)
        self.assertEqual(participants[1]["participant_id"], "mechanic1.closed-operation.cyclic-step-one")
        self.assertEqual(participants[1]["slot"], 1)
        self.assertTrue(participants[0]["source_digest"])
        self.assertTrue(participants[1]["source_digest"])
        self.assertEqual(receipt["whole_id"], closed.whole_id)

    def test_degree_ledger_is_slot_sensitive(self) -> None:
        hub = _participant("hub")
        first = _participant("first")
        second = _participant("second")
        first_coupling = m.coupling("hub-first", (hub, first))
        second_coupling = m.coupling("hub-second", (hub, second))
        reversed_coupling = m.coupling("first-hub", (first, hub))
        ledger = {
            entry.participant_id: entry
            for entry in m.degree_ledger((first_coupling, second_coupling, reversed_coupling))
        }
        self.assertEqual(ledger[hub.participant_id].degree, 3)
        self.assertEqual(ledger[hub.participant_id].slot_degrees, ((0, 2), (1, 1)))
        self.assertEqual(ledger[first.participant_id].slot_degrees, ((0, 1), (1, 1)))
        self.assertEqual(ledger[second.participant_id].slot_degrees, ((1, 1),))

    def test_closure_receipts_replay_byte_identically(self) -> None:
        left = _participant("left")
        right = _participant("right")
        item = m.coupling("stable.left-right", (left, right))
        first = m.close_affinization(item)
        second = m.close_affinization(m.coupling("stable.left-right", (left, right)))
        self.assertEqual(first.receipt, second.receipt)
        self.assertEqual(first.digest, second.digest)
        self.assertEqual(first.whole_id, second.whole_id)
        self.assertTrue(first.whole_id.startswith("ucns.affinization:"))

        payload = m.receipt_payload()
        self.assertEqual(m.receipt_bytes(payload), m.receipt_bytes(m.receipt_payload()))
        self.assertEqual(m.receipt_digest(payload), sha256(m.receipt_bytes(payload)).hexdigest())
        self.assertEqual(payload["definition"]["admitted_relation_kind"], "constitutive-simultaneous")
        self.assertFalse(payload["definition"]["status_transfer"])


if __name__ == "__main__":
    unittest.main()
