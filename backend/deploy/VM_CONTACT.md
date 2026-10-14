# VM personal-console bootstrap

This is the one-time bridge from the existing human SSH/OS Login/IAP recovery path to a
private MCP console for the VM owner. The control-plane runtime remains owned by
canonical `The-Interdependency/skill-lib`; `stack` records only how this deployment
consumes it.

## Work-graph identity

```text
skill-lib producer: The-Interdependency/skill-lib@e74ce1ee8a2cea50b0a6acce7697a6d3d9b2e128
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
privileged:      separate vm-mcp-admin.service over AF_UNIX (personal-console only)
public 8765:     forbidden
```

The profile's privileged components are documented in skill-lib (`vm-mcp/SKILL.md`)
and are intentional for this single-owner VM. They stay visibly separate from the
workspace and host-user tools.

The MCP HTTP service itself remains non-root and hardened. Privileged work happens only
inside the separate broker unit after Unix peer-credential verification.

Some checks below need the name of the profile's privileged tool. Write it once,
from skill-lib's `vm-mcp/SKILL.md`, into a root-only file:

```text
sudo -n sh -c 'umask 077; printf "%s\n" "<privileged tool name>" > /root/vm-mcp.priv-tool'
```

## Human preflight

If vm-mcp is already installed on the VM (`/opt/vm-mcp` or `/etc/vm-mcp.env` exists),
run the preflight, then follow **Upgrading a VM that already has vm-mcp** instead of
steps 1–2.

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

## Upgrading a VM that already has vm-mcp

Use this section instead of a fresh install whenever `/opt/vm-mcp` or `/etc/vm-mcp.env`
already exists. A rerun of `install.sh` is **not** history-preserving on its own: it
takes `VM_MCP_ROOT` and `VM_MCP_PROFILE` only from its environment (defaulting to
`/srv/vm-mcp/workspace` and `read-only`), rewrites `/etc/vm-mcp.env` from scratch, and
drops keys it does not know (for example the legacy `VM_MCP_SHELL_ENABLED`). Its
`usermod` also fails with exit 8 while any `vmmcp` process is running. The steps below
(U1–U6) make the upgrade preserve what the VM already has, and they replace steps 1–2
for this case. Checks a–f and the #127 checks then follow, adapted in U5.

Principles:

- **Preserve by default.** The existing workspace root, service-user home, profile and
  privileged components carry over unchanged. The upgrade only changes the code and
  token-protects every local endpoint.
- **No new empty workspace.** The service is never pointed at a different
  `VM_MCP_ROOT` unless the operator writes that choice into the target file in U2.
- **No silent profile change.** A different profile is a separate, explicit decision
  recorded in U2, never a side effect of the installer's defaults.
- **Token everywhere.** After the upgrade every HTTP request, loopback included,
  needs the bearer token, whatever the profile.

### U1. Inventory and back up (read-only on the VM's state)

This writes only a new root-only backup and publishes the latest pointer **after**
all copies, archive reads, and state checks succeed. Do not run concurrent upgrades
or change the units/configuration between U1 and U4. An incomplete backup is not a
rollback point. The backup/staging filesystems must support the recorded ownership,
permissions, ACLs and extended attributes; any tar/copy warning blocks acceptance.
The supported baseline has an existing `vmmcp` account and stable
`active`/`inactive` services with `enabled`, `disabled`, `static`, or absent units;
external install-tree symlinks (except standard venv interpreter links) and
other states stop as `hmmm` before any service is stopped. Masked, linked, runtime-
enabled, or transient units need a separately reviewed recovery plan.

```bash
(
set -Eeuo pipefail
sudo -n python3 -I - <<'PY'
# U1 snapshot: keep raw environment and credentials inside the root-only archive.
import hashlib, json, os, pathlib, pwd, re, stat, subprocess, tarfile, tempfile

def deployment_manifest(paths):
    """Read names, content and preservation metadata without following symlinks."""
    records = {}
    pending = [pathlib.Path("/") / p for p in paths]
    while pending:
        path = pending.pop()
        if not os.path.lexists(path):
            continue
        info = os.lstat(path)
        record = {"kind": stat.S_IFMT(info.st_mode), "mode": stat.S_IMODE(info.st_mode),
                  "uid": info.st_uid, "gid": info.st_gid, "mtime_ns": info.st_mtime_ns,
                  "xattrs": {name: os.getxattr(path, name, follow_symlinks=False).hex()
                             for name in sorted(os.listxattr(path, follow_symlinks=False))}}
        if stat.S_ISLNK(info.st_mode):
            record["link"] = os.readlink(path)
        elif stat.S_ISDIR(info.st_mode):
            pending.extend(path.iterdir())
        elif stat.S_ISREG(info.st_mode):
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            record["sha256"] = digest.hexdigest()
        else:
            raise SystemExit("hmmm: unsupported special file in deployment snapshot")
        records[str(path)] = record
    return records

def require(condition, message):
    if not condition:
        raise AssertionError(message)

os.umask(0o077)
paths = ["opt/vm-mcp", "etc/vm-mcp.env",
         "etc/systemd/system/vm-mcp.service", "etc/systemd/system/vm-mcp-admin.service",
         "etc/systemd/system/vm-mcp.service.d", "etc/systemd/system/vm-mcp-admin.service.d",
         "etc/credstore/vm-mcp-token", "etc/sysctl.d/99-zz-vm-mcp-ptrace.conf"]
B = pathlib.Path(tempfile.mkdtemp(prefix="vm-mcp-upgrade.", dir="/root"))
account = pwd.getpwnam("vmmcp")  # absent account: stop, do not invent a rollback
units = {}
for unit in ("vm-mcp.service", "vm-mcp-admin.service"):
    result = subprocess.run(["systemctl", "show", unit, "--property=LoadState,ActiveState,UnitFileState"],
                            check=True, text=True, capture_output=True)
    state = dict(line.split("=", 1) for line in result.stdout.splitlines() if "=" in line)
    if state.get("LoadState") == "not-found":
        state["UnitFileState"] = "absent"
    if (state.get("LoadState") not in {"loaded", "not-found"}
        or state.get("ActiveState") not in {"active", "inactive"}
        or state.get("UnitFileState") not in {"enabled", "disabled", "static", "absent"}):
        raise SystemExit("hmmm: unsupported or transitional unit state; no upgrade: " + unit)
    units[unit] = state
present = [p for p in paths if os.path.lexists("/" + p)]
# The installer can follow these locations while writing; a symlink baseline
# would require backing up external referents, which this transaction does not own.
for path in present:
    require(not pathlib.Path('/' + path).is_symlink(), 'hmmm: deployment artifact symlink needs separate recovery plan')
for directory in ("/etc/systemd/system/vm-mcp.service.d", "/etc/systemd/system/vm-mcp-admin.service.d"):
    if pathlib.Path(directory).is_dir():
        require(not any((p.is_symlink() for p in pathlib.Path(directory).rglob('*'))), 'hmmm: drop-in symlink needs separate recovery plan')
install_tree = pathlib.Path("/opt/vm-mcp").resolve()
for entry in install_tree.rglob("*") if install_tree.is_dir() else []:
    if not entry.is_symlink():
        continue
    referent = entry.resolve()
    if referent == install_tree or install_tree in referent.parents:
        continue  # internal referent is part of this same archive
    relative = entry.relative_to(install_tree).as_posix()
    interpreter = (re.fullmatch(r"\.venv/bin/python(?:[0-9]+(?:\.[0-9]+)?)?", relative)
                   and referent.parent in {pathlib.Path("/usr/bin").resolve(), pathlib.Path("/usr/local/bin").resolve()}
                   and re.fullmatch(r"python[0-9]+(?:\.[0-9]+)?", referent.name))
    require(interpreter, "hmmm: install-tree symlink escapes backup; separate recovery plan required")
before = deployment_manifest(paths)
archive = B / "state.tar"
tar_result = subprocess.run(["tar", "--acls", "--xattrs", "--xattrs-include=*", "-C", "/", "-cpf", str(archive), "--", *present], check=True, capture_output=True)
require(not tar_result.stderr, "hmmm: archive operation warned; inspect backup/storage before continuing")
# Read every byte, not just the archive header; tar --compare also detects changed sources.
with tarfile.open(archive, "r:") as saved:
    for member in saved:
        if member.isfile():
            with saved.extractfile(member) as content:
                while content.read(1024 * 1024):
                    pass
tar_result = subprocess.run(["tar", "--acls", "--xattrs", "--xattrs-include=*", "--compare", "-f", str(archive), "-C", "/"], check=True, capture_output=True)
require(not tar_result.stderr, "hmmm: archive operation warned; inspect backup/storage before continuing")
h = hashlib.sha256()
with archive.open("rb") as stream:
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        h.update(chunk)
archive_digest = h.hexdigest()
require(deployment_manifest(paths) == before, "deployment changed during backup; repeat U1")
manifest = {"deployment": before, "paths": paths, "present": present, "units": units,
            "home": account.pw_dir, "uid": account.pw_uid,
            "archive_sha256": archive_digest}
(B / "state.json").write_text(json.dumps(manifest, indent=2) + "\n")
# Copy the environment for the non-evaluating target parser; never print arbitrary env/drop-ins.
if "etc/vm-mcp.env" in present:
    with tarfile.open(archive, "r:") as saved:
        with saved.extractfile("etc/vm-mcp.env") as source:
            (B / "vm-mcp.env").write_bytes(source.read())
summary = {"backup": str(B), "home": account.pw_dir, "units": units,
           "present": present, "environment": "saved privately; token values never printed"}
(B / "inventory.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
# The marker and atomic latest-pointer publication happen last.
(B / "COMPLETE").write_text("complete\n")
pointer = pathlib.Path("/root/vm-mcp-upgrade.latest.new")
pointer.write_text(str(B) + "\n")
pointer.replace("/root/vm-mcp-upgrade.latest")
PY
)
```

The raw archive and private environment copy contain secrets. Do not print, upload,
or attach them to a PR. Printed inventory is an allowlist, so even indented token
assignments and secrets inside unit drop-ins are never copied to a terminal log.
### U2. Derive the preserved target

Resolve the profile like `profiles.resolve_profile`: explicit profile wins; otherwise
legacy `VM_MCP_SHELL_ENABLED=1/true/yes/on` means `workspace`, else `read-only`.
Store values as JSON, never shell source or `eval`. Unsupported multiline or ambiguous
environment syntax stops rather than guessing a root or losing configuration.

```bash
(
set -Eeuo pipefail
sudo -n python3 -I - <<'PY'
# U2 target: parse data, never execute environment assignments.
import json, os, pathlib, re, shlex

def require(condition, message):
    if not condition:
        raise AssertionError(message)

os.umask(0o077)
B = pathlib.Path(pathlib.Path("/root/vm-mcp-upgrade.latest").read_text().strip())
require((B / 'COMPLETE').read_text() == 'complete\n', 'incomplete backup')
state = json.loads((B / "state.json").read_text())
env = {}
source = B / "vm-mcp.env"
for line in source.read_text().splitlines() if source.exists() else []:
    if not line.strip() or line.lstrip().startswith(("#", ";")):
        continue
    match = re.fullmatch(r'\s*([A-Z_][A-Z_0-9]*)\s*=(.*)', line)
    if not match:
        raise SystemExit("hmmm: unsupported environment syntax; review privately")
    key, raw = match.groups()
    try:
        words = shlex.split(raw, comments=False, posix=True)
    except ValueError:
        raise SystemExit("hmmm: multiline/invalid environment value; review privately")
    if len(words) > 1 or raw.rstrip().endswith("\\"):
        raise SystemExit("hmmm: ambiguous environment value; review privately")
    env[key] = words[0] if words else ""
profile = env.get("VM_MCP_PROFILE", "").strip().lower()
if not profile:
    profile = "workspace" if env.get("VM_MCP_SHELL_ENABLED", "").strip().lower() in {"1", "true", "yes", "on"} else "read-only"
if profile not in {"read-only", "workspace", "personal-console"}:
    raise SystemExit("hmmm: unknown profile")
broker = state["units"]["vm-mcp-admin.service"]
if (broker["ActiveState"] == "active" or broker["UnitFileState"] == "enabled") and profile != "personal-console":
    raise SystemExit("hmmm: broker state conflicts with resolved profile")
root = env.get("VM_MCP_ROOT") or "/srv/vm-mcp/workspace"
if state["home"] != root.rstrip("/") + "/.vm-mcp-home":
    raise SystemExit("hmmm: existing home differs from installer convention; stop and review")
target = {"root": root, "profile": profile, "port": env.get("VM_MCP_PORT", "8765"),
          "admin_socket": env.get("VM_MCP_ADMIN_SOCKET", "/run/vm-mcp/admin.sock"),
          "token_file": "/etc/credstore/vm-mcp-token" if "etc/credstore/vm-mcp-token" in state["present"] else "/root/vm-mcp.token"}
(B / "target.json").write_text(json.dumps(target, indent=2) + "\n")
print(json.dumps(target, indent=2))
PY
)
```

Check the printed root, profile, port and socket against the existing configuration.
To deliberately change them, edit the root-only `$B/target.json` through the human
path and record the decision. This JSON is data, including spaces and shell
metacharacters; it is never evaluated. The pinned installer's workspace drop-in
cannot safely represent every systemd path (whitespace, `%`, backslashes or quotes),
so U4 stops for those roots **before downtime**. Resolve that producer limitation
separately rather than changing the workspace silently or consuming an unmerged fix.
The same fail-closed boundary applies to non-default admin sockets: the pinned
broker unit hardcodes `/run/vm-mcp/admin.sock` and does not read the environment
file. Passing `VM_MCP_ADMIN_SOCKET` alone cannot preserve both endpoints. U2 records
the actual socket, but U4 refuses a custom socket before downtime; use a separately
reviewed producer/deployment fix rather than silently changing it.
### U3. Select and validate the token source

The default target reuses `/etc/credstore/vm-mcp-token` when present, avoiding a client
update. Otherwise provision a token using fresh-install step 1 below. If choosing a
different existing file, write its absolute path into `target.json`'s `token_file`,
or set `VM_MCP_AUTH_TOKEN_FILE=/absolute/path` when running U4. U4 persists that
selected path before installation; verification reads the same path. No token value
belongs in JSON, shell arguments, logs, or chat. Token permissions, owner, descriptor
identity and format are checked before the services stop, and again by the installer.

### U4. Stop, install with the preserved target, restart

Run from the known-good human recovery path, never through MCP. Source tests and
preflight complete before stopping units. Expect an MCP outage; package installation
or download failures can make it longer than a minute. The installer starts/enables
the main unit and starts/enables the broker only for `personal-console`; approving
this step includes that target activation. U6 restores prior activation/enablement.

```bash
(
set -Eeuo pipefail
trap 'echo "FAIL step U4 at line $LINENO (exit $?)" >&2' ERR
umask 077
SKILL_LIB_SHA=e74ce1ee8a2cea50b0a6acce7697a6d3d9b2e128
BOOTSTRAP_DIR="$(mktemp -d)"
ROOT_SRC="$(sudo -n mktemp -d /root/vm-mcp-src.XXXXXX)"
trap 'rm -rf "$BOOTSTRAP_DIR"; sudo -n rm -rf "$ROOT_SRC"' EXIT
git clone --quiet --filter=blob:none https://github.com/The-Interdependency/skill-lib.git "$BOOTSTRAP_DIR/skill-lib"
git -C "$BOOTSTRAP_DIR/skill-lib" checkout --quiet --detach "$SKILL_LIB_SHA"
test "$(git -C "$BOOTSTRAP_DIR/skill-lib" rev-parse HEAD)" = "$SKILL_LIB_SHA"
(cd "$BOOTSTRAP_DIR/skill-lib" && PYTHONPATH=vm-mcp python3 -W error::ResourceWarning -m unittest discover -s vm-mcp/tests -p 'test_*.py')
sudo -n git clone --quiet https://github.com/The-Interdependency/skill-lib.git "$ROOT_SRC/skill-lib"
sudo -n git -C "$ROOT_SRC/skill-lib" checkout --quiet --detach "$SKILL_LIB_SHA"
test "$(sudo -n git -C "$ROOT_SRC/skill-lib" rev-parse HEAD)" = "$SKILL_LIB_SHA"
# Only the token PATH is passed; the token value is never an argument/environment value.
sudo -n env ROOT_SRC="$ROOT_SRC" TOKEN_OVERRIDE="${VM_MCP_AUTH_TOKEN_FILE:-}" python3 -I - <<'PY'
# U4 preflight and install: every target value remains a subprocess argument or env value.
import hashlib, json, os, pathlib, pwd, re, stat, subprocess, time

def deployment_manifest(paths):
    """Read names, content and preservation metadata without following symlinks."""
    records = {}
    pending = [pathlib.Path("/") / p for p in paths]
    while pending:
        path = pending.pop()
        if not os.path.lexists(path):
            continue
        info = os.lstat(path)
        record = {"kind": stat.S_IFMT(info.st_mode), "mode": stat.S_IMODE(info.st_mode),
                  "uid": info.st_uid, "gid": info.st_gid, "mtime_ns": info.st_mtime_ns,
                  "xattrs": {name: os.getxattr(path, name, follow_symlinks=False).hex()
                             for name in sorted(os.listxattr(path, follow_symlinks=False))}}
        if stat.S_ISLNK(info.st_mode):
            record["link"] = os.readlink(path)
        elif stat.S_ISDIR(info.st_mode):
            pending.extend(path.iterdir())
        elif stat.S_ISREG(info.st_mode):
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            record["sha256"] = digest.hexdigest()
        else:
            raise SystemExit("hmmm: unsupported special file in deployment snapshot")
        records[str(path)] = record
    return records

def require(condition, message):
    if not condition:
        raise AssertionError(message)

B = pathlib.Path(pathlib.Path("/root/vm-mcp-upgrade.latest").read_text().strip())
require((B / 'COMPLETE').read_text() == 'complete\n', 'incomplete backup')
state = json.loads((B / "state.json").read_text())
target = json.loads((B / "target.json").read_text())
account = pwd.getpwnam("vmmcp")
require((account.pw_uid, account.pw_dir) == (state['uid'], state['home']), 'service account changed; repeat U1')
if os.environ.get("TOKEN_OVERRIDE"):
    target["token_file"] = os.environ["TOKEN_OVERRIDE"]
require(set(target) == {'root', 'profile', 'port', 'admin_socket', 'token_file'}, 'unknown target fields')
require(all((isinstance(v, str) and '\n' not in v and ('\r' not in v) and ('\x00' not in v) for v in target.values())), 'invalid target value')
require(target['profile'] in {'read-only', 'workspace', 'personal-console'}, 'invalid profile')
require(target["admin_socket"] == "/run/vm-mcp/admin.sock", "hmmm: pinned broker unit cannot preserve a custom socket; stop before downtime")
require(re.fullmatch('[0-9]+', target['port']) and 1 <= int(target['port']) <= 65535, 'invalid port')
require(all((target[k].startswith('/') for k in ('root', 'admin_socket', 'token_file'))), 'paths must be absolute')
root = pathlib.Path(target["root"]).resolve()
install = pathlib.Path("/opt/vm-mcp").resolve()
require(root != pathlib.Path('/') and root != install and (root not in install.parents) and (install not in root.parents), 'workspace overlaps install')
# A preserved root (the inventoried one) may be empty; a newly chosen root must hold data.
preserved = root == pathlib.Path(state['home']).parent.resolve()
require(root.is_dir(), 'workspace must exist and be a directory')
require(preserved or any((p.name != '.vm-mcp-home' for p in root.iterdir())), 'a changed workspace root must exist and be nonempty')
require(not re.search('[\\s%\\\\"\']', target['root']), 'hmmm: pinned installer cannot represent this workspace drop-in safely')
# Verify the completed archive without touching the live deployment.
h = hashlib.sha256()
with (B / "state.tar").open("rb") as stream:
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        h.update(chunk)
require(h.hexdigest() == state['archive_sha256'], 'backup checksum mismatch')
# Detect additions and ACL/xattr/content drift, including entries tar --compare ignores.
require(deployment_manifest(state["paths"]) == state["deployment"], "deployment changed; repeat U1")
# Also compare archived payloads before overwriting them.
tar_result = subprocess.run(["tar", "--acls", "--xattrs", "--xattrs-include=*", "--compare", "-f", str(B / "state.tar"), "-C", "/"], check=True, capture_output=True)
require(not tar_result.stderr, "hmmm: archive operation warned; inspect backup/storage before continuing")
for path in set(state["paths"]) - set(state["present"]):
    require(not os.path.lexists('/' + path), 'previously absent artifact appeared; repeat U1')
for unit, prior in state["units"].items():
    result = subprocess.run(["systemctl", "show", unit, "--property=LoadState,ActiveState,UnitFileState"], check=True, text=True, capture_output=True)
    now = dict(line.split("=", 1) for line in result.stdout.splitlines() if "=" in line)
    if now.get("LoadState") == "not-found":
        now["UnitFileState"] = "absent"
    require(now == prior, 'unit state changed; repeat U1')
# Same one-open descriptor/owner/permission contract as the canonical installer.
fd = os.open(target["token_file"], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
with os.fdopen(fd, "rb") as token_file:
    opened = os.fstat(token_file.fileno())
    named = os.lstat(target["token_file"])
    require(stat.S_ISREG(opened.st_mode) and stat.S_ISREG(named.st_mode), 'token is not regular')
    require((opened.st_dev, opened.st_ino) == (named.st_dev, named.st_ino), 'token path changed')
    require(opened.st_uid == 0 and stat.S_IMODE(opened.st_mode) & 63 == 0, 'unsafe token owner/mode')
    token = token_file.readline(258).removesuffix(b"\n")
    require(re.fullmatch(b'[A-Za-z0-9_-]{32,256}', token), 'invalid token format')
del token
(B / "target.json").write_text(json.dumps(target, indent=2) + "\n")
for unit, prior in state["units"].items():
    if prior["LoadState"] != "not-found":
        subprocess.run(["systemctl", "stop", unit], check=True)
# Bounded safety wait: usermod must never race a remaining vmmcp process.
for attempt in range(31):
    probe = subprocess.run(["pgrep", "-u", str(state["uid"])], capture_output=True)
    if probe.returncode == 1:
        break
    require(probe.returncode == 0, 'could not check service processes')
    if attempt == 30:
        raise SystemExit("hmmm: vmmcp processes remain; stop and use U6")
    time.sleep(1)
env = {k: v for k, v in os.environ.items() if not k.startswith("VM_MCP_")}
env.update(VM_MCP_ROOT=target["root"], VM_MCP_PROFILE=target["profile"],
           VM_MCP_PORT=target["port"], VM_MCP_ADMIN_SOCKET=target["admin_socket"],
           VM_MCP_AUTH_TOKEN_FILE=target["token_file"])
result = subprocess.run(["bash", os.environ["ROOT_SRC"] + "/skill-lib/vm-mcp/install.sh"], env=env)
print("rc=" + str(result.returncode))
if result.returncode:
    raise SystemExit(result.returncode)
require(pathlib.Path('/opt/vm-mcp/SOURCE_COMMIT').read_text().strip() == 'e74ce1ee8a2cea50b0a6acce7697a6d3d9b2e128', 'wrong installed source')
PY
)
```

The workspace guard accepts the preserved (inventoried) root whether or not it holds
data; it must still exist and be a directory. Only a root changed in `target.json`
must also be nonempty, so an edit cannot silently point the service at an empty one.

Expect `rc=0`. The Python result is initialized by the actual invocation, so an
interactive shell's old `rc` cannot turn success into failure. On any failure after
stopping, keep using the human recovery path and use U6 or fix forward. Do not infer
"nothing changed" from an installer exit code: even busy-user/root failures may
follow ptrace-file or package changes. U6 restores the inventoried deployment files
and service-user home, but does not undo package-manager changes or lower live Yama
policy. Never restore old unauthenticated code without considering that exposure.

From #131 (`e74ce1e`) a rerun over an existing install is upgrade-safe:

- Workspace root, profile, port and socket default to the existing `/etc/vm-mcp.env`.
  U4 still passes the persisted target explicitly; it should match what is installed.
- Changing the root or profile needs `VM_MCP_ALLOW_RECONFIGURE=1`. Without it a
  mismatch is refused (exit 3) before anything changes. U4 does not set it: if U4 is
  refused, the persisted target differs from the installed one, so stop and compare
  rather than adding the override.
- Before anything is overwritten, the previous install is copied to a root-only
  directory under `/var/backups/vm-mcp/`; the installer prints the path. That is an
  extra copy alongside U1's backup, not a replacement for it.
- If that backup fails the installer exits 9 with nothing changed.

Exit order in the pinned installer: 3 (token, or a settings change without the
override) and 7 (Yama precheck) come before the installer's backup; 9 means that
backup failed. Exit 8 (service user) and 5 (root not a directory) come after it, and 5
also after the service-user step. By then the `/var/backups/vm-mcp/` directory, package
installs and any service-user home change may already exist; the ptrace sysctl.d file
is rolled back on those failures. Use U6 for them.

### U5. Checks for the upgrade case

Run checks a–f below in order. Their b/e/f blocks load the persisted JSON target,
including custom port, socket, selected token source and profile. For non-personal
profiles the broker must be inactive and the privileged call must be policy-refused,
with no receipt for that probe. A failing check is not acceptance.

Also confirm preservation (read-only):

```bash
(
set -Eeuo pipefail
sudo -n python3 -I - <<'PY'
import json, pathlib, pwd, shlex, subprocess
B = pathlib.Path(pathlib.Path("/root/vm-mcp-upgrade.latest").read_text().strip())
target = json.loads((B / "target.json").read_text())
env = {}
for line in pathlib.Path("/etc/vm-mcp.env").read_text().splitlines():
    if "=" in line and not line.lstrip().startswith("#"):
        key, value = line.split("=", 1)
        words = shlex.split(value)
        env[key.strip()] = words[0] if len(words) == 1 else ""
failures = []
def check(label, passed):
    print(("PASS " if passed else "FAIL ") + label)
    if not passed:
        failures.append(label)
for key, field in (("VM_MCP_ROOT", "root"), ("VM_MCP_PROFILE", "profile"), ("VM_MCP_PORT", "port"), ("VM_MCP_ADMIN_SOCKET", "admin_socket")):
    check(key + " preserved", env.get(key) == target[field])
check("target service home", pwd.getpwnam("vmmcp").pw_dir == target["root"].rstrip("/") + "/.vm-mcp-home")
check("workspace not empty", any(p.name != ".vm-mcp-home" for p in pathlib.Path(target["root"]).iterdir()))
unit_result = subprocess.run(["systemctl", "show", "vm-mcp.service",
                              "--property=ReadWritePaths,ProtectSystem"], check=True, text=True, capture_output=True)
unit = dict(line.split("=", 1) for line in unit_result.stdout.splitlines() if "=" in line)
write_paths = shlex.split(unit.get("ReadWritePaths", ""))
check("effective ProtectSystem=strict", unit.get("ProtectSystem") == "strict")
check("effective workspace write boundary", len(write_paths) == 1
      and str(pathlib.Path(write_paths[0]).resolve()) == str(pathlib.Path(target["root"]).resolve()))
raise SystemExit(bool(failures))
PY
)
```

#### #127 non-destructive checks on an existing install

`vm-mcp-127-check.sh --skip-install` checks the installed tree without reinstalling,
but in that mode it has no source checkout, so its fixed-install-root and
workspace-overlap checks would fail falsely; and `--repo` alone turns `--skip-install`
off (it would reinstall). Never pass `--destructive` or `--reinstall-readonly` on a
real VM. Its step 3/7 expectations assume `personal-console`; use the executable profile-aware
checks b/f below instead of interpreting those false failures as acceptance. Run the source checks separately against the pinned
`e74ce1e` checkout (#130 and #131 do not change the installer's install-root or work-root
checks, or the token descriptor check):

```bash
(
ok() { if [ "$2" = "$3" ]; then echo "PASS $1"; else echo "FAIL $1 (want $2, got $3)"; fi; }
trap 'echo "FAIL source checks at line $LINENO (exit $?)" >&2' ERR
S=$(mktemp -d)
P=$(sudo -n mktemp /root/vm-mcp-token-probe.XXXXXX)
trap 'rm -rf "$S"; sudo -n rm -f "$P"' EXIT
git clone -q --filter=blob:none https://github.com/The-Interdependency/skill-lib.git "$S/sl"
git -C "$S/sl" checkout -q --detach e74ce1ee8a2cea50b0a6acce7697a6d3d9b2e128
I="$S/sl/vm-mcp/install.sh"
ok "fixed install root" 0 "$(grep -c VM_MCP_INSTALL_ROOT "$I" || true)"
ok "INSTALL_ROOT=/opt/vm-mcp" 1 "$(grep -cx 'INSTALL_ROOT=/opt/vm-mcp' "$I" || true)"
sed -n '/^check_work_root() {/,/^}/p' "$I" > "$S/cwr.sh"
for bad in / /opt /opt/vm-mcp /opt/vm-mcp/x /opt/vm-mcp/../vm-mcp; do
  ok "overlap $bad rejected" 1 "$(bash -c '. "$1"; check_work_root "$2" /opt/vm-mcp 2>/dev/null && echo 0 || echo 1' _ "$S/cwr.sh" "$bad")"
done
B=$(sudo -n cat /root/vm-mcp-upgrade.latest)
TARGET_ROOT=$(sudo -n python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["root"])' "$B/target.json")
TARGET_PROFILE=$(sudo -n python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["profile"])' "$B/target.json")
ok "preserved root $TARGET_ROOT accepted" 0 "$(bash -c '. "$1"; check_work_root "$2" /opt/vm-mcp 2>/dev/null && echo 0 || echo 1' _ "$S/cwr.sh" "$TARGET_ROOT")"
# token descriptor owner/mode check, against the installed code, with a throwaway file
probe() { sudo -n sh -c 'cd /opt/vm-mcp && .venv/bin/python -I -c "import sys; sys.path.insert(0,\".\"); import auth; auth._read_stdin_token()" < "$1"' _ "$P" >/dev/null 2>&1 && echo accepted || echo refused; }
sudo -n sh -c 'umask 077; head -c 48 /dev/urandom | base64 -w0 > "$1"; echo >> "$1"' _ "$P"
ok "token file 0600 root" accepted "$(probe)"
sudo -n chmod 0640 "$P"; ok "token file 0640 refused" refused "$(probe)"
sudo -n chmod 0604 "$P"; ok "token file 0604 refused" refused "$(probe)"
sudo -n chmod 0600 "$P"; sudo -n chown vmmcp "$P"; ok "token file owned by vmmcp refused" refused "$(probe)"
# step 9 sysctl handling, observed without changing the profile
if [ "$TARGET_PROFILE" = read-only ]; then
  ok "read-only: installer's own ptrace sysctl removed" absent "$(test -e /etc/sysctl.d/99-zz-vm-mcp-ptrace.conf && echo present || echo absent)"
else
  ok "shell profile: ptrace sysctl present" "root:root 644" "$(stat -c '%U:%G %a' /etc/sysctl.d/99-zz-vm-mcp-ptrace.conf 2>/dev/null)"
fi
)
```

The step 9 check is observational: on a `read-only` target the U4 install itself
exercises #127's removal path; on other profiles it is not exercised (that would need
a profile change) and stays covered by the scratch-VM run.

### U6. Roll back to the inventoried state

This is a recovery operation through the human path. **Old code may be
unauthenticated.** Prefer fixing forward; restoring a previously active old service
reopens that old exposure. Units that were inactive or disabled remain so. Review
that security consequence before running this block. It restores only the declared
deployment artifacts and service-user home, not application/workspace data, installed
OS packages, or a lowered live `ptrace_scope`. Do not use the profile-only `sed`
example later in this document as an upgrade rollback.

```bash
(
set -Eeuo pipefail
sudo -n python3 -I - <<'PY'
# U6 rollback: validate and stage completely before touching the live deployment.
import hashlib, json, os, pathlib, pwd, shutil, stat, subprocess, tarfile, tempfile

def deployment_manifest(paths):
    """Read names, content and preservation metadata without following symlinks."""
    records = {}
    pending = [pathlib.Path("/") / p for p in paths]
    while pending:
        path = pending.pop()
        if not os.path.lexists(path):
            continue
        info = os.lstat(path)
        record = {"kind": stat.S_IFMT(info.st_mode), "mode": stat.S_IMODE(info.st_mode),
                  "uid": info.st_uid, "gid": info.st_gid, "mtime_ns": info.st_mtime_ns,
                  "xattrs": {name: os.getxattr(path, name, follow_symlinks=False).hex()
                             for name in sorted(os.listxattr(path, follow_symlinks=False))}}
        if stat.S_ISLNK(info.st_mode):
            record["link"] = os.readlink(path)
        elif stat.S_ISDIR(info.st_mode):
            pending.extend(path.iterdir())
        elif stat.S_ISREG(info.st_mode):
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            record["sha256"] = digest.hexdigest()
        else:
            raise SystemExit("hmmm: unsupported special file in deployment snapshot")
        records[str(path)] = record
    return records

def require(condition, message):
    if not condition:
        raise AssertionError(message)

os.umask(0o077)
B = pathlib.Path(pathlib.Path("/root/vm-mcp-upgrade.latest").read_text().strip())
require((B / 'COMPLETE').read_text() == 'complete\n', 'incomplete backup')
state = json.loads((B / "state.json").read_text())
paths = ["opt/vm-mcp", "etc/vm-mcp.env",
         "etc/systemd/system/vm-mcp.service", "etc/systemd/system/vm-mcp-admin.service",
         "etc/systemd/system/vm-mcp.service.d", "etc/systemd/system/vm-mcp-admin.service.d",
         "etc/credstore/vm-mcp-token", "etc/sysctl.d/99-zz-vm-mcp-ptrace.conf"]
require(state['paths'] == paths and set(state['present']) <= set(paths), 'invalid backup manifest')
require(pwd.getpwnam('vmmcp').pw_uid == state['uid'], 'service account identity changed')
h = hashlib.sha256()
with (B / "state.tar").open("rb") as stream:
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        h.update(chunk)
require(h.hexdigest() == state['archive_sha256'], 'backup checksum mismatch')
staging = pathlib.Path(tempfile.mkdtemp(prefix="restore.", dir=B))
# Archive was made by U1 from exact paths, without following symlinks.
# Root-only backup ownership and checksum are trust prerequisites, not tar sandboxing.
tar_result = subprocess.run(["tar", "--acls", "--xattrs", "--xattrs-include=*", "-xpf", str(B / "state.tar"), "-C", str(staging)], check=True, capture_output=True)
require(not tar_result.stderr, "hmmm: archive operation warned; inspect backup/storage before continuing")
for path in state["present"]:
    require(os.path.lexists(staging / path), 'missing staged artifact')
# Keep the staging and displaced upgraded artifacts for recovery if copying fails.
displaced = pathlib.Path(tempfile.mkdtemp(prefix="displaced.", dir=B))
for unit in state["units"]:
    result = subprocess.run(["systemctl", "show", unit, "--property=LoadState", "--value"], check=True, text=True, capture_output=True)
    if result.stdout.strip() != "not-found":
        subprocess.run(["systemctl", "stop", unit], check=True)
        subprocess.run(["systemctl", "disable", unit], check=True)
probe = subprocess.run(["pgrep", "-u", str(state["uid"])], capture_output=True)
require(probe.returncode == 1, 'vmmcp processes remain; no files restored')
for path in paths:
    live = pathlib.Path("/") / path
    if os.path.lexists(live):
        saved = displaced / path
        saved.parent.mkdir(parents=True, exist_ok=True)
        # Move across filesystems if needed; preserve this inspection copy.
        shutil.move(str(live), str(saved))
    if path in state["present"]:
        live.parent.mkdir(parents=True, exist_ok=True)
        copy_result = subprocess.run(["cp", "-a", "--", str(staging / path), str(live)], check=True, capture_output=True)
        require(not copy_result.stderr, "hmmm: restore copy warned; leave services down and inspect")
    else:
        require(not os.path.lexists(live), 'new artifact was not removed')
require(deployment_manifest(paths) == state["deployment"], "restored deployment metadata/content differs; leave services down")
subprocess.run(["usermod", "--home", state["home"], "vmmcp"], check=True)
subprocess.run(["systemctl", "daemon-reload"], check=True)
for unit, prior in state["units"].items():
    if prior["UnitFileState"] == "enabled":
        subprocess.run(["systemctl", "enable", unit], check=True)
# Restore active state separately from boot enablement, broker before HTTP.
for unit in ("vm-mcp-admin.service", "vm-mcp.service"):
    if state["units"][unit]["ActiveState"] == "active":
        subprocess.run(["systemctl", "start", unit], check=True)
for unit, prior in state["units"].items():
    result = subprocess.run(["systemctl", "show", unit, "--property=LoadState,ActiveState,UnitFileState"], check=True, text=True, capture_output=True)
    now = dict(line.split("=", 1) for line in result.stdout.splitlines() if "=" in line)
    if now.get("LoadState") == "not-found":
        now["UnitFileState"] = "absent"
    require(now == prior, 'rollback unit state differs: ' + unit)
require(pwd.getpwnam('vmmcp').pw_dir == state['home'], 'home was not restored')
print("PASS deployment rollback; preserved upgraded artifacts in " + str(displaced))
PY
)
```

Keep the backup and displaced artifacts root-only until recovery is verified. If
restoration fails, leave services down and inspect through the human recovery path;
do not claim rollback success from a partial copy. The complete staged backup and
separately retained upgraded artifacts remain available. Workspace content is not
reverted or deleted; U4's installer changes there may need a separate reviewed repair.
### Worked example: a VM from an earlier vm-mcp release

A real upgrade on Oct 13, 2026 met this layout:

```text
version:          pre-#123 vm-mcp (no token)
/etc/vm-mcp.env:  VM_MCP_ROOT="/srv/a0/workspaces", VM_MCP_PORT=8765,
                  VM_MCP_SHELL_ENABLED=0, no VM_MCP_PROFILE, no token key
vmmcp home:       /srv/a0/workspaces/.vm-mcp-home
units:            vm-mcp.service active (running for days); broker unit inactive
listener:         127.0.0.1:8765
```

Following the fresh-install steps 1–2 verbatim failed with `usermod: user vmmcp is
currently used by process …` and exit 8, after the tests passed and the ptrace sysctl
file was written but before any code, unit or env changed; the old service kept
running. Had it succeeded, it would also have moved the service to an empty
`/srv/vm-mcp/workspace` and changed the profile.

With this section:

1. U1 records the layout above.
2. U2 resolves the profile from the legacy flag (`VM_MCP_SHELL_ENABLED=0` →
   `read-only`) and writes `TARGET_ROOT=/srv/a0/workspaces`, `TARGET_PROFILE=read-only`.
3. U4 stops the old service (brief outage), installs e74ce1e with those values, and
   the installer removes its own ptrace sysctl file again because the target is
   `read-only`.
4. U5 expects the read-only profile-aware checks, the preservation block all `PASS`,
   and the read-only step 9 line `absent`.
5. Any other profile for that VM is a separate, explicit decision in `target.json`.

## Install the exact canonical personal console

The pinned `e74ce1e` is the merge of The-Interdependency/skill-lib#131 (upgrade-safe
installer reruns, see U4), on top of #130 (`acd5e9f`, a first-use context notice from
vm-mcp; its privileged components record a one-time marker in a new root-only state
directory), #127 (`023ae12`) and #123 (`24029ca`).
 #127 hardens the installer and makes the server check its token
descriptor: fd 0 must be a regular file owned by root with no group or other bits. The
installer's `/etc/credstore/vm-mcp-token` (root, `0600`) satisfies that. From #123 on,
vm-mcp refuses every HTTP request, loopback included, that lacks
`Authorization: Bearer <token>`. Before it, any local process could reach
every local endpoint through the loopback listener. A VM running an older vm-mcp (for example
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
trap 'echo "FAIL step 2 at line $LINENO (exit $?)" >&2' ERR
umask 077

SKILL_LIB_SHA=e74ce1ee8a2cea50b0a6acce7697a6d3d9b2e128
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

rc=0
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

If any command fails, the ERR trap prints `FAIL step 2 at line N`, using the line number bash
reports, and the block stops. The clean-up trap runs when the block's subshell ends, so both clones are removed
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
`046c4cf` (Oct 11, 2026). vm-mcp at `24029ca` is identical to `046c4cf`. `023ae12` adds
#127, `acd5e9f` adds #130 and `e74ce1e` adds #131 on top; the scratch run covered none of them (hmmm), so a FAIL here may be new
behaviour, not an install mistake. Run them as
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

### b. Profile-appropriate services and loopback listener

Each of b, e and f independently loads the root-only `target.json` from U2/U3
through `/root/vm-mcp-upgrade.latest`. A missing pointer means fresh-install defaults;
a present but unreadable or invalid pointer/target is a failure, never a default.
The loader reads data as JSON, never shell code. The token default is the installed
credstore file, so a deleted fresh-install staging token does not break checks.

```bash
(
sudo -n python3 -I - <<'PY'
import json, os, stat
from pathlib import Path

def private_text(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd) as stream:
        st = os.fstat(stream.fileno())
        if not stat.S_ISREG(st.st_mode) or st.st_uid != 0 or st.st_mode & 0o077:
            raise ValueError("expected a root-only regular file")
        return stream.read()

def load_target():
    pointer = Path("/root/vm-mcp-upgrade.latest")
    if not os.path.lexists(pointer):
        return 8765, "personal-console", "/run/vm-mcp/admin.sock", "/etc/credstore/vm-mcp-token"
    B = Path(private_text(pointer).strip())
    if not B.is_absolute():
        raise ValueError("invalid upgrade backup path")
    target = json.loads(private_text(B / "target.json"))
    port = int(target["port"])
    profile, socket, token = (target[k] for k in ("profile", "admin_socket", "token_file"))
    if not 1 <= port <= 65535 or profile not in {"read-only", "workspace", "personal-console"}:
        raise ValueError("invalid upgrade target")
    if any(not isinstance(v, str) or not v.startswith("/") or "\n" in v or "\x00" in v for v in (socket, token)):
        raise ValueError("invalid target path")
    return port, profile, socket, token

try:
    CHECK_PORT, CHECK_PROFILE, CHECK_SOCKET, TOKEN_FILE = load_target()
except (OSError, ValueError, KeyError, TypeError):
    raise SystemExit("FAIL reading preserved verification target; repair U2/U3 before continuing")
failures = []
def check(label, probe):
    try:
        passed = bool(probe())
    except Exception:
        passed = False
    print(("PASS " if passed else "FAIL ") + label)
    if not passed:
        failures.append(label)
import grp, subprocess, time

def run(*args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode:
        raise OSError("inspection command failed")
    return result.stdout.strip()

def listeners():
    return [line.split()[3] for line in run("ss", "-ltnH").splitlines()
            if len(line.split()) >= 4 and line.split()[3].rsplit(":", 1)[-1] == str(CHECK_PORT)]

def await_listener():
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        if f"127.0.0.1:{CHECK_PORT}" in listeners():
            return True
        time.sleep(1)
    return False

def boundary(path, mode, kind):
    st = os.lstat(path)
    return (kind(st.st_mode) and st.st_uid == 0 and st.st_gid == grp.getgrnam("vmmcp").gr_gid
            and stat.S_IMODE(st.st_mode) == mode)

check("listening within 60 s", await_listener)
check("vm-mcp active", lambda: run("systemctl", "is-active", "vm-mcp.service") == "active")
check("one listener, loopback only", lambda: listeners() == [f"127.0.0.1:{CHECK_PORT}"])
check("service user", lambda: run("systemctl", "show", "-p", "User", "--value", "vm-mcp.service") == "vmmcp")
if CHECK_PROFILE == "personal-console":
    check("vm-mcp-admin active", lambda: run("systemctl", "is-active", "vm-mcp-admin.service") == "active")
    check("broker directory root:vmmcp 750", lambda: boundary(Path(CHECK_SOCKET).parent, 0o750, stat.S_ISDIR))
    check("broker socket root:vmmcp 660", lambda: boundary(CHECK_SOCKET, 0o660, stat.S_ISSOCK))
else:
    check("broker inactive for lower-authority profile", lambda:
          run("systemctl", "show", "-p", "ActiveState", "--value", "vm-mcp-admin.service") == "inactive")
    check("no broker socket for lower-authority profile", lambda: not os.path.lexists(CHECK_SOCKET))
raise SystemExit(bool(failures))
PY
)
```

Wait for the selected port first. Expect every check to pass. Lower-authority
profiles require an inactive broker and no socket; they do not require or enable
root execution. Inspection errors count as failures.

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

The selected root-only token file is read inside the root Python process. Headers
remain in memory, never in argv, shell variables, or persistent header files. Local
requests explicitly bypass proxy environment settings.

```bash
(
sudo -n python3 -I - <<'PY'
import json, os, stat
from pathlib import Path

def private_text(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd) as stream:
        st = os.fstat(stream.fileno())
        if not stat.S_ISREG(st.st_mode) or st.st_uid != 0 or st.st_mode & 0o077:
            raise ValueError("expected a root-only regular file")
        return stream.read()

def load_target():
    pointer = Path("/root/vm-mcp-upgrade.latest")
    if not os.path.lexists(pointer):
        return 8765, "personal-console", "/run/vm-mcp/admin.sock", "/etc/credstore/vm-mcp-token"
    B = Path(private_text(pointer).strip())
    if not B.is_absolute():
        raise ValueError("invalid upgrade backup path")
    target = json.loads(private_text(B / "target.json"))
    port = int(target["port"])
    profile, socket, token = (target[k] for k in ("profile", "admin_socket", "token_file"))
    if not 1 <= port <= 65535 or profile not in {"read-only", "workspace", "personal-console"}:
        raise ValueError("invalid upgrade target")
    if any(not isinstance(v, str) or not v.startswith("/") or "\n" in v or "\x00" in v for v in (socket, token)):
        raise ValueError("invalid target path")
    return port, profile, socket, token

try:
    CHECK_PORT, CHECK_PROFILE, CHECK_SOCKET, TOKEN_FILE = load_target()
except (OSError, ValueError, KeyError, TypeError):
    raise SystemExit("FAIL reading preserved verification target; repair U2/U3 before continuing")
failures = []
def check(label, probe):
    try:
        passed = bool(probe())
    except Exception:
        passed = False
    print(("PASS " if passed else "FAIL ") + label)
    if not passed:
        failures.append(label)
import re
import urllib.request, urllib.error
U = f"http://127.0.0.1:{CHECK_PORT}/mcp"
try:
    token = private_text(TOKEN_FILE).splitlines()[0]
    if not re.fullmatch(r"[A-Za-z0-9_-]{32,256}", token):
        raise ValueError("invalid token")
except (OSError, ValueError, IndexError):
    raise SystemExit("FAIL reading selected root-only token file")
INIT = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
    "protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "check", "version": "0"}}}
LIST = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
def request(payload, credential=None, scheme="Bearer"):
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if credential is not None:
        headers["Authorization"] = f"{scheme} {credential}"
    req = urllib.request.Request(U, data=json.dumps(payload).encode(), headers=headers)
    # Do not route a local credential through HTTP_PROXY/HTTPS_PROXY.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(req, timeout=15) as response:
            return response.status, response.read().decode()
    except urllib.error.HTTPError as error:
        return error.code, ""
check("no header", lambda: request(INIT)[0] == 401)
check("lowercase bearer, selected token", lambda: request(INIT, token, "bearer")[0] == 200)
check("wrong token", lambda: request(INIT, "wrong-token-wrong-token-wrong-token")[0] == 401)
check("unauthenticated tools/list", lambda: request(LIST)[0] == 401)
raise SystemExit(bool(failures))
PY
)
```

Expect four `PASS` lines. Nothing from this shell must survive for f. The server
accepts protocolVersion `2025-03-26`.

### f. Profile and privileged result through MCP, with a matching receipt

The pinned server is stateless (`stateless_http=True`); there is no session header
or initialized notification to carry between calls. This block reads its own target
and token, verifies `vm_info` (including the resolved root and its existence), and requires a harmless uniquely tagged privileged
probe to receive the canonical policy refusal for `read-only` and `workspace`,
without a broker receipt. Tools being listed does not mean those profiles permit them.

For `personal-console`, parse JSON or SSE JSON-RPC envelopes, then the actual
structured tool result. Assert root stdout, successful exit, `admin` mode, root
identity and no timeout; then match the exact returned request ID to a new journal
receipt with the same mode, run-as identity, digest and terminal status. Digest-only
or older `id -u` receipts cannot satisfy this check.

```bash
(
sudo -n python3 -I - <<'PY'
import json, os, stat
from pathlib import Path

def private_text(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd) as stream:
        st = os.fstat(stream.fileno())
        if not stat.S_ISREG(st.st_mode) or st.st_uid != 0 or st.st_mode & 0o077:
            raise ValueError("expected a root-only regular file")
        return stream.read()

def load_target():
    pointer = Path("/root/vm-mcp-upgrade.latest")
    if not os.path.lexists(pointer):
        return 8765, "personal-console", "/run/vm-mcp/admin.sock", "/etc/credstore/vm-mcp-token", str(Path("/srv/vm-mcp/workspace").resolve())
    B = Path(private_text(pointer).strip())
    if not B.is_absolute():
        raise ValueError("invalid upgrade backup path")
    target = json.loads(private_text(B / "target.json"))
    port = int(target["port"])
    profile, socket, token = (target[k] for k in ("profile", "admin_socket", "token_file"))
    if not 1 <= port <= 65535 or profile not in {"read-only", "workspace", "personal-console"}:
        raise ValueError("invalid upgrade target")
    if any(not isinstance(v, str) or not v.startswith("/") or "\n" in v or "\x00" in v for v in (socket, token)):
        raise ValueError("invalid target path")
    root = target["root"]
    if not isinstance(root, str) or not root.startswith("/") or any(c in root for c in ("\n", "\r", "\0")):
        raise ValueError("invalid workspace root")
    return port, profile, socket, token, str(Path(root).resolve())

try:
    CHECK_PORT, CHECK_PROFILE, CHECK_SOCKET, TOKEN_FILE, CHECK_ROOT = load_target()
except (OSError, ValueError, KeyError, TypeError):
    raise SystemExit("FAIL reading preserved verification target; repair U2/U3 before continuing")
failures = []
def check(label, probe):
    try:
        passed = bool(probe())
    except Exception:
        passed = False
    print(("PASS " if passed else "FAIL ") + label)
    if not passed:
        failures.append(label)
import re
import urllib.request, urllib.error
U = f"http://127.0.0.1:{CHECK_PORT}/mcp"
try:
    token = private_text(TOKEN_FILE).splitlines()[0]
    if not re.fullmatch(r"[A-Za-z0-9_-]{32,256}", token):
        raise ValueError("invalid token")
except (OSError, ValueError, IndexError):
    raise SystemExit("FAIL reading selected root-only token file")
INIT = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
    "protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "check", "version": "0"}}}
LIST = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
def request(payload, credential=None, scheme="Bearer"):
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if credential is not None:
        headers["Authorization"] = f"{scheme} {credential}"
    req = urllib.request.Request(U, data=json.dumps(payload).encode(), headers=headers)
    # Do not route a local credential through HTTP_PROXY/HTTPS_PROXY.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(req, timeout=15) as response:
            return response.status, response.read().decode()
    except urllib.error.HTTPError as error:
        return error.code, ""
import hashlib, subprocess, time
START = str(time.time())

def rpc(payload):
    status, body = request(payload, token)
    if status != 200:
        raise ValueError("MCP HTTP request failed")
    try:
        messages = [json.loads(body)]
    except ValueError:
        messages = [json.loads(event[5:].strip()) for event in body.splitlines() if event.startswith("data:")]
    replies = [m for m in messages if isinstance(m, dict) and m.get("id") == payload["id"]]
    if len(replies) != 1 or "error" in replies[0]:
        raise ValueError("missing or failed JSON-RPC result")
    result = replies[0]["result"]
    if result.get("isError", False):
        raise ValueError("MCP tool error")
    return result

def tool_result(result):
    value = result.get("structuredContent")
    if value is None:
        texts = [c["text"] for c in result.get("content", []) if c.get("type") == "text"]
        if len(texts) != 1:
            raise ValueError("missing structured tool result")
        value = json.loads(texts[0])
    if not isinstance(value, dict):
        raise ValueError("invalid tool result")
    return value

def call(name, arguments, identity):
    return tool_result(rpc({"jsonrpc": "2.0", "id": identity, "method": "tools/call",
                           "params": {"name": name, "arguments": arguments}}))

def target_matches():
    info = call("vm_info", {}, 3)
    return (info.get("ok") is True and info.get("profile") == CHECK_PROFILE
            and info.get("admin_socket") == CHECK_SOCKET
            and info.get("root") == CHECK_ROOT and info.get("root_exists") is True)

check("authenticated profile, broker path and resolved workspace root", target_matches)
if failures:
    raise SystemExit(1)  # Do not attempt privilege after a target mismatch.
# Lower profiles must return the canonical policy refusal, not a transport error.
if CHECK_PROFILE != "personal-console":
    import uuid
    probe_command = "id -u # vm-mcp-policy-check-" + uuid.uuid4().hex
    probe_digest = hashlib.sha256(probe_command.encode()).hexdigest()
    def refused():
        denied = call("admin_exec", {"command": probe_command, "cwd": "/"}, 4)
        return (denied.get("ok") is False and denied.get("error_type") == "PermissionError"
                and denied.get("error") == "host execution is disabled; set VM_MCP_PROFILE=personal-console")
    check("privileged call refused by profile policy", refused)
    def no_probe_receipt():
        journal = subprocess.run(["journalctl", "-u", "vm-mcp-admin.service", "--since", "@" + START,
                                  "--no-pager", "-o", "cat"], capture_output=True, text=True)
        if journal.returncode:
            return False
        for line in journal.stdout.splitlines():
            try:
                receipt = json.loads(line)
            except ValueError:
                continue
            if isinstance(receipt, dict) and receipt.get("command_sha256") == probe_digest:
                return False
        return True
    check("no broker receipt for refused probe", no_probe_receipt)
    raise SystemExit(bool(failures))
T = "admin_exec"  # canonical skill-lib e74ce1e server.py
check("privileged tool listed", lambda: T in {t["name"] for t in rpc(LIST)["tools"]})
SHA = hashlib.sha256(b"id -u").hexdigest()
result = {}
def root_result():
    result.update(call(T, {"command": "id -u", "cwd": "/"}, 4))
    return (result.get("ok") is True and result.get("mode") == "admin"
            and result.get("run_as") == "root" and type(result.get("uid")) is int and result["uid"] == 0
            and type(result.get("exit_code")) is int and result["exit_code"] == 0
            and result.get("stdout") == "0\n" and result.get("timed_out") is False
            and result.get("stdout_truncated") is False and result.get("command_sha256") == SHA
            and result.get("cwd") == "/" and bool(result.get("request_id")))
check("privileged root stdout, identity, mode and exit", root_result)

def receipt_matches():
    journal = subprocess.run(["journalctl", "-u", "vm-mcp-admin.service", "--since", "@" + START,
                              "--no-pager", "-o", "cat"], capture_output=True, text=True)
    if journal.returncode or not result.get("request_id"):
        return False
    for line in journal.stdout.splitlines():
        try:
            receipt = json.loads(line)
        except ValueError:
            continue
        if (isinstance(receipt, dict) and receipt.get("event") == "vm_mcp_exec"
                and receipt.get("request_id") == result["request_id"]
                and receipt.get("mode") == "admin" and receipt.get("run_as") == "root"
                and receipt.get("cwd") == "/" and receipt.get("command_sha256") == SHA
                and type(receipt.get("exit_code")) is int and receipt["exit_code"] == 0
                and receipt.get("timed_out") is False):
            return True
    return False
check("broker receipt bound to this root call", receipt_matches)
raise SystemExit(bool(failures))
PY
)
```

Expect four `PASS` lines for `personal-console`; lower profiles produce three `PASS` lines
including the canonical policy refusal and absence of a probe receipt. Any `FAIL` makes the block exit nonzero.
The broker receipt has no peer PID; the pinned broker verifies the service MainPID
before execution, so only a successful root result plus its receipt proves this path.

Acceptance requires a through f for the selected target:

```text
MCP listener:       127.0.0.1:<selected port> only
vm-mcp.service:     User=vmmcp; non-root hardening retained; no token in environment or fds
profile:            preserved target, or fresh-install personal-console
personal-console:   separate privileged unit; selected AF_UNIX socket only
broker directory:   root:vmmcp mode 750
broker socket:      root:vmmcp mode 660
lower profiles:     broker inactive; selected socket absent; privileged probe policy-refused
HTTP:               401 without or with a wrong bearer token
human recovery:     still independently usable
```

A listener on a wildcard or a VM public/private interface at the selected port is
a stop condition. Repository mock tests verify this runbook, not live VM acceptance.

## Connect the MCP client privately

Use the client's current authenticated private-network/tunnel mechanism. Do not publish
port `8765` to the internet and do not put SSH private keys, service-account keys,
refresh tokens, or sudo passwords into MCP arguments or prompts.

The client must also send the bearer token on every request: the tunnel alone does not
authenticate, because every local process can reach loopback. Configure it as a
header in the client's secret or secure-header settings for this server, never in the
URL, a tool argument, a prompt or a repository file:

```text
Authorization: Bearer <contents of /etc/credstore/vm-mcp-token>
```

Use the installed `/etc/credstore/vm-mcp-token` copy for every client transfer,
regardless of the original U3/U4 token source. Move its value without printing it. Don't `cat` it in an
interactive SSH session, because it would stay in the terminal scrollback. Run one of
these from the machine where the client is configured. The token travels only through
the pipe. Use your usual human access for `ssh` (for example `gcloud compute ssh VM
--zone ZONE --tunnel-through-iap --command '...'` for IAP/OS Login):

```text
# into the clipboard, then paste into the client's secret header field and clear the clipboard
ssh VM 'sudo -n cat /etc/credstore/vm-mcp-token' | tr -d '\n' | pbcopy          # macOS
ssh VM 'sudo -n cat /etc/credstore/vm-mcp-token' | tr -d '\n' | wl-copy         # Wayland (xclip -selection clipboard on X11)

# or into a local 0600 file that the client's secret configuration reads
(umask 077 && mkdir -p -m 700 ~/.config/vm-mcp && rm -f ~/.config/vm-mcp/token &&
  ssh VM 'sudo -n cat /etc/credstore/vm-mcp-token' | tr -d '\n' > ~/.config/vm-mcp/token)

# the same through IAP
(umask 077 && mkdir -p -m 700 ~/.config/vm-mcp && rm -f ~/.config/vm-mcp/token &&
  gcloud compute ssh VM --zone ZONE --tunnel-through-iap \
    --command 'sudo -n cat /etc/credstore/vm-mcp-token' | tr -d '\n' > ~/.config/vm-mcp/token)
```

**For an agent client** (ChatGPT, Claude, Codex, Grok Bot or similar), the token goes
only in the MCP connector's secret or header configuration (`Authorization: Bearer ...`).
Never type, paste or upload it into the conversation itself, and never ask the agent to
read `/etc/credstore/vm-mcp-token` through MCP. Anything in the conversation is model context.

Never delete the installed `/etc/credstore/vm-mcp-token`: the service needs it.
A separate provisioning source such as `/root/vm-mcp.token` can be retained under
your secret handling or deleted after successful client setup. If deleting the
selected upgrade source, first change `target.json`'s `token_file` to the installed
copy so later e/f checks still have their selected source. Remember that every
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
<privileged tool>(command="id -u", cwd="/")
```

Expected distinctions:

```text
shell_exec: vmmcp / non-root
user_exec:  requested non-root account
privileged: as documented in skill-lib vm-mcp/SKILL.md
```

Then inspect the broker audit trail:

```bash
sudo -n journalctl -u vm-mcp-admin.service --no-pager -n 50
```

The journal should make mode, run-as identity, cwd, command digest, and terminal
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

<privileged tool>(
  cwd="/",
  command="systemctl --no-pager --full status stack-orchestrator-worker.service"
)
```

Use ordinary authority when it is sufficient; use the privileged tool only when it is
actually required. This is an observability preference, not an artificial capability
restriction.

## Rollback

Return the MCP layer to read-only without removing human recovery:

```bash
sudo -n sed -i 's/^VM_MCP_PROFILE=.*/VM_MCP_PROFILE=read-only/' /etc/vm-mcp.env
sudo -n systemctl disable --now vm-mcp-admin.service
sudo -n systemctl restart vm-mcp.service
```

Under `read-only`, `tools/list` still advertises the host and privileged tools.
Calling them returns `PermissionError`,
`vm-mcp-admin` is inactive and `admin.sock` is gone. Bearer authentication stays
required.

This `sed` rollback does not run the installer, so `/etc/sysctl.d/99-zz-vm-mcp-ptrace.conf`
stays in place and the ptrace scope stays at 1 or higher. To remove it too, rerun the
step 2 install block with `VM_MCP_PROFILE=read-only` and a token source. Since
skill-lib#127, the installer's read-only path deletes only its own
`99-zz-vm-mcp-ptrace.conf`, and only after `/etc/vm-mcp.env` is written and
`vm-mcp.service` has restarted successfully. A file it didn't write is kept, with a
warning. The live ptrace scope is left as it is until the next reboot or `sysctl --system`.

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
- Installer reruns are not history-preserving by themselves (root/profile defaults,
  dropped legacy keys, busy-user `usermod`). The upgrade section works around this;
  installer-side fixes are tracked as a skill-lib follow-up.
- The broad `personal-console` profile is intentional for this single-owner deployment;
  it should not be silently generalized to shared or multi-owner hosts.
