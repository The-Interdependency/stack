"""Web (HTML5 Canvas) viewer for AHBG boards.

Preserves exact hex geometry: "hex is still hex".
Uses the same flat-top axial layout, colors, and interaction model
as the native pygame Viewer, but outputs a self-contained .html
that works in any browser (no server required for basic use).

Usage:

    cd src/stack/ahbg/grok
    python3 -m bridges.web --driver deepcode --layers 8 --out viewer.html
    # then open viewer.html in a browser

The page supports:
- Real hex tiles (identical math to common.hex_center / hex_corners)
- LMB click empty adjacent = move
- RMB or "Build mode" checkbox on buildable = build
- Drag to pan, wheel to zoom
- Step button (prefers construction when available)
- Works on large construction boards (layers=30 etc.)

For live Python-driven updates you can either:
- embed a fresh snapshot each time you generate the page, or
- run a tiny server that serves this HTML + /action endpoint (not included here).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

# Make imports work when run as -m
import sys
WORKSPACE = Path(__file__).resolve().parents[1]
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))

from bridges import make_driver
from bridges.common import hex_center, hex_corners  # kept as the single source of truth


def observation_to_web_snapshot(obs: dict[str, Any], driver: str = "", layers: int | None = None) -> dict[str, Any]:
    """Convert a normalized observation to the minimal shape the web viewer expects."""
    tiles = []
    for t in obs.get("tiles", []):
        tiles.append({
            "tile_id": t["tile_id"],
            "q": int(t["q"]),
            "r": int(t["r"]),
            "built": bool(t.get("built", False)),
        })
    units = []
    for u in obs.get("units", []):
        units.append({
            "unit_id": u.get("unit_id", "A0"),
            "tile_id": u.get("tile_id"),
        })
    snap = {
        "turn": obs.get("turn", 0),
        "tiles": tiles,
        "units": units,
    }
    if driver:
        snap["driver"] = driver
    if layers is not None:
        snap["layers"] = layers
    return snap


def generate_html(
    snapshot: dict[str, Any],
    title: str = "AHBG Web Viewer — hex is still hex",
) -> str:
    """Return a complete self-contained HTML document with the board snapshot embedded."""
    # Read the sibling web_viewer.html as a template (it already contains the full viewer).
    template_path = Path(__file__).parent / "web_viewer.html"
    if not template_path.exists():
        # Fallback: the file we just created should be there, but be defensive.
        raise RuntimeError("web_viewer.html template is missing next to web.py")

    html = template_path.read_text(encoding="utf-8")

    # Inject the snapshot as a JSON script block that the page will pick up on load.
    # We replace the demo boot with the real snapshot.
    snap_json = json.dumps(snapshot, separators=(",", ":"))

    # The page already has a hook:
    #   const snap = document.getElementById('ahbg-snapshot');
    # We will insert a script tag with id="ahbg-snapshot" containing the JSON,
    # plus a small bootstrap that calls AHBGWebViewer.setState if present.

    injection = f'''
<script id="ahbg-snapshot" type="application/json">
{snap_json}
</script>
<script>
(function() {{
  // If the viewer script already ran, push the snapshot now.
  function push() {{
    try {{
      const raw = document.getElementById('ahbg-snapshot').textContent;
      const data = JSON.parse(raw);
      if (window.AHBGWebViewer && data && data.tiles) {{
        window.AHBGWebViewer.setState(data);
        if (data.driver) window.__driver = data.driver;
        if (data.layers != null) window.__layers = data.layers;
      }}
    }} catch(e){{}}
  }}
  if (document.readyState === 'complete') push();
  else window.addEventListener('load', push, {{once:true}});
}})();
</script>
'''

    # Insert the injection right before </body>
    if "</body>" in html:
        html = html.replace("</body>", injection + "\n</body>")
    else:
        html = html + "\n" + injection

    # Also update the title if we have driver info
    if snapshot.get("driver"):
        layers = snapshot.get("layers")
        extra = f" — {snapshot['driver']}" + (f" layers={layers}" if layers is not None else "")
        html = html.replace(
            "<title>AHBG Web Viewer — hex is still hex</title>",
            f"<title>AHBG Web Viewer{extra}</title>"
        )

    return html


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate a self-contained web (Canvas) viewer for an AHBG board. Hex geometry is preserved exactly.")
    parser.add_argument("--driver", default="deepcode", choices=["deepcode", "codex", "grok"])
    parser.add_argument("--layers", type=int, default=6, help="Hex layers for construction boards (deepcode)")
    parser.add_argument("--seed", type=int, default=101)
    parser.add_argument("--out", type=Path, default=None, help="Output .html path (default: ahbg-web-viewer.html)")
    args = parser.parse_args(argv)

    drv = make_driver(args.driver, layers=args.layers if args.driver in ("deepcode", "d", "dc") else None, seed=args.seed)
    obs = drv.observe()

    snap = observation_to_web_snapshot(
        obs,
        driver=args.driver,
        layers=args.layers if args.driver in ("deepcode", "d", "dc") else None
    )

    html = generate_html(snap)

    out_path = args.out or Path("ahbg-web-viewer.html")
    out_path.write_text(html, encoding="utf-8")

    print(f"Wrote {out_path.resolve()}")
    print(f"Board: {args.driver}  tiles={len(snap['tiles'])}  layers={snap.get('layers')}")
    print("Open the .html in any browser. Hex tiles are rendered with the exact same flat-top axial math as the pygame viewer.")
    print("LMB = move to empty adjacent, RMB or check 'Build mode' = construct on unbuilt adjacent.")


if __name__ == "__main__":
    main()
