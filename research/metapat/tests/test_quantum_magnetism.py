"""Checks for the catalog-bound quantum-magnetism application vertical slice."""

# === CHECKS ===
# id: check_quantum_application_catalog_bound
#   proves: metapat_quantum_application_catalog_bound
#   call: self::test_quantum_application_bindings_match_catalog
#   mutates: none
#   cleanup: none
#
# id: check_quantum_application_status_preserved
#   proves: metapat_quantum_application_status_preserved
#   call: self::test_quantum_application_status_and_exclusions
#   mutates: none
#   cleanup: none
#
# id: check_quantum_application_scales_distinct
#   proves: metapat_quantum_application_scales_distinct
#   call: self::test_quantum_application_preserves_scale_distinctions
#   mutates: none
#   cleanup: none
#
# id: check_quantum_application_physics_firewall
#   proves: metapat_quantum_application_physics_firewall
#   call: self::test_quantum_application_preserves_physics_firewall
#   mutates: none
#   cleanup: none
#
# id: check_quantum_application_source_current
#   proves: metapat_quantum_application_source_current
#   call: self::test_quantum_application_source_is_current
#   mutates: none
#   cleanup: none
#
# id: check_quantum_fixture_generated
#   proves: metapat_quantum_fixture_generated
#   call: self::test_quantum_fixture_render_is_deterministic
#   mutates: none
#   cleanup: none
#
# id: check_quantum_fixture_current
#   proves: metapat_quantum_fixture_current
#   call: self::test_packaged_quantum_fixture_is_current
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from importlib.resources import files
from pathlib import Path

import metapat
from tools.generate_application_fixtures import render_quantum_magnetism_fixture


def test_quantum_application_bindings_match_catalog() -> None:
    catalog = metapat.canonical_semantic_catalog()
    application = metapat.quantum_magnetism_application_module(catalog)
    metapat.validate_application_against_catalog(application, catalog)
    assert len(application.catalog_bindings) == 12
    assert len({binding.module_id for binding in application.catalog_bindings}) == 12
    assert all(len(binding.module_digest) == 64 for binding in application.catalog_bindings)


def test_quantum_application_status_and_exclusions() -> None:
    application = metapat.quantum_magnetism_application_module()
    bound_ids = {binding.module_id for binding in application.catalog_bindings}
    assert application.claim_status == "CROSS-DOMAIN-HYPOTHESIS"
    assert application.root_impact == "none"
    assert "metapat.theory.10.symbolic_and_memetic_transfer" not in bound_ids
    assert "metapat.theory.11.cross_domain_question_forms" in bound_ids


def test_quantum_application_preserves_scale_distinctions() -> None:
    application = metapat.quantum_magnetism_application_module()
    assert application.selected_scales == (
        "nuclear",
        "atomic",
        "crystalline",
        "magnetic-domain",
    )
    assert any("one-to-one identity" in item for item in application.does_not_transfer)
    assert any("preserving their differences" in item for item in application.transfers)


def test_quantum_application_preserves_physics_firewall() -> None:
    application = metapat.quantum_magnetism_application_module()
    assert "answerable to atomic physics" in application.evidence_boundary
    assert len(application.evidence_requirements) == 4
    assert all(
        value is False
        for value in (
            application.metapat_validity_claim,
            application.domain_validity_claim,
            application.measurement_validity_claim,
            application.ucns_theorem_status_transfer,
            application.ucns_topology_claim,
        )
    )


def test_quantum_application_source_is_current() -> None:
    application = metapat.quantum_magnetism_application_module()
    metapat.assert_application_sources_match(Path(__file__).resolve().parents[1], application)
    assert application.unresolved_constraints[0].startswith("hmmm:")
    assert "Field-space" in application.unresolved_constraints[0]


def test_quantum_fixture_render_is_deterministic() -> None:
    rendered = render_quantum_magnetism_fixture()
    assert rendered.endswith("\n")
    assert rendered.count("\n") == 1
    assert rendered == render_quantum_magnetism_fixture()


def test_packaged_quantum_fixture_is_current() -> None:
    fixture = files("metapat").joinpath(
        "fixtures/quantum-magnetism-application-v2.json"
    )
    assert fixture.is_file()
    assert fixture.read_text(encoding="utf-8") == render_quantum_magnetism_fixture()
    assert not files("metapat").joinpath(
        "fixtures/quantum-magnetism-application-v1.json"
    ).is_file()
