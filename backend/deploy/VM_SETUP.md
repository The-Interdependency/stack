# VM deployment checklist

This checklist begins with observation of the actual VM. Do not infer its Linux
distribution, PostgreSQL state, mount layout, service accounts, or recovery path from
this repository.

## Required observed facts

```text
OS/distribution: hmmm
PostgreSQL version/state: hmmm
stack checkout path: /srv/stack (intended; verify)
target checkout root: /srv/stack-repos (intended; verify)
independent backup mount/device: hmmm
human SSH/OS Login recovery path: hmmm
```

## Personal agent contact

Before replacing repeated human SSH with model-side operations, establish the private
single-owner `vm-mcp` personal console described in [`VM_CONTACT.md`](VM_CONTACT.md).
The runtime comes from an exact canonical `The-Interdependency/skill-lib` commit and
keeps credentials outside model context.

The authority split is deliberate:

```text
shell_exec -> confined non-root vmmcp
user_exec  -> explicit requested non-root account
admin_exec -> explicit root through separate AF_UNIX broker
```

The MCP HTTP service remains loopback-only and non-root even when the personal-console
root broker is enabled. Keep human SSH/OS Login/IAP as independent bootstrap and
break-glass access. Do not publish port `8765` or hide root execution behind an
apparently non-privileged tool.

## Intended stack-orchestrator privilege boundary

```text
Unix service account:  stackorchestrator
PostgreSQL role:       stackorchestrator
production database:   stack_orchestrator
restore-test database: stack_orchestrator_restore_test
```

Prefer local PostgreSQL Unix-socket/peer authentication. The worker itself does not need
a database password, root privileges, Docker socket access, or cloud metadata
credentials. Host administration remains a separate personal-console operation rather
than being granted to the worker service.

The worker needs only:

```text
read:  /srv/stack
write: /srv/stack-repos/<allowed-repo>/<repo>_msdmd.ts
write: /var/lib/stack-orchestrator/receipts
write: PostgreSQL fresh-making tables through the local socket
```

The repository allow-list is declared by `STACK_ALLOWED_REPOS`; production execution
requires a target to be the direct path `$STACK_REPO_ROOT/<repo>`.

## Install application dependencies

```bash
cd /srv/stack
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r backend/requirements.txt
# MSDMD native reader runtimes for the default STACK_SKILL_LIB_ROOT (/srv/stack/skill-lib);
# backend/ops/install_msdmd_runtime.sh below does the same for a configured root.
.venv/bin/pip install -r skill-lib/msdmd/requirements.txt
npm ci --ignore-scripts --prefix skill-lib/msdmd

sudo install -m 0600 backend/deploy/stack-orchestrator.env.example \
  /etc/stack-orchestrator.env
sudo editor /etc/stack-orchestrator.env
```

### MSDMD native reader runtimes

The skill-lib collector at `STACK_SKILL_LIB_ROOT` needs its pinned Python reader
packages in the worker venv and its TypeScript compiler installed beside the
worker script. Without them the collector exits 3 and fresh-making fails closed.
Run this as root after every skill-lib snapshot refresh, before restarting the
worker (Node and npm must already be installed; Node version on the VM: hmmm):

```bash
set -a
. /etc/stack-orchestrator.env
set +a
sudo -E env STACK_VENV=/srv/stack/.venv backend/ops/install_msdmd_runtime.sh
```

The script sets `umask 022` so the worker user (`STACK_WORKER_USER`, default
`stackorchestrator`, which must exist) can read what it installs, runs
`pip install -r $STACK_SKILL_LIB_ROOT/msdmd/requirements.txt` into the venv and
`npm ci --ignore-scripts --prefix $STACK_SKILL_LIB_ROOT/msdmd`, then probes
`python -P -m msdmd.collect --print-generator-identity --json` twice: in the
calling shell, and inside the worker unit's sandbox through
`backend/ops/worker_sandbox_run.sh` (systemd-run with the unit's `User`,
`EnvironmentFile` and sandbox properties, including `MemoryDenyWriteExecute`,
read with `systemctl show` from the installed unit, drop-ins included). Install
the unit file and run `systemctl daemon-reload` first (see Worker below; enabling
it can wait). The wrapper refuses to run (exit 2) unless the unit is loaded,
runs as `STACK_WORKER_USER` and has `MemoryDenyWriteExecute=yes`.
It fails (exit 3) if either probe fails or reports `node` or `typescript` as
`absent`, and exits 4 if the sandboxed probe cannot run (not root, or no
systemd-run). The sandboxed identity is the one the worker records, so a
runtime upgrade re-keys every MSDMD derivation. pip hash-checking is not used
(hmmm: skill-lib publishes pinned versions without hashes).

Targets that still vendor the schema-1 `.agents/skills/msdmd/collection.ts` helper
make the collector exit 4 (helper older than the schema-2 output). Those targets
need a skill-lib propagation before they can be made fresh. A target where git is
missing from the worker's PATH, or whose root an enclosing repository ignores,
makes it exit 5. The worker records each refusal as a failed attempt with an
operator action rather than writing an artifact.

`stack-orchestrator-worker.service` keeps `MemoryDenyWriteExecute=true`. V8's
JIT cannot run under it: Node dies with a V8 fatal error (SIGTRAP). The pinned
skill-lib snapshot (`1b1a947`, after The-Interdependency/skill-lib#120) runs
Node with `--jitless`, so the sandboxed probe and TypeScript extraction work
under MDWE. `node` must also be on the unit's default PATH.

Create `/var/lib/stack-orchestrator/receipts` and
`/var/backups/stack-orchestrator/postgres` owned by the service account after that
account is created using the VM's native administration path.

## PostgreSQL

Provision the role and two databases using the VM's installed PostgreSQL administration
mechanism. Do not blindly paste distro-specific package/service commands before
confirming the VM.

Then exercise the same local authorization path the worker will use:

```bash
set -a
. /etc/stack-orchestrator.env
set +a
/srv/stack/.venv/bin/python -m frontend.cli.stackctl db migrate
```

PostgreSQL is the single production authority for derivation specs, freshness keys,
logical jobs, attempts/leases, receipts, target acceptance, dependencies, and `hmmm`.
There is no SQLite production fallback.

## Worker

```bash
sudo install -m 0644 backend/deploy/stack-orchestrator-worker.service \
  /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now stack-orchestrator-worker.service
sudo systemctl --no-pager --full status stack-orchestrator-worker.service
```

The service is non-root and `RestrictAddressFamilies=AF_UNIX`; its production path does
not require hosted CI or outbound network access.

## First fresh-making vertical slice

Register and queue an exact MSDMD derivation. Queueing from the operator shell
never probes the generator identity (that shell's PATH, Node or venv may differ
from the worker's); the derivation is recorded as `worker-pending`, or keeps the
identity a worker already recorded:

```bash
/srv/stack/.venv/bin/python -m frontend.cli.stackctl fresh make-msdmd ucns \
  --root /srv/stack-repos/ucns \
  --source-sha <40-hex-commit> \
  --queue-only
```

The worker observes its own identity, records it with its components, and
supersedes a `worker-pending` job once under the observed key. With the service
running this happens on its own; by hand, the first `worker once` reports the
`superseded` job and the second makes the target fresh. Run `worker once` in the
worker's environment, not the operator shell:

```bash
sudo backend/ops/worker_sandbox_run.sh -- /srv/stack/.venv/bin/python -m frontend.cli.stackctl worker once
sudo backend/ops/worker_sandbox_run.sh -- /srv/stack/.venv/bin/python -m frontend.cli.stackctl worker once
```

Then verify accepted freshness. `status` and `explain` never re-key the
derivation, but their independent rerender compares the generator identity
where they run, so use the same wrapper; from a different shell they report
`verifier-unavailable` with the components that differ:

```bash
sudo backend/ops/worker_sandbox_run.sh -- /srv/stack/.venv/bin/python -m frontend.cli.stackctl fresh status msdmd:ucns
sudo backend/ops/worker_sandbox_run.sh -- /srv/stack/.venv/bin/python -m frontend.cli.stackctl fresh explain msdmd:ucns
```

## Independent backup

Mount independent storage at:

```text
/mnt/stack-orchestrator-backups
```

"Independent" means loss of the VM's primary/root/data filesystem does not also lose
this copy. `backup_postgres.sh` verifies that the mirror root is a real mountpoint and
has a different filesystem device id from the local backup directory. A second
directory on the same filesystem is rejected as `hmmm`.

```bash
sudo mkdir -p /mnt/stack-orchestrator-backups/postgres
sudo chown -R stackorchestrator:stackorchestrator \
  /mnt/stack-orchestrator-backups/postgres
sudo chmod 0700 /mnt/stack-orchestrator-backups/postgres

sudo install -m 0644 backend/deploy/stack-orchestrator-backup.service \
  /etc/systemd/system/
sudo install -m 0644 backend/deploy/stack-orchestrator-backup.timer \
  /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start stack-orchestrator-backup.service
```

Run a restore drill against the disposable restore-test database:

```bash
set -a
. /etc/stack-orchestrator.env
set +a
backend/ops/restore_test.sh
```

Only after backup and restore both succeed:

```bash
sudo systemctl enable --now stack-orchestrator-backup.timer
systemctl list-timers stack-orchestrator-backup.timer
```

## Deployment acceptance

Deployment is not complete until all of these are observed on the VM:

```text
[ ] human bootstrap/recovery path remains independently available
[ ] vm-mcp service is non-root and listens only on 127.0.0.1:8765
[ ] vm-mcp personal-console profile is active
[ ] root broker is AF_UNIX-only with root:vmmcp 0660 socket
[ ] shell_exec proves non-root vmmcp identity
[ ] user_exec proves requested non-root identity (including stackorchestrator)
[ ] admin_exec proves uid 0 and journald audit evidence
[ ] PostgreSQL version/state and local auth boundary observed
[ ] stackctl db migrate succeeds
[ ] worker runs as non-root stackorchestrator
[ ] exact-SHA msdmd:ucns reaches fresh with SQL target_acceptance + JSON projection
[ ] a second make with unchanged identities schedules no new attempt
[ ] wrong/moved source identity cannot produce target acceptance
[ ] changed generator identity invalidates the desired freshness key
[ ] dirty worktree becomes hmmm without claiming repository authority
[ ] false-green/nondeterministic executor output is rejected by independent rerender
[ ] expired lease is preserved as hmmm and the logical job is requeued
[ ] same-key tamper repair creates a later attempt without deleting prior evidence
[ ] backup creates validated local + independent copies
[ ] backup mirror is a distinct mounted filesystem/device
[ ] restore drill succeeds against disposable database
```

## hmmm

The concrete VM distribution, PostgreSQL installation/auth state, storage mount, service
account state, MCP private transport, and end-to-end deployment results remain
unobserved here. PostgreSQL integration tests, personal-console host acceptance, and
backup/restore acceptance therefore remain live VM gates rather than being represented
as passed. `VM_CONTACT.md` defines the path for turning those unknowns into observable
evidence without exporting SSH credentials to the model.
