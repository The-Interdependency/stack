from __future__ import annotations

import importlib.util
import json
import os
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
    def test_publication_rejects_aliases_and_input_collisions(self) -> None:
        receipt = json.loads(pi_radix.DEFAULT_RECEIPT.read_text())
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output, alias = root / "receipt", root / "alias"
            output.write_bytes(b"old")
            with self.assertRaisesRegex(ValueError, "must not alias"):
                pi_radix.write_outputs(receipt, output, output)
            alias.symlink_to(output)
            with self.assertRaisesRegex(ValueError, "must not alias"):
                pi_radix.write_outputs(receipt, output, alias)
            alias.unlink()
            os.link(output, alias)
            with self.assertRaisesRegex(ValueError, "must not alias"):
                pi_radix.write_outputs(receipt, output, alias)
            with self.assertRaisesRegex(ValueError, "aliases an input"):
                pi_radix.publish_artifacts([(alias, b"new")], [output])
            self.assertEqual(output.read_bytes(), b"old")
            self.assertEqual(alias.read_bytes(), b"old")

    def test_publication_stages_all_targets_before_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output, report = root / "receipt", root / "reports" / "report"
            report.parent.mkdir()
            output.write_bytes(b"old receipt")
            report.write_bytes(b"old report")
            with self.assertRaisesRegex(ValueError, "not a regular file"):
                pi_radix.publish_artifacts([(output, b"new"), (report.parent, b"invalid")])
            original = pi_radix.tempfile.mkstemp
            def deny_report_stage(*args, **kwargs):
                if Path(kwargs["dir"]) == report.parent:
                    raise PermissionError("report staging denied")
                return original(*args, **kwargs)
            with patch.object(pi_radix.tempfile, "mkstemp", side_effect=deny_report_stage):
                with self.assertRaisesRegex(PermissionError, "report staging denied"):
                    pi_radix.publish_artifacts([(output, b"new receipt"), (report, b"new report")])
            self.assertEqual(output.read_bytes(), b"old receipt")
            self.assertEqual(report.read_bytes(), b"old report")
            self.assertFalse(list(root.rglob(".*")))

    def test_publication_rolls_back_replacement_failure(self) -> None:
        for existed in (True, False):
            with self.subTest(existed=existed), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                output, report = root / "receipt", root / "report"
                if existed:
                    output.write_bytes(b"old receipt")
                report.write_bytes(b"old report")
                original = pi_radix.os.replace
                def deny_report_replace(source, target):
                    if target == report:
                        raise PermissionError("report replacement denied")
                    return original(source, target)
                with patch.object(pi_radix.os, "replace", side_effect=deny_report_replace):
                    with self.assertRaisesRegex(PermissionError, "report replacement denied"):
                        pi_radix.publish_artifacts([(output, b"new receipt"), (report, b"new report")])
                self.assertEqual(output.exists(), existed)
                if existed:
                    self.assertEqual(output.read_bytes(), b"old receipt")
                self.assertEqual(report.read_bytes(), b"old report")
                self.assertFalse(list(root.glob(".*")))
                pi_radix.publish_artifacts([(output, b"new receipt"), (report, b"new report")])
                self.assertEqual(output.read_bytes(), b"new receipt")
                self.assertEqual(report.read_bytes(), b"new report")
                self.assertFalse(list(root.glob(".*")))

    def test_oversized_horizon_rejected_before_exact_horizon_work(self) -> None:
        original = json.loads((ROOT / "EXPERIMENT.json").read_text())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            config = original | dict(bases=list(range(2, 1414)), fractional_symbol_count=2,
                                    matched_information_horizon_bits=1000000, prime_block_lengths=[1])
            path.write_text(json.dumps(config))
            with patch.object(pi_radix, "horizon_count", side_effect=AssertionError("expensive horizon work")), \
                 patch.object(pi_radix, "chudnovsky_pi") as generate:
                with self.assertRaisesRegex(ValueError, "horizon exceeds generated stream"):
                    pi_radix.run_experiment(path)
                generate.assert_not_called()
            # Exact-power and between-power edges: floor(log_4(2**13)) is 6,
            # whereas 14 bits admits a seventh symbol and must be rejected.
            for horizon in (12, 13, 14):
                config.update(bases=[4], fractional_symbol_count=6, matched_information_horizon_bits=horizon)
                path.write_text(json.dumps(config))
                if horizon == 14:
                    with self.assertRaisesRegex(ValueError, "horizon exceeds generated stream"):
                        pi_radix.load_config(path)
                else:
                    self.assertEqual(pi_radix.load_config(path), config)

    def test_phase_report_counts_positions_separately_from_groups(self) -> None:
        config = json.loads((ROOT / "EXPERIMENT.json").read_text())
        config.update(bases=list(range(2, 31)), fractional_symbol_count=100,
                      matched_information_horizon_bits=100, prime_block_lengths=[1])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            path.write_text(json.dumps(config))
            receipt = pi_radix.run_experiment(path)
            phases = receipt["cross_base_results"]["aligned_exact_angular_phase_matches"]
            self.assertEqual(len(phases), 279)
            self.assertEqual(len({row["position"] for row in phases}), 100)
            self.assertIn("in at least two bases: **100** (**279** phase groups)", pi_radix.render_report(receipt))

    def test_scan_rejects_midrun_source_changes_without_publication(self) -> None:
        for target in ("config", "implementation"):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source = root / "pi_radix.py"
                source.write_bytes((ROOT / "pi_radix.py").read_bytes())
                spec = importlib.util.spec_from_file_location("scan_snapshot_test", source)
                subject = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(subject)
                config = json.loads((ROOT / "EXPERIMENT.json").read_text())
                config.update(bases=[30], fractional_symbol_count=30, matched_information_horizon_bits=100)
                config_path = root / "config.json"
                config_path.write_text(json.dumps(config))
                output, report = root / "receipt.json", root / "report.md"
                output.write_text("old receipt")
                report.write_text("old report")
                original = subject.chudnovsky_pi
                changed = config_path if target == "config" else source
                def edit_during_generation(precision):
                    changed.write_bytes(changed.read_bytes() + b"\n")
                    return original(precision)
                with patch.object(subject, "chudnovsky_pi", side_effect=edit_during_generation):
                    with self.assertRaisesRegex(ValueError, "source changed during execution"):
                        subject.main(["scan", "--config", str(config_path), "--output", str(output), "--report", str(report)])
                self.assertEqual(output.read_text(), "old receipt")
                self.assertEqual(report.read_text(), "old report")
                if target == "implementation":
                    with patch.object(subject, "chudnovsky_pi") as generate:
                        with self.assertRaisesRegex(ValueError, "differs from loaded implementation"):
                            subject.run_experiment(config_path)
                        generate.assert_not_called()

    def test_unimplemented_rules_rejected_before_generation(self) -> None:
        original = json.loads((ROOT / "EXPERIMENT.json").read_text())
        for field in pi_radix.SUPPORTED_RULES:
            for replacement in ("e" if field == "constant" else "unsupported rule", None):
                with self.subTest(field=field, replacement=replacement), tempfile.TemporaryDirectory() as directory:
                    config = original.copy()
                    if replacement is None:
                        del config[field]
                    else:
                        config[field] = replacement
                    path = Path(directory) / "config.json"
                    path.write_text(json.dumps(config))
                    with patch.object(pi_radix, "chudnovsky_pi") as generate:
                        with self.assertRaisesRegex(ValueError, f"unsupported {field}"):
                            pi_radix.run_experiment(path)
                        generate.assert_not_called()

    def test_decimal_generation_work_rejected_before_generation(self) -> None:
        original = json.loads((ROOT / "EXPERIMENT.json").read_text())
        for bases, count, message in (([100000], 100000, "decimal precision"),
                                      ([99999, 100000], 1600, "generation digit work")):
            with self.subTest(bases=bases), tempfile.TemporaryDirectory() as directory:
                config = original | dict(bases=bases, fractional_symbol_count=count,
                                        matched_information_horizon_bits=17, prime_block_lengths=[1])
                path = Path(directory) / "config.json"
                path.write_text(json.dumps(config))
                with patch.object(pi_radix, "chudnovsky_pi") as generate:
                    with self.assertRaisesRegex(ValueError, message):
                        pi_radix.run_experiment(path)
                    generate.assert_not_called()

    def test_aggregate_admission_precedes_generation(self) -> None:
        original = json.loads((ROOT / "EXPERIMENT.json").read_text())
        cases = [
            (dict(bases=list(range(2, 100001)), fractional_symbol_count=100000,
                  matched_information_horizon_bits=100000, prime_block_lengths=[1]), "symbol"),
            (dict(bases=[2], fractional_symbol_count=1000,
                  matched_information_horizon_bits=64, prime_block_lengths=list(range(1, 65))), "block"),
            (dict(bases=list(range(90000, 90012)), fractional_symbol_count=2,
                  matched_information_horizon_bits=17, prime_block_lengths=[1]), "sieve"),
        ]
        for changes, budget in cases:
            with self.subTest(budget=budget), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "config.json"
                path.write_text(json.dumps(original | changes))
                with patch.object(pi_radix, "chudnovsky_pi") as generate, \
                     patch.object(pi_radix, "prime_sieve") as sieve:
                    with self.assertRaisesRegex(ValueError, f"aggregate .*{budget}"):
                        pi_radix.run_experiment(path)
                    generate.assert_not_called()
                    sieve.assert_not_called()

    def test_sieve_rejects_allocation_before_bytearray(self) -> None:
        with patch("builtins.bytearray", side_effect=AssertionError("allocation attempted")):
            for limit in (pi_radix.MAX_BASE, 1_000_000_007, 2**64):
                with self.subTest(limit=limit), self.assertRaisesRegex(ValueError, "sieve limit"):
                    pi_radix.prime_sieve(limit)
        self.assertEqual(len(pi_radix.prime_sieve(pi_radix.MAX_BASE - 1)), 9592)

    def test_u64_exact_power_domains(self) -> None:
        original = json.loads((ROOT / "EXPERIMENT.json").read_text())
        for base, width in ((2, 64), (4, 32), (16, 16)):
            with self.subTest(base=base), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "config.json"
                config = original | dict(bases=[base], fractional_symbol_count=width,
                                        matched_information_horizon_bits=64, prime_block_lengths=[width])
                path.write_text(json.dumps(config))
                self.assertEqual(pi_radix.load_config(path), config)
                result = pi_radix.run_experiment(path)
                self.assertEqual(result["base_results"][0]["blocks"][str(width)]["window_count"], 1)
                digits = [base - 1] * width
                self.assertEqual(pi_radix.decode_block(digits, base), 2**64 - 1)
                self.assertEqual(pi_radix.analyze_base(base, digits, [width])["blocks"][str(width)]["prime_count"], 0)
                config.update(fractional_symbol_count=width + 1, prime_block_lengths=[width + 1])
                path.write_text(json.dumps(config))
                with self.assertRaisesRegex(ValueError, "unsigned-64-bit"):
                    pi_radix.load_config(path)
        self.assertTrue(pi_radix.is_prime_u64(2**64 - 59))
        with self.assertRaises(ValueError):
            pi_radix.is_prime_u64(2**64)

    def test_prime_radix_terminal_exception(self) -> None:
        for base in (2, 3, 359, 4, 360):
            block = pi_radix.analyze_base(base, [1, 0], [2])["blocks"]["2"]
            self.assertEqual(block["terminal_gcd_eligible_count"], 1)
            self.assertEqual(block["prime_count"], int(base in (2, 3, 359)))

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
        # Exact reduced nonzero equality must survive the shorter third stream,
        # including when input ordering changes; singleton tails cannot match.
        scans = [pi_radix.analyze_base(base, digits, [1]) for base, digits in
                 ((4, [0, 2, 3]), (6, [1, 3]), (5, [1]))]
        for ordered in (scans, list(reversed(scans))):
            matches = pi_radix.cross_base_results(ordered)["aligned_exact_angular_phase_matches"]
            self.assertEqual(len(matches), 1)
            self.assertEqual((matches[0]["position"], matches[0]["turn"]), (2, [1, 2]))
            self.assertEqual({s["base"] for s in matches[0]["symbols"]}, {4, 6})

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
