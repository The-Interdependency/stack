"""Executable evidence for exact UCNS receipt consumption."""

from copy import deepcopy

import pytest

from ptcna.ucns_integration import (
    UCNS_PRODUCER_COMMIT,
    UCNSIntegrationState,
    UCNSIntegrationSuspended,
    UCNSReceiptError,
    consume_ucns_receipt,
    load_bundled_ucns_receipt,
    require_ucns_integration,
    ucns_integration_status,
)

# === CHECKS ===
# id: check_ptcna_ucns_producer_validation
#   proves: ptcna_ucns_receipt_is_producer_validated
#   call: self::test_bundled_receipt_activates_exact_pinned_producer
#   requires: python3, numpy, ucns
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_ptcna_ucns_independent_state
#   proves: ptcna_ucns_state_is_independently_verified
#   call: self::test_materialized_state_identity_is_reported
#   requires: python3, numpy, ucns
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_ptcna_ucns_tamper_rejection
#   proves: ptcna_ucns_tampering_fails_closed
#   call: self::test_tampered_receipt_is_rejected
#   requires: python3, numpy, ucns
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_ptcna_ucns_shape_suspension
#   proves: ptcna_ucns_tampering_fails_closed
#   call: self::test_uncovered_shape_is_explicitly_suspended
#   requires: python3, numpy, ucns
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===


def test_bundled_receipt_activates_exact_pinned_producer() -> None:
    status = consume_ucns_receipt(load_bundled_ucns_receipt())
    assert status.state is UCNSIntegrationState.ACTIVE
    assert status.adapter_active is True
    assert status.producer_profile is not None
    assert status.producer_profile["commit"] == UCNS_PRODUCER_COMMIT
    assert status.producer_profile["candidate_id"] == "ucns-ptcna-157x7x7x53-v1"


def test_materialized_state_identity_is_reported() -> None:
    status = ucns_integration_status()
    assert status.state_shape == (157, 7, 7, 53)
    assert status.state_sha256 == (
        "e6247664fdcbc1fc6ac4bdc373258d6ba1c4f9d3d017e540627022ace3657c3a"
    )


def test_tampered_receipt_is_rejected() -> None:
    mutations = [
        ("producer", "commit", "0" * 40),
        ("state", "shape", [157, 7, 7, 52]),
        ("state", "sha256", "0" * 64),
        ("boundaries", "usefulness_established", True),
    ]
    for section, field, value in mutations:
        receipt = deepcopy(load_bundled_ucns_receipt())
        receipt[section][field] = value
        with pytest.raises(UCNSReceiptError, match="receipt rejected"):
            consume_ucns_receipt(receipt)


def test_uncovered_shape_is_explicitly_suspended() -> None:
    status = ucns_integration_status((1, 1, 1, 1))
    assert status.state is UCNSIntegrationState.SUSPENDED
    assert status.adapter_active is False
    with pytest.raises(UCNSIntegrationSuspended) as caught:
        require_ucns_integration((1, 1, 1, 1))
    assert caught.value.status == status
