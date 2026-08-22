# === MODULE_BUILD ===
# id: ucns_mobius_seed_global_compatibility
#   module_name: mobius_global_compatibility
#   module_kind: experiment
#   summary: proves the single-state phase/chirality capacity and contact-versus-braid boundary for assembling the certified Mobius Vesica across the twelve structural Seed-of-Life pairs
#   owner: Erin Spencer
#   public_surface: EdgeOrientation, SurfacePhaseState, StructuralEdge, CertifiedEdgeCopy, CompatibilityBoundary, surface_phase, build_structural_edges, certified_edge_copies, pinned_pr174_assignment, edge_inherits_certificate, contact_and_strict_braid_compatible, prove_global_compatibility_boundary, write_global_compatibility_certificate
#   internal_surface: exact half-turn phase quotient, rigid-rotation transport, W7 cut and matching enumeration, pinned PR-174 comparison
#   auth_boundary: none
#   storage_boundary: caller-supplied local path only
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_mobius_global_compatibility.py
#   rollout: stacked nonselecting UCNS obstruction certificate; does not alter PR 174 or PR 175
#   rollback: remove this module, its test, documentation, and generated certificate
#   requires: ucns_mobius_vesica_continuation, ucns_mobius_seed_of_life_candidate
#   since: 2026-08-10
#   unresolved: nonconstant phase fields, recursive or multichannel carriers, other local dyad families, simultaneous surface embedding, complete lift equations, spectral operator, zeta correspondence
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: mobius_seed_incident_certified_dyads_are_state_incompatible
#   given: two wheel-W7 structural pairs share a band and each is a rigid copy of the certified quarter-turn anti-chiral vesica
#   then: all four orientation combinations demand different chirality-phase states at the shared band
#   class: correctness
#   since: 2026-08-10
#
# id: mobius_seed_single_state_certified_capacity_is_three
#   given: each band has one chirality and one constant surface phase modulo one half turn
#   then: compatible certified pairs form a matching and W7 has maximum matching size three
#   class: correctness
#   since: 2026-08-10
#
# id: mobius_seed_center_needs_six_phase_channels_for_six_spokes
#   given: all six spokes are rigid copies while the center retains one chirality
#   then: they demand six distinct center phases modulo one half turn
#   class: evidence
#   since: 2026-08-10
#
# id: mobius_seed_physical_contact_and_strict_braid_are_event_exclusive
#   given: the same occurrences at one event are declared both physically equal and strictly height-separated
#   then: delta-z equals zero contradicts delta-z nonzero
#   class: doctrine
#   since: 2026-08-10
#
# id: mobius_seed_pr174_inherits_no_exact_rigid_vesica_pairs
#   given: the pinned PR-174 phase/chirality schedule is compared with both exact rigid-copy orientations
#   then: zero of twelve structural pairs inherit the complete local certificate
#   class: evidence
#   since: 2026-08-10
#
# id: mobius_seed_global_compatibility_certificate_is_nonselecting
#   given: the certificate is serialized
#   then: selection effect is none and the obstruction remains bounded to its declared assumptions
#   class: doctrine
#   since: 2026-08-10
# === END CONTRACTS ===

"""Exact global compatibility boundary for the certified Möbius vesica.

Within the declared family—one constant chirality and one constant surface
phase per global band, with every inheriting edge a rigid copy of the local
quarter-turn anti-chiral certificate—no two incident W7 edges are compatible.
This is not an obstruction to nonconstant phase fields or other carrier types.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
from typing import Mapping

from .mobius_continuation import (
    SEED_CANDIDATE_BRANCH,
    SEED_CANDIDATE_HEAD,
    SEED_CANDIDATE_PR,
    MobiusVesicaContinuationEngine,
)
from .mobius_vesica import (
    SOURCE_DOCUMENT_NAME,
    SOURCE_DOCUMENT_SHA256,
    TwistChirality,
    fraction_text,
)

SCHEMA_ID = "ucns.mobius-seed.global-compatibility"
SCHEMA_VERSION = "0.1.0"
VESICA_PR = 175
VESICA_HEAD = "c7354608711bc7471aef881777800a686c8385c4"
VESICA_BRANCH = "agent/mobius-vesica-certificate"
HALF_TURN = Fraction(1, 2)
QUARTER_TURN = Fraction(1, 4)


class GlobalCompatibilityError(ValueError):
    pass


class EdgeOrientation(str, Enum):
    PLUS_AT_LEFT = "plus-at-left"
    PLUS_AT_RIGHT = "plus-at-right"


def surface_phase(value: Fraction) -> Fraction:
    if not isinstance(value, Fraction):
        raise GlobalCompatibilityError("phase must be an exact Fraction")
    return value % HALF_TURN


@dataclass(frozen=True, slots=True)
class SurfacePhaseState:
    chirality: TwistChirality
    phase_turns_mod_half: Fraction

    def __post_init__(self) -> None:
        if not isinstance(self.chirality, TwistChirality):
            raise GlobalCompatibilityError("invalid chirality")
        if surface_phase(self.phase_turns_mod_half) != self.phase_turns_mod_half:
            raise GlobalCompatibilityError("phase must be in [0,1/2)")

    def as_dict(self) -> dict[str, str]:
        return {
            "chirality": self.chirality.name.lower(),
            "phase_mod_half": fraction_text(self.phase_turns_mod_half),
        }


@dataclass(frozen=True, slots=True)
class StructuralEdge:
    edge_id: str
    left: str
    right: str
    axis_turns: Fraction

    @property
    def endpoints(self) -> frozenset[str]:
        return frozenset((self.left, self.right))

    def shared_vertex(self, other: "StructuralEdge") -> str | None:
        shared = self.endpoints & other.endpoints
        return next(iter(shared)) if shared else None


@dataclass(frozen=True, slots=True)
class CertifiedEdgeCopy:
    edge: StructuralEdge
    orientation: EdgeOrientation
    left_state: SurfacePhaseState
    right_state: SurfacePhaseState

    def state_at(self, vertex: str) -> SurfacePhaseState:
        if vertex == self.edge.left:
            return self.left_state
        if vertex == self.edge.right:
            return self.right_state
        raise GlobalCompatibilityError(f"{vertex} is not incident to {self.edge.edge_id}")


@dataclass(frozen=True, slots=True)
class CompatibilityBoundary:
    edges: tuple[StructuralEdge, ...]
    adjacent_edge_pair_count: int
    oriented_adjacency_checks: int
    compatible_oriented_adjacencies: int
    maximum_opposite_chirality_edges: int
    maximum_cut_assignments: tuple[Mapping[str, TwistChirality], ...]
    maximum_matching_size: int
    maximum_matchings: tuple[tuple[str, ...], ...]
    center_positive_spoke_phases: tuple[Fraction, ...]
    center_negative_spoke_phases: tuple[Fraction, ...]
    pr174_assignment: Mapping[str, SurfacePhaseState]
    pr174_inherited_edge_ids: tuple[str, ...]

    @property
    def total_structural_pairs(self) -> int:
        return len(self.edges)

    @property
    def minimum_noninheriting_pairs(self) -> int:
        return self.total_structural_pairs - self.maximum_matching_size

    @property
    def payload(self) -> dict[str, object]:
        edge_rows = [
            {
                "id": edge.edge_id,
                "left": edge.left,
                "right": edge.right,
                "axis_turns": fraction_text(edge.axis_turns),
            }
            for edge in self.edges
        ]
        payload: dict[str, object] = {
            "schema_id": SCHEMA_ID,
            "schema_version": SCHEMA_VERSION,
            "authority": "Erin Spencer",
            "recorded_on": "2026-08-10",
            "selection_effect": "none",
            "status": "obstructed-under-single-constant-state-rigid-copy-assumptions",
            "source": {
                "name": SOURCE_DOCUMENT_NAME,
                "sha256": SOURCE_DOCUMENT_SHA256,
            },
            "stack": {
                "seed": {
                    "pr": SEED_CANDIDATE_PR,
                    "branch": SEED_CANDIDATE_BRANCH,
                    "head": SEED_CANDIDATE_HEAD,
                },
                "vesica": {
                    "pr": VESICA_PR,
                    "branch": VESICA_BRANCH,
                    "head": VESICA_HEAD,
                },
            },
            "assumptions": [
                "structural graph is W7 with six spokes and six rim edges",
                "each global band has one constant chirality and one constant surface phase",
                "each inheriting edge is a rigid copy of the certified opposite-chirality quarter-turn dyad",
                "surface phase is quotiented modulo one half turn; retaining a seam label can only make compatibility stricter",
            ],
            "rotation_law": {
                "plus_at_left": ["(+,-rho/2)", "(-,1/4+rho/2)"],
                "plus_at_right": ["(-,rho/2)", "(+,1/4-rho/2)"],
                "phase_modulus": "1/2 turn",
            },
            "graph": {
                "edges": edge_rows,
                "adjacent_edge_pairs": self.adjacent_edge_pair_count,
            },
            "chirality_only": {
                "maximum_opposite_edges": self.maximum_opposite_chirality_edges,
                "minimum_same_chirality_edges": 12 - self.maximum_opposite_chirality_edges,
                "maximizers_with_center_positive": [
                    {
                        vertex: chirality.name.lower()
                        for vertex, chirality in sorted(assignment.items())
                    }
                    for assignment in self.maximum_cut_assignments
                ],
            },
            "full_state": {
                "oriented_incidence_checks": self.oriented_adjacency_checks,
                "compatible_incident_checks": self.compatible_oriented_adjacencies,
                "maximum_simultaneous_exact_dyads": self.maximum_matching_size,
                "maximum_fraction": fraction_text(Fraction(self.maximum_matching_size, 12)),
                "minimum_pairs_requiring_relaxation": self.minimum_noninheriting_pairs,
                "maximum_matching_count": len(self.maximum_matchings),
                "matching_witness": list(self.maximum_matchings[0]),
            },
            "center_channel_bound": {
                "positive_phases": [fraction_text(v) for v in self.center_positive_spoke_phases],
                "negative_phases": [fraction_text(v) for v in self.center_negative_spoke_phases],
                "minimum_channels_for_six_rigid_spokes": 6,
            },
            "pr174": {
                "assignment": {
                    vertex: state.as_dict()
                    for vertex, state in sorted(self.pr174_assignment.items())
                },
                "inherited_edges": list(self.pr174_inherited_edge_ids),
                "inherited_count": len(self.pr174_inherited_edge_ids),
            },
            "lift_boundary": {
                "physical_contact": "delta_z=0",
                "strict_braid": "delta_z!=0",
                "same_event_compatible": False,
                "pr174_events": "nonzero sign-reversing lift differences are projected braid crossings, not physical centerline contacts",
            },
            "next": [
                "solve a seam-compatible nonconstant phase field",
                "test recursive or multichannel carriers; center lower bound is six channels",
                "classify other local two-plus-four contact families",
                "split physical contacts from projected braid events",
            ],
            "nonclaims": [
                "not an obstruction to every Möbius Seed embedding",
                "not a complete lift or ambient-isotopy theorem",
                "not an electron model or Pauli derivation",
                "not a zeta theorem or proof of the Riemann hypothesis",
            ],
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        payload["payload_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
        return payload

    def json_text(self, *, indent: int = 2) -> str:
        return json.dumps(self.payload, indent=indent, sort_keys=True, ensure_ascii=False) + "\n"


def build_structural_edges() -> tuple[StructuralEdge, ...]:
    edges = tuple(
        StructuralEdge(
            placement.pair_id,
            placement.left_label,
            placement.right_label,
            placement.rotation_turns,
        )
        for placement in MobiusVesicaContinuationEngine.seed_structural_placements()
    )
    if len(edges) != 12:
        raise GlobalCompatibilityError("expected twelve structural edges")
    return edges


def certified_edge_copies(edge: StructuralEdge) -> tuple[CertifiedEdgeCopy, CertifiedEdgeCopy]:
    rho = edge.axis_turns
    return (
        CertifiedEdgeCopy(
            edge,
            EdgeOrientation.PLUS_AT_LEFT,
            SurfacePhaseState(TwistChirality.POSITIVE, surface_phase(-rho / 2)),
            SurfacePhaseState(TwistChirality.NEGATIVE, surface_phase(QUARTER_TURN + rho / 2)),
        ),
        CertifiedEdgeCopy(
            edge,
            EdgeOrientation.PLUS_AT_RIGHT,
            SurfacePhaseState(TwistChirality.NEGATIVE, surface_phase(rho / 2)),
            SurfacePhaseState(TwistChirality.POSITIVE, surface_phase(QUARTER_TURN - rho / 2)),
        ),
    )


def _adjacent_pairs(edges: tuple[StructuralEdge, ...]) -> tuple[tuple[StructuralEdge, StructuralEdge, str], ...]:
    rows = []
    for left, right in itertools.combinations(edges, 2):
        shared = left.shared_vertex(right)
        if shared is not None:
            rows.append((left, right, shared))
    return tuple(rows)


def _maximum_cut(edges: tuple[StructuralEdge, ...]) -> tuple[int, tuple[Mapping[str, TwistChirality], ...]]:
    best = -1
    witnesses: list[Mapping[str, TwistChirality]] = []
    signs = (TwistChirality.POSITIVE, TwistChirality.NEGATIVE)
    for outer in itertools.product(signs, repeat=6):
        assignment: dict[str, TwistChirality] = {"CENTER": TwistChirality.POSITIVE}
        assignment.update({f"RING_{i}": outer[i] for i in range(6)})
        count = sum(assignment[e.left] is not assignment[e.right] for e in edges)
        if count > best:
            best, witnesses = count, [assignment]
        elif count == best:
            witnesses.append(assignment)
    return best, tuple(witnesses)


def _maximum_matchings(edges: tuple[StructuralEdge, ...]) -> tuple[tuple[str, ...], ...]:
    best = -1
    witnesses: list[tuple[str, ...]] = []
    for mask in range(1 << len(edges)):
        chosen = tuple(edges[i] for i in range(len(edges)) if mask & (1 << i))
        endpoints = [vertex for edge in chosen for vertex in (edge.left, edge.right)]
        if len(endpoints) != len(set(endpoints)):
            continue
        ids = tuple(edge.edge_id for edge in chosen)
        if len(ids) > best:
            best, witnesses = len(ids), [ids]
        elif len(ids) == best:
            witnesses.append(ids)
    return tuple(sorted(witnesses))


def _center_phases(edges: tuple[StructuralEdge, ...], chirality: TwistChirality) -> tuple[Fraction, ...]:
    phases = []
    for edge in edges[:6]:
        state = next(
            copy.state_at("CENTER")
            for copy in certified_edge_copies(edge)
            if copy.state_at("CENTER").chirality is chirality
        )
        phases.append(state.phase_turns_mod_half)
    return tuple(sorted(phases))


def pinned_pr174_assignment() -> dict[str, SurfacePhaseState]:
    result = {"CENTER": SurfacePhaseState(TwistChirality.POSITIVE, Fraction(0))}
    result.update(
        {
            f"RING_{i}": SurfacePhaseState(
                TwistChirality.NEGATIVE,
                surface_phase(Fraction(1, 2) + Fraction(i, 12)),
            )
            for i in range(6)
        }
    )
    return result


def edge_inherits_certificate(edge: StructuralEdge, assignment: Mapping[str, SurfacePhaseState]) -> bool:
    return any(
        assignment[edge.left] == copy.left_state
        and assignment[edge.right] == copy.right_state
        for copy in certified_edge_copies(edge)
    )


def contact_and_strict_braid_compatible(*, physical_contact: bool, delta_z_nonzero: bool) -> bool:
    return not (physical_contact and delta_z_nonzero)


def prove_global_compatibility_boundary() -> CompatibilityBoundary:
    edges = build_structural_edges()
    adjacent = _adjacent_pairs(edges)
    checks = 0
    compatible = 0
    for left, right, vertex in adjacent:
        for left_copy in certified_edge_copies(left):
            for right_copy in certified_edge_copies(right):
                checks += 1
                compatible += left_copy.state_at(vertex) == right_copy.state_at(vertex)
    maximum_opposite, cut_witnesses = _maximum_cut(edges)
    matchings = _maximum_matchings(edges)
    assignment = pinned_pr174_assignment()
    inherited = tuple(e.edge_id for e in edges if edge_inherits_certificate(e, assignment))
    boundary = CompatibilityBoundary(
        edges=edges,
        adjacent_edge_pair_count=len(adjacent),
        oriented_adjacency_checks=checks,
        compatible_oriented_adjacencies=int(compatible),
        maximum_opposite_chirality_edges=maximum_opposite,
        maximum_cut_assignments=cut_witnesses,
        maximum_matching_size=len(matchings[0]),
        maximum_matchings=matchings,
        center_positive_spoke_phases=_center_phases(edges, TwistChirality.POSITIVE),
        center_negative_spoke_phases=_center_phases(edges, TwistChirality.NEGATIVE),
        pr174_assignment=assignment,
        pr174_inherited_edge_ids=inherited,
    )
    if (len(adjacent), checks, compatible) != (33, 132, 0):
        raise GlobalCompatibilityError("incidence certificate mismatch")
    if (maximum_opposite, len(cut_witnesses)) != (9, 2):
        raise GlobalCompatibilityError("maximum-cut certificate mismatch")
    if (boundary.maximum_matching_size, len(matchings)) != (3, 20):
        raise GlobalCompatibilityError("matching certificate mismatch")
    if inherited or len(set(boundary.center_positive_spoke_phases)) != 6:
        raise GlobalCompatibilityError("phase certificate mismatch")
    return boundary


def write_global_compatibility_certificate(path: str | Path, *, indent: int = 2) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(prove_global_compatibility_boundary().json_text(indent=indent), encoding="utf-8")
    return output
