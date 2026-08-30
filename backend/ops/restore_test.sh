#!/usr/bin/env bash
set -euo pipefail
umask 077

# === MODULE_BUILD ===
# id: stack_postgres_restore_drill
#   module_name: postgres_restore_drill
#   module_kind: worker
#   summary: verifies an independent backup by restoring it only into an explicitly separate test database
#   owner: stack
#   public_surface: backend/ops/restore_test.sh
#   internal_surface: sha256sum, pg_restore
#   auth_boundary: write
#   storage_boundary: delete
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: true
#   tests: bash -n plus VM restore acceptance drill
#   rollout: manual acceptance drill before enabling backup timer
#   rollback: recreate disposable restore-test database; production database is never a permitted target
# === END MODULE_BUILD ===

# === BOUNDARIES ===
# id: stack_postgres_restore_test_boundary
#   summary: performs destructive clean restore only against a DSN proven different from the production DSN
#   auth_boundary: write
#   storage_boundary: delete
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: true
#   side_effects: database
#   owner: stack
# === END BOUNDARIES ===

: "${STACK_DATABASE_URL:?STACK_DATABASE_URL is required}"
: "${STACK_RESTORE_TEST_DATABASE_URL:?STACK_RESTORE_TEST_DATABASE_URL is required}"

if [[ "$STACK_DATABASE_URL" == "$STACK_RESTORE_TEST_DATABASE_URL" ]]; then
  echo "refusing restore drill against production database" >&2
  exit 2
fi

MIRROR_ROOT="${STACK_BACKUP_MIRROR_ROOT:-/mnt/stack-orchestrator-backups}"
BACKUP_DIR="${MIRROR_ROOT}/postgres"
if [[ ! -d "$MIRROR_ROOT" ]] || ! mountpoint -q "$MIRROR_ROOT"; then
  echo "hmmm: independent backup mount is unavailable: ${MIRROR_ROOT}" >&2
  exit 2
fi

backup="${1:-}"
if [[ -z "$backup" ]]; then
  backup="$(find "$BACKUP_DIR" -maxdepth 1 -type f -name 'stack-orchestrator-*.dump' -print | sort | tail -n 1)"
fi
if [[ -z "$backup" || ! -f "$backup" ]]; then
  echo "no backup selected/found" >&2
  exit 2
fi

checksum_file="${backup}.sha256"
if [[ ! -f "$checksum_file" ]]; then
  echo "checksum file missing: $checksum_file" >&2
  exit 2
fi

(
  cd "$(dirname "$backup")"
  sha256sum --check "$(basename "$checksum_file")"
)
pg_restore --list "$backup" >/dev/null
pg_restore \
  --dbname="$STACK_RESTORE_TEST_DATABASE_URL" \
  --clean --if-exists --no-owner --no-acl \
  "$backup"

printf 'restore drill succeeded: %s\n' "$backup"
