"""Executable recursive-scale transition research.

This module formalizes mechanic 3 from the UCNS gonol research handoff. It
consumes closed affinization receipts from mechanic 2 and promotes a closed
whole into one atomic participant at a declared consuming scale. It does not
run successor validation and does not use successor observations.
"""

# === MODULE_BUILD ===
# id: ucns_recursive_scale_transition
#   module_name: recursive_scale_transition
#   module_kind: experiment
#   summary: defines stack-local executable promotion of closed affinization receipts into atomic participants at a declared next scale while preserving recoverable source structure
#   owner: The Interdependency
#   public_surface: AtomicParticipant, RecursiveScaleTransition, load_transition_authority, promote_closed_affinization, recover_constituent_references, sample_recursive_transition, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _stack_root, _canonical_bytes, _file_digest, _source_file_digests, _text, _atomic_identity, _producer_code_reference
#   auth_boundary: none; reads stack-pinned UCNS/METAPAT identities plus mechanics 1 and 2 only
#   storage_boundary: read stack-manifest.json, research/ucns/BASE.json, research/metapat/BASE.json, and research/ucns mechanic modules; no writes at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_recursive_scale_transition.py
#   rollout: stack-local research machinery; no successor experiment resumed until explicitly run later
#   rollback: remove this module, its tests, and its research report
#   requires: ucns_public_gonol_functional_operations, ucns_affinization_coupling_geometry, gonol-build construction discipline
#   since: 2026-09-02
#   unresolved: whether digest-bound atomic promotion is the selected UCNS recursive-scale law; exact next-scale carrier placement; direct coupling across non-adjacent scales; successor validation
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: recursive_scale_transition_binds_prior_mechanics
#   given: the recursive-scale transition layer is loaded
#   then: it binds pinned UCNS and METAPAT commits plus mechanic-1 and mechanic-2 receipt identities before promotion
#   class: safety
#   since: 2026-09-02
#
# id: recursive_scale_transition_promotes_closed_whole_only
#   given: a value is promoted across scale
#   then: promotion requires a closed affinization receipt with recoverable participants and intrinsic relation
#   class: correctness
#   since: 2026-09-02
#
# id: recursive_scale_transition_atomic_identity_is_deterministic
#   given: the same closed whole and target scale are promoted more than once
#   then: the atomic participant identity is stable while occurrence records remain separately addressable
#   class: correctness
#   since: 2026-09-02
#
# id: recursive_scale_transition_preserves_recoverable_constituents
#   given: a closed whole becomes atomic at the consuming scale
#   then: source whole id, source digest, source scale, target scale, coupling digest, and constituent references remain recoverable
#   class: doctrine
#   since: 2026-09-02
#
# id: recursive_scale_transition_receipts_are_deterministic
#   given: the same promotion is replayed
#   then: transition receipt bytes and digest replay byte-identically
#   class: evidence
#   since: 2026-09-02
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

import affinization_coupling_geometry as acg
import public_gonol_functional_operations as pgfo


SCHEMA = "the-interdependency.stack-research.ucns.recursive-scale-transition"
VERSION = "0.1.0"
STANDING = "stack-local-research-machinery"
SELECTION_EFFECT = "none"
PINNED_UCNS_COMMIT = "1975fe70cf4e0826a8020c2da3047569e277af64"
PINNED_METAPAT_COMMIT = "34d954aa1e2092e615b03a180500f6b6977f501e"

NONCLAIMS: tuple[str, ...] = (
    "not UCNS canon",
    "not METAPAT canon",
    "not a successor constructor",
    "not PCEA key research",
    "not evidence that digest size or geometry is entropy or hardness",
    "not cryptographic, replay-resistance, recovery, or public-authenticity evidence",
)

HMMM: tuple[str, ...] = (
    "whether digest-bound atomic promotion is the selected UCNS recursive-scale law remains unresolved",
    "exact next-scale carrier placement remains unresolved",
    "direct coupling across non-adjacent recursive scales remains unresolved",
    "successor validation remains paused until the three mechanics are reviewed as dependency-complete",
)

FALSIFICATION_CONDITIONS: tuple[str, ...] = (
    "pinned UCNS, METAPAT, mechanic-1, or mechanic-2 source identities change without refreshing this receipt",
    "promotion accepts a value without a closed affinization receipt",
    "promotion accepts a closed receipt whose participants are not recoverable",
    "promotion accepts a closed receipt whose relation is not intrinsic to the whole",
    "the same source whole and target scale produce different atomic identities under replay",
    "different target scales do not rotate atomic identity",
    "repeated occurrences collapse into one occurrence record",
    "source whole id, source digest, source scale, target scale, coupling digest, or constituent references are lost",
    "later UCNS authority supplies an incompatible recursive-scale transition law",
)

PROMOTION_EVIDENCE: tuple[str, ...] = (
    "UCNS research must decide whether digest-bound atomic promotion is sufficient or requires carrier-coordinate placement",
    "the transition must consume mechanic-2 closed receipts without modifying mechanics 1 or 2 after outcome inspection",
    "negative tests must keep rejecting unclosed, provenance-dropping, and non-intrinsic relation inputs",
    "only after review should the successor experiment be resumed with mechanics 1 through 3 frozen",
)


class RecursiveScaleTransitionError(ValueError):
    """Raised when recursive-scale transition violates this research contract."""


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


def _source_file_digests(root: Path) -> tuple[tuple[str, str], ...]:
    return tuple(
        _file_digest(root, path)
        for path in (
            "research/ucns/BASE.json",
            "research/metapat/BASE.json",
            "stack-manifest.json",
            "research/ucns/public_gonol_functional_operations.py",
            "research/ucns/affinization_coupling_geometry.py",
            "libs/ucns/CANON.md",
            "libs/metapat/UCNS_IMPLEMENTATION.md",
        )
    )


def _text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RecursiveScaleTransitionError(f"{field} must be non-empty text")
    return value


@dataclass(frozen=True, slots=True)
class TransitionAuthority:
    """Pinned authority identities required before recursive promotion."""

    ucns_base: dict[str, Any]
    metapat_base: dict[str, Any]
    mechanic1_receipt_sha256: str
    mechanic2_receipt_sha256: str
    source_file_digests: tuple[tuple[str, str], ...]
    stack_manifest_work_graph_sha256: str


@dataclass(frozen=True, slots=True)
class AtomicParticipant:
    """One closed whole as an atomic participant at a consuming scale."""

    atomic_id: str
    source_whole_id: str
    source_digest: str
    source_scale: str
    target_scale: str
    constituents_recoverable: bool
    coupling_digest: str

    def __post_init__(self) -> None:
        _text(self.atomic_id, "atomic_id")
        _text(self.source_whole_id, "source_whole_id")
        _text(self.source_digest, "source_digest")
        _text(self.source_scale, "source_scale")
        _text(self.target_scale, "target_scale")
        _text(self.coupling_digest, "coupling_digest")
        if self.constituents_recoverable is not True:
            raise RecursiveScaleTransitionError("constituents must remain recoverable")

    def to_payload(self) -> dict[str, Any]:
        return {
            "atomic_id": self.atomic_id,
            "source_whole_id": self.source_whole_id,
            "source_digest": self.source_digest,
            "source_scale": self.source_scale,
            "target_scale": self.target_scale,
            "constituents_recoverable": self.constituents_recoverable,
            "coupling_digest": self.coupling_digest,
        }


@dataclass(frozen=True, slots=True)
class RecursiveScaleTransition:
    """Occurrence-addressed promotion record for one atomic participant."""

    occurrence_id: str
    atomic_participant: AtomicParticipant
    source_constituents: tuple[dict[str, Any], ...]
    receipt: dict[str, Any]

    @property
    def digest(self) -> str:
        return sha256(_canonical_bytes(self.receipt)).hexdigest()


def load_transition_authority() -> TransitionAuthority:
    """Load pinned authority and prior mechanic receipts."""

    root = _stack_root()
    ucns_base = _load_json(root / "research" / "ucns" / "BASE.json")
    metapat_base = _load_json(root / "research" / "metapat" / "BASE.json")
    if ucns_base["source_commit"] != PINNED_UCNS_COMMIT:
        raise RecursiveScaleTransitionError("UCNS source commit mismatch")
    if metapat_base["source_commit"] != PINNED_METAPAT_COMMIT:
        raise RecursiveScaleTransitionError("METAPAT source commit mismatch")
    stack_manifest = _load_json(root / "stack-manifest.json")
    return TransitionAuthority(
        ucns_base=ucns_base,
        metapat_base=metapat_base,
        mechanic1_receipt_sha256=pgfo.receipt_digest(pgfo.receipt_payload()),
        mechanic2_receipt_sha256=acg.receipt_digest(acg.receipt_payload()),
        source_file_digests=_source_file_digests(root),
        stack_manifest_work_graph_sha256=stack_manifest["work_graph_sha256"],
    )


def _atomic_identity(
    *,
    source_whole_id: str,
    source_digest: str,
    source_scale: str,
    target_scale: str,
    coupling_digest: str,
) -> str:
    payload = {
        "source_whole_id": source_whole_id,
        "source_digest": source_digest,
        "source_scale": source_scale,
        "target_scale": target_scale,
        "coupling_digest": coupling_digest,
    }
    return "ucns.atomic:" + sha256(_canonical_bytes(payload)).hexdigest()


def _validate_closed_affinization(closed: acg.ClosedAffinization) -> None:
    if not isinstance(closed, acg.ClosedAffinization):
        raise RecursiveScaleTransitionError("promotion requires a ClosedAffinization")
    closure = closed.receipt.get("closure")
    if not isinstance(closure, dict):
        raise RecursiveScaleTransitionError("closed affinization receipt lacks closure block")
    if closure.get("participants_recoverable") is not True:
        raise RecursiveScaleTransitionError("closed affinization must preserve recoverable participants")
    if closure.get("relation_intrinsic_to_whole") is not True:
        raise RecursiveScaleTransitionError("closed affinization relation must be intrinsic to whole")
    if closed.receipt.get("whole_id") != closed.whole_id:
        raise RecursiveScaleTransitionError("closed affinization whole id mismatch")
    if closed.receipt.get("coupling", {}).get("coupling_digest") != closed.coupling.coupling_digest:
        raise RecursiveScaleTransitionError("closed affinization coupling digest mismatch")


def recover_constituent_references(
    transition: RecursiveScaleTransition,
) -> tuple[dict[str, Any], ...]:
    """Return source constituent references without reopening consuming-scale atom."""

    return transition.source_constituents


def promote_closed_affinization(
    closed: acg.ClosedAffinization,
    *,
    source_scale: str,
    target_scale: str,
    occurrence_id: str,
    authority: TransitionAuthority | None = None,
) -> RecursiveScaleTransition:
    """Promote one closed affinization to one atomic participant at target scale."""

    _validate_closed_affinization(closed)
    _text(source_scale, "source_scale")
    _text(target_scale, "target_scale")
    _text(occurrence_id, "occurrence_id")
    snapshot = authority or load_transition_authority()
    coupling_payload = closed.receipt["coupling"]
    constituents = tuple(coupling_payload["participants"])
    atomic = AtomicParticipant(
        atomic_id=_atomic_identity(
            source_whole_id=closed.whole_id,
            source_digest=closed.digest,
            source_scale=source_scale,
            target_scale=target_scale,
            coupling_digest=closed.coupling.coupling_digest,
        ),
        source_whole_id=closed.whole_id,
        source_digest=closed.digest,
        source_scale=source_scale,
        target_scale=target_scale,
        constituents_recoverable=True,
        coupling_digest=closed.coupling.coupling_digest,
    )
    receipt = {
        "schema": SCHEMA + ".transition",
        "version": VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "authority": {
            "ucns": snapshot.ucns_base,
            "metapat": snapshot.metapat_base,
            "mechanic1_receipt_sha256": snapshot.mechanic1_receipt_sha256,
            "mechanic2_receipt_sha256": snapshot.mechanic2_receipt_sha256,
            "stack_manifest_work_graph_sha256": snapshot.stack_manifest_work_graph_sha256,
            "source_file_digests": [
                {"path": path, "sha256": digest}
                for path, digest in snapshot.source_file_digests
            ],
        },
        "transition": {
            "operation": "closed-affinization-to-atomic-participant",
            "occurrence_id": occurrence_id,
            "source_scale": source_scale,
            "target_scale": target_scale,
            "atomic_at_consuming_scale": True,
            "reopen_constituents_by_default": False,
        },
        "atomic_participant": atomic.to_payload(),
        "source_constituents": list(constituents),
        "source_closed_affinization": {
            "whole_id": closed.whole_id,
            "digest": closed.digest,
            "coupling_digest": closed.coupling.coupling_digest,
        },
        "falsification_conditions": list(FALSIFICATION_CONDITIONS),
        "promotion_evidence": list(PROMOTION_EVIDENCE),
        "hmmm": list(HMMM),
        "nonclaims": list(NONCLAIMS),
    }
    return RecursiveScaleTransition(occurrence_id, atomic, constituents, receipt)


def sample_recursive_transition() -> RecursiveScaleTransition:
    """Build the deterministic mechanic-3 sample from mechanic-2 output."""

    closed = acg.sample_public_operation_affinization()
    return promote_closed_affinization(
        closed,
        source_scale="public-gonol-coupled-operation",
        target_scale="recursive-gonol-participant",
        occurrence_id="mechanic3.sample.closed-affinization.occurrence0",
    )


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def receipt_payload() -> dict[str, Any]:
    """Return the deterministic mechanic-3 research receipt."""

    authority = load_transition_authority()
    sample = sample_recursive_transition()
    return {
        "schema": SCHEMA,
        "version": VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "producer_code_reference": _producer_code_reference(),
        "source_identity": {
            "authority": {
                "ucns": "The-Interdependency/ucns",
                "metapat": "The-Interdependency/metapat",
            },
            "ucns_commit": authority.ucns_base["source_commit"],
            "metapat_commit": authority.metapat_base["source_commit"],
            "mechanic1_receipt_sha256": authority.mechanic1_receipt_sha256,
            "mechanic2_receipt_sha256": authority.mechanic2_receipt_sha256,
            "source_file_digests": [
                {"path": path, "sha256": digest}
                for path, digest in authority.source_file_digests
            ],
        },
        "mechanic": "recursive-scale transition",
        "definition": {
            "operation": "closed affinization receipt to atomic participant",
            "atomic_identity": "digest-bound source whole, source digest, source scale, target scale, and coupling digest",
            "occurrence": "separately addressable from stable atomic identity",
            "constituent_policy": "recoverable by receipt, not reopened by default at consuming scale",
            "successor_validation": "paused",
        },
        "sample_transition": {
            "digest": sample.digest,
            "receipt": sample.receipt,
        },
        "rejected_alternatives": [
            "promoting unclosed couplings",
            "dropping constituent provenance at atomic scale",
            "reopening constituents by default in the consuming construction",
            "collapsing repeated occurrences into one occurrence address",
            "using successor observations to tune atomic identity",
        ],
        "falsification_conditions": list(FALSIFICATION_CONDITIONS),
        "promotion_evidence": list(PROMOTION_EVIDENCE),
        "hmmm": list(HMMM),
        "nonclaims": list(NONCLAIMS),
        "next_dependency_complete_action": (
            "review mechanics 1 through 3 as a frozen dependency chain before "
            "resuming any successor validation experiment"
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
