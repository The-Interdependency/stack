# === MODULE_BUILD ===
# id: ucns_mobius_seed_of_life_candidate
#   module_name: mobius_seed
#   module_kind: experiment
#   summary: constructs the seven-band Mobius Seed of Life as an exact projection ledger plus a deterministic nonselecting three-dimensional braid-lift candidate
#   owner: Erin Spencer
#   public_surface: Qsqrt3, ExactPoint2, Point3, BandSlot, TwistChirality, PairStanding, NodeStanding, ProjectionNode, PairProjectionEvent, PairRelation, MobiusBandSpec, MobiusSeedOfLife, build_mobius_seed_of_life
#   internal_surface: exact sextant trigonometry, incidence construction, candidate validation, deterministic OBJ serialization
#   auth_boundary: none
#   storage_boundary: caller-supplied local paths only through write_obj and write_receipt
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_mobius_seed.py
#   rollout: explicit UCNS-only implemented candidate; selection effect none; no canonical seven-gonol composition, zeta proof, physical-model validation, EDCM activation, or METAPAT activation
#   rollback: remove this module, its tests, and MOBIUS_SEED_OF_LIFE_V1 documents without altering arity-one, arity-two, or arity-three relationship-display primitives
#   requires: ucns_gonol_relationship_display_v1, edcm_native_direct_mobius_candidate
#   since: 2026-08-10
#   unresolved: smooth boundary-edge intersection realization, pairwise linking matrix, ambient-isotopy lock proof, canonical seven-gonol composition, spectral operator, zeta-zero correspondence, proof-assistant formalization
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: mobius_seed_projection_is_exact_and_pair_complete
#   given: the default Mobius Seed of Life candidate is constructed
#   then: seven equal-radius operands, all twenty-one unordered pairs, thirteen unique projection nodes, twelve structural vesicas, six incidental secants, and three incidental tangencies are retained without hidden pair deletion
#   class: correctness
#   since: 2026-08-10
#
# id: mobius_seed_dyad_is_anti_aligned_and_outer_phase_is_incremental
#   given: the default seven-band schedule is inspected
#   then: the central band and first outer band have opposite chirality and half-turn seam displacement while the six outer seam phases advance by one twelfth turn
#   class: evidence
#   since: 2026-08-10
#
# id: mobius_seed_lift_preserves_null_as_nonvertex_void
#   given: coincident projected occurrences are lifted into three dimensions
#   then: every incident band has a distinct exact lift height, the six outer strands occupy nonzero one-two-three lane pairs at the center, and exact origin exclusion plus compactness preserves a positive three-dimensional void
#   class: safety
#   since: 2026-08-10
#
# id: mobius_seed_surface_obeys_360_seam_and_720_return
#   given: any default band surface point is advanced one or two carrier turns
#   then: one turn equals the seam-identified point at reversed breadth and two turns restore the complete sampled point
#   class: correctness
#   since: 2026-08-10
#
# id: mobius_seed_structural_pairs_have_alternating_braid_order
#   given: either projected crossing of each structural vesica is inspected
#   then: the exact lift-height difference is nonzero at both events and changes sign between them without claiming physical contact or a verified boundary-edge intersection
#   class: evidence
#   since: 2026-08-10
#
# id: mobius_seed_candidate_is_nonselecting_and_proof_firewalled
#   given: a receipt or OBJ realization is emitted
#   then: the artifact records selection effect none and explicitly denies zeta proof, electron ontology, Pauli-derived geometry, verified linking, and canonical UCNS completion
#   class: doctrine
#   since: 2026-08-10
# === END CONTRACTS ===

"""Exact projection ledger and deterministic braid-lift candidate for the full
seven-band UCNS Möbius Seed of Life.

The construction implements geometry and falsifiable evidence only. It does not
claim a zeta-function proof, a physical electron model, verified boundary-edge
contacts, a linking matrix, or canonical UCNS completion.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path

MOBIUS_SEED_SCHEMA_ID = "ucns.mobius-seed-of-life"
MOBIUS_SEED_SCHEMA_VERSION = "0.1.0"
MOBIUS_SEED_SELECTION_EFFECT = "none"
MOBIUS_SEED_PROJECTION_ID = "seed-of-life-seven-equal-circles"
MOBIUS_SEED_LIFT_ID = "ucns.mobius-seed.sin-two-theta-lane-lift"
MOBIUS_SEED_LIFT_VERSION = "0.1.0"
SOURCE_DOCUMENT_NAME = "Möbius Strips and Quantum Geometry.txt"
SOURCE_DOCUMENT_SHA256 = "dc3a94ca5070ffff8f2a246f48db77192b08f521e721bc7c2a011aa05ddeb9a1"
TARGET_UCNS_BASE_COMMIT = "560743ce429f18ef595bc438e327d76344aa5993"


class MobiusSeedError(ValueError):
    """Raised when the candidate violates its declared construction boundary."""


def _fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _as_fraction(value: int | Fraction, field: str) -> Fraction:
    if isinstance(value, bool):
        raise MobiusSeedError(f"{field} cannot be boolean")
    if isinstance(value, int):
        return Fraction(value)
    if not isinstance(value, Fraction):
        raise MobiusSeedError(f"{field} must be int or exact Fraction")
    return value


def _mod_one(value: Fraction) -> Fraction:
    return value - value.numerator // value.denominator


@dataclass(frozen=True, slots=True)
class Qsqrt3:
    """An exact element ``a + b*sqrt(3)`` with rational coefficients."""

    rational: Fraction = Fraction(0)
    sqrt3: Fraction = Fraction(0)

    def __post_init__(self) -> None:
        if not isinstance(self.rational, Fraction) or not isinstance(self.sqrt3, Fraction):
            raise MobiusSeedError("Qsqrt3 coefficients must be exact Fractions")

    @classmethod
    def rational_value(cls, value: int | Fraction) -> Qsqrt3:
        return cls(_as_fraction(value, "rational value"), Fraction(0))

    def __add__(self, other: object) -> Qsqrt3:
        if isinstance(other, (int, Fraction)) and not isinstance(other, bool):
            other = Qsqrt3.rational_value(other)
        if not isinstance(other, Qsqrt3):
            return NotImplemented
        return Qsqrt3(self.rational + other.rational, self.sqrt3 + other.sqrt3)

    __radd__ = __add__

    def __sub__(self, other: object) -> Qsqrt3:
        if isinstance(other, (int, Fraction)) and not isinstance(other, bool):
            other = Qsqrt3.rational_value(other)
        if not isinstance(other, Qsqrt3):
            return NotImplemented
        return Qsqrt3(self.rational - other.rational, self.sqrt3 - other.sqrt3)

    def __neg__(self) -> Qsqrt3:
        return Qsqrt3(-self.rational, -self.sqrt3)

    def __mul__(self, other: object) -> Qsqrt3:
        if isinstance(other, (int, Fraction)) and not isinstance(other, bool):
            scalar = _as_fraction(other, "scalar")
            return Qsqrt3(self.rational * scalar, self.sqrt3 * scalar)
        if not isinstance(other, Qsqrt3):
            return NotImplemented
        return Qsqrt3(
            self.rational * other.rational + 3 * self.sqrt3 * other.sqrt3,
            self.rational * other.sqrt3 + self.sqrt3 * other.rational,
        )

    __rmul__ = __mul__

    def square(self) -> Qsqrt3:
        return self * self

    def sign(self) -> int:
        a, b = self.rational, self.sqrt3
        if a == 0:
            return (b > 0) - (b < 0)
        if b == 0:
            return (a > 0) - (a < 0)
        if a > 0 and b > 0:
            return 1
        if a < 0 and b < 0:
            return -1
        a2, radical2 = a * a, 3 * b * b
        if a2 == radical2:
            return 0
        if a > 0:
            return 1 if a2 > radical2 else -1
        return -1 if a2 > radical2 else 1

    def to_float(self) -> float:
        return float(self.rational) + float(self.sqrt3) * math.sqrt(3.0)

    def exact_text(self) -> str:
        return f"({_fraction_text(self.rational)})+({_fraction_text(self.sqrt3)})*sqrt(3)"

    def as_dict(self) -> dict[str, str | float]:
        return {
            "rational": _fraction_text(self.rational),
            "sqrt3_coefficient": _fraction_text(self.sqrt3),
            "exact": self.exact_text(),
            "binary64": self.to_float(),
        }


ZERO_Q3 = Qsqrt3()
ONE_Q3 = Qsqrt3.rational_value(1)
HALF_Q3 = Qsqrt3.rational_value(Fraction(1, 2))
SQRT3_HALF = Qsqrt3(sqrt3=Fraction(1, 2))


@dataclass(frozen=True, slots=True)
class ExactPoint2:
    x: Qsqrt3
    y: Qsqrt3

    def __add__(self, other: ExactPoint2) -> ExactPoint2:
        return ExactPoint2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: ExactPoint2) -> ExactPoint2:
        return ExactPoint2(self.x - other.x, self.y - other.y)

    def squared_distance_to(self, other: ExactPoint2) -> Qsqrt3:
        delta = self - other
        return delta.x.square() + delta.y.square()

    def to_float(self) -> tuple[float, float]:
        return self.x.to_float(), self.y.to_float()

    def as_dict(self) -> dict[str, object]:
        return {"x": self.x.as_dict(), "y": self.y.as_dict()}


ORIGIN_2 = ExactPoint2(ZERO_Q3, ZERO_Q3)


@dataclass(frozen=True, slots=True)
class Point3:
    x: float
    y: float
    z: float

    def distance_to(self, other: Point3) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2)


class BandSlot(str, Enum):
    CENTER = "CENTER"
    RING_0 = "RING_0"
    RING_1 = "RING_1"
    RING_2 = "RING_2"
    RING_3 = "RING_3"
    RING_4 = "RING_4"
    RING_5 = "RING_5"

    @property
    def ring_index(self) -> int | None:
        return None if self is BandSlot.CENTER else int(self.value.rsplit("_", 1)[1])


RING_SLOTS = (
    BandSlot.RING_0,
    BandSlot.RING_1,
    BandSlot.RING_2,
    BandSlot.RING_3,
    BandSlot.RING_4,
    BandSlot.RING_5,
)


def _ring_slot(index: int) -> BandSlot:
    return RING_SLOTS[index % 6]


class TwistChirality(int, Enum):
    POSITIVE = 1
    NEGATIVE = -1


class PairStanding(str, Enum):
    STRUCTURAL_VESICA = "structural-vesica"
    INCIDENTAL_SECANT = "incidental-secant"
    INCIDENTAL_TANGENCY = "incidental-tangency"


class NodeStanding(str, Enum):
    NULL_PROJECTION = "null-projection-nonvertex"
    RING_COINCIDENCE = "ring-center-projection-coincidence"
    PETAL_INTERSECTION = "external-petal-projection-intersection"


@dataclass(frozen=True, slots=True)
class ProjectionNode:
    node_id: str
    point: ExactPoint2
    incident_slots: tuple[BandSlot, ...]
    standing: NodeStanding
    is_vertex: bool = False
    is_structural_null: bool = False

    def __post_init__(self) -> None:
        if not self.node_id or not self.incident_slots:
            raise MobiusSeedError("projection node identity and incidents are required")
        if len(set(self.incident_slots)) != len(self.incident_slots):
            raise MobiusSeedError("projection-node incidents must be unique")
        if self.is_vertex or self.is_structural_null:
            raise MobiusSeedError("display coincidence cannot be promoted to vertex or Structural Null")


@dataclass(frozen=True, slots=True)
class PairProjectionEvent:
    event_id: str
    node_id: str
    left_turn: Fraction
    right_turn: Fraction

    def __post_init__(self) -> None:
        if not self.event_id or not self.node_id:
            raise MobiusSeedError("pair-event identity is required")
        if _mod_one(self.left_turn) != self.left_turn or _mod_one(self.right_turn) != self.right_turn:
            raise MobiusSeedError("pair-event turns must be canonical in [0,1)")


@dataclass(frozen=True, slots=True)
class PairRelation:
    relation_id: str
    left: BandSlot
    right: BandSlot
    standing: PairStanding
    center_distance_squared: int
    events: tuple[PairProjectionEvent, ...]
    declared_boundary_relation_events: int | None
    boundary_realization_standing: str

    @property
    def unordered_key(self) -> frozenset[BandSlot]:
        return frozenset((self.left, self.right))

    def __post_init__(self) -> None:
        expected = {
            PairStanding.STRUCTURAL_VESICA: (1, 2),
            PairStanding.INCIDENTAL_SECANT: (3, 2),
            PairStanding.INCIDENTAL_TANGENCY: (4, 1),
        }[self.standing]
        if self.left is self.right or not self.relation_id:
            raise MobiusSeedError("pair relation needs two distinct identified slots")
        if (self.center_distance_squared, len(self.events)) != expected:
            raise MobiusSeedError("pair relation distance/event count mismatch")
        if self.standing is PairStanding.STRUCTURAL_VESICA:
            if self.declared_boundary_relation_events != 4:
                raise MobiusSeedError("structural pair must retain four source-declared boundary events")
        elif self.declared_boundary_relation_events is not None:
            raise MobiusSeedError("incidental pair cannot inherit structural boundary count")
        if not self.boundary_realization_standing:
            raise MobiusSeedError("boundary realization standing is required")


@dataclass(frozen=True, slots=True)
class MobiusBandSpec:
    slot: BandSlot
    center: ExactPoint2
    chirality: TwistChirality
    twist_phase_turns: Fraction
    braid_bias: Qsqrt3

    def __post_init__(self) -> None:
        if _mod_one(self.twist_phase_turns) != self.twist_phase_turns:
            raise MobiusSeedError("twist phase must be canonical in [0,1)")


@dataclass(frozen=True, slots=True)
class MobiusSeedOfLife:
    bands: tuple[MobiusBandSpec, ...]
    nodes: tuple[ProjectionNode, ...]
    relations: tuple[PairRelation, ...]
    radius: Fraction = Fraction(1)
    lift_amplitude: Fraction = Fraction(1, 5)
    half_width: Fraction = Fraction(1, 100)
    schema_id: str = MOBIUS_SEED_SCHEMA_ID
    schema_version: str = MOBIUS_SEED_SCHEMA_VERSION
    selection_effect: str = MOBIUS_SEED_SELECTION_EFFECT
    hmmm: tuple[str, ...] = (
        "the source-declared four boundary events per structural pair remain relation events until a smooth boundary-edge realization is verified",
        "pairwise linking numbers and a locked ambient-isotopy class remain unresolved",
        "the canonical UCNS seven-gonol composition and option-registry standing remain separate decisions",
        "no spectral operator or correspondence with the nontrivial zeros of the zeta function has been supplied",
        "no electron ontology, Pauli-derived geometry, empirical quantum model, EDCM activation, or METAPAT activation is claimed",
    )

    def __post_init__(self) -> None:
        for value, field in ((self.radius, "radius"), (self.lift_amplitude, "lift_amplitude"), (self.half_width, "half_width")):
            if not isinstance(value, Fraction) or value <= 0:
                raise MobiusSeedError(f"{field} must be a positive exact Fraction")
        if self.half_width >= self.radius:
            raise MobiusSeedError("half width must be smaller than radius")
        if self.schema_id != MOBIUS_SEED_SCHEMA_ID or self.schema_version != MOBIUS_SEED_SCHEMA_VERSION:
            raise MobiusSeedError("Möbius Seed schema identity mismatch")
        if self.selection_effect != MOBIUS_SEED_SELECTION_EFFECT:
            raise MobiusSeedError("candidate cannot select UCNS canon")
        if not self.hmmm or any(not item.strip() for item in self.hmmm):
            raise MobiusSeedError("candidate must retain explicit hmmm boundaries")
        self._validate()

    @property
    def band_by_slot(self) -> dict[BandSlot, MobiusBandSpec]:
        return {band.slot: band for band in self.bands}

    @property
    def node_by_id(self) -> dict[str, ProjectionNode]:
        return {node.node_id: node for node in self.nodes}

    @property
    def structural_relations(self) -> tuple[PairRelation, ...]:
        return tuple(r for r in self.relations if r.standing is PairStanding.STRUCTURAL_VESICA)

    @property
    def incidental_secants(self) -> tuple[PairRelation, ...]:
        return tuple(r for r in self.relations if r.standing is PairStanding.INCIDENTAL_SECANT)

    @property
    def incidental_tangencies(self) -> tuple[PairRelation, ...]:
        return tuple(r for r in self.relations if r.standing is PairStanding.INCIDENTAL_TANGENCY)

    @property
    def pairwise_projection_event_count(self) -> int:
        return sum(len(r.events) for r in self.relations)

    @property
    def declared_structural_boundary_event_count(self) -> int:
        return sum(r.declared_boundary_relation_events or 0 for r in self.structural_relations)

    def exact_projected_point(self, slot: BandSlot, turn: Fraction) -> ExactPoint2:
        band = self.band_by_slot[slot]
        unit = _unit_circle_exact(turn)
        return ExactPoint2(band.center.x + unit.x * self.radius, band.center.y + unit.y * self.radius)

    def exact_braid_height_at_event(self, slot: BandSlot, turn: Fraction) -> Qsqrt3:
        return (_sin_two_theta_exact(turn) + self.band_by_slot[slot].braid_bias) * self.lift_amplitude

    def lifted_occurrences(self, node_id: str) -> tuple[tuple[BandSlot, Fraction, Qsqrt3], ...]:
        node = self.node_by_id[node_id]
        turns = self._event_turns()
        return tuple((slot, turns[(node_id, slot)], self.exact_braid_height_at_event(slot, turns[(node_id, slot)])) for slot in node.incident_slots)

    def null_lane_heights_exact(self) -> tuple[Qsqrt3, ...]:
        return tuple(height for _, _, height in self.lifted_occurrences("NULL"))

    def origin_contact_margin_exact(self) -> Qsqrt3:
        magnitudes = tuple(h if h.sign() > 0 else -h for h in self.null_lane_heights_exact())
        smallest = magnitudes[0]
        for value in magnitudes[1:]:
            if (value - smallest).sign() < 0:
                smallest = value
        return smallest - self.half_width

    def centerline_point(self, slot: BandSlot, turn: float | Fraction) -> Point3:
        if isinstance(turn, bool) or not isinstance(turn, (int, float, Fraction)):
            raise MobiusSeedError("turn must be numeric and nonboolean")
        band = self.band_by_slot[slot]
        t = float(turn)
        theta = math.tau * t
        cx, cy = band.center.to_float()
        radius = float(self.radius)
        z = float(self.lift_amplitude) * (math.sin(2 * theta) + band.braid_bias.to_float())
        return Point3(cx + radius * math.cos(theta), cy + radius * math.sin(theta), z)

    def surface_point(self, slot: BandSlot, turn: float | Fraction, breadth: float | Fraction) -> Point3:
        if isinstance(breadth, bool) or not isinstance(breadth, (int, float, Fraction)):
            raise MobiusSeedError("breadth must be numeric and nonboolean")
        b = float(breadth)
        if abs(b) > float(self.half_width) + 1e-15:
            raise MobiusSeedError("breadth exceeds declared half width")
        band = self.band_by_slot[slot]
        t = float(turn)
        theta = math.tau * t
        twist = band.chirality.value * math.pi * t + math.tau * float(band.twist_phase_turns)
        core = self.centerline_point(slot, t)
        radial = b * math.cos(twist)
        vertical = b * math.sin(twist)
        return Point3(core.x + radial * math.cos(theta), core.y + radial * math.sin(theta), core.z + vertical)

    def boundary_point(self, slot: BandSlot, boundary_turn: float | Fraction) -> Point3:
        return self.surface_point(slot, boundary_turn, self.half_width)

    def structural_braid_differences(self, relation: PairRelation) -> tuple[Qsqrt3, Qsqrt3]:
        if relation.standing is not PairStanding.STRUCTURAL_VESICA:
            raise MobiusSeedError("braid-order contract applies only to structural pairs")
        values = tuple(
            self.exact_braid_height_at_event(relation.left, event.left_turn)
            - self.exact_braid_height_at_event(relation.right, event.right_turn)
            for event in relation.events
        )
        return values[0], values[1]

    def receipt(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "authority": "Erin Spencer",
            "recorded_on": "2026-08-10",
            "record_status": "authority-directed-implemented-candidate",
            "selection_effect": self.selection_effect,
            "jurisdiction": {
                "construction_owner": "UCNS",
                "metapat_role": "later semantic consumer only; no geometry or theorem-status transfer",
                "edcm_activation": False,
                "metapat_activation": False,
            },
            "source_basis": {
                "name": SOURCE_DOCUMENT_NAME,
                "sha256": SOURCE_DOCUMENT_SHA256,
                "target_ucns_base_commit": TARGET_UCNS_BASE_COMMIT,
            },
            "construction": {
                "primitive_arity": 7,
                "projection_id": MOBIUS_SEED_PROJECTION_ID,
                "lift_id": MOBIUS_SEED_LIFT_ID,
                "lift_version": MOBIUS_SEED_LIFT_VERSION,
                "radius": _fraction_text(self.radius),
                "lift_amplitude": _fraction_text(self.lift_amplitude),
                "half_width": _fraction_text(self.half_width),
                "surface_identification": "X(t+1,b)=X(t,-b)",
                "local_return": "X(t+2,b)=X(t,b)",
            },
            "counts": {
                "bands": len(self.bands),
                "all_unordered_pairs": len(self.relations),
                "structural_vesica_pairs": len(self.structural_relations),
                "incidental_secant_pairs": len(self.incidental_secants),
                "incidental_tangent_pairs": len(self.incidental_tangencies),
                "unique_projection_nodes": len(self.nodes),
                "pairwise_projection_events": self.pairwise_projection_event_count,
                "source_declared_structural_boundary_relation_events": self.declared_structural_boundary_event_count,
            },
            "bands": [
                {
                    "slot": b.slot.value,
                    "center": b.center.as_dict(),
                    "chirality": b.chirality.name.lower(),
                    "twist_phase_turns": _fraction_text(b.twist_phase_turns),
                    "braid_bias": b.braid_bias.as_dict(),
                }
                for b in self.bands
            ],
            "nodes": [
                {
                    "node_id": n.node_id,
                    "point": n.point.as_dict(),
                    "incident_slots": [slot.value for slot in n.incident_slots],
                    "standing": n.standing.value,
                    "is_vertex": n.is_vertex,
                    "is_structural_null": n.is_structural_null,
                    "lifted_occurrences": [
                        {"slot": slot.value, "turn": _fraction_text(turn), "height": height.as_dict()}
                        for slot, turn, height in self.lifted_occurrences(n.node_id)
                    ],
                }
                for n in self.nodes
            ],
            "relations": [
                {
                    "relation_id": r.relation_id,
                    "left": r.left.value,
                    "right": r.right.value,
                    "standing": r.standing.value,
                    "center_distance_squared": r.center_distance_squared,
                    "events": [
                        {
                            "event_id": e.event_id,
                            "node_id": e.node_id,
                            "left_turn": _fraction_text(e.left_turn),
                            "right_turn": _fraction_text(e.right_turn),
                        }
                        for e in r.events
                    ],
                    "declared_boundary_relation_events": r.declared_boundary_relation_events,
                    "boundary_realization_standing": r.boundary_realization_standing,
                }
                for r in self.relations
            ],
            "null": {
                "projection_point": ORIGIN_2.as_dict(),
                "semantics": "topological anchor and compactness-backed three-dimensional void candidate; not a vertex and not promoted to Structural Null",
                "lane_heights": [height.as_dict() for height in self.null_lane_heights_exact()],
                "origin_contact_margin": self.origin_contact_margin_exact().as_dict(),
                "global_void_radius_standing": "positive by compactness after exact origin exclusion; closed-form maximum radius unresolved",
            },
            "nonclaims": [
                "not a proof of the Riemann hypothesis or any zeta-function theorem",
                "not a spectral operator or a correspondence with zeta zeros",
                "not an established electron model or Pauli-exclusion derivation",
                "not a verified four-intersection smooth boundary embedding",
                "not a verified Hopf-link matrix or locked ambient-isotopy class",
                "not a complete UCNSObject or canonical seven-gonol composition",
                "not EDCM measurement validity or METAPAT validity",
            ],
            "hmmm": list(self.hmmm),
        }

    def receipt_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.receipt(), indent=indent, ensure_ascii=False) + "\n"

    def write_receipt(self, path: str | Path, *, indent: int = 2) -> Path:
        output = Path(path)
        output.write_text(self.receipt_json(indent=indent), encoding="utf-8")
        return output

    def obj_text(self, *, longitudinal_segments: int = 144, breadth_segments: int = 8) -> str:
        if isinstance(longitudinal_segments, bool) or not isinstance(longitudinal_segments, int) or longitudinal_segments < 12:
            raise MobiusSeedError("longitudinal_segments must be an integer >= 12")
        if isinstance(breadth_segments, bool) or not isinstance(breadth_segments, int) or breadth_segments < 1:
            raise MobiusSeedError("breadth_segments must be an integer >= 1")
        lines = [
            "# UCNS Mobius Seed of Life implemented candidate",
            f"# schema {self.schema_id}@{self.schema_version}",
            "# selection_effect none",
            "o ucns_mobius_seed_of_life",
        ]
        vertices: list[Point3] = []
        faces_by_band: list[tuple[BandSlot, list[tuple[int, int, int, int]]]] = []
        row = breadth_segments + 1
        for band in self.bands:
            start = len(vertices)
            for longitudinal in range(longitudinal_segments):
                turn = Fraction(longitudinal, longitudinal_segments)
                for breadth_index in range(row):
                    breadth = -self.half_width + 2 * self.half_width * Fraction(breadth_index, breadth_segments)
                    vertices.append(self.surface_point(band.slot, turn, breadth))
            faces: list[tuple[int, int, int, int]] = []
            for longitudinal in range(longitudinal_segments):
                nxt = (longitudinal + 1) % longitudinal_segments
                seam = longitudinal == longitudinal_segments - 1
                for breadth_index in range(breadth_segments):
                    a = start + longitudinal * row + breadth_index
                    d = a + 1
                    if seam:
                        b_index = breadth_segments - breadth_index
                        c_index = breadth_segments - breadth_index - 1
                    else:
                        b_index, c_index = breadth_index, breadth_index + 1
                    b = start + nxt * row + b_index
                    c = start + nxt * row + c_index
                    faces.append((a + 1, b + 1, c + 1, d + 1))
            faces_by_band.append((band.slot, faces))
        lines.extend(f"v {p.x:.17g} {p.y:.17g} {p.z:.17g}" for p in vertices)
        for slot, faces in faces_by_band:
            lines.append(f"g {slot.value}")
            lines.extend("f " + " ".join(str(index) for index in face) for face in faces)
        return "\n".join(lines) + "\n"

    def write_obj(self, path: str | Path, *, longitudinal_segments: int = 144, breadth_segments: int = 8) -> Path:
        output = Path(path)
        output.write_text(self.obj_text(longitudinal_segments=longitudinal_segments, breadth_segments=breadth_segments), encoding="utf-8")
        return output

    def _event_turns(self) -> dict[tuple[str, BandSlot], Fraction]:
        turns: dict[tuple[str, BandSlot], Fraction] = {}
        for relation in self.relations:
            for event in relation.events:
                for slot, turn in ((relation.left, event.left_turn), (relation.right, event.right_turn)):
                    key = (event.node_id, slot)
                    if key in turns and turns[key] != turn:
                        raise MobiusSeedError(f"inconsistent turn for {slot.value} at {event.node_id}")
                    turns[key] = turn
        return turns

    def _validate(self) -> None:
        slots = tuple(b.slot for b in self.bands)
        if len(self.bands) != 7 or set(slots) != set(BandSlot) or len(set(slots)) != 7:
            raise MobiusSeedError("candidate must retain exactly the seven declared slots")
        node_ids = tuple(n.node_id for n in self.nodes)
        expected_nodes = {"NULL", *(f"RING_{i}" for i in range(6)), *(f"PETAL_{i}" for i in range(6))}
        if len(self.nodes) != 13 or set(node_ids) != expected_nodes or len(set(node_ids)) != 13:
            raise MobiusSeedError("projection must retain exactly thirteen unique nodes")
        if len(self.relations) != 21:
            raise MobiusSeedError("all twenty-one unordered band pairs must be retained")
        expected_pairs = {frozenset(pair) for pair in itertools.combinations(tuple(BandSlot), 2)}
        if {r.unordered_key for r in self.relations} != expected_pairs:
            raise MobiusSeedError("pair ledger must cover every unordered pair exactly once")
        if (len(self.structural_relations), len(self.incidental_secants), len(self.incidental_tangencies)) != (12, 6, 3):
            raise MobiusSeedError("pair standing counts must be 12/6/3")
        degree = {slot: 0 for slot in BandSlot}
        for relation in self.structural_relations:
            degree[relation.left] += 1
            degree[relation.right] += 1
        if degree[BandSlot.CENTER] != 6 or any(degree[slot] != 3 for slot in RING_SLOTS):
            raise MobiusSeedError("structural pairing graph must be wheel W7")
        null = self.node_by_id["NULL"]
        if null.point != ORIGIN_2 or set(null.incident_slots) != set(RING_SLOTS):
            raise MobiusSeedError("NULL projection must retain six outer occurrences at origin")
        turns = self._event_turns()
        for node in self.nodes:
            if {slot for node_id, slot in turns if node_id == node.node_id} != set(node.incident_slots):
                raise MobiusSeedError(f"incident ledger mismatch at {node.node_id}")
            heights = [self.exact_braid_height_at_event(slot, turns[(node.node_id, slot)]) for slot in node.incident_slots]
            for left, right in itertools.combinations(heights, 2):
                if (left - right).sign() == 0:
                    raise MobiusSeedError(f"braid-lift collision at {node.node_id}")
        for relation in self.relations:
            distance = self.band_by_slot[relation.left].center.squared_distance_to(self.band_by_slot[relation.right].center)
            if distance.sqrt3 != 0 or distance.rational != relation.center_distance_squared:
                raise MobiusSeedError(f"pair distance mismatch for {relation.relation_id}")
            for event in relation.events:
                node = self.node_by_id[event.node_id]
                if self.exact_projected_point(relation.left, event.left_turn) != node.point:
                    raise MobiusSeedError(f"left event geometry mismatch for {event.event_id}")
                if self.exact_projected_point(relation.right, event.right_turn) != node.point:
                    raise MobiusSeedError(f"right event geometry mismatch for {event.event_id}")
        for relation in self.structural_relations:
            first, second = self.structural_braid_differences(relation)
            if first.sign() == 0 or second.sign() == 0 or first.sign() == second.sign():
                raise MobiusSeedError("structural pair must reverse over-under order")
        if self.origin_contact_margin_exact().sign() <= 0:
            raise MobiusSeedError("default width must exclude origin contact")


def _unit_circle_exact(turn: Fraction) -> ExactPoint2:
    table = {
        Fraction(0): ExactPoint2(ONE_Q3, ZERO_Q3),
        Fraction(1, 6): ExactPoint2(HALF_Q3, SQRT3_HALF),
        Fraction(1, 3): ExactPoint2(-HALF_Q3, SQRT3_HALF),
        Fraction(1, 2): ExactPoint2(-ONE_Q3, ZERO_Q3),
        Fraction(2, 3): ExactPoint2(-HALF_Q3, -SQRT3_HALF),
        Fraction(5, 6): ExactPoint2(HALF_Q3, -SQRT3_HALF),
    }
    try:
        return table[_mod_one(turn)]
    except KeyError as exc:
        raise MobiusSeedError("exact projection is defined at sextant event turns only") from exc


def _sin_two_theta_exact(turn: Fraction) -> Qsqrt3:
    table = {Fraction(0): ZERO_Q3, Fraction(1, 3): SQRT3_HALF, Fraction(2, 3): -SQRT3_HALF}
    try:
        return table[_mod_one(2 * turn)]
    except KeyError as exc:
        raise MobiusSeedError("exact braid height is defined at declared event turns only") from exc


def _ring_centers() -> tuple[ExactPoint2, ...]:
    return (
        ExactPoint2(ONE_Q3, ZERO_Q3),
        ExactPoint2(HALF_Q3, SQRT3_HALF),
        ExactPoint2(-HALF_Q3, SQRT3_HALF),
        ExactPoint2(-ONE_Q3, ZERO_Q3),
        ExactPoint2(-HALF_Q3, -SQRT3_HALF),
        ExactPoint2(HALF_Q3, -SQRT3_HALF),
    )


def _outer_braid_bias(index: int) -> Qsqrt3:
    return Qsqrt3(sqrt3=(Fraction(-1, 5), Fraction(-1, 10), Fraction(1, 10), Fraction(1, 5), Fraction(1, 10), Fraction(-1, 10))[index % 6])


def _event(relation_id: str, node_id: str, left_turn: Fraction, right_turn: Fraction) -> PairProjectionEvent:
    return PairProjectionEvent(f"{relation_id}:{node_id}", node_id, _mod_one(left_turn), _mod_one(right_turn))


def _build_bands() -> tuple[MobiusBandSpec, ...]:
    bands = [MobiusBandSpec(BandSlot.CENTER, ORIGIN_2, TwistChirality.POSITIVE, Fraction(0), ZERO_Q3)]
    for index, center in enumerate(_ring_centers()):
        bands.append(MobiusBandSpec(_ring_slot(index), center, TwistChirality.NEGATIVE, _mod_one(Fraction(1, 2) + Fraction(index, 12)), _outer_braid_bias(index)))
    return tuple(bands)


def _build_nodes() -> tuple[ProjectionNode, ...]:
    centers = _ring_centers()
    nodes: list[ProjectionNode] = [ProjectionNode("NULL", ORIGIN_2, RING_SLOTS, NodeStanding.NULL_PROJECTION)]
    for index, point in enumerate(centers):
        nodes.append(ProjectionNode(f"RING_{index}", point, (BandSlot.CENTER, _ring_slot(index - 1), _ring_slot(index + 1)), NodeStanding.RING_COINCIDENCE))
    for index in range(6):
        nodes.append(ProjectionNode(f"PETAL_{index}", centers[index] + centers[(index + 1) % 6], (_ring_slot(index), _ring_slot(index + 1)), NodeStanding.PETAL_INTERSECTION))
    return tuple(nodes)


def _build_relations() -> tuple[PairRelation, ...]:
    relations: list[PairRelation] = []
    structural_standing = "source-declared relation count; smooth boundary contact not verified"
    for index in range(6):
        relation_id = f"STRUCTURAL:CENTER-RING_{index}"
        relations.append(PairRelation(
            relation_id, BandSlot.CENTER, _ring_slot(index), PairStanding.STRUCTURAL_VESICA, 1,
            (
                _event(relation_id, f"RING_{(index + 1) % 6}", Fraction(index + 1, 6), Fraction(index, 6) + Fraction(1, 3)),
                _event(relation_id, f"RING_{(index - 1) % 6}", Fraction(index - 1, 6), Fraction(index, 6) - Fraction(1, 3)),
            ),
            4, structural_standing,
        ))
    for index in range(6):
        relation_id = f"STRUCTURAL:RING_{index}-RING_{(index + 1) % 6}"
        relations.append(PairRelation(
            relation_id, _ring_slot(index), _ring_slot(index + 1), PairStanding.STRUCTURAL_VESICA, 1,
            (
                _event(relation_id, "NULL", Fraction(index, 6) + Fraction(1, 2), Fraction(index + 1, 6) + Fraction(1, 2)),
                _event(relation_id, f"PETAL_{index}", Fraction(index + 1, 6), Fraction(index, 6)),
            ),
            4, structural_standing,
        ))
    for index in range(6):
        relation_id = f"INCIDENTAL:RING_{index}-RING_{(index + 2) % 6}"
        relations.append(PairRelation(
            relation_id, _ring_slot(index), _ring_slot(index + 2), PairStanding.INCIDENTAL_SECANT, 3,
            (
                _event(relation_id, "NULL", Fraction(index, 6) + Fraction(1, 2), Fraction(index + 2, 6) + Fraction(1, 2)),
                _event(relation_id, f"RING_{(index + 1) % 6}", Fraction(index, 6) + Fraction(1, 3), Fraction(index, 6)),
            ),
            None, "retained projection overlap; no structural promotion",
        ))
    for index in range(3):
        relation_id = f"INCIDENTAL:RING_{index}-RING_{index + 3}"
        relations.append(PairRelation(
            relation_id, _ring_slot(index), _ring_slot(index + 3), PairStanding.INCIDENTAL_TANGENCY, 4,
            (_event(relation_id, "NULL", Fraction(index, 6) + Fraction(1, 2), Fraction(index + 3, 6) + Fraction(1, 2)),),
            None, "retained projection tangency; no structural promotion",
        ))
    return tuple(relations)


def build_mobius_seed_of_life() -> MobiusSeedOfLife:
    """Construct the exact v0.1 seven-band UCNS candidate."""

    return MobiusSeedOfLife(_build_bands(), _build_nodes(), _build_relations())


__all__ = [
    "MOBIUS_SEED_SCHEMA_ID", "MOBIUS_SEED_SCHEMA_VERSION", "MOBIUS_SEED_SELECTION_EFFECT",
    "MOBIUS_SEED_PROJECTION_ID", "MOBIUS_SEED_LIFT_ID", "MOBIUS_SEED_LIFT_VERSION",
    "SOURCE_DOCUMENT_NAME", "SOURCE_DOCUMENT_SHA256", "TARGET_UCNS_BASE_COMMIT",
    "MobiusSeedError", "Qsqrt3", "ExactPoint2", "Point3", "BandSlot", "RING_SLOTS",
    "TwistChirality", "PairStanding", "NodeStanding", "ProjectionNode",
    "PairProjectionEvent", "PairRelation", "MobiusBandSpec", "MobiusSeedOfLife",
    "build_mobius_seed_of_life",
]
