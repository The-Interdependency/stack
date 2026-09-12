"""Executable Public Gonol functional operations research.

This module formalizes mechanic 1 from the UCNS gonol research handoff:
operations on the pinned 157-position Public Gonol carrier. It does not define
glyph semantics, infer operations from Unicode names or shapes, or run gonol
successor validation. The observed successor values are intentionally absent
from this mechanic.
"""

# === MODULE_BUILD ===
# id: ucns_public_gonol_functional_operations
#   module_name: public_gonol_functional_operations
#   module_kind: experiment
#   summary: defines stack-local executable Public Gonol carrier operations, composition, closure receipts, participation records, and admissible transformation checks without assigning glyph semantics
#   owner: The Interdependency
#   public_surface: PublicGonolCarrier, PublicGonolAddress, PublicGonolOperation, ClosedOperation, ParticipationRecord, load_carrier, identity_operation, cyclic_order_motion, compose_operations, close_operation, participation_record, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _stack_root, _load_module, _canonical_bytes, _file_digest, _source_file_digests, _cyclic_offset, _operation_payload, _producer_code_reference
#   auth_boundary: none; reads stack-pinned UCNS Public Gonol and geometry authority files only
#   storage_boundary: read stack-manifest.json, research/ucns/BASE.json, and libs/ucns source/canon files; no writes at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_public_gonol_functional_operations.py
#   rollout: stack-local research machinery; no UCNS canon, stack libs, or PCEA promotion
#   rollback: remove this module, its tests, and its research report
#   requires: ucns_public_gonol_geometry, gonol-build construction discipline
#   since: 2026-09-02
#   unresolved: whether cyclic order motion is canonical Public Gonol topology; exact operation expressed by each function position; coupling geometry that consumes closed operations; recursive-scale use of closed operations
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: public_gonol_operations_bind_pinned_carrier
#   given: the operation layer is loaded
#   then: it binds the stack-pinned UCNS commit, exact 157-position Public Gonol digest, source file digests, and origin position
#   class: safety
#   since: 2026-09-02
#
# id: public_gonol_operations_are_position_relations_not_glyph_semantics
#   given: a Public Gonol operation is constructed
#   then: application is defined only by carrier positions and never by glyph class, Unicode name, punctuation role, lexical role, or mathematical interpretation
#   class: doctrine
#   since: 2026-09-02
#
# id: public_gonol_operations_compose_as_total_carrier_functions
#   given: two total carrier operations over the same pinned carrier
#   then: composition is total, deterministic, associative under application, and has identity as a two-sided neutral operation
#   class: correctness
#   since: 2026-09-02
#
# id: public_gonol_admissible_transformations_are_bijective
#   given: an operation is declared as an admissible carrier transformation
#   then: every carrier position maps to exactly one carrier position and every carrier position is reached exactly once
#   class: correctness
#   since: 2026-09-02
#
# id: public_gonol_closure_receipts_are_deterministic
#   given: an operation is closed over the pinned 157-position carrier
#   then: the closure receipt binds operation identity, mapping digest, source provenance, standing, nonclaims, hmmm, and falsification conditions byte-identically
#   class: evidence
#   since: 2026-09-02
#
# id: public_gonol_participation_records_preserve_occurrence_identity
#   given: one participant position is operated on in an occurrence-addressed context
#   then: the participation record retains occurrence identity, input address, output address, operation identity, carrier digest, and operation digest
#   class: correctness
#   since: 2026-09-02
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
from types import ModuleType
from typing import Any


SCHEMA = "the-interdependency.stack-research.ucns.public-gonol-functional-operations"
VERSION = "0.1.0"
STANDING = "stack-local-research-machinery"
SELECTION_EFFECT = "none"
PINNED_UCNS_COMMIT = "1975fe70cf4e0826a8020c2da3047569e277af64"
PINNED_PUBLIC_GONOL_SHA256 = "55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5"

OPERATION_STANDINGS = frozenset({
    "pinned-carrier-identity",
    "stack-local-candidate",
    "composed-stack-local-candidate",
})
OPERATION_BASES = frozenset({
    "identity",
    "cyclic_order_motion",
    "explicit_total_carrier_function",
})

NONCLAIMS: tuple[str, ...] = (
    "not UCNS canon",
    "not a stack/libs refresh",
    "not a successor constructor",
    "not PCEA key research",
    "not glyph, Unicode, punctuation, lexical, mathematical, or grammar semantics",
    "not cryptographic, entropy, hardness, or public-authenticity evidence",
)

HMMM: tuple[str, ...] = (
    "cyclic order motion remains a stack-local candidate until UCNS canon confirms wrap topology and orientation",
    "the exact operation expressed by each Public Gonol function position remains unresolved",
    "coupling geometry that consumes closed Public Gonol operations remains unresolved",
    "recursive-scale participation of closed operations remains unresolved",
)

FALSIFICATION_CONDITIONS: tuple[str, ...] = (
    "pinned UCNS source commit or Public Gonol digest changes without refreshing this receipt",
    "an operation maps any input outside the pinned 157-position carrier",
    "an admissible transformation is not bijective over all 157 positions",
    "composition fails identity or associativity checks under application",
    "closure receipts are not byte-identical under deterministic replay",
    "participation records omit occurrence identity, input, output, operation identity, carrier digest, or operation digest",
    "later UCNS authority rejects cyclic order motion as a valid Public Gonol topology",
    "later UCNS authority supplies position-specific function operations that conflict with this carrier-only operation layer",
)

PROMOTION_EVIDENCE: tuple[str, ...] = (
    "UCNS canon or an accepted UCNS research receipt must explicitly authorize at least one non-identity Public Gonol operation",
    "the authorized operation must retain exact carrier membership, occurrence identity, and deterministic replay",
    "the operation must be consumed by an executable coupling geometry without changing its definition after outcome inspection",
    "negative tests must demonstrate rejection of non-total, out-of-carrier, non-bijective, or provenance-dropping variants",
)


class PublicGonolOperationError(ValueError):
    """Raised when a Public Gonol operation violates this research contract."""


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


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise PublicGonolOperationError(f"cannot load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _file_digest(root: Path, relative_path: str) -> tuple[str, str]:
    return (relative_path, sha256((root / relative_path).read_bytes()).hexdigest())


def _source_file_digests(root: Path) -> tuple[tuple[str, str], ...]:
    return tuple(
        _file_digest(root, path)
        for path in (
            "research/ucns/BASE.json",
            "stack-manifest.json",
            "libs/ucns/CANON.md",
            "libs/ucns/docs/GEOMETRY.md",
            "libs/ucns/src/ucns/public_gonol.py",
        )
    )


@dataclass(frozen=True, slots=True)
class PublicGonolAddress:
    """One exact Public Gonol carrier address."""

    index: int
    glyph: str


@dataclass(frozen=True, slots=True)
class PublicGonolCarrier:
    """Pinned 157-position Public Gonol carrier used by this research layer."""

    source_commit: str
    source_repository: str
    arrangement: tuple[str, ...]
    public_gonol_sha256: str
    source_file_digests: tuple[tuple[str, str], ...]
    stack_manifest_work_graph_sha256: str

    def __post_init__(self) -> None:
        if self.source_commit != PINNED_UCNS_COMMIT:
            raise PublicGonolOperationError("UCNS source commit mismatch")
        if len(self.arrangement) != 157:
            raise PublicGonolOperationError("Public Gonol carrier must have exactly 157 positions")
        if len(set(self.arrangement)) != len(self.arrangement):
            raise PublicGonolOperationError("Public Gonol carrier positions must be unique")
        computed = sha256(
            json.dumps(
                self.arrangement,
                ensure_ascii=False,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        if computed != self.public_gonol_sha256 or computed != PINNED_PUBLIC_GONOL_SHA256:
            raise PublicGonolOperationError("Public Gonol digest mismatch")
        if self.arrangement[0] != " ":
            raise PublicGonolOperationError("Public Gonol origin must be SPACE")

    @property
    def arity(self) -> int:
        return len(self.arrangement)

    @property
    def origin(self) -> PublicGonolAddress:
        return self.address(0)

    def address(self, value: int | str | PublicGonolAddress) -> PublicGonolAddress:
        if isinstance(value, PublicGonolAddress):
            self._validate_address(value)
            return value
        if isinstance(value, bool):
            raise PublicGonolOperationError("Public Gonol address cannot be boolean")
        if isinstance(value, int):
            if not 0 <= value < self.arity:
                raise PublicGonolOperationError("Public Gonol index outside carrier")
            return PublicGonolAddress(value, self.arrangement[value])
        if not isinstance(value, str) or len(value) != 1:
            raise PublicGonolOperationError("Public Gonol glyph must be exactly one scalar")
        if 0xD800 <= ord(value) <= 0xDFFF:
            raise PublicGonolOperationError("surrogate code points are not Unicode scalars")
        try:
            return PublicGonolAddress(self.arrangement.index(value), value)
        except ValueError as exc:
            raise PublicGonolOperationError("glyph is not on the Public Gonol carrier") from exc

    def addresses(self) -> tuple[PublicGonolAddress, ...]:
        return tuple(PublicGonolAddress(index, glyph) for index, glyph in enumerate(self.arrangement))

    def _validate_address(self, address: PublicGonolAddress) -> None:
        if isinstance(address.index, bool) or not isinstance(address.index, int):
            raise PublicGonolOperationError("Public Gonol index must be an integer")
        if not 0 <= address.index < self.arity:
            raise PublicGonolOperationError("Public Gonol index outside carrier")
        if self.arrangement[address.index] != address.glyph:
            raise PublicGonolOperationError("glyph does not occupy the declared Public Gonol position")


@dataclass(frozen=True, slots=True)
class PublicGonolOperation:
    """A total operation over the pinned Public Gonol carrier."""

    operation_id: str
    basis: str
    standing: str
    carrier: PublicGonolCarrier
    transform: tuple[int, ...]
    hmmm: tuple[str, ...] = ()
    nonclaims: tuple[str, ...] = NONCLAIMS

    def __post_init__(self) -> None:
        if not self.operation_id.strip():
            raise PublicGonolOperationError("operation_id is required")
        if self.basis not in OPERATION_BASES:
            raise PublicGonolOperationError("operation basis is not admitted by this research layer")
        if self.standing not in OPERATION_STANDINGS:
            raise PublicGonolOperationError("operation standing is not admitted")
        if len(self.transform) != self.carrier.arity:
            raise PublicGonolOperationError("operation must map every carrier position")
        for value in self.transform:
            if isinstance(value, bool) or not isinstance(value, int):
                raise PublicGonolOperationError("operation outputs must be integer positions")
            if not 0 <= value < self.carrier.arity:
                raise PublicGonolOperationError("operation output outside carrier")
        if self.basis == "identity" and self.transform != tuple(range(self.carrier.arity)):
            raise PublicGonolOperationError("identity operation must preserve every carrier position")
        if self.basis == "cyclic_order_motion":
            offset = self.transform[0] % self.carrier.arity
            if any(
                output != (index + offset) % self.carrier.arity
                for index, output in enumerate(self.transform)
            ):
                raise PublicGonolOperationError("cyclic order motion must preserve one fixed carrier offset")

    @property
    def is_bijective(self) -> bool:
        return len(set(self.transform)) == self.carrier.arity

    @property
    def is_admissible_transformation(self) -> bool:
        return self.is_bijective and self.basis in {"identity", "cyclic_order_motion"}

    def apply(self, value: int | str | PublicGonolAddress) -> PublicGonolAddress:
        address = self.carrier.address(value)
        return self.carrier.address(self.transform[address.index])

    def graph(self) -> tuple[tuple[PublicGonolAddress, PublicGonolAddress], ...]:
        return tuple((address, self.apply(address)) for address in self.carrier.addresses())

    @property
    def mapping_sha256(self) -> str:
        return sha256(_canonical_bytes(self.transform)).hexdigest()


@dataclass(frozen=True, slots=True)
class ClosedOperation:
    """Deterministic closure of one operation over the entire carrier."""

    operation: PublicGonolOperation
    receipt: dict[str, Any]

    @property
    def digest(self) -> str:
        return sha256(_canonical_bytes(self.receipt)).hexdigest()


@dataclass(frozen=True, slots=True)
class ParticipationRecord:
    """Occurrence-addressed application of one operation to one participant."""

    operation_id: str
    operation_digest: str
    carrier_digest: str
    occurrence_id: str
    relation_context: str
    input: PublicGonolAddress
    output: PublicGonolAddress

    def as_payload(self) -> dict[str, Any]:
        return {
            "operation_id": self.operation_id,
            "operation_digest": self.operation_digest,
            "carrier_digest": self.carrier_digest,
            "occurrence_id": self.occurrence_id,
            "relation_context": self.relation_context,
            "input": {"index": self.input.index, "glyph": self.input.glyph},
            "output": {"index": self.output.index, "glyph": self.output.glyph},
        }

    @property
    def digest(self) -> str:
        return sha256(_canonical_bytes(self.as_payload())).hexdigest()


def load_carrier() -> PublicGonolCarrier:
    """Load the stack-pinned Public Gonol carrier and provenance."""

    root = _stack_root()
    public_gonol = _load_module(
        "stack_pinned_ucns_public_gonol_for_functional_operations",
        root / "libs" / "ucns" / "src" / "ucns" / "public_gonol.py",
    )
    ucns_base = _load_json(root / "research" / "ucns" / "BASE.json")
    stack_manifest = _load_json(root / "stack-manifest.json")
    arrangement = tuple(public_gonol.PUBLIC_GONOL_157)
    return PublicGonolCarrier(
        source_commit=ucns_base["source_commit"],
        source_repository=ucns_base["source_repository"],
        arrangement=arrangement,
        public_gonol_sha256=public_gonol.public_gonol_sha256(arrangement),
        source_file_digests=_source_file_digests(root),
        stack_manifest_work_graph_sha256=stack_manifest["work_graph_sha256"],
    )


def identity_operation(carrier: PublicGonolCarrier | None = None) -> PublicGonolOperation:
    resolved = carrier or load_carrier()
    return PublicGonolOperation(
        operation_id="public_gonol.identity",
        basis="identity",
        standing="pinned-carrier-identity",
        carrier=resolved,
        transform=tuple(range(resolved.arity)),
    )


def cyclic_order_motion(
    offset: int,
    carrier: PublicGonolCarrier | None = None,
) -> PublicGonolOperation:
    if isinstance(offset, bool) or not isinstance(offset, int):
        raise PublicGonolOperationError("cyclic order offset must be an integer")
    resolved = carrier or load_carrier()
    normalized = offset % resolved.arity
    sign = "+" if normalized >= 0 else ""
    return PublicGonolOperation(
        operation_id=f"public_gonol.cyclic_order_motion:{sign}{normalized}",
        basis="cyclic_order_motion",
        standing="stack-local-candidate",
        carrier=resolved,
        transform=tuple((index + normalized) % resolved.arity for index in range(resolved.arity)),
        hmmm=(
            "cyclic wrap and orientation are executable research machinery, not selected UCNS canon",
        ),
    )


def _same_carrier(first: PublicGonolCarrier, second: PublicGonolCarrier) -> bool:
    return (
        first.source_commit == second.source_commit
        and first.public_gonol_sha256 == second.public_gonol_sha256
        and first.arrangement == second.arrangement
    )


def _cyclic_offset(operation: PublicGonolOperation) -> int | None:
    if operation.basis not in {"identity", "cyclic_order_motion"}:
        return None
    offset = operation.transform[0] % operation.carrier.arity
    if all(output == (index + offset) % operation.carrier.arity for index, output in enumerate(operation.transform)):
        return offset
    return None


def compose_operations(
    first: PublicGonolOperation,
    second: PublicGonolOperation,
) -> PublicGonolOperation:
    """Return the operation that applies ``first`` and then ``second``."""

    if not _same_carrier(first.carrier, second.carrier):
        raise PublicGonolOperationError("cannot compose operations over different carrier identities")
    transform = tuple(second.transform[first.transform[index]] for index in range(first.carrier.arity))
    first_offset = _cyclic_offset(first)
    second_offset = _cyclic_offset(second)
    if first_offset is not None and second_offset is not None:
        combined = (first_offset + second_offset) % first.carrier.arity
        return cyclic_order_motion(combined, first.carrier)
    return PublicGonolOperation(
        operation_id=f"compose({second.operation_id},{first.operation_id})",
        basis="explicit_total_carrier_function",
        standing="composed-stack-local-candidate",
        carrier=first.carrier,
        transform=transform,
        hmmm=first.hmmm + second.hmmm,
        nonclaims=tuple(dict.fromkeys(first.nonclaims + second.nonclaims)),
    )


def _address_payload(address: PublicGonolAddress) -> dict[str, Any]:
    return {"index": address.index, "glyph": address.glyph}


def _operation_payload(operation: PublicGonolOperation) -> dict[str, Any]:
    return {
        "operation_id": operation.operation_id,
        "basis": operation.basis,
        "standing": operation.standing,
        "mapping_sha256": operation.mapping_sha256,
        "is_bijective": operation.is_bijective,
        "is_admissible_transformation": operation.is_admissible_transformation,
        "transform": list(operation.transform),
        "graph": [
            {
                "input": _address_payload(source),
                "output": _address_payload(target),
            }
            for source, target in operation.graph()
        ],
        "hmmm": list(operation.hmmm),
        "nonclaims": list(operation.nonclaims),
    }


def close_operation(operation: PublicGonolOperation) -> ClosedOperation:
    """Close one operation over all carrier positions with deterministic receipt."""

    if not operation.is_admissible_transformation:
        raise PublicGonolOperationError("closed Public Gonol transformations must be bijective")
    carrier = operation.carrier
    receipt = {
        "schema": SCHEMA + ".closed-operation",
        "version": VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "carrier": {
            "source_repository": carrier.source_repository,
            "source_commit": carrier.source_commit,
            "public_gonol_sha256": carrier.public_gonol_sha256,
            "origin": _address_payload(carrier.origin),
            "arity": carrier.arity,
            "stack_manifest_work_graph_sha256": carrier.stack_manifest_work_graph_sha256,
            "source_file_digests": [
                {"path": path, "sha256": digest}
                for path, digest in carrier.source_file_digests
            ],
        },
        "operation": _operation_payload(operation),
        "closure": {
            "closed_over_positions": carrier.arity,
            "total": True,
            "bijective": operation.is_bijective,
            "receipt_scope": "operation mapping and provenance only",
        },
        "falsification_conditions": list(FALSIFICATION_CONDITIONS),
        "promotion_evidence": list(PROMOTION_EVIDENCE),
        "hmmm": list(HMMM),
        "nonclaims": list(NONCLAIMS),
    }
    return ClosedOperation(operation, receipt)


def participation_record(
    operation: PublicGonolOperation,
    participant: int | str | PublicGonolAddress,
    occurrence_id: str,
    relation_context: str,
) -> ParticipationRecord:
    """Apply an operation while preserving occurrence identity and provenance."""

    if not occurrence_id.strip():
        raise PublicGonolOperationError("occurrence_id is required")
    if not relation_context.strip():
        raise PublicGonolOperationError("relation_context is required")
    closed = close_operation(operation)
    source = operation.carrier.address(participant)
    target = operation.apply(source)
    return ParticipationRecord(
        operation_id=operation.operation_id,
        operation_digest=closed.digest,
        carrier_digest=operation.carrier.public_gonol_sha256,
        occurrence_id=occurrence_id,
        relation_context=relation_context,
        input=source,
        output=target,
    )


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def receipt_payload() -> dict[str, Any]:
    """Return the deterministic mechanic-1 research receipt."""

    carrier = load_carrier()
    identity = identity_operation(carrier)
    step_one = cyclic_order_motion(1, carrier)
    step_two = cyclic_order_motion(2, carrier)
    composed = compose_operations(step_one, step_two)
    sample_participation = participation_record(
        step_one,
        carrier.origin,
        "mechanic-1-public-gonol-origin-occurrence",
        "public-gonol-functional-operations-v0-sample",
    )
    operations = (identity, step_one, step_two, composed)
    return {
        "schema": SCHEMA,
        "version": VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "producer_code_reference": _producer_code_reference(),
        "source_identity": {
            "authority": "The-Interdependency/ucns",
            "ucns_commit": carrier.source_commit,
            "source_repository": carrier.source_repository,
            "public_gonol_sha256": carrier.public_gonol_sha256,
            "stack_manifest_work_graph_sha256": carrier.stack_manifest_work_graph_sha256,
            "source_file_digests": [
                {"path": path, "sha256": digest}
                for path, digest in carrier.source_file_digests
            ],
        },
        "mechanic": "Public Gonol functional operations",
        "definition": {
            "carrier_positions": carrier.arity,
            "operation_type": "total function over pinned carrier positions",
            "admissible_transformation": "total bijection over all pinned positions",
            "composition": "second after first, by carrier index",
            "closure": "deterministic receipt over all source and target positions",
            "participation": "occurrence-addressed operation application retaining input, output, operation, carrier, and relation context",
        },
        "operations": [_operation_payload(operation) for operation in operations],
        "closed_operation_digests": [
            {
                "operation_id": operation.operation_id,
                "closure_digest": close_operation(operation).digest,
            }
            for operation in operations
        ],
        "sample_participation": sample_participation.as_payload() | {
            "participation_digest": sample_participation.digest,
        },
        "rejected_alternatives": [
            "glyph class operations",
            "Unicode name operations",
            "punctuation or grammar operations",
            "lexical or mathematical symbol interpretation",
            "partial carrier maps",
            "non-bijective transformations promoted as admissible transformations",
            "successor-number fitting",
        ],
        "falsification_conditions": list(FALSIFICATION_CONDITIONS),
        "promotion_evidence": list(PROMOTION_EVIDENCE),
        "hmmm": list(HMMM),
        "nonclaims": list(NONCLAIMS),
        "next_dependency_complete_action": (
            "use this closed carrier-operation layer as input to an executable "
            "affinization/affixiation coupling candidate without changing mechanic 1"
        ),
    }


def receipt_bytes(payload: dict[str, Any] | None = None) -> bytes:
    receipt = payload if payload is not None else receipt_payload()
    return _canonical_bytes(receipt) + b"\n"


def receipt_digest(payload: dict[str, Any] | None = None) -> str:
    return sha256(receipt_bytes(payload)).hexdigest()


def main() -> None:
    payload = receipt_payload()
    print(json.dumps(
        {"receipt_sha256": receipt_digest(payload), "receipt": payload},
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
