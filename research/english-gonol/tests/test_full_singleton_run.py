# === CHECKS ===
# id: check_full_singleton_construct_deterministic
#   proves: full_singleton_construct_is_finite_and_deterministic
#   call: self::test_full_construct_builds_deterministically
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_full_singleton_construct_run_and_replay
#   proves: full_singleton_construct_replays_byte_identically, full_singleton_construct_preserves_occurrence_ordinals_and_provenance
#   call: self::test_full_construct_run_and_replay
#   requires: python3
#   timeout: 30
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_full_singleton_construct_tangency_hmmm
#   proves: full_singleton_construct_never_invents_ucns_geometry
#   call: self::test_full_construct_tangency_verdicts_are_hmmm
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===

import os
from pathlib import Path

import pytest

from english_gonol.full_singleton_run import (
    FullSingletonError,
    UCNS_SINGLETON_GEOMETRY_COMMIT,
    build_full_construct,
    run,
    verify_replay,
)
from test_definition_affixiation_run import _snapshot


def _ucns_source_root() -> Path | None:
    root = Path(os.environ.get("UCNS_SOURCE_ROOT", Path.home() / "src" / "ucns")).resolve()
    if not (root / "src" / "ucns" / "singleton_geometry.py").is_file():
        return None
    return root


_ucns_available = _ucns_source_root() is not None


def test_full_construct_builds_deterministically() -> None:
    if not _ucns_available:
        pytest.skip("pinned UCNS singleton-geometry checkout is unavailable")
    root = _ucns_source_root()
    assert root is not None

    first, first_counts = build_full_construct(_snapshot(), ucns_source_root=root)
    second, second_counts = build_full_construct(_snapshot(), ucns_source_root=root)

    assert first_counts == second_counts
    assert first.receipt_sha256() == second.receipt_sha256()
    assert first.replay_equals(second)
    assert first_counts["characters"] >= 1
    assert first_counts["words"] >= 1
    assert first_counts["sentences"] >= 1
    assert first_counts["higher"] >= 1


def test_full_construct_run_and_replay(tmp_path: Path) -> None:
    if not _ucns_available:
        pytest.skip("pinned UCNS singleton-geometry checkout is unavailable")
    root = _ucns_source_root()
    assert root is not None

    manifest = run(_snapshot(), out_dir=tmp_path, ucns_source_root=root)
    verified = verify_replay(tmp_path)

    assert verified["receipt_sha256"] == manifest["receipt_sha256"]
    assert verified["schema"] == manifest["schema"]
    assert verified["coverage"]["no_sampling"] is True
    assert len(manifest["receipt_sha256"]) == 64

    (tmp_path / "construct.json").write_text("tampered\n", encoding="utf-8")
    with pytest.raises(FullSingletonError):
        verify_replay(tmp_path)


def test_full_construct_tangency_verdicts_are_hmmm() -> None:
    if not _ucns_available:
        pytest.skip("pinned UCNS singleton-geometry checkout is unavailable")
    root = _ucns_source_root()
    assert root is not None

    construct, _counts = build_full_construct(_snapshot(), ucns_source_root=root)
    tangencies = construct.tangencies
    assert tangencies
    assert all(record.status == "hmmm" for record in tangencies)
    assert all(record.center_distance_turns is None for record in tangencies)
    assert all("undeclared" in record.reason for record in tangencies)
