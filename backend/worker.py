"""VM-local durable worker for stack orchestration jobs.

Usage:
    python -m frontend.cli.stackctl worker once
    python -m frontend.cli.stackctl worker run
"""
from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_orchestration_worker
#   module_name: orchestration_worker
#   module_kind: worker
#   summary: claims PostgreSQL jobs with leases and executes the bounded local executor loop
#   owner: stack
#   public_surface: run_once, run_forever
#   internal_surface: stale lease recovery, SKIP LOCKED claims, polling
#   auth_boundary: write
#   storage_boundary: write
#   network_boundary: internal
#   user_data_boundary: none
#   admin_only: true
#   tests: backend.tests.test_orchestrator
#   rollout: stack-orchestrator-worker.service on VM
#   rollback: stop and disable the worker service
# === END MODULE_BUILD ===

# === BOUNDARIES ===
# id: stack_orchestration_worker_runtime
#   summary: coordinates database job state and bounded filesystem/subprocess work as a non-root VM service account
#   auth_boundary: write
#   storage_boundary: write
#   network_boundary: internal
#   user_data_boundary: none
#   admin_only: true
#   side_effects: job, database, filesystem, subprocess
#   owner: stack
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: stack_worker_recovers_stale_lease
#   given: a previous worker dies after claiming a job and its lease expires
#   then: the attempt is preserved as hmmm and the job returns to the queue before new work is claimed
#   class: resilience
#
# id: stack_worker_claims_one_job
#   given: one worker iteration with queued eligible jobs
#   then: at most one job is claimed and executed by that iteration
#   class: concurrency
# === END CONTRACTS ===

import os
import socket
import time

from .jobs import JobLedger
from .msdmd import run_job

def default_worker_id() -> str:
    return socket.gethostname()

def run_once(ledger: JobLedger, *, executor: str = "local",
             worker_id: str | None = None, lease_seconds: int | None = None) -> bool:
    worker_id = worker_id or default_worker_id()
    lease_seconds = lease_seconds or int(os.environ.get("STACK_LEASE_SECONDS", "1800"))
    command_timeout = int(os.environ.get("STACK_COMMAND_TIMEOUT_SECONDS", "900"))
    if lease_seconds < command_timeout + 60:
        raise ValueError("STACK_LEASE_SECONDS must exceed STACK_COMMAND_TIMEOUT_SECONDS by at least 60")
    ledger.requeue_stale()
    job = ledger.claim_next(executor=executor, worker_id=worker_id, lease_seconds=lease_seconds)
    if job is None:
        return False
    run_job(ledger, job.id, worker_id=worker_id)
    return True

def run_forever(ledger: JobLedger, *, executor: str = "local",
                worker_id: str | None = None) -> None:
    poll_seconds = float(os.environ.get("STACK_POLL_SECONDS", "5"))
    if poll_seconds <= 0:
        raise ValueError("STACK_POLL_SECONDS must be > 0")
    while True:
        if not run_once(ledger, executor=executor, worker_id=worker_id):
            time.sleep(poll_seconds)
