"""Strict semantic relation records for the METAPAT module catalog."""

# === MODULE_BUILD ===
# id: metapat_semantic_relations
#   module_name: metapat.relations
#   module_kind: schema
#   summary: defines strict digest-bound semantic relation records and bounded claim-status vocabulary for the canonical module catalog
#   owner: The Interdependency
#   public_surface: CLAIM_STATUSES, RELATION_KINDS, RELATION_SCHEMA_ID, RELATION_SCHEMA_VERSION, MetapatModuleRelation, build_relation
#   internal_surface: _canonical_json, _digest, _text, _strings
#   auth_boundary: none
#   storage_boundary: serialization-only
#   network_boundary: none
#   user_data_boundary: exact doctrine references and statements only
#   admin_only: false
#   tests: tests.test_relations
#   rollout: importable_package
#   rollback: remove relation exports and catalog relation records
#   requires: metapat_module_envelope
#   since: 2026-07-21
#   unresolved: formal proof objects remain outside relation records
# === END MODULE_BUILD ===

# === DOCS ===
# id: metapat_semantic_relations_docs
#   summary: documents relation vocabulary, evidence status, strict identity, and the prohibition on inferred constitutive containment
#   audience: developer, agent
#   source: docs/semantic-module-catalog.md
#   covers: MetapatModuleRelation, RELATION_KINDS, CLAIM_STATUSES
#   status: current
# === END DOCS ===

# === CAPABILITIES ===
# id: metapat_semantic_relation_records
#   summary: emits deterministic semantic ancestry records with exact source provenance and no inherited proof or measurement status
#   exposes: metapat.MetapatModuleRelation, metapat.build_relation
#   inputs: module endpoints, relation kind, evidence status, exact source references and statements, unresolved constraints
#   outputs: immutable relation record, deterministic JSON, relation digest
#   boundaries: auth:none, storage:serialization-only, network:none, user_data:canon text only
# === END CAPABILITIES ===

# === BOUNDARIES ===
# id: metapat_semantic_relation_boundary
#   summary: relation records declare semantic ancestry only; they do not prove ontology, measurement validity, UCNS topology, or constitutive containment
#   auth_boundary: none
#   storage_boundary: serialization-only
#   network_boundary: none
#   user_data_boundary: canon text and module identifiers only
#   admin_only: false
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: metapat_relation_vocabulary_bounded
#   given: semantic relation and claim-status vocabularies are inspected
#   then: only declared relation kinds and evidence statuses are accepted
#   class: schema_contract
#
# id: metapat_relation_roundtrip_strict
#   given: a valid semantic relation is serialized and reconstructed
#   then: every field and the deterministic digest survive while unknown, missing, or incorrectly typed fields fail closed
#   class: schema_contract
#
# id: metapat_relation_tamper_rejected
#   given: relation endpoints, source provenance, evidence status, or unresolved constraints change without digest rotation
#   then: reconstruction fails closed
#   class: safety
#
# id: metapat_relation_no_status_transfer
#   given: a semantic ancestry record is constructed
#   then: the record contains evidence classification but no theorem-transfer, measurement-value, ontology-validity, or topology-validity field
#   class: boundary_contract
# === END CONTRACTS ===
from __future__ import annotations
import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

RELATION_SCHEMA_ID = "metapat.semantic-relation"
RELATION_SCHEMA_VERSION = "1.0.0"
RELATION_KINDS = frozenset({
    "defines",
    "derived-from",
    "constrains",
    "organizes",
    "applies",
    "constitutive-simultaneous",
})
CLAIM_STATUSES = frozenset({
    "ROOT-STIPULATION",
    "DEFINITION",
    "WORKING-POSTULATE",
    "INTERNAL-DERIVATION",
    "IMPLEMENTED-CONTRACT",
    "CROSS-DOMAIN-HYPOTHESIS",
    "EMPIRICAL-FRONTIER",
    "RETRACTED_OR_SUPERSEDED",
})


def _canonical_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _strings(value: Any, name: str, *, minimum: int = 0) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{name} must be an array of strings")
    result = tuple(value)
    if len(result) < minimum:
        raise ValueError(f"{name} must contain at least {minimum} entries")
    if any(not isinstance(item, str) or not item.strip() for item in result):
        raise ValueError(f"{name} must contain only non-empty strings")
    return result


@dataclass(frozen=True, slots=True)
class MetapatModuleRelation:
    subject_module_id: str
    relation_kind: str
    object_module_id: str
    evidence_status: str
    source_statement_refs: tuple[str, ...]
    source_statements: tuple[str, ...]
    unresolved_constraints: tuple[str, ...] = ()
    schema_id: str = RELATION_SCHEMA_ID
    schema_version: str = RELATION_SCHEMA_VERSION
    relation_digest: str = ""

    def __post_init__(self) -> None:
        _text(self.subject_module_id, "subject_module_id")
        _text(self.object_module_id, "object_module_id")
        if self.subject_module_id == self.object_module_id:
            raise ValueError("semantic relation endpoints must differ")
        if self.relation_kind not in RELATION_KINDS:
            raise ValueError(f"unsupported relation_kind {self.relation_kind!r}")
        if self.evidence_status not in CLAIM_STATUSES:
            raise ValueError(f"unsupported evidence_status {self.evidence_status!r}")
        if self.schema_id != RELATION_SCHEMA_ID or self.schema_version != RELATION_SCHEMA_VERSION:
            raise ValueError("unsupported semantic relation schema")
        refs = _strings(self.source_statement_refs, "source_statement_refs", minimum=1)
        statements = _strings(self.source_statements, "source_statements", minimum=1)
        if len(refs) != len(statements):
            raise ValueError("source_statement_refs and source_statements must have equal length")
        unresolved = _strings(self.unresolved_constraints, "unresolved_constraints")
        object.__setattr__(self, "source_statement_refs", refs)
        object.__setattr__(self, "source_statements", statements)
        object.__setattr__(self, "unresolved_constraints", unresolved)
        expected = _digest(self._payload())
        if self.relation_digest and self.relation_digest != expected:
            raise ValueError("relation_digest mismatch")
        object.__setattr__(self, "relation_digest", expected)

    def _payload(self) -> dict[str, Any]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "subject_module_id": self.subject_module_id,
            "relation_kind": self.relation_kind,
            "object_module_id": self.object_module_id,
            "evidence_status": self.evidence_status,
            "source_statement_refs": list(self.source_statement_refs),
            "source_statements": list(self.source_statements),
            "unresolved_constraints": list(self.unresolved_constraints),
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "relation_digest": self.relation_digest}

    def to_json(self) -> str:
        return _canonical_json(self.to_dict())

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "MetapatModuleRelation":
        if not isinstance(data, Mapping):
            raise ValueError("semantic relation must be a mapping")
        expected = {
            "schema_id", "schema_version", "subject_module_id", "relation_kind",
            "object_module_id", "evidence_status", "source_statement_refs",
            "source_statements", "unresolved_constraints", "relation_digest",
        }
        unknown, missing = set(data) - expected, expected - set(data)
        if unknown:
            raise ValueError(f"unknown semantic relation fields: {sorted(unknown)!r}")
        if missing:
            raise ValueError(f"missing semantic relation fields: {sorted(missing)!r}")
        return cls(
            schema_id=_text(data["schema_id"], "schema_id"),
            schema_version=_text(data["schema_version"], "schema_version"),
            subject_module_id=_text(data["subject_module_id"], "subject_module_id"),
            relation_kind=_text(data["relation_kind"], "relation_kind"),
            object_module_id=_text(data["object_module_id"], "object_module_id"),
            evidence_status=_text(data["evidence_status"], "evidence_status"),
            source_statement_refs=_strings(data["source_statement_refs"], "source_statement_refs", minimum=1),
            source_statements=_strings(data["source_statements"], "source_statements", minimum=1),
            unresolved_constraints=_strings(data["unresolved_constraints"], "unresolved_constraints"),
            relation_digest=_text(data["relation_digest"], "relation_digest"),
        )

    @classmethod
    def from_json(cls, value: str) -> "MetapatModuleRelation":
        if not isinstance(value, str):
            raise ValueError("semantic relation JSON must be a string")
        decoded = json.loads(value)
        if not isinstance(decoded, dict):
            raise ValueError("semantic relation JSON must decode to an object")
        return cls.from_dict(decoded)


def build_relation(
    *,
    subject_module_id: str,
    relation_kind: str,
    object_module_id: str,
    evidence_status: str,
    source_statement_refs: Iterable[str],
    source_statements: Iterable[str],
    unresolved_constraints: Iterable[str] = (),
) -> MetapatModuleRelation:
    return MetapatModuleRelation(
        subject_module_id=subject_module_id,
        relation_kind=relation_kind,
        object_module_id=object_module_id,
        evidence_status=evidence_status,
        source_statement_refs=tuple(source_statement_refs),
        source_statements=tuple(source_statements),
        unresolved_constraints=tuple(unresolved_constraints),
    )

__all__ = [
    "CLAIM_STATUSES", "RELATION_KINDS", "RELATION_SCHEMA_ID", "RELATION_SCHEMA_VERSION",
    "MetapatModuleRelation", "build_relation",
]
