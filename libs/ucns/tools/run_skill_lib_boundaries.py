# ratios: loc_comments=422:71 imports_exports=20:4 calls_definitions=187:20
# === MODULE_BUILD ===
# id: skill_lib_boundary_runner
#   module_name: run_skill_lib_boundaries
#   module_kind: instrument
#   summary: audits and executes declared skill-lib CHECKS as isolated pytest boundaries with capability, timeout, and receipt enforcement
#   owner: Erin Spencer
#   public_surface: command-line boundary runner, run_boundaries, write_receipt
#   internal_surface: capability resolution, subprocess classification, receipt hashing
#   auth_boundary: none
#   storage_boundary: write
#   storage_notes: optional caller-selected JSON receipt path
#   network_boundary: none
#   user_data_boundary: write
#   user_data_notes: captured test output is bounded and retained only in the caller-selected receipt
#   admin_only: false
#   tests: tests/test_skill_lib_boundary_runner.py
#   rollout: explicit local and CI evidence runner; no product, EDCM, or canon activation
#   rollback: remove this tool, its tests, and documentation
#   requires: skill_lib_contract_audit
#   since: 2026-08-15
#   unresolved: mutation verification and non-pytest CHECKS call schemes
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: boundary_runner_audits_before_execution
#   given: declared skill-lib checks are requested for execution
#   then: the no-exec contract graph audit must close before any check process starts
#   class: safety
#   since: 2026-08-15
#
# id: boundary_runner_consumes_capabilities_and_timeouts
#   given: a CHECKS declaration names requires and timeout fields
#   then: execution refuses missing capabilities and applies the positive timeout to the spawned pytest process group
#   class: safety
#   since: 2026-08-15
#
# id: boundary_runner_classifies_and_continues
#   given: one declared check passes, fails an assertion, raises unexpectedly, or times out
#   then: the runner records PASS, FAIL, ERROR, TIMEOUT, or SKIP from machine-readable outcomes and continues after per-check harness errors; absent or skipped evidence never passes
#   class: evidence
#   since: 2026-08-15
#
# id: boundary_runner_receipt_is_bounded_and_bound
#   given: a boundary run completes
#   then: its receipt binds source/declaration digests before and after execution, commands, capabilities, outcomes, declared mutation and cleanup, and bounded output; source mutation prevents acceptance
#   class: evidence
#   since: 2026-08-15
#
# id: boundary_runner_has_no_activation_effect
#   given: every selected check passes
#   then: the receipt closes only the declared executable evidence boundary and cannot select UCNS options, activate EDCM, or confer canon status
#   class: doctrine
#   since: 2026-08-15
# === END CONTRACTS ===

"""Execute UCNS skill-lib ``CHECKS`` declarations as bounded processes.

Usage: ``python tools/run_skill_lib_boundaries.py . --check CHECK_ID
--receipt /tmp/receipt.json``. Schema v2.1 requires observed pytest outcomes,
bound import origins, unchanged source snapshots, and no Linux inotify write
events. JUnit remains diagnostic only. Receipts are not theorem or freshness
certificates. Timeouts retain the existing declared execution-safety boundary.
"""

from __future__ import annotations

import argparse
import ctypes
import ctypes.util
from dataclasses import asdict, dataclass, field, replace
from hashlib import sha256
import importlib.util
import json
import os
import re
from pathlib import Path
import shutil
import signal
import struct
import subprocess
import sys
import tempfile
import time
from typing import Iterable, Sequence

TOOLS_DIRECTORY = Path(__file__).resolve().parent
if str(TOOLS_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIRECTORY))

from verify_skill_lib_contracts import Entry, audit_repository, parse_blocks


SCHEMA_ID = "ucns.skill-lib-boundary-run-receipt"
SCHEMA_VERSION = "2.1.0"
MAX_EXCERPT_BYTES = 16_384
ALLOWED_MUTATIONS = {"none", "filesystem", "temporary_path"}
ALLOWED_CLEANUPS = {"none", "tempdir_teardown", "pytest temporary_path"}
SOURCE_DIRECTORIES = ("src", "tools", "tests", "docs", "generated", ".agents/skills", ".github/workflows")
ROOT_INPUTS = ("pyproject.toml", "uv.lock", "pytest.ini", "setup.cfg", "MANIFEST.in", "conftest.py", "CANON.md", "AGENTS.md", "README.md", "CLAUDE.md", "LICENSE")
BOOTSTRAP = TOOLS_DIRECTORY / "_boundary_pytest.py"
SUPERVISOR = TOOLS_DIRECTORY / "_boundary_supervisor.py"
STARTUP_DIRECTORY = TOOLS_DIRECTORY / "_boundary_site"


class _SourceWatch:
    """Observe Linux source write events, including a write followed by restoration.

    Receipt execution requires inotify; an unavailable observer fails closed.
    This detects changed inputs, not malicious checks or a security sandbox.
    """
    def __init__(self, root: Path):
        self.root = root
        self.libc = ctypes.CDLL(None, use_errno=True)
        self.fd = self.libc.inotify_init1(os.O_NONBLOCK | os.O_CLOEXEC)
        if self.fd < 0:
            raise OSError(ctypes.get_errno(), "source observer unavailable")
        self.watches = {}
        try:
            directories = {root}
            for relative in SOURCE_DIRECTORIES:
                base = root / relative
                if base.exists():
                    directories.add(base)
                    directories.update(p for p in base.rglob("*") if p.is_dir() and "__pycache__" not in p.parts)
                parent = base.parent
                while parent != root and parent.is_relative_to(root):
                    if parent.is_dir():
                        directories.add(parent)
                    parent = parent.parent
            # MODIFY, ATTRIB, MOVED_FROM/TO, CREATE, DELETE, DELETE_SELF, MOVE_SELF.
            # File watches follow the inode, including writes via external hardlinks.
            files, _ = _source_snapshot(root)
            watched = directories | {root / name for name in files}
            for directory in sorted(watched):
                descriptor = self.libc.inotify_add_watch(self.fd, os.fsencode(directory), 0xFC6)
                if descriptor < 0:
                    raise OSError(ctypes.get_errno(), "cannot watch source directory")
                self.watches[descriptor] = directory
        except BaseException:
            os.close(self.fd)
            raise

    def finish(self) -> tuple[str, ...]:
        changed = set()
        try:
            while True:
                try:
                    data = os.read(self.fd, 65536)
                except BlockingIOError:
                    break
                if not data:
                    break
                offset = 0
                while offset < len(data):
                    descriptor, mask, _, length = struct.unpack_from("iIII", data, offset)
                    name = os.fsdecode(data[offset + 16:offset + 16 + length].split(b"\0", 1)[0])
                    offset += 16 + length
                    if mask & 0x4000:
                        changed.add("hmmm: source event queue overflow")
                        continue
                    parent = self.watches.get(descriptor)
                    if parent is None:
                        changed.add("hmmm: unknown source watch")
                        continue
                    relative = (parent / name).relative_to(self.root).as_posix()
                    if "__pycache__" in Path(relative).parts:
                        continue
                    if relative in ROOT_INPUTS or any(relative == d or relative.startswith(d + "/") or d.startswith(relative + "/") for d in SOURCE_DIRECTORIES):
                        changed.add(relative)
        finally:
            os.close(self.fd)
        return tuple(sorted(changed))


@dataclass(frozen=True)
class CheckOutcome:
    check_id: str
    source: str
    contract_ids: tuple[str, ...]
    call: str
    command: tuple[str, ...]
    requires: tuple[str, ...]
    timeout_seconds: int
    mutates: str
    cleanup: str
    status: str
    returncode: int | None
    duration_seconds: float
    stdout_sha256: str
    stderr_sha256: str
    stdout_bytes: int
    stderr_bytes: int
    stdout_excerpt: str
    stderr_excerpt: str
    missing_capabilities: tuple[str, ...] = ()
    diagnostic: str = ""
    descendants_reaped: int = 0
    imported_sources: dict[str, list[str]] = field(default_factory=dict)
    source_events: tuple[str, ...] = ()
    source_before_sha256: str = ""
    source_after_sha256: str = ""


def _sha(data: bytes) -> str:
    return sha256(data).hexdigest()


def _split(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


def _capability_available(name: str) -> bool:
    if name == "python3":
        return True
    if name == "node24":
        executable = shutil.which("node")
        if executable is None:
            return False
        try:
            result = subprocess.run([sys.executable, str(SUPERVISOR), "--probe", "5", executable, "--version"], capture_output=True, text=True)
        except (OSError, UnicodeError, subprocess.TimeoutExpired):
            return False
        return result.returncode == 0 and re.fullmatch(r"v24\.\d+\.\d+", result.stdout.strip()) is not None
    if name == "posix_shell":
        return os.name == "posix" and shutil.which("sh") is not None
    if name == "posix_resource":
        return os.name == "posix" and importlib.util.find_spec("resource") is not None
    if name == "sched_affinity":
        return hasattr(os, "sched_getaffinity") and hasattr(os, "sched_setaffinity")
    if name in {"libmpfr", "system-libmpfr"}:
        return ctypes.util.find_library("mpfr") is not None
    if name in {"mpmath", "numpy", "sympy", "pytest", "build"}:
        return importlib.util.find_spec(name) is not None
    return shutil.which(name) is not None


def _declared_checks(root: Path) -> tuple[Entry, ...]:
    checks: list[Entry] = []
    for path in sorted((root / "tests").rglob("*.py")):
        if "__pycache__" not in path.parts and (path.name.startswith("test_") or path.name.endswith("_test.py")):
            checks.extend(entry for entry in parse_blocks(path) if entry.block == "CHECKS")
    return tuple(checks)


def _validate_check(check: Entry) -> tuple[tuple[str, ...], int, str, str]:
    requires = _split(check.fields.get("requires", ""))
    raw_timeout = check.fields.get("timeout", "")
    if not raw_timeout:
        raise ValueError(f"{check.id}: executable CHECKS entry requires timeout")
    try:
        timeout = int(raw_timeout)
    except ValueError as exc:
        raise ValueError(f"{check.id}: timeout must be an integer") from exc
    if timeout <= 0:
        raise ValueError(f"{check.id}: timeout must be positive")
    mutates = check.fields.get("mutates", "")
    cleanup = check.fields.get("cleanup", "")
    if mutates not in ALLOWED_MUTATIONS:
        raise ValueError(f"{check.id}: unsupported mutates declaration: {mutates!r}")
    if cleanup not in ALLOWED_CLEANUPS:
        raise ValueError(f"{check.id}: unsupported cleanup declaration: {cleanup!r}")
    return requires, timeout, mutates, cleanup


def _excerpt(path: Path) -> tuple[str, int, str]:
    digest = sha256()
    size = 0
    excerpt = b""
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65_536), b""):
            digest.update(chunk)
            size += len(chunk)
            excerpt += chunk[:max(0, MAX_EXCERPT_BYTES - len(excerpt))]
    text = excerpt.decode("utf-8", errors="replace")
    if size > len(excerpt):
        text += f"\n[truncated {size - len(excerpt)} bytes]"
    return digest.hexdigest(), size, text


def _pytest_outcome(path: Path, returncode: int) -> tuple[str, dict]:
    """Validate the bootstrap's machine report; absent evidence is an error."""
    try:
        observed = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "ERROR", {}
    if not isinstance(observed, dict):
        return "ERROR", {}
    calls, other = observed.get("calls"), observed.get("other")
    origins = observed.get("origins")
    allowed = {"PASS", "FAIL", "ERROR", "SKIP"}
    if not isinstance(calls, list) or not isinstance(other, list) or not isinstance(origins, dict):
        return "ERROR", {}
    if any(not isinstance(value, str) or value not in allowed for value in calls + other):
        return "ERROR", {}
    statuses = calls + other
    if observed.get("wrong_origins") or "ERROR" in statuses:
        status = "ERROR"
    elif "FAIL" in statuses:
        status = "FAIL"
    elif "SKIP" in statuses:
        status = "SKIP"
    else:
        status = "PASS" if calls and returncode == 0 and observed.get("item_coverage_closed") is True else "ERROR"
    if observed.get("status") != status:
        return "ERROR", {}
    return status, observed


def _source_snapshot(root: Path) -> tuple[dict[str, str], str]:
    """Bind declared execution inputs, excluding bytecode caches."""
    entries = {root / name for name in ROOT_INPUTS}
    for directory in SOURCE_DIRECTORIES:
        base = root / directory
        parent = base
        while parent != root:
            if parent.is_symlink():
                raise ValueError("unsupported source symlink: " + parent.relative_to(root).as_posix())
            entries.add(parent)
            parent = parent.parent
        entries.update(base.rglob("*"))
    links = sorted(path.relative_to(root).as_posix() for path in entries if path.is_symlink())
    if links:
        raise ValueError("unsupported source symlink: " + ", ".join(links))
    paths = {path for path in entries if path.is_file() and "__pycache__" not in path.parts}
    inventory = {path.relative_to(root).as_posix(): _sha(path.read_bytes()) for path in sorted(paths)}
    return inventory, _sha(json.dumps(inventory, sort_keys=True, separators=(",", ":")).encode())


def _error_outcome(root: Path, check: Entry, error: Exception) -> CheckOutcome:
    empty = _sha(b"")
    return CheckOutcome(
        check.id, check.source.relative_to(root).as_posix(),
        _split(check.fields.get("proves", "")), check.fields.get("call", ""), (),
        _split(check.fields.get("requires", "")), 0,
        check.fields.get("mutates", ""), check.fields.get("cleanup", ""),
        "ERROR", None, 0.0, empty, empty, 0, 0, "", "",
        diagnostic=f"{type(error).__name__}: {error}",
    )


def _run_check(root: Path, check: Entry) -> CheckOutcome:
    started = time.monotonic()
    watcher = _SourceWatch(root)
    try:
        outcome = _execute_check(root, check)
    finally:
        source_events = watcher.finish()
    return replace(outcome, source_events=source_events, duration_seconds=round(time.monotonic() - started, 6))


def _execute_check(root: Path, check: Entry) -> CheckOutcome:
    requires, timeout, mutates, cleanup = _validate_check(check)
    missing = tuple(name for name in requires if not _capability_available(name))
    call = check.fields["call"]
    function = call.removeprefix("self::")
    relative_source = check.source.relative_to(root).as_posix()
    command = (sys.executable, "-m", "pytest", "-q", f"{relative_source}::{function}")
    if missing:
        empty_digest = _sha(b"")
        return CheckOutcome(
            check.id, relative_source, _split(check.fields["proves"]), call,
            command, requires, timeout, mutates, cleanup, "ERROR", None, 0.0,
            empty_digest, empty_digest, 0, 0, "",
            f"missing required capabilities: {', '.join(missing)}", missing,
        )

    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="ucns-boundary-") as temporary:
        stdout_path = Path(temporary) / "stdout"
        stderr_path = Path(temporary) / "stderr"
        junit_path = Path(temporary) / "outcomes.xml"
        report_path = Path(temporary) / "outcomes.json"
        command = (sys.executable, str(BOOTSTRAP), str(root), str(report_path),
                   "-q", "-p", "no:cacheprovider", "-c", str(root / "pyproject.toml"), "--noconftest", f"{relative_source}::{function}", f"--junitxml={junit_path}", "-o", "xfail_strict=true")
        command = (sys.executable, str(SUPERVISOR), str(timeout), *command[1:])
        environment = dict(os.environ)
        for name in ("PYTHONPATH", "PYTHONHOME", "PYTEST_ADDOPTS", "PYTEST_PLUGINS"):
            environment.pop(name, None)
        environment.update(PYTHONDONTWRITEBYTECODE="1", PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
        environment["PYTHONPYCACHEPREFIX"] = str(Path(temporary) / "bytecode")
        environment["UCNS_BOUND_SOURCE_ROOT"] = str(root)
        environment["PYTHONPATH"] = os.pathsep.join((str(STARTUP_DIRECTORY), str(root / "src"), str(root)))
        with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
            process = subprocess.Popen(
                command, cwd=root, stdin=subprocess.DEVNULL,
                stdout=stdout, stderr=stderr, start_new_session=True, env=environment,
            )
            # The separate supervisor owns the timeout and descendant reaping;
            # pytest signal handlers never run in that process.
            returncode = process.wait()
        stdout_sha, stdout_bytes, stdout_excerpt = _excerpt(stdout_path)
        stderr_sha, stderr_bytes, stderr_excerpt = _excerpt(stderr_path)
        status, observed = _pytest_outcome(report_path, returncode)
        if observed.get("timed_out"):
            status = "TIMEOUT"

    duration = round(time.monotonic() - started, 6)
    return CheckOutcome(
        check.id, relative_source, _split(check.fields["proves"]), call,
        command, requires, timeout, mutates, cleanup, status, returncode,
        duration, stdout_sha, stderr_sha, stdout_bytes, stderr_bytes,
        stdout_excerpt, stderr_excerpt,
        diagnostic=("background descendants outlived the check" if observed.get("descendants_reaped") else
                    "collected pytest items did not all execute" if status == "ERROR" and observed.get("item_coverage_closed") is False else ""),
        descendants_reaped=observed.get("descendants_reaped", 0),
        imported_sources=observed.get("origins", {}),
    )


def _receipt_identity(receipt: dict[str, object]) -> str:
    payload = dict(receipt)
    payload.pop("receipt_sha256", None)
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return _sha(encoded)


def run_boundaries(
    root: Path, *, selected_ids: Iterable[str] = (),
) -> dict[str, object]:
    root = root.resolve()
    try:
        source_files, source_before = _source_snapshot(root)
    except (ValueError, OSError) as error:
        source_files, source_before = {}, ""
        audit_ok, gaps = False, [f"GAP source snapshot {type(error).__name__}: {error}"]
    else:
        audit_ok, gaps = audit_repository(root)
    if not audit_ok:
        receipt: dict[str, object] = {
            "schema_id": SCHEMA_ID, "schema_version": SCHEMA_VERSION,
            "status": "audit-gap", "audit_closed": False,
            "audit_gaps": gaps, "outcomes": [], "selection_effect": "none",
            "bound_source_root": str(root),
            "edcm_activation": "inactive", "canon_status": "none",
        }
        receipt["receipt_sha256"] = _receipt_identity(receipt)
        return receipt

    checks = _declared_checks(root)
    requested = tuple(selected_ids)
    known = {check.id for check in checks}
    unknown = tuple(item for item in requested if item not in known)
    if unknown:
        raise ValueError(f"unknown check ids: {', '.join(unknown)}")
    selected = checks if not requested else tuple(
        check for check in checks if check.id in requested
    )
    outcomes = []
    snapshot_errors = []
    for check in selected:
        check_before = check_after = ""
        try:
            _, check_before = _source_snapshot(root)
        except (ValueError, OSError) as error:
            snapshot_errors.append({"check_id": check.id, "phase": "before", "error": str(error)})
            outcomes.append(_error_outcome(root, check, error))
            continue
        try:
            outcome = _run_check(root, check)
        except (ValueError, OSError, AttributeError) as error:
            outcome = _error_outcome(root, check, error)
        try:
            _, check_after = _source_snapshot(root)
        except (ValueError, OSError) as error:
            snapshot_errors.append({"check_id": check.id, "phase": "after", "error": str(error)})
            outcome = replace(outcome, status="ERROR", diagnostic=f"source snapshot {type(error).__name__}: {error}")
        outcomes.append(replace(outcome, source_before_sha256=check_before, source_after_sha256=check_after))
    try:
        _, source_after = _source_snapshot(root)
    except (ValueError, OSError) as error:
        source_after = ""
        snapshot_errors.append({"phase": "final", "error": str(error)})
    statuses = {outcome.status for outcome in outcomes}
    unchanged = not snapshot_errors and source_before == source_after and all(
        not outcome.source_events and outcome.source_before_sha256 == outcome.source_after_sha256
        for outcome in outcomes
    )
    receipt: dict[str, object] = {
        "schema_id": SCHEMA_ID, "schema_version": SCHEMA_VERSION,
        "bound_source_root": str(root),
        "status": "passed" if outcomes and statuses == {"PASS"} and unchanged else "not-passed",
        "audit_closed": True, "audit_gaps": [],
        "source_files_sha256": source_files,
        "source_before_sha256": source_before,
        "source_after_sha256": source_after,
        "source_unchanged": unchanged,
        "snapshot_errors": snapshot_errors,
        "bootstrap_sha256": _sha(BOOTSTRAP.read_bytes()),
        "supervisor_sha256": _sha(SUPERVISOR.read_bytes()),
        "startup_hook_sha256": _sha((STARTUP_DIRECTORY / "sitecustomize.py").read_bytes()),
        "python_version": sys.version,
        "selected_check_ids": [outcome.check_id for outcome in outcomes],
        "outcome_counts": {
            key: sum(outcome.status == key for outcome in outcomes)
            for key in ("PASS", "FAIL", "ERROR", "TIMEOUT", "SKIP")
        },
        "outcomes": [asdict(outcome) for outcome in outcomes],
        "selection_effect": "none", "edcm_activation": "inactive",
        "canon_status": "none",
        "boundary_effect": "declared executable evidence only",
    }
    receipt["receipt_sha256"] = _receipt_identity(receipt)
    return receipt


def _receipt_inside_source(path: Path, root: Path) -> bool:
    lexical = Path(os.path.abspath(path))
    destination = path.parent.resolve() / path.name
    bound = root.resolve()
    return any(candidate.is_relative_to(bound) for candidate in (lexical, destination, path.resolve()))


def write_receipt(receipt: dict[str, object], path: Path) -> None:
    bound_root = receipt.get("bound_source_root")
    if not isinstance(bound_root, str) or not bound_root:
        raise ValueError("receipt must identify its bound source tree")
    if _receipt_inside_source(path, Path(bound_root)):
        raise ValueError("receipt output must be outside the bound source tree")
    path.parent.mkdir(parents=True, exist_ok=True)
    # Replacing the directory entry avoids writing through an external hardlink.
    with tempfile.TemporaryDirectory(prefix=".ucns-receipt-", dir=path.parent) as temporary:
        output = Path(temporary) / "receipt.json"
        output.write_text(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
        os.replace(output, path)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--check", action="append", default=[], dest="checks")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args(argv)
    if args.receipt and _receipt_inside_source(args.receipt, Path(args.root)):
        parser.error("receipt output must be outside the bound source tree")
    receipt = run_boundaries(Path(args.root), selected_ids=args.checks)
    if args.receipt:
        write_receipt(receipt, args.receipt)
    print(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if receipt["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
# ratios: loc_comments=422:71 imports_exports=20:4 calls_definitions=187:20
