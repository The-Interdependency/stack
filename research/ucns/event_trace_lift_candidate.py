"""Structure-derived event/trace lift candidate for recursive gonol research.

The experiment does not infer a recurrence from the observed integers. It
extracts two independently executable invariants from the stack-pinned Mobius
Seed of Life:

* 39 pairwise projection events;
* 720 center-rooted construction orders of the seven-band structural graph.

The source-declared boundary multiplicity is then tested as a fourfold lift
around one Structural Null origin. The resulting identities are retrodictive
research evidence, not a selected UCNS constructor.
"""

# === MODULE_BUILD ===
# id: ucns_event_trace_lift_candidate
#   module_name: event_trace_lift_candidate
#   module_kind: experiment
#   summary: tests a source-derived fourfold-plus-origin relationship over Mobius seed projection events and construction traces, then falsifies bounded next-scale continuations
#   owner: The Interdependency
#   public_surface: OBSERVED_GONOLS, SeedGeometry, ContinuationResult, LiftEvaluation, load_seed_geometry, count_connected_build_orders, fourfold_origin_lift, evaluate, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _stack_root, _load_module, _file_digest, _seed_graph, _radius_two_hex_graph, _structural_incidence_graph, _projection_incidence_graph
#   auth_boundary: none; reads stack-pinned UCNS research and geometry sources only
#   storage_boundary: read-only at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_event_trace_lift_candidate.py
#   rollout: stack-local post-observation experiment only; no UCNS canon, stack libs, or PCEA promotion
#   rollback: remove this module, its tests, report, and receipt
#   requires: ucns_public_gonol_geometry, ucns_mobius_seed_of_life_candidate, gonol-build construction discipline
#   since: 2026-09-02
#   unresolved: whether four source-declared boundary events define a global lift, completed 2881-gonol geometry, later Flower-of-Life ring authority, recursive-scale cardinalization
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: event_trace_lift_binds_pinned_seed_geometry
#   given: the event/trace lift experiment loads its source geometry
#   then: it binds the exact UCNS research base, Public Gonol digest, source file digests, seven bands, twelve structural relations, thirty-nine projection events, and uniform source-declared boundary multiplicity
#   class: safety
#   since: 2026-09-02
#
# id: event_trace_lift_recovers_seed_build_orders
#   given: construction starts with the center band and uses only structural-vesica adjacency
#   then: the six ring bands admit exactly 720 complete construction orders
#   class: correctness
#   since: 2026-09-02
#
# id: event_trace_lift_matches_are_retrodictive_only
#   given: the fourfold-plus-origin lift is applied to the event and trace invariants
#   then: 157 and 2881 are reproduced but are labeled post-observation identities rather than a surviving recursive constructor
#   class: doctrine
#   since: 2026-09-02
#
# id: event_trace_lift_continuations_are_unchanged_and_falsifiable
#   given: a bounded next-scale graph candidate is evaluated
#   then: the same adjacency-order count and fourfold-plus-origin lift are used without target-specific constants or tuning
#   class: evidence
#   since: 2026-09-02
#
# id: event_trace_lift_has_no_survivor_without_second_geometry
#   given: all declared bounded continuations miss the third observation
#   then: constructor survivor count is zero, no next prediction is emitted, and completed 2881 geometry remains hmmm
#   class: doctrine
#   since: 2026-09-02
#
# id: event_trace_lift_receipt_replays_byte_identical
#   given: the same pinned sources and observed comparison tuple are evaluated
#   then: canonical receipt bytes and their digest are byte-identical
#   class: correctness
#   since: 2026-09-02
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
from types import ModuleType
from typing import Any


SCHEMA_ID = "the-interdependency.stack-research.ucns.event-trace-lift"
SCHEMA_VERSION = "0.1.0"
STANDING = "stack-local-post-observation-candidate"

OBSERVED_GONOLS: tuple[int, int, int] = (157, 2881, 54837698421)
PINNED_UCNS_COMMIT = "1975fe70cf4e0826a8020c2da3047569e277af64"
PINNED_PUBLIC_GONOL_SHA256 = "55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5"

STATUS_RETRODICTIVE_MATCH = "RETRODICTIVE_MATCH_ONLY"
STATUS_FALSIFIED = "FALSIFIED"

NONCLAIMS: tuple[str, ...] = (
    "not UCNS canon",
    "not a recovered recursive-scale transition law",
    "not a preregistered first-gate prediction",
    "not evidence that source-declared boundary events are physical contacts",
    "not a PCEA runtime, entropy, hardness, or authenticity claim",
)

HMMM: tuple[str, ...] = (
    "the source declares four boundary relation events per structural pair, not one selected global cardinality lift",
    "the 157 identity uses projection-event count while the 2881 identity uses construction-trace count, so they are not yet one unchanged state extractor",
    "the completed 2881-gonol event and structural-relation ledger has not been constructed",
    "later Flower-of-Life rings are unresolved in UCNS authority",
    "no continuation survives the second observed gate and no next prediction is authorized",
)


class EventTraceLiftError(RuntimeError):
    """Raised when source provenance or a candidate graph is invalid."""


@dataclass(frozen=True, slots=True)
class SeedGeometry:
    """Exact pinned geometry consumed by this experiment."""

    base_commit: str
    public_gonol_arity: int
    public_gonol_sha256: str
    source_file_digests: tuple[tuple[str, str], ...]
    bands: tuple[str, ...]
    structural_edges: tuple[tuple[str, str], ...]
    projection_node_incidence: tuple[tuple[str, tuple[str, ...]], ...]
    pair_relation_count: int
    structural_relation_count: int
    pairwise_projection_event_count: int
    boundary_multiplicity: int
    total_declared_structural_boundary_events: int


@dataclass(frozen=True, slots=True)
class ContinuationResult:
    """One unchanged trace-count/lift continuation."""

    candidate_id: str
    standing: str
    basis: str
    vertex_count: int
    edge_count: int
    construction_trace_count: int
    lifted_cardinality: int
    target_match: bool


@dataclass(frozen=True, slots=True)
class LiftEvaluation:
    """Complete result at the current research boundary."""

    status: str
    event_state_count: int
    event_lifted_cardinality: int
    public_arity_match: bool
    seed_construction_trace_count: int
    trace_lifted_cardinality: int
    first_successor_match: bool
    third_observation_state_quotient: int | None
    continuations: tuple[ContinuationResult, ...]
    constructor_survivor_count: int
    next_prediction: int | None
    hmmm: tuple[str, ...]


def _stack_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise EventTraceLiftError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _file_digest(root: Path, relative_path: str) -> tuple[str, str]:
    return relative_path, sha256((root / relative_path).read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def load_seed_geometry() -> SeedGeometry:
    """Load and validate the exact stack-pinned UCNS seed geometry."""

    root = _stack_root()
    with (root / "research" / "ucns" / "BASE.json").open(encoding="utf-8") as handle:
        base = json.load(handle)
    if base.get("source_commit") != PINNED_UCNS_COMMIT:
        raise EventTraceLiftError("UCNS research base commit mismatch")

    public_gonol = _load_module(
        "stack_pinned_public_gonol_for_event_trace_lift",
        root / "libs" / "ucns" / "src" / "ucns" / "public_gonol.py",
    )
    mobius_seed = _load_module(
        "stack_pinned_mobius_seed_for_event_trace_lift",
        root / "libs" / "ucns" / "src" / "ucns" / "mobius_seed.py",
    )

    arrangement = tuple(public_gonol.PUBLIC_GONOL_157)
    public_digest = public_gonol.public_gonol_sha256(arrangement)
    if public_digest != PINNED_PUBLIC_GONOL_SHA256:
        raise EventTraceLiftError("Public Gonol digest mismatch")

    seed = mobius_seed.build_mobius_seed_of_life()
    structural = tuple(seed.structural_relations)
    multiplicities = {relation.declared_boundary_relation_events for relation in structural}
    if len(multiplicities) != 1 or None in multiplicities:
        raise EventTraceLiftError("structural boundary multiplicity is not uniform")
    boundary_multiplicity = int(next(iter(multiplicities)))

    paths = (
        "research/ucns/BASE.json",
        "libs/ucns/CANON.md",
        "libs/ucns/docs/GEOMETRY.md",
        "libs/ucns/src/ucns/public_gonol.py",
        "libs/ucns/src/ucns/mobius_seed.py",
    )
    return SeedGeometry(
        base_commit=base["source_commit"],
        public_gonol_arity=len(arrangement),
        public_gonol_sha256=public_digest,
        source_file_digests=tuple(_file_digest(root, path) for path in paths),
        bands=tuple(band.slot.value for band in seed.bands),
        structural_edges=tuple((relation.left.value, relation.right.value) for relation in structural),
        projection_node_incidence=tuple(
            (node.node_id, tuple(slot.value for slot in node.incident_slots))
            for node in seed.nodes
        ),
        pair_relation_count=len(seed.relations),
        structural_relation_count=len(structural),
        pairwise_projection_event_count=seed.pairwise_projection_event_count,
        boundary_multiplicity=boundary_multiplicity,
        total_declared_structural_boundary_events=seed.declared_structural_boundary_event_count,
    )


def _canonical_graph(
    vertices: tuple[str, ...], edges: tuple[tuple[str, str], ...], root: str
) -> tuple[tuple[str, ...], tuple[tuple[str, str], ...], str]:
    if not vertices or len(vertices) != len(set(vertices)):
        raise EventTraceLiftError("candidate graph vertices must be unique and nonempty")
    if root not in vertices:
        raise EventTraceLiftError("candidate graph root is absent")
    known = set(vertices)
    canonical_edges: set[tuple[str, str]] = set()
    for left, right in edges:
        if left not in known or right not in known or left == right:
            raise EventTraceLiftError("candidate graph edge is invalid")
        canonical_edges.add(tuple(sorted((left, right))))
    return vertices, tuple(sorted(canonical_edges)), root


@lru_cache(maxsize=None)
def count_connected_build_orders(
    vertices: tuple[str, ...], edges: tuple[tuple[str, str], ...], root: str
) -> int:
    """Count orders where every new vertex is adjacent to the built set."""

    vertices, edges, root = _canonical_graph(vertices, edges, root)
    index = {vertex: offset for offset, vertex in enumerate(vertices)}
    adjacency = [0] * len(vertices)
    for left, right in edges:
        i, j = index[left], index[right]
        adjacency[i] |= 1 << j
        adjacency[j] |= 1 << i

    full = (1 << len(vertices)) - 1
    level: dict[int, int] = {1 << index[root]: 1}
    for _ in range(1, len(vertices)):
        following: dict[int, int] = {}
        for built, ways in level.items():
            frontier = 0
            remaining = built
            while remaining:
                bit = remaining & -remaining
                frontier |= adjacency[bit.bit_length() - 1]
                remaining -= bit
            frontier &= full ^ built
            while frontier:
                bit = frontier & -frontier
                state = built | bit
                following[state] = following.get(state, 0) + ways
                frontier -= bit
        level = following
    return level.get(full, 0)


def fourfold_origin_lift(state_count: int, boundary_multiplicity: int) -> int:
    """Candidate cardinality: one origin plus one boundary lift per state."""

    if isinstance(state_count, bool) or not isinstance(state_count, int) or state_count < 0:
        raise EventTraceLiftError("state_count must be a nonnegative integer")
    if (
        isinstance(boundary_multiplicity, bool)
        or not isinstance(boundary_multiplicity, int)
        or boundary_multiplicity <= 0
    ):
        raise EventTraceLiftError("boundary_multiplicity must be a positive integer")
    return 1 + boundary_multiplicity * state_count


def _seed_graph(geometry: SeedGeometry) -> tuple[tuple[str, ...], tuple[tuple[str, str], ...], str]:
    return _canonical_graph(geometry.bands, geometry.structural_edges, "CENTER")


def _radius_two_hex_graph() -> tuple[tuple[str, ...], tuple[tuple[str, str], ...], str]:
    """Bounded later-ring candidate; UCNS does not currently select it."""

    coordinates = tuple(
        sorted(
            (q, r)
            for q in range(-2, 3)
            for r in range(-2, 3)
            if max(abs(q), abs(r), abs(q + r)) <= 2
        )
    )
    vertices = tuple(f"{q},{r}" for q, r in coordinates)
    coordinate_set = set(coordinates)
    directions = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
    edges: set[tuple[str, str]] = set()
    for q, r in coordinates:
        for dq, dr in directions:
            other = q + dq, r + dr
            if other in coordinate_set:
                edges.add(tuple(sorted((f"{q},{r}", f"{other[0]},{other[1]}"))))
    return _canonical_graph(vertices, tuple(edges), "0,0")


def _structural_incidence_graph(
    geometry: SeedGeometry,
) -> tuple[tuple[str, ...], tuple[tuple[str, str], ...], str]:
    relation_vertices = tuple(f"relation:{offset}" for offset in range(len(geometry.structural_edges)))
    vertices = tuple(f"band:{band}" for band in geometry.bands) + relation_vertices
    edges: list[tuple[str, str]] = []
    for offset, (left, right) in enumerate(geometry.structural_edges):
        relation = f"relation:{offset}"
        edges.extend(((f"band:{left}", relation), (f"band:{right}", relation)))
    return _canonical_graph(vertices, tuple(edges), "band:CENTER")


def _projection_incidence_graph(
    geometry: SeedGeometry,
) -> tuple[tuple[str, ...], tuple[tuple[str, str], ...], str]:
    vertices = tuple(f"band:{band}" for band in geometry.bands) + tuple(
        f"node:{node_id}" for node_id, _ in geometry.projection_node_incidence
    )
    edges = tuple(
        (f"band:{band}", f"node:{node_id}")
        for node_id, incident_bands in geometry.projection_node_incidence
        for band in incident_bands
    )
    return _canonical_graph(vertices, edges, "band:CENTER")


def _continuation(
    *,
    candidate_id: str,
    standing: str,
    basis: str,
    graph: tuple[tuple[str, ...], tuple[tuple[str, str], ...], str],
    boundary_multiplicity: int,
    target: int,
) -> ContinuationResult:
    vertices, edges, root = graph
    traces = count_connected_build_orders(vertices, edges, root)
    lifted = fourfold_origin_lift(traces, boundary_multiplicity)
    return ContinuationResult(
        candidate_id=candidate_id,
        standing=standing,
        basis=basis,
        vertex_count=len(vertices),
        edge_count=len(edges),
        construction_trace_count=traces,
        lifted_cardinality=lifted,
        target_match=lifted == target,
    )


@lru_cache(maxsize=None)
def evaluate(observed: tuple[int, int, int] = OBSERVED_GONOLS) -> LiftEvaluation:
    """Evaluate identities and unchanged continuations against observations."""

    if (
        len(observed) != 3
        or any(isinstance(value, bool) or not isinstance(value, int) or value <= 0 for value in observed)
    ):
        raise EventTraceLiftError("observed must contain three positive integers")

    geometry = load_seed_geometry()
    seed_vertices, seed_edges, seed_root = _seed_graph(geometry)
    seed_traces = count_connected_build_orders(seed_vertices, seed_edges, seed_root)
    event_lift = fourfold_origin_lift(
        geometry.pairwise_projection_event_count,
        geometry.boundary_multiplicity,
    )
    trace_lift = fourfold_origin_lift(seed_traces, geometry.boundary_multiplicity)

    third_quotient = None
    if (observed[2] - 1) % geometry.boundary_multiplicity == 0:
        third_quotient = (observed[2] - 1) // geometry.boundary_multiplicity

    continuations = (
        _continuation(
            candidate_id="radius_two_hex_disk",
            standing="FALSIFIED",
            basis="the next complete hexagonal ring under the unchanged adjacency-to-built rule",
            graph=_radius_two_hex_graph(),
            boundary_multiplicity=geometry.boundary_multiplicity,
            target=observed[2],
        ),
        _continuation(
            candidate_id="structural_relation_incidence",
            standing="FALSIFIED",
            basis="promote each of the twelve structural relations to one incidence participant",
            graph=_structural_incidence_graph(geometry),
            boundary_multiplicity=geometry.boundary_multiplicity,
            target=observed[2],
        ),
        _continuation(
            candidate_id="projection_node_incidence",
            standing="FALSIFIED",
            basis="promote each of the thirteen projection nodes to one incidence participant",
            graph=_projection_incidence_graph(geometry),
            boundary_multiplicity=geometry.boundary_multiplicity,
            target=observed[2],
        ),
    )
    survivors = sum(result.target_match for result in continuations)
    first_match = trace_lift == observed[1]
    status = (
        STATUS_RETRODICTIVE_MATCH
        if event_lift == observed[0] and first_match and survivors == 0
        else STATUS_FALSIFIED
    )
    return LiftEvaluation(
        status=status,
        event_state_count=geometry.pairwise_projection_event_count,
        event_lifted_cardinality=event_lift,
        public_arity_match=event_lift == observed[0] == geometry.public_gonol_arity,
        seed_construction_trace_count=seed_traces,
        trace_lifted_cardinality=trace_lift,
        first_successor_match=first_match,
        third_observation_state_quotient=third_quotient,
        continuations=continuations,
        constructor_survivor_count=survivors,
        next_prediction=None,
        hmmm=HMMM,
    )


def _continuation_payload(result: ContinuationResult) -> dict[str, Any]:
    return {
        "candidate_id": result.candidate_id,
        "standing": result.standing,
        "basis": result.basis,
        "vertex_count": result.vertex_count,
        "edge_count": result.edge_count,
        "construction_trace_count": result.construction_trace_count,
        "lifted_cardinality": result.lifted_cardinality,
        "target_match": result.target_match,
    }


def receipt_payload(observed: tuple[int, int, int] = OBSERVED_GONOLS) -> dict[str, Any]:
    geometry = load_seed_geometry()
    result = evaluate(observed)
    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "standing": STANDING,
        "source": {
            "ucns_base_commit": geometry.base_commit,
            "public_gonol_arity": geometry.public_gonol_arity,
            "public_gonol_sha256": geometry.public_gonol_sha256,
            "source_file_digests": [
                {"path": path, "sha256": digest}
                for path, digest in geometry.source_file_digests
            ],
        },
        "seed_geometry": {
            "bands": len(geometry.bands),
            "pair_relations": geometry.pair_relation_count,
            "structural_relations": geometry.structural_relation_count,
            "pairwise_projection_events": geometry.pairwise_projection_event_count,
            "source_declared_boundary_multiplicity_per_structural_relation": geometry.boundary_multiplicity,
            "total_source_declared_structural_boundary_events": geometry.total_declared_structural_boundary_events,
        },
        "comparison": {
            "observed": list(observed),
            "status": result.status,
            "preregistration_standing": "post-observation; first-gate matches are retrodictive only",
            "event_identity": {
                "state_count": result.event_state_count,
                "lifted_cardinality": result.event_lifted_cardinality,
                "public_arity_match": result.public_arity_match,
            },
            "trace_identity": {
                "construction_trace_count": result.seed_construction_trace_count,
                "lifted_cardinality": result.trace_lifted_cardinality,
                "first_successor_match": result.first_successor_match,
            },
            "third_observation_state_quotient": result.third_observation_state_quotient,
            "continuations": [_continuation_payload(item) for item in result.continuations],
            "constructor_survivor_count": result.constructor_survivor_count,
            "next_prediction": result.next_prediction,
        },
        "nonclaims": list(NONCLAIMS),
        "hmmm": list(result.hmmm),
    }


def receipt_bytes(observed: tuple[int, int, int] = OBSERVED_GONOLS) -> bytes:
    return json.dumps(
        receipt_payload(observed),
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def receipt_digest(observed: tuple[int, int, int] = OBSERVED_GONOLS) -> str:
    return sha256(receipt_bytes(observed)).hexdigest()


def main() -> int:
    payload = receipt_payload()
    payload["receipt_sha256"] = receipt_digest()
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
