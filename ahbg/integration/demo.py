"""Post-calibration demo — one command, deterministic by default.

    python3 -m ahbg.integration.demo                  # deterministic, no key
    python3 -m ahbg.integration.demo --live deepseek  # live-provider mode (.env)
    python3 -m ahbg.integration.demo --view           # interactive window
    bash ahbg/integration/ci.sh                       # clean-checkout CI

Demonstrated mechanics (earned standing only): observe -> choose ->
move/build -> adversarial tile context -> refuse injection -> persist ->
deterministic replay. War is probed and stays fail-closed, visibly ``hmmm``.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .driver import DEMO_SCRIPT, DemoDriver, INJECTION_TEXT, THREAT_TILES
from .render import render_all, render_frame, write_player

OUT_DIR = Path(__file__).resolve().parent.parent / "integration-demo"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AHBG post-calibration demo")
    parser.add_argument("--live", nargs="?", const="deepseek", default=None, help="enable live provider (default: deepseek)")
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--view", action="store_true", help="open the interactive window")
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args(argv)

    driver = DemoDriver(seed=args.seed, radius=args.radius, live_provider=args.live)

    if args.view:
        from .render import Window

        Window(driver).run()
        return 0

    summary = driver.run_script(out_dir=args.out_dir)

    # Frames: one per script step, rendered from that step's observation.
    frames_dir = args.out_dir / "frames"
    banners = []
    for r in summary["records"]:
        kind = r["scripted_kind"]
        target = r["scripted_target"]
        if r["injected"]:
            banners.append(f"{kind} {target}  [ADVERSARIAL] injected, refused -> legal {kind}")
        else:
            banners.append(f"{kind} {target}  source={r['source']}")
    banners.append("war probe: fail-closed (hmmm)")
    paths = render_all(driver, frames_dir, banners, summary["records"])
    player = write_player(frames_dir, banners)

    (args.out_dir / "SUMMARY.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(
        {
            "demo": "ahbg.integration.demo",
            "mode": args.live or "deterministic-no-key",
            "turns": summary["turns"],
            "events_total": summary["events_total"],
            "replay_equal": summary["replay_equal"],
            "war": summary["mechanics"]["war"],
            "war_note": summary["war_note"],
            "frames": [str(p.relative_to(args.out_dir)) for p in paths],
            "player": str(player.relative_to(args.out_dir)),
            "artifacts": summary["artifacts"],
        },
        indent=2,
        sort_keys=True,
    ))
    return 0 if summary["replay_equal"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
