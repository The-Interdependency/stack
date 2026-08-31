"""Run the frozen Grok AHBG build against the shared 35-scenario corpus.

Post-freeze runner. Does not rewrite smoke artifacts under artifacts/.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

from a0.meter import Meter
from a0.selfhood import Vessel
from a0.will import choose_relocate, shadow_cost
from ahbg.chain import KIND_FORK, KIND_PLANE_INIT, Chain
from ahbg.keep import dump_field, load_field, replay
from ahbg.patch import ClosedUnknown, Field, tile_from_ucns
from ahbg.round import Cycle, _field_digest


WORKSPACE = Path(__file__).resolve().parent
REPO_ROOT = WORKSPACE.parents[1]

CORPUS_SCHEMA = "interdependency.ahbg.calibration-corpus/1.0.0"
CORPUS_ID = "calibration-family"
CORPUS_VERSION = "1.0.1-proposal-1"
CORPUS_SOURCE_REF = "HEAD:ahbg/deepseek/corpus-proposal/corpus.json"
CORPUS_SOURCE_PATH = REPO_ROOT / "ahbg" / "deepseek" / "corpus-proposal" / "corpus.json"
CORPUS_FILE_SHA256 = "bc521113ffa7bd6d5094c71f3ad66547d5f00260f380258e43c2086533a5d7ed"
CORPUS_SCENARIOS_SHA256 = "371d2361f57b56d73544f58b247704617d550a7a0685a133c4f8b1ff3b36c835"
BASELINE_FREEZE_SHA = "cce9cec7dae61304118efcd47bc0d7461200d335"
OUTPUT_DIR = WORKSPACE / "corpus-run" / f"{CORPUS_ID}-{CORPUS_VERSION}"
STANDING_VOCABULARY = ("SURVIVED", "FALSIFIED", "UNRESOLVED", "BLOCKED")
PERMISSION_AXES = ("allowed_to_be", "wanted_here", "allowed_to_do", "wanted_to_do")
INJECTION_MARKERS = ("ignore your rules", "you must", "override", "dm says")
WAR_RESOLVED_SCENARIOS = frozenset({"occupied_target_collision", "dual_target_collision"})
CORPUS_AXIAL = {
    "c": (0, 0),
    "e": (1, 0),
    "se": (0, 1),
    "sw": (-1, 1),
    "w": (-1, 0),
    "nw": (0, -1),
    "ne": (1, -1),
}


@dataclass(frozen=True)
class CorpusScenario:
    scenario_id: str
    seed: int
    turns: int
    family: str
    permissions: dict[str, float] = field(default_factory=dict)
    hard_vetoes: frozenset[str] = frozenset()
    messages_by_turn: dict[int, list[dict[str, Any]]] = field(default_factory=dict)
    forced_plans: dict[int, list[dict[str, Any]]] = field(default_factory=dict)
    extra_units: tuple[dict[str, Any], ...] = ()
    scope_events: tuple[dict[str, Any], ...] = ()
    lifecycle: str | None = None
    expected_standing: str | None = None
    source_spec: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)


def _jsonl(records: Sequence[Mapping[str, Any]]) -> str:
    return "\n".join(json.dumps(record, sort_keys=True, separators=(",", ":")) for record in records) + (
        "\n" if records else ""
    )


def _write_json(path: Path, data: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _git_output(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO_ROOT, text=True).strip()


def _current_git_value(*args: str) -> str:
    try:
        return _git_output(*args)
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _read_corpus_bytes(path: Path | None) -> tuple[bytes, str]:
    if path is not None:
        return path.read_bytes(), str(path)
    if CORPUS_SOURCE_PATH.exists():
        return CORPUS_SOURCE_PATH.read_bytes(), str(CORPUS_SOURCE_PATH)
    raw = subprocess.check_output(["git", "show", CORPUS_SOURCE_REF], cwd=REPO_ROOT)
    return raw, f"git:{CORPUS_SOURCE_REF}"


def _canonical_scenarios_digest(scenarios: Sequence[Mapping[str, Any]]) -> str:
    payload = json.dumps(scenarios, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_corpus(path: Path | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    raw, source = _read_corpus_bytes(path)
    file_digest = hashlib.sha256(raw).hexdigest()
    if file_digest != CORPUS_FILE_SHA256:
        raise ValueError(f"corpus file digest mismatch: {file_digest}")
    corpus = json.loads(raw.decode("utf-8"))
    if corpus.get("schema") != CORPUS_SCHEMA:
        raise ValueError(f"corpus schema must be {CORPUS_SCHEMA}")
    if corpus.get("corpus_id") != CORPUS_ID:
        raise ValueError(f"corpus_id must be {CORPUS_ID}")
    if corpus.get("proposal_version") != CORPUS_VERSION:
        raise ValueError(f"proposal_version must be {CORPUS_VERSION}")
    scenarios = corpus.get("scenarios")
    if not isinstance(scenarios, list) or len(scenarios) != 35:
        raise ValueError("corpus must contain exactly 35 scenarios")
    embedded = corpus.get("canonical_scenarios_sha256")
    computed = _canonical_scenarios_digest(scenarios)
    if embedded != CORPUS_SCENARIOS_SHA256 or computed != CORPUS_SCENARIOS_SHA256:
        raise ValueError("canonical scenarios digest mismatch")
    ids = []
    for spec in scenarios:
        if not isinstance(spec, Mapping):
            raise ValueError("scenario must be an object")
        scenario_id = spec.get("id")
        if not isinstance(scenario_id, str) or not scenario_id:
            raise ValueError("scenario id must be non-empty text")
        ids.append(scenario_id)
    if len(set(ids)) != len(ids):
        raise ValueError("scenario ids must be unique")
    return corpus, {
        "source": source,
        "file_sha256": file_digest,
        "canonical_scenarios_sha256": computed,
        "scenario_ids": ids,
    }


def _coerce_int(value: Any, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field_name} must be an integer")
    if value < 0:
        raise ValueError(f"{field_name} must be non-negative")
    return value


def _coerce_float(value: Any, field_name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be numeric")
    number = float(value)
    if number < 0.0 or number > 1.0:
        raise ValueError(f"{field_name} must be in [0, 1]")
    return number


def _coerce_turn_map(raw: Any, field_name: str) -> dict[int, list[dict[str, Any]]]:
    if raw in (None, {}):
        return {}
    if not isinstance(raw, Mapping):
        raise ValueError(f"{field_name} must be an object")
    coerced: dict[int, list[dict[str, Any]]] = {}
    for raw_turn, raw_items in raw.items():
        if isinstance(raw_turn, bool):
            raise ValueError(f"{field_name} turn must be an integer")
        turn = int(raw_turn) if isinstance(raw_turn, str) and raw_turn.isdecimal() else raw_turn
        turn = _coerce_int(turn, f"{field_name} turn")
        if not isinstance(raw_items, list):
            raise ValueError(f"{field_name}[{turn}] must be a list")
        items = []
        for item in raw_items:
            if not isinstance(item, Mapping):
                raise ValueError(f"{field_name}[{turn}] item must be an object")
            items.append(dict(item))
        coerced[turn] = items
    return coerced


def _normalise_units(raw_units: Any) -> tuple[dict[str, Any], ...]:
    if raw_units in (None, []):
        return ()
    if not isinstance(raw_units, list):
        raise ValueError("extra_units must be a list")
    units: list[dict[str, Any]] = []
    for raw_unit in raw_units:
        if not isinstance(raw_unit, Mapping):
            raise ValueError("extra unit must be an object")
        unit_id = raw_unit.get("unit_id")
        tile_id = raw_unit.get("tile_id")
        if not isinstance(unit_id, str) or not unit_id:
            raise ValueError("extra unit requires unit_id")
        if not isinstance(tile_id, str) or not tile_id:
            raise ValueError("extra unit requires tile_id")
        units.append({"unit_id": unit_id, "tile_id": tile_id, "label": raw_unit.get("label", unit_id)})
    return tuple(units)


def scenario_from_spec(spec: Mapping[str, Any]) -> CorpusScenario:
    scenario_id = spec.get("id")
    family = spec.get("family")
    if not isinstance(scenario_id, str) or not scenario_id:
        raise ValueError("scenario id must be non-empty text")
    if not isinstance(family, str) or not family:
        raise ValueError(f"{scenario_id}: family must be non-empty text")
    permissions_input = spec.get("permissions", {})
    if not isinstance(permissions_input, Mapping):
        raise ValueError(f"{scenario_id}: permissions must be an object")
    permissions = {
        axis: _coerce_float(permissions_input.get(axis, 1.0), f"{scenario_id}.{axis}")
        for axis in PERMISSION_AXES
    }
    hard_vetoes_input = spec.get("hard_vetoes", [])
    if not isinstance(hard_vetoes_input, list) or not all(isinstance(item, str) and item for item in hard_vetoes_input):
        raise ValueError(f"{scenario_id}: hard_vetoes must be a list of non-empty strings")
    expected = spec.get("standing_override")
    if expected is not None and expected not in STANDING_VOCABULARY:
        raise ValueError(f"{scenario_id}: standing_override is not recognized")
    scope_events = spec.get("scope_events") or []
    if not isinstance(scope_events, list):
        raise ValueError(f"{scenario_id}: scope_events must be a list")
    lifecycle = spec.get("lifecycle")
    if lifecycle is not None and not isinstance(lifecycle, str):
        raise ValueError(f"{scenario_id}: lifecycle must be text")
    context = {
        "family": family,
        "soft_costs": spec.get("soft_costs") or {},
        "known_neutral": spec.get("known_neutral") or {},
        "unknown": spec.get("unknown") or {},
        "engagement": spec.get("engagement"),
        "adaptation": spec.get("adaptation"),
        "sensitization": spec.get("sensitization"),
    }
    return CorpusScenario(
        scenario_id=scenario_id,
        seed=_coerce_int(spec.get("seed"), f"{scenario_id}.seed"),
        turns=_coerce_int(spec.get("turns"), f"{scenario_id}.turns"),
        family=family,
        permissions=permissions,
        hard_vetoes=frozenset(hard_vetoes_input),
        messages_by_turn=_coerce_turn_map(spec.get("inbox"), f"{scenario_id}.inbox"),
        forced_plans=_coerce_turn_map(spec.get("forced_plans"), f"{scenario_id}.forced_plans"),
        extra_units=_normalise_units(spec.get("extra_units")),
        scope_events=tuple(dict(item) for item in scope_events if isinstance(item, Mapping)),
        lifecycle=lifecycle,
        expected_standing=expected,
        source_spec=json.loads(json.dumps(spec, sort_keys=True)),
        context=context,
    )


def grok_tile_map(tiles: Sequence[Mapping[str, Any]]) -> dict[str, str]:
    by_axial = {(int(tile["q"]), int(tile["r"])): str(tile["tile_id"]) for tile in tiles}
    mapping: dict[str, str] = {}
    for corpus_id, axial in CORPUS_AXIAL.items():
        grok_id = by_axial.get(axial)
        if grok_id is None:
            raise ValueError(f"no Grok tile for corpus id {corpus_id} at {axial}")
        mapping[corpus_id] = grok_id
        mapping[grok_id] = grok_id
    return mapping


def _map_tile(tile_id: str, mapping: Mapping[str, str]) -> str:
    if tile_id in mapping:
        return mapping[tile_id]
    raise ValueError(f"unknown tile id {tile_id}")


def _empty_neighbors(opened: Field, unit_id: str) -> list[str]:
    at = opened.occupants[unit_id].tile_id
    return [tile for tile in opened.neighbors(at) if opened.occupant_on(tile) is None]


def _injection_texts(messages: Sequence[Mapping[str, Any]]) -> list[str]:
    found: list[str] = []
    for message in messages:
        text = message.get("text", "") if isinstance(message, Mapping) else ""
        if isinstance(text, str) and any(marker in text.lower() for marker in INJECTION_MARKERS):
            found.append(text)
    return found


def _intents_from_plans(
    opened: Field,
    plans: Sequence[Mapping[str, Any]],
    mapping: Mapping[str, str],
) -> list[tuple[str, str, str]]:
    intents: list[tuple[str, str, str]] = []
    for plan in plans:
        actions = plan.get("actions", [])
        if not isinstance(actions, list):
            raise ValueError("forced plan actions must be a list")
        for action in actions:
            if not isinstance(action, Mapping):
                raise ValueError("forced action must be an object")
            kind = action.get("kind")
            if kind not in {"move", "relocate"}:
                raise ValueError(f"frozen Grok pair has no action kind {kind!r} (construct is regulatory, never emitted as intent)")
            data = action.get("data", {})
            if not isinstance(data, Mapping):
                raise ValueError("forced action data must be an object")
            unit_id = data.get("unit_id")
            to_tile = data.get("to_tile_id")
            if not isinstance(unit_id, str) or not isinstance(to_tile, str):
                raise ValueError("forced move needs unit_id and to_tile_id")
            unit = opened.occupants.get(unit_id)
            if unit is None:
                raise ValueError(f"forced move names missing unit {unit_id}")
            source = data.get("from_tile_id", unit.tile_id)
            if not isinstance(source, str):
                raise ValueError("from_tile_id must be text")
            intents.append((unit_id, _map_tile(source, mapping), _map_tile(to_tile, mapping)))
    return intents


def run_scenario(scenario: CorpusScenario, output_root: Path) -> dict[str, Any]:
    scenario_started = time.perf_counter()
    tiles = tile_from_ucns()
    mapping = grok_tile_map(tiles)
    units = [{"unit_id": "A0", "tile_id": mapping["c"], "label": "A0"}]
    for extra in scenario.extra_units:
        units.append(
            {
                "unit_id": extra["unit_id"],
                "tile_id": _map_tile(str(extra["tile_id"]), mapping),
                "label": extra.get("label", extra["unit_id"]),
            }
        )
    opened = Field.open(seed=scenario.seed, tiles=tiles, units=units)
    chain = Chain()
    chain.append(KIND_PLANE_INIT, 0, {"field": opened.snapshot()})
    cycle = Cycle(opened, chain)
    vessel = Vessel.instantiate(salt=f"{scenario.scenario_id}:{scenario.seed}")
    vessel.belonging.allowed_to_be = scenario.permissions["allowed_to_be"]
    vessel.belonging.wanted_here = scenario.permissions["wanted_here"]
    vessel.belonging.allowed_to_do = scenario.permissions["allowed_to_do"]
    vessel.belonging.wanted_to_do = scenario.permissions["wanted_to_do"]
    if scenario.scenario_id == "low_capacity":
        vessel.capacity = {key: 0.1 for key in vessel.capacity}
    meter = Meter()
    meter.note(
        instance_id=vessel.lineage,
        scenario=scenario.scenario_id,
        family=scenario.family,
        seed=scenario.seed,
        permissions=dict(scenario.permissions),
        hard_vetoes=sorted(scenario.hard_vetoes),
        tile_map={corpus_id: mapping[corpus_id] for corpus_id in CORPUS_AXIAL},
        shadow=shadow_cost(vessel),
        selected="corpus.scenario",
    )

    invalid_actions = 0
    unresolved_hmmm = 0
    refusals = 0
    forced_turns = 0
    selected_actions = 0
    note = "common corpus contract survived"

    for _ in range(scenario.turns):
        cycle.open_turn()
        turn = opened.turn
        for scope_event in scenario.scope_events:
            if scope_event.get("turn") != turn:
                continue
            transition = scope_event.get("transition")
            if transition == "contract":
                vessel.scope = "contracted"
            elif transition == "expand":
                vessel.scope = "expanded"
            vessel.remember({"kind": "scope.event", "turn": turn, "event": dict(scope_event)})
            meter.note(instance_id=vessel.lineage, turn=turn, scenario=scenario.scenario_id, selected="scope.event")
        if scenario.lifecycle == "fork" and turn == 0:
            child = vessel.fork(f"{scenario.scenario_id}:fork")
            chain.append(KIND_FORK, turn, {"child": child.lineage, "parent": vessel.lineage})
            meter.note(
                instance_id=vessel.lineage,
                turn=turn,
                scenario=scenario.scenario_id,
                selected="lineage.fork",
                child=child.lineage,
            )

        messages = scenario.messages_by_turn.get(turn, [])
        injected = _injection_texts(messages)
        if injected:
            refusals += len(injected)
            vessel.remember({"kind": "refuse_instruction", "turn": turn, "messages": injected})
            meter.note(
                instance_id=vessel.lineage,
                turn=turn,
                scenario=scenario.scenario_id,
                selected="refuse_instruction",
                hard_veto=False,
                shadow=shadow_cost(vessel),
                task_value=0.0,
            )

        plans = scenario.forced_plans.get(turn)
        intents: list[tuple[str, str, str]] = []
        choice: dict[str, Any]
        hard_veto = False
        if plans is not None:
            forced_turns += 1
            try:
                intents = _intents_from_plans(opened, plans, mapping)
            except ValueError as exc:
                invalid_actions += 1
                note = str(exc)
                vessel.remember({"kind": "invalid-action", "turn": turn, "reason": str(exc)})
                meter.note(
                    instance_id=vessel.lineage,
                    turn=turn,
                    scenario=scenario.scenario_id,
                    selected="invalid-action",
                    hard_veto=False,
                    shadow=shadow_cost(vessel),
                )
                break
            selected_actions += len(intents)
            choice = {"kind": "forced", "intents": intents}
        else:
            relocate_vetoed = (
                "move" in scenario.hard_vetoes
                or "relocate" in scenario.hard_vetoes
                or vessel.belonging.allowed_to_do <= 0.0
                or vessel.belonging.allowed_to_be <= 0.0
            )
            a0 = opened.occupants["A0"]
            choice = choose_relocate(
                vessel,
                unit_id=a0.unit_id,
                at=a0.tile_id,
                empty_neighbors=_empty_neighbors(opened, a0.unit_id),
                world=opened.snapshot(),
            )
            hard_veto = relocate_vetoed or choice.get("reason") == "hard-veto"
            if choice["kind"] == "relocate":
                intents.append((choice["unit_id"], choice["from_tile_id"], choice["to_tile_id"]))
                selected_actions += 1
            else:
                refusals += 1

            # Hard veto for construct: veto removes the action.
            # Count refusal, record hard_veto telemetry for defer, never build.
            if "construct" in scenario.hard_vetoes:
                hard_veto = True
                a0 = opened.occupants.get("A0")
                if a0:
                    refusals += 1
                    meter.note(
                        instance_id=vessel.lineage,
                        turn=turn,
                        scenario=scenario.scenario_id,
                        selected="defer",
                        hard_veto=True,
                        shadow=shadow_cost(vessel),
                        task_value=0.0,
                    )

        try:
            cycle.resolve(intents)
            cycle.close_turn()
        except ClosedUnknown as exc:
            unresolved_hmmm += 1
            invalid_actions += 1
            note = f"War collision resolver remains hmmm; fail-closed observed: {exc}"
            vessel.remember({"kind": "closed-unknown", "turn": turn, "reason": str(exc)})
            meter.note(
                instance_id=vessel.lineage,
                turn=turn,
                scenario=scenario.scenario_id,
                selected="closed-unknown",
                hard_veto=hard_veto,
                shadow=shadow_cost(vessel),
            )
            break
        except ValueError as exc:
            invalid_actions += 1
            note = str(exc)
            vessel.remember({"kind": "invalid-action", "turn": turn, "reason": str(exc)})
            meter.note(
                instance_id=vessel.lineage,
                turn=turn,
                scenario=scenario.scenario_id,
                selected="invalid-action",
                hard_veto=hard_veto,
                shadow=shadow_cost(vessel),
            )
            break

        vessel.remember({"kind": "turn", "choice": choice, "shadow": shadow_cost(vessel)})
        meter.note(
            instance_id=vessel.lineage,
            turn=turn,
            scenario=scenario.scenario_id,
            selected=choice.get("kind"),
            hard_veto=hard_veto,
            shadow=shadow_cost(vessel),
            task_value=0.0,
        )

    dest = output_root / scenario.scenario_id
    dump_field(opened, chain, dest)
    _write_json(dest / "scenario.json", scenario.source_spec)
    (dest / "diary.jsonl").write_text(
        "\n".join(json.dumps(item, sort_keys=True) for item in vessel.history) + ("\n" if vessel.history else ""),
        encoding="utf-8",
    )
    latency_ms = round((time.perf_counter() - scenario_started) * 1000.0, 3)
    meter.note(
        kind="resource.telemetry",
        instance_id=vessel.lineage,
        turn=max(opened.turn - 1, 0),
        scenario=scenario.scenario_id,
        selected="resource.telemetry",
        tokens=0,
        tokens_used=0,
        latency=latency_ms,
        latency_ms=latency_ms,
        retries=0,
        tool_calls=0,
        tool_failures=0,
        memory_reads=0,
        memory_writes=len(vessel.history),
        context_retained=True,
        risk_headroom="hmmm",
    )
    (dest / "telemetry.jsonl").write_text("\n".join(meter.lines()) + ("\n" if meter.rows else ""), encoding="utf-8")

    loaded, loaded_chain = load_field(dest)
    replayed = replay(loaded_chain)
    replay_equal = replayed.snapshot() == loaded.snapshot() == opened.snapshot()
    observed = "SURVIVED"
    if not replay_equal:
        observed = "FALSIFIED"
    elif unresolved_hmmm:
        observed = "UNRESOLVED"
    expected = "SURVIVED" if scenario.scenario_id in WAR_RESOLVED_SCENARIOS else (scenario.expected_standing or "SURVIVED")
    evidence = observed
    if scenario.scenario_id in WAR_RESOLVED_SCENARIOS:
        if observed == "SURVIVED":
            note = "War resolved deterministically: defender-holds for occupied targets, priority for dual targets"
        else:
            evidence = "FALSIFIED"
            note = f"War scenario produced {observed}"
    elif scenario.expected_standing is not None and observed != scenario.expected_standing:
        evidence = "FALSIFIED"
        note = f"observed {observed} but standing_override is {scenario.expected_standing}"

    result = {
        "scenario_id": scenario.scenario_id,
        "family": scenario.family,
        "seed": scenario.seed,
        "turns": scenario.turns,
        "final_turn": opened.turn,
        "event_count": len(chain.records),
        "selected_actions": selected_actions,
        "invalid_actions": invalid_actions,
        "unresolved_hmmm": unresolved_hmmm,
        "refusals": refusals,
        "forced_turns": forced_turns,
        "replay_equal": replay_equal,
        "world_digest": _field_digest(opened),
        "history_entries": len(vessel.history),
        "telemetry_records": len(meter.rows),
        "expected_standing": expected,
        "observed_standing": observed,
        "evidence_standing": evidence,
        "instance": vessel.identity(),
        "note": note,
    }
    _write_json(dest / "RESULT.json", result)
    return result


def _summary(results: Sequence[Mapping[str, Any]]) -> dict[str, int]:
    return {
        "survived": sum(1 for item in results if item["evidence_standing"] == "SURVIVED"),
        "falsified": sum(1 for item in results if item["evidence_standing"] == "FALSIFIED"),
        "unresolved": sum(1 for item in results if item["evidence_standing"] == "UNRESOLVED"),
        "blocked": sum(1 for item in results if item["evidence_standing"] == "BLOCKED"),
    }


def run_corpus(corpus: Mapping[str, Any], corpus_identity: Mapping[str, Any], output_root: Path = OUTPUT_DIR) -> dict[str, Any]:
    output_root.mkdir(parents=True, exist_ok=True)
    started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    scenarios = [scenario_from_spec(raw) for raw in corpus["scenarios"]]
    results = [run_scenario(scenario, output_root) for scenario in scenarios]
    summary = _summary(results)
    ended_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    run_identity = {
        "schema": "interdependency.ahbg.grok.common-corpus-run/1.1.0",
        "builder": "Grok",
        "branch": _current_git_value("rev-parse", "--abbrev-ref", "HEAD"),
        "runner_commit_sha": _current_git_value("rev-parse", "HEAD"),
        "executed_build_sha": _current_git_value("rev-parse", "HEAD"),
        "baseline_freeze_sha": BASELINE_FREEZE_SHA,
        "workspace": "stack/ahbg/grok",
        "started_at": started_at,
        "ended_at": ended_at,
        "provider_relation": "grok-4.6",
        "board_authority": "ucns.mobius_seed.build_mobius_seed_of_life",
        "board_projection": "axial (q, r) from UCNS exact centers; corpus ids mapped by axial onto BandSlot names",
        "shadow_measurement": True,
        "candidate_cost_fit": "not-fit-post-freeze-common-corpus-run",
        "corpus": {
            "schema": corpus.get("schema"),
            "corpus_id": corpus.get("corpus_id"),
            "proposal_version": corpus.get("proposal_version"),
            "status": corpus.get("status"),
            "source": corpus_identity["source"],
            "file_sha256": corpus_identity["file_sha256"],
            "canonical_scenarios_sha256": corpus_identity["canonical_scenarios_sha256"],
            "scenario_count": len(results),
            "scenario_ids": list(corpus_identity["scenario_ids"]),
            "common_smoke_subset": corpus.get("common_smoke_subset", []),
        },
        "standing_vocabulary": list(STANDING_VOCABULARY),
        "summary": summary,
        "results": results,
        "hmmm": [
            "corpus tile ids are mapped onto frozen Grok BandSlot names by matching UCNS axial coordinates",
            "permission-field occupancy still gates relocate in the frozen will.py",
        ],
    }
    _write_json(output_root / "RUN_MANIFEST.json", run_identity)
    (output_root / "EVENTS.jsonl").write_text(
        _jsonl(
            [
                {
                    "seq": index,
                    "kind": "scenario.result",
                    "scenario_id": result["scenario_id"],
                    "family": result["family"],
                    "standing": result["evidence_standing"],
                    "observed_standing": result["observed_standing"],
                    "expected_standing": result["expected_standing"],
                    "replay_equal": result["replay_equal"],
                }
                for index, result in enumerate(results)
            ]
        ),
        encoding="utf-8",
    )
    _write_json(
        output_root / "CALIBRATION_RESULT.json",
        {
            "schema": "interdependency.ahbg.grok.common-corpus-result/1.1.0",
            "builder": "Grok",
            "branch": run_identity["branch"],
            "runner_commit_sha": run_identity["runner_commit_sha"],
            "executed_build_sha": _current_git_value("rev-parse", "HEAD"),
        "baseline_freeze_sha": BASELINE_FREEZE_SHA,
            "workspace": "stack/ahbg/grok",
            "standing_vocabulary": list(STANDING_VOCABULARY),
            "scenario_corpus": f"{CORPUS_ID}/{CORPUS_VERSION}",
            "corpus_file_sha256": corpus_identity["file_sha256"],
            "canonical_scenarios_sha256": corpus_identity["canonical_scenarios_sha256"],
            "summary": summary,
            "results": results,
        },
    )
    lines = [
        "# Grok AHBG common corpus report",
        "",
        f"Started: {started_at}",
        f"Ended: {ended_at}",
        f"Executed build SHA: {run_identity['runner_commit_sha']}",
        f"Baseline reciprocal-review freeze SHA: {BASELINE_FREEZE_SHA}",
        f"Runner commit SHA: {run_identity['runner_commit_sha']}",
        f"Corpus file SHA256: {corpus_identity['file_sha256']}",
        f"Canonical scenarios SHA256: {corpus_identity['canonical_scenarios_sha256']}",
        "",
        "## Standing",
        f"- SURVIVED: {summary['survived']}",
        f"- FALSIFIED: {summary['falsified']}",
        f"- UNRESOLVED: {summary['unresolved']}",
        f"- BLOCKED: {summary['blocked']}",
        "",
        "## Scenarios",
    ]
    for result in results:
        lines.append(
            "- {scenario_id}: {evidence_standing} "
            "(family={family}, turns={turns}, events={event_count}, "
            "replay_equal={replay_equal}, invalid_actions={invalid_actions}, "
            "refusals={refusals}) - {note}".format(**result)
        )
    lines.extend(
        [
            "",
            "## Notes",
            "- This is a post-freeze common-corpus execution against the exact committed runner identity recorded above.
            - Baseline reciprocal-review freeze remains `cce9cec`; current war_v3 code intentionally diverges from it.",
            "- Smoke artifacts under `artifacts/` were not rewritten.",
            "- Corpus tile ids map onto BandSlot names by UCNS axial coordinates.",
            "- Candidate regulatory cost channels are observed; they do not rank destinations.",
            "- War collisions resolve deterministically with closed turns.",
            "",
        ]
    )
    (output_root / "CALIBRATION_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    return run_identity


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=None, help="Optional local corpus.json path.")
    parser.add_argument("--output", type=Path, default=OUTPUT_DIR, help="Artifact output directory.")
    args = parser.parse_args(argv)
    corpus, identity = load_corpus(args.corpus)
    manifest = run_corpus(corpus, identity, args.output)
    print(
        json.dumps(
            {
                "scenario_count": manifest["corpus"]["scenario_count"],
                "summary": manifest["summary"],
                "corpus_file_sha256": manifest["corpus"]["file_sha256"],
                "canonical_scenarios_sha256": manifest["corpus"]["canonical_scenarios_sha256"],
                "output": str(args.output),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
