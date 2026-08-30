#!/data/data/com.termux/files/usr/bin/bash
#
# Termux launcher for the AHBG Web Viewer (HTML5 Canvas)
#
# "hex is still hex" — this generates and serves the real hexagonal board
# using the same flat-top axial geometry as the desktop pygame viewer.
#
# Requirements in Termux:
#   pkg install python
#   (no pygame needed — this is pure web output)
#
# Usage examples (run from inside the repo or anywhere):
#
#   bash bridges/termux.sh
#   bash bridges/termux.sh --layers 12
#   bash bridges/termux.sh --driver codex
#   GROK_DIR=/sdcard/my-grok-src bash bridges/termux.sh --layers 8
#
# After running it will:
#   1. Generate ahbg-viewer.html (with real hex tiles + construction)
#   2. Start a local HTTP server
#   3. Try to open it with termux-open-url (if available)
#   4. Print the URL you can paste into any browser on the device
#
# To stop the server: Ctrl+C
#

set -e

# --- Configurable defaults ---
DEFAULT_DRIVER="deepcode"
DEFAULT_LAYERS=8
DEFAULT_SEED=101
DEFAULT_PORT=8080
OUTFILE="$HOME/ahbg-viewer.html"

# --- Parse simple args ---
DRIVER="$DEFAULT_DRIVER"
LAYERS="$DEFAULT_LAYERS"
SEED="$DEFAULT_SEED"
PORT="$DEFAULT_PORT"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --driver)
      DRIVER="$2"; shift 2 ;;
    --layers)
      LAYERS="$2"; shift 2 ;;
    --seed)
      SEED="$2"; shift 2 ;;
    --port)
      PORT="$2"; shift 2 ;;
    --out)
      OUTFILE="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $0 [--driver deepcode|codex|grok] [--layers N] [--port N] [--out path]"
      echo "Example: $0 --driver deepcode --layers 8"
      exit 0
      ;;
    *)
      echo "Unknown arg: $1"
      exit 1
      ;;
  esac
done

echo "=== AHBG Web Viewer for Termux ==="
echo "Driver : $DRIVER"
echo "Layers : $LAYERS (larger = more hex tiles, full construction support)"
echo "Output : $OUTFILE"
echo

# --- Find the Grok AHBG directory ---
# Try several common locations so the script works whether you run it
# from inside the repo or from anywhere.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CANDIDATES=(
  "${GROK_DIR:-}"
  "$SCRIPT_DIR/.."
  "$SCRIPT_DIR/../.."
  "$HOME/src/stack/ahbg/grok"
  "$HOME/ahbg/grok"
  "$HOME/grok"
  "$(pwd)"
  "$(pwd)/.."
)

GROK_DIR=""
for cand in "${CANDIDATES[@]}"; do
  if [[ -n "$cand" && -d "$cand/bridges" && -f "$cand/bridges/web.py" ]]; then
    GROK_DIR="$cand"
    break
  fi
done

if [[ -z "$GROK_DIR" ]]; then
  echo "ERROR: Could not find the AHBG grok directory (where bridges/ lives)."
  echo "Set it explicitly with:"
  echo "  GROK_DIR=/path/to/src/stack/ahbg/grok bash $0"
  echo
  echo "Or cd into the grok directory first and run:"
  echo "  bash bridges/termux.sh"
  exit 1
fi

echo "Using code from: $GROK_DIR"
export PYTHONPATH="$GROK_DIR:$PYTHONPATH"

# --- Generate the HTML (real hex tiles) ---
echo
echo "Generating web viewer with real hex geometry..."
python3 -m bridges.web \
  --driver "$DRIVER" \
  --layers "$LAYERS" \
  --seed "$SEED" \
  --out "$OUTFILE"

if [[ ! -f "$OUTFILE" ]]; then
  echo "ERROR: Failed to create $OUTFILE"
  exit 1
fi

echo "Generated: $OUTFILE"

TILE_COUNT=$(python3 -c '
import json, re, sys
with open(sys.argv[1]) as f:
    txt = f.read()
m = re.search(r"id=\"ahbg-snapshot\"[^>]*>(.*?)</script>", txt, re.DOTALL)
if m:
    snap = json.loads(m.group(1).strip())
    print(len(snap.get("tiles", [])), "tiles (true hexes)")
else:
    print("hex board ready")
' "$OUTFILE" 2>/dev/null || echo "hex board ready")

echo "Board size: $TILE_COUNT"

# --- Serve it ---
HTML_DIR="$(dirname "$OUTFILE")"
HTML_NAME="$(basename "$OUTFILE")"

echo
echo "Starting local web server on port $PORT..."
echo "URL: http://127.0.0.1:$PORT/$HTML_NAME"
echo
echo "On your phone:"
echo "  • Open the URL above in any browser (Chrome, Firefox, Termux:Tasker, etc.)"
echo "  • Or let termux-open-url try to launch it automatically"
echo
echo "Controls in the page:"
echo "  LMB / tap empty adjacent tile  → move"
echo "  RMB / long-press or check 'Build mode' on unbuilt tile → construct"
echo "  Drag to pan, pinch/wheel to zoom"
echo "  'Step' button prefers building when possible"
echo
echo "Hex is still hex — same flat-top axial layout as the desktop version."
echo
echo "Press Ctrl+C to stop the server."
echo

# Try to open automatically if termux-open-url is available
if command -v termux-open-url >/dev/null 2>&1; then
  termux-open-url "http://127.0.0.1:$PORT/$HTML_NAME" || true
else
  echo "(termux-open-url not found — install with: pkg install termux-api)"
fi

# Change to the directory containing the file and serve
cd "$HTML_DIR"

# Use a slightly more robust server that serves the file nicely
python3 -m http.server "$PORT" --bind 127.0.0.1
