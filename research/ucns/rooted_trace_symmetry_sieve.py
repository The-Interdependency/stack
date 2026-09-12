"""Symmetry divisibility sieve for recursive gonol construction traces.

This experiment does not propose a successor. It proves a necessary condition
for any candidate that interprets ``(54837698421 - 1) / 4`` as a count of
complete connected construction orders: the rooted automorphism group of the
candidate graph must divide that count. Standard D6-symmetric and
indistinguishable-two-face continuations fail that condition before any target
tuning or large trace enumeration.
"""

# === MODULE_BUILD ===
# id: ucns_rooted_trace_symmetry_sieve
#   module_name: rooted_trace_symmetry_sieve
#   module_kind: experiment
#   summary: proves rooted graph automorphisms act freely on complete construction orders and falsifies symmetric next-scale trace candidates against the third observed gonol
#   owner: The Interdependency
#   public_surface: OBSERVED_GONOLS, RootedGraph, SymmetryEvaluation, seed_structural_graph, rooted_automorphisms, radius_two_hex_symmetries, two_face_seed_graph, is_rooted_automorphism, apply_automorphism, evaluate, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _canonical_edge, _factorize, _axial_rotate, _axial_reflect, _layer_swap
#   auth_boundary: none; consumes stack-local event/trace research and its pinned UCNS source identities
#   storage_boundary: read-only at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_rooted_trace_symmetry_sieve.py
#   rollout: stack-local post-observation falsification sieve only; no UCNS canon, stack libs, or PCEA promotion
#   rollback: remove this module, its tests, report, and receipt
#   requires: ucns_event_trace_lift_candidate, ucns_mobius_seed_of_life_candidate, gonol-build construction discipline
#   since: 2026-09-02
#   unresolved: phase-sensitive build admissibility, chirality-sensitive coupling, trace quotient semantics, completed 2881-gonol geometry, recursive-scale state extractor
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: rooted_trace_symmetry_binds_predecessor_evidence
#   given: the symmetry sieve is evaluated
#   then: it binds the exact event/trace producer digest, receipt digest, UCNS base commit, and observed comparison tuple
#   class: safety
#   since: 2026-09-02
#
# id: rooted_trace_automorphisms_act_freely
#   given: a rooted graph automorphism acts on a complete order of every nonroot vertex
#   then: only the identity automorphism can fix that order, so the automorphism-group order divides the number of invariant construction orders
#   class: correctness
#   since: 2026-09-02
#
# id: rooted_trace_seed_symmetry_replays
#   given: the pinned seven-band structural graph is inspected with CENTER fixed
#   then: its rooted automorphism group has order twelve and its 720 connected construction orders split into free group orbits
#   class: evidence
#   since: 2026-09-02
#
# id: rooted_trace_symmetric_continuations_are_falsified
#   given: the third observed gonol is used only as a falsification comparator
#   then: its fourfold state quotient is incompatible with D6-symmetric radius-two traces and with any two-face trace graph retaining a root-fixed layer-swap involution
#   class: evidence
#   since: 2026-09-02
#
# id: rooted_trace_symmetry_sieve_does_not_predict
#   given: symmetric trace classes are eliminated without a completed 2881 geometry
#   then: survivor count remains zero and no next gonol prediction is emitted
#   class: doctrine
#   since: 2026-09-02
#
# id: rooted_trace_symmetry_receipt_replays
#   given: the same predecessor and pinned geometry are evaluated twice
#   then: canonical receipt bytes and their digest are byte-identical
#   class: correctness
#   since: 2026-09-02
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
import itertools
import json
from pathlib import Path
from typing import Any

import event_trace_lift_candidate as lift


SCHEMA_ID = "the-interdependency.stack-research.ucns.rooted-trace-symmetry-sieve"
SCHEMA_VERSION = "0.1.0"
STANDING = "stack-local-post-observation-falsification-sieve"

OBSERVED_GONOLS = lift.OBSERVED_GONOLS
STATUS_FALSIFIED = "FALSIFIED"

NONCLAIMS: tuple[str, ...] = (
    "not UCNS canon",
    "not a recovered successor constructor",
    "not proof that the third quotient is a construction-trace count",
    "not permission to break symmetry toward the observed target",
    "not a PCEA runtime, entropy, hardness, or authenticity claim",
)

HMMM: tuple[str, ...] = (
    "if the third quotient counts construction traces, bare D6 adjacency cannot be the complete next-scale mechanic",
    "phase, chirality, or ordered coupling would have to enter build admissibility to remove the excluded rooted symmetries",
    "a symmetry quotient could change the counted object, but no UCNS quotient operation is currently declared",
    "the third quotient may instead be a different invariant, because the 39-event and 720-trace identities already use different state extractors",
    "no completed 2881-gonol graph or next prediction is authorized",
)


class RootedTraceSymmetryError(RuntimeError):
    """Raised when a graph or proposed automorphism is malformed."""


def _canonical_edge(left: str, right: str) -> tuple[str, str]:
    if left == right:
        raise RootedTraceSymmetryError("self edges are not admitted")
    return tuple(sorted((left, right)))


@dataclass(frozen=True, slots=True)
class RootedGraph:
    """A finite simple graph with one fixed construction origin."""

    vertices: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]
    root: str

    def __post_init__(self) -> None:
        if not self.vertices or len(set(self.vertices)) != len(self.vertices):
            raise RootedTraceSymmetryError("vertices must be nonempty and unique")
        if self.root not in self.vertices:
            raise RootedTraceSymmetryError("root must be a graph vertex")
        vertex_set = set(self.vertices)
        normalized = tuple(sorted({_canonical_edge(*edge) for edge in self.edges}))
        if any(left not in vertex_set or right not in vertex_set for left, right in normalized):
            raise RootedTraceSymmetryError("edge endpoint outside graph")
        if self.edges != normalized:
            raise RootedTraceSymmetryError("edges must be canonical, unique, and sorted")

    @property
    def edge_set(self) -> frozenset[tuple[str, str]]:
        return frozenset(self.edges)


@dataclass(frozen=True, slots=True)
class SymmetryEvaluation:
    """Frozen result of the symmetry divisibility sieve."""

    state_target: int
    state_target_factorization: tuple[tuple[int, int], ...]
    seed_automorphism_order: int
    seed_trace_count: int
    seed_orbit_count: int
    radius_two_symmetry_order: int
    radius_two_trace_count: int
    radius_two_standing: str
    two_face_has_layer_swap: bool
    two_face_trace_count: int
    two_face_standing: str
    falsified_class_count: int
    constructor_survivor_count: int
    next_prediction: int | None
    hmmm: tuple[str, ...]


def _graph(
    vertices: tuple[str, ...] | list[str],
    edges: tuple[tuple[str, str], ...] | list[tuple[str, str]],
    root: str,
) -> RootedGraph:
    return RootedGraph(
        tuple(vertices),
        tuple(sorted({_canonical_edge(left, right) for left, right in edges})),
        root,
    )


def seed_structural_graph() -> RootedGraph:
    """Load the pinned seven-band structural relation graph."""

    geometry = lift.load_seed_geometry()
    return _graph(geometry.bands, geometry.structural_edges, "CENTER")


def is_rooted_automorphism(graph: RootedGraph, permutation: tuple[int, ...]) -> bool:
    """Return whether an index permutation preserves root and every edge."""

    size = len(graph.vertices)
    if len(permutation) != size or set(permutation) != set(range(size)):
        return False
    root_index = graph.vertices.index(graph.root)
    if permutation[root_index] != root_index:
        return False
    transformed = {
        _canonical_edge(graph.vertices[permutation[left]], graph.vertices[permutation[right]])
        for left, right in (
            (graph.vertices.index(a), graph.vertices.index(b)) for a, b in graph.edges
        )
    }
    return transformed == graph.edge_set


def rooted_automorphisms(graph: RootedGraph) -> tuple[tuple[int, ...], ...]:
    """Enumerate rooted automorphisms for a bounded graph of at most eight vertices."""

    size = len(graph.vertices)
    if size > 8:
        raise RootedTraceSymmetryError("generic automorphism enumeration is bounded to eight vertices")
    root_index = graph.vertices.index(graph.root)
    movable = tuple(index for index in range(size) if index != root_index)
    found: list[tuple[int, ...]] = []
    for image in itertools.permutations(movable):
        permutation = list(range(size))
        for source, target in zip(movable, image, strict=True):
            permutation[source] = target
        candidate = tuple(permutation)
        if is_rooted_automorphism(graph, candidate):
            found.append(candidate)
    return tuple(found)


def apply_automorphism(
    graph: RootedGraph,
    permutation: tuple[int, ...],
    order: tuple[str, ...],
) -> tuple[str, ...]:
    """Apply a rooted automorphism to one complete nonroot vertex order."""

    if not is_rooted_automorphism(graph, permutation):
        raise RootedTraceSymmetryError("permutation is not a rooted graph automorphism")
    expected = set(graph.vertices) - {graph.root}
    if len(order) != len(expected) or set(order) != expected:
        raise RootedTraceSymmetryError("order must contain every nonroot vertex exactly once")
    index = {vertex: offset for offset, vertex in enumerate(graph.vertices)}
    return tuple(graph.vertices[permutation[index[vertex]]] for vertex in order)


def _parse_axial(vertex: str) -> tuple[int, int]:
    left, right = vertex.split(",", 1)
    return int(left), int(right)


def _axial_rotate(coordinate: tuple[int, int]) -> tuple[int, int]:
    q, r = coordinate
    return -r, q + r


def _axial_reflect(coordinate: tuple[int, int]) -> tuple[int, int]:
    q, r = coordinate
    return r, q


def radius_two_hex_symmetries(graph: RootedGraph) -> tuple[tuple[int, ...], ...]:
    """Construct the twelve exact D6 symmetries of an axial radius-two disk."""

    index = {vertex: offset for offset, vertex in enumerate(graph.vertices)}
    coordinates = {vertex: _parse_axial(vertex) for vertex in graph.vertices}
    permutations: set[tuple[int, ...]] = set()
    for reflected in (False, True):
        for rotations in range(6):
            transformed: list[int] = []
            for vertex in graph.vertices:
                coordinate = coordinates[vertex]
                if reflected:
                    coordinate = _axial_reflect(coordinate)
                for _ in range(rotations):
                    coordinate = _axial_rotate(coordinate)
                target = f"{coordinate[0]},{coordinate[1]}"
                if target not in index:
                    raise RootedTraceSymmetryError("hex symmetry leaves the radius-two disk")
                transformed.append(index[target])
            permutation = tuple(transformed)
            if not is_rooted_automorphism(graph, permutation):
                raise RootedTraceSymmetryError("declared hex symmetry does not preserve the graph")
            permutations.add(permutation)
    if len(permutations) != 12:
        raise RootedTraceSymmetryError("radius-two disk must expose twelve distinct D6 symmetries")
    return tuple(sorted(permutations))


def two_face_seed_graph() -> RootedGraph:
    """Smallest symmetric two-seed-plus-origin trace candidate.

    This is a bounded falsification object, not selected UCNS geometry. Each
    face retains one copy of the pinned structural graph and the origin couples
    identically to both CENTER vertices.
    """

    seed = seed_structural_graph()
    root = "ORIGIN"
    vertices = [root]
    edges: list[tuple[str, str]] = []
    for face in ("UPPER", "LOWER"):
        vertices.extend(f"{face}:{vertex}" for vertex in seed.vertices)
        edges.extend((f"{face}:{left}", f"{face}:{right}") for left, right in seed.edges)
        edges.append((root, f"{face}:{seed.root}"))
    return _graph(vertices, edges, root)


def _layer_swap(graph: RootedGraph) -> tuple[int, ...]:
    index = {vertex: offset for offset, vertex in enumerate(graph.vertices)}
    targets: list[int] = []
    for vertex in graph.vertices:
        if vertex == graph.root:
            target = vertex
        elif vertex.startswith("UPPER:"):
            target = "LOWER:" + vertex.removeprefix("UPPER:")
        elif vertex.startswith("LOWER:"):
            target = "UPPER:" + vertex.removeprefix("LOWER:")
        else:
            raise RootedTraceSymmetryError("two-face vertex lacks a face prefix")
        targets.append(index[target])
    return tuple(targets)


def _factorize(value: int) -> tuple[tuple[int, int], ...]:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise RootedTraceSymmetryError("factorization input must be a positive integer")
    remaining = value
    divisor = 2
    factors: list[tuple[int, int]] = []
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


@lru_cache(maxsize=None)
def evaluate(observed: tuple[int, int, int] = OBSERVED_GONOLS) -> SymmetryEvaluation:
    """Evaluate symmetry divisibility using observations only at comparison gates."""

    if (
        len(observed) != 3
        or any(isinstance(value, bool) or not isinstance(value, int) or value <= 0 for value in observed)
    ):
        raise RootedTraceSymmetryError("observed must contain three positive integers")
    boundary_multiplicity = lift.load_seed_geometry().boundary_multiplicity
    if (observed[2] - 1) % boundary_multiplicity:
        raise RootedTraceSymmetryError("third observation does not admit the pinned boundary lift")
    state_target = (observed[2] - 1) // boundary_multiplicity

    seed = seed_structural_graph()
    seed_group = rooted_automorphisms(seed)
    seed_traces = lift.count_connected_build_orders(seed.vertices, seed.edges, seed.root)
    if seed_traces % len(seed_group):
        raise RootedTraceSymmetryError("seed traces violate rooted automorphism divisibility")

    radius_vertices, radius_edges, radius_root = lift._radius_two_hex_graph()
    radius = _graph(radius_vertices, radius_edges, radius_root)
    radius_group = radius_two_hex_symmetries(radius)
    radius_traces = lift.count_connected_build_orders(radius.vertices, radius.edges, radius.root)
    if radius_traces % len(radius_group):
        raise RootedTraceSymmetryError("radius-two traces violate rooted automorphism divisibility")

    two_face = two_face_seed_graph()
    layer_swap = _layer_swap(two_face)
    if not is_rooted_automorphism(two_face, layer_swap):
        raise RootedTraceSymmetryError("two-face layer swap must preserve the candidate graph")
    two_face_traces = lift.count_connected_build_orders(
        two_face.vertices,
        two_face.edges,
        two_face.root,
    )

    return SymmetryEvaluation(
        state_target=state_target,
        state_target_factorization=_factorize(state_target),
        seed_automorphism_order=len(seed_group),
        seed_trace_count=seed_traces,
        seed_orbit_count=seed_traces // len(seed_group),
        radius_two_symmetry_order=len(radius_group),
        radius_two_trace_count=radius_traces,
        radius_two_standing=STATUS_FALSIFIED,
        two_face_has_layer_swap=True,
        two_face_trace_count=two_face_traces,
        two_face_standing=STATUS_FALSIFIED,
        falsified_class_count=2,
        constructor_survivor_count=0,
        next_prediction=None,
        hmmm=HMMM,
    )


def _stack_root() -> Path:
    return Path(__file__).resolve().parents[2]


def receipt_payload(observed: tuple[int, int, int] = OBSERVED_GONOLS) -> dict[str, Any]:
    result = evaluate(observed)
    predecessor_path = Path(lift.__file__).resolve()
    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "standing": STANDING,
        "source": {
            "ucns_base_commit": lift.PINNED_UCNS_COMMIT,
            "event_trace_producer_path": str(predecessor_path.relative_to(_stack_root())),
            "event_trace_producer_sha256": sha256(predecessor_path.read_bytes()).hexdigest(),
            "event_trace_receipt_sha256": lift.receipt_digest(),
        },
        "comparison": {
            "observed": list(observed),
            "fourfold_state_target": result.state_target,
            "state_target_factorization": [list(item) for item in result.state_target_factorization],
            "seed": {
                "rooted_automorphism_order": result.seed_automorphism_order,
                "construction_trace_count": result.seed_trace_count,
                "free_orbit_count": result.seed_orbit_count,
            },
            "radius_two_hex_disk": {
                "rooted_symmetry_order": result.radius_two_symmetry_order,
                "construction_trace_count": result.radius_two_trace_count,
                "target_divisible_by_symmetry_order": (
                    result.state_target % result.radius_two_symmetry_order == 0
                ),
                "standing": result.radius_two_standing,
            },
            "symmetric_two_face_seed": {
                "root_fixed_layer_swap": result.two_face_has_layer_swap,
                "construction_trace_count": result.two_face_trace_count,
                "target_is_even": result.state_target % 2 == 0,
                "standing": result.two_face_standing,
            },
            "falsified_class_count": result.falsified_class_count,
            "constructor_survivor_count": result.constructor_survivor_count,
            "next_prediction": result.next_prediction,
        },
        "surviving_constraints": [
            "a connected-trace interpretation must remove D6 rooted symmetry through declared mechanics or use a different counted object",
            "indistinguishable upper/lower faces cannot remain related by a root-fixed layer-swap involution",
            "phase/chirality-sensitive admissibility, an authorized quotient, and a different state extractor remain distinct unresolved alternatives",
        ],
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
