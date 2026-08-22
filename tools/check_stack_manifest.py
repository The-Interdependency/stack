#!/usr/bin/env python3
"""Validate the stack manifest and root lifecycle contract.

This verifier is intentionally offline. It does not fetch archived repositories or
interpret participant research. It checks that the stack's root provenance record is
internally consistent and that declared stack paths exist.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "stack-manifest.json"
HUMAN_MANIFEST_PATH = ROOT / "STACK_MANIFEST.md"

SCHEMA = "the-interdependency.stack-manifest"
VERSION = "1.0.0"
HEX40 = re.compile(r"^[0-9a-f]{40}$")


def _fail(message: str) -> None:
    raise SystemExit(f"stack manifest check failed: {message}")


def _load_manifest() -> dict[str, Any]:
    try:
        data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        _fail(f"{MANIFEST_PATH.name} is not valid JSON: {error}")
    if not isinstance(data, dict):
        _fail("manifest root must be an object")
    return data


def _canonical_digest(manifest: dict[str, Any]) -> str:
    payload = {
        "repositories": manifest.get("repositories"),
        "boundaries": manifest.get("boundaries"),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _require_text(mapping: dict[str, Any], key: str, *, context: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        _fail(f"{context}.{key} must be non-empty text")
    return value


def _validate_repository(entry: Any, seen: set[str]) -> None:
    if not isinstance(entry, dict):
        _fail("every repositories[] entry must be an object")

    repository = _require_text(entry, "repository", context="repository")
    if repository in seen:
        _fail(f"duplicate repository entry: {repository}")
    seen.add(repository)
    if not repository.startswith("The-Interdependency/"):
        _fail(f"repository is outside The-Interdependency: {repository}")

    commit = _require_text(entry, "commit", context=repository)
    authority = _require_text(entry, "authority", context=repository)
    relation = _require_text(entry, "relation", context=repository)
    archive_status = _require_text(entry, "archive_status", context=repository)
    path_text = _require_text(entry, "path", context=repository)

    if "\n" in authority or "\n" in relation:
        _fail(f"{repository} authority/relation must be single-line text")

    if archive_status == "archived-source-tree":
        if not HEX40.fullmatch(commit):
            _fail(f"{repository} archived source commit must be a 40-hex SHA")
        if "archived source tree" not in relation:
            _fail(f"{repository} relation must describe an archived source tree")
    elif archive_status == "stack-owned-provisional-research":
        if commit != "hmmm":
            _fail(f"{repository} provisional stack-owned research must use commit hmmm")
    else:
        _fail(f"{repository} has unknown archive_status {archive_status!r}")

    path = ROOT / path_text
    if path_text.startswith("/") or ".." in Path(path_text).parts:
        _fail(f"{repository} path must be repository-relative")
    if not path.exists():
        _fail(f"{repository} path does not exist: {path_text}")
    if (path / ".git").exists():
        _fail(f"{repository} path must not contain nested VCS metadata: {path_text}")


def _validate_boundaries(boundaries: Any) -> None:
    if not isinstance(boundaries, dict):
        _fail("boundaries must be an object")
    expected_false = (
        "authority_transfer",
        "proof_status_transfer",
        "measurement_status_transfer",
    )
    for key in expected_false:
        if boundaries.get(key) is not False:
            _fail(f"boundaries.{key} must be false")
    if boundaries.get("archive_provenance_required") is not True:
        _fail("boundaries.archive_provenance_required must be true")
    if boundaries.get("promotion_requires_public_gonol") is not True:
        _fail("boundaries.promotion_requires_public_gonol must be true")
    if boundaries.get("public_gonol_timing") != "after-research-closure":
        _fail("boundaries.public_gonol_timing must be after-research-closure")
    if boundaries.get("semantic_mapping") != "stack-research-with-archive-provenance":
        _fail("boundaries.semantic_mapping has unexpected value")
    hmmm = boundaries.get("hmmm")
    if not isinstance(hmmm, list) or not all(isinstance(item, str) and item for item in hmmm):
        _fail("boundaries.hmmm must be a non-empty text list")


def main() -> int:
    manifest = _load_manifest()
    if manifest.get("schema") != SCHEMA:
        _fail(f"schema must be {SCHEMA}")
    if manifest.get("version") != VERSION:
        _fail(f"version must be {VERSION}")

    repositories = manifest.get("repositories")
    if not isinstance(repositories, list) or not repositories:
        _fail("repositories must be a non-empty list")
    seen: set[str] = set()
    for entry in repositories:
        _validate_repository(entry, seen)

    _validate_boundaries(manifest.get("boundaries"))

    computed = _canonical_digest(manifest)
    declared = manifest.get("work_graph_sha256")
    if declared != computed:
        _fail(f"work_graph_sha256 mismatch: declared {declared!r}, computed {computed}")

    human = HUMAN_MANIFEST_PATH.read_text(encoding="utf-8")
    if computed not in human:
        _fail("STACK_MANIFEST.md does not contain the computed digest")

    print(f"stack manifest ok: {computed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
