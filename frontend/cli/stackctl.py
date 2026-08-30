"""Operator CLI for PostgreSQL-backed stack orchestration.

Usage:
    python -m frontend.cli.stackctl db migrate
    python -m frontend.cli.stackctl msdmd refresh ucns --root /srv/stack-repos/ucns
    python -m frontend.cli.stackctl msdmd status
    python -m frontend.cli.stackctl worker run
"""
from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_operator_cli
#   module_name: stackctl
#   module_kind: adapter
#   summary: exposes PostgreSQL migrations, durable MSDMD controls, status, and the VM worker loop to a human operator
#   owner: stack
#   public_surface: python -m frontend.cli.stackctl
#   internal_surface: argparse command dispatch, JobLedger, backend.msdmd, backend.worker
#   auth_boundary: write
#   storage_boundary: write
#   network_boundary: internal
#   user_data_boundary: none
#   admin_only: true
#   tests: backend.tests.test_orchestrator
#   rollout: explicit operator invocation and systemd worker ExecStart
#   rollback: stop worker and stop invoking the module
# === END MODULE_BUILD ===

# === BOUNDARIES ===
# id: stack_operator_cli_orchestration
#   summary: permits an authorized VM operator to migrate, create, execute, inspect, cancel, and retry orchestration jobs
#   auth_boundary: write
#   storage_boundary: write
#   network_boundary: internal
#   user_data_boundary: none
#   admin_only: true
#   side_effects: job, database, filesystem, subprocess
#   owner: stack
# === END BOUNDARIES ===

import argparse
from dataclasses import asdict
import json
import os
from pathlib import Path
import sys

from backend.jobs import Job, JobLedger
from backend.msdmd import queue_refresh, retry_job, run_job
from backend.worker import run_forever, run_once

def _database_url(args: argparse.Namespace) -> str:
    value = args.database_url or os.environ.get("STACK_DATABASE_URL", "")
    if not value:
        raise ValueError("STACK_DATABASE_URL or --database-url is required")
    return value

def _ledger(args: argparse.Namespace) -> JobLedger:
    receipt_dir = args.receipt_dir or os.environ.get("STACK_RECEIPT_DIR", ".stack/state/receipts")
    return JobLedger(_database_url(args), receipt_dir=receipt_dir)

def _print_job(job: Job) -> None:
    print(json.dumps(asdict(job), indent=2, sort_keys=True))

def _target_root(args: argparse.Namespace) -> Path:
    if args.root is not None:
        return args.root
    configured = os.environ.get("STACK_REPO_ROOT", "").strip()
    if not configured:
        raise ValueError("--root is required when STACK_REPO_ROOT is not configured")
    return Path(configured) / args.repo

def _generator_root(args: argparse.Namespace) -> Path:
    if args.generator_root is not None:
        return args.generator_root
    configured = os.environ.get("STACK_SKILL_LIB_ROOT", "").strip()
    if configured:
        return Path(configured)
    return Path(__file__).resolve().parents[2] / "skill-lib"

def _cmd_db_migrate(args: argparse.Namespace) -> int:
    ledger = _ledger(args)
    ledger.migrate()
    print("database schema ready")
    return 0

def _cmd_refresh(args: argparse.Namespace) -> int:
    ledger = _ledger(args)
    job = queue_refresh(
        ledger, repo=args.repo, root=_target_root(args), out=args.out,
        source_sha=args.source_sha, generator_root=_generator_root(args),
        executor=args.executor,
    )
    if args.queue_only:
        _print_job(job)
        return 0
    if job.state == "succeeded":
        _print_job(job)
        return 0
    if job.state in {"failed", "hmmm", "cancelled"}:
        job = ledger.retry(job.id)
    if job.state == "running":
        _print_job(job)
        return 0
    result = run_job(ledger, job.id)
    _print_job(result)
    return 0 if result.state == "succeeded" else 1

def _cmd_run(args: argparse.Namespace) -> int:
    result = run_job(_ledger(args), args.job_id)
    _print_job(result)
    return 0 if result.state == "succeeded" else 1

def _cmd_retry(args: argparse.Namespace) -> int:
    result = retry_job(_ledger(args), args.job_id)
    _print_job(result)
    return 0 if result.state == "succeeded" else 1

def _cmd_cancel(args: argparse.Namespace) -> int:
    result = _ledger(args).cancel(args.job_id)
    _print_job(result)
    return 0

def _cmd_status(args: argparse.Namespace) -> int:
    ledger = _ledger(args)
    if args.job_id:
        _print_job(ledger.get(args.job_id))
        return 0
    print(json.dumps([asdict(job) for job in ledger.list(limit=args.limit)], indent=2, sort_keys=True))
    return 0

def _cmd_explain(args: argparse.Namespace) -> int:
    job = _ledger(args).get(args.job_id)
    explanation = {
        "id": job.id, "state": job.state, "target": job.target,
        "source_sha": job.source_sha, "generator_identity": job.generator_identity,
        "attempts": job.attempts, "error": job.error, "hmmm": job.hmmm,
        "artifact_path": job.artifact_path, "artifact_sha256": job.artifact_sha256,
    }
    print(json.dumps(explanation, indent=2, sort_keys=True))
    return 0

def _cmd_worker_once(args: argparse.Namespace) -> int:
    did_work = run_once(_ledger(args), executor=args.executor, worker_id=args.worker_id)
    return 0 if did_work else 3

def _cmd_worker_run(args: argparse.Namespace) -> int:
    try:
        run_forever(_ledger(args), executor=args.executor, worker_id=args.worker_id)
    except KeyboardInterrupt:
        return 130
    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="stackctl")
    parser.add_argument("--database-url", help="PostgreSQL DSN; defaults to STACK_DATABASE_URL")
    parser.add_argument(
        "--receipt-dir", type=Path,
        help="JSON receipt directory; defaults to STACK_RECEIPT_DIR or .stack/state/receipts",
    )
    top = parser.add_subparsers(dest="domain", required=True)
    db = top.add_parser("db", help="PostgreSQL schema operations")
    db_actions = db.add_subparsers(dest="action", required=True)
    migrate = db_actions.add_parser("migrate", help="apply idempotent PostgreSQL schema")
    migrate.set_defaults(func=_cmd_db_migrate)

    msdmd = top.add_parser("msdmd", help="durable MSDMD regeneration")
    actions = msdmd.add_subparsers(dest="action", required=True)
    refresh = actions.add_parser("refresh", help="queue and run one repository refresh")
    refresh.add_argument("repo")
    refresh.add_argument("--root", type=Path, help="repository checkout; defaults to STACK_REPO_ROOT/<repo>")
    refresh.add_argument("--out", type=Path, help="artifact path; must remain at target repository root")
    refresh.add_argument("--source-sha", help="full source commit; resolved from git when omitted")
    refresh.add_argument(
        "--generator-root", type=Path,
        help="skill-lib root; defaults to STACK_SKILL_LIB_ROOT or stack/skill-lib",
    )
    refresh.add_argument("--executor", default="local", choices=("local",))
    refresh.add_argument("--queue-only", action="store_true")
    refresh.set_defaults(func=_cmd_refresh)
    run = actions.add_parser("run", help="execute one queued job")
    run.add_argument("job_id")
    run.set_defaults(func=_cmd_run)
    retry = actions.add_parser("retry", help="requeue and execute one failed/hmmm/cancelled job")
    retry.add_argument("job_id")
    retry.set_defaults(func=_cmd_retry)
    cancel = actions.add_parser("cancel", help="cancel a queued/failed/hmmm job")
    cancel.add_argument("job_id")
    cancel.set_defaults(func=_cmd_cancel)
    status = actions.add_parser("status", help="show durable job state")
    status.add_argument("job_id", nargs="?")
    status.add_argument("--limit", type=int, default=100)
    status.set_defaults(func=_cmd_status)
    explain = actions.add_parser("explain", help="show one job's evidence and unresolved boundary")
    explain.add_argument("job_id")
    explain.set_defaults(func=_cmd_explain)

    worker = top.add_parser("worker", help="VM worker loop")
    worker_actions = worker.add_subparsers(dest="action", required=True)
    once = worker_actions.add_parser("once", help="recover stale leases and execute at most one job")
    once.add_argument("--worker-id")
    once.add_argument("--executor", default="local", choices=("local",))
    once.set_defaults(func=_cmd_worker_once)
    forever = worker_actions.add_parser("run", help="poll PostgreSQL and execute queued jobs")
    forever.add_argument("--worker-id")
    forever.add_argument("--executor", default="local", choices=("local",))
    forever.set_defaults(func=_cmd_worker_run)
    return parser

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (KeyError, ValueError, FileNotFoundError, PermissionError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
