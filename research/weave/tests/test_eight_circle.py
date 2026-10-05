"""Tests for the explicit eight-circle -> two-circle Weave candidate.

These prove construction properties and preserve the current attack witness. They do
not claim asymmetric security.
"""
from fractions import Fraction
import unittest

from stages.eight_circle import Circle, FullKeySet, encode, decode, encode_byte


def circle(i: int, *, shift: int = 0) -> Circle:
    # Exact rational positions over a 720-degree return. 1 turn = 360 degrees.
    return Circle(
        identity=f"g{i}",
        space=Fraction((i * 3 + shift) % 16, 8),
        zero=Fraction((i * 3 + shift + 1) % 16, 8),
        one=Fraction((i * 3 + shift + 9) % 16, 8),
    )


def keyset(*, shift: int = 0) -> FullKeySet:
    return FullKeySet(tuple(circle(i, shift=shift) for i in range(8)))


class EightCircleTests(unittest.TestCase):
    def test_full_key_is_exactly_eight_and_public_is_exactly_two(self):
        full = keyset()
        public = full.degenerate(1, 6)
        self.assertEqual(len(full.circles), 8)
        self.assertEqual(public.indices, (1, 6))
        self.assertEqual(len(public.circles), 2)
        self.assertEqual(tuple(c.identity for c in public.circles), ("g1", "g6"))
        with self.assertRaises(ValueError):
            full.degenerate(2, 2)

    def test_positions_use_exact_720_degree_return(self):
        c = Circle("x", Fraction(15, 8), Fraction(1, 8), Fraction(9, 8))
        self.assertEqual(c.position(0, Fraction(1, 4)), Fraction(1, 2))
        self.assertEqual(c.position(1, Fraction(1, 4)), Fraction(3, 2))
        self.assertEqual(c.position(0, Fraction(9, 4)), Fraction(1, 2))
        self.assertEqual(c.public_sheet(0, Fraction(1, 4)), 0)
        self.assertEqual(c.public_sheet(1, Fraction(1, 4)), 1)

    def test_key_set_space_relations_are_data_not_a_global_rule(self):
        origin = Fraction(1, 8)
        a = keyset(shift=0).degenerate(0, 1)
        b = keyset(shift=5).degenerate(0, 1)
        # The API accepts both key sets without privileging either space relation.
        self.assertNotEqual(
            tuple(c.space for c in a.circles),
            tuple(c.space for c in b.circles),
        )
        self.assertEqual(len(encode_byte(a, 0xA5, origin)), 16)
        self.assertEqual(len(encode_byte(b, 0xA5, origin)), 16)

    def test_raw_bytes_double_in_bit_length_and_roundtrip(self):
        full = keyset()
        public = full.degenerate(0, 3)
        origin = Fraction(3, 16)
        data = bytes(range(256))
        witness = encode(data, public, origin)
        self.assertEqual(len(witness), len(data) * 16)
        self.assertEqual(decode(full, public.indices, witness, origin), data)

    def test_malformed_or_nonadmitted_witness_fails(self):
        full = keyset()
        public = full.degenerate(0, 3)
        origin = Fraction(3, 16)
        witness = list(encode_byte(public, 0x5A, origin))
        # Fixture admits only (0,0) and (1,1); mixed pair is impossible.
        witness[0:2] = [0, 1]
        with self.assertRaises(ValueError):
            decode(full, public.indices, witness, origin)
        with self.assertRaises(ValueError):
            decode(full, public.indices, (0,) * 15, origin)

    def test_independent_bit_baseline_is_publicly_bruteforceable(self):
        """Falsification boundary: two public circles alone decode this baseline.

        An attacker can compare each observed two-bit witness with the public forward
        images of 0 and 1. Therefore this independent-bit sheet projection is a useful
        executable geometry scaffold but NOT the intended asymmetric construction.
        The missing requirement is the message-coupled UCHC origin/axis relation in
        which the six omitted circles alter the recoverable trajectory.
        """
        full = keyset()
        public = full.degenerate(2, 7)
        origin = Fraction(5, 16)
        value = 0xD3
        witness = encode_byte(public, value, origin)

        recovered = 0
        code = {public.witness(bit, origin): bit for bit in (0, 1)}
        self.assertEqual(len(code), 2)
        for i in range(0, 16, 2):
            recovered = (recovered << 1) | code[witness[i:i + 2]]
        self.assertEqual(recovered, value)


if __name__ == "__main__":
    unittest.main()
