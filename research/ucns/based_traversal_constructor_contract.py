"""Fail-closed contract for a geometry-selected UCNS based traversal.

This module does not choose traversal geometry.  It evaluates the five required
constructor fields in dependency order against explicitly registered,
authority-bound UCNS derivations.  Current canon supplies a distinguished
carrier origin but no attachment from that origin to a recursive return-
groupoid object, so evaluation stops at the first field.
"""

# === MODULE_BUILD ===
# id: ucns_based_traversal_constructor_contract
#   module_name: based_traversal_constructor_contract
#   module_kind: experiment
#   summary: defines and executes the minimal five-field UCNS based-traversal certificate contract, stopping at the first field not derivable from pinned canon
#   owner: The Interdependency
#   public_surface: ConstructorContractError, FieldRequirement, FieldDerivation, FieldEvaluation, OriginPrimitiveEvidence, BasedTraversalContractResult, field_requirements, origin_primitive_evidence, registered_derivations, evaluate_fields, certificate_output_contract, construct, receipt_payload, receipt_bytes, receipt_digest, formatted_receipt_bytes, write_frozen_receipt
#   internal_surface: _stack_root, _canonical_bytes, _file_digest, _source_file_digests, _load_and_verify_receipt, _derivation_replay_payload, _verify_derivation, _producer_code_reference, main
#   auth_boundary: none; consumes only the pinned UCNS view and frozen stack-local obstruction receipts
#   storage_boundary: read-only except explicit generation of the fixed stack-local receipt path
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_based_traversal_constructor_contract.py
#   rollout: stack-local constructor-contract gate only; no UCNS canon, PCEA, traversal, monodromy, arithmetic, or successor promotion
#   rollback: remove this module, its tests, report, and receipt
#   requires: ucns_geometry_selected_based_traversal_audit, ucns_based_traversal_provenance_history_audit, gonol-build construction discipline
#   since: 2026-09-03
#   unresolved: authoritative origin-to-recursive-groupoid attachment; all downstream traversal fields remain dependency-blocked
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: based_traversal_contract_binds_current_authority
#   given: the constructor contract is evaluated
#   then: pinned UCNS geometry plus the geometry-selection and provenance stop receipts are bound to exact identities before any field is considered
#   class: evidence
#   since: 2026-09-03
#
# id: based_traversal_contract_orders_five_fields
#   given: constructor fields are evaluated
#   then: origin attachment, direction, rotation, outgoing dart, and closure are evaluated in dependency order with no later field evaluated after a stop
#   class: correctness
#   since: 2026-09-03
#
# id: based_traversal_contract_rejects_nongeometric_derivations
#   given: a field derivation depends on source order, caller order, API defaults, commits, ids, hashes, prose adjacency, or PCEA expectations
#   then: the derivation is rejected rather than registered as intrinsic UCNS geometry
#   class: safety
#   since: 2026-09-03
#
# id: based_traversal_contract_separates_origin_from_attachment
#   given: pinned Public Gonol position zero and Structural Null position zero are present
#   then: those primitives are retained while the absent morphism to a recursive return-groupoid object remains the first missing field
#   class: doctrine
#   since: 2026-09-03
#
# id: based_traversal_contract_stops_at_first_missing_field
#   given: no authority-bound origin-attachment derivation is registered
#   then: status is STOP_MISSING_ORIGIN_ATTACHMENT, origin_attachment is hmmm, later fields are dependency-blocked, and no constructor output is emitted
#   class: safety
#   since: 2026-09-03
#
# id: based_traversal_contract_defines_certificate_output
#   given: a future constructor claims completion
#   then: it must bind all five derivations, exact UCNS authority and input geometry, a deterministic traversal word, closure output, and independent replay digest
#   class: doctrine
#   since: 2026-09-03
#
# id: based_traversal_contract_receipt_replays
#   given: pinned canon and predecessor receipts are unchanged
#   then: canonical payload bytes, payload digest, and formatted receipt replay byte-identically
#   class: evidence
#   since: 2026-09-03
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any

import based_traversal_provenance_history_audit as provenance
import geometry_selected_based_traversal_audit as selection


SCHEMA_ID = "the-interdependency.stack-research.ucns.based-traversal-constructor-contract"
SCHEMA_VERSION = "0.1.0"
STANDING = "stack-local-fail-closed-constructor-contract"
SELECTION_EFFECT = "none"

PINNED_UCNS_COMMIT = "1975fe70cf4e0826a8020c2da3047569e277af64"
PINNED_UCNS_TREE = "06c2fe6cf2e148d610808c6f00f4a26e85f43d62"
STOP_STATUS = "STOP_MISSING_ORIGIN_ATTACHMENT"
MISSING_STATUS = "MISSING_AUTHORITATIVE_GEOMETRIC_DERIVATION"
BLOCKED_STATUS = "NOT_EVALUATED_DEPENDENCY_BLOCKED"
READY_STATUS = "AUTHORITY_BOUND_DERIVATION_READY"

FIELD_ORDER = (
    "origin_attachment",
    "directed_tangent_or_chirality",
    "rotation_system",
    "marked_outgoing_dart",
    "closure_rule",
)

ALLOWED_SELECTION_BASIS = "intrinsic-ucns-geometry"
FORBIDDEN_SELECTION_BASES = (
    "carrier tuple order",
    "source text order",
    "caller order",
    "caller slot order",
    "API default",
    "local frame default",
    "construction ordinal",
    "commit order",
    "prose adjacency",
    "identifier",
    "hash",
    "PCEA expectation",
    "observed gonol number",
)

NONCLAIMS = (
    "not a completed based-traversal constructor",
    "not evidence that position zero alone attaches to a recursive path object",
    "not permission to choose orientation, cyclic order, first dart, or closure by convention",
    "not a traversal word, attaching word, monodromy, arithmetic readout, or gonol successor",
    "not PCEA work and not a PCEA control comparison",
    "not UCNS canon",
)

HMMM = (
    "origin_attachment: current UCNS canon distinguishes Public Gonol and Structural Null origin, but defines no geometric morphism from that origin to one recursive return-groupoid object",
    "the contract stops before direction because direction must be transported through the missing attachment",
    "rotation system, marked outgoing dart, and closure rule are not evaluated after the first missing dependency",
    "resume only when an authoritative UCNS geometric operation supplies the origin attachment with deterministic replay evidence",
)


class ConstructorContractError(ValueError):
    """Raised when a derivation or constructor result crosses the contract."""


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
            "libs/ucns/docs/GEOMETRY.md",
            "libs/ucns/src/ucns/public_gonol.py",
            "libs/ucns/src/ucns/carrier.py",
            "libs/ucns/src/ucns/direct_mobius.py",
            "research/ucns/geometry_selected_based_traversal_audit.py",
            "research/ucns/receipts/geometry-selected-based-traversal-audit-v0.json",
            "research/ucns/based_traversal_provenance_history_audit.py",
            "research/ucns/receipts/based-traversal-provenance-history-audit-v0.json",
        )
    )


def _load_and_verify_receipt(relative_path: str, expected_digest: str) -> dict[str, Any]:
    path = _stack_root() / relative_path
    payload = json.loads(path.read_bytes())
    recorded = payload.pop("receipt_sha256")
    replayed = sha256(_canonical_bytes(payload)).hexdigest()
    if recorded != expected_digest or replayed != expected_digest:
        raise ConstructorContractError(f"receipt identity changed: {relative_path}")
    return payload


@dataclass(frozen=True, slots=True)
class FieldRequirement:
    """One field in the ordered based-traversal certificate contract."""

    field: str
    prerequisites: tuple[str, ...]
    required_semantics: str
    acceptance_condition: str
    current_authoritative_primitives: tuple[str, ...]
    forbidden_substitutes: tuple[str, ...]

    def to_payload(self) -> dict[str, Any]:
        return {
            "field": self.field,
            "prerequisites": list(self.prerequisites),
            "required_semantics": self.required_semantics,
            "acceptance_condition": self.acceptance_condition,
            "current_authoritative_primitives": list(self.current_authoritative_primitives),
            "forbidden_substitutes": list(self.forbidden_substitutes),
        }


@lru_cache(maxsize=1)
def field_requirements() -> tuple[FieldRequirement, ...]:
    """Return the five fields in their load-bearing dependency order."""

    common_forbidden = FORBIDDEN_SELECTION_BASES
    requirements = (
        FieldRequirement(
            "origin_attachment",
            (),
            "attach one intrinsic Public Gonol or Structural Null origin to one recursive return-groupoid object",
            "an authoritative UCNS geometric morphism identifies both source origin and target path object and replays independently",
            (
                "Public Gonol carrier position zero",
                "direct Mobius Structural Null carrier position zero",
                "coordinate-free carrier Structural Null",
            ),
            common_forbidden,
        ),
        FieldRequirement(
            "directed_tangent_or_chirality",
            ("origin_attachment",),
            "transport one intrinsic directed germ or chirality through the origin attachment",
            "geometry selects one direction and demonstrates why exact sign reflection no longer preserves the attached structure",
            (
                "positive and reversed local frames",
                "caller-addressable positive and negative displacement",
            ),
            common_forbidden,
        ),
        FieldRequirement(
            "rotation_system",
            ("origin_attachment", "directed_tangent_or_chirality"),
            "derive cyclic incidence for every oriented recursive return germ",
            "an intrinsic incidence operation returns one replayable cyclic order independent of storage and caller enumeration",
            ("unmarked identical local return loops",),
            common_forbidden,
        ),
        FieldRequirement(
            "marked_outgoing_dart",
            ("rotation_system",),
            "mark one outgoing recursive germ as the based traversal start",
            "geometry distinguishes one dart after cyclic incidence, preventing cyclic conjugacy from erasing the based word",
            ("distinguished carrier origin without an outgoing relation germ",),
            common_forbidden,
        ),
        FieldRequirement(
            "closure_rule",
            (
                "origin_attachment",
                "directed_tangent_or_chirality",
                "rotation_system",
                "marked_outgoing_dart",
            ),
            "close the selected ordered return as an attaching or monodromy word",
            "the same geometry deterministically emits termination, the complete traversal word, and a replay-verifiable closure witness",
            ("local two-turn frame restoration",),
            common_forbidden,
        ),
    )
    if tuple(item.field for item in requirements) != FIELD_ORDER:
        raise ConstructorContractError("field requirement order changed")
    return requirements


@dataclass(frozen=True, slots=True)
class FieldDerivation:
    """Envelope for a future authority-bound geometric field derivation."""

    field: str
    authority: str
    ucns_commit: str
    operation_id: str
    source_paths: tuple[str, ...]
    selection_basis: str
    input_binding_sha256: str
    output_payload: dict[str, Any]
    replay_sha256: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "field": self.field,
            "authority": self.authority,
            "ucns_commit": self.ucns_commit,
            "operation_id": self.operation_id,
            "source_paths": list(self.source_paths),
            "selection_basis": self.selection_basis,
            "input_binding_sha256": self.input_binding_sha256,
            "output_payload": self.output_payload,
            "replay_sha256": self.replay_sha256,
        }


def _derivation_replay_payload(derivation: FieldDerivation) -> dict[str, Any]:
    payload = derivation.to_payload()
    payload.pop("replay_sha256")
    return payload


def _verify_derivation(requirement: FieldRequirement, derivation: FieldDerivation) -> None:
    if derivation.field != requirement.field:
        raise ConstructorContractError("derivation field does not match requirement")
    if derivation.authority != "The-Interdependency/ucns":
        raise ConstructorContractError("derivation is not owned by UCNS authority")
    if derivation.ucns_commit != PINNED_UCNS_COMMIT:
        raise ConstructorContractError("derivation is not bound to pinned UCNS commit")
    if derivation.selection_basis != ALLOWED_SELECTION_BASIS:
        raise ConstructorContractError("derivation is not selected by intrinsic UCNS geometry")
    if not derivation.operation_id or not derivation.source_paths:
        raise ConstructorContractError("derivation lacks operation or source provenance")
    if len(derivation.input_binding_sha256) != 64:
        raise ConstructorContractError("derivation input binding is not a SHA-256 identity")
    replayed = sha256(_canonical_bytes(_derivation_replay_payload(derivation))).hexdigest()
    if derivation.replay_sha256 != replayed:
        raise ConstructorContractError("derivation replay digest does not match")


@lru_cache(maxsize=1)
def registered_derivations() -> tuple[FieldDerivation, ...]:
    """Return current canon-backed derivations; deliberately empty at this stop."""

    return ()


@dataclass(frozen=True, slots=True)
class OriginPrimitiveEvidence:
    """Retain exact origin primitives without relabeling them as attachment."""

    public_gonol_index: int
    public_gonol_glyph: str
    public_gonol_arrangement_sha256: str
    direct_structural_null_carrier_position: int
    carrier_structural_null_coordinate_free: bool
    recursive_groupoid_base_object: str
    origin_to_groupoid_attachment: None
    status: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "public_gonol_origin": {
                "index": self.public_gonol_index,
                "glyph": self.public_gonol_glyph,
                "arrangement_sha256": self.public_gonol_arrangement_sha256,
            },
            "direct_structural_null_carrier_position": self.direct_structural_null_carrier_position,
            "carrier_structural_null_coordinate_free": self.carrier_structural_null_coordinate_free,
            "recursive_groupoid_base_object": self.recursive_groupoid_base_object,
            "origin_to_groupoid_attachment": self.origin_to_groupoid_attachment,
            "status": self.status,
        }


@lru_cache(maxsize=1)
def origin_primitive_evidence() -> OriginPrimitiveEvidence:
    """Read the predecessor's exact origin witness and preserve its null map."""

    prior = selection.origin_attachment_audit()
    if prior.geometry_selected_origin_to_base_object_map is not None:
        raise ConstructorContractError("predecessor unexpectedly gained origin attachment")
    return OriginPrimitiveEvidence(
        public_gonol_index=prior.public_gonol_index,
        public_gonol_glyph=prior.public_gonol_glyph,
        public_gonol_arrangement_sha256=prior.public_gonol_sha256,
        direct_structural_null_carrier_position=prior.direct_structural_null_carrier_position,
        carrier_structural_null_coordinate_free=prior.carrier_structural_null_coordinate_free,
        recursive_groupoid_base_object=prior.ordered_model_base_object,
        origin_to_groupoid_attachment=None,
        status="ORIGIN_PRIMITIVES_PRESENT__ATTACHMENT_ABSENT",
    )


@dataclass(frozen=True, slots=True)
class FieldEvaluation:
    """One sequential field result."""

    field: str
    status: str
    derivation: FieldDerivation | None
    reason: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "field": self.field,
            "status": self.status,
            "derivation": None if self.derivation is None else self.derivation.to_payload(),
            "reason": self.reason,
        }


@lru_cache(maxsize=1)
def evaluate_fields() -> tuple[FieldEvaluation, ...]:
    """Evaluate fields in order and block every field after the first miss."""

    requirements = field_requirements()
    derivations = registered_derivations()
    by_field = {item.field: item for item in derivations}
    if len(by_field) != len(derivations):
        raise ConstructorContractError("duplicate registered field derivation")

    evaluations = []
    stop_field: str | None = None
    for requirement in requirements:
        if stop_field is not None:
            evaluations.append(FieldEvaluation(
                field=requirement.field,
                status=BLOCKED_STATUS,
                derivation=None,
                reason=f"not evaluated after missing prerequisite field {stop_field}",
            ))
            continue
        derivation = by_field.get(requirement.field)
        if derivation is None:
            stop_field = requirement.field
            evaluations.append(FieldEvaluation(
                field=requirement.field,
                status=MISSING_STATUS,
                derivation=None,
                reason=(
                    "no registered authority-bound intrinsic UCNS geometric operation "
                    "satisfies this field"
                ),
            ))
            continue
        _verify_derivation(requirement, derivation)
        evaluations.append(FieldEvaluation(
            field=requirement.field,
            status=READY_STATUS,
            derivation=derivation,
            reason="authority-bound geometric derivation verified",
        ))
    return tuple(evaluations)


def certificate_output_contract() -> dict[str, Any]:
    """Describe the output required before any traversal may leave UCNS."""

    return {
        "emitted_only_when_all_fields_ready": True,
        "required_field_order": list(FIELD_ORDER),
        "required_authority_bindings": [
            "ucns_repository",
            "ucns_commit",
            "ucns_tree",
            "constructor_id",
            "input_geometry_sha256",
        ],
        "required_field_evidence": [
            "operation_id",
            "source_paths",
            "selection_basis",
            "input_binding_sha256",
            "output_payload",
            "replay_sha256",
        ],
        "required_outputs": [
            "attached_origin_object",
            "selected_direction",
            "rotation_system",
            "marked_outgoing_dart",
            "closure_witness",
            "traversal_word",
            "certificate_sha256",
        ],
        "independent_replay_requirement": (
            "recompute every field and the traversal from pinned input geometry; "
            "canonical bytes must reproduce certificate_sha256"
        ),
    }


@dataclass(frozen=True, slots=True)
class BasedTraversalContractResult:
    """Current sequential contract outcome."""

    status: str
    stop_field: str
    evaluations: tuple[FieldEvaluation, ...]
    hmmm: dict[str, str]
    constructor_certificate: None
    traversal_word: None
    attaching_word: None
    monodromy: None
    arithmetic_readout: None
    successor: None

    def to_payload(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "stop_field": self.stop_field,
            "field_evaluations": [item.to_payload() for item in self.evaluations],
            "hmmm": self.hmmm,
            "constructor_certificate": self.constructor_certificate,
            "outputs": {
                "traversal_word": self.traversal_word,
                "attaching_word": self.attaching_word,
                "monodromy": self.monodromy,
                "arithmetic_readout": self.arithmetic_readout,
                "successor": self.successor,
            },
            "pcea_handoff_permitted": False,
        }


@lru_cache(maxsize=1)
def construct() -> BasedTraversalContractResult:
    """Execute the contract and stop at missing origin attachment."""

    if provenance.audit().history_status != provenance.HISTORY_STATUS:
        raise ConstructorContractError("provenance predecessor status changed")
    if provenance.audit().constructor_status != provenance.CONSTRUCTOR_STATUS:
        raise ConstructorContractError("provenance predecessor constructor boundary changed")
    if selection.audit().status != selection.STATUS:
        raise ConstructorContractError("geometry-selection predecessor status changed")

    origin = origin_primitive_evidence()
    if origin.origin_to_groupoid_attachment is not None:
        raise ConstructorContractError("origin evidence no longer supports this stop")
    evaluations = evaluate_fields()
    missing = tuple(item for item in evaluations if item.status == MISSING_STATUS)
    ready = tuple(item for item in evaluations if item.status == READY_STATUS)
    if len(missing) != 1 or ready:
        raise ConstructorContractError("current first-field stop no longer replays")
    stop_field = missing[0].field
    if stop_field != "origin_attachment":
        raise ConstructorContractError("unexpected first missing field")
    return BasedTraversalContractResult(
        status=STOP_STATUS,
        stop_field=stop_field,
        evaluations=evaluations,
        hmmm={
            "field": stop_field,
            "unresolved": (
                "geometric morphism from intrinsic Public Gonol or Structural Null origin "
                "to one recursive return-groupoid object"
            ),
            "promotion_evidence": (
                "authoritative UCNS operation, exact source identity, target path object, "
                "intrinsic selection proof, and deterministic replay receipt"
            ),
        },
        constructor_certificate=None,
        traversal_word=None,
        attaching_word=None,
        monodromy=None,
        arithmetic_readout=None,
        successor=None,
    )


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def receipt_payload() -> dict[str, Any]:
    geometry_receipt = _load_and_verify_receipt(
        "research/ucns/receipts/geometry-selected-based-traversal-audit-v0.json",
        "4c4f06aae237fd4ce771dc7849738617b0cbc9ab3cc5bd6685ffec84b2921a09",
    )
    provenance_receipt = _load_and_verify_receipt(
        "research/ucns/receipts/based-traversal-provenance-history-audit-v0.json",
        "ed08c5315ab7dc6988985455d7226ced9151481883b7b8bbb0050ffc2bbc82e2",
    )
    if geometry_receipt["audit"]["status"] != selection.STATUS:
        raise ConstructorContractError("geometry predecessor receipt status changed")
    if provenance_receipt["audit"]["constructor_status"] != provenance.CONSTRUCTOR_STATUS:
        raise ConstructorContractError("provenance predecessor receipt status changed")
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
            "geometry_selection_receipt_sha256": "4c4f06aae237fd4ce771dc7849738617b0cbc9ab3cc5bd6685ffec84b2921a09",
            "provenance_history_receipt_sha256": "ed08c5315ab7dc6988985455d7226ced9151481883b7b8bbb0050ffc2bbc82e2",
        },
        "contract": {
            "field_requirements": [item.to_payload() for item in field_requirements()],
            "allowed_selection_basis": ALLOWED_SELECTION_BASIS,
            "registered_derivations": [item.to_payload() for item in registered_derivations()],
            "certificate_output_contract": certificate_output_contract(),
        },
        "origin_primitive_evidence": origin_primitive_evidence().to_payload(),
        "result": construct().to_payload(),
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
    path = _stack_root() / "research/ucns/receipts/based-traversal-constructor-contract-v0.json"
    path.write_bytes(formatted_receipt_bytes())
    return path


def main() -> None:
    if len(sys.argv) == 2 and sys.argv[1] == "--write-receipt":
        print(write_frozen_receipt())
        return
    if len(sys.argv) != 1:
        raise SystemExit("usage: based_traversal_constructor_contract.py [--write-receipt]")
    sys.stdout.buffer.write(formatted_receipt_bytes())


if __name__ == "__main__":
    main()
