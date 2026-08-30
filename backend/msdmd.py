"""MSDMD adapter for stack fresh-making.

Generation is local in the first vertical slice. The executor produces a
candidate; a second deterministic render verifies it before atomic publication.
GitHub Actions is not required for identity, state, verification, or recovery.
"""
from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_msdmd_fresh_maker
#   module_name: msdmd_fresh_maker
#   module_kind: adapter
#   summary: applies fresh-making to repo-owned MSDMD collection generation using a local executor and independent rerender verification
#   owner: stack
#   public_surface: build_spec, evaluate, queue_make, run_job, make, retry_job
#   storage_boundary: write
#   network_boundary: none
#   tests: backend.tests.test_orchestrator
#   rollout: frontend.cli.stackctl fresh commands
#   rollback: stop fresh commands; accepted source repositories remain authoritative
#   unresolved: VM and GitHub Actions executor adapters
# === END MODULE_BUILD ===

# === BOUNDARIES ===
# id: stack_msdmd_fresh_execution
#   summary: executes a pinned repo-local MSDMD collector against an explicit checkout; publishes only verified generated output
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   side_effects: job, filesystem, subprocess
#   owner: stack
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: stack_msdmd_fresh_exact_identity
#   given: source or generator identity changes after a job is queued
#   then: the queued job fails closed and cannot publish under the old freshness key
#   class: provenance
#
# id: stack_msdmd_false_green_rejected
#   given: an executor exits successfully but an independent rerender differs
#   then: no accepted receipt or published output is produced
#   class: verification
#
# id: stack_msdmd_publish_after_verify
#   given: candidate and independent verifier outputs match byte-for-byte
#   then: the candidate is atomically published and a fresh-making receipt becomes the accepted target evidence
#   class: evidence
# === END CONTRACTS ===

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

from .freshness import (
    SPEC_SCHEMA,
    SPEC_VERSION,
    SpecStore,
    FreshnessReport,
    base_report,
    freshness_key,
    read_receipt,
    receipt_payload,
    sha256_file,
    tree_sha256,
    write_receipt,
)
from .jobs import Job, JobLedger


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
    package = Path(generator_root).resolve() / "msdmd"
    if not (package / "collect.py").is_file():
        raise FileNotFoundError(f"MSDMD collector not found: {package / 'collect.py'}")
    return tree_sha256(package, suffixes=(".py",))


def _source_identity(source_sha: str) -> str:
    if len(source_sha) != 40:
        raise ValueError("source SHA must be a full 40-character commit identity")
    return f"git:{source_sha}"


def _source_sha(spec: dict[str, Any]) -> str:
    for item in spec["inputs"]:
        if item.get("name") == "repository":
            identity = str(item.get("identity", ""))
            if identity.startswith("git:") and len(identity) == 44:
                return identity[4:]
    raise ValueError("MSDMD spec has no exact repository git identity")


def build_spec(*, repo: str, root: str | Path, generator_root: str | Path,
               out: str | Path | None = None, source_sha: str | None = None) -> dict[str, Any]:
    root_path = Path(root).resolve()
    if not root_path.is_dir():
        raise FileNotFoundError(root_path)
    resolved = source_sha or resolve_git_head(root_path)
    if not resolved:
        raise ValueError("exact source SHA is required when target root is not a git checkout")
    source_mode = "explicit" if source_sha and resolve_git_head(root_path) is None else "git"
    output_path = Path(out) if out is not None else Path(f"{repo}_msdmd.ts")
    if not output_path.is_absolute():
        output_path = root_path / output_path
    generator_path = Path(generator_root).resolve()
    gen_identity = generator_identity(generator_path)
    return {
        "schema": SPEC_SCHEMA,
        "version": SPEC_VERSION,
        "target": f"msdmd:{repo}",
        "kind": "msdmd.collection",
        "inputs": [{"name": "repository", "identity": _source_identity(resolved)}],
        "generator": {
            "identity": f"sha256:{gen_identity}",
            "command": "python -m msdmd.collect --root <root> --repo <repo> --out <candidate> --source-commit <sha>",
        },
        "outputs": [{"path": output_path.name}],
        "verifier": {
            "identity": f"sha256:{gen_identity}",
            "command": "rerender-to-isolated-candidate-and-byte-compare@1",
        },
        "depends_on": [],
        "runtime": {
            "repo": repo,
            "root": str(root_path),
            "out": str(output_path.resolve()),
            "generator_root": str(generator_path),
            "source_identity_mode": source_mode,
        },
    }


def refresh_identities(spec: dict[str, Any]) -> dict[str, Any]:
    if spec.get("kind") != "msdmd.collection":
        raise ValueError(f"unsupported derivation kind: {spec.get('kind')}")
    current = json.loads(json.dumps(spec))
    runtime = current["runtime"]
    root = Path(runtime["root"])
    if runtime.get("source_identity_mode") == "git":
        resolved = resolve_git_head(root)
        if not resolved:
            current["inputs"][0]["identity"] = "hmmm"
        else:
            current["inputs"][0]["identity"] = _source_identity(resolved)
    try:
        current_generator = generator_identity(runtime["generator_root"])
    except (FileNotFoundError, ValueError):
        current["generator"]["identity"] = "hmmm"
        current["verifier"]["identity"] = "hmmm"
    else:
        identity = f"sha256:{current_generator}"
        current["generator"]["identity"] = identity
        current["verifier"]["identity"] = identity
    return current


def _collector_command(spec: dict[str, Any], output: Path) -> list[str]:
    runtime = spec["runtime"]
    return [
        sys.executable, "-m", "msdmd.collect",
        "--root", runtime["root"],
        "--repo", runtime["repo"],
        "--out", str(output),
        "--source-commit", _source_sha(spec),
    ]


def _run_collector(spec: dict[str, Any], output: Path) -> subprocess.CompletedProcess[str]:
    runtime = spec["runtime"]
    generator_root = Path(runtime["generator_root"])
    env = os.environ.copy()
    existing = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(generator_root) if not existing
        else os.pathsep.join((str(generator_root), existing))
    )
    return subprocess.run(
        _collector_command(spec, output), cwd=runtime["root"], env=env,
        text=True, capture_output=True, check=False,
    )


def evaluate(ledger: JobLedger, store: SpecStore, target: str) -> FreshnessReport:
    spec = refresh_identities(store.get(target))
    store.put(spec)
    report = base_report(ledger, spec)
    if report.state != "fresh":
        return report

    acceptance = ledger.get_acceptance(target)
    assert acceptance is not None
    try:
        receipt = read_receipt(acceptance.receipt_path)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        return FreshnessReport(
            target=target, state="hmmm", diagnosis="receipt-unreadable",
            desired_freshness_key=report.desired_freshness_key,
            accepted_freshness_key=report.accepted_freshness_key,
            receipt_path=acceptance.receipt_path, active_job_id=None,
            reason="accepted receipt cannot be validated", hmmm=[str(exc)],
        )

    runtime = spec["runtime"]
    output = Path(runtime["out"])
    receipt_outputs = receipt.get("outputs", [])
    if len(receipt_outputs) != 1:
        return FreshnessReport(
            target=target, state="hmmm", diagnosis="receipt-output-shape",
            desired_freshness_key=report.desired_freshness_key,
            accepted_freshness_key=report.accepted_freshness_key,
            receipt_path=acceptance.receipt_path, active_job_id=None,
            reason="MSDMD receipt must describe exactly one output",
            hmmm=["receipt/output contract mismatch"],
        )
    if not output.is_file():
        return FreshnessReport(
            target=target, state="making-fresh", diagnosis="output-missing",
            desired_freshness_key=report.desired_freshness_key,
            accepted_freshness_key=report.accepted_freshness_key,
            receipt_path=acceptance.receipt_path, active_job_id=None,
            reason=f"accepted output is missing: {output}", hmmm=[],
        )
    actual_digest = sha256_file(output)
    if actual_digest != receipt_outputs[0].get("sha256"):
        return FreshnessReport(
            target=target, state="making-fresh", diagnosis="output-tampered",
            desired_freshness_key=report.desired_freshness_key,
            accepted_freshness_key=report.accepted_freshness_key,
            receipt_path=acceptance.receipt_path, active_job_id=None,
            reason="output digest differs from accepted receipt", hmmm=[],
        )

    verifier_output = output.with_name(f".{output.name}.fresh-verify")
    try:
        proc = _run_collector(spec, verifier_output)
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout or "verifier render exited non-zero").strip()
            return FreshnessReport(
                target=target, state="hmmm", diagnosis="verifier-failed",
                desired_freshness_key=report.desired_freshness_key,
                accepted_freshness_key=report.accepted_freshness_key,
                receipt_path=acceptance.receipt_path, active_job_id=None,
                reason="current verifier could not reproduce the artifact", hmmm=[detail],
            )
        if not verifier_output.is_file() or sha256_file(verifier_output) != actual_digest:
            return FreshnessReport(
                target=target, state="making-fresh", diagnosis="verifier-mismatch",
                desired_freshness_key=report.desired_freshness_key,
                accepted_freshness_key=report.accepted_freshness_key,
                receipt_path=acceptance.receipt_path, active_job_id=None,
                reason="current deterministic verifier does not reproduce accepted bytes",
                hmmm=[],
            )
    finally:
        verifier_output.unlink(missing_ok=True)

    return FreshnessReport(
        target=target, state="fresh", diagnosis="verified",
        desired_freshness_key=report.desired_freshness_key,
        accepted_freshness_key=report.accepted_freshness_key,
        receipt_path=acceptance.receipt_path, active_job_id=None,
        reason="identities, receipt, output digest, and independent rerender all agree",
        hmmm=[],
    )


def queue_make(ledger: JobLedger, store: SpecStore, target: str,
               *, executor: str = "local") -> tuple[Job | None, FreshnessReport]:
    if executor != "local":
        raise ValueError(f"executor not implemented: {executor}")
    report = evaluate(ledger, store, target)
    if report.state == "fresh":
        return None, report
    if report.state in {"blocked", "hmmm"}:
        return None, report
    spec = store.get(target)
    key = freshness_key(spec)
    job = ledger.enqueue(
        kind="fresh.make", target=target, freshness_key=key,
        payload={"spec_target": target}, executor=executor,
    )
    return job, report


def run_job(ledger: JobLedger, store: SpecStore, job_id: str,
            *, worker: str = "stackctl", executor: str | None = None,
            lease_ttl_seconds: int = 300) -> Job:
    job = ledger.get(job_id)
    if job.kind != "fresh.make":
        raise ValueError(f"unsupported job kind: {job.kind}")
    if job.state != "queued":
        raise ValueError(f"job must be queued before execution: {job.state}")
    selected_executor = executor or job.preferred_executor
    if selected_executor != "local":
        raise ValueError(f"executor not implemented: {selected_executor}")

    spec = refresh_identities(store.get(job.target))
    store.put(spec)
    current_key = freshness_key(spec)
    if current_key != job.freshness_key:
        leased = ledger.acquire_lease(
            job.id, owner=worker, executor=selected_executor,
            ttl_seconds=lease_ttl_seconds,
        )
        ledger.start(leased.id, owner=worker)
        return ledger.fail(
            leased.id,
            error=f"desired freshness key moved: queued={job.freshness_key} current={current_key}",
            hmmm="enqueue a new make-fresh job for the current identities",
        )

    leased = ledger.acquire_lease(
        job.id, owner=worker, executor=selected_executor,
        ttl_seconds=lease_ttl_seconds,
    )
    running = ledger.start(leased.id, owner=worker)
    runtime = spec["runtime"]
    output = Path(runtime["out"])
    output.parent.mkdir(parents=True, exist_ok=True)
    attempt_id = running.active_attempt_id
    assert attempt_id is not None
    candidate = output.with_name(f".{output.name}.{attempt_id}.candidate")
    verifier_output = output.with_name(f".{output.name}.{attempt_id}.verify")

    try:
        proc = _run_collector(spec, candidate)
        if proc.returncode != 0:
            detail = (proc.stderr or proc.stdout or "MSDMD collector exited non-zero").strip()
            return ledger.fail(running.id, error=detail)
        if not candidate.is_file():
            return ledger.fail(
                running.id,
                error=f"executor reported success but candidate is missing: {candidate}",
                hmmm="collector/output contract mismatch",
            )

        ledger.mark_verifying(running.id, owner=worker)
        verify_proc = _run_collector(spec, verifier_output)
        if verify_proc.returncode != 0:
            detail = (verify_proc.stderr or verify_proc.stdout or "verifier render exited non-zero").strip()
            return ledger.fail(running.id, error=f"verifier failed: {detail}")
        if not verifier_output.is_file():
            return ledger.fail(
                running.id, error="verifier reported success but produced no output",
                hmmm="verifier/output contract mismatch",
            )
        candidate_digest = sha256_file(candidate)
        verifier_digest = sha256_file(verifier_output)
        if candidate_digest != verifier_digest:
            return ledger.fail(
                running.id,
                error="executor candidate and independent verifier output differ",
                hmmm="generation is nondeterministic or executor/verifier environments diverge",
            )

        os.replace(candidate, output)
        made_at = datetime.now(timezone.utc).isoformat()
        payload = receipt_payload(
            spec=spec, key=current_key,
            outputs=[{"path": str(output), "sha256": candidate_digest}],
            verifier_identity=spec["verifier"]["identity"],
            executor=selected_executor, attempt_id=attempt_id,
            made_fresh_at=made_at,
        )
        receipt = write_receipt(ledger.db_path.parent, payload)
        ledger.accept_target(
            target=job.target, freshness_key=current_key, receipt_path=str(receipt)
        )
        return ledger.succeed(running.id, receipt_path=str(receipt))
    finally:
        candidate.unlink(missing_ok=True)
        verifier_output.unlink(missing_ok=True)


def make(ledger: JobLedger, store: SpecStore, target: str, *,
         executor: str = "local", worker: str = "stackctl") -> tuple[Job | None, FreshnessReport]:
    job, before = queue_make(ledger, store, target, executor=executor)
    if job is None:
        return None, before
    if job.state in {"succeeded", "failed", "cancelled", "hmmm"}:
        job = ledger.retry(job.id, executor=executor)
    if job.state in {"leased", "running", "verifying"}:
        return job, evaluate(ledger, store, target)
    result = run_job(ledger, store, job.id, worker=worker, executor=executor)
    return result, evaluate(ledger, store, target)


def retry_job(ledger: JobLedger, store: SpecStore, job_id: str, *,
              executor: str = "local", worker: str = "stackctl") -> Job:
    job = ledger.retry(job_id, executor=executor)
    return run_job(ledger, store, job.id, worker=worker, executor=executor)
