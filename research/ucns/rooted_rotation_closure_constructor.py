"""Explicit-assumption completion of the UCNS based-traversal fields.

The existing ordered-return groupoid supplies typed complete-return loops but
does not select an origin attachment, chirality, rotation system, marked dart,
or face closure.  This experiment adds those data as *named candidate
assumptions* and constructs the resulting rooted oriented ribbon map.

Observed gonol cardinalities are deliberately absent from this module.  A
separate gate freezes this source and its assumptions before comparing any
arithmetic readout with observations.
"""

# === MODULE_BUILD ===
# id: ucns_rooted_rotation_closure_constructor
#   module_name: rooted_rotation_closure_constructor
#   module_kind: experiment
#   summary: completes the five based-traversal fields under explicit candidate assumptions and derives exact ribbon-face closures without treating provenance order as selected UCNS canon
#   owner: The Interdependency
#   public_surface: ConstructorError, PrimeRoleOccurrence, OrderedRelation, RetainedStructure, TraversalAssumptions, RootedRibbonCertificate, retained_structure, construct, frozen_assumptions, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: exact prime validation, coefficient construction, dart involution, cyclic rotation, face permutation, rational rank, finite-cokernel order
#   auth_boundary: none
#   storage_boundary: read-only at runtime; deterministic receipt output only through caller
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_rooted_rotation_closure_constructor.py
#   rollout: stack-local pre-ratification geometry experiment only; no UCNS canon, PCEA runtime, selector, or cryptographic promotion
#   rollback: remove this module, its tests, report, and receipts
#   requires: ucns_ordered_complete_return_groupoid, ucns_origin_attachment_basepoint_symmetry, gonol-build construction discipline
#   since: 2026-09-18
#   unresolved: canonical origin attachment; geometry-selected chirality; selected rotation system; intrinsic marked dart; torsion-producing global presentation; prime successor selector
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: rooted_constructor_preserves_retained_structure
#   given: prime-role occurrences with ordered mutually-constraining relations and provenance are admitted
#   then: the full coefficient vector, repeated occurrences, relation order, recoverable constituents, and provenance remain in the certificate without scalar flattening
#   class: doctrine
#
# id: rooted_constructor_names_every_added_assumption
#   given: a based traversal is constructed
#   then: attachment, direction, rotation, marked-dart, and closure choices are explicit fields and no field is reported as canon-derived
#   class: safety
#
# id: rooted_constructor_uses_actual_complete_return_geometry
#   given: k role occurrences are bound to the existing ordered return groupoid
#   then: every role binds exactly one native two-turn loop generator and the ribbon darts are the two oriented germs of those generators
#   class: correctness
#
# id: rooted_constructor_closes_by_face_permutation
#   given: dart reversal alpha and oriented cyclic rotation sigma
#   then: closure is the complete orbit decomposition of phi=sigma-after-alpha, with the marked orbit distinguished and every dart visited once
#   class: correctness
#
# id: rooted_constructor_exposes_rotation_ambiguity
#   given: paired-germs and sign-block rotations receive the same retained input and other assumptions
#   then: both are coherent ribbon maps but can produce different face words and topology, so earlier fields do not select one rotation
#   class: falsification
#
# id: rooted_constructor_does_not_manufacture_prime_selector
#   given: a ribbon cellular boundary matrix is derived
#   then: only its exact finite-cokernel order or absence is reported; no hash, ordinal, target, or supplied next prime becomes a successor
#   class: safety
#
# id: rooted_constructor_replays_byte_identically
#   given: identical retained input and frozen assumptions
#   then: certificate and receipt bytes replay exactly
#   class: correctness
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from math import gcd
from pathlib import Path
from typing import Any, Iterable

import ordered_complete_return_groupoid as return_groupoid


SCHEMA_ID = "the-interdependency.stack-research.ucns.rooted-rotation-closure-constructor"
SCHEMA_VERSION = "0.1.0"
STANDING = "stack-local-explicit-assumption-geometry-candidate"

NATIVE_TRANSITION_LAW = "(t,epsilon)~(t+n,(-1)^n epsilon)"
FACE_SUCCESSOR_LAW = "phi(d)=sigma(alpha(d))"

PAIRED_GERMS = "paired-germs"
SIGN_BLOCKS = "sign-blocks"

NONCLAIMS = (
    "not UCNS canon or a canon-authorized origin attachment",
    "not a geometry-selected chirality, rotation system, or marked dart",
    "not a prime-role or successor selector",
    "not a cryptographic primitive or security result",
    "not permission to infer geometry from hashes, ordinals, or observed cardinalities",
)


class ConstructorError(ValueError):
    """Raised when retained structure or ribbon assumptions are incomplete."""


def _text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ConstructorError(f"{field} must be non-empty text")
    return value


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def _is_prime(value: int) -> bool:
    """Deterministic Miller-Rabin for the unsigned 64-bit domain."""

    if isinstance(value, bool) or not isinstance(value, int) or value < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    if value in small:
        return True
    if any(value % prime == 0 for prime in small):
        return False
    odd = value - 1
    power = 0
    while odd % 2 == 0:
        power += 1
        odd //= 2
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % value == 0:
            continue
        witness = pow(base, odd, value)
        if witness in (1, value - 1):
            continue
        for _ in range(power - 1):
            witness = witness * witness % value
            if witness == value - 1:
                break
        else:
            return False
    return True


def _coefficients(primes: Iterable[int]) -> tuple[int, ...]:
    coefficients = [1]
    for prime in primes:
        updated = coefficients + [0]
        for degree in range(1, len(updated)):
            updated[degree] += prime * coefficients[degree - 1]
        coefficients = updated
    return tuple(coefficients)


def _factor_integer(value: int) -> tuple[tuple[int, int], ...]:
    if value < 1:
        raise ConstructorError("finite order must be positive")
    remaining = value
    factors: list[tuple[int, int]] = []
    divisor = 2
    while divisor * divisor <= remaining:
        exponent = 0
        while remaining % divisor == 0:
            remaining //= divisor
            exponent += 1
        if exponent:
            factors.append((divisor, exponent))
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors.append((remaining, 1))
    return tuple(factors)


@dataclass(frozen=True, slots=True)
class PrimeRoleOccurrence:
    """One occurrence-addressed supplied prime role bound to one return loop."""

    occurrence_id: str
    prime: int
    geometry_relation_id: str
    provenance: tuple[str, ...]

    def __post_init__(self) -> None:
        _text(self.occurrence_id, "occurrence_id")
        _text(self.geometry_relation_id, "geometry_relation_id")
        if not _is_prime(self.prime):
            raise ConstructorError("prime role value must be a nonboolean 64-bit prime")
        if not self.provenance or any(not isinstance(item, str) or not item.strip() for item in self.provenance):
            raise ConstructorError("role provenance is required")

    def to_payload(self) -> dict[str, Any]:
        return {
            "occurrence_id": self.occurrence_id,
            "prime": self.prime,
            "geometry_relation_id": self.geometry_relation_id,
            "provenance": list(self.provenance),
        }


@dataclass(frozen=True, slots=True)
class OrderedRelation:
    """An explicitly declared, identity-bearing ordered relation."""

    relation_id: str
    kind: str
    participant_occurrences: tuple[str, ...]
    provenance: tuple[str, ...]

    def __post_init__(self) -> None:
        _text(self.relation_id, "relation_id")
        if self.kind != "mutually-constraining-role-cycle":
            raise ConstructorError("relation kind is not admitted by this candidate")
        if not self.participant_occurrences:
            raise ConstructorError("ordered relation requires participants")
        if len(set(self.participant_occurrences)) != len(self.participant_occurrences):
            raise ConstructorError("one relation cannot repeat an occurrence address")
        if any(not isinstance(item, str) or not item.strip() for item in self.participant_occurrences):
            raise ConstructorError("relation participants require occurrence addresses")
        if not self.provenance or any(not isinstance(item, str) or not item.strip() for item in self.provenance):
            raise ConstructorError("relation provenance is required")

    def to_payload(self) -> dict[str, Any]:
        return {
            "relation_id": self.relation_id,
            "kind": self.kind,
            "participant_occurrences": list(self.participant_occurrences),
            "provenance": list(self.provenance),
        }


@dataclass(frozen=True, slots=True)
class RetainedStructure:
    """R=(C_k(t), relations, provenance), retaining occurrence multiplicity."""

    structure_id: str
    roles: tuple[PrimeRoleOccurrence, ...]
    relations: tuple[OrderedRelation, ...]
    provenance: tuple[str, ...]

    def __post_init__(self) -> None:
        _text(self.structure_id, "structure_id")
        if not self.roles:
            raise ConstructorError("retained structure requires at least one role")
        occurrence_ids = tuple(role.occurrence_id for role in self.roles)
        if len(set(occurrence_ids)) != len(occurrence_ids):
            raise ConstructorError("role occurrence addresses must be unique")
        geometry_ids = tuple(role.geometry_relation_id for role in self.roles)
        if len(set(geometry_ids)) != len(geometry_ids):
            raise ConstructorError("each occurrence must bind a distinct return loop")
        if not self.relations:
            raise ConstructorError("retained structure requires explicit relations")
        if len({relation.relation_id for relation in self.relations}) != len(self.relations):
            raise ConstructorError("relation ids must be unique")
        known = set(occurrence_ids)
        for relation in self.relations:
            if any(item not in known for item in relation.participant_occurrences):
                raise ConstructorError("relation references an unknown occurrence")
        if not self.provenance or any(not isinstance(item, str) or not item.strip() for item in self.provenance):
            raise ConstructorError("structure provenance is required")

    @property
    def coefficients(self) -> tuple[int, ...]:
        return _coefficients(role.prime for role in self.roles)

    @property
    def complete_product(self) -> int:
        return self.coefficients[-1]

    @property
    def c_at_one(self) -> int:
        return sum(self.coefficients)

    def relation(self, relation_id: str) -> OrderedRelation:
        result = next((item for item in self.relations if item.relation_id == relation_id), None)
        if result is None:
            raise ConstructorError("rotation relation is not retained")
        return result

    def role(self, occurrence_id: str) -> PrimeRoleOccurrence:
        result = next((item for item in self.roles if item.occurrence_id == occurrence_id), None)
        if result is None:
            raise ConstructorError("unknown role occurrence")
        return result

    def to_payload(self) -> dict[str, Any]:
        return {
            "structure_id": self.structure_id,
            "coefficient_polynomial": {
                "coefficients_low_to_high": list(self.coefficients),
                "complete_product": self.complete_product,
                "C_at_1_lossy_projection": self.c_at_one,
            },
            "roles": [role.to_payload() for role in self.roles],
            "relations": [relation.to_payload() for relation in self.relations],
            "provenance": list(self.provenance),
        }

    @property
    def digest(self) -> str:
        return sha256(_canonical_bytes(self.to_payload())).hexdigest()


@dataclass(frozen=True, slots=True, order=True)
class Dart:
    occurrence_id: str
    sign: int

    def __post_init__(self) -> None:
        _text(self.occurrence_id, "dart occurrence_id")
        if self.sign not in (-1, 1):
            raise ConstructorError("dart sign must be plus or minus one")

    def reversed(self) -> "Dart":
        return Dart(self.occurrence_id, -self.sign)

    @property
    def id(self) -> str:
        return f"{self.occurrence_id}:{'+' if self.sign == 1 else '-'}"

    def to_payload(self) -> list[Any]:
        return [self.occurrence_id, self.sign]


@dataclass(frozen=True, slots=True)
class TraversalAssumptions:
    """Every non-derived field required to turn the groupoid into a ribbon map."""

    assumption_id: str
    origin_attachment: str
    direction: str
    rotation_policy: str
    marked_dart_policy: str
    closure_policy: str
    chirality: int = 1

    def __post_init__(self) -> None:
        _text(self.assumption_id, "assumption_id")
        if self.origin_attachment != "structural-null-to-model-positive-base-object":
            raise ConstructorError("origin attachment is not an admitted explicit candidate")
        if self.direction != "native-two-turn-positive-trace":
            raise ConstructorError("direction must retain the native positive two-turn trace")
        if self.rotation_policy not in (PAIRED_GERMS, SIGN_BLOCKS):
            raise ConstructorError("unknown rotation policy")
        if self.marked_dart_policy != "first-declared-role-positive-germ":
            raise ConstructorError("marked dart policy is incomplete")
        if self.closure_policy != "fill-all-oriented-ribbon-face-orbits":
            raise ConstructorError("closure policy is incomplete")
        if self.chirality not in (-1, 1):
            raise ConstructorError("chirality must be plus or minus one")

    def to_payload(self) -> dict[str, Any]:
        return {
            "assumption_id": self.assumption_id,
            "origin_attachment": self.origin_attachment,
            "direction": self.direction,
            "chirality": self.chirality,
            "rotation_policy": self.rotation_policy,
            "marked_dart_policy": self.marked_dart_policy,
            "closure_policy": self.closure_policy,
            "selection_basis": "explicit candidate assumptions; not canon-derived",
        }


@lru_cache(maxsize=1)
def frozen_assumptions() -> tuple[TraversalAssumptions, ...]:
    common = {
        "origin_attachment": "structural-null-to-model-positive-base-object",
        "direction": "native-two-turn-positive-trace",
        "marked_dart_policy": "first-declared-role-positive-germ",
        "closure_policy": "fill-all-oriented-ribbon-face-orbits",
        "chirality": 1,
    }
    return (
        TraversalAssumptions(
            assumption_id="rooted-ribbon.paired-germs.v0",
            rotation_policy=PAIRED_GERMS,
            **common,
        ),
        TraversalAssumptions(
            assumption_id="rooted-ribbon.sign-blocks.v0",
            rotation_policy=SIGN_BLOCKS,
            **common,
        ),
    )


def retained_structure(
    structure_id: str,
    primes: tuple[int, ...],
    *,
    provenance: tuple[str, ...],
    participant_order: tuple[int, ...] | None = None,
) -> RetainedStructure:
    """Bind supplied roles to the existing ordered-return geometry.

    This function is intentionally not a prime selector.  ``primes`` are
    caller-supplied diagnostic roles, and the receipt retains that boundary.
    """

    groupoid = return_groupoid.build_ordered_return_groupoid(len(primes))
    roles = tuple(
        PrimeRoleOccurrence(
            occurrence_id=f"{structure_id}.role-{index}",
            prime=prime,
            geometry_relation_id=generator.relation_id,
            provenance=provenance + (f"supplied-prime-role-index:{index}",),
        )
        for index, (prime, generator) in enumerate(zip(primes, groupoid.generators, strict=True), start=1)
    )
    indices = participant_order or tuple(range(1, len(roles) + 1))
    if tuple(sorted(indices)) != tuple(range(1, len(roles) + 1)):
        raise ConstructorError("participant_order must be a permutation of role ordinals")
    participants = tuple(roles[index - 1].occurrence_id for index in indices)
    relation = OrderedRelation(
        relation_id=f"{structure_id}.mutual-role-cycle",
        kind="mutually-constraining-role-cycle",
        participant_occurrences=participants,
        provenance=provenance + ("explicit-identity-bearing-participant-order",),
    )
    return RetainedStructure(structure_id, roles, (relation,), provenance)


def _matrix_rank(matrix: tuple[tuple[int, ...], ...], columns: int) -> int:
    if columns <= 0:
        return 0
    work = [[Fraction(value) for value in row] for row in matrix]
    rank = 0
    for column in range(columns):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        divisor = work[rank][column]
        work[rank] = [value / divisor for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            multiple = work[row][column]
            work[row] = [
                value - multiple * pivot_value
                for value, pivot_value in zip(work[row], work[rank], strict=True)
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


def _determinant(matrix: tuple[tuple[int, ...], ...]) -> int:
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ConstructorError("determinant requires a square matrix")
    if size == 1:
        return matrix[0][0]
    work = [list(row) for row in matrix]
    sign = 1
    previous = 1
    for index in range(size - 1):
        if work[index][index] == 0:
            swap = next((row for row in range(index + 1, size) if work[row][index]), None)
            if swap is None:
                return 0
            work[index], work[swap] = work[swap], work[index]
            sign *= -1
        pivot = work[index][index]
        for row in range(index + 1, size):
            for column in range(index + 1, size):
                numerator = work[row][column] * pivot - work[row][index] * work[index][column]
                if numerator % previous:
                    raise ConstructorError("fraction-free determinant division failed")
                work[row][column] = numerator // previous
        previous = pivot
        for row in range(index + 1, size):
            work[row][index] = 0
    return sign * work[-1][-1]


def _finite_cokernel_order(
    matrix: tuple[tuple[int, ...], ...], columns: int
) -> tuple[int, int | None]:
    rank = _matrix_rank(matrix, columns)
    if rank < columns:
        return rank, None
    minors = (
        abs(_determinant(tuple(matrix[index] for index in row_indices)))
        for row_indices in combinations(range(len(matrix)), columns)
    )
    order = 0
    for minor in minors:
        order = gcd(order, minor)
    if order == 0:
        raise ConstructorError("full-rank presentation unexpectedly has zero maximal minors")
    return rank, order


@dataclass(frozen=True, slots=True)
class RootedRibbonCertificate:
    structure: RetainedStructure
    assumptions: TraversalAssumptions
    base_object: str
    relation_id: str
    rotation_cycle: tuple[Dart, ...]
    alpha: tuple[tuple[Dart, Dart], ...]
    sigma: tuple[tuple[Dart, Dart], ...]
    face_successor: tuple[tuple[Dart, Dart], ...]
    face_cycles: tuple[tuple[Dart, ...], ...]
    marked_dart: Dart
    marked_face_index: int
    genus: int
    cellular_boundary_matrix: tuple[tuple[int, ...], ...]
    cellular_boundary_rank: int
    finite_cokernel_order: int | None
    finite_cokernel_factorization: tuple[tuple[int, int], ...]

    @property
    def traversal_word(self) -> tuple[Dart, ...]:
        return self.face_cycles[self.marked_face_index]

    @property
    def digest(self) -> str:
        return sha256(_canonical_bytes(self.to_payload())).hexdigest()

    def to_payload(self) -> dict[str, Any]:
        return {
            "standing": STANDING,
            "structure": self.structure.to_payload(),
            "structure_sha256": self.structure.digest,
            "assumptions": self.assumptions.to_payload(),
            "five_field_audit": {
                "origin_attachment": {
                    "value": ["ucns.structural-null", self.base_object],
                    "status": "EXPLICIT_CANDIDATE_ASSUMPTION",
                },
                "directed_tangent_or_chirality": {
                    "value": self.assumptions.direction,
                    "chirality": self.assumptions.chirality,
                    "native_transition_law": NATIVE_TRANSITION_LAW,
                    "status": "EXPLICIT_CANDIDATE_ASSUMPTION_USING_EXISTING_TRACE",
                },
                "rotation_system": {
                    "policy": self.assumptions.rotation_policy,
                    "cycle": [dart.to_payload() for dart in self.rotation_cycle],
                    "status": "CONSTRUCTED_FROM_EXPLICIT_ORDER_ASSUMPTION",
                },
                "marked_outgoing_dart": {
                    "dart": self.marked_dart.to_payload(),
                    "status": "SELECTED_BY_EXPLICIT_LINEAR_START_ASSUMPTION",
                },
                "closure_rule": {
                    "law": FACE_SUCCESSOR_LAW,
                    "policy": self.assumptions.closure_policy,
                    "status": "IMPLEMENTED_FROM_ALPHA_AND_SIGMA",
                },
            },
            "base_object": self.base_object,
            "rotation_relation_id": self.relation_id,
            "dart_involution": [
                [source.to_payload(), target.to_payload()] for source, target in self.alpha
            ],
            "rotation_successor": [
                [source.to_payload(), target.to_payload()] for source, target in self.sigma
            ],
            "face_successor": [
                [source.to_payload(), target.to_payload()]
                for source, target in self.face_successor
            ],
            "closure": {
                "marked_face_index": self.marked_face_index,
                "marked_traversal_word": [dart.to_payload() for dart in self.traversal_word],
                "face_cycles": [
                    [dart.to_payload() for dart in cycle] for cycle in self.face_cycles
                ],
                "all_darts_visited_once": sum(map(len, self.face_cycles)) == len(self.rotation_cycle),
                "face_count": len(self.face_cycles),
                "orientable_genus": self.genus,
            },
            "cellular_readout": {
                "basis_occurrences": [role.occurrence_id for role in self.structure.roles],
                "boundary_matrix": [list(row) for row in self.cellular_boundary_matrix],
                "boundary_rank": self.cellular_boundary_rank,
                "finite_cokernel_order": self.finite_cokernel_order,
                "factorization": [
                    {"prime": prime, "exponent": exponent}
                    for prime, exponent in self.finite_cokernel_factorization
                ],
                "successor_selector": None,
                "supplied_next_prime": None,
            },
            "nonclaims": list(NONCLAIMS),
        }


def construct(
    structure: RetainedStructure,
    assumptions: TraversalAssumptions,
    *,
    rotation_relation_id: str,
) -> RootedRibbonCertificate:
    """Construct the exact ribbon closure under the supplied named assumptions."""

    if not isinstance(structure, RetainedStructure):
        raise ConstructorError("structure must be a RetainedStructure")
    if not isinstance(assumptions, TraversalAssumptions):
        raise ConstructorError("assumptions must be TraversalAssumptions")
    relation = structure.relation(rotation_relation_id)
    if set(relation.participant_occurrences) != {role.occurrence_id for role in structure.roles}:
        raise ConstructorError("rotation relation must contain every role occurrence exactly once")

    groupoid = return_groupoid.build_ordered_return_groupoid(len(structure.roles))
    if {role.geometry_relation_id for role in structure.roles} != {
        generator.relation_id for generator in groupoid.generators
    }:
        raise ConstructorError("role-to-return-loop binding does not match the existing groupoid")
    for role in structure.roles:
        path = groupoid.complete_loop_path(role.geometry_relation_id)
        if not path.is_loop or len(path.steps) != 2:
            raise ConstructorError("role is not bound to one native complete-return loop")

    ordered = relation.participant_occurrences
    if assumptions.rotation_policy == PAIRED_GERMS:
        rotation = tuple(
            Dart(occurrence_id, sign)
            for occurrence_id in ordered
            for sign in (1, -1)
        )
    else:
        rotation = tuple(Dart(item, 1) for item in ordered) + tuple(
            Dart(item, -1) for item in ordered
        )

    alpha_map = {dart: dart.reversed() for dart in rotation}
    sigma_map = {
        dart: rotation[(index + assumptions.chirality) % len(rotation)]
        for index, dart in enumerate(rotation)
    }
    phi_map = {dart: sigma_map[alpha_map[dart]] for dart in rotation}
    marked = Dart(ordered[0], 1)

    face_cycles: list[tuple[Dart, ...]] = []
    unvisited = set(rotation)
    starts = [marked] + sorted(unvisited - {marked})
    for start in starts:
        if start not in unvisited:
            continue
        cycle: list[Dart] = []
        current = start
        while current in unvisited:
            unvisited.remove(current)
            cycle.append(current)
            current = phi_map[current]
        if current != start:
            raise ConstructorError("face successor did not close an orbit")
        face_cycles.append(tuple(cycle))
    if unvisited or sum(map(len, face_cycles)) != len(rotation):
        raise ConstructorError("face closure did not cover every dart exactly once")

    face_count = len(face_cycles)
    genus_numerator = 1 + len(structure.roles) - face_count
    if genus_numerator < 0 or genus_numerator % 2:
        raise ConstructorError("rotation system does not define an orientable one-vertex ribbon map")
    genus = genus_numerator // 2
    matrix = tuple(
        tuple(
            sum(dart.sign for dart in cycle if dart.occurrence_id == role.occurrence_id)
            for role in structure.roles
        )
        for cycle in face_cycles
    )
    rank, order = _finite_cokernel_order(matrix, len(structure.roles))
    factorization = _factor_integer(order) if order is not None else ()
    return RootedRibbonCertificate(
        structure=structure,
        assumptions=assumptions,
        base_object=groupoid.base_object,
        relation_id=relation.relation_id,
        rotation_cycle=rotation,
        alpha=tuple((dart, alpha_map[dart]) for dart in rotation),
        sigma=tuple((dart, sigma_map[dart]) for dart in rotation),
        face_successor=tuple((dart, phi_map[dart]) for dart in rotation),
        face_cycles=tuple(face_cycles),
        marked_dart=marked,
        marked_face_index=0,
        genus=genus,
        cellular_boundary_matrix=matrix,
        cellular_boundary_rank=rank,
        finite_cokernel_order=order,
        finite_cokernel_factorization=factorization,
    )


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def receipt_payload() -> dict[str, Any]:
    """Return target-free constructor identities and a synthetic replay fixture."""

    groupoid = return_groupoid.build_ordered_return_groupoid(2)
    synthetic = RetainedStructure(
        structure_id="synthetic-distinct-role-replay",
        roles=(
            PrimeRoleOccurrence(
                "synthetic.role-a",
                5,
                groupoid.generators[0].relation_id,
                ("synthetic-target-free-fixture",),
            ),
            PrimeRoleOccurrence(
                "synthetic.role-b",
                7,
                groupoid.generators[1].relation_id,
                ("synthetic-target-free-fixture",),
            ),
        ),
        relations=(
            OrderedRelation(
                "synthetic.mutual-role-cycle",
                "mutually-constraining-role-cycle",
                ("synthetic.role-a", "synthetic.role-b"),
                ("synthetic-target-free-fixture",),
            ),
        ),
        provenance=("synthetic-target-free-fixture",),
    )
    certificates = tuple(
        construct(
            synthetic,
            assumption,
            rotation_relation_id="synthetic.mutual-role-cycle",
        )
        for assumption in frozen_assumptions()
    )
    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "standing": STANDING,
        "producer_code_reference": _producer_code_reference(),
        "existing_geometry": {
            "module": "research/ucns/ordered_complete_return_groupoid.py",
            "receipt_sha256": return_groupoid.receipt_digest(),
            "native_transition_law": NATIVE_TRANSITION_LAW,
        },
        "frozen_assumptions": [item.to_payload() for item in frozen_assumptions()],
        "synthetic_fixture": synthetic.to_payload(),
        "candidate_certificates": [item.to_payload() for item in certificates],
        "rotation_ambiguity": {
            "same_retained_structure": certificates[0].structure.digest == certificates[1].structure.digest,
            "different_face_cycles": certificates[0].face_cycles != certificates[1].face_cycles,
            "different_genus": certificates[0].genus != certificates[1].genus,
            "selection": None,
        },
        "observed_successor_inputs": None,
        "next_prime_selector": None,
        "nonclaims": list(NONCLAIMS),
        "hmmm": [
            "the explicit attachment and linear start break symmetries but are assumptions, not recovered UCNS selection laws",
            "the retained ordered relation can drive a rotation candidate only if UCNS declares that order geometric rather than provenance-only",
            "ordinary oriented ribbon-face closure supplies no nontrivial finite prime successor in the synthetic fixture",
        ],
    }


def receipt_bytes(payload: dict[str, Any] | None = None) -> bytes:
    return _canonical_bytes(payload if payload is not None else receipt_payload()) + b"\n"


def receipt_digest(payload: dict[str, Any] | None = None) -> str:
    return sha256(receipt_bytes(payload)).hexdigest()


def main() -> None:
    payload = receipt_payload()
    envelope = {"receipt_sha256": receipt_digest(payload), "receipt": payload}
    print(json.dumps(envelope, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
