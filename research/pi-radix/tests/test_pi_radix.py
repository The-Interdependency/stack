from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from decimal import Decimal
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pi_radix", ROOT / "pi_radix.py")
assert SPEC and SPEC.loader
pi_radix = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pi_radix)


# === CHECKS ===
# id: check_pi_radix_precision_agreement
#   proves: pi_radix_precision_agreement
#   call: TestPiRadix::test_default_receipt_matches_regeneration
#   requires: python3
#   timeout: natural_completion
#   mutates: temporary_files
#   cleanup: temporary_directory
#
# id: check_pi_radix_exact_angular_identity
#   proves: pi_radix_exact_angular_identity
#   call: TestPiRadix::test_angular_symbol_is_exact
#   requires: python3
#   timeout: natural_completion
#   mutates: none
#   cleanup: none
#
# id: check_pi_radix_prime_claim_bounded
#   proves: pi_radix_prime_claim_bounded
#   call: TestPiRadix::test_primality_and_terminal_sieve
#   requires: python3
#   timeout: natural_completion
#   mutates: none
#   cleanup: none
#
# id: check_pi_radix_receipt_deterministic
#   proves: pi_radix_receipt_deterministic
#   call: TestPiRadix::test_default_receipt_matches_regeneration
#   requires: python3
#   timeout: natural_completion
#   mutates: temporary_files
#   cleanup: temporary_directory
# === END CHECKS ===


class TestPiRadix(unittest.TestCase):
    def test_base_digits_known_values(self) -> None:
        integer, decimal_digits = pi_radix.base_digits(Decimal("3.141592653589793238462643383279"), 10, 12)
        self.assertEqual(integer, 3)
        self.assertEqual(decimal_digits, [1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9])

        pi_value = pi_radix.chudnovsky_pi(160)
        _, digits_360 = pi_radix.base_digits(pi_value, 360, 20)
        self.assertEqual(
            digits_360,
            [50, 350, 146, 304, 186, 268, 328, 34, 198, 290, 178, 36, 331, 186, 77, 39, 35, 13, 89, 249],
        )

        # Regression: extraction once inherited Decimal's default 28-digit
        # ambient context and silently emitted zeros through the tail.
        pi_value = pi_radix.chudnovsky_pi(400)
        _, deep_digits_360 = pi_radix.base_digits(pi_value, 360, 100)
        self.assertEqual(deep_digits_360[49], 263)
        self.assertEqual(deep_digits_360[99], 120)
        self.assertGreater(len(set(deep_digits_360[28:])), 1)

    def test_angular_symbol_is_exact(self) -> None:
        symbol = pi_radix.angular_symbol(360, 50)
        self.assertEqual(symbol["turn"], [5, 36])
        self.assertEqual(symbol["degrees"], [50, 1])
        self.assertEqual(symbol["pi_radian_coefficient"], [5, 18])
        self.assertEqual(Fraction(*symbol["turn"]), Fraction(50, 360))
        with self.assertRaises(ValueError):
            pi_radix.angular_symbol(360, 360)

    def test_primality_and_terminal_sieve(self) -> None:
        self.assertTrue(pi_radix.is_prime_u64(13_291))
        self.assertTrue(pi_radix.is_prime_u64(1_722_580_637))
        self.assertFalse(pi_radix.is_prime_u64(360 * 36 + 330))
        self.assertEqual(pi_radix.decode_block([36, 331], 360), 13_291)
        for last_digit in range(360):
            value = pi_radix.decode_block([1, last_digit], 360)
            self.assertEqual(math_gcd(value, 360), math_gcd(last_digit, 360))

    def test_config_rejects_unbounded_prime_domain(self) -> None:
        config = json.loads((ROOT / "EXPERIMENT.json").read_text(encoding="utf-8"))
        config["bases"] = [2**32]
        config["prime_block_lengths"] = [1, 2]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps(config), encoding="utf-8")
            with self.assertRaises(ValueError):
                pi_radix.load_config(path)

    def test_default_receipt_matches_regeneration(self) -> None:
        expected = json.loads((ROOT / "receipts" / "pi-radix-scan-v1.json").read_text(encoding="utf-8"))
        actual = pi_radix.run_experiment(ROOT / "EXPERIMENT.json")
        self.assertEqual(actual, expected)
        payload = dict(actual)
        digest = payload.pop("receipt_sha256")
        self.assertEqual(pi_radix.sha256_bytes(pi_radix.canonical_json_bytes(payload)), digest)
        self.assertEqual(
            (ROOT / "docs" / "pi-radix-scan-v1.md").read_text(encoding="utf-8"),
            pi_radix.render_report(actual),
        )


def math_gcd(left: int, right: int) -> int:
    while right:
        left, right = right, left % right
    return left


if __name__ == "__main__":
    unittest.main()
