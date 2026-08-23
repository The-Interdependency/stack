#!/usr/bin/env python3
"""Validate root stack provenance without touching participant research semantics."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "stack-manifest.json"
HUMAN_MANIFEST_PATH = ROOT / "STACK_MANIFEST.md"
SCHEMA = "the-interdependency.stack-manifest"
VERSION = "1.0.0"
HEX40 = re.compile(r"^[0-9a-f]{40}$")
GENERATED_DIRS = {"__pycache__", ".pytest_cache", "build", "dist"}
GENERATED_SUFFIXES = (".pyc", ".pyo", ".egg-info")


def fail(message: str) -> None:
    raise SystemExit(f"stack manifest check failed: {message}")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def load_manifest() -> dict[str, Any]:
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        fail(f"{MANIFEST_PATH.name} is not valid JSON: {error}")
    if not isinstance(manifest, dict):
        fail("manifest root must be an object")
    return manifest


def canonical_digest(manifest: dict[str, Any]) -> str:
    payload = {
        "repositories": manifest.get("repositories"),
        "boundaries": manifest.get("boundaries"),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def require_text(mapping: dict[str, Any], key: str, context: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        fail(f"{context}.{key} must be non-empty text")
    return value


def tracked_tree_digest(path_text: str, *, exclude_paths: set[str] | None = None) -> str:
    exclude_paths = exclude_paths or set()
    entries = subprocess.check_output(
        ["git", "ls-tree", "-r", "-z", "HEAD", path_text],
        cwd=ROOT,
    )
    digest = hashlib.sha256()
    for raw in entries.split(b"\0"):
        if not raw:
            continue
        metadata, file_path_b = raw.split(b"\t", 1)
        mode, object_type, _object_id = metadata.decode("utf-8").split()
        if object_type != "blob":
            fail(f"unexpected git object type under {path_text}: {object_type}")
        file_path = file_path_b.decode("utf-8")
        if file_path in exclude_paths:
            continue
        prefix = f"{path_text}/"
        relative = file_path[len(prefix) :] if file_path.startswith(prefix) else file_path
        data = subprocess.check_output(["git", "show", f"HEAD:{file_path}"], cwd=ROOT)
        digest.update(mode.encode("utf-8"))
        digest.update(b"\0")
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(data).hexdigest().encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generated_artifacts(path: Path) -> list[str]:
    found: list[str] = []
    for item in path.rglob("*"):
        rel = item.relative_to(ROOT).as_posix()
        if item.is_dir() and (item.name in GENERATED_DIRS or item.name.endswith(".egg-info")):
            found.append(rel)
        elif item.is_file() and item.name.endswith(GENERATED_SUFFIXES):
            found.append(rel)
    return found


def validate_overlay_paths(entry: dict[str, Any], path_text: str, repository: str) -> set[str]:
    overlays = entry.get("stack_overlay_paths", [])
    if not isinstance(overlays, list):
        fail(f"{repository}.stack_overlay_paths must be a list when present")

    overlay_paths: set[str] = set()
    prefix = f"{path_text}/"
    for index, overlay in enumerate(overlays):
        context = f"{repository}.stack_overlay_paths[{index}]"
        if not isinstance(overlay, dict):
            fail(f"{context} must be an object")
        overlay_path_text = require_text(overlay, "path", context)
        overlay_path = Path(overlay_path_text)
        if overlay_path.is_absolute() or ".." in overlay_path.parts:
            fail(f"{context}.path must be repository-relative")
        if not overlay_path_text.startswith(prefix):
            fail(f"{context}.path must live under {path_text}")
        if overlay_path_text in overlay_paths:
            fail(f"{context}.path is duplicated: {overlay_path_text}")

        full_path = ROOT / overlay_path
        if not full_path.is_file():
            fail(f"{context}.path does not name a file: {overlay_path_text}")
        declared_sha256 = require_text(overlay, "sha256", context)
        if file_sha256(full_path) != declared_sha256:
            fail(f"{context}.sha256 mismatch for {overlay_path_text}")
        require_text(overlay, "purpose", context)
        overlay_paths.add(overlay_path_text)
    return overlay_paths


def validate_archived_entry(entry: dict[str, Any], seen: set[str]) -> None:
    repository = require_text(entry, "repository", "repository")
    if repository in seen:
        fail(f"duplicate repository entry: {repository}")
    seen.add(repository)
    if not repository.startswith("The-Interdependency/"):
        fail(f"repository is outside The-Interdependency: {repository}")

    commit = require_text(entry, "commit", repository)
    archive_status = entry.get("archive_status")
    if archive_status is None:
        if commit != "hmmm":
            fail(f"{repository} without archive_status must use commit hmmm")
        return

    if archive_status != "archived-source-tree":
        fail(f"{repository} has unknown archive_status {archive_status!r}")
    if not HEX40.fullmatch(commit):
        fail(f"{repository} commit must be a 40-hex SHA")

    path_text = require_text(entry, "path", repository)
    path = Path(path_text)
    if path.is_absolute() or ".." in path.parts:
        fail(f"{repository} path must be repository-relative")
    full_path = ROOT / path
    if not full_path.exists():
        fail(f"{repository} path does not exist: {path_text}")
    if (full_path / ".git").exists():
        fail(f"{repository} path contains nested VCS metadata: {path_text}")

    overlay_paths = validate_overlay_paths(entry, path_text, repository)

    declared_tree = require_text(entry, "source_tree_git_sha1", repository)
    if not HEX40.fullmatch(declared_tree):
        fail(f"{repository} source_tree_git_sha1 must be a 40-hex SHA")
    if not overlay_paths:
        actual_tree = git("rev-parse", f"HEAD:{path_text}")
        if actual_tree != declared_tree:
            fail(f"{repository} tree object mismatch: {actual_tree} != {declared_tree}")

    declared_digest = require_text(entry, "tree_sha256", repository)
    actual_digest = tracked_tree_digest(path_text, exclude_paths=overlay_paths)
    if actual_digest != declared_digest:
        fail(f"{repository} tree_sha256 mismatch: {actual_digest} != {declared_digest}")

    artifacts = generated_artifacts(full_path)
    if artifacts:
        fail(f"{repository} contains generated artifacts: {', '.join(artifacts[:10])}")


def validate_boundaries(boundaries: Any) -> None:
    if not isinstance(boundaries, dict):
        fail("boundaries must be an object")
    for key in ("authority_transfer", "proof_status_transfer", "measurement_status_transfer"):
        if boundaries.get(key) is not False:
            fail(f"boundaries.{key} must be false")
    if boundaries.get("archive_provenance_required") is not True:
        fail("boundaries.archive_provenance_required must be true")
    if boundaries.get("public_gonol_timing") != "after-research-closure":
        fail("boundaries.public_gonol_timing must be after-research-closure")
    hmmm = boundaries.get("hmmm")
    if not isinstance(hmmm, list) or not all(isinstance(item, str) and item for item in hmmm):
        fail("boundaries.hmmm must be a non-empty text list")


def main() -> int:
    manifest = load_manifest()
    if manifest.get("schema") != SCHEMA:
        fail(f"schema must be {SCHEMA}")
    if manifest.get("version") != VERSION:
        fail(f"version must be {VERSION}")

    repositories = manifest.get("repositories")
    if not isinstance(repositories, list) or not repositories:
        fail("repositories must be a non-empty list")
    seen: set[str] = set()
    for entry in repositories:
        if not isinstance(entry, dict):
            fail("every repository entry must be an object")
        validate_archived_entry(entry, seen)

    validate_boundaries(manifest.get("boundaries"))

    computed = canonical_digest(manifest)
    if manifest.get("work_graph_sha256") != computed:
        fail(
            "work_graph_sha256 mismatch: "
            f"declared {manifest.get('work_graph_sha256')!r}, computed {computed}"
        )
    if computed not in HUMAN_MANIFEST_PATH.read_text(encoding="utf-8"):
        fail("STACK_MANIFEST.md does not contain the computed work graph digest")

    print(f"stack manifest ok: {computed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
