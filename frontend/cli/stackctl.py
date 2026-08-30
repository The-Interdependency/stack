"""Operator CLI for PostgreSQL-backed stack fresh-making."""
from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_fresh_operator_cli
#   module_name: stackctl
#   module_kind: adapter
#   summary: exposes PostgreSQL migration, fresh-making status/make/retry/recover/affected operations, and VM worker control
#   owner: stack
#   public_surface: python -m frontend.cli.stackctl
#   auth_boundary: write
#   storage_boundary: write
#   network_boundary: internal
#   tests: backend.tests.test_orchestrator, backend.tests.test_worker_postgres
#   rollout: explicit operator invocation and systemd worker entrypoint
#   rollback: stop invoking the CLI; PostgreSQL records remain inspectable
# === END MODULE_BUILD ===

# === BOUNDARIES ===
# id: stack_fresh_operator_cli_boundary
#   summary: operator commands may mutate orchestration state and, for make operations, bounded generated artifacts through backend adapters
#   auth_boundary: write
#   storage_boundary: write
#   network_boundary: internal
#   user_data_boundary: none
#   admin_only: true
#   side_effects: database, filesystem, subprocess, job
#   owner: stack
# === END BOUNDARIES ===

import argparse
from dataclasses import asdict
import json
import os
from pathlib import Path
import sys

from backend.freshness import base_report
from backend.jobs import JobLedger
from backend import msdmd
from backend.worker import run_forever, run_once


def _database_url(args: argparse.Namespace) -> str:
    value = args.database_url or os.environ.get("STACK_DATABASE_URL", "")
    if not value:
        raise ValueError("STACK_DATABASE_URL or --database-url is required")
    return value


def _ledger(args: argparse.Namespace) -> JobLedger:
    receipt_dir = args.receipt_dir or os.environ.get("STACK_RECEIPT_DIR")
    return JobLedger(_database_url(args), receipt_dir=receipt_dir)


def _print(value) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=str))


def _evaluate(ledger: JobLedger, target: str):
    spec = ledger.get_derivation(target)
    if spec.get("kind") == "msdmd.collection":
        return msdmd.evaluate(ledger, target)
    return base_report(ledger, spec)


def _make(ledger: JobLedger, target: str, *, executor: str, worker_id: str):
    spec = ledger.get_derivation(target)
    if spec.get("kind") == "msdmd.collection":
        return msdmd.make(ledger, target, executor=executor, worker_id=worker_id)
    raise ValueError(f"no make adapter registered for derivation kind: {spec.get('kind')}")


def cmd_db_migrate(args):
    _ledger(args).migrate()
    print("PostgreSQL fresh-making schema: migrated")
    return 0


def cmd_make_msdmd(args):
    ledger = _ledger(args)
    stack_root = Path(__file__).resolve().parents[2]
    spec = msdmd.build_spec(
        repo=args.repo, root=args.root, out=args.out, source_sha=args.source_sha,
        generator_root=args.generator_root or (stack_root / "skill-lib"),
    )
    msdmd.register_spec(ledger, spec)
    if args.queue_only:
        job, report = msdmd.queue_make(ledger, spec["target"], executor=args.executor)
    else:
        job, report = msdmd.make(
            ledger, spec["target"], executor=args.executor, worker_id=args.worker_id,
        )
    _print({"target": spec["target"], "job": asdict(job) if job else None, "freshness": report.to_dict()})
    return 0 if report.state in {"fresh", "making-fresh"} else 1


def cmd_make(args):
    ledger = _ledger(args)
    job, report = _make(ledger, args.target, executor=args.executor, worker_id=args.worker_id)
    _print({"target": args.target, "job": asdict(job) if job else None, "freshness": report.to_dict()})
    return 0 if report.state == "fresh" else 1


def cmd_status(args):
    ledger = _ledger(args)
    if args.target:
        _print(_evaluate(ledger, args.target).to_dict())
        return 0
    reports = [_evaluate(ledger, spec["target"]).to_dict() for spec in ledger.list_derivations()]
    _print(reports)
    return 0


def cmd_explain(args):
    ledger = _ledger(args)
    jobs = ledger.list(limit=10, target=args.target)
    active = ledger.active_job_for_target(args.target)
    _print({
        "spec": ledger.get_derivation(args.target),
        "freshness": _evaluate(ledger, args.target).to_dict(),
        "active_job": asdict(active) if active else None,
        "recent_jobs": [asdict(job) for job in jobs],
        "active_attempts": [asdict(a) for a in ledger.attempts_for(active.id)] if active else [],
    })
    return 0


def cmd_run(args):
    ledger = _ledger(args)
    job = ledger.get(args.job_id)
    if job.kind != "fresh.make":
        raise ValueError(f"unsupported job kind: {job.kind}")
    spec = ledger.get_derivation(job.target)
    if spec.get("kind") != "msdmd.collection":
        raise ValueError(f"no executor adapter for {spec.get('kind')}")
    result = msdmd.run_job(
        ledger, job.id, worker_id=args.worker_id, executor=args.executor,
        lease_seconds=args.lease_seconds,
    )
    _print(asdict(result))
    return 0 if result.state == "succeeded" else 1


def cmd_retry(args):
    ledger = _ledger(args)
    job = ledger.get(args.job_id)
    spec = ledger.get_derivation(job.target)
    if spec.get("kind") != "msdmd.collection":
        raise ValueError(f"no retry adapter for {spec.get('kind')}")
    result = msdmd.retry_job(ledger, job.id, executor=args.executor, worker_id=args.worker_id)
    _print(asdict(result))
    return 0 if result.state == "succeeded" else 1


def cmd_cancel(args):
    _print(asdict(_ledger(args).cancel(args.job_id)))
    return 0


def cmd_jobs(args):
    ledger = _ledger(args)
    _print([asdict(j) for j in ledger.list(limit=args.limit, target=args.target)])
    return 0


def cmd_recover(args):
    count = _ledger(args).requeue_stale()
    _print({"recovered": count})
    return 0


def cmd_affected(args):
    ledger = _ledger(args)
    _print(msdmd.registered_affected_closure(ledger, args.changed_target))
    return 0


def cmd_worker_once(args):
    worked = run_once(
        _ledger(args), executor=args.executor, worker_id=args.worker_id,
        lease_seconds=args.lease_seconds,
    )
    return 0 if worked else 3


def cmd_worker_run(args):
    run_forever(_ledger(args), executor=args.executor, worker_id=args.worker_id)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="stackctl")
    parser.add_argument("--database-url", help="PostgreSQL DSN; defaults to STACK_DATABASE_URL")
    parser.add_argument("--receipt-dir", type=Path, help="JSON receipt projection directory")
    top = parser.add_subparsers(dest="domain", required=True)

    db = top.add_parser("db")
    db_actions = db.add_subparsers(dest="action", required=True)
    migrate = db_actions.add_parser("migrate")
    migrate.set_defaults(func=cmd_db_migrate)

    fresh = top.add_parser("fresh", help="deterministic derived-artifact restoration")
    actions = fresh.add_subparsers(dest="action", required=True)

    mm = actions.add_parser("make-msdmd", help="register and make a repo MSDMD collection fresh")
    mm.add_argument("repo")
    mm.add_argument("--root", type=Path, required=True)
    mm.add_argument("--out", type=Path)
    mm.add_argument("--source-sha")
    mm.add_argument("--generator-root", type=Path)
    mm.add_argument("--executor", default="local", choices=("local",))
    mm.add_argument("--worker-id", default="stackctl")
    mm.add_argument("--queue-only", action="store_true")
    mm.set_defaults(func=cmd_make_msdmd)

    make = actions.add_parser("make")
    make.add_argument("target")
    make.add_argument("--executor", default="local", choices=("local",))
    make.add_argument("--worker-id", default="stackctl")
    make.set_defaults(func=cmd_make)

    status = actions.add_parser("status")
    status.add_argument("target", nargs="?")
    status.set_defaults(func=cmd_status)
    explain = actions.add_parser("explain")
    explain.add_argument("target")
    explain.set_defaults(func=cmd_explain)

    run = actions.add_parser("run")
    run.add_argument("job_id")
    run.add_argument("--executor", default="local", choices=("local",))
    run.add_argument("--worker-id", default="stackctl")
    run.add_argument("--lease-seconds", type=int)
    run.set_defaults(func=cmd_run)

    retry = actions.add_parser("retry")
    retry.add_argument("job_id")
    retry.add_argument("--executor", default="local", choices=("local",))
    retry.add_argument("--worker-id", default="stackctl")
    retry.set_defaults(func=cmd_retry)
    cancel = actions.add_parser("cancel")
    cancel.add_argument("job_id")
    cancel.set_defaults(func=cmd_cancel)

    jobs = actions.add_parser("jobs")
    jobs.add_argument("--target")
    jobs.add_argument("--limit", type=int, default=100)
    jobs.set_defaults(func=cmd_jobs)
    recover = actions.add_parser("recover")
    recover.set_defaults(func=cmd_recover)
    affected = actions.add_parser("affected")
    affected.add_argument("changed_target", nargs="+")
    affected.set_defaults(func=cmd_affected)

    worker = top.add_parser("worker")
    wa = worker.add_subparsers(dest="action", required=True)
    once = wa.add_parser("once")
    once.add_argument("--executor", default="local", choices=("local",))
    once.add_argument("--worker-id")
    once.add_argument("--lease-seconds", type=int)
    once.set_defaults(func=cmd_worker_once)
    forever = wa.add_parser("run")
    forever.add_argument("--executor", default="local", choices=("local",))
    forever.add_argument("--worker-id")
    forever.set_defaults(func=cmd_worker_run)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except (KeyError, ValueError, FileNotFoundError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
