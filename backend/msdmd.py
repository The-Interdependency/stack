"""Durable MSDMD regeneration orchestration.

The first executor is local and synchronous. GitHub Actions is deliberately not
required for job identity, durable state, verification, or retry.

Usage:
    python -m frontend.cli.stackctl msdmd refresh ucns --root ../ucns
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
#   internal_surface: source identity resolution, generator identity, local subprocess execution, receipt writing
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: backend.tests.test_orchestrator
#   rollout: invoked through frontend.cli.stackctl; local executor only in first vertical slice
#   rollback: stop invoking the CLI and remove untracked .stack operational state
#   unresolved: vm executor, github-actions executor, organization-level affected-repo discovery
# === END MODULE_BUILD ===

# === BOUNDARIES ===
# id: stack_msdmd_regeneration_execution
#   summary: executes the pinned skill-lib MSDMD collector against an explicit repository checkout and writes that repository collection artifact
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   side_effects: job, filesystem, subprocess
#   owner: stack
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: stack_msdmd_refresh_source_pinned
#   given: an MSDMD refresh job was queued for an exact source commit
#   then: execution refuses to write when the target checkout has moved to a different resolvable commit
#   class: provenance
#
# id: stack_msdmd_refresh_receipted
#   given: a local MSDMD regeneration exits successfully and produces the requested collection artifact
#   then: the artifact SHA-256 and exact source and generator identities are persisted in the job ledger and a JSON receipt
#   class: evidence
#
# id: stack_msdmd_refresh_executor_independent_state
#   given: GitHub Actions is unavailable or unused
#   then: local execution still queues, executes, verifies, records, and retries through the SQLite ledger
#   class: resilience
# === END CONTRACTS ===

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

from .jobs import Job, JobLedger


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
    return value if len(value) == 40 else None


def generator_identity(generator_root: str | Path) -> str:
    collector = Path(generator_root).resolve() / "msdmd" / "collect.py"
    if not collector.is_file():
        raise FileNotFoundError(f"MSDMD collector not found: {collector}")
    return sha256_file(collector)


def queue_refresh(ledger: JobLedger, *, repo: str, root: str | Path,
                  generator_root: str | Path, out: str | Path | None = None,
                  source_sha: str | None = None, executor: str = "local") -> Job:
    if executor != "local":
        raise ValueError(f"executor not implemented: {executor}")
    root_path = Path(root).resolve()
    if not root_path.is_dir():
        raise FileNotFoundError(root_path)
    resolved_source = source_sha or resolve_git_head(root_path)
    if not resolved_source:
        raise ValueError("exact source SHA is required when target root is not a git checkout")
    if len(resolved_source) != 40:
        raise ValueError("source SHA must be a full 40-character commit identity")
    output_path = Path(out) if out is not None else Path(f"{repo}_msdmd.ts")
    if not output_path.is_absolute():
        output_path = root_path / output_path
    payload: dict[str, Any] = {
        "root": str(root_path),
        "out": str(output_path.resolve()),
        "generator_root": str(Path(generator_root).resolve()),
    }
    return ledger.enqueue(
        kind="msdmd.refresh", target=repo, source_sha=resolved_source,
        generator_identity=generator_identity(generator_root), executor=executor,
        payload=payload, hmmm=None,
    )


def _receipt_dir(ledger: JobLedger) -> Path:
    path = ledger.db_path.parent / "receipts"
    path.mkdir(parents=True, exist_ok=True)
    return path


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
    path = _receipt_dir(ledger) / f"{job.id}.json"
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def run_job(ledger: JobLedger, job_id: str) -> Job:
    job = ledger.get(job_id)
    if job.kind != "msdmd.refresh":
        raise ValueError(f"unsupported job kind: {job.kind}")
    if job.executor != "local":
        raise ValueError(f"executor not implemented: {job.executor}")
    if job.state != "queued":
        raise ValueError(f"job must be queued before execution: {job.state}")

    root = Path(job.payload["root"])
    out = Path(job.payload["out"])
    generator_root = Path(job.payload["generator_root"])

    current_sha = resolve_git_head(root)
    if current_sha is not None and current_sha != job.source_sha:
        running = ledger.start(job.id)
        return ledger.fail(
            running.id,
            error=f"source checkout moved: queued={job.source_sha} current={current_sha}",
            hmmm="requeue against the intended exact commit or restore the checkout before retrying",
        )

    current_generator = generator_identity(generator_root)
    if current_generator != job.generator_identity:
        running = ledger.start(job.id)
        return ledger.fail(
            running.id,
            error=("generator identity moved: "
                   f"queued={job.generator_identity} current={current_generator}"),
            hmmm="requeue with the intended skill-lib generator identity",
        )

    running = ledger.start(job.id)
    out.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(generator_root) if not existing else os.pathsep.join((str(generator_root), existing))
    command = [
        sys.executable, "-m", "msdmd.collect",
        "--root", str(root), "--repo", job.target,
        "--out", str(out), "--source-commit", job.source_sha,
    ]
    proc = subprocess.run(command, cwd=root, env=env, text=True,
                          capture_output=True, check=False)
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "MSDMD collector exited non-zero").strip()
        return ledger.fail(running.id, error=detail)
    if not out.is_file():
        return ledger.fail(
            running.id,
            error=f"collector reported success but artifact is missing: {out}",
            hmmm="collector/output contract mismatch",
        )

    succeeded = ledger.succeed(
        running.id, artifact_path=str(out), artifact_sha256=sha256_file(out)
    )
    _write_receipt(ledger, succeeded)
    return succeeded


def retry_job(ledger: JobLedger, job_id: str) -> Job:
    job = ledger.get(job_id)
    if job.state not in {"failed", "cancelled"}:
        raise ValueError(f"only failed or cancelled jobs can be retried: {job.state}")
    queued = ledger.retry(job_id)
    return run_job(ledger, queued.id)
