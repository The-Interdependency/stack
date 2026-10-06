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
#   tests: bash -n plus VM install acceptance (generator identity reports node and typescript versions)
#   rollout: run by the operator after each skill-lib snapshot refresh, before restarting the worker
#   rollback: reinstall from the previous pinned skill-lib snapshot; derivations re-key on the new generator identity
# === END MODULE_BUILD ===

# Usage: backend/ops/install_msdmd_runtime.sh
#   STACK_VENV            default /srv/stack/.venv (the worker's interpreter)
#   STACK_SKILL_LIB_ROOT  default /srv/stack/skill-lib (must match the worker env)
# Without these runtimes the collector exits 3 and fresh-making fails closed
# (exit 4: target helper older than the output; exit 5: git cannot list files).

venv="${STACK_VENV:-/srv/stack/.venv}"
skill_root="${STACK_SKILL_LIB_ROOT:-/srv/stack/skill-lib}"
msdmd="$skill_root/msdmd"

[[ -x "$venv/bin/python" ]] || { echo "hmmm: no venv interpreter at $venv/bin/python" >&2; exit 2; }
[[ -f "$msdmd/requirements.txt" && -f "$msdmd/package-lock.json" ]] || {
  echo "hmmm: $msdmd is not a skill-lib msdmd generator root" >&2; exit 2; }
command -v node >/dev/null && command -v npm >/dev/null || {
  echo "hmmm: node and npm are required for the TypeScript reader" >&2; exit 2; }

"$venv/bin/python" -m pip install -r "$msdmd/requirements.txt"
npm ci --ignore-scripts --prefix "$msdmd"

# Report what the worker will fingerprint; node/typescript must not be "absent".
PYTHONPATH="$skill_root" "$venv/bin/python" -m msdmd.collect --print-generator-identity --json
