"""Strict, provenance-bound records for Stack-local digital metric research.

This module defines transport and integrity contracts.  It does not assign
numbers to METAPAT doctrine, prove UCNS geometry, or validate EDCM metrics.

Usage guidance
--------------
Construct definitions and observations with the helpers below, then seal them
inside a receipt::

    definition = make_metric_definition(...)
    observation = make_observation(definition=definition, ...)
    receipt = seal_receipt(...)
    verify_receipt(receipt)

All wire records are strict.  Missing fields, unknown fields, booleans used as
integers, floating-point numbers, and implicit missing-to-zero conversions are
rejected.  A non-observed value must be explicit ``null`` with a reason.
"""

from __future__ import annotations

# === MODULE_BUILD ===
# id: stack_digital_metric_protocol
#   module_name: digital metric protocol
#   module_kind: schema
#   summary: strict candidate metric definitions, observations, retained structures, and deterministic receipts for cross-repository research
#   owner: The-Interdependency/stack
#   public_surface: canonical_json,sha256_json,integer_value,rational_value,make_metric_definition,validate_metric_definition,make_observation,validate_observation,seal_structure,validate_structure,retention_definitions,measure_retention,seal_receipt,verify_receipt
#   internal_surface: strict field, scalar, digest, integer, rational, provenance, and uncertainty validators
#   auth_boundary: none
#   storage_boundary: serialization-only
#   network_boundary: none
#   user_data_boundary: public research fixtures only
#   admin_only: false
#   tests: research/digital-metrics/tests/test_metric_protocol.py
#   rollout: stack-local research only; no canonical or production activation
#   rollback: remove research/digital-metrics and its manifest projections
#   requires: stack fresh-making identity discipline, exact METAPAT/UCNS/EDCM producer identities
#   since: 2026-09-20
#   unresolved: empirical calibration, EDCM projection selection, independent verifier implementation, producer authentication
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: digital_metric_missing_never_becomes_zero
#   given: an observation field or a definition's entire observation is omitted, or a non-observed status is used
#   then: omission is rejected and non-observed status requires explicit null plus a non-empty reason
#   class: correctness
#
# id: digital_metric_types_are_exact
#   given: metric records contain booleans, integers, rationals, or unsupported floating-point values
#   then: each value is accepted only under its exact declared kind and floats are rejected
#   class: correctness
#
# id: digital_metric_provenance_revision_is_typed
#   given: an observation identifies a committed producer or a pre-commit local artifact
#   then: its source revision is explicitly typed and candidate-content identity must equal the artifact digest
#   class: provenance
#
# id: digital_metric_structure_preserves_order_multiplicity_provenance
#   given: retained structures differ by participant provenance, relation order, or relation multiplicity
#   then: the corresponding integrity observation changes rather than collapsing the structures
#   class: evidence
#
# id: digital_metric_receipt_replays_byte_identically
#   given: identical definitions, observations, bindings, inputs, and verifier identity
#   then: canonical receipt bytes and digest are identical and tampering fails verification
#   class: provenance
#
# id: digital_metric_status_does_not_transfer
#   given: a receipt binds METAPAT, UCNS, EDCM, and Stack identities
#   then: every binding keeps authority and measurement-status transfer false
#   class: boundary
# === END CONTRACTS ===

from collections import Counter
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
import re
from typing import Any, Iterable, Mapping


DEFINITION_SCHEMA = "the-interdependency.metric-definition"
DEFINITION_VERSION = "0.1.0"
OBSERVATION_SCHEMA = "the-interdependency.metric-observation"
OBSERVATION_VERSION = "0.1.0"
STRUCTURE_SCHEMA = "the-interdependency.retained-structure"
STRUCTURE_VERSION = "0.1.0"
RECEIPT_SCHEMA = "the-interdependency.metric-receipt"
RECEIPT_VERSION = "0.1.0"

OBSERVATION_STATUSES = frozenset({"observed", "not_applicable", "unresolved", "failed"})
VALIDATION_STATUSES = frozenset({"candidate", "test-backed", "calibrated", "validated-for-scope"})
VALUE_KINDS = frozenset({"boolean", "integer", "rational", "category"})
REPLAY_RESULTS = frozenset({"pending", "pass"})
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


class MetricProtocolError(ValueError):
    """Raised when a digital metric record violates the strict wire contract."""


def canonical_json(value: Any) -> str:
    """Return deterministic compact JSON after rejecting lossy scalar types."""

    _reject_unsupported_scalars(value, "record")
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _reject_unsupported_scalars(value: Any, path: str) -> None:
    if value is None or isinstance(value, (str, bool)):
        return
    if type(value) is int:
        return
    if isinstance(value, float):
        raise MetricProtocolError(f"{path} contains unsupported floating-point value")
    if isinstance(value, list):
        for index, item in enumerate(value):
            _reject_unsupported_scalars(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise MetricProtocolError(f"{path} contains a non-string key")
            _reject_unsupported_scalars(item, f"{path}.{key}")
        return
    raise MetricProtocolError(f"{path} contains unsupported value type {type(value).__name__}")


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MetricProtocolError(f"{label} must be an object")
    return value


def _exact_fields(record: Mapping[str, Any], expected: Iterable[str], label: str) -> None:
    expected_set = set(expected)
    actual = set(record)
    missing = sorted(expected_set - actual)
    unknown = sorted(actual - expected_set)
    if missing:
        raise MetricProtocolError(f"{label} missing required fields: {', '.join(missing)}")
    if unknown:
        raise MetricProtocolError(f"{label} contains unknown fields: {', '.join(unknown)}")


def _text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MetricProtocolError(f"{label} must be a non-empty string")
    return value


def _optional_text(value: Any, label: str) -> str | None:
    if value is None:
        return None
    return _text(value, label)


def _boolean(value: Any, label: str) -> bool:
    if type(value) is not bool:
        raise MetricProtocolError(f"{label} must be a boolean")
    return value


def _integer(value: Any, label: str, *, minimum: int | None = None) -> int:
    if type(value) is not int:
        raise MetricProtocolError(f"{label} must be an integer, not {type(value).__name__}")
    if minimum is not None and value < minimum:
        raise MetricProtocolError(f"{label} must be >= {minimum}")
    return value


def _sha256(value: Any, label: str) -> str:
    text = _text(value, label)
    if SHA256_RE.fullmatch(text) is None:
        raise MetricProtocolError(f"{label} must be a lowercase SHA-256 digest")
    return text


def _commit(value: Any, label: str) -> str:
    text = _text(value, label)
    if COMMIT_RE.fullmatch(text) is None:
        raise MetricProtocolError(f"{label} must be a 40-character lowercase Git commit")
    return text


def _string_list(value: Any, label: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list):
        raise MetricProtocolError(f"{label} must be an array")
    if not allow_empty and not value:
        raise MetricProtocolError(f"{label} must not be empty")
    return [_text(item, f"{label}[{index}]") for index, item in enumerate(value)]


def rational_value(value: Fraction | int) -> dict[str, Any]:
    if isinstance(value, bool) or not isinstance(value, (Fraction, int)):
        raise MetricProtocolError("rational value must be an exact Fraction or integer")
    fraction = Fraction(value)
    return {"kind": "rational", "numerator": fraction.numerator, "denominator": fraction.denominator}


def integer_value(value: int) -> dict[str, Any]:
    return {"kind": "integer", "value": _integer(value, "integer value")}


def boolean_value(value: bool) -> dict[str, Any]:
    return {"kind": "boolean", "value": _boolean(value, "boolean value")}


def _validate_rational_wire(value: Any, label: str) -> Fraction:
    record = _mapping(value, label)
    _exact_fields(record, ("kind", "numerator", "denominator"), label)
    if record["kind"] != "rational":
        raise MetricProtocolError(f"{label}.kind must be 'rational'")
    numerator = _integer(record["numerator"], f"{label}.numerator")
    denominator = _integer(record["denominator"], f"{label}.denominator", minimum=1)
    if Fraction(numerator, denominator).denominator != denominator:
        raise MetricProtocolError(f"{label} must be reduced to canonical rational form")
    return Fraction(numerator, denominator)


def _validate_integer_wire(value: Any, label: str) -> int:
    record = _mapping(value, label)
    _exact_fields(record, ("kind", "value"), label)
    if record["kind"] != "integer":
        raise MetricProtocolError(f"{label}.kind must be 'integer'")
    return _integer(record["value"], f"{label}.value")


def _validate_value_contract(value: Any) -> dict[str, Any]:
    record = _mapping(value, "metric definition value_contract")
    _exact_fields(record, ("kind", "unit", "minimum", "maximum"), "metric definition value_contract")
    kind = _text(record["kind"], "value_contract.kind")
    if kind not in VALUE_KINDS:
        raise MetricProtocolError(f"unsupported value kind {kind!r}")
    _text(record["unit"], "value_contract.unit")
    if kind == "integer":
        if record["minimum"] is not None:
            _validate_integer_wire(record["minimum"], "value_contract.minimum")
        if record["maximum"] is not None:
            _validate_integer_wire(record["maximum"], "value_contract.maximum")
        if record["minimum"] is not None and record["maximum"] is not None:
            if _validate_integer_wire(record["minimum"], "value_contract.minimum") > _validate_integer_wire(record["maximum"], "value_contract.maximum"):
                raise MetricProtocolError("value_contract minimum exceeds maximum")
    elif kind == "rational":
        if record["minimum"] is not None:
            _validate_rational_wire(record["minimum"], "value_contract.minimum")
        if record["maximum"] is not None:
            _validate_rational_wire(record["maximum"], "value_contract.maximum")
        if record["minimum"] is not None and record["maximum"] is not None:
            if _validate_rational_wire(record["minimum"], "value_contract.minimum") > _validate_rational_wire(record["maximum"], "value_contract.maximum"):
                raise MetricProtocolError("value_contract minimum exceeds maximum")
    elif record["minimum"] is not None or record["maximum"] is not None:
        raise MetricProtocolError(f"{kind} value contract must use null numeric bounds")
    return record


def make_metric_definition(
    *,
    metric_id: str,
    metric_version: str,
    owner_repository: str,
    construct: str,
    subject_kind: str,
    value_kind: str,
    unit: str,
    minimum: Fraction | int | None,
    maximum: Fraction | int | None,
    computation_id: str,
    computation_sha256: str,
    interpretation: str,
    nonclaims: Iterable[str],
    validation_status: str = "candidate",
) -> dict[str, Any]:
    definition = {
        "schema": DEFINITION_SCHEMA,
        "version": DEFINITION_VERSION,
        "metric_id": metric_id,
        "metric_version": metric_version,
        "owner_repository": owner_repository,
        "construct": construct,
        "subject_kind": subject_kind,
        "value_contract": {
            "kind": value_kind,
            "unit": unit,
            "minimum": (
                integer_value(minimum) if value_kind == "integer" else rational_value(minimum)
            ) if minimum is not None else None,
            "maximum": (
                integer_value(maximum) if value_kind == "integer" else rational_value(maximum)
            ) if maximum is not None else None,
        },
        "computation": {"id": computation_id, "sha256": computation_sha256},
        "interpretation": interpretation,
        "nonclaims": list(nonclaims),
        "validation_status": validation_status,
        "missingness": {
            "statuses": ["observed", "not_applicable", "unresolved", "failed"],
            "observed_requires_value": True,
            "non_observed_requires_null": True,
            "non_observed_requires_reason": True,
        },
    }
    return validate_metric_definition(definition)


def validate_metric_definition(value: Any) -> dict[str, Any]:
    record = _mapping(value, "metric definition")
    _exact_fields(
        record,
        (
            "schema", "version", "metric_id", "metric_version", "owner_repository",
            "construct", "subject_kind", "value_contract", "computation",
            "interpretation", "nonclaims", "validation_status", "missingness",
        ),
        "metric definition",
    )
    if (record["schema"], record["version"]) != (DEFINITION_SCHEMA, DEFINITION_VERSION):
        raise MetricProtocolError("unsupported metric definition schema/version")
    for field in ("metric_id", "metric_version", "owner_repository", "construct", "subject_kind", "interpretation"):
        _text(record[field], f"metric definition {field}")
    _validate_value_contract(record["value_contract"])
    computation = _mapping(record["computation"], "metric definition computation")
    _exact_fields(computation, ("id", "sha256"), "metric definition computation")
    _text(computation["id"], "computation.id")
    _sha256(computation["sha256"], "computation.sha256")
    _string_list(record["nonclaims"], "metric definition nonclaims", allow_empty=False)
    if record["validation_status"] not in VALIDATION_STATUSES:
        raise MetricProtocolError("unsupported metric definition validation_status")
    missingness = _mapping(record["missingness"], "metric definition missingness")
    _exact_fields(
        missingness,
        ("statuses", "observed_requires_value", "non_observed_requires_null", "non_observed_requires_reason"),
        "metric definition missingness",
    )
    if missingness["statuses"] != ["observed", "not_applicable", "unresolved", "failed"]:
        raise MetricProtocolError("metric definition missingness statuses differ from protocol")
    for field in ("observed_requires_value", "non_observed_requires_null", "non_observed_requires_reason"):
        if _boolean(missingness[field], f"missingness.{field}") is not True:
            raise MetricProtocolError(f"missingness.{field} must be true")
    normalized = deepcopy(record)
    _reject_unsupported_scalars(normalized, "metric definition")
    return normalized


def metric_definition_sha256(definition: Mapping[str, Any]) -> str:
    return sha256_json(validate_metric_definition(definition))


def _validate_metric_value(value: Any, contract: Mapping[str, Any], label: str) -> None:
    kind = contract["kind"]
    if kind == "boolean":
        record = _mapping(value, label)
        _exact_fields(record, ("kind", "value"), label)
        if record["kind"] != "boolean":
            raise MetricProtocolError(f"{label}.kind must be 'boolean'")
        _boolean(record["value"], f"{label}.value")
        return
    if kind == "integer":
        integer = _validate_integer_wire(value, label)
        minimum = contract["minimum"]
        maximum = contract["maximum"]
        if minimum is not None and integer < _validate_integer_wire(minimum, "value_contract.minimum"):
            raise MetricProtocolError(f"{label} falls below metric minimum")
        if maximum is not None and integer > _validate_integer_wire(maximum, "value_contract.maximum"):
            raise MetricProtocolError(f"{label} exceeds metric maximum")
        return
    if kind == "rational":
        fraction = _validate_rational_wire(value, label)
        minimum = contract["minimum"]
        maximum = contract["maximum"]
        if minimum is not None and fraction < _validate_rational_wire(minimum, "value_contract.minimum"):
            raise MetricProtocolError(f"{label} falls below metric minimum")
        if maximum is not None and fraction > _validate_rational_wire(maximum, "value_contract.maximum"):
            raise MetricProtocolError(f"{label} exceeds metric maximum")
        return
    if kind == "category":
        record = _mapping(value, label)
        _exact_fields(record, ("kind", "value"), label)
        if record["kind"] != "category":
            raise MetricProtocolError(f"{label}.kind must be 'category'")
        _text(record["value"], f"{label}.value")
        return
    raise MetricProtocolError(f"unsupported metric value kind {kind!r}")


def _validate_provenance(value: Any) -> dict[str, Any]:
    record = _mapping(value, "observation provenance")
    _exact_fields(
        record,
        (
            "work_graph_sha256", "source_repository", "source_revision",
            "source_artifact_sha256", "generator_id", "generator_sha256",
        ),
        "observation provenance",
    )
    _sha256(record["work_graph_sha256"], "provenance.work_graph_sha256")
    _text(record["source_repository"], "provenance.source_repository")
    artifact_sha256 = _sha256(
        record["source_artifact_sha256"], "provenance.source_artifact_sha256"
    )
    revision = _mapping(record["source_revision"], "provenance.source_revision")
    _exact_fields(revision, ("kind", "value"), "provenance.source_revision")
    revision_kind = _text(revision["kind"], "provenance.source_revision.kind")
    if revision_kind == "git-commit":
        _commit(revision["value"], "provenance.source_revision.value")
    elif revision_kind == "candidate-content":
        revision_value = _sha256(revision["value"], "provenance.source_revision.value")
        if revision_value != artifact_sha256:
            raise MetricProtocolError("candidate-content revision must equal source artifact digest")
    else:
        raise MetricProtocolError(f"unsupported provenance source revision kind {revision_kind!r}")
    _text(record["generator_id"], "provenance.generator_id")
    _sha256(record["generator_sha256"], "provenance.generator_sha256")
    return record


def make_observation(
    *,
    definition: Mapping[str, Any],
    subject_id: str,
    subject_sha256: str,
    sequence_index: int,
    status: str,
    value: dict[str, Any] | None,
    reason: str | None,
    uncertainty_kind: str,
    provenance: Mapping[str, Any],
) -> dict[str, Any]:
    validated_definition = validate_metric_definition(definition)
    observation: dict[str, Any] = {
        "schema": OBSERVATION_SCHEMA,
        "version": OBSERVATION_VERSION,
        "metric_id": validated_definition["metric_id"],
        "metric_version": validated_definition["metric_version"],
        "definition_sha256": metric_definition_sha256(validated_definition),
        "subject": {"id": subject_id, "sha256": subject_sha256},
        "sequence_index": sequence_index,
        "status": status,
        "value": value,
        "reason": reason,
        "uncertainty": {"kind": uncertainty_kind},
        "provenance": dict(provenance),
    }
    observation["observation_sha256"] = sha256_json(observation)
    return validate_observation(observation, validated_definition)


def validate_observation(value: Any, definition: Mapping[str, Any]) -> dict[str, Any]:
    record = _mapping(value, "metric observation")
    _exact_fields(
        record,
        (
            "schema", "version", "metric_id", "metric_version", "definition_sha256",
            "subject", "sequence_index", "status", "value", "reason", "uncertainty",
            "provenance", "observation_sha256",
        ),
        "metric observation",
    )
    if (record["schema"], record["version"]) != (OBSERVATION_SCHEMA, OBSERVATION_VERSION):
        raise MetricProtocolError("unsupported metric observation schema/version")
    validated_definition = validate_metric_definition(definition)
    if record["metric_id"] != validated_definition["metric_id"] or record["metric_version"] != validated_definition["metric_version"]:
        raise MetricProtocolError("observation metric identity differs from definition")
    if _sha256(record["definition_sha256"], "observation.definition_sha256") != metric_definition_sha256(validated_definition):
        raise MetricProtocolError("observation definition digest mismatch")
    subject = _mapping(record["subject"], "observation subject")
    _exact_fields(subject, ("id", "sha256"), "observation subject")
    _text(subject["id"], "observation subject id")
    _sha256(subject["sha256"], "observation subject sha256")
    _integer(record["sequence_index"], "observation sequence_index", minimum=0)
    status = _text(record["status"], "observation status")
    if status not in OBSERVATION_STATUSES:
        raise MetricProtocolError(f"unsupported observation status {status!r}")
    reason = _optional_text(record["reason"], "observation reason")
    uncertainty = _mapping(record["uncertainty"], "observation uncertainty")
    _exact_fields(uncertainty, ("kind",), "observation uncertainty")
    uncertainty_kind = _text(uncertainty["kind"], "observation uncertainty kind")
    if status == "observed":
        if record["value"] is None:
            raise MetricProtocolError("observed metric value must not be null")
        if reason is not None:
            raise MetricProtocolError("observed metric reason must be null")
        if uncertainty_kind != "exact":
            raise MetricProtocolError("prototype observed values require exact uncertainty")
        _validate_metric_value(record["value"], validated_definition["value_contract"], "observation value")
    else:
        if record["value"] is not None:
            raise MetricProtocolError("non-observed metric value must be explicit null")
        if reason is None:
            raise MetricProtocolError("non-observed metric requires a non-empty reason")
        if uncertainty_kind != "not_quantified":
            raise MetricProtocolError("non-observed metric uncertainty must be not_quantified")
    _validate_provenance(record["provenance"])
    digest = _sha256(record["observation_sha256"], "observation.observation_sha256")
    payload = {key: deepcopy(item) for key, item in record.items() if key != "observation_sha256"}
    if digest != sha256_json(payload):
        raise MetricProtocolError("observation digest mismatch")
    normalized = deepcopy(record)
    _reject_unsupported_scalars(normalized, "metric observation")
    return normalized


def seal_structure(
    *,
    structure_id: str,
    scale: str,
    participants: Iterable[Mapping[str, Any]],
    relations: Iterable[Mapping[str, Any]],
    unresolved: Iterable[str] = (),
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "schema": STRUCTURE_SCHEMA,
        "version": STRUCTURE_VERSION,
        "structure_id": structure_id,
        "scale": scale,
        "participants": [dict(item) for item in participants],
        "relations": [dict(item) for item in relations],
        "unresolved": list(unresolved),
    }
    record["structure_sha256"] = sha256_json(record)
    return validate_structure(record)


def validate_structure(value: Any) -> dict[str, Any]:
    record = _mapping(value, "retained structure")
    _exact_fields(
        record,
        ("schema", "version", "structure_id", "scale", "participants", "relations", "unresolved", "structure_sha256"),
        "retained structure",
    )
    if (record["schema"], record["version"]) != (STRUCTURE_SCHEMA, STRUCTURE_VERSION):
        raise MetricProtocolError("unsupported retained structure schema/version")
    _text(record["structure_id"], "retained structure id")
    _text(record["scale"], "retained structure scale")
    if not isinstance(record["participants"], list):
        raise MetricProtocolError("retained structure participants must be an array")
    participant_ids: set[str] = set()
    for index, value in enumerate(record["participants"]):
        participant = _mapping(value, f"participant[{index}]")
        _exact_fields(participant, ("identity", "provenance_sha256"), f"participant[{index}]")
        identity = _text(participant["identity"], f"participant[{index}].identity")
        if identity in participant_ids:
            raise MetricProtocolError(f"duplicate participant identity {identity!r}")
        participant_ids.add(identity)
        _sha256(participant["provenance_sha256"], f"participant[{index}].provenance_sha256")
    if not isinstance(record["relations"], list):
        raise MetricProtocolError("retained structure relations must be an array")
    relation_ids: set[str] = set()
    for index, value in enumerate(record["relations"]):
        relation = _mapping(value, f"relation[{index}]")
        _exact_fields(relation, ("identity", "kind", "ordered_participants", "multiplicity"), f"relation[{index}]")
        identity = _text(relation["identity"], f"relation[{index}].identity")
        if identity in relation_ids:
            raise MetricProtocolError(f"duplicate relation identity {identity!r}")
        relation_ids.add(identity)
        _text(relation["kind"], f"relation[{index}].kind")
        ordered = _string_list(relation["ordered_participants"], f"relation[{index}].ordered_participants", allow_empty=False)
        unknown = [item for item in ordered if item not in participant_ids]
        if unknown:
            raise MetricProtocolError(f"relation[{index}] references unknown participants: {unknown!r}")
        _integer(relation["multiplicity"], f"relation[{index}].multiplicity", minimum=1)
    _string_list(record["unresolved"], "retained structure unresolved")
    digest = _sha256(record["structure_sha256"], "retained structure sha256")
    payload = {key: deepcopy(item) for key, item in record.items() if key != "structure_sha256"}
    if digest != sha256_json(payload):
        raise MetricProtocolError("retained structure digest mismatch")
    normalized = deepcopy(record)
    _reject_unsupported_scalars(normalized, "retained structure")
    return normalized


def retention_definitions(computation_sha256: str) -> list[dict[str, Any]]:
    common = {
        "metric_version": "0.1.0",
        "owner_repository": "The-Interdependency/stack",
        "subject_kind": "retained-structure-transition",
        "computation_id": "stack.digital-metrics.retention-v0",
        "computation_sha256": computation_sha256,
        "validation_status": "candidate",
    }
    nonclaims = (
        "Does not establish METAPAT validity, UCNS theorem status, EDCM measurement validity, or external truth.",
        "Measures record preservation only; it does not measure semantic quality or geometric correctness.",
    )
    return [
        make_metric_definition(
            metric_id="stack.integrity.participant_identity_retention",
            construct="Fraction of before-participant identities still individually addressable after transition.",
            value_kind="rational", unit="ratio", minimum=0, maximum=1,
            interpretation="One means all declared participant identities remain addressable; it does not mean their states are unchanged.",
            nonclaims=nonclaims, **common,
        ),
        make_metric_definition(
            metric_id="stack.integrity.ordered_relation_retention",
            construct="Multiplicity-weighted fraction of relation identities, kinds, and ordered participant tuples retained after transition.",
            value_kind="rational", unit="ratio", minimum=0, maximum=1,
            interpretation="Order reversal or multiplicity loss lowers the value rather than collapsing to the same relation.",
            nonclaims=nonclaims, **common,
        ),
        make_metric_definition(
            metric_id="stack.integrity.provenance_binding_complete",
            construct="Whether every before participant remains present with the identical provenance digest.",
            value_kind="boolean", unit="truth-value", minimum=None, maximum=None,
            interpretation="True means exact participant/provenance binding survived this record transition.",
            nonclaims=nonclaims, **common,
        ),
    ]


def _relation_counter(structure: Mapping[str, Any]) -> Counter[tuple[Any, ...]]:
    counter: Counter[tuple[Any, ...]] = Counter()
    for relation in structure["relations"]:
        signature = (
            relation["identity"], relation["kind"], tuple(relation["ordered_participants"]),
        )
        counter[signature] += relation["multiplicity"]
    return counter


def measure_retention(
    before: Mapping[str, Any],
    after: Mapping[str, Any],
    *,
    provenance: Mapping[str, Any],
    computation_sha256: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    before_record = validate_structure(before)
    after_record = validate_structure(after)
    definitions = retention_definitions(computation_sha256)
    subject_id = f"{before_record['structure_id']}->{after_record['structure_id']}"
    subject_sha256 = sha256_json(
        {"before": before_record["structure_sha256"], "after": after_record["structure_sha256"]}
    )

    before_participants = {item["identity"]: item["provenance_sha256"] for item in before_record["participants"]}
    after_participants = {item["identity"]: item["provenance_sha256"] for item in after_record["participants"]}
    retained_participants = set(before_participants) & set(after_participants)
    before_relations = _relation_counter(before_record)
    after_relations = _relation_counter(after_record)
    retained_relations = sum(min(count, after_relations[signature]) for signature, count in before_relations.items())
    total_relations = sum(before_relations.values())
    provenance_complete = bool(before_participants) and all(
        after_participants.get(identity) == digest for identity, digest in before_participants.items()
    )

    values: list[tuple[str, dict[str, Any] | None, str | None, str]] = []
    if before_participants:
        values.append(("observed", rational_value(Fraction(len(retained_participants), len(before_participants))), None, "exact"))
    else:
        values.append(("not_applicable", None, "before structure contains no participants", "not_quantified"))
    if total_relations:
        values.append(("observed", rational_value(Fraction(retained_relations, total_relations)), None, "exact"))
    else:
        values.append(("not_applicable", None, "before structure contains no relations", "not_quantified"))
    if before_participants:
        values.append(("observed", boolean_value(provenance_complete), None, "exact"))
    else:
        values.append(("not_applicable", None, "before structure contains no participants", "not_quantified"))

    observations = [
        make_observation(
            definition=definition,
            subject_id=subject_id,
            subject_sha256=subject_sha256,
            sequence_index=index,
            status=status,
            value=value,
            reason=reason,
            uncertainty_kind=uncertainty,
            provenance=provenance,
        )
        for index, (definition, (status, value, reason, uncertainty)) in enumerate(zip(definitions, values, strict=True))
    ]
    return definitions, observations


def _validate_binding(value: Any, index: int) -> dict[str, Any]:
    label = f"receipt binding[{index}]"
    record = _mapping(value, label)
    _exact_fields(
        record,
        (
            "kind", "identity", "version", "repository", "commit", "artifact_sha256",
            "record_digest", "authority_transfer", "measurement_status_transfer",
        ),
        label,
    )
    for field in ("kind", "identity", "version", "repository"):
        _text(record[field], f"{label}.{field}")
    _commit(record["commit"], f"{label}.commit")
    _sha256(record["artifact_sha256"], f"{label}.artifact_sha256")
    _sha256(record["record_digest"], f"{label}.record_digest")
    if _boolean(record["authority_transfer"], f"{label}.authority_transfer") is not False:
        raise MetricProtocolError(f"{label}.authority_transfer must be false")
    if _boolean(record["measurement_status_transfer"], f"{label}.measurement_status_transfer") is not False:
        raise MetricProtocolError(f"{label}.measurement_status_transfer must be false")
    return record


def seal_receipt(
    *,
    work_graph_sha256: str,
    definitions: Iterable[Mapping[str, Any]],
    observations: Iterable[Mapping[str, Any]],
    bindings: Iterable[Mapping[str, Any]],
    inputs: Iterable[Mapping[str, Any]],
    verifier_id: str,
    verifier_sha256: str,
    hmmm: Iterable[str],
) -> dict[str, Any]:
    definition_list = [validate_metric_definition(item) for item in definitions]
    definition_index = {
        (item["metric_id"], item["metric_version"]): item for item in definition_list
    }
    if len(definition_index) != len(definition_list):
        raise MetricProtocolError("receipt contains duplicate metric definitions")
    observation_list = []
    observed_definition_keys: set[tuple[str, str]] = set()
    for item in observations:
        record = _mapping(item, "receipt observation")
        key = (record.get("metric_id"), record.get("metric_version"))
        if key not in definition_index:
            raise MetricProtocolError(f"receipt observation has no matching definition: {key!r}")
        observation_list.append(validate_observation(record, definition_index[key]))
        observed_definition_keys.add(key)
    missing_observations = set(definition_index) - observed_definition_keys
    if missing_observations:
        raise MetricProtocolError(
            f"receipt definitions without observations: {sorted(missing_observations)!r}"
        )
    receipt: dict[str, Any] = {
        "schema": RECEIPT_SCHEMA,
        "version": RECEIPT_VERSION,
        "work_graph_sha256": work_graph_sha256,
        "definitions": definition_list,
        "observations": observation_list,
        "bindings": [dict(item) for item in bindings],
        "inputs": [dict(item) for item in inputs],
        "verification": {
            "verifier_id": verifier_id,
            "verifier_sha256": verifier_sha256,
            "result": "pending",
        },
        "hmmm": list(hmmm),
    }
    receipt["receipt_sha256"] = sha256_json(receipt)
    return verify_receipt(receipt)


def verify_receipt(value: Any) -> dict[str, Any]:
    record = _mapping(value, "metric receipt")
    _exact_fields(
        record,
        (
            "schema", "version", "work_graph_sha256", "definitions", "observations",
            "bindings", "inputs", "verification", "hmmm", "receipt_sha256",
        ),
        "metric receipt",
    )
    if (record["schema"], record["version"]) != (RECEIPT_SCHEMA, RECEIPT_VERSION):
        raise MetricProtocolError("unsupported metric receipt schema/version")
    _sha256(record["work_graph_sha256"], "receipt.work_graph_sha256")
    if not isinstance(record["definitions"], list) or not record["definitions"]:
        raise MetricProtocolError("receipt definitions must be a non-empty array")
    definitions = [validate_metric_definition(item) for item in record["definitions"]]
    definition_index = {(item["metric_id"], item["metric_version"]): item for item in definitions}
    if len(definition_index) != len(definitions):
        raise MetricProtocolError("receipt contains duplicate metric definitions")
    if not isinstance(record["observations"], list) or not record["observations"]:
        raise MetricProtocolError("receipt observations must be a non-empty array")
    observed_definition_keys: set[tuple[str, str]] = set()
    for item in record["observations"]:
        observation = _mapping(item, "receipt observation")
        key = (observation.get("metric_id"), observation.get("metric_version"))
        if key not in definition_index:
            raise MetricProtocolError(f"receipt observation has no matching definition: {key!r}")
        validate_observation(observation, definition_index[key])
        observed_definition_keys.add(key)
        if observation["provenance"]["work_graph_sha256"] != record["work_graph_sha256"]:
            raise MetricProtocolError("observation work-graph digest differs from receipt")
    missing_observations = set(definition_index) - observed_definition_keys
    if missing_observations:
        raise MetricProtocolError(
            f"receipt definitions without observations: {sorted(missing_observations)!r}"
        )
    if not isinstance(record["bindings"], list) or not record["bindings"]:
        raise MetricProtocolError("receipt bindings must be a non-empty array")
    for index, item in enumerate(record["bindings"]):
        _validate_binding(item, index)
    if not isinstance(record["inputs"], list) or not record["inputs"]:
        raise MetricProtocolError("receipt inputs must be a non-empty array")
    for index, item in enumerate(record["inputs"]):
        input_record = _mapping(item, f"receipt input[{index}]")
        _exact_fields(input_record, ("identity", "sha256"), f"receipt input[{index}]")
        _text(input_record["identity"], f"receipt input[{index}].identity")
        _sha256(input_record["sha256"], f"receipt input[{index}].sha256")
    verification = _mapping(record["verification"], "receipt verification")
    _exact_fields(verification, ("verifier_id", "verifier_sha256", "result"), "receipt verification")
    _text(verification["verifier_id"], "receipt verifier_id")
    _sha256(verification["verifier_sha256"], "receipt verifier_sha256")
    result = _text(verification["result"], "receipt verification result")
    if result not in REPLAY_RESULTS:
        raise MetricProtocolError(f"unsupported receipt verification result {result!r}")
    _string_list(record["hmmm"], "receipt hmmm")
    digest = _sha256(record["receipt_sha256"], "receipt.receipt_sha256")
    payload = {key: deepcopy(item) for key, item in record.items() if key != "receipt_sha256"}
    if digest != sha256_json(payload):
        raise MetricProtocolError("receipt digest mismatch")
    normalized = deepcopy(record)
    _reject_unsupported_scalars(normalized, "metric receipt")
    return normalized


__all__ = [
    "MetricProtocolError",
    "integer_value",
    "boolean_value",
    "canonical_json",
    "make_metric_definition",
    "make_observation",
    "measure_retention",
    "metric_definition_sha256",
    "rational_value",
    "retention_definitions",
    "seal_receipt",
    "seal_structure",
    "sha256_json",
    "validate_metric_definition",
    "validate_observation",
    "validate_structure",
    "verify_receipt",
]
