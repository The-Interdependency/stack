"""Canonical catalog construction, lookup, completeness, and source-integrity checks."""

# === MODULE_BUILD ===
# id: metapat_semantic_catalog_builder
#   module_name: metapat.catalog_build
#   module_kind: schema
#   summary: constructs the canonical semantic catalog from static declarations and verifies completeness and exact Markdown source resolution
#   owner: The Interdependency
#   public_surface: canonical_semantic_catalog, semantic_module_by_id, catalog_digest, catalog_module_counts, assert_catalog_complete, catalog_source_mismatches, assert_catalog_sources_match
#   internal_surface: _refs, _envelope, _slug, _section, _ANCHORS, _STATUS
#   auth_boundary: none
#   storage_boundary: read-only canon verification and serialization only
#   network_boundary: none
#   user_data_boundary: exact canon statements and references only
#   admin_only: false
#   tests: tests.test_catalog
#   rollout: importable package constructor and compliance gate
#   rollback: remove only with semantic catalog schema and fixture
#   requires: metapat_semantic_catalog, metapat_semantic_catalog_declarations, metapat_semantic_relations
#   since: 2026-07-21
#   unresolved: downstream application meaning and Phi topology binding remain separate
# === END MODULE_BUILD ===

from __future__ import annotations

import re
from pathlib import Path

from .catalog import (
    EXPECTED_MODULE_COUNT,
    EXPECTED_MODULE_COUNTS,
    MetapatSemanticCatalog,
    SemanticCatalogModule,
    _text,
)
from .catalog_data import CATALOG_DERIVATIONS, CATALOG_DERIVED_TEXT, CATALOG_SPECS
from .envelope import MetapatModuleEnvelope, build_module_envelope, root_spine_module_envelope
from .relations import MetapatModuleRelation, build_relation


def _refs(file_name: str, anchor: str, statements: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(
        f"{file_name}#{anchor}::statement-{index}"
        for index in range(1, len(statements) + 1)
    )


def _envelope(
    module_id: str,
    module_kind: str,
    file_name: str,
    anchor: str,
    statements: tuple[str, ...],
    doctrine_class: str,
    unresolved: tuple[str, ...] = (),
) -> MetapatModuleEnvelope:
    constraints = (
        "Preserve exact source text and source order.",
        "Do not inherit empirical, measurement, or theorem status from a consumer or geometric representation.",
    )
    permitted = (
        f"Use this {doctrine_class} module as addressable METAPAT semantic authority.",
        "Bind consumers to the module envelope provenance digest and catalog digest.",
    )
    if doctrine_class == "postulate":
        constraints += (
            "Treat this working commitment as revisable without allowing it to rewrite root axioms.",
        )
    if doctrine_class == "theory":
        constraints += (
            "Keep this application lens reducible to Chapter Zero and demotable if it causes domain capture.",
        )
    return build_module_envelope(
        module_id=module_id,
        module_kind=module_kind,
        source_statement_refs=_refs(file_name, anchor, statements),
        source_statements=statements,
        constraints=constraints,
        permitted_interpretations=permitted,
        unresolved_constraints=unresolved,
    )


_ANCHORS = {spec[0]: spec[5] for spec in CATALOG_SPECS}
_STATUS = {spec[0]: spec[3] for spec in CATALOG_SPECS}


def canonical_semantic_catalog() -> MetapatSemanticCatalog:
    modules = [
        SemanticCatalogModule(0, "root", "ROOT-STIPULATION", root_spine_module_envelope())
    ]
    for ordinal, spec in enumerate(CATALOG_SPECS, start=1):
        module_id, kind, doctrine_class, status, file_name, anchor, statements, unresolved = spec
        modules.append(
            SemanticCatalogModule(
                ordinal,
                doctrine_class,
                status,
                _envelope(
                    module_id,
                    kind,
                    file_name,
                    anchor,
                    statements,
                    doctrine_class,
                    unresolved,
                ),
            )
        )
    relations: list[MetapatModuleRelation] = []
    for subject, objects in CATALOG_DERIVATIONS.items():
        statement = CATALOG_DERIVED_TEXT[subject]
        ref = f"THEORIES.md#{_ANCHORS[subject]}::derived-from"
        evidence = _STATUS[subject]
        for object_id in objects:
            relations.append(
                build_relation(
                    subject_module_id=subject,
                    relation_kind="derived-from",
                    object_module_id=object_id,
                    evidence_status=evidence,
                    source_statement_refs=(ref,),
                    source_statements=(statement,),
                    unresolved_constraints=(
                        "hmmm: a derivation edge records declared semantic ancestry; it does not supply formal proof or empirical validation.",
                    ),
                )
            )
    return MetapatSemanticCatalog(tuple(modules), tuple(relations))


def semantic_module_by_id(
    module_id: str,
    catalog: MetapatSemanticCatalog | None = None,
) -> SemanticCatalogModule:
    target = _text(module_id, "module_id")
    selected = catalog or canonical_semantic_catalog()
    for module in selected.modules:
        if module.module_id == target:
            return module
    raise KeyError(target)


def catalog_digest() -> str:
    return canonical_semantic_catalog().catalog_digest


def catalog_module_counts(
    catalog: MetapatSemanticCatalog | None = None,
) -> dict[str, int]:
    selected = catalog or canonical_semantic_catalog()
    return {
        name: sum(module.doctrine_class == name for module in selected.modules)
        for name in EXPECTED_MODULE_COUNTS
    }


def assert_catalog_complete(catalog: MetapatSemanticCatalog | None = None) -> None:
    selected = catalog or canonical_semantic_catalog()
    observed = catalog_module_counts(selected)
    if observed != EXPECTED_MODULE_COUNTS or len(selected.modules) != EXPECTED_MODULE_COUNT:
        raise ValueError(
            f"semantic catalog incomplete: expected {EXPECTED_MODULE_COUNTS!r}, observed {observed!r}"
        )


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


def catalog_source_mismatches(
    root: Path,
    catalog: MetapatSemanticCatalog | None = None,
) -> tuple[str, ...]:
    selected = catalog or canonical_semantic_catalog()
    mismatches: list[str] = []
    records: list[tuple[tuple[str, ...], tuple[str, ...]]] = [
        (module.envelope.source_statement_refs, module.envelope.source_statements)
        for module in selected.modules
    ] + [
        (relation.source_statement_refs, relation.source_statements)
        for relation in selected.relations
    ]
    cache: dict[str, list[str] | None] = {}
    for refs, statements in records:
        for ref, statement in zip(refs, statements, strict=True):
            try:
                file_and_anchor, _label = ref.split("::", 1)
                file_name, anchor = file_and_anchor.split("#", 1)
            except ValueError:
                mismatches.append(f"invalid source reference: {ref}")
                continue
            if file_name not in cache:
                try:
                    cache[file_name] = (root / file_name).read_text(
                        encoding="utf-8"
                    ).splitlines()
                except OSError:
                    cache[file_name] = None
            lines = cache[file_name]
            if lines is None:
                mismatches.append(f"missing source file: {file_name}")
                continue
            section = _section(lines, anchor)
            if section is None:
                mismatches.append(f"missing source heading: {file_name}#{anchor}")
                continue
            if statement not in (line.strip() for line in section):
                mismatches.append(f"source statement mismatch: {ref}")
    return tuple(sorted(set(mismatches)))


def assert_catalog_sources_match(
    root: Path,
    catalog: MetapatSemanticCatalog | None = None,
) -> None:
    mismatches = catalog_source_mismatches(root, catalog)
    if mismatches:
        raise ValueError("semantic catalog source mismatch: " + "; ".join(mismatches))


__all__ = [
    "assert_catalog_complete",
    "assert_catalog_sources_match",
    "canonical_semantic_catalog",
    "catalog_digest",
    "catalog_module_counts",
    "catalog_source_mismatches",
    "semantic_module_by_id",
]
