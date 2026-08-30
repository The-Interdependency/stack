"""Checks for the catalog-bound affixiation and harmonic-relation application."""

# === CHECKS ===
# id: check_affixiation_harmonics_catalog_bound
#   proves: metapat_affixiation_harmonics_catalog_bound
#   call: self::test_application_bindings_match_catalog
#   mutates: none
#   cleanup: none
#
# id: check_affixiation_identity_preserved
#   proves: metapat_affixiation_identity_preserved
#   call: self::test_affixiation_preserves_identity_without_selecting_topology
#   mutates: none
#   cleanup: none
#
# id: check_harmonics_time_agnostic
#   proves: metapat_harmonics_time_agnostic
#   call: self::test_harmonic_semantics_do_not_require_time
#   mutates: none
#   cleanup: none
#
# id: check_affixiation_harmonics_authority_firewall
#   proves: metapat_affixiation_harmonics_authority_firewall
#   call: self::test_authority_firewall_is_explicit
#   mutates: none
#   cleanup: none
#
# id: check_affixiation_harmonics_candidate_status
#   proves: metapat_affixiation_harmonics_candidate_status
#   call: self::test_application_remains_unpromoted
#   mutates: none
#   cleanup: none
#
# id: check_affixiation_harmonics_source_current
#   proves: metapat_affixiation_harmonics_source_current
#   call: self::test_application_source_is_current
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from pathlib import Path

import metapat
from metapat.affixiation_harmonics import (
    AFFIXIATION_HARMONICS_BINDING_SPECS,
    affixiation_harmonics_application_module,
)


def test_application_bindings_match_catalog() -> None:
    catalog = metapat.canonical_semantic_catalog()
    application = affixiation_harmonics_application_module(catalog)
    metapat.validate_application_against_catalog(application, catalog)
    assert len(application.catalog_bindings) == len(AFFIXIATION_HARMONICS_BINDING_SPECS) == 13
    assert len({binding.module_id for binding in application.catalog_bindings}) == 13
    assert all(len(binding.module_digest) == 64 for binding in application.catalog_bindings)


def test_affixiation_preserves_identity_without_selecting_topology() -> None:
    application = affixiation_harmonics_application_module()
    assert any("remain individually addressable" in item for item in application.domain_statements)
    assert any("identities and provenance" in item for item in application.domain_statements)
    assert any("does not by itself select a UCNS carrier" in item for item in application.does_not_transfer)
    assert application.ucns_topology_claim is False


def test_harmonic_semantics_do_not_require_time() -> None:
    application = affixiation_harmonics_application_module()
    assert any("ordered parameter other than time" in item for item in application.transfers)
    assert any("does not imply a physical frequency" in item for item in application.does_not_transfer)
    assert any(binding.application_role == "time-boundary" for binding in application.catalog_bindings)
    assert any(binding.application_role == "time-separation" for binding in application.catalog_bindings)


def test_authority_firewall_is_explicit() -> None:
    application = affixiation_harmonics_application_module()
    assert "UCNS owns any exact representation or executable construction" in application.evidence_boundary
    assert "EDCM owns any explicit measurement projection" in application.evidence_boundary
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


def test_application_remains_unpromoted() -> None:
    application = affixiation_harmonics_application_module()
    assert application.claim_status == "CROSS-DOMAIN-HYPOTHESIS"
    assert application.root_impact == "none"
    assert application.catalog_version == metapat.CATALOG_VERSION
    assert any("promoted from application terminology" in item for item in application.unresolved_constraints)
    assert application.to_json() == affixiation_harmonics_application_module().to_json()


def test_application_source_is_current() -> None:
    application = affixiation_harmonics_application_module()
    metapat.assert_application_sources_match(Path(__file__).resolve().parents[1], application)
    assert len(application.unresolved_constraints) == 3
    assert all(item.startswith("hmmm:") for item in application.unresolved_constraints)
