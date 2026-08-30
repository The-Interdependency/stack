# VM personal-console bootstrap

This is the one-time bridge from the existing human SSH/OS Login/IAP recovery path to a
broad private MCP console for the VM owner. The control-plane runtime remains owned by
canonical `The-Interdependency/skill-lib`; `stack` records only how this deployment
consumes it.

## Work-graph identity

```text
skill-lib producer: The-Interdependency/skill-lib@222ba4d4348022d81950c3fad054bae7e528b6a0
stack consumer:     this stack checkout
relation:           canonical vm-mcp runtime -> stack VM operations
runtime authority:  skill-lib owns vm-mcp implementation; stack owns its deployment/use
```

No semantic, scientific, repository, or package authority transfers through this
control-plane relation.

## Boundary

```text
human/bootstrap: SSH / Google OS Login / IAP (retain as break-glass access)
agent path:      private MCP transport -> 127.0.0.1:8765 on VM
MCP service:     vmmcp, non-root
profile:         personal-console
workspace:       /srv/vm-mcp/workspace
workspace tools: read/write/stat/move/remove + shell_exec
host user tool:  user_exec(user, command, cwd)
root tool:       admin_exec(command, cwd)
root boundary:   separate vm-mcp-admin.service over AF_UNIX
public 8765:     forbidden
```

`admin_exec` is intentionally broad root authority for this single-owner VM. It is kept
visibly separate from `shell_exec` and `user_exec`; named stack/git/PostgreSQL/systemd
conveniences may be added for ergonomics but are not permission cages.

The MCP HTTP service itself remains non-root and hardened. Root execution occurs only
inside the separate root broker after Unix peer-credential verification.

## Human preflight

From the already-working human recovery route (for example `ai.sh`), establish that the
VM and recovery path are the intended ones before installing anything:

```bash
set -Eeuo pipefail

test -r /etc/os-release
command -v python3 >/dev/null
command -v git >/dev/null
command -v systemctl >/dev/null
command -v sudo >/dev/null
sudo -n true

if [[ -d /srv/stack/.git ]]; then
  STACK_ROOT=/srv/stack
elif [[ -d "$HOME/src/stack/.git" ]]; then
  STACK_ROOT="$HOME/src/stack"
else
  printf 'hmmm: stack checkout not found\n' >&2
  exit 22
fi

git -C "$STACK_ROOT" rev-parse HEAD
python3 --version
systemctl is-system-running || true
```

If the human recovery path is not known-good, systemd is absent, or the stack checkout
is ambiguous, stop as `hmmm`.

## Install the exact canonical personal console

Fetch the exact merged skill-lib source, run its shipped tests, then install
`personal-console`:

```bash
set -Eeuo pipefail
umask 077

SKILL_LIB_SHA=222ba4d4348022d81950c3fad054bae7e528b6a0
BOOTSTRAP_DIR="$(mktemp -d)"
trap 'rm -rf "$BOOTSTRAP_DIR"' EXIT

git clone --quiet --filter=blob:none \
  https://github.com/The-Interdependency/skill-lib.git \
  "$BOOTSTRAP_DIR/skill-lib"
git -C "$BOOTSTRAP_DIR/skill-lib" checkout --quiet --detach "$SKILL_LIB_SHA"

test "$(git -C "$BOOTSTRAP_DIR/skill-lib" rev-parse HEAD)" = "$SKILL_LIB_SHA"

cd "$BOOTSTRAP_DIR/skill-lib"
PYTHONPATH=vm-mcp \
  python3 -W error::ResourceWarning -m unittest discover \
  -s vm-mcp/tests -p 'test_*.py'

sudo -n \
  VM_MCP_PROFILE=personal-console \
  VM_MCP_ROOT=/srv/vm-mcp/workspace \
  bash vm-mcp/install.sh

test "$(sudo -n cat /opt/vm-mcp/SOURCE_COMMIT)" = "$SKILL_LIB_SHA"
```

The installer must not change ownership of an already-existing application checkout.
Do not use `/srv/stack` as an excuse to transfer repository ownership to `vmmcp`.

## Verify the authority split before connecting a client

```bash
sudo -n systemctl --no-pager --full status vm-mcp.service
sudo -n systemctl --no-pager --full status vm-mcp-admin.service

ss -ltnp | grep ':8765'
sudo -n stat -c '%U %G %a %n' /run/vm-mcp /run/vm-mcp/admin.sock
sudo -n systemctl show vm-mcp.service -p User -p Group -p Environment --no-pager
```

Acceptance requires:

```text
MCP listener:       127.0.0.1:8765 only
vm-mcp.service:     User=vmmcp; non-root hardening retained
profile:            personal-console
vm-mcp-admin:       root process; AF_UNIX only
/run/vm-mcp:        root:vmmcp mode 750
admin.sock:         root:vmmcp mode 660
human recovery:     still independently usable
```

A listener on `0.0.0.0:8765` or a VM public/private interface is a stop condition.

## Connect the MCP client privately

Use the client's current authenticated private-network/tunnel mechanism. Do not publish
port `8765` to the internet and do not put SSH private keys, service-account keys,
refresh tokens, or sudo passwords into MCP arguments or prompts.

Connection/product behavior changes over time; resolve it from the actual current client
surface rather than freezing product-plan claims in this repository.

## First end-to-end calls

Exercise authority progressively:

```text
vm_info()
write_text(path="contact-test.txt", text="vm-mcp personal console\n")
read_text(path="contact-test.txt")
shell_exec(command="id -u", cwd=".")
user_exec(user="stackorchestrator", command="id -u && pwd", cwd="/srv/stack")
admin_exec(command="id -u", cwd="/")
```

Expected distinctions:

```text
shell_exec: vmmcp / non-root
user_exec:  requested non-root account
admin_exec: uid 0
```

Then inspect the root broker audit trail:

```bash
sudo -n journalctl -u vm-mcp-admin.service --no-pager -n 50
```

The journal should make root/user mode, run-as identity, cwd, command digest, and terminal
status visible without relying on hidden MCP scheduler state.

## Stack operations after contact

Once the authority split is proven, the console may operate the stack directly. Typical
examples are:

```text
user_exec(
  user="stackorchestrator",
  cwd="/srv/stack",
  command="python -m frontend.cli.stackctl fresh status"
)

admin_exec(
  cwd="/",
  command="systemctl --no-pager --full status stack-orchestrator-worker.service"
)
```

Use ordinary authority when it is sufficient; use `admin_exec` when host/root authority
is actually required. This is an observability preference, not an artificial capability
restriction.

## Rollback

Return the MCP layer to read-only without removing human recovery:

```bash
sudo -n sed -i 's/^VM_MCP_PROFILE=.*/VM_MCP_PROFILE=read-only/' /etc/vm-mcp.env
sudo -n systemctl disable --now vm-mcp-admin.service
sudo -n systemctl restart vm-mcp.service
```

Full MCP stop:

```bash
sudo -n systemctl disable --now vm-mcp.service vm-mcp-admin.service
```

Disconnect the MCP client/private tunnel as a separate action. Do not delete SSH/OS
Login/IAP recovery as part of MCP rollback.

## hmmm

- Concrete VM OS, PostgreSQL, mount, account, and deployment state remain unobserved
  until the commands above are executed on the actual VM.
- Client/private-tunnel provisioning remains product infrastructure and must be resolved
  from the current connected client.
- The broad `personal-console` profile is intentional for this single-owner deployment;
  it should not be silently generalized to shared or multi-owner hosts.
