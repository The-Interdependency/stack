"""MSDMD derivation adapter for stack fresh-making."""
from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_msdmd_fresh_adapter
#   module_name: msdmd_fresh_adapter
#   module_kind: adapter
#   summary: applies fresh-making to repo-owned MSDMD collections with exact identities, independent rerender verification, atomic publication, and PostgreSQL acceptance
#   owner: stack
#   public_surface: build_spec, register_spec, evaluate, queue_make, run_job, make, retry_job
#   auth_boundary: write
#   storage_boundary: write
#   network_boundary: none
#   tests: backend.tests.test_orchestrator
#   rollout: frontend.cli.stackctl fresh and the VM worker
#   rollback: stop fresh-making; repository source authority is unchanged
# === END MODULE_BUILD ===

# === BOUNDARIES ===
# id: stack_msdmd_fresh_execution_boundary
#   summary: executes a pinned MSDMD generator only against an explicitly bounded repository checkout and publishes only independently reproduced output
#   auth_boundary: write
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: true
#   side_effects: filesystem, subprocess, database, job
#   owner: stack
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: stack_msdmd_fresh_exact_identity
#   given: source or generator identity moves after the desired freshness key is queued
#   then: the attempt fails closed and cannot publish under the obsolete key
#   class: provenance
#
# id: stack_msdmd_false_green_rejected
#   given: the executor exits successfully but an independent rerender differs
#   then: no target acceptance is recorded and the prior accepted artifact remains the freshness authority
#   class: verification
#
# id: stack_msdmd_publish_after_verify
#   given: executor candidate and independent verifier output match under unchanged exact identities
#   then: output is atomically published and PostgreSQL accepts one receipt for that target freshness key
#   class: evidence
# === END CONTRACTS ===

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any

from .freshness import (
    SPEC_SCHEMA, SPEC_VERSION, FreshnessReport, affected_closure, base_report,
    freshness_key, receipt_payload,
)
from .jobs import Job, JobLedger

_SHA40 = re.compile(r"^[0-9a-f]{40}$")


class ConstraintError(RuntimeError):
    """Operator-resolvable boundary preserved as hmmm."""


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_sha256(root: str | Path, *, suffixes: tuple[str, ...] = (".py",)) -> str:
    base = Path(root).resolve()
    if not base.is_dir():
        raise FileNotFoundError(base)
    digest = hashlib.sha256()
    files = sorted(path for path in base.rglob("*") if path.is_file() and (not suffixes or path.suffix in suffixes))
    if not files:
        raise ValueError(f"no generator files found under {base}")
    for path in files:
        digest.update(path.relative_to(base).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def resolve_git_head(root: str | Path) -> str | None:
    proc = subprocess.run(
        ["git", "-C", str(Path(root).resolve()), "rev-parse", "HEAD"],
        text=True, capture_output=True, check=False,
    )
    if proc.returncode != 0:
        return None
    value = proc.stdout.strip()
    return value if _SHA40.fullmatch(value) else None


def generator_identity(generator_root: str | Path) -> str:
    package = Path(generator_root).resolve() / "msdmd"
    if not (package / "collect.py").is_file():
        raise FileNotFoundError(f"MSDMD collector not found: {package / 'collect.py'}")
    return tree_sha256(package, suffixes=(".py",))


def _parse_allowed_repos(raw: str) -> set[str]:
    return {part.strip() for part in raw.split(",") if part.strip()}


def _validate_runtime_boundaries(*, repo: str, root: Path, generator_root: Path, out: Path) -> None:
    repo_root_raw = os.environ.get("STACK_REPO_ROOT", "").strip()
    if repo_root_raw:
        repo_root = Path(repo_root_raw).expanduser().resolve()
        allowed = _parse_allowed_repos(os.environ.get("STACK_ALLOWED_REPOS", ""))
        if not allowed:
            raise ConstraintError("STACK_ALLOWED_REPOS is required with STACK_REPO_ROOT")
        if repo not in allowed:
            raise ConstraintError(f"repository is not allowed by STACK_ALLOWED_REPOS: {repo}")
        if root.parent != repo_root or root.name != repo:
            raise ConstraintError(f"target must be the direct configured checkout {repo_root / repo}: {root}")
        if not (root / ".git").exists():
            raise ConstraintError(f"configured production target is not a git checkout: {root}")

    skill_root_raw = os.environ.get("STACK_SKILL_LIB_ROOT", "").strip()
    if skill_root_raw:
        expected = Path(skill_root_raw).expanduser().resolve()
        if generator_root != expected:
            raise ConstraintError(f"generator root differs from STACK_SKILL_LIB_ROOT: {generator_root} != {expected}")
    if out.parent != root:
        raise ConstraintError(f"MSDMD artifact must remain at repository root: {out}")


def _git_status(root: Path) -> list[str]:
    proc = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain=v1", "--untracked-files=all"],
        text=True, capture_output=True, check=False,
    )
    return proc.stdout.splitlines() if proc.returncode == 0 else []


def _dirty_path(line: str) -> str:
    path = line[3:]
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    return path.strip('"')


def _unrelated_dirty(root: Path, ignored_names: set[str]) -> list[str]:
    return [line for line in _git_status(root) if _dirty_path(line) not in ignored_names]


def _source_identity(source_sha: str) -> str:
    if not _SHA40.fullmatch(source_sha):
        raise ValueError("source SHA must be an exact 40-character lowercase commit identity")
    return f"git:{source_sha}"


def _source_sha(spec: dict[str, Any]) -> str:
    for item in spec["inputs"]:
        if item.get("name") == "repository":
            identity = str(item.get("identity", ""))
            if identity.startswith("git:") and _SHA40.fullmatch(identity[4:]):
                return identity[4:]
    raise ValueError("MSDMD spec has no exact repository git identity")


def build_spec(*, repo: str, root: str | Path, generator_root: str | Path,
               out: str | Path | None = None, source_sha: str | None = None) -> dict[str, Any]:
    root_path = Path(root).expanduser().resolve()
    if not root_path.is_dir():
        raise FileNotFoundError(root_path)
    generator_path = Path(generator_root).expanduser().resolve()
    resolved = source_sha or resolve_git_head(root_path)
    if not resolved:
        raise ValueError("exact source SHA is required when target root has no resolvable git HEAD")
    output = Path(out) if out is not None else Path(f"{repo}_msdmd.ts")
    if not output.is_absolute():
        output = root_path / output
    output = output.resolve()
    _validate_runtime_boundaries(repo=repo, root=root_path, generator_root=generator_path, out=output)
    gen = generator_identity(generator_path)
    source_mode = "git" if resolve_git_head(root_path) is not None else "explicit"
    return {
        "schema": SPEC_SCHEMA,
        "version": SPEC_VERSION,
        "target": f"msdmd:{repo}",
        "kind": "msdmd.collection",
        "inputs": [{"name": "repository", "identity": _source_identity(resolved)}],
        "generator": {
            "identity": f"sha256:{gen}",
            "command": "python -m msdmd.collect --root <root> --repo <repo> --out <candidate> --source-commit <sha>",
        },
        "outputs": [{"path": output.name}],
        "verifier": {
            "identity": f"sha256:{gen}",
            "command": "independent-rerender-byte-compare@1",
        },
        "depends_on": [],
        "runtime": {
            "repo": repo, "root": str(root_path), "out": str(output),
            "generator_root": str(generator_path), "source_identity_mode": source_mode,
        },
    }


def refresh_identities(spec: dict[str, Any]) -> dict[str, Any]:
    if spec.get("kind") != "msdmd.collection":
        raise ValueError(f"unsupported derivation kind: {spec.get('kind')}")
    current = json.loads(json.dumps(spec))
    runtime = current["runtime"]
    root = Path(runtime["root"])
    if runtime.get("source_identity_mode") == "git":
        head = resolve_git_head(root)
        current["inputs"][0]["identity"] = _source_identity(head) if head else "hmmm"
    try:
        gen = generator_identity(runtime["generator_root"])
    except (FileNotFoundError, ValueError):
        current["generator"]["identity"] = "hmmm"
        current["verifier"]["identity"] = "hmmm"
    else:
        identity = f"sha256:{gen}"
        current["generator"]["identity"] = identity
        current["verifier"]["identity"] = identity
    return current


def register_spec(ledger: JobLedger, spec: dict[str, Any]) -> dict[str, Any]:
    key = freshness_key(spec)
    ledger.upsert_derivation(spec, key)
    return spec


def _collector_command(spec: dict[str, Any], output: Path) -> list[str]:
    runtime = spec["runtime"]
    return [
        sys.executable, "-m", "msdmd.collect",
        "--root", runtime["root"], "--repo", runtime["repo"],
        "--out", str(output), "--source-commit", _source_sha(spec),
    ]


def _run_collector(spec: dict[str, Any], output: Path, *, timeout_seconds: int) -> subprocess.CompletedProcess[str]:
    runtime = spec["runtime"]
    generator_root = Path(runtime["generator_root"])
    env = os.environ.copy()
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(generator_root) if not existing else os.pathsep.join((str(generator_root), existing))
    return subprocess.run(
        _collector_command(spec, output), cwd=runtime["root"], env=env,
        text=True, capture_output=True, check=False, timeout=timeout_seconds,
    )


def _verify_runtime(spec: dict[str, Any], *, ignore_names: set[str] | None = None) -> None:
    runtime = spec["runtime"]
    root = Path(runtime["root"]).resolve()
    output = Path(runtime["out"]).resolve()
    generator_root = Path(runtime["generator_root"]).resolve()
    _validate_runtime_boundaries(repo=runtime["repo"], root=root, generator_root=generator_root, out=output)
    head = resolve_git_head(root)
    if head is None:
        raise ConstraintError(f"target has no resolvable git HEAD: {root}")
    if head != _source_sha(spec):
        raise ConstraintError(f"source checkout moved: expected={_source_sha(spec)} current={head}")
    current_generator = f"sha256:{generator_identity(generator_root)}"
    if current_generator != spec["generator"]["identity"]:
        raise ConstraintError("generator identity differs from derivation spec")
    ignored = {output.name}
    if ignore_names:
        ignored.update(ignore_names)
    dirty = _unrelated_dirty(root, ignored)
    if dirty:
        rendered = "; ".join(dirty[:10]) + (f"; +{len(dirty)-10} more" if len(dirty) > 10 else "")
        raise ConstraintError(f"unrelated target worktree changes are present: {rendered}")


def evaluate(ledger: JobLedger, target: str) -> FreshnessReport:
    spec = refresh_identities(ledger.get_derivation(target))
    register_spec(ledger, spec)
    report = base_report(ledger, spec)
    if report.state != "fresh":
        return report
    acceptance = ledger.get_acceptance(target)
    assert acceptance is not None
    try:
        receipt = ledger.get_receipt(acceptance.receipt_id)
    except KeyError:
        return FreshnessReport(
            target=target, state="hmmm", diagnosis="receipt-missing",
            desired_freshness_key=report.desired_freshness_key,
            accepted_freshness_key=report.accepted_freshness_key,
            receipt_id=acceptance.receipt_id, active_job_id=None,
            reason="accepted SQL receipt cannot be resolved", hmmm=["accepted receipt missing"],
        )
    output = Path(spec["runtime"]["out"])
    if not output.is_file():
        return FreshnessReport(
            target=target, state="making-fresh", diagnosis="output-missing",
            desired_freshness_key=report.desired_freshness_key,
            accepted_freshness_key=report.accepted_freshness_key,
            receipt_id=receipt.id, active_job_id=None,
            reason=f"accepted output is missing: {output}", hmmm=[],
        )
    actual = sha256_file(output)
    if actual != receipt.output_sha256:
        return FreshnessReport(
            target=target, state="making-fresh", diagnosis="output-tampered",
            desired_freshness_key=report.desired_freshness_key,
            accepted_freshness_key=report.accepted_freshness_key,
            receipt_id=receipt.id, active_job_id=None,
            reason="output digest differs from accepted receipt", hmmm=[],
        )
    timeout = int(os.environ.get("STACK_VERIFY_TIMEOUT_SECONDS", "900"))
    verify_path = output.with_name(f".{output.name}.fresh-status-verify")
    try:
        try:
            _verify_runtime(spec, ignore_names={verify_path.name})
            proc = _run_collector(spec, verify_path, timeout_seconds=timeout)
        except (ConstraintError, FileNotFoundError, subprocess.TimeoutExpired) as exc:
            return FreshnessReport(
                target=target, state="hmmm", diagnosis="verifier-unavailable",
                desired_freshness_key=report.desired_freshness_key,
                accepted_freshness_key=report.accepted_freshness_key,
                receipt_id=receipt.id, active_job_id=None,
                reason="current verifier cannot establish freshness", hmmm=[str(exc)],
            )
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout or "verifier render exited non-zero").strip()
            return FreshnessReport(
                target=target, state="hmmm", diagnosis="verifier-failed",
                desired_freshness_key=report.desired_freshness_key,
                accepted_freshness_key=report.accepted_freshness_key,
                receipt_id=receipt.id, active_job_id=None,
                reason="current verifier failed", hmmm=[detail],
            )
        if not verify_path.is_file() or sha256_file(verify_path) != actual:
            return FreshnessReport(
                target=target, state="making-fresh", diagnosis="verifier-mismatch",
                desired_freshness_key=report.desired_freshness_key,
                accepted_freshness_key=report.accepted_freshness_key,
                receipt_id=receipt.id, active_job_id=None,
                reason="current deterministic verifier does not reproduce accepted bytes", hmmm=[],
            )
    finally:
        verify_path.unlink(missing_ok=True)
    return FreshnessReport(
        target=target, state="fresh", diagnosis="verified",
        desired_freshness_key=report.desired_freshness_key,
        accepted_freshness_key=report.accepted_freshness_key,
        receipt_id=receipt.id, active_job_id=None,
        reason="identities, accepted SQL receipt, output digest, and independent rerender agree",
        hmmm=[],
    )


def queue_make(ledger: JobLedger, target: str, *, executor: str = "local") -> tuple[Job | None, FreshnessReport]:
    if executor != "local":
        raise ValueError(f"executor not implemented: {executor}")
    report = evaluate(ledger, target)
    if report.state == "fresh" or report.state in {"blocked", "hmmm"}:
        return None, report
    spec = ledger.get_derivation(target)
    key = freshness_key(spec)
    active = ledger.active_job_for_target(target)
    if active and active.freshness_key != key:
        if active.state == "queued":
            ledger.cancel(active.id)
        else:
            return None, FreshnessReport(
                target=target, state="making-fresh", diagnosis="obsolete-attempt-finishing",
                desired_freshness_key=key,
                accepted_freshness_key=report.accepted_freshness_key,
                receipt_id=report.receipt_id, active_job_id=active.id,
                reason="an older-key attempt must terminate before replacement work can start",
                hmmm=[],
            )
    job = ledger.enqueue(
        kind="fresh.make", target=target, freshness_key=key,
        payload={"target": target}, executor=executor,
    )
    return job, report


def _receipt_projection(ledger: JobLedger, payload: dict[str, Any], job: Job) -> Path:
    ledger.receipt_dir.mkdir(parents=True, exist_ok=True)
    attempt = job.active_attempt_id or "unknown"
    path = ledger.receipt_dir / f"{job.id}.{attempt}.json"
    tmp = path.with_suffix(".json.tmp")
    projected = dict(payload)
    projected["authority"] = "projection-only; PostgreSQL target_acceptance is authoritative"
    tmp.write_text(json.dumps(projected, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    return path


def run_job(ledger: JobLedger, job_id: str, *, worker_id: str = "operator",
            executor: str | None = None, lease_seconds: int | None = None) -> Job:
    job = ledger.get(job_id)
    if job.kind != "fresh.make":
        raise ValueError(f"unsupported job kind: {job.kind}")
    selected_executor = executor or job.preferred_executor
    if selected_executor != "local":
        raise ValueError(f"executor not implemented: {selected_executor}")
    timeout = int(os.environ.get("STACK_COMMAND_TIMEOUT_SECONDS", "900"))
    lease_seconds = lease_seconds or int(os.environ.get("STACK_LEASE_SECONDS", "1800"))
    if lease_seconds < timeout + 60:
        raise ValueError("lease must exceed one bounded subprocess timeout by at least 60 seconds")
    if job.state == "queued":
        job = ledger.acquire_lease(job.id, worker_id=worker_id, executor=selected_executor, lease_seconds=lease_seconds)
    if job.state != "leased":
        raise ValueError(f"job must be queued/leased before execution: {job.state}")
    job = ledger.start(job.id, worker_id=worker_id)

    spec = refresh_identities(ledger.get_derivation(job.target))
    register_spec(ledger, spec)
    current_key = freshness_key(spec)
    if current_key != job.freshness_key:
        return ledger.fail(
            job.id,
            error=f"desired freshness key moved: queued={job.freshness_key} current={current_key}",
            hmmm="enqueue current identities after this obsolete attempt terminates",
        )
    try:
        _verify_runtime(spec)
    except (ConstraintError, FileNotFoundError) as exc:
        return ledger.hold(job.id, constraint=str(exc))

    output = Path(spec["runtime"]["out"])
    output.parent.mkdir(parents=True, exist_ok=True)
    fd1, candidate_name = tempfile.mkstemp(prefix=f".{output.name}.", suffix=".candidate", dir=output.parent)
    fd2, verify_name = tempfile.mkstemp(prefix=f".{output.name}.", suffix=".verify", dir=output.parent)
    os.close(fd1)
    os.close(fd2)
    candidate = Path(candidate_name)
    verifier = Path(verify_name)
    candidate.unlink(missing_ok=True)
    verifier.unlink(missing_ok=True)
    try:
        ledger.heartbeat(job.id, worker_id=worker_id, lease_seconds=lease_seconds)
        try:
            proc = _run_collector(spec, candidate, timeout_seconds=timeout)
        except subprocess.TimeoutExpired as exc:
            return ledger.fail(job.id, error=f"executor exceeded {timeout}s: {exc}")
        if proc.returncode != 0:
            return ledger.fail(job.id, error=(proc.stderr or proc.stdout or "executor failed").strip())
        if not candidate.is_file():
            return ledger.fail(job.id, error="executor reported success without candidate output")

        try:
            _verify_runtime(spec, ignore_names={candidate.name, verifier.name})
        except (ConstraintError, FileNotFoundError) as exc:
            return ledger.hold(job.id, constraint=str(exc))
        ledger.heartbeat(job.id, worker_id=worker_id, lease_seconds=lease_seconds)
        ledger.mark_verifying(job.id, worker_id=worker_id)
        try:
            verify_proc = _run_collector(spec, verifier, timeout_seconds=timeout)
        except subprocess.TimeoutExpired as exc:
            return ledger.fail(job.id, error=f"verifier exceeded {timeout}s: {exc}")
        if verify_proc.returncode != 0:
            return ledger.fail(job.id, error=(verify_proc.stderr or verify_proc.stdout or "verifier failed").strip())
        if not verifier.is_file():
            return ledger.fail(job.id, error="verifier reported success without output")
        candidate_digest = sha256_file(candidate)
        if candidate_digest != sha256_file(verifier):
            return ledger.fail(
                job.id, error="executor candidate and independent verifier output differ",
                hmmm="generation is nondeterministic or executor/verifier environments diverge",
            )
        try:
            _verify_runtime(spec, ignore_names={candidate.name, verifier.name})
        except (ConstraintError, FileNotFoundError) as exc:
            return ledger.hold(job.id, constraint=str(exc))

        os.replace(candidate, output)
        made_at = datetime.now(timezone.utc).isoformat()
        attempt_id = ledger.get(job.id).active_attempt_id
        assert attempt_id is not None
        payload = receipt_payload(
            spec=spec, key=current_key,
            outputs=[{"path": str(output), "sha256": candidate_digest}],
            verifier_identity=spec["verifier"]["identity"],
            executor=selected_executor, attempt_id=attempt_id, made_fresh_at=made_at,
        )
        current_job = ledger.get(job.id)
        _receipt_projection(ledger, payload, current_job)
        return ledger.accept_success(
            job.id, receipt=payload, output_path=str(output), output_sha256=candidate_digest,
        )
    finally:
        candidate.unlink(missing_ok=True)
        verifier.unlink(missing_ok=True)


def make(ledger: JobLedger, target: str, *, executor: str = "local",
         worker_id: str = "operator") -> tuple[Job | None, FreshnessReport]:
    job, before = queue_make(ledger, target, executor=executor)
    if job is None:
        return None, before
    if job.state in {"succeeded", "failed", "hmmm", "cancelled"}:
        job = ledger.retry(job.id, executor=executor)
    if job.state in {"leased", "running", "verifying"}:
        return job, evaluate(ledger, target)
    result = run_job(ledger, job.id, worker_id=worker_id, executor=executor)
    return result, evaluate(ledger, target)


def retry_job(ledger: JobLedger, job_id: str, *, executor: str = "local",
              worker_id: str = "operator") -> Job:
    queued = ledger.retry(job_id, executor=executor)
    return run_job(ledger, queued.id, worker_id=worker_id, executor=executor)


def registered_affected_closure(ledger: JobLedger, changed_targets: list[str]) -> list[str]:
    return affected_closure(ledger.list_derivations(), changed_targets)
