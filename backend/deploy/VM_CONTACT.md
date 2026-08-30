# VM agent contact bootstrap

This is the one-time bridge from human SSH/OS Login bootstrap to bounded agent contact.
The VM control plane remains owned by canonical `The-Interdependency/skill-lib`; `stack`
only records how this deployment consumes it.

## Source pin

Use canonical `skill-lib` at:

```text
5c46d0534fa0726a9078f0a242c66a217fbaa501
```

Do not copy `vm-mcp` runtime files into this repository.

## Boundary

```text
human/bootstrap: SSH / Google OS Login / IAP
agent path:      ChatGPT MCP -> Secure MCP Tunnel -> 127.0.0.1:8765 on VM
runtime user:    vmmcp (non-root)
workspace:       /srv/vm-mcp/stack-observer
initial tools:   vm_info, list_directory, read_text
shell_exec:      disabled
public port:     none
```

The MCP workspace is deliberately separate from `/srv/stack`. Canonical `vm-mcp`
installation takes ownership of `VM_MCP_ROOT`; therefore `/srv/stack` itself must never
be used as that root. The stack checkout keeps its existing ownership and authority.

The initial MCP surface is observation-only. Do not enable `shell_exec`. If later write
capability is required, add named, reviewed administrative tools for specific
stack-orchestrator operations rather than exposing a generic writable shell.

## Human preflight

From the existing human recovery path, establish the minimum facts before installing
anything:

```bash
set -Eeuo pipefail

test -r /etc/os-release
command -v python3 >/dev/null
command -v systemctl >/dev/null
test -d /srv/stack/.git

git -C /srv/stack rev-parse HEAD
python3 --version
systemctl is-system-running || true
```

If `/srv/stack` is not the intended checkout, systemd is absent, or the human
SSH/OS-Login recovery path is not known-good, stop as `hmmm`.

## Bootstrap from the human-controlled VM session

Fetch the exact canonical source in a temporary checkout and run its shipped tests
before host installation:

```bash
set -Eeuo pipefail
umask 077

SKILL_LIB_SHA=5c46d0534fa0726a9078f0a242c66a217fbaa501
BOOTSTRAP_DIR="$(mktemp -d)"
trap 'rm -rf "$BOOTSTRAP_DIR"' EXIT

git clone --filter=blob:none https://github.com/The-Interdependency/skill-lib.git \
  "$BOOTSTRAP_DIR/skill-lib"
git -C "$BOOTSTRAP_DIR/skill-lib" checkout --detach "$SKILL_LIB_SHA"

test "$(git -C "$BOOTSTRAP_DIR/skill-lib" rev-parse HEAD)" = "$SKILL_LIB_SHA"

cd "$BOOTSTRAP_DIR/skill-lib"
PYTHONPATH=vm-mcp python -m unittest discover -s vm-mcp/tests -p 'test_*.py'

sudo VM_MCP_ROOT=/srv/vm-mcp/stack-observer bash vm-mcp/install.sh
```

The tests must pass before host installation. The installer records its source commit at
`/opt/vm-mcp/SOURCE_COMMIT`; verify it after installation:

```bash
test "$(cat /opt/vm-mcp/SOURCE_COMMIT)" = \
  5c46d0534fa0726a9078f0a242c66a217fbaa501
```

## Publish a non-secret observation snapshot

The read-only MCP workspace does not need direct filesystem access to the stack checkout.
GitHub remains the repository source; the VM contact only needs host facts that GitHub
cannot observe. Create one bounded snapshot for the agent to read:

```bash
bash <<'LOCAL'
set -Eeuo pipefail
umask 077

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

{
  printf 'observed_at_utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf '\n[os-release]\n'
  cat /etc/os-release
  printf '\n[kernel]\n'
  uname -srmo
  printf '\n[python]\n'
  python3 --version 2>&1
  printf '\n[postgres-client]\n'
  psql --version 2>&1 || true
  printf '\n[postgres-ready]\n'
  pg_isready 2>&1 || true
  printf '\n[stack-checkout]\n'
  git -C /srv/stack rev-parse HEAD
  stat -c 'owner=%U group=%G mode=%a path=%n' /srv/stack
  printf '\n[stack-filesystem]\n'
  findmnt -T /srv/stack -o TARGET,SOURCE,FSTYPE,OPTIONS
  printf '\n[orchestrator-account]\n'
  id stackorchestrator 2>&1 || true
  printf '\n[worker-service]\n'
  systemctl is-enabled stack-orchestrator-worker.service 2>&1 || true
  systemctl is-active stack-orchestrator-worker.service 2>&1 || true
  printf '\n[backup-mount]\n'
  if [[ -e /mnt/stack-orchestrator-backups ]]; then
    findmnt -T /mnt/stack-orchestrator-backups -o TARGET,SOURCE,FSTYPE,OPTIONS || true
  else
    printf 'absent\n'
  fi
} >"$tmp"

sudo install -o root -g vmmcp -m 0640 "$tmp" \
  /srv/vm-mcp/stack-observer/vm-observation.txt
LOCAL
```

Do not add environment dumps, database URLs, credential files, cloud metadata, private
keys, or token-bearing command output to this snapshot.

## Verify the local service before any tunnel

```bash
sudo systemctl --no-pager --full status vm-mcp.service
ss -ltnp | grep ':8765'
sudo systemctl show vm-mcp.service -p Environment
```

Acceptance requires:

```text
listener: 127.0.0.1:8765
VM_MCP_ROOT: /srv/vm-mcp/stack-observer
VM_MCP_SHELL_ENABLED: 0
service user: vmmcp
```

A listener on `0.0.0.0`, the VM's private address, or a public address is a stop
condition. `VM_MCP_SHELL_ENABLED=1` is also a stop condition during initial contact.

## Connect ChatGPT privately

ChatGPT does not connect directly to local/private MCP servers. Use OpenAI Secure MCP
Tunnel rather than opening port `8765` to the public internet. Follow the current OpenAI
product UI/documentation for tunnel provisioning; do not invent tunnel commands in
this repository.

Current product capability must be checked at connection time. As of this runbook's
creation, full MCP write/modify is available to Business and Enterprise/Edu workspaces;
Pro custom MCP is read/fetch only. Read-only bootstrap does not depend on write support.

## First end-to-end calls

After the private tunnel is connected, call only:

```text
vm_info
list_directory(path=".")
read_text(path="vm-observation.txt")
```

Verify the reported MCP root resolves to `/srv/vm-mcp/stack-observer`, the service
identity is non-root `vmmcp`, and the observation snapshot matches the intended VM.

Do not enable generic shell execution after this succeeds. The next design step is a
narrow stack deployment/acceptance capability based on the actual VM facts observed
through this contact plus the human bootstrap path.

## Removal / rollback

If the service or tunnel boundary is wrong, disconnect the ChatGPT app/tunnel first,
then stop the VM service:

```bash
sudo systemctl disable --now vm-mcp.service
```

Use the canonical `vm-mcp` uninstall/update guidance from the pinned `skill-lib` source
for any further cleanup. Do not delete SSH/OS Login recovery access as part of MCP
rollout.

## hmmm

- Concrete VM OS, PostgreSQL, mount, and service-account facts remain unobserved until
  the snapshot is produced and read through the private MCP contact.
- Secure MCP Tunnel provisioning is intentionally delegated to current OpenAI product
  infrastructure and documentation.
- A write-capable stack administrative broker is not designed until actual VM state and
  current client write capability are observed.
