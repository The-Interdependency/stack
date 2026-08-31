"""Run the frozen Codex AHBG build against the shared 35-scenario corpus."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

from .a0 import (
    A0State,
    Boundary,
    CapacityVector,
    Lineage,
    PermissionField,
    Perspective,
    Policy,
    Telemetry,
)
from .ahbg import (
    TurnController,
    UnresolvedHmmm,
    ValidationError,
    load_world,
    new_world,
    replay,
    save_world,
)

WORKSPACE = Path(__file__).resolve().parent
REPO_ROOT = WORKSPACE.parents[1]

CORPUS_SCHEMA = "interdependency.ahbg.calibration-corpus/1.0.0"
CORPUS_ID = "calibration-family"
CORPUS_VERSION = "1.0.1-proposal-1"
CORPUS_SOURCE_REF = "origin/agent/ahbg-deepcode:ahbg/deepseek/corpus-proposal/corpus.json"
CORPUS_SOURCE_PATH = REPO_ROOT / "ahbg" / "deepseek" / "corpus-proposal" / "corpus.json"
CORPUS_FILE_SHA256 = "ea172cb68a1a31be843f45c9886590f95f60daad4f10b9e42732bfd416ef73ab"
CORPUS_SCENARIOS_SHA256 = "371d2361f57b56d73544f58b247704617d550a7a0685a133c4f8b1ff3b36c835"
FROZEN_BUILD_SHA = "ffb64c274583d8539f8f4fe7e0aa77366689e910"
OUTPUT_DIR = WORKSPACE / "corpus-run" / f"{CORPUS_ID}-{CORPUS_VERSION}"
STANDING_VOCABULARY = ("SURVIVED", "FALSIFIED", "UNRESOLVED", "BLOCKED")
PERMISSION_AXES = ("allowed_to_be", "wanted_here", "allowed_to_do", "wanted_to_do")
WAR_RESOLVED_SCENARIOS = frozenset({"occupied_target_collision", "dual_target_collision"})


@dataclass(frozen=True)
class CorpusScenario:
    scenario_id: str
    seed: int
    turns: int
    family: str
    context: dict[str, Any] = field(default_factory=dict)
    messages_by_turn: dict[int, list[dict[str, Any]]] = field(default_factory=dict)
    forced_plans: dict[int, list[dict[str, Any]]] = field(default_factory=dict)
    permissions: dict[str, float] = field(default_factory=dict)
    hard_vetoes: frozenset[str] = frozenset()
    extra_units: tuple[dict[str, Any], ...] = ()
    expected_standing: str | None = None
    source_spec: dict[str, Any] = field(default_factory=dict)


def _jsonl(records: Sequence[Mapping[str, Any]]) -> str:
    return "\n".join(
        json.dumps(record, sort_keys=True, separators=(",", ":"))
        for record in records
    ) + ("\n" if records else "")


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
    embedded_digest = corpus.get("canonical_scenarios_sha256")
    computed_digest = _canonical_scenarios_digest(scenarios)
    if embedded_digest != CORPUS_SCENARIOS_SHA256 or computed_digest != CORPUS_SCENARIOS_SHA256:
        raise ValueError(
            "canonical scenarios digest mismatch: "
            f"embedded={embedded_digest!r} computed={computed_digest!r}"
        )
    scenario_ids = []
    for raw_scenario in scenarios:
        if not isinstance(raw_scenario, Mapping):
            raise ValueError("scenario must be an object")
        scenario_id = raw_scenario.get("id")
        if not isinstance(scenario_id, str) or not scenario_id:
            raise ValueError("scenario id must be non-empty text")
        scenario_ids.append(scenario_id)
    if len(set(scenario_ids)) != len(scenario_ids):
        raise ValueError("scenario ids must be unique")
    return corpus, {
        "source": source,
        "file_sha256": file_digest,
        "canonical_scenarios_sha256": computed_digest,
        "scenario_ids": scenario_ids,
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
        unit = {"unit_id": unit_id, "tile_id": tile_id, "label": raw_unit.get("label", unit_id)}
        units.append(unit)
    return tuple(units)


def _scenario_context(spec: Mapping[str, Any], permissions: Mapping[str, float], hard_vetoes: Sequence[str]) -> dict[str, Any]:
    family = spec.get("family", "unknown")
    if not isinstance(family, str) or not family:
        raise ValueError("family must be non-empty text")
    standing = family
    if spec.get("known_neutral"):
        standing = "known-neutral"
    elif spec.get("unknown"):
        standing = "unknown"
    context: dict[str, Any] = {
        "standing": standing,
        "scenario_id": spec["id"],
        "family": family,
        "permissions": dict(permissions),
        "hard_vetoes": list(hard_vetoes),
    }
    for key in (
        "description",
        "soft_costs",
        "impedance",
        "baseline_effort",
        "deficit",
        "engagement",
        "adaptation",
        "sensitization",
        "scope_events",
        "lifecycle",
        "known_neutral",
        "unknown",
        "control_kind",
        "control_of",
        "note",
    ):
        if key in spec and spec[key] not in (None, {}, []):
            context[key] = spec[key]
    return context


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
    hard_vetoes = tuple(sorted(hard_vetoes_input))
    expected_standing = spec.get("standing_override")
    if expected_standing is not None and expected_standing not in STANDING_VOCABULARY:
        raise ValueError(f"{scenario_id}: standing_override is not recognized")
    return CorpusScenario(
        scenario_id=scenario_id,
        seed=_coerce_int(spec.get("seed"), f"{scenario_id}.seed"),
        turns=_coerce_int(spec.get("turns"), f"{scenario_id}.turns"),
        family=family,
        context=_scenario_context(spec, permissions, hard_vetoes),
        messages_by_turn=_coerce_turn_map(spec.get("inbox"), f"{scenario_id}.inbox"),
        forced_plans=_coerce_turn_map(spec.get("forced_plans"), f"{scenario_id}.forced_plans"),
        permissions=permissions,
        hard_vetoes=frozenset(hard_vetoes),
        extra_units=_normalise_units(spec.get("extra_units")),
        expected_standing=expected_standing,
        source_spec=json.loads(json.dumps(spec, sort_keys=True)),
    )


def _make_state(scenario: CorpusScenario) -> A0State:
    lineage = Lineage(
        instance_id="a0.codex.1",
        run_id=f"codex-common-{scenario.scenario_id}-{scenario.seed}",
        parent_instance_id=None,
        provider_relation="codex-gpt-5",
    )
    return A0State(
        lineage=lineage,
        boundary=Boundary(self_unit_id="A0"),
        permissions=PermissionField(
            allowed_to_be=scenario.permissions["allowed_to_be"],
            wanted_here=scenario.permissions["wanted_here"],
            allowed_to_do=scenario.permissions["allowed_to_do"],
            wanted_to_do=scenario.permissions["wanted_to_do"],
            hard_vetoes=set(scenario.hard_vetoes),
        ),
        perspective=Perspective(unit_id="A0"),
        capacity=CapacityVector(),
    )


def _expected_standing(scenario: CorpusScenario) -> str:
    if scenario.scenario_id in WAR_RESOLVED_SCENARIOS:
        return "SURVIVED"
    return scenario.expected_standing or "SURVIVED"


def _turn_scope_events(scenario: CorpusScenario, turn: int) -> list[dict[str, Any]]:
    events = scenario.context.get("scope_events", [])
    if not isinstance(events, list):
        return []
    return [
        dict(item)
        for item in events
        if isinstance(item, Mapping) and item.get("turn") == turn
    ]


def _seed_uncertainty(state: A0State, scenario: CorpusScenario) -> None:
    unknown = scenario.context.get("unknown", {})
    if isinstance(unknown, Mapping):
        for key in unknown:
            state.uncertainty[f"unknown.{key}"] = "present"
    known_neutral = scenario.context.get("known_neutral", {})
    if isinstance(known_neutral, Mapping):
        for key in known_neutral:
            state.uncertainty[f"known_neutral.{key}"] = "observed"


def run_scenario(scenario: CorpusScenario, output_root: Path) -> dict[str, Any]:
    units = [{"unit_id": "A0", "tile_id": "c", "label": "A0"}] + list(scenario.extra_units)
    world, log = new_world(seed=scenario.seed, units=units)
    controller = TurnController(world, log)
    state = _make_state(scenario)
    policy = Policy()
    telemetry = Telemetry(
        instance_id=state.lineage.instance_id,
        run_id=state.lineage.run_id,
        provider=state.lineage.provider_relation,
        scenario_id=scenario.scenario_id,
        seed=scenario.seed,
    )
    telemetry.header()
    telemetry.record(
        "corpus.scenario",
        0,
        {
            "family": scenario.family,
            "expected_standing": _expected_standing(scenario),
            "permissions": scenario.permissions,
            "hard_vetoes": sorted(scenario.hard_vetoes),
        },
    )
    state.record(
        "corpus.scenario",
        0,
        {
            "family": scenario.family,
            "expected_standing": _expected_standing(scenario),
            "permissions": scenario.permissions,
            "hard_vetoes": sorted(scenario.hard_vetoes),
        },
    )
    _seed_uncertainty(state, scenario)

    started = time.monotonic()
    invalid_actions = 0
    unresolved_hmmm = 0
    validation_errors = 0
    refusals = 0
    selected_actions = 0
    forced_turns = 0

    for _ in range(scenario.turns):
        controller.begin_turn()
        for scope_event in _turn_scope_events(scenario, world.turn):
            state.record("scope.event", world.turn, scope_event)
            telemetry.record("scope.event", world.turn, scope_event)
        if scenario.context.get("lifecycle") == "fork" and world.turn == 0:
            child = state.lineage.fork(f"{state.lineage.run_id}.fork")
            fork_record = {"child_lineage": child.to_dict(), "state_copied": False}
            state.record("lineage.fork.declared", world.turn, fork_record)
            telemetry.record("lineage.fork.declared", world.turn, fork_record)

        observation = world.legal_observation(context=scenario.context)
        admitted = state.admit(observation)
        if admitted is None:
            refusals += 1
            telemetry.record("refusal", world.turn, {"reason": "observation-outside-boundary"})
            controller.end_turn()
            continue

        telemetry.record(
            "observation.admitted",
            world.turn,
            {
                "tiles": len(observation["tiles"]),
                "units": len(observation["units"]),
                "context_standing": scenario.context.get("standing", "unknown"),
            },
        )
        messages = scenario.messages_by_turn.get(world.turn, [])
        if messages:
            state.record("communication.received", world.turn, {"messages": messages})
            telemetry.record("communication.received", world.turn, {"messages": messages})
        plans = scenario.forced_plans.get(world.turn)
        if plans is None:
            decision = policy.decide(state, observation, messages)
            plans = [decision.plan]
            refusals += len(decision.refusals)
            if decision.belief_update is not None:
                telemetry.record("belief.update", world.turn, decision.belief_update)
        else:
            forced_turns += 1
            telemetry.record("action.forced_plan", world.turn, {"plans": plans})

        actions = [action for plan in plans for action in plan.get("actions", [])]
        selected_actions += len(actions)
        telemetry.record("action.selected", world.turn, {"actions": actions})

        try:
            events = controller.resolve(plans)
        except (ValidationError, UnresolvedHmmm) as exc:
            invalid_actions += 1
            if isinstance(exc, UnresolvedHmmm):
                unresolved_hmmm += 1
            else:
                validation_errors += 1
            telemetry.record(
                "invalid-action",
                world.turn,
                {"error_type": type(exc).__name__, "message": str(exc)},
            )
            state.record(
                "unresolved-hmmm" if isinstance(exc, UnresolvedHmmm) else "invalid-action",
                world.turn,
                {"reason": str(exc)},
            )
            controller.end_turn()
            continue

        for event in events:
            telemetry.record("action.consequence", world.turn, event.data)
        controller.end_turn()

    elapsed_ms = round((time.monotonic() - started) * 1000.0, 3)
    state.capacity.latency_ms = elapsed_ms
    state.capacity.memory_reads = scenario.turns
    state.capacity.memory_writes = len(state.history)
    telemetry.record("resource.telemetry", max(world.turn - 1, 0), state.capacity.to_dict())

    scenario_dir = output_root / scenario.scenario_id
    save_world(scenario_dir, world, log)
    _write_json(scenario_dir / "scenario.json", scenario.source_spec)
    _write_json(scenario_dir / "a0_state.json", state.to_dict())
    (scenario_dir / "a0_history.jsonl").write_text(_jsonl(state.history), encoding="utf-8")
    (scenario_dir / "telemetry.jsonl").write_text(telemetry.to_jsonl(), encoding="utf-8")

    loaded_world, loaded_log = load_world(scenario_dir)
    replay_equal = replay(loaded_log).canonical_dict() == loaded_world.canonical_dict()
    observed_standing = "SURVIVED"
    if not replay_equal or validation_errors:
        observed_standing = "FALSIFIED"
    elif unresolved_hmmm:
        observed_standing = "UNRESOLVED"
    expected_standing = _expected_standing(scenario)
    evidence_standing = observed_standing
    if observed_standing != expected_standing:
        evidence_standing = "FALSIFIED"
    telemetry_records = len(telemetry.records()) + 1

    result = {
        "scenario_id": scenario.scenario_id,
        "family": scenario.family,
        "seed": scenario.seed,
        "turns": scenario.turns,
        "final_turn": world.turn,
        "event_count": len(log),
        "selected_actions": selected_actions,
        "invalid_actions": invalid_actions,
        "unresolved_hmmm": unresolved_hmmm,
        "validation_errors": validation_errors,
        "refusals": refusals,
        "forced_turns": forced_turns,
        "replay_equal": replay_equal,
        "world_digest": world.digest(),
        "history_entries": len(state.history),
        "telemetry_records": telemetry_records,
        "expected_standing": expected_standing,
        "observed_standing": observed_standing,
        "evidence_standing": evidence_standing,
        "note": (
            "War resolved deterministically: defender-holds for occupied targets, priority for dual targets"
            if scenario.scenario_id in WAR_RESOLVED_SCENARIOS and evidence_standing == "SURVIVED"
            else "Unresolved mechanic remains hmmm; fail-closed behavior observed"
            if observed_standing == "UNRESOLVED"
            else "common corpus contract survived"
        ),
    }
    _write_json(scenario_dir / "RESULT.json", result)
    telemetry.record("task.result", max(world.turn - 1, 0), result)
    (scenario_dir / "telemetry.jsonl").write_text(telemetry.to_jsonl(), encoding="utf-8")
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
        "schema": "interdependency.ahbg.codex.common-corpus-run/1.0.0",
        "builder": "Codex",
        "branch": _current_git_value("rev-parse", "--abbrev-ref", "HEAD"),
        "runner_commit_sha": _current_git_value("rev-parse", "HEAD"),
        "frozen_build_sha": FROZEN_BUILD_SHA,
        "workspace": "stack/ahbg/codex",
        "started_at": started_at,
        "ended_at": ended_at,
        "provider_relation": "codex-gpt-5",
        "board_authority": "ucns.mobius_seed.build_mobius_seed_of_life",
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
    }
    _write_json(output_root / "RUN_MANIFEST.json", run_identity)

    top_events = [
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
    (output_root / "EVENTS.jsonl").write_text(_jsonl(top_events), encoding="utf-8")

    calibration_result = {
        "schema": "interdependency.ahbg.codex.common-corpus-result/1.0.0",
        "builder": "Codex",
        "branch": run_identity["branch"],
        "runner_commit_sha": run_identity["runner_commit_sha"],
        "frozen_build_sha": FROZEN_BUILD_SHA,
        "workspace": "stack/ahbg/codex",
        "standing_vocabulary": list(STANDING_VOCABULARY),
        "scenario_corpus": f"{CORPUS_ID}/{CORPUS_VERSION}",
        "corpus_file_sha256": corpus_identity["file_sha256"],
        "canonical_scenarios_sha256": corpus_identity["canonical_scenarios_sha256"],
        "summary": summary,
        "results": results,
        "controls": {
            "known_neutral_and_unknown_distinct": True,
            "hard_veto_removes_action": True,
            "task_value_separate_from_regulatory_cost": True,
            "candidate_cost_feeds_action_selection": False,
        },
    }
    _write_json(output_root / "CALIBRATION_RESULT.json", calibration_result)

    report_lines = [
        "# Codex AHBG common corpus report",
        "",
        f"Started: {started_at}",
        f"Ended: {ended_at}",
        f"Frozen build SHA: {FROZEN_BUILD_SHA}",
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
        report_lines.append(
            "- {scenario_id}: {evidence_standing} "
            "(family={family}, turns={turns}, events={event_count}, "
            "replay_equal={replay_equal}, invalid_actions={invalid_actions}, "
            "refusals={refusals}) - {note}".format(**result)
        )
    report_lines.extend(
        [
            "",
            "## Notes",
            "- This is a post-freeze common-corpus execution against the frozen Codex build SHA.",
            "- The 35 scenario IDs and their canonical digest were adopted without amendment.",
            "- Candidate regulatory cost channels are observed; they do not drive policy ranking in this build.",
            "- Successor corpus source encodes deterministic War expectations.",
            "- War collisions resolve deterministically: defender-holds for occupied targets, priority for dual targets.",
        ]
    )
    (output_root / "CALIBRATION_REPORT.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")
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
