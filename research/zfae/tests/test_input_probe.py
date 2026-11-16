# ratios: loc_comments=39:25 imports_exports=6:4 calls_definitions=17:4
"""Harness falsifiers, not tests of an invented inference engine.

Usage: python -m unittest discover -s research/zfae/tests -v
Only synthetic inputs and temporary local files are used.
"""
from pathlib import Path
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import input_probe

# === CHECKS ===
# id: zfae_probe_rejects_mutated_source
#   proves: zfae_probe_pins_before_execution
#   call: self::test_source_mismatch_precedes_execution
#   mutates: filesystem
#   cleanup: tempdir_teardown
# id: zfae_probe_control_failures_block
#   proves: zfae_probe_controls_interpretation
#   call: self::test_controls_and_nondeterminism_block
#   mutates: none
#   cleanup: none
# id: zfae_probe_identity_and_collision_controls
#   proves: zfae_probe_preserves_counterexamples
#   call: self::test_identity_witness_and_case_collision
#   mutates: none
#   cleanup: none
# === END CHECKS ===


def test_source_mismatch_precedes_execution():
    """Modified input must be refused before its top-level code runs."""
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "parser.py"
        source.write_text("raise RuntimeError('untrusted source ran')\n")
        try:
            input_probe.run(source)
        except ValueError as exc:
            assert "source Git blob mismatch" in str(exc)
        else:
            raise AssertionError("modified source admitted")


def test_controls_and_nondeterminism_block():
    """A broken constant witness and an unstable witness cannot earn a result."""
    pairs = json.loads((input_probe.HERE / "INPUT_PROBE.json").read_text())["pairs"]
    assert input_probe.evaluate(pairs, lambda _: {})["standing"] == "BLOCKED"
    counter = iter(range(100))
    result = input_probe.evaluate(pairs, lambda text: {"text": text, "call": next(counter)})
    assert result["standing"] == "BLOCKED"
    assert all(not row["replay_equal"] for row in result["observations"])


def test_identity_witness_and_case_collision():
    """An exact witness survives; a lossy case view retains its counterexample."""
    pairs = json.loads((input_probe.HERE / "INPUT_PROBE.json").read_text())["pairs"]
    intact = input_probe.evaluate(pairs, lambda text: {"scalar_sequence": list(map(ord, text))})
    assert intact["standing"] == "SURVIVED"
    assert intact["collision_ids"] == []
    lossy = input_probe.evaluate(pairs, lambda text: {"text": text.lower()})
    assert lossy["standing"] == "FALSIFIED"
    assert lossy["collision_ids"] == ["letter-case"]
    assert len(lossy["observations"]) == len(pairs)


def load_tests(loader, tests, pattern):
    """Expose the source-linked witness functions to stdlib unittest."""
    return unittest.TestSuite(unittest.FunctionTestCase(fn) for fn in (
        test_source_mismatch_precedes_execution,
        test_controls_and_nondeterminism_block,
        test_identity_witness_and_case_collision,
    ))
# ratios: loc_comments=39:25 imports_exports=6:4 calls_definitions=17:4
