"""Declared inactive protocol for exact post-reset UCNS profile consumption."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class UCNSProfileIdentity:
    producer_epoch: str
    profile_id: str
    profile_version: str
    bridge_schema_id: str
    bridge_schema_version: str
    source_commit: str
    package_identity: str
    option_set: tuple[tuple[str, str], ...]
    stable_object_identity: str
    theorem_transfer: bool = False
    measurement_validity: bool = False
    metapat_validity: bool = False

    def __post_init__(self) -> None:
        required = (
            self.producer_epoch,
            self.profile_id,
            self.profile_version,
            self.bridge_schema_id,
            self.bridge_schema_version,
            self.source_commit,
            self.package_identity,
            self.stable_object_identity,
        )
        if any(not isinstance(value, str) or not value.strip() for value in required):
            raise ValueError("all UCNS profile identity fields must be exact non-empty strings")
        if not self.option_set:
            raise ValueError("complete option_set declaration is required")
        if self.theorem_transfer or self.measurement_validity or self.metapat_validity:
            raise ValueError("all transfer and validity flags must remain false")


@dataclass(frozen=True, slots=True)
class OrderedOccurrenceRequest:
    identity: UCNSProfileIdentity
    source_refs: tuple[str, ...]
    occurrence_ids: tuple[str, ...]
    option_set: tuple[tuple[str, str], ...]
    semantic_payload_authorized: bool = False

    def __post_init__(self) -> None:
        if len(self.source_refs) != len(self.occurrence_ids):
            raise ValueError("one occurrence ID is required for each ordered source statement")
        if self.option_set != self.identity.option_set:
            raise ValueError("request option_set must exactly match the pinned profile identity")
        if self.semantic_payload_authorized:
            raise ValueError("semantic text payload placement is not authorized")


def validate_exact_identity(actual: Mapping[str, Any], expected: UCNSProfileIdentity) -> None:
    required = {
        "producer_epoch": expected.producer_epoch,
        "profile_id": expected.profile_id,
        "profile_version": expected.profile_version,
        "bridge_schema_id": expected.bridge_schema_id,
        "bridge_schema_version": expected.bridge_schema_version,
        "source_commit": expected.source_commit,
        "package_identity": expected.package_identity,
        "option_set": list(expected.option_set),
        "stable_object_identity": expected.stable_object_identity,
        "theorem_transfer": False,
        "measurement_validity": False,
        "metapat_validity": False,
    }
    for key, value in required.items():
        if actual.get(key) != value:
            raise ValueError(f"UCNS profile identity mismatch for {key}; fail closed")
