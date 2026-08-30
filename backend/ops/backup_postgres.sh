#!/usr/bin/env bash
set -euo pipefail
umask 077

# === MODULE_BUILD ===
# id: stack_postgres_backup
#   module_name: postgres_backup
#   module_kind: worker
#   summary: creates, validates, hashes, mirrors, and ages orchestration database backups
#   owner: stack
#   public_surface: backend/ops/backup_postgres.sh
#   internal_surface: pg_dump, pg_restore, sha256sum, independent mount verification
#   auth_boundary: read
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: true
#   tests: bash -n plus VM backup/restore acceptance drill
#   rollout: stack-orchestrator-backup.timer
#   rollback: disable timer; retained custom-format dumps remain readable by pg_restore
# === END MODULE_BUILD ===

# === BOUNDARIES ===
# id: stack_postgres_backup_storage
#   summary: reads the orchestration database and writes verified dumps to local recovery storage plus an independently mounted mirror
#   auth_boundary: read
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: true
#   side_effects: database, filesystem
#   owner: stack
# === END BOUNDARIES ===

: "${STACK_DATABASE_URL:?STACK_DATABASE_URL is required}"

LOCAL_DIR="${STACK_BACKUP_LOCAL_DIR:-/var/backups/stack-orchestrator/postgres}"
MIRROR_ROOT="${STACK_BACKUP_MIRROR_ROOT:-/mnt/stack-orchestrator-backups}"
MIRROR_DIR="${MIRROR_ROOT}/postgres"
LOCAL_RETENTION_DAYS="${STACK_BACKUP_LOCAL_RETENTION_DAYS:-14}"
MIRROR_RETENTION_DAYS="${STACK_BACKUP_MIRROR_RETENTION_DAYS:-60}"

for cmd in pg_dump pg_restore sha256sum stat mountpoint install find; do
  command -v "$cmd" >/dev/null
done

mkdir -p "$LOCAL_DIR"
stamp="$(date -u +'%Y%m%dT%H%M%SZ')"
name="stack-orchestrator-${stamp}.dump"
tmp="$(mktemp "${LOCAL_DIR}/.${name}.XXXXXX")"
trap 'rm -f "$tmp"' EXIT

pg_dump --dbname="$STACK_DATABASE_URL" --format=custom --no-owner --no-acl --file="$tmp"
pg_restore --list "$tmp" >/dev/null
hash="$(sha256sum "$tmp" | awk '{print $1}')"
final="${LOCAL_DIR}/${name}"
mv "$tmp" "$final"
trap - EXIT
printf '%s  %s\n' "$hash" "$name" > "${final}.sha256"

find "$LOCAL_DIR" -maxdepth 1 -type f -name 'stack-orchestrator-*.dump' \
  -mtime "+${LOCAL_RETENTION_DAYS}" -delete
find "$LOCAL_DIR" -maxdepth 1 -type f -name 'stack-orchestrator-*.dump.sha256' \
  -mtime "+${LOCAL_RETENTION_DAYS}" -delete

if [[ ! -d "$MIRROR_ROOT" ]] || ! mountpoint -q "$MIRROR_ROOT"; then
  echo "hmmm: independent backup mount is unavailable: ${MIRROR_ROOT}" >&2
  echo "local verified recovery dump retained: ${final}" >&2
  exit 2
fi

local_dev="$(stat -c '%d' "$LOCAL_DIR")"
mirror_dev="$(stat -c '%d' "$MIRROR_ROOT")"
if [[ "$local_dev" == "$mirror_dev" ]]; then
  echo "hmmm: backup mirror shares the local filesystem device: ${MIRROR_ROOT}" >&2
  echo "local verified recovery dump retained: ${final}" >&2
  exit 2
fi

mkdir -p "$MIRROR_DIR"
install -m 0600 "$final" "${MIRROR_DIR}/${name}"
install -m 0600 "${final}.sha256" "${MIRROR_DIR}/${name}.sha256"
(
  cd "$MIRROR_DIR"
  sha256sum --check "${name}.sha256" >/dev/null
)
pg_restore --list "${MIRROR_DIR}/${name}" >/dev/null

find "$MIRROR_DIR" -maxdepth 1 -type f -name 'stack-orchestrator-*.dump' \
  -mtime "+${MIRROR_RETENTION_DAYS}" -delete
find "$MIRROR_DIR" -maxdepth 1 -type f -name 'stack-orchestrator-*.dump.sha256' \
  -mtime "+${MIRROR_RETENTION_DAYS}" -delete

printf 'backup=%s sha256=%s mirror=%s\n' "$final" "$hash" "${MIRROR_DIR}/${name}"
