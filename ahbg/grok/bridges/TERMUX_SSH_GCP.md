# Termux → SSH → GCP VM (for AHBG Web Viewer)

This is the **recommended phone workflow** when your AHBG code lives on a GCP Compute Engine VM and you want to use it from Termux on Android.

**Goal**: From your phone:
1. SSH into the GCP VM from Termux.
2. Generate/run the real-hex web viewer on the VM.
3. View and interact with the hex board (construction + larger boards) in your phone browser.

You do **not** need to run the heavy logic on the phone. The VM does the work; Termux just gives you a terminal + port forwarding.

---

## 1. In Termux (on your phone)

```bash
pkg update && pkg upgrade
pkg install openssh
```

Generate a dedicated key (recommended, don't reuse phone keys for everything):

```bash
mkdir -p ~/.ssh
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_gcp -C "termux-ahbg"
chmod 600 ~/.ssh/id_ed25519_gcp
```

Copy the public key:

```bash
cat ~/.ssh/id_ed25519_gcp.pub
```

Copy the entire output (it starts with `ssh-ed25519 ...`).

---

## 2. Add the key to your GCP VM

### Easiest (Google Cloud Console)

1. Go to Compute Engine → VM instances.
2. Click your VM (e.g. `a0-prod-1`).
3. Click **Edit**.
4. Scroll to **SSH Keys**.
5. Click **Add item**.
6. Paste the public key you copied from Termux.
7. Save.

The username will usually be the one in the key or the OS default. From previous sessions it was `wayseer_interdependentway_org`.

### Alternative: gcloud (from your laptop or Cloud Shell)

```bash
gcloud compute os-login ssh-keys add \
  --key-file=/path/to/id_ed25519_gcp.pub \
  --project=YOUR_PROJECT
```

Or add to instance metadata (older style):

```bash
gcloud compute instances add-metadata YOUR_VM_NAME \
  --metadata-from-file ssh-keys=/path/to/local_key.pub
```

---

## 3. Find how to reach the VM

Two common cases:

**A. External IP (simplest)**  
In the VM details page, note the **External IP**.

**B. IAP tunneling (more secure, no public IP needed)**  
Use Identity-Aware Proxy. Requires `gcloud` on the client.

For Termux we usually use **A** (external IP + proper firewall rule on port 22).

Make sure your VM's firewall allows SSH from your IP (or 0.0.0.0/0 for testing).

---

## 4. Connect from Termux

```bash
ssh -i ~/.ssh/id_ed25519_gcp wayseer_interdependentway_org@YOUR_EXTERNAL_IP
```

Example:

```bash
ssh -i ~/.ssh/id_ed25519_gcp wayseer_interdependentway_org@34.XX.XX.XX
```

First time you will be asked to accept the host key — type `yes`.

Once inside you should see the normal Linux prompt on the VM.

---

## 5. Run the AHBG Web Viewer on the VM (from the SSH session)

```bash
cd /home/wayseer_interdependentway_org/src/stack/ahbg/grok
# or wherever your checkout is

# Generate a real hex board (layers=8 = 61 tiles, full construction)
python3 -m bridges.web --driver deepcode --layers 8 --out ~/ahbg-viewer.html
```

Start the web server **bound to localhost only** (safer):

```bash
python3 -m http.server 8080 --bind 127.0.0.1
```

**Keep this SSH session open** (or run it in background with `&` + `disown` or `tmux`/`screen`).

---

## 6. Access the web viewer from your phone (best method: SSH port forward)

**Do not** exit the SSH session yet.

Open a **new** Termux window (or split screen) and run a port-forwarded SSH:

```bash
ssh -i ~/.ssh/id_ed25519_gcp -L 8080:localhost:8080 wayseer_interdependentway_org@YOUR_EXTERNAL_IP -N
```

- `-L 8080:localhost:8080` forwards port 8080 on your phone to port 8080 on the VM.
- `-N` means "don't run a command, just forward".

Now, on the **same phone**, open your browser and go to:

```
http://localhost:8080/ahbg-viewer.html
```

You should see the real hex board. Tap to move, build, etc.

When done, Ctrl+C the forwarding SSH. The server on the VM can be left running or killed.

---

## 7. Convenient one-liner workflow (recommended)

In Termux, create a small helper (or just use these commands):

```bash
# One-time: make a quick launcher
cat > ~/ahbg-ssh << 'LAUNCHER'
#!/data/data/com.termux/files/usr/bin/bash
set -e
VM_USER="wayseer_interdependentway_org"
VM_IP="YOUR_EXTERNAL_IP_HERE"          # <-- CHANGE THIS
KEY="$HOME/.ssh/id_ed25519_gcp"

echo "=== Termux → GCP VM (AHBG) ==="
echo "Connecting and forwarding port 8080..."

# First connection (interactive) so you can generate the board if needed
ssh -i "$KEY" "$VM_USER@$VM_IP" -t '
  cd /home/wayseer_interdependentway_org/src/stack/ahbg/grok || cd ~/src/stack/ahbg/grok || true
  echo "On VM. Generating viewer (layers=8)..."
  python3 -m bridges.web --driver deepcode --layers 8 --out ~/ahbg-viewer.html || true
  echo "Starting http.server on VM (localhost only)..."
  python3 -m http.server 8080 --bind 127.0.0.1
'

# This won't be reached if the above stays open.
# For background server + separate forward, use the two-session method above.
LAUNCHER
chmod +x ~/ahbg-ssh
```

Edit `~/ahbg-ssh` and put your real VM IP.

Then just run:

```bash
~/ahbg-ssh
```

For the cleanest experience use **two terminals** in Termux:
- Terminal 1: full SSH + run the generator + http.server
- Terminal 2: port-forward SSH (`-L 8080:... -N`)

---

## 8. Tips & Troubleshooting

- **Use tmux or screen on the VM** so the web server keeps running after you disconnect:
  ```bash
  # on the VM
  tmux new -s ahbg
  python3 -m http.server 8080 --bind 127.0.0.1
  # detach with Ctrl+b then d
  ```

- Reconnect and forward later with the `-L` command.

- **IAP instead of public IP** (more secure):
  Install gcloud in Termux (heavy but works):
  ```bash
  pkg install python clang
  # then follow Google’s gcloud install for Linux, or use the official tarball
  ```
  Then:
  ```bash
  gcloud compute ssh wayseer_interdependentway_org@VM_NAME \
    --zone=ZONE --tunnel-through-iap -- -L 8080:localhost:8080
  ```

- Firewall: Make sure port 22 is open for your phone’s IP (or use IAP).

- Key permissions: `chmod 600 ~/.ssh/id_ed25519_gcp`

- If you get "Permission denied (publickey)":
  - Double-check you added the **public** key to the correct user on the VM.
  - The username must match (usually `wayseer_interdependentway_org` or whatever you see in the console).

- View the board from phone browser after forwarding: **http://localhost:8080/ahbg-viewer.html**

---

## 9. Quick reference commands (Termux)

```bash
# Connect
ssh -i ~/.ssh/id_ed25519_gcp wayseer_interdependentway_org@34.xx.xx.xx

# Generate + serve on VM (run inside the SSH session)
cd /home/wayseer_interdependentway_org/src/stack/ahbg/grok
python3 -m bridges.web --driver deepcode --layers 8 --out ~/ahbg-viewer.html
python3 -m http.server 8080 --bind 127.0.0.1

# Separate port-forward (new Termux session)
ssh -i ~/.ssh/id_ed25519_gcp -L 8080:localhost:8080 wayseer_interdependentway_org@34.xx.xx.xx -N

# Then open on phone:
# http://localhost:8080/ahbg-viewer.html
```

---

This gives you the full power of the VM (big layers, fast python) while using only Termux as a thin client + browser on the phone.

Hex is still hex. Build away.