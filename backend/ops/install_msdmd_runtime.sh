#!/usr/bin/env bash
set -euo pipefail

# === MODULE_BUILD ===
# id: stack_msdmd_runtime_install
#   module_name: msdmd_runtime_install
#   module_kind: worker
#   summary: installs the pinned MSDMD native reader runtimes into the stack venv and the skill-lib generator root used by fresh-making
#   owner: stack
#   public_surface: backend/ops/install_msdmd_runtime.sh
#   internal_surface: pip install -r <skill-lib>/msdmd/requirements.txt, npm ci --ignore-scripts --prefix <skill-lib>/msdmd
#   auth_boundary: write
#   storage_boundary: write
#   network_boundary: outbound package registry during install only
#   user_data_boundary: none
#   admin_only: true
#   tests: bash -n, backend.tests.test_install_script (stubbed tools), plus VM install acceptance (sandboxed identity reports node and typescript versions)
#   rollout: run by the operator with sudo -E after each skill-lib snapshot refresh, before restarting the worker
#   rollback: reinstall from the previous pinned skill-lib snapshot; derivations re-key on the new generator identity
# === END MODULE_BUILD ===

# Usage: sudo -E backend/ops/install_msdmd_runtime.sh
#   STACK_VENV            default /srv/stack/.venv (the worker's interpreter)
#   STACK_SKILL_LIB_ROOT  default /srv/stack/skill-lib (must match the worker env)
#   STACK_WORKER_USER     default stackorchestrator (must exist; installed trees must be readable by it)
#   STACK_SANDBOX_PROBE   "skip" to skip the sandboxed probe (non-root dev hosts only; prints hmmm)
# Exit: 2 bad input, 3 node or typescript absent / probe failed, 4 sandboxed probe not run.
# Without these runtimes the collector exits 3 and fresh-making fails closed
# (exit 4: target helper older than the output; exit 5: git cannot list files).
# hmmm: pip hash-checking (--require-hashes) is not used; skill-lib's
# msdmd/requirements.txt pins versions but publishes no hashes.

# Installed files must be readable by the worker user, whatever the caller's umask.
umask 022

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
venv="${STACK_VENV:-/srv/stack/.venv}"
skill_root="${STACK_SKILL_LIB_ROOT:-/srv/stack/skill-lib}"
worker_user="${STACK_WORKER_USER:-stackorchestrator}"
msdmd="$skill_root/msdmd"

[[ -x "$venv/bin/python" ]] || { echo "hmmm: no venv interpreter at $venv/bin/python" >&2; exit 2; }
[[ -f "$msdmd/requirements.txt" && -f "$msdmd/package-lock.json" ]] || {
  echo "hmmm: $msdmd is not a skill-lib msdmd generator root" >&2; exit 2; }
command -v node >/dev/null && command -v npm >/dev/null || {
  echo "hmmm: node and npm are required for the TypeScript reader" >&2; exit 2; }
id -u "$worker_user" >/dev/null 2>&1 || {
  echo "hmmm: worker user $worker_user does not exist; create it or set STACK_WORKER_USER" >&2; exit 2; }

"$venv/bin/python" -m pip install -r "$msdmd/requirements.txt"
npm ci --ignore-scripts --prefix "$msdmd"

# Same flags as backend/msdmd.py: cwd at the generator root and -P (Python 3.11+).
safe_path=()
"$venv/bin/python" -c 'import sys; sys.exit(sys.version_info < (3, 11))' && safe_path=(-P)
probe=("$venv/bin/python" "${safe_path[@]}" -m msdmd.collect --print-generator-identity --json)

# Fail unless the probe succeeded and reports both Node and TypeScript.
require_runtimes() {
  local label="$1" output="$2"
  printf '%s\n' "$output" | "$venv/bin/python" -c '
import json, sys
label = sys.argv[1]
try:
    data = json.load(sys.stdin)
except ValueError:
    sys.exit("hmmm: " + label + ": identity probe printed no JSON")
print(json.dumps(data, indent=2, sort_keys=True))
missing = [key for key in ("node", "typescript") if data.get(key) in (None, "", "absent")]
if missing:
    sys.exit("hmmm: " + label + ": " + ", ".join(missing) + " absent; the TypeScript reader cannot run there")
' "$label" || exit 3
}

echo "== generator identity in this shell"
if ! shell_identity="$(cd "$skill_root" && PYTHONPATH="$skill_root" "${probe[@]}")"; then
  echo "hmmm: identity probe failed in this shell" >&2; exit 3
fi
require_runtimes "this shell" "$shell_identity"

# The worker runs as $worker_user inside its systemd sandbox (MemoryDenyWriteExecute,
# ProtectSystem, its own PATH). Probe there too; that is the identity it records.
if [[ "${STACK_SANDBOX_PROBE:-}" == "skip" ]]; then
  echo "hmmm: sandboxed probe skipped (STACK_SANDBOX_PROBE=skip); the worker may still be unable to run Node" >&2
  exit 0
fi
if [[ "$(id -u)" -ne 0 ]] || ! command -v systemd-run >/dev/null; then
  echo "hmmm: sandboxed probe needs root and systemd-run; rerun with sudo -E, or set STACK_SANDBOX_PROBE=skip on a dev host" >&2
  exit 4
fi
echo "== generator identity inside the worker unit's sandbox (user $worker_user)"
if ! sandbox_identity="$("$here/worker_sandbox_run.sh" --chdir "$skill_root" --setenv "PYTHONPATH=$skill_root" -- "${probe[@]}")"; then
  echo "hmmm: identity probe failed inside the worker sandbox (see journalctl for the transient unit)" >&2; exit 3
fi
require_runtimes "worker sandbox" "$sandbox_identity"
