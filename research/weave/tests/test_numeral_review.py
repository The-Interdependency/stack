# === CHECKS ===
# id: numeral_review_aggregate_budget
#   proves: numeral_strict_input
#   call: self::test_decode_has_one_aggregate_prime_budget
#   mutates: none
#   cleanup: none
# id: numeral_review_malformed_not_capacity
#   proves: numeral_strict_input
#   call: self::test_malformed_structures_are_not_capacity_failures
#   mutates: none
#   cleanup: none
# id: numeral_review_cli_angle
#   proves: numeral_strict_input
#   call: self::test_zero_denominator_cli_is_concise_refusal
#   mutates: none
#   cleanup: none
# === END CHECKS ===
"""Run: python -m unittest discover -s tests -p test_numeral_review.py -v.

Regression witnesses for the live PR #77 input/budget findings. The CLI refusal
occurs before input reads or output writes; no original tests are weakened.
"""
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import subprocess
import sys
import unittest
from numeral import BitBlock, Entry, Packet, PrimePath, Limits, Refused, ResourceLimit, encode, decode

ROOT = Path(__file__).resolve().parents[1]
A = chr(0xE000)


class NumeralReviewTests(unittest.TestCase):
    def test_decode_has_one_aggregate_prime_budget(self):
        path = PrimePath(101, ())
        p = Packet('budget', 0, (Entry(A, BitBlock(101, 16), Fraction(1, 7), 1, path),), A)
        wire = encode(p)
        # One recipe step and four trial-divisor candidates per pass: 10 total.
        with self.assertRaises(ResourceLimit):
            decode(wire, Limits(prime_work=9))
        self.assertEqual(decode(wire, Limits(prime_work=10)), p)

    def test_malformed_structures_are_not_capacity_failures(self):
        p = Packet('scope', 0, (Entry(A, BitBlock(5,8), Fraction(1,7), 1),), A)
        operations = (lambda: PrimePath(2, []).replay(),
                      lambda: encode(replace(p, entries=list(p.entries))),
                      lambda: encode(replace(p, symbols=[A])))
        for operation in operations:
            with self.assertRaises(Refused) as raised:
                operation()
            self.assertNotIsInstance(raised.exception, ResourceLimit)

    def test_zero_denominator_cli_is_concise_refusal(self):
        result = subprocess.run([sys.executable, str(ROOT/'numeral.py'), 'bind',
            'unused-input', 'unused-output', '--origin', 'test', '--angle', '1/0',
            '--circle', '3'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('Traceback', result.stderr)
        self.assertIn('exact finite fraction', result.stderr)


if __name__ == '__main__': unittest.main()
