"""Entitlement gate regression tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

STACK_ROOT = Path(__file__).resolve().parents[3]
if str(STACK_ROOT) not in sys.path:
    sys.path.insert(0, str(STACK_ROOT))

from ahbg.runtime.entitlements import (
    ENTITLEMENT_BENCHMARK_LAB,
    EntitlementError,
    EntitlementGate,
    GATED_FEATURES,
)


class EntitlementTests(unittest.TestCase):
    def test_basic_is_always_present(self) -> None:
        gate = EntitlementGate()
        self.assertIn("basic", gate.entitlements)
        self.assertFalse(gate.has_benchmark_lab())

    def test_benchmark_lab_unlocks_all_gated_features(self) -> None:
        gate = EntitlementGate.from_claims([ENTITLEMENT_BENCHMARK_LAB])
        for feature in GATED_FEATURES:
            gate.require(feature)  # must not raise

    def test_gated_features_fail_closed_without_entitlement(self) -> None:
        gate = EntitlementGate()
        for feature in GATED_FEATURES:
            with self.assertRaises(EntitlementError):
                gate.require(feature)

    def test_unknown_feature_rejected(self) -> None:
        with self.assertRaises(ValueError):
            EntitlementGate.from_claims([ENTITLEMENT_BENCHMARK_LAB]).require("not_a_feature")


if __name__ == "__main__":
    unittest.main()
