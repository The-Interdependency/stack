"""Matched one-variable intervention receipts for AHBG."""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from numbers import Real
from typing import Any, Mapping

INTERVENTION_SCHEMA = "interdependency.ahbg.matched-intervention/1"
RECEIPT_SCHEMA = "interdependency.ahbg.matched-intervention-receipt/1"
RELATIONS = frozenset({"eq", "ne", "gt", "ge", "lt", "le"})
_MISSING = object()
_MASK = {"__ahbg_intervention_mask__": True}


class InterventionError(ValueError):
    pass


def _canonical_bytes(value: Any) -> bytes:
    try:
        text = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise InterventionError(f"value is not canonical JSON: {exc}") from exc
    return text.encode("utf-8")


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _path_parts(path: str) -> tuple[str, ...]:
    if not isinstance(path, str) or not path.strip():
        raise InterventionError("path must be nonempty text")
    parts = tuple(path.split("."))
    if any(not part for part in parts):
        raise InterventionError(f"invalid dotted path {path!r}")
    return parts


def _at(document: Mapping[str, Any], path: str) -> Any:
    current: Any = document
    for part in _path_parts(path):
        if not isinstance(current, Mapping) or part not in current:
            return _MISSING
        current = current[part]
    return current


def _masked(document: Mapping[str, Any], path: str) -> dict[str, Any]:
    copied = copy.deepcopy(dict(document))
    current: Any = copied
    parts = _path_parts(path)
    for part in parts[:-1]:
        if not isinstance(current, dict) or part not in current:
            raise InterventionError(f"intervention path {path!r} is absent")
        current = current[part]
    if not isinstance(current, dict) or parts[-1] not in current:
        raise InterventionError(f"intervention path {path!r} is absent")
    current[parts[-1]] = copy.deepcopy(_MASK)
    return copied


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InterventionError(f"{field} must be nonempty text")
    return value


@dataclass(frozen=True)
class Prediction:
    observable: str
    relation: str

    @classmethod
    def parse(cls, raw: Mapping[str, Any]) -> "Prediction":
        if not isinstance(raw, Mapping):
            raise InterventionError("prediction must be an object")
        observable = _text(raw.get("observable"), "prediction.observable")
        relation = _text(raw.get("relation"), "prediction.relation")
        _path_parts(observable)
        if relation not in RELATIONS:
            raise InterventionError(
                f"prediction relation must be one of {sorted(RELATIONS)}"
            )
        return cls(observable, relation)

    def as_dict(self) -> dict[str, str]:
        return {"observable": self.observable, "relation": self.relation}


@dataclass(frozen=True)
class InterventionSpec:
    intervention_id: str
    variable: str
    control: Any
    treatment: Any
    seeds: tuple[int, ...]
    predictions: tuple[Prediction, ...]
    held_constant: tuple[str, ...]
    hmmm: tuple[str, ...] = ()

    @classmethod
    def parse(cls, raw: Mapping[str, Any]) -> "InterventionSpec":
        if not isinstance(raw, Mapping):
            raise InterventionError("spec must be an object")
        if raw.get("schema") not in (None, INTERVENTION_SCHEMA):
            raise InterventionError("unknown matched-intervention schema")

        intervention_id = _text(raw.get("intervention_id"), "intervention_id")
        variable = _text(raw.get("variable"), "variable")
        _path_parts(variable)
        if "control" not in raw or "treatment" not in raw:
            raise InterventionError("control and treatment are required")
        control = copy.deepcopy(raw["control"])
        treatment = copy.deepcopy(raw["treatment"])
        if _canonical_bytes(control) == _canonical_bytes(treatment):
            raise InterventionError("control and treatment must differ")

        seeds_raw = raw.get("seeds")
        if not isinstance(seeds_raw, list) or not seeds_raw:
            raise InterventionError("seeds must be a nonempty list")
        seeds: list[int] = []
        for seed in seeds_raw:
            if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
                raise InterventionError("seeds must be unique nonnegative integers")
            seeds.append(seed)
        if len(set(seeds)) != len(seeds):
            raise InterventionError("seeds must be unique")

        predictions_raw = raw.get("predictions")
        if not isinstance(predictions_raw, list) or not predictions_raw:
            raise InterventionError("predictions must be a nonempty list")
        predictions = tuple(Prediction.parse(item) for item in predictions_raw)
        if len({item.observable for item in predictions}) != len(predictions):
            raise InterventionError("prediction observables must be unique")

        held_raw = raw.get("held_constant")
        if not isinstance(held_raw, list) or not held_raw:
            raise InterventionError("held_constant must be a nonempty list")
        held = tuple(_text(item, "held_constant item") for item in held_raw)
        if len(set(held)) != len(held):
            raise InterventionError("held_constant entries must be unique")
        if variable in held:
            raise InterventionError("variable cannot also be held constant")

        hmmm_raw = raw.get("hmmm", [])
        if not isinstance(hmmm_raw, list) or any(
            not isinstance(item, str) or not item.strip() for item in hmmm_raw
        ):
            raise InterventionError("hmmm must contain nonempty text")

        spec = cls(
            intervention_id,
            variable,
            control,
            treatment,
            tuple(seeds),
            predictions,
            held,
            tuple(hmmm_raw),
        )
        _canonical_bytes(spec.as_dict())
        return spec

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": INTERVENTION_SCHEMA,
            "intervention_id": self.intervention_id,
            "variable": self.variable,
            "control": copy.deepcopy(self.control),
            "treatment": copy.deepcopy(self.treatment),
            "seeds": list(self.seeds),
            "predictions": [prediction.as_dict() for prediction in self.predictions],
            "held_constant": list(self.held_constant),
            "hmmm": list(self.hmmm),
        }

    @property
    def identity_sha256(self) -> str:
        return _sha256(self.as_dict())


def validate_case_pair(
    spec: InterventionSpec,
    control_case: Mapping[str, Any],
    treatment_case: Mapping[str, Any],
) -> str:
    control_value = _at(control_case, spec.variable)
    treatment_value = _at(treatment_case, spec.variable)
    if control_value is _MISSING or treatment_value is _MISSING:
        raise InterventionError("intervention variable must exist in both cases")
    if _canonical_bytes(control_value) != _canonical_bytes(spec.control):
        raise InterventionError("control case does not match preregistration")
    if _canonical_bytes(treatment_value) != _canonical_bytes(spec.treatment):
        raise InterventionError("treatment case does not match preregistration")

    masked_control = _canonical_bytes(_masked(control_case, spec.variable))
    masked_treatment = _canonical_bytes(_masked(treatment_case, spec.variable))
    if masked_control != masked_treatment:
        raise InterventionError(
            "matched cases differ outside the preregistered variable"
        )
    return hashlib.sha256(masked_control).hexdigest()


def _compare(treatment: Any, control: Any, relation: str) -> bool | None:
    if relation == "eq":
        return _canonical_bytes(treatment) == _canonical_bytes(control)
    if relation == "ne":
        return _canonical_bytes(treatment) != _canonical_bytes(control)
    if (
        isinstance(treatment, bool)
        or isinstance(control, bool)
        or not isinstance(treatment, Real)
        or not isinstance(control, Real)
    ):
        return None
    if relation == "gt":
        return treatment > control
    if relation == "ge":
        return treatment >= control
    if relation == "lt":
        return treatment < control
    if relation == "le":
        return treatment <= control
    raise InterventionError(f"unknown relation {relation!r}")


def build_pair_receipt(
    spec: InterventionSpec,
    *,
    seed: int,
    control_case: Mapping[str, Any],
    treatment_case: Mapping[str, Any],
    control_result: Mapping[str, Any],
    treatment_result: Mapping[str, Any],
) -> dict[str, Any]:
    if seed not in spec.seeds:
        raise InterventionError(f"seed {seed} was not preregistered")
    held_hash = validate_case_pair(spec, control_case, treatment_case)

    rows: list[dict[str, Any]] = []
    for prediction in spec.predictions:
        control_value = _at(control_result, prediction.observable)
        treatment_value = _at(treatment_result, prediction.observable)
        if control_value is _MISSING or treatment_value is _MISSING:
            passed = None
            standing = "UNRESOLVED"
        else:
            passed = _compare(treatment_value, control_value, prediction.relation)
            standing = (
                "UNRESOLVED"
                if passed is None
                else "SURVIVED"
                if passed
                else "FALSIFIED"
            )
        rows.append(
            {
                "observable": prediction.observable,
                "relation": prediction.relation,
                "control": None if control_value is _MISSING else copy.deepcopy(control_value),
                "treatment": None if treatment_value is _MISSING else copy.deepcopy(treatment_value),
                "standing": standing,
            }
        )

    if any(row["standing"] == "FALSIFIED" for row in rows):
        overall = "FALSIFIED"
    elif any(row["standing"] == "UNRESOLVED" for row in rows):
        overall = "UNRESOLVED"
    else:
        overall = "SURVIVED"

    receipt = {
        "schema": RECEIPT_SCHEMA,
        "intervention_id": spec.intervention_id,
        "intervention_sha256": spec.identity_sha256,
        "seed": seed,
        "variable": spec.variable,
        "held_constant_sha256": held_hash,
        "control_case_sha256": _sha256(control_case),
        "treatment_case_sha256": _sha256(treatment_case),
        "control_result_sha256": _sha256(control_result),
        "treatment_result_sha256": _sha256(treatment_result),
        "predictions": rows,
        "standing": overall,
        "hmmm": list(spec.hmmm),
    }
    receipt["receipt_sha256"] = _sha256(receipt)
    return receipt
