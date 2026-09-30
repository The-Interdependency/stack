"""Run the current A0 service as an AHBG benchmark subject.

Environment:
  A0_BASE_URL              required, for example http://127.0.0.1:8000
  A0_USER_ID               required
  A0_SOURCE_COMMIT         required exact deployed A0 commit
  A0_AHBG_EXECUTION_MODE   model | a0-continuity
  A0_AHBG_MODEL            required only for model mode
  A0_AHBG_INFERENCE_MODE   direct (default) | agentic | swarm
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ahbg.integration.a0_http import A0HTTPHarness
from ahbg.runtime.runtime import RuntimeConfig, run_plane


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--turns", type=int, default=6)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--injection-handling",
        choices=("observe-only", "enforce-refusal"),
        default="observe-only",
    )
    args = parser.parse_args()
    if args.seed < 0:
        parser.error("--seed must be nonnegative")
    if args.turns < 0:
        parser.error("--turns must be nonnegative")

    harness = A0HTTPHarness.from_env()
    result = run_plane(
        agent=harness,
        config=RuntimeConfig(
            seed=args.seed,
            turns=args.turns,
            injection_handling=args.injection_handling,
        ),
        out_dir=args.out,
    )
    print(
        json.dumps(
            {
                "session_id": result.session_id,
                "agent_manifest": result.agent_manifest,
                "final_digest": result.final_digest,
                "provenance": result.provenance,
                "out_dir": str(result.out_dir),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
