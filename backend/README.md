# backend — durable stack orchestration

`backend/` is the stack-level orchestration plane. It exists because repository
automation must remain inspectable and recoverable when a hosted executor such
as GitHub Actions is delayed, unavailable, or unreliable.

The first vertical slice is MSDMD regeneration.

```text
request
  -> PostgreSQL job on the VM
  -> exact source + generator identities
  -> leased worker attempt
  -> bounded repo-local generation
  -> source/generator re-verification
  -> atomic artifact replacement
  -> PostgreSQL + JSON SHA-256 receipt
  -> explicit retry / hmmm
```

GitHub Actions is not the job database and is not required by this slice. The
implemented executor is the VM-local worker; a future GitHub-hosted adapter may
claim the same durable contract without becoming the state owner.

## Authority boundary

PostgreSQL owns orchestration state only:

- requested jobs and idempotent identities;
- worker leases and attempts;
- receipts;
- dependency ordering;
- unresolved `hmmm`.

Repositories continue to own their source, canon, and generated artifacts. The
worker coordinates one target at an exact commit using an exact skill-lib
collector digest; it acquires no semantic authority from that access.

## Runtime requirements

- Linux VM with systemd.
- PostgreSQL 14+.
- Python 3.11+.
- `git`.
- target checkouts directly under `STACK_REPO_ROOT`.
- a pinned skill-lib checkout at `STACK_SKILL_LIB_ROOT`.
- an independent mounted filesystem/device for the verified backup mirror.

The production worker is intended to use local PostgreSQL Unix-socket/peer
authentication and no outbound network access.

## Install

After observing the actual VM, follow [`deploy/VM_SETUP.md`](deploy/VM_SETUP.md).
The application portion is:

```bash
cd /srv/stack
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r backend/requirements.txt
```

Configure `/etc/stack-orchestrator.env` from
`deploy/stack-orchestrator.env.example`. Keep it mode `0600`.

Initialize PostgreSQL:

```bash
set -a
. /etc/stack-orchestrator.env
set +a
/srv/stack/.venv/bin/python -m frontend.cli.stackctl db migrate
```

`SQLite` is no longer a production fallback. One VM PostgreSQL service owns the
orchestration state so leases, concurrent claims, retries, and recovery have one
transactional boundary.

## MSDMD usage

Moving branch names are not execution identities. A queued job records the full
source commit plus SHA-256 of `msdmd/collect.py`.

```bash
python -m frontend.cli.stackctl msdmd refresh ucns \
  --root /srv/stack-repos/ucns \
  --source-sha <40-hex-commit>

python -m frontend.cli.stackctl msdmd status
python -m frontend.cli.stackctl msdmd explain <job-id>
python -m frontend.cli.stackctl msdmd retry <job-id>
```

Queue without running immediately:

```bash
python -m frontend.cli.stackctl msdmd refresh ucns \
  --root /srv/stack-repos/ucns \
  --source-sha <40-hex-commit> \
  --queue-only
```

The persistent worker claims queued jobs with `FOR UPDATE SKIP LOCKED` and a
lease:

```bash
python -m frontend.cli.stackctl worker once
python -m frontend.cli.stackctl worker run
```

A regeneration becomes `hmmm`, not guessed-through success, when the worker
finds an operator-resolvable boundary such as:

- target HEAD differs from the requested commit;
- target HEAD changes during generation;
- skill-lib collector digest differs from the queued identity;
- unrelated worktree changes are present;
- target is outside `STACK_REPO_ROOT` / `STACK_ALLOWED_REPOS`;
- an expired worker lease is recovered.

A collector non-zero exit is `failed`. Successful output is written to a temp
file, re-verified, hashed, and atomically replaced at the repository root.

## Backups

`ops/backup_postgres.sh`:

1. runs custom-format `pg_dump`;
2. validates the dump with `pg_restore --list`;
3. records SHA-256;
4. retains a local recovery copy;
5. requires an independent mounted backup root;
6. refuses a same-filesystem mirror;
7. copies, re-hashes, and re-validates the independent copy;
8. applies local and mirror retention windows.

If the independent mount is absent, the script leaves the validated local dump
in place but exits non-zero with `hmmm`; that is recovery material, not a
complete backup.

The systemd timer runs daily with a randomized delay. Install it only after one
manual backup and one restore drill succeed.

Restore drill:

```bash
set -a
. /etc/stack-orchestrator.env
set +a
backend/ops/restore_test.sh
```

The script refuses to restore into the production DSN.

## Tests

Local unit tests require no PostgreSQL installation:

```bash
python -m unittest backend.tests.test_orchestrator
```

A PostgreSQL integration test is enabled only when a disposable database is
explicitly supplied:

```bash
STACK_TEST_DATABASE_URL='postgresql:///stack_orchestrator_test?host=/var/run/postgresql' \
  python -m unittest backend.tests.test_orchestrator.PostgresIntegrationTests
```

Shell syntax:

```bash
bash -n backend/ops/backup_postgres.sh backend/ops/restore_test.sh
```

## hmmm

- The actual VM distribution, PostgreSQL state, service account, and filesystem
  ownership are not observable from this chat and must be inspected before
  installation.
- The independent backup device/remote-backed mount is not yet identified from
  this environment.
- GitHub Actions executor adapter remains deliberately unimplemented; VM-local
  execution is the resilience baseline.
- Organization-level affected-repository discovery and automatic dependency
  scheduling are represented as a next layer, not silently inferred.
- Automatic commit/PR materialization of regenerated collection points remains
  separate from regeneration and receipt verification.
