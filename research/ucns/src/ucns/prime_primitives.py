# === MODULE_BUILD ===
# id: ucns_prime_primitives_p7_p5
#   module_name: prime_primitives
#   module_kind: experiment
#   summary: constructs P7 first and P5 second as direct exact projected carrier complexes, preserves n-ary hypernodes, and separates arithmetic primality from UCNS closed-primitive standing
#   owner: Erin Spencer
#   public_surface: RelationKind, Hypernode, PrimePrimitive, is_arithmetic_prime, cycle_rank, dyadic_boundary, build_prime_seven, build_prime_five, family_certificate
#   internal_surface: exact pair-distance ledgers, hypernode reconciliation, restriction counts, deterministic hashing
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_primitives.py
#   rollout: nonselecting P7-first research artifact; lower-prime forms are restrictions, not construction parts
#   rollback: remove this module, its test, and documentation
#   requires: none
#   since: 2026-08-11
#   unresolved: P2 ontology, P3 artifact, smooth Möbius lift, phase field, physical event semantics, braid topology, spectral operator, zeta correspondence
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: prime_arithmetic_geometry_firewall
#   given: arithmetic primality and UCNS primitive standing are evaluated
#   then: the predicates remain separate and two remains arithmetic-prime
#   class: doctrine
#   since: 2026-08-11
#
# id: prime_two_cycle_boundary
#   given: K2 is tested under a closure axiom requiring a nontrivial relational cycle
#   then: its cycle rank is zero and it conditionally fails closed-primitive standing without changing arithmetic primality
#   class: doctrine
#   since: 2026-08-11
#
# id: prime_p7_direct_exact_signature
#   given: P7 is constructed directly from one center plus six outer carriers
#   then: twenty-one pairs, thirty-nine projected pair events, and arity spectrum two-six three-six six-one reconcile exactly
#   class: correctness
#   since: 2026-08-11
#
# id: prime_p7_uniform_structural_relation
#   given: P7 spoke and adjacent-rim separations are measured
#   then: all twelve structural edges are unit-vesica relations and q equals six is the unique equal-spoke-rim ring order
#   class: correctness
#   since: 2026-08-11
#
# id: prime_p5_direct_exact_signature
#   given: P5 is constructed directly from one center plus four outer carriers
#   then: ten pairs, eighteen projected pair events, and arity spectrum two-twelve four-one reconcile exactly
#   class: correctness
#   since: 2026-08-11
#
# id: prime_restrictions_follow_construction
#   given: dyadic and triadic readouts are reported
#   then: they are derived restrictions and never treated as construction lineage
#   class: doctrine
#   since: 2026-08-11
# === END CONTRACTS ===

"""Direct P7 and P5 projected prime-primitive research candidates.

Standard arithmetic primality is not redefined.  The exact conditional result
about two is only that K2 has cycle rank zero and fails a *declared* closure
criterion requiring a nontrivial relational cycle.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import Enum
import hashlib
import itertools
import json
import math

SOURCE_NAME = "Möbius Strips and Quantum Geometry.txt"
SOURCE_SHA256 = "dc3a94ca5070ffff8f2a246f48db77192b08f521e721bc7c2a011aa05ddeb9a1"
SCHEMA_VERSION = "0.1.0"


class PrimitiveError(ValueError):
    pass


class RelationKind(str, Enum):
    UNIT_VESICA = "unit-vesica"
    SECANT = "secant"
    TANGENT = "tangent"


def is_arithmetic_prime(n: int) -> bool:
    if isinstance(n, bool) or not isinstance(n, int):
        raise PrimitiveError("n must be an integer and nonboolean")
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    return all(n % d for d in range(3, math.isqrt(n) + 1, 2))


def cycle_rank(vertices: int, edges: int, components: int = 1) -> int:
    rank = edges - vertices + components
    if min(vertices, edges, components, rank) < 0:
        raise PrimitiveError("invalid graph counts")
    return rank


@dataclass(frozen=True, slots=True)
class Hypernode:
    node_id: str
    point: tuple[str, str]
    carriers: tuple[str, ...]

    @property
    def arity(self) -> int:
        return len(self.carriers)

    @property
    def pair_count(self) -> int:
        return self.arity * (self.arity - 1) // 2


@dataclass(frozen=True, slots=True)
class PrimePrimitive:
    prime: int
    name: str
    outer_order: int
    pair_distance_squared: tuple[tuple[str, str, int], ...]
    hypernodes: tuple[Hypernode, ...]
    structural_pairs: tuple[tuple[str, str], ...]
    unit_triangles: tuple[tuple[str, str, str], ...]

    def __post_init__(self) -> None:
        if not is_arithmetic_prime(self.prime) or self.outer_order != self.prime - 1:
            raise PrimitiveError("invalid prime label or outer order")
        labels = {"C", *(f"R{i}" for i in range(self.outer_order))}
        if len(self.pair_distance_squared) != self.prime * (self.prime - 1) // 2:
            raise PrimitiveError("complete pair ledger required")
        if len({tuple(sorted((a, b))) for a, b, _ in self.pair_distance_squared}) != len(self.pair_distance_squared):
            raise PrimitiveError("duplicate pair")
        if any(a not in labels or b not in labels for a, b, _ in self.pair_distance_squared):
            raise PrimitiveError("unknown carrier")
        if any(tuple(sorted(node.carriers)) != node.carriers for node in self.hypernodes):
            raise PrimitiveError("hypernode carriers must be sorted")
        for a, b, distance2 in self.pair_distance_squared:
            expected = 2 if distance2 < 4 else 1
            observed = sum(a in node.carriers and b in node.carriers for node in self.hypernodes)
            if observed != expected:
                raise PrimitiveError(f"pair ledger mismatch for {a},{b}")
        if self.pair_event_count != self.hypernode_pair_count:
            raise PrimitiveError("global event ledgers disagree")
        origin = [node for node in self.hypernodes if node.point == ("0", "0")]
        if len(origin) != 1 or origin[0].arity != self.outer_order:
            raise PrimitiveError("origin must be one outer-orbit hypernode")

    @property
    def relation_counts(self) -> dict[str, int]:
        counts = Counter(
            RelationKind.UNIT_VESICA.value if d2 == 1
            else RelationKind.SECANT.value if d2 < 4
            else RelationKind.TANGENT.value
            for _, _, d2 in self.pair_distance_squared
        )
        return {kind.value: counts[kind.value] for kind in RelationKind}

    @property
    def pair_event_count(self) -> int:
        return sum(2 if d2 < 4 else 1 for _, _, d2 in self.pair_distance_squared)

    @property
    def hypernode_pair_count(self) -> int:
        return sum(node.pair_count for node in self.hypernodes)

    @property
    def arity_spectrum(self) -> dict[str, int]:
        counts = Counter(node.arity for node in self.hypernodes)
        return {str(k): counts[k] for k in sorted(counts)}

    @property
    def unit_pairs(self) -> tuple[tuple[str, str], ...]:
        return tuple((a, b) for a, b, d2 in self.pair_distance_squared if d2 == 1)

    @property
    def structural_cycle_rank(self) -> int:
        return cycle_rank(self.prime, len(self.structural_pairs))

    def payload(self) -> dict[str, object]:
        result: dict[str, object] = {
            "prime": self.prime,
            "arithmetic_prime": True,
            "ucns_standing": "direct-projected-candidate",
            "name": self.name,
            "carrier_count": self.prime,
            "outer_order": self.outer_order,
            "relation_counts": self.relation_counts,
            "pair_event_count": self.pair_event_count,
            "hypernode_count": len(self.hypernodes),
            "arity_spectrum": self.arity_spectrum,
            "origin": {
                "arity": self.outer_order,
                "pairwise_flattening": self.outer_order * (self.outer_order - 1) // 2,
                "standing": "one projected n-ary hypernode",
            },
            "structural_cycle_rank": self.structural_cycle_rank,
            "unit_pair_restrictions": len(self.unit_pairs),
            "unit_triangle_restrictions": len(self.unit_triangles),
            "construction_lineage": "direct from prime cardinality and outer orbit; restrictions derived afterward",
            "mobius_lift": "unresolved; one-turn reversal and two-turn return required",
        }
        canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
        result["payload_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
        return result


def dyadic_boundary() -> dict[str, object]:
    return {
        "number": 2,
        "arithmetic_prime": is_arithmetic_prime(2),
        "relation_graph": "K2",
        "cycle_rank": cycle_rank(2, 1),
        "has_nontrivial_relational_cycle": False,
        "mobius_two_turn_return": True,
        "conditional_result": "not a closed primitive if positive relational cycle rank is required",
        "proof_boundary": "not a proof that 2 is nonprime in conventional arithmetic",
    }


def _pairs(outer_order: int, distances: dict[int, int]) -> tuple[tuple[str, str, int], ...]:
    labels = ("C", *(f"R{i}" for i in range(outer_order)))
    rows = []
    for a, b in itertools.combinations(labels, 2):
        if a == "C":
            d2 = 1
        else:
            i, j = int(a[1:]), int(b[1:])
            step = min(abs(i - j), outer_order - abs(i - j))
            d2 = distances[step]
        rows.append((a, b, d2))
    return tuple(rows)


def build_prime_seven() -> PrimePrimitive:
    nodes = (
        Hypernode("P7_N00", ("0", "-sqrt(3)"), ("R4", "R5")),
        Hypernode("P7_N01", ("-3/2", "-sqrt(3)/2"), ("R3", "R4")),
        Hypernode("P7_N02", ("-1/2", "-sqrt(3)/2"), ("C", "R3", "R5")),
        Hypernode("P7_N03", ("1/2", "-sqrt(3)/2"), ("C", "R0", "R4")),
        Hypernode("P7_N04", ("3/2", "-sqrt(3)/2"), ("R0", "R5")),
        Hypernode("P7_N05", ("-1", "0"), ("C", "R2", "R4")),
        Hypernode("P7_N06", ("0", "0"), ("R0", "R1", "R2", "R3", "R4", "R5")),
        Hypernode("P7_N07", ("1", "0"), ("C", "R1", "R5")),
        Hypernode("P7_N08", ("-3/2", "sqrt(3)/2"), ("R2", "R3")),
        Hypernode("P7_N09", ("-1/2", "sqrt(3)/2"), ("C", "R1", "R3")),
        Hypernode("P7_N10", ("1/2", "sqrt(3)/2"), ("C", "R0", "R2")),
        Hypernode("P7_N11", ("3/2", "sqrt(3)/2"), ("R0", "R1")),
        Hypernode("P7_N12", ("0", "sqrt(3)"), ("R1", "R2")),
    )
    structural = tuple(("C", f"R{i}") for i in range(6)) + tuple((f"R{i}", f"R{(i + 1) % 6}") for i in range(6))
    triangles = tuple(tuple(sorted(("C", f"R{i}", f"R{(i + 1) % 6}"))) for i in range(6))
    return PrimePrimitive(7, "Möbius prime-seven Seed projected primitive", 6, _pairs(6, {1: 1, 2: 3, 3: 4}), nodes, structural, triangles)


def build_prime_five() -> PrimePrimitive:
    nodes = (
        Hypernode("P5_N00", ("-1", "-1"), ("R2", "R3")),
        Hypernode("P5_N01", ("1", "-1"), ("R0", "R3")),
        Hypernode("P5_N02", ("-1/2", "-sqrt(3)/2"), ("C", "R2")),
        Hypernode("P5_N03", ("1/2", "-sqrt(3)/2"), ("C", "R0")),
        Hypernode("P5_N04", ("-sqrt(3)/2", "-1/2"), ("C", "R3")),
        Hypernode("P5_N05", ("sqrt(3)/2", "-1/2"), ("C", "R3")),
        Hypernode("P5_N06", ("0", "0"), ("R0", "R1", "R2", "R3")),
        Hypernode("P5_N07", ("-sqrt(3)/2", "1/2"), ("C", "R1")),
        Hypernode("P5_N08", ("sqrt(3)/2", "1/2"), ("C", "R1")),
        Hypernode("P5_N09", ("-1/2", "sqrt(3)/2"), ("C", "R2")),
        Hypernode("P5_N10", ("1/2", "sqrt(3)/2"), ("C", "R0")),
        Hypernode("P5_N11", ("-1", "1"), ("R1", "R2")),
        Hypernode("P5_N12", ("1", "1"), ("R0", "R1")),
    )
    structural = tuple(("C", f"R{i}") for i in range(4)) + tuple((f"R{i}", f"R{(i + 1) % 4}") for i in range(4))
    return PrimePrimitive(5, "Möbius prime-five central-ring projected primitive", 4, _pairs(4, {1: 2, 2: 4}), nodes, structural, ())


def family_certificate() -> dict[str, object]:
    p7, p5 = build_prime_seven(), build_prime_five()
    result: dict[str, object] = {
        "schema": "ucns.prime-primitives",
        "schema_version": SCHEMA_VERSION,
        "authority": "Erin Spencer",
        "selection_effect": "none",
        "research_order": [7, 5],
        "source": {"name": SOURCE_NAME, "sha256": SOURCE_SHA256, "lines": [5, 6, 13, 14, 15, 16, 17]},
        "dyadic_boundary": dyadic_boundary(),
        "p7": p7.payload(),
        "p5": p5.payload(),
        "p7_unique_equal_relation_theorem": {
            "equation": "2*sin(pi/q)=1",
            "integer_domain": "q>=3",
            "unique_solution": 6,
            "carrier_cardinality": 7,
        },
        "next": "construct a P7-native seam-compatible phase and lift on carriers and hypernodes; lift P5 afterward under the same protocol",
        "nonclaims": ["no arithmetic redefinition", "no full 3D Möbius embedding", "no zeta theorem", "no Riemann-hypothesis proof"],
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["payload_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return result
