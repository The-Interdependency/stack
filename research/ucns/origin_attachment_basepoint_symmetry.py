"""Test whether current UCNS root-loop geometry selects an unframed basepoint.

The smallest canon-defined traversable candidate is the exact visible-state
action groupoid of the native Mobius root loop.  Its objects are rational phase
classes Q/Z and its paths retain exact rational displacement.  This module
computes the label-preserving automorphism group, its object orbits, and the
fixed-point obstruction before any origin attachment is constructed.
"""

# === MODULE_BUILD ===
# id: ucns_origin_attachment_basepoint_symmetry
#   module_name: origin_attachment_basepoint_symmetry
#   module_kind: experiment
#   summary: defines the minimal canon-backed unframed root-loop groupoid and proves that its exact translation automorphisms act simply transitively on all admissible base objects
#   owner: The Interdependency
#   public_surface: BasepointSymmetryError, UnframedBaseObject, UnframedPath, TranslationAutomorphism, CandidateTraversableStructure, AutomorphismGroupWitness, OrbitPartition, FiniteReplayWitness, CandidateBoundary, AdditionalStructureRequirement, BasepointSymmetryResult, enumerate_unframed_base_objects, transporter, candidate_traversable_structure, automorphism_group_witness, orbit_partition, finite_replay_witness, candidate_boundaries, additional_structure_requirement, audit, receipt_payload, receipt_bytes, receipt_digest, formatted_receipt_bytes, write_frozen_receipt
#   internal_surface: _stack_root, _canonical_bytes, _file_digest, _source_file_digests, _load_module, _direct_mobius, _load_and_verify_receipt, _coerce_fraction, _mod_one, _fraction_text, _producer_code_reference, main
#   auth_boundary: none; reads only stack-pinned UCNS geometry and frozen stack-local UCNS obstruction receipts
#   storage_boundary: read-only except explicit generation of the fixed stack-local receipt path
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_origin_attachment_basepoint_symmetry.py
#   rollout: stack-local pre-ratification symmetry result only; no UCNS canon, origin attachment, or downstream constructor promotion
#   rollback: remove this module, its test, report, and receipt
#   requires: ucns_native_mobius_geometry, directed_carrier_floor, ucns_origin_attachment_canon_gap, gonol-build construction discipline
#   since: 2026-09-03
#   unresolved: canon-defined recursive traversable structure and a geometry-derived mark that breaks root-loop translation symmetry
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: basepoint_symmetry_binds_exact_authority
#   given: the basepoint symmetry audit runs
#   then: the pinned UCNS commit, tree, native geometry, prior canon gap, and excluded bouquet candidate are bound to exact identities
#   class: evidence
#   since: 2026-09-03
#
# id: basepoint_symmetry_defines_exact_candidate
#   given: the smallest canon-defined traversable structure is selected for analysis
#   then: T is the exact rational-displacement action groupoid on unframed visible phase classes Q/Z, with Structural Null outside its object set
#   class: doctrine
#   since: 2026-09-03
#
# id: basepoint_symmetry_enumerates_unframed_objects
#   given: admissible unframed base objects are requested
#   then: V(T) is exactly Q/Z with unique reduced representatives and no canonically excluded or marked phase
#   class: correctness
#   since: 2026-09-03
#
# id: basepoint_symmetry_derives_exact_automorphism_group
#   given: automorphisms preserve every signed rational displacement label
#   then: every automorphism is exactly one phase translation and Aut(T) is isomorphic to Q/Z
#   class: correctness
#   since: 2026-09-03
#
# id: basepoint_symmetry_partitions_one_transitive_orbit
#   given: Aut(T) acts on V(T)
#   then: V(T) has one simply transitive orbit, no globally fixed object, and no canonical object-valued section of the orbit quotient
#   class: correctness
#   since: 2026-09-03
#
# id: basepoint_symmetry_rejects_phase_zero_default
#   given: phase zero is proposed as v0
#   then: exact half-turn translation preserves T and moves phase zero, so a coordinate or API default is not an intrinsic base object
#   class: safety
#   since: 2026-09-03
#
# id: basepoint_symmetry_rejects_circular_bouquet_base
#   given: the stack-local subdivided bouquet has a unique high-valence vertex at rank at least two
#   then: that vertex is not imported because the candidate creates it with the unresolved shared-basepoint attachment being tested
#   class: safety
#   since: 2026-09-03
#
# id: basepoint_symmetry_identifies_minimum_new_structure
#   given: the translation action is simply transitive
#   then: selecting v0 requires at least one geometry-derived distinguished unframed zero-cell or an equivalent unique singular incidence
#   class: doctrine
#   since: 2026-09-03
#
# id: basepoint_symmetry_stops_without_iota
#   given: no current geometric mark breaks translation symmetry
#   then: status is TRANSITIVE_SYMMETRY, iota remains null, tangent and chirality are not evaluated, and no downstream constructor output is emitted
#   class: safety
#   since: 2026-09-03
#
# id: basepoint_symmetry_receipt_replays
#   given: pinned canon and predecessor receipts are unchanged
#   then: canonical payload bytes, payload digest, and formatted receipt replay byte-identically
#   class: evidence
#   since: 2026-09-03
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from math import gcd
from pathlib import Path
import sys
from types import ModuleType
from typing import Any

import origin_attachment_canon_gap as canon_gap


SCHEMA_ID = "the-interdependency.stack-research.ucns.origin-attachment-basepoint-symmetry"
SCHEMA_VERSION = "0.1.0"
STANDING = "stack-local-pre-ratification-exact-symmetry-obstruction"
SELECTION_EFFECT = "none"

PINNED_UCNS_COMMIT = canon_gap.PINNED_UCNS_COMMIT
PINNED_UCNS_TREE = canon_gap.PINNED_UCNS_TREE
ORIGIN_GAP_RECEIPT_SHA256 = "f0f2a4a127e7a83c26291b94f58543b6881f7e1eda52940c7df3c14b121ad0f4"
ORDERED_GROUPOID_RECEIPT_SHA256 = "cf61151f9e9ce1479b6d7eb95ff51bb2a683045de292243e1f14a9b3dd050f69"

STATUS = "TRANSITIVE_SYMMETRY"
SECONDARY_CLASSIFICATION = "UNIQUE_ORBIT_NOT_OBJECT"
STRUCTURE_ID = "ucns.native-mobius-visible-rational-displacement-groupoid"
AUTOMORPHISM_GROUP_ID = "Aut_Q(T)"

FORBIDDEN_SELECTORS = (
    "glyph or relation label",
    "source order",
    "storage order",
    "numeric order",
    "local frame",
    "chirality",
    "API default",
    "implementation convenience",
    "external expectation",
)

NONCLAIMS = (
    "not UCNS canon or canon ratification",
    "not a definition of the absent full recursive traversable structure",
    "not an origin attachment or choice of base object",
    "not a tangent, chirality, rotation-system, outgoing-dart, or closure result",
    "not a traversal, monodromy, arithmetic readout, or successor operation",
    "not proof that every future enriched UCNS geometry must remain homogeneous",
)

HMMM = (
    "the exact canon-backed root loop is homogeneous: its unframed rational visible objects form one simply transitive translation orbit",
    "the one orbit is canonical as an equivalence class, but it has no canonical object-valued section",
    "Structural Null is uniquely distinguished outside T, yet current canon supplies no incidence transporting that distinction into V(T)",
    "the stack-local return bouquet has a degree-distinguished center only because its unresolved shared-basepoint attachment has already been assumed",
    "a future recursive T may break symmetry, but that requires new canon-defined incidence, singularity, boundary, or marked zero-cell structure",
)


class BasepointSymmetryError(ValueError):
    """Raised when the declared exact symmetry model fails closed."""


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


def _file_digest(root: Path, relative_path: str) -> tuple[str, str]:
    return relative_path, sha256((root / relative_path).read_bytes()).hexdigest()


def _source_file_digests() -> tuple[tuple[str, str], ...]:
    root = _stack_root()
    return tuple(
        _file_digest(root, path)
        for path in (
            "research/ucns/BASE.json",
            "stack-manifest.json",
            "libs/ucns/AGENTS.md",
            "libs/ucns/CANON.md",
            "libs/ucns/docs/GEOMETRY.md",
            "libs/ucns/src/ucns/public_gonol.py",
            "libs/ucns/src/ucns/carrier.py",
            "libs/ucns/src/ucns/direct_mobius.py",
            "libs/ucns/tests/test_carrier.py",
            "libs/ucns/tests/test_direct_mobius.py",
            "research/ucns/origin_attachment_canon_gap.py",
            "research/ucns/receipts/origin-attachment-canon-gap-v0.json",
            "research/ucns/ordered_complete_return_groupoid.py",
            "research/ucns/receipts/ordered-complete-return-groupoid-v0.json",
        )
    )


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise BasepointSymmetryError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def _direct_mobius() -> ModuleType:
    return _load_module(
        "stack_pinned_ucns_direct_mobius_for_basepoint_symmetry",
        _stack_root() / "libs/ucns/src/ucns/direct_mobius.py",
    )


def _load_and_verify_receipt(relative_path: str, expected_digest: str) -> dict[str, Any]:
    payload = json.loads((_stack_root() / relative_path).read_bytes())
    recorded = payload.pop("receipt_sha256")
    replayed = sha256(_canonical_bytes(payload)).hexdigest()
    if recorded != expected_digest or replayed != expected_digest:
        raise BasepointSymmetryError(f"receipt identity changed: {relative_path}")
    return payload


def _coerce_fraction(value: Fraction | int, field: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (Fraction, int)):
        raise BasepointSymmetryError(f"{field} must be an int or exact Fraction")
    return Fraction(value)


def _mod_one(value: Fraction | int) -> Fraction:
    return _coerce_fraction(value, "phase") % 1


def _fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True, slots=True, order=True)
class UnframedBaseObject:
    """One exact visible phase class in Q/Z."""

    phase: Fraction

    def __post_init__(self) -> None:
        if not isinstance(self.phase, Fraction) or not Fraction(0) <= self.phase < Fraction(1):
            raise BasepointSymmetryError("phase must be the reduced representative in [0,1)")

    @classmethod
    def from_phase(cls, phase: Fraction | int) -> "UnframedBaseObject":
        return cls(_mod_one(phase))

    def advance(self, displacement: Fraction | int) -> "UnframedBaseObject":
        return UnframedBaseObject.from_phase(self.phase + _coerce_fraction(displacement, "displacement"))

    def to_payload(self) -> dict[str, str]:
        return {"phase_class_mod_one": _fraction_text(self.phase)}


@dataclass(frozen=True, slots=True)
class UnframedPath:
    """A path retaining exact rational displacement on the visible quotient."""

    source: UnframedBaseObject
    displacement: Fraction

    def __post_init__(self) -> None:
        if not isinstance(self.source, UnframedBaseObject):
            raise BasepointSymmetryError("path source must be an unframed base object")
        if not isinstance(self.displacement, Fraction):
            raise BasepointSymmetryError("path displacement must be an exact Fraction")

    @classmethod
    def from_displacement(
        cls,
        source: UnframedBaseObject,
        displacement: Fraction | int,
    ) -> "UnframedPath":
        return cls(source, _coerce_fraction(displacement, "displacement"))

    @property
    def target(self) -> UnframedBaseObject:
        return self.source.advance(self.displacement)

    def then(self, following: "UnframedPath") -> "UnframedPath":
        if self.target != following.source:
            raise BasepointSymmetryError("path composition endpoint mismatch")
        return UnframedPath(self.source, self.displacement + following.displacement)

    def to_payload(self) -> dict[str, Any]:
        return {
            "source": self.source.to_payload(),
            "displacement": _fraction_text(self.displacement),
            "target": self.target.to_payload(),
        }


@dataclass(frozen=True, slots=True)
class TranslationAutomorphism:
    """One displacement-label-preserving translation of T."""

    offset: Fraction

    def __post_init__(self) -> None:
        if not isinstance(self.offset, Fraction) or not Fraction(0) <= self.offset < Fraction(1):
            raise BasepointSymmetryError("translation offset must be reduced modulo one")

    @classmethod
    def from_offset(cls, offset: Fraction | int) -> "TranslationAutomorphism":
        return cls(_mod_one(offset))

    def apply_object(self, value: UnframedBaseObject) -> UnframedBaseObject:
        return value.advance(self.offset)

    def apply_path(self, path: UnframedPath) -> UnframedPath:
        return UnframedPath(self.apply_object(path.source), path.displacement)

    def then(self, following: "TranslationAutomorphism") -> "TranslationAutomorphism":
        return TranslationAutomorphism.from_offset(self.offset + following.offset)

    def inverse(self) -> "TranslationAutomorphism":
        return TranslationAutomorphism.from_offset(-self.offset)

    def to_payload(self) -> dict[str, str]:
        return {"offset_class_mod_one": _fraction_text(self.offset)}


def enumerate_unframed_base_objects(max_denominator: int) -> tuple[UnframedBaseObject, ...]:
    """Return a finite exact replay prefix of the symbolic Q/Z enumeration."""

    if isinstance(max_denominator, bool) or not isinstance(max_denominator, int):
        raise BasepointSymmetryError("max_denominator must be an integer")
    if max_denominator < 1:
        raise BasepointSymmetryError("max_denominator must be positive")
    phases = {
        Fraction(numerator, denominator)
        for denominator in range(1, max_denominator + 1)
        for numerator in range(denominator)
        if gcd(numerator, denominator) == 1
    }
    return tuple(UnframedBaseObject(phase) for phase in sorted(phases))


def transporter(source: UnframedBaseObject, target: UnframedBaseObject) -> TranslationAutomorphism:
    """Return the unique translation carrying source to target."""

    if not isinstance(source, UnframedBaseObject) or not isinstance(target, UnframedBaseObject):
        raise BasepointSymmetryError("transporter endpoints must be unframed base objects")
    return TranslationAutomorphism.from_offset(target.phase - source.phase)


@dataclass(frozen=True, slots=True)
class CandidateTraversableStructure:
    """Exact signature of the smallest canon-backed traversable candidate."""

    structure_id: str
    authority_operation: str
    law_id: str
    law_version: str
    object_set: str
    object_enumeration: str
    morphism_set: str
    source_map: str
    target_map: str
    composition: str
    unframed: bool
    structural_null_is_object: bool
    phase_zero_intrinsically_marked: bool

    def to_payload(self) -> dict[str, Any]:
        return {
            "structure_id": self.structure_id,
            "authority_operation": self.authority_operation,
            "law_id": self.law_id,
            "law_version": self.law_version,
            "objects": {
                "set": self.object_set,
                "enumeration": self.object_enumeration,
                "cardinality": "countably infinite",
                "all_objects_admissible": True,
                "excluded_or_marked_phase": None,
            },
            "morphisms": {
                "set": self.morphism_set,
                "source": self.source_map,
                "target": self.target_map,
                "composition": self.composition,
            },
            "unframed": self.unframed,
            "structural_null_is_object": self.structural_null_is_object,
            "phase_zero_intrinsically_marked": self.phase_zero_intrinsically_marked,
        }


@lru_cache(maxsize=1)
def candidate_traversable_structure() -> CandidateTraversableStructure:
    """Define T from the pinned exact visible phase and motion law."""

    direct = _direct_mobius()
    result = CandidateTraversableStructure(
        structure_id=STRUCTURE_ID,
        authority_operation="NativeMobiusState.advance with frame forgotten only after visible projection",
        law_id=direct.NATIVE_MOBIUS_LAW_ID,
        law_version=direct.NATIVE_MOBIUS_LAW_VERSION,
        object_set="V(T) = Q/Z",
        object_enumeration=(
            "{a/b : b > 0, 0 <= a < b, gcd(a,b) = 1}; "
            "a = 0 occurs only as 0/1"
        ),
        morphism_set="Mor(T) = {([q], d) : [q] in Q/Z, d in Q}",
        source_map="s([q], d) = [q]",
        target_map="t([q], d) = [q + d]",
        composition="([q], d) then ([q+d], e) = ([q], d+e)",
        unframed=True,
        structural_null_is_object=False,
        phase_zero_intrinsically_marked=False,
    )
    if direct.STRUCTURAL_NULL_ORIGIN.carrier_position != 0:
        raise BasepointSymmetryError("pinned Structural Null origin changed")
    return result


@dataclass(frozen=True, slots=True)
class AutomorphismGroupWitness:
    """Classification of displacement-label-preserving automorphisms."""

    group_id: str
    exact_group: str
    element_form: str
    action: str
    composition: str
    inverse: str
    preserved_data: tuple[str, ...]
    completeness_proof: tuple[str, ...]
    action_free: bool
    action_transitive: bool
    larger_unlabelled_group_needed: bool

    def to_payload(self) -> dict[str, Any]:
        return {
            "group_id": self.group_id,
            "exact_group": self.exact_group,
            "element_form": self.element_form,
            "action": self.action,
            "composition": self.composition,
            "inverse": self.inverse,
            "preserved_data": list(self.preserved_data),
            "completeness_proof": list(self.completeness_proof),
            "action_free": self.action_free,
            "action_transitive": self.action_transitive,
            "larger_unlabelled_group_needed": self.larger_unlabelled_group_needed,
            "scope_note": (
                "translations already prove transitivity; allowing sign reversal would enlarge "
                "symmetry without creating a fixed object"
            ),
        }


@lru_cache(maxsize=1)
def automorphism_group_witness() -> AutomorphismGroupWitness:
    """Derive Aut_Q(T) rather than infer it from finite probes."""

    return AutomorphismGroupWitness(
        group_id=AUTOMORPHISM_GROUP_ID,
        exact_group="Q/Z under addition",
        element_form="tau_c for one unique c in Q/Z",
        action="tau_c([q]) = [q+c]; tau_c([q],d) = ([q+c],d)",
        composition="tau_c then tau_e = tau_[c+e]",
        inverse="tau_c^-1 = tau_[-c]",
        preserved_data=(
            "visible phase equivalence modulo one",
            "every signed rational displacement label d",
            "path source, target, identity, inverse, and composition",
            "one-turn visible return and two-turn complete-return locations",
        ),
        completeness_proof=(
            "for any label-preserving automorphism F, set c = F([0])",
            "equivariance gives F([q]) = F([0]+q) = F([0])+q = [c+q]",
            "therefore F = tau_c, and c is unique",
            "conversely every tau_c preserves every declared object and path operation",
        ),
        action_free=True,
        action_transitive=True,
        larger_unlabelled_group_needed=False,
    )


@dataclass(frozen=True, slots=True)
class OrbitPartition:
    """Exact orbit and fixed-point result for V(T)."""

    object_set: str
    orbit_count: int
    orbits: tuple[str, ...]
    unique_orbit: bool
    unique_object_within_orbit: bool
    globally_fixed_objects: tuple[UnframedBaseObject, ...]
    canonical_orbit_section: None
    transporter_formula: str
    fixed_point_obstruction: str
    phase_zero_half_turn_image: UnframedBaseObject
    outcome: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "object_set": self.object_set,
            "orbit_count": self.orbit_count,
            "orbits": list(self.orbits),
            "unique_orbit": self.unique_orbit,
            "unique_object_within_orbit": self.unique_object_within_orbit,
            "globally_fixed_objects": [item.to_payload() for item in self.globally_fixed_objects],
            "canonical_orbit_section": self.canonical_orbit_section,
            "transporter_formula": self.transporter_formula,
            "fixed_point_obstruction": self.fixed_point_obstruction,
            "phase_zero_half_turn_image": self.phase_zero_half_turn_image.to_payload(),
            "outcome": self.outcome,
        }


@lru_cache(maxsize=1)
def orbit_partition() -> OrbitPartition:
    """Partition Q/Z and exhibit a fixed-point-free canonical automorphism."""

    phase_zero = UnframedBaseObject.from_phase(0)
    half_turn = TranslationAutomorphism.from_offset(Fraction(1, 2))
    image = half_turn.apply_object(phase_zero)
    if image == phase_zero:
        raise BasepointSymmetryError("half-turn translation unexpectedly fixes phase zero")
    return OrbitPartition(
        object_set="Q/Z",
        orbit_count=1,
        orbits=("Q/Z",),
        unique_orbit=True,
        unique_object_within_orbit=False,
        globally_fixed_objects=(),
        canonical_orbit_section=None,
        transporter_formula="c = [y-x] uniquely sends [x] to [y]",
        fixed_point_obstruction=(
            "tau_[1/2]([q]) = [q+1/2] differs from [q] for every [q], "
            "because 1/2 is not zero in Q/Z"
        ),
        phase_zero_half_turn_image=image,
        outcome=STATUS,
    )


@dataclass(frozen=True, slots=True)
class FiniteReplayWitness:
    """Bounded exhaustive replay supporting the symbolic proof."""

    maximum_denominator: int
    object_count: int
    object_pair_count: int
    transporter_checks: int
    automorphism_path_checks: int
    canonical_visible_state_checks: int
    half_turn_fixed_object_count: int
    all_checks_passed: bool
    witness_sha256: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "maximum_denominator": self.maximum_denominator,
            "object_count": self.object_count,
            "object_pair_count": self.object_pair_count,
            "transporter_checks": self.transporter_checks,
            "automorphism_path_checks": self.automorphism_path_checks,
            "canonical_visible_state_checks": self.canonical_visible_state_checks,
            "half_turn_fixed_object_count": self.half_turn_fixed_object_count,
            "all_checks_passed": self.all_checks_passed,
            "witness_sha256": self.witness_sha256,
            "standing": "finite exact replay witness; the full transitivity result is algebraic",
        }


@lru_cache(maxsize=1)
def finite_replay_witness(maximum_denominator: int = 8) -> FiniteReplayWitness:
    """Replay translations and canonical visible states over a finite exact prefix."""

    objects = enumerate_unframed_base_objects(maximum_denominator)
    direct = _direct_mobius()
    transporter_checks = 0
    path_checks = 0
    canonical_checks = 0
    for source in objects:
        for target in objects:
            move = transporter(source, target)
            if move.apply_object(source) != target:
                raise BasepointSymmetryError("transporter failed")
            transporter_checks += 1
            path = UnframedPath.from_displacement(source, target.phase)
            moved_path = move.apply_path(path)
            if moved_path.target != move.apply_object(path.target):
                raise BasepointSymmetryError("translation failed to preserve path target")
            if moved_path.displacement != path.displacement:
                raise BasepointSymmetryError("translation changed displacement label")
            path_checks += 1
        for frame in direct.NativeMobiusFrame:
            state = direct.native_mobius_state(source.phase, frame)
            if state.visible_key[1] != source.phase:
                raise BasepointSymmetryError("candidate object disagrees with canonical visible state")
            for displacement_object in objects:
                displacement = displacement_object.phase
                if state.advance(displacement).visible_key[1] != source.advance(displacement).phase:
                    raise BasepointSymmetryError("candidate path disagrees with canonical advance")
                canonical_checks += 1

    half_turn = TranslationAutomorphism.from_offset(Fraction(1, 2))
    fixed_count = sum(half_turn.apply_object(item) == item for item in objects)
    witness_payload = {
        "maximum_denominator": maximum_denominator,
        "objects": [item.to_payload() for item in objects],
        "transporter_checks": transporter_checks,
        "automorphism_path_checks": path_checks,
        "canonical_visible_state_checks": canonical_checks,
        "half_turn_fixed_object_count": fixed_count,
    }
    return FiniteReplayWitness(
        maximum_denominator=maximum_denominator,
        object_count=len(objects),
        object_pair_count=len(objects) ** 2,
        transporter_checks=transporter_checks,
        automorphism_path_checks=path_checks,
        canonical_visible_state_checks=canonical_checks,
        half_turn_fixed_object_count=fixed_count,
        all_checks_passed=True,
        witness_sha256=sha256(_canonical_bytes(witness_payload)).hexdigest(),
    )


@dataclass(frozen=True, slots=True)
class CandidateBoundary:
    """Disposition of another apparent target structure."""

    candidate_id: str
    standing: str
    orbit_information: str
    qualifies_as_t: bool
    reason: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "standing": self.standing,
            "orbit_information": self.orbit_information,
            "qualifies_as_t": self.qualifies_as_t,
            "reason": self.reason,
        }


@lru_cache(maxsize=1)
def candidate_boundaries() -> tuple[CandidateBoundary, ...]:
    """Prevent absent or already-based structures from deciding the result."""

    return (
        CandidateBoundary(
            candidate_id="public-gonol-157-position-carrier",
            standing="pinned canon",
            orbit_information="not defined; positions have no canonical traversal or incidence operation",
            qualifies_as_t=False,
            reason="an ordered carrier identity alone is not a traversable structure",
        ),
        CandidateBoundary(
            candidate_id="non-null-directed-carrier",
            standing="pinned geometric candidate/projection",
            orbit_information=(
                "each fixed positive-breadth angular shell is translation-transitive; "
                "different breadths remain separate and no breadth is selected from Structural Null"
            ),
            qualifies_as_t=False,
            reason="canon supplies neither a selected non-null breadth nor an origin incidence",
        ),
        CandidateBoundary(
            candidate_id="stack-local-subdivided-return-bouquet",
            standing="stack-local candidate, not canon",
            orbit_information=(
                "for rank at least two the shared vertex is uniquely distinguished by degree 2r "
                "from degree-two midpoint vertices"
            ),
            qualifies_as_t=False,
            reason=(
                "the unique vertex is created by the declared shared positive-basepoint, "
                "basepoint-preserving attachment whose geometric authorization remains unresolved"
            ),
        ),
    )


@dataclass(frozen=True, slots=True)
class AdditionalStructureRequirement:
    """Smallest structural kind that can break the exact translation action."""

    required_kind: str
    exact_effect: str
    equivalent_geometric_forms: tuple[str, ...]
    current_canon_supplies: bool
    selected_object: None

    def to_payload(self) -> dict[str, Any]:
        return {
            "required_kind": self.required_kind,
            "exact_effect": self.exact_effect,
            "equivalent_geometric_forms": list(self.equivalent_geometric_forms),
            "current_canon_supplies": self.current_canon_supplies,
            "selected_object": self.selected_object,
        }


@lru_cache(maxsize=1)
def additional_structure_requirement() -> AdditionalStructureRequirement:
    """Name the missing symmetry breaker without choosing one."""

    return AdditionalStructureRequirement(
        required_kind="one geometry-derived distinguished unframed zero-cell in T",
        exact_effect=(
            "marking b restricts the translation group to {tau_c : tau_c(b)=b}; "
            "because the action is free, only tau_0 remains"
        ),
        equivalent_geometric_forms=(
            "a unique branch or singular point lying in the traversable structure",
            "a unique boundary incidence or attachment germ with its direction forgotten",
            "an intrinsic scalar or incidence invariant with exactly one object-level extremum",
        ),
        current_canon_supplies=False,
        selected_object=None,
    )


@dataclass(frozen=True, slots=True)
class BasepointSymmetryResult:
    """Final pre-ratification result with no selected representative."""

    status: str
    secondary_classification: str
    structure: CandidateTraversableStructure
    automorphisms: AutomorphismGroupWitness
    partition: OrbitPartition
    replay: FiniteReplayWitness
    alternatives: tuple[CandidateBoundary, ...]
    additional_structure: AdditionalStructureRequirement
    existing_canon_distinguishes_exactly_one_orbit: bool
    existing_canon_distinguishes_exactly_one_object: bool
    iota: None
    tangent_or_chirality_evaluated: bool
    downstream_constructor_fields_evaluated: bool

    def to_payload(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "secondary_classification": self.secondary_classification,
            "candidate_traversable_structure": self.structure.to_payload(),
            "automorphism_group": self.automorphisms.to_payload(),
            "orbit_partition": self.partition.to_payload(),
            "finite_replay_witness": self.replay.to_payload(),
            "candidate_boundaries": [item.to_payload() for item in self.alternatives],
            "existing_canon_test": {
                "distinguishes_exactly_one_orbit": (
                    self.existing_canon_distinguishes_exactly_one_orbit
                ),
                "distinguishes_exactly_one_object_within_orbit": (
                    self.existing_canon_distinguishes_exactly_one_object
                ),
                "invariant_witness": (
                    "tau_[1/2] preserves every declared unframed displacement relation "
                    "and has no fixed object"
                ),
            },
            "required_additional_structure": self.additional_structure.to_payload(),
            "outputs": {
                "iota": self.iota,
                "tangent_or_chirality_evaluated": self.tangent_or_chirality_evaluated,
                "downstream_constructor_fields_evaluated": (
                    self.downstream_constructor_fields_evaluated
                ),
            },
            "stop_reason": (
                "V(T) is one transitive automorphism orbit with no invariant object; "
                "a canonical v0 requires new geometry that marks or singularizes one object"
            ),
        }


@lru_cache(maxsize=1)
def audit() -> BasepointSymmetryResult:
    """Run the exact orbit test and stop before constructing iota."""

    prior = canon_gap.audit()
    if prior.status != canon_gap.STATUS or prior.origin_attachment is not None:
        raise BasepointSymmetryError("origin-attachment gap predecessor changed")
    partition = orbit_partition()
    group = automorphism_group_witness()
    if not (group.action_free and group.action_transitive):
        raise BasepointSymmetryError("declared automorphism action is not simply transitive")
    if partition.orbit_count != 1 or partition.globally_fixed_objects:
        raise BasepointSymmetryError("orbit obstruction changed")
    return BasepointSymmetryResult(
        status=STATUS,
        secondary_classification=SECONDARY_CLASSIFICATION,
        structure=candidate_traversable_structure(),
        automorphisms=group,
        partition=partition,
        replay=finite_replay_witness(),
        alternatives=candidate_boundaries(),
        additional_structure=additional_structure_requirement(),
        existing_canon_distinguishes_exactly_one_orbit=True,
        existing_canon_distinguishes_exactly_one_object=False,
        iota=None,
        tangent_or_chirality_evaluated=False,
        downstream_constructor_fields_evaluated=False,
    )


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def receipt_payload() -> dict[str, Any]:
    origin_gap_receipt = _load_and_verify_receipt(
        "research/ucns/receipts/origin-attachment-canon-gap-v0.json",
        ORIGIN_GAP_RECEIPT_SHA256,
    )
    groupoid_receipt = _load_and_verify_receipt(
        "research/ucns/receipts/ordered-complete-return-groupoid-v0.json",
        ORDERED_GROUPOID_RECEIPT_SHA256,
    )
    if origin_gap_receipt["canon_gap"]["origin_attachment"] is not None:
        raise BasepointSymmetryError("origin gap receipt unexpectedly contains an attachment")
    if groupoid_receipt["standing"] == "UCNS canon":
        raise BasepointSymmetryError("ordered groupoid standing unexpectedly changed")
    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "producer_code_reference": _producer_code_reference(),
        "source": {
            "authority": "The-Interdependency/ucns",
            "ucns_commit": PINNED_UCNS_COMMIT,
            "ucns_tree": PINNED_UCNS_TREE,
            "source_file_digests": [
                {"path": path, "sha256": digest}
                for path, digest in _source_file_digests()
            ],
            "origin_attachment_canon_gap_receipt_sha256": ORIGIN_GAP_RECEIPT_SHA256,
            "ordered_groupoid_candidate_receipt_sha256": ORDERED_GROUPOID_RECEIPT_SHA256,
            "network_used": False,
        },
        "experiment_boundary": {
            "question": "does current canon intrinsically select one unframed v0 in the smallest traversable T?",
            "automorphism_signature": (
                "bijections of Q/Z preserving every signed rational displacement label and path operation"
            ),
            "forbidden_selectors": list(FORBIDDEN_SELECTORS),
            "observed_cardinality_input": None,
            "framing_or_chirality_input": None,
        },
        "audit": audit().to_payload(),
        "nonclaims": list(NONCLAIMS),
        "hmmm": list(HMMM),
    }


def receipt_bytes() -> bytes:
    return _canonical_bytes(receipt_payload())


def receipt_digest() -> str:
    return sha256(receipt_bytes()).hexdigest()


def formatted_receipt_bytes() -> bytes:
    payload = dict(receipt_payload())
    payload["receipt_sha256"] = receipt_digest()
    return (json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n").encode("ascii")


def write_frozen_receipt() -> Path:
    path = _stack_root() / "research/ucns/receipts/origin-attachment-basepoint-symmetry-v0.json"
    path.write_bytes(formatted_receipt_bytes())
    return path


def main() -> None:
    if len(sys.argv) == 2 and sys.argv[1] == "--write-receipt":
        print(write_frozen_receipt())
        return
    if len(sys.argv) != 1:
        raise SystemExit("usage: origin_attachment_basepoint_symmetry.py [--write-receipt]")
    sys.stdout.buffer.write(formatted_receipt_bytes())


if __name__ == "__main__":
    main()
