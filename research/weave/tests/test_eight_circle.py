# === CHECKS ===
# id: weave_byte_mapping_witness
#   proves: weave_byte_has_eight_circle_placements
#   call: tests.test_eight_circle.EightCircleTests.test_all_bytes
# id: weave_star_witness
#   proves: weave_public_pair_always_contains_whole
#   call: tests.test_eight_circle.EightCircleTests.test_all_seven_star_views
# id: weave_no_bit_code_witness
#   proves: weave_positions_are_not_bit_codes
#   call: tests.test_eight_circle.EightCircleTests.test_removed_bitwise_cipher_surface
# === END CHECKS ===
"""Run with: python -m unittest discover -s tests -p test_eight_circle.py.

Coverage: all 256 byte values, all 40,320 bit/circle assignments, all seven
whole-part views and invalid direct construction. This is not cryptanalysis.
"""
from dataclasses import FrozenInstanceError, replace
from fractions import Fraction
from itertools import permutations
import unittest

from stages import eight_circle as module
from stages.eight_circle import (
    BitPlacement, ByteConstruction, Circle, FullKeySet, PublicPair, construct_byte,
)

POSITIONS = tuple(Fraction(i, 7) for i in range(8))


def key(mapping=tuple(range(8))):
    return FullKeySet(tuple(Circle(i, f"G{i}", Fraction(i, 9)) for i in range(8)), mapping)


def build(value=0xA5, full=None, positions=POSITIONS):
    return construct_byte(value, key() if full is None else full, positions,
                          origin_id="message", byte_index=0)


class EightCircleTests(unittest.TestCase):
    def test_all_bytes(self):
        full = key()
        for value in range(256):
            state = build(value, full)
            self.assertEqual(len(state.placements), 8)
            self.assertEqual(state.source_value, value)
            self.assertEqual(tuple(p.circle_index for p in state.placements), tuple(range(8)))
            self.assertEqual(tuple(p.bit for p in state.placements),
                             tuple((value >> i) & 1 for i in range(7, -1, -1)))

    def test_all_40320_assignments(self):
        circles = key().circles
        count = 0
        for mapping in permutations(range(8)):
            state = build(0xA5, FullKeySet(circles, mapping))
            self.assertEqual(state.source_value, 0xA5)
            for source, circle in enumerate(mapping):
                self.assertEqual(state.placements[circle].source_bit_index, source)
            count += 1
        self.assertEqual(count, 40320)

    def test_all_seven_star_views(self):
        full = key()
        for part in range(1, 8):
            pair = full.degenerate(part)
            self.assertEqual(pair.indices, (0, part))
            self.assertEqual(len(pair.circles), 2)
            self.assertIs(pair.circles[0], full.circles[0])
            self.assertIs(pair.circles[1], full.circles[part])

    def test_arbitrary_and_malformed_pairs_rejected(self):
        full = key()
        for bad in (0, -1, 8, True, 1.0, "1", None):
            with self.subTest(part=bad), self.assertRaises(ValueError):
                full.degenerate(bad)
        for members in ((full.circles[1], full.circles[2]),
                        (full.circles[1], full.circles[0]),
                        (full.circles[0], full.circles[0]),
                        list(full.circles[:2]), (), (None, None)):
            with self.subTest(members=members), self.assertRaises(ValueError):
                PublicPair(members)
        with self.assertRaises(TypeError):
            full.degenerate(0, 1)

    def test_full_key_validation(self):
        full = key()
        for circles in (full.circles[:-1], list(full.circles),
                        tuple(reversed(full.circles)), (None,) * 8,
                        (full.circles[0],) * 8):
            with self.assertRaises(ValueError):
                FullKeySet(circles, tuple(range(8)))
        duplicate_names = tuple(Circle(i, "same", Fraction(0)) for i in range(8))
        with self.assertRaises(ValueError):
            FullKeySet(duplicate_names, tuple(range(8)))
        for mapping in ((), (0,) * 8, (False,) + tuple(range(1, 8)),
                        (0.0,) + tuple(range(1, 8)), list(range(8)), tuple(range(1, 9))):
            with self.assertRaises(ValueError):
                FullKeySet(full.circles, mapping)

    def test_exact_720_positions_not_two_bit_codes(self):
        phases = (Fraction(0), Fraction(1), Fraction(2), Fraction(-1),
                  Fraction(1, 10**40 + 7), Fraction(9, 4), Fraction(3, 2), Fraction(7, 4))
        state = build(0, positions=phases)
        self.assertEqual(tuple(p.position for p in state.placements),
                         tuple(p % 2 for p in phases))
        self.assertNotEqual(state.placements[0].position, state.placements[1].position)
        self.assertEqual(state.placements[0].position, state.placements[2].position)
        self.assertEqual(state.placements[4].position, phases[4])

    def test_positions_and_space_are_independent_supplied_data(self):
        full = key()
        other = FullKeySet(tuple(replace(c, space=c.space + Fraction(1, 17))
                                 for c in full.circles), full.bit_to_circle)
        self.assertNotEqual(full.circles, other.circles)
        shifted = tuple(p + Fraction(1, 19) for p in POSITIONS)
        first, second = build(full=full), build(full=other, positions=shifted)
        self.assertEqual(first.source_value, second.source_value)
        self.assertNotEqual(first.placements[0].position, second.placements[0].position)
        # No claim that changing private data with identical public inputs must
        # change encryption. This test checks supplied construction data only.

    def test_invalid_byte_and_position_inputs(self):
        for value in (-1, 256, True, 1.0, b"A", None):
            with self.assertRaises(ValueError):
                build(value)
        for phases in ((), list(POSITIONS), POSITIONS[:-1]):
            with self.assertRaises(ValueError):
                build(positions=phases)
        for phase in (0, 0.0, True, None):
            with self.assertRaises(TypeError):
                build(positions=(phase,) + POSITIONS[1:])
        with self.assertRaises(TypeError):
            build(full="not a full key")

    def test_direct_construction_validation(self):
        state = build()
        for changes in ({"placements": state.placements[:-1]},
                        {"placements": tuple(reversed(state.placements))},
                        {"placements": (state.placements[0],) * 8},
                        {"placements": (None,) * 8},
                        {"placements": list(state.placements)},
                        {"origin_id": " "}, {"byte_index": True}, {"byte_index": -1}):
            with self.assertRaises(ValueError):
                replace(state, **changes)
        for changes in ({"source_bit_index": True}, {"circle_index": 8}, {"bit": False}):
            with self.assertRaises(ValueError):
                replace(state.placements[0], **changes)
        duplicate_source = (replace(state.placements[0], source_bit_index=1),) + state.placements[1:]
        with self.assertRaises(ValueError):
            replace(state, placements=duplicate_source)
        for bad in (True, -1, 8):
            with self.assertRaises(ValueError):
                Circle(bad, "bad", Fraction(0))

    def test_public_view_does_not_export_byte_or_other_six(self):
        full = key()
        pair = full.degenerate(4)
        self.assertEqual(set(vars(pair)), {"circles"})
        self.assertEqual(pair.indices, (0, 4))
        self.assertFalse(hasattr(pair, "bit_to_circle"))
        self.assertFalse(hasattr(pair, "full"))
        self.assertFalse(hasattr(pair, "placements"))
        self.assertEqual({c.index for c in pair.circles}, {0, 4})

    def test_removed_bitwise_cipher_surface(self):
        for name in ("encode", "decode", "encode_byte", "decode_byte"):
            self.assertFalse(hasattr(module, name), name)
        self.assertFalse(hasattr(Circle, "public_sheet"))
        self.assertFalse(hasattr(PublicPair, "witness"))

    def test_records_are_immutable_and_payload_not_repr(self):
        state = build()
        with self.assertRaises(FrozenInstanceError):
            state.byte_index = 2
        self.assertNotIn("placements=", repr(state))
        self.assertNotIn("bit=", repr(state.placements[0]))
        self.assertNotIn("space=", repr(key().circles[0]))


if __name__ == "__main__":
    unittest.main()
