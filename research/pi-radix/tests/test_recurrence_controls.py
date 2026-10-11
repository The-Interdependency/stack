from __future__ import annotations

import json
import math
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import recurrence_controls as controls
import pi_radix as scan

# === CHECKS ===
# id: check_pi_control_interval
#   proves: pi_control_same_number
#   call: self::test_interval_and_boundary_failure
#   mutates: none
#   cleanup: none
#
# id: check_pi_control_count
#   proves: pi_control_count_distinct
#   call: self::test_independent_counter_and_planted_recurrence
#   mutates: none
#   cleanup: none
#
# id: check_pi_control_shuffle
#   proves: pi_control_shuffle_preserves
#   call: self::test_shuffle_and_rejection
#   mutates: none
#   cleanup: none
#
# id: check_pi_control_rank
#   proves: pi_control_source_bound
#   call: self::test_rank_ties_and_nonzero_tail
#   mutates: none
#   cleanup: none
#
# id: check_pi_control_receipt
#   proves: pi_control_source_bound
#   call: self::test_receipt_sources_and_replay
#   mutates: none
#   cleanup: none
# === END CHECKS ===


class TestControls(unittest.TestCase):
    def test_interval_and_boundary_failure(self):
        digits = controls.interval_digits(31415, 20, 10, 3)
        self.assertEqual(digits, [0, 2, 9])
        # Encode the SAME dyadic point through different bases; every prefix
        # interval must contain both the lower point and the upper endpoint limit.
        for base in (2, 3, 10, 30):
            digits = controls.interval_digits(31415, 30, base, 3)
            value = scan.decode_block(digits, base)
            self.assertLessEqual(value * (1 << 30), 31415 * base**3)
            self.assertGreaterEqual((value + 1) * (1 << 30), 31416 * base**3)
        with self.assertRaises(ArithmeticError):
            controls.interval_digits(0, 1, 3, 1)
        self.assertEqual(controls.interval_digits(1, 1, 2, 1), [1])

    def test_independent_counter_and_planted_recurrence(self):
        streams = {10: [1, 3, 0, 1, 3], 12: [1, 1, 0, 1, 1]}
        self.assertEqual(controls.recurrence(streams)["primes"], [{"prime": 13, "bases": [10, 12]}])
        self.assertEqual(controls.recurrence({10: streams[10]})["count"], 0)
        # Independent trial division, direct arithmetic, no terminal sieve.
        streams = {b: [controls.Draws(f"test/{b}/{i}").below(b) for i in range(35)]
                   for b in (5, 7, 10, 12)}
        support = {}
        for base, digits in streams.items():
            for width in (2, 3, 4):
                for start in range(len(digits) - width + 1):
                    block = digits[start:start + width]
                    if not block[0]:
                        continue
                    value = sum(d * base**(width - i - 1) for i, d in enumerate(block))
                    if value >= 2 and all(value % p for p in range(2, math.isqrt(value) + 1)):
                        support.setdefault(value, set()).add(base)
        expected = [{"prime": p, "bases": sorted(bs)} for p, bs in sorted(support.items()) if len(bs) > 1]
        self.assertEqual(controls.recurrence(streams)["primes"], expected)

    def test_shuffle_and_rejection(self):
        digits = [0, 0, 1, 2, 2, 2, 5, 7] * 4
        actual = controls.shuffled(digits, controls.Draws("test"))
        self.assertEqual(Counter(actual), Counter(digits))
        self.assertEqual(actual, controls.shuffled(digits, controls.Draws("test")))
        self.assertNotEqual(actual, digits)
        class Forced(controls.Draws):
            def __init__(self):
                self.values = iter([b"\xff", b"\x04"])
            def bytes(self, size):
                return next(self.values)
        self.assertEqual(Forced().below(3), 1)

    def test_rank_ties_and_nonzero_tail(self):
        self.assertEqual(controls.summary(8, [7, 8, 9])["upper_tail_rank"], [3, 4])
        self.assertEqual(controls.summary(10, [7, 8, 9])["upper_tail_rank"], [1, 4])
        self.assertEqual(controls.summary(1, [7, 8, 9])["upper_tail_rank"], [4, 4])

    def test_receipt_sources_and_replay(self):
        receipt = json.loads(controls.RECEIPT.read_text())
        payload = dict(receipt)
        claimed = payload.pop("receipt_sha256")
        self.assertEqual(claimed, scan.sha256_bytes(scan.canonical_json_bytes(payload)))
        for path, digest in receipt["sources_sha256"].items():
            self.assertEqual(digest, scan.sha256_bytes((ROOT / path).read_bytes()), path)
        self.assertEqual(len(receipt["replicates"]), 199)
        replay = controls.run_controls(2)
        self.assertEqual(replay["replicates"], receipt["replicates"][:2])
        self.assertEqual(controls.render_report(receipt), controls.REPORT.read_text())


if __name__ == "__main__":
    unittest.main()
