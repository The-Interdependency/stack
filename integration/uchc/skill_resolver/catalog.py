# ratios: loc_comments=209:6 imports_exports=10:5 calls_definitions=109:15
"""Read the pinned skill-lib catalog and resolve its directed skill relations."""
from __future__ import annotations

import argparse
from collections import defaultdict
from collections.abc import Callable, Iterable
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import subprocess


class CatalogError(ValueError):
    """A source, relation or selection cannot be resolved exactly."""


_RELATIONS = ("depends_on", "load_with")
_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
_REPO = "The-Interdependency/skill-lib"
_FIELDS = {"name", "path", "kind", "description", "status", "runner", "runner_scope",
           "native_ingestion", "provenance", *_RELATIONS}


def _name(value: object) -> str:
    if not isinstance(value, str) or not _NAME.fullmatch(value):
        raise CatalogError(f"invalid skill name: {value!r}")
    return value


def _unique_keys(items: list[tuple]) -> dict:
    result = {}
    for key, value in items:
        if key in result:
            raise CatalogError(f"duplicate index field: {key}")
        result[key] = value
    return result


def _pinned_blobs(root: Path, commit: str) -> dict[str, str]:
    if not isinstance(commit, str) or not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", commit):
        raise CatalogError("expected an exact lowercase Git commit ID")
    try:
        kind = subprocess.check_output(["git", "-C", root, "cat-file", "-t", commit],
                                       stderr=subprocess.PIPE)
        if kind.strip() != b"commit":
            raise CatalogError("source identity is not a commit")
        listing = subprocess.check_output(["git", "-C", root, "ls-tree", "-rz", commit],
                                          stderr=subprocess.PIPE)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise CatalogError("cannot inspect pinned skill-lib commit") from exc
    blobs = {}
    for entry in listing.split(b"\0"):
        if entry:
            metadata, path = entry.split(b"\t", 1)
            mode, kind, oid = metadata.split()
            if kind == b"blob" and mode in (b"100644", b"100755"):
                blobs[path.decode("utf-8", "surrogateescape")] = oid.decode("ascii")
    return blobs


def _source_file(root: Path, path: str, blobs: dict[str, str]) -> bytes:
    oid = blobs.get(path)
    if oid is None:
        raise CatalogError(f"absent regular file in source commit: {path}")
    target = root / path
    if target.resolve() != target:
        raise CatalogError(f"source path traverses a symlink: {path}")
    try:
        data = target.read_bytes()
    except OSError as exc:
        raise CatalogError(f"cannot read source path: {path}") from exc
    digest = hashlib.sha1() if len(oid) == 40 else hashlib.sha256()
    digest.update(f"blob {len(data)}\0".encode("ascii"))
    digest.update(data)
    if digest.hexdigest() != oid:
        raise CatalogError(f"source file differs from pinned commit: {path}")
    return data


def _record(entry: dict, root: Path, blobs: dict[str, str]) -> dict:
    if not isinstance(entry, dict) or set(entry) - _FIELDS:
        raise CatalogError("unsupported skill declaration fields")
    name = _name(entry.get("name"))
    path = entry.get("path")
    if path != f"{name}/SKILL.md":
        raise CatalogError(f"noncanonical skill source path for {name}: {path!r}")
    if not isinstance(entry.get("description"), str) or not entry["description"].strip():
        raise CatalogError(f"missing discovery description: {name}")
    raw = _source_file(root, path, blobs)
    record = {"name": name, "path": path, "description": entry["description"],
              "sha256": hashlib.sha256(raw).hexdigest(), "relations": []}
    for field in ("status", "runner", "runner_scope"):
        if field in entry:
            if not isinstance(entry[field], str) or not entry[field].strip():
                raise CatalogError(f"malformed {field}: {name}")
            record[field] = entry[field]
    for kind in _RELATIONS:
        targets = entry.get(kind, [])
        if not isinstance(targets, list):
            raise CatalogError(f"{name}.{kind}: expected a list of skill names")
        seen = set()
        for item in targets:
            target = _name(item)
            if kind == "load_with" and target == name:
                raise CatalogError(f"self co-load: {name}")
            if target in seen:
                raise CatalogError(f"duplicate {kind}: {name} -> {target}")
            seen.add(target)
            record["relations"].append({"kind": kind, "target": target})
    return record


class Catalog:
    def __init__(self, root, commit, index_digest, blobs, records, retired):
        self._root = root
        self._blobs = blobs
        self._records = records
        self._retired = retired
        self._source = {"repo": _REPO, "commit": commit, "index_sha256": index_digest}

    @property
    def source(self) -> dict:
        return dict(self._source)

    @property
    def records(self) -> dict[str, dict]:
        return deepcopy(self._records)

    def get(self, name: str) -> dict:
        _name(name)
        if name in self._retired:
            raise CatalogError(f"retired skill: {name}")
        if name not in self._records:
            raise CatalogError(f"unknown skill: {name}")
        return deepcopy(self._records[name])

    def read_body(self, name: str) -> str:
        record = self.get(name)
        data = _source_file(self._root, record["path"], self._blobs)
        if hashlib.sha256(data).hexdigest() != record["sha256"]:
            raise CatalogError(f"skill digest mismatch: {name}")
        try:
            return data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise CatalogError(f"skill body is not UTF-8: {name}") from exc


def load_catalog(root: Path, *, source_commit: str) -> Catalog:
    root = Path(root).resolve()
    blobs = _pinned_blobs(root, source_commit)
    index = _source_file(root, "skills.json", blobs)
    try:
        data = json.loads(index, object_pairs_hook=_unique_keys)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise CatalogError("invalid skills.json encoding or syntax") from exc
    if (not isinstance(data, dict) or type(data.get("version")) is not int
            or data["version"] != 1 or data.get("repo") != _REPO):
        raise CatalogError("unsupported skills.json source or schema")
    if not isinstance(data.get("skills"), list) or not isinstance(data.get("superseded_skills", []), list):
        raise CatalogError("malformed active or superseded skill list")
    retired = set()
    for prior in data.get("superseded_skills", []):
        if not isinstance(prior, dict):
            raise CatalogError("malformed superseded skill")
        name = _name(prior.get("name"))
        if name in retired:
            raise CatalogError(f"duplicate superseded skill: {name}")
        retired.add(name)
    records = {}
    for row in data["skills"]:
        record = _record(row, root, blobs)
        name = record["name"]
        if name in retired or name in records:
            raise CatalogError(f"ambiguous active skill: {name}")
        records[name] = record
    catalog = Catalog(root, source_commit, hashlib.sha256(index).hexdigest(), blobs, records, retired)
    if records:
        resolve(catalog, sorted(records))
    return catalog


def verify_checkout(root: Path, expected: dict) -> None:
    """Check the independently selected Git HEAD and catalog bytes against the lock."""
    head = subprocess.check_output(
        ["git", "-C", root, "rev-parse", "--verify", "HEAD^{commit}"], text=True
    ).strip()
    if head != expected.get("commit"):
        raise CatalogError("checked-out skill-lib HEAD differs from the pilot lock")
    if load_catalog(root, source_commit=head).source != expected:
        raise CatalogError("checked-out catalog repository or index differs from the pilot lock")


def resolve(catalog: Catalog, roots: Iterable[str], *, get_record: Callable[[str], dict] | None = None) -> dict:
    """Return a deterministic plan, including every direct reason each skill is present."""
    if isinstance(roots, (str, bytes)):
        raise CatalogError("expected a collection of skill names")
    roots = sorted({_name(name) for name in roots})
    if not roots:
        raise CatalogError("expected at least one root skill")
    frontier = list(roots)
    reasons = defaultdict(list)
    for name in roots:
        reasons[name].append({"kind": "requested", "source": name})
    active = {}
    while frontier:
        name = frontier.pop()
        if name in active:
            continue
        source_record = catalog.get(name)
        record = source_record if get_record is None else get_record(name)
        if record != source_record:
            raise CatalogError(f"replayed record differs from pinned source: {name}")
        active[name] = record["relations"]
        for edge in record["relations"]:
            target = edge["target"]
            reasons[target].append({"kind": edge["kind"], "source": name})
            frontier.append(target)

    remaining = set(active)
    order = []
    while remaining:
        ready = sorted(name for name in remaining if not any(
            edge["kind"] == "depends_on" and edge["target"] in remaining
            for edge in active[name]))
        if not ready:
            raise CatalogError(f"prerequisite cycle among: {', '.join(sorted(remaining))}")
        # Prefer an available co-load target first. Mutual co-load is satisfiable
        # in one plan if its members have no circular hard prerequisites.
        name = next((name for name in ready if not any(
            edge["target"] in remaining for edge in active[name])), ready[0])
        remaining.remove(name)
        order.append(name)
    return {"roots": roots, "order": order, "reasons": {
        name: sorted(reasons[name], key=lambda reason: (reason["source"], reason["kind"]))
        for name in order}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=verify_checkout.__doc__)
    parser.add_argument("checkout", type=Path, help="path to the skill-lib checkout")
    args = parser.parse_args()
    lock = json.loads(Path(__file__).with_name("source.json").read_bytes())
    verify_checkout(args.checkout, lock["catalog"])
# ratios: loc_comments=209:6 imports_exports=10:5 calls_definitions=109:15
