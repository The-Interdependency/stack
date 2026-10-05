"""Executable tests for the message-scoped UCHC-style Weave coupling candidate.

Usage:
    python -m unittest tests.test_message_origin

The suite proves the message-origin/axis topology and preserves the public-recovery
falsification. Passing these tests does not establish encryption security.
"""
from fractions import Fraction
import unittest

from stages.eight_circle import Circle, FullKeySet
from stages.message_origin import CouplingKey, construct_origin, encode, public_recover


def base_circle(i: int, *, hidden_shift: int = 0) -> Circle:
    shift = 0 if i in (0, 1) else hidden_shift
    return Circle(
        identity=f"g{i}",
        space=Fraction((i * 3 + shift) % 16, 8),
        zero=Fraction((i * 3 + shift + 1) % 16, 8),
        one=Fraction((i * 3 + shift + 9) % 16, 8),
    )


def keyset(*, hidden_shift: int = 0) -> FullKeySet:
    return FullKeySet(tuple(base_circle(i, hidden_shift=hidden_shift) for i in range(8)))


COUPLING = CouplingKey(
    initial_origin=Fraction(1, 16),
    axis_step=Fraction(3, 16),
    feedback_step=Fraction(5, 16),
)


class MessageOriginTests(unittest.TestCase):
    def test_one_message_is_one_origin_with_ordered_occurrence_axes(self):
        origin = construct_origin(b"AA")
        self.assertEqual(origin.identity, "O_M")
        self.assertEqual(origin.byte_length, 2)
        self.assertEqual(len(origin.axes), 16)
        self.assertEqual(tuple(axis.index for axis in origin.axes), tuple(range(16)))
        # Equal byte/bit values remain different occurrences by source position.
        self.assertNotEqual(origin.axes[0], origin.axes[8])
        self.assertEqual((origin.axes[0].byte_index, origin.axes[8].byte_index), (0, 1))

    def test_coupled_candidate_preserves_two_bits_per_source_bit(self):
        public = keyset().degenerate(0, 1)
        data = b"origin"
        result = encode(data, public, COUPLING)
        self.assertEqual(result.origin.byte_length, len(data))
        self.assertEqual(len(result.bits), len(data) * 16)

    def test_key_set_coupling_changes_trajectory(self):
        public = keyset().degenerate(0, 1)
        data = b"same message"
        first = encode(data, public, COUPLING)
        second = encode(
            data,
            public,
            CouplingKey(Fraction(7, 16), Fraction(1, 8), Fraction(3, 8)),
        )
        self.assertNotEqual(first.bits, second.bits)

    def test_public_recovery_falsifies_this_coupling_as_asymmetric(self):
        public = keyset().degenerate(0, 1)
        for data in (b"", b"\x00", b"\xff", bytes(range(32)), b"message origin"):
            witness = encode(data, public, COUPLING)
            self.assertEqual(public_recover(public, COUPLING, witness), data)

    def test_six_hidden_circles_are_not_causal_in_this_candidate(self):
        first_full = keyset(hidden_shift=0)
        second_full = keyset(hidden_shift=5)
        first_public = first_full.degenerate(0, 1)
        second_public = second_full.degenerate(0, 1)
        self.assertEqual(first_public, second_public)

        data = bytes(range(64))
        first = encode(data, first_public, COUPLING)
        second = encode(data, second_public, COUPLING)
        self.assertEqual(first, second)
        self.assertEqual(public_recover(first_public, COUPLING, first), data)

    def test_nonbyte_input_and_bad_coupling_fail_closed(self):
        with self.assertRaises(TypeError):
            construct_origin("not bytes")
        with self.assertRaises(TypeError):
            CouplingKey(Fraction(0), Fraction(1, 8), 1)


if __name__ == "__main__":
    unittest.main()
