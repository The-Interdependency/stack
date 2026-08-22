"""Checks for the canonical METAPAT semantic module catalog."""

# === CHECKS ===
# id: check_catalog_complete_ordered
#   proves: metapat_catalog_complete_ordered
#   call: self::test_catalog_is_complete_and_ordered
#   mutates: none
#   cleanup: none
#
# id: check_catalog_identity_unique
#   proves: metapat_catalog_module_identity_unique
#   call: self::test_catalog_module_identity_is_unique
#   mutates: none
#   cleanup: none
#
# id: check_catalog_roundtrip_strict
#   proves: metapat_catalog_roundtrip_strict
#   call: self::test_catalog_roundtrip_is_strict
#   mutates: none
#   cleanup: none
#
# id: check_catalog_sources_exact
#   proves: metapat_catalog_sources_exact
#   call: self::test_catalog_sources_match_repository
#   mutates: none
#   cleanup: none
#
# id: check_catalog_claim_status_bounded
#   proves: metapat_catalog_claim_status_bounded
#   call: self::test_catalog_claim_statuses_remain_bounded
#   mutates: none
#   cleanup: none
#
# id: check_catalog_relations_declared
#   proves: metapat_catalog_relations_declared
#   call: self::test_catalog_relations_are_declared_and_resolvable
#   mutates: none
#   cleanup: none
#
# id: check_catalog_no_constitutive_inference
#   proves: metapat_catalog_no_constitutive_inference
#   call: self::test_catalog_rejects_unauthorized_constitutive_relation
#   mutates: none
#   cleanup: none
#
# id: check_catalog_rotation_visible
#   proves: metapat_catalog_rotation_visible
#   call: self::test_catalog_rotation_changes_identity
#   mutates: none
#   cleanup: none
#
# id: check_catalog_fixture_generated
#   proves: metapat_catalog_fixture_generated
#   call: self::test_catalog_fixture_render_is_deterministic
#   mutates: none
#   cleanup: none
#
# id: check_catalog_fixture_current
#   proves: metapat_catalog_fixture_current
#   call: self::test_packaged_catalog_fixture_is_current
#   mutates: none
#   cleanup: none
#
# id: check_root_envelope_fixture_generated
#   proves: metapat_root_envelope_fixture_generated
#   call: self::test_root_spine_fixture_render_is_deterministic
#   mutates: none
#   cleanup: none
#
# id: check_root_envelope_fixture_current
#   proves: metapat_root_envelope_fixture_current
#   call: self::test_packaged_root_spine_fixture_is_current
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from dataclasses import replace
from importlib.resources import files
from pathlib import Path

import pytest

import metapat
from metapat.catalog import (
    EXPECTED_MODULE_COUNTS,
    MetapatSemanticCatalog,
    assert_catalog_complete,
    canonical_semantic_catalog,
    catalog_module_counts,
    semantic_module_by_id,
)
from metapat.relations import build_relation
from tools.generate_catalog import render_catalog, render_root_spine_envelope


def test_catalog_is_complete_and_ordered() -> None:
    catalog = canonical_semantic_catalog()
    assert_catalog_complete(catalog)
    assert len(catalog.modules) == 40
    assert catalog_module_counts(catalog) == EXPECTED_MODULE_COUNTS
    assert [module.ordinal for module in catalog.modules] == list(range(40))


def test_catalog_module_identity_is_unique() -> None:
    catalog = canonical_semantic_catalog()
    assert len({module.module_id for module in catalog.modules}) == 40
    assert len({module.module_digest for module in catalog.modules}) == 40
    assert (
        semantic_module_by_id("metapat.axiom.4.tensor", catalog).envelope.module_kind
        == "tensor"
    )


def test_catalog_roundtrip_is_strict() -> None:
    catalog = canonical_semantic_catalog()
    assert MetapatSemanticCatalog.from_json(catalog.to_json()) == catalog
    data = catalog.to_dict()
    data["extra"] = "no"
    with pytest.raises(ValueError, match="unknown"):
        MetapatSemanticCatalog.from_dict(data)
    data = catalog.to_dict()
    data["modules"] = "not-an-array"
    with pytest.raises(ValueError, match="arrays"):
        MetapatSemanticCatalog.from_dict(data)


def test_catalog_sources_match_repository() -> None:
    metapat.assert_catalog_sources_match(Path(__file__).resolve().parents[1])


def test_catalog_claim_statuses_remain_bounded() -> None:
    catalog = canonical_semantic_catalog()
    assert {
        module.claim_status
        for module in catalog.modules
        if module.doctrine_class == "postulate"
    } == {"WORKING-POSTULATE"}
    assert (
        semantic_module_by_id(
            "metapat.theory.10.symbolic_and_memetic_transfer", catalog
        ).claim_status
        == "CROSS-DOMAIN-HYPOTHESIS"
    )
    assert all(
        module.claim_status == "INTERNAL-DERIVATION"
        for module in catalog.modules
        if module.doctrine_class == "theorem"
    )


def test_catalog_relations_are_declared_and_resolvable() -> None:
    catalog = canonical_semantic_catalog()
    module_ids = {module.module_id for module in catalog.modules}
    assert len(catalog.relations) == 52
    assert all(relation.relation_kind == "derived-from" for relation in catalog.relations)
    assert all(
        relation.subject_module_id in module_ids
        and relation.object_module_id in module_ids
        for relation in catalog.relations
    )
    assert all(
        relation.source_statements[0].startswith("Derived from:")
        for relation in catalog.relations
    )


def test_catalog_rejects_unauthorized_constitutive_relation() -> None:
    catalog = canonical_semantic_catalog()
    relation = build_relation(
        subject_module_id=catalog.modules[1].module_id,
        relation_kind="constitutive-simultaneous",
        object_module_id=catalog.modules[2].module_id,
        evidence_status="ROOT-STIPULATION",
        source_statement_refs=("AXIOMS.md#1-legible-difference::statement-1",),
        source_statements=("Legible difference is distinction.",),
    )
    with pytest.raises(ValueError, match="UCNSForkAuthorization"):
        MetapatSemanticCatalog(catalog.modules, catalog.relations + (relation,))


def test_catalog_rotation_changes_identity() -> None:
    catalog = canonical_semantic_catalog()
    module = catalog.modules[1]
    rotated_envelope = replace(
        module.envelope,
        constraints=module.envelope.constraints + ("new constraint",),
        provenance_digest="",
    )
    rotated_module = replace(module, envelope=rotated_envelope, module_digest="")
    modules = (catalog.modules[0], rotated_module, *catalog.modules[2:])
    rotated = MetapatSemanticCatalog(tuple(modules), catalog.relations)
    assert rotated_module.module_digest != module.module_digest
    assert rotated.catalog_digest != catalog.catalog_digest


def test_catalog_fixture_render_is_deterministic() -> None:
    rendered = render_catalog()
    assert rendered.endswith("\n") and rendered.count("\n") == 1
    assert rendered == render_catalog()


def test_root_spine_fixture_render_is_deterministic() -> None:
    rendered = render_root_spine_envelope()
    assert rendered.endswith("\n") and rendered.count("\n") == 1
    assert rendered == render_root_spine_envelope()


def test_packaged_root_spine_fixture_is_current() -> None:
    fixture = files("metapat").joinpath("fixtures/root-spine-envelope-v2.json")
    assert fixture.is_file()
    assert fixture.read_text(encoding="utf-8") == render_root_spine_envelope()


def test_packaged_catalog_fixture_is_current() -> None:
    fixture = files("metapat").joinpath("fixtures/semantic-module-catalog-v2.json")
    assert fixture.is_file()
    assert fixture.read_text(encoding="utf-8") == render_catalog()
    assert not files("metapat").joinpath("fixtures/semantic-module-catalog-v1.json").is_file()
