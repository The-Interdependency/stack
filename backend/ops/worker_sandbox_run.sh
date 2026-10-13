#!/usr/bin/env bash
set -euo pipefail

# === MODULE_BUILD ===
# id: stack_worker_sandbox_run
#   module_name: worker_sandbox_run
#   module_kind: adapter
#   summary: runs one command as a transient systemd service with the fresh-making worker unit's user, environment file and sandbox properties
#   owner: stack
#   public_surface: backend/ops/worker_sandbox_run.sh
#   internal_surface: systemctl show (loaded unit plus drop-ins) -> systemd-run --wait --pipe --collect properties
#   auth_boundary: admin
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: true
#   tests: backend.tests.test_worker_sandbox_run (stubbed systemctl/systemd-run) plus VM acceptance
#   rollout: operator tool on the stack VM
#   rollback: none needed; it changes nothing persistent
# === END MODULE# Usage: sudo backend/ops/worker_sandbox_run.sh [--chdir DIR] [--setenv NAME=VALUE]... -- COMMAND [ARG...]
#   STACK_WORKER_UNIT  installed worker unit (default stack-orchestrator-worker.service)
#   STACK_WORKER_USER  User= the unit must run as (default stackorchestrator)
# The generator identity depends on PATH, Node, the venv and the sandbox, so
# probes and status checks that must match the worker run through this wrapper
# instead of an operator shell. Properties come from `systemctl show`, i.e. the
# loaded unit with its drop-ins, not from parsing a unit file. The wrapper
# fails closed (exit 2) unless the unit is loaded, runs as STACK_WORKER_USER and
# has MemoryDenyWriteExecute=yes. The exit status of COMMAND is propagated.

unit="${STACK_WORKER_UNIT:-stack-orchestrator-worker.service}"
expected_user="${STACK_WORKER_USER:-stackorchestrator}"
command -v systemctl >/dev/null || { echo "hmmm: systemctl is not available" >&2; exit 2; }
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
keys=(User Group WorkingDirectory EnvironmentFiles Environment UMask NoNewPrivileges PrivateTmp
      ProtectHome ProtectSystem ReadWritePaths ReadOnlyPaths InaccessiblePaths
      RestrictAddressFamilies LockPersonality MemoryDenyWriteExecute)
show=(-p LoadState)
for key in "${keys[@]}"; do show+=(-p "$key"); done
if ! shown="$(systemctl show "${show[@]}" -- "$unit")"; then
  echo "hmmm: systemctl show failed for $unit" >&2; exit 2
fi

declare -A value=()
env_files=()
while IFS= read -r line; do
  [[ "$line" == *=* ]] || continue
  key="${line%%=*}"
  if [[ "$key" == "EnvironmentFiles" ]]; then
    # "<path> (ignore_errors=yes|no)", one line per file.
    entry="${line#*=}"
    path="${entry% (ignore_errors=*}"
    [[ -n "$path" ]] || continue
    [[ "$entry" == *"(ignore_errors=yes)" ]] && path="-$path"
    env_files+=("$path")
  else
    value[$key]="${line#*=}"
  fi
done <<< "$shown"

[[ "${value[LoadState]:-}" == "loaded" ]] || {
  echo "hmmm: $unit is not loaded (LoadState=${value[LoadState]:-missing}); install it and run systemctl daemon-reload" >&2; exit 2; }
[[ "${value[User]:-}" == "$expected_user" ]] || {
  echo "hmmm: $unit User=${value[User]:-missing}, expected $expected_user; refusing to probe as another identity" >&2; exit 2; }
[[ "${value[MemoryDenyWriteExecute]:-}" == "yes" ]] || {
  echo "hmmm: $unit MemoryDenyWriteExecute=${value[MemoryDenyWriteExecute]:-missing}, expected yes; refusing a probe that would not match the hardened worker" >&2; exit 2; }

props=()
for path in "${env_files[@]}"; do props+=("--property=EnvironmentFile=$path"); done
for key in "${keys[@]}"; do
  [[ "$key" == "EnvironmentFiles" ]] && continue
  [[ -n "$chdir" && "$key" == "WorkingDirectory" ]] && continue
  v="${value[$key]:-}"
  [[ -n "$v" ]] && props+=("--property=$key=$v")
done

exec systemd-run --wait --pipe --collect --quiet "${props[@]}" "${extra[@]}" -- "$@"
