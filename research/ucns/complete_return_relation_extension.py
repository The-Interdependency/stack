"""Minimal complete-return relation extension for recursive UCNS closure.

This stack-local candidate transports one closed atomic participant through the
native Mobius root loop.  The one-turn occurrence remains distinct because its
local frame is reversed.  The two-turn endpoint is identified with the start
only after complete state returns.  The resulting two-edge quotient has one
independent first-homology generator, which is retained alongside prior
relation generators when the whole promotes to the next declared scale.

No observed successor cardinality, arithmetic factorization, or desired next
rank is an input to this operation.
"""

# === MODULE_BUILD ===
# id: ucns_complete_return_relation_extension
#   module_name: complete_return_relation_extension
#   module_kind: experiment
#   summary: derives a target-free recursive relation extension by attaching the exact native Mobius two-turn return loop to a closed atomic participant and preserving its one new cycle generator across promotion
#   owner: The Interdependency
#   public_surface: RecursiveRelationState, ReturnOccurrence, CompleteReturnTrace, CompleteReturnExtension, bootstrap_public_gonol_state, complete_return_trace, extend_complete_return, iterate_complete_return, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _stack_root, _canonical_bytes, _load_json, _load_module, _direct_mobius, _file_digest, _source_file_digests, _matrix_rank, _text, _relation_id, _producer_code_reference, main
#   auth_boundary: none; consumes stack-pinned UCNS native Mobius and Public Gonol geometry plus stack-local mechanics 1 through 3
#   storage_boundary: read-only at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_complete_return_relation_extension.py
#   rollout: stack-local geometric candidate only; no UCNS canon, stack libs, PCEA, arithmetic-factor, or successor-cardinality promotion
#   rollback: remove this module, its tests, report, and receipt
#   requires: ucns_native_mobius_geometry, ucns_public_gonol_geometry, ucns_affinization_coupling_geometry, ucns_recursive_scale_transition, gonol-build construction discipline
#   since: 2026-09-02
#   unresolved: higher-dimensional attachment of the return loop; whether a later two-cell fills the loop; monodromy action on retained inner relations; whether topological relation rank corresponds to arithmetic prime-factor rank; successor cardinality law
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: complete_return_extension_binds_native_geometry
#   given: the complete-return trace is constructed
#   then: exact pinned native Mobius states at zero, one, and two turns have equal visible phase, reversed frame at one turn, and restored complete state only at two turns
#   class: safety
#   since: 2026-09-02
#
# id: complete_return_extension_closes_only_complete_state
#   given: the trace quotient is formed
#   then: zero and two turns share one quotient vertex while the one-turn reversed-frame occurrence remains distinct
#   class: doctrine
#   since: 2026-09-02
#
# id: complete_return_extension_adds_one_cycle
#   given: the exact two-edge complete-return quotient has no filling two-cell
#   then: its integer boundary map has rank one and its first-homology rank is exactly one
#   class: correctness
#   since: 2026-09-02
#
# id: complete_return_extension_preserves_prior_relations
#   given: a recursive relation state closes through one complete return
#   then: every prior relation id remains unchanged and exactly one geometry-derived return relation id is appended
#   class: correctness
#   since: 2026-09-02
#
# id: complete_return_extension_promotes_closed_whole
#   given: one complete-return relation is attached
#   then: explicit occurrence-addressed coupling closes and promotes through mechanics 2 and 3 with recoverable provenance and a distinct next-scale atomic identity
#   class: correctness
#   since: 2026-09-02
#
# id: complete_return_extension_is_target_free
#   given: the operation and its receipt are inspected
#   then: no successor cardinality, observed factorization, arithmetic omega sequence, or desired next lattice rank defines any branch or relation id
#   class: safety
#   since: 2026-09-02
#
# id: complete_return_extension_receipt_replays
#   given: pinned source identities and the one-step sample are unchanged
#   then: canonical receipt bytes and digest replay byte-identically
#   class: evidence
#   since: 2026-09-02
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
from types import ModuleType
from typing import Any

import affinization_coupling_geometry as acg
import public_gonol_functional_operations as pgfo
import recursive_scale_transition as rst


SCHEMA_ID = "the-interdependency.stack-research.ucns.complete-return-relation-extension"
SCHEMA_VERSION = "0.1.0"
STANDING = "stack-local-target-free-geometric-candidate"
SELECTION_EFFECT = "none"
PINNED_UCNS_COMMIT = "1975fe70cf4e0826a8020c2da3047569e277af64"

NONCLAIMS: tuple[str, ...] = (
    "not UCNS canon",
    "not a completed higher-dimensional gonol geometry",
    "not a successor-cardinality constructor",
    "not evidence that a return-cycle generator is an arithmetic prime factor",
    "not a numerical next-gonol prediction",
    "not PCEA key, entropy, hardness, replay-resistance, recovery, or public-authenticity evidence",
)

HMMM: tuple[str, ...] = (
    "the native root loop is exact, but its attachment to circle, epicycle, disk, sphere, and full gonol constructions remains unresolved in UCNS authority",
    "the candidate assumes no higher-dimensional two-cell fills the outer complete-return loop at the tested closure boundary",
    "the candidate retains inner relation ids under atomic promotion because current carrier geometry defines no payload action; later nontrivial monodromy would require a different quotient",
    "one topological cycle generator is not yet an arithmetic factor or Boolean divisor-lattice axis",
    "successor cardinality and the size of any new arithmetic factor remain unresolved",
)

FALSIFICATION_CONDITIONS: tuple[str, ...] = (
    "the pinned native Mobius law no longer reverses frame after one turn or restore complete state after two turns",
    "the one-turn occurrence is identified using visible phase while its complete frame differs",
    "the two-turn endpoint fails exact complete-state equality with the start",
    "the complete-return quotient boundary matrix does not have first-homology rank one",
    "a required UCNS two-cell fills the return loop and kills its first-homology generator",
    "promotion drops, rewrites, or identifies a prior relation generator",
    "later UCNS geometry supplies nontrivial monodromy on the promoted whole incompatible with retained inner relations",
    "a successor value, factorization, or requested rank enters the operation definition",
)

PROMOTION_EVIDENCE: tuple[str, ...] = (
    "construct the return-loop attachment inside an accepted higher-dimensional UCNS gonol geometry",
    "show whether disk or sphere closure preserves rather than fills the return-cycle generator",
    "derive any monodromy action on inner relations from geometry and recompute the quotient exactly",
    "validate the unchanged operation against independently observed relation structure without changing this module",
    "supply a separate geometric map before interpreting relation rank as arithmetic prime-factor rank",
)


class CompleteReturnExtensionError(ValueError):
    """Raised when the complete-return candidate violates its boundary."""


def _stack_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise CompleteReturnExtensionError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def _direct_mobius() -> ModuleType:
    return _load_module(
        "stack_pinned_ucns_direct_mobius_for_complete_return_extension",
        _stack_root() / "libs" / "ucns" / "src" / "ucns" / "direct_mobius.py",
    )


def _file_digest(root: Path, relative_path: str) -> tuple[str, str]:
    return (relative_path, sha256((root / relative_path).read_bytes()).hexdigest())


def _source_file_digests(root: Path) -> tuple[tuple[str, str], ...]:
    return tuple(
        _file_digest(root, path)
        for path in (
            "research/ucns/BASE.json",
            "stack-manifest.json",
            "libs/ucns/CANON.md",
            "libs/ucns/docs/GEOMETRY.md",
            "libs/ucns/src/ucns/direct_mobius.py",
            "libs/ucns/src/ucns/carrier.py",
            "libs/ucns/src/ucns/public_gonol.py",
            "research/ucns/public_gonol_functional_operations.py",
            "research/ucns/affinization_coupling_geometry.py",
            "research/ucns/recursive_scale_transition.py",
        )
    )


def _text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CompleteReturnExtensionError(f"{field} must be non-empty text")
    return value


def _matrix_rank(matrix: tuple[tuple[int, ...], ...]) -> int:
    """Return exact rational matrix rank without external dependencies."""

    if not matrix:
        return 0
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise CompleteReturnExtensionError("boundary matrix must be rectangular")
    work = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [value / pivot_value for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            multiple = work[row][column]
            work[row] = [
                value - multiple * pivot_entry
                for value, pivot_entry in zip(work[row], work[rank], strict=True)
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


@dataclass(frozen=True, slots=True)
class RecursiveRelationState:
    """One atomic scale state with recoverable independent relation ids."""

    scale_id: str
    atomic_id: str
    source_digest: str
    relation_basis: tuple[str, ...]
    provenance: tuple[str, ...]

    def __post_init__(self) -> None:
        _text(self.scale_id, "scale_id")
        _text(self.atomic_id, "atomic_id")
        _text(self.source_digest, "source_digest")
        if len(set(self.relation_basis)) != len(self.relation_basis):
            raise CompleteReturnExtensionError("relation basis ids must be unique")
        if any(not isinstance(item, str) or not item.strip() for item in self.relation_basis):
            raise CompleteReturnExtensionError("relation basis ids must be non-empty text")
        if not self.provenance or any(not isinstance(item, str) or not item.strip() for item in self.provenance):
            raise CompleteReturnExtensionError("state provenance is required")

    @property
    def relation_rank(self) -> int:
        return len(self.relation_basis)

    def to_payload(self) -> dict[str, Any]:
        return {
            "scale_id": self.scale_id,
            "atomic_id": self.atomic_id,
            "source_digest": self.source_digest,
            "relation_basis": list(self.relation_basis),
            "relation_rank": self.relation_rank,
            "provenance": list(self.provenance),
        }


@dataclass(frozen=True, slots=True)
class ReturnOccurrence:
    """One exact occurrence in the native complete-return trace."""

    ordinal: int
    turns: int
    phase_turns: str
    frame: str
    visible_key: tuple[str, str]
    complete_key: tuple[str, str, str]
    quotient_vertex: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "ordinal": self.ordinal,
            "turns": self.turns,
            "phase_turns": self.phase_turns,
            "frame": self.frame,
            "visible_key": list(self.visible_key),
            "complete_key": list(self.complete_key),
            "quotient_vertex": self.quotient_vertex,
        }


@dataclass(frozen=True, slots=True)
class CompleteReturnTrace:
    """Exact two-turn quotient trace and its one-dimensional chain witness."""

    law_id: str
    law_version: str
    occurrences: tuple[ReturnOccurrence, ...]
    quotient_vertices: tuple[str, ...]
    directed_edges: tuple[tuple[str, str], ...]
    boundary_matrix_c1_to_c0: tuple[tuple[int, ...], ...]
    boundary_rank: int
    filling_two_cell_count: int
    first_homology_rank: int

    def to_payload(self) -> dict[str, Any]:
        return {
            "law_id": self.law_id,
            "law_version": self.law_version,
            "occurrences": [item.to_payload() for item in self.occurrences],
            "quotient": {
                "vertices": list(self.quotient_vertices),
                "directed_edges": [list(edge) for edge in self.directed_edges],
                "endpoint_policy": "identify zero and two turns only after complete state restoration",
                "one_turn_policy": "retain as distinct reversed-frame occurrence despite equal visible phase",
            },
            "chain_witness": {
                "boundary_matrix_c1_to_c0": [list(row) for row in self.boundary_matrix_c1_to_c0],
                "boundary_rank": self.boundary_rank,
                "c1_dimension": len(self.directed_edges),
                "filling_two_cell_count": self.filling_two_cell_count,
                "first_homology_rank": self.first_homology_rank,
            },
        }


@dataclass(frozen=True, slots=True)
class CompleteReturnExtension:
    """One complete-return closure and promoted relation-state result."""

    source: RecursiveRelationState
    trace: CompleteReturnTrace
    new_relation_id: str
    relation_basis_digest: str
    closed_affinization: acg.ClosedAffinization
    transition: rst.RecursiveScaleTransition
    output: RecursiveRelationState

    @property
    def rank_delta(self) -> int:
        return self.output.relation_rank - self.source.relation_rank

    def to_payload(self) -> dict[str, Any]:
        return {
            "operation": "atomic-complete-return-loop-extension",
            "source": self.source.to_payload(),
            "trace": self.trace.to_payload(),
            "new_relation_id": self.new_relation_id,
            "relation_basis_digest": self.relation_basis_digest,
            "closed_affinization": {
                "whole_id": self.closed_affinization.whole_id,
                "digest": self.closed_affinization.digest,
                "coupling_digest": self.closed_affinization.coupling.coupling_digest,
            },
            "transition": {
                "digest": self.transition.digest,
                "occurrence_id": self.transition.occurrence_id,
                "atomic_participant": self.transition.atomic_participant.to_payload(),
            },
            "output": self.output.to_payload(),
            "rank_delta": self.rank_delta,
            "prior_relation_ids_preserved": self.output.relation_basis[:-1] == self.source.relation_basis,
        }


def bootstrap_public_gonol_state() -> RecursiveRelationState:
    """Bind the pinned Public Gonol carrier as the target-free starting atom."""

    carrier = pgfo.load_carrier()
    payload = {
        "kind": "stack-local-public-gonol-carrier-atom",
        "ucns_commit": carrier.source_commit,
        "carrier_sha256": carrier.public_gonol_sha256,
        "carrier_arity": carrier.arity,
    }
    return RecursiveRelationState(
        scale_id="public-gonol-carrier",
        atomic_id="ucns.research.public-gonol-atom:" + sha256(_canonical_bytes(payload)).hexdigest(),
        source_digest=carrier.public_gonol_sha256,
        relation_basis=(),
        provenance=(
            "libs/ucns/src/ucns/public_gonol.py",
            f"ucns-commit:{carrier.source_commit}",
            f"public-gonol-sha256:{carrier.public_gonol_sha256}",
        ),
    )


@lru_cache(maxsize=1)
def complete_return_trace() -> CompleteReturnTrace:
    """Construct the exact native zero, one, and two-turn quotient trace."""

    direct = _direct_mobius()
    states = tuple(direct.native_mobius_state(turn) for turn in (0, 1, 2))
    if not (states[0].visible_key == states[1].visible_key == states[2].visible_key):
        raise CompleteReturnExtensionError("integer-turn visible phases must agree")
    if states[0].complete_key == states[1].complete_key:
        raise CompleteReturnExtensionError("one-turn reversed frame cannot close complete state")
    if states[0].complete_key != states[2].complete_key:
        raise CompleteReturnExtensionError("two turns must restore complete state")

    vertex_for_frame = {
        direct.NativeMobiusFrame.POSITIVE: "return-quotient.frame-positive",
        direct.NativeMobiusFrame.REVERSED: "return-quotient.frame-reversed",
    }
    occurrences = tuple(
        ReturnOccurrence(
            ordinal=ordinal,
            turns=ordinal,
            phase_turns=str(state.phase_turns),
            frame=state.frame.value,
            visible_key=(state.visible_key[0], str(state.visible_key[1])),
            complete_key=(state.complete_key[0], str(state.complete_key[1]), state.complete_key[2].value),
            quotient_vertex=vertex_for_frame[state.frame],
        )
        for ordinal, state in enumerate(states)
    )
    vertices = (
        vertex_for_frame[direct.NativeMobiusFrame.POSITIVE],
        vertex_for_frame[direct.NativeMobiusFrame.REVERSED],
    )
    edges = (
        (occurrences[0].quotient_vertex, occurrences[1].quotient_vertex),
        (occurrences[1].quotient_vertex, occurrences[2].quotient_vertex),
    )
    boundary = ((-1, 1), (1, -1))
    boundary_rank = _matrix_rank(boundary)
    filling_two_cells = 0
    first_homology_rank = len(edges) - boundary_rank - filling_two_cells
    if first_homology_rank != 1:
        raise CompleteReturnExtensionError("complete-return quotient must add exactly one cycle")
    return CompleteReturnTrace(
        law_id=direct.NATIVE_MOBIUS_LAW_ID,
        law_version=direct.NATIVE_MOBIUS_LAW_VERSION,
        occurrences=occurrences,
        quotient_vertices=vertices,
        directed_edges=edges,
        boundary_matrix_c1_to_c0=boundary,
        boundary_rank=boundary_rank,
        filling_two_cell_count=filling_two_cells,
        first_homology_rank=first_homology_rank,
    )


def _relation_id(
    source: RecursiveRelationState,
    trace: CompleteReturnTrace,
    target_scale: str,
    occurrence_id: str,
) -> str:
    payload = {
        "operation": "native-complete-return-loop",
        "source_atomic_id": source.atomic_id,
        "source_state_sha256": sha256(_canonical_bytes(source.to_payload())).hexdigest(),
        "trace": trace.to_payload(),
        "target_scale": target_scale,
        "occurrence_id": occurrence_id,
    }
    return "ucns.relation.complete-return:" + sha256(_canonical_bytes(payload)).hexdigest()


def extend_complete_return(
    source: RecursiveRelationState,
    *,
    target_scale: str,
    occurrence_id: str,
) -> CompleteReturnExtension:
    """Attach one complete-return loop, close it, and promote the resulting whole."""

    if not isinstance(source, RecursiveRelationState):
        raise CompleteReturnExtensionError("source must be a RecursiveRelationState")
    _text(target_scale, "target_scale")
    _text(occurrence_id, "occurrence_id")
    if target_scale == source.scale_id:
        raise CompleteReturnExtensionError("complete-return extension must advance to a distinct scale")
    trace = complete_return_trace()
    source_state_digest = sha256(_canonical_bytes(source.to_payload())).hexdigest()
    new_relation_id = _relation_id(source, trace, target_scale, occurrence_id)
    if new_relation_id in source.relation_basis:
        raise CompleteReturnExtensionError("new return relation must be distinct from prior basis")
    next_relation_basis = source.relation_basis + (new_relation_id,)
    relation_basis_digest = sha256(_canonical_bytes({
        "basis_kind": "ordered-independent-relation-ids",
        "relation_basis": next_relation_basis,
    })).hexdigest()
    participants = (
        acg.CouplingParticipant(
            participant_id=f"{occurrence_id}.turn-0",
            scale=source.scale_id,
            role="complete-return-start-positive-frame",
            source_digest=source_state_digest,
        ),
        acg.CouplingParticipant(
            participant_id=f"{occurrence_id}.turn-1",
            scale=source.scale_id,
            role="complete-return-midpoint-reversed-frame",
            source_digest=source_state_digest,
        ),
    )
    coupled = acg.coupling(
        f"{occurrence_id}.native-complete-return",
        participants,
        source_refs=(
            f"{trace.law_id}@{trace.law_version}",
            "research.ucns.complete-return-relation-extension.v0",
            source.atomic_id,
            new_relation_id,
            f"ordered-relation-basis-sha256:{relation_basis_digest}",
        ),
        unresolved_constraints=HMMM,
    )
    closed = acg.close_affinization(coupled)
    transition = rst.promote_closed_affinization(
        closed,
        source_scale=source.scale_id,
        target_scale=target_scale,
        occurrence_id=f"{occurrence_id}.promoted-whole",
    )
    output = RecursiveRelationState(
        scale_id=target_scale,
        atomic_id=transition.atomic_participant.atomic_id,
        source_digest=transition.digest,
        relation_basis=next_relation_basis,
        provenance=source.provenance + (
            f"complete-return-trace:{sha256(_canonical_bytes(trace.to_payload())).hexdigest()}",
            f"closed-affinization:{closed.digest}",
            f"recursive-transition:{transition.digest}",
        ),
    )
    result = CompleteReturnExtension(
        source,
        trace,
        new_relation_id,
        relation_basis_digest,
        closed,
        transition,
        output,
    )
    if result.rank_delta != trace.first_homology_rank:
        raise CompleteReturnExtensionError("relation rank delta must equal return-loop homology rank")
    if output.relation_basis[:-1] != source.relation_basis:
        raise CompleteReturnExtensionError("prior relation basis changed during promotion")
    return result


def iterate_complete_return(
    steps: int,
    *,
    initial: RecursiveRelationState | None = None,
    scale_prefix: str = "recursive-complete-return-scale",
) -> tuple[CompleteReturnExtension, ...]:
    """Apply the same complete-return operation for a declared number of scales."""

    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 0:
        raise CompleteReturnExtensionError("steps must be a nonnegative integer")
    _text(scale_prefix, "scale_prefix")
    state = initial or bootstrap_public_gonol_state()
    results = []
    for index in range(steps):
        result = extend_complete_return(
            state,
            target_scale=f"{scale_prefix}-{index + 1}",
            occurrence_id=f"complete-return.iteration-{index + 1}",
        )
        results.append(result)
        state = result.output
    return tuple(results)


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_bytes()).hexdigest()


def receipt_payload() -> dict[str, Any]:
    """Return the deterministic one-step candidate receipt without observation gates."""

    root = _stack_root()
    base = _load_json(root / "research" / "ucns" / "BASE.json")
    if base["source_commit"] != PINNED_UCNS_COMMIT:
        raise CompleteReturnExtensionError("UCNS source commit mismatch")
    initial = bootstrap_public_gonol_state()
    sample = extend_complete_return(
        initial,
        target_scale="sample-complete-return-scale-1",
        occurrence_id="complete-return.sample-1",
    )
    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "producer_code_reference": _producer_code_reference(),
        "source": {
            "authority": "The-Interdependency/ucns",
            "ucns_base_commit": base["source_commit"],
            "source_file_digests": [
                {"path": path, "sha256": digest}
                for path, digest in _source_file_digests(root)
            ],
            "mechanic_receipts": {
                "public_gonol_functional_operations": pgfo.receipt_digest(pgfo.receipt_payload()),
                "affinization_coupling_geometry": acg.receipt_digest(acg.receipt_payload()),
                "recursive_scale_transition": rst.receipt_digest(rst.receipt_payload()),
            },
        },
        "candidate": {
            "operation": "attach native two-turn complete-return loop at promoted atomic whole",
            "closure_gate": "complete key equality, not visible phase equality",
            "relation_measure": "first-homology rank of unfilled return quotient",
            "prior_relation_policy": "retain exact ids; append one geometry-derived generator",
            "successor_cardinality_input": None,
            "arithmetic_factor_input": None,
            "desired_relation_rank_input": None,
        },
        "bootstrap": initial.to_payload(),
        "sample_extension": sample.to_payload(),
        "validation_state": "NOT_COMPARED_WITH_OBSERVED_SCALES",
        "promotion_evidence": list(PROMOTION_EVIDENCE),
        "falsification_conditions": list(FALSIFICATION_CONDITIONS),
        "hmmm": list(HMMM),
        "nonclaims": list(NONCLAIMS),
    }


def receipt_bytes() -> bytes:
    return _canonical_bytes(receipt_payload()) + b"\n"


def receipt_digest() -> str:
    return sha256(receipt_bytes()).hexdigest()


def main() -> None:
    payload = receipt_payload()
    payload["receipt_sha256"] = receipt_digest()
    print(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
