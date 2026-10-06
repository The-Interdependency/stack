#!/usr/bin/env bash
set -euo pipefail

# === MODULE_BUILD ===
# id: stack_worker_sandbox_run
#   module_name: worker_sandbox_run
#   module_kind: adapter
#   summary: runs one command as a transient systemd service with the fresh-making worker unit's user, environment file and sandbox properties
#   owner: stack
#   public_surface: backend/ops/worker_sandbox_run.sh
#   internal_surface: systemd-run --wait --pipe --collect with [Service] properties read from the worker unit
#   auth_boundary: admin
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: true
#   tests: bash -n plus VM acceptance (sandboxed identity probe in install_msdmd_runtime.sh)
#   rollout: operator tool on the stack VM
#   rollback: none needed; it changes nothing persistent
# === END MODULE_BUILD ===

# Usage: sudo backend/ops/worker_sandbox_run.sh [--chdir DIR] [--setenv NAME=VALUE]... -- COMMAND [ARG...]
#   STACK_WORKER_UNIT_FILE  unit whose [Service] properties are applied (default: the installed
#                           /etc/systemd/system/stack-orchestrator-worker.service, else the repo copy)
# The generator identity depends on PATH, Node, the venv and the sandbox, so
# probes and status checks that must match the worker run through this wrapper
# instead of an operator shell. The exit status of COMMAND is propagated.

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
unit="${STACK_WORKER_UNIT_FILE:-/etc/systemd/system/stack-orchestrator-worker.service}"
[[ -f "$unit" ]] || unit="$here/../deploy/stack-orchestrator-worker.service"
[[ -f "$unit" ]] || { echo "hmmm: worker unit file not found: $unit" >&2; exit 2; }
command -v systemd-run >/dev/null || { echo "hmmm: systemd-run is not available" >&2; exit 2; }

extra=()
chdir=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --chdir) chdir="$2"; extra+=("--working-directory=$2"); shift 2 ;;
    --setenv) extra+=("--setenv=$2"); shift 2 ;;
    --) shift; break ;;
    *) break ;;
  esac
done
[[ $# -gt 0 ]] || { echo "usage: $0 [--chdir DIR] [--setenv NAME=VALUE]... -- COMMAND [ARG...]" >&2; exit 2; }

# Properties that shape what the worker process can see or do.
allowed=" User Group WorkingDirectory EnvironmentFile Environment UMask NoNewPrivileges PrivateTmp
  ProtectHome ProtectSystem ReadWritePaths ReadOnlyPaths InaccessiblePaths RestrictAddressFamilies
  LockPersonality MemoryDenyWriteExecute SystemCallFilter SystemCallArchitectures RestrictNamespaces
  RestrictRealtime PrivateDevices ProtectKernelTunables ProtectKernelModules ProtectControlGroups
  CapabilityBoundingSet AmbientCapabilities "
allowed="${allowed//$'\n'/ }"
props=()
section=""
while IFS= read -r line || [[ -n "$line" ]]; do
  line="${line#"${line%%[![:space:]]*}"}"
  line="${line%"${line##*[![:space:]]}"}"
  [[ -z "$line" || "$line" == \#* || "$line" == \;* ]] && continue
  if [[ "$line" =~ ^\[(.*)\]$ ]]; then section="${BASH_REMATCH[1]}"; continue; fi
  [[ "$section" == "Service" && "$line" == *=* ]] || continue
  key="${line%%=*}"
  [[ -n "$chdir" && "$key" == "WorkingDirectory" ]] && continue
  [[ "$allowed" == *" $key "* ]] && props+=("--property=$line")
done < "$unit"

exec systemd-run --wait --pipe --collect --quiet "${props[@]}" "${extra[@]}" -- "$@"
