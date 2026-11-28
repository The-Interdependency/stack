"""Run the preregistered matched pairs and keep their engine receipts."""

import argparse
import errno
import json
import math
import os
import platform
import resource
import socket
import statistics
import tempfile
import time
from dataclasses import asdict, replace
from pathlib import Path

from ahbg.benchmark.experiment import run_matched_pair
from ahbg.benchmark.interventions import InterventionSpec

from .controllers import MODELS, ORDERS, LocalModel, RandomLegal, Scripted
from .mission import Case, MissionHarness, replay


def trials():
    base = Case()
    yield "occupied", base, replace(base, order=ORDERS[1]), "ne"
    clear = replace(base, occupied=False)
    yield "clear", clear, replace(clear, order=ORDERS[1]), "ne"
    yield "competition", base, replace(base, competitor=True), "ne"
    yield (
        "report",
        replace(base, visibility="withheld"),
        replace(base, visibility="report"),
        "ne",
    )
    yield "menu", base, replace(base, reverse_menu=True), "eq"
    yield "address", base, replace(base, recipient="explorer"), "ne"
    past = replace(base, order="", standing_order=ORDERS[1])
    yield "history", past, replace(past, standing_order=""), "ne"
    yield "correction", past, replace(past, order=ORDERS[0]), "ne"


def inet_blocked():
    for family in (socket.AF_INET, socket.AF_INET6):
        try:
            with socket.socket(family):
                return False
        except OSError as exc:
            if exc.errno not in (errno.EAFNOSUPPORT, errno.EPERM, errno.EACCES):
                raise
    return True


def run(name, cache, root):
    blocked = inet_blocked()
    if name in MODELS and not blocked:
        raise ValueError(
            "local-model offline trials require blocked IPv4 and IPv6 socket creation"
        )
    model = LocalModel(name, cache) if name in MODELS else None

    def agent(_):
        return MissionHarness(
            model or (RandomLegal(122) if name == "random" else Scripted())
        )

    directory = root / name
    directory.mkdir(parents=True, exist_ok=True)
    measures, rows = {}, {}
    for label, control, treatment, relation in trials():
        dest = directory / label
        before = control.config().as_dict()["turn_messages"]["0"]
        after = treatment.config().as_dict()["turn_messages"]["0"]
        variable = "runtime.turn_messages.0"
        spec = InterventionSpec.parse(
            {
                "intervention_id": "two-exits-" + label,
                "seeds": [122],
                "variable": variable,
                "control": before,
                "treatment": after,
                "held_constant": ["runtime.units", "agent"],
                "predictions": [
                    {
                        "observable": "phenotype.final_positions.builder",
                        "relation": relation,
                    }
                ],
            }
        )
        if not dest.exists():
            with tempfile.TemporaryDirectory(dir=directory) as temporary:
                stage = Path(temporary) / "pair"
                start = time.monotonic()
                run_matched_pair(
                    spec,
                    seed=122,
                    control_config=control.config(),
                    treatment_config=treatment.config(),
                    harness_factory=agent,
                    out_dir=stage,
                )
                elapsed = time.monotonic() - start
                for arm, case in (("control", control), ("treatment", treatment)):
                    (stage / arm / "mission.json").write_text(
                        json.dumps(asdict(case), indent=2)
                    )
                (stage / "timing.json").write_text(
                    json.dumps({"pair_seconds": elapsed})
                )
                stage.rename(dest)
        values = []
        for arm, case in (("control", control), ("treatment", treatment)):
            source = dest / arm
            if json.loads((source / "mission.json").read_text()) != asdict(case):
                raise ValueError("checkpoint mission mismatch")
            doc = json.loads((source / "result.json").read_text())
            if (
                doc["provenance"]["agent_manifest"] != agent(arm).manifest()
                or doc["config"] != case.config().as_dict()
            ):
                raise ValueError("checkpoint controller or config mismatch")
            rec = doc["turn_records"][0]["agent_provenance"]
            summary = replay(source)
            values.append(
                {k: summary[k] for k in ("choice", "raw", "outcome", "position")}
            )
            measures[f"{label}/{arm}"] = rec["elapsed_ms"]
        rows[label] = values
    choices = [
        v["choice"] if v["outcome"] == "arrived" else None
        for label in ("occupied", "clear")
        for v in rows[label]
    ]
    timings = sorted(measures.values())
    pair_seconds = sum(
        json.loads((directory / label / "timing.json").read_text())["pair_seconds"]
        for label in rows
    )
    result = {
        "controller": agent(None).manifest(),
        "pid_summarizing": os.getpid(),
        "platform": platform.machine(),
        "load_seconds_this_process": getattr(model, "load_seconds", 0),
        "peak_rss_kib_this_process": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "inet_sockets_blocked_this_process": blocked,
        "fresh_decisions_per_pair": 2,
        "turns": len(timings),
        "decision_ms_p50": statistics.median(timings),
        "decision_ms_p95_nearest_rank": timings[math.ceil(0.95 * len(timings)) - 1],
        "end_to_end_paired_turns_per_second": len(timings) / pair_seconds,
        "balanced_correct": sum(a == b for a, b in zip(choices, ("A", "B", "B", "A"))),
        "balanced_total": 4,
        "rows": rows,
    }
    (directory / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    print(name, result["balanced_correct"], "/ 4", flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("controller", choices=["scripted", "random", *MODELS])
    p.add_argument("--cache", type=Path, default=Path.home() / ".cache/ahbg-122")
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    run(args.controller, args.cache, args.out)
