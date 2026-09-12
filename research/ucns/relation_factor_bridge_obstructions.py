"""Obstruction audit for mapping UCNS return relations to arithmetic factors.

The complete-return extension supplies a nested basis of free topological
relation generators.  This post-observation audit tests which classes of
generator-to-factor bridge are already impossible and defines the exact
integer-presentation readout that a future geometric bridge would need.

Observed gonol values and factors are used only to falsify bridge classes after
the geometric relation candidate is frozen.  They never define a map.
"""

# === MODULE_BUILD ===
# id: ucns_relation_factor_bridge_obstructions
#   module_name: relation_factor_bridge_obstructions
#   module_kind: experiment
#   summary: proves that stable local generator-to-prime products cannot explain the observed gonols, records that complete-return homology is free rather than finite, rejects nongeometric hash and scale maps, and leaves a geometry-derived global integer presentation as the unresolved bridge class
#   owner: The Interdependency
#   public_surface: HomologyScaleProfile, PresentationReadout, BridgeClassEvaluation, FactorBridgeAudit, return_homology_profiles, evaluate_integer_presentation, audit, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _stack_root, _canonical_bytes, _file_digest, _validate_square_integer_matrix, _determinant, _producer_code_reference, main
#   auth_boundary: none; consumes the frozen complete-return relation candidate, pinned UCNS prime-geometry boundary, and squarefree observation receipt
#   storage_boundary: read-only at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_relation_factor_bridge_obstructions.py
#   rollout: stack-local obstruction and acceptance-gate research only; no UCNS canon, stack libs, PCEA, factor bridge, or successor prediction promotion
#   rollback: remove this module, its tests, report, and receipt
#   requires: ucns_complete_return_relation_extension, ucns_complete_return_relation_rank_experiment, ucns_squarefree_divisor_lattice_control, ucns_prime_primitives_p7_p5, gonol-build construction discipline
#   since: 2026-09-02
#   unresolved: full geometric interaction matrix among recursive relation generators; degree-two attachment or monodromy coefficients; target-free finite presentation; arithmetic factor identities; numerical next gonol
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: relation_factor_bridge_profiles_free_homology
#   given: unchanged complete-return extensions are accumulated
#   then: the retained relation module at rank r is free Z^r with no torsion invariant and therefore no finite arithmetic cardinality
#   class: correctness
#   since: 2026-09-02
#
# id: relation_factor_bridge_falsifies_stable_generator_products
#   given: prior relation ids persist and each has one stable prime cardinality whose product is the gonol cardinality
#   then: prior gonol cardinality must divide every successor, contradicting the pairwise-coprime observed cardinalities
#   class: evidence
#   since: 2026-09-02
#
# id: relation_factor_bridge_falsifies_local_trace_maps
#   given: factor cardinality depends only on the isomorphism class of each local complete-return trace
#   then: identical trace geometry assigns one repeated cardinality at every scale and cannot produce squarefree products once rank exceeds one
#   class: evidence
#   since: 2026-09-02
#
# id: relation_factor_bridge_rejects_nongeometric_addresses
#   given: hashes, generator ids, scale indices, or observed-factor tables are proposed as prime selectors
#   then: they are rejected as deterministic addresses or fitted data rather than UCNS geometric cardinality operations
#   class: safety
#   since: 2026-09-02
#
# id: relation_factor_bridge_defines_presentation_readout
#   given: a square integer relation matrix with explicit per-entry provenance is supplied independently
#   then: exact determinant and prime factorization produce a deterministic finite-cokernel readout only when the determinant is nonzero
#   class: correctness
#   since: 2026-09-02
#
# id: relation_factor_bridge_keeps_global_matrix_unresolved
#   given: current complete-return and UCNS prime geometry are audited
#   then: no target-free degree-two, linking, intersection, or monodromy matrix over the recursive relation basis exists, so factor cardinalities and numerical n4 remain null
#   class: doctrine
#   since: 2026-09-02
#
# id: relation_factor_bridge_receipt_replays
#   given: frozen candidate and observation identities are unchanged
#   then: canonical receipt bytes and digest replay byte-identically
#   class: correctness
#   since: 2026-09-02
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
import json
from math import gcd
from pathlib import Path
from typing import Any

import complete_return_relation_extension as extension
import complete_return_relation_rank_experiment as rank_gate
import squarefree_divisor_lattice_control as lattice


SCHEMA_ID = "the-interdependency.stack-research.ucns.relation-factor-bridge-obstructions"
SCHEMA_VERSION = "0.1.0"
STANDING = "stack-local-post-observation-bridge-obstruction-audit"
SELECTION_EFFECT = "none"

STATUS_FALSIFIED = "FALSIFIED"
STATUS_REJECTED = "REJECTED_NON_GEOMETRIC"
STATUS_BLOCKED = "BLOCKED_MISSING_GEOMETRIC_PRESENTATION"
CURRENT_BRIDGE_STATUS = "NO_SURVIVING_EXECUTABLE_FACTOR_CARDINALITY_MAP"

NONCLAIMS: tuple[str, ...] = (
    "not UCNS canon",
    "not proof that no future geometry-to-prime bridge can exist",
    "not an arithmetic reinterpretation of free first homology",
    "not permission to use hashes, ids, or scale indices as geometric measurements",
    "not a factor-cardinality or successor-gonol constructor",
    "not PCEA key, entropy, hardness, replay-resistance, recovery, or public-authenticity evidence",
)

HMMM: tuple[str, ...] = (
    "persistent relation ids cannot carry fixed prime labels because observed prime sets are not nested and observed gonol cardinalities are pairwise coprime",
    "all current return generators have the same local trace geometry, so a local isomorphism-invariant map cannot distinguish their prime identities",
    "the current unfilled return loops generate free Z modules, which have no finite order to factor",
    "a viable bridge must be global and scale-dependent through exact geometric interactions rather than generator addresses",
    "no complete-return linking, intersection, degree-two boundary, or monodromy presentation matrix is currently defined",
    "numerical n4 remains unresolved",
)

FALSIFICATION_CONDITIONS: tuple[str, ...] = (
    "a reported stable generator-prime product does not imply divisibility nesting",
    "a local trace-only map assigns different values to isomorphic trace inputs without additional geometry",
    "free homology is reported as a finite cyclic group without an independently derived relation",
    "a matrix entry is selected from an observed gonol value or factor rather than exact geometric evidence",
    "a singular presentation is reported as having finite cokernel order",
    "hashes, scale labels, or generator ids are presented as physical or geometric factor cardinalities",
    "factor identities or numerical n4 are emitted while the geometric presentation matrix is absent",
)

PROMOTION_EVIDENCE: tuple[str, ...] = (
    "construct exact pairwise linking, intersection, degree-two attachment, or monodromy coefficients for the full recursive relation basis",
    "bind every integer matrix entry to replayable UCNS geometry without observation-derived constants",
    "freeze the complete integer presentation before factoring its determinant or Smith invariants",
    "recover all three observed factor multisets under one unchanged matrix-construction law",
    "derive the next presentation and factor multiset before any numerical next-gonol comparison",
)


class RelationFactorBridgeError(ValueError):
    """Raised when a proposed factor bridge violates the audit boundary."""


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


def _file_digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _validate_square_integer_matrix(matrix: tuple[tuple[int, ...], ...]) -> None:
    if not isinstance(matrix, tuple) or not matrix:
        raise RelationFactorBridgeError("presentation matrix must be a nonempty tuple")
    size = len(matrix)
    for row in matrix:
        if not isinstance(row, tuple) or len(row) != size:
            raise RelationFactorBridgeError("presentation matrix must be square")
        if any(isinstance(value, bool) or not isinstance(value, int) for value in row):
            raise RelationFactorBridgeError("presentation entries must be integers and nonboolean")


def _determinant(matrix: tuple[tuple[int, ...], ...]) -> int:
    """Return an exact determinant using fraction-free Bareiss elimination."""

    _validate_square_integer_matrix(matrix)
    size = len(matrix)
    if size == 1:
        return matrix[0][0]
    work = [list(row) for row in matrix]
    sign = 1
    previous_pivot = 1
    for pivot_index in range(size - 1):
        if work[pivot_index][pivot_index] == 0:
            swap = next(
                (row for row in range(pivot_index + 1, size) if work[row][pivot_index] != 0),
                None,
            )
            if swap is None:
                return 0
            work[pivot_index], work[swap] = work[swap], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = work[row][column] * pivot - work[row][pivot_index] * work[pivot_index][column]
                if numerator % previous_pivot:
                    raise RelationFactorBridgeError("Bareiss exact division failed")
                work[row][column] = numerator // previous_pivot
        previous_pivot = pivot
        for row in range(pivot_index + 1, size):
            work[row][pivot_index] = 0
    return sign * work[-1][-1]


@dataclass(frozen=True, slots=True)
class PresentationReadout:
    """Exact arithmetic readout of one independently supplied presentation."""

    matrix: tuple[tuple[int, ...], ...]
    entry_provenance: tuple[tuple[str, ...], ...]
    determinant: int
    finite_cokernel: bool
    finite_order: int | None
    factorization: tuple[tuple[int, int], ...]

    def to_payload(self) -> dict[str, Any]:
        return {
            "matrix": [list(row) for row in self.matrix],
            "entry_provenance": [list(row) for row in self.entry_provenance],
            "determinant": self.determinant,
            "finite_cokernel": self.finite_cokernel,
            "finite_order": self.finite_order,
            "factorization": [
                {"prime": prime, "exponent": exponent}
                for prime, exponent in self.factorization
            ],
        }


def evaluate_integer_presentation(
    matrix: tuple[tuple[int, ...], ...],
    entry_provenance: tuple[tuple[str, ...], ...],
) -> PresentationReadout:
    """Factor a finite presentation only after every integer has provenance."""

    _validate_square_integer_matrix(matrix)
    size = len(matrix)
    if not isinstance(entry_provenance, tuple) or len(entry_provenance) != size:
        raise RelationFactorBridgeError("entry provenance must match matrix shape")
    for row in entry_provenance:
        if not isinstance(row, tuple) or len(row) != size:
            raise RelationFactorBridgeError("entry provenance must match matrix shape")
        if any(not isinstance(item, str) or not item.strip() for item in row):
            raise RelationFactorBridgeError("every presentation entry requires provenance")
    determinant = _determinant(matrix)
    finite = determinant != 0
    order = abs(determinant) if finite else None
    factors = lattice.factor_integer(order) if order is not None else ()
    return PresentationReadout(matrix, entry_provenance, determinant, finite, order, factors)


@dataclass(frozen=True, slots=True)
class HomologyScaleProfile:
    """Current complete-return relation module at one recursive scale."""

    scale_index: int
    relation_rank: int
    local_trace_sha256: str
    relation_ids: tuple[str, ...]
    free_rank: int
    torsion_invariants: tuple[int, ...]
    finite_order: int | None

    def to_payload(self) -> dict[str, Any]:
        return {
            "scale_index": self.scale_index,
            "relation_rank": self.relation_rank,
            "local_trace_sha256": self.local_trace_sha256,
            "relation_ids": list(self.relation_ids),
            "homology": {
                "module": f"Z^{self.free_rank}",
                "free_rank": self.free_rank,
                "torsion_invariants": list(self.torsion_invariants),
                "finite_order": self.finite_order,
            },
        }


@lru_cache(maxsize=None)
def return_homology_profiles(steps: int = 4) -> tuple[HomologyScaleProfile, ...]:
    """Replay unchanged return extensions as free relation modules."""

    if isinstance(steps, bool) or not isinstance(steps, int) or steps <= 0:
        raise RelationFactorBridgeError("steps must be a positive integer")
    generated = extension.iterate_complete_return(
        steps,
        scale_prefix="relation-factor-bridge-audit-scale",
    )
    profiles = []
    for index, item in enumerate(generated, start=1):
        if item.trace.filling_two_cell_count != 0:
            raise RelationFactorBridgeError("current return profile unexpectedly has a two-cell")
        if item.trace.first_homology_rank != 1 or item.rank_delta != 1:
            raise RelationFactorBridgeError("current return extension no longer adds one free cycle")
        profiles.append(HomologyScaleProfile(
            scale_index=index,
            relation_rank=item.output.relation_rank,
            local_trace_sha256=sha256(_canonical_bytes(item.trace.to_payload())).hexdigest(),
            relation_ids=item.output.relation_basis,
            free_rank=item.output.relation_rank,
            torsion_invariants=(),
            finite_order=None,
        ))
    return tuple(profiles)


@dataclass(frozen=True, slots=True)
class BridgeClassEvaluation:
    """One bounded class of proposed geometry-to-factor map."""

    bridge_class: str
    status: str
    necessary_condition: str
    evidence: dict[str, Any]
    conclusion: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "bridge_class": self.bridge_class,
            "status": self.status,
            "necessary_condition": self.necessary_condition,
            "evidence": self.evidence,
            "conclusion": self.conclusion,
        }


@dataclass(frozen=True, slots=True)
class FactorBridgeAudit:
    """Complete obstruction result and remaining admissible bridge boundary."""

    status: str
    homology_profiles: tuple[HomologyScaleProfile, ...]
    observed_values: tuple[int, ...]
    observed_factor_sets: tuple[tuple[int, ...], ...]
    bridge_classes: tuple[BridgeClassEvaluation, ...]
    current_geometric_presentation: None
    current_factor_cardinalities: None
    numerical_next_gonol: None

    def to_payload(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "homology_profiles": [item.to_payload() for item in self.homology_profiles],
            "observed_values": list(self.observed_values),
            "observed_factor_sets": [list(item) for item in self.observed_factor_sets],
            "bridge_classes": [item.to_payload() for item in self.bridge_classes],
            "remaining_admissible_class": {
                "kind": "global geometry-derived integer presentation",
                "required_sources": [
                    "exact linking or intersection numbers among all retained return generators",
                    "or exact degree-two attachment coefficients",
                    "or exact monodromy presentation coefficients",
                ],
                "readout": "prime factors of the finite cokernel order abs(det R_s), with Smith invariants retained",
                "current_geometric_presentation": self.current_geometric_presentation,
                "current_factor_cardinalities": self.current_factor_cardinalities,
            },
            "numerical_next_gonol": self.numerical_next_gonol,
        }


@lru_cache(maxsize=1)
def audit() -> FactorBridgeAudit:
    """Falsify impossible bridge classes and preserve the missing global map."""

    frozen_rank = rank_gate.evaluate()
    if frozen_rank.status != rank_gate.STATUS_MATCH:
        raise RelationFactorBridgeError("relation-rank predecessor gate changed")
    profiles = return_homology_profiles(4)
    witnesses = lattice.observed_witnesses()
    values = tuple(item.value for item in witnesses)
    factor_sets = tuple(tuple(prime for prime, _ in item.factorization) for item in witnesses)
    adjacent_divisibility = tuple(
        values[index + 1] % values[index] == 0
        for index in range(len(values) - 1)
    )
    pairwise_gcds = tuple(
        gcd(values[left], values[right])
        for left in range(len(values))
        for right in range(left + 1, len(values))
    )
    nested_factor_sets = tuple(
        set(factor_sets[index]).issubset(factor_sets[index + 1])
        for index in range(len(factor_sets) - 1)
    )
    trace_digests = tuple(item.local_trace_sha256 for item in profiles)

    bridge_classes = (
        BridgeClassEvaluation(
            bridge_class="stable persistent-generator prime product",
            status=STATUS_FALSIFIED,
            necessary_condition="preserved generator factors make every prior gonol divide every successor and make prime-factor sets nested",
            evidence={
                "relation_basis_nested": all(
                    profiles[index].relation_ids == profiles[index + 1].relation_ids[:-1]
                    for index in range(len(profiles) - 1)
                ),
                "adjacent_divisibility": list(adjacent_divisibility),
                "nested_factor_sets": list(nested_factor_sets),
                "pairwise_gcds": list(pairwise_gcds),
            },
            conclusion="observed cardinalities are pairwise coprime, so no preserved generator can retain one fixed prime factor in the product",
        ),
        BridgeClassEvaluation(
            bridge_class="local complete-return trace isomorphism map",
            status=STATUS_FALSIFIED,
            necessary_condition="isomorphic local trace geometry receives the same factor cardinality",
            evidence={
                "local_trace_digests": list(trace_digests),
                "all_local_traces_identical": len(set(trace_digests)) == 1,
                "rank_two_observation_squarefree": witnesses[1].squarefree,
                "repeated_local_factor_product_at_rank_two": "p^2",
            },
            conclusion="one local value repeated at rank two has a squared prime exponent and cannot equal a squarefree two-factor cardinality",
        ),
        BridgeClassEvaluation(
            bridge_class="generator hash, id, or scale-address prime selection",
            status=STATUS_REJECTED,
            necessary_condition="factor cardinality must be derived from UCNS geometry rather than deterministic addressing",
            evidence={
                "generator_ids_are_sha256_addresses": all(
                    relation_id.startswith("ucns.relation.complete-return:")
                    for profile in profiles
                    for relation_id in profile.relation_ids
                ),
                "scale_indices_are_external_addresses": True,
                "geometric_measurement_defined": False,
            },
            conclusion="hash-to-prime and index-to-prime rules are target-free numerically but nongeometric and therefore inadmissible",
        ),
        BridgeClassEvaluation(
            bridge_class="current free-homology cardinality",
            status=STATUS_FALSIFIED,
            necessary_condition="a finite arithmetic cardinality requires torsion or another independently derived finite presentation",
            evidence={
                "modules": [f"Z^{profile.free_rank}" for profile in profiles],
                "torsion_invariants": [list(profile.torsion_invariants) for profile in profiles],
                "finite_orders": [profile.finite_order for profile in profiles],
            },
            conclusion="free relation modules have infinite cardinality and do not contain a canonical prime order",
        ),
        BridgeClassEvaluation(
            bridge_class="global geometry-derived integer presentation",
            status=STATUS_BLOCKED,
            necessary_condition="all matrix entries come from replayable linking, intersection, degree-two, or monodromy geometry before determinant factorization",
            evidence={
                "complete_return_pairing_matrix": None,
                "complete_return_degree_two_boundary": None,
                "complete_return_monodromy_matrix": None,
                "finite_presentation_readout_implemented": True,
            },
            conclusion="this class can rotate all arithmetic factors globally between scales, but current UCNS geometry supplies no matrix to execute",
        ),
    )
    return FactorBridgeAudit(
        status=CURRENT_BRIDGE_STATUS,
        homology_profiles=profiles,
        observed_values=values,
        observed_factor_sets=factor_sets,
        bridge_classes=bridge_classes,
        current_geometric_presentation=None,
        current_factor_cardinalities=None,
        numerical_next_gonol=None,
    )


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_bytes()).hexdigest()


def receipt_payload() -> dict[str, Any]:
    """Return the deterministic factor-bridge obstruction receipt."""

    root = _stack_root()
    candidate_path = Path(extension.__file__).resolve()
    rank_path = Path(rank_gate.__file__).resolve()
    lattice_path = Path(lattice.__file__).resolve()
    prime_path = root / "libs" / "ucns" / "src" / "ucns" / "prime_primitives.py"
    result = audit()
    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "producer_code_reference": _producer_code_reference(),
        "source": {
            "complete_return_candidate": {
                "path": str(candidate_path.relative_to(root)),
                "code_sha256": _file_digest(candidate_path),
                "receipt_sha256": extension.receipt_digest(),
            },
            "relation_rank_gate": {
                "path": str(rank_path.relative_to(root)),
                "code_sha256": _file_digest(rank_path),
                "receipt_sha256": rank_gate.receipt_digest(),
            },
            "squarefree_control": {
                "path": str(lattice_path.relative_to(root)),
                "code_sha256": _file_digest(lattice_path),
                "receipt_sha256": lattice.receipt_digest(),
            },
            "ucns_prime_primitives": {
                "path": str(prime_path.relative_to(root)),
                "code_sha256": _file_digest(prime_path),
                "direction_boundary": "constructs geometry from selected arithmetic prime labels; does not invert recursive return geometry to a prime",
            },
        },
        "audit": result.to_payload(),
        "generic_presentation_gate": {
            "operation": "geometry-derived square integer matrix R -> finite order abs(det R) -> exact prime factorization",
            "target_values_are_inputs": False,
            "current_matrix": None,
        },
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
