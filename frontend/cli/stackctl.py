"""Operator CLI for stack fresh-making.

Examples:
    python -m frontend.cli.stackctl fresh make-msdmd ucns --root ../ucns
    python -m frontend.cli.stackctl fresh status msdmd:ucns
    python -m frontend.cli.stackctl fresh make msdmd:ucns
    python -m frontend.cli.stackctl fresh explain msdmd:ucns
    python -m frontend.cli.stackctl fresh jobs
    python -m frontend.cli.stackctl fresh recover
"""
from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_fresh_operator_cli
#   module_name: stackctl
#   module_kind: adapter
#   summary: exposes make, status, explain, retry, cancel, recover, jobs, and affected-closure operations for stack fresh-making
#   owner: stack
#   public_surface: python -m frontend.cli.stackctl fresh
#   storage_boundary: write
#   network_boundary: none
#   tests: backend.tests.test_orchestrator
#   rollout: explicit operator invocation
#   rollback: stop invoking the module
# === END MODULE_BUILD ===

import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys

from backend.freshness import SpecStore
from backend.jobs import Job, JobLedger
from backend.msdmd import build_spec, evaluate, make, retry_job, run_job


def _default_state_dir() -> Path:
    return Path(".stack/state")


def _state_dir(args: argparse.Namespace) -> Path:
    return Path(args.state_dir)


def _ledger(args: argparse.Namespace) -> JobLedger:
    return JobLedger(_state_dir(args) / "jobs.sqlite3")


def _store(args: argparse.Namespace) -> SpecStore:
    return SpecStore(_state_dir(args))


def _print(value) -> None:
    if isinstance(value, Job):
        value = asdict(value)
    print(json.dumps(value, indent=2, sort_keys=True))


def _cmd_make_msdmd(args: argparse.Namespace) -> int:
    stack_root = Path(__file__).resolve().parents[2]
    spec = build_spec(
        repo=args.repo,
        root=args.root,
        out=args.out,
        source_sha=args.source_sha,
        generator_root=args.generator_root or (stack_root / "skill-lib"),
    )
    store = _store(args)
    store.put(spec)
    if args.queue_only:
        from backend.msdmd import queue_make
        job, report = queue_make(_ledger(args), store, spec["target"], executor=args.executor)
        _print({"target": spec["target"], "job": asdict(job) if job else None, "freshness": report.to_dict()})
        return 0 if report.state != "hmmm" else 1
    job, report = make(
        _ledger(args), store, spec["target"], executor=args.executor, worker=args.worker
    )
    _print({"target": spec["target"], "job": asdict(job) if job else None, "freshness": report.to_dict()})
    return 0 if report.state == "fresh" else 1


def _cmd_make(args: argparse.Namespace) -> int:
    job, report = make(
        _ledger(args), _store(args), args.target,
        executor=args.executor, worker=args.worker,
    )
    _print({"target": args.target, "job": asdict(job) if job else None, "freshness": report.to_dict()})
    return 0 if report.state == "fresh" else 1


def _cmd_run(args: argparse.Namespace) -> int:
    result = run_job(
        _ledger(args), _store(args), args.job_id,
        worker=args.worker, executor=args.executor,
    )
    _print(result)
    return 0 if result.state == "succeeded" else 1


def _cmd_retry(args: argparse.Namespace) -> int:
    result = retry_job(
        _ledger(args), _store(args), args.job_id,
        executor=args.executor, worker=args.worker,
    )
    _print(result)
    return 0 if result.state == "succeeded" else 1


def _cmd_cancel(args: argparse.Namespace) -> int:
    _print(_ledger(args).cancel(args.job_id))
    return 0


def _cmd_status(args: argparse.Namespace) -> int:
    ledger = _ledger(args)
    store = _store(args)
    if args.target:
        _print(evaluate(ledger, store, args.target).to_dict())
        return 0
    reports = []
    for spec in store.list():
        reports.append(evaluate(ledger, store, spec["target"]).to_dict())
    _print(reports)
    return 0


def _cmd_explain(args: argparse.Namespace) -> int:
    ledger = _ledger(args)
    store = _store(args)
    report = evaluate(ledger, store, args.target)
    active = ledger.active_job_for_target(args.target)
    attempts = ledger.attempts_for(active.id) if active else []
    _print({
        "freshness": report.to_dict(),
        "active_job": asdict(active) if active else None,
        "active_attempts": [asdict(item) for item in attempts],
        "spec": store.get(args.target),
    })
    return 0


def _cmd_jobs(args: argparse.Namespace) -> int:
    ledger = _ledger(args)
    _print([asdict(job) for job in ledger.list(limit=args.limit, target=args.target)])
    return 0


def _cmd_recover(args: argparse.Namespace) -> int:
    recovered = _ledger(args).recover_expired_leases()
    _print([asdict(job) for job in recovered])
    return 0


def _cmd_affected(args: argparse.Namespace) -> int:
    _print(_store(args).affected_closure(args.changed_target))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="stackctl")
    parser.add_argument(
        "--state-dir", type=Path, default=_default_state_dir(),
        help="durable operational state directory (default: .stack/state)",
    )
    top = parser.add_subparsers(dest="domain", required=True)
    fresh = top.add_parser("fresh", help="deterministic fresh-making control plane")
    actions = fresh.add_subparsers(dest="action", required=True)

    make_msdmd = actions.add_parser("make-msdmd", help="register and make one repo MSDMD collection fresh")
    make_msdmd.add_argument("repo")
    make_msdmd.add_argument("--root", type=Path, required=True, help="explicit repository checkout")
    make_msdmd.add_argument("--out", type=Path, help="artifact path; defaults to <repo>_msdmd.ts in target root")
    make_msdmd.add_argument("--source-sha", help="full commit; required only when the root is not a git checkout")
    make_msdmd.add_argument("--generator-root", type=Path, help="skill-lib root containing msdmd/")
    make_msdmd.add_argument("--executor", default="local", choices=("local",))
    make_msdmd.add_argument("--worker", default="stackctl")
    make_msdmd.add_argument("--queue-only", action="store_true")
    make_msdmd.set_defaults(func=_cmd_make_msdmd)

    make_target = actions.add_parser("make", help="make a previously registered target fresh")
    make_target.add_argument("target")
    make_target.add_argument("--executor", default="local", choices=("local",))
    make_target.add_argument("--worker", default="stackctl")
    make_target.set_defaults(func=_cmd_make)

    run = actions.add_parser("run", help="execute one queued fresh-making job")
    run.add_argument("job_id")
    run.add_argument("--executor", default="local", choices=("local",))
    run.add_argument("--worker", default="stackctl")
    run.set_defaults(func=_cmd_run)

    retry = actions.add_parser("retry", help="retry one failed/cancelled/hmmm job")
    retry.add_argument("job_id")
    retry.add_argument("--executor", default="local", choices=("local",))
    retry.add_argument("--worker", default="stackctl")
    retry.set_defaults(func=_cmd_retry)

    cancel = actions.add_parser("cancel", help="cancel a non-terminal job")
    cancel.add_argument("job_id")
    cancel.set_defaults(func=_cmd_cancel)

    status = actions.add_parser("status", help="verify target freshness")
    status.add_argument("target", nargs="?")
    status.set_defaults(func=_cmd_status)

    explain = actions.add_parser("explain", help="show spec, freshness evidence, and active attempt")
    explain.add_argument("target")
    explain.set_defaults(func=_cmd_explain)

    jobs = actions.add_parser("jobs", help="show durable job history")
    jobs.add_argument("--target")
    jobs.add_argument("--limit", type=int, default=100)
    jobs.set_defaults(func=_cmd_jobs)

    recover = actions.add_parser("recover", help="recover expired leases back to queued")
    recover.set_defaults(func=_cmd_recover)

    affected = actions.add_parser("affected", help="compute minimal dependent closure from changed targets")
    affected.add_argument("changed_target", nargs="+")
    affected.set_defaults(func=_cmd_affected)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (KeyError, ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
