#!/usr/bin/env python3
"""Validate root stack MSDMD pointers without rewriting archived metadata."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "stack-manifest.json"
STACK_MSDMD_PATH = ROOT / "stack_msdmd.ts"
CALL_MARKER = "defineMsdmdCollection("
IMPORT_RE = re.compile(
    r'import\s+\{\s*defineMsdmdCollection\s*\}\s+from\s+"([^"]+)";'
)


def fail(message: str) -> None:
    raise SystemExit(f"stack msdmd check failed: {message}")


def _repo_slug(repository: str) -> str:
    try:
        _owner, slug = repository.split("/", 1)
    except ValueError:
        fail(f"repository must be owner/name: {repository}")
    return slug


def _safe_relative(path_text: str, *, context: str) -> Path:
    path = Path(path_text)
    if path.is_absolute() or ".." in path.parts:
        fail(f"{context} must be repository-relative")
    return path


def _resolve_import(collection_path: Path, import_path: str) -> Path:
    if not import_path.startswith("."):
        fail(f"{collection_path.relative_to(ROOT)} import must be relative: {import_path}")
    target = collection_path.parent / import_path
    if target.suffix == "":
        target = target.with_suffix(".ts")
    target = target.resolve()
    if not target.is_relative_to(ROOT):
        fail(f"{collection_path.relative_to(ROOT)} import escapes repository: {import_path}")
    if not target.exists():
        fail(
            f"{collection_path.relative_to(ROOT)} import target missing: "
            f"{target.relative_to(ROOT)}"
        )
    return target


def _validate_import_target(collection_path: Path) -> None:
    text = collection_path.read_text(encoding="utf-8")
    match = IMPORT_RE.search(text)
    if not match:
        fail(f"{collection_path.relative_to(ROOT)} has no defineMsdmdCollection import")
    _resolve_import(collection_path, match.group(1))


def _extract_payload(text: str) -> str:
    start = text.find(CALL_MARKER)
    if start < 0:
        fail(f"{STACK_MSDMD_PATH.name} has no defineMsdmdCollection call")
    index = start + len(CALL_MARKER)
    depth = 1
    quote = ""
    while index < len(text):
        char = text[index]
        if quote:
            if char == "\\":
                index += 2
                continue
            if char == quote:
                quote = ""
        elif char in "\"'":
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start + len(CALL_MARKER) : index]
        index += 1
    fail(f"{STACK_MSDMD_PATH.name} has an unterminated defineMsdmdCollection call")


def _load_stack_msdmd() -> dict[str, Any]:
    text = STACK_MSDMD_PATH.read_text(encoding="utf-8")
    _validate_import_target(STACK_MSDMD_PATH)
    try:
        collection = json.loads(_extract_payload(text))
    except json.JSONDecodeError as error:
        fail(f"{STACK_MSDMD_PATH.name} payload is not strict JSON: {error}")
    if not isinstance(collection, dict):
        fail(f"{STACK_MSDMD_PATH.name} payload must be an object")
    return collection


def _load_manifest() -> dict[str, Any]:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        fail(f"{MANIFEST_PATH.name} is not valid JSON: {error}")
    if not isinstance(manifest, dict):
        fail("manifest root must be an object")
    return manifest


def _expected_collection_point(entry: dict[str, Any]) -> Path:
    repository = entry.get("repository")
    path_text = entry.get("path")
    if not isinstance(repository, str) or not isinstance(path_text, str):
        fail("archived repository entries must have repository and path")
    path = _safe_relative(path_text, context=f"{repository}.path")
    return path / f"{_repo_slug(repository)}_msdmd.ts"


def _declarations_by_file(collection: dict[str, Any]) -> dict[str, dict[str, Any]]:
    declarations = collection.get("declarations")
    if not isinstance(declarations, list):
        fail("stack_msdmd.ts declarations must be a list")
    by_file: dict[str, dict[str, Any]] = {}
    for declaration in declarations:
        if not isinstance(declaration, dict):
            fail("each stack_msdmd declaration must be an object")
        file_text = declaration.get("file")
        if not isinstance(file_text, str) or not file_text:
            fail("each stack_msdmd declaration must have file")
        file_path = _safe_relative(file_text, context=f"{STACK_MSDMD_PATH.name} file")
        full_path = ROOT / file_path
        if not full_path.exists():
            fail(f"stack_msdmd declaration points at missing file: {file_text}")
        if file_text in by_file:
            fail(f"duplicate stack_msdmd declaration for file: {file_text}")
        by_file[file_text] = declaration
        _validate_import_target(full_path)
    return by_file


def _gaps_by_file(collection: dict[str, Any]) -> dict[str, dict[str, Any]]:
    gaps = collection.get("gaps")
    if not isinstance(gaps, list):
        fail("stack_msdmd.ts gaps must be a list")
    by_file: dict[str, dict[str, Any]] = {}
    for gap in gaps:
        if not isinstance(gap, dict):
            fail("each stack_msdmd gap must be an object")
        file_text = gap.get("file")
        if not isinstance(file_text, str) or not file_text:
            fail("each stack_msdmd gap must have file")
        _safe_relative(file_text, context=f"{STACK_MSDMD_PATH.name} gap file")
        if file_text in by_file:
            fail(f"duplicate stack_msdmd gap for file: {file_text}")
        missing = gap.get("missing")
        if not isinstance(missing, list) or not all(isinstance(item, str) for item in missing):
            fail(f"stack_msdmd gap for {file_text} must have text missing list")
        reason = gap.get("reason")
        if not isinstance(reason, str) or not reason:
            fail(f"stack_msdmd gap for {file_text} must explain the gap")
        by_file[file_text] = gap
    return by_file


def _require_field(fields: dict[str, Any], key: str, expected: str, context: str) -> None:
    if fields.get(key) != expected:
        fail(f"{context} field {key!r} must be {expected!r}, got {fields.get(key)!r}")


def _validate_archived_pointer(
    entry: dict[str, Any],
    declaration: dict[str, Any],
    collection_point: str,
) -> None:
    repository = entry["repository"]
    if declaration.get("block") != "MODULE_BUILD":
        fail(f"{collection_point} stack_msdmd declaration must use MODULE_BUILD")
    fields = declaration.get("fields")
    if not isinstance(fields, dict):
        fail(f"{collection_point} stack_msdmd declaration must have fields")
    _require_field(fields, "repository", repository, collection_point)
    _require_field(fields, "stack_path", entry["path"], collection_point)
    _require_field(fields, "collection_point", collection_point, collection_point)
    _require_field(fields, "archive_status", "archived-source-tree", collection_point)
    _require_field(fields, "source_commit", entry["commit"], collection_point)
    _require_field(fields, "source_tree_git_sha1", entry["source_tree_git_sha1"], collection_point)
    _require_field(fields, "tree_sha256", entry["tree_sha256"], collection_point)


def main() -> int:
    manifest = _load_manifest()
    collection = _load_stack_msdmd()
    if collection.get("repo") != "The-Interdependency/stack":
        fail("stack_msdmd.ts repo must be The-Interdependency/stack")
    declarations = _declarations_by_file(collection)
    gaps = _gaps_by_file(collection)
    if gaps:
        fail(f"stack_msdmd.ts carries unresolved gaps: {', '.join(sorted(gaps))}")

    repositories = manifest.get("repositories")
    if not isinstance(repositories, list):
        fail("stack-manifest repositories must be a list")
    for entry in repositories:
        if not isinstance(entry, dict):
            fail("each stack-manifest repository entry must be an object")
        if entry.get("archive_status") != "archived-source-tree":
            continue
        collection_point = _expected_collection_point(entry).as_posix()
        collection_path = ROOT / collection_point
        if collection_path.exists():
            declaration = declarations.get(collection_point)
            if declaration is None:
                fail(f"stack_msdmd.ts missing pointer for {collection_point}")
            _validate_archived_pointer(entry, declaration, collection_point)
            continue
        fail(f"archived repository is missing collection point: {collection_point}")

    print(f"stack msdmd ok: {STACK_MSDMD_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
