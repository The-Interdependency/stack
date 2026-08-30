from __future__ import annotations

# === CHECKS ===
# id: check_canon_manifest_complete
#   proves: metapat_canon_manifest_complete
#   call: self::test_manifest_names_all_canon_files
#   mutates: none
#   cleanup: none
#
# id: check_repository_canon_files_match
#   proves: metapat_canon_files_match_repository
#   call: self::test_repository_canon_files_match_manifest
#   mutates: filesystem_read
#   cleanup: none
#
# id: check_canon_file_drift_visible
#   proves: metapat_canon_file_drift_visible
#   call: self::test_canon_file_drift_is_reported
#   mutates: tempdir
#   cleanup: tempdir_teardown
# === END CHECKS ===

from pathlib import Path

import pytest

import metapat.canon as canon_module
from metapat import (
    CANON_FILE_BLOBS,
    ROOT_SPINE,
    CanonIntegrityError,
    assert_canon_files_match,
    canon_file_mismatches,
    canon_manifest_digest,
    canonical_canon_manifest_data,
    definitions,
    git_blob_sha1,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_manifest_names_all_canon_files() -> None:
    assert set(CANON_FILE_BLOBS) == {
        "AXIOMS.md",
        "CHAPTER_ZERO.md",
        "DOMAIN_RESTRAINT.md",
        "GLOSSARY.md",
        "POSTULATES.md",
        "THEOREMS.md",
        "THEORIES.md",
    }
    assert all(len(blob) == 40 for blob in CANON_FILE_BLOBS.values())
    assert canonical_canon_manifest_data()["files"] == dict(sorted(CANON_FILE_BLOBS.items()))
    assert len(canon_manifest_digest()) == 64


def test_repository_canon_files_match_manifest() -> None:
    assert canon_file_mismatches(REPO_ROOT) == {}
    assert_canon_files_match(REPO_ROOT)

    axioms = (REPO_ROOT / "AXIOMS.md").read_text(encoding="utf-8")
    chapter_zero = (REPO_ROOT / "CHAPTER_ZERO.md").read_text(encoding="utf-8")
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    for statement in ROOT_SPINE:
        assert statement in axioms
        assert statement in chapter_zero
    assert definitions()["METAPAT"] in readme


def test_canon_file_drift_is_reported(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    original = b"canon bytes\n"
    expected = git_blob_sha1(original)
    monkeypatch.setattr(canon_module, "CANON_FILE_BLOBS", {"ONE.md": expected})
    path = tmp_path / "ONE.md"
    path.write_bytes(original)
    assert canon_module.canon_file_mismatches(tmp_path) == {}
    path.write_bytes(original + b"drift")
    mismatches = canon_module.canon_file_mismatches(tmp_path)
    assert mismatches["ONE.md"]["expected"] == expected
    assert mismatches["ONE.md"]["observed"] != expected
    with pytest.raises(CanonIntegrityError, match="ONE.md"):
        canon_module.assert_canon_files_match(tmp_path)
