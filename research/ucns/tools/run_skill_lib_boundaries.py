# === MODULE_BUILD ===
# id: skill_lib_boundary_runner
#   module_name: run_skill_lib_boundaries
#   module_kind: instrument
#   summary: audits and executes declared skill-lib CHECKS as isolated pytest boundaries with capability, timeout, and receipt enforcement
#   owner: Erin Spencer
#   public_surface: command-line boundary runner, run_boundaries, write_receipt
#   internal_surface: capability resolution, subprocess classification, receipt hashing
#   auth_boundary: none
#   storage_boundary: optional caller-selected JSON receipt path
#   network_boundary: none
#   user_data_boundary: captured test output is bounded and retained only in the caller-selected receipt
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
#   then: the runner records PASS, FAIL, ERROR, or TIMEOUT respectively and continues with remaining selected checks
#   class: evidence
#   since: 2026-08-15
#
# id: boundary_runner_receipt_is_bounded_and_bound
#   given: a boundary run completes
#   then: its receipt binds declarations, commands, capabilities, outcomes, output digests, declared mutation and cleanup, bounded output excerpts, and an identity digest
#   class: evidence
#   since: 2026-08-15
#
# id: boundary_runner_has_no_activation_effect
#   given: every selected check passes
#   then: the receipt closes only the declared executable evidence boundary and cannot select UCNS options, activate EDCM, or confer canon status
#   class: doctrine
#   since: 2026-08-15
# === END CONTRACTS ===

"""Execute UCNS skill-lib ``CHECKS`` declarations as bounded processes."""

from __future__ import annotations

import argparse
import ctypes.util
from dataclasses import asdict, dataclass
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
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
SCHEMA_VERSION = "1.0.0"
MAX_EXCERPT_BYTES = 16_384
ALLOWED_MUTATIONS = {"none", "filesystem", "temporary_path"}
ALLOWED_CLEANUPS = {"none", "tempdir_teardown", "pytest temporary_path"}


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


def _sha(data: bytes) -> str:
    return sha256(data).hexdigest()


def _split(value: str) -> tuple[str, ...]:
    return tuple(item.strip() for item in value.split(",") if item.strip())


def _capability_available(name: str) -> bool:
    if name == "python3":
        return True
    if name == "posix_shell":
        return os.name == "posix" and shutil.which("sh") is not None
    if name == "posix_resource":
        return os.name == "posix" and importlib.util.find_spec("resource") is not None
    if name == "sched_affinity":
        return hasattr(os, "sched_getaffinity") and hasattr(os, "sched_setaffinity")
    if name in {"libmpfr", "system-libmpfr"}:
        return ctypes.util.find_library("mpfr") is not None
    if name in {"mpmath", "numpy", "sympy", "pytest"}:
        return importlib.util.find_spec(name) is not None
    return shutil.which(name) is not None


def _declared_checks(root: Path) -> tuple[Entry, ...]:
    checks: list[Entry] = []
    for path in sorted((root / "tests").rglob("test_*.py")):
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
    data = path.read_bytes()
    excerpt = data[:MAX_EXCERPT_BYTES]
    text = excerpt.decode("utf-8", errors="replace")
    if len(data) > len(excerpt):
        text += f"\n[truncated {len(data) - len(excerpt)} bytes]"
    return _sha(data), len(data), text


def _run_check(root: Path, check: Entry) -> CheckOutcome:
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
        with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
            process = subprocess.Popen(
                command, cwd=root, stdin=subprocess.DEVNULL,
                stdout=stdout, stderr=stderr, start_new_session=True,
            )
            timed_out = False
            try:
                returncode = process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                returncode = process.wait()
        stdout_sha, stdout_bytes, stdout_excerpt = _excerpt(stdout_path)
        stderr_sha, stderr_bytes, stderr_excerpt = _excerpt(stderr_path)

    duration = round(time.monotonic() - started, 6)
    if timed_out:
        status = "TIMEOUT"
    elif returncode == 0:
        status = "PASS"
    elif returncode == 1 and "AssertionError" in (stdout_excerpt + stderr_excerpt):
        status = "FAIL"
    else:
        status = "ERROR"
    return CheckOutcome(
        check.id, relative_source, _split(check.fields["proves"]), call,
        command, requires, timeout, mutates, cleanup, status, returncode,
        duration, stdout_sha, stderr_sha, stdout_bytes, stderr_bytes,
        stdout_excerpt, stderr_excerpt,
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
    audit_ok, gaps = audit_repository(root)
    if not audit_ok:
        receipt: dict[str, object] = {
            "schema_id": SCHEMA_ID, "schema_version": SCHEMA_VERSION,
            "status": "audit-gap", "audit_closed": False,
            "audit_gaps": gaps, "outcomes": [], "selection_effect": "none",
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
    outcomes = tuple(_run_check(root, check) for check in selected)
    statuses = {outcome.status for outcome in outcomes}
    receipt: dict[str, object] = {
        "schema_id": SCHEMA_ID, "schema_version": SCHEMA_VERSION,
        "status": "passed" if statuses <= {"PASS"} else "not-passed",
        "audit_closed": True, "audit_gaps": [],
        "selected_check_ids": [outcome.check_id for outcome in outcomes],
        "outcome_counts": {
            key: sum(outcome.status == key for outcome in outcomes)
            for key in ("PASS", "FAIL", "ERROR", "TIMEOUT")
        },
        "outcomes": [asdict(outcome) for outcome in outcomes],
        "selection_effect": "none", "edcm_activation": "inactive",
        "canon_status": "none",
        "boundary_effect": "declared executable evidence only",
    }
    receipt["receipt_sha256"] = _receipt_identity(receipt)
    return receipt


def write_receipt(receipt: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--check", action="append", default=[], dest="checks")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args(argv)
    receipt = run_boundaries(Path(args.root), selected_ids=args.checks)
    if args.receipt:
        write_receipt(receipt, args.receipt)
    print(json.dumps(receipt, indent=2, sort_keys=True, ensure_ascii=False))
    return 0 if receipt["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
