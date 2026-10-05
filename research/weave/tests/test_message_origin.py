# === CHECKS ===
# id: weave_message_byte_origin_witness
#   proves: weave_message_origin_contains_bytes
#   call: tests.test_message_origin.MessageOriginTests.test_one_participant_per_byte
# id: weave_message_occurrence_scope_witness
#   proves: weave_byte_occurrences_preserve_scope
#   call: tests.test_message_origin.MessageOriginTests.test_repeated_bytes_preserve_occurrences
# === END CHECKS ===
"""Run: python -m unittest discover -s tests -p test_message_origin.py.

The source construction can be recovered because it retains its plaintext.
These tests never report that operation as private-key decryption.
"""
from dataclasses import replace
from fractions import Fraction
import unittest

from stages.eight_circle import Circle, FullKeySet
from stages import message_origin as module
from stages.message_origin import ByteOccurrence, MessageOrigin, construct_at, construct_origin


def key():
    return FullKeySet(tuple(Circle(i, f"G{i}", Fraction(i, 9)) for i in range(8)),
                      (7, 2, 5, 0, 3, 1, 6, 4))


class MessageOriginTests(unittest.TestCase):
    def test_one_participant_per_byte(self):
        origin = construct_origin(b"AA", identity="M")
        self.assertEqual(origin.byte_length, 2)
        self.assertEqual(len(origin.bytesets), 2)
        self.assertEqual(tuple(b.index for b in origin.bytesets), (0, 1))
        self.assertFalse(hasattr(origin, "axes"))

    def test_eight_placements_are_inside_each_byte(self):
        origin = construct_origin(b"ABC", identity="M")
        full = key()
        positions = tuple(Fraction(i, 7) for i in range(8))
        for index, value in enumerate(b"ABC"):
            state = construct_at(origin, index, full, positions)
            self.assertEqual((state.origin_id, state.byte_index), ("M", index))
            self.assertEqual(len(state.placements), 8)
            self.assertEqual(state.source_value, value)
            self.assertEqual(tuple(p.circle_index for p in state.placements), tuple(range(8)))

    def test_repeated_bytes_preserve_occurrences(self):
        origin = construct_origin(b"AA", identity="M")
        self.assertEqual(origin.bytesets[0].value, origin.bytesets[1].value)
        self.assertNotEqual(origin.bytesets[0], origin.bytesets[1])
        self.assertEqual(origin.recover_bytes(), b"AA")

    def test_all_bytes_without_text_normalization(self):
        data = bytes(range(256)) + b"\x00\xff\r\n"
        origin = construct_origin(data, identity="binary")
        self.assertEqual(origin.recover_bytes(), data)
        self.assertEqual(origin.byte_length, len(data))

    def test_empty_message_keeps_its_origin(self):
        origin = construct_origin(b"", identity="empty")
        self.assertEqual(origin.bytesets, ())
        self.assertEqual(origin.recover_bytes(), b"")
        self.assertEqual(origin.identity, "empty")
        with self.assertRaises(ValueError):
            construct_at(origin, 0, key(), (Fraction(0),) * 8)

    def test_message_names_scope_occurrences_not_content_hashes(self):
        first = construct_origin(b"same", identity="first")
        second = construct_origin(b"same", identity="second")
        self.assertNotEqual(first, second)
        self.assertNotEqual(first.bytesets[0], second.bytesets[0])
        self.assertEqual(first.recover_bytes(), second.recover_bytes())
        self.assertEqual(first.identity, "first")

    def test_bad_input_and_identity_rejected(self):
        for data in ("text", bytearray(b"A"), [65], None):
            with self.assertRaises(TypeError):
                construct_origin(data, identity="M")
        for identity in (None, "", " ", True, 1):
            with self.assertRaises(ValueError):
                construct_origin(b"A", identity=identity)
        with self.assertRaises(TypeError):
            construct_origin(b"A")

    def test_direct_origin_validation(self):
        origin = construct_origin(b"AB", identity="M")
        for members in (list(origin.bytesets), (None,)):
            with self.assertRaises(TypeError):
                MessageOrigin("M", members)
        for members in (tuple(reversed(origin.bytesets)), (origin.bytesets[1],),
                        (origin.bytesets[0], origin.bytesets[0]),
                        (replace(origin.bytesets[0], origin_id="other"),)):
            with self.assertRaises(ValueError):
                MessageOrigin("M", members)
        for index, value in ((True, 0), (-1, 0), (0, False), (0, 256)):
            with self.assertRaises(ValueError):
                ByteOccurrence("M", index, value)

    def test_attachment_indices_fail_closed(self):
        origin = construct_origin(b"A", identity="M")
        positions = (Fraction(0),) * 8
        for index in (True, -1, 1, 0.0, None):
            with self.assertRaises(ValueError):
                construct_at(origin, index, key(), positions)
        with self.assertRaises(TypeError):
            construct_at("M", 0, key(), positions)
        self.assertNotIn("value=", repr(origin.bytesets[0]))
        self.assertNotIn("bytesets=", repr(origin))

    def test_removed_feedback_and_bit_axis_surface(self):
        for name in ("MessageAxis", "CouplingKey", "CoupledWitness", "encode", "public_recover",
                     "_axis_origin", "_source_bits", "witness_bits"):
            self.assertFalse(hasattr(module, name), name)


if __name__ == "__main__":
    unittest.main()
