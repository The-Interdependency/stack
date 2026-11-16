# === CHECKS ===
# id: frame_consumer_full_population_check
#   proves: frame_consumer_replays_complete_population, frame_consumer_deterministic_receipt
#   call: self::test_full_population_and_replay
#   requires: python3, git
#   mutates: none
#   cleanup: none
# id: frame_consumer_scope_check
#   proves: frame_consumer_preserves_relation_scope
#   call: self::test_anchor_scope_rejections
#   requires: python3, git
#   mutates: none
#   cleanup: none
# id: frame_consumer_wrong_commit_check
#   proves: frame_consumer_admits_exact_sources
#   call: self::test_wrong_commit_rejected
#   requires: python3, git
#   mutates: none
#   cleanup: none
# id: frame_consumer_dirty_bytes_check
#   proves: frame_consumer_admits_exact_sources
#   call: self::test_dirty_source_rejected
#   requires: python3, git
#   mutates: filesystem
#   cleanup: tempdir_teardown
# id: frame_consumer_receipt_mutation_check
#   proves: frame_consumer_admits_exact_sources
#   call: self::test_altered_receipt_rejected
#   requires: python3, git
#   mutates: filesystem
#   cleanup: tempdir_teardown
# id: frame_consumer_record_validation_check
#   proves: frame_consumer_replays_complete_population, frame_consumer_preserves_relation_scope
#   call: self::test_malformed_records_rejected
#   requires: python3, git
#   mutates: none
#   cleanup: none
# === END CHECKS ===

"""Usage: UCNS_COMPARISON_ROOT=/exact/ucns python research/urpcs/frame_comparison_tests.py.

Six accountable consumer tests; no third-party dependency. They deliberately
live outside the frozen codec's test discovery and have a dedicated CI gate.
Synthetic negative fixtures test rejection only; population claims use the
complete hash-admitted sealed receipt.
"""
from __future__ import annotations

import os
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import urpcs_frame_comparison as consumer


def roots() -> tuple[Path, Path]:
    return Path(__file__).resolve().parents[2], Path(os.environ["UCNS_COMPARISON_ROOT"])


def context():
    stack, ucns = roots()
    native, geometry = consumer.load_geometry(ucns)
    _, rows = consumer.read_population(stack / consumer.SEALED_PATH, native)
    return native, geometry, rows


def rejects(call) -> None:
    try:
        call()
    except consumer.FrameComparisonError:
        return
    raise AssertionError("invalid input was accepted")


def test_full_population_and_replay() -> None:
    stack, ucns = roots()
    first = consumer.run(stack, ucns)
    second = consumer.run(stack, ucns)
    assert consumer.json_bytes(first) == consumer.json_bytes(second)
    assert first["population"]["observations"] == 2737
    assert first["original_geometry_probe"]["checks"] == 120
    assert first["original_geometry_probe"]["naive_product_changes"] == 44
    assert first["shared_anchor_probe"]["pairs"] > 0
    assert first["existing_attachment_probe"]["edges"] > 0
    for name in ("original_geometry_probe", "shared_anchor_probe", "existing_attachment_probe"):
        assert first[name]["corrected_changes"] == 0
    payload = dict(first)
    expected = payload.pop("payload_sha256")
    assert consumer.digest(consumer.json_bytes(payload)) == expected


def test_anchor_scope_rejections() -> None:
    native, geometry, rows = context()
    left = rows[0]
    assert consumer.compare_local(left, left, native, geometry).relative_turns == Fraction(0)
    for key in ("case_id", "origin", "gonol"):
        changed = dict(left, **{key: left[key] + "-different"})
        rejects(lambda: consumer.compare_local(left, changed, native, geometry))
        missing = dict(left)
        del missing[key]
        rejects(lambda: consumer.compare_local(missing, missing, native, geometry))
    other = next(row for row in rows if row["origin"] != left["origin"])
    rejects(lambda: consumer.compare_local(left, other, native, geometry))


def test_wrong_commit_rejected() -> None:
    _, ucns = roots()
    with patch.object(consumer.subprocess, "check_output", return_value="0" * 40):
        rejects(lambda: consumer.load_geometry(ucns))


def test_dirty_source_rejected() -> None:
    _, ucns = roots()
    for dirty in consumer.UCNS_FILES:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for path in consumer.UCNS_FILES:
                destination = root / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes((ucns / path).read_bytes() + (b"\n# planted byte mutation\n" if path == dirty else b""))
            # Simulate an unchanged HEAD while consumed worktree bytes differ.
            # This is a negative admission fixture, not an execution receipt.
            with patch.object(consumer.subprocess, "check_output", return_value=consumer.UCNS_COMMIT):
                rejects(lambda: consumer.load_geometry(root))


def test_altered_receipt_rejected() -> None:
    stack, ucns = roots()
    native, _ = consumer.load_geometry(ucns)
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "receipt.json"
        path.write_bytes((stack / consumer.SEALED_PATH).read_bytes() + b" ")
        rejects(lambda: consumer.read_population(path, native))


def test_malformed_records_rejected() -> None:
    native, _, rows = context()
    row = rows[0]
    for phase in (0.5, "(0,0)", "(8,8)", "(0,16)", "(1.0,8)", "(0,8) trailing"):
        rejects(lambda: consumer.native_state(dict(row, phase=phase), native))
    for displacement in (True, 0.0, "0"):
        rejects(lambda: consumer.native_state(dict(row, S=displacement), native))
    rejects(lambda: consumer.native_state(dict(row, S=row["S"] + 8), native))


if __name__ == "__main__":
    tests = (
        test_full_population_and_replay,
        test_anchor_scope_rejections,
        test_wrong_commit_rejected,
        test_dirty_source_rejected,
        test_altered_receipt_rejected,
        test_malformed_records_rejected,
    )
    suite = unittest.TestSuite(unittest.FunctionTestCase(test) for test in tests)
    outcome = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if outcome.wasSuccessful() and not outcome.skipped else 1)
