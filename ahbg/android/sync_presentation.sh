#!/usr/bin/env bash
# Sync the canonical presentation board into Android assets.
#
# The mobile layer bundles a pinned copy of ahbg/presentation so the board can
# render even when the runtime bridge is unreachable (presentation-only mode).
# Authority stays with ahbg/presentation: this script copies the three UI files
# and records their SHA256 digests so drift is visible in review.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$ROOT/ahbg/presentation"
DST="$ROOT/ahbg/android/app/src/main/assets"
mkdir -p "$DST"

cp "$SRC/board.html" "$SRC/board.js" "$SRC/board.css" "$SRC/sample_snapshot.json" "$DST/"

(
  cd "$DST"
  sha256sum board.html board.js board.css sample_snapshot.json > PRESENTATION.sha256
)

echo "synced presentation assets to $DST"
cat "$DST/PRESENTATION.sha256"
