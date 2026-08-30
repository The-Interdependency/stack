#!/data/data/com.termux/files/usr/bin/bash
# phone-workflow.sh
# Fast phone workflow for AHBG Web Viewer (real hex tiles + construction)
# Run this from Termux on your phone.

set -e

echo "=== AHBG Phone Workflow (hex is still hex) ==="
echo

# 1. Make sure we have python
if ! command -v python3 >/dev/null; then
  echo "Installing python..."
  pkg install -y python
fi

# 2. Find or ask for the grok directory
GROK_DIR="${GROK_DIR:-}"

if [[ -z "$GROK_DIR" || ! -f "$GROK_DIR/bridges/web.py" ]]; then
  for cand in \
    "$HOME/src/stack/ahbg/grok" \
    "$HOME/ahbg/grok" \
    "$HOME/grok" \
    "$(pwd)" \
    "$(pwd)/.." \
    "$(dirname "$0")" \
    "$(dirname "$0")/.."
  do
    if [[ -f "$cand/bridges/web.py" ]]; then
      GROK_DIR="$cand"
      break
    fi
  done
fi

if [[ -z "$GROK_DIR" || ! -f "$GROK_DIR/bridges/web.py" ]]; then
  echo "Could not find the code."
  echo "Please cd into the directory containing bridges/web.py and run this again,"
  echo "or set GROK_DIR=/full/path"
  exit 1
fi

echo "Using code from: $GROK_DIR"
export PYTHONPATH="$GROK_DIR:$PYTHONPATH"

# 3. Generate board (default: deepcode layers 8 - nice size for phone)
LAYERS="${LAYERS:-8}"
OUT="$HOME/ahbg-phone.html"

echo
echo "Generating board (layers=$LAYERS)..."
python3 -m bridges.web --driver deepcode --layers "$LAYERS" --out "$OUT"

echo
echo "Board ready: $OUT"
echo

# 4. Start server in background
PORT="${PORT:-8080}"
echo "Starting server on port $PORT..."
pkill -f "http.server $PORT" 2>/dev/null || true
cd "$(dirname "$OUT")"
python3 -m http.server "$PORT" --bind 127.0.0.1 > /tmp/ahbg-server.log 2>&1 &
SERVER_PID=$!
sleep 1

URL="http://127.0.0.1:$PORT/$(basename "$OUT")"

echo
echo "=== OPEN THIS ON YOUR PHONE ==="
echo "$URL"
echo

# 5. Try to open automatically
if command -v termux-open-url >/dev/null 2>&1; then
  echo "Opening in browser..."
  termux-open-url "$URL" || true
else
  echo "Tip: pkg install termux-api   then you can auto-open links"
fi

echo
echo "Controls:"
echo "  • Tap empty adjacent hex → move"
echo "  • Tap unbuilt hex (or check Build mode) → construct"
echo "  • Drag to pan, pinch to zoom"
echo "  • Use the Step button (prefers building)"
echo
echo "To stop server later: pkill -f http.server"
echo
echo "Server is running in background (PID $SERVER_PID)."
echo "You can now switch to your browser."
