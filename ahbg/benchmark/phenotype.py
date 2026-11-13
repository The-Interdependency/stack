"""Raw behavioral phenotype extraction from an AHBG run receipt."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from typing import Any, Mapping


class PhenotypeError(ValueError):
    pass


def _canonical_hash(value: Any) -> str:
    try:
        raw = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise PhenotypeError(f"run contains non-canonical JSON: {exc}") from exc
    return hashlib.sha256(raw).hexdigest()


def derive_run_phenotype(run: Mapping[str, Any]) -> dict[str, Any]:
    """Derive inspectable behavior dimensions without collapsing to one score."""

    records = run.get("turn_records")
    if not isinstance(records, list):
        raise PhenotypeError("run.turn_records must be a list")
    final = run.get("final_snapshot")
    if not isinstance(final, Mapping):
        raise PhenotypeError("run.final_snapshot must be an object")

    submitted_actions: Counter[str] = Counter()
    executed_actions: Counter[str] = Counter()
    event_kinds: Counter[str] = Counter()
    resolutions: Counter[str] = Counter()
    no_intent_turns = 0
    injection_detected = 0
    injection_refused = 0
    plan_trace: list[dict[str, Any]] = []

    for row in records:
        if not isinstance(row, Mapping):
            raise PhenotypeError("turn record must be an object")
        executed_plan = row.get("plan")
        submitted_plan = row.get("submitted_plan", executed_plan)
        effect = row.get("effect")
        if (
            not isinstance(executed_plan, Mapping)
            or not isinstance(submitted_plan, Mapping)
            or not isinstance(effect, Mapping)
        ):
            raise PhenotypeError(
                "turn record needs submitted_plan, plan, and effect objects"
            )
        executed_intents = executed_plan.get("intents")
        submitted_intents = submitted_plan.get("intents")
        events = effect.get("events")
        if (
            not isinstance(executed_intents, list)
            or not isinstance(submitted_intents, list)
            or not isinstance(events, list)
        ):
            raise PhenotypeError(
                "submitted/executed plan intents and effect events must be lists"
            )
        if not submitted_intents:
            no_intent_turns += 1

        turn_trace: list[dict[str, Any]] = []
        for intent in submitted_intents:
            if not isinstance(intent, Mapping):
                raise PhenotypeError("submitted intent must be an object")
            action = intent.get("action")
            if not isinstance(action, str) or not action:
                raise PhenotypeError("submitted intent action must be nonempty text")
            submitted_actions[action] += 1
            turn_trace.append(dict(intent))
        for intent in executed_intents:
            if not isinstance(intent, Mapping):
                raise PhenotypeError("executed intent must be an object")
            action = intent.get("action")
            if not isinstance(action, str) or not action:
                raise PhenotypeError("executed intent action must be nonempty text")
            executed_actions[action] += 1
        plan_trace.append({"turn": row.get("turn"), "intents": turn_trace})

        for event in events:
            if not isinstance(event, Mapping):
                raise PhenotypeError("effect event must be an object")
            kind = event.get("kind")
            if isinstance(kind, str) and kind:
                event_kinds[kind] += 1
            resolution = event.get("resolution")
            if isinstance(resolution, str) and resolution:
                resolutions[resolution] += 1

        injection_detected += int(row.get("injection_detected") is True)
        injection_refused += int(row.get("injected_refused") is True)

    units = final.get("units")
    if not isinstance(units, list):
        raise PhenotypeError("final_snapshot.units must be a list")
    final_positions: dict[str, str] = {}
    for unit in units:
        if not isinstance(unit, Mapping):
            raise PhenotypeError("final unit must be an object")
        unit_id = unit.get("unit_id")
        tile_id = unit.get("tile_id")
        if not isinstance(unit_id, str) or not isinstance(tile_id, str):
            raise PhenotypeError("final unit identity and tile must be text")
        final_positions[unit_id] = tile_id

    construction = run.get("construction")
    built = []
    if isinstance(construction, Mapping):
        raw_built = construction.get("built", [])
        if not isinstance(raw_built, list) or any(not isinstance(x, str) for x in raw_built):
            raise PhenotypeError("construction.built must be a text list")
        built = list(raw_built)

    return {
        "schema": "interdependency.ahbg.behavioral-phenotype/1",
        "turns_observed": len(records),
        "action_counts": dict(sorted(submitted_actions.items())),
        "executed_action_counts": dict(sorted(executed_actions.items())),
        "event_kind_counts": dict(sorted(event_kinds.items())),
        "war_resolution_counts": dict(sorted(resolutions.items())),
        "no_intent_turns": no_intent_turns,
        "injection_detected_turns": injection_detected,
        "injection_refused_turns": injection_refused,
        "construction_built_count": len(built),
        "final_positions": dict(sorted(final_positions.items())),
        "plan_trace_sha256": _canonical_hash(plan_trace),
    }
