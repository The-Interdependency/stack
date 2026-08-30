"""VM-local PostgreSQL worker for stack fresh-making jobs."""
from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_fresh_worker
#   module_name: fresh_worker
#   module_kind: worker
#   summary: recovers stale PostgreSQL leases, claims one fresh-making job, and dispatches the bounded local executor
#   owner: stack
#   public_surface: run_once, run_forever
#   auth_boundary: write
#   storage_boundary: write
#   network_boundary: internal
#   tests: backend.tests.test_worker_postgres
#   rollout: non-root systemd worker on the stack VM
#   rollback: stop and disable the worker service
# === END MODULE_BUILD ===

# === BOUNDARIES ===
# id: stack_fresh_worker_runtime_boundary
#   summary: coordinates PostgreSQL state and bounded filesystem/subprocess execution as a non-root VM service account
#   auth_boundary: write
#   storage_boundary: write
#   network_boundary: internal
#   user_data_boundary: none
#   admin_only: true
#   side_effects: database, filesystem, subprocess, job
#   owner: stack
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: stack_fresh_worker_recovers_stale_lease
#   given: a prior worker lease expired
#   then: recovery preserves the old attempt as hmmm before any new work is claimed
#   class: resilience
#
# id: stack_fresh_worker_claims_one_job
#   given: one worker iteration with eligible queued jobs
#   then: at most one logical job is claimed and dispatched by that iteration
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
    timeout = int(os.environ.get("STACK_COMMAND_TIMEOUT_SECONDS", "900"))
    if lease_seconds < timeout + 60:
        raise ValueError("STACK_LEASE_SECONDS must exceed one command timeout by at least 60 seconds")
    ledger.requeue_stale()
    job = ledger.claim_next(executor=executor, worker_id=worker_id, lease_seconds=lease_seconds)
    if job is None:
        return False
    run_job(
        ledger, job.id, worker_id=worker_id, executor=executor,
        lease_seconds=lease_seconds,
    )
    return True


def run_forever(ledger: JobLedger, *, executor: str = "local",
                worker_id: str | None = None) -> None:
    poll_seconds = float(os.environ.get("STACK_POLL_SECONDS", "5"))
    if poll_seconds <= 0:
        raise ValueError("STACK_POLL_SECONDS must be > 0")
    while True:
        if not run_once(ledger, executor=executor, worker_id=worker_id):
            time.sleep(poll_seconds)
