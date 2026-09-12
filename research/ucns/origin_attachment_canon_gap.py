"""Freeze the exact UCNS canon gap at origin attachment.

Pinned UCNS canon distinguishes the Public Gonol/Structural Null origin, but it
does not define an incidence or attachment from that origin to a traversable
recursive object.  This audit records only that first missing relation.  It
does not evaluate direction, rotation, an outgoing dart, or closure.
"""

# === MODULE_BUILD ===
# id: ucns_origin_attachment_canon_gap
#   module_name: origin_attachment_canon_gap
#   module_kind: experiment
#   summary: audits pinned UCNS canon for an origin-to-traversable-structure relation and freezes the exact first-field canon gap without selecting an attachment
#   owner: The Interdependency
#   public_surface: OriginAttachmentCanonGapError, CanonicalCallableInventory, CanonicalGeometryEvidence, ConditionalNativeFiber, AttachmentChoiceAudit, RequiredCanonAxiom, OriginAttachmentCanonGap, canonical_callable_inventory, canonical_geometry_evidence, conditional_native_fiber, attachment_choice_audit, required_canon_axiom, audit, receipt_payload, receipt_bytes, receipt_digest, formatted_receipt_bytes, write_frozen_receipt
#   internal_surface: _stack_root, _canonical_bytes, _file_digest, _source_file_digests, _load_pinned_ucns, _load_and_verify_receipt, _fraction_text, _producer_code_reference, main
#   auth_boundary: none; reads only the exact stack-pinned UCNS canon and frozen UCNS research stop receipts
#   storage_boundary: read-only except explicit generation of the fixed stack-local receipt path
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_origin_attachment_canon_gap.py
#   rollout: stack-local first-field canon-gap record only; no UCNS canon or downstream constructor promotion
#   rollback: remove this module, its test, report, and receipt
#   requires: ucns_based_traversal_constructor_contract, ucns_based_traversal_provenance_history_audit, gonol-build construction discipline
#   since: 2026-09-03
#   unresolved: authoritative geometric incidence from the exact origin to one canon-defined traversable recursive base object
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: origin_attachment_gap_binds_exact_authority
#   given: the origin-attachment audit runs
#   then: the pinned UCNS commit, tree, relevant canonical definitions, tests, receipts, and predecessor stop records are bound to exact identities
#   class: evidence
#   since: 2026-09-03
#
# id: origin_attachment_gap_preserves_null_boundary
#   given: canonical carrier and direct Mobius origin primitives are inspected
#   then: null remains coordinate-free and null-preserving operations do not turn it into a non-null traversable state
#   class: doctrine
#   since: 2026-09-03
#
# id: origin_attachment_gap_rejects_geometric_near_misses
#   given: canonical vesica, seed, prime-lift, and compatibility evidence are inspected
#   then: projected origins, voids, local basepoints, and nonselecting incident structures are not promoted to a Public-Gonol origin attachment
#   class: safety
#   since: 2026-09-03
#
# id: origin_attachment_gap_records_choice_boundary
#   given: current authoritative attachments and the native phase-zero fiber are enumerated
#   then: the authoritative attachment set is empty while the conditional local fiber is recorded as one visible class with two framed lifts and no selected lift
#   class: correctness
#   since: 2026-09-03
#
# id: origin_attachment_gap_defines_minimal_axiom
#   given: current canon contains no origin attachment
#   then: the record states the exact unoriented incidence relation and replay evidence required to close only this field
#   class: doctrine
#   since: 2026-09-03
#
# id: origin_attachment_gap_stops_before_downstream_fields
#   given: origin attachment remains missing
#   then: no downstream constructor field is evaluated and no traversal or constructor continuation is emitted
#   class: safety
#   since: 2026-09-03
#
# id: origin_attachment_gap_receipt_replays
#   given: pinned canon and predecessor receipts are unchanged
#   then: canonical payload bytes, payload digest, and formatted receipt replay byte-identically
#   class: evidence
#   since: 2026-09-03
# === END CONTRACTS ===

from __future__ import annotations

import ast
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
from types import ModuleType
from typing import Any

import based_traversal_constructor_contract as constructor_contract
import based_traversal_provenance_history_audit as provenance


SCHEMA_ID = "the-interdependency.stack-research.ucns.origin-attachment-canon-gap"
SCHEMA_VERSION = "0.1.0"
STANDING = "stack-local-authority-bound-first-field-canon-gap"
SELECTION_EFFECT = "none"

PINNED_UCNS_COMMIT = constructor_contract.PINNED_UCNS_COMMIT
PINNED_UCNS_TREE = constructor_contract.PINNED_UCNS_TREE
STATUS = "CANON_GAP"
FIELD = "origin_attachment"
FIELD_STATUS = constructor_contract.MISSING_STATUS
CURRENT_CHOICE_STATUS = "NO_AUTHORITATIVE_ADMISSIBLE_ATTACHMENT"
FUTURE_CHOICE_STATUS = "NOT_DETERMINABLE_UNTIL_TARGET_STRUCTURE_IS_CANON"

CONSTRUCTOR_RECEIPT_SHA256 = "12100f1bd08d76d2b86bd3d4b7786b5e7bde07fda789dc2937817990c7a5849a"
PROVENANCE_RECEIPT_SHA256 = "ed08c5315ab7dc6988985455d7226ced9151481883b7b8bbb0050ffc2bbc82e2"

NONCLAIMS = (
    "not UCNS canon",
    "not an origin attachment",
    "not a choice of positive or reversed local frame",
    "not a claim that a projected coincidence is a physical vertex",
    "not an evaluation of direction, rotation, outgoing-dart, or closure fields",
    "not a traversal, monodromy, arithmetic readout, or successor operation",
)

HMMM = (
    "the origin has an exact address but no authority-owned incidence to a traversable recursive object",
    "current canon does not define the target recursive path object strongly enough to enumerate future attachment choices",
    "the direct Mobius phase-zero fiber has one visible class and two framed lifts, but neither fact attaches Structural Null to it",
    "the smallest admissible addition is an unoriented geometric incidence; direction must remain a later dependency",
)


class OriginAttachmentCanonGapError(ValueError):
    """Raised when the first-field authority boundary no longer replays."""


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
            "libs/ucns/docs/GEOMETRY.md",
            "libs/ucns/src/ucns/__init__.py",
            "libs/ucns/src/ucns/public_gonol.py",
            "libs/ucns/src/ucns/carrier.py",
            "libs/ucns/src/ucns/direct_mobius.py",
            "libs/ucns/src/ucns/mobius_vesica.py",
            "libs/ucns/src/ucns/mobius_seed.py",
            "libs/ucns/src/ucns/mobius_global_compatibility.py",
            "libs/ucns/src/ucns/prime_primitives.py",
            "libs/ucns/src/ucns/prime_phase_lift.py",
            "libs/ucns/tests/test_public_gonol.py",
            "libs/ucns/tests/test_carrier.py",
            "libs/ucns/tests/test_direct_mobius.py",
            "libs/ucns/tests/test_mobius_seed.py",
            "libs/ucns/tests/test_mobius_global_compatibility.py",
            "libs/ucns/tests/test_prime_primitives.py",
            "libs/ucns/generated/mobius-vesica-certificate.json",
            "libs/ucns/generated/mobius-seed-global-compatibility-certificate.json",
            "libs/ucns/generated/prime-phase-lift-family-certificate.json",
            "research/ucns/based_traversal_constructor_contract.py",
            "research/ucns/receipts/based-traversal-constructor-contract-v0.json",
            "research/ucns/based_traversal_provenance_history_audit.py",
            "research/ucns/receipts/based-traversal-provenance-history-audit-v0.json",
        )
    )


def _load_and_verify_receipt(relative_path: str, expected_digest: str) -> dict[str, Any]:
    payload = json.loads((_stack_root() / relative_path).read_bytes())
    recorded = payload.pop("receipt_sha256")
    replayed = sha256(_canonical_bytes(payload)).hexdigest()
    if recorded != expected_digest or replayed != expected_digest:
        raise OriginAttachmentCanonGapError(f"receipt identity changed: {relative_path}")
    return payload


@lru_cache(maxsize=1)
def _load_pinned_ucns() -> ModuleType:
    package_dir = _stack_root() / "libs" / "ucns" / "src" / "ucns"
    package_name = "stack_pinned_ucns_for_origin_attachment_gap"
    spec = importlib.util.spec_from_file_location(
        package_name,
        package_dir / "__init__.py",
        submodule_search_locations=[str(package_dir)],
    )
    if spec is None or spec.loader is None:
        raise OriginAttachmentCanonGapError("cannot load pinned UCNS package")
    module = importlib.util.module_from_spec(spec)
    sys.modules[package_name] = module
    spec.loader.exec_module(module)
    return module


def _fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True, slots=True)
class CanonicalCallableInventory:
    """Exact declared-callable boundary in the pinned Python package."""

    python_module_count: int
    public_and_native_symbol_modules: tuple[str, ...]
    facade_top_level_callable_count: int
    typed_public_origin_consumers: tuple[str, ...]
    typed_direct_origin_consumers: tuple[str, ...]
    direct_state_factory_parameters: tuple[str, ...]
    declared_origin_to_traversable_callables: tuple[str, ...]

    def to_payload(self) -> dict[str, Any]:
        return {
            "python_module_count": self.python_module_count,
            "public_and_native_symbol_modules": list(self.public_and_native_symbol_modules),
            "facade_top_level_callable_count": self.facade_top_level_callable_count,
            "typed_public_origin_consumers": list(self.typed_public_origin_consumers),
            "typed_direct_origin_consumers": list(self.typed_direct_origin_consumers),
            "direct_state_factory_parameters": list(self.direct_state_factory_parameters),
            "declared_origin_to_traversable_callables": list(
                self.declared_origin_to_traversable_callables
            ),
            "conclusion": (
                "the only module text joining Public Gonol and native Mobius symbols is the "
                "re-export facade; no declared callable consumes either origin type and emits a traversable state"
            ),
        }


@lru_cache(maxsize=1)
def canonical_callable_inventory() -> CanonicalCallableInventory:
    """Inspect declared APIs without interpreting import adjacency as geometry."""

    source_root = _stack_root() / "libs" / "ucns" / "src" / "ucns"
    paths = tuple(sorted(source_root.glob("*.py")))
    bridge_modules = []
    public_consumers = []
    direct_consumers = []
    direct_parameters: tuple[str, ...] = ()
    facade_callables = 0

    for path in paths:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        if "PublicGonolPosition" in source and "NativeMobiusState" in source:
            bridge_modules.append(path.name)
        top_level_callables = tuple(
            node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        )
        if path.name == "__init__.py":
            facade_callables = len(top_level_callables)
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            annotations = tuple(
                ast.unparse(argument.annotation)
                for argument in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs)
                if argument.annotation is not None
            )
            qualified = f"{path.name}:{node.name}"
            if any("PublicGonolPosition" in annotation for annotation in annotations):
                public_consumers.append(qualified)
            if any("StructuralNullIdentity" in annotation for annotation in annotations):
                direct_consumers.append(qualified)
            if path.name == "direct_mobius.py" and node.name == "native_mobius_state":
                direct_parameters = tuple(argument.arg for argument in node.args.args)

    result = CanonicalCallableInventory(
        python_module_count=len(paths),
        public_and_native_symbol_modules=tuple(bridge_modules),
        facade_top_level_callable_count=facade_callables,
        typed_public_origin_consumers=tuple(public_consumers),
        typed_direct_origin_consumers=tuple(direct_consumers),
        direct_state_factory_parameters=direct_parameters,
        declared_origin_to_traversable_callables=tuple(
            sorted(set(public_consumers + direct_consumers))
        ),
    )
    if result.public_and_native_symbol_modules != ("__init__.py",):
        raise OriginAttachmentCanonGapError("canonical Public Gonol/native module boundary changed")
    if result.facade_top_level_callable_count != 0:
        raise OriginAttachmentCanonGapError("package facade unexpectedly gained a constructor")
    if result.typed_public_origin_consumers or result.typed_direct_origin_consumers:
        raise OriginAttachmentCanonGapError("canonical origin type gained a declared consumer")
    if result.direct_state_factory_parameters != ("turns", "frame"):
        raise OriginAttachmentCanonGapError("native Mobius state factory signature changed")
    return result


@dataclass(frozen=True, slots=True)
class CanonicalGeometryEvidence:
    """Positive origin facts and exact exclusions, without inferred incidence."""

    public_origin: dict[str, Any]
    direct_origin: dict[str, Any]
    carrier_structural_null_coordinate_free: bool
    carrier_null_preserved_by_project: bool
    carrier_null_preserved_by_deck_translation: bool
    carrier_null_has_only_null_preimage: bool
    public_origin_to_structural_null_map: None
    structural_null_to_native_state_map: None
    vesica: dict[str, Any]
    seed: dict[str, Any]
    compatibility: dict[str, Any]
    prime_lifts: dict[str, Any]

    def to_payload(self) -> dict[str, Any]:
        return {
            "public_origin": self.public_origin,
            "direct_origin": self.direct_origin,
            "carrier": {
                "structural_null_coordinate_free": self.carrier_structural_null_coordinate_free,
                "null_preserved_by_project": self.carrier_null_preserved_by_project,
                "null_preserved_by_deck_translation": self.carrier_null_preserved_by_deck_translation,
                "null_has_only_null_preimage": self.carrier_null_has_only_null_preimage,
            },
            "missing_maps": {
                "public_origin_to_structural_null": self.public_origin_to_structural_null_map,
                "structural_null_to_native_state": self.structural_null_to_native_state_map,
            },
            "vesica": self.vesica,
            "seed": self.seed,
            "compatibility": self.compatibility,
            "prime_lifts": self.prime_lifts,
        }


@lru_cache(maxsize=1)
def canonical_geometry_evidence() -> CanonicalGeometryEvidence:
    """Evaluate exact canonical origin and non-incidence witnesses."""

    ucns = _load_pinned_ucns()
    public_origin = ucns.public_gonol_function(0)
    direct_origin = ucns.STRUCTURAL_NULL_ORIGIN
    structural_null = ucns.STRUCTURAL_NULL
    vesica = ucns.build_mobius_vesica()
    seed = ucns.build_mobius_seed_of_life()
    seed_null = seed.node_by_id["NULL"]
    seed_occurrences = seed.lifted_occurrences("NULL")

    generated = _stack_root() / "libs" / "ucns" / "generated"
    compatibility = json.loads(
        (generated / "mobius-seed-global-compatibility-certificate.json").read_bytes()
    )
    prime_lifts = json.loads(
        (generated / "prime-phase-lift-family-certificate.json").read_bytes()
    )

    result = CanonicalGeometryEvidence(
        public_origin={
            "index": public_origin.index,
            "glyph": public_origin.glyph,
            "arrangement_sha256": ucns.PUBLIC_GONOL_SHA256,
            "operation_beyond_carrier_identity": None,
        },
        direct_origin={
            "origin_id": direct_origin.origin_id,
            "carrier_position": direct_origin.carrier_position,
            "phase_turns": None,
            "frame": None,
        },
        carrier_structural_null_coordinate_free=not any(
            hasattr(structural_null, field)
            for field in ("angle", "phase", "phase_turns", "frame")
        ),
        carrier_null_preserved_by_project=ucns.project(structural_null) is structural_null,
        carrier_null_preserved_by_deck_translation=(
            ucns.deck_translate(structural_null) is structural_null
        ),
        carrier_null_has_only_null_preimage=(
            ucns.lifted_preimages(structural_null) == (structural_null,)
        ),
        public_origin_to_structural_null_map=None,
        structural_null_to_native_state_map=None,
        vesica={
            "selection_effect": vesica.selection_effect,
            "null_clearance_lower_bound": _fraction_text(
                vesica.parameters.null_clearance_lower_bound
            ),
            "origin_incident_to_band": False,
            "standing": "origin excluded from both bands",
        },
        seed={
            "selection_effect": seed.selection_effect,
            "projected_null_incident_slot_count": len(seed_null.incident_slots),
            "projected_null_is_vertex": seed_null.is_vertex,
            "projected_null_is_structural_null": seed_null.is_structural_null,
            "lifted_occurrence_count": len(seed_occurrences),
            "all_lifted_occurrences_nonzero": all(
                height.sign() != 0 for _, _, height in seed_occurrences
            ),
            "origin_contact_margin": seed.origin_contact_margin_exact().as_dict(),
            "origin_contact_margin_positive": seed.origin_contact_margin_exact().sign() > 0,
            "standing": "projection coincidence remains a nonvertex void",
        },
        compatibility={
            "selection_effect": compatibility["selection_effect"],
            "compatible_incident_checks": compatibility["full_state"][
                "compatible_incident_checks"
            ],
            "standing": (
                "all tested incident seed-edge full states are incompatible; "
                "no origin attachment is supplied"
            ),
        },
        prime_lifts={
            "selection_effect": prime_lifts["selection_effect"],
            "p5_origin_void_lower_bound": prime_lifts["p5"]["lift"][
                "origin_void_lower_bound"
            ],
            "p7_origin_void_lower_bound": prime_lifts["p7"]["lift"][
                "origin_void_lower_bound"
            ],
            "public_gonol_bridge": None,
            "standing": "prime-indexed local origin voids, not Public Gonol attachment",
        },
    )
    if not all((
        result.carrier_structural_null_coordinate_free,
        result.carrier_null_preserved_by_project,
        result.carrier_null_preserved_by_deck_translation,
        result.carrier_null_has_only_null_preimage,
        result.vesica["null_clearance_lower_bound"] == "49/100",
        not result.seed["projected_null_is_vertex"],
        not result.seed["projected_null_is_structural_null"],
        result.seed["all_lifted_occurrences_nonzero"],
        result.seed["origin_contact_margin_positive"],
        result.compatibility["compatible_incident_checks"] == 0,
    )):
        raise OriginAttachmentCanonGapError("canonical non-incidence evidence changed")
    return result


@dataclass(frozen=True, slots=True)
class ConditionalNativeFiber:
    """The local phase-zero target fiber, explicitly not an attachment set."""

    assumption: str
    visible_key: tuple[str, str]
    visible_class_count: int
    framed_lifts: tuple[dict[str, str], ...]
    framed_lift_count: int
    one_turn_exchanges_framed_lifts: bool
    selected_framed_lift: None
    standing: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "assumption": self.assumption,
            "visible_key": list(self.visible_key),
            "visible_class_count": self.visible_class_count,
            "framed_lifts": list(self.framed_lifts),
            "framed_lift_count": self.framed_lift_count,
            "one_turn_exchanges_framed_lifts": self.one_turn_exchanges_framed_lifts,
            "selected_framed_lift": self.selected_framed_lift,
            "standing": self.standing,
        }


@lru_cache(maxsize=1)
def conditional_native_fiber() -> ConditionalNativeFiber:
    """Describe the smallest local fiber without asserting origin incidence."""

    ucns = _load_pinned_ucns()
    positive = ucns.native_mobius_state(0, ucns.NativeMobiusFrame.POSITIVE)
    reversed_state = ucns.native_mobius_state(0, ucns.NativeMobiusFrame.REVERSED)
    visible_keys = {positive.visible_key, reversed_state.visible_key}
    result = ConditionalNativeFiber(
        assumption="the undeclared attachment target is the native Mobius phase-zero fiber",
        visible_key=(positive.visible_key[0], _fraction_text(positive.visible_key[1])),
        visible_class_count=len(visible_keys),
        framed_lifts=(
            {
                "phase_turns": _fraction_text(positive.phase_turns),
                "frame": positive.frame.value,
            },
            {
                "phase_turns": _fraction_text(reversed_state.phase_turns),
                "frame": reversed_state.frame.value,
            },
        ),
        framed_lift_count=2,
        one_turn_exchanges_framed_lifts=(
            positive.advance(1) == reversed_state
            and reversed_state.advance(1) == positive
        ),
        selected_framed_lift=None,
        standing="CONDITIONAL_TARGET_FIBER_ONLY__NOT_ATTACHMENT_CHOICES",
    )
    if result.visible_class_count != 1 or not result.one_turn_exchanges_framed_lifts:
        raise OriginAttachmentCanonGapError("native phase-zero fiber changed")
    return result


@dataclass(frozen=True, slots=True)
class AttachmentChoiceAudit:
    """Separate current admissible attachments from counterfactual targets."""

    authoritative_admissible_attachments: tuple[dict[str, Any], ...]
    authoritative_attachment_count: int
    current_status: str
    future_attachment_choice_space_determinable: bool
    future_status: str
    reason: str
    conditional_native_target_fiber: ConditionalNativeFiber

    def to_payload(self) -> dict[str, Any]:
        return {
            "authoritative_admissible_attachments": list(
                self.authoritative_admissible_attachments
            ),
            "authoritative_attachment_count": self.authoritative_attachment_count,
            "current_status": self.current_status,
            "future_attachment_choice_space_determinable": (
                self.future_attachment_choice_space_determinable
            ),
            "future_status": self.future_status,
            "reason": self.reason,
            "conditional_native_target_fiber": self.conditional_native_target_fiber.to_payload(),
        }


@lru_cache(maxsize=1)
def attachment_choice_audit() -> AttachmentChoiceAudit:
    """Return no attachment while retaining the bounded local target fiber."""

    return AttachmentChoiceAudit(
        authoritative_admissible_attachments=(),
        authoritative_attachment_count=0,
        current_status=CURRENT_CHOICE_STATUS,
        future_attachment_choice_space_determinable=False,
        future_status=FUTURE_CHOICE_STATUS,
        reason=(
            "canon defines neither an origin incidence nor the recursive traversable codomain; "
            "therefore no future attachment alternatives can be declared complete"
        ),
        conditional_native_target_fiber=conditional_native_fiber(),
    )


@dataclass(frozen=True, slots=True)
class RequiredCanonAxiom:
    """Minimal additional UCNS relation needed to close only this field."""

    axiom_id: str
    relation: str
    source_requirement: str
    target_requirement: str
    selection_requirement: str
    replay_requirement: str
    minimum_receipt_fields: tuple[str, ...]
    must_not_select: tuple[str, ...]

    def to_payload(self) -> dict[str, Any]:
        return {
            "axiom_id": self.axiom_id,
            "relation": self.relation,
            "source_requirement": self.source_requirement,
            "target_requirement": self.target_requirement,
            "selection_requirement": self.selection_requirement,
            "replay_requirement": self.replay_requirement,
            "minimum_receipt_fields": list(self.minimum_receipt_fields),
            "must_not_select": list(self.must_not_select),
        }


@lru_cache(maxsize=1)
def required_canon_axiom() -> RequiredCanonAxiom:
    """State the missing door without choosing its direction."""

    return RequiredCanonAxiom(
        axiom_id="ucns.origin-to-traversable-base-incidence",
        relation=(
            "an authority-owned geometric incidence iota: {O} -> V(T) with iota(O) = v0, "
            "mapping the exact Public Gonol or Structural Null origin O to one unframed "
            "base object v0 of a canon-defined traversable recursive structure T"
        ),
        source_requirement=(
            "identify the exact origin representation; if Public Gonol position zero and "
            "Structural Null are identified, bind that identification explicitly"
        ),
        target_requirement=(
            "identify T and one target object from intrinsic geometry, including any required "
            "embedding from the native visible phase-zero class into T"
        ),
        selection_requirement=(
            "the target must be invariantly characterized without source, storage, numeric, "
            "commit, caller, or default order"
        ),
        replay_requirement=(
            "independent replay from exact UCNS geometry must reproduce the same source, target, "
            "relation kind, and evidence digest"
        ),
        minimum_receipt_fields=(
            "authority",
            "ucns_commit",
            "operation_id",
            "source_origin_id",
            "target_structure_id",
            "target_object_id",
            "relation_kind",
            "input_geometry_sha256",
            "replay_sha256",
        ),
        must_not_select=(
            "directed tangent or chirality",
            "rotation system",
            "marked outgoing dart",
            "closure rule",
        ),
    )


@dataclass(frozen=True, slots=True)
class OriginAttachmentCanonGap:
    """Final first-field-only canon-gap result."""

    status: str
    field: str
    field_status: str
    origin_attachment: None
    callable_inventory: CanonicalCallableInventory
    geometry_evidence: CanonicalGeometryEvidence
    choices: AttachmentChoiceAudit
    required_axiom: RequiredCanonAxiom
    downstream_fields_evaluated: bool
    constructor_continuation_permitted: bool

    def to_payload(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "field": self.field,
            "field_status": self.field_status,
            "origin_attachment": self.origin_attachment,
            "canonical_callable_inventory": self.callable_inventory.to_payload(),
            "canonical_geometry_evidence": self.geometry_evidence.to_payload(),
            "attachment_choice_audit": self.choices.to_payload(),
            "required_additional_axiom": self.required_axiom.to_payload(),
            "downstream": {
                "fields_evaluated": self.downstream_fields_evaluated,
                "constructor_continuation_permitted": self.constructor_continuation_permitted,
                "reason": "origin_attachment is the first unresolved dependency",
            },
            "stop_reason": (
                "pinned UCNS canon contains an exact origin but no authoritative geometric "
                "incidence from it to a traversable recursive base object"
            ),
        }


@lru_cache(maxsize=1)
def audit() -> OriginAttachmentCanonGap:
    """Audit only origin attachment and stop at the missing relation."""

    predecessor = constructor_contract.construct()
    if predecessor.stop_field != FIELD or predecessor.status != constructor_contract.STOP_STATUS:
        raise OriginAttachmentCanonGapError("constructor predecessor no longer stops at origin attachment")
    if provenance.audit().history_status != provenance.HISTORY_STATUS:
        raise OriginAttachmentCanonGapError("provenance predecessor status changed")
    choices = attachment_choice_audit()
    if choices.authoritative_admissible_attachments:
        raise OriginAttachmentCanonGapError("an attachment choice cannot be selected in this gap record")
    return OriginAttachmentCanonGap(
        status=STATUS,
        field=FIELD,
        field_status=FIELD_STATUS,
        origin_attachment=None,
        callable_inventory=canonical_callable_inventory(),
        geometry_evidence=canonical_geometry_evidence(),
        choices=choices,
        required_axiom=required_canon_axiom(),
        downstream_fields_evaluated=False,
        constructor_continuation_permitted=False,
    )


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def receipt_payload() -> dict[str, Any]:
    constructor_receipt = _load_and_verify_receipt(
        "research/ucns/receipts/based-traversal-constructor-contract-v0.json",
        CONSTRUCTOR_RECEIPT_SHA256,
    )
    provenance_receipt = _load_and_verify_receipt(
        "research/ucns/receipts/based-traversal-provenance-history-audit-v0.json",
        PROVENANCE_RECEIPT_SHA256,
    )
    if constructor_receipt["result"]["stop_field"] != FIELD:
        raise OriginAttachmentCanonGapError("constructor receipt stop field changed")
    if provenance_receipt["audit"]["history_status"] != provenance.HISTORY_STATUS:
        raise OriginAttachmentCanonGapError("provenance receipt status changed")
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
            "constructor_contract_receipt_sha256": CONSTRUCTOR_RECEIPT_SHA256,
            "provenance_history_receipt_sha256": PROVENANCE_RECEIPT_SHA256,
            "network_used": False,
        },
        "scope": {
            "evaluated_field": FIELD,
            "downstream_fields_evaluated": False,
            "admitted_basis": "existing authoritative UCNS geometry only",
            "forbidden_bases": list(constructor_contract.FORBIDDEN_SELECTION_BASES),
        },
        "canon_gap": audit().to_payload(),
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
    path = _stack_root() / "research/ucns/receipts/origin-attachment-canon-gap-v0.json"
    path.write_bytes(formatted_receipt_bytes())
    return path


def main() -> None:
    if len(sys.argv) == 2 and sys.argv[1] == "--write-receipt":
        print(write_frozen_receipt())
        return
    if len(sys.argv) != 1:
        raise SystemExit("usage: origin_attachment_canon_gap.py [--write-receipt]")
    sys.stdout.buffer.write(formatted_receipt_bytes())


if __name__ == "__main__":
    main()
