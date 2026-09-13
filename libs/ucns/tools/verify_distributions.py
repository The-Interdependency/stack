# ratios: loc_comments=336:35 imports_exports=17:4 calls_definitions=178:11
# === MODULE_BUILD ===
# id: ucns_distribution_audit
#   module_name: verify_distributions
#   module_kind: instrument
#   summary: checks built UCNS source and wheel archive bytes against repository-owned replay inputs
#   owner: Erin Spencer
#   public_surface: verify_distributions, command-line audit
#   internal_surface: expected_files, read_archive
#   auth_boundary: none
#   storage_boundary: read
#   storage_notes: read-only repository and archives
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_distributions.py
#   rollout: CI artifact gate after build
#   rollback: remove tool, test, and CI invocation together
#   since: 2026-09-11
#   unresolved: semantic validity of archived certificates and independent wheel runtime replay
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: distributions_retain_exact_replay_inputs
#   given: a built sdist and wheel are compared to a UCNS source tree
#   then: missing or altered required inputs, unsafe archive members, duplicate members, unexpected executable payloads/metadata, and altered license material fail without extraction or execution
#   class: evidence
#   since: 2026-09-11
# === END CONTRACTS ===

"""Usage: ``python tools/verify_distributions.py . dist`` after a clean build.

The wheel contains the package plus a narrowly admitted generated ``.dist-info``
set; the sdist also contains the tests, their evidence, preregistrations, tools,
vendored parser, and exact license bytes. Matching archive bytes is packaging
evidence only, not certificate verification or ratification.
"""

from __future__ import annotations

import argparse
import base64
from collections import Counter
import csv
from email.parser import BytesParser
import hashlib
import io
from pathlib import Path, PurePosixPath
import tarfile
import zipfile

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name, parse_wheel_filename, parse_sdist_filename
from packaging.tags import Tag
from packaging.version import Version

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10; declared in the build extra.
    import tomli as tomllib


ROOT_INPUTS = (
    "pyproject.toml", "README.md", "AGENTS.md", "CANON.md", "CLAUDE.md",
    "LICENSE", "uv.lock", "MANIFEST.in",
)
TREE_INPUTS = (
    "src/ucns", "tests", "tools", "docs", "generated", ".agents/skills", ".github/workflows",
)

SDIST_GENERATED = {
    "setup.cfg",
    "PKG-INFO",
    "src/ucns.egg-info/PKG-INFO",
    "src/ucns.egg-info/SOURCES.txt",
    "src/ucns.egg-info/dependency_links.txt",
    "src/ucns.egg-info/requires.txt",
    "src/ucns.egg-info/top_level.txt",
}
GENERATED_SETUP_CFG = b"[egg_info]\ntag_build = \ntag_date = 0\n\n"
WHEEL_DIST_INFO_FILES = {"METADATA", "WHEEL", "RECORD", "top_level.txt"}
WHEEL_LICENSE_PATH = "licenses/LICENSE"


def expected_files(root: Path) -> dict[str, bytes]:
    paths = {root / name for name in ROOT_INPUTS}
    if any(path.is_symlink() for path in paths):
        raise ValueError("unsupported source symlink in root distribution inputs")
    for directory in TREE_INPUTS:
        base = root / directory
        parent = base
        while parent != root:
            if parent.is_symlink():
                raise ValueError(f"unsupported source symlink: {parent}")
            parent = parent.parent
        for path in base.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"unsupported source symlink: {path}")
            if path.is_file() and "__pycache__" not in path.parts:
                paths.add(path)
    missing_roots = [path.name for path in paths if path.parent == root and not path.is_file()]
    if missing_roots:
        raise ValueError(f"missing root distribution inputs: {', '.join(sorted(missing_roots))}")
    if not any(path.is_relative_to(root / "src/ucns") for path in paths):
        raise ValueError("missing UCNS package source")
    return {path.relative_to(root).as_posix(): path.read_bytes() for path in sorted(paths)}


def read_archive(path: Path, *, wheel: bool, expected_prefix: str | None = None, directories: set[str] | None = None) -> dict[str, bytes]:
    """Read regular files only; reject ambiguous names rather than extracting."""
    files: dict[str, bytes] = {}
    prefixes: set[str] = set()
    kinds: dict[str, bool] = {}

    def record(name: str, data: bytes | None) -> None:
        parts = PurePosixPath(name).parts
        directory = data is None
        if not parts or name.startswith("/") or ".." in parts or "\\" in name or "\0" in name:
            raise ValueError(f"unsafe archive name: {name}")
        if not wheel:
            if expected_prefix is not None and parts[0] != expected_prefix:
                raise ValueError("sdist root identity differs from project/filename")
            prefixes.add(parts[0])
            if (len(parts) < 2 and not directory) or len(prefixes) != 1:
                raise ValueError("sdist must have one enclosing directory")
            parts = parts[1:]
        name = "/".join(parts)
        if name in kinds:
            raise ValueError(f"duplicate archive member: {name}")
        if any(kinds.get("/".join(parts[:index])) is False for index in range(1, len(parts))):
            raise ValueError(f"file/directory archive collision: {name}")
        if not directory and any(existing.startswith(name + "/") for existing in kinds):
            raise ValueError(f"file/directory archive collision: {name}")
        kinds[name] = directory
        if directory and directories is not None:
            directories.add(name)
        if not directory:
            files[name] = data

    if wheel:
        with zipfile.ZipFile(path) as archive:
            for member in archive.infolist():
                if (member.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError(f"archive symlink: {member.filename}")
                if member.is_dir() and member.file_size:
                    raise ValueError(f"nonempty archive directory: {member.filename}")
                record(member.filename, None if member.is_dir() else archive.read(member))
    else:
        with tarfile.open(path, "r:gz") as archive:
            for member in archive:
                required_mode = 0o700 if member.isdir() else 0o600
                if member.mode & required_mode != required_mode or member.mode & 0o7000:
                    raise ValueError(f"unusable sdist permissions: {member.name}: {oct(member.mode)}")
                if member.isdir():
                    if member.size:
                        raise ValueError(f"nonempty archive directory: {member.name}")
                    record(member.name, None)
                    continue
                if not member.isfile():
                    raise ValueError(f"non-regular archive member: {member.name}")
                stream = archive.extractfile(member)
                if stream is None:
                    raise ValueError(f"unreadable archive member: {member.name}")
                with stream:
                    record(member.name, stream.read())
    return files


def _requirement_key(value: str) -> tuple[str, ...]:
    requirement = Requirement(value)
    return (canonicalize_name(requirement.name), ",".join(sorted(requirement.extras)),
            str(requirement.specifier), requirement.url or "", str(requirement.marker or ""))


def _project_requirements(project: dict) -> list[str]:
    requirements = list(project.get("dependencies", []))
    for extra, dependencies in project.get("optional-dependencies", {}).items():
        for value in dependencies:
            requirement = Requirement(value)
            marker = f'({requirement.marker}) and extra == "{extra}"' if requirement.marker else f'extra == "{extra}"'
            requirement.marker = None
            requirements.append(f"{requirement}; {marker}")
    return requirements


def _metadata_content_problems(data: bytes, expected: dict[str, bytes]) -> list[str]:
    """Bind installer-facing metadata to this project's static configuration."""
    project = tomllib.loads(expected["pyproject.toml"].decode("utf-8"))["project"]
    metadata = BytesParser().parsebytes(data)
    wanted = {
        "Metadata-Version": ["2.4"], "Name": [project["name"]],
        "Version": [project["version"]], "Summary": [project["description"]],
        "Requires-Python": [project["requires-python"]],
        "Author": [", ".join(author["name"] for author in project["authors"])],
        "Classifier": project.get("classifiers", []),
        "Description-Content-Type": ["text/markdown"], "License-File": ["LICENSE"],
        "Dynamic": ["license-file"],
        "Provides-Extra": list(project.get("optional-dependencies", {})),
    }
    problems = []
    if metadata.defects:
        problems.append("malformed wheel METADATA")
    allowed = {key.lower() for key in wanted} | {"license", "requires-dist"}
    for name in metadata.keys():
        if name.lower() not in allowed:
            problems.append(f"unexpected wheel METADATA field {name}")
    for name, values in wanted.items():
        if Counter(metadata.get_all(name, [])) != Counter(values):
            problems.append(f"wheel METADATA {name} differs from project configuration")
    licenses = metadata.get_all("License", [])
    if len(licenses) != 1 or " ".join(licenses[0].split()) != " ".join(expected["LICENSE"].decode().split()):
        problems.append("wheel METADATA License differs from source license")
    if metadata.get_payload(decode=True).rstrip() != expected[project["readme"]].rstrip():
        problems.append("wheel METADATA description differs from source README")
    requirements = _project_requirements(project)
    try:
        if Counter(map(_requirement_key, metadata.get_all("Requires-Dist", []))) != Counter(map(_requirement_key, requirements)):
            problems.append("wheel METADATA Requires-Dist differs from project configuration")
    except ValueError as error:
        problems.append(f"invalid wheel METADATA Requires-Dist: {error}")
    return problems


def _sdist_metadata_problems(actual: dict[str, bytes], expected: dict[str, bytes]) -> list[str]:
    problems = []
    for name in ("PKG-INFO", "src/ucns.egg-info/PKG-INFO"):
        if name not in actual:
            problems.append(f"missing sdist metadata {name}")
        else:
            problems.extend(problem.replace("wheel METADATA", f"sdist {name}")
                            for problem in _metadata_content_problems(actual[name], expected))
    for name, value in (("top_level.txt", b"ucns\n"), ("dependency_links.txt", b"\n")):
        if actual.get("src/ucns.egg-info/" + name) != value:
            problems.append(f"altered or missing sdist {name}")
    sources = actual.get("src/ucns.egg-info/SOURCES.txt", b"").decode("utf-8").splitlines()
    if Counter(sources) != Counter(actual.keys() - {"PKG-INFO", "setup.cfg"}):
        problems.append("sdist SOURCES.txt differs from archive members")
    project = tomllib.loads(expected["pyproject.toml"].decode("utf-8"))["project"]
    requirements = []
    marker = ""
    try:
        for line in actual.get("src/ucns.egg-info/requires.txt", b"").decode("utf-8").splitlines():
            if not line.strip():
                continue
            if line.startswith("[") and line.endswith("]"):
                extra, _, condition = line[1:-1].partition(":")
                marker = condition
                if extra:
                    marker = f'({marker}) and extra == "{extra}"' if marker else f'extra == "{extra}"'
            else:
                requirements.append(_requirement_key(line + ("; " + marker if marker else "")))
        if Counter(requirements) != Counter(map(_requirement_key, _project_requirements(project))):
            problems.append("sdist requires.txt differs from project dependencies")
    except (ValueError, UnicodeError):
        problems.append("invalid sdist requires.txt")
    return problems


def _record_problems(actual: dict[str, bytes], record_path: str) -> list[str]:
    problems = []
    seen = set()
    try:
        for row in csv.reader(io.StringIO(actual[record_path].decode("utf-8")), strict=True):
            if len(row) != 3:
                problems.append("wheel RECORD row must have three fields")
                continue
            name, digest, size = row
            if name in seen or name not in actual:
                problems.append(f"wheel RECORD duplicate or unknown path {name}")
                continue
            seen.add(name)
            if name == record_path:
                if digest or size:
                    problems.append("wheel RECORD self-entry must omit hash and size")
            else:
                expected_digest = base64.urlsafe_b64encode(hashlib.sha256(actual[name]).digest()).rstrip(b"=").decode()
                if digest != "sha256=" + expected_digest or size != str(len(actual[name])):
                    problems.append(f"wheel RECORD digest or size mismatch {name}")
    except (UnicodeError, csv.Error) as error:
        problems.append(f"malformed wheel RECORD: {error}")
    for name in sorted(actual.keys() - seen):
        problems.append(f"wheel RECORD missing path {name}")
    return problems


def _wheel_metadata_problems(actual: dict[str, bytes], expected: dict[str, bytes], directories: set[str]) -> list[str]:
    problems: list[str] = []
    prefixes = {
        name.split("/", 1)[0]
        for name in actual.keys() | directories
        if name.split("/", 1)[0].endswith(".dist-info")
    }
    if len(prefixes) != 1:
        return ["wheel must contain exactly one .dist-info directory"]
    prefix = next(iter(prefixes))
    project = tomllib.loads(expected["pyproject.toml"].decode("utf-8"))["project"]
    expected_prefix = f"{project['name'].replace('-', '_')}-{project['version']}.dist-info"
    if prefix != expected_prefix:
        problems.append("wheel .dist-info identity differs from project configuration")
    allowed = {f"{prefix}/{name}" for name in WHEEL_DIST_INFO_FILES}
    allowed.add(f"{prefix}/{WHEEL_LICENSE_PATH}")
    for name in sorted(actual):
        if name.startswith(f"{prefix}/") and name not in allowed:
            problems.append(f"unexpected wheel metadata {name}")
    required = {f"{prefix}/{name}" for name in ("METADATA", "WHEEL", "RECORD")}
    required.add(f"{prefix}/{WHEEL_LICENSE_PATH}")
    for name in sorted(required - actual.keys()):
        problems.append(f"missing wheel metadata {name}")
    packaged_license = actual.get(f"{prefix}/{WHEEL_LICENSE_PATH}")
    if packaged_license is not None and packaged_license != expected["LICENSE"]:
        problems.append(f"altered wheel license {prefix}/{WHEEL_LICENSE_PATH}")
    if f"{prefix}/METADATA" in actual:
        problems.extend(_metadata_content_problems(actual[f"{prefix}/METADATA"], expected))
    if f"{prefix}/WHEEL" in actual:
        metadata = BytesParser().parsebytes(actual[f"{prefix}/WHEEL"])
        wanted = {"Wheel-Version": ["1.0"], "Root-Is-Purelib": ["true"], "Tag": ["py3-none-any"]}
        if metadata.defects or metadata.get_payload().strip():
            problems.append("malformed wheel WHEEL metadata")
        for name, values in wanted.items():
            if metadata.get_all(name, []) != values:
                problems.append(f"wheel WHEEL {name} differs from pure Python configuration")
        if len(metadata.get_all("Generator", [])) != 1 or not metadata["Generator"].strip():
            problems.append("wheel WHEEL must identify its generator")
        if any(name.lower() not in {"wheel-version", "root-is-purelib", "tag", "generator"} for name in metadata.keys()):
            problems.append("unexpected wheel WHEEL field")
    if f"{prefix}/RECORD" in actual:
        problems.extend(_record_problems(actual, f"{prefix}/RECORD"))
    if f"{prefix}/top_level.txt" in actual and actual[f"{prefix}/top_level.txt"] != b"ucns\n":
        problems.append("altered wheel top_level.txt")
    return problems


def verify_distributions(root: Path, sdist: Path, wheel: Path) -> list[str]:
    expected = expected_files(root.resolve())
    project = tomllib.loads(expected["pyproject.toml"].decode("utf-8"))["project"]
    wheel_expected = {
        name.removeprefix("src/"): data
        for name, data in expected.items()
        if name.startswith("src/ucns/")
    }
    problems: list[str] = []
    try:
        name, version, build, tags = parse_wheel_filename(wheel.name)
        if name != canonicalize_name(project["name"]) or version != Version(project["version"]) or build or tags != {Tag("py3", "none", "any")}:
            problems.append("wheel filename identity or tags differ from project/WHEEL metadata")
        name, version = parse_sdist_filename(sdist.name)
        if name != canonicalize_name(project["name"]) or version != Version(project["version"]):
            problems.append("sdist filename identity differs from project metadata")
    except ValueError as error:
        problems.append(f"invalid distribution filename: {error}")
    for path, inputs, is_wheel in ((sdist, expected, False), (wheel, wheel_expected, True)):
        try:
            directories: set[str] = set()
            actual = read_archive(path, wheel=is_wheel, expected_prefix=None if is_wheel else sdist.name.removesuffix(".tar.gz"), directories=directories)
        except (OSError, ValueError, tarfile.TarError, zipfile.BadZipFile) as error:
            problems.append(f"{path.name}: {error}")
            continue
        implied_directories = {parent.as_posix() for name in actual for parent in PurePosixPath(name).parents if parent.as_posix() != "."}
        if not is_wheel:
            implied_directories.add("")  # The single enclosing sdist root.
        for name in sorted(directories - implied_directories):
            problems.append(f"{path.name}: unexpected directory {name}")
        for name, data in inputs.items():
            if name not in actual:
                problems.append(f"{path.name}: missing {name}")
            elif actual[name] != data:
                problems.append(f"{path.name}: altered {name}")
        if is_wheel:
            metadata_problems = _wheel_metadata_problems(actual, expected, directories)
            problems.extend(f"{path.name}: {problem}" for problem in metadata_problems)
            dist_prefixes = {
                name.split("/", 1)[0]
                for name in actual
                if "/" in name and name.split("/", 1)[0].endswith(".dist-info")
            }
            metadata_prefix = next(iter(dist_prefixes), "")
            for name in sorted(actual.keys() - inputs.keys()):
                if not metadata_prefix or not name.startswith(f"{metadata_prefix}/"):
                    problems.append(f"{path.name}: unexpected payload {name}")
        else:
            problems.extend(f"{path.name}: {problem}" for problem in _sdist_metadata_problems(actual, expected))
            if "setup.cfg" not in actual:
                problems.append(f"{path.name}: missing generated setup.cfg")
            elif actual["setup.cfg"] != GENERATED_SETUP_CFG:
                problems.append(f"{path.name}: altered generated setup.cfg")
            for name in sorted(actual.keys() - inputs.keys()):
                if name not in SDIST_GENERATED:
                    problems.append(f"{path.name}: unexpected payload {name}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("dist", type=Path)
    args = parser.parse_args()
    sdists, wheels = sorted(args.dist.glob("*.tar.gz")), sorted(args.dist.glob("*.whl"))
    if len(sdists) != 1 or len(wheels) != 1:
        parser.error("expected exactly one sdist and one wheel; use a clean output directory")
    problems = verify_distributions(args.root, sdists[0], wheels[0])
    print("\n".join(problems) if problems else "distribution replay inputs: exact")
    return int(bool(problems))


if __name__ == "__main__":
    raise SystemExit(main())
# ratios: loc_comments=336:35 imports_exports=17:4 calls_definitions=178:11
