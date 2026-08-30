"""Versioned immutable semantic-authority envelopes for METAPAT consumers.

Serialization is deterministic and strict. Deserialization rejects unknown,
missing, or incorrectly typed fields rather than coercing malformed values.
"""

# === MODULE_BUILD ===
# id: metapat_module_envelope
#   module_name: metapat.envelope
#   module_kind: schema
#   summary: versioned immutable semantic-authority and provenance envelope for UCNS adapters and EDCM consumers
#   owner: The Interdependency
#   public_surface: MODULE_ENVELOPE_SCHEMA_ID, MODULE_ENVELOPE_SCHEMA_VERSION, MODULE_KINDS, MetapatModuleEnvelope, build_module_envelope, root_spine_module_envelope
#   internal_surface: _canonical_payload, _digest_payload, _tuple_of_strings, _require_string, _require_string_sequence
#   auth_boundary: none
#   storage_boundary: serialized envelope only; no persistence performed
#   network_boundary: none
#   user_data_boundary: caller-supplied statements and constraints are preserved exactly
#   admin_only: false
#   tests: tests.test_envelope, tests.test_catalog, tests.test_ucns_bridge, tests.test_packaging
#   rollout: importable_package
#   rollback: remove envelope exports and cross-repository adapter fixtures
#   requires: metapat_canon_core
#   since: 2026-07-12
#   unresolved: semantic mappings beyond external provenance and explicitly authorized constitutive-simultaneous forks remain unresolved
# === END MODULE_BUILD ===

# === DOCS ===
# id: metapat_module_envelope_docs
#   summary: defines the METAPAT-to-consumer semantic authority boundary
#   audience: developer, agent
#   source: codex-handoff/2026-07-12-stack-repair/REQUIRED_CHANGES.md
#   covers: MetapatModuleEnvelope, strict schema validation, provenance digest, canon identity, unresolved hmmm preservation
#   status: current
# === END DOCS ===

# === CAPABILITIES ===
# id: metapat_semantic_envelope
#   summary: emits deterministic immutable semantic constraints and provenance without calculated EDCM measurements
#   exposes: metapat.envelope.MetapatModuleEnvelope, metapat.envelope.root_spine_module_envelope
#   inputs: module identity, kind, exact source references and statements, constraints, permitted interpretations, unresolved constraints
#   outputs: immutable envelope, deterministic JSON, provenance digest
#   boundaries: auth:none, storage:serialization-only, network:none, user_data:caller-supplied exact text
# === END CAPABILITIES ===

# === BOUNDARIES ===
# id: metapat_module_envelope_boundary
#   summary: semantic authority and provenance only; no UCNS algebra, EDCM measurement, theorem transfer, or empirical validation
#   auth_boundary: none
#   storage_boundary: serialization-only
#   network_boundary: none
#   user_data_boundary: preserves caller-supplied text exactly
#   admin_only: false
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: metapat_envelope_exact_provenance
#   given: the canonical root-spine envelope is constructed
#   then: exact statements, references, constraints, permitted interpretations, canon identity, and unresolved hmmm are present
#   class: schema_contract
#
# id: metapat_envelope_roundtrip
#   given: a valid immutable module envelope including unresolved hmmm fields
#   then: deterministic JSON roundtrip preserves every field and digest
#   class: schema_contract
#
# id: metapat_envelope_rotation_visible
#   given: otherwise identical envelopes with different canon digest or semantic constraints
#   then: provenance digests differ
#   class: provenance_contract
#
# id: metapat_labels_not_measurements
#   given: a semantic envelope is constructed
#   then: no measured-values field or measurement-validity claim exists
#   class: boundary_contract
#
# id: metapat_envelope_tamper_rejected
#   given: serialized envelope content changes without a matching provenance digest
#   then: reconstruction fails closed
#   class: safety
#
# id: metapat_envelope_unknown_field_rejected
#   given: serialized envelope data contains an undeclared field
#   then: reconstruction fails closed
#   class: safety
#
# id: metapat_envelope_canonical_json
#   given: the same envelope is serialized repeatedly
#   then: JSON bytes remain canonical and deterministic
#   class: evidence
#
# id: metapat_envelope_type_strict
#   given: serialized envelope fields have incorrect scalar or sequence types
#   then: reconstruction rejects them rather than coercing them
#   class: safety
# === END CONTRACTS ===

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from .canon import CANON_VERSION, ROOT_SPINE, canon_digest

MODULE_ENVELOPE_SCHEMA_ID = "metapat.module-envelope"
MODULE_ENVELOPE_SCHEMA_VERSION = "1.2.0"
MODULE_KINDS = frozenset(
    {
        "canon-module",
        "distinction",
        "simplex",
        "boundary-simplex",
        "tensor",
        "energy-state",
        "scalar",
        "vector",
        "relation",
        "gradient",
        "transformation",
        "registration",
        "observer",
        "time",
        "question",
        "postulate",
        "theorem",
        "theory",
    }
)


def _tuple_of_strings(name: str, values: Iterable[str], *, allow_empty: bool = True) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise ValueError(f"{name} must be a sequence of strings, not a scalar string")
    try:
        result = tuple(values)
    except TypeError as exc:
        raise ValueError(f"{name} must be an iterable of strings") from exc
    if not allow_empty and not result:
        raise ValueError(f"{name} must not be empty")
    for index, value in enumerate(result):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name}[{index}] must be a non-empty string")
    return result


def _require_string(data: Mapping[str, Any], name: str) -> str:
    value = data[name]
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string")
    return value


def _require_string_sequence(data: Mapping[str, Any], name: str) -> tuple[str, ...]:
    value = data[name]
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{name} must be an array of strings")
    return _tuple_of_strings(name, value)


def _canonical_payload(data: Mapping[str, Any]) -> bytes:
    return json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest_payload(data: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_payload(data)).hexdigest()


@dataclass(frozen=True, slots=True)
class MetapatModuleEnvelope:
    """Immutable semantic-authority record for external adapters and consumers."""

    module_id: str
    module_kind: str
    source_statement_refs: tuple[str, ...]
    source_statements: tuple[str, ...]
    constraints: tuple[str, ...]
    permitted_interpretations: tuple[str, ...]
    unresolved_constraints: tuple[str, ...]
    canon_version: str = CANON_VERSION
    canon_digest: str = ""
    schema_id: str = MODULE_ENVELOPE_SCHEMA_ID
    schema_version: str = MODULE_ENVELOPE_SCHEMA_VERSION
    provenance_digest: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.module_id, str) or not self.module_id.strip():
            raise ValueError("module_id must be a non-empty string")
        if not isinstance(self.module_kind, str) or self.module_kind not in MODULE_KINDS:
            raise ValueError(
                f"unsupported module_kind {self.module_kind!r}; "
                f"expected one of {sorted(MODULE_KINDS)!r}"
            )
        if self.schema_id != MODULE_ENVELOPE_SCHEMA_ID:
            raise ValueError(f"unsupported schema_id {self.schema_id!r}")
        if self.schema_version != MODULE_ENVELOPE_SCHEMA_VERSION:
            raise ValueError(f"unsupported schema_version {self.schema_version!r}")
        if not isinstance(self.canon_version, str) or not self.canon_version.strip():
            raise ValueError("canon_version must be a non-empty string")

        refs = _tuple_of_strings("source_statement_refs", self.source_statement_refs, allow_empty=False)
        statements = _tuple_of_strings("source_statements", self.source_statements, allow_empty=False)
        if len(refs) != len(statements):
            raise ValueError("source_statement_refs and source_statements must have equal length")
        constraints = _tuple_of_strings("constraints", self.constraints)
        permitted = _tuple_of_strings("permitted_interpretations", self.permitted_interpretations)
        if not constraints and not permitted:
            raise ValueError("at least one constraint or permitted interpretation is required")
        unresolved = _tuple_of_strings("unresolved_constraints", self.unresolved_constraints)

        object.__setattr__(self, "source_statement_refs", refs)
        object.__setattr__(self, "source_statements", statements)
        object.__setattr__(self, "constraints", constraints)
        object.__setattr__(self, "permitted_interpretations", permitted)
        object.__setattr__(self, "unresolved_constraints", unresolved)

        digest = self.canon_digest or canon_digest()
        if not isinstance(digest, str):
            raise ValueError("canon_digest must be a string")
        if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest.lower()):
            raise ValueError("canon_digest must be a lowercase hexadecimal SHA-256 digest")
        object.__setattr__(self, "canon_digest", digest.lower())

        expected = _digest_payload(self._provenance_fields())
        if self.provenance_digest and self.provenance_digest != expected:
            raise ValueError("provenance_digest does not match envelope contents")
        object.__setattr__(self, "provenance_digest", expected)

    def _provenance_fields(self) -> dict[str, Any]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "module_id": self.module_id,
            "module_kind": self.module_kind,
            "canon_version": self.canon_version,
            "canon_digest": self.canon_digest,
            "source_statement_refs": list(self.source_statement_refs),
            "source_statements": list(self.source_statements),
            "constraints": list(self.constraints),
            "permitted_interpretations": list(self.permitted_interpretations),
            "unresolved_constraints": list(self.unresolved_constraints),
        }

    def to_dict(self) -> dict[str, Any]:
        data = self._provenance_fields()
        data["provenance_digest"] = self.provenance_digest
        return data

    def to_json(self) -> str:
        return _canonical_payload(self.to_dict()).decode("utf-8")

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "MetapatModuleEnvelope":
        if not isinstance(data, Mapping):
            raise ValueError("module envelope must be a mapping")
        expected_fields = {
            "schema_id",
            "schema_version",
            "module_id",
            "module_kind",
            "canon_version",
            "canon_digest",
            "source_statement_refs",
            "source_statements",
            "constraints",
            "permitted_interpretations",
            "unresolved_constraints",
            "provenance_digest",
        }
        unknown = set(data) - expected_fields
        missing = expected_fields - set(data)
        if unknown:
            raise ValueError(f"unknown envelope fields: {sorted(unknown)!r}")
        if missing:
            raise ValueError(f"missing envelope fields: {sorted(missing)!r}")
        return cls(
            schema_id=_require_string(data, "schema_id"),
            schema_version=_require_string(data, "schema_version"),
            module_id=_require_string(data, "module_id"),
            module_kind=_require_string(data, "module_kind"),
            canon_version=_require_string(data, "canon_version"),
            canon_digest=_require_string(data, "canon_digest"),
            source_statement_refs=_require_string_sequence(data, "source_statement_refs"),
            source_statements=_require_string_sequence(data, "source_statements"),
            constraints=_require_string_sequence(data, "constraints"),
            permitted_interpretations=_require_string_sequence(data, "permitted_interpretations"),
            unresolved_constraints=_require_string_sequence(data, "unresolved_constraints"),
            provenance_digest=_require_string(data, "provenance_digest"),
        )

    @classmethod
    def from_json(cls, value: str) -> "MetapatModuleEnvelope":
        if not isinstance(value, str):
            raise ValueError("module envelope JSON must be a string")
        decoded = json.loads(value)
        if not isinstance(decoded, dict):
            raise ValueError("module envelope JSON must decode to an object")
        return cls.from_dict(decoded)


def build_module_envelope(
    *,
    module_id: str,
    module_kind: str,
    source_statement_refs: Iterable[str],
    source_statements: Iterable[str],
    constraints: Iterable[str] = (),
    permitted_interpretations: Iterable[str] = (),
    unresolved_constraints: Iterable[str] = (),
    canon_version: str = CANON_VERSION,
    canon_identity: str | None = None,
) -> MetapatModuleEnvelope:
    return MetapatModuleEnvelope(
        module_id=module_id,
        module_kind=module_kind,
        source_statement_refs=tuple(source_statement_refs),
        source_statements=tuple(source_statements),
        constraints=tuple(constraints),
        permitted_interpretations=tuple(permitted_interpretations),
        unresolved_constraints=tuple(unresolved_constraints),
        canon_version=canon_version,
        canon_digest=canon_identity or canon_digest(),
    )


def root_spine_module_envelope() -> MetapatModuleEnvelope:
    refs = (
        "AXIOMS.md#1-legible-difference::statement-1",
        "AXIOMS.md#2-boundary::statement-1",
        "AXIOMS.md#3-simplex::statement-1",
        "AXIOMS.md#2-boundary::statement-2",
        "AXIOMS.md#3-simplex::statement-3",
    )
    return build_module_envelope(
        module_id="metapat.root_spine",
        module_kind="canon-module",
        source_statement_refs=refs,
        source_statements=ROOT_SPINE,
        constraints=(
            "Preserve source statement order and exact text.",
            "Do not let a consuming domain redefine METAPAT root terms.",
            "Do not treat semantic labels as calculated EDCM measurements.",
            "Do not transfer UCNS theorem status into METAPAT ontology claims.",
        ),
        permitted_interpretations=(
            "Use the statements as semantic authority and external provenance constraints.",
            "Bind adaptations and consumer epochs to canon_digest and provenance_digest.",
        ),
        unresolved_constraints=(
            "hmmm: semantic mappings beyond external provenance and explicitly authorized constitutive-simultaneous forks remain unresolved.",
        ),
    )


__all__ = [
    "MODULE_ENVELOPE_SCHEMA_ID",
    "MODULE_ENVELOPE_SCHEMA_VERSION",
    "MODULE_KINDS",
    "MetapatModuleEnvelope",
    "build_module_envelope",
    "root_spine_module_envelope",
]
