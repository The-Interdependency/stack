# ratios: loc_comments=15:32 imports_exports=3:2 calls_definitions=6:2
"""Run this repository's reviewed tests; never authenticate arbitrary witnesses.

Usage: set STACK_DIGITAL_METRICS_SKILL_LIB_ROOT to the graph-pinned checkout,
then run `python research/digital-metrics/run_tests.py` from Stack.
These are trusted checker sources subject to code review. Contract linkage is
a separate no-exec audit; its report supplies zero behavioral proof credit.
"""
from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_digital_metric_repository_test_gate
#   module_name: digital metric repository test gate
#   module_kind: verification-tool
#   summary: execute the fixed reviewed repository suite and reject empty or nonpassing completion
#   owner: The-Interdependency/stack
#   public_surface: main,clean_completion
#   internal_surface: standard unittest discovery and outcome checks
#   auth_boundary: trusted repository checker code, not an arbitrary witness sandbox
#   storage_boundary: temporary files owned and cleaned by the tests
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_metric_protocol.py
#   rollout: dedicated local and CI behavioral gate
#   rollback: revert only with an equivalent nonempty no-skip gate
#   requires: Python standard library and exact source checkouts
#   since: 2026-11-15
#   unresolved: hostile Python execution remains unsupported and receives no attestation
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: digital_metric_repository_tests_require_clean_completion
#   given: the fixed reviewed suite is empty, skipped, expected-failing, unexpectedly successful or assertion-failing
#   then: the repository test gate exits nonzero; only nonempty entirely passing completion exits zero
#   class: correctness
# === END CONTRACTS ===

from pathlib import Path
import unittest


def clean_completion(result: unittest.TestResult) -> bool:
    return bool(result.testsRun) and result.wasSuccessful() and not (
        result.skipped or result.expectedFailures or result.unexpectedSuccesses
    )


def main() -> int:
    suite = unittest.defaultTestLoader.discover(
        str(Path(__file__).resolve().parent / 'tests'), pattern='test*.py'
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if clean_completion(result) else 1


if __name__ == '__main__':
    raise SystemExit(main())
# ratios: loc_comments=15:32 imports_exports=3:2 calls_definitions=6:2
