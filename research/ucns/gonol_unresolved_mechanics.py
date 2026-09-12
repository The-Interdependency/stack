"""UCNS gonol successor mechanics research.

This stack-local artifact researches the three unresolved UCNS mechanics named
by the PCEA gonol-successor pass:

* Public Gonol functional operations;
* affinization/affixiation and coupling geometry;
* recursive-scale transition.

It starts from the pinned 157-position Public Gonol carrier. The observed
sequence is a falsification gate only; candidate operations receive the current
gonol size and pinned UCNS mechanics, not the target values.
"""

# === MODULE_BUILD ===
# id: ucns_gonol_unresolved_mechanics
#   module_name: gonol_unresolved_mechanics
#   module_kind: experiment
#   summary: evaluates UCNS-structure-derived gonol successor candidates for the unresolved Public Gonol operation, coupling geometry, and recursive-scale transition mechanics
#   owner: The Interdependency
#   public_surface: OBSERVED_TRANSITIONS, MechanicsSnapshot, CandidateResult, evaluate_candidates, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _stack_root, _load_module, _candidate_functions, _evaluate_candidate, _mechanics_payload, _result_payload, _producer_code_reference
#   auth_boundary: none; reads stack-pinned UCNS identity and geometry files only
#   storage_boundary: read stack-manifest.json, research/ucns/BASE.json, and libs/ucns source/canon files; no writes at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_gonol_unresolved_mechanics.py
#   rollout: stack-local UCNS research artifact; no UCNS canon, stack libs, or PCEA promotion
#   rollback: remove this module, its tests, and its research report
#   requires: ucns_public_gonol_geometry, ucns_native_mobius_geometry, ucns_mobius_seed_of_life_candidate, gonol-build construction discipline
#   since: 2026-09-02
#   unresolved: exact Public Gonol function-position operation, exact affinization/affixiation coupling geometry, exact recursive-scale transition law, completed 2881-gonol internal structure
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: ucns_unresolved_mechanics_start_from_pinned_public_gonol
#   given: UCNS unresolved mechanics candidates are evaluated
#   then: the source mechanics bind the stack-pinned UCNS commit, exact 157-position Public Gonol digest, and retained Mobius geometry facts
#   class: safety
#   since: 2026-09-02
#
# id: ucns_observations_are_falsification_gates_only
#   given: a candidate operation is inspected and evaluated
#   then: it does not embed 2881, 54837698421, or a PCEA interpolation control as an internal operation constant
#   class: safety
#   since: 2026-09-02
#
# id: ucns_candidate_mechanics_are_structure_derived
#   given: bounded candidates are enumerated
#   then: each candidate is tied to pinned Public Gonol order, Mobius twofold return, or the implemented Mobius seed relation ledger rather than numeric interpolation
#   class: doctrine
#   since: 2026-09-02
#
# id: ucns_candidates_must_pass_two_transition_gate
#   given: a candidate fails to produce 2881 from the pinned 157-gonol
#   then: it is falsified before any second-gate or next-prediction claim
#   class: evidence
#   since: 2026-09-02
#
# id: ucns_unresolved_operations_remain_hmmm
#   given: a candidate requires the exact Public Gonol operation, exact coupling geometry, or exact recursive-scale law
#   then: the candidate is marked UNRESOLVED rather than completed by a fitted formula
#   class: doctrine
#   since: 2026-09-02
#
# id: ucns_unresolved_mechanics_receipt_replays_byte_identical
#   given: the same pinned UCNS source identities and declared candidates are evaluated
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


OBSERVED_TRANSITIONS: tuple[int, int, int] = (157, 2881, 54837698421)
SCHEMA = "the-interdependency.stack-research.ucns.gonol-unresolved-mechanics"
VERSION = "0.1.0"
STANDING = "stack-local-research"

STATUS_FALSIFIED = "FALSIFIED"
STATUS_UNRESOLVED = "UNRESOLVED"
STATUS_SURVIVED = "SURVIVED"

PINNED_PUBLIC_GONOL_SHA256 = "55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5"
PINNED_UCNS_COMMIT = "1975fe70cf4e0826a8020c2da3047569e277af64"

WITHHELD_COMPARISON_POLICY = (
    "PCEA interpolation control is not loaded or compared in this UCNS pass; "
    "comparison is deferred until a UCNS-derived candidate survives both gates"
)

NONCLAIMS: tuple[str, ...] = (
    "not UCNS canon",
    "not a stack/libs refresh",
    "not a PCEA runtime or key-research change",
    "not a fitted recurrence over observed integers",
    "not an inferred operation from glyph names or glyph shapes",
    "not cryptographic, entropy, hardness, or public-authenticity evidence",
)

HMMM: tuple[str, ...] = (
    "Public Gonol functional operations remain unresolved at UCNS geometry level",
    "UCNS affinization/affixiation and coupling geometry remains unresolved",
    "recursive-scale transition from closed gonol to successor gonol remains unresolved",
    "the completed 2881-gonol constituent relation structure is not available",
    "a successor constructor must be derived from UCNS geometry before PCEA key research resumes",
)


class UcnsMechanicsError(RuntimeError):
    """Base error for UCNS unresolved-mechanics research."""


class CandidateBlocked(UcnsMechanicsError):
    """Raised when a candidate depends on mechanics currently recorded as hmmm."""


@dataclass(frozen=True, slots=True)
class MechanicsSnapshot:
    """Pinned UCNS mechanics available to candidate operations."""

    ucns_base: dict[str, Any]
    stack_manifest_work_graph_sha256: str
    source_file_digests: tuple[tuple[str, str], ...]
    public_gonol_arity: int
    public_gonol_sha256: str
    public_gonol_origin: tuple[int, str]
    public_gonol_positions: tuple[tuple[int, str], ...]
    public_gonol_arrangement_bytes_sha256: str
    public_gonol_arrangement_byte_count: int
    mobius_visible_return_turns: int
    mobius_complete_return_turns: int
    mobius_visible_preimage_count: int
    mobius_seed_bands: int
    mobius_seed_projection_nodes: int
    mobius_seed_pair_relations: int
    mobius_seed_structural_relations: int
    mobius_seed_incidental_secants: int
    mobius_seed_incidental_tangencies: int
    mobius_seed_pairwise_projection_events: int
    mobius_seed_declared_structural_boundary_events: int
    public_position_operation: str
    affinization_coupling_geometry: str
    recursive_scale_transition_law: str


@dataclass(frozen=True, slots=True)
class MechanicsCandidate:
    """One UCNS-structure-derived candidate operation."""

    candidate_id: str
    mechanic: str
    basis: str
    operation: Callable[[MechanicsSnapshot, int], int]
    hmmm: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CandidateResult:
    """One candidate's status against the two-transition falsification gate."""

    candidate_id: str
    status: str
    mechanic: str
    basis: str
    first_input: int
    first_output: int | None
    first_target_match: bool
    second_input: int | None
    second_output: int | None
    second_target_match: bool
    next_prediction: int | None
    rejection_reason: str | None
    hmmm: tuple[str, ...]


def _stack_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise UcnsMechanicsError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _file_digest(root: Path, relative_path: str) -> tuple[str, str]:
    path = root / relative_path
    return (relative_path, sha256(path.read_bytes()).hexdigest())


def load_mechanics() -> MechanicsSnapshot:
    """Load the pinned UCNS mechanics allowed before any candidate fitting."""

    root = _stack_root()
    public_gonol = _load_module(
        "stack_pinned_ucns_public_gonol_for_unresolved_mechanics",
        root / "libs" / "ucns" / "src" / "ucns" / "public_gonol.py",
    )
    direct_mobius = _load_module(
        "stack_pinned_ucns_direct_mobius_for_unresolved_mechanics",
        root / "libs" / "ucns" / "src" / "ucns" / "direct_mobius.py",
    )
    carrier = _load_module(
        "stack_pinned_ucns_carrier_for_unresolved_mechanics",
        root / "libs" / "ucns" / "src" / "ucns" / "carrier.py",
    )
    mobius_seed = _load_module(
        "stack_pinned_ucns_mobius_seed_for_unresolved_mechanics",
        root / "libs" / "ucns" / "src" / "ucns" / "mobius_seed.py",
    )

    ucns_base = _load_json(root / "research" / "ucns" / "BASE.json")
    stack_manifest = _load_json(root / "stack-manifest.json")
    if ucns_base["source_commit"] != PINNED_UCNS_COMMIT:
        raise UcnsMechanicsError("UCNS research base commit mismatch")

    arrangement = tuple(public_gonol.PUBLIC_GONOL_157)
    positions = tuple((index, glyph) for index, glyph in enumerate(arrangement))
    arrangement_bytes = json.dumps(
        arrangement,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    public_digest = public_gonol.public_gonol_sha256(arrangement)
    if public_digest != PINNED_PUBLIC_GONOL_SHA256:
        raise UcnsMechanicsError("Public Gonol digest mismatch")
    if len(arrangement) != OBSERVED_TRANSITIONS[0]:
        raise UcnsMechanicsError("starting observation must equal pinned Public Gonol arity")

    origin = direct_mobius.native_mobius_state(0)
    if origin.advance(2) != origin:
        raise UcnsMechanicsError("native Mobius two-turn return failed")
    preimage_point = carrier.VisibleCarrierPoint(1.0, 0.0)
    visible_preimage_count = len(carrier.lifted_preimages(preimage_point))

    seed = mobius_seed.build_mobius_seed_of_life()
    source_paths = (
        "research/ucns/BASE.json",
        "stack-manifest.json",
        "libs/ucns/CANON.md",
        "libs/ucns/docs/GEOMETRY.md",
        "libs/ucns/src/ucns/public_gonol.py",
        "libs/ucns/src/ucns/direct_mobius.py",
        "libs/ucns/src/ucns/carrier.py",
        "libs/ucns/src/ucns/mobius_seed.py",
    )

    return MechanicsSnapshot(
        ucns_base=ucns_base,
        stack_manifest_work_graph_sha256=stack_manifest["work_graph_sha256"],
        source_file_digests=tuple(_file_digest(root, path) for path in source_paths),
        public_gonol_arity=len(arrangement),
        public_gonol_sha256=public_digest,
        public_gonol_origin=positions[0],
        public_gonol_positions=positions,
        public_gonol_arrangement_bytes_sha256=sha256(arrangement_bytes).hexdigest(),
        public_gonol_arrangement_byte_count=len(arrangement_bytes),
        mobius_visible_return_turns=1,
        mobius_complete_return_turns=2,
        mobius_visible_preimage_count=visible_preimage_count,
        mobius_seed_bands=len(seed.bands),
        mobius_seed_projection_nodes=len(seed.nodes),
        mobius_seed_pair_relations=len(seed.relations),
        mobius_seed_structural_relations=len(seed.structural_relations),
        mobius_seed_incidental_secants=len(seed.incidental_secants),
        mobius_seed_incidental_tangencies=len(seed.incidental_tangencies),
        mobius_seed_pairwise_projection_events=seed.pairwise_projection_event_count,
        mobius_seed_declared_structural_boundary_events=seed.declared_structural_boundary_event_count,
        public_position_operation="hmmm",
        affinization_coupling_geometry="hmmm",
        recursive_scale_transition_law="hmmm",
    )


def _public_identity_carry(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    return gonol_size


def _public_cyclic_order_closure(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    return gonol_size + gonol_size + 1


def _complete_public_function_application(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    if mechanics.public_position_operation == "hmmm":
        raise CandidateBlocked("Public Gonol function-position operation is unresolved")
    return gonol_size + gonol_size * gonol_size + 1


def _unordered_position_pair_closure(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    return gonol_size + (gonol_size * (gonol_size - 1)) // 2 + 1


def _directed_position_pair_closure(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    return gonol_size + gonol_size * (gonol_size - 1) + 1


def _seed_w7_structural_relations_per_position(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    return gonol_size + gonol_size * mechanics.mobius_seed_structural_relations + 1


def _seed_pair_projection_events_per_position(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    return gonol_size + gonol_size * mechanics.mobius_seed_pairwise_projection_events + 1


def _exact_affinization_coupling_geometry(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    if mechanics.affinization_coupling_geometry == "hmmm":
        raise CandidateBlocked("UCNS affinization/affixiation coupling geometry is unresolved")
    return gonol_size + gonol_size * mechanics.mobius_seed_pair_relations + 1


def _mobius_visible_preimage_promotion(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    return gonol_size * mechanics.mobius_visible_preimage_count + 1


def _seed_seven_band_scale_promotion(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    return gonol_size * mechanics.mobius_seed_bands + 1


def _recursive_scale_transition_law(mechanics: MechanicsSnapshot, gonol_size: int) -> int:
    if mechanics.recursive_scale_transition_law == "hmmm":
        raise CandidateBlocked("UCNS recursive-scale transition law is unresolved")
    return gonol_size


def _candidate_functions() -> tuple[MechanicsCandidate, ...]:
    return (
        MechanicsCandidate(
            "public_identity_carry",
            "Public Gonol functional operations",
            "every function position carries its current atomic identity",
            _public_identity_carry,
        ),
        MechanicsCandidate(
            "public_cyclic_order_closure",
            "Public Gonol functional operations",
            "exact Public Gonol cyclic order, one successor edge per position, and one closure",
            _public_cyclic_order_closure,
        ),
        MechanicsCandidate(
            "complete_public_function_application",
            "Public Gonol functional operations",
            "all function positions applied to all positions under an exact UCNS function operation",
            _complete_public_function_application,
            ("blocked until UCNS supplies the geometric operation of function positions",),
        ),
        MechanicsCandidate(
            "unordered_position_pair_closure",
            "affinization/coupling geometry",
            "all unordered exact-position pairs, retained participants, and one closure",
            _unordered_position_pair_closure,
        ),
        MechanicsCandidate(
            "directed_position_pair_closure",
            "affinization/coupling geometry",
            "all direction-sensitive exact-position pairs, retained participants, and one closure",
            _directed_position_pair_closure,
        ),
        MechanicsCandidate(
            "seed_w7_structural_relations_per_position",
            "affinization/coupling geometry",
            "implemented Mobius seed W7 structural relation count tiled once per Public Gonol position",
            _seed_w7_structural_relations_per_position,
        ),
        MechanicsCandidate(
            "seed_pair_projection_events_per_position",
            "affinization/coupling geometry",
            "implemented Mobius seed pairwise projection-event count tiled once per Public Gonol position",
            _seed_pair_projection_events_per_position,
        ),
        MechanicsCandidate(
            "exact_affinization_coupling_geometry",
            "affinization/coupling geometry",
            "the exact UCNS coupling geometry itself, preserving bounded participant identity and provenance",
            _exact_affinization_coupling_geometry,
            ("blocked until UCNS supplies the exact coupling law",),
        ),
        MechanicsCandidate(
            "mobius_visible_preimage_promotion",
            "recursive-scale transition",
            "one visible Mobius state has two lifted representatives, plus one closure",
            _mobius_visible_preimage_promotion,
        ),
        MechanicsCandidate(
            "seed_seven_band_scale_promotion",
            "recursive-scale transition",
            "one Public Gonol position promotes through the seven-band Mobius seed scale, plus one closure",
            _seed_seven_band_scale_promotion,
        ),
        MechanicsCandidate(
            "recursive_scale_transition_law",
            "recursive-scale transition",
            "the full circle-to-epicycle-to-disk-to-sphere recursive-scale transition law",
            _recursive_scale_transition_law,
            ("blocked until UCNS supplies the recursive-scale law",),
        ),
    )


def _evaluate_candidate(
    candidate: MechanicsCandidate,
    mechanics: MechanicsSnapshot,
    gate: tuple[int, int, int],
) -> CandidateResult:
    first_input, first_target, second_target = gate
    try:
        first_output = candidate.operation(mechanics, first_input)
    except CandidateBlocked as exc:
        return CandidateResult(
            candidate.candidate_id,
            STATUS_UNRESOLVED,
            candidate.mechanic,
            candidate.basis,
            first_input,
            None,
            False,
            None,
            None,
            False,
            None,
            str(exc),
            candidate.hmmm,
        )
    if first_output != first_target:
        return CandidateResult(
            candidate.candidate_id,
            STATUS_FALSIFIED,
            candidate.mechanic,
            candidate.basis,
            first_input,
            first_output,
            False,
            None,
            None,
            False,
            None,
            f"first transition produced {first_output}, not the external comparator",
            candidate.hmmm,
        )
    try:
        second_output = candidate.operation(mechanics, first_output)
    except CandidateBlocked as exc:
        return CandidateResult(
            candidate.candidate_id,
            STATUS_UNRESOLVED,
            candidate.mechanic,
            candidate.basis,
            first_input,
            first_output,
            True,
            first_output,
            None,
            False,
            None,
            str(exc),
            candidate.hmmm,
        )
    if second_output != second_target:
        return CandidateResult(
            candidate.candidate_id,
            STATUS_FALSIFIED,
            candidate.mechanic,
            candidate.basis,
            first_input,
            first_output,
            True,
            first_output,
            second_output,
            False,
            None,
            f"second transition produced {second_output}, not the external comparator",
            candidate.hmmm,
        )
    return CandidateResult(
        candidate.candidate_id,
        STATUS_SURVIVED,
        candidate.mechanic,
        candidate.basis,
        first_input,
        first_output,
        True,
        first_output,
        second_output,
        True,
        candidate.operation(mechanics, second_output),
        None,
        candidate.hmmm,
    )


def evaluate_candidates(
    gate: tuple[int, int, int] = OBSERVED_TRANSITIONS,
    mechanics: MechanicsSnapshot | None = None,
) -> tuple[CandidateResult, ...]:
    """Apply UCNS-structure-derived candidates to the falsification gate."""

    if len(gate) != 3 or any(isinstance(value, bool) or not isinstance(value, int) for value in gate):
        raise TypeError("gate must contain exactly three integer gonol sizes")
    if any(value <= 0 for value in gate):
        raise ValueError("gate gonol sizes must be positive")
    snapshot = mechanics or load_mechanics()
    if gate[0] != snapshot.public_gonol_arity:
        raise ValueError("first gate value must match the pinned Public Gonol arity")
    return tuple(_evaluate_candidate(candidate, snapshot, gate) for candidate in _candidate_functions())


def _mechanics_payload(mechanics: MechanicsSnapshot) -> dict[str, Any]:
    return {
        "ucns_base": mechanics.ucns_base,
        "stack_manifest_work_graph_sha256": mechanics.stack_manifest_work_graph_sha256,
        "source_file_digests": [
            {"path": path, "sha256": digest}
            for path, digest in mechanics.source_file_digests
        ],
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
        "mobius_seed": {
            "bands": mechanics.mobius_seed_bands,
            "projection_nodes": mechanics.mobius_seed_projection_nodes,
            "pair_relations": mechanics.mobius_seed_pair_relations,
            "structural_relations": mechanics.mobius_seed_structural_relations,
            "incidental_secants": mechanics.mobius_seed_incidental_secants,
            "incidental_tangencies": mechanics.mobius_seed_incidental_tangencies,
            "pairwise_projection_events": mechanics.mobius_seed_pairwise_projection_events,
            "declared_structural_boundary_events": mechanics.mobius_seed_declared_structural_boundary_events,
        },
        "unresolved_mechanics": {
            "public_position_operation": mechanics.public_position_operation,
            "affinization_coupling_geometry": mechanics.affinization_coupling_geometry,
            "recursive_scale_transition_law": mechanics.recursive_scale_transition_law,
        },
    }


def _result_payload(result: CandidateResult) -> dict[str, Any]:
    return {
        "candidate_id": result.candidate_id,
        "status": result.status,
        "mechanic": result.mechanic,
        "basis": result.basis,
        "first_input": result.first_input,
        "first_output": result.first_output,
        "first_target_match": result.first_target_match,
        "second_input": result.second_input,
        "second_output": result.second_output,
        "second_target_match": result.second_target_match,
        "next_prediction": result.next_prediction,
        "rejection_reason": result.rejection_reason,
        "hmmm": list(result.hmmm),
    }


def _surviving_constraints(results: tuple[CandidateResult, ...]) -> tuple[str, ...]:
    falsified = tuple(result.candidate_id for result in results if result.status == STATUS_FALSIFIED)
    return (
        "any successor constructor must do more than identity carry, cyclic closure, all-pair closure, Mobius twofold lift, or simple Mobius-seed tiling",
        "any successor constructor must expose at least one of the currently unresolved UCNS mechanics as executable geometry",
        "the first comparator blocks every completed candidate in this pass before second-stage replay",
        "the completed 2881-gonol relation structure remains a required input for structural second-stage construction",
        "falsified_candidates=" + ",".join(falsified),
    )


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def receipt_payload() -> dict[str, Any]:
    """Return the deterministic UCNS unresolved-mechanics receipt."""

    mechanics = load_mechanics()
    results = evaluate_candidates(OBSERVED_TRANSITIONS, mechanics)
    survivors = tuple(result for result in results if result.status == STATUS_SURVIVED)
    return {
        "schema": SCHEMA,
        "version": VERSION,
        "standing": STANDING,
        "producer_code_reference": _producer_code_reference(),
        "source_identity": {
            "authority": "The-Interdependency/ucns",
            "ucns_commit": mechanics.ucns_base["source_commit"],
            "canon_path": mechanics.ucns_base["canon_path"],
            "public_gonol_sha256": mechanics.public_gonol_sha256,
        },
        "construction_identity": {
            "candidate_sieve": "ucns.gonol-unresolved-mechanics.v0",
            "selection_effect": "none",
            "constructor_candidates": [result.candidate_id for result in survivors],
        },
        "observed_gate": {
            "sequence": list(OBSERVED_TRANSITIONS),
            "target_use_policy": "external observations are comparators only, not candidate inputs",
        },
        "withheld_comparison_policy": WITHHELD_COMPARISON_POLICY,
        "mechanics": _mechanics_payload(mechanics),
        "candidate_policy": {
            "numeric_interpolation": "forbidden",
            "pre_existing_transition_operator_search": "forbidden",
            "candidate_source": "pinned UCNS geometry and construction discipline",
            "first_gate": "candidate must produce the second observed value from the pinned 157-gonol",
            "second_gate": "unchanged candidate must produce the third observed value from the resulting successor",
            "next_prediction": "frozen only after both gates pass",
        },
        "results": [_result_payload(result) for result in results],
        "survivors": [_result_payload(result) for result in survivors],
        "summary": {
            "falsified": sum(result.status == STATUS_FALSIFIED for result in results),
            "unresolved": sum(result.status == STATUS_UNRESOLVED for result in results),
            "survivors": len(survivors),
            "next_prediction_available": any(result.next_prediction is not None for result in survivors),
        },
        "surviving_constraints": list(_surviving_constraints(results)),
        "nonclaims": list(NONCLAIMS),
        "hmmm": list(HMMM),
        "next_dependency_complete_action": (
            "derive and freeze an executable UCNS geometric operation for at least one "
            "Public Gonol function or coupling law, then rerun the two-transition gate"
        ),
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
