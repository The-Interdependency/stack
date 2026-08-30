#!/bin/bash
# Run this from anywhere on the server to generate + serve the AHBG web viewer.

set -e

# Find the grok directory relative to this script or common locations
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GROK_DIR=""

for cand in \
  "$GROK_DIR" \
  "$SCRIPT_DIR/.." \
  "$SCRIPT_DIR/../.." \
  "$HOME/src/stack/ahbg/grok" \
  "/home/wayseer_interdependentway_org/src/stack/ahbg/grok" \
  "$(pwd)" \
  "$(pwd)/.."
do
  if [[ -f "$cand/bridges/web.py" ]]; then
    GROK_DIR="$cand"
    break
  fi
done

if [[ -z "$GROK_DIR" ]]; then
  echo "ERROR: Could not find the ahbg/grok directory."
  echo "Please cd into it or set GROK_DIR=/full/path"
  exit 1
fi

echo "Using: $GROK_DIR"
export PYTHONPATH="$GROK_DIR:$PYTHONPATH"

LAYERS="${LAYERS:-8}"
OUT="${OUT:-$HOME/ahbg-viewer.html}"
PORT="${PORT:-8080}"

echo "Generating real hex board (layers=$LAYERS)..."
python3 -m bridges.web --driver deepcode --layers "$LAYERS" --out "$OUT"

echo
echo "Generated: $OUT"
echo "To view:"
echo "  1. python3 -m http.server $PORT --bind 0.0.0.0"
echo "  2. Open http://<this-machine-ip>:$PORT/$(basename "$OUT")"
echo
echo "Or just open the file directly in a browser if your environment allows file:// URLs."
