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

Every `bash` block in this runbook is pasted into an interactive SSH shell, so each one
runs inside a `( ... )` subshell. `set -e`, traps, `umask` and variables end with the
block, and a failing command ends only that block, never your SSH session. Install
blocks stop at the first error. Check blocks run every check and print `PASS` or `FAIL`
for each one.

From the already-working human recovery route (for example `ai.sh`), establish that the
VM and recovery path are the intended ones before installing anything:

```bash
(
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
)
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
(
set -Eeuo pipefail
sudo -n sh -c 'umask 077 && python3 -c "import secrets; print(secrets.token_urlsafe(32))" > /root/vm-mcp.token'
sudo -n stat -c '%U:%G %a %n' /root/vm-mcp.token
)
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
(
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
  bash "$ROOT_SRC/skill-lib/vm-mcp/install.sh" || rc=$?
echo "rc=${rc:-0}"
[ "${rc:-0}" -eq 0 ] || exit "$rc"

test "$(sudo -n cat /opt/vm-mcp/SOURCE_COMMIT)" = "$SKILL_LIB_SHA"
sudo -n sysctl -n kernel.yama.ptrace_scope
sudo -n stat -c '%U:%G %a %n' /etc/sysctl.d/99-zz-vm-mcp-ptrace.conf /etc/credstore/vm-mcp-token
)
```

Expect `rc=0`, the matching `SOURCE_COMMIT`, a ptrace scope of `1` or higher,
`root:root 644` for the sysctl file and `root:root 600` for `/etc/credstore/vm-mcp-token`.
The installer exits 3 on a bad or missing token, and exits 7 if the kernel has no Yama
LSM. On exit 7, enable Yama or stop as `hmmm`. Do not fall back to an unauthenticated or
`read-only` listener to get access back. The installer also removes any old
`VM_MCP_AUTH_TOKEN` from `/etc/vm-mcp.env`.

The clean-up trap runs when the block's subshell ends, so both clones are removed
whether the install succeeds or fails.

**Every future installer rerun needs a token source too.** Without one, the installer
exits 3 and changes nothing. If `/root/vm-mcp.token` has been deleted, pass the token
the service already uses, `VM_MCP_AUTH_TOKEN_FILE=/etc/credstore/vm-mcp-token` (root,
`0600`), or rotate: write a new `/root/vm-mcp.token` as in step 1, rerun with it, and
update the client.

If the Yama gate refuses at start (for example a later sysctl.d file sets
`ptrace_scope` back to 0), or the token file is missing, `vm-mcp.service` stays down
but loops in `activating (auto-restart)` with a rising `NRestarts`. It does not reach
`failed`/`start-limit-hit`. The #123 scratch run saw this for the Yama gate; the
missing-token case wasn't tested, but should behave the same (hmmm). `server.py`
never runs, so the service stays fail-closed.
Fix the cause, then run `systemctl restart vm-mcp.service`.

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
(
ok() { if [ "$2" = "$3" ]; then echo "PASS $1"; else echo "FAIL $1 (want $2, got $3)"; fi; }
rc=0; sudo -n systemd-analyze verify /etc/systemd/system/vm-mcp.service || rc=$?
ok "unit verifies" 0 "$rc"
unit=$(sudo -n systemctl cat vm-mcp.service || true)
ok "privileged yama gate" 1 "$(grep -cxF 'ExecStartPre=+/opt/vm-mcp/.venv/bin/python -I /opt/vm-mcp/yama_gate.py' <<<"$unit" || true)"
ok "token on stdin" 1 "$(grep -cxF 'StandardInput=file:/etc/credstore/vm-mcp-token' <<<"$unit" || true)"
sudo -n systemctl show vm-mcp.service -p ExecStartPre
)
```

Expect three `PASS` lines and no error lines from `systemd-analyze`. The unit must
contain `ExecStartPre=+/opt/vm-mcp/.venv/bin/python -I /opt/vm-mcp/yama_gate.py` (with
the `+`) and `StandardInput=file:/etc/credstore/vm-mcp-token`. The last line must show
`status=0`. Check the `+` and the file path with `systemctl cat`:
`systemctl show` drops the `+` and prints only `StandardInput=file`.

### b. Both services up and listening on loopback only

```bash
(
ok() { if [ "$2" = "$3" ]; then echo "PASS $1"; else echo "FAIL $1 (want $2, got $3)"; fi; }
rc=0; timeout 60 sh -c "until ss -ltn | grep -q '127.0.0.1:8765 '; do sleep 1; done" || rc=$?
ok "listening within 60 s" 0 "$rc"
ok "vm-mcp active" active "$(systemctl is-active vm-mcp.service || true)"
ok "vm-mcp-admin active" active "$(systemctl is-active vm-mcp-admin.service || true)"
j=$(sudo -n journalctl -u vm-mcp.service -b --no-pager) || j=READ-FAILED
ok "no yama-gate refusals this boot" 0 "$(grep -ci -e yama-gate -e READ-FAILED <<<"$j" || true)"
ok "one listener on :8765" 1 "$(ss -ltnH | awk '$4 ~ /:8765$/' | wc -l)"
ok "listener is 127.0.0.1" 1 "$(ss -ltnH | awk '$4 == "127.0.0.1:8765"' | wc -l)"
ok "/run/vm-mcp" "root vmmcp 750" "$(sudo -n stat -c '%U %G %a' /run/vm-mcp || true)"
ok "admin.sock" "root vmmcp 660" "$(sudo -n stat -c '%U %G %a' /run/vm-mcp/admin.sock || true)"
ok "service user" vmmcp "$(systemctl show -p User --value vm-mcp.service || true)"
)
```

Wait for the port first. The server took 3 to 5 seconds to listen on an e2-small,
and every earlier request fails with curl `000`. Expect every line to be `PASS`.

### c. The running server holds no token

```bash
(
ok() { if [ "$2" = "$3" ]; then echo "PASS $1"; else echo "FAIL $1 (want $2, got $3)"; fi; }
P=$(systemctl show -p MainPID --value vm-mcp.service); echo "pid=$P"
U=$(id -u vmmcp)
ok "fd 0 is /dev/null" /dev/null "$(sudo -n readlink /proc/$P/fd/0 || true)"
fds=$(sudo -n ls -l /proc/$P/fd) || fds=READ-FAILED
ok "no credstore fds" 0 "$(grep -c -e credstore -e READ-FAILED <<<"$fds" || true)"
envs=$(sudo -n sh -c 'tr "\0" "\n" < /proc/$1/environ' _ "$P") || envs=READ-FAILED
ok "no AUTH_TOKEN= in environment" 0 "$(grep -c -e AUTH_TOKEN= -e READ-FAILED <<<"$envs" || true)"
ok "not traced" 0 "$(sudo -n awk '/^TracerPid:/{print $2}' /proc/$P/status || true)"
ok "all uids are vmmcp" "$U $U $U $U" "$(sudo -n awk '/^Uid:/{print $2, $3, $4, $5}' /proc/$P/status || true)"
)
```

Expect five `PASS` lines. A check whose input can't be read prints `FAIL`, never a
false `PASS`.
`VM_MCP_AUTH_TOKEN_SOURCE=stdin` in the environment is a setting, not the token.

### d. No vmmcp-writable code

```bash
(
ok() { if [ "$2" = "$3" ]; then echo "PASS $1"; else echo "FAIL $1 (want $2, got $3)"; fi; }
w=$(sudo -n -u vmmcp find /opt/vm-mcp -writable) || w=READ-FAILED
ok "nothing vmmcp-writable" 0 "$(grep -c . <<<"$w" || true)"
o=$(sudo -n find /opt/vm-mcp ! -user root) || o=READ-FAILED
ok "everything root-owned" 0 "$(grep -c . <<<"$o" || true)"
m=$(sudo -n find /opt /opt/vm-mcp /opt/vm-mcp/.venv/pyvenv.cfg -maxdepth 0 -perm /022) || m=READ-FAILED
ok "no group/world write" 0 "$(grep -c . <<<"$m" || true)"
stat -c '%U %a %n' /opt /opt/vm-mcp /opt/vm-mcp/.venv/pyvenv.cfg
)
```

Expect three `PASS` lines. All three paths must be owned by `root` with no group or
world write bit (for example `755` or `644`). If `find` reports a directory it can't read, the check
prints `FAIL`. Look at that directory's permissions before treating the result as a pass.

### e. HTTP authentication

The token goes into root-only header files, so it never appears in a command line or
`/proc/*/cmdline`. curl reads a header file with `-H @FILE`.

```bash
(
ok() { if [ "$2" = "$3" ]; then echo "PASS $1"; else echo "FAIL $1 (want $2, got $3)"; fi; }
sudo -n sh -c 'umask 077
  printf "Authorization: Bearer %s\n" "$(cat /root/vm-mcp.token)" > /root/vm-mcp.auth
  printf "Authorization: bearer %s\n" "$(cat /root/vm-mcp.token)" > /root/vm-mcp.auth-lower
  printf "Authorization: Bearer wrong-token-wrong-token-wrong-token\n" > /root/vm-mcp.auth-wrong'
U=http://127.0.0.1:8765/mcp
H=(-H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream')
INIT='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"check","version":"0"}}}'
LIST='{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
ok "no header" 401 "$(curl -s -o /dev/null -w '%{http_code}' "${H[@]}" -d "$INIT" $U || true)"
ok "lowercase bearer, real token" 200 "$(sudo -n curl -s -o /dev/null -w '%{http_code}' "${H[@]}" -H @/root/vm-mcp.auth-lower -d "$INIT" $U || true)"
ok "wrong token" 401 "$(sudo -n curl -s -o /dev/null -w '%{http_code}' "${H[@]}" -H @/root/vm-mcp.auth-wrong -d "$INIT" $U || true)"
ok "unauthenticated tools/list" 401 "$(curl -s -o /dev/null -w '%{http_code}' "${H[@]}" -d "$LIST" $U || true)"
)
```

Expect four `PASS` lines. The header files stay in place for step f, which deletes
them. The server accepts
protocolVersion `2025-03-26`.

### f. admin_exec through MCP, with a broker receipt

The server is stateless (`stateless_http=True`). It returns no `Mcp-Session-Id`, and
`notifications/initialized` isn't needed. `admin_exec` takes `command` (required),
`cwd` (default `/`) and `timeout_seconds` (default 60).

Step f defines `U`, `H` and `LIST` itself, so it doesn't depend on step e's shell.
It needs step e's `/root/vm-mcp.auth`.

```bash
(
ok() { if [ "$2" = "$3" ]; then echo "PASS $1"; else echo "FAIL $1 (want $2, got $3)"; fi; }
U=http://127.0.0.1:8765/mcp
H=(-H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream')
INIT='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"check","version":"0"}}}'
LIST='{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
ok "admin_exec listed" 1 "$(sudo -n curl -s "${H[@]}" -H @/root/vm-mcp.auth -d "$LIST" $U | grep -o '"admin_exec"' | sort -u | wc -l)"
sudo -n curl -s "${H[@]}" -H @/root/vm-mcp.auth \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"admin_exec","arguments":{"command":"id -u","cwd":"/"}}}' $U || true
echo
SHA=$(printf %s 'id -u' | sha256sum | cut -d' ' -f1)
ok "broker receipt for id -u" 1 "$(sudo -n journalctl -u vm-mcp-admin.service -n 50 --no-pager | grep -F '"command_sha256":"'"$SHA"'"' | grep -F '"mode":"admin"' | grep -F '"run_as":"root"' | grep -cF '"exit_code":0' | sed 's/^[1-9][0-9]*$/1/' || true)"
sudo -n journalctl -u vm-mcp-admin.service -n 20 --no-pager
sudo -n rm -f /root/vm-mcp.auth /root/vm-mcp.auth-lower /root/vm-mcp.auth-wrong
)
```

Expect both `PASS` lines. The call should return `ok: true` with mode `admin`,
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

Move the value from the VM to the client without printing it. Don't `cat` it in an
interactive SSH session, because it would stay in the terminal scrollback. Run one of
these from the machine where the client is configured. The token travels only through
the pipe. Use your usual human access for `ssh` (for example `gcloud compute ssh VM
--tunnel-through-iap --command '...'` for IAP/OS Login):

```text
# into the clipboard, then paste into the client's secret header field and clear the clipboard
ssh VM 'sudo -n cat /root/vm-mcp.token' | tr -d '\n' | pbcopy          # macOS
ssh VM 'sudo -n cat /root/vm-mcp.token' | tr -d '\n' | wl-copy         # Wayland (xclip -selection clipboard on X11)

# or into a local 0600 file that the client's secret configuration reads
(umask 077 && ssh VM 'sudo -n cat /root/vm-mcp.token' > ~/.config/vm-mcp/token)
```

**For an agent client** (ChatGPT, Claude, Codex, Grok Bot or similar), the token goes
only in the MCP connector's secret or header configuration (`Authorization: Bearer ...`).
Never type, paste or upload it into the conversation itself, and never ask the agent to
read `/root/vm-mcp.token` through MCP. Anything in the conversation is model context.

Afterwards, either delete `/root/vm-mcp.token` or keep it under your own secret
handling. The service reads only `/etc/credstore/vm-mcp-token`. Remember that every
installer rerun needs a token source (see step 2). To rotate, write a new token file
as in step 1 and rerun the step 2 install block, then update the client. A client with
no header, or a stale one, gets `401` on every call.

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
