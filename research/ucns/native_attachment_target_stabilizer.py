"""Exact stabilizer audit for candidate native Möbius attachment targets.

The previous origin-attachment audit proves that the visible rational carrier
``Q/Z`` has no equivariant point selector.  This experiment continues from
that result instead of treating its STOP label as terminal.  It lifts the
visible carrier to the exact complete-state torsor ``Q/2Z`` and compares four
explicit target types:

* a visible phase basepoint;
* its unordered two-lift fiber;
* one complete framed lift; and
* one complete lift with a directed local germ.

The ordered parameter is geometric turn displacement.  It is not time.  The
module contains no observed gonol cardinalities and emits no successor.
"""

# === MODULE_BUILD ===
# id: ucns_native_attachment_target_stabilizer
#   module_name: native_attachment_target_stabilizer
#   module_kind: experiment
#   summary: compares exact signed-turn-isometry stabilizers of visible, two-lift, framed, and directed-germ origin-attachment targets on the native Mobius complete-state carrier
#   owner: The Interdependency
#   public_surface: AttachmentTargetError, CompleteCarrierState, AffineCarrierSymmetry, DirectedGerm, AttachmentTarget, candidate_targets, target_stabilizer, audit_payload, receipt_bytes, receipt_digest, formatted_receipt_bytes, render_markdown, markdown_receipt_bytes, write_receipts
#   internal_surface: exact Q/2Z normalization, visible projection, target action, collision and dependency audits
#   auth_boundary: none
#   storage_boundary: read-only except caller-requested deterministic receipts
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_native_attachment_target_stabilizer.py
#   rollout: stack-local pre-ratification geometry experiment only; no UCNS canon, PCEA runtime, successor, or cryptographic promotion
#   rollback: remove this module, its tests, report, and receipts
#   requires: ucns_origin_attachment_basepoint_symmetry, ucns_rooted_rotation_closure_constructor, current UCNS native Mobius and gonal-boundary candidate identities
#   since: 2026-09-19
#   unresolved: geometry-owned Public-Gonol-to-native-carrier incidence; selected directed germ; selected rotation system; global torsion presentation; prime successor selector
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: attachment_target_uses_exact_complete_state_carrier
#   given: a complete native state and exact turn displacement
#   then: state is represented in Q/2Z, visible projection is in Q/Z, one turn exchanges lifts, and two turns restore the complete state
#   class: correctness
#
# id: attachment_target_compares_full_unoriented_stabilizer
#   given: a candidate target is audited
#   then: stabilizers include every translation and exact reflection preserving turn displacement up to one global sign rather than presupposing a selected direction
#   class: correctness
#
# id: attachment_target_exposes_visible_fiber_collision
#   given: one visible phase target and its C2-invariant two-lift fiber
#   then: they have the same complete-state subset and stabilizer, so the fiber spelling adds no observable
#   class: falsification
#
# id: attachment_target_minimal_refinements_are_exact
#   given: the target is refined from visible phase to one lift to one directed germ
#   then: a lift choice removes deck swap while a directed germ is the smallest tested observable that also removes reflection
#   class: evidence
#
# id: attachment_target_does_not_confuse_construction_with_selection
#   given: every candidate can be explicitly constructed
#   then: homogeneous target orbits remain unselected and no candidate is promoted as intrinsic UCNS geometry
#   class: safety
#
# id: attachment_target_preserves_downstream_stop
#   given: no geometry-owned directed-germ incidence is selected
#   then: rotation, marked-dart, closure-selection, torsion, and successor claims remain unresolved or blocked and observed successor values are absent
#   class: safety
#
# id: attachment_target_receipt_replays
#   given: identical source identities and candidate assumptions
#   then: canonical JSON and Markdown replay byte-identically
#   class: correctness
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import argparse
import json
from pathlib import Path
from typing import Any

import rooted_rotation_closure_constructor as ribbon


SCHEMA_ID = "the-interdependency.stack-research.ucns.native-attachment-target-stabilizer"
SCHEMA_VERSION = "0.1.0"
STANDING = "stack-local-explicit-assumption-stabilizer-audit"

VISIBLE_PHASE = "visible-phase-basepoint"
TWO_LIFT_FIBER = "c2-invariant-two-lift-fiber"
SINGLE_LIFT = "single-complete-framed-lift"
DIRECTED_GERM = "single-lift-with-directed-local-germ"

UCNS_CURRENT_COMMIT = "d8f0c505e6f5132e9711de0e7c24e4718e77e51a"
PCEA_CURRENT_COMMIT = "1595842abd1a5b443c6a601a2afe935b60c4adf7"
STACK_PR42_HEAD = "57e3f047c092a6df5435ed4f502347664513a0ff"
STACK_PREDECESSOR = "7419712f5bfa0813b9d2e8f28743aa44dad6f30c"
STACK_ROOTED_CONSTRUCTOR_COMMIT = "ef9dfee02f67231e08d49cc44159bfee501aef28"
STACK_CURRENT_MAIN = "bcaba85900716e5209150a504660fa2ca5158299"
METAPAT_AUTHORITY_COMMIT = "e4165b0cac9eca41daef9c2f941881028ca55d48"
METAPAT_VM_WORKING_HEAD = "e3111d9bf34eae17255af96d2e4f6c072ef16dc4"
SKILL_LIB_AUTHORITY_COMMIT = "dd5027d99516831c0dcb83a176a67140d3819b66"
SKILL_LIB_VM_WORKING_HEAD = "22c2c5702d14fb4b0faeb717777ecab2665770a1"
CRYPTO_AUDIT_COMMIT = "0b49672862a30cec0a0ee24e39a34241c9626f27"
TRAPDOOR_AUDIT_BASE = "82dc5e39f1e0c3f162138c2e7b642814df14dd98"
BASEPOINT_FROZEN_RECEIPT_SHA256 = "5b38d70047ec62ba4c269b13f0f41f3e0c5f661d9f9b317bf8cf8c2b61cda197"

CURRENT_UCNS_SOURCE_SHA256 = {
    "CANON.md": "24977f0dfa7af56d59705cb131c6506c2b551832358bee57b592266be7599f33",
    "src/ucns/carrier.py": "7983f49df68271b2b6b758ba74ea19a3bec332279ef667616456c5ea6b1acf7f",
    "src/ucns/direct_mobius.py": "d8d1360c753dac7431071e007c5105a21b5396dd9e2f7e5ba4089d99e056a5bf",
    "src/ucns/gonal_boundary_trace.py": "332358a21d5d9edac5b0b61806d4785f0c3caecf6704abb842e173c2939c35d0",
    "src/ucns/modular_orbit.py": "7bfab10697b93ff87ea53f49f540896840f8c3fc789a2ef7f901c2cf5836f282",
}

TRAPDOOR_UNPUBLISHED_SHA256 = {
    "research/ucns/trapdoor_lift_falsification.py": "9039d55c3d6230327338fd6c1d004a351ed5f9084f22ac546d675151ecfd8903",
    "research/ucns/tests/test_trapdoor_lift_falsification.py": "d129cc090b06893f412bc05e31320838578a4b9d9f22d073a027b64d054f12f8",
    "research/ucns/receipts/trapdoor-lift-falsification-v0.json": "991a48b0df0bd6ded5d8cae9c6d507eb7b0642b3a58ae302b3beee389411690c",
    "research/ucns/receipts/trapdoor-lift-falsification-v0.md": "8412bdd507b4efe35a06df5a1c178ec3f3f6167e17897eb25603ecf34d76fc8d",
}

NONCLAIMS = (
    "not UCNS canon or a selected Public-Gonol-to-native-carrier incidence",
    "not a claim that local turn displacement is physical or METAPAT time",
    "not a selected rotation system, marked dart, attaching word, torsion presentation, or successor",
    "not PCEA runtime or cryptographic security evidence",
    "not permission to use coordinate zero, positive frame, source order, or observed cardinalities as intrinsic geometry",
)


class AttachmentTargetError(ValueError):
    """Raised when an exact carrier state, symmetry, or target is malformed."""


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def _coerce_fraction(value: Fraction | int, field: str) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (Fraction, int)):
        raise AttachmentTargetError(f"{field} must be an exact int or Fraction")
    return Fraction(value)


def _mod(value: Fraction | int, period: int) -> Fraction:
    return _coerce_fraction(value, "coordinate") % period


def _fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True, slots=True, order=True)
class CompleteCarrierState:
    """One canonical complete native state, represented as Q/2Z."""

    coordinate: Fraction

    def __post_init__(self) -> None:
        if not isinstance(self.coordinate, Fraction) or not Fraction(0) <= self.coordinate < 2:
            raise AttachmentTargetError("complete-state coordinate must be a Fraction in [0,2)")

    @classmethod
    def from_coordinate(cls, coordinate: Fraction | int) -> "CompleteCarrierState":
        return cls(_mod(coordinate, 2))

    @property
    def visible_phase(self) -> Fraction:
        return self.coordinate % 1

    @property
    def frame(self) -> str:
        return "positive-local-frame" if self.coordinate < 1 else "reversed-local-frame"

    def advance(self, displacement: Fraction | int) -> "CompleteCarrierState":
        return CompleteCarrierState.from_coordinate(self.coordinate + _coerce_fraction(displacement, "displacement"))

    def to_payload(self) -> dict[str, str]:
        return {
            "complete_coordinate_mod_two": _fraction_text(self.coordinate),
            "visible_phase_mod_one": _fraction_text(self.visible_phase),
            "frame": self.frame,
        }


@dataclass(frozen=True, slots=True)
class AffineCarrierSymmetry:
    """An exact signed-turn isometry x -> sign*x + offset."""

    sign: int
    offset: Fraction

    def __post_init__(self) -> None:
        if self.sign not in (-1, 1):
            raise AttachmentTargetError("symmetry sign must be plus or minus one")
        if not isinstance(self.offset, Fraction) or not Fraction(0) <= self.offset < 2:
            raise AttachmentTargetError("symmetry offset must be a Fraction in [0,2)")

    @classmethod
    def create(cls, sign: int, offset: Fraction | int) -> "AffineCarrierSymmetry":
        return cls(sign, _mod(offset, 2))

    @property
    def symmetry_id(self) -> str:
        prefix = "tau" if self.sign == 1 else "rho"
        return f"{prefix}_{_fraction_text(self.offset)}"

    @property
    def orientation_preserving(self) -> bool:
        return self.sign == 1

    def apply_state(self, state: CompleteCarrierState) -> CompleteCarrierState:
        return CompleteCarrierState.from_coordinate(self.sign * state.coordinate + self.offset)

    def apply_direction(self, direction: int) -> int:
        if direction not in (-1, 1):
            raise AttachmentTargetError("germ direction must be plus or minus one")
        return self.sign * direction

    def to_payload(self) -> dict[str, Any]:
        return {
            "id": self.symmetry_id,
            "law": f"x -> {self.sign}*x + {_fraction_text(self.offset)} (mod 2)",
            "signed_displacement_action": f"d -> {self.sign}*d",
            "orientation_preserving": self.orientation_preserving,
        }


@dataclass(frozen=True, slots=True)
class DirectedGerm:
    state: CompleteCarrierState
    direction: int

    def __post_init__(self) -> None:
        if not isinstance(self.state, CompleteCarrierState):
            raise AttachmentTargetError("directed germ requires one complete carrier state")
        if self.direction not in (-1, 1):
            raise AttachmentTargetError("directed germ direction must be plus or minus one")

    def to_payload(self) -> dict[str, Any]:
        return {"state": self.state.to_payload(), "direction": self.direction}


@dataclass(frozen=True, slots=True)
class AttachmentTarget:
    assumption_id: str
    kind: str
    visible_phase: Fraction | None = None
    state: CompleteCarrierState | None = None
    direction: int | None = None

    def __post_init__(self) -> None:
        if not self.assumption_id:
            raise AttachmentTargetError("assumption_id is required")
        if self.kind in (VISIBLE_PHASE, TWO_LIFT_FIBER):
            if not isinstance(self.visible_phase, Fraction) or not Fraction(0) <= self.visible_phase < 1:
                raise AttachmentTargetError("visible/fiber target requires a phase in [0,1)")
            if self.state is not None or self.direction is not None:
                raise AttachmentTargetError("visible/fiber target cannot contain a selected lift or direction")
        elif self.kind == SINGLE_LIFT:
            if not isinstance(self.state, CompleteCarrierState) or self.visible_phase is not None or self.direction is not None:
                raise AttachmentTargetError("single-lift target requires exactly one complete state")
        elif self.kind == DIRECTED_GERM:
            DirectedGerm(self.state, self.direction)  # type: ignore[arg-type]
            if self.visible_phase is not None:
                raise AttachmentTargetError("directed-germ target derives its visible phase from its state")
        else:
            raise AttachmentTargetError("unknown attachment target kind")

    @property
    def complete_state_subset(self) -> tuple[CompleteCarrierState, ...]:
        if self.kind in (VISIBLE_PHASE, TWO_LIFT_FIBER):
            assert self.visible_phase is not None
            first = CompleteCarrierState.from_coordinate(self.visible_phase)
            return (first, first.advance(1))
        assert self.state is not None
        return (self.state,)

    def to_payload(self) -> dict[str, Any]:
        return {
            "assumption_id": self.assumption_id,
            "kind": self.kind,
            "selection_basis": "explicit coordinate-zero control; not intrinsic UCNS geometry",
            "visible_phase": None if self.visible_phase is None else _fraction_text(self.visible_phase),
            "complete_state_subset": [state.to_payload() for state in self.complete_state_subset],
            "directed_germ": None if self.kind != DIRECTED_GERM else DirectedGerm(self.state, self.direction).to_payload(),  # type: ignore[arg-type]
        }


@lru_cache(maxsize=1)
def candidate_targets() -> tuple[AttachmentTarget, ...]:
    zero = CompleteCarrierState.from_coordinate(0)
    return (
        AttachmentTarget("attachment.visible-zero-control.v0", VISIBLE_PHASE, visible_phase=Fraction(0)),
        AttachmentTarget("attachment.two-lift-zero-fiber-control.v0", TWO_LIFT_FIBER, visible_phase=Fraction(0)),
        AttachmentTarget("attachment.positive-zero-lift-control.v0", SINGLE_LIFT, state=zero),
        AttachmentTarget("attachment.positive-zero-directed-germ-control.v0", DIRECTED_GERM, state=zero, direction=1),
    )


def _target_fixed(target: AttachmentTarget, symmetry: AffineCarrierSymmetry) -> bool:
    transformed = tuple(sorted(symmetry.apply_state(state) for state in target.complete_state_subset))
    if transformed != tuple(sorted(target.complete_state_subset)):
        return False
    if target.kind == DIRECTED_GERM:
        assert target.direction is not None
        return symmetry.apply_direction(target.direction) == target.direction
    return True


def target_stabilizer(target: AttachmentTarget) -> tuple[AffineCarrierSymmetry, ...]:
    """Return the exact stabilizer inside the declared signed-turn isometry group."""

    if target.kind in (VISIBLE_PHASE, TWO_LIFT_FIBER):
        assert target.visible_phase is not None
        phase = target.visible_phase
        candidates = (
            AffineCarrierSymmetry.create(1, 0),
            AffineCarrierSymmetry.create(1, 1),
            AffineCarrierSymmetry.create(-1, 2 * phase),
            AffineCarrierSymmetry.create(-1, 2 * phase + 1),
        )
    else:
        assert target.state is not None
        candidates = (
            AffineCarrierSymmetry.create(1, 0),
            AffineCarrierSymmetry.create(-1, 2 * target.state.coordinate),
        )
    result = tuple(item for item in candidates if _target_fixed(target, item))
    return tuple(sorted(set(result), key=lambda item: item.symmetry_id))


def _candidate_evaluation(target: AttachmentTarget) -> dict[str, Any]:
    stabilizer = target_stabilizer(target)
    has_deck_swap = any(item.sign == 1 and item.offset == 1 for item in stabilizer)
    has_reflection = any(item.sign == -1 for item in stabilizer)
    if target.kind == DIRECTED_GERM:
        verdict = "SURVIVED_LOCALLY"
        sufficiency = "explicit assumption constructs a locally rigid carrier target in Isom_turn(X)"
    else:
        verdict = "FALSIFIED"
        sufficiency = "insufficient to select direction/chirality"
    return {
        "target": target.to_payload(),
        "stabilizer": [item.to_payload() for item in stabilizer],
        "stabilizer_order": len(stabilizer),
        "retains_deck_swap": has_deck_swap,
        "retains_direction_reversal": has_reflection,
        "local_rooting_sufficiency": sufficiency,
        "verdict": verdict,
        "intrinsic_selection": "UNRESOLVED",
        "target_orbit": "one transitive homogeneous orbit of targets of this kind",
    }


def _stack_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _file_digest(relative_path: str) -> str:
    return sha256((_stack_root() / relative_path).read_bytes()).hexdigest()


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def audit_payload() -> dict[str, Any]:
    targets = candidate_targets()
    evaluations = tuple(_candidate_evaluation(target) for target in targets)
    visible, fiber, single, germ = targets
    visible_stabilizer = target_stabilizer(visible)
    fiber_stabilizer = target_stabilizer(fiber)
    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "standing": STANDING,
        "producer_code_reference": _producer_code_reference(),
        "source_identities": {
            "stack_pr42_head": STACK_PR42_HEAD,
            "stack_predecessor_commit": STACK_PREDECESSOR,
            "stack_rooted_constructor_commit": STACK_ROOTED_CONSTRUCTOR_COMMIT,
            "current_stack_main": STACK_CURRENT_MAIN,
            "metapat_authority_commit": METAPAT_AUTHORITY_COMMIT,
            "metapat_vm_working_head": METAPAT_VM_WORKING_HEAD,
            "skill_lib_authority_commit": SKILL_LIB_AUTHORITY_COMMIT,
            "skill_lib_vm_working_head": SKILL_LIB_VM_WORKING_HEAD,
            "current_ucns_authority_commit": UCNS_CURRENT_COMMIT,
            "current_ucns_source_sha256": CURRENT_UCNS_SOURCE_SHA256,
            "current_pcea_authority_commit": PCEA_CURRENT_COMMIT,
            "crypto_audit_commit": CRYPTO_AUDIT_COMMIT,
            "trapdoor_unpublished_base_commit": TRAPDOOR_AUDIT_BASE,
            "trapdoor_unpublished_sha256": TRAPDOOR_UNPUBLISHED_SHA256,
            "stack_predecessor_files": {
                "research/ucns/origin_attachment_basepoint_symmetry.py": _file_digest("research/ucns/origin_attachment_basepoint_symmetry.py"),
                "research/ucns/rooted_rotation_closure_constructor.py": _file_digest("research/ucns/rooted_rotation_closure_constructor.py"),
                "research/ucns/rooted_rotation_successor_gate.py": _file_digest("research/ucns/rooted_rotation_successor_gate.py"),
            },
            "basepoint_symmetry_receipt_sha256": BASEPOINT_FROZEN_RECEIPT_SHA256,
            "rooted_rotation_receipt_sha256": ribbon.receipt_digest(),
        },
        "carrier_model": {
            "complete_states": "X = Q/2Z",
            "visible_states": "V = Q/Z",
            "projection": "pi([x]_2) = [x]_1",
            "deck_involution": "delta([x]_2) = [x+1]_2",
            "tested_unoriented_isometry_group": "Isom_turn(X) = (Q/2Z) semidirect C2; x -> s*x+c, preserving d up to one global sign",
            "path_parameter": "exact geometric turn displacement d in Q",
            "time_interpretation": None,
            "native_transition_law": ribbon.NATIVE_TRANSITION_LAW,
        },
        "candidate_evaluations": list(evaluations),
        "exact_collision": {
            "left": visible.assumption_id,
            "right": fiber.assumption_id,
            "same_complete_state_subset": visible.complete_state_subset == fiber.complete_state_subset,
            "same_stabilizer": visible_stabilizer == fiber_stabilizer,
            "smallest_counterexample": {
                "visible_phase": "0",
                "two_lifts": ["0", "1"],
                "shared_stabilizer": [item.symmetry_id for item in visible_stabilizer],
            },
            "verdict": "FALSIFIED",
            "deprecated_representation": "treating a visible basepoint and its full inverse-image fiber as distinct primitive information",
            "deprecated_status": "DEPRECATED",
        },
        "minimal_refinements": [
            {
                "from": visible.kind,
                "to": single.kind,
                "additional_observable": "one complete-state lift (frame choice)",
                "stabilizer_order_before": len(visible_stabilizer),
                "stabilizer_order_after": len(target_stabilizer(single)),
                "removes": "deck swap",
                "does_not_remove": "reflection fixing the chosen complete state",
                "verdict": "SURVIVED",
            },
            {
                "from": single.kind,
                "to": germ.kind,
                "additional_observable": "one directed local germ at the chosen complete state",
                "stabilizer_order_before": len(target_stabilizer(single)),
                "stabilizer_order_after": len(target_stabilizer(germ)),
                "removes": "the final sign-reversing reflection",
                "verdict": "SURVIVED_LOCALLY",
            },
        ],
        "dependency_audit": [
            {
                "field": "origin_attachment",
                "why_necessary": "a singular source must be incident to one traversable carrier target before local data can be transported",
                "implementation": "IMPLEMENTED_FOR_EXPLICIT_TARGET_ASSUMPTIONS",
                "selection": "MISSING_GEOMETRY_OWNED_INCIDENCE",
                "obstruction": "no equivariant target selector exists on any homogeneous candidate orbit without additional incidence",
                "classification": "UNRESOLVED",
            },
            {
                "field": "directed_tangent_or_chirality",
                "why_necessary": "reflection fixes a chosen complete lift while reversing every signed displacement germ",
                "implementation": "IMPLEMENTED_BY_DIRECTED_GERM_CONTROL",
                "selection": "MISSING",
                "obstruction": "visible, fiber, and single-lift targets have a nontrivial reversing stabilizer",
                "classification": "UNRESOLVED",
            },
            {
                "field": "rotation_system",
                "why_necessary": "face permutation requires a cyclic successor sigma on all incident darts",
                "implementation": "TWO_COHERENT_STACK_CANDIDATES_EXIST",
                "selection": "MISSING",
                "obstruction": "paired-germs and sign-blocks preserve earlier fields but yield different faces and genus",
                "classification": "FALSIFIED",
            },
            {
                "field": "marked_outgoing_dart",
                "why_necessary": "a cyclic rotation determines a boundary word only up to cyclic conjugacy and component choice",
                "implementation": "EXPLICIT_FIRST_ROLE_CONTROL_EXISTS",
                "selection": "MISSING",
                "obstruction": "relation/source order is provenance rather than geometry",
                "classification": "UNRESOLVED",
            },
            {
                "field": "closure_rule",
                "why_necessary": "alpha and sigma do not authorize a filled face, relator, torsion, or arithmetic readout until a closure operation is declared",
                "implementation": "RIBBON_FACE_ORBITS_IMPLEMENTED_AS_PHI_EQUALS_SIGMA_AFTER_ALPHA",
                "selection": "GLOBAL_ATTACHING_OR_TORSION_LAW_MISSING",
                "obstruction": "ordinary face closure gives only trivial or non-finite cellular order in the frozen candidates",
                "classification": "UNRESOLVED",
            },
        ],
        "result_classifications": {
            "visible_phase_suffices_for_direction": "FALSIFIED",
            "two_lift_fiber_adds_information_over_visible_phase": "FALSIFIED",
            "single_framed_lift_suffices_for_direction": "FALSIFIED",
            "directed_germ_explicit_constructor": "SURVIVED_LOCALLY",
            "intrinsic_directed_germ_selection": "UNRESOLVED",
            "rotation_selected_by_earlier_fields": "FALSIFIED",
            "canonical_successor_evaluation": "BLOCKED",
            "visible_and_full_fiber_as_distinct_primitives": "DEPRECATED",
            "pcea_cryptographic_security": "FALSIFIED",
            "minimal_fourth_power_trapdoor": "FALSIFIED",
            "general_ucns_trapdoor_lift": "UNRESOLVED",
        },
        "observed_successor_gate": {
            "constructor_frozen": True,
            "observed_values_present_in_constructor": False,
            "successor_selector_derived": False,
            "observed_successor_values_evaluated": False,
            "reason": "target selection and rotation remain unresolved; an attachment stabilizer is not a successor law",
        },
        "first_remaining_irreducible_assumption": {
            "name": "geometry-owned oriented incidence",
            "statement": "one intrinsic UCNS relation must attach Structural Null or Public Gonol origin to a complete native Mobius state and distinguish one local displacement germ",
            "why_irreducible": "a visible point and its two-lift fiber collide; a chosen lift still has an exact reversing stabilizer; provenance and coordinate defaults cannot remove it",
        },
        "next_experiment": {
            "name": "public-origin to native-germ incidence sieve",
            "freeze_inputs": [
                "current 157-position Public Gonol arrangement",
                "current exact gonal boundary samples r/157",
                "native Q/2Z complete-state projection",
                "all candidate lift and local-germ choices before comparator access",
            ],
            "competing_candidates": [
                "Public Gonol index r maps only to visible boundary phase r/157",
                "the inverse-image two-lift fiber is retained as an unordered target",
                "one complete lift plus directed germ is supplied only as the stronger control",
            ],
            "falsifier": "every candidate either lacks an authority-declared Public-Gonol bridge or retains a nontrivial target stabilizer",
            "survival_gate": "an exact carrier-owned incidence must select one directed germ with trivial signed-turn-isometry stabilizer and replay independently of source order, frame defaults, covering-degree choice, hashes, or PCEA expectations",
        },
        "security_separation": {
            "geometric_result": "local target refinement SURVIVED_LOCALLY under explicit assumptions; intrinsic selection UNRESOLVED",
            "pcea_security": "FALSIFIED at crypto-audit commit 0b49672",
            "trapdoor_lift": "general claim UNRESOLVED; smallest fourth-power candidate FALSIFIED",
            "security_promotion": None,
        },
        "nonclaims": list(NONCLAIMS),
    }


def receipt_bytes(payload: dict[str, Any] | None = None) -> bytes:
    return _canonical_bytes(payload if payload is not None else audit_payload()) + b"\n"


def receipt_digest(payload: dict[str, Any] | None = None) -> str:
    return sha256(receipt_bytes(payload)).hexdigest()


def formatted_receipt_bytes(payload: dict[str, Any] | None = None) -> bytes:
    value = payload if payload is not None else audit_payload()
    return json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True).encode("ascii") + b"\n"


def render_markdown(payload: dict[str, Any] | None = None) -> str:
    value = payload if payload is not None else audit_payload()
    lines = [
        "# Native attachment target stabilizer v0",
        "",
        "Standing: **Stack-local explicit-assumption geometry experiment**.",
        "",
        f"Receipt SHA-256: `{receipt_digest(value)}`.",
        "",
        "## Exact result",
        "",
        "| Target | Stabilizer order | Deck swap | Reflection | Verdict |",
        "|---|---:|---|---|---|",
    ]
    for item in value["candidate_evaluations"]:
        lines.append(
            f"| `{item['target']['kind']}` | {item['stabilizer_order']} | "
            f"{item['retains_deck_swap']} | {item['retains_direction_reversal']} | `{item['verdict']}` |"
        )
    first = value["first_remaining_irreducible_assumption"]
    experiment = value["next_experiment"]
    lines.extend(
        (
            "",
            "The visible phase target and its full two-lift fiber are the same complete-state subset with the same stabilizer. A single lift removes the deck swap but retains reflection. Adding one directed local germ makes the target rigid within the declared signed-turn isometry group.",
            "",
            "## First remaining irreducible assumption",
            "",
            f"**{first['name']}**: {first['statement']}",
            "",
            "## Next experiment",
            "",
            f"**{experiment['name']}**. {experiment['survival_gate']}",
            "",
            "## Security boundary",
            "",
            "PCEA cryptographic security remains `FALSIFIED`. The general UCNS trapdoor lift remains `UNRESOLVED`; its smallest fourth-power candidate remains `FALSIFIED`.",
            "",
            "hmmm: the directed germ is the smallest locally sufficient refinement tested here, but current geometry still does not select one.",
            "",
        )
    )
    return "\n".join(lines)


def markdown_receipt_bytes(payload: dict[str, Any] | None = None) -> bytes:
    return render_markdown(payload).encode("utf-8")


def write_receipts(directory: Path) -> tuple[Path, Path]:
    directory.mkdir(parents=True, exist_ok=True)
    payload = audit_payload()
    json_path = directory / "native-attachment-target-stabilizer-v0.json"
    md_path = directory / "native-attachment-target-stabilizer-v0.md"
    json_path.write_bytes(formatted_receipt_bytes(payload))
    md_path.write_bytes(markdown_receipt_bytes(payload))
    return json_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--write-receipts", type=Path)
    args = parser.parse_args()
    if args.write_receipts is not None:
        for path in write_receipts(args.write_receipts):
            print(path)
        return
    payload = audit_payload()
    if args.format == "markdown":
        print(render_markdown(payload), end="")
    else:
        print(json.dumps({"receipt_sha256": receipt_digest(payload), "receipt": payload}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
