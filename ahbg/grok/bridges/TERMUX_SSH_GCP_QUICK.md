# Termux → SSH → GCP VM (Quick Commands)

## 1. Termux setup (one time)
```bash
pkg install openssh
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_gcp -C termux-ahbg
cat ~/.ssh/id_ed25519_gcp.pub   # copy this
```

## 2. Add the key to your GCP VM
- Compute Engine → VM → Edit → SSH Keys → paste the public key.

## 3. Connect from Termux
```bash
ssh -i ~/.ssh/id_ed25519_gcp wayseer_interdependentway_org@YOUR_VM_EXTERNAL_IP
```

## 4. Inside the SSH session, run the viewer
```bash
cd /home/wayseer_interdependentway_org/src/stack/ahbg/grok
python3 -m bridges.web --driver deepcode --layers 8 --out ~/ahbg-viewer.html
python3 -m http.server 8080 --bind 127.0.0.1
```

## 5. Port forward (in a SECOND Termux session)
```bash
ssh -i ~/.ssh/id_ed25519_gcp -L 8080:localhost:8080 wayseer_interdependentway_org@YOUR_VM_EXTERNAL_IP -N
```

## 6. Open on phone
http://localhost:8080/ahbg-viewer.html

Real hex tiles + full construction, running on the VM.
