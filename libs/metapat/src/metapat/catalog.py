"""Canonical addressable semantic module catalog for METAPAT doctrine."""

# === MODULE_BUILD ===
# id: metapat_semantic_catalog
#   module_name: metapat.catalog
#   module_kind: schema
#   summary: materializes the complete current METAPAT root, axiom, postulate, theorem, and theory surfaces as addressable provenance-bearing modules
#   owner: The Interdependency
#   public_surface: catalog constants, SemanticCatalogModule, MetapatSemanticCatalog, canonical_semantic_catalog, semantic_module_by_id, catalog_digest, catalog_module_counts, assert_catalog_complete, catalog_source_mismatches, assert_catalog_sources_match
#   internal_surface: _canonical_json, _digest, _text, _integer
#   auth_boundary: none
#   storage_boundary: read-only canon verification and serialization only
#   network_boundary: none
#   user_data_boundary: exact canon statements and references only
#   admin_only: false
#   tests: tests.test_catalog
#   rollout: importable_package and packaged semantic-module-catalog-v2 fixture
#   rollback: remove catalog exports and fixture while preserving envelope and canon surfaces
#   requires: metapat_canon_core, metapat_module_envelope, metapat_semantic_relations, metapat_semantic_catalog_builder
#   since: 2026-07-21
#   unresolved: downstream consumers must declare application meaning and any Phi topology binding separately
# === END MODULE_BUILD ===

# === DOCS ===
# id: metapat_semantic_catalog_docs
#   summary: documents catalog completeness, source resolution, claim classification, relation ancestry, and downstream limits
#   audience: developer, agent, consumer
#   source: docs/semantic-module-catalog.md
#   covers: canonical_semantic_catalog, SemanticCatalogModule, MetapatSemanticCatalog, source integrity, catalog fixture
#   status: current
# === END DOCS ===

# === CAPABILITIES ===
# id: metapat_addressable_semantic_catalog
#   summary: emits a deterministic complete catalog of current METAPAT doctrine and exact declared derivation edges
#   exposes: metapat.canonical_semantic_catalog, metapat.semantic_module_by_id, metapat.catalog_digest
#   inputs: byte-identified METAPAT canon and static catalog declarations
#   outputs: 40 ordered semantic modules, declared derivation relations, strict JSON, catalog digest
#   boundaries: auth:none, storage:serialization-only, network:none, user_data:canon text only
# === END CAPABILITIES ===

# === BOUNDARIES ===
# id: metapat_semantic_catalog_boundary
#   summary: catalog identity and semantic addressability only; no empirical state, EDCM value, formal proof, inferred UCNS containment, or consumer application meaning
#   auth_boundary: none
#   storage_boundary: read-only canon verification and serialization only
#   network_boundary: none
#   user_data_boundary: canon text and module identifiers only
#   admin_only: false
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: metapat_catalog_complete_ordered
#   given: the canonical semantic catalog is constructed
#   then: it contains exactly one root, twelve axioms, seven postulates, eight theorems, and twelve theories in contiguous deterministic order
#   class: canon_contract
#
# id: metapat_catalog_module_identity_unique
#   given: catalog modules are inspected
#   then: every module id, ordinal, envelope digest, and module digest is unique and deterministic
#   class: identity_contract
#
# id: metapat_catalog_roundtrip_strict
#   given: the complete catalog is serialized and reconstructed
#   then: all modules, relations, unresolved hmmm, and digests survive while malformed or unknown fields fail closed
#   class: schema_contract
#
# id: metapat_catalog_sources_exact
#   given: catalog references are resolved against repository canon files
#   then: every heading exists and every exact source statement occurs within its declared section
#   class: provenance_contract
#
# id: metapat_catalog_claim_status_bounded
#   given: doctrine classes and claim statuses are inspected
#   then: postulates remain working postulates, internal derivations remain internal, and the symbolic transfer theory remains a cross-domain hypothesis
#   class: boundary_contract
#
# id: metapat_catalog_relations_declared
#   given: catalog relation records are inspected
#   then: every endpoint exists and every relation is an exact source-backed declared derivation rather than inferred analogy
#   class: provenance_contract
#
# id: metapat_catalog_no_constitutive_inference
#   given: a catalog is constructed without a UCNS fork authorization
#   then: constitutive-simultaneous relations are rejected rather than inferred from ancestry, order, or geometry
#   class: safety
#
# id: metapat_catalog_rotation_visible
#   given: a module statement, claim status, relation, constraint, canon identity, or unresolved field changes
#   then: a module, relation, or catalog digest changes
#   class: provenance_contract
# === END CONTRACTS ===

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Mapping

from .canon import CANON_VERSION, canon_digest
from .envelope import MetapatModuleEnvelope
from .relations import CLAIM_STATUSES, MetapatModuleRelation

CATALOG_SCHEMA_ID = "metapat.semantic-catalog"
CATALOG_SCHEMA_VERSION = "1.0.0"
CATALOG_VERSION = "metapat-semantic-catalog-v2"
DOCTRINE_CLASSES = frozenset({"root", "axiom", "postulate", "theorem", "theory"})
EXPECTED_MODULE_COUNTS = {"root": 1, "axiom": 12, "postulate": 7, "theorem": 8, "theory": 12}
EXPECTED_MODULE_COUNT = sum(EXPECTED_MODULE_COUNTS.values())


def _canonical_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _digest(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _integer(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return value


@dataclass(frozen=True, slots=True)
class SemanticCatalogModule:
    ordinal: int
    doctrine_class: str
    claim_status: str
    envelope: MetapatModuleEnvelope
    module_digest: str = ""

    def __post_init__(self) -> None:
        _integer(self.ordinal, "ordinal")
        if self.doctrine_class not in DOCTRINE_CLASSES:
            raise ValueError(f"unsupported doctrine_class {self.doctrine_class!r}")
        if self.claim_status not in CLAIM_STATUSES:
            raise ValueError(f"unsupported claim_status {self.claim_status!r}")
        if not isinstance(self.envelope, MetapatModuleEnvelope):
            raise TypeError("envelope must be a MetapatModuleEnvelope")
        expected = _digest(self._payload())
        if self.module_digest and self.module_digest != expected:
            raise ValueError("module_digest mismatch")
        object.__setattr__(self, "module_digest", expected)

    @property
    def module_id(self) -> str:
        return self.envelope.module_id

    def _payload(self) -> dict[str, Any]:
        return {
            "ordinal": self.ordinal,
            "doctrine_class": self.doctrine_class,
            "claim_status": self.claim_status,
            "envelope": self.envelope.to_dict(),
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "module_digest": self.module_digest}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SemanticCatalogModule":
        if not isinstance(data, Mapping):
            raise ValueError("catalog module must be a mapping")
        expected = {"ordinal", "doctrine_class", "claim_status", "envelope", "module_digest"}
        unknown, missing = set(data) - expected, expected - set(data)
        if unknown:
            raise ValueError(f"unknown catalog module fields: {sorted(unknown)!r}")
        if missing:
            raise ValueError(f"missing catalog module fields: {sorted(missing)!r}")
        if not isinstance(data["envelope"], Mapping):
            raise ValueError("catalog module envelope must be a mapping")
        return cls(
            ordinal=_integer(data["ordinal"], "ordinal"),
            doctrine_class=_text(data["doctrine_class"], "doctrine_class"),
            claim_status=_text(data["claim_status"], "claim_status"),
            envelope=MetapatModuleEnvelope.from_dict(data["envelope"]),
            module_digest=_text(data["module_digest"], "module_digest"),
        )


@dataclass(frozen=True, slots=True)
class MetapatSemanticCatalog:
    modules: tuple[SemanticCatalogModule, ...]
    relations: tuple[MetapatModuleRelation, ...]
    canon_version: str = CANON_VERSION
    canon_digest: str = ""
    schema_id: str = CATALOG_SCHEMA_ID
    schema_version: str = CATALOG_SCHEMA_VERSION
    catalog_version: str = CATALOG_VERSION
    catalog_digest: str = ""

    def __post_init__(self) -> None:
        if self.schema_id != CATALOG_SCHEMA_ID or self.schema_version != CATALOG_SCHEMA_VERSION:
            raise ValueError("unsupported semantic catalog schema")
        if self.catalog_version != CATALOG_VERSION:
            raise ValueError("unsupported semantic catalog version")
        _text(self.canon_version, "canon_version")
        modules = tuple(self.modules)
        relations = tuple(self.relations)
        if any(not isinstance(item, SemanticCatalogModule) for item in modules):
            raise TypeError("modules must contain only SemanticCatalogModule values")
        if any(not isinstance(item, MetapatModuleRelation) for item in relations):
            raise TypeError("relations must contain only MetapatModuleRelation values")
        module_ids = [item.module_id for item in modules]
        ordinals = [item.ordinal for item in modules]
        if len(set(module_ids)) != len(module_ids):
            raise ValueError("catalog module ids must be unique")
        if ordinals != list(range(len(modules))):
            raise ValueError("catalog ordinals must be contiguous and ordered from zero")
        expected_canon = self.canon_digest or canon_digest()
        if any(item.envelope.canon_digest != expected_canon for item in modules):
            raise ValueError("every catalog module must bind the catalog canon digest")
        known = set(module_ids)
        for relation in relations:
            if relation.subject_module_id not in known or relation.object_module_id not in known:
                raise ValueError("catalog relation endpoint is not a catalog module")
            if relation.relation_kind == "constitutive-simultaneous":
                raise ValueError(
                    "catalog cannot infer constitutive-simultaneous meaning without UCNSForkAuthorization"
                )
        object.__setattr__(self, "modules", modules)
        object.__setattr__(self, "relations", relations)
        object.__setattr__(self, "canon_digest", expected_canon)
        expected = _digest(self._payload())
        if self.catalog_digest and self.catalog_digest != expected:
            raise ValueError("catalog_digest mismatch")
        object.__setattr__(self, "catalog_digest", expected)

    def _payload(self) -> dict[str, Any]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "catalog_version": self.catalog_version,
            "canon_version": self.canon_version,
            "canon_digest": self.canon_digest,
            "modules": [item.to_dict() for item in self.modules],
            "relations": [item.to_dict() for item in self.relations],
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "catalog_digest": self.catalog_digest}

    def to_json(self) -> str:
        return _canonical_json(self.to_dict())

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "MetapatSemanticCatalog":
        if not isinstance(data, Mapping):
            raise ValueError("semantic catalog must be a mapping")
        expected = {
            "schema_id",
            "schema_version",
            "catalog_version",
            "canon_version",
            "canon_digest",
            "modules",
            "relations",
            "catalog_digest",
        }
        unknown, missing = set(data) - expected, expected - set(data)
        if unknown:
            raise ValueError(f"unknown semantic catalog fields: {sorted(unknown)!r}")
        if missing:
            raise ValueError(f"missing semantic catalog fields: {sorted(missing)!r}")
        if not isinstance(data["modules"], (list, tuple)) or not isinstance(
            data["relations"], (list, tuple)
        ):
            raise ValueError("catalog modules and relations must be arrays")
        return cls(
            schema_id=_text(data["schema_id"], "schema_id"),
            schema_version=_text(data["schema_version"], "schema_version"),
            catalog_version=_text(data["catalog_version"], "catalog_version"),
            canon_version=_text(data["canon_version"], "canon_version"),
            canon_digest=_text(data["canon_digest"], "canon_digest"),
            modules=tuple(SemanticCatalogModule.from_dict(item) for item in data["modules"]),
            relations=tuple(MetapatModuleRelation.from_dict(item) for item in data["relations"]),
            catalog_digest=_text(data["catalog_digest"], "catalog_digest"),
        )

    @classmethod
    def from_json(cls, value: str) -> "MetapatSemanticCatalog":
        if not isinstance(value, str):
            raise ValueError("semantic catalog JSON must be a string")
        decoded = json.loads(value)
        if not isinstance(decoded, dict):
            raise ValueError("semantic catalog JSON must decode to an object")
        return cls.from_dict(decoded)


from .catalog_build import (
    assert_catalog_complete,
    assert_catalog_sources_match,
    canonical_semantic_catalog,
    catalog_digest,
    catalog_module_counts,
    catalog_source_mismatches,
    semantic_module_by_id,
)

__all__ = [
    "CATALOG_SCHEMA_ID",
    "CATALOG_SCHEMA_VERSION",
    "CATALOG_VERSION",
    "DOCTRINE_CLASSES",
    "EXPECTED_MODULE_COUNT",
    "EXPECTED_MODULE_COUNTS",
    "SemanticCatalogModule",
    "MetapatSemanticCatalog",
    "assert_catalog_complete",
    "assert_catalog_sources_match",
    "canonical_semantic_catalog",
    "catalog_digest",
    "catalog_module_counts",
    "catalog_source_mismatches",
    "semantic_module_by_id",
]
