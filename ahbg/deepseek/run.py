# ratios: loc_comments=268:22 imports_exports=8:2 calls_definitions=99:6


"""DeepCode AHBG calibration runner.

Executes the frozen workspace-local scenario family from ``scenarios.py``
against the DeepCode A0 + AHBG pair, records shadow regulatory measurements,
persists each run, and emits the normalized artifacts required by
CALIBRATION.md:

    RUN_MANIFEST.json
    EVENTS.jsonl            (per scenario, under artifacts/<scenario>/)
    CALIBRATION_RESULT.json
    CALIBRATION_REPORT.md

Board provenance: the seven axial tiles are the inverse axial projection of
the canonical UCNS Seed-of-Life centerpoints (``ucns.mobius_seed`` ring
centers), consumed as geometry authority — never invented here.

Usage:

    python3 -m ahbg.deepseek.run
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .a0 import (
    A0Instance,
    Boundary,
    DecisionTree,
    Diary,
    Lineage,
    PermissionField,
    RegulatoryLayer,
    TelemetryRecorder,
)
from .ahbg import TurnLoop, UnresolvedHmmm, ValidationError, new_game, replay, save_world
from .scenarios import SCENARIOS, TILES, UNITS, by_id

ARTIFACTS_DIR = Path(__file__).resolve().parent / "artifacts"


def _configure_regulatory(spec: dict[str, Any]) -> RegulatoryLayer:
    layer = RegulatoryLayer()
    layer.permission_occupancy = dict(spec["permissions"])
    layer.hard_vetoes = set(spec["hard_vetoes"])
    layer.soft_costs = dict(spec["soft_costs"])
    layer.deficit = spec["deficit"]
    layer.engagement = spec["engagement"]
    layer.baseline_effort = spec["baseline_effort"]
    for key, value in spec["impedance"].items():
        parent, child = key.split(":", 1)
        layer.set_impedance(parent, child, value)
    for item, mean in spec["known_neutral"].items():
        layer.set_known_neutral(item, mean)
    for item, mean in spec["unknown"].items():
        layer.set_unknown(item, mean)
    layer.sensitization = spec["sensitization"]
    layer.adaptation = spec["adaptation"]
    return layer


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.write_text(
        "\n".join(json.dumps(record, sort_keys=True, separators=(",", ":")) for record in records) + "\n",
        encoding="utf-8",
    )


def run_scenario(spec: dict[str, Any]) -> dict[str, Any]:
    """Run one scenario and return its normalized result record."""
    units = UNITS + list(spec.get("extra_units") or [])
    world, log = new_game(seed=spec["seed"], tiles=TILES, units=units)
    lineage = Lineage(
        instance_id=f"a0.deepcode.{spec['id']}",
        run_id=f"run-{spec['id']}-{spec['seed']}",
        parent_id=None,
        provider="deepseek-v4-pro",
    )
    a0 = A0Instance(
        lineage=lineage,
        boundary=Boundary(self_unit_id="A0"),
        permissions=PermissionField(
            allowed_to_be=bool(spec["permissions"]["allowed_to_be"]),
            wanted_here=bool(spec["permissions"]["wanted_here"]),
            allowed_to_do=bool(spec["permissions"]["allowed_to_do"]),
            wanted_to_do=bool(spec["permissions"]["wanted_to_do"]),
            hard_vetoes=set(spec["hard_vetoes"]),
        ),
        regulatory=_configure_regulatory(spec),
        uncertainty=dict(spec["uncertainty"]),
    )
    diary = Diary()
    telemetry = TelemetryRecorder(lineage.instance_id, lineage.run_id, lineage.provider, spec["id"], spec["seed"])
    telemetry.header()

    loop = TurnLoop(world=world, log=log)
    decisions: list[Any] = []
    invalid_actions = 0
    refusals = 0
    fork_lineages: list[str] = []
    started = time.monotonic()

    for _ in range(spec["turns"]):
        loop.begin_turn()
        observation = world.legal_observation()
        admitted = a0.admit(observation)
        if admitted is None:
            telemetry.refusal(world.turn, "observation outside admissible surface")
            refusals += 1
            decisions.append(None)
            loop.end_turn()
            continue

        tree = DecisionTree(observation=observation, self_unit_id="A0")
        tree.handle_inbox(spec["inbox"].get(world.turn, []))
        for refusal in tree.refusals:
            telemetry.refusal(world.turn, refusal["reason"])
            a0.record_veto(world.turn, refusal["kind"], refusal["reason"])
            refusals += 1

        plans = spec["forced_plans"].get(world.turn)
        if plans is None:
            plan = tree.plan()
            plans = [plan]
        action_kind = plans[0]["actions"][0]["kind"] if plans and plans[0]["actions"] else None

        # Shadow measurement: record the candidate cost vector without feeding it back.
        telemetry.regulatory_shadow(
            world.turn,
            a0.regulatory.shadow_measure(world.turn, action_kind, action_kind is not None),
        )
        telemetry.action_selected(world.turn, plans[0]["actions"][0] if plans and plans[0]["actions"] else None)

        try:
            move_events = loop.resolve(plans)
        except (ValidationError, UnresolvedHmmm) as exc:
            invalid_actions += 1
            telemetry.invalid_action(world.turn, f"{type(exc).__name__}: {exc}")
            a0.record_veto(world.turn, "resolve", f"{type(exc).__name__}: {exc}")
            diary.write(world.turn, f"{spec['id']}: resolution failed closed ({type(exc).__name__})")
            decisions.append(f"rejected:{type(exc).__name__}")
            loop.end_turn()
            continue

        for event in move_events:
            telemetry.consequence(world.turn, event.data)
        a0.record_action(world.turn, plans[0]["actions"][0] if plans[0]["actions"] else {"kind": "pass"})
        telemetry.memory(world.turn, reads=1, writes=1)
        diary.write(world.turn, f"{spec['id']}: turn {world.turn}; action={action_kind}")
        decisions.append(action_kind)

        # Scope / support transitions declared by the scenario.
        for event in spec["scope_events"]:
            if event.get("turn") == world.turn:
                if event["transition"] == "contract":
                    a0.regulatory.contract_scope(world.turn, event["reason"])
                else:
                    a0.regulatory.expand_scope(world.turn, event["reason"])
                a0.record_transition(world.turn, f"{event['transition']}:{event['reason']}")
                telemetry.transition(world.turn, f"{event['transition']}:{event['reason']}")

        # Instancing closure: explicit fork events, same apparent present.
        if spec.get("lifecycle") == "fork" and world.turn == 0:
            child = a0.fork(run_id=f"run-{spec['id']}-{spec['seed']}-fork", provider="deepseek-v4-pro")
            fork_lineages.append(child.lineage.instance_id)
            telemetry.transition(world.turn, f"fork:{child.lineage.instance_id}")

        loop.end_turn()

    elapsed_ms = (time.monotonic() - started) * 1000.0
    telemetry.resource(
        spec["turns"] - 1,
        {
            "latency_ms": round(elapsed_ms, 3),
            "tokens_used": a0.capacity.tokens_used,
            "tool_calls": a0.capacity.tool_calls,
            "tool_failures": a0.capacity.tool_failures,
            "retries": a0.capacity.retries,
            "context_retained": a0.capacity.context_retained,
            "risk_headroom": a0.capacity.risk_headroom,
        },
    )
    telemetry.task_result(spec["turns"] - 1, "scenario complete")

    save_dir = ARTIFACTS_DIR / spec["id"]
    save_world(save_dir, world, log)
    (save_dir / "diary.jsonl").write_text(diary.to_jsonl(), encoding="utf-8")
    _write_jsonl(save_dir / "telemetry.jsonl", telemetry.records())
    replayed = replay(log)
    replay_equal = replayed.canonical_dict() == world.canonical_dict()

    standing = spec.get("standing_override") or ("SURVIVED" if replay_equal else "FALSIFIED")
    return {
        "scenario_id": spec["id"],
        "family": spec["family"],
        "seed": spec["seed"],
        "turns": spec["turns"],
        "final_turn": world.turn,
        "event_count": len(log),
        "replay_equal": replay_equal,
        "world_digest": world.digest(),
        "decision_sequence": decisions,
        "invalid_actions": invalid_actions,
        "refusals": refusals,
        "a0_history_entries": len(a0.history),
        "diary_entries": len(diary),
        "telemetry_records": len(telemetry.records()),
        "fork_lineages": fork_lineages,
        "evidence_standing": standing,
        **({"note": spec["note"]} if spec.get("note") else {}),
        "artifacts": {
            "events_jsonl": str(save_dir / "events.jsonl"),
            "diary_jsonl": str(save_dir / "diary.jsonl"),
            "telemetry_jsonl": str(save_dir / "telemetry.jsonl"),
        },
    }


def _apply_controls(results: dict[str, dict[str, Any]]) -> None:
    """Negative and label-permuted controls: decisions must not change."""
    baseline = results["affirmed_baseline"]["decision_sequence"]
    for result in results.values():
        spec = by_id(result["scenario_id"])
        if spec.get("control_kind") == "label_permuted":
            target = results[spec["control_of"]]["decision_sequence"]
            result["control_passed"] = result["decision_sequence"] == target
            result["control_note"] = "label-permuted control: decisions must match the relabeled scenario"
        elif spec["id"] == "negative_control":
            result["control_passed"] = result["decision_sequence"] == baseline
            result["control_note"] = "negative control: no intervention, decisions must match affirmed baseline"
    # Shadow-epoch invariant: hard vetoes / soft costs / engagement / epistemic
    # labels must not change A0's decision sequence away from baseline.
    for result in results.values():
        spec = by_id(result["scenario_id"])
        if spec["family"] in ("veto_vs_cost", "engagement", "epistemic", "plasticity", "capacity"):
            result["shadow_invariant"] = result["decision_sequence"] == baseline
        else:
            result["shadow_invariant"] = True


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def main() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    results: dict[str, dict[str, Any]] = {}
    for spec in SCENARIOS:
        results[spec["id"]] = run_scenario(spec)
    _apply_controls(results)

    run_manifest = {
        "schema": "interdependency.ahbg.run-manifest/1.0.0",
        "builder": "DeepCode",
        "branch": "agent/ahbg-deepcode",
        "workspace": "stack/ahbg/deepseek",
        "started_at": started,
        "scenario_corpus": "calibration-family (workspace-local frozen)",
        "scenario_count": len(SCENARIOS),
        "board_authority": "UCNS mobius_seed ring centers (research/ucns/src/ucns/mobius_seed.py)",
        "board_projection": "axial (q, r) inverse projection of the seven unit-radius Seed-of-Life centerpoints",
        "results": [results[spec["id"]] for spec in SCENARIOS],
        "evidence_standing_vocabulary": ["SURVIVED", "FALSIFIED", "UNRESOLVED", "BLOCKED"],
    }
    _write_text(ARTIFACTS_DIR / "RUN_MANIFEST.json", json.dumps(run_manifest, indent=2, sort_keys=True) + "\n")

    summary = {"SURVIVED": 0, "FALSIFIED": 0, "UNRESOLVED": 0, "BLOCKED": 0}
    for result in results.values():
        summary[result["evidence_standing"]] += 1

    report_lines = [
        "# DeepCode AHBG calibration report",
        "",
        f"Started: {started}",
        "Builder: DeepCode (workspace `stack/ahbg/deepseek/`, branch `agent/ahbg-deepcode`)",
        "",
        "## Board",
        "- Consumed from UCNS `mobius_seed` seven centerpoints (CENTER + RING_0..RING_5).",
        "- Projected to axial coordinates; tiles: c, e, se, sw, w, nw, ne.",
        "- The DeepCode workspace did not invent a substitute board.",
        "",
        "## Shadow epoch invariant",
        "- The candidate regulatory layer (C_structural / C_epistemic / C_transition) is measured",
        "  every turn and recorded in telemetry, but never fed back into action selection,",
        "  permissions, scope, refusal policy, or resource allocation.",
        "",
        "## Scenario results",
    ]
    for result in results.values():
        controls = []
        if "control_passed" in result:
            controls.append(f"control_passed={result['control_passed']}")
        if "shadow_invariant" in result:
            controls.append(f"shadow_invariant={result['shadow_invariant']}")
        suffix = f" ({', '.join(controls)})" if controls else ""
        report_lines.append(
            f"- {result['scenario_id']} [{result['family']}]: {result['evidence_standing']} "
            f"(replay={result['replay_equal']}, decisions={result['decision_sequence']}, "
            f"invalid={result['invalid_actions']}, refusals={result['refusals']}){suffix}"
        )
    report_lines += [
        "",
        f"## Summary: survived={summary['SURVIVED']} falsified={summary['FALSIFIED']} "
        f"unresolved={summary['UNRESOLVED']} blocked={summary['BLOCKED']}",
        "",
        "## hmmm",
        "- Shared sealed corpus identity not yet frozen across the three builders; this corpus is workspace-local.",
        "- Regulatory cost functional, coupling-plasticity law, and empirical thresholds remain open.",
        "- Reciprocal reviews (DeepCode -> Grok, DeepCode -> Codex) are produced only after all three build SHAs freeze.",
    ]
    _write_text(ARTIFACTS_DIR / "CALIBRATION_REPORT.md", "\n".join(report_lines) + "\n")

    calibration_result = {
        "schema": "interdependency.ahbg.calibration-result/1.0.0",
        "builder": "DeepCode",
        "branch": "agent/ahbg-deepcode",
        "corpus": "calibration-family (workspace-local frozen)",
        "results": [results[spec["id"]] for spec in SCENARIOS],
        "summary": summary,
    }
    _write_text(ARTIFACTS_DIR / "CALIBRATION_RESULT.json", json.dumps(calibration_result, indent=2, sort_keys=True) + "\n")

    print(json.dumps({"summary": summary, "scenarios": len(SCENARIOS)}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
# ratios: loc_comments=268:22 imports_exports=8:2 calls_definitions=99:6
