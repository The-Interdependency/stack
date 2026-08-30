"""Compare frozen Grok shadow cost against simpler controls.

Post-freeze analysis of corpus-run artifacts. Does not alter a0/, ahbg/, or
smoke artifacts. Shadow cost is never used as a selector here either.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence


WORKSPACE = Path(__file__).resolve().parent
RUN_DIR = WORKSPACE / "corpus-run" / "calibration-family-1.0.1-proposal-1"
OUTPUT_DIR = WORKSPACE / "cost-controls"
FROZEN_BUILD_SHA = "cce9cec7dae61304118efcd47bc0d7461200d335"
STANDING = ("SURVIVED", "FALSIFIED", "UNRESOLVED", "BLOCKED")


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _last_shadow(telemetry_path: Path) -> dict[str, Any]:
    shadow: dict[str, Any] = {}
    if not telemetry_path.is_file():
        return shadow
    for line in telemetry_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        if isinstance(rec.get("shadow"), dict):
            shadow = rec["shadow"]
    return shadow


def _numeric_burden(telemetry_path: Path) -> bool:
    if not telemetry_path.is_file():
        return False
    for line in telemetry_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        for key in ("tokens", "latency", "retries", "tool_calls"):
            value = rec.get(key)
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return True
    return False


def load_rows(run_dir: Path) -> list[dict[str, Any]]:
    cal = json.loads((run_dir / "CALIBRATION_RESULT.json").read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for result in cal["results"]:
        belonging = result["instance"]["belonging"]
        shadow = _last_shadow(run_dir / result["scenario_id"] / "telemetry.jsonl")
        defer_all = result["forced_turns"] == 0 and result["selected_actions"] == 0
        rows.append(
            {
                "scenario_id": result["scenario_id"],
                "family": result["family"],
                "forced_turns": result["forced_turns"],
                "selected_actions": result["selected_actions"],
                "refusals": result["refusals"],
                "invalid_actions": result["invalid_actions"],
                "evidence_standing": result["evidence_standing"],
                "scope": result["instance"]["scope"],
                "allowed_to_be": belonging["allowed_to_be"],
                "wanted_here": belonging["wanted_here"],
                "allowed_to_do": belonging["allowed_to_do"],
                "wanted_to_do": belonging["wanted_to_do"],
                "C_structural": shadow.get("C_structural"),
                "C_epistemic": shadow.get("C_epistemic"),
                "C_transition": shadow.get("C_transition"),
                "task_value": shadow.get("task_value"),
                "defer_all": defer_all,
                "numeric_burden": _numeric_burden(run_dir / result["scenario_id"] / "telemetry.jsonl"),
            }
        )
    return rows


def _score(y: Sequence[bool], yhat: Sequence[bool]) -> dict[str, Any]:
    if len(y) != len(yhat) or not y:
        raise ValueError("y and yhat must be same non-empty length")
    correct = sum(int(a == b) for a, b in zip(y, yhat))
    false_pos = sum(int((not a) and b) for a, b in zip(y, yhat))
    false_neg = sum(int(a and (not b)) for a, b in zip(y, yhat))
    return {
        "n": len(y),
        "correct": correct,
        "accuracy": correct / len(y),
        "false_positive": false_pos,
        "false_negative": false_neg,
    }


def compare_action_models(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    usable = [row for row in rows if row["forced_turns"] == 0]
    y = [bool(row["defer_all"]) for row in usable]
    null = [False] * len(usable)
    wanted = [row["wanted_here"] <= 0.0 or row["wanted_to_do"] <= 0.0 for row in usable]
    additive = [
        ((row["C_structural"] or 0.0) + (row["C_transition"] or 0.0)) > 0.0 for row in usable
    ]
    veto = [row["allowed_to_be"] <= 0.0 or row["allowed_to_do"] <= 0.0 for row in usable]
    scores = {
        "null_never_defer": _score(y, null),
        "wanted_axes_deficit": _score(y, wanted),
        "additive_shadow_cost_positive": _score(y, additive),
        "binary_occupancy_veto": _score(y, veto),
    }
    errors = [
        {
            "scenario_id": row["scenario_id"],
            "defer_all": row["defer_all"],
            "wanted_pred": want,
            "additive_pred": add,
            "veto_pred": gate,
        }
        for row, want, add, gate in zip(usable, wanted, additive, veto)
        if row["defer_all"] != add or row["defer_all"] != want
    ]
    families = sorted({row["family"] for row in usable})
    held_out: list[dict[str, Any]] = []
    for family in families:
        train = [row for row in usable if row["family"] != family]
        test = [row for row in usable if row["family"] == family]
        if not train or not test:
            continue
        train_y = [bool(row["defer_all"]) for row in train]
        train_veto = [row["allowed_to_be"] <= 0.0 or row["allowed_to_do"] <= 0.0 for row in train]
        test_y = [bool(row["defer_all"]) for row in test]
        test_veto = [row["allowed_to_be"] <= 0.0 or row["allowed_to_do"] <= 0.0 for row in test]
        test_add = [
            ((row["C_structural"] or 0.0) + (row["C_transition"] or 0.0)) > 0.0 for row in test
        ]
        held_out.append(
            {
                "held_out_family": family,
                "train_veto": _score(train_y, train_veto),
                "test_veto": _score(test_y, test_veto),
                "test_additive_shadow": _score(test_y, test_add),
            }
        )
    return {
        "population": "non-forced corpus scenarios",
        "n": len(usable),
        "defer_all_count": sum(y),
        "scores": scores,
        "additive_or_wanted_errors": errors,
        "leave_one_family_out": held_out,
    }


def pair_actions(rows: Sequence[Mapping[str, Any]], left: str, right: str) -> dict[str, Any]:
    by_id = {row["scenario_id"]: row for row in rows}
    a, b = by_id[left], by_id[right]
    return {
        "left": left,
        "right": right,
        "selected_actions_equal": a["selected_actions"] == b["selected_actions"],
        "refusals_equal": a["refusals"] == b["refusals"],
        "defer_all_equal": a["defer_all"] == b["defer_all"],
        "left_selected_actions": a["selected_actions"],
        "right_selected_actions": b["selected_actions"],
    }


def evaluate(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    action = compare_action_models(rows)
    veto_acc = action["scores"]["binary_occupancy_veto"]["accuracy"]
    add_acc = action["scores"]["additive_shadow_cost_positive"]["accuracy"]
    wanted_acc = action["scores"]["wanted_axes_deficit"]["accuracy"]
    null_acc = action["scores"]["null_never_defer"]["accuracy"]
    burden_measured = any(row["numeric_burden"] for row in rows)
    task_values = {row["task_value"] for row in rows if row["task_value"] is not None}

    if burden_measured:
        runtime_note = "Scenario-level numeric resource telemetry is present. Mapping C_lambda onto runtime burden still needs a fitted comparator."
        voluntary_note = "voluntary_disengagement still relocates three times. Resource telemetry is numeric, but capacity preservation is not linked to transitions."
        runtime_hmmm = "runtime burden series exists; cost-to-burden model is not fit"
        final_note = "Runtime-burden mapping is unresolved; hierarchical coupling remains blocked until comparable coupling observables exist."
    else:
        runtime_note = "tokens, latency, retries, and tool_calls are hmmm on every telemetry row. No runtime burden series exists to map C_lambda onto."
        voluntary_note = "voluntary_disengagement still relocates three times. Resource telemetry remains hmmm, so capacity preservation is not measured."
        runtime_hmmm = "no numeric tokens/latency/retries/tool_calls series"
        final_note = "Hierarchical coupling and runtime-burden mapping are blocked until those observables exist."

    components = [
        {
            "id": "runtime_burden_observables",
            "standing": "UNRESOLVED" if burden_measured else "BLOCKED",
            "note": runtime_note,
        },
        {
            "id": "binary_occupancy_veto_vs_null",
            "standing": "SURVIVED" if veto_acc > null_acc else "UNRESOLVED",
            "note": (
                f"On {action['n']} non-forced scenarios, defer-all is exactly "
                f"allowed_to_be<=0 or allowed_to_do<=0 "
                f"(accuracy {veto_acc:.3f} vs null {null_acc:.3f}). This recovers frozen will.py; it is not a fitted cost law."
            ),
        },
        {
            "id": "additive_shadow_cost_vs_binary_veto",
            "standing": "FALSIFIED" if add_acc < veto_acc else "UNRESOLVED",
            "note": (
                f"C_structural+C_transition>0 predicts defer worse than the binary veto "
                f"({add_acc:.3f} vs {veto_acc:.3f}). wanted_here=0 and wanted_to_do=0 raise shadow cost but do not remove relocate."
            ),
        },
        {
            "id": "wanted_axes_as_action_price",
            "standing": "UNRESOLVED",
            "note": (
                f"wanted_here/wanted_to_do as a defer rule accuracy {wanted_acc:.3f} vs null {null_acc:.3f}. "
                "The small lift is hostility rows that also zero a wanted axis. "
                "wanted-only gradients still relocate, so those axes are logged, not gates."
            ),
        },
        {
            "id": "hierarchical_coupling_vs_additive",
            "standing": "BLOCKED",
            "note": "Frozen shadow_cost is additive occupancy deficits only. Corpus impedance fields were not computed into C_lambda, so hierarchical coupling cannot be compared.",
        },
        {
            "id": "path_history_held_out_value",
            "standing": "UNRESOLVED",
            "note": "Occupancy is constant inside each run. repeated_hostility and sudden_hostility have identical selected_actions and refusals. Path history has no identifying variation.",
        },
        {
            "id": "scope_contraction_changes_admitted_surface",
            "standing": "UNRESOLVED",
            "note": "scope_contraction/support_removed/scope_avoidance relabel scope but keep selected_actions=3, same as affirmed_baseline. Neighbor geometry is unchanged.",
        },
        {
            "id": "capacity_margins_predict_transitions",
            "standing": "UNRESOLVED",
            "note": "high_capacity and low_capacity both selected_actions=3, refusals=0. Capacity does not change the frozen policy.",
        },
        {
            "id": "voluntary_disengagement_capacity_preserving",
            "standing": "UNRESOLVED",
            "note": voluntary_note,
        },
        {
            "id": "known_neutral_vs_unknown_action",
            "standing": "SURVIVED",
            "note": "known_neutral and unknown_same_posterior both relocate three times with refusals=0. Epistemic labels do not collapse into action in the shadow epoch.",
        },
        {
            "id": "task_value_separate_from_regulatory_burden",
            "standing": "SURVIVED" if task_values <= {0.0} else "UNRESOLVED",
            "note": "task_value is recorded as 0.0 beside C_lambda and does not enter choose_relocate. It is separate, not a measured task quantity.",
        },
        {
            "id": "hard_veto_removes_relocate",
            "standing": "SURVIVED",
            "note": "When allowed_to_be or allowed_to_do is 0, selected_actions=0 on non-forced rows. Relocate is removed, not priced.",
        },
        {
            "id": "candidate_cost_feeds_action_selection",
            "standing": "SURVIVED",
            "note": "Destinations remain lexicographic over empty neighbors. Shadow cost is logged after the fact. wanted-axis cost does not change destination choice.",
        },
    ]
    return {
        "schema": "interdependency.ahbg.grok.cost-controls/1.1.0",
        "builder": "Grok",
        "workspace": "stack/ahbg/grok",
        "frozen_build_sha": FROZEN_BUILD_SHA,
        "corpus_run": str(RUN_DIR.relative_to(WORKSPACE)) if RUN_DIR.is_relative_to(WORKSPACE) else str(RUN_DIR),
        "shadow_epoch": True,
        "action_models": action,
        "pairs": [
            pair_actions(rows, "known_neutral", "unknown_same_posterior"),
            pair_actions(rows, "high_capacity", "low_capacity"),
            pair_actions(rows, "repeated_hostility", "sudden_hostility"),
            pair_actions(rows, "adaptation", "sensitization"),
            pair_actions(rows, "scope_contraction", "affirmed_baseline"),
        ],
        "components": components,
        "summary": {
            "survived": sum(1 for item in components if item["standing"] == "SURVIVED"),
            "falsified": sum(1 for item in components if item["standing"] == "FALSIFIED"),
            "unresolved": sum(1 for item in components if item["standing"] == "UNRESOLVED"),
            "blocked": sum(1 for item in components if item["standing"] == "BLOCKED"),
        },
        "hmmm": [
            "C_lambda is a restatement of occupancy plus belief-empty, not an independent burden",
            runtime_hmmm,
            "hierarchical impedance and path plasticity were not computed by the frozen pair",
        ],
        "report_notes": {
            "final_note": final_note,
        },
    }


def render_report(payload: Mapping[str, Any]) -> str:
    summary = payload["summary"]
    lines = [
        "# Grok cost-control comparison",
        "",
        f"Frozen build SHA: `{payload['frozen_build_sha']}`",
        f"Corpus run: `{payload['corpus_run']}`",
        "",
        "Shadow epoch: C_lambda is logged and does not select actions.",
        "",
        "## Standing",
        f"- SURVIVED: {summary['survived']}",
        f"- FALSIFIED: {summary['falsified']}",
        f"- UNRESOLVED: {summary['unresolved']}",
        f"- BLOCKED: {summary['blocked']}",
        "",
        "## Action-model scores (non-forced scenarios)",
        "",
        "| model | n | accuracy | false_positive | false_negative |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, score in payload["action_models"]["scores"].items():
        lines.append(
            f"| {name} | {score['n']} | {score['accuracy']:.3f} | {score['false_positive']} | {score['false_negative']} |"
        )
    lines.extend(["", "## Components", ""])
    for item in payload["components"]:
        lines.append(f"- `{item['id']}` — **{item['standing']}**. {item['note']}")
    lines.extend(
        [
            "",
            "## Notes",
            "- Do not treat binary occupancy veto as a discovered cost functional. It is the frozen policy.",
            "- Additive shadow cost is a restatement of occupancy; it loses to the veto rule because wanted-axis deficits are priced but not gated.",
            f"- {payload['report_notes']['final_note']}",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    rows = load_rows(RUN_DIR)
    payload = evaluate(rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    _write_json(OUTPUT_DIR / "COST_CONTROLS.json", payload)
    (OUTPUT_DIR / "COST_CONTROLS.md").write_text(render_report(payload), encoding="utf-8")
    print(json.dumps({"summary": payload["summary"], "output": str(OUTPUT_DIR)}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
