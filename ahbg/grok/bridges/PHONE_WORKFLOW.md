# Phone Workflow — AHBG Web Viewer (Termux)

**"hex is still hex"** — Real flat-top axial hex tiles with full construction support on large boards (layers=8, 12, 20, 30+).

You do **not** need pygame. The web version is pure HTML5 Canvas + embedded board data. It runs in any browser on your phone.

## 1. Install Termux (important)

- Download **Termux** from **F-Droid** (not Google Play — the Play version is outdated and broken).
- Open Termux and run:

```bash
pkg update && pkg upgrade
pkg install python
```

Optional but recommended for opening links automatically:

```bash
pkg install termux-api
```

Grant storage permission the first time you need it:

```bash
termux-setup-storage
```

## 2. Get the code on your phone

### Recommended: Full repo (best experience)

```bash
cd ~
git clone https://github.com/The-Interdependency/stack.git
cd stack/src/stack/ahbg/grok
```

(Adjust the clone command if you have a private fork or different source.)

### Minimal (just the web viewer)

You only need these two files for basic use:

- `bridges/web.py`
- `bridges/web_viewer.html`

Copy them into Termux (via `termux-setup-storage` + file manager, scp, adb push, etc.).

## 3. Generate a real hex board (one command)

From inside the `grok` directory:

```bash
# layers=8 → 61-tile centered hex, full construction
python3 -m bridges.web --driver deepcode --layers 8 --out ~/ahbg-viewer.html
```

Bigger boards:

```bash
python3 -m bridges.web --driver deepcode --layers 12 --out ~/ahbg-12.html
python3 -m bridges.web --driver deepcode --layers 20 --out ~/ahbg-20.html
```

You can also use the launcher scripts:

```bash
bash bridges/termux.sh --layers 8
# or
bash bridges/termux-viewer.sh --layers 8
```

Both generate + start the server in one go.

## 4. Serve the page

### Simple static server (recommended)

```bash
cd ~
python3 -m http.server 8080 --bind 127.0.0.1
```

Then open in your phone's browser:

```
http://127.0.0.1:8080/ahbg-viewer.html
```

### Completely offline (no server needed)

Because the HTML contains the entire board snapshot as JSON, you can open the file directly:

```bash
termux-open ~/ahbg-viewer.html
# or just tap the file in your file manager
```

Many browsers support `file://` for this kind of self-contained page.

## 5. Controls on the phone (same as desktop)

- **Tap** an empty adjacent hex → move
- **Tap** an unbuilt adjacent hex → build (construction)
- Enable **"Build mode"** checkbox at the top for easier building
- **Drag** to pan
- **Pinch** to zoom
- **Step** button (bottom/top bar) — automatically prefers building when possible

The hex tiles are real 6-sided polygons using the exact same math as the pygame version (`hexCenter` / `hexCorners` from `common.py`).

## 6. Typical daily phone session (fastest)

```bash
# 1. Open Termux
cd ~/stack/src/stack/ahbg/grok

# 2. (Optional) regenerate if you want a fresh board
python3 -m bridges.web --driver deepcode --layers 8 --out ~/ahbg.html

# 3. Serve
python3 -m http.server 8080 --bind 127.0.0.1 &

# 4. Open in browser
termux-open-url http://127.0.0.1:8080/ahbg.html
```

To stop the server later:

```bash
pkill -f "http.server"
```

## 7. Make it even more phone-friendly

### Add a quick alias

Put this in `~/.bashrc` (or `~/.zshrc` if you use zsh):

```bash
alias ahbg='cd ~/stack/src/stack/ahbg/grok && python3 -m bridges.web --driver deepcode --layers 8 --out ~/ahbg.html && python3 -m http.server 8080 --bind 127.0.0.1'
```

Then just type `ahbg` and open the link.

### Background / persistent server

Install `termux-services`:

```bash
pkg install termux-services
```

Then you can create a service, but for casual use the simple `&` + `pkill` is usually enough.

### Widget / shortcut (advanced)

- Use **Termux:Tasker** + **Tasker** or **Automate** app.
- Create a task that runs the generate + serve commands and opens the URL.
- Add a home screen shortcut or widget.

### Storage locations

Common easy paths:

- `~/ahbg-viewer.html` (Termux home)
- `/sdcard/Download/ahbg-viewer.html` (after `termux-setup-storage`)

## 8. Troubleshooting on phone

- **"No such file" for bridges/web.py** → You are not inside a directory that contains the `bridges/` folder, or `PYTHONPATH` is wrong. Use the full path or `cd` correctly.
- **Port already in use** → Change port: `--port 9090` or kill the old server.
- **Black/blank page** → Try the direct file open method (`termux-open ~/ahbg.html`) or a different browser.
- **Very large layers** (30+) → Phone browsers can handle it, but very high zoom + huge boards may feel slow. Start with layers 6–12.
- **No construction** → Make sure you are clicking an adjacent **unbuilt** tile. The center starts built.

## 9. What you get on the phone

- Full bridge support (DeepCode construction boards by default)
- Real hex geometry (not squares, not simplified)
- Move + build actions
- Large boards (hundreds of tiles)
- Works completely offline once the `.html` file exists
- Same logic as the desktop pygame viewer (just rendered in Canvas)

## Quick one-liner reference

```bash
pkg install python
cd ~/stack/src/stack/ahbg/grok
python3 -m bridges.web --driver deepcode --layers 8 --out ~/ahbg.html && python3 -m http.server 8080 --bind 127.0.0.1
```

Open `http://127.0.0.1:8080/ahbg.html`

---

**Files that matter on the phone:**

- `bridges/web.py` + `bridges/web_viewer.html` → core web renderer
- `bridges/termux.sh` and `bridges/termux-viewer.sh` → convenient launchers
- Generated `~/ahbg-*.html` files → the actual boards you play with

Hex is still hex. Enjoy building on your phone.