from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pi_radix", ROOT / "pi_radix.py")
assert SPEC and SPEC.loader
pi_radix = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pi_radix)


# === CHECKS ===
# id: check_pi_radix_precision_agreement
#   proves: pi_radix_precision_agreement
#   call: self::test_default_receipt_matches_regeneration
#   requires: python3
#   timeout: natural_completion
#   mutates: temporary_files
#   cleanup: temporary_directory
#
# id: check_pi_radix_exact_angular_identity
#   proves: pi_radix_exact_angular_identity
#   call: self::test_angular_symbol_is_exact
#   requires: python3
#   timeout: natural_completion
#   mutates: none
#   cleanup: none
#
# id: check_pi_radix_prime_claim_bounded
#   proves: pi_radix_prime_claim_bounded
#   call: self::test_primality_and_terminal_sieve
#   requires: python3
#   timeout: natural_completion
#   mutates: none
#   cleanup: none
#
# id: check_pi_radix_receipt_deterministic
#   proves: pi_radix_receipt_deterministic
#   call: self::test_default_receipt_matches_regeneration
#   requires: python3
#   timeout: natural_completion
#   mutates: temporary_files
#   cleanup: temporary_directory
#
# id: check_pi_radix_known_digits
#   proves: pi_radix_precision_agreement
#   call: self::test_base_digits_known_values
#   mutates: none
#   cleanup: none
#
# id: check_pi_radix_domain_limit
#   proves: pi_radix_prime_claim_bounded
#   call: self::test_config_rejects_unbounded_prime_domain
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_pi_radix_config_guards
#   proves: pi_radix_configuration_faithful
#   call: self::test_config_guards
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_pi_radix_custom_report
#   proves: pi_radix_configuration_faithful
#   call: self::test_custom_report_and_no_partial_render_write
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_pi_radix_overlap
#   proves: pi_radix_overlap_complete
#   call: self::test_unequal_prefix_overlap
#   mutates: none
#   cleanup: none
# === END CHECKS ===


class TestPiRadix(unittest.TestCase):
    def test_config_guards(self) -> None:
        original = json.loads((ROOT / "EXPERIMENT.json").read_text())
        for change in (
            {"fractional_symbol_count": 5, "matched_information_horizon_bits": 100, "bases": [30]},
            {"bases": [1_000_000_007], "prime_block_lengths": [1]},
        ):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "config.json"
                path.write_text(json.dumps(original | change))
                with self.assertRaises(ValueError):
                    pi_radix.load_config(path)
        with self.assertRaises(ValueError):
            pi_radix.analyze_base(1_000_000_007, [1], [1])
        self.assertEqual(pi_radix.horizon_count(4, 12), 6)
        self.assertEqual(pi_radix.horizon_count(3, 12), 7)

    def test_custom_report_and_no_partial_render_write(self) -> None:
        config = json.loads((ROOT / "EXPERIMENT.json").read_text())
        config.update(bases=[30], fractional_symbol_count=30,
                      matched_information_horizon_bits=100, prime_block_lengths=[1, 2])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps(config))
            receipt = pi_radix.run_experiment(path)
            report = pi_radix.render_report(receipt)
            self.assertIn("first 30 fractional symbols", report)
            self.assertIn("100-bit profile", report)
            self.assertNotIn("L3 eligible", report)
            output, projection = Path(directory) / "result.json", Path(directory) / "report.md"
            output.write_text("unchanged")
            projection.write_text("unchanged")
            with patch.object(pi_radix, "render_report", side_effect=ValueError("injected")):
                with self.assertRaises(ValueError):
                    pi_radix.write_outputs(receipt, output, projection)
            self.assertEqual(output.read_text(), "unchanged")
            self.assertEqual(projection.read_text(), "unchanged")

    def test_unequal_prefix_overlap(self) -> None:
        scans = [pi_radix.analyze_base(base, [0] * length, [1, 2])
                 for base, length in ((2, 12), (3, 7), (4, 6))]
        matches = pi_radix.cross_base_results(scans)["aligned_exact_angular_phase_matches"]
        self.assertEqual([m["position"] for m in matches], list(range(1, 8)))
        self.assertEqual([s["base"] for s in matches[-1]["symbols"]], [2, 3])

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
