# === MODULE_BUILD ===
# id: ucns_prime_replay_phase_milnor_receipt
#   module_name: prime_replay_phase_milnor_receipt
#   module_kind: experiment
#   summary: freezes the independent P7/P5 interval replay, phase-winding sensitivity, and length-three P7 Milnor audit while preserving the executable reference packet as the producing evidence
#   owner: Erin Spencer
#   public_surface: boundary_knot, validate_receipt, build_receipt
#   internal_surface: immutable base receipt validation and deterministic payload hashing
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_replay_phase_milnor_receipt.py
#   rollout: compact GitHub publication surface; selection effect none
#   rollback: remove this module, its test, documents, and generated summary
#   requires: ucns_prime_smooth_ribbons_p7_p5
#   since: 2026-08-11
#   unresolved: proof-assistant interval replay, analytic crossing extraction, length-four and higher Milnor invariants, multivariable Alexander polynomial, spectral operator, zeta correspondence
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: prime_replay_receipt_preserves_independent_interval_result
#   given: the compact receipt is loaded
#   then: P7 and P5 pair counts, box counts, margins, and independent Decimal ledger hashes remain pinned
#   class: evidence
#   since: 2026-08-11
#
# id: prime_replay_receipt_exposes_phase_imposition
#   given: P7 and P5 selected phase laws are compared
#   then: both use center winding three and therefore both produce T two-seven
#   class: doctrine
#   since: 2026-08-11
#
# id: prime_replay_receipt_freezes_p7_milnor_values
#   given: the five algebraically split outer triples are audited
#   then: each length-three mu-bar value is zero across the frozen projection, resolution, and basepoint sweeps
#   class: evidence
#   since: 2026-08-11
#
# id: prime_replay_receipt_is_nonselecting
#   given: the compact receipt is serialized
#   then: no phase law, arithmetic redefinition, electron ontology, zeta theorem, or Riemann-hypothesis proof is selected
#   class: doctrine
#   since: 2026-08-11
# === END CONTRACTS ===

"""Compact, deterministic receipt for the expanded P7 replay/phase/Milnor packet."""

from __future__ import annotations

import hashlib
import json

from copy import deepcopy
import hashlib
import json

from .prime_replay_phase_milnor_data import BASE_RECEIPT, SPLIT_TRIPLES

SCHEMA_ID = "ucns.prime-replay-phase-milnor.receipt"
SCHEMA_VERSION = "0.1.0"


def boundary_knot(center_winding: int) -> str:
    if isinstance(center_winding, bool) or not isinstance(center_winding, int):
        raise TypeError("center_winding must be an integer")
    return f"T(2,{1 + 2 * center_winding})"


def validate_receipt(payload: dict[str, object]) -> None:
    if payload["selection_effect"] != "none" or payload["research_order"] != [7, 5]:
        raise ValueError("authority or research-order boundary changed")
    replay = payload["independent_decimal_replay"]
    if replay["p7"]["boxes_evaluated"] != 6173 or replay["p5"]["boxes_evaluated"] != 4340:
        raise ValueError("independent replay partition changed")
    phase = payload["phase_sensitivity"]
    if not (phase["p7"]["center_boundary"] == phase["p5"]["center_boundary"] == "T(2,7)"):
        raise ValueError("phase sensitivity boundary changed")
    milnor = payload["p7_milnor_audit"]
    if milnor["mu_bar_123_values"] != [0, 0, 0, 0, 0] or len(milnor["triples"]) != 5:
        raise ValueError("P7 length-three Milnor receipt changed")


def build_receipt() -> dict[str, object]:
    payload = deepcopy(BASE_RECEIPT)
    validate_receipt(payload)
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    payload["payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload
