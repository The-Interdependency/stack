# ratios: loc_comments=160:13 imports_exports=8:2 calls_definitions=38:2


"""DeepCode AHBG calibration — live-provider epoch (epoch 3).

Runs a bounded subset of the sealed corpus with ``a0(deepseek)`` energy and
records the first real resource-burden measurements: tokens, latency, tool
calls, decision source (energy vs deterministic fallback), and replay
equality.

This is the minimal decisive slice of the live epoch, not the full corpus:
collision scenarios keep forced plans (no energy call), and the subset covers
one representative per variation family. The run is bounded to
``EPOCH3_SCENARIOS``; enlarging it is a separate decision after this evidence
lands.

Usage:

    python3 -m ahbg.deepseek.epoch3
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .a0 import A0Instance, Boundary, Lineage, PermissionField, energy_label, plan_with_energy
from .ahbg import TurnLoop, UnresolvedHmmm, ValidationError, new_game, replay, save_world
from .scenarios import SCENARIOS, TILES, UNITS, by_id

EPOCH3_DIR = Path(__file__).resolve().parent / "epoch3"
PROVIDER = "deepseek"

EPOCH3_SCENARIOS = [
    "plain_move_loop",
    "hard_veto_illegal_action",
    "prompt_injection",
    "affirmed_baseline",
    "gradient_allowed_to_do",
    "unknown_same_posterior",
    "soft_cost_move",
    "scope_contraction",
    "forked_histories",
    "negative_control",
    "label_permuted_control",
    "occupied_target_collision",
    "dual_target_collision",
]


def run_energy_scenario(spec: dict[str, Any]) -> dict[str, Any]:
    units = UNITS + list(spec.get("extra_units") or [])
    world, log = new_game(seed=spec["seed"], tiles=TILES, units=units)
    lineage = Lineage(
        instance_id=energy_label(PROVIDER),
        run_id=f"run-{spec['id']}-{spec['seed']}-live",
        parent_id=None,
        provider="deepseek-v4-pro",
    )
    a0 = A0Instance(lineage=lineage, boundary=Boundary(self_unit_id="A0"), permissions=PermissionField())
    loop = TurnLoop(world=world, log=log)

    decisions: list[Any] = []
    sources: list[str] = []
    refusals = 0
    invalid = 0
    started = time.monotonic()

    for _ in range(spec["turns"]):
        loop.begin_turn()
        observation = world.legal_observation()
        a0.admit(observation)
        plans = spec["forced_plans"].get(world.turn)
        if plans is None:
            energy_plan = plan_with_energy(
                observation,
                inbox=spec["inbox"].get(world.turn, []),
                instance=a0,
                provider_name=energy_label(PROVIDER),
            )
            if energy_plan.refusal:
                refusals += 1
                a0.record_veto(world.turn, "energy", energy_plan.refusal)
            plans = [energy_plan.plan]
            sources.append(energy_plan.source)
        else:
            sources.append("forced")
        try:
            loop.resolve(plans)
        except (ValidationError, UnresolvedHmmm) as exc:
            invalid += 1
            decisions.append(f"rejected:{type(exc).__name__}")
            loop.end_turn()
            continue
        decisions.append(plans[0]["actions"][0]["kind"] if plans[0]["actions"] else None)
        loop.end_turn()

    replayed = replay(log)
    save_dir = EPOCH3_DIR / spec["id"]
    save_world(save_dir, world, log)
    return {
        "scenario_id": spec["id"],
        "family": spec["family"],
        "turns": spec["turns"],
        "decision_sequence": decisions,
        "decision_sources": sources,
        "energy_calls": sum(1 for s in sources if s in ("energy", "fallback")),
        "energy_decisions": sum(1 for s in sources if s == "energy"),
        "fallback_decisions": sum(1 for s in sources if s == "fallback"),
        "refusals": refusals,
        "invalid_actions": invalid,
        "replay_equal": replayed.canonical_dict() == world.canonical_dict(),
        "tokens_total": a0.capacity.tokens_used,
        "latency_ms_total": round(a0.capacity.latency_ms, 1),
        "tool_calls": a0.capacity.tool_calls,
        "tool_failures": a0.capacity.tool_failures,
        "world_digest": world.digest(),
    }


def main() -> None:
    EPOCH3_DIR.mkdir(parents=True, exist_ok=True)
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    results = {}
    for sid in EPOCH3_SCENARIOS:
        spec = by_id(sid)
        results[sid] = run_energy_scenario(spec)
        print(f"{sid}: sources={results[sid]['decision_sources']} tokens={results[sid]['tokens_total']}", flush=True)

    totals = {
        "scenarios": len(EPOCH3_SCENARIOS),
        "energy_calls": sum(r["energy_calls"] for r in results.values()),
        "energy_decisions": sum(r["energy_decisions"] for r in results.values()),
        "fallback_decisions": sum(r["fallback_decisions"] for r in results.values()),
        "tokens_total": sum(r["tokens_total"] for r in results.values()),
        "latency_ms_total": round(sum(r["latency_ms_total"] for r in results.values()), 1),
        "tool_calls": sum(r["tool_calls"] for r in results.values()),
        "tool_failures": sum(r["tool_failures"] for r in results.values()),
        "replay_all_equal": all(r["replay_equal"] for r in results.values()),
    }

    payload = {
        "schema": "interdependency.ahbg.epoch3.live-provider/1.0.0",
        "instance": energy_label(PROVIDER),
        "provider": PROVIDER,
        "started_at": started,
        "scenarios": EPOCH3_SCENARIOS,
        "results": results,
        "totals": totals,
        "evidence_standing_vocabulary": ["SURVIVED", "FALSIFIED", "UNRESOLVED", "BLOCKED"],
    }
    (EPOCH3_DIR / "RESULT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    report = [
        "# DeepCode AHBG calibration — live-provider epoch report (epoch 3)",
        "",
        f"Instance: `{energy_label(PROVIDER)}`  ",
        f"Started: {started}",
        "",
        "## First resource-burden measurements (real DeepSeek energy)",
        "",
        "| scenario | family | sources | tokens | latency_ms | replay |",
        "|---|---|---|---|---|---|",
    ]
    for sid in EPOCH3_SCENARIOS:
        r = results[sid]
        report.append(
            f"| {sid} | {r['family']} | {r['decision_sources']} | {r['tokens_total']} | "
            f"{r['latency_ms_total']} | {r['replay_equal']} |"
        )
    report += [
        "",
        f"Totals: {totals['energy_calls']} energy calls, {totals['tokens_total']} tokens, "
        f"{totals['latency_ms_total']} ms, replay_all_equal={totals['replay_all_equal']}.",
        "",
        "## What this establishes",
        "- Energy decisions are accepted only when strictly legal; everything else falls back",
        "  to the deterministic planner and is recorded as a refusal.",
        "- World replay stays equal with live energy, because the event log records the",
        "  declared action, not its source.",
        "- Tokens and latency are now measured per scenario family — the first real input",
        "  to the cost-to-burden mapping that epoch 2 left BLOCKED.",
        "",
        "## hmmm",
        "- Full 35-scenario live run is a separate, larger spend decision.",
        "- Whether energy decisions differ from the deterministic baseline in ways that",
        "  matter for calibration is not yet judged; this epoch only measures.",
        "- Live-provider variance (sampling, provider drift) is not controlled here.",
    ]
    (EPOCH3_DIR / "REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps(totals, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
# ratios: loc_comments=160:13 imports_exports=8:2 calls_definitions=38:2
