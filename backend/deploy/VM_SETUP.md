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

## Bounded agent contact

Before replacing repeated human SSH with model-side operations, establish the separate
read-only `vm-mcp` contact described in [`VM_CONTACT.md`](VM_CONTACT.md). The runtime
comes from an exact canonical `The-Interdependency/skill-lib` commit and must not take
ownership of `/srv/stack`, expose a public listener, inherit SSH keys, or start with a
writable shell.

Initial contact is observation-only. Keep human SSH/OS Login/IAP as bootstrap and
break-glass access. A later write surface must be a named, reviewed stack operation,
not a generic privileged shell.

## Intended privilege boundary

```text
Unix service account:  stackorchestrator
PostgreSQL role:       stackorchestrator
production database:   stack_orchestrator
restore-test database: stack_orchestrator_restore_test
```

Prefer local PostgreSQL Unix-socket/peer authentication. The worker does not need a
database password, root privileges, Docker socket access, cloud metadata credentials,
or a generic administrative shell.

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

sudo install -m 0600 backend/deploy/stack-orchestrator.env.example \
  /etc/stack-orchestrator.env
sudo editor /etc/stack-orchestrator.env
```

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

Register and queue an exact MSDMD derivation:

```bash
/srv/stack/.venv/bin/python -m frontend.cli.stackctl fresh make-msdmd ucns \
  --root /srv/stack-repos/ucns \
  --source-sha <40-hex-commit> \
  --queue-only
```

Then observe the worker and verify accepted freshness:

```bash
/srv/stack/.venv/bin/python -m frontend.cli.stackctl worker once
/srv/stack/.venv/bin/python -m frontend.cli.stackctl fresh status msdmd:ucns
/srv/stack/.venv/bin/python -m frontend.cli.stackctl fresh explain msdmd:ucns
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
[ ] human bootstrap/recovery path remains available
[ ] read-only vm-mcp contact is loopback/private-tunnel only, non-root, shell disabled
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
account state, and end-to-end deployment results remain unobserved here. PostgreSQL
integration tests and backup/restore acceptance therefore remain live VM gates rather
than being represented as passed. `VM_CONTACT.md` defines the bounded path for turning
those unknowns into observable evidence without exporting SSH credentials to the model.
