"""Measure a fresh turn from before observation through durable runtime replay checks."""

import argparse
import json
import math
import statistics
import tempfile
import time
from pathlib import Path

from .controllers import MODELS, LocalModel, RandomLegal, Scripted
from .mission import play
from .trial import inet_blocked, trials


def measure(name, cache):
    if not inet_blocked():
        raise ValueError("run the local latency suite with IPv4 and IPv6 disabled")
    model = LocalModel(name, cache) if name in MODELS else None
    times = []
    with tempfile.TemporaryDirectory() as tmp:
        for label, control, treatment, _ in trials():
            for arm, case in (("control", control), ("treatment", treatment)):
                agent = model or (
                    RandomLegal(case.seed) if name == "random" else Scripted()
                )
                start = time.monotonic()
                turn = play(case, agent, Path(tmp) / label / arm)
                times.append(
                    {
                        "pair": label,
                        "arm": arm,
                        "end_to_end_ms": 1000 * (time.monotonic() - start),
                        "outcome": turn["outcome"],
                        "state_digest": turn["state_digest"],
                    }
                )
    values = sorted(r["end_to_end_ms"] for r in times)
    return {
        "controller": name,
        "trials": times,
        "sample_size": len(values),
        "p50_ms": statistics.median(values),
        "p95_ms_nearest_rank": values[math.ceil(0.95 * len(values)) - 1],
        "turns_per_second": len(values) * 1000 / sum(values),
        "definition": "After loading resident weights, before constructing observation to after writing mission and runtime evidence. Includes resolution and internal replay check.",
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("name", choices=[*MODELS, "random", "scripted"])
    p.add_argument("output", type=Path)
    p.add_argument("--cache", type=Path, default=Path.home() / ".cache/ahbg-122")
    a = p.parse_args()
    a.output.write_text(json.dumps(measure(a.name, a.cache), indent=2) + "\n")
