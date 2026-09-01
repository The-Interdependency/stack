"""Asynchronous PCEA gonol key-state research candidate.

This module freezes the exact observation replay currently available for the
PCEA gonol-recursion handoff. It does not recover or claim the unresolved UCNS
recursive-scale geometry. The next value is frozen as a prediction from the
named interpolation baseline so it can be tested against the actual UCNS
constructor once that constructor exists.
"""

# === MODULE_BUILD ===
# id: pcea_async_gonol_key_state
#   module_name: async_gonol_keys
#   module_kind: experiment
#   summary: observation-level gonol transition replay, interpolation-baseline prediction, and gated lazy gonol-addressed key derivation candidate for asynchronous PCEA state
#   owner: The Interdependency
#   public_surface: OBSERVED_GONOL_SEQUENCE, OPERATOR_ID, PREDICTED_NEXT_GONOL, GonolAddress, ReplayCache, interpolation_baseline_operator, transition_at, replay_transition, predict_next_gonol, actual_ucns_constructor_status, compare_prediction_to_actual_ucns, derive_state_digest, derive_lazy_key, key_addressing_comparison, freeze_document, write_freeze_document
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
# id: interpolation_prediction_is_not_derived_law
#   given: the replayed observation and no recovered UCNS recursive-scale law
#   then: predict_next_gonol returns a frozen prediction under the named interpolation baseline and marks it as non-canonical research
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
# id: key_addressing_comparison_waits_for_actual_ucns_result
#   given: no actual UCNS recursive gonol constructor value is available
#   then: linear/tree/gonol key-addressing comparison is deferred instead of reported as survived
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
FREEZE_SCHEMA = "pcea.async-gonol-key-state.freeze.v2"

OBSERVED_GONOL_SEQUENCE: tuple[int, ...] = (157, 2881, 54837698421)
PREDICTED_NEXT_GONOL = 164513086777

PCEA_STACK_PINNED_COMMIT = "91ffa8c7249dfb810ca64a0bbc500481c0bd12a9"
PCEA_LIVE_MAIN_COMMIT = "834987cb0c1fea5f62d6ea08e5c5bb878c312646"
PCEA_PYPROJECT_BLOB = "a4c2d9449c77765c0698afb869ecfd08bc1c5483"
UCNS_STACK_PINNED_COMMIT = "1975fe70cf4e0826a8020c2da3047569e277af64"
UCNS_LIVE_MAIN_COMMIT = "cff04c85df5a56fd3f9d3b178e7c49160d749652"
UCNS_PUBLIC_GONOL_BLOB = "c1955e46e2dc918fb657cb346e42106d71937e91"
STACK_ORIGIN_MAIN_AT_REFRESH = "04253ab5bed7e913ab3df7bbb00939340bca291e"
STACK_BRANCH_PARENT_AT_REFRESH = "675836eef7bbcdaaa2edc4f8246591617e161955"
STACK_PCEA_REFRESH_COMMIT = "eaec7fd6ee4e829b6fae10a2c6d520b35857137d"
PRIOR_ACTOR_A_COMMIT = "ce41ceb86b0e4819bfbb976f3ce187567391af48"
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
    "not a linear/tree/gonol key-addressing comparison until an actual UCNS out-of-sample result exists",
)

HMMM: tuple[str, ...] = (
    "exact UCNS recursive-scale transition law remains unresolved",
    "live UCNS main has no actual recursive gonol constructor value for the next step",
    "the observed sequence has no source-level transition operator in the current stack refresh, live UCNS, or migrated PCEA research lane",
    "candidate key schedule comparison is gated until the interpolation baseline is tested against an actual UCNS value",
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


def interpolation_baseline_operator(
    observed: Sequence[int] = OBSERVED_GONOL_SEQUENCE,
) -> dict[str, Any]:
    """Return the exact interpolation baseline available from current evidence.

    Current source evidence exposes only three observed values. The baseline is
    therefore the minimal constant-second-difference interpolation over
    observation index. It is sufficient to replay and make a prediction, but it
    is explicitly not the unresolved UCNS recursive-scale law.
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
        "operator_standing": "three-point interpolation baseline, not UCNS recursive-scale canon",
        "second_difference": second_difference,
        "source_values": list(values),
        "y_0": values[0],
    }


def transition_at(index: int, operator: Mapping[str, Any] | None = None) -> int:
    """Return the gonol value at one observation index under the candidate."""

    _require_nonnegative_int(index, "index")
    op = interpolation_baseline_operator() if operator is None else operator
    y0 = int(op["y_0"])
    d1 = int(op["first_difference"])
    d2 = int(op["second_difference"])
    return y0 + (index * d1) + ((index * (index - 1)) // 2 * d2)


def replay_transition(count: int = len(OBSERVED_GONOL_SEQUENCE)) -> tuple[int, ...]:
    """Replay the observed candidate transition sequence."""

    _require_positive_int(count, "count")
    operator = interpolation_baseline_operator()
    return tuple(transition_at(index, operator) for index in range(count))


def predict_next_gonol() -> int:
    """Predict the next gonol under the interpolation baseline."""

    return transition_at(len(OBSERVED_GONOL_SEQUENCE), interpolation_baseline_operator())


def actual_ucns_constructor_status() -> dict[str, Any]:
    """Report whether current UCNS authority exposes the actual next constructor."""

    return {
        "actual_next_gonol": None,
        "constructor_available": False,
        "constructor_id": None,
        "status": "UNRESOLVED_ACTUAL_CONSTRUCTOR_MISSING",
        "reason": "UCNS CANON.md at live main still marks the recursive-scale transition law as hmmm",
        "searched_authorities": [
            {
                "repository": "The-Interdependency/ucns",
                "commit": UCNS_LIVE_MAIN_COMMIT,
                "standing": "live origin/main",
            },
            {
                "repository": "The-Interdependency/ucns",
                "commit": UCNS_STACK_PINNED_COMMIT,
                "standing": "stack/libs pinned snapshot",
            },
            {
                "repository": "The-Interdependency/pcea",
                "commit": LEGACY_RESEARCH_SOURCE_COMMIT,
                "standing": "materialized legacy PCEA research lane",
            },
        ],
        "hmmm": "actual recursive UCNS gonol constructor must supply the next value before out-of-sample comparison",
    }


def compare_prediction_to_actual_ucns(actual_next_gonol: int | None = None) -> dict[str, Any]:
    """Compare the interpolation prediction with an actual UCNS next value."""

    prediction = predict_next_gonol()
    if actual_next_gonol is None:
        return {
            "actual_next_gonol": None,
            "baseline_outcome": "UNRESOLVED",
            "comparison_rule": "actual missing -> no mismatch/match classification",
            "prediction": prediction,
            "status": "UNRESOLVED_ACTUAL_CONSTRUCTOR_MISSING",
        }
    _require_positive_int(actual_next_gonol, "actual_next_gonol")
    if actual_next_gonol == prediction:
        return {
            "actual_next_gonol": actual_next_gonol,
            "baseline_outcome": "SURVIVED_ONE_OUT_OF_SAMPLE_TEST",
            "comparison_rule": "actual == prediction -> survived one out-of-sample test",
            "prediction": prediction,
            "status": "SURVIVED_ONE_OUT_OF_SAMPLE_TEST",
        }
    return {
        "actual_next_gonol": actual_next_gonol,
        "baseline_outcome": "FALSIFIED",
        "comparison_rule": "actual != prediction -> quadratic interpolation candidate falsified",
        "prediction": prediction,
        "status": "FALSIFIED",
    }


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


def key_addressing_comparison(actual_next_gonol: int | None = None) -> dict[str, Any]:
    """Compare key addressing only after the interpolation baseline is tested."""

    out_of_sample = compare_prediction_to_actual_ucns(actual_next_gonol)
    if out_of_sample["baseline_outcome"] != "SURVIVED_ONE_OUT_OF_SAMPLE_TEST":
        return {
            "comparison_scope": "deferred until actual UCNS constructor supplies an out-of-sample next value",
            "gate": out_of_sample,
            "nonclaims": list(NONCLAIMS),
            "security_basis": "external secret entropy plus standard KDF only",
            "status": "DEFERRED",
        }
    return {
        "comparison_scope": "topology/control comparison with equal root entropy and standard KDF",
        "gate": out_of_sample,
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
            "security_basis": "external secret entropy plus standard KDF only",
        },
        "nonclaims": list(NONCLAIMS),
        "status": "AVAILABLE_AFTER_BASELINE_SURVIVAL",
    }


def freeze_document() -> dict[str, Any]:
    """Return the frozen research receipt for this candidate."""

    operator = interpolation_baseline_operator()
    replayed = replay_transition()
    prediction = predict_next_gonol()
    actual_status = actual_ucns_constructor_status()
    out_of_sample = compare_prediction_to_actual_ucns(actual_status["actual_next_gonol"])
    document: dict[str, Any] = {
        "actual_ucns_constructor": actual_status,
        "interpolation_prediction_test": out_of_sample,
        "key_addressing_comparison": key_addressing_comparison(actual_status["actual_next_gonol"]),
        "predicted_next_gonol": {
            "standing": "prediction under OPERATOR_ID, not derived law and not UCNS canon",
            "value": prediction,
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
            "standing": "shape test only; linear/tree/gonol comparison is deferred until actual UCNS out-of-sample result",
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
            "live_pcea_main_commit": PCEA_LIVE_MAIN_COMMIT,
            "live_ucns_main_commit": UCNS_LIVE_MAIN_COMMIT,
            "legacy_gonal_architecture_blob": LEGACY_GONAL_ARCHITECTURE_BLOB,
            "legacy_research_source_commit": LEGACY_RESEARCH_SOURCE_COMMIT,
            "pcea_pyproject_blob": PCEA_PYPROJECT_BLOB,
            "pcea_stack_pinned_commit": PCEA_STACK_PINNED_COMMIT,
            "pinned_public_gonol_sha256": PINNED_PUBLIC_GONOL_SHA256,
            "prior_actor_a_commit": PRIOR_ACTOR_A_COMMIT,
            "stack_branch_parent_at_refresh": STACK_BRANCH_PARENT_AT_REFRESH,
            "stack_origin_main_at_refresh": STACK_ORIGIN_MAIN_AT_REFRESH,
            "stack_pcea_refresh_commit": STACK_PCEA_REFRESH_COMMIT,
            "ucns_public_gonol_blob": UCNS_PUBLIC_GONOL_BLOB,
            "ucns_stack_pinned_commit": UCNS_STACK_PINNED_COMMIT,
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
    "FREEZE_SCHEMA",
    "GonolAddress",
    "HMMM",
    "KDF_PROTOCOL_LABEL",
    "NONCLAIMS",
    "OBSERVED_GONOL_SEQUENCE",
    "OPERATOR_ID",
    "PREDICTED_NEXT_GONOL",
    "ReplayCache",
    "ReplayError",
    "actual_ucns_constructor_status",
    "canonical_json_bytes",
    "compare_prediction_to_actual_ucns",
    "coordinate_id",
    "derive_fresh_lazy_key",
    "derive_lazy_key",
    "derive_state_digest",
    "freeze_document",
    "interpolation_baseline_operator",
    "key_addressing_comparison",
    "predict_next_gonol",
    "replay_transition",
    "transition_at",
    "write_freeze_document",
]
