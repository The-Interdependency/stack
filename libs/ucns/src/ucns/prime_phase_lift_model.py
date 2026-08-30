# === MODULE_BUILD ===
# id: ucns_prime_phase_lift_model
#   module_name: prime_phase_lift_model
#   module_kind: experiment
#   summary: defines the typed exact phase, lift, event-semantic, geometric, and derived pair-link readouts for the P7-first witness
#   owner: Erin Spencer
#   public_surface: EventSemantic, PhaseLaw, LiftOccurrence, LiftHypernode, PairLinkReadout, PrimePhaseLiftCandidate, PhaseLiftError
#   internal_surface: exact modular phase helpers, height-gap calculation, component and cycle-rank readouts
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_phase_lift.py
#   rollout: typed research model; projected coincidence remains distinct from physical contact
#   rollback: remove with the complete prime phase-and-lift witness
#   requires: ucns_prime_phase_lift_data, ucns_prime_primitives_p7_p5
#   since: 2026-08-11
#   unresolved: smooth lift replacement, whole-ribbon disjointness, tangent regularization, ambient isotopy
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: prime_phase_lift_model_preserves_event_semantics
#   given: a lifted projected event is represented
#   then: projected coincidence and strict braid order remain typed separately and no physical contact is inferred
#   class: doctrine
#   since: 2026-08-11
#
# id: prime_phase_lift_model_derives_links_after_global_lift
#   given: pair readouts are requested from a complete phase-and-lift candidate
#   then: link readouts are derived from the globally fixed occurrence heights rather than used as construction inputs
#   class: evidence
#   since: 2026-08-11
# === END CONTRACTS ===

"""Data model and geometric readouts for the P7-first phase-and-lift witness."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
import itertools
import math
from typing import Sequence

from .prime_phase_lift_data import P5_CENTERS, P7_CENTERS
from .prime_primitives import PrimePrimitive, cycle_rank

SCHEMA_ID = "ucns.prime-phase-lift"
SCHEMA_VERSION = "0.1.0"
SOURCE_SHA256 = "dc3a94ca5070ffff8f2a246f48db77192b08f521e721bc7c2a011aa05ddeb9a1"
HALF_WIDTH = Fraction(1, 100)
LANE_SPACING = Fraction(1, 10)

class PhaseLiftError(ValueError):
    pass


class EventSemantic(str, Enum):
    PROJECTED_COINCIDENCE = "projected-centerline-coincidence"
    STRICT_BRAID_ORDER = "strict-braid-order"


def _text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _mod1(value: Fraction) -> Fraction:
    return value % 1


def _outer(carrier: str) -> int:
    return int(carrier[1:])


def _min_gap(values: Sequence[Fraction]) -> Fraction:
    ordered = sorted(values)
    if len(set(ordered)) != len(ordered):
        return Fraction(0)
    return min([b - a for a, b in zip(ordered, ordered[1:])] + [ordered[0] + 1 - ordered[-1]])


@dataclass(frozen=True, slots=True)
class PhaseLaw:
    prime: int
    center_winding: int
    outer_step: Fraction
    minimum_gap: Fraction
    candidates: int
    admissible: int

    def unwrapped(self, carrier: str, turn: Fraction) -> Fraction:
        return self.center_winding * turn if carrier == "C" else _outer(carrier) * self.outer_step

    def phase(self, carrier: str, turn: Fraction) -> Fraction:
        return _mod1(self.unwrapped(carrier, turn))


@dataclass(frozen=True, slots=True)
class LiftOccurrence:
    carrier: str
    turn: Fraction
    phase: Fraction
    residue: int
    height: Fraction


@dataclass(frozen=True, slots=True)
class LiftHypernode:
    node_id: str
    point: tuple[str, str]
    occurrences: tuple[LiftOccurrence, ...]

    @property
    def arity(self) -> int:
        return len(self.occurrences)

    @property
    def minimum_phase_gap(self) -> Fraction:
        return _min_gap([item.phase for item in self.occurrences])

    @property
    def minimum_height_gap(self) -> Fraction:
        return min(abs(a.height - b.height) for a, b in itertools.combinations(self.occurrences, 2))

    def occurrence(self, carrier: str) -> LiftOccurrence:
        return next(item for item in self.occurrences if item.carrier == carrier)


@dataclass(frozen=True, slots=True)
class PairLinkReadout:
    left: str
    right: str
    node_ids: tuple[str, ...]
    linking_number: int | None


@dataclass(frozen=True, slots=True)
class PrimePhaseLiftCandidate:
    primitive: PrimePrimitive
    phase_law: PhaseLaw
    hypernodes: tuple[LiftHypernode, ...]
    pair_readouts: tuple[PairLinkReadout, ...]
    primitive_root: int

    @property
    def prime(self) -> int:
        return self.primitive.prime

    @property
    def carriers(self) -> tuple[str, ...]:
        return ("C", *(f"R{i}" for i in range(self.prime - 1)))

    @property
    def origin(self) -> LiftHypernode:
        return next(node for node in self.hypernodes if node.point == ("0", "0"))

    @property
    def minimum_height_gap(self) -> Fraction:
        return min(node.minimum_height_gap for node in self.hypernodes)

    @property
    def event_ribbon_clearance(self) -> Fraction:
        return self.minimum_height_gap - 2 * HALF_WIDTH

    @property
    def origin_void_lower_bound(self) -> Fraction:
        return min(abs(item.height) for item in self.origin.occurrences) - HALF_WIDTH

    def _knots(self, carrier: str) -> tuple[tuple[Fraction, Fraction], ...]:
        return tuple(sorted((item.turn, item.height) for node in self.hypernodes for item in node.occurrences if item.carrier == carrier))

    def lift(self, carrier: str, turn: Fraction) -> Fraction:
        knots, target = self._knots(carrier), _mod1(turn)
        for index, (a_t, a_z) in enumerate(knots):
            b_t, b_z = knots[(index + 1) % len(knots)]
            if index == len(knots) - 1:
                b_t += 1
                if target < a_t:
                    target += 1
            if a_t <= target <= b_t:
                if target == a_t:
                    return a_z
                ratio = (target - a_t) / (b_t - a_t)
                return a_z + ratio * (b_z - a_z)
        raise AssertionError("periodic interpolation failed")

    def centerline_point(self, carrier: str, turn: Fraction) -> tuple[float, float, float]:
        cx, cy = (P7_CENTERS if self.prime == 7 else P5_CENTERS)[carrier]
        angle = math.tau * float(turn)
        return cx + math.cos(angle), cy + math.sin(angle), float(self.lift(carrier, turn))

    def surface_point(self, carrier: str, turn: Fraction, breadth: Fraction) -> tuple[float, float, float]:
        if abs(breadth) > HALF_WIDTH:
            raise PhaseLiftError("breadth exceeds half width")
        x, y, z = self.centerline_point(carrier, turn)
        theta = math.tau * float(turn)
        frame = math.tau * float(Fraction(1, 2) * turn + self.phase_law.unwrapped(carrier, turn))
        radial = float(breadth) * math.cos(frame)
        return x + radial * math.cos(theta), y + radial * math.sin(theta), z + float(breadth) * math.sin(frame)

    def seam_residuals(self) -> tuple[float, float]:
        one = two = 0.0
        for carrier in self.carriers:
            for turn in (Fraction(0), Fraction(1, 13), Fraction(5, 17)):
                for breadth in (-HALF_WIDTH, Fraction(0), HALF_WIDTH):
                    one = max(one, math.dist(self.surface_point(carrier, turn + 1, breadth), self.surface_point(carrier, turn, -breadth)))
                    two = max(two, math.dist(self.surface_point(carrier, turn + 2, breadth), self.surface_point(carrier, turn, breadth)))
        return one, two

    @property
    def link_summary(self) -> dict[str, object]:
        issued = [item for item in self.pair_readouts if item.linking_number is not None]
        nonzero = [item for item in issued if item.linking_number]
        values = sorted({item.linking_number for item in issued})
        counts = {str(value): sum(item.linking_number == value for item in issued) for value in values}
        edges = [(item.left, item.right) for item in nonzero]
        components = _components(self.carriers, edges)
        return {
            "regular_linking_number_counts": counts,
            "nonzero_link_pairs": len(nonzero),
            "tangent_pairs_unresolved": len(self.pair_readouts) - len(issued),
            "nonzero_link_graph": {"edges": len(edges), "components": components, "cycle_rank": cycle_rank(len(self.carriers), len(edges), components)},
        }

    def summary(self) -> dict[str, object]:
        one, two = self.seam_residuals()
        return {
            "prime": self.prime,
            "carriers": len(self.carriers),
            "hypernodes": len(self.hypernodes),
            "arity_spectrum": self.primitive.arity_spectrum,
            "phase_law": {"center_winding": self.phase_law.center_winding, "outer_step": _text(self.phase_law.outer_step), "minimum_gap": _text(self.phase_law.minimum_gap), "candidates": self.phase_law.candidates, "admissible": self.phase_law.admissible},
            "lift": {"field": f"F_{self.prime}", "primitive_root": self.primitive_root, "minimum_height_gap": _text(self.minimum_height_gap), "event_ribbon_clearance": _text(self.event_ribbon_clearance), "origin_void_lower_bound": _text(self.origin_void_lower_bound), "origin_heights": [_text(item.height) for item in self.origin.occurrences]},
            "mobius_return": {"one_turn_residual": one, "two_turn_residual": two},
            "event_semantics": [EventSemantic.PROJECTED_COINCIDENCE.value, EventSemantic.STRICT_BRAID_ORDER.value],
            "physical_centerline_contacts_claimed": 0,
            "physical_boundary_contacts_claimed": 0,
            "centerline_link": "pairwise disjoint by complete projected-event separation",
            "link_summary": self.link_summary,
        }


def _components(vertices: Sequence[str], edges: Sequence[tuple[str, str]]) -> int:
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right); adjacency[right].add(left)
    seen, count = set(), 0
    for start in vertices:
        if start in seen:
            continue
        count += 1; pending = [start]
        while pending:
            vertex = pending.pop()
            if vertex in seen:
                continue
            seen.add(vertex); pending.extend(adjacency[vertex] - seen)
    return count
