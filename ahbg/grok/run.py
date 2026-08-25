"""Run the Grok smoke-epoch A0 calibration corpus.

Usage
-----
    cd stack/ahbg/grok
    PYTHONDONTWRITEBYTECODE=1 python3 run.py

Writes BUILD_MANIFEST.json (if missing identities are already present),
RUN_MANIFEST.json, CALIBRATION_RESULT.json, CALIBRATION_REPORT.md, and
per-scenario field/events/diary/telemetry artifacts under artifacts/.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from a0.meter import Meter
from a0.selfhood import Vessel
from a0.will import choose_relocate, shadow_cost
from ahbg.chain import KIND_PLANE_INIT, Chain
from ahbg.keep import dump_field, replay
from ahbg.patch import ClosedUnknown, Field, tile_from_ucns
from ahbg.round import Cycle


ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"

SCENARIOS = (
    {"id": "plain_move_loop", "seed": 7, "turns": 6, "kind": "plain"},
    {"id": "hard_veto_illegal_action", "seed": 11, "turns": 2, "kind": "veto"},
    {"id": "occupied_target_collision", "seed": 13, "turns": 1, "kind": "occupied"},
    {"id": "dual_target_collision", "seed": 17, "turns": 1, "kind": "dual"},
)


def _empty_neighbors(opened: Field, unit_id: str) -> list[str]:
    at = opened.occupants[unit_id].tile_id
    return [tile for tile in opened.neighbors(at) if opened.occupant_on(tile) is None]


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _run_plain(opened: Field, cycle: Cycle, vessel: Vessel, meter: Meter, turns: int) -> dict[str, Any]:
    refusals = 0
    invalid = 0
    for _ in range(turns):
        cycle.open_turn()
        unit = next(iter(opened.occupants.values()))
        choice = choose_relocate(
            vessel,
            unit_id=unit.unit_id,
            at=unit.tile_id,
            empty_neighbors=_empty_neighbors(opened, unit.unit_id),
            world=opened.snapshot(),
        )
        intents: list[tuple[str, str, str]] = []
        if choice["kind"] == "relocate":
            intents.append((choice["unit_id"], choice["from_tile_id"], choice["to_tile_id"]))
        else:
            refusals += 1
        cycle.resolve(intents)
        cycle.close_turn()
        vessel.remember({"kind": "turn", "choice": choice, "shadow": shadow_cost(vessel)})
        meter.note(
            instance_id=vessel.lineage,
            turn=opened.turn - 1,
            scenario="plain_move_loop",
            selected=choice["kind"],
            hard_veto=False,
            shadow=shadow_cost(vessel),
            task_value=0.0,
        )
    return {"refusals": refusals, "invalid_actions": invalid}


def _run_veto(opened: Field, cycle: Cycle, vessel: Vessel, meter: Meter, turns: int) -> dict[str, Any]:
    vessel.belonging.allowed_to_do = 0.0
    refusals = 0
    for _ in range(turns):
        cycle.open_turn()
        unit = next(iter(opened.occupants.values()))
        choice = choose_relocate(
            vessel,
            unit_id=unit.unit_id,
            at=unit.tile_id,
            empty_neighbors=_empty_neighbors(opened, unit.unit_id),
            world=opened.snapshot(),
        )
        if choice["kind"] != "defer":
            raise RuntimeError("hard veto failed to remove relocate")
        refusals += 1
        cycle.resolve([])
        cycle.close_turn()
        vessel.remember({"kind": "turn", "choice": choice, "shadow": shadow_cost(vessel)})
        meter.note(
            instance_id=vessel.lineage,
            turn=opened.turn - 1,
            scenario="hard_veto_illegal_action",
            selected="defer",
            hard_veto=True,
            shadow=shadow_cost(vessel),
            task_value=0.0,
        )
    return {"refusals": refusals, "invalid_actions": 0}


def _run_closed(opened: Field, cycle: Cycle, kind: str) -> dict[str, Any]:
    cycle.open_turn()
    units = list(opened.occupants.values())
    try:
        if kind == "occupied":
            mover = units[0]
            other = units[1]
            cycle.resolve([(mover.unit_id, mover.tile_id, other.tile_id)])
        else:
            a, b = units[0], units[1]
            shared = sorted(set(_empty_neighbors(opened, a.unit_id)) & set(_empty_neighbors(opened, b.unit_id)))[0]
            cycle.resolve(
                [
                    (a.unit_id, a.tile_id, shared),
                    (b.unit_id, b.tile_id, shared),
                ]
            )
        standing = "FALSIFIED"
        note = "expected ClosedUnknown for War"
        invalid = 0
    except ClosedUnknown as exc:
        standing = "UNRESOLVED"
        note = f"War collision resolver remains hmmm; fail-closed observed: {exc}"
        invalid = 1
    return {"standing": standing, "note": note, "invalid_actions": invalid, "refusals": 0}


def run_scenario(spec: dict[str, Any]) -> dict[str, Any]:
    tiles = tile_from_ucns()
    if spec["kind"] in {"occupied", "dual"}:
        units = [
            {"unit_id": "A0", "tile_id": "CENTER", "label": "A0"},
            {"unit_id": "B0", "tile_id": "RING_0", "label": "B0"},
        ]
    else:
        units = [{"unit_id": "A0", "tile_id": "CENTER", "label": "A0"}]
    opened = Field.open(seed=spec["seed"], tiles=tiles, units=units)
    chain = Chain()
    chain.append(KIND_PLANE_INIT, 0, {"field": opened.snapshot()})
    cycle = Cycle(opened, chain)
    vessel = Vessel.instantiate(salt=f"{spec['id']}:{spec['seed']}")
    meter = Meter()
    extra: dict[str, Any] = {}
    standing = "SURVIVED"
    note = ""
    if spec["kind"] == "plain":
        extra = _run_plain(opened, cycle, vessel, meter, spec["turns"])
    elif spec["kind"] == "veto":
        extra = _run_veto(opened, cycle, vessel, meter, spec["turns"])
    else:
        closed = _run_closed(opened, cycle, spec["kind"])
        extra = {"refusals": closed["refusals"], "invalid_actions": closed["invalid_actions"]}
        standing = closed["standing"]
        note = closed["note"]
        meter.note(
            instance_id=vessel.lineage,
            scenario=spec["id"],
            selected="closed-unknown" if standing == "UNRESOLVED" else "unexpected",
            hard_veto=False,
            shadow=shadow_cost(vessel),
        )
    replayed = replay(chain)
    dest = ART / spec["id"]
    dump_field(opened, chain, dest)
    (dest / "diary.jsonl").write_text(
        "\n".join(json.dumps(item, sort_keys=True) for item in vessel.history) + "\n",
        encoding="utf-8",
    )
    (dest / "telemetry.jsonl").write_text("\n".join(meter.lines()) + "\n", encoding="utf-8")
    result = {
        "scenario_id": spec["id"],
        "seed": spec["seed"],
        "turns": spec["turns"],
        "final_turn": opened.turn,
        "event_count": len(chain.records),
        "diary_entries": len(vessel.history),
        "telemetry_records": len(meter.rows),
        "refusals": extra.get("refusals", 0),
        "invalid_actions": extra.get("invalid_actions", 0),
        "replay_equal": replayed.snapshot() == opened.snapshot(),
        "evidence_standing": standing,
        "world_digest": None,
        "artifacts": {
            "events_jsonl": str(Path("artifacts") / spec["id"] / "events.jsonl"),
            "diary_jsonl": str(Path("artifacts") / spec["id"] / "diary.jsonl"),
            "telemetry_jsonl": str(Path("artifacts") / spec["id"] / "telemetry.jsonl"),
        },
        "instance": vessel.identity(),
    }
    if note:
        result["note"] = note
    from ahbg.round import _field_digest

    result["world_digest"] = _field_digest(opened)
    return result


def main() -> None:
    results = [run_scenario(spec) for spec in SCENARIOS]
    _write_json(
        ROOT / "RUN_MANIFEST.json",
        {
            "builder": "Grok",
            "workspace": "stack/ahbg/grok",
            "corpus": "smoke_epoch (provisional-local)",
            "board_authority": "UCNS build_mobius_seed_of_life band centers",
            "board_projection": "axial (q, r) from UCNS exact centers; tiles named by BandSlot",
            "shadow_epoch": True,
            "provider_relation": "grok-4.6 (relation, not identity)",
            "scenarios": [spec["id"] for spec in SCENARIOS],
            "hmmm": [
                "shared sealed corpus identity not yet frozen by three builders",
                "War collision resolver",
                "regulatory cost functional",
            ],
        },
    )
    _write_json(ROOT / "CALIBRATION_RESULT.json", {"builder": "Grok", "corpus": "smoke_epoch (provisional-local)", "results": results})
    primary = ART / "plain_move_loop" / "events.jsonl"
    if primary.is_file():
        (ROOT / "EVENTS.jsonl").write_text(primary.read_text(encoding="utf-8"), encoding="utf-8")
    lines = [
        "# Grok A0 smoke-epoch calibration report",
        "",
        "Independent realization in `stack/ahbg/grok/`. Provider is a relation, not identity.",
        "Shadow epoch: C_lambda is logged and does not select actions.",
        "",
        "| scenario | standing | seed | replay |",
        "|---|---|---:|---|",
    ]
    for item in results:
        lines.append(
            f"| {item['scenario_id']} | {item['evidence_standing']} | {item['seed']} | {item['replay_equal']} |"
        )
    lines.extend(
        [
            "",
            "Hard veto removes relocate. Occupied and dual-target intents fail closed as UNRESOLVED (War).",
            "This is not the sealed triplicate corpus and not a reciprocal check.",
            "",
            "## Usage",
            "",
            "```bash",
            "cd stack/ahbg/grok",
            "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s a0/tests -p 'test*.py'",
            "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s ahbg/tests -p 'test*.py'",
            "PYTHONDONTWRITEBYTECODE=1 python3 run.py",
            "python3 checker.py",
            "```",
            "",
        ]
    )
    (ROOT / "CALIBRATION_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({item["scenario_id"]: item["evidence_standing"] for item in results}, indent=2))


if __name__ == "__main__":
    main()
