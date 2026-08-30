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
initial tools:   vm_info, list_directory, read_text
shell_exec:      disabled
public port:     none
```

The initial `VM_MCP_ROOT` is `/srv/stack`. This is deliberately read-only at the MCP
tool layer. Do not enable `shell_exec` against that root: a writable generic shell over
the stack checkout would be broader than the deployment operation requires.

If later write capability is required, add named, reviewed administrative tools for the
specific stack-orchestrator operations instead of enabling a generic privileged shell.

## Bootstrap from a human-controlled VM session

First verify that `/srv/stack` is the intended checkout and that human recovery access
works. Then fetch the exact canonical source in a temporary bootstrap checkout:

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

sudo VM_MCP_ROOT=/srv/stack bash vm-mcp/install.sh
```

The tests must pass before host installation. If checkout identity, tests, systemd, or
`/srv/stack` identity is unresolved, stop as `hmmm`.

## Verify the local service before any tunnel

```bash
sudo systemctl --no-pager --full status vm-mcp.service
ss -ltnp | grep ':8765'
```

Acceptance requires the listener to be `127.0.0.1:8765`. A listener on `0.0.0.0`, the
VM's private address, or a public address is a stop condition.

Confirm no shell override exists:

```bash
sudo systemctl show vm-mcp.service -p Environment
```

`VM_MCP_SHELL_ENABLED=1` must not be present during initial contact.

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
read_text(path="backend/deploy/VM_SETUP.md")
```

Verify the reported MCP root resolves to `/srv/stack` and the service identity is the
non-root `vmmcp` account.

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

- Concrete VM OS, Python, systemd, PostgreSQL, mount, and service-account facts remain
  unobserved until read-only VM contact is established.
- Secure MCP Tunnel provisioning is intentionally delegated to current OpenAI product
  infrastructure and documentation.
- A write-capable stack administrative broker is not designed until actual VM state and
  current client write capability are observed.
