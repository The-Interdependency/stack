"""Stack-local gonol successor mechanics research.

This module starts from the pinned UCNS Public Gonol carrier and the current
construction/closure discipline available in stack. It does not fit formulas to
the observed sequence and does not search for a pre-existing transition
operator. Candidate operations are mechanical counts or explicitly blocked
mechanics derived from the pinned carrier, Mobius root loop, and closure rules.
"""

# === MODULE_BUILD ===
# id: pcea_gonol_successor_mechanics
#   module_name: gonol_successor_mechanics
#   module_kind: experiment
#   summary: evaluates mechanics-derived gonol successor operations from the pinned 157-position Public Gonol carrier without fitting the observed integer chain
#   owner: The Interdependency
#   public_surface: OBSERVED_GATE, INTERPOLATION_CONTROL_NEXT, MechanicsSnapshot, SuccessorResult, evaluate_successor_candidates, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _load_module, _stack_root, _candidate_functions, _evaluate_candidate, _result_payload, _mechanics_payload, _producer_code_reference
#   auth_boundary: none; reads stack-pinned UCNS and PCEA identity files only
#   storage_boundary: read stack-manifest.json, research/pcea/BASE.json, research/ucns/BASE.json, and libs/ucns source files; no writes at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research.pcea.tests.test_gonol_successor_mechanics
#   rollout: stack-local research artifact; not promoted to PCEA runtime, UCNS canon, or stack libs
#   rollback: remove this module, its tests, and its research report
#   requires: ucns_public_gonol_geometry, ucns_native_mobius_geometry, gonol-build construction discipline
#   since: 2026-09-02
#   unresolved: exact Public Gonol position operations; exact UCNS affixiation/coupling law; exact recursive-scale transition law; structure of a completed 2881-gonol
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: successor_mechanics_start_from_pinned_157_gonol
#   given: successor mechanics are evaluated
#   then: the source mechanics bind the stack-pinned UCNS Public Gonol arity, digest, origin, and exact position count
#   class: safety
#   since: 2026-09-02
#
# id: successor_candidates_do_not_embed_gate_targets
#   given: mechanics-derived candidate functions are inspected
#   then: no candidate function embeds 2881, 54837698421, or 164513086777 as an internal numeric constant
#   class: safety
#   since: 2026-09-02
#
# id: successor_candidates_reject_failed_mechanics
#   given: mechanics-derived candidates are applied to the pinned 157-gonol
#   then: candidates that do not produce 2881 are rejected before any 2881-to-target or next-gonol claim
#   class: evidence
#   since: 2026-09-02
#
# id: successor_mechanics_record_unresolved_operations
#   given: a candidate requires an unresolved Public Gonol function operation, affixiation geometry, or recursive-scale law
#   then: the candidate is marked UNRESOLVED rather than fitted numerically
#   class: doctrine
#   since: 2026-09-02
#
# id: successor_mechanics_receipt_replays_byte_identical
#   given: the same stack-pinned source identities and mechanics candidates
#   then: receipt bytes and receipt digest are identical across independent constructions
#   class: correctness
#   since: 2026-09-02
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
from types import ModuleType
from typing import Any, Callable


OBSERVED_GATE: tuple[int, int, int] = (157, 2881, 54837698421)
INTERPOLATION_CONTROL_NEXT = 164513086777
SCHEMA = "the-interdependency.stack-research.pcea.gonol-successor-mechanics"
VERSION = "0.1.0"
STANDING = "stack-local-research"
STATUS_FALSIFIED = "FALSIFIED"
STATUS_UNRESOLVED = "UNRESOLVED"
STATUS_CONSTRUCTOR_CANDIDATE = "CONSTRUCTOR_CANDIDATE"

PINNED_PUBLIC_GONOL_SHA256 = "55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5"

NONCLAIMS: tuple[str, ...] = (
    "not a UCNS canon modification",
    "not PCEA runtime behavior",
    "not a fitted recurrence over observed integers",
    "not a recovered pre-existing transition operator",
    "not cryptographic security evidence",
    "not entropy or hardness evidence",
    "not public authenticity or provenance proof",
)

HMMM: tuple[str, ...] = (
    "the exact operation of each Public Gonol function position is unresolved",
    "the exact UCNS Mobius-carrier affixiation/coupling law is unresolved",
    "the full circle-to-epicycle-to-disk-to-sphere recursive-scale transition law is unresolved",
    "no completed 2881-gonol constituent structure is available for second-stage structural operations",
    "the interpolation control 164513086777 has no empirical meaning until an independent constructor reaches the comparison stage",
)


class SuccessorMechanicsError(RuntimeError):
    """Base error for stack-local successor mechanics research."""


class CandidateBlocked(SuccessorMechanicsError):
    """Raised when a candidate depends on mechanics currently recorded as hmmm."""


@dataclass(frozen=True, slots=True)
class MechanicsSnapshot:
    """Pinned mechanics available before fitting any observed transition."""

    pcea_base: dict[str, Any]
    ucns_base: dict[str, Any]
    stack_manifest_work_graph_sha256: str
    public_gonol_arity: int
    public_gonol_sha256: str
    public_gonol_positions: tuple[tuple[int, str], ...]
    public_gonol_origin: tuple[int, str]
    public_gonol_arrangement_bytes_sha256: str
    public_gonol_arrangement_byte_count: int
    mobius_visible_return_turns: int
    mobius_complete_return_turns: int
    mobius_visible_preimage_count: int
    public_position_operation: str
    affixiation_coupling_law: str
    recursive_scale_transition_law: str


@dataclass(frozen=True, slots=True)
class SuccessorCandidate:
    """One mechanics-derived candidate operation."""

    candidate_id: str
    mechanic_basis: str
    operation: Callable[[MechanicsSnapshot, int], int]
    hmmm: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class SuccessorResult:
    """One candidate's result through the two-transition successor gate."""

    candidate_id: str
    status: str
    mechanic_basis: str
    first_input: int
    first_output: int | None
    first_target_match: bool
    second_input: int | None
    second_output: int | None
    second_target_match: bool
    next_prediction: int | None
    control_comparison: str | None
    rejection_reason: str | None
    hmmm: tuple[str, ...]


def _stack_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SuccessorMechanicsError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def load_mechanics() -> MechanicsSnapshot:
    """Load the pinned 157-gonol mechanics available in stack."""

    root = _stack_root()
    public_gonol = _load_module(
        "stack_pinned_ucns_public_gonol",
        root / "libs" / "ucns" / "src" / "ucns" / "public_gonol.py",
    )
    direct_mobius = _load_module(
        "stack_pinned_ucns_direct_mobius",
        root / "libs" / "ucns" / "src" / "ucns" / "direct_mobius.py",
    )
    pcea_base = _load_json(root / "research" / "pcea" / "BASE.json")
    ucns_base = _load_json(root / "research" / "ucns" / "BASE.json")
    stack_manifest = _load_json(root / "stack-manifest.json")

    arrangement = tuple(public_gonol.PUBLIC_GONOL_157)
    positions = tuple((index, glyph) for index, glyph in enumerate(arrangement))
    arrangement_bytes = _canonical_bytes(arrangement)
    origin = direct_mobius.native_mobius_state(0)
    one_turn = origin.advance(1)
    two_turns = origin.advance(2)
    visible_preimages = {
        (origin.visible_key[0], str(origin.visible_key[1]), str(origin.frame)),
        (one_turn.visible_key[0], str(one_turn.visible_key[1]), str(one_turn.frame)),
    }
    if two_turns != origin:
        raise SuccessorMechanicsError("pinned Mobius two-turn return failed")

    computed_digest = public_gonol.public_gonol_sha256()
    if computed_digest != PINNED_PUBLIC_GONOL_SHA256:
        raise SuccessorMechanicsError("pinned Public Gonol digest mismatch")
    if len(arrangement) != OBSERVED_GATE[0]:
        raise SuccessorMechanicsError("observed first gonol does not match pinned Public Gonol arity")

    return MechanicsSnapshot(
        pcea_base=pcea_base,
        ucns_base=ucns_base,
        stack_manifest_work_graph_sha256=stack_manifest["work_graph_sha256"],
        public_gonol_arity=len(arrangement),
        public_gonol_sha256=computed_digest,
        public_gonol_positions=positions,
        public_gonol_origin=positions[0],
        public_gonol_arrangement_bytes_sha256=sha256(arrangement_bytes).hexdigest(),
        public_gonol_arrangement_byte_count=len(arrangement_bytes),
        mobius_visible_return_turns=1,
        mobius_complete_return_turns=2,
        mobius_visible_preimage_count=len(visible_preimages),
        public_position_operation="hmmm",
        affixiation_coupling_law="hmmm",
        recursive_scale_transition_law="hmmm",
    )


def _atomic_identity_carry(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    return gonol_size


def _mobius_twofold_lift(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    return gonol_size * mechanics.mobius_visible_preimage_count


def _mobius_twofold_closed_whole(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    return gonol_size * mechanics.mobius_visible_preimage_count + 1


def _cyclic_order_edges_with_positions(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    return gonol_size + gonol_size


def _cyclic_order_edges_closed_whole(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    return gonol_size + gonol_size + 1


def _unordered_position_pair_closure(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    return gonol_size + (gonol_size * (gonol_size - 1)) // 2 + 1


def _directed_order_pair_closure(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    return gonol_size + gonol_size * (gonol_size - 1) + 1


def _canonical_arrangement_byte_count(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    if gonol_size != mechanics.public_gonol_arity:
        raise CandidateBlocked("canonical byte count requires a completed successor arrangement")
    return mechanics.public_gonol_arrangement_byte_count


def _complete_public_function_application(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    if mechanics.public_position_operation == "hmmm":
        raise CandidateBlocked("Public Gonol function-position operation is unresolved")
    return gonol_size + gonol_size * gonol_size + 1


def _affixiate_all_position_pairs(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    if mechanics.affixiation_coupling_law == "hmmm":
        raise CandidateBlocked("UCNS affixiation/coupling geometry is unresolved")
    return gonol_size + (gonol_size * (gonol_size - 1)) // 2 + 1


def _recursive_scale_transition(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    if mechanics.recursive_scale_transition_law == "hmmm":
        raise CandidateBlocked("UCNS recursive-scale transition law is unresolved")
    return gonol_size


def _candidate_functions() -> tuple[SuccessorCandidate, ...]:
    return (
        SuccessorCandidate(
            "atomic_identity_carry",
            "closed gonol remains atomic when participating at another scale",
            _atomic_identity_carry,
        ),
        SuccessorCandidate(
            "mobius_twofold_lift",
            "one visible Mobius phase has two complete local-frame representatives",
            _mobius_twofold_lift,
        ),
        SuccessorCandidate(
            "mobius_twofold_closed_whole",
            "two Mobius representatives per position plus one closed whole",
            _mobius_twofold_closed_whole,
        ),
        SuccessorCandidate(
            "cyclic_order_edges_with_positions",
            "exact cyclic carrier order plus one successor edge per position",
            _cyclic_order_edges_with_positions,
        ),
        SuccessorCandidate(
            "cyclic_order_edges_closed_whole",
            "cyclic successor edges, retained positions, and one closed whole",
            _cyclic_order_edges_closed_whole,
        ),
        SuccessorCandidate(
            "unordered_position_pair_closure",
            "all unordered pairs of exact positions, retained positions, and one closed whole",
            _unordered_position_pair_closure,
        ),
        SuccessorCandidate(
            "directed_order_pair_closure",
            "all direction-sensitive ordered pairs, retained positions, and one closed whole",
            _directed_order_pair_closure,
        ),
        SuccessorCandidate(
            "canonical_arrangement_byte_count",
            "canonical JSON byte count of the exact 157-position arrangement",
            _canonical_arrangement_byte_count,
            ("cannot recur without a completed successor arrangement",),
        ),
        SuccessorCandidate(
            "complete_public_function_application",
            "all function positions applied to all positions plus retained positions and one closure",
            _complete_public_function_application,
            ("blocked by unresolved Public Gonol function-position operation",),
        ),
        SuccessorCandidate(
            "affixiate_all_position_pairs",
            "all pairwise affixiations of bounded positions under UCNS coupling geometry",
            _affixiate_all_position_pairs,
            ("blocked by unresolved UCNS affixiation/coupling geometry",),
        ),
        SuccessorCandidate(
            "recursive_scale_transition",
            "the UCNS recursive-scale transition law itself",
            _recursive_scale_transition,
            ("blocked by unresolved recursive-scale transition law",),
        ),
    )


def _evaluate_candidate(
    candidate: SuccessorCandidate,
    mechanics: MechanicsSnapshot,
    gate: tuple[int, int, int],
) -> SuccessorResult:
    first_input, first_target, second_target = gate
    try:
        first_output = candidate.operation(mechanics, first_input)
    except CandidateBlocked as exc:
        return SuccessorResult(
            candidate.candidate_id,
            STATUS_UNRESOLVED,
            candidate.mechanic_basis,
            first_input,
            None,
            False,
            None,
            None,
            False,
            None,
            None,
            str(exc),
            candidate.hmmm,
        )
    first_matches = first_output == first_target
    if not first_matches:
        return SuccessorResult(
            candidate.candidate_id,
            STATUS_FALSIFIED,
            candidate.mechanic_basis,
            first_input,
            first_output,
            False,
            None,
            None,
            False,
            None,
            None,
            f"first transition produced {first_output}, not {first_target}",
            candidate.hmmm,
        )
    try:
        second_output = candidate.operation(mechanics, first_output)
    except CandidateBlocked as exc:
        return SuccessorResult(
            candidate.candidate_id,
            STATUS_UNRESOLVED,
            candidate.mechanic_basis,
            first_input,
            first_output,
            True,
            first_output,
            None,
            False,
            None,
            None,
            str(exc),
            candidate.hmmm,
        )
    second_matches = second_output == second_target
    if not second_matches:
        return SuccessorResult(
            candidate.candidate_id,
            STATUS_FALSIFIED,
            candidate.mechanic_basis,
            first_input,
            first_output,
            True,
            first_output,
            second_output,
            False,
            None,
            None,
            f"second transition produced {second_output}, not {second_target}",
            candidate.hmmm,
        )
    next_prediction = candidate.operation(mechanics, second_output)
    comparison = "equal" if next_prediction == INTERPOLATION_CONTROL_NEXT else "unequal"
    return SuccessorResult(
        candidate.candidate_id,
        STATUS_CONSTRUCTOR_CANDIDATE,
        candidate.mechanic_basis,
        first_input,
        first_output,
        True,
        first_output,
        second_output,
        True,
        next_prediction,
        comparison,
        None,
        candidate.hmmm,
    )


def evaluate_successor_candidates(
    gate: tuple[int, int, int] = OBSERVED_GATE,
    mechanics: MechanicsSnapshot | None = None,
) -> tuple[SuccessorResult, ...]:
    """Apply mechanics-derived candidates to the two-transition gate."""

    if len(gate) != 3 or any(isinstance(value, bool) or not isinstance(value, int) for value in gate):
        raise TypeError("gate must contain exactly three integer gonol sizes")
    if any(value <= 0 for value in gate):
        raise ValueError("gate gonol sizes must be positive")
    snapshot = mechanics or load_mechanics()
    if gate[0] != snapshot.public_gonol_arity:
        raise ValueError("first gate value must match the pinned Public Gonol arity")
    return tuple(_evaluate_candidate(candidate, snapshot, gate) for candidate in _candidate_functions())


def _result_payload(result: SuccessorResult) -> dict[str, Any]:
    return {
        "candidate_id": result.candidate_id,
        "status": result.status,
        "mechanic_basis": result.mechanic_basis,
        "first_input": result.first_input,
        "first_output": result.first_output,
        "first_target_match": result.first_target_match,
        "second_input": result.second_input,
        "second_output": result.second_output,
        "second_target_match": result.second_target_match,
        "next_prediction": result.next_prediction,
        "control_comparison": result.control_comparison,
        "rejection_reason": result.rejection_reason,
        "hmmm": list(result.hmmm),
    }


def _mechanics_payload(mechanics: MechanicsSnapshot) -> dict[str, Any]:
    return {
        "pcea_base": mechanics.pcea_base,
        "ucns_base": mechanics.ucns_base,
        "stack_manifest_work_graph_sha256": mechanics.stack_manifest_work_graph_sha256,
        "public_gonol": {
            "arity": mechanics.public_gonol_arity,
            "sha256": mechanics.public_gonol_sha256,
            "origin": list(mechanics.public_gonol_origin),
            "positions": [[index, glyph] for index, glyph in mechanics.public_gonol_positions],
            "arrangement_bytes_sha256": mechanics.public_gonol_arrangement_bytes_sha256,
            "arrangement_byte_count": mechanics.public_gonol_arrangement_byte_count,
        },
        "mobius": {
            "visible_return_turns": mechanics.mobius_visible_return_turns,
            "complete_return_turns": mechanics.mobius_complete_return_turns,
            "visible_preimage_count": mechanics.mobius_visible_preimage_count,
        },
        "unresolved_mechanics": {
            "public_position_operation": mechanics.public_position_operation,
            "affixiation_coupling_law": mechanics.affixiation_coupling_law,
            "recursive_scale_transition_law": mechanics.recursive_scale_transition_law,
        },
    }


def _producer_code_reference() -> str:
    text = Path(__file__).read_text(encoding="utf-8")
    return "sha256:" + sha256(text.encode("utf-8")).hexdigest()


def receipt_payload() -> dict[str, Any]:
    """Return the deterministic successor-mechanics research receipt."""

    mechanics = load_mechanics()
    results = evaluate_successor_candidates(OBSERVED_GATE, mechanics)
    constructor_candidates = [
        result for result in results if result.status == STATUS_CONSTRUCTOR_CANDIDATE
    ]
    return {
        "schema": SCHEMA,
        "version": VERSION,
        "standing": STANDING,
        "producer_code_reference": _producer_code_reference(),
        "observed_gate": {
            "first_source": OBSERVED_GATE[0],
            "first_target_for_comparison_only": OBSERVED_GATE[1],
            "second_target_for_comparison_only": OBSERVED_GATE[2],
            "target_use_policy": (
                "targets are comparators only; candidate operations receive mechanics and current size"
            ),
        },
        "mechanics": _mechanics_payload(mechanics),
        "candidate_policy": {
            "numeric_fitting": "forbidden",
            "transition_operator_search": "forbidden",
            "first_gate": "candidate must produce 2881 from 157 without target constants",
            "second_gate": "unchanged candidate must produce 54837698421 from 2881",
            "next_prediction": "emitted only after both gates pass",
            "interpolation_control": INTERPOLATION_CONTROL_NEXT,
            "control_comparison": "not reached unless a constructor candidate emits a next prediction",
        },
        "results": [_result_payload(result) for result in results],
        "constructor_candidates": [_result_payload(result) for result in constructor_candidates],
        "next_predictions": [
            {
                "candidate_id": result.candidate_id,
                "next_prediction": result.next_prediction,
                "control_comparison": result.control_comparison,
            }
            for result in constructor_candidates
        ],
        "summary": {
            "falsified": sum(result.status == STATUS_FALSIFIED for result in results),
            "unresolved": sum(result.status == STATUS_UNRESOLVED for result in results),
            "constructor_candidates": len(constructor_candidates),
            "next_prediction_available": bool(constructor_candidates),
        },
        "nonclaims": list(NONCLAIMS),
        "hmmm": list(HMMM),
    }


def receipt_bytes(payload: dict[str, Any] | None = None) -> bytes:
    receipt = payload if payload is not None else receipt_payload()
    return _canonical_bytes(receipt) + b"\n"


def receipt_digest(payload: dict[str, Any] | None = None) -> str:
    return sha256(receipt_bytes(payload)).hexdigest()


def main() -> None:
    payload = receipt_payload()
    print(json.dumps(
        {"receipt_sha256": receipt_digest(payload), "receipt": payload},
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
