"""Executable witnesses for the composed successor constructor gate."""

# === CHECKS ===
# id: check_composed_successor_freezes_mechanics_before_gate
#   proves: composed_successor_freezes_mechanics_before_gate
#   call: self::test_freezes_exact_mechanic_hashes_before_gate
#   mutates: none
#   cleanup: none
#
# id: check_composed_successor_constructor_has_no_target_constants
#   proves: composed_successor_constructor_has_no_target_constants
#   call: self::test_constructor_source_contains_no_observation_or_control_constants
#   mutates: none
#   cleanup: none
#
# id: check_composed_successor_uses_only_declared_mechanics
#   proves: composed_successor_uses_only_declared_mechanics
#   call: self::test_smallest_composition_counts_and_edges
#   mutates: none
#   cleanup: none
#
# id: check_composed_successor_falsifies_without_tuning
#   proves: composed_successor_falsifies_without_tuning
#   call: self::test_first_gate_falsifies_and_stops
#   mutates: none
#   cleanup: none
#
# id: check_composed_successor_receipt_replays_byte_identical
#   proves: composed_successor_receipt_replays_byte_identical
#   call: self::test_receipt_replays_byte_identically
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import sys
import unittest
from unittest import mock


UCNS_RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(UCNS_RESEARCH_ROOT))

import composed_successor_constructor as m


EXPECTED_MECHANICS = {
    "mechanic_1_public_gonol_functional_operations": {
        "module_path": "research/ucns/public_gonol_functional_operations.py",
        "code_sha256": "bf81a18b9074ce10232e73afa42d23690f4172c9b60b0284a986abbf5738a1d3",
        "receipt_sha256": "351d91a1d27f9b29b4222325df0a359682c9c8dd0903fdfef8d4f73c13074194",
    },
    "mechanic_2_affinization_coupling_geometry": {
        "module_path": "research/ucns/affinization_coupling_geometry.py",
        "code_sha256": "65c5bbee87fa1a5cb9119c19a8e186b62827e55a91b17c4111aa06b8df0ce21a",
        "receipt_sha256": "a59d291b77c0110ffc0c401dcc94d25ad63a3372c51eab26989a5b6acf9ff68d",
    },
    "mechanic_3_recursive_scale_transition": {
        "module_path": "research/ucns/recursive_scale_transition.py",
        "code_sha256": "882b2defbc88c686011a3c66d1e7d080adc9623b219a91a4253c0378b69292f1",
        "receipt_sha256": "3297ced3efb9c127a01337d479ce8382b771ea9d2ab66faa7e79a0ec2a197496",
    },
}


class ComposedSuccessorConstructorTest(unittest.TestCase):
    def test_freezes_exact_mechanic_hashes_before_gate(self) -> None:
        frozen = {item.mechanic_id: item for item in m.freeze_mechanics()}
        self.assertEqual(set(frozen), set(EXPECTED_MECHANICS))
        for mechanic_id, expected in EXPECTED_MECHANICS.items():
            item = frozen[mechanic_id]
            self.assertEqual(item.module_path, expected["module_path"])
            self.assertEqual(item.code_sha256, expected["code_sha256"])
            self.assertEqual(item.receipt_sha256, expected["receipt_sha256"])
            self.assertEqual(item.producer_code_reference, "sha256:" + expected["code_sha256"])

        with mock.patch.object(m, "freeze_mechanics", wraps=m.freeze_mechanics) as freezer:
            gate = m.evaluate_gate(source=1, first_target=2, second_target=3)
        self.assertGreaterEqual(freezer.call_count, 1)
        self.assertEqual(gate.status, m.STATUS_FALSIFIED)

    def test_constructor_source_contains_no_observation_or_control_constants(self) -> None:
        source = Path(m.__file__).read_text(encoding="utf-8")
        for value in {"28" + "81", "548" + "37698421", "164" + "513086777"}:
            self.assertNotIn(value, source)

    def test_smallest_composition_counts_and_edges(self) -> None:
        result = m.construct_successor_once(157)
        self.assertEqual(result.constructor_id, "ucns.smallest-composed-successor.v0")
        self.assertEqual(result.input_size, 157)
        self.assertEqual(result.output_size, 629)
        self.assertEqual(result.layer_counts, {
            "input_participants": 157,
            "public_gonol_function_participations": 157,
            "closed_affinizations": 157,
            "recursive_atomic_participants": 157,
            "successor_closure_whole": 1,
        })
        self.assertEqual(len(result.sample_edges), 6)
        first = result.sample_edges[0]
        self.assertEqual(first["slot"], 0)
        self.assertEqual(first["input_address"]["index"], 0)
        self.assertEqual(first["output_address"]["index"], 1)
        self.assertTrue(first["participation_digest"])
        self.assertTrue(first["coupling_digest"])
        self.assertTrue(first["closed_affinization_digest"])
        self.assertTrue(first["atomic_id"].startswith("ucns.atomic:"))
        self.assertTrue(first["transition_digest"])

    def test_first_gate_falsifies_and_stops(self) -> None:
        gate = m.evaluate_gate(source=157, first_target=2881, second_target=54837698421)
        self.assertEqual(gate.status, m.STATUS_FALSIFIED)
        self.assertEqual(gate.first.output_size, 629)
        self.assertEqual(gate.first_target, 2881)
        self.assertIsNone(gate.second)
        self.assertIsNone(gate.next_prediction)
        self.assertEqual(gate.interpolation_control_comparison, "not reached; first gate falsified")
        self.assertIn("first transition produced 629", gate.rejection_reason or "")

    def test_receipt_replays_byte_identically(self) -> None:
        kwargs = {
            "source": 157,
            "first_target": 2881,
            "second_target": 54837698421,
        }
        first = m.receipt_payload(**kwargs)
        second = m.receipt_payload(**kwargs)
        self.assertEqual(first, second)
        self.assertEqual(m.receipt_bytes(first), m.receipt_bytes(second))
        self.assertEqual(m.receipt_digest(first), sha256(m.receipt_bytes(first)).hexdigest())
        self.assertEqual(first["summary"]["status"], m.STATUS_FALSIFIED)
        self.assertEqual(first["summary"]["source_to_first_output"], 629)
        self.assertFalse(first["summary"]["second_gate_executed"])
        self.assertFalse(first["summary"]["next_prediction_available"])


if __name__ == "__main__":
    unittest.main()
