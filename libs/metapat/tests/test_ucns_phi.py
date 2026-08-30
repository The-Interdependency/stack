"""Checks for METAPAT's explicit UCNS constitutive-fork authorization policy."""

from __future__ import annotations

# === CHECKS ===
# id: check_phi_default_external_provenance
#   proves: metapat_phi_default_external_provenance
#   call: self::test_default_policy_keeps_external_provenance_and_requires_authorization
#   mutates: none
#   cleanup: none
#
# id: check_phi_explicit_authorization
#   proves: metapat_phi_fork_requires_explicit_authorization
#   call: self::test_authorization_binds_parent_children_canon_policy_and_sources
#   mutates: none
#   cleanup: none
#
# id: check_phi_relation_exact
#   proves: metapat_phi_constitutive_relation_only
#   call: self::test_only_constitutive_simultaneous_relation_is_accepted
#   mutates: none
#   cleanup: none
#
# id: check_phi_canon_order_binding
#   proves: metapat_phi_authorization_binds_canon_and_order
#   call: self::test_validation_fails_on_child_order_and_rejects_parent_or_canon_tamper
#   mutates: none
#   cleanup: none
#
# id: check_phi_negative_relations
#   proves: metapat_phi_negative_relations_rejected
#   call: self::test_prohibited_relation_kinds_fail_closed
#   mutates: none
#   cleanup: none
#
# id: check_phi_roundtrip
#   proves: metapat_phi_record_roundtrip
#   call: self::test_authorization_roundtrip_is_strict_and_tamper_evident
#   mutates: none
#   cleanup: none
#
# id: check_phi_no_status_transfer
#   proves: metapat_phi_no_status_transfer
#   call: self::test_policy_and_authorization_never_transfer_status
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from dataclasses import replace

import pytest

from metapat import root_spine_module_envelope
from metapat.ucns_phi import (
    CONSTITUTIVE_RELATION_KIND,
    DEFAULT_UCNS_PHI_POLICY,
    PROHIBITED_FORK_RELATION_KINDS,
    ForkAuthorizationError,
    UCNSForkAuthorization,
    authorize_constitutive_fork,
    validate_fork_authorization,
)


def _authorization():
    envelope = root_spine_module_envelope()
    children = ("metapat.child.alpha", "metapat.child.beta")
    record = authorize_constitutive_fork(
        envelope,
        child_module_ids=children,
        source_statement_refs=(envelope.source_statement_refs[0],),
        unresolved_constraints=("hmmm: downstream payload location",),
    )
    return envelope, children, record


def test_default_policy_keeps_external_provenance_and_requires_authorization() -> None:
    policy = DEFAULT_UCNS_PHI_POLICY
    assert policy.default_semantic_mapping == "external-provenance"
    assert policy.fork_mode == "explicit-authorization-only"
    assert policy.allowed_relation_kind == CONSTITUTIVE_RELATION_KIND


def test_authorization_binds_parent_children_canon_policy_and_sources() -> None:
    envelope, children, record = _authorization()
    assert record.parent_module_id == envelope.module_id
    assert record.child_module_ids == children
    assert record.canon_digest == envelope.canon_digest
    assert record.encoding_policy_version == DEFAULT_UCNS_PHI_POLICY.schema_version
    assert record.source_statement_refs == (envelope.source_statement_refs[0],)
    assert record.authorization_digest


def test_only_constitutive_simultaneous_relation_is_accepted() -> None:
    _, _, record = _authorization()
    data = record.to_dict()
    data["relation_kind"] = "temporal-successor"
    with pytest.raises(ForkAuthorizationError, match="constitutive-simultaneous"):
        UCNSForkAuthorization.from_dict(data)


def test_validation_fails_on_child_order_and_rejects_parent_or_canon_tamper() -> None:
    envelope, children, record = _authorization()
    with pytest.raises(ForkAuthorizationError, match="child order"):
        validate_fork_authorization(
            record,
            envelope=envelope,
            child_module_ids=tuple(reversed(children)),
        )

    # Parent and canon identity are covered by the authorization digest itself.
    # Directly changing either field must fail before downstream validation can
    # accidentally treat a tampered record as a newly authorized fork.
    with pytest.raises(ForkAuthorizationError, match="authorization_digest mismatch"):
        replace(record, parent_module_id="metapat.other")
    with pytest.raises(ForkAuthorizationError, match="authorization_digest mismatch"):
        replace(record, canon_digest="different")


def test_prohibited_relation_kinds_fail_closed() -> None:
    _, _, record = _authorization()
    for relation_kind in PROHIBITED_FORK_RELATION_KINDS:
        data = record.to_dict()
        data["relation_kind"] = relation_kind
        with pytest.raises(ForkAuthorizationError):
            UCNSForkAuthorization.from_dict(data)


def test_authorization_roundtrip_is_strict_and_tamper_evident() -> None:
    _, _, record = _authorization()
    reconstructed = UCNSForkAuthorization.from_json(record.to_json())
    assert reconstructed == record
    assert reconstructed.to_json() == record.to_json()

    unknown = record.to_dict()
    unknown["extra"] = "no"
    with pytest.raises(ForkAuthorizationError, match="unknown"):
        UCNSForkAuthorization.from_dict(unknown)

    coerced = record.to_dict()
    coerced["child_module_ids"] = "not-an-array"
    with pytest.raises(ForkAuthorizationError, match="array"):
        UCNSForkAuthorization.from_dict(coerced)

    tampered = record.to_dict()
    tampered["source_statement_refs"] = ["different"]
    with pytest.raises(ForkAuthorizationError, match="digest"):
        UCNSForkAuthorization.from_dict(tampered)


def test_policy_and_authorization_never_transfer_status() -> None:
    _, _, record = _authorization()
    assert DEFAULT_UCNS_PHI_POLICY.theorem_status_transfer is False
    assert DEFAULT_UCNS_PHI_POLICY.metapat_validity_claim is False
    assert record.theorem_status_transfer is False
    assert record.metapat_validity_claim is False
