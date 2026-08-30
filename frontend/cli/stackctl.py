"""Operator CLI for stack orchestration.

Usage:
    python -m frontend.cli.stackctl msdmd refresh ucns --root ../ucns
    python -m frontend.cli.stackctl msdmd status
    python -m frontend.cli.stackctl msdmd explain <job-id>
    python -m frontend.cli.stackctl msdmd retry <job-id>
"""
from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_operator_cli
#   module_name: stackctl
#   module_kind: adapter
#   summary: exposes durable stack orchestration state and bounded MSDMD regeneration controls to a human operator
#   owner: stack
#   public_surface: python -m frontend.cli.stackctl
#   internal_surface: argparse command dispatch, JobLedger, backend.msdmd
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: backend.tests.test_orchestrator
#   rollout: explicit operator invocation only
#   rollback: stop invoking the module
#   unresolved: stable console-script package name
# === END MODULE_BUILD ===

# === BOUNDARIES ===
# id: stack_operator_cli_orchestration
#   summary: permits an operator to create, execute, inspect, cancel, and retry local orchestration jobs
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   side_effects: job, filesystem, subprocess
#   owner: stack
# === END BOUNDARIES ===

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

from backend.jobs import Job, JobLedger
from backend.msdmd import queue_refresh, retry_job, run_job


def _default_state_db() -> Path:
    return Path(".stack/state/jobs.sqlite3")


def _print_job(job: Job) -> None:
    print(json.dumps(asdict(job), indent=2, sort_keys=True))


def _ledger(args: argparse.Namespace) -> JobLedger:
    return JobLedger(args.db)


def _cmd_refresh(args: argparse.Namespace) -> int:
    ledger = _ledger(args)
    stack_root = Path(__file__).resolve().parents[2]
    job = queue_refresh(
        ledger,
        repo=args.repo,
        root=args.root,
        out=args.out,
        source_sha=args.source_sha,
        generator_root=args.generator_root or (stack_root / "skill-lib"),
        executor=args.executor,
    )
    if args.queue_only:
        _print_job(job)
        return 0
    if job.state == "succeeded":
        _print_job(job)
        return 0
    if job.state in {"failed", "cancelled"}:
        job = ledger.retry(job.id)
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
        "id": job.id,
        "state": job.state,
        "target": job.target,
        "source_sha": job.source_sha,
        "generator_identity": job.generator_identity,
        "attempts": job.attempts,
        "error": job.error,
        "hmmm": job.hmmm,
        "artifact_path": job.artifact_path,
        "artifact_sha256": job.artifact_sha256,
    }
    print(json.dumps(explanation, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="stackctl")
    parser.add_argument(
        "--db", type=Path, default=_default_state_db(),
        help="SQLite job ledger (default: .stack/state/jobs.sqlite3)",
    )
    top = parser.add_subparsers(dest="domain", required=True)
    msdmd = top.add_parser("msdmd", help="durable MSDMD regeneration")
    actions = msdmd.add_subparsers(dest="action", required=True)

    refresh = actions.add_parser("refresh", help="queue and run one repository refresh")
    refresh.add_argument("repo")
    refresh.add_argument("--root", type=Path, required=True, help="explicit repository checkout")
    refresh.add_argument("--out", type=Path, help="artifact path; defaults to <repo>_msdmd.ts in target root")
    refresh.add_argument("--source-sha", help="full source commit; resolved from git when omitted")
    refresh.add_argument("--generator-root", type=Path, help="skill-lib root containing msdmd/collect.py")
    refresh.add_argument("--executor", default="local", choices=("local",))
    refresh.add_argument("--queue-only", action="store_true")
    refresh.set_defaults(func=_cmd_refresh)

    run = actions.add_parser("run", help="execute one queued job")
    run.add_argument("job_id")
    run.set_defaults(func=_cmd_run)

    retry = actions.add_parser("retry", help="requeue and execute one failed/cancelled job")
    retry.add_argument("job_id")
    retry.set_defaults(func=_cmd_retry)

    cancel = actions.add_parser("cancel", help="cancel a queued or failed job")
    cancel.add_argument("job_id")
    cancel.set_defaults(func=_cmd_cancel)

    status = actions.add_parser("status", help="show durable job state")
    status.add_argument("job_id", nargs="?")
    status.add_argument("--limit", type=int, default=100)
    status.set_defaults(func=_cmd_status)

    explain = actions.add_parser("explain", help="show one job's evidence and unresolved boundary")
    explain.add_argument("job_id")
    explain.set_defaults(func=_cmd_explain)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (KeyError, ValueError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
