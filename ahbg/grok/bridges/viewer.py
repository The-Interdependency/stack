"""Separate-window pygame viewer for AHBG boards.

Supports:
- All three boards via the bridges (Grok native, Codex, DeepCode)
- Construction (build) actions + larger boards (DeepCode world model)
- Cross-board normalized observations

Run from the Grok workspace:

    cd stack/ahbg/grok
    python3 -m bridges.viewer --driver deepcode --layers 6

Requires pygame (pip install pygame).

Controls:
  Left-click empty adjacent tile  -> move
  Right-click / Ctrl+click buildable tile -> build
  SPACE  -> step one turn (auto)
  R      -> reset board
  +/-    -> zoom
  Arrow keys / drag -> pan
  Q / ESC -> quit
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import Any

# pygame is imported lazily inside Viewer so the module can be imported
# for driver creation, tests, etc. without pygame installed.
_pygame = None

def _get_pygame():
    """Return the real pygame module or raise a clear error if unavailable."""
    global _pygame
    if _pygame is not None:
        return _pygame
    try:
        import pygame as _pg  # type: ignore
        _pygame = _pg
        return _pygame
    except Exception as e:
        raise RuntimeError(
            "pygame is required for the AHBG viewer window. Install with: pip install pygame"
        ) from e

# Make local Grok a0 + bridges importable
WORKSPACE = Path(__file__).resolve().parents[1]
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))

from a0.selfhood import Vessel
from a0.will import choose_relocate

from bridges import CodexBoardDriver, DeepCodeBoardDriver
from bridges.common import (
    axial_to_label,
    hex_center,
    hex_corners,
    label_to_axial,
    normalize_observation,
    unbuilt_adjacent_from_observation,
)


def make_driver(name: str, layers: int = 5, seed: int = 101):
    """Create a driver for the requested board, optionally with a larger construction board."""
    name = name.lower()
    if name in ("codex", "c"):
        return CodexBoardDriver(seed=seed)
    if name in ("deepcode", "deepseek", "d", "dc"):
        # Build a larger board with construction support (like DeepCode game.py)
        tiles = _build_hex_tiles(layers)
        units = [{"unit_id": "A0", "tile_id": "t0,0"}]
        # Mark center as built for construction demos
        for t in tiles:
            if t["tile_id"] == "t0,0":
                t["built"] = True
        drv = DeepCodeBoardDriver(seed=seed, tiles=tiles, units=units)
        return drv
    # Default to Grok native (7-tile move only)
    # For Grok native we still go through a thin adapter so the viewer API is uniform.
    # We synthesize a minimal driver using the Grok Field directly.
    return _GrokNativeDriver(seed=seed)


def _build_hex_tiles(layers: int) -> list[dict[str, Any]]:
    """Generate axial hex tiles for a centered hex of given radius (layers)."""
    tiles = []
    for q in range(-layers, layers + 1):
        for r in range(-layers, layers + 1):
            if abs(q) + abs(q + r) + abs(r) <= layers:
                tiles.append({"tile_id": f"t{q},{r}", "q": q, "r": r, "built": False})
    return tiles


class _GrokNativeDriver:
    """Minimal wrapper so the viewer can drive the pure Grok Field the same way."""

    def __init__(self, seed: int = 101):
        from ahbg.patch import Field, tile_from_ucns
        self._from_naming = "grok"
        self._to_naming = "grok"
        tiles = tile_from_ucns()
        self._field = Field.open(seed, tiles, [{"unit_id": "A0", "tile_id": tiles[0]["tile_id"]}])
        self._turn = 0
        self._last_obs = None

    def observe(self):
        snap = self._field.snapshot()
        self._last_obs = normalize_observation(snap, from_naming="grok", to_naming="grok")
        # Grok Field does not track "built"; treat everything as present
        for t in self._last_obs["tiles"]:
            t["built"] = True
        return self._last_obs

    def empty_neighbors(self, unit_id="A0"):
        from bridges.common import empty_neighbors_from_observation
        obs = self._last_obs or self.observe()
        return empty_neighbors_from_observation(obs, unit_id, naming="grok")

    def submit_choice(self, choice):
        if choice.get("kind") != "relocate":
            return []
        # Directly apply on the Grok Field
        unit_id = choice["unit_id"]
        dest = choice["to_tile_id"]
        # Find current position
        current = None
        for u in self._field.occupants.values():
            if u.unit_id == unit_id:
                current = u.tile_id
                break
        if current:
            try:
                self._field.apply_moves([(unit_id, current, dest)])
                return [{"unit_id": unit_id, "from_tile_id": current, "to_tile_id": dest}]
            except Exception:
                return []
        return []

    def submit_build(self, unit_id, tile_id):
        # Grok native Field in this workspace does not have build yet
        return []

    def submit_plan(self, plan):
        for action in plan.get("actions", []):
            if action.get("kind") == "move":
                self.submit_choice({
                    "kind": "relocate",
                    "unit_id": action["data"]["unit_id"],
                    "to_tile_id": action["data"]["to_tile_id"],
                })
        return []

    def end_turn(self):
        self._turn += 1
        return ""

    def replay_check(self):
        return True

    def current_digest(self):
        return f"grok-native-{self._turn}"


class Viewer:
    def __init__(self, driver, title="AHBG Viewer"):
        pg = _get_pygame()
        pg.init()
        self.driver = driver
        self.screen = pg.display.set_mode((1024, 768), pg.RESIZABLE)
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("monospace", 14)
        self.bigfont = pg.font.SysFont("monospace", 18)

        self.zoom = 1.0
        self.offset = [0.0, 0.0]
        self.dragging = False
        self.last_mouse = (0, 0)

        self.obs = None
        self.running = True
        self.auto_step = False
        self.step_delay = 120  # ms
        self.last_step = 0

        self._refresh()

    def _refresh(self):
        self.obs = self.driver.observe()

    def _tile_center(self, tile: dict[str, Any]) -> tuple[float, float]:
        q, r = int(tile["q"]), int(tile["r"])
        size = 18.0 * self.zoom
        cx, cy = hex_center(q, r, size)
        return cx + self.offset[0] + 400, cy + self.offset[1] + 320

    def _screen_to_axial(self, sx: int, sy: int) -> tuple[int, int] | None:
        """Crude inverse: find closest tile center."""
        best = None
        best_d = 1e9
        size = 18.0 * self.zoom
        for t in self.obs.get("tiles", []):
            cx, cy = self._tile_center(t)
            d = (cx - sx) ** 2 + (cy - sy) ** 2
            if d < best_d:
                best_d = d
                best = (int(t["q"]), int(t["r"]))
        return best

    def draw(self):
        pg = _get_pygame()
        self.screen.fill((18, 18, 22))

        if not self.obs:
            return

        size = 18.0 * self.zoom

        # Draw tiles
        for t in self.obs.get("tiles", []):
            cx, cy = self._tile_center(t)
            corners = hex_corners(cx, cy, size)
            built = bool(t.get("built", True))
            color = (70, 140, 90) if built else (55, 55, 65)
            pg.draw.polygon(self.screen, color, corners)
            pg.draw.polygon(self.screen, (30, 30, 35), corners, 1)

            # Label
            label = t.get("tile_id", "")
            txt = self.font.render(label, True, (200, 200, 210))
            self.screen.blit(txt, (cx - 12, cy - 6))

        # Draw units
        for u in self.obs.get("units", []):
            ax = label_to_axial(str(u["tile_id"]), naming="grok")  # tolerant
            # Find matching tile record for position
            tile_rec = next((tt for tt in self.obs.get("tiles", []) if tt["tile_id"] == u["tile_id"]), None)
            if tile_rec:
                cx, cy = self._tile_center(tile_rec)
            else:
                cx, cy = hex_center(*ax, size) 
                cx += self.offset[0] + 400
                cy += self.offset[1] + 320
            pg.draw.circle(self.screen, (220, 180, 60), (int(cx), int(cy)), int(size * 0.55))
            ulabel = self.font.render(u.get("unit_id", "?"), True, (20, 20, 25))
            self.screen.blit(ulabel, (cx - 8, cy - 6))

        # HUD
        hud = [
            f"turn: {self.obs.get('turn', 0)}",
            f"tiles: {len(self.obs.get('tiles', []))}",
            f"zoom: {self.zoom:.1f}",
            "LMB: move   RMB/Ctrl: build   SPACE: auto   +/-: zoom   arrows/drag: pan   Q: quit",
        ]
        y = 8
        for line in hud:
            surf = self.font.render(line, True, (230, 230, 240))
            self.screen.blit(surf, (8, y))
            y += 16

        pg.display.flip()

    def handle_event(self, event):
        pg = _get_pygame()
        if event.type == pg.QUIT:
            self.running = False
        elif event.type == pg.KEYDOWN:
            if event.key in (pg.K_q, pg.K_ESCAPE):
                self.running = False
            elif event.key == pg.K_SPACE:
                self.auto_step = not self.auto_step
            elif event.key in (pg.K_PLUS, pg.K_EQUALS):
                self.zoom = min(4.0, self.zoom * 1.2)
            elif event.key == pg.K_MINUS:
                self.zoom = max(0.3, self.zoom / 1.2)
            elif event.key == pg.K_r:
                # reset by recreating driver (simple)
                self.driver = make_driver("deepcode" if isinstance(self.driver, DeepCodeBoardDriver) else "codex")
                self._refresh()
            elif event.key in (pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN):
                dx = 30 if event.key == pg.K_LEFT else -30 if event.key == pg.K_RIGHT else 0
                dy = 30 if event.key == pg.K_UP else -30 if event.key == pg.K_DOWN else 0
                self.offset[0] += dx
                self.offset[1] += dy
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # left = move
                self._try_move(event.pos)
            elif event.button == 3 or (event.button == 1 and pg.key.get_mods() & pg.KMOD_CTRL):
                self._try_build(event.pos)
            elif event.button == 4:  # wheel up
                self.zoom = min(4.0, self.zoom * 1.1)
            elif event.button == 5:
                self.zoom = max(0.3, self.zoom / 1.1)
        elif event.type == pg.MOUSEMOTION and event.buttons[0]:
            if not self.dragging:
                self.dragging = True
            dx, dy = event.rel
            self.offset[0] += dx
            self.offset[1] += dy
        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False

    def _try_move(self, pos):
        ax = self._screen_to_axial(*pos)
        if not ax:
            return
        obs = self.obs
        unit = obs["units"][0]["unit_id"] if obs.get("units") else "A0"
        empty = self.driver.empty_neighbors(unit)
        label = axial_to_label(ax, naming="grok")
        if label in empty:
            choice = {"kind": "relocate", "unit_id": unit, "from_tile_id": obs["units"][0]["tile_id"], "to_tile_id": label}
            self.driver.submit_choice(choice)
            self.driver.end_turn()
            self._refresh()

    def _try_build(self, pos):
        ax = self._screen_to_axial(*pos)
        if not ax:
            return
        label = axial_to_label(ax, naming="grok")
        # Find buildable
        obs = self.obs
        unit = obs["units"][0]["unit_id"] if obs.get("units") else "A0"
        buildables = unbuilt_adjacent_from_observation(obs, unit, naming="grok")
        if label in buildables:
            # Use generic plan submit if available
            if hasattr(self.driver, "submit_build"):
                self.driver.submit_build(unit, label)
            else:
                plan = {"turn": obs.get("turn", 0), "actions": [{"kind": "build", "data": {"unit_id": unit, "tile_id": label}}]}
                if hasattr(self.driver, "submit_plan"):
                    self.driver.submit_plan(plan)
            self.driver.end_turn()
            self._refresh()

    def step(self):
        # Auto step: prefer construction when available on boards that support it,
        # otherwise move. Only close the turn (end_turn) after an actual submit
        # that opens a turn on the underlying controller (Codex requires it).
        obs = self.obs
        if not obs.get("units"):
            # nothing to do; avoid end_turn without a begin
            self._refresh()
            return

        unit = obs["units"][0]["unit_id"]
        did_action = False

        # Prefer build if the board exposes buildables and the driver can accept builds
        buildables = unbuilt_adjacent_from_observation(obs, unit, naming="grok")
        can_build = bool(buildables) and (hasattr(self.driver, "submit_build") or hasattr(self.driver, "submit_plan"))
        if can_build:
            # Only attempt build on drivers that will actually act on it.
            # (Codex base driver ignores builds; Grok native returns [].)
            try:
                if hasattr(self.driver, "submit_build"):
                    ev = self.driver.submit_build(unit, buildables[0])
                    did_action = bool(ev) or True  # even empty list means we tried to open
                else:
                    plan = {
                        "turn": obs.get("turn", 0),
                        "actions": [{"kind": "build", "data": {"unit_id": unit, "tile_id": buildables[0]}}],
                    }
                    ev = self.driver.submit_plan(plan)
                    did_action = True
            except Exception:
                did_action = False

        if not did_action:
            empty = self.driver.empty_neighbors(unit)
            if empty:
                choice = {"kind": "relocate", "unit_id": unit, "to_tile_id": empty[0]}
                try:
                    self.driver.submit_choice(choice)
                    did_action = True
                except Exception:
                    did_action = False

        if did_action:
            # Codex requires explicit end_turn after begin+resolve in submit_choice/submit_plan.
            # DeepCode end_turn is a no-op digest; Grok native increments.
            try:
                self.driver.end_turn()
            except Exception:
                pass
        self._refresh()

    def run(self):
        pg = _get_pygame()
        while self.running:
            for event in pg.event.get():
                self.handle_event(event)

            now = pg.time.get_ticks()
            if self.auto_step and now - self.last_step > self.step_delay:
                self.step()
                self.last_step = now

            self.draw()
            self.clock.tick(60)

        pg.quit()


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--driver", default="deepcode", choices=["deepcode", "codex", "grok"])
    parser.add_argument("--layers", type=int, default=6, help="Hex layers for construction board (deepcode)")
    parser.add_argument("--seed", type=int, default=101)
    args = parser.parse_args(argv)

    driver = make_driver(args.driver, layers=args.layers, seed=args.seed)
    title = f"AHBG Viewer — {args.driver} (layers={args.layers if args.driver=='deepcode' else 1})"
    viewer = Viewer(driver, title=title)
    viewer.run()


if __name__ == "__main__":
    main()
