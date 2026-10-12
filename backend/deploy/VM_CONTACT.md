# VM personal-console bootstrap

This is the one-time bridge from the existing human SSH/OS Login/IAP recovery path to a
broad private MCP console for the VM owner. The control-plane runtime remains owned by
canonical `The-Interdependency/skill-lib`; `stack` records only how this deployment
consumes it.

## Work-graph identity

```text
skill-lib producer: The-Interdependency/skill-lib@24029ca728c02d12bd887a28325cfa6e4e00d581
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

`24029ca` is The-Interdependency/skill-lib#123 (squash merge). From that commit on,
vm-mcp refuses every HTTP request, loopback included, that lacks
`Authorization: Bearer <token>`. Before it, any local process could reach
`admin_exec` through the loopback listener. A VM running an older vm-mcp (for example
`222ba4d`) is therefore still exposed until the installer below is rerun with a token.
The upgraded unit will not start without a token, so the MCP path stays down, not open,
until steps 1 to 3 are done. Do them through the human SSH/OS Login/IAP path.

### 1. Provision a root-owned 0600 token

```bash
set -Eeuo pipefail
sudo -n sh -c 'umask 077 && python3 -c "import secrets; print(secrets.token_urlsafe(32))" > /root/vm-mcp.token'
sudo -n stat -c '%U:%G %a %n' /root/vm-mcp.token
```

Expect `root:root 600 /root/vm-mcp.token`. The token is 43 URL-safe characters (the
installer accepts 32 to 256 of `A-Za-z0-9_-`). It must be owned by the installing user
(root, under `sudo`), with no group or other access, or the installer exits 3. Never
print it, paste it into a command line, or put it in chat, prompts, tool arguments,
URLs or repository files.

### 2. Fetch, test and install the exact merged source

The tests run from your own clone. The install runs from a separate root-owned clone of
the same commit, because root's `git` refuses to read a checkout another user owns
("dubious ownership") and the installer would then record `SOURCE_COMMIT=hmmm`.

```bash
set -Eeuo pipefail
umask 077

SKILL_LIB_SHA=24029ca728c02d12bd887a28325cfa6e4e00d581
BOOTSTRAP_DIR="$(mktemp -d)"
ROOT_SRC="$(sudo -n mktemp -d /root/vm-mcp-src.XXXXXX)"
trap 'rm -rf "$BOOTSTRAP_DIR"; sudo -n rm -rf "$ROOT_SRC"' EXIT

git clone --quiet --filter=blob:none \
  https://github.com/The-Interdependency/skill-lib.git \
  "$BOOTSTRAP_DIR/skill-lib"
git -C "$BOOTSTRAP_DIR/skill-lib" checkout --quiet --detach "$SKILL_LIB_SHA"
test "$(git -C "$BOOTSTRAP_DIR/skill-lib" rev-parse HEAD)" = "$SKILL_LIB_SHA"

(cd "$BOOTSTRAP_DIR/skill-lib" && PYTHONPATH=vm-mcp \
  python3 -W error::ResourceWarning -m unittest discover \
  -s vm-mcp/tests -p 'test_*.py')

sudo -n git clone --quiet https://github.com/The-Interdependency/skill-lib.git "$ROOT_SRC/skill-lib"
sudo -n git -C "$ROOT_SRC/skill-lib" checkout --quiet --detach "$SKILL_LIB_SHA"
test "$(sudo -n git -C "$ROOT_SRC/skill-lib" rev-parse HEAD)" = "$SKILL_LIB_SHA"

sudo -n \
  VM_MCP_PROFILE=personal-console \
  VM_MCP_ROOT=/srv/vm-mcp/workspace \
  VM_MCP_AUTH_TOKEN_FILE=/root/vm-mcp.token \
  bash "$ROOT_SRC/skill-lib/vm-mcp/install.sh"; echo "rc=$?"

test "$(sudo -n cat /opt/vm-mcp/SOURCE_COMMIT)" = "$SKILL_LIB_SHA"
sudo -n sysctl -n kernel.yama.ptrace_scope
sudo -n stat -c '%U:%G %a %n' /etc/sysctl.d/99-zz-vm-mcp-ptrace.conf /etc/credstore/vm-mcp-token
```

Expect `rc=0`, the matching `SOURCE_COMMIT`, a ptrace scope of `1` or higher,
`root:root 644` for the sysctl file and `root:root 600` for `/etc/credstore/vm-mcp-token`.
The installer exits 3 on a bad or missing token, and exits 7 if the kernel has no Yama
LSM. On exit 7, enable Yama or stop as `hmmm`. Do not fall back to an unauthenticated or
`read-only` listener to get access back. The installer also removes any old
`VM_MCP_AUTH_TOKEN` from `/etc/vm-mcp.env`.

The installer must not change ownership of an already-existing application checkout.
Do not use `/srv/stack` as an excuse to transfer repository ownership to `vmmcp`.

## Verify the authority split before connecting a client

These are the skill-lib#123 checklist steps, corrected by the scratch-VM run at
`046c4cf` (Oct 11, 2026). vm-mcp at `24029ca` is identical to `046c4cf`. Run them as
root through the human path. The scratch run's step 8 (setting `ptrace_scope` to 0 to
watch the service fail closed) is deliberately left out on this VM. So is its step 9
(reinstalling as `read-only`), because it would change the deployed profile.

### a. Unit file

```bash
sudo -n systemd-analyze verify /etc/systemd/system/vm-mcp.service; echo "rc=$?"
sudo -n systemctl cat vm-mcp.service | grep -E 'StandardInput|ExecStartPre'
sudo -n systemctl show vm-mcp.service -p ExecStartPre
```

Expect `rc=0` with no error lines. Then expect
`ExecStartPre=+/opt/vm-mcp/.venv/bin/python -I /opt/vm-mcp/yama_gate.py` (with the `+`)
and `StandardInput=file:/etc/credstore/vm-mcp-token` in the unit, and `status=0` from
`systemctl show`. Check the `+` and the file path with `systemctl cat`:
`systemctl show` drops the `+` and prints only `StandardInput=file`.

### b. Both services up and listening on loopback only

```bash
timeout 60 sh -c "until ss -ltn | grep -q '127.0.0.1:8765 '; do sleep 1; done"
systemctl is-active vm-mcp.service vm-mcp-admin.service
sudo -n journalctl -u vm-mcp.service -b | grep -i yama-gate
ss -ltnp | grep ':8765'
sudo -n stat -c '%U %G %a %n' /run/vm-mcp /run/vm-mcp/admin.sock
sudo -n systemctl show vm-mcp.service -p User -p Group --no-pager
```

Wait for the port first. The server took 3 to 5 seconds to listen on an e2-small,
and every earlier request fails with curl `000`. Expect `active` twice, no yama-gate
lines, and a single `127.0.0.1:8765` listener.

### c. The running server holds no token

```bash
P=$(systemctl show -p MainPID --value vm-mcp.service); echo "pid=$P"
sudo -n readlink /proc/$P/fd/0
sudo -n ls -l /proc/$P/fd | grep -c credstore
sudo -n sh -c "tr '\\0' '\\n' < /proc/$P/environ | grep -c AUTH_TOKEN="
sudo -n grep -E '^(TracerPid|Uid):' /proc/$P/status
id -u vmmcp
```

Expect `/dev/null`, `0`, `0`, `TracerPid: 0`, and every Uid field equal to `id -u vmmcp`.
`VM_MCP_AUTH_TOKEN_SOURCE=stdin` in the environment is a setting, not the token.

### d. No vmmcp-writable code

```bash
sudo -n -u vmmcp find /opt/vm-mcp -writable 2>/dev/null | wc -l
sudo -n find /opt/vm-mcp ! -user root | wc -l
stat -c '%U %a %n' /opt /opt/vm-mcp /opt/vm-mcp/.venv/pyvenv.cfg
```

Expect `0`, `0`, and all three owned by `root` with no group or world write bit (for
example `755` or `644`).

### e. HTTP authentication

The token goes into root-only header files, so it never appears in a command line or
`/proc/*/cmdline`. curl reads a header file with `-H @FILE`.

```bash
sudo -n sh -c 'umask 077
  printf "Authorization: Bearer %s\n" "$(cat /root/vm-mcp.token)" > /root/vm-mcp.auth
  printf "Authorization: bearer %s\n" "$(cat /root/vm-mcp.token)" > /root/vm-mcp.auth-lower
  printf "Authorization: Bearer wrong-token-wrong-token-wrong-token\n" > /root/vm-mcp.auth-wrong'
U=http://127.0.0.1:8765/mcp
H=(-H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream')
INIT='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"check","version":"0"}}}'
LIST='{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
curl -s -o /dev/null -w '%{http_code}\n' "${H[@]}" -d "$INIT" $U
sudo -n curl -s -o /dev/null -w '%{http_code}\n' "${H[@]}" -H @/root/vm-mcp.auth-lower -d "$INIT" $U
sudo -n curl -s -o /dev/null -w '%{http_code}\n' "${H[@]}" -H @/root/vm-mcp.auth-wrong -d "$INIT" $U
curl -s -o /dev/null -w '%{http_code}\n' "${H[@]}" -d "$LIST" $U
```

Expect `401` with no header, `200` with lowercase `bearer` and the real token, `401`
with a wrong token, and `401` for an unauthenticated `tools/list`. The server accepts
protocolVersion `2025-03-26`.

### f. admin_exec through MCP, with a broker receipt

The server is stateless (`stateless_http=True`). It returns no `Mcp-Session-Id`, and
`notifications/initialized` isn't needed. `admin_exec` takes `command` (required),
`cwd` (default `/`) and `timeout_seconds` (default 60).

```bash
sudo -n curl -s "${H[@]}" -H @/root/vm-mcp.auth -d "$LIST" $U | grep -o '"admin_exec"'
sudo -n curl -s "${H[@]}" -H @/root/vm-mcp.auth \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"admin_exec","arguments":{"command":"id -u","cwd":"/"}}}' $U
printf %s 'id -u' | sha256sum
sudo -n journalctl -u vm-mcp-admin.service -n 20 --no-pager
sudo -n rm -f /root/vm-mcp.auth /root/vm-mcp.auth-lower /root/vm-mcp.auth-wrong
```

Expect `"admin_exec"` in the list. The call should return `ok: true` with mode `admin`,
run-as `root`, uid `0`, exit code `0` and stdout `0`. Expect a broker journal line
`{"event":"vm_mcp_exec","mode":"admin","run_as":"root","command_sha256":...,"exit_code":0}`
whose `command_sha256` equals the `sha256sum` output. The receipt carries no peer PID.
The broker checks vm-mcp's systemd MainPID on every request and logs only rejections,
so a successful call is the evidence that the check passed.

Acceptance requires all of a to f, plus:

```text
MCP listener:       127.0.0.1:8765 only
vm-mcp.service:     User=vmmcp; non-root hardening retained; no token in its environment or fds
profile:            personal-console
vm-mcp-admin:       root process; AF_UNIX only
/run/vm-mcp:        root:vmmcp mode 750
admin.sock:         root:vmmcp mode 660
HTTP:               401 without or with a wrong bearer token
human recovery:     still independently usable
```

A listener on `0.0.0.0:8765` or a VM public/private interface is a stop condition.

## Connect the MCP client privately

Use the client's current authenticated private-network/tunnel mechanism. Do not publish
port `8765` to the internet and do not put SSH private keys, service-account keys,
refresh tokens, or sudo passwords into MCP arguments or prompts.

The client must also send the bearer token on every request: the tunnel alone does not
authenticate, because every local process can reach loopback. Configure it as a
header in the client's secret or secure-header settings for this server, never in the
URL, a tool argument, a prompt or a repository file:

```text
Authorization: Bearer <contents of /root/vm-mcp.token>
```

Move the value from the VM into the client's secret store through the human path (for
example, read `/root/vm-mcp.token` in an SSH session and paste it straight into the
client's header or secret field). Afterwards, either delete `/root/vm-mcp.token` or keep
it under your own secret handling. The service reads only `/etc/credstore/vm-mcp-token`.
To rotate, write a new token file and rerun the step 2 installer command, then update
the client. A client with no header, or a stale one, gets `401` on every call.

Connection/product behavior changes over time; resolve it from the actual current client
surface rather than freezing product-plan claims in this repository. hmmm: the exact
header-configuration field for whichever MCP client and tunnel is used.

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

Under `read-only`, `tools/list` still advertises `admin_exec`, `user_exec` and
`shell_exec`. Calling them returns `PermissionError` ("host execution is disabled"),
`vm-mcp-admin` is inactive and `admin.sock` is gone. Bearer authentication stays
required. The installer's `99-zz-vm-mcp-ptrace.conf` stays in place.

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
- vm-mcp keeps restarting (`activating/auto-restart`) instead of landing in
  `failed`/`start-limit-hit` when the Yama gate refuses or the token is missing. It
  stays fail-closed (no `server.py` runs), but it fills the journal. Tracked as a
  skill-lib follow-up.
- Tools a profile disallows are still registered and listed. Tracked as a skill-lib
  follow-up.
- The broad `personal-console` profile is intentional for this single-owner deployment;
  it should not be silently generalized to shared or multi-owner hosts.
