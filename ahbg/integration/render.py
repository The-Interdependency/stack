# ratios: loc_comments=172:17 imports_exports=8:5 calls_definitions=81:11


"""Headless frame renderer + compact interactive viewer.

Reuses Grok's cross-driver geometry (``ahbg/grok/bridges/common.py``:
``hex_center`` / ``hex_corners``) read-only so the rendered frames use the
exact tile geometry of the Grok viewer. Headless PNG frames are produced with
pygame's dummy video driver (no window, no key); the interactive window uses
the same drawing code with Grok's viewer controls.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

# Read-only vendored reference of Grok's cross-driver geometry surface
# (ahbg/grok/bridges/common.py at grok branch head c1f9d81). Frozen builds
# are never modified; this copy pins the viewer geometry for clean-checkout CI.
from . import grok_common as _common


def grok_common() -> Any:
    return _common


def _pygame() -> Any:
    import os

    if os.environ.get("SDL_VIDEODRIVER") != "dummy" and not os.environ.get("DISPLAY"):
        os.environ["SDL_VIDEODRIVER"] = "dummy"
    import pygame

    if not pygame.get_init():
        pygame.init()
    return pygame


def render_frame(
    obs: dict[str, Any],
    banner: str,
    path: Path,
    *,
    size: int = 640,
    bg: tuple[int, int, int] = (18, 18, 22),
) -> None:
    """Render one observation to a PNG frame."""
    pg = _pygame()
    common = grok_common()
    screen = pg.Surface((size, size + 48))
    screen.fill(bg)
    font = pg.font.SysFont("monospace", 13)

    tiles = obs.get("tiles", [])
    qs = [int(t["q"]) for t in tiles] or [0]
    rs = [int(t["r"]) for t in tiles] or [0]
    span = max(max(qs) - min(qs), max(rs) - min(rs), 1)
    cell = 12.0 * (size / 640.0)
    scale = min((size - 80) / (span * 1.8 * cell), 2.5)
    cell *= max(scale, 0.6)

    centers: dict[str, tuple[float, float]] = {}
    for t in tiles:
        cx, cy = common.hex_center(int(t["q"]), int(t["r"]), cell)
        px, py = cx + size / 2, cy + (size / 2)
        corners = [(px + x, py + y) for x, y in common.hex_corners(0.0, 0.0, cell)]
        built = bool(t.get("built", False))
        pg.draw.polygon(screen, (70, 140, 90) if built else (55, 55, 65), corners)
        pg.draw.polygon(screen, (30, 30, 35), corners, 1)
        centers[str(t["tile_id"])] = (px, py)
        label = font.render(str(t["tile_id"]), True, (200, 200, 210))
        screen.blit(label, (px - 14, py - 6))

    for u in obs.get("units", []):
        pos = centers.get(str(u["tile_id"]))
        if pos:
            pg.draw.circle(screen, (220, 180, 60), (int(pos[0]), int(pos[1])), int(cell * 0.55))
            ulabel = font.render(str(u.get("unit_id", "?")), True, (20, 20, 25))
            screen.blit(ulabel, (pos[0] - 8, pos[1] - 6))

    hud = font.render(f"turn {obs.get('turn', 0)}   {banner}", True, (230, 230, 235))
    screen.blit(hud, (8, size + 10))
    pg.image.save(screen, str(path))


def render_all(driver: Any, frames_dir: Path, banners: list[str], records: list[dict[str, Any]] | None = None) -> list[Path]:
    """Render one frame per demo step; records carry per-step observations."""
    frames_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, banner in enumerate(banners):
        if records and i < len(records) and records[i].get("observation"):
            obs = records[i]["observation"]
        else:
            obs = driver.observe()
        path = frames_dir / f"frame_{i:03d}.png"
        render_frame(obs, banner, path)
        paths.append(path)
    return paths


def write_player(frames_dir: Path, banners: list[str]) -> Path:
    """Write a dependency-free HTML player that steps through the PNG frames."""
    html = [
        "<!doctype html><html><head><meta charset='utf-8'><title>AHBG demo</title></head>",
        "<body style='background:#121216;color:#e6e6eb;font-family:monospace'>",
        "<h3>AHBG post-calibration demo</h3>",
        "<img id='f' src='frame_000.png' style='background:#121216'>",
        "<div style='margin-top:8px'>",
        "<button onclick='step(-1)'>prev</button>",
        "<button onclick='step(1)'>next</button>",
        "<span id='caption' style='margin-left:12px'></span>",
        "</div><script>",
        "const banners=" + repr(banners).replace("'", '"') + ";",
        "let i=0;",
        "function show(){document.getElementById('f').src='frame_'+String(i).padStart(3,'0')+'.png';",
        "document.getElementById('caption').textContent=banners[i]||'';}",
        "function step(d){i=Math.min(Math.max(i+d,0),banners.length-1);show();}",
        "show();</script></body></html>",
    ]
    path = frames_dir / "index.html"
    path.write_text("\n".join(html), encoding="utf-8")
    return path


class Window:
    """Compact interactive viewer with Grok's viewer controls.

    LMB move onto empty adjacent tile; RMB/Ctrl+click build unbuilt adjacent
    tile; SPACE auto-step; Q/ESC quit. Requires a display (not CI).
    """

    def __init__(self, driver: Any, title: str = "AHBG integration demo") -> None:
        import os

        if os.environ.get("SDL_VIDEODRIVER") == "dummy":
            os.environ.pop("SDL_VIDEODRIVER", None)
        self.pg = _pygame()
        self.pg.init()
        self.driver = driver
        self.screen = self.pg.display.set_mode((1024, 768), self.pg.RESIZABLE)
        self.pg.display.set_caption(title)
        self.font = self.pg.font.SysFont("monospace", 14)
        self.obs = None
        self.banner = ""
        self._refresh()

    def _refresh(self) -> None:
        self.obs = self.driver.observe()
        self.banner = f"turn {self.obs.get('turn', 0)}"

    def run(self) -> None:
        pg = self.pg
        clock = pg.time.Clock()
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key in (pg.K_q, pg.K_ESCAPE):
                        running = False
                    elif event.key == pg.K_r:
                        self._refresh()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self._click(event)
            self._draw()
            pg.display.flip()
            clock.tick(30)

    def _click(self, event: Any) -> None:
        pg = self.pg
        common = grok_common()
        tiles = {t["tile_id"]: t for t in self.obs.get("tiles", [])}
        cell = 18.0
        best = None
        best_d = 1e9
        for tid, t in tiles.items():
            cx, cy = common.hex_center(int(t["q"]), int(t["r"]), cell)
            px, py = cx + 400, cy + 320
            d = (px - event.pos[0]) ** 2 + (py - event.pos[1]) ** 2
            if d < best_d:
                best_d = d
                best = tid
        if best is None:
            return
        if event.button == 1:
            try:
                self.driver.submit_choice({"kind": "relocate", "unit_id": "A0", "to_tile_id": best})
                self.driver.end_turn()
                self._refresh()
            except Exception as exc:
                self.banner = f"rejected: {type(exc).__name__}"
        elif event.button == 3:
            try:
                self.driver.submit_build("A0", best)
                self.driver.end_turn()
                self._refresh()
            except Exception as exc:
                self.banner = f"rejected: {type(exc).__name__}"

    def _draw(self) -> None:
        pg = self.pg
        common = grok_common()
        self.screen.fill((18, 18, 22))
        for t in self.obs.get("tiles", []):
            cx, cy = common.hex_center(int(t["q"]), int(t["r"]), 18.0)
            px, py = cx + 400, cy + 320
            corners = [(px + x, py + y) for x, y in common.hex_corners(0.0, 0.0, 18.0)]
            pg.draw.polygon(self.screen, (70, 140, 90) if t.get("built") else (55, 55, 65), corners)
            pg.draw.polygon(self.screen, (30, 30, 35), corners, 1)
            txt = self.font.render(str(t["tile_id"]), True, (200, 200, 210))
            self.screen.blit(txt, (px - 12, py - 6))
        for u in self.obs.get("units", []):
            t = next((x for x in self.obs.get("tiles", []) if x["tile_id"] == u["tile_id"]), None)
            if t:
                cx, cy = common.hex_center(int(t["q"]), int(t["r"]), 18.0)
                pg.draw.circle(self.screen, (220, 180, 60), (int(cx + 400), int(cy + 320)), 10)
        hud = self.font.render(self.banner + "   LMB move / RMB build / R refresh / Q quit", True, (230, 230, 235))
        self.screen.blit(hud, (8, 8))
# ratios: loc_comments=172:17 imports_exports=8:5 calls_definitions=81:11
