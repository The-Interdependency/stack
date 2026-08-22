"""Checks for strict catalog-bound METAPAT application modules."""

# === CHECKS ===
# id: check_application_binding_exact
#   proves: metapat_application_binding_exact
#   call: self::test_application_binding_is_exact_and_digest_bound
#   mutates: none
#   cleanup: none
#
# id: check_application_catalog_validation
#   proves: metapat_application_catalog_validation
#   call: self::test_application_validates_against_exact_catalog
#   mutates: none
#   cleanup: none
#
# id: check_application_roundtrip_strict
#   proves: metapat_application_roundtrip_strict
#   call: self::test_application_roundtrip_and_types_are_strict
#   mutates: none
#   cleanup: none
#
# id: check_application_source_exact
#   proves: metapat_application_source_exact
#   call: self::test_application_source_statements_match
#   mutates: none
#   cleanup: none
#
# id: check_application_status_firewall
#   proves: metapat_application_status_firewall
#   call: self::test_application_status_firewall_is_explicit
#   mutates: none
#   cleanup: none
#
# id: check_application_tamper_rejected
#   proves: metapat_application_tamper_rejected
#   call: self::test_application_and_binding_tamper_are_rejected
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from dataclasses import replace
from pathlib import Path

import pytest

import metapat
from metapat.application import ApplicationCatalogBinding, MetapatApplicationModule


def test_application_binding_is_exact_and_digest_bound() -> None:
    application = metapat.quantum_magnetism_application_module()
    binding = application.catalog_bindings[0]
    assert binding.module_id == "metapat.axiom.0.root_untouchable"
    assert len(binding.module_digest) == 64
    assert len(binding.binding_digest) == 64
    data = binding.to_dict()
    data["application_statement"] = "changed"
    with pytest.raises(ValueError, match="binding_digest"):
        ApplicationCatalogBinding.from_dict(data)


def test_application_validates_against_exact_catalog() -> None:
    catalog = metapat.canonical_semantic_catalog()
    application = metapat.quantum_magnetism_application_module(catalog)
    metapat.validate_application_against_catalog(application, catalog)
    with pytest.raises(ValueError, match="catalog_digest"):
        metapat.validate_application_against_catalog(
            replace(application, catalog_digest="0" * 64, application_digest=""),
            catalog,
        )


def test_application_roundtrip_and_types_are_strict() -> None:
    application = metapat.quantum_magnetism_application_module()
    assert MetapatApplicationModule.from_json(application.to_json()) == application
    data = application.to_dict()
    data["extra"] = "no"
    with pytest.raises(ValueError, match="unknown"):
        MetapatApplicationModule.from_dict(data)
    data = application.to_dict()
    data["domains"] = "not-an-array"
    with pytest.raises(ValueError, match="array"):
        MetapatApplicationModule.from_dict(data)


def test_application_source_statements_match() -> None:
    application = metapat.quantum_magnetism_application_module()
    metapat.assert_application_sources_match(Path(__file__).resolve().parents[1], application)
    assert not metapat.application_source_mismatches(
        Path(__file__).resolve().parents[1],
        application,
    )


def test_application_status_firewall_is_explicit() -> None:
    application = metapat.quantum_magnetism_application_module()
    assert application.claim_status == "CROSS-DOMAIN-HYPOTHESIS"
    assert application.root_impact == "none"
    assert application.metapat_validity_claim is False
    assert application.domain_validity_claim is False
    assert application.measurement_validity_claim is False
    assert application.ucns_theorem_status_transfer is False
    assert application.ucns_topology_claim is False


def test_application_and_binding_tamper_are_rejected() -> None:
    application = metapat.quantum_magnetism_application_module()
    with pytest.raises(ValueError, match="application_digest"):
        replace(application, working_question="different")
    binding = application.catalog_bindings[0]
    with pytest.raises(ValueError, match="binding_digest"):
        replace(binding, module_digest="f" * 64)
