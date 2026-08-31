"""Minimal demonstration: run Grok's a0 regulatory surface on foreign boards.

Intended to be executed from inside the Grok AHBG workspace:

    cd stack/ahbg/grok
    PYTHONDONTWRITEBYTECODE=1 python3 bridges/demo.py

This drives both Codex and DeepCode boards using the exact same Grok
regulatory code (Vessel + choose_relocate) through the bridges.

The bridges handle label translation (Grok BandSlot <-> short axial labels)
and observation shaping while preserving each foreign board's collision
semantics (Codex/DeepCode War remains UnresolvedHmmm; Grok's own board
resolves war_v3 deterministically).
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure we can import the local Grok a0/ as "a0" when running the demo directly.
WORKSPACE = Path(__file__).resolve().parent.parent
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))

from a0.selfhood import Vessel
from a0.will import choose_relocate

from bridges.codex import CodexBoardDriver
from bridges.deepcode import DeepCodeBoardDriver


def drive_board(driver, name: str, turns: int = 3) -> dict[str, int]:
    """Drive a foreign board for N turns using Grok's choose_relocate."""
    vessel = Vessel.instantiate(salt=f"bridge-{name}")
    unit_id = "A0"

    stats = {"turns": 0, "relocates": 0, "defers": 0, "errors": 0}

    for t in range(turns):
        try:
            obs = driver.observe()
            empty = driver.empty_neighbors(unit_id)

            # Find current position (in the naming the driver exposes to Grok)
            current_tile = None
            for u in obs.get("units", []):
                if u.get("unit_id") == unit_id:
                    current_tile = u.get("tile_id")
                    break

            choice = choose_relocate(
                vessel,
                unit_id=unit_id,
                at=current_tile or "CENTER",
                empty_neighbors=empty,
                world=obs,
            )

            if choice.get("kind") == "relocate":
                driver.submit_choice(choice)
                stats["relocates"] += 1
            else:
                stats["defers"] += 1

            driver.end_turn()
            stats["turns"] += 1
        except Exception as e:
            stats["errors"] += 1
            print(f"[{name}] turn {t} surfaced: {type(e).__name__}: {e}")

    return stats


def main() -> None:
    print("=== Grok a0 on Codex board ===")
    codex = CodexBoardDriver(seed=101)
    c_stats = drive_board(codex, "codex", turns=3)
    print("Codex result:", c_stats)
    print("Codex replay check:", codex.replay_check())

    print()
    print("=== Grok a0 on DeepCode board ===")
    deep = DeepCodeBoardDriver(seed=101)
    d_stats = drive_board(deep, "deepcode", turns=3)
    print("DeepCode result:", d_stats)
    print("DeepCode replay check:", deep.replay_check())

    print()
    print("Bridge demo complete.")
    print("Grok's regulatory surface (Vessel + choose_relocate) operated on")
    print("both foreign AHBG boards via the bridges.")


if __name__ == "__main__":
    main()
