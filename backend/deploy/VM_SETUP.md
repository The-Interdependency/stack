# VM deployment checklist

This checklist begins with observation of the actual VM. Do not infer its
Linux distribution, PostgreSQL state, mount layout, service accounts, or
recovery path from this repository.

## Required observed facts

```text
OS/distribution: hmmm
PostgreSQL version/state: hmmm
stack checkout path: /srv/stack (intended; verify)
target checkout root: /srv/stack-repos (intended; verify)
independent backup mount/device: hmmm
human SSH/OS Login recovery path: hmmm
```

## Intended privilege boundary

```text
Unix service account: stackorchestrator
PostgreSQL role:      stackorchestrator
production database:  stack_orchestrator
restore-test database: stack_orchestrator_restore_test
```

Prefer local PostgreSQL Unix-socket/peer authentication. The worker does not
need a database password, root privileges, Docker socket access, cloud metadata
credentials, or a generic administrative shell.

The worker needs only:

```text
read:  /srv/stack
write: /srv/stack-repos/<allowed-repo>/<repo>_msdmd.ts
write: /var/lib/stack-orchestrator/receipts
write: PostgreSQL orchestration tables through the local socket
```

The repository allow-list is declared by `STACK_ALLOWED_REPOS`; production
execution requires a target to be the direct path
`$STACK_REPO_ROOT/<repo>`.

## Install application dependencies

After the VM and checkout paths have been observed:

```bash
cd /srv/stack
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r backend/requirements.txt
```

Install and edit the environment file:

```bash
sudo install -m 0600 backend/deploy/stack-orchestrator.env.example \
  /etc/stack-orchestrator.env
sudo editor /etc/stack-orchestrator.env
```

Create `/var/lib/stack-orchestrator/receipts` and
`/var/backups/stack-orchestrator/postgres` owned by the service account after
that account is created using the VM's native administration path.

## PostgreSQL

Provision the role and two databases using the VM's installed PostgreSQL
administration mechanism. Do not blindly paste distro-specific package/service
commands before confirming the VM.

Then, as the service account or another identity that exercises the same local
PostgreSQL authorization path:

```bash
set -a
. /etc/stack-orchestrator.env
set +a
/srv/stack/.venv/bin/python -m frontend.cli.stackctl db migrate
```

## Worker

```bash
sudo install -m 0644 backend/deploy/stack-orchestrator-worker.service \
  /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now stack-orchestrator-worker.service
sudo systemctl --no-pager --full status stack-orchestrator-worker.service
```

The service is non-root and `RestrictAddressFamilies=AF_UNIX`; its production
path does not require hosted CI or outbound network access.

## Independent backup

Mount independent storage at:

```text
/mnt/stack-orchestrator-backups
```

"Independent" means loss of the VM's primary/root/data filesystem does not also
lose this copy. `backup_postgres.sh` verifies that the mirror root is a real
mountpoint and that it has a different filesystem device id from the local
backup directory. A second directory on the same filesystem is rejected as
`hmmm`.

After the mount exists:

```bash
sudo mkdir -p /mnt/stack-orchestrator-backups/postgres
sudo chown -R stackorchestrator:stackorchestrator \
  /mnt/stack-orchestrator-backups/postgres
sudo chmod 0700 /mnt/stack-orchestrator-backups/postgres
```

Install and run one backup manually before enabling the timer:

```bash
sudo install -m 0644 backend/deploy/stack-orchestrator-backup.service \
  /etc/systemd/system/
sudo install -m 0644 backend/deploy/stack-orchestrator-backup.timer \
  /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start stack-orchestrator-backup.service
```

Then run a restore drill against the disposable restore-test database:

```bash
set -a
. /etc/stack-orchestrator.env
set +a
backend/ops/restore_test.sh
```

Only after both succeed:

```bash
sudo systemctl enable --now stack-orchestrator-backup.timer
systemctl list-timers stack-orchestrator-backup.timer
```

## Deployment acceptance

Deployment is not complete until all of these are observed on the VM:

```text
[ ] PostgreSQL version/state and local auth boundary observed
[ ] stackctl db migrate succeeds
[ ] worker runs as non-root stackorchestrator
[ ] one exact-SHA MSDMD job reaches succeeded with SQL + JSON receipt
[ ] wrong-SHA job reaches hmmm without replacing the artifact
[ ] dirty-worktree job reaches hmmm without replacing the artifact
[ ] expired lease is surfaced as hmmm and requeued
[ ] backup creates validated local + independent copies
[ ] backup mirror is a distinct mounted filesystem/device
[ ] restore drill succeeds against disposable database
[ ] human bootstrap/recovery path remains available
```

## hmmm

The VM is not directly reachable from this chat through a bounded VM control
connector, so its concrete distribution, PostgreSQL installation, storage
mount, service account state, and end-to-end deployment results remain
unobserved rather than guessed.
