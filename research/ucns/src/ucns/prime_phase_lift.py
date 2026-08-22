# === MODULE_BUILD ===
# id: ucns_prime_phase_lift_p7_p5
#   module_name: prime_phase_lift
#   module_kind: experiment
#   summary: solves P7 globally with an exact seam-compatible phase law and finite-field lift over all thirteen hypernodes, then applies the same protocol independently to P5
#   owner: Erin Spencer
#   public_surface: EventSemantic, PhaseLaw, LiftOccurrence, LiftHypernode, PairLinkReadout, PrimePhaseLiftCandidate, select_phase_law, build_prime_seven_phase_lift, build_prime_five_phase_lift, phase_lift_family_certificate, write_phase_lift_family_certificate
#   internal_surface: exact phase-law search, finite-field lane assignment, deterministic certificate serialization
#   auth_boundary: none
#   storage_boundary: caller-supplied local path only through write_phase_lift_family_certificate
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_phase_lift.py
#   rollout: nonselecting P7-first witness; pair and triad readouts follow the global solution
#   rollback: remove this module with prime_phase_lift_data, prime_phase_lift_model, their test, document, and generated certificate
#   requires: ucns_prime_primitives_p7_p5
#   since: 2026-08-11
#   unresolved: smooth lift replacement, whole-ribbon disjointness, tangent regularization, boundary topology, ambient isotopy, spectral operator, zeta correspondence
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: prime_phase_lift_constructs_p7_before_restrictions
#   given: the phase-lift family is built
#   then: P7 is solved globally on seven carriers and thirteen hypernodes before pair or triad readouts
#   class: doctrine
#   since: 2026-08-11
#
# id: prime_phase_lift_is_seam_compatible
#   given: a carrier surface is evaluated
#   then: one turn reverses breadth and two turns return the same point
#   class: correctness
#   since: 2026-08-11
#
# id: prime_phase_lift_resolves_every_hypernode
#   given: any P7 or P5 hypernode
#   then: every occurrence has a distinct exact phase and lift lane
#   class: correctness
#   since: 2026-08-11
#
# id: prime_phase_lift_preserves_nary_origin
#   given: the P7 origin is evaluated
#   then: it remains one arity-six hypernode with six nonzero lanes and fifteen derived pair comparisons
#   class: doctrine
#   since: 2026-08-11
#
# id: prime_phase_lift_centerlines_are_disjoint
#   given: the complete projected pair-event ledger
#   then: every projected coincidence has nonzero height separation
#   class: correctness
#   since: 2026-08-11
#
# id: prime_phase_lift_link_numbers_are_derived
#   given: a pair has a regular two-crossing projection
#   then: linking number is computed only after the global lift is fixed
#   class: evidence
#   since: 2026-08-11
#
# id: prime_phase_lift_p5_follows_same_protocol
#   given: P7 is complete
#   then: P5 is solved independently by the same protocol
#   class: doctrine
#   since: 2026-08-11
#
# id: prime_phase_lift_receipt_is_nonselecting
#   given: the family receipt is serialized
#   then: it claims no arithmetic redefinition, electron ontology, zeta theorem, or proof of the Riemann hypothesis
#   class: doctrine
#   since: 2026-08-11
# === END CONTRACTS ===


"""P7-first prime-native Möbius phase-and-lift witness."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Mapping, Sequence

from .prime_phase_lift_data import (
    P5_CARRIER_RESIDUES, P5_NODE_GENERATORS, P5_TURNS,
    P7_CARRIER_RESIDUES, P7_NODE_GENERATORS, P7_TURNS,
)
from .prime_phase_lift_model import (
    EventSemantic, HALF_WIDTH, LANE_SPACING, LiftHypernode, LiftOccurrence,
    PairLinkReadout, PhaseLaw, PhaseLiftError, PrimePhaseLiftCandidate,
    SCHEMA_ID, SCHEMA_VERSION, SOURCE_SHA256, _min_gap, _mod1, _outer,
)
from .prime_primitives import PrimePrimitive, build_prime_five, build_prime_seven

def _dataset(prime: int):
    if prime == 7:
        return build_prime_seven(), P7_TURNS, P7_CARRIER_RESIDUES, P7_NODE_GENERATORS, 3
    if prime == 5:
        return build_prime_five(), P5_TURNS, P5_CARRIER_RESIDUES, P5_NODE_GENERATORS, 2
    raise PhaseLiftError("only P7 and P5 are supported")


def select_phase_law(prime: int) -> PhaseLaw:
    primitive, turns, _, _, _ = _dataset(prime)
    admissible = []
    for winding in range(-2 * prime, 2 * prime + 1):
        for numerator in range(1, prime):
            step, gaps = Fraction(numerator, prime), []
            for node in primitive.hypernodes:
                values = [_mod1(winding * turns[c][node.node_id] if c == "C" else _outer(c) * step) for c in node.carriers]
                gap = _min_gap(values)
                if gap == 0:
                    break
                gaps.append(gap)
            else:
                admissible.append((min(gaps), -abs(winding), int(winding > 0), -numerator, winding))
    best = max(admissible)
    return PhaseLaw(prime, best[4], Fraction(-best[3], prime), best[0], (4 * prime + 1) * (prime - 1), len(admissible))


def _centered(residue: int, prime: int) -> int:
    return residue if residue <= prime // 2 else residue - prime


def _nodes(primitive: PrimePrimitive, law: PhaseLaw, turns: Mapping[str, Mapping[str, Fraction]], residues: Mapping[str, int], generators: Mapping[str, int]) -> tuple[LiftHypernode, ...]:
    result = []
    for node in primitive.hypernodes:
        inverse = pow(generators[node.node_id], -1, primitive.prime)
        occurrences = []
        for carrier in node.carriers:
            residue = residues[carrier] * inverse % primitive.prime
            turn = turns[carrier][node.node_id]
            occurrences.append(LiftOccurrence(carrier, turn, law.phase(carrier, turn), residue, _centered(residue, primitive.prime) * LANE_SPACING))
        lifted = LiftHypernode(node.node_id, node.point, tuple(occurrences))
        if lifted.minimum_phase_gap == 0 or lifted.minimum_height_gap == 0:
            raise PhaseLiftError(f"collision at {node.node_id}")
        result.append(lifted)
    return tuple(result)


def _orientation(a: Fraction, b: Fraction) -> int:
    difference = _mod1(b - a)
    return 0 if difference in {Fraction(0), Fraction(1, 2)} else (1 if difference < Fraction(1, 2) else -1)


def _pairs(primitive: PrimePrimitive, nodes: Sequence[LiftHypernode]) -> tuple[PairLinkReadout, ...]:
    result = []
    for left, right, _ in primitive.pair_distance_squared:
        common = sorted((node for node in nodes if {left, right} <= {item.carrier for item in node.occurrences}), key=lambda node: node.node_id)
        signs, regular = [], len(common) == 2
        for node in common:
            a, b = node.occurrence(left), node.occurrence(right)
            orientation = _orientation(a.turn, b.turn)
            regular &= orientation != 0
            order = (a.height > b.height) - (a.height < b.height)
            signs.append(order * orientation)
        result.append(PairLinkReadout(left, right, tuple(node.node_id for node in common), sum(signs) // 2 if regular else None))
    return tuple(result)


def _build(prime: int) -> PrimePhaseLiftCandidate:
    primitive, turns, residues, generators, root = _dataset(prime)
    law = select_phase_law(prime)
    nodes = _nodes(primitive, law, turns, residues, generators)
    candidate = PrimePhaseLiftCandidate(primitive, law, nodes, _pairs(primitive, nodes), root)
    if candidate.event_ribbon_clearance <= 0:
        raise PhaseLiftError("event ribbon margin consumed")
    return candidate


def build_prime_seven_phase_lift() -> PrimePhaseLiftCandidate:
    return _build(7)


def build_prime_five_phase_lift() -> PrimePhaseLiftCandidate:
    return _build(5)


def phase_lift_family_certificate() -> dict[str, object]:
    payload: dict[str, object] = {
        "schema_id": f"{SCHEMA_ID}.family",
        "schema_version": SCHEMA_VERSION,
        "authority": "Erin Spencer",
        "recorded_on": "2026-08-11",
        "selection_effect": "none",
        "research_order": [7, 5],
        "source": {"name": "Möbius Strips and Quantum Geometry.txt", "sha256": SOURCE_SHA256, "line_basis": [5, 6, 13, 14, 15, 16, 17]},
        "construction_lineage": "global prime primitive first; pair and triad restrictions derived afterward",
        "p7": build_prime_seven_phase_lift().summary(),
        "p5": build_prime_five_phase_lift().summary(),
        "unresolved": ["smooth lift", "whole-ribbon collision certificate", "tangent regularization", "boundary topology", "ambient isotopy", "spectral operator", "zeta correspondence"],
        "nonclaims": ["no arithmetic redefinition", "no electron ontology", "no zeta theorem", "no proof of the Riemann hypothesis"],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    payload["payload_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return payload


def write_phase_lift_family_certificate(path: str | Path) -> Path:
    output = Path(path); output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(phase_lift_family_certificate(), indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    return output
