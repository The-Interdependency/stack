"""Event-pair quotient candidate for the recursive gonol state relation.

The pinned seed has 39 pairwise projection events and 21 band-pair relations.
This post-observation candidate treats the exterior pair space over those event
states as having one independent constraint per band-pair relation. It exactly
accounts for ``720 = C(39, 2) - 21`` and is then falsified by applying that same
operator unchanged at the next observed gate.
"""

# === MODULE_BUILD ===
# id: ucns_event_pair_quotient_candidate
#   module_name: event_pair_quotient_candidate
#   module_kind: experiment
#   summary: tests the exact retrodictive identity C(39,2)-21=720 as an unchanged event-pair quotient transition and falsifies it at the next observed gate
#   owner: The Interdependency
#   public_surface: OBSERVED_GONOLS, PairQuotientEvaluation, exterior_pair_quotient_dimension, evaluate, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _stack_root
#   auth_boundary: none; consumes stack-local event/trace research and pinned UCNS seed counts
#   storage_boundary: read-only at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_event_pair_quotient_candidate.py
#   rollout: stack-local post-observation falsification experiment only; no UCNS canon, stack libs, or PCEA promotion
#   rollback: remove this module, its tests, report, and receipt
#   requires: ucns_event_trace_lift_candidate, ucns_mobius_seed_of_life_candidate, gonol-build construction discipline
#   since: 2026-09-02
#   unresolved: whether event pairs form an exterior state space, whether 21 source relations are independent quotient constraints, completed 2881-gonol relation rank, recursive-scale state extractor
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: event_pair_quotient_binds_pinned_counts
#   given: the candidate loads its source state
#   then: it binds the exact event/trace receipt, UCNS base, 39 pairwise projection events, 21 band-pair relations, and boundary multiplicity four
#   class: safety
#   since: 2026-09-02
#
# id: event_pair_quotient_operator_is_target_free
#   given: a state count and independently supplied constraint rank
#   then: the operator returns C(state_count,2)-constraint_rank without receiving an observed target
#   class: correctness
#   since: 2026-09-02
#
# id: event_pair_quotient_first_match_is_retrodictive
#   given: the operator consumes the pinned 39-event state and 21 relation constraints
#   then: it returns 720 and the fourfold-plus-origin lift returns 2881, labeled retrodictive only
#   class: doctrine
#   since: 2026-09-02
#
# id: event_pair_quotient_fails_unchanged_second_gate
#   given: the same operator and constraint rank consume the resulting 720 state
#   then: they return 258819 and lifted gonol 1035277, which falsifies the candidate against 54837698421 without tuning
#   class: evidence
#   since: 2026-09-02
#
# id: event_pair_quotient_does_not_predict_after_failure
#   given: the unchanged second gate fails
#   then: constructor survivor count is zero and no next prediction is emitted
#   class: doctrine
#   since: 2026-09-02
#
# id: event_pair_quotient_receipt_replays
#   given: the same predecessor and pinned source are evaluated twice
#   then: canonical receipt bytes and their digest are byte-identical
#   class: correctness
#   since: 2026-09-02
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
import json
from math import comb
from pathlib import Path
from typing import Any

import event_trace_lift_candidate as lift


SCHEMA_ID = "the-interdependency.stack-research.ucns.event-pair-quotient"
SCHEMA_VERSION = "0.1.0"
STANDING = "stack-local-post-observation-falsified-candidate"

OBSERVED_GONOLS = lift.OBSERVED_GONOLS
STATUS_FALSIFIED = "FALSIFIED"
FIRST_GATE_STANDING = "RETRODICTIVE_MATCH_ONLY"

NONCLAIMS: tuple[str, ...] = (
    "not UCNS canon",
    "not evidence that projection events form an exterior vector space",
    "not evidence that each band-pair relation has independent quotient rank one",
    "not a recovered recursive-scale transition law",
    "not a PCEA runtime, entropy, hardness, or authenticity claim",
)

HMMM: tuple[str, ...] = (
    "UCNS declares event and relation ledgers but no exterior algebra over them",
    "constraint independence is an explicit candidate assumption, not source authority",
    "the exact first-gate identity does not survive unchanged recursion",
    "the completed 2881-gonol relation ledger and its actual constraint rank remain absent",
    "no constructor survives and no next prediction is authorized",
)


class EventPairQuotientError(RuntimeError):
    """Raised when candidate inputs or pinned provenance are invalid."""


@dataclass(frozen=True, slots=True)
class PairQuotientEvaluation:
    """Frozen two-gate result for the event-pair quotient candidate."""

    status: str
    event_state_count: int
    relation_constraint_rank: int
    exterior_pair_dimension: int
    first_quotient_state: int
    first_lifted_gonol: int
    first_gate_match: bool
    first_gate_standing: str
    second_pair_dimension: int
    second_quotient_state: int
    second_lifted_gonol: int
    second_gate_match: bool
    constructor_survivor_count: int
    next_prediction: int | None
    hmmm: tuple[str, ...]


def exterior_pair_quotient_dimension(state_count: int, constraint_rank: int) -> int:
    """Return the candidate dimension ``C(state_count, 2) - constraint_rank``."""

    if isinstance(state_count, bool) or not isinstance(state_count, int) or state_count < 2:
        raise EventPairQuotientError("state_count must be an integer of at least two")
    if (
        isinstance(constraint_rank, bool)
        or not isinstance(constraint_rank, int)
        or constraint_rank < 0
    ):
        raise EventPairQuotientError("constraint_rank must be a nonnegative integer")
    dimension = comb(state_count, 2)
    if constraint_rank > dimension:
        raise EventPairQuotientError("constraint rank exceeds exterior pair dimension")
    return dimension - constraint_rank


@lru_cache(maxsize=None)
def evaluate(observed: tuple[int, int, int] = OBSERVED_GONOLS) -> PairQuotientEvaluation:
    """Run the target-free operator and compare only after each output freezes."""

    if (
        len(observed) != 3
        or any(isinstance(value, bool) or not isinstance(value, int) or value <= 0 for value in observed)
    ):
        raise EventPairQuotientError("observed must contain three positive integers")
    geometry = lift.load_seed_geometry()
    event_count = geometry.pairwise_projection_event_count
    constraint_rank = geometry.pair_relation_count
    first_state = exterior_pair_quotient_dimension(event_count, constraint_rank)
    first_lift = lift.fourfold_origin_lift(first_state, geometry.boundary_multiplicity)

    second_state = exterior_pair_quotient_dimension(first_state, constraint_rank)
    second_lift = lift.fourfold_origin_lift(second_state, geometry.boundary_multiplicity)
    first_match = first_lift == observed[1]
    second_match = second_lift == observed[2]
    status = STATUS_FALSIFIED
    if not first_match:
        status = STATUS_FALSIFIED
    elif second_match:
        raise EventPairQuotientError("post-observation candidate unexpectedly reached survivor state")

    return PairQuotientEvaluation(
        status=status,
        event_state_count=event_count,
        relation_constraint_rank=constraint_rank,
        exterior_pair_dimension=comb(event_count, 2),
        first_quotient_state=first_state,
        first_lifted_gonol=first_lift,
        first_gate_match=first_match,
        first_gate_standing=FIRST_GATE_STANDING,
        second_pair_dimension=comb(first_state, 2),
        second_quotient_state=second_state,
        second_lifted_gonol=second_lift,
        second_gate_match=second_match,
        constructor_survivor_count=0,
        next_prediction=None,
        hmmm=HMMM,
    )


def _stack_root() -> Path:
    return Path(__file__).resolve().parents[2]


def receipt_payload(observed: tuple[int, int, int] = OBSERVED_GONOLS) -> dict[str, Any]:
    result = evaluate(observed)
    predecessor = Path(lift.__file__).resolve()
    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "standing": STANDING,
        "source": {
            "ucns_base_commit": lift.PINNED_UCNS_COMMIT,
            "event_trace_producer_path": str(predecessor.relative_to(_stack_root())),
            "event_trace_producer_sha256": sha256(predecessor.read_bytes()).hexdigest(),
            "event_trace_receipt_sha256": lift.receipt_digest(),
        },
        "candidate": {
            "operator": "C(state_count,2)-constraint_rank",
            "constraint_assumption": "one independent rank-one constraint per pinned band-pair relation",
            "boundary_lift": "1+4*state_count",
            "post_observation": True,
        },
        "comparison": {
            "observed": list(observed),
            "event_state_count": result.event_state_count,
            "relation_constraint_rank": result.relation_constraint_rank,
            "first_gate": {
                "exterior_pair_dimension": result.exterior_pair_dimension,
                "quotient_state": result.first_quotient_state,
                "lifted_gonol": result.first_lifted_gonol,
                "target_match": result.first_gate_match,
                "standing": result.first_gate_standing,
            },
            "second_gate": {
                "exterior_pair_dimension": result.second_pair_dimension,
                "quotient_state": result.second_quotient_state,
                "lifted_gonol": result.second_lifted_gonol,
                "target_match": result.second_gate_match,
                "standing": result.status,
            },
            "constructor_survivor_count": result.constructor_survivor_count,
            "next_prediction": result.next_prediction,
        },
        "nonclaims": list(NONCLAIMS),
        "hmmm": list(result.hmmm),
    }


def receipt_bytes(observed: tuple[int, int, int] = OBSERVED_GONOLS) -> bytes:
    return (
        json.dumps(
            receipt_payload(observed),
            ensure_ascii=True,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("ascii")
        + b"\n"
    )


def receipt_digest(observed: tuple[int, int, int] = OBSERVED_GONOLS) -> str:
    return sha256(receipt_bytes(observed)).hexdigest()


def main() -> None:
    payload = receipt_payload()
    payload["receipt_sha256"] = receipt_digest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
