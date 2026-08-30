# ratios: loc_comments=99:66 imports_exports=10:9 calls_definitions=19:10
"""Validate and materialize the exact UCNS PTCNA candidate-state receipt.

Usage::

    from ptcna.ucns_integration import ucns_integration_status

    status = ucns_integration_status()
    assert status.adapter_active
    assert status.state_shape == (157, 7, 7, 53)

The bundled receipt is a reviewed producer artifact, pinned to one UCNS merge.
Call :func:`consume_ucns_receipt` with decoded JSON to validate an externally
persisted copy. Validation delegates producer-schema authority to UCNS and then
independently verifies the dense state bytes PTCNA will use. A different shape
remains explicitly suspended and locally attributed.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from importlib.resources import files
import json
from typing import Any, Mapping

import numpy as np
from ucns.ptcna_state import validate_ptcna_state_receipt

# === MODULE_BUILD ===
# id: ptcna_ucns_integration
#   module_name: ucns_integration
#   module_kind: adapter
#   summary: consumes the exactly pinned UCNS 157x7x7x53 candidate receipt and independently verifies the target state bytes
#   owner: Erin Spencer
#   public_surface: UCNSIntegrationState, UCNSIntegrationStatus, UCNSReceiptError, consume_ucns_receipt, load_bundled_ucns_receipt, ucns_integration_status, require_ucns_integration
#   internal_surface: _receipt_status, _suspended_status
#   auth_boundary: none
#   storage_boundary: read bundled immutable receipt
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: ptcna/tests/test_ucns_integration.py
#   rollout: active only for the exact bundled producer receipt and matching state contract
#   rollback: restore typed suspension while retaining PTCNA-local composition and fallback
#   requires: ucns_ptcna_candidate_state
#   since: unreleased
#   unresolved: continuous seven-fold geometry, representative efficacy, and production privacy
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: ptcna_ucns_receipt_is_producer_validated
#   given: PTCNA consumes a UCNS candidate-state receipt
#   then: the exact pinned UCNS validator accepts every authority-bearing field before PTCNA materializes state
#   class: evidence
#
# id: ptcna_ucns_state_is_independently_verified
#   given: the producer receipt passes UCNS validation
#   then: PTCNA independently materializes C-order little-endian float64 positive-zero state and matches its shape, byte count, and digest
#   class: correctness
#
# id: ptcna_ucns_tampering_fails_closed
#   given: receipt content or expected state shape differs
#   then: consumption raises or returns an explicit suspended status without substituting PTCNA-local provenance
#   class: safety
# === END CONTRACTS ===

# === BOUNDARIES ===
# id: ptcna_ucns_integration_runtime_boundary
#   summary: validates a bundled immutable producer receipt and materializes deterministic in-memory state without network, authentication, user-data, or administrative effects
#   auth_boundary: none
#   storage_boundary: read bundled immutable receipt
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   pii: none
#   secrets: none
#   owner: Erin Spencer
#   since: unreleased
# === END BOUNDARIES ===

UCNS_PRODUCER_COMMIT = "b7b6f35cce69c273860923489a1c8b5372d14eb0"
UCNS_RECEIPT_SHA256 = "51aff240fb74d7183d2e004ebf0e7c65b4a613458b2ff0a83ba919eef8774b4a"
UCNS_STATE_SHAPE = (157, 7, 7, 53)
_RECEIPT_RESOURCE = "data/ucns-ptcna-state-v1.json"


class UCNSIntegrationState(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"


@dataclass(frozen=True)
class UCNSIntegrationStatus:
    state: UCNSIntegrationState
    adapter_active: bool
    reason: str
    required_scope: str
    producer_profile: Mapping[str, Any] | None
    rejected_legacy_surfaces: tuple[str, ...]
    state_shape: tuple[int, ...] | None = None
    state_sha256: str | None = None


class UCNSReceiptError(ValueError):
    """Raised before construction when producer or materialized state differs."""


class UCNSIntegrationSuspended(RuntimeError):
    def __init__(self, status: UCNSIntegrationStatus) -> None:
        self.status = status
        super().__init__(status.reason)


def load_bundled_ucns_receipt() -> dict[str, Any]:
    """Load the immutable receipt shipped in the PTCNA wheel."""

    return json.loads(files("ptcna").joinpath(_RECEIPT_RESOURCE).read_text("utf-8"))


def consume_ucns_receipt(receipt: Mapping[str, Any]) -> UCNSIntegrationStatus:
    """Producer-validate a receipt, then independently verify its state bytes."""

    try:
        validated = validate_ptcna_state_receipt(receipt)
    except (TypeError, ValueError) as exc:
        raise UCNSReceiptError(f"UCNS producer receipt rejected: {exc}") from exc
    producer = validated["producer"]
    if producer["commit"] != UCNS_PRODUCER_COMMIT:
        raise UCNSReceiptError("UCNS producer commit is not the pinned merge")
    if validated["receipt_sha256"] != UCNS_RECEIPT_SHA256:
        raise UCNSReceiptError("UCNS receipt identity is not the pinned artifact")
    state_contract = validated["state"]
    shape = tuple(state_contract["shape"])
    state = np.zeros(shape, dtype=np.dtype(state_contract["dtype"]), order="C")
    state_digest = sha256(state.tobytes(order="C")).hexdigest()
    if state.nbytes != state_contract["bytes"] or state_digest != state_contract["sha256"]:
        raise UCNSReceiptError("independent PTCNA state materialization disagrees")
    return UCNSIntegrationStatus(
        state=UCNSIntegrationState.ACTIVE,
        adapter_active=True,
        reason="exact UCNS candidate-state receipt validated",
        required_scope="PTCNA 157x7x7x53 initialization",
        producer_profile={
            "repository": producer["repository"],
            "commit": producer["commit"],
            "candidate_id": validated["candidate"]["id"],
            "receipt_sha256": validated["receipt_sha256"],
        },
        rejected_legacy_surfaces=(
            "ucns.a0_safe", "UCNSObject", "factor_search",
            "pre-reset serialization identity",
        ),
        state_shape=shape,
        state_sha256=state_digest,
    )


def _suspended_status(shape: tuple[int, ...]) -> UCNSIntegrationStatus:
    return UCNSIntegrationStatus(
        state=UCNSIntegrationState.SUSPENDED,
        adapter_active=False,
        reason=f"UCNS receipt covers {UCNS_STATE_SHAPE}, not requested {shape}",
        required_scope="PTCNA 157x7x7x53 initialization",
        producer_profile=None,
        rejected_legacy_surfaces=(
            "ucns.a0_safe", "UCNSObject", "factor_search",
            "pre-reset serialization identity",
        ),
    )


def ucns_integration_status(
    state_shape: tuple[int, ...] = UCNS_STATE_SHAPE,
) -> UCNSIntegrationStatus:
    """Return active status only for the exact producer-covered shape."""

    if tuple(state_shape) != UCNS_STATE_SHAPE:
        return _suspended_status(tuple(state_shape))
    return consume_ucns_receipt(load_bundled_ucns_receipt())


def require_ucns_integration(
    state_shape: tuple[int, ...] = UCNS_STATE_SHAPE,
) -> UCNSIntegrationStatus:
    """Return the validated status or raise a typed shape suspension."""

    status = ucns_integration_status(state_shape)
    if not status.adapter_active:
        raise UCNSIntegrationSuspended(status)
    return status


__all__ = [
    "UCNS_PRODUCER_COMMIT", "UCNS_RECEIPT_SHA256", "UCNS_STATE_SHAPE",
    "UCNSIntegrationState", "UCNSIntegrationStatus",
    "UCNSIntegrationSuspended", "UCNSReceiptError", "consume_ucns_receipt",
    "load_bundled_ucns_receipt", "ucns_integration_status",
    "require_ucns_integration",
]
# ratios: loc_comments=99:66 imports_exports=10:9 calls_definitions=19:10
