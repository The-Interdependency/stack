# === MODULE_BUILD ===
# id: metapat_exact_ucns_profile_consumer
#   module_name: metapat.ucns
#   module_kind: adapter
#   summary: consumes only the exact post-reset UCNS ordered-occurrence profile while retaining METAPAT semantic authority externally
#   owner: The Interdependency
#   public_surface: UCNSConsumerStatus, UCNSAdaptationRecord, UCNSAdaptation, require_ucns, adapt_envelope_to_ucns, root_spine_adaptation, root_spine_ucns, compose
#   internal_surface: _package_present, _validate_module
#   auth_boundary: none
#   storage_boundary: deterministic serialized bridge and provenance records
#   network_boundary: package import only
#   user_data_boundary: semantic statements remain external provenance and are not placed in UCNS payloads
#   admin_only: false
#   tests: tests/test_ucns_bridge.py
#   rollout: exact_profile_only
#   rollback: restore typed suspension without restoring archived adapter surfaces
#   requires: metapat_module_envelope, exact UCNS post-reset profile
#   since: 2026-07-23
#   unresolved: no universal composition or factorization is authorized
# === END MODULE_BUILD ===
#
# === CONTRACTS ===
# id: metapat_ucns_exact_identity_or_inactive
#   given: an installed package named ucns is inspected
#   then: only the exact producer epoch, profile, and bridge identities activate the adapter
#   class: safety
#
# id: metapat_ucns_ordered_occurrence_provenance
#   given: a METAPAT envelope is adapted through the exact profile
#   then: statement order and multiplicity survive while semantic text remains external provenance
#   class: provenance
#
# id: metapat_ucns_no_authority_transfer
#   given: an adaptation succeeds
#   then: theorem, measurement, and METAPAT validity transfer fields remain false
#   class: boundary
#
# id: metapat_ucns_archived_operations_rejected
#   given: archived face-bit or universal composition behavior is requested
#   then: the adapter fails closed
#   class: safety
# === END CONTRACTS ===

"""Exact-profile METAPAT consumer for the post-reset UCNS ordered-occurrence bridge.

``UCNS`` is a stable identifier without a canonical expansion. METAPAT retains
semantic authority; UCNS supplies only the explicitly pinned carrier profile.
"""
from __future__ import annotations

import importlib
import importlib.util
import json
from dataclasses import asdict, dataclass
from types import ModuleType
from typing import Any, Mapping

from .envelope import MetapatModuleEnvelope, root_spine_module_envelope

GONOL_VERTEX_COUNT = 157
SPACE_ANCHOR_VERTEX = 0
ADDRESSABLE_GONOL_VERTICES = GONOL_VERTEX_COUNT - 1
UCNS_ADAPTER_SCHEMA = "metapat-ucns-ordered-occurrence-consumer"
UCNS_ADAPTER_VERSION = "1.0.0"
SUPPORTED_PRODUCER_EPOCH = "ucns.post-reset.v1"
SUPPORTED_PROFILE = ("ucns.profile.edcm-metapat-ordered-occurrence", "1.0.0")
SUPPORTED_BRIDGE_SCHEMA = ("ucns.bridge.edcm-metapat-ordered-occurrence", "1.0.0")
PINNED_UCNS_COMMIT = "19f1afddb993f7d933ac8727627e7d5e1c3b88fc"
RESET_BOUNDARY_REASON = "exact post-reset UCNS producer profile is unavailable or mismatched"
REJECTED_LEGACY_SCHEMAS = frozenset({
    "metapat-actual-ucns-adapter-v1",
    "ucns-canonical-json-v1",
    "ucns.bridge-record@1.0.0",
    "ucns.factorization-evidence@1.0.0",
})


class UCNSDependencyError(RuntimeError):
    """Raised when the exact pinned UCNS producer cannot be imported."""


class UCNSAdapterError(RuntimeError):
    """Raised when UCNS fails the exact profile or bridge contract."""


@dataclass(frozen=True, slots=True)
class UCNSConsumerStatus:
    package_present: bool
    producer_recognized: bool
    profile_supported: bool
    adapter_active: bool
    supported_producer_epoch: str = SUPPORTED_PRODUCER_EPOCH
    supported_profile: tuple[str, str] = SUPPORTED_PROFILE
    supported_bridge_schema: tuple[str, str] = SUPPORTED_BRIDGE_SCHEMA
    pinned_ucns_commit: str = PINNED_UCNS_COMMIT
    reason: str | None = None
    theorem_status_transfer: bool = False
    measurement_validity: bool = False
    metapat_validity: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class UCNSAdaptationRecord:
    adapter_schema: str
    adapter_version: str
    producer_epoch: str
    profile_id: str
    profile_version: str
    bridge_schema_id: str
    bridge_schema_version: str
    ucns_source_commit: str
    ucns_stable_identity: str
    ucns_bridge_json: str
    envelope_schema_id: str
    envelope_schema_version: str
    envelope_provenance_digest: str
    canon_version: str
    canon_digest: str
    module_id: str
    module_kind: str
    source_statement_refs: tuple[str, ...]
    source_statements: tuple[str, ...]
    constraints: tuple[str, ...]
    permitted_interpretations: tuple[str, ...]
    unresolved_constraints: tuple[str, ...]
    semantic_mapping: str = "external-provenance"
    theorem_status_transfer: bool = False
    measurement_validity_claim: bool = False
    metapat_validity_claim: bool = False

    def __post_init__(self) -> None:
        if (self.adapter_schema, self.adapter_version) != (UCNS_ADAPTER_SCHEMA, UCNS_ADAPTER_VERSION):
            raise ValueError("unsupported METAPAT UCNS adapter identity")
        if self.producer_epoch != SUPPORTED_PRODUCER_EPOCH:
            raise ValueError("producer epoch mismatch")
        if (self.profile_id, self.profile_version) != SUPPORTED_PROFILE:
            raise ValueError("profile identity mismatch")
        if (self.bridge_schema_id, self.bridge_schema_version) != SUPPORTED_BRIDGE_SCHEMA:
            raise ValueError("bridge schema mismatch")
        if self.ucns_source_commit != PINNED_UCNS_COMMIT:
            raise ValueError("UCNS source commit mismatch")
        if self.semantic_mapping != "external-provenance":
            raise ValueError("semantic text must remain external provenance")
        if self.theorem_status_transfer or self.measurement_validity_claim or self.metapat_validity_claim:
            raise ValueError("validity or theorem status cannot transfer")
        if len(self.source_statement_refs) != len(self.source_statements):
            raise ValueError("source references and statements must preserve ordered occurrence count")

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        for key in ("source_statement_refs", "source_statements", "constraints", "permitted_interpretations", "unresolved_constraints"):
            data[key] = list(data[key])
        return data

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "UCNSAdaptationRecord":
        values = dict(data)
        for key in ("source_statement_refs", "source_statements", "constraints", "permitted_interpretations", "unresolved_constraints"):
            values[key] = tuple(values[key])
        return cls(**values)

    @classmethod
    def from_json(cls, text: str) -> "UCNSAdaptationRecord":
        value = json.loads(text)
        if not isinstance(value, Mapping):
            raise ValueError("adaptation record JSON must contain an object")
        return cls.from_dict(value)


@dataclass(frozen=True, slots=True)
class UCNSAdaptation:
    ucns_object: Any
    record: UCNSAdaptationRecord
    status: UCNSConsumerStatus


def _package_present() -> bool:
    try:
        return importlib.util.find_spec("ucns") is not None
    except (ImportError, AttributeError, ValueError):
        return False


def _validate_module(module: ModuleType) -> None:
    required = (
        "PRODUCER_EPOCH", "PROFILE_ID", "PROFILE_VERSION",
        "BRIDGE_SCHEMA_ID", "BRIDGE_SCHEMA_VERSION", "Cell", "make_carrier",
        "EdcmMetapatOrderedOccurrenceProfile", "EdcmMetapatBridgeRecord",
    )
    missing = [name for name in required if not hasattr(module, name)]
    if missing:
        raise UCNSAdapterError("UCNS exact-profile surface missing: " + ", ".join(missing))
    if str(module.PRODUCER_EPOCH) != SUPPORTED_PRODUCER_EPOCH:
        raise UCNSAdapterError("UCNS producer epoch mismatch")
    if (str(module.PROFILE_ID), str(module.PROFILE_VERSION)) != SUPPORTED_PROFILE:
        raise UCNSAdapterError("UCNS profile identity mismatch")
    if (str(module.BRIDGE_SCHEMA_ID), str(module.BRIDGE_SCHEMA_VERSION)) != SUPPORTED_BRIDGE_SCHEMA:
        raise UCNSAdapterError("UCNS bridge schema mismatch")


def require_ucns() -> ModuleType:
    try:
        module = importlib.import_module("ucns")
    except ModuleNotFoundError as exc:
        if exc.name != "ucns":
            raise
        raise UCNSDependencyError(RESET_BOUNDARY_REASON) from exc
    _validate_module(module)
    return module


def ucns_consumer_status() -> UCNSConsumerStatus:
    present = _package_present()
    if not present:
        return UCNSConsumerStatus(False, False, False, False, reason=RESET_BOUNDARY_REASON)
    try:
        require_ucns()
    except (UCNSDependencyError, UCNSAdapterError) as exc:
        return UCNSConsumerStatus(True, False, False, False, reason=str(exc))
    return UCNSConsumerStatus(True, True, True, True)


def suspended_envelope_record(envelope: MetapatModuleEnvelope) -> Mapping[str, Any]:
    """Return semantic provenance even when geometry is unavailable."""
    return {
        "source_statement_refs": tuple(envelope.source_statement_refs),
        "source_statements": tuple(envelope.source_statements),
        "canon_digest": envelope.canon_digest,
        "constraints": tuple(envelope.constraints),
        "permitted_interpretations": tuple(envelope.permitted_interpretations),
        "unresolved_constraints": tuple((*envelope.unresolved_constraints, RESET_BOUNDARY_REASON)),
        "semantic_mapping": "external-provenance",
    }


def adapt_envelope_to_ucns(envelope: MetapatModuleEnvelope, *, face_bits: Any = None) -> UCNSAdaptation:
    if not isinstance(envelope, MetapatModuleEnvelope):
        raise TypeError("envelope must be a MetapatModuleEnvelope")
    if face_bits is not None:
        raise UCNSAdapterError("face_bits belong to the archived adapter and are not accepted by this profile")
    module = require_ucns()
    cells = tuple(
        module.Cell(payload=None, provenance={"source_ref": ref})
        for ref in envelope.source_statement_refs
    )
    carrier = module.make_carrier(cells)
    profile = module.EdcmMetapatOrderedOccurrenceProfile()
    bound = profile.bind(carrier)
    bridge = profile.to_bridge(
        bound,
        source_commit=PINNED_UCNS_COMMIT,
        operator_history=("metapat-envelope-ordered-occurrence",),
    )
    encoded = bridge.to_json_bytes()
    decoded = module.EdcmMetapatBridgeRecord.from_json_bytes(encoded)
    if decoded != bridge:
        raise UCNSAdapterError("UCNS bridge round-trip mismatch")
    record = UCNSAdaptationRecord(
        adapter_schema=UCNS_ADAPTER_SCHEMA,
        adapter_version=UCNS_ADAPTER_VERSION,
        producer_epoch=SUPPORTED_PRODUCER_EPOCH,
        profile_id=SUPPORTED_PROFILE[0],
        profile_version=SUPPORTED_PROFILE[1],
        bridge_schema_id=SUPPORTED_BRIDGE_SCHEMA[0],
        bridge_schema_version=SUPPORTED_BRIDGE_SCHEMA[1],
        ucns_source_commit=PINNED_UCNS_COMMIT,
        ucns_stable_identity=bridge.stable_identity,
        ucns_bridge_json=encoded.decode("utf-8"),
        envelope_schema_id=envelope.schema_id,
        envelope_schema_version=envelope.schema_version,
        envelope_provenance_digest=envelope.provenance_digest,
        canon_version=envelope.canon_version,
        canon_digest=envelope.canon_digest,
        module_id=envelope.module_id,
        module_kind=envelope.module_kind,
        source_statement_refs=tuple(envelope.source_statement_refs),
        source_statements=tuple(envelope.source_statements),
        constraints=tuple(envelope.constraints),
        permitted_interpretations=tuple(envelope.permitted_interpretations),
        unresolved_constraints=tuple(envelope.unresolved_constraints),
    )
    return UCNSAdaptation(bound, record, UCNSConsumerStatus(True, True, True, True))


def root_spine_adaptation() -> UCNSAdaptation:
    return adapt_envelope_to_ucns(root_spine_module_envelope())


def root_spine_ucns() -> Any:
    return root_spine_adaptation().ucns_object


def compose(*objects: Any) -> None:
    del objects
    raise UCNSAdapterError("composition is not authorized by the ordered-occurrence profile")


__all__ = [
    "ADDRESSABLE_GONOL_VERTICES", "GONOL_VERTEX_COUNT", "PINNED_UCNS_COMMIT",
    "REJECTED_LEGACY_SCHEMAS", "RESET_BOUNDARY_REASON", "SPACE_ANCHOR_VERTEX",
    "SUPPORTED_BRIDGE_SCHEMA", "SUPPORTED_PRODUCER_EPOCH", "SUPPORTED_PROFILE",
    "UCNS_ADAPTER_SCHEMA", "UCNS_ADAPTER_VERSION", "UCNSAdapterError",
    "UCNSAdaptation", "UCNSAdaptationRecord", "UCNSConsumerStatus",
    "UCNSDependencyError", "adapt_envelope_to_ucns", "compose", "require_ucns",
    "root_spine_adaptation", "root_spine_ucns", "suspended_envelope_record",
    "ucns_consumer_status",
]
