"""Strict catalog-bound application module records for METAPAT consumers."""

# === MODULE_BUILD ===
# id: metapat_application_module_schema
#   module_name: metapat.application
#   module_kind: schema
#   summary: defines strict application modules and catalog bindings that preserve source, claim status, evidence boundaries, and unresolved hmmm without promoting applications into canon or proof
#   owner: The Interdependency
#   public_surface: application schema constants, ApplicationCatalogBinding, MetapatApplicationModule, bind_catalog_module, validate_application_against_catalog, application_source_mismatches, assert_application_sources_match
#   internal_surface: canonical JSON, digest, strict scalar and sequence validators, Markdown source resolver
#   auth_boundary: none
#   storage_boundary: serialization-only and read-only source verification
#   network_boundary: none
#   user_data_boundary: application doctrine, domain statements, and source provenance only
#   admin_only: false
#   tests: tests.test_application
#   rollout: importable package schema and packaged application fixtures
#   rollback: remove application exports and fixtures while preserving canonical catalog
#   requires: metapat_semantic_catalog, metapat_semantic_relations
#   since: 2026-07-21
#   unresolved: application-specific empirical validation remains external to METAPAT
# === END MODULE_BUILD ===

# === DOCS ===
# id: metapat_application_module_docs
#   summary: documents catalog-bound application identity, source integrity, evidence firewalls, and downstream limits
#   audience: developer, agent, domain reviewer
#   source: docs/application-modules.md
#   covers: ApplicationCatalogBinding, MetapatApplicationModule, source checks, catalog validation
#   status: current
# === END DOCS ===

# === CAPABILITIES ===
# id: metapat_catalog_bound_application_modules
#   summary: binds application statements to exact catalog modules and preserves domain evidence boundaries without claim-status transfer
#   exposes: metapat.ApplicationCatalogBinding, metapat.MetapatApplicationModule, metapat.validate_application_against_catalog
#   inputs: catalog modules, application statements, domain scales, evidence requirements, source provenance, unresolved constraints
#   outputs: immutable application module, strict JSON, deterministic binding and application digests
#   boundaries: auth:none, storage:serialization-only, network:none, user_data:application text only
# === END CAPABILITIES ===

# === BOUNDARIES ===
# id: metapat_application_module_boundary
#   summary: application identity and semantic mapping only; no canon amendment, domain validation, EDCM measurement, formal proof, UCNS topology claim, or theorem-status transfer
#   auth_boundary: none
#   storage_boundary: serialization-only and read-only source verification
#   network_boundary: none
#   user_data_boundary: exact application statements and provenance only
#   admin_only: false
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: metapat_application_binding_exact
#   given: an application binds a catalog module
#   then: module id, module digest, module claim status, application role, and application statement are digest-bound
#   class: provenance_contract
#
# id: metapat_application_catalog_validation
#   given: an application is checked against a canonical catalog
#   then: catalog version and digest plus every bound module identity, digest, and claim status match exactly
#   class: integration_contract
#
# id: metapat_application_roundtrip_strict
#   given: a valid application module is serialized and reconstructed
#   then: every field and digest survive while unknown, missing, or incorrectly typed fields fail closed
#   class: schema_contract
#
# id: metapat_application_source_exact
#   given: application source references are resolved against repository Markdown
#   then: every heading exists and each exact source statement occurs within its declared section
#   class: provenance_contract
#
# id: metapat_application_status_firewall
#   given: an application module or binding is constructed
#   then: root impact and all ontology, domain, measurement, theorem-transfer, and topology claims remain false
#   class: boundary_contract
#
# id: metapat_application_tamper_rejected
#   given: application content, binding content, catalog identity, or evidence boundary changes without digest rotation
#   then: reconstruction fails closed
#   class: safety
# === END CONTRACTS ===

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .catalog import MetapatSemanticCatalog, SemanticCatalogModule

APPLICATION_SCHEMA_ID = "metapat.application-module"
APPLICATION_SCHEMA_VERSION = "1.0.0"
APPLICATION_BINDING_SCHEMA_ID = "metapat.application-catalog-binding"
APPLICATION_BINDING_SCHEMA_VERSION = "1.0.0"
APPLICATION_CLAIM_STATUSES = frozenset({"CROSS-DOMAIN-HYPOTHESIS", "EMPIRICAL-FRONTIER"})


def _canonical_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _boolean(value: Any, name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be boolean")
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


def _hex_digest(value: Any, name: str) -> str:
    text = _text(value, name).lower()
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        raise ValueError(f"{name} must be a lowercase hexadecimal SHA-256 digest")
    return text


@dataclass(frozen=True, slots=True)
class ApplicationCatalogBinding:
    module_id: str
    module_digest: str
    module_claim_status: str
    application_role: str
    application_statement: str
    schema_id: str = APPLICATION_BINDING_SCHEMA_ID
    schema_version: str = APPLICATION_BINDING_SCHEMA_VERSION
    binding_digest: str = ""

    def __post_init__(self) -> None:
        _text(self.module_id, "module_id")
        object.__setattr__(self, "module_digest", _hex_digest(self.module_digest, "module_digest"))
        _text(self.module_claim_status, "module_claim_status")
        _text(self.application_role, "application_role")
        _text(self.application_statement, "application_statement")
        if self.schema_id != APPLICATION_BINDING_SCHEMA_ID:
            raise ValueError(f"unsupported binding schema_id {self.schema_id!r}")
        if self.schema_version != APPLICATION_BINDING_SCHEMA_VERSION:
            raise ValueError(f"unsupported binding schema_version {self.schema_version!r}")
        expected = _digest(self._payload())
        if self.binding_digest and self.binding_digest != expected:
            raise ValueError("binding_digest mismatch")
        object.__setattr__(self, "binding_digest", expected)

    def _payload(self) -> dict[str, Any]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "module_id": self.module_id,
            "module_digest": self.module_digest,
            "module_claim_status": self.module_claim_status,
            "application_role": self.application_role,
            "application_statement": self.application_statement,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "binding_digest": self.binding_digest}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ApplicationCatalogBinding":
        if not isinstance(data, Mapping):
            raise ValueError("application catalog binding must be a mapping")
        expected = {
            "schema_id", "schema_version", "module_id", "module_digest",
            "module_claim_status", "application_role", "application_statement",
            "binding_digest",
        }
        unknown, missing = set(data) - expected, expected - set(data)
        if unknown:
            raise ValueError(f"unknown application binding fields: {sorted(unknown)!r}")
        if missing:
            raise ValueError(f"missing application binding fields: {sorted(missing)!r}")
        return cls(
            schema_id=_text(data["schema_id"], "schema_id"),
            schema_version=_text(data["schema_version"], "schema_version"),
            module_id=_text(data["module_id"], "module_id"),
            module_digest=_hex_digest(data["module_digest"], "module_digest"),
            module_claim_status=_text(data["module_claim_status"], "module_claim_status"),
            application_role=_text(data["application_role"], "application_role"),
            application_statement=_text(data["application_statement"], "application_statement"),
            binding_digest=_hex_digest(data["binding_digest"], "binding_digest"),
        )


def bind_catalog_module(
    module: SemanticCatalogModule,
    *,
    application_role: str,
    application_statement: str,
) -> ApplicationCatalogBinding:
    if not isinstance(module, SemanticCatalogModule):
        raise TypeError("module must be a SemanticCatalogModule")
    return ApplicationCatalogBinding(
        module_id=module.module_id,
        module_digest=module.module_digest,
        module_claim_status=module.claim_status,
        application_role=application_role,
        application_statement=application_statement,
    )


@dataclass(frozen=True, slots=True)
class MetapatApplicationModule:
    application_id: str
    application_version: str
    title: str
    claim_status: str
    domains: tuple[str, ...]
    selected_scales: tuple[str, ...]
    source_document: str
    source_statement_refs: tuple[str, ...]
    source_statements: tuple[str, ...]
    catalog_version: str
    catalog_digest: str
    catalog_bindings: tuple[ApplicationCatalogBinding, ...]
    domain_statements: tuple[str, ...]
    shared_question_form: tuple[str, ...]
    transfers: tuple[str, ...]
    does_not_transfer: tuple[str, ...]
    working_question: str
    evidence_boundary: str
    evidence_requirements: tuple[str, ...]
    unresolved_constraints: tuple[str, ...]
    root_impact: str = "none"
    metapat_validity_claim: bool = False
    domain_validity_claim: bool = False
    measurement_validity_claim: bool = False
    ucns_theorem_status_transfer: bool = False
    ucns_topology_claim: bool = False
    schema_id: str = APPLICATION_SCHEMA_ID
    schema_version: str = APPLICATION_SCHEMA_VERSION
    application_digest: str = ""

    def __post_init__(self) -> None:
        _text(self.application_id, "application_id")
        _text(self.application_version, "application_version")
        _text(self.title, "title")
        if self.claim_status not in APPLICATION_CLAIM_STATUSES:
            raise ValueError(f"unsupported application claim_status {self.claim_status!r}")
        domains = _strings(self.domains, "domains", minimum=1)
        scales = _strings(self.selected_scales, "selected_scales", minimum=1)
        _text(self.source_document, "source_document")
        refs = _strings(self.source_statement_refs, "source_statement_refs", minimum=1)
        statements = _strings(self.source_statements, "source_statements", minimum=1)
        if len(refs) != len(statements):
            raise ValueError("source_statement_refs and source_statements must have equal length")
        _text(self.catalog_version, "catalog_version")
        catalog_digest = _hex_digest(self.catalog_digest, "catalog_digest")
        bindings = tuple(self.catalog_bindings)
        if not bindings or any(not isinstance(item, ApplicationCatalogBinding) for item in bindings):
            raise ValueError("catalog_bindings must contain ApplicationCatalogBinding values")
        if len({binding.module_id for binding in bindings}) != len(bindings):
            raise ValueError("catalog binding module ids must be unique")
        domain_statements = _strings(self.domain_statements, "domain_statements", minimum=1)
        question_form = _strings(self.shared_question_form, "shared_question_form", minimum=1)
        transfers = _strings(self.transfers, "transfers", minimum=1)
        does_not_transfer = _strings(self.does_not_transfer, "does_not_transfer", minimum=1)
        _text(self.working_question, "working_question")
        _text(self.evidence_boundary, "evidence_boundary")
        evidence_requirements = _strings(self.evidence_requirements, "evidence_requirements", minimum=1)
        unresolved = _strings(self.unresolved_constraints, "unresolved_constraints", minimum=1)
        if self.root_impact != "none":
            raise ValueError("root_impact must remain none")
        false_fields = {
            "metapat_validity_claim": self.metapat_validity_claim,
            "domain_validity_claim": self.domain_validity_claim,
            "measurement_validity_claim": self.measurement_validity_claim,
            "ucns_theorem_status_transfer": self.ucns_theorem_status_transfer,
            "ucns_topology_claim": self.ucns_topology_claim,
        }
        for name, value in false_fields.items():
            if _boolean(value, name) is not False:
                raise ValueError(f"{name} must remain false")
        if self.schema_id != APPLICATION_SCHEMA_ID or self.schema_version != APPLICATION_SCHEMA_VERSION:
            raise ValueError("unsupported application module schema")
        object.__setattr__(self, "domains", domains)
        object.__setattr__(self, "selected_scales", scales)
        object.__setattr__(self, "source_statement_refs", refs)
        object.__setattr__(self, "source_statements", statements)
        object.__setattr__(self, "catalog_digest", catalog_digest)
        object.__setattr__(self, "catalog_bindings", bindings)
        object.__setattr__(self, "domain_statements", domain_statements)
        object.__setattr__(self, "shared_question_form", question_form)
        object.__setattr__(self, "transfers", transfers)
        object.__setattr__(self, "does_not_transfer", does_not_transfer)
        object.__setattr__(self, "evidence_requirements", evidence_requirements)
        object.__setattr__(self, "unresolved_constraints", unresolved)
        expected = _digest(self._payload())
        if self.application_digest and self.application_digest != expected:
            raise ValueError("application_digest mismatch")
        object.__setattr__(self, "application_digest", expected)

    def _payload(self) -> dict[str, Any]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "application_id": self.application_id,
            "application_version": self.application_version,
            "title": self.title,
            "claim_status": self.claim_status,
            "domains": list(self.domains),
            "selected_scales": list(self.selected_scales),
            "source_document": self.source_document,
            "source_statement_refs": list(self.source_statement_refs),
            "source_statements": list(self.source_statements),
            "catalog_version": self.catalog_version,
            "catalog_digest": self.catalog_digest,
            "catalog_bindings": [binding.to_dict() for binding in self.catalog_bindings],
            "domain_statements": list(self.domain_statements),
            "shared_question_form": list(self.shared_question_form),
            "transfers": list(self.transfers),
            "does_not_transfer": list(self.does_not_transfer),
            "working_question": self.working_question,
            "evidence_boundary": self.evidence_boundary,
            "evidence_requirements": list(self.evidence_requirements),
            "unresolved_constraints": list(self.unresolved_constraints),
            "root_impact": self.root_impact,
            "metapat_validity_claim": self.metapat_validity_claim,
            "domain_validity_claim": self.domain_validity_claim,
            "measurement_validity_claim": self.measurement_validity_claim,
            "ucns_theorem_status_transfer": self.ucns_theorem_status_transfer,
            "ucns_topology_claim": self.ucns_topology_claim,
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "application_digest": self.application_digest}

    def to_json(self) -> str:
        return _canonical_json(self.to_dict())

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "MetapatApplicationModule":
        if not isinstance(data, Mapping):
            raise ValueError("application module must be a mapping")
        expected = {
            "schema_id", "schema_version", "application_id", "application_version", "title",
            "claim_status", "domains", "selected_scales", "source_document",
            "source_statement_refs", "source_statements", "catalog_version", "catalog_digest",
            "catalog_bindings", "domain_statements", "shared_question_form", "transfers",
            "does_not_transfer", "working_question", "evidence_boundary", "evidence_requirements",
            "unresolved_constraints", "root_impact", "metapat_validity_claim",
            "domain_validity_claim", "measurement_validity_claim",
            "ucns_theorem_status_transfer", "ucns_topology_claim", "application_digest",
        }
        unknown, missing = set(data) - expected, expected - set(data)
        if unknown:
            raise ValueError(f"unknown application fields: {sorted(unknown)!r}")
        if missing:
            raise ValueError(f"missing application fields: {sorted(missing)!r}")
        if not isinstance(data["catalog_bindings"], (list, tuple)):
            raise ValueError("catalog_bindings must be an array")
        return cls(
            schema_id=_text(data["schema_id"], "schema_id"),
            schema_version=_text(data["schema_version"], "schema_version"),
            application_id=_text(data["application_id"], "application_id"),
            application_version=_text(data["application_version"], "application_version"),
            title=_text(data["title"], "title"),
            claim_status=_text(data["claim_status"], "claim_status"),
            domains=_strings(data["domains"], "domains", minimum=1),
            selected_scales=_strings(data["selected_scales"], "selected_scales", minimum=1),
            source_document=_text(data["source_document"], "source_document"),
            source_statement_refs=_strings(data["source_statement_refs"], "source_statement_refs", minimum=1),
            source_statements=_strings(data["source_statements"], "source_statements", minimum=1),
            catalog_version=_text(data["catalog_version"], "catalog_version"),
            catalog_digest=_hex_digest(data["catalog_digest"], "catalog_digest"),
            catalog_bindings=tuple(ApplicationCatalogBinding.from_dict(item) for item in data["catalog_bindings"]),
            domain_statements=_strings(data["domain_statements"], "domain_statements", minimum=1),
            shared_question_form=_strings(data["shared_question_form"], "shared_question_form", minimum=1),
            transfers=_strings(data["transfers"], "transfers", minimum=1),
            does_not_transfer=_strings(data["does_not_transfer"], "does_not_transfer", minimum=1),
            working_question=_text(data["working_question"], "working_question"),
            evidence_boundary=_text(data["evidence_boundary"], "evidence_boundary"),
            evidence_requirements=_strings(data["evidence_requirements"], "evidence_requirements", minimum=1),
            unresolved_constraints=_strings(data["unresolved_constraints"], "unresolved_constraints", minimum=1),
            root_impact=_text(data["root_impact"], "root_impact"),
            metapat_validity_claim=_boolean(data["metapat_validity_claim"], "metapat_validity_claim"),
            domain_validity_claim=_boolean(data["domain_validity_claim"], "domain_validity_claim"),
            measurement_validity_claim=_boolean(data["measurement_validity_claim"], "measurement_validity_claim"),
            ucns_theorem_status_transfer=_boolean(data["ucns_theorem_status_transfer"], "ucns_theorem_status_transfer"),
            ucns_topology_claim=_boolean(data["ucns_topology_claim"], "ucns_topology_claim"),
            application_digest=_hex_digest(data["application_digest"], "application_digest"),
        )

    @classmethod
    def from_json(cls, value: str) -> "MetapatApplicationModule":
        if not isinstance(value, str):
            raise ValueError("application module JSON must be a string")
        decoded = json.loads(value)
        if not isinstance(decoded, dict):
            raise ValueError("application module JSON must decode to an object")
        return cls.from_dict(decoded)


def validate_application_against_catalog(
    application: MetapatApplicationModule,
    catalog: MetapatSemanticCatalog,
) -> None:
    if not isinstance(application, MetapatApplicationModule):
        raise TypeError("application must be a MetapatApplicationModule")
    if not isinstance(catalog, MetapatSemanticCatalog):
        raise TypeError("catalog must be a MetapatSemanticCatalog")
    if application.catalog_version != catalog.catalog_version:
        raise ValueError("application catalog_version mismatch")
    if application.catalog_digest != catalog.catalog_digest:
        raise ValueError("application catalog_digest mismatch")
    modules = {module.module_id: module for module in catalog.modules}
    for binding in application.catalog_bindings:
        module = modules.get(binding.module_id)
        if module is None:
            raise ValueError(f"unknown bound catalog module {binding.module_id!r}")
        if binding.module_digest != module.module_digest:
            raise ValueError(f"module digest mismatch for {binding.module_id}")
        if binding.module_claim_status != module.claim_status:
            raise ValueError(f"module claim-status mismatch for {binding.module_id}")


def _slug(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    return re.sub(r"[\s-]+", "-", value).strip("-")


def _section(lines: list[str], anchor: str) -> list[str] | None:
    for index, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not match or _slug(match.group(2)) != anchor:
            continue
        level = len(match.group(1))
        end = len(lines)
        for cursor in range(index + 1, len(lines)):
            later = re.match(r"^(#{1,6})\s+", lines[cursor])
            if later and len(later.group(1)) <= level:
                end = cursor
                break
        return lines[index + 1 : end]
    return None


def application_source_mismatches(
    root: Path,
    application: MetapatApplicationModule,
) -> tuple[str, ...]:
    path = root / application.source_document
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return (f"missing application source: {application.source_document}",)
    mismatches: list[str] = []
    for ref, statement in zip(
        application.source_statement_refs,
        application.source_statements,
        strict=True,
    ):
        try:
            file_and_anchor, _label = ref.split("::", 1)
            file_name, anchor = file_and_anchor.split("#", 1)
        except ValueError:
            mismatches.append(f"invalid source reference: {ref}")
            continue
        if file_name != application.source_document:
            mismatches.append(f"source document mismatch: {ref}")
            continue
        section = _section(lines, anchor)
        if section is None:
            mismatches.append(f"missing source heading: {file_name}#{anchor}")
            continue
        if statement not in (line.strip() for line in section):
            mismatches.append(f"source statement mismatch: {ref}")
    return tuple(sorted(set(mismatches)))


def assert_application_sources_match(
    root: Path,
    application: MetapatApplicationModule,
) -> None:
    mismatches = application_source_mismatches(root, application)
    if mismatches:
        raise ValueError("application source mismatch: " + "; ".join(mismatches))


__all__ = [
    "APPLICATION_BINDING_SCHEMA_ID",
    "APPLICATION_BINDING_SCHEMA_VERSION",
    "APPLICATION_CLAIM_STATUSES",
    "APPLICATION_SCHEMA_ID",
    "APPLICATION_SCHEMA_VERSION",
    "ApplicationCatalogBinding",
    "MetapatApplicationModule",
    "application_source_mismatches",
    "assert_application_sources_match",
    "bind_catalog_module",
    "validate_application_against_catalog",
]
