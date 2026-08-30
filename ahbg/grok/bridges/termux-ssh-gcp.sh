#!/data/data/com.termux/files/usr/bin/bash
#
# termux-ssh-gcp.sh
# Helper to SSH from Termux into your GCP VM and set up the AHBG web viewer.
#
# Edit the variables below once, then run:
#   bash termux-ssh-gcp.sh
#
# It will:
#   - SSH into the VM
#   - Generate the real-hex web viewer (layers=8 by default)
#   - Start the server on the VM (localhost)
#   - Print the port-forward command you should run in another Termux session
#
# Then open http://localhost:8080/ahbg-viewer.html on your phone.

set -e

# ==================== EDIT THESE ====================
VM_USER="wayseer_interdependentway_org"
VM_IP="YOUR_EXTERNAL_IP_HERE"          # e.g. 34.123.45.67
KEY="$HOME/.ssh/id_ed25519_gcp"        # your Termux private key
LAYERS="${LAYERS:-8}"
PORT=8080
# ====================================================

if [[ "$VM_IP" == "YOUR_EXTERNAL_IP_HERE" ]]; then
  echo "ERROR: Edit this script and set VM_IP to your GCP VM external IP."
  exit 1
fi

echo "=== Termux → GCP VM (AHBG Web Viewer) ==="
echo "VM: $VM_USER@$VM_IP"
echo "Layers: $LAYERS"
echo

# Run on the VM: cd to the right place, generate viewer, start server
ssh -i "$KEY" "$VM_USER@$VM_IP" -t "
  set -e
  echo 'Connected to VM.'
  cd /home/wayseer_interdependentway_org/src/stack/ahbg/grok 2>/dev/null || \\
  cd ~/src/stack/ahbg/grok 2>/dev/null || \\
  cd ~/ahbg/grok 2>/dev/null || true

  echo 'Generating web viewer (real hex tiles)...'
  python3 -m bridges.web --driver deepcode --layers $LAYERS --out ~/ahbg-viewer.html

  echo
  echo 'Starting server on VM (localhost only)...'
  echo 'Keep this session open, or run it under tmux/screen.'
  echo
  python3 -m http.server $PORT --bind 127.0.0.1
"

# If the above command returns, the server stopped.
echo
echo "Server session ended."
echo
echo "To forward the port from another Termux tab:"
echo "  ssh -i $KEY -L $PORT:localhost:$PORT $VM_USER@$VM_IP -N"
echo
echo "Then open on your phone:"
echo "  http://localhost:$PORT/ahbg-viewer.html"
