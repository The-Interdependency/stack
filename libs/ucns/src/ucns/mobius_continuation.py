# === MODULE_BUILD ===
# id: ucns_mobius_vesica_continuation
#   module_name: mobius_continuation
#   module_kind: experiment
#   summary: continues the exact Mobius Vesica across rational widths, replicates it into the twelve rigid Seed-of-Life pair placements, and firewalls the quarter-turn certificate from the current half-turn seed phase
#   owner: Erin Spencer
#   public_surface: ContinuationStage, PhaseStage, SeedDyadComparison, VesicaPlacement, MobiusVesicaContinuationEngine, build_default_continuation_report, build_artifact_payload, write_default_artifact
#   internal_surface: exact width stages, half-turn obstruction, rigid pair placement, deterministic combined receipt
#   auth_boundary: none
#   storage_boundary: caller-supplied local paths only through write_default_artifact
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_mobius_vesica_exact.py
#   rollout: research continuation only; does not rewrite PR 174 phase law or select the seven-band candidate
#   rollback: remove with mobius_vesica and mobius_certificates
#   requires: ucns_mobius_vesica_certificates, ucns_mobius_seed_of_life_candidate
#   since: 2026-08-10
#   unresolved: general phase classification, compatible seven-band global phase assignment, simultaneous twelve-pair realization, link invariants, spectral bridge
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: mobius_vesica_width_continuation_recertifies_each_stage
#   given: a sequence of rational widths strictly between zero and one half is requested at quarter-turn phase
#   then: every stage is independently Sturm-certified rather than inheriting a sampled contact count
#   class: correctness
#   since: 2026-08-10
#
# id: mobius_vesica_rigid_placements_cover_seed_structural_pairs
#   given: the Seed-of-Life wheel relation graph is requested
#   then: six center-to-ring and six adjacent-ring rigid placements are emitted, each preserving the local two-plus-four certificate in isolation
#   class: evidence
#   since: 2026-08-10
#
# id: mobius_vesica_seed_phase_mismatch_blocks_certificate_inheritance
#   given: the exact quarter-turn dyad is compared with the current PR-174 half-turn first dyad
#   then: chirality and width matches are retained, phase mismatch is explicit, and the four-contact certificate is not transferred
#   class: doctrine
#   since: 2026-08-10
#
# id: mobius_vesica_half_turn_phase_has_exact_contact_obstruction
#   given: the standard circular family has opposite chirality, phase pair zero and one half, and width below one half
#   then: exact branch equations admit zero physical boundary contacts
#   class: correctness
#   since: 2026-08-10
# === END CONTRACTS ===

"""Continuation and Seed-of-Life placement tools for the certified dyad."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable

from .mobius_certificates import MobiusVesicaCertificate, certify_mobius_vesica
from .mobius_vesica import (
    MOBIUS_VESICA_SCHEMA_ID,
    MOBIUS_VESICA_SCHEMA_VERSION,
    MobiusVesicaParameters,
    TwistChirality,
    build_mobius_vesica,
    fraction_text,
)

SEED_CANDIDATE_PR = 174
SEED_CANDIDATE_HEAD = "eae0776de6436b495c8d8b27d139602fde963e43"
SEED_CANDIDATE_BRANCH = "agent/mobius-seed-of-life-v1"
SEED_CANDIDATE_FIRST_DYAD_PHASE = Fraction(1, 2)
SEED_CANDIDATE_HALF_WIDTH = Fraction(1, 100)


class ContinuationError(ValueError):
    """Raised when a continuation request exceeds the certified boundary."""


@dataclass(frozen=True, slots=True)
class ContinuationStage:
    index: int
    half_width: Fraction
    root_count: int
    physical_boundary_contact_count: int
    null_clearance_lower_bound: Fraction
    certificate_sha256: str
    standing: str = "independently-sturm-certified"

    def as_dict(self) -> dict[str, object]:
        return {
            "index": self.index,
            "half_width": fraction_text(self.half_width),
            "root_count_in_minus_one_to_one": self.root_count,
            "physical_boundary_contact_count": self.physical_boundary_contact_count,
            "null_clearance_lower_bound": fraction_text(self.null_clearance_lower_bound),
            "certificate_sha256": self.certificate_sha256,
            "standing": self.standing,
        }


@dataclass(frozen=True, slots=True)
class PhaseStage:
    index: int
    right_phase_turns: Fraction
    standing: str
    physical_boundary_contact_count: int | None
    exact_reason: str

    def as_dict(self) -> dict[str, object]:
        return {
            "index": self.index,
            "right_phase_turns": fraction_text(self.right_phase_turns),
            "standing": self.standing,
            "physical_boundary_contact_count": self.physical_boundary_contact_count,
            "exact_reason": self.exact_reason,
        }


@dataclass(frozen=True, slots=True)
class SeedDyadComparison:
    certified_phase_turns: Fraction
    seed_phase_turns: Fraction
    certified_half_width: Fraction
    seed_half_width: Fraction
    chirality_match: bool
    width_match: bool
    phase_match: bool
    certified_physical_boundary_contacts: int
    seed_phase_physical_boundary_contacts_in_standard_family: int
    certificate_inherits: bool
    standing: str

    def as_dict(self) -> dict[str, object]:
        return {
            "seed_candidate_pr": SEED_CANDIDATE_PR,
            "seed_candidate_head": SEED_CANDIDATE_HEAD,
            "seed_candidate_branch": SEED_CANDIDATE_BRANCH,
            "certified_phase_turns": fraction_text(self.certified_phase_turns),
            "seed_phase_turns": fraction_text(self.seed_phase_turns),
            "certified_half_width": fraction_text(self.certified_half_width),
            "seed_half_width": fraction_text(self.seed_half_width),
            "chirality_match": self.chirality_match,
            "width_match": self.width_match,
            "phase_match": self.phase_match,
            "certified_physical_boundary_contacts": self.certified_physical_boundary_contacts,
            "seed_phase_physical_boundary_contacts_in_standard_family": self.seed_phase_physical_boundary_contacts_in_standard_family,
            "certificate_inherits": self.certificate_inherits,
            "standing": self.standing,
        }


@dataclass(frozen=True, slots=True)
class VesicaPlacement:
    pair_id: str
    left_label: str
    right_label: str
    rotation_turns: Fraction
    midpoint_x: float
    midpoint_y: float
    left_center_x: float
    left_center_y: float
    right_center_x: float
    right_center_y: float
    local_certificate_preserved: bool = True
    global_simultaneous_realization_claimed: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "pair_id": self.pair_id,
            "left_label": self.left_label,
            "right_label": self.right_label,
            "rotation_turns": fraction_text(self.rotation_turns),
            "midpoint_binary64": [self.midpoint_x, self.midpoint_y],
            "left_center_binary64": [self.left_center_x, self.left_center_y],
            "right_center_binary64": [self.right_center_x, self.right_center_y],
            "local_certificate_preserved": self.local_certificate_preserved,
            "global_simultaneous_realization_claimed": self.global_simultaneous_realization_claimed,
        }


class MobiusVesicaContinuationEngine:
    """Exact local continuation plus firewalled global placement planning."""

    def __init__(self, base_certificate: MobiusVesicaCertificate | None = None) -> None:
        self.base_certificate = base_certificate or certify_mobius_vesica()

    def continue_widths(
        self,
        widths: Iterable[Fraction] = (
            Fraction(1, 200),
            Fraction(1, 100),
            Fraction(1, 80),
            Fraction(1, 50),
            Fraction(1, 20),
            Fraction(1, 10),
            Fraction(1, 5),
            Fraction(1, 4),
        ),
    ) -> tuple[ContinuationStage, ...]:
        stages: list[ContinuationStage] = []
        for index, width in enumerate(widths):
            if not isinstance(width, Fraction) or width <= 0 or width >= Fraction(1, 2):
                raise ContinuationError("every width must be an exact Fraction in 0 < w < 1/2")
            params = MobiusVesicaParameters(half_width=width)
            certificate = certify_mobius_vesica(build_mobius_vesica(params))
            stages.append(
                ContinuationStage(
                    index=index,
                    half_width=width,
                    root_count=certificate.sturm.root_count,
                    physical_boundary_contact_count=certificate.boundary_physical_contact_count,
                    null_clearance_lower_bound=params.null_clearance_lower_bound,
                    certificate_sha256=str(certificate.payload["payload_sha256"]),
                )
            )
        return tuple(stages)

    @staticmethod
    def half_turn_contact_obstruction(half_width: Fraction = Fraction(1, 100)) -> PhaseStage:
        if not isinstance(half_width, Fraction) or half_width <= 0 or half_width >= Fraction(1, 2):
            raise ContinuationError("half-turn obstruction requires 0 < w < 1/2")
        return PhaseStage(
            index=0,
            right_phase_turns=Fraction(1, 2),
            standing="exact-zero-contact-obstruction-in-standard-circular-family",
            physical_boundary_contact_count=0,
            exact_reason=(
                "height equality splits into t=s (mod 2), where planar equality would require "
                "|2*w*cos(pi*t)|=1 although 2*w<1, and t+s=1 (mod 2), where planar "
                "equality forces sin(2*pi*t)=0 but the x coordinates still differ by one"
            ),
        )

    def phase_path_to_seed(self, steps: int = 5) -> tuple[PhaseStage, ...]:
        if isinstance(steps, bool) or not isinstance(steps, int) or steps < 2:
            raise ContinuationError("phase path requires at least two stages")
        start = Fraction(1, 4)
        stop = Fraction(1, 2)
        result: list[PhaseStage] = []
        for index in range(steps):
            phase = start + (stop - start) * Fraction(index, steps - 1)
            if phase == start:
                result.append(
                    PhaseStage(
                        index=index,
                        right_phase_turns=phase,
                        standing="exact-four-contact-certificate",
                        physical_boundary_contact_count=4,
                        exact_reason="quarter-turn height branch reduces to a cubic with two Sturm-certified roots",
                    )
                )
            elif phase == stop:
                obstruction = self.half_turn_contact_obstruction(
                    self.base_certificate.vesica.parameters.half_width
                )
                result.append(
                    PhaseStage(
                        index=index,
                        right_phase_turns=phase,
                        standing=obstruction.standing,
                        physical_boundary_contact_count=0,
                        exact_reason=obstruction.exact_reason,
                    )
                )
            else:
                result.append(
                    PhaseStage(
                        index=index,
                        right_phase_turns=phase,
                        standing="general-phase-unresolved",
                        physical_boundary_contact_count=None,
                        exact_reason="no exact root-classification theorem is asserted for this intermediate phase",
                    )
                )
        return tuple(result)

    def compare_with_seed_candidate(self) -> SeedDyadComparison:
        base = self.base_certificate
        certified_phase = base.vesica.parameters.right_phase_turns
        certified_width = base.vesica.parameters.half_width
        phase_match = certified_phase == SEED_CANDIDATE_FIRST_DYAD_PHASE
        width_match = certified_width == SEED_CANDIDATE_HALF_WIDTH
        chirality_match = (
            base.vesica.parameters.left_chirality is TwistChirality.POSITIVE
            and base.vesica.parameters.right_chirality is TwistChirality.NEGATIVE
        )
        return SeedDyadComparison(
            certified_phase_turns=certified_phase,
            seed_phase_turns=SEED_CANDIDATE_FIRST_DYAD_PHASE,
            certified_half_width=certified_width,
            seed_half_width=SEED_CANDIDATE_HALF_WIDTH,
            chirality_match=chirality_match,
            width_match=width_match,
            phase_match=phase_match,
            certified_physical_boundary_contacts=base.boundary_physical_contact_count,
            seed_phase_physical_boundary_contacts_in_standard_family=0,
            certificate_inherits=chirality_match and width_match and phase_match,
            standing=(
                "phase-law reconciliation required before PR-174 structural pairs may inherit "
                "the exact physical four-contact certificate"
            ),
        )

    @staticmethod
    def seed_structural_placements() -> tuple[VesicaPlacement, ...]:
        placements: list[VesicaPlacement] = []
        ring_centers = [
            (math.cos(math.tau * index / 6), math.sin(math.tau * index / 6))
            for index in range(6)
        ]

        for index, (right_x, right_y) in enumerate(ring_centers):
            placements.append(
                VesicaPlacement(
                    pair_id=f"CENTER_RING_{index}",
                    left_label="CENTER",
                    right_label=f"RING_{index}",
                    rotation_turns=Fraction(index, 6),
                    midpoint_x=right_x / 2,
                    midpoint_y=right_y / 2,
                    left_center_x=0.0,
                    left_center_y=0.0,
                    right_center_x=right_x,
                    right_center_y=right_y,
                )
            )

        for index in range(6):
            left_x, left_y = ring_centers[index]
            right_x, right_y = ring_centers[(index + 1) % 6]
            placements.append(
                VesicaPlacement(
                    pair_id=f"RING_{index}_RING_{(index + 1) % 6}",
                    left_label=f"RING_{index}",
                    right_label=f"RING_{(index + 1) % 6}",
                    rotation_turns=Fraction(index, 6) + Fraction(1, 3),
                    midpoint_x=(left_x + right_x) / 2,
                    midpoint_y=(left_y + right_y) / 2,
                    left_center_x=left_x,
                    left_center_y=left_y,
                    right_center_x=right_x,
                    right_center_y=right_y,
                )
            )
        return tuple(placements)

    def report(self) -> dict[str, object]:
        widths = self.continue_widths()
        phase_path = self.phase_path_to_seed()
        placements = self.seed_structural_placements()
        comparison = self.compare_with_seed_candidate()
        return {
            "width_continuation": {
                "standing": "each listed stage independently recertified",
                "stages": [stage.as_dict() for stage in widths],
            },
            "phase_continuation_to_current_seed_candidate": {
                "standing": "certificate is lost before the half-turn endpoint; intermediate phases remain open",
                "stages": [stage.as_dict() for stage in phase_path],
            },
            "seed_candidate_comparison": comparison.as_dict(),
            "structural_pair_placements": {
                "count": len(placements),
                "center_to_ring": 6,
                "adjacent_ring": 6,
                "standing": (
                    "each is a rigid local copy preserving the dyad certificate in isolation; "
                    "no simultaneous seven-band embedding is claimed"
                ),
                "placements": [placement.as_dict() for placement in placements],
            },
            "next_proof_obligation": (
                "solve the global phase-and-lift compatibility problem for all twelve structural pairs "
                "without importing the local four-contact certificate across the quarter/half-turn mismatch"
            ),
        }


def build_default_continuation_report() -> dict[str, object]:
    return MobiusVesicaContinuationEngine().report()


def build_artifact_payload() -> dict[str, object]:
    certificate = certify_mobius_vesica()
    certificate_payload = dict(certificate.payload)
    certificate_digest = certificate_payload.pop("payload_sha256")
    payload: dict[str, object] = {
        **certificate_payload,
        "certificate_payload_sha256": certificate_digest,
        "continuation": MobiusVesicaContinuationEngine(certificate).report(),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    payload["artifact_payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload


def write_default_artifact(path: str | Path, *, indent: int = 2) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(build_artifact_payload(), indent=indent, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output
