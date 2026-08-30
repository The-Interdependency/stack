#!/data/data/com.termux/files/usr/bin/bash
#
# termux-viewer.sh
# Quick one-file launcher for AHBG Web Viewer (hex is still hex) from Termux.
#
# This version tries to be convenient:
# - Works even if you run it from anywhere.
# - Generates a standalone HTML page with real hex tiles + construction.
# - Serves it on localhost.
# - Prints the URL.
#
# Requirements (in Termux):
#   pkg install python
#
# How to use:
#   1. Copy this file to your Termux (or wget/curl it).
#   2. Make it executable: chmod +x termux-viewer.sh
#   3. Run it: ./termux-viewer.sh --layers 8
#
# You need the actual code. The easiest ways:
#   A. git clone the repo that contains src/stack/ahbg/grok
#   B. Or manually copy the "bridges/" directory + the two frozen ahbg trees
#      (stack-deepcode and stack-codex) so the drivers can load.
#
# If the foreign ahbg trees are missing, the script will still try to generate
# a demo board using the local _GrokNativeDriver path when possible.

set -e

OUTFILE="$HOME/ahbg-viewer.html"
PORT=8080
DRIVER="deepcode"
LAYERS=8
SEED=101

while [[ $# -gt 0 ]]; do
  case "$1" in
    --layers) LAYERS="$2"; shift 2;;
    --driver) DRIVER="$2"; shift 2;;
    --seed) SEED="$2"; shift 2;;
    --port) PORT="$2"; shift 2;;
    --out) OUTFILE="$2"; shift 2;;
    -h|--help)
      echo "termux-viewer.sh [--layers N] [--driver deepcode|codex|grok] [--port N]"
      exit 0
      ;;
    *) echo "Unknown: $1"; exit 1;;
  esac
done

echo "=== AHBG Web Viewer (Termux) ==="
echo "Generating real hex board (layers=$LAYERS, driver=$DRIVER)..."

# Try to locate a usable grok/bridges directory
find_grok_dir() {
  local candidates=(
    "$GROK_DIR"
    "$HOME/src/stack/ahbg/grok"
    "$HOME/ahbg/grok"
    "$HOME/grok"
    "$(pwd)"
    "$(pwd)/.."
    "$(dirname "$0")"
    "$(dirname "$0")/.."
  )
  for d in "${candidates[@]}"; do
    if [[ -n "$d" && -d "$d/bridges" && -f "$d/bridges/web.py" ]]; then
      echo "$d"
      return 0
    fi
  done
  return 1
}

GROK_DIR_FOUND="$(find_grok_dir || true)"

if [[ -n "$GROK_DIR_FOUND" ]]; then
  echo "Found code at: $GROK_DIR_FOUND"
  export PYTHONPATH="$GROK_DIR_FOUND:$PYTHONPATH"
  python3 -m bridges.web --driver "$DRIVER" --layers "$LAYERS" --seed "$SEED" --out "$OUTFILE"
else
  echo "WARNING: Could not find the full grok/bridges code tree."
  echo "Falling back to a minimal embedded hex board generator (still real hexes)."
  python3 - <<'PYEOF' "$OUTFILE" "$LAYERS" "$SEED"
import sys, json, math, re
outfile = sys.argv[1]
layers = int(sys.argv[2])
seed = int(sys.argv[3])

def make_hex_board(layers):
    tiles = []
    for q in range(-layers, layers+1):
        for r in range(-layers, layers+1):
            if abs(q) + abs(q + r) + abs(r) <= layers:
                tiles.append({"tile_id": f"t{q},{r}", "q": q, "r": r, "built": (q==0 and r==0)})
    return tiles

tiles = make_hex_board(layers)
units = [{"unit_id": "A0", "tile_id": "t0,0"}]
snap = {"turn": 0, "tiles": tiles, "units": units, "driver": "deepcode-fallback", "layers": layers}

# Read the template if possible, otherwise create a minimal self-contained page
template = None
for p in ["bridges/web_viewer.html", "../bridges/web_viewer.html", "web_viewer.html"]:
    try:
        with open(p) as f: template = f.read(); break
    except: pass

if template:
    html = template
    inj = f'<script id="ahbg-snapshot" type="application/json">\n{json.dumps(snap)}\n</script>'
    if "</body>" in html:
        html = html.replace("</body>", inj + "\n</body>")
    else:
        html += "\n" + inj
else:
    # Ultra-minimal standalone page with correct hex math
    html = f'''<!doctype html>
<html><head><meta charset="utf-8"><title>AHBG (hex is still hex)</title>
<style>body{{background:#121216;color:#ddd;font-family:monospace;margin:0}}
#hud{{padding:6px;background:#1a1a20}}canvas{{display:block;background:#121216}}</style>
</head><body>
<canvas id="c" width="1024" height="768"></canvas>
<div id="hud">tap empty hex to move • tap unbuilt to build • drag=pan • pinch=zoom</div>
<script>
const snap = {json.dumps(snap)};
function hexCenter(q,r,s){{return [s*(3/2*q), s*(Math.sqrt(3)/2*q + Math.sqrt(3)*r)];}}
function hexCorners(cx,cy,s){{const p=[]; for(let i=0;i<6;i++){{const a=Math.PI/180*(60*i); p.push([cx+s*Math.cos(a),cy+s*Math.sin(a)]);}} return p;}}
let canvas=document.getElementById('c'), ctx=canvas.getContext('2d');
let ox=400, oy=320, zoom=1.0, size=18;
let tiles = snap.tiles, units = snap.units;
function draw(){{
  ctx.fillStyle='#121216'; ctx.fillRect(0,0,canvas.width,canvas.height);
  const s = size*zoom;
  for(const t of tiles){{
    const [cx,cy] = hexCenter(t.q,t.r,s); const px=cx+ox, py=cy+oy;
    const corners = hexCorners(px,py,s);
    ctx.fillStyle = t.built ? '#468c5a' : '#373741';
    ctx.beginPath(); ctx.moveTo(corners[0][0],corners[0][1]);
    for(let i=1;i<6;i++) ctx.lineTo(corners[i][0],corners[i][1]);
    ctx.closePath(); ctx.fill(); ctx.strokeStyle='#222'; ctx.stroke();
    ctx.fillStyle='#ccc'; ctx.font='11px monospace'; ctx.fillText(t.tile_id, px-10, py+3);
  }}
  for(const u of units){{
    const t = tiles.find(x=>x.tile_id===u.tile_id) || {{q:0,r:0}};
    const [cx,cy] = hexCenter(t.q,t.r,s);
    ctx.fillStyle='#dcb43c'; ctx.beginPath(); ctx.arc(cx+ox,cy+oy,s*0.55,0,Math.PI*2); ctx.fill();
  }}
}}
let dragging=false,lx=0,ly=0;
canvas.addEventListener('mousedown',e=>{dragging=true;lx=e.offsetX;ly=e.offsetY; handleClick(e.offsetX,e.offsetY,e.button===2);});
canvas.addEventListener('mousemove',e=>{if(dragging){ox+=e.offsetX-lx;oy+=e.offsetY-ly;lx=e.offsetX;ly=e.offsetY;draw();}});
window.addEventListener('mouseup',()=>dragging=false);
canvas.addEventListener('wheel',e=>{e.preventDefault(); zoom=Math.max(0.3,Math.min(4,zoom*(e.deltaY<0?1.1:0.9))); draw();},{passive:false});
function handleClick(sx,sy,isBuild){{
  const s=size*zoom; let best=null,bestD=1e9;
  for(const t of tiles){{
    const [cx,cy]=hexCenter(t.q,t.r,s); const d=(cx+ox-sx)**2+(cy+oy-sy)**2;
    if(d<bestD){bestD=d;best=t;}
  }}
  if(!best) return;
  const u=units[0]; const ut=tiles.find(x=>x.tile_id===u.tile_id);
  const dirs=[[1,0],[1,-1],[0,-1],[-1,0],[-1,1],[0,1]];
  let ok=false;
  for(const [dq,dr] of dirs){{
    if(best.q===ut.q+dq && best.r===ut.r+dr){{
      if(isBuild || (event && event.shiftKey)){{
        if(!best.built){{best.built=true; ok=true;}}
      }}else{{
        if(!tiles.some(x=>x.tile_id===best.tile_id && units.some(uu=>uu.tile_id===best.tile_id))){{
          u.tile_id=best.tile_id; ok=true;
        }}
      }}
    }}
  }}
  if(ok) draw();
}}
draw();
alert("Hex board ready. LMB=move, RMB or long tap=build. Drag to pan.");
</script></body></html>'''
with open(outfile,'w') as f: f.write(html)
print("Wrote fallback viewer:", outfile)
PYEOF
fi

echo
echo "Serving on http://127.0.0.1:$PORT/$(basename "$OUTFILE")"
echo "Open that URL in your browser."

if command -v termux-open-url >/dev/null 2>&1; then
  termux-open-url "http://127.0.0.1:$PORT/$(basename "$OUTFILE")" || true
fi

cd "$(dirname "$OUTFILE")"
python3 -m http.server "$PORT" --bind 127.0.0.1
