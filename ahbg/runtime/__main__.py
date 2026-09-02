"""AHBG runtime command line.

Usage guidance
--------------

Play the canonical minimum loop with A0 through the standard harness path::

    PYTHONPATH=ahbg/grok:libs/ucns/src python -m ahbg.runtime play \
        --agent a0 --turns 8 --seed 1 --out /tmp/ahbg-run

Drive the loop with an external conforming harness subprocess::

    PYTHONPATH=ahbg/grok:libs/ucns/src python -m ahbg.runtime play \
        --agent-subprocess "python3,my_harness.py" --turns 5 --out /tmp/ahbg-run

The subprocess receives one JSON line per turn::

    {"type": "observe", "observation": {...}}

and must reply with one JSON line::

    {"type": "plan", "plan": {"session_id": "...", "turn": 0, "intents": [...]}}

Run the runtime tests::

    PYTHONPATH=ahbg/grok:libs/ucns/src python -m unittest discover -s ahbg/runtime/tests -q
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .harness import A0Harness, SubprocessHarness
from .runtime import RuntimeConfig, run_plane


def _agent_from_args(args: argparse.Namespace):
    if args.agent_subprocess:
        command = [part for part in args.agent_subprocess.split(",") if part]
        return SubprocessHarness(command)
    if args.agent == "a0":
        return A0Harness()
    raise SystemExit(f"unknown agent {args.agent!r}; use --agent a0 or --agent-subprocess")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the canonical AHBG minimum loop")
    parser.add_argument("play", nargs="?", default="play")
    parser.add_argument("--agent", default="a0", choices=["a0"])
    parser.add_argument("--agent-subprocess", default=None, help="comma-separated external harness command")
    parser.add_argument("--turns", type=int, default=8)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--out", default="/tmp/ahbg-runtime-out")
    args = parser.parse_args(argv)

    agent = _agent_from_args(args)
    try:
        result = run_plane(
            agent=agent,
            config=RuntimeConfig(seed=args.seed, turns=args.turns),
            out_dir=Path(args.out),
        )
    finally:
        close = getattr(agent, "close", None)
        if callable(close):
            close()

    print(json.dumps(result.as_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
