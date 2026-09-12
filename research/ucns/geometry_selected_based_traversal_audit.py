"""Audit whether current UCNS geometry selects one based return traversal.

The ordered return groupoid can represent noncommutative words, but capacity is
not selection.  This module asks whether the pinned Public Gonol and recursive
UCNS geometry provide all three marks needed for a canonical based traversal:
a geometric basepoint attachment, an orientation at that attachment, and a
geometry-derived successor/closure rule on oriented return germs.

Carrier order, API defaults, caller tuple order, construction provenance,
seed-event order without a recursive attachment, hashes, and arithmetic
observations are not admitted selectors.
"""

# === MODULE_BUILD ===
# id: ucns_geometry_selected_based_traversal_audit
#   module_name: geometry_selected_based_traversal_audit
#   module_kind: experiment
#   summary: tests whether pinned Public Gonol and recursive UCNS geometry canonically mark a basepoint, orientation, and complete-return attaching word, and records the exact symmetry stop when they do not
#   owner: The Interdependency
#   public_surface: BasedTraversalAuditError, OriginAttachmentAudit, NativeDirectionSymmetry, PermutationSelectionOrbit, SelectorEvaluation, BasedTraversalRequirements, BasedTraversalAudit, origin_attachment_audit, native_direction_symmetry, permutation_selection_orbit, selector_evaluations, audit, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _stack_root, _canonical_bytes, _load_module, _public_gonol, _carrier, _direct_mobius, _file_digest, _source_file_digests, _fraction_text, _state_payload, _lift_coordinate, _state_from_lift, _reflect_state, _rename_word, _producer_code_reference, main
#   auth_boundary: none; reads only stack-pinned UCNS canon and frozen stack-local ordered-return research
#   storage_boundary: read-only at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_geometry_selected_based_traversal_audit.py
#   rollout: stack-local traversal-selection obstruction research only; no UCNS canon, stack libs, PCEA, attaching-word, arithmetic-factor, or successor promotion
#   rollback: remove this module, its tests, report, and receipt
#   requires: ucns_public_gonol_geometry, directed_carrier_floor, ucns_native_mobius_geometry, ucns_ordered_complete_return_groupoid, ucns_ordered_return_invariant_audit, gonol-build construction discipline
#   since: 2026-09-02
#   unresolved: geometric map from Structural Null/Public Gonol origin to the recursive return base object; directed attachment or chirality at that basepoint; rotation system and marked outgoing germ; geometry-derived closure/attaching word; monodromy; arithmetic readout
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: based_traversal_audit_binds_exact_geometry
#   given: the traversal-selection audit runs
#   then: Public Gonol origin, coordinate-free Structural Null, native Mobius law, ordered return groupoid, and prior noncommutative audit are bound to exact source and receipt identities
#   class: evidence
#   since: 2026-09-02
#
# id: based_traversal_audit_separates_origin_from_attachment
#   given: Public Gonol position zero and Structural Null are inspected
#   then: their exact distinguished identities are retained without inventing a map to the non-null promoted groupoid base object
#   class: doctrine
#   since: 2026-09-02
#
# id: based_traversal_audit_exhibits_direction_symmetry
#   given: positive and negative native Mobius complete returns begin at the same framed state
#   then: exact lifted-coordinate reflection fixes the base state, conjugates every tested displacement to its negative, and makes the integer-turn return-state traces identical
#   class: correctness
#   since: 2026-09-02
#
# id: based_traversal_audit_exhibits_permutation_obstruction
#   given: the rank-three return bouquet has identical local traces, no geometric loop marks, no relators, and no monodromy
#   then: its S3 loop-renaming symmetry moves one once-each based word through all six permutations and fixes no such word
#   class: correctness
#   since: 2026-09-02
#
# id: based_traversal_audit_rejects_nongeometric_selectors
#   given: carrier order, API defaults, caller slots, construction ordinals, seed order without attachment, ids, hashes, or observations are proposed as traversal selectors
#   then: none is promoted as a geometry-selected basepoint, orientation, or attaching word
#   class: safety
#   since: 2026-09-02
#
# id: based_traversal_audit_defines_exact_missing_marks
#   given: a future geometry-selected traversal is evaluated
#   then: it must supply a Public-Gonol-to-groupoid basepoint attachment, directed tangent or chirality, rotation/successor system, marked outgoing germ, and closure rule with geometric provenance
#   class: doctrine
#   since: 2026-09-02
#
# id: based_traversal_audit_stops_without_word
#   given: one or more required geometric marks are absent
#   then: canonical basepoint, orientation, traversal word, attaching word, monodromy, arithmetic comparison, and numerical successor remain null
#   class: safety
#   since: 2026-09-02
#
# id: based_traversal_audit_receipt_replays
#   given: pinned canon and frozen predecessor receipts are unchanged
#   then: canonical receipt bytes and digest replay byte-identically
#   class: evidence
#   since: 2026-09-02
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
from itertools import permutations
import json
from pathlib import Path
import sys
from types import ModuleType
from typing import Any, Mapping

import complete_return_relation_extension as extension
import ordered_complete_return_groupoid as groupoid_module
import ordered_return_invariant_audit as invariant_audit


SCHEMA_ID = "the-interdependency.stack-research.ucns.geometry-selected-based-traversal-audit"
SCHEMA_VERSION = "0.1.0"
STANDING = "stack-local-target-free-geometry-selection-obstruction-audit"
SELECTION_EFFECT = "none"
STATUS = "STOP_NO_GEOMETRY_SELECTED_BASED_TRAVERSAL"

STATUS_UNRESOLVED = "UNRESOLVED_NO_GEOMETRIC_ATTACHMENT_MAP"
STATUS_REJECTED = "REJECTED_SELECTOR_BASIS"
STATUS_UNSELECTED = "UNSELECTED_BY_CURRENT_GEOMETRY"

NONCLAIMS: tuple[str, ...] = (
    "not UCNS canon",
    "not proof that future UCNS geometry cannot select a based traversal",
    "not denial that Public Gonol has an exact distinguished carrier origin",
    "not permission to treat carrier order, API defaults, construction order, ids, or hashes as geometric traversal",
    "not a monodromy, attaching-word, arithmetic-factor, or successor-cardinality operation",
    "not a numerical next-gonol prediction",
    "not PCEA key, entropy, hardness, replay-resistance, recovery, or public-authenticity evidence",
)

HMMM: tuple[str, ...] = (
    "Public Gonol position zero and Structural Null are distinguished, but Structural Null is coordinate-free and no admitted geometry attaches it to the non-null promoted return-groupoid base object",
    "the native Mobius state law admits exact sign-reversing reflection; a directed carrier could break that symmetry only after a Public-Gonol-to-recursive-return attachment is geometrically supplied",
    "the retained loops have identical local trace geometry and no cross-generator incidence, so their unmarked rank-three shape admits every S3 loop permutation",
    "recursive construction ordinals and relation ids distinguish provenance occurrences but are not traversal geometry",
    "a canonical based boundary word requires at least an oriented rotation system and a geometrically marked outgoing dart or equivalent structure",
    "no complete-return attaching word, global monodromy, arithmetic readout, or numerical successor is currently selected",
)

FALSIFICATION_CONDITIONS: tuple[str, ...] = (
    "current canon already defines a geometric map from Public Gonol origin to the promoted return base object and this audit omits it",
    "current canon already derives recursive orientation or chirality at that attachment and this audit omits it",
    "current geometry already supplies a rotation system, marked outgoing germ, or attaching word over retained return loops",
    "the exact native Mobius reflection fails to conjugate signed displacement while fixing the chosen phase-zero positive state",
    "the unmarked identical-loop rank-three shape does not admit all six loop permutations",
    "a carrier tuple, API default, caller order, construction ordinal, seed order without attachment, hash, id, or observation is reported as geometry-selected",
    "a based traversal, monodromy, factorization, or numerical successor is emitted while any required geometric mark is absent",
)

PROMOTION_EVIDENCE: tuple[str, ...] = (
    "construct an exact geometric attachment from the distinguished Public Gonol origin or another intrinsic point to one recursive return-groupoid object",
    "derive an orientation, tangent, chirality, or directed germ at that attachment from UCNS geometry rather than a coordinate convention",
    "derive a rotation/successor system on all incident oriented return germs from geometric incidence",
    "mark the first outgoing germ geometrically so cyclic conjugacy does not erase the based distinction",
    "derive and freeze the complete return closure or attaching word before computing monodromy or any arithmetic invariant",
)


class BasedTraversalAuditError(ValueError):
    """Raised when traversal selection crosses an undeclared boundary."""


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


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise BasedTraversalAuditError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def _public_gonol() -> ModuleType:
    return _load_module(
        "stack_pinned_ucns_public_gonol_for_based_traversal_audit",
        _stack_root() / "libs" / "ucns" / "src" / "ucns" / "public_gonol.py",
    )


@lru_cache(maxsize=1)
def _carrier() -> ModuleType:
    return _load_module(
        "stack_pinned_ucns_carrier_for_based_traversal_audit",
        _stack_root() / "libs" / "ucns" / "src" / "ucns" / "carrier.py",
    )


@lru_cache(maxsize=1)
def _direct_mobius() -> ModuleType:
    return _load_module(
        "stack_pinned_ucns_direct_mobius_for_based_traversal_audit",
        _stack_root() / "libs" / "ucns" / "src" / "ucns" / "direct_mobius.py",
    )


def _file_digest(root: Path, relative_path: str) -> tuple[str, str]:
    return relative_path, sha256((root / relative_path).read_bytes()).hexdigest()


def _source_file_digests(root: Path) -> tuple[tuple[str, str], ...]:
    return tuple(
        _file_digest(root, path)
        for path in (
            "research/ucns/BASE.json",
            "stack-manifest.json",
            "libs/ucns/docs/GEOMETRY.md",
            "libs/ucns/src/ucns/public_gonol.py",
            "libs/ucns/src/ucns/carrier.py",
            "libs/ucns/src/ucns/direct_mobius.py",
            "libs/ucns/src/ucns/mobius_seed.py",
            "research/ucns/public_gonol_functional_operations.py",
            "research/ucns/affinization_coupling_geometry.py",
            "research/ucns/recursive_scale_transition.py",
            "research/ucns/complete_return_relation_extension.py",
            "research/ucns/ordered_complete_return_groupoid.py",
            "research/ucns/receipts/ordered-complete-return-groupoid-v0.json",
            "research/ucns/ordered_return_invariant_audit.py",
            "research/ucns/receipts/ordered-return-invariant-audit-v0.json",
        )
    )


def _fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _state_payload(state: Any) -> dict[str, str]:
    return {
        "phase_turns": _fraction_text(state.phase_turns),
        "frame": state.frame.value,
    }


@dataclass(frozen=True, slots=True)
class OriginAttachmentAudit:
    """Distinguish an exact carrier origin from a recursive path attachment."""

    public_gonol_index: int
    public_gonol_glyph: str
    public_gonol_sha256: str
    direct_structural_null_carrier_position: int
    carrier_structural_null_coordinate_free: bool
    ordered_model_base_object: str
    geometry_selected_origin_to_base_object_map: None
    status: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "public_gonol_origin": {
                "index": self.public_gonol_index,
                "glyph": self.public_gonol_glyph,
                "arrangement_sha256": self.public_gonol_sha256,
            },
            "direct_structural_null_carrier_position": self.direct_structural_null_carrier_position,
            "carrier_structural_null_coordinate_free": self.carrier_structural_null_coordinate_free,
            "ordered_model_base_object": self.ordered_model_base_object,
            "geometry_selected_origin_to_base_object_map": self.geometry_selected_origin_to_base_object_map,
            "status": self.status,
            "conclusion": (
                "an intrinsic carrier origin exists, but current geometry defines no attachment morphism "
                "from coordinate-free Structural Null to the non-null recursive return base object"
            ),
        }


@lru_cache(maxsize=1)
def origin_attachment_audit() -> OriginAttachmentAudit:
    """Retain the exact origin while refusing an undeclared path attachment."""

    public = _public_gonol()
    carrier = _carrier()
    direct = _direct_mobius()
    origin = public.public_gonol_function(0)
    if origin.index != 0 or origin.glyph != public.PUBLIC_GONOL_157[0]:
        raise BasedTraversalAuditError("Public Gonol origin changed")
    if direct.STRUCTURAL_NULL_ORIGIN.carrier_position != 0:
        raise BasedTraversalAuditError("direct Structural Null carrier position changed")
    coordinate_free = not any(
        hasattr(carrier.STRUCTURAL_NULL, field)
        for field in ("angle", "phase", "phase_turns", "frame")
    )
    if not coordinate_free:
        raise BasedTraversalAuditError("carrier Structural Null unexpectedly gained coordinates")
    return OriginAttachmentAudit(
        public_gonol_index=origin.index,
        public_gonol_glyph=origin.glyph,
        public_gonol_sha256=public.PUBLIC_GONOL_SHA256,
        direct_structural_null_carrier_position=direct.STRUCTURAL_NULL_ORIGIN.carrier_position,
        carrier_structural_null_coordinate_free=coordinate_free,
        ordered_model_base_object=groupoid_module.POSITIVE_BASE_OBJECT,
        geometry_selected_origin_to_base_object_map=None,
        status=STATUS_UNRESOLVED,
    )


def _lift_coordinate(direct: ModuleType, state: Any) -> Fraction:
    sheet = Fraction(1) if state.frame is direct.NativeMobiusFrame.REVERSED else Fraction(0)
    return state.phase_turns + sheet


def _state_from_lift(direct: ModuleType, coordinate: Fraction) -> Any:
    reduced = coordinate % 2
    if reduced < 1:
        return direct.NativeMobiusState(reduced, direct.NativeMobiusFrame.POSITIVE)
    return direct.NativeMobiusState(reduced - 1, direct.NativeMobiusFrame.REVERSED)


def _reflect_state(direct: ModuleType, state: Any) -> Any:
    return _state_from_lift(direct, -_lift_coordinate(direct, state))


@dataclass(frozen=True, slots=True)
class NativeDirectionSymmetry:
    """Exact sign-reversing symmetry of the un-attached native state law."""

    positive_turns: tuple[Fraction, ...]
    negative_turns: tuple[Fraction, ...]
    positive_states: tuple[dict[str, str], ...]
    negative_states: tuple[dict[str, str], ...]
    integer_return_traces_equal: bool
    reflection_fixes_base_state: bool
    reflection_conjugacy_checks: int
    reflection_conjugacy_all_exact: bool
    geometry_selected_direction: None

    def to_payload(self) -> dict[str, Any]:
        return {
            "positive_turns": [_fraction_text(value) for value in self.positive_turns],
            "negative_turns": [_fraction_text(value) for value in self.negative_turns],
            "positive_states": list(self.positive_states),
            "negative_states": list(self.negative_states),
            "integer_return_traces_equal": self.integer_return_traces_equal,
            "reflection": {
                "lifted_coordinate_law": "rho(u) = -u mod 2",
                "fixes_base_state": self.reflection_fixes_base_state,
                "conjugacy_law": "rho(state.advance(d)) = rho(state).advance(-d)",
                "exact_check_count": self.reflection_conjugacy_checks,
                "all_exact": self.reflection_conjugacy_all_exact,
            },
            "geometry_selected_direction": self.geometry_selected_direction,
            "conclusion": (
                "the local state law does not select displacement sign; a directed recursive attachment "
                "would have to be supplied independently"
            ),
        }


@lru_cache(maxsize=1)
def native_direction_symmetry() -> NativeDirectionSymmetry:
    """Prove exact reversal symmetry before any directed recursive attachment."""

    direct = _direct_mobius()
    base = direct.native_mobius_state(0, direct.NativeMobiusFrame.POSITIVE)
    positive_turns = (Fraction(0), Fraction(1), Fraction(2))
    negative_turns = (Fraction(0), Fraction(-1), Fraction(-2))
    positive = tuple(base.advance(value) for value in positive_turns)
    negative = tuple(base.advance(value) for value in negative_turns)
    probes = (
        Fraction(0),
        Fraction(1, 4),
        Fraction(1, 2),
        Fraction(3, 4),
        Fraction(1),
        Fraction(5, 4),
        Fraction(-1, 3),
    )
    displacements = (
        Fraction(-2),
        Fraction(-1, 2),
        Fraction(1, 3),
        Fraction(1),
        Fraction(2),
    )
    checks = tuple(
        _reflect_state(direct, base.advance(start).advance(displacement))
        == _reflect_state(direct, base.advance(start)).advance(-displacement)
        for start in probes
        for displacement in displacements
    )
    result = NativeDirectionSymmetry(
        positive_turns=positive_turns,
        negative_turns=negative_turns,
        positive_states=tuple(_state_payload(state) for state in positive),
        negative_states=tuple(_state_payload(state) for state in negative),
        integer_return_traces_equal=positive == negative,
        reflection_fixes_base_state=_reflect_state(direct, base) == base,
        reflection_conjugacy_checks=len(checks),
        reflection_conjugacy_all_exact=all(checks),
        geometry_selected_direction=None,
    )
    if not (
        result.integer_return_traces_equal
        and result.reflection_fixes_base_state
        and result.reflection_conjugacy_all_exact
    ):
        raise BasedTraversalAuditError("native direction-reflection witness failed")
    return result


def _rename_word(
    groupoid: groupoid_module.OrderedReturnGroupoid,
    word: groupoid_module.FreeReturnWord,
    rename: Mapping[str, str],
) -> groupoid_module.FreeReturnWord:
    relation_ids = {item.relation_id for item in groupoid.generators}
    if set(rename) != relation_ids or set(rename.values()) != relation_ids:
        raise BasedTraversalAuditError("loop renaming must be a basis permutation")
    return groupoid.word(
        groupoid_module.WordLetter(rename[letter.relation_id], letter.exponent)
        for letter in word.letters
    )


@dataclass(frozen=True, slots=True)
class PermutationSelectionOrbit:
    """S3 obstruction to selecting a word from an unmarked identical-loop shape."""

    rank: int
    unmarked_shape_sha256: str
    action_count: int
    seed_word: tuple[str, ...]
    orbit_words: tuple[tuple[str, ...], ...]
    orbit_size: int
    fixed_once_each_words: tuple[tuple[str, ...], ...]
    common_abelianization: tuple[int, ...]
    geometry_selected_word: None

    def to_payload(self) -> dict[str, Any]:
        return {
            "rank": self.rank,
            "unmarked_shape_sha256": self.unmarked_shape_sha256,
            "symmetry_group": "S3 loop renaming",
            "action_count": self.action_count,
            "seed_word": list(self.seed_word),
            "orbit_words": [list(word) for word in self.orbit_words],
            "orbit_size": self.orbit_size,
            "fixed_once_each_words": [list(word) for word in self.fixed_once_each_words],
            "common_abelianization": list(self.common_abelianization),
            "geometry_selected_word": self.geometry_selected_word,
            "conclusion": (
                "no once-each based word is invariant under every symmetry of the current unmarked "
                "identical-loop shape"
            ),
        }


@lru_cache(maxsize=1)
def permutation_selection_orbit() -> PermutationSelectionOrbit:
    """Compute the complete S3 orbit and its empty fixed-word set."""

    groupoid = groupoid_module.build_ordered_return_groupoid(3)
    generators = groupoid.generators
    relation_ids = tuple(item.relation_id for item in generators)
    seed = groupoid.word_from_ordinals((1, 2, 3))
    actions = tuple(
        dict(zip(relation_ids, (item.relation_id for item in ordering), strict=True))
        for ordering in permutations(generators)
    )
    orbit = tuple({_rename_word(groupoid, seed, action) for action in actions})
    orbit_words = tuple(sorted(groupoid.word_symbols(word) for word in orbit))
    once_each = tuple(
        groupoid.word(
            groupoid_module.WordLetter(item.relation_id) for item in ordering
        )
        for ordering in permutations(generators)
    )
    fixed = tuple(
        groupoid.word_symbols(word)
        for word in once_each
        if all(_rename_word(groupoid, word, action) == word for action in actions)
    )
    abelianizations = {groupoid.abelianize(word) for word in orbit}
    trace_digests = {item.trace_sha256 for item in generators}
    if len(trace_digests) != 1:
        raise BasedTraversalAuditError("local return traces are no longer identical")
    shape_payload = {
        "kind": "unmarked-subdivided-return-bouquet",
        "rank": groupoid.relation_rank,
        "base_vertex_degree": 2 * groupoid.relation_rank,
        "midpoint_degree_multiset": [2] * groupoid.relation_rank,
        "shared_local_trace_sha256": next(iter(trace_digests)),
        "filling_two_cells": 0,
        "cross_generator_relators": [],
        "global_monodromy": None,
        "geometric_loop_labels": None,
        "rotation_system": None,
        "marked_outgoing_dart": None,
    }
    result = PermutationSelectionOrbit(
        rank=groupoid.relation_rank,
        unmarked_shape_sha256=sha256(_canonical_bytes(shape_payload)).hexdigest(),
        action_count=len(actions),
        seed_word=groupoid.word_symbols(seed),
        orbit_words=orbit_words,
        orbit_size=len(orbit_words),
        fixed_once_each_words=tuple(sorted(fixed)),
        common_abelianization=next(iter(abelianizations)),
        geometry_selected_word=None,
    )
    if result.action_count != 6 or result.orbit_size != 6 or result.fixed_once_each_words:
        raise BasedTraversalAuditError("rank-three permutation obstruction changed")
    if len(abelianizations) != 1:
        raise BasedTraversalAuditError("S3 once-each orbit changed homology control")
    return result


@dataclass(frozen=True, slots=True)
class SelectorEvaluation:
    """One proposed selector basis and its bounded disposition."""

    component: str
    proposed_basis: str
    source: str
    status: str
    reason: str

    def to_payload(self) -> dict[str, str]:
        return {
            "component": self.component,
            "proposed_basis": self.proposed_basis,
            "source": self.source,
            "status": self.status,
            "reason": self.reason,
        }


@lru_cache(maxsize=1)
def selector_evaluations() -> tuple[SelectorEvaluation, ...]:
    """Reject data order and preserve the one plausible but unattached origin."""

    return (
        SelectorEvaluation(
            "basepoint",
            "Public Gonol position zero / Structural Null identity",
            "pinned Public Gonol and carrier geometry",
            STATUS_UNRESOLVED,
            "intrinsically distinguished, but coordinate-free and not attached to the promoted return-groupoid object",
        ),
        SelectorEvaluation(
            "orientation",
            "forward direction of the Public Gonol arrangement tuple",
            "pinned carrier order",
            STATUS_REJECTED,
            "exact carrier order is data geometry but no Public Gonol operation turns tuple direction into recursive path orientation",
        ),
        SelectorEvaluation(
            "basepoint/orientation",
            "phase-zero positive-frame API default",
            "native_mobius_state default arguments",
            STATUS_REJECTED,
            "a local coordinate representative and frame label are not a Public-Gonol-derived recursive attachment",
        ),
        SelectorEvaluation(
            "orientation",
            "positive native turn displacement",
            "native Mobius state law",
            STATUS_UNSELECTED,
            "exact reflection exchanges displacement signs until an admitted directed recursive attachment breaks the symmetry",
        ),
        SelectorEvaluation(
            "traversal",
            "retained relation-basis ordinal order",
            "recursive construction provenance",
            STATUS_REJECTED,
            "generation history addresses loops but supplies no path incidence or successor relation between them",
        ),
        SelectorEvaluation(
            "traversal",
            "affinization participant slot order",
            "stack-local coupling mechanic",
            STATUS_REJECTED,
            "the tuple is explicitly caller supplied and its coordinate/topological embedding remains unresolved",
        ),
        SelectorEvaluation(
            "traversal",
            "Mobius seed event or band order",
            "pinned seed candidate",
            STATUS_REJECTED,
            "exact seed order has no authorized map to Public Gonol recursive return generators",
        ),
        SelectorEvaluation(
            "traversal",
            "one permutation of the unmarked rank-three return loops",
            "ordered return groupoid",
            STATUS_UNSELECTED,
            "S3 preserves every currently admitted unlabeled shape datum and moves the word through all six permutations",
        ),
    )


@dataclass(frozen=True, slots=True)
class BasedTraversalRequirements:
    """The exact missing geometric marks for a future based attaching word."""

    origin_to_groupoid_attachment: None
    directed_tangent_or_chirality: None
    oriented_rotation_or_successor_system: None
    geometrically_marked_outgoing_dart: None
    complete_return_closure_rule: None

    @property
    def ready(self) -> bool:
        return all(value is not None for value in (
            self.origin_to_groupoid_attachment,
            self.directed_tangent_or_chirality,
            self.oriented_rotation_or_successor_system,
            self.geometrically_marked_outgoing_dart,
            self.complete_return_closure_rule,
        ))

    def to_payload(self) -> dict[str, Any]:
        return {
            "origin_to_groupoid_attachment": self.origin_to_groupoid_attachment,
            "directed_tangent_or_chirality": self.directed_tangent_or_chirality,
            "oriented_rotation_or_successor_system": self.oriented_rotation_or_successor_system,
            "geometrically_marked_outgoing_dart": self.geometrically_marked_outgoing_dart,
            "complete_return_closure_rule": self.complete_return_closure_rule,
            "all_required_marks_present": self.ready,
            "required_provenance": "each mark must replay from UCNS geometry before word construction",
        }


@dataclass(frozen=True, slots=True)
class BasedTraversalAudit:
    """Final bounded result of the current geometry-selection test."""

    status: str
    origin: OriginAttachmentAudit
    direction: NativeDirectionSymmetry
    permutation: PermutationSelectionOrbit
    selectors: tuple[SelectorEvaluation, ...]
    requirements: BasedTraversalRequirements
    geometry_selected_basepoint: None
    geometry_selected_orientation: None
    geometry_selected_traversal_word: None
    geometry_selected_attaching_word: None
    current_global_monodromy: None
    current_arithmetic_readout: None
    observation_comparison: None
    numerical_next_gonol: None

    def to_payload(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "origin_attachment_audit": self.origin.to_payload(),
            "native_direction_symmetry": self.direction.to_payload(),
            "rank_three_permutation_obstruction": self.permutation.to_payload(),
            "selector_evaluations": [item.to_payload() for item in self.selectors],
            "required_geometric_marks": self.requirements.to_payload(),
            "result": {
                "geometry_selected_basepoint": self.geometry_selected_basepoint,
                "geometry_selected_orientation": self.geometry_selected_orientation,
                "geometry_selected_traversal_word": self.geometry_selected_traversal_word,
                "geometry_selected_attaching_word": self.geometry_selected_attaching_word,
                "current_global_monodromy": self.current_global_monodromy,
                "current_arithmetic_readout": self.current_arithmetic_readout,
                "observation_comparison": self.observation_comparison,
                "numerical_next_gonol": self.numerical_next_gonol,
            },
            "stop_reason": (
                "current Public Gonol and recursive UCNS geometry do not provide the attachment, "
                "orientation, rotation/marked-germ, and closure data needed to select one based word"
            ),
        }


@lru_cache(maxsize=1)
def audit() -> BasedTraversalAudit:
    """Run the target-free selection test and stop before inventing a word."""

    predecessor = invariant_audit.audit()
    if predecessor.status != invariant_audit.STATUS:
        raise BasedTraversalAuditError("ordered invariant predecessor status changed")
    if predecessor.current_relators or predecessor.current_global_monodromy is not None:
        raise BasedTraversalAuditError("predecessor unexpectedly gained traversal geometry")
    requirements = BasedTraversalRequirements(None, None, None, None, None)
    if requirements.ready:
        raise BasedTraversalAuditError("empty traversal requirements cannot be ready")
    return BasedTraversalAudit(
        status=STATUS,
        origin=origin_attachment_audit(),
        direction=native_direction_symmetry(),
        permutation=permutation_selection_orbit(),
        selectors=selector_evaluations(),
        requirements=requirements,
        geometry_selected_basepoint=None,
        geometry_selected_orientation=None,
        geometry_selected_traversal_word=None,
        geometry_selected_attaching_word=None,
        current_global_monodromy=None,
        current_arithmetic_readout=None,
        observation_comparison=None,
        numerical_next_gonol=None,
    )


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def receipt_payload() -> dict[str, Any]:
    root = _stack_root()
    result = audit()
    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "producer_code_reference": _producer_code_reference(),
        "source": {
            "authority": "The-Interdependency/ucns",
            "ucns_commit": extension.PINNED_UCNS_COMMIT,
            "source_file_digests": [
                {"path": path, "sha256": digest}
                for path, digest in _source_file_digests(root)
            ],
            "ordered_groupoid_receipt_sha256": groupoid_module.receipt_digest(),
            "ordered_invariant_audit_receipt_sha256": invariant_audit.receipt_digest(),
        },
        "experiment_boundary": {
            "question": "does current Public Gonol geometry select a canonical based complete-return traversal?",
            "admitted_selector_basis": "intrinsic replayable UCNS geometry only",
            "excluded_selector_bases": [
                "caller order",
                "carrier tuple order without a geometric operation",
                "local API or frame default",
                "construction ordinal or scale address",
                "seed order without a recursive Public Gonol attachment",
                "hash or id",
                "observed gonol cardinality or arithmetic factor",
            ],
            "observed_successor_cardinality_input": None,
            "observed_arithmetic_factor_input": None,
        },
        "audit": result.to_payload(),
        "nonclaims": list(NONCLAIMS),
        "falsification_conditions": list(FALSIFICATION_CONDITIONS),
        "promotion_evidence": list(PROMOTION_EVIDENCE),
        "hmmm": list(HMMM),
    }


def receipt_bytes() -> bytes:
    return _canonical_bytes(receipt_payload())


def receipt_digest() -> str:
    return sha256(receipt_bytes()).hexdigest()


def main() -> None:
    payload = receipt_payload()
    payload["receipt_sha256"] = receipt_digest()
    print(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
