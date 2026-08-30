"""Durable MSDMD regeneration orchestration.

PostgreSQL owns job/attempt/receipt state; the target repository owns its source
and generated collection artifact. The worker uses a pinned skill-lib collector
identity and refuses to write across source, generator, checkout, or worktree
boundaries it cannot prove.

Usage:
    python -m frontend.cli.stackctl msdmd refresh ucns --root /srv/stack-repos/ucns
    python -m frontend.cli.stackctl msdmd status
    python -m frontend.cli.stackctl msdmd retry <job-id>
"""
from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_msdmd_regeneration_orchestrator
#   module_name: msdmd_regeneration_orchestrator
#   module_kind: engine
#   summary: queues, executes, verifies, and receipts commit-pinned MSDMD regeneration jobs independently of GitHub Actions
#   owner: stack
#   public_surface: queue_refresh, run_job, retry_job
#   internal_surface: runtime boundary checks, source identity, generator identity, atomic local subprocess execution, receipt writing
#   auth_boundary: write
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: true
#   tests: backend.tests.test_orchestrator
#   rollout: VM worker and frontend.cli.stackctl
#   rollback: stop worker; PostgreSQL records and repository artifacts remain inspectable
# === END MODULE_BUILD ===

# === BOUNDARIES ===
# id: stack_msdmd_regeneration_execution
#   summary: executes a pinned skill-lib MSDMD collector against one explicitly allowed repository checkout and atomically replaces its collection artifact
#   auth_boundary: write
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: true
#   side_effects: job, filesystem, subprocess
#   owner: stack
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: stack_msdmd_refresh_source_pinned
#   given: an MSDMD refresh job was queued for an exact source commit
#   then: execution refuses to replace the artifact unless target HEAD equals that commit both before and after generation
#   class: provenance
#
# id: stack_msdmd_refresh_generator_pinned
#   given: an MSDMD refresh job was queued with an exact collector digest
#   then: execution refuses to replace the artifact if the collector digest changes before completion
#   class: provenance
#
# id: stack_msdmd_refresh_clean_boundary
#   given: a target git checkout contains unrelated uncommitted changes
#   then: execution enters hmmm before invoking the generator and preserves those changes
#   class: safety
#
# id: stack_msdmd_refresh_receipted
#   given: local MSDMD regeneration exits successfully and produces the requested collection artifact
#   then: artifact SHA-256 plus exact source and generator identities are persisted in PostgreSQL and a JSON receipt
#   class: evidence
#
# id: stack_msdmd_refresh_executor_independent_state
#   given: GitHub Actions is unavailable or unused
#   then: VM-local execution still queues, executes, verifies, records, and retries through PostgreSQL
#   class: resilience
# === END CONTRACTS ===

from dataclasses import replace
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any

from .jobs import Job, JobLedger

_SHA40 = re.compile(r"^[0-9a-f]{40}$")

class ConstraintError(RuntimeError):
    """Operator-resolvable constraint that must remain visible as hmmm."""

def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
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
    collector = Path(generator_root).resolve() / "msdmd" / "collect.py"
    if not collector.is_file():
        raise FileNotFoundError(f"MSDMD collector not found: {collector}")
    return sha256_file(collector)

def _parse_allowed_repos(raw: str) -> set[str]:
    return {part.strip() for part in raw.split(",") if part.strip()}

def _validate_runtime_boundaries(*, repo: str, root: Path,
                                 generator_root: Path, out: Path) -> None:
    repo_root_raw = os.environ.get("STACK_REPO_ROOT", "").strip()
    if repo_root_raw:
        repo_root = Path(repo_root_raw).expanduser().resolve()
        allowed = _parse_allowed_repos(os.environ.get("STACK_ALLOWED_REPOS", ""))
        if not allowed:
            raise ConstraintError("STACK_ALLOWED_REPOS is required with STACK_REPO_ROOT")
        if repo not in allowed:
            raise ConstraintError(f"repository is not allowed by STACK_ALLOWED_REPOS: {repo}")
        if root.parent != repo_root or root.name != repo:
            raise ConstraintError(
                f"target must be the direct configured checkout {repo_root / repo}: {root}"
            )
        if not (root / ".git").exists():
            raise ConstraintError(f"configured production target is not a git checkout: {root}")

    skill_root_raw = os.environ.get("STACK_SKILL_LIB_ROOT", "").strip()
    if skill_root_raw:
        expected = Path(skill_root_raw).expanduser().resolve()
        if generator_root != expected:
            raise ConstraintError(
                f"generator root differs from STACK_SKILL_LIB_ROOT: {generator_root} != {expected}"
            )

    if out.parent != root:
        raise ConstraintError(f"MSDMD artifact must remain at repository root: {out}")

def _git_status(root: Path) -> list[str]:
    proc = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain=v1", "--untracked-files=all"],
        text=True, capture_output=True, check=False,
    )
    if proc.returncode != 0:
        return []
    return [line for line in proc.stdout.splitlines() if line]

def _dirty_path(line: str) -> str:
    path = line[3:]
    if " -> " in path:
        path = path.split(" -> ", 1)[1]
    return path.strip('"')

def _unrelated_dirty(root: Path, output_name: str) -> list[str]:
    return [line for line in _git_status(root) if _dirty_path(line) != output_name]

def queue_refresh(ledger: JobLedger, *, repo: str, root: str | Path,
                  generator_root: str | Path, out: str | Path | None = None,
                  source_sha: str | None = None, executor: str = "local") -> Job:
    if executor not in {"local", "github-actions"}:
        raise ValueError(f"unknown executor: {executor}")
    if executor != "local":
        raise ValueError(f"executor not implemented: {executor}")

    root_path = Path(root).expanduser().resolve()
    if not root_path.is_dir():
        raise FileNotFoundError(root_path)
    generator_path = Path(generator_root).expanduser().resolve()
    resolved_source = source_sha or resolve_git_head(root_path)
    if not resolved_source or not _SHA40.fullmatch(resolved_source):
        raise ValueError("source SHA must be an exact 40-character lowercase commit identity")

    output_path = Path(out) if out is not None else Path(f"{repo}_msdmd.ts")
    if not output_path.is_absolute():
        output_path = root_path / output_path
    output_path = output_path.resolve()
    _validate_runtime_boundaries(
        repo=repo, root=root_path, generator_root=generator_path, out=output_path,
    )
    payload: dict[str, Any] = {
        "root": str(root_path),
        "out": str(output_path),
        "generator_root": str(generator_path),
    }
    return ledger.enqueue(
        kind="msdmd.refresh", target=repo, source_sha=resolved_source,
        generator_identity=generator_identity(generator_path), executor=executor,
        payload=payload, hmmm=None,
    )

def _write_receipt(ledger: JobLedger, job: Job) -> Path:
    receipt = {
        "schema": "the-interdependency.stack-job-receipt",
        "version": "1.0.0",
        "job": {
            "id": job.id,
            "kind": job.kind,
            "target": job.target,
            "source_sha": job.source_sha,
            "generator_identity": job.generator_identity,
            "executor": job.executor,
            "attempts": job.attempts,
            "artifact_path": job.artifact_path,
            "artifact_sha256": job.artifact_sha256,
        },
    }
    ledger.receipt_dir.mkdir(parents=True, exist_ok=True)
    path = ledger.receipt_dir / f"{job.id}.json"
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    return path

def _hold(ledger: JobLedger, job_id: str, constraint: str) -> Job:
    return ledger.hold(job_id, constraint=constraint)

def run_job(ledger: JobLedger, job_id: str, *, worker_id: str = "operator") -> Job:
    job = ledger.get(job_id)
    if job.kind != "msdmd.refresh":
        raise ValueError(f"unsupported job kind: {job.kind}")
    if job.executor != "local":
        raise ValueError(f"executor not implemented: {job.executor}")
    if job.state == "queued":
        job = ledger.start(job.id, worker_id=worker_id)
    elif job.state != "running":
        raise ValueError(f"job must be queued/running before execution: {job.state}")

    root = Path(job.payload["root"]).resolve()
    out = Path(job.payload["out"]).resolve()
    generator_root = Path(job.payload["generator_root"]).resolve()
    try:
        _validate_runtime_boundaries(repo=job.target, root=root, generator_root=generator_root, out=out)
        before_sha = resolve_git_head(root)
        production_bound = bool(os.environ.get("STACK_REPO_ROOT", "").strip())
        if production_bound and before_sha is None:
            raise ConstraintError(f"production target has no resolvable git HEAD: {root}")
        if before_sha is not None and before_sha != job.source_sha:
            raise ConstraintError(f"source checkout moved: queued={job.source_sha} current={before_sha}")
        current_generator = generator_identity(generator_root)
        if current_generator != job.generator_identity:
            raise ConstraintError(
                "generator identity moved: "
                f"queued={job.generator_identity} current={current_generator}"
            )
        if before_sha is not None:
            dirty = _unrelated_dirty(root, out.name)
            if dirty:
                rendered = "; ".join(dirty[:10])
                if len(dirty) > 10:
                    rendered += f"; +{len(dirty) - 10} more"
                raise ConstraintError(f"unrelated target worktree changes are present: {rendered}")
    except (ConstraintError, FileNotFoundError) as exc:
        return _hold(ledger, job.id, str(exc))

    out.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{out.name}.", suffix=".tmp", dir=out.parent)
    os.close(fd)
    temp_path = Path(temp_name)
    env = os.environ.copy()
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(generator_root) if not existing else os.pathsep.join((str(generator_root), existing))
    command = [
        sys.executable, "-m", "msdmd.collect",
        "--root", str(root), "--repo", job.target,
        "--out", str(temp_path), "--source-commit", job.source_sha,
    ]
    timeout_seconds = int(os.environ.get("STACK_COMMAND_TIMEOUT_SECONDS", "900"))
    try:
        try:
            proc = subprocess.run(
                command, cwd=root, env=env, text=True, capture_output=True,
                check=False, timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            return ledger.fail(job.id, error=f"MSDMD collector exceeded {timeout_seconds}s: {exc}")
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout or "MSDMD collector exited non-zero").strip()
            return ledger.fail(job.id, error=detail)
        if not temp_path.is_file() or temp_path.stat().st_size == 0:
            return ledger.fail(job.id, error=f"collector reported success but artifact is empty/missing: {temp_path}")

        after_sha = resolve_git_head(root)
        if before_sha is not None and after_sha != job.source_sha:
            return _hold(
                ledger, job.id,
                f"source checkout changed during generation: queued={job.source_sha} current={after_sha}",
            )
        after_generator = generator_identity(generator_root)
        if after_generator != job.generator_identity:
            return _hold(
                ledger, job.id,
                "generator identity changed during generation: "
                f"queued={job.generator_identity} current={after_generator}",
            )
        artifact_sha = sha256_file(temp_path)
        os.replace(temp_path, out)
        # Materialize the JSON evidence before closing SQL success. If this
        # filesystem write fails, the leased job remains recoverable instead of
        # becoming succeeded-without-projection. PostgreSQL remains authoritative.
        _write_receipt(
            ledger,
            replace(job, artifact_path=str(out), artifact_sha256=artifact_sha),
        )
        return ledger.succeed(
            job.id, artifact_path=str(out), artifact_sha256=artifact_sha
        )
    finally:
        temp_path.unlink(missing_ok=True)

def retry_job(ledger: JobLedger, job_id: str, *, worker_id: str = "operator") -> Job:
    job = ledger.get(job_id)
    if job.state not in {"failed", "hmmm", "cancelled"}:
        raise ValueError(f"only failed, hmmm, or cancelled jobs can be retried: {job.state}")
    queued = ledger.retry(job_id)
    return run_job(ledger, queued.id, worker_id=worker_id)
