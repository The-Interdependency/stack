"""Asynchronous PCEA gonol key-state research candidate.

This module freezes the exact observation replay currently available for the
PCEA gonol-recursion handoff. It does not recover or claim the unresolved UCNS
recursive-scale geometry. The next value is derived by the named candidate
operator so it can be attacked and replaced when a stronger constructor is
found.
"""

# === MODULE_BUILD ===
# id: pcea_async_gonol_key_state
#   module_name: async_gonol_keys
#   module_kind: research
#   summary: observation-level gonol transition replay and lazy gonol-addressed key derivation candidate for asynchronous PCEA state
#   owner: The Interdependency
#   public_surface: OBSERVED_GONOL_SEQUENCE, OPERATOR_ID, GonolAddress, ReplayCache, recover_transition_operator, transition_at, replay_transition, derive_next_gonol, derive_state_digest, derive_lazy_key, comparison_matrix, freeze_document, write_freeze_document
#   internal_surface: _require_positive_int, _require_nonnegative_int, _require_digest, _normalize, _payload_digest
#   auth_boundary: stack/research/pcea owns this candidate; PCEA runtime, stack/libs/pcea, and UCNS canon are not changed
#   storage_boundary: in-memory receipts and optional research freeze JSON only
#   network_boundary: none
#   user_data_boundary: caller-supplied address/state/transcript digests remain caller-owned inputs
#   admin_only: false
#   tests: research/pcea/tests/test_async_gonol_keys.py
#   rollout: keep in stack/research/pcea until bounded behavior survives attack and promotion review
#   rollback: delete this module, tests, and generated freeze JSON; retain README narrative as negative evidence if needed
#   requires: ucns_public_gonol_geometry, pcea_stable_snapshot
#   since: 2026-08-31
#   unresolved: exact UCNS recursive-scale transition law producing the observed gonol progression; cryptographic review of any deployed key schedule
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: observed_gonol_transition_replays_handoff
#   given: the handoff observation 157 -> 2881 -> 54837698421
#   then: the frozen candidate operator independently replays those exact values
#   class: correctness
#   since: 2026-08-31
#
# id: candidate_next_gonol_is_derived_not_canon
#   given: the replayed observation and no recovered UCNS recursive-scale law
#   then: derive_next_gonol returns the next value under the named candidate operator and marks it as non-canonical research
#   class: doctrine
#   since: 2026-08-31
#
# id: lazy_key_derivation_binds_secret_and_address
#   given: a root secret and one gonol address/path/state/transcript coordinate
#   then: derive_lazy_key deterministically derives only the requested key and changes when any bound coordinate changes
#   class: construction
#   since: 2026-08-31
#
# id: address_replay_cache_rejects_coordinate_reuse
#   given: an asynchronous receiver tracks accepted gonol coordinates
#   then: the first use is accepted and repeated use of the same coordinate is rejected
#   class: security-control
#   since: 2026-08-31
#
# id: comparison_keeps_security_basis_external
#   given: the candidate is compared with ordinary ratchet and tree KDF schemes
#   then: no gonol size, geometry, or address-space property is counted as entropy or cryptographic hardness
#   class: doctrine
#   since: 2026-08-31
# === END CONTRACTS ===

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from hashlib import sha256
import hmac
import json
from pathlib import Path
from typing import Any


OPERATOR_ID = "pcea.async_gonol.observation_second_difference.v1"
KDF_PROTOCOL_LABEL = "pcea.async-gonol-key-state.v1"
FREEZE_SCHEMA = "pcea.async-gonol-key-state.freeze.v1"

OBSERVED_GONOL_SEQUENCE: tuple[int, ...] = (157, 2881, 54837698421)
DERIVED_NEXT_GONOL = 164513086777

PCEA_CLEANUP_COMMIT = "91ffa8c7249dfb810ca64a0bbc500481c0bd12a9"
STACK_REFRESH_COMMIT = "eaec7fd6ee4e829b6fae10a2c6d520b35857137d"
LEGACY_RESEARCH_SOURCE_COMMIT = "ecf2ca0dec38bef29382e02121b0edde66763aa9"
LEGACY_GONAL_ARCHITECTURE_BLOB = "a24e31110521b30ca941bf151b99458a06c910af"
PINNED_PUBLIC_GONOL_SHA256 = "55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5"

NONCLAIMS: tuple[str, ...] = (
    "not PCEA runtime behavior",
    "not stack/libs/pcea mutation",
    "not UCNS recursive-scale canon",
    "not a public-key construction",
    "not entropy from gonol size, geometry, or address space",
    "not cryptographic hardness evidence",
)

HMMM: tuple[str, ...] = (
    "exact UCNS recursive-scale transition law remains unresolved",
    "the observed sequence has no source-level transition operator in the current stack refresh or migrated PCEA research lane",
    "candidate key schedule needs attack review before any promotion",
)


class AsyncGonolError(ValueError):
    """Fail-closed error for malformed research inputs."""


class ReplayError(RuntimeError):
    """Raised when a gonol coordinate is reused."""


@dataclass(frozen=True, slots=True)
class GonolAddress:
    """One lazy derivation coordinate in the asynchronous candidate topology."""

    gonol_size: int
    recursive_path: tuple[int, ...]
    position: int
    epoch: int
    message_counter: int
    state_digest: str
    transcript_digest: str
    protocol_label: str = KDF_PROTOCOL_LABEL
    operator_id: str = OPERATOR_ID

    def __post_init__(self) -> None:
        _require_positive_int(self.gonol_size, "gonol_size")
        _require_nonnegative_int(self.position, "position")
        if self.position >= self.gonol_size:
            raise AsyncGonolError("position must be inside gonol_size")
        _require_nonnegative_int(self.epoch, "epoch")
        _require_nonnegative_int(self.message_counter, "message_counter")
        path = tuple(self.recursive_path)
        if not path:
            raise AsyncGonolError("recursive_path must not be empty")
        for index, value in enumerate(path):
            _require_positive_int(value, f"recursive_path[{index}]")
        object.__setattr__(self, "recursive_path", path)
        _require_digest(self.state_digest, "state_digest")
        _require_digest(self.transcript_digest, "transcript_digest")
        if not isinstance(self.protocol_label, str) or not self.protocol_label:
            raise AsyncGonolError("protocol_label must be non-empty text")
        if not isinstance(self.operator_id, str) or not self.operator_id:
            raise AsyncGonolError("operator_id must be non-empty text")

    def canonical(self) -> dict[str, Any]:
        """Return the canonical address payload consumed by the KDF."""

        return {
            "epoch": self.epoch,
            "gonol_size": self.gonol_size,
            "message_counter": self.message_counter,
            "operator_id": self.operator_id,
            "position": self.position,
            "protocol_label": self.protocol_label,
            "recursive_path": list(self.recursive_path),
            "state_digest": self.state_digest,
            "transcript_digest": self.transcript_digest,
        }


class ReplayCache:
    """Minimal coordinate-reuse guard for asynchronous delivery tests."""

    def __init__(self) -> None:
        self._seen: set[str] = set()

    @property
    def seen_count(self) -> int:
        return len(self._seen)

    def accept(self, address: GonolAddress) -> bool:
        coordinate = coordinate_id(address)
        if coordinate in self._seen:
            return False
        self._seen.add(coordinate)
        return True

    def require_fresh(self, address: GonolAddress) -> None:
        if not self.accept(address):
            raise ReplayError("gonol coordinate already accepted")


def _require_positive_int(value: int, field: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise AsyncGonolError(f"{field} must be a positive integer")


def _require_nonnegative_int(value: int, field: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise AsyncGonolError(f"{field} must be a non-negative integer")


def _require_digest(value: str, field: str) -> None:
    if not isinstance(value, str) or len(value) != 64:
        raise AsyncGonolError(f"{field} must be a sha256 hex digest")
    try:
        int(value, 16)
    except ValueError as exc:
        raise AsyncGonolError(f"{field} must be a sha256 hex digest") from exc


def _normalize(value: Any) -> Any:
    if hasattr(value, "canonical"):
        return _normalize(value.canonical())
    if isinstance(value, Mapping):
        return {str(key): _normalize(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, tuple):
        return [_normalize(item) for item in value]
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    raise TypeError(f"not canonically encodable: {type(value).__name__}")


def canonical_json_bytes(value: Any) -> bytes:
    """Encode a payload deterministically for receipts and HMAC input."""

    return json.dumps(
        _normalize(value),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _payload_digest(value: Any) -> str:
    return sha256(canonical_json_bytes(value)).hexdigest()


def derive_state_digest(state: Any) -> str:
    """Digest caller-owned state without interpreting it as entropy."""

    return _payload_digest({"state": state})


def recover_transition_operator(
    observed: Sequence[int] = OBSERVED_GONOL_SEQUENCE,
) -> dict[str, Any]:
    """Recover the exact transition operator available from current evidence.

    Current source evidence exposes only three observed values. The recovered
    operator is therefore the minimal constant-second-difference operator over
    observation index. It is sufficient to replay and falsify the handoff, but
    it is explicitly not the unresolved UCNS recursive-scale law.
    """

    values = tuple(observed)
    if len(values) < 3:
        raise AsyncGonolError("at least three observed gonol values are required")
    for index, value in enumerate(values):
        _require_positive_int(value, f"observed[{index}]")
    first_difference = values[1] - values[0]
    second_difference = values[2] - (2 * values[1]) + values[0]
    for index in range(2, len(values)):
        prior = values[index - 2]
        current = values[index - 1]
        following = values[index]
        if following - (2 * current) + prior != second_difference:
            raise AsyncGonolError("observed values do not share one second difference")
    return {
        "basis": "minimal constant-second-difference interpolation over observation index",
        "first_difference": first_difference,
        "formula": "y_i = y_0 + i*d_1 + (i*(i-1)//2)*d_2",
        "operator_id": OPERATOR_ID,
        "operator_standing": "candidate observation replay, not UCNS recursive-scale canon",
        "second_difference": second_difference,
        "source_values": list(values),
        "y_0": values[0],
    }


def transition_at(index: int, operator: Mapping[str, Any] | None = None) -> int:
    """Return the gonol value at one observation index under the candidate."""

    _require_nonnegative_int(index, "index")
    op = recover_transition_operator() if operator is None else operator
    y0 = int(op["y_0"])
    d1 = int(op["first_difference"])
    d2 = int(op["second_difference"])
    return y0 + (index * d1) + ((index * (index - 1)) // 2 * d2)


def replay_transition(count: int = len(OBSERVED_GONOL_SEQUENCE)) -> tuple[int, ...]:
    """Replay the observed candidate transition sequence."""

    _require_positive_int(count, "count")
    operator = recover_transition_operator()
    return tuple(transition_at(index, operator) for index in range(count))


def derive_next_gonol() -> int:
    """Derive the next candidate gonol after the observed handoff sequence."""

    return transition_at(len(OBSERVED_GONOL_SEQUENCE), recover_transition_operator())


def coordinate_id(address: GonolAddress) -> str:
    """Digest one public coordinate for replay tracking."""

    return _payload_digest({"coordinate": address.canonical()})


def derive_lazy_key(root_secret: bytes, address: GonolAddress, length: int = 32) -> bytes:
    """Derive one traffic key for one address without expanding the gonol.

    The root secret is the only entropy-bearing input. Gonol fields are public
    context and synchronization coordinates for domain separation.
    """

    if not isinstance(root_secret, (bytes, bytearray, memoryview)):
        raise TypeError("root_secret must be bytes-like")
    secret = bytes(root_secret)
    if not secret:
        raise AsyncGonolError("root_secret must not be empty")
    _require_positive_int(length, "length")

    output = bytearray()
    counter = 0
    while len(output) < length:
        block_payload = {
            "address": address.canonical(),
            "counter": counter,
            "domain": "pcea.async-gonol.lazy-key-block",
        }
        output.extend(hmac.new(secret, canonical_json_bytes(block_payload), sha256).digest())
        counter += 1
    return bytes(output[:length])


def derive_fresh_lazy_key(
    root_secret: bytes,
    address: GonolAddress,
    replay_cache: ReplayCache,
    length: int = 32,
) -> bytes:
    """Derive one key only if the address has not already been accepted."""

    replay_cache.require_fresh(address)
    return derive_lazy_key(root_secret, address, length=length)


def comparison_matrix() -> dict[str, Any]:
    """Compare the candidate with ordinary linear ratchet and tree KDF controls."""

    return {
        "comparison_scope": "topology/control comparison with equal root entropy",
        "ordinary_linear_ratchet": {
            "synchronization": "ordered delivery is natural; out-of-order delivery needs skipped-key storage or auxiliary headers",
            "replay_resistance": "requires nonce/message-number cache or AEAD nonce discipline",
            "compromise_containment": "strong only when old chain keys are deleted and forward ratcheting continues",
            "recovery": "loss of current state can block future messages unless a higher-level resync path exists",
        },
        "ordinary_tree_kdf": {
            "synchronization": "addressable branches support sparse derivation and out-of-order delivery",
            "replay_resistance": "requires used-leaf tracking or nonce discipline",
            "compromise_containment": "can isolate branches when independent subkeys are derived and erased",
            "recovery": "path disclosure can help resync but may expose metadata",
        },
        "pcea_gonol_addressed_candidate": {
            "synchronization": "public gonol path/position/epoch/message coordinates allow lazy out-of-order derivation",
            "replay_resistance": "coordinate reuse is rejected only when the receiver tracks accepted coordinates",
            "compromise_containment": "no advantage is credited from gonol geometry; containment depends on secret separation, deletion, and ratcheting policy",
            "recovery": "address/path/state receipts can support resync, but public metadata leakage must be attacked",
        },
        "standing": {
            "synchronization": "survives as an addressability candidate",
            "replay_resistance": "survives only with explicit replay cache or nonce discipline",
            "compromise_containment": "unresolved; no better than tree KDF without additional evidence",
            "recovery": "partial candidate; needs loss and metadata-leakage tests",
            "security_basis": "external secret entropy plus approved KDF only",
        },
        "nonclaims": list(NONCLAIMS),
    }


def freeze_document() -> dict[str, Any]:
    """Return the frozen research receipt for this candidate."""

    operator = recover_transition_operator()
    replayed = replay_transition()
    next_gonol = derive_next_gonol()
    document: dict[str, Any] = {
        "comparison": comparison_matrix(),
        "derived_next_gonol": {
            "standing": "candidate value under OPERATOR_ID, not UCNS canon",
            "value": next_gonol,
        },
        "hmmm": list(HMMM),
        "key_derivation": {
            "address_bound_fields": [
                "protocol_label",
                "operator_id",
                "gonol_size",
                "recursive_path",
                "position",
                "epoch",
                "message_counter",
                "state_digest",
                "transcript_digest",
            ],
            "entropy_basis": "root_secret only",
            "kdf_shape": "HMAC-SHA256 expansion over canonical address payload",
            "materialization": "lazy single-coordinate derivation",
            "replay_control": "receiver-side coordinate cache or equivalent nonce discipline required",
        },
        "nonclaims": list(NONCLAIMS),
        "observed_sequence": list(OBSERVED_GONOL_SEQUENCE),
        "operator": operator,
        "replay": {
            "matches_observation": replayed == OBSERVED_GONOL_SEQUENCE,
            "values": list(replayed),
        },
        "schema": FREEZE_SCHEMA,
        "source_identities": {
            "legacy_gonal_architecture_blob": LEGACY_GONAL_ARCHITECTURE_BLOB,
            "legacy_research_source_commit": LEGACY_RESEARCH_SOURCE_COMMIT,
            "pcea_cleanup_commit": PCEA_CLEANUP_COMMIT,
            "pinned_public_gonol_sha256": PINNED_PUBLIC_GONOL_SHA256,
            "stack_refresh_commit": STACK_REFRESH_COMMIT,
        },
    }
    document["receipt_digest"] = _payload_digest(document)
    return document


def write_freeze_document(path: str | Path | None = None) -> Path:
    """Write the freeze JSON beside this module unless a path is supplied."""

    destination = Path(path) if path is not None else Path(__file__).with_name("async_gonol_key_state_freeze.json")
    destination.write_bytes(
        json.dumps(freeze_document(), ensure_ascii=True, indent=2, sort_keys=True).encode("utf-8")
        + b"\n"
    )
    return destination


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-freeze", action="store_true", help="write async_gonol_key_state_freeze.json")
    parser.add_argument("--path", help="optional freeze output path")
    args = parser.parse_args(argv)
    if args.write_freeze:
        path = write_freeze_document(args.path)
        print(path)
        return 0
    print(json.dumps(freeze_document(), ensure_ascii=True, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "AsyncGonolError",
    "DERIVED_NEXT_GONOL",
    "FREEZE_SCHEMA",
    "GonolAddress",
    "HMMM",
    "KDF_PROTOCOL_LABEL",
    "NONCLAIMS",
    "OBSERVED_GONOL_SEQUENCE",
    "OPERATOR_ID",
    "ReplayCache",
    "ReplayError",
    "canonical_json_bytes",
    "comparison_matrix",
    "coordinate_id",
    "derive_fresh_lazy_key",
    "derive_lazy_key",
    "derive_next_gonol",
    "derive_state_digest",
    "freeze_document",
    "recover_transition_operator",
    "replay_transition",
    "transition_at",
    "write_freeze_document",
]
