# ratios: loc_comments=94:28 imports_exports=10:4 calls_definitions=63:4
# === MODULE_BUILD ===
# id: ucns_distribution_evidence
#   module_name: _distribution_evidence
#   module_kind: instrument
#   summary: binds complete archived inputs and installed distribution files to replay evidence
#   owner: Erin Spencer
#   public_surface: snapshot and verify-snapshot CLI; installed_inventory
#   internal_surface: source_snapshot
#   auth_boundary: none
#   storage_boundary: write
#   storage_notes: caller-selected snapshot receipt
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_distribution_replay.py
#   rollout: distribution replay gate
#   rollback: retain earlier evidence as historical only
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: ucns_distribution_evidence_binds_all_files
#   given: a source archive and a clean installed distribution
#   then: persistent source changes and missing, altered, or unexpected installed files fail replay
#   class: evidence
# === END CONTRACTS ===
"""Usage: python tools/_distribution_evidence.py snapshot|verify-snapshot SOURCE JSON.

Snapshots exclude bytecode caches only. Installed RECORD and installer-generated
metadata are retained and validated separately from immutable wheel payloads.
"""
from __future__ import annotations

import base64
import csv
import hashlib
from importlib import metadata
import io
import json
from pathlib import Path
import sys
import zipfile


def source_snapshot(root: Path) -> dict[str, str]:
    entries = tuple(root.rglob("*"))
    if root.is_symlink() or any(path.is_symlink() for path in entries):
        raise ValueError("source snapshot contains a symlink")
    return {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in entries if path.is_file() and "__pycache__" not in path.relative_to(root).parts}


def verify_snapshot(root: Path, expected: dict[str, str]) -> None:
    if source_snapshot(root) != expected:
        raise ValueError("archived source changed during distribution replay")


def installed_inventory(wheel: Path, artifact: Path) -> dict:
    distribution = metadata.distribution("ucns")
    base = Path(distribution.locate_file("")).resolve()
    if not base.is_relative_to(Path(sys.prefix).resolve()):
        raise ValueError("installed distribution escaped verification environment")
    with zipfile.ZipFile(wheel) as archive:
        expected = {name: archive.read(name) for name in archive.namelist() if not name.endswith("/")}
    records = [name for name in expected if name.endswith(".dist-info/RECORD")]
    if len(records) != 1:
        raise ValueError("wheel RECORD identity is ambiguous")
    record = records[0]
    info = record.rsplit("/", 1)[0]
    generated = {info + "/" + name for name in ("RECORD", "INSTALLER", "REQUESTED", "direct_url.json", "uv_cache.json", "uv_build.json")}
    paths = {str(path): Path(distribution.locate_file(path)) for path in distribution.files or ()}
    for name, path in paths.items():
        if Path(name).is_absolute() or ".." in Path(name).parts or path.is_symlink() or not path.resolve().is_relative_to(base):
            raise ValueError("unsafe installed path: " + name)
    actual = {name: path.read_bytes() for name, path in paths.items() if "__pycache__" not in Path(name).parts}
    if set(actual) - set(expected) - generated or set(expected) - set(actual):
        raise ValueError("unexpected or missing installed distribution file")
    for directory in (base / "ucns", base / info):
        entries = tuple(directory.rglob("*"))
        if directory.is_symlink() or any(path.is_symlink() for path in entries):
            raise ValueError("installed distribution contains a symlink")
        observed = {path.relative_to(base).as_posix() for path in entries if path.is_file() and "__pycache__" not in path.relative_to(base).parts}
        declared = {name for name in actual if Path(name).is_relative_to(directory.relative_to(base))}
        if observed != declared:
            raise ValueError("installed distribution has unrecorded files")
    for name, payload in expected.items():
        if name != record and actual[name] != payload:
            raise ValueError("installed wheel payload differs: " + name)
    if actual.get(info + "/INSTALLER") != b"uv" or actual.get(info + "/REQUESTED", b"") != b"":
        raise ValueError("unexpected installer metadata")
    direct = json.loads(actual[info + "/direct_url.json"])
    expected_uri = artifact.resolve().as_uri() + "#sha256=" + hashlib.sha256(artifact.read_bytes()).hexdigest()
    if direct != {"url": expected_uri, "archive_info": {}}:
        raise ValueError("installed artifact origin differs")
    build_metadata = actual.get(info + "/uv_build.json")
    if artifact.name.endswith(".tar.gz"):
        if build_metadata is None or json.loads(build_metadata) != {}:
            raise ValueError("unexpected uv build metadata")
    elif build_metadata is not None:
        raise ValueError("wheel install contains source-build metadata")
    cache = json.loads(actual[info + "/uv_cache.json"])
    if set(cache) != {"timestamp", "commit", "tags", "env", "directories"} or cache["commit"] is not None or cache["tags"] is not None or cache["env"] != {} or cache["directories"] != {}:
        raise ValueError("unexpected uv cache metadata")
    timestamp = cache["timestamp"]
    if set(timestamp) != {"secs_since_epoch", "nanos_since_epoch"} or not all(type(value) is int and value >= 0 for value in timestamp.values()) or timestamp["nanos_since_epoch"] >= 1000000000:
        raise ValueError("invalid uv cache timestamp")
    rows = list(csv.reader(io.StringIO(actual[record].decode())))
    if any(len(row) != 3 for row in rows) or len({row[0] for row in rows}) != len(rows):
        raise ValueError("invalid installed RECORD")
    if {row[0] for row in rows} != set(paths):
        raise ValueError("installed RECORD coverage differs")
    for name, digest, size in rows:
        if name == record or "__pycache__" in Path(name).parts:
            if digest or size:
                raise ValueError("unexpected generated RECORD hash")
            continue
        wanted = "sha256=" + base64.urlsafe_b64encode(hashlib.sha256(actual[name]).digest()).rstrip(b"=").decode()
        if digest != wanted or size != str(len(actual[name])):
            raise ValueError("installed RECORD digest differs: " + name)
    return {"files_sha256": {name: hashlib.sha256(payload).hexdigest() for name, payload in sorted(actual.items())},
            "installer_metadata": {name: actual[name].decode() for name in sorted(generated & actual.keys())}}


def main() -> None:
    action, source, receipt = sys.argv[1:]
    root, output = Path(source), Path(receipt)
    if action == "snapshot":
        output.write_text(json.dumps(source_snapshot(root), indent=2, sort_keys=True) + "\n")
    elif action == "verify-snapshot":
        verify_snapshot(root, json.loads(output.read_text()))
    else:
        raise ValueError("unknown snapshot action")


if __name__ == "__main__":
    main()
# ratios: loc_comments=94:28 imports_exports=10:4 calls_definitions=63:4
