"""Falsifiable successor constructor from the three frozen UCNS mechanics.

This module composes the executable research mechanics in the smallest declared
way:

1. one Public Gonol cyclic participation per input occurrence;
2. one explicit ordered coupling for each participation;
3. one recursive atomic promotion for each closed coupling;
4. one final successor closure whole.

Observation values are supplied by the caller. The constructor code does not
embed successor targets or interpolation controls.
"""

# === MODULE_BUILD ===
# id: ucns_composed_successor_constructor_v0
#   module_name: composed_successor_constructor
#   module_kind: experiment
#   summary: freezes the three UCNS research mechanic identities and composes their declared operations into the smallest falsifiable successor constructor
#   owner: The Interdependency
#   public_surface: FrozenMechanic, SuccessorConstruction, GateResult, freeze_mechanics, construct_successor_once, evaluate_gate, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _stack_root, _canonical_bytes, _file_digest, _load_json, _mechanic_code_sha256, _mechanic_receipt, _input_digest, _edge_record, _aggregate_digest, _result_payload, _producer_code_reference, main
#   auth_boundary: none; reads stack-pinned UCNS/METAPAT identities and stack-local UCNS research mechanics only
#   storage_boundary: read stack-manifest.json, research/ucns/BASE.json, research/metapat/BASE.json, and research/ucns mechanic modules; no writes at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_composed_successor_constructor.py
#   rollout: stack-local falsification experiment; no UCNS canon, stack libs, or PCEA promotion
#   rollback: remove this module, its tests, and its research report
#   requires: ucns_public_gonol_functional_operations, ucns_affinization_coupling_geometry, ucns_recursive_scale_transition, gonol-build construction discipline
#   since: 2026-09-02
#   unresolved: whether this smallest composition is the selected UCNS successor constructor; successor validation beyond first failed gate; interpolation-control comparison
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: composed_successor_freezes_mechanics_before_gate
#   given: successor gate evaluation begins
#   then: exact code hashes, receipt hashes, and pinned UCNS/METAPAT identities for mechanics 1 through 3 are recorded before any successor output is evaluated
#   class: safety
#   since: 2026-09-02
#
# id: composed_successor_constructor_has_no_target_constants
#   given: the constructor operation is inspected
#   then: successor targets and interpolation controls are not embedded in constructor code or branch conditions
#   class: safety
#   since: 2026-09-02
#
# id: composed_successor_uses_only_declared_mechanics
#   given: one successor step is constructed
#   then: it uses Public Gonol cyclic participation, explicit ordered coupling, recursive atomic promotion, and one final closure without adding fitted terms
#   class: doctrine
#   since: 2026-09-02
#
# id: composed_successor_falsifies_without_tuning
#   given: the first constructed result does not equal the external first target
#   then: status is FALSIFIED, no second gate is run, no next prediction is produced, and no interpolation comparison occurs
#   class: evidence
#   since: 2026-09-02
#
# id: composed_successor_receipt_replays_byte_identical
#   given: the same frozen mechanics and external observation gate are evaluated
#   then: receipt bytes and receipt digest replay byte-identically
#   class: correctness
#   since: 2026-09-02
# === END CONTRACTS ===

from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Iterable

import affinization_coupling_geometry as acg
import public_gonol_functional_operations as pgfo
import recursive_scale_transition as rst


SCHEMA = "the-interdependency.stack-research.ucns.composed-successor-constructor"
VERSION = "0.1.0"
STANDING = "stack-local-falsification-experiment"
SELECTION_EFFECT = "none"

STATUS_FALSIFIED = "FALSIFIED"
STATUS_SURVIVED_FIRST = "SURVIVED_FIRST"
STATUS_SURVIVED = "SURVIVED"

MECHANIC_MODULES: tuple[tuple[str, str, Any], ...] = (
    ("mechanic_1_public_gonol_functional_operations", "public_gonol_functional_operations.py", pgfo),
    ("mechanic_2_affinization_coupling_geometry", "affinization_coupling_geometry.py", acg),
    ("mechanic_3_recursive_scale_transition", "recursive_scale_transition.py", rst),
)

NONCLAIMS: tuple[str, ...] = (
    "not UCNS canon",
    "not a stack/libs refresh",
    "not PCEA runtime or key research",
    "not proof of the gonol recursion",
    "not a fitted recurrence or interpolation",
    "not cryptographic, entropy, hardness, replay-resistance, recovery, or public-authenticity evidence",
)

HMMM: tuple[str, ...] = (
    "whether the smallest mechanics composition is the selected UCNS successor constructor remains unresolved",
    "the first failed gate blocks second-gate execution and next-prediction freezing for this constructor",
    "interpolation-control comparison remains unreached unless a frozen constructor survives both observation gates",
)


class ComposedSuccessorError(ValueError):
    """Raised when the composed successor experiment violates its contract."""


@dataclass(frozen=True, slots=True)
class FrozenMechanic:
    """One frozen mechanic identity before successor testing."""

    mechanic_id: str
    module_path: str
    code_sha256: str
    receipt_sha256: str
    producer_code_reference: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "mechanic_id": self.mechanic_id,
            "module_path": self.module_path,
            "code_sha256": self.code_sha256,
            "receipt_sha256": self.receipt_sha256,
            "producer_code_reference": self.producer_code_reference,
        }


@dataclass(frozen=True, slots=True)
class SuccessorConstruction:
    """One execution of the smallest composed successor constructor."""

    input_size: int
    output_size: int
    layer_counts: dict[str, int]
    aggregate_transition_sha256: str
    sample_edges: tuple[dict[str, Any], ...]
    constructor_id: str = "ucns.smallest-composed-successor.v0"

    def to_payload(self) -> dict[str, Any]:
        return {
            "constructor_id": self.constructor_id,
            "input_size": self.input_size,
            "output_size": self.output_size,
            "layer_counts": self.layer_counts,
            "aggregate_transition_sha256": self.aggregate_transition_sha256,
            "sample_edges": list(self.sample_edges),
        }


@dataclass(frozen=True, slots=True)
class GateResult:
    """Result of the external two-transition observation gate."""

    status: str
    first: SuccessorConstruction
    first_target: int
    second: SuccessorConstruction | None
    second_target: int
    next_prediction: SuccessorConstruction | None
    interpolation_control_comparison: str
    rejection_reason: str | None

    def to_payload(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "first": self.first.to_payload(),
            "first_target": self.first_target,
            "second": None if self.second is None else self.second.to_payload(),
            "second_target": self.second_target,
            "next_prediction": None if self.next_prediction is None else self.next_prediction.to_payload(),
            "interpolation_control_comparison": self.interpolation_control_comparison,
            "rejection_reason": self.rejection_reason,
        }


def _stack_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _file_digest(root: Path, relative_path: str) -> tuple[str, str]:
    return (relative_path, sha256((root / relative_path).read_bytes()).hexdigest())


def _mechanic_code_sha256(module_path: str) -> str:
    return sha256((_stack_root() / "research" / "ucns" / module_path).read_bytes()).hexdigest()


def _mechanic_receipt(module: Any) -> tuple[str, str]:
    payload = module.receipt_payload()
    return (module.receipt_digest(payload), payload["producer_code_reference"])


def freeze_mechanics() -> tuple[FrozenMechanic, ...]:
    """Freeze mechanic code and receipt identities before successor evaluation."""

    frozen: list[FrozenMechanic] = []
    for mechanic_id, module_path, module in MECHANIC_MODULES:
        code_sha256 = _mechanic_code_sha256(module_path)
        receipt_sha256, producer_code_reference = _mechanic_receipt(module)
        if producer_code_reference != "sha256:" + code_sha256:
            raise ComposedSuccessorError(f"{mechanic_id} producer code reference mismatch")
        frozen.append(
            FrozenMechanic(
                mechanic_id=mechanic_id,
                module_path="research/ucns/" + module_path,
                code_sha256=code_sha256,
                receipt_sha256=receipt_sha256,
                producer_code_reference=producer_code_reference,
            )
        )
    return tuple(frozen)


def _input_digest(input_size: int) -> str:
    return sha256(_canonical_bytes({
        "kind": "ucns.successor-input-size",
        "input_size": input_size,
    })).hexdigest()


def _edge_record(
    *,
    slot: int,
    input_size: int,
    operation: pgfo.PublicGonolOperation,
    aff_authority: acg.AuthoritySnapshot,
    transition_authority: rst.TransitionAuthority,
) -> dict[str, Any]:
    carrier = operation.carrier
    source = carrier.address(slot % carrier.arity)
    participation = pgfo.participation_record(
        operation,
        source,
        f"successor-v0.input-{input_size}.slot-{slot}.public-function",
        "smallest-composed-successor-v0",
    )
    coupled = acg.coupling(
        f"successor-v0.input-{input_size}.slot-{slot}.coupling",
        (
            acg.CouplingParticipant(
                participant_id=f"successor-v0.input-{input_size}.slot-{slot}.source",
                scale="successor-input-gonol",
                role="function-source",
                source_digest=_input_digest(input_size),
            ),
            acg.CouplingParticipant(
                participant_id=f"successor-v0.input-{input_size}.slot-{slot}.target",
                scale="public-gonol-function-output",
                role="function-target",
                source_digest=participation.digest,
            ),
        ),
        source_refs=(
            "research.ucns.public_gonol_functional_operations.v0",
            "research.ucns.affinization_coupling_geometry.v0",
        ),
    )
    closed = acg.close_affinization(coupled, aff_authority)
    promoted = rst.promote_closed_affinization(
        closed,
        source_scale="public-gonol-functional-coupling",
        target_scale="recursive-successor-atom",
        occurrence_id=f"successor-v0.input-{input_size}.slot-{slot}.recursive-atom",
        authority=transition_authority,
    )
    return {
        "slot": slot,
        "input_address": {
            "index": source.index,
            "glyph": source.glyph,
        },
        "output_address": {
            "index": participation.output.index,
            "glyph": participation.output.glyph,
        },
        "participation_digest": participation.digest,
        "coupling_digest": coupled.coupling_digest,
        "closed_affinization_digest": closed.digest,
        "atomic_id": promoted.atomic_participant.atomic_id,
        "transition_digest": promoted.digest,
    }


def _aggregate_digest(records: Iterable[dict[str, Any]]) -> str:
    digest = sha256()
    for record in records:
        digest.update(_canonical_bytes(record))
        digest.update(b"\n")
    return digest.hexdigest()


def construct_successor_once(input_size: int, sample_limit: int = 6) -> SuccessorConstruction:
    """Run one successor step using only the frozen mechanics' declared operations."""

    if isinstance(input_size, bool) or not isinstance(input_size, int):
        raise ComposedSuccessorError("input_size must be an integer")
    if input_size <= 0:
        raise ComposedSuccessorError("input_size must be positive")
    if isinstance(sample_limit, bool) or not isinstance(sample_limit, int) or sample_limit < 0:
        raise ComposedSuccessorError("sample_limit must be a nonnegative integer")

    carrier = pgfo.load_carrier()
    operation = pgfo.cyclic_order_motion(1, carrier)
    aff_authority = acg.load_authority_snapshot()
    transition_authority = rst.load_transition_authority()

    sample_slots = tuple(range(min(input_size, sample_limit)))
    sample_edges = tuple(
        _edge_record(
            slot=slot,
            input_size=input_size,
            operation=operation,
            aff_authority=aff_authority,
            transition_authority=transition_authority,
        )
        for slot in sample_slots
    )
    aggregate = _aggregate_digest(
        _edge_record(
            slot=slot,
            input_size=input_size,
            operation=operation,
            aff_authority=aff_authority,
            transition_authority=transition_authority,
        )
        for slot in range(input_size)
    )
    layer_counts = {
        "input_participants": input_size,
        "public_gonol_function_participations": input_size,
        "closed_affinizations": input_size,
        "recursive_atomic_participants": input_size,
        "successor_closure_whole": 1,
    }
    output_size = sum(layer_counts.values())
    return SuccessorConstruction(
        input_size=input_size,
        output_size=output_size,
        layer_counts=layer_counts,
        aggregate_transition_sha256=aggregate,
        sample_edges=sample_edges,
    )


def evaluate_gate(
    *,
    source: int,
    first_target: int,
    second_target: int,
    interpolation_control: int | None = None,
) -> GateResult:
    """Evaluate the external observation gate without target-specific tuning."""

    if any(isinstance(value, bool) or not isinstance(value, int) for value in (source, first_target, second_target)):
        raise ComposedSuccessorError("gate values must be integers")
    if source <= 0 or first_target <= 0 or second_target <= 0:
        raise ComposedSuccessorError("gate values must be positive")
    if interpolation_control is not None and (
        isinstance(interpolation_control, bool) or not isinstance(interpolation_control, int)
    ):
        raise ComposedSuccessorError("interpolation_control must be an integer or None")

    freeze_mechanics()
    first = construct_successor_once(source)
    if first.output_size != first_target:
        return GateResult(
            status=STATUS_FALSIFIED,
            first=first,
            first_target=first_target,
            second=None,
            second_target=second_target,
            next_prediction=None,
            interpolation_control_comparison="not reached; first gate falsified",
            rejection_reason=f"first transition produced {first.output_size}, not external comparator",
        )

    second = construct_successor_once(first.output_size)
    if second.output_size != second_target:
        return GateResult(
            status=STATUS_FALSIFIED,
            first=first,
            first_target=first_target,
            second=second,
            second_target=second_target,
            next_prediction=None,
            interpolation_control_comparison="not reached; second gate falsified",
            rejection_reason=f"second transition produced {second.output_size}, not external comparator",
        )

    next_prediction = construct_successor_once(second.output_size, sample_limit=0)
    comparison = "control not supplied"
    if interpolation_control is not None:
        comparison = "equal" if next_prediction.output_size == interpolation_control else "unequal"
    return GateResult(
        status=STATUS_SURVIVED,
        first=first,
        first_target=first_target,
        second=second,
        second_target=second_target,
        next_prediction=next_prediction,
        interpolation_control_comparison=comparison,
        rejection_reason=None,
    )


def _source_identity(frozen: tuple[FrozenMechanic, ...]) -> dict[str, Any]:
    root = _stack_root()
    ucns_base = _load_json(root / "research" / "ucns" / "BASE.json")
    metapat_base = _load_json(root / "research" / "metapat" / "BASE.json")
    stack_manifest = _load_json(root / "stack-manifest.json")
    return {
        "authority": {
            "ucns": "The-Interdependency/ucns",
            "metapat": "The-Interdependency/metapat",
        },
        "ucns_base": ucns_base,
        "metapat_base": metapat_base,
        "stack_manifest_work_graph_sha256": stack_manifest["work_graph_sha256"],
        "source_file_digests": [
            {"path": path, "sha256": digest}
            for path, digest in (
                _file_digest(root, "research/ucns/BASE.json"),
                _file_digest(root, "research/metapat/BASE.json"),
                _file_digest(root, "stack-manifest.json"),
                _file_digest(root, "libs/ucns/CANON.md"),
                _file_digest(root, "libs/metapat/UCNS_IMPLEMENTATION.md"),
            )
        ],
        "frozen_mechanics": [item.to_payload() for item in frozen],
    }


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def receipt_payload(
    *,
    source: int,
    first_target: int,
    second_target: int,
    interpolation_control: int | None = None,
) -> dict[str, Any]:
    """Return the deterministic composed-constructor receipt."""

    frozen = freeze_mechanics()
    gate = evaluate_gate(
        source=source,
        first_target=first_target,
        second_target=second_target,
        interpolation_control=interpolation_control,
    )
    return {
        "schema": SCHEMA,
        "version": VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "producer_code_reference": _producer_code_reference(),
        "source_identity": _source_identity(frozen),
        "construction_identity": {
            "constructor_id": "ucns.smallest-composed-successor.v0",
            "frozen_before_gate": True,
            "target_values_in_constructor": False,
            "candidate_source": "mechanics 1 through 3 only",
        },
        "external_observation_gate": {
            "source": source,
            "first_target": first_target,
            "second_target": second_target,
            "target_use_policy": "external comparators only; constructor receives input size but not target values",
        },
        "gate_result": gate.to_payload(),
        "summary": {
            "status": gate.status,
            "source_to_first_output": gate.first.output_size,
            "second_gate_executed": gate.second is not None,
            "next_prediction_available": gate.next_prediction is not None,
            "interpolation_control_comparison": gate.interpolation_control_comparison,
        },
        "nonclaims": list(NONCLAIMS),
        "hmmm": list(HMMM),
        "next_dependency_complete_action": (
            "do not tune this constructor toward the comparator; revise only by changing "
            "a frozen mechanic through its own tests and receipts, then rerun as a new constructor"
        ),
    }


def receipt_bytes(payload: dict[str, Any] | None = None, **kwargs: Any) -> bytes:
    receipt = payload if payload is not None else receipt_payload(**kwargs)
    return _canonical_bytes(receipt) + b"\n"


def receipt_digest(payload: dict[str, Any] | None = None, **kwargs: Any) -> str:
    return sha256(receipt_bytes(payload, **kwargs)).hexdigest()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the UCNS composed successor gate.")
    parser.add_argument("source", type=int)
    parser.add_argument("first_target", type=int)
    parser.add_argument("second_target", type=int)
    parser.add_argument("--interpolation-control", type=int, default=None)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = _parser().parse_args(argv)
    payload = receipt_payload(
        source=args.source,
        first_target=args.first_target,
        second_target=args.second_target,
        interpolation_control=args.interpolation_control,
    )
    print(json.dumps(
        {"receipt_sha256": receipt_digest(payload), "receipt": payload},
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
