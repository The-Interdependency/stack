#!/bin/bash
# Simple launcher for the AHBG web viewer on this server / any Linux machine.
# Usage: ./bridges/run-web-viewer.sh [layers]

set -e

cd "$(dirname "$0")/.."   # go to the grok directory

LAYERS="${1:-8}"
OUT="$HOME/ahbg-viewer.html"
PORT="${PORT:-8080}"

echo "Generating AHBG web viewer (layers=$LAYERS, real hex tiles)..."
python3 -m bridges.web --driver deepcode --layers "$LAYERS" --out "$OUT"

echo
echo "Viewer file: $OUT"
echo
echo "Starting server on port $PORT..."
echo "Open in browser:"
echo "  http://localhost:$PORT/$(basename "$OUT")"
echo
if command -v hostname >/dev/null; then
  IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "YOUR-SERVER-IP")
  echo "From another machine/phone on the same network:"
  echo "  http://$IP:$PORT/$(basename "$OUT")"
fi
echo
echo "Press Ctrl+C to stop the server."

cd "$(dirname "$OUT")"
python3 -m http.server "$PORT" --bind 0.0.0.0
