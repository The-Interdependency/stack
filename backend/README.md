# backend — durable fresh-making orchestration

`backend/` is the stack-level control plane for derived artifacts. It exists so
freshness remains inspectable and recoverable when a hosted executor such as GitHub
Actions is delayed, unavailable, or unreliable.

PostgreSQL on the VM is the **single production state authority**. SQLite is not a
production fallback. Repository canon and generated artifacts remain owned by their
repositories; PostgreSQL owns only derivation specifications, desired freshness,
logical jobs, attempts/leases, receipts, accepted freshness, dependency edges, and
visible `hmmm`.

MSDMD collection regeneration is the first derivation adapter.

## Contract

```text
exact current identities
  -> versioned derivation spec
  -> deterministic freshness key
  -> executor-independent logical job
  -> leased attempt (FOR UPDATE SKIP LOCKED)
  -> bounded executor candidate
  -> independent rerender verifier
  -> atomic filesystem publication
  -> PostgreSQL receipt + target acceptance
  -> replayable fresh / making-fresh / hmmm decision
```

`fresh != recent`. Timestamps and executor choice are audit metadata; they do not
enter the freshness key.

## Authority boundary

PostgreSQL owns orchestration/freshness evidence only:

- derivation specs and dependency edges;
- desired freshness keys;
- logical jobs;
- worker leases and immutable attempt history;
- verified receipts and target acceptance;
- unresolved `hmmm`.

Repositories continue to own source, canon, and generated artifacts. A successful
fresh-making receipt proves derivation consistency under its declared contract; it
does not transfer semantic, mathematical, empirical, measurement, or publication
standing.

JSON receipts under `STACK_RECEIPT_DIR` are projections for inspection/recovery.
`target_acceptance` in PostgreSQL is the acceptance authority.

## Runtime requirements

- Linux VM with systemd.
- PostgreSQL 14+.
- Python 3.11+ and `psycopg`.
- `git`.
- target checkouts directly under `STACK_REPO_ROOT`.
- a pinned skill-lib checkout at `STACK_SKILL_LIB_ROOT`.
- an independent mounted filesystem/device for the verified backup mirror.

Prefer local PostgreSQL Unix-socket/peer authentication. The worker should not need a
database password, root privileges, Docker socket access, cloud metadata credentials,
or outbound network access.

## Install

After observing the actual VM, follow [`deploy/VM_SETUP.md`](deploy/VM_SETUP.md).

```bash
cd /srv/stack
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r backend/requirements.txt

set -a
. /etc/stack-orchestrator.env
set +a
/srv/stack/.venv/bin/python -m frontend.cli.stackctl db migrate
```

## Fresh-making usage

Register current identities and make one repository's MSDMD collection fresh:

```bash
python -m frontend.cli.stackctl fresh make-msdmd ucns \
  --root /srv/stack-repos/ucns \
  --source-sha <40-hex-commit>
```

Inspect or repair a registered derivation:

```bash
python -m frontend.cli.stackctl fresh status msdmd:ucns
python -m frontend.cli.stackctl fresh explain msdmd:ucns
python -m frontend.cli.stackctl fresh make msdmd:ucns
python -m frontend.cli.stackctl fresh jobs --target msdmd:ucns
python -m frontend.cli.stackctl fresh recover
python -m frontend.cli.stackctl fresh affected msdmd:ucns
```

Queue for the persistent worker instead of executing immediately:

```bash
python -m frontend.cli.stackctl fresh make-msdmd ucns \
  --root /srv/stack-repos/ucns \
  --source-sha <40-hex-commit> \
  --queue-only

python -m frontend.cli.stackctl worker once
python -m frontend.cli.stackctl worker run
```

The old `stackctl msdmd ...` namespace is removed. MSDMD is an adapter under one
fresh-making architecture, not a parallel job system.

## Failure semantics

Fresh-making fails closed when exact evidence cannot support publication. Examples:

- source HEAD differs from the desired commit or changes during execution;
- the pinned MSDMD generator identity changes;
- unrelated worktree changes are present;
- target checkout violates `STACK_REPO_ROOT` / `STACK_ALLOWED_REPOS`;
- executor reports success but independent rerender differs;
- an expired worker lease is recovered;
- required identities or verifier evidence are unresolved.

An executor non-zero result is `failed`. An operator-resolvable evidence boundary is
`hmmm`. Neither can produce target acceptance.

Logical job identity is `kind + target + desired freshness key`. Executor selection is
attempt metadata, so a future GitHub Actions adapter may retry the same logical work
without becoming another state authority.

## Backups

`ops/backup_postgres.sh`:

1. runs custom-format `pg_dump`;
2. validates it with `pg_restore --list`;
3. records SHA-256;
4. retains a local recovery copy;
5. requires an independent mounted backup root;
6. refuses a same-filesystem mirror;
7. copies, re-hashes, and re-validates the independent copy;
8. applies retention windows.

If the independent mount is absent, the script leaves validated local recovery
material but exits non-zero with `hmmm`; that is not a complete backup.

Run one manual backup and one restore drill before enabling the timer:

```bash
backend/ops/restore_test.sh
```

The restore script refuses to restore into the production DSN.

## Verification

Pure/local checks:

```bash
python -W error::ResourceWarning -m unittest \
  backend.tests.test_orchestrator backend.tests.test_worker_postgres
python -m compileall -q backend frontend
bash -n backend/ops/backup_postgres.sh backend/ops/restore_test.sh
```

PostgreSQL integration checks run only against an explicitly disposable database:

```bash
STACK_TEST_DATABASE_URL='postgresql:///stack_orchestrator_test?host=/var/run/postgresql' \
  python -m unittest \
    backend.tests.test_orchestrator.PostgresIntegrationTests \
    backend.tests.test_worker_postgres.PostgresStaleLeaseTests
```

Skipped PostgreSQL tests are deployment gates, not passes.

## Provenance

`fresh-making-provenance.json` binds this runtime to exact `skill-lib` fresh-making
doctrine. The root `skill-lib/` snapshot remains older because refreshing it would
also import unrelated doctrine changes; the comparison records that the MSDMD
generator tree did not change across that gap.

## hmmm

- Actual VM distribution, PostgreSQL/auth state, service account, filesystem ownership,
  and end-to-end deployment remain unobserved until inspected on the VM.
- The independent backup device/remote-backed mount remains to be identified and
  verified.
- GitHub Actions executor adapter remains deliberately unimplemented; VM-local
  execution is the resilience baseline.
- Organization aggregate and website-projection derivation specs are not yet
  registered; the generic affected-closure logic is present.
- Automatic commit/PR materialization of regenerated collection points remains
  separate from freshness verification and acceptance.
- The complete root `skill-lib/` snapshot refresh remains a separate bounded change.
