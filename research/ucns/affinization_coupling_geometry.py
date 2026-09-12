"""Executable affinization/coupling geometry research.

This module formalizes mechanic 2 from the UCNS gonol research handoff. It
consumes closed Public Gonol operations from mechanic 1 and defines an explicit
ordered incidence-coupling candidate with deterministic closure receipts. It
does not run gonol successor validation and does not infer coupling from
overlap, adjacency, glyph meaning, or ambient membership.
"""

# === MODULE_BUILD ===
# id: ucns_affinization_coupling_geometry
#   module_name: affinization_coupling_geometry
#   module_kind: experiment
#   summary: defines stack-local executable ordered coupling geometry for closed gonols or constituent relations while preserving participant identity, provenance, degree, and fail-closed relation boundaries
#   owner: The Interdependency
#   public_surface: CouplingParticipant, OrientedCoupling, DegreeEntry, ClosedAffinization, load_authority_snapshot, coupling, degree_ledger, close_affinization, sample_public_operation_affinization, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _stack_root, _canonical_bytes, _file_digest, _source_file_digests, _load_metapat_phi, _text, _participant_payload, _coupling_payload, _producer_code_reference
#   auth_boundary: none; reads stack-pinned UCNS and METAPAT authority files only
#   storage_boundary: read stack-manifest.json, research/ucns/BASE.json, research/metapat/BASE.json, libs/metapat source files, libs/ucns authority files, and mechanic-1 research module; no writes at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_affinization_coupling_geometry.py
#   rollout: stack-local research machinery; no UCNS canon, METAPAT canon, stack libs, or PCEA promotion
#   rollback: remove this module, its tests, and its research report
#   requires: ucns_public_gonol_functional_operations, metapat_ucns_phi_policy, gonol-build construction discipline
#   since: 2026-09-02
#   unresolved: exact coordinate embedding of coupling on the UCNS carrier; whether this incidence geometry is sufficient for recursive-scale transition; direct coupling across distant scales
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: affinization_coupling_binds_ucns_and_metapat_authority
#   given: the coupling layer is loaded
#   then: it binds pinned UCNS and METAPAT commits, METAPAT Phi relation policy, source file digests, and mechanic-1 receipt identity
#   class: safety
#   since: 2026-09-02
#
# id: affinization_coupling_requires_explicit_ordered_relation
#   given: a coupling is constructed
#   then: it requires an explicit ordered participant tuple and rejects prohibited relation kinds, duplicate occurrence ids, and inferred overlap closure
#   class: doctrine
#   since: 2026-09-02
#
# id: affinization_coupling_preserves_participant_provenance
#   given: a coupling is closed as an affinization
#   then: every participant id, scale, role, source digest, slot, and coupling digest remains recoverable from the closed receipt
#   class: correctness
#   since: 2026-09-02
#
# id: affinization_coupling_degree_is_slot_sensitive
#   given: declared couplings share participants
#   then: degree records incidence count and slot-specific incidence without treating reversed order as identical
#   class: correctness
#   since: 2026-09-02
#
# id: affinization_coupling_closure_receipts_are_deterministic
#   given: the same ordered coupling is closed twice
#   then: closure payload and digest replay byte-identically
#   class: evidence
#   since: 2026-09-02
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import importlib
import json
from pathlib import Path
import sys
from typing import Any

import public_gonol_functional_operations as pgfo


SCHEMA = "the-interdependency.stack-research.ucns.affinization-coupling-geometry"
VERSION = "0.1.0"
STANDING = "stack-local-research-machinery"
SELECTION_EFFECT = "none"
PINNED_UCNS_COMMIT = "1975fe70cf4e0826a8020c2da3047569e277af64"
PINNED_METAPAT_COMMIT = "34d954aa1e2092e615b03a180500f6b6977f501e"
RELATION_KIND = "constitutive-simultaneous"

COUPLING_BASES = frozenset({
    "declared_ordered_incidence",
    "mechanic1_closed_operation_pair",
})

NONCLAIMS: tuple[str, ...] = (
    "not UCNS canon",
    "not METAPAT canon",
    "not a coordinate embedding of the full UCNS coupling law",
    "not a successor constructor",
    "not PCEA key research",
    "not theorem, ontology, measurement, or proof-status transfer",
    "not cryptographic, entropy, hardness, or public-authenticity evidence",
)

HMMM: tuple[str, ...] = (
    "exact coordinate embedding of coupling on the UCNS carrier remains unresolved",
    "whether ordered incidence is sufficient geometry for recursive-scale transition remains unresolved",
    "direct coupling across distant scales remains unresolved",
    "how completed affinization receipts become Public Gonol participants remains unresolved until mechanic 3",
)

FALSIFICATION_CONDITIONS: tuple[str, ...] = (
    "pinned UCNS, METAPAT, or mechanic-1 source identities change without refreshing this receipt",
    "a coupling is accepted without an explicit ordered participant tuple",
    "a prohibited relation kind is accepted as constitutive coupling",
    "duplicate participant occurrence ids are accepted inside one coupling",
    "overlap, adjacency, ambient membership, or provenance alone creates a coupling",
    "reversing participant order leaves the coupling digest unchanged",
    "degree fails to retain slot-specific incidence",
    "closure receipts are not byte-identical under deterministic replay",
    "closed receipts fail to preserve participant identity, scale, role, source digest, slot, and coupling digest",
    "later UCNS authority requires a coordinate coupling law incompatible with this incidence candidate",
)

PROMOTION_EVIDENCE: tuple[str, ...] = (
    "UCNS research must bind this incidence layer to an explicit coordinate or topological coupling realization",
    "METAPAT constitutive relation authorization must remain exact and status-transfer fields must remain false",
    "negative tests must keep rejecting prohibited relation kinds and overlap-derived closure",
    "mechanic 3 must consume the closed affinization receipt without changing mechanic 2 after outcome inspection",
)


class CouplingGeometryError(ValueError):
    """Raised when coupling geometry violates this research contract."""


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
            "libs/ucns/CANON.md",
            "libs/ucns/docs/GEOMETRY.md",
            "libs/metapat/README.md",
            "libs/metapat/UCNS_IMPLEMENTATION.md",
            "libs/metapat/src/metapat/ucns_phi.py",
            "research/ucns/public_gonol_functional_operations.py",
        )
    )


def _load_metapat_phi() -> Any:
    metapat_src = _stack_root() / "libs" / "metapat" / "src"
    if str(metapat_src) not in sys.path:
        sys.path.insert(0, str(metapat_src))
    return importlib.import_module("metapat.ucns_phi")


def _text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CouplingGeometryError(f"{field} must be non-empty text")
    return value


@dataclass(frozen=True, slots=True)
class AuthoritySnapshot:
    """Pinned UCNS, METAPAT, and mechanic-1 identities."""

    ucns_base: dict[str, Any]
    metapat_base: dict[str, Any]
    metapat_phi_policy: dict[str, Any]
    metapat_prohibited_relation_kinds: tuple[str, ...]
    mechanic1_receipt_sha256: str
    source_file_digests: tuple[tuple[str, str], ...]
    stack_manifest_work_graph_sha256: str


@dataclass(frozen=True, slots=True)
class CouplingParticipant:
    """One occurrence-addressed participant in an ordered coupling."""

    participant_id: str
    scale: str
    role: str
    source_digest: str

    def __post_init__(self) -> None:
        _text(self.participant_id, "participant_id")
        _text(self.scale, "scale")
        _text(self.role, "role")
        _text(self.source_digest, "source_digest")


@dataclass(frozen=True, slots=True)
class OrientedCoupling:
    """One explicitly declared ordered coupling."""

    coupling_id: str
    participants: tuple[CouplingParticipant, ...]
    relation_kind: str
    basis: str
    source_refs: tuple[str, ...]
    unresolved_constraints: tuple[str, ...] = HMMM

    def __post_init__(self) -> None:
        _text(self.coupling_id, "coupling_id")
        if self.basis not in COUPLING_BASES:
            raise CouplingGeometryError("coupling basis is not admitted")
        if self.relation_kind != RELATION_KIND:
            raise CouplingGeometryError("only constitutive-simultaneous relation kind is admitted")
        if len(self.participants) < 2:
            raise CouplingGeometryError("a coupling requires at least two ordered participants")
        ids = tuple(participant.participant_id for participant in self.participants)
        if len(set(ids)) != len(ids):
            raise CouplingGeometryError("participant occurrence ids must be unique within a coupling")
        if not self.source_refs or any(not isinstance(item, str) or not item.strip() for item in self.source_refs):
            raise CouplingGeometryError("coupling source refs are required")
        if any(not isinstance(item, str) or not item.strip() for item in self.unresolved_constraints):
            raise CouplingGeometryError("unresolved constraints must be explicit text")

    @property
    def arity(self) -> int:
        return len(self.participants)

    def payload_without_digest(self) -> dict[str, Any]:
        return {
            "coupling_id": self.coupling_id,
            "relation_kind": self.relation_kind,
            "basis": self.basis,
            "arity": self.arity,
            "participants": [
                _participant_payload(participant, slot)
                for slot, participant in enumerate(self.participants)
            ],
            "source_refs": list(self.source_refs),
            "unresolved_constraints": list(self.unresolved_constraints),
            "theorem_status_transfer": False,
            "metapat_validity_claim": False,
            "measurement_status_transfer": False,
        }

    @property
    def coupling_digest(self) -> str:
        return sha256(_canonical_bytes(self.payload_without_digest())).hexdigest()

    def to_payload(self) -> dict[str, Any]:
        return {**self.payload_without_digest(), "coupling_digest": self.coupling_digest}


@dataclass(frozen=True, slots=True)
class DegreeEntry:
    """Slot-sensitive incidence degree for one participant."""

    participant_id: str
    degree: int
    slot_degrees: tuple[tuple[int, int], ...]
    coupling_ids: tuple[str, ...]

    def to_payload(self) -> dict[str, Any]:
        return {
            "participant_id": self.participant_id,
            "degree": self.degree,
            "slot_degrees": [[slot, count] for slot, count in self.slot_degrees],
            "coupling_ids": list(self.coupling_ids),
        }


@dataclass(frozen=True, slots=True)
class ClosedAffinization:
    """Closed whole produced by explicit ordered coupling."""

    whole_id: str
    coupling: OrientedCoupling
    receipt: dict[str, Any]

    @property
    def digest(self) -> str:
        return sha256(_canonical_bytes(self.receipt)).hexdigest()


def _participant_payload(participant: CouplingParticipant, slot: int) -> dict[str, Any]:
    return {
        "slot": slot,
        "participant_id": participant.participant_id,
        "scale": participant.scale,
        "role": participant.role,
        "source_digest": participant.source_digest,
    }


def load_authority_snapshot() -> AuthoritySnapshot:
    """Load pinned authority identities used by mechanic 2."""

    root = _stack_root()
    ucns_base = _load_json(root / "research" / "ucns" / "BASE.json")
    metapat_base = _load_json(root / "research" / "metapat" / "BASE.json")
    if ucns_base["source_commit"] != PINNED_UCNS_COMMIT:
        raise CouplingGeometryError("UCNS source commit mismatch")
    if metapat_base["source_commit"] != PINNED_METAPAT_COMMIT:
        raise CouplingGeometryError("METAPAT source commit mismatch")
    phi = _load_metapat_phi()
    policy = phi.DEFAULT_UCNS_PHI_POLICY.to_dict()
    if policy["allowed_relation_kind"] != RELATION_KIND:
        raise CouplingGeometryError("METAPAT Phi relation kind mismatch")
    if policy["theorem_status_transfer"] is not False or policy["metapat_validity_claim"] is not False:
        raise CouplingGeometryError("METAPAT Phi policy must not transfer status")
    mechanic1 = pgfo.receipt_payload()
    stack_manifest = _load_json(root / "stack-manifest.json")
    return AuthoritySnapshot(
        ucns_base=ucns_base,
        metapat_base=metapat_base,
        metapat_phi_policy=policy,
        metapat_prohibited_relation_kinds=tuple(phi.PROHIBITED_FORK_RELATION_KINDS),
        mechanic1_receipt_sha256=pgfo.receipt_digest(mechanic1),
        source_file_digests=_source_file_digests(root),
        stack_manifest_work_graph_sha256=stack_manifest["work_graph_sha256"],
    )


def coupling(
    coupling_id: str,
    participants: tuple[CouplingParticipant, ...],
    *,
    relation_kind: str = RELATION_KIND,
    basis: str = "declared_ordered_incidence",
    source_refs: tuple[str, ...] = ("metapat.ucns_phi.constitutive-simultaneous",),
    unresolved_constraints: tuple[str, ...] = HMMM,
) -> OrientedCoupling:
    """Construct one explicit ordered coupling."""

    return OrientedCoupling(
        coupling_id=coupling_id,
        participants=tuple(participants),
        relation_kind=relation_kind,
        basis=basis,
        source_refs=tuple(source_refs),
        unresolved_constraints=tuple(unresolved_constraints),
    )


def reject_inferred_overlap_coupling(reason: str) -> None:
    """Fail closed for overlap, adjacency, ambient-fill, or provenance inference."""

    _text(reason, "reason")
    raise CouplingGeometryError("coupling must be explicit; inferred overlap closure is forbidden")


def degree_ledger(couplings: tuple[OrientedCoupling, ...]) -> tuple[DegreeEntry, ...]:
    """Return slot-sensitive incidence degree for explicit couplings."""

    if not couplings:
        raise CouplingGeometryError("degree ledger requires at least one explicit coupling")
    incidences: dict[str, list[tuple[int, str]]] = {}
    for item in couplings:
        for slot, participant in enumerate(item.participants):
            incidences.setdefault(participant.participant_id, []).append((slot, item.coupling_id))
    result = []
    for participant_id, entries in sorted(incidences.items()):
        slot_counts: dict[int, int] = {}
        coupling_ids = []
        for slot, coupling_id in entries:
            slot_counts[slot] = slot_counts.get(slot, 0) + 1
            coupling_ids.append(coupling_id)
        result.append(
            DegreeEntry(
                participant_id=participant_id,
                degree=len(entries),
                slot_degrees=tuple(sorted(slot_counts.items())),
                coupling_ids=tuple(coupling_ids),
            )
        )
    return tuple(result)


def close_affinization(
    item: OrientedCoupling,
    authority: AuthoritySnapshot | None = None,
) -> ClosedAffinization:
    """Close one explicit coupling as a recoverable affinization whole."""

    snapshot = authority or load_authority_snapshot()
    receipt = {
        "schema": SCHEMA + ".closed-affinization",
        "version": VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "authority": {
            "ucns": snapshot.ucns_base,
            "metapat": snapshot.metapat_base,
            "metapat_phi_policy": snapshot.metapat_phi_policy,
            "mechanic1_receipt_sha256": snapshot.mechanic1_receipt_sha256,
            "stack_manifest_work_graph_sha256": snapshot.stack_manifest_work_graph_sha256,
            "source_file_digests": [
                {"path": path, "sha256": digest}
                for path, digest in snapshot.source_file_digests
            ],
        },
        "coupling": item.to_payload(),
        "degree": [entry.to_payload() for entry in degree_ledger((item,))],
        "closure": {
            "whole_id_policy": "sha256 of ordered coupling payload",
            "participants_recoverable": True,
            "relation_intrinsic_to_whole": True,
            "closed_over_couplings": 1,
        },
        "falsification_conditions": list(FALSIFICATION_CONDITIONS),
        "promotion_evidence": list(PROMOTION_EVIDENCE),
        "hmmm": list(HMMM),
        "nonclaims": list(NONCLAIMS),
    }
    whole_id = "ucns.affinization:" + sha256(_canonical_bytes(item.to_payload())).hexdigest()
    return ClosedAffinization(whole_id, item, {**receipt, "whole_id": whole_id})


def sample_public_operation_affinization() -> ClosedAffinization:
    """Build the deterministic mechanic-2 sample from mechanic-1 closed operations."""

    carrier = pgfo.load_carrier()
    identity = pgfo.close_operation(pgfo.identity_operation(carrier))
    step = pgfo.close_operation(pgfo.cyclic_order_motion(1, carrier))
    participants = (
        CouplingParticipant(
            "mechanic1.closed-operation.identity",
            "public-gonol-operation",
            "left",
            identity.digest,
        ),
        CouplingParticipant(
            "mechanic1.closed-operation.cyclic-step-one",
            "public-gonol-operation",
            "right",
            step.digest,
        ),
    )
    return close_affinization(
        coupling(
            "mechanic2.public-operation-pair",
            participants,
            basis="mechanic1_closed_operation_pair",
            source_refs=(
                "metapat.ucns_phi.CONSTITUTIVE_RELATION_KIND",
                "research.ucns.public_gonol_functional_operations.v0",
            ),
        )
    )


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_text(encoding="utf-8").encode("utf-8")).hexdigest()


def receipt_payload() -> dict[str, Any]:
    """Return the deterministic mechanic-2 research receipt."""

    authority = load_authority_snapshot()
    sample = sample_public_operation_affinization()
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
            "metapat_phi_policy": authority.metapat_phi_policy,
            "mechanic1_receipt_sha256": authority.mechanic1_receipt_sha256,
            "source_file_digests": [
                {"path": path, "sha256": digest}
                for path, digest in authority.source_file_digests
            ],
        },
        "mechanic": "affinization/coupling geometry",
        "definition": {
            "coupling": "explicit ordered relation over occurrence-addressed participants",
            "admitted_relation_kind": RELATION_KIND,
            "degree": "slot-sensitive incidence count over explicit couplings",
            "closure": "deterministic whole retaining intrinsic relation and recoverable participants",
            "forbidden_inference": "overlap, adjacency, ambient membership, and provenance do not create coupling",
            "status_transfer": False,
        },
        "sample_closed_affinization": {
            "whole_id": sample.whole_id,
            "digest": sample.digest,
            "receipt": sample.receipt,
        },
        "rejected_alternatives": [
            "overlap-derived coupling",
            "adjacency-derived coupling",
            "ambient power-set coupling",
            "order-insensitive coupling",
            "provenance-only containment",
            "theorem or measurement status transfer",
            "successor-number fitting",
        ],
        "falsification_conditions": list(FALSIFICATION_CONDITIONS),
        "promotion_evidence": list(PROMOTION_EVIDENCE),
        "hmmm": list(HMMM),
        "nonclaims": list(NONCLAIMS),
        "next_dependency_complete_action": (
            "derive recursive-scale transition over closed affinization receipts "
            "without changing mechanics 1 or 2 after outcome inspection"
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
