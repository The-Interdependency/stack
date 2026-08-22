"""Canon-bound authorization for semantic UCNS payload forks.

METAPAT may authorize a payload fork only when ordered children are simultaneous
constitutive components of one parent. UCNS owns geometry; downstream EDCM must
verify the authorization against the encoded topology. With no authorization,
semantic mapping remains external provenance.

Usage::

    authorization = authorize_constitutive_fork(
        envelope,
        child_module_ids=("metapat.child.alpha", "metapat.child.beta"),
        source_statement_refs=(envelope.source_statement_refs[0],),
    )
    wire_record = authorization.to_dict()

Temporal succession, adjacency, provenance, alternatives, fiq connectivity,
and external symmetry actions are not payload containment.
"""

# === MODULE_BUILD ===
# id: metapat_ucns_phi_policy
#   module_name: ucns_phi
#   module_kind: schema
#   summary: issues strict canon-bound constitutive-simultaneous authorization records before semantic UCNS payload forks
#   owner: The Interdependency
#   public_surface: UCNSPhiPolicy, UCNSForkAuthorization, ForkAuthorizationError, DEFAULT_UCNS_PHI_POLICY, authorize_constitutive_fork, validate_fork_authorization, PHI_POLICY_SCHEMA_ID, PHI_POLICY_VERSION, FORK_AUTHORIZATION_SCHEMA_ID, FORK_AUTHORIZATION_SCHEMA_VERSION, CONSTITUTIVE_RELATION_KIND, PROHIBITED_FORK_RELATION_KINDS
#   internal_surface: _canonical_json, _strings, _payload, _digest
#   auth_boundary: none
#   storage_boundary: serialization-only
#   network_boundary: none
#   user_data_boundary: METAPAT module identities and source references remain semantic provenance; no transcript or measurement values
#   admin_only: false
#   tests: tests.test_ucns_phi
#   rollout: additive_semantic_authority_surface
#   rollback: remove exports and consumers; external-provenance UCNS adaptation remains unchanged
#   requires: metapat_module_envelope
#   since: 2026-07-15
#   unresolved: downstream EDCM must bind authorizations to actual UCNS payload topology
# === END MODULE_BUILD ===

# === DOCS ===
# id: metapat_ucns_phi_docs
#   summary: documents constitutive-fork authorization and downstream fail-closed enforcement
#   audience: developer
#   source: docs/ucns-phi-policy.md
#   covers: UCNSPhiPolicy, UCNSForkAuthorization, authorize_constitutive_fork, validate_fork_authorization
#   status: current
# === END DOCS ===

# === CAPABILITIES ===
# id: metapat_constitutive_fork_authority
#   summary: authorizes ordered simultaneous constitutive children of one METAPAT parent
#   exposes: metapat.authorize_constitutive_fork
#   inputs: MetapatModuleEnvelope, ordered child ids, source references, unresolved constraints
#   outputs: UCNSForkAuthorization
#   boundaries: auth:none, storage:serialization-only, network:none, user_data:semantic provenance only
# === END CAPABILITIES ===

# === BOUNDARIES ===
# id: metapat_ucns_phi_boundary
#   summary: METAPAT authorizes meaning but does not construct UCNS algebra, validate topology, or transfer proof/measurement status
#   auth_boundary: none
#   storage_boundary: serialization-only
#   network_boundary: none
#   user_data_boundary: semantic module identities and canon references only
#   admin_only: false
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: metapat_phi_default_external_provenance
#   given: the default Phi policy is inspected
#   then: mapping remains external-provenance and forks require explicit authorization
#   class: boundary_contract
#
# id: metapat_phi_fork_requires_explicit_authorization
#   given: a fork is authorized from a canonical envelope
#   then: parent, ordered children, canon, policy, and source references are digest-bound
#   class: provenance_contract
#
# id: metapat_phi_constitutive_relation_only
#   given: an authorization is constructed or decoded
#   then: relation_kind equals constitutive-simultaneous exactly
#   class: safety
#
# id: metapat_phi_authorization_binds_canon_and_order
#   given: authorization is checked against an envelope and child order
#   then: canon, parent, order, references, and policy match exactly
#   class: integration_contract
#
# id: metapat_phi_negative_relations_rejected
#   given: time, adjacency, provenance, alternatives, fiq connectivity, or external action is presented as containment
#   then: authorization fails closed
#   class: safety
#
# id: metapat_phi_record_roundtrip
#   given: authorization is serialized and reconstructed
#   then: fields and digest survive while malformed or tampered records fail closed
#   class: schema_contract
#
# id: metapat_phi_no_status_transfer
#   given: any Phi policy or authorization
#   then: theorem_status_transfer and metapat_validity_claim remain false
#   class: boundary_contract
# === END CONTRACTS ===

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from .envelope import MetapatModuleEnvelope

PHI_POLICY_SCHEMA_ID = "metapat.ucns-phi-policy"
PHI_POLICY_VERSION = "1.0.0"
FORK_AUTHORIZATION_SCHEMA_ID = "metapat.ucns-fork-authorization"
FORK_AUTHORIZATION_SCHEMA_VERSION = "1.0.0"
CONSTITUTIVE_RELATION_KIND = "constitutive-simultaneous"
PROHIBITED_FORK_RELATION_KINDS = (
    "temporal-successor",
    "adjacency",
    "provenance",
    "alternative",
    "fiq-connectivity",
    "external-symmetry-action",
    "arbitrary-association",
)


class ForkAuthorizationError(ValueError):
    """Raised when semantic payload-fork authorization fails closed."""


def _canonical_json(value: Mapping[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _strings(value: Any, name: str, *, minimum: int = 0) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)):
        raise ForkAuthorizationError(f"{name} must be an array of strings")
    result = tuple(value)
    if len(result) < minimum:
        raise ForkAuthorizationError(f"{name} must contain at least {minimum} entries")
    if any(not isinstance(item, str) or not item.strip() for item in result):
        raise ForkAuthorizationError(f"{name} must contain only non-empty strings")
    return result


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ForkAuthorizationError(f"{name} must be a non-empty string")
    return value


@dataclass(frozen=True, slots=True)
class UCNSPhiPolicy:
    schema_id: str = PHI_POLICY_SCHEMA_ID
    schema_version: str = PHI_POLICY_VERSION
    default_semantic_mapping: str = "external-provenance"
    fork_mode: str = "explicit-authorization-only"
    allowed_relation_kind: str = CONSTITUTIVE_RELATION_KIND
    theorem_status_transfer: bool = False
    metapat_validity_claim: bool = False

    def __post_init__(self) -> None:
        expected = (
            (self.schema_id, PHI_POLICY_SCHEMA_ID, "schema_id"),
            (self.schema_version, PHI_POLICY_VERSION, "schema_version"),
            (self.default_semantic_mapping, "external-provenance", "default_semantic_mapping"),
            (self.fork_mode, "explicit-authorization-only", "fork_mode"),
            (self.allowed_relation_kind, CONSTITUTIVE_RELATION_KIND, "allowed_relation_kind"),
        )
        for observed, required, name in expected:
            if observed != required:
                raise ForkAuthorizationError(f"{name} must remain {required}")
        if self.theorem_status_transfer is not False or self.metapat_validity_claim is not False:
            raise ForkAuthorizationError("Phi policy status-transfer fields must be false")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "default_semantic_mapping": self.default_semantic_mapping,
            "fork_mode": self.fork_mode,
            "allowed_relation_kind": self.allowed_relation_kind,
            "theorem_status_transfer": self.theorem_status_transfer,
            "metapat_validity_claim": self.metapat_validity_claim,
        }


DEFAULT_UCNS_PHI_POLICY = UCNSPhiPolicy()


def _payload(
    *,
    parent_module_id: str,
    child_module_ids: tuple[str, ...],
    source_statement_refs: tuple[str, ...],
    canon_digest: str,
    unresolved_constraints: tuple[str, ...],
) -> dict[str, Any]:
    return {
        "schema_id": FORK_AUTHORIZATION_SCHEMA_ID,
        "schema_version": FORK_AUTHORIZATION_SCHEMA_VERSION,
        "parent_module_id": parent_module_id,
        "child_module_ids": list(child_module_ids),
        "relation_kind": CONSTITUTIVE_RELATION_KIND,
        "source_statement_refs": list(source_statement_refs),
        "encoding_policy_version": PHI_POLICY_VERSION,
        "canon_digest": canon_digest,
        "unresolved_constraints": list(unresolved_constraints),
        "theorem_status_transfer": False,
        "metapat_validity_claim": False,
    }


def _digest(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class UCNSForkAuthorization:
    schema_id: str
    schema_version: str
    parent_module_id: str
    child_module_ids: tuple[str, ...]
    relation_kind: str
    source_statement_refs: tuple[str, ...]
    encoding_policy_version: str
    canon_digest: str
    unresolved_constraints: tuple[str, ...]
    theorem_status_transfer: bool
    metapat_validity_claim: bool
    authorization_digest: str

    def __post_init__(self) -> None:
        if self.schema_id != FORK_AUTHORIZATION_SCHEMA_ID:
            raise ForkAuthorizationError(f"unsupported fork schema_id {self.schema_id!r}")
        if self.schema_version != FORK_AUTHORIZATION_SCHEMA_VERSION:
            raise ForkAuthorizationError(f"unsupported fork schema_version {self.schema_version!r}")
        _text(self.parent_module_id, "parent_module_id")
        children = _strings(self.child_module_ids, "child_module_ids", minimum=2)
        if len(set(children)) != len(children):
            raise ForkAuthorizationError("child_module_ids must be unique and ordered")
        if self.relation_kind != CONSTITUTIVE_RELATION_KIND:
            raise ForkAuthorizationError("relation_kind must be constitutive-simultaneous")
        _strings(self.source_statement_refs, "source_statement_refs", minimum=1)
        if self.encoding_policy_version != PHI_POLICY_VERSION:
            raise ForkAuthorizationError(f"encoding_policy_version must be {PHI_POLICY_VERSION}")
        _text(self.canon_digest, "canon_digest")
        _strings(self.unresolved_constraints, "unresolved_constraints")
        if self.theorem_status_transfer is not False or self.metapat_validity_claim is not False:
            raise ForkAuthorizationError("authorization status-transfer fields must be false")
        if self.authorization_digest != _digest(self._payload()):
            raise ForkAuthorizationError("authorization_digest mismatch")

    def _payload(self) -> dict[str, Any]:
        return _payload(
            parent_module_id=self.parent_module_id,
            child_module_ids=self.child_module_ids,
            source_statement_refs=self.source_statement_refs,
            canon_digest=self.canon_digest,
            unresolved_constraints=self.unresolved_constraints,
        )

    def to_dict(self) -> dict[str, Any]:
        return {**self._payload(), "authorization_digest": self.authorization_digest}

    def to_json(self) -> str:
        return _canonical_json(self.to_dict())

    @classmethod
    def create(
        cls,
        *,
        envelope: MetapatModuleEnvelope,
        child_module_ids: Iterable[str],
        source_statement_refs: Iterable[str],
        unresolved_constraints: Iterable[str] = (),
    ) -> "UCNSForkAuthorization":
        if not isinstance(envelope, MetapatModuleEnvelope):
            raise TypeError("envelope must be a MetapatModuleEnvelope")
        children = _strings(tuple(child_module_ids), "child_module_ids", minimum=2)
        refs = _strings(tuple(source_statement_refs), "source_statement_refs", minimum=1)
        unresolved = _strings(tuple(unresolved_constraints), "unresolved_constraints")
        if any(ref not in envelope.source_statement_refs for ref in refs):
            raise ForkAuthorizationError("source_statement_refs must resolve in the envelope")
        payload = _payload(
            parent_module_id=envelope.module_id,
            child_module_ids=children,
            source_statement_refs=refs,
            canon_digest=envelope.canon_digest,
            unresolved_constraints=unresolved,
        )
        return cls(
            child_module_ids=children,
            source_statement_refs=refs,
            unresolved_constraints=unresolved,
            authorization_digest=_digest(payload),
            **{key: payload[key] for key in (
                "schema_id", "schema_version", "parent_module_id", "relation_kind",
                "encoding_policy_version", "canon_digest", "theorem_status_transfer",
                "metapat_validity_claim",
            )},
        )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "UCNSForkAuthorization":
        if not isinstance(data, Mapping):
            raise ForkAuthorizationError("fork authorization must be a mapping")
        expected = {
            "schema_id", "schema_version", "parent_module_id", "child_module_ids",
            "relation_kind", "source_statement_refs", "encoding_policy_version",
            "canon_digest", "unresolved_constraints", "theorem_status_transfer",
            "metapat_validity_claim", "authorization_digest",
        }
        unknown, missing = set(data) - expected, expected - set(data)
        if unknown:
            raise ForkAuthorizationError(f"unknown fork authorization fields: {sorted(unknown)!r}")
        if missing:
            raise ForkAuthorizationError(f"missing fork authorization fields: {sorted(missing)!r}")
        if not isinstance(data["theorem_status_transfer"], bool) or not isinstance(data["metapat_validity_claim"], bool):
            raise ForkAuthorizationError("status-transfer fields must be boolean")
        return cls(
            schema_id=_text(data["schema_id"], "schema_id"),
            schema_version=_text(data["schema_version"], "schema_version"),
            parent_module_id=_text(data["parent_module_id"], "parent_module_id"),
            child_module_ids=_strings(data["child_module_ids"], "child_module_ids", minimum=2),
            relation_kind=_text(data["relation_kind"], "relation_kind"),
            source_statement_refs=_strings(data["source_statement_refs"], "source_statement_refs", minimum=1),
            encoding_policy_version=_text(data["encoding_policy_version"], "encoding_policy_version"),
            canon_digest=_text(data["canon_digest"], "canon_digest"),
            unresolved_constraints=_strings(data["unresolved_constraints"], "unresolved_constraints"),
            theorem_status_transfer=data["theorem_status_transfer"],
            metapat_validity_claim=data["metapat_validity_claim"],
            authorization_digest=_text(data["authorization_digest"], "authorization_digest"),
        )

    @classmethod
    def from_json(cls, value: str) -> "UCNSForkAuthorization":
        if not isinstance(value, str):
            raise ForkAuthorizationError("fork authorization JSON must be a string")
        decoded = json.loads(value)
        if not isinstance(decoded, dict):
            raise ForkAuthorizationError("fork authorization JSON must decode to an object")
        return cls.from_dict(decoded)


def validate_fork_authorization(
    authorization: UCNSForkAuthorization,
    *,
    envelope: MetapatModuleEnvelope,
    child_module_ids: Iterable[str],
    policy: UCNSPhiPolicy = DEFAULT_UCNS_PHI_POLICY,
) -> UCNSForkAuthorization:
    """Fail closed unless authorization matches exact canon and child order."""

    if not isinstance(policy, UCNSPhiPolicy):
        raise TypeError("policy must be a UCNSPhiPolicy")
    if not isinstance(authorization, UCNSForkAuthorization):
        raise TypeError("authorization must be a UCNSForkAuthorization")
    if not isinstance(envelope, MetapatModuleEnvelope):
        raise TypeError("envelope must be a MetapatModuleEnvelope")
    children = _strings(tuple(child_module_ids), "child_module_ids", minimum=2)
    checks = (
        (authorization.parent_module_id, envelope.module_id, "parent_module_id"),
        (authorization.child_module_ids, children, "child order"),
        (authorization.canon_digest, envelope.canon_digest, "canon_digest"),
        (authorization.encoding_policy_version, policy.schema_version, "policy version"),
        (authorization.relation_kind, policy.allowed_relation_kind, "relation kind"),
    )
    for observed, expected, name in checks:
        if observed != expected:
            raise ForkAuthorizationError(f"authorization {name} mismatch")
    if any(ref not in envelope.source_statement_refs for ref in authorization.source_statement_refs):
        raise ForkAuthorizationError("authorization source statement no longer resolves")
    return authorization


def authorize_constitutive_fork(
    envelope: MetapatModuleEnvelope,
    *,
    child_module_ids: Iterable[str],
    source_statement_refs: Iterable[str],
    unresolved_constraints: Iterable[str] = (),
) -> UCNSForkAuthorization:
    """Create and self-validate one canon-bound constitutive authorization."""

    authorization = UCNSForkAuthorization.create(
        envelope=envelope,
        child_module_ids=child_module_ids,
        source_statement_refs=source_statement_refs,
        unresolved_constraints=unresolved_constraints,
    )
    return validate_fork_authorization(
        authorization,
        envelope=envelope,
        child_module_ids=authorization.child_module_ids,
    )


__all__ = [
    "CONSTITUTIVE_RELATION_KIND", "DEFAULT_UCNS_PHI_POLICY",
    "FORK_AUTHORIZATION_SCHEMA_ID", "FORK_AUTHORIZATION_SCHEMA_VERSION",
    "ForkAuthorizationError", "PHI_POLICY_SCHEMA_ID", "PHI_POLICY_VERSION",
    "PROHIBITED_FORK_RELATION_KINDS", "UCNSForkAuthorization", "UCNSPhiPolicy",
    "authorize_constitutive_fork", "validate_fork_authorization",
]
