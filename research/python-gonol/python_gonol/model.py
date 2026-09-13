"""Immutable records for bottom-up Python source gonol affixiation.

Usage guidance
--------------
Callers normally receive these records from :func:`affixiate_python_source` or
:func:`affixiate_python_bytes`.  A parent gonol contains only identity-bearing
references to already-closed children.  The receipt registry keeps every child
recoverable without reopening it during construction.
"""

# === MODULE_BUILD ===
# id: python_gonol_model
#   module_name: python_gonol.model
#   module_kind: schema
#   summary: defines immutable source spans, intrinsic affixiation relations, closed gonols, and deterministic Python affixiation receipts
#   owner: Python Gonol Construction (stack-local research)
#   public_surface: SourceSpan, RelationMember, AffixiationRelation, ClosedGonol, PythonAffixiationReceipt, canonical_json_bytes
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: immutable caller-owned values only
#   network_boundary: none
#   user_data_boundary: caller-supplied source remains inside the receipt
#   admin_only: false
#   tests: tests.test_affixiation
#   rollout: imported by the explicit Python 3.12 candidate constructor
#   rollback: remove the python-gonol research workspace before any downstream consumer binds its schema
#   requires: none
#   since: 2026-09-12
#   unresolved: independent release schema and migration policy remain hmmm
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: python_gonol_parent_references_closed_children
#   given: a non-letter gonol is present in a receipt
#   then: every constitutive member names an already-closed gonol by exact address and identity while the child remains independently recoverable
#   class: construction
#
# id: python_gonol_receipt_is_canonical_json
#   given: the same visible receipt payload is serialized repeatedly
#   then: sorted compact UTF-8 JSON bytes and the resulting SHA-256 identity are byte-identical
#   class: replay
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Mapping


def canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    """Return deterministic UTF-8 JSON bytes for identities and receipts."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


@dataclass(frozen=True, slots=True)
class SourceSpan:
    """Half-open decoded-source span with human-readable line coordinates."""

    start: int
    end: int
    start_line: int
    start_column: int
    end_line: int
    end_column: int

    def to_dict(self) -> dict[str, int]:
        return {
            "start": self.start,
            "end": self.end,
            "start_line": self.start_line,
            "start_column": self.start_column,
            "end_line": self.end_line,
            "end_column": self.end_column,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "SourceSpan":
        return cls(
            start=int(value["start"]),
            end=int(value["end"]),
            start_line=int(value["start_line"]),
            start_column=int(value["start_column"]),
            end_line=int(value["end_line"]),
            end_column=int(value["end_column"]),
        )


@dataclass(frozen=True, slots=True)
class RelationMember:
    """One ordered, role-bearing reference to an already-closed gonol."""

    ordinal: int
    role: str
    gonol_id: str
    address: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "ordinal": self.ordinal,
            "role": self.role,
            "gonol_id": self.gonol_id,
            "address": self.address,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "RelationMember":
        return cls(
            ordinal=int(value["ordinal"]),
            role=str(value["role"]),
            gonol_id=str(value["gonol_id"]),
            address=str(value["address"]),
        )


@dataclass(frozen=True, slots=True)
class AffixiationRelation:
    """The identity-bearing relation that makes one construction a whole."""

    kind: str
    members: tuple[RelationMember, ...]
    properties: tuple[tuple[str, str], ...]
    authority: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "members": [member.to_dict() for member in self.members],
            "properties": [list(pair) for pair in self.properties],
            "authority": self.authority,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "AffixiationRelation":
        return cls(
            kind=str(value["kind"]),
            members=tuple(RelationMember.from_dict(item) for item in value["members"]),
            properties=tuple((str(key), str(item)) for key, item in value["properties"]),
            authority=str(value["authority"]),
        )


@dataclass(frozen=True, slots=True)
class ClosedGonol:
    """One closed gonol; parents consume its identity, never flattened descendants."""

    address: str
    scale: str
    span: SourceSpan
    relation: AffixiationRelation
    provenance: tuple[tuple[str, str], ...]
    hmmm: tuple[str, ...]
    gonol_id: str

    def identity_payload(self) -> dict[str, Any]:
        return {
            "address": self.address,
            "scale": self.scale,
            "span": self.span.to_dict(),
            "relation": self.relation.to_dict(),
            "provenance": [list(pair) for pair in self.provenance],
            "hmmm": list(self.hmmm),
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self.identity_payload(), "gonol_id": self.gonol_id}

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ClosedGonol":
        return cls(
            address=str(value["address"]),
            scale=str(value["scale"]),
            span=SourceSpan.from_dict(value["span"]),
            relation=AffixiationRelation.from_dict(value["relation"]),
            provenance=tuple((str(key), str(item)) for key, item in value["provenance"]),
            hmmm=tuple(str(item) for item in value["hmmm"]),
            gonol_id=str(value["gonol_id"]),
        )


@dataclass(frozen=True, slots=True)
class PythonAffixiationReceipt:
    """Complete visible registry and provenance for one source construction."""

    schema: str
    version: str
    constructor_id: str
    constructor_version: str
    language_profile: str
    source_id: str
    encoding: str
    source_bytes_base64: str
    source_bytes_sha256: str
    decoded_source_sha256: str
    recognition_witness: str
    standing: str
    selection_effect: str
    root_gonol_id: str
    gonols: tuple[ClosedGonol, ...]
    nonclaims: tuple[str, ...]
    hmmm: tuple[str, ...]
    receipt_digest: str

    def payload(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "version": self.version,
            "constructor_id": self.constructor_id,
            "constructor_version": self.constructor_version,
            "language_profile": self.language_profile,
            "source_id": self.source_id,
            "encoding": self.encoding,
            "source_bytes_base64": self.source_bytes_base64,
            "source_bytes_sha256": self.source_bytes_sha256,
            "decoded_source_sha256": self.decoded_source_sha256,
            "recognition_witness": self.recognition_witness,
            "standing": self.standing,
            "selection_effect": self.selection_effect,
            "root_gonol_id": self.root_gonol_id,
            "gonols": [gonol.to_dict() for gonol in self.gonols],
            "nonclaims": list(self.nonclaims),
            "hmmm": list(self.hmmm),
        }

    def to_dict(self) -> dict[str, Any]:
        return {**self.payload(), "receipt_digest": self.receipt_digest}

    def to_json(self, *, pretty: bool = False) -> str:
        if pretty:
            return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        return canonical_json_bytes(self.to_dict()).decode("utf-8") + "\n"

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "PythonAffixiationReceipt":
        return cls(
            schema=str(value["schema"]),
            version=str(value["version"]),
            constructor_id=str(value["constructor_id"]),
            constructor_version=str(value["constructor_version"]),
            language_profile=str(value["language_profile"]),
            source_id=str(value["source_id"]),
            encoding=str(value["encoding"]),
            source_bytes_base64=str(value["source_bytes_base64"]),
            source_bytes_sha256=str(value["source_bytes_sha256"]),
            decoded_source_sha256=str(value["decoded_source_sha256"]),
            recognition_witness=str(value["recognition_witness"]),
            standing=str(value["standing"]),
            selection_effect=str(value["selection_effect"]),
            root_gonol_id=str(value["root_gonol_id"]),
            gonols=tuple(ClosedGonol.from_dict(item) for item in value["gonols"]),
            nonclaims=tuple(str(item) for item in value["nonclaims"]),
            hmmm=tuple(str(item) for item in value["hmmm"]),
            receipt_digest=str(value["receipt_digest"]),
        )

    @classmethod
    def from_json(cls, source: str) -> "PythonAffixiationReceipt":
        value = json.loads(source)
        if not isinstance(value, dict):
            raise TypeError("receipt JSON must contain one object")
        return cls.from_dict(value)


__all__ = [
    "AffixiationRelation",
    "ClosedGonol",
    "PythonAffixiationReceipt",
    "RelationMember",
    "SourceSpan",
    "canonical_json_bytes",
]
