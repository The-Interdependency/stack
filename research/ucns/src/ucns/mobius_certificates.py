# === MODULE_BUILD ===
# id: ucns_mobius_vesica_certificates
#   module_name: mobius_certificates
#   module_kind: experiment
#   summary: certifies the canonical Mobius Vesica centerline count, physical boundary-contact count, quotient return, null clearance, and proof firewall using exact rational Sturm arithmetic plus residual witnesses
#   owner: Erin Spencer
#   public_surface: RationalInterval, SturmCertificate, BoundaryContactWitness, MobiusVesicaCertificate, sturm_sequence, count_real_roots, isolate_real_roots, certify_mobius_vesica, write_default_certificate
#   internal_surface: rational polynomial arithmetic, branch obstruction, deterministic witness realization, payload hashing
#   auth_boundary: none
#   storage_boundary: caller-supplied local paths only through write_default_certificate
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_mobius_vesica_exact.py
#   rollout: exact certificate for the normalized circular-ribbon quarter-turn family only; selection effect none
#   rollback: remove with mobius_vesica and mobius_continuation without changing the seven-band candidate
#   requires: ucns_mobius_vesica_exact_embedding
#   since: 2026-08-10
#   unresolved: full surface-pair intersection locus, general-phase classification, arbitrary-perturbation stability, linking, ambient isotopy, zeta operator
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: mobius_vesica_sturm_proves_four_physical_boundary_contacts
#   given: the normalized radius-one, separation-one, half-width-one-hundredth, opposite-chirality, quarter-turn dyad is constructed
#   then: exact Sturm arithmetic proves two roots of the boundary-contact cubic in minus one to one and each root induces two distinct physical contacts, for exactly four
#   class: correctness
#   since: 2026-08-10
#
# id: mobius_vesica_contact_semantics_are_not_flattened
#   given: a certificate is emitted
#   then: physical boundary contacts, centerline contacts, projected crossings, and the unresolved full surface-intersection locus remain distinct fields
#   class: doctrine
#   since: 2026-08-10
#
# id: mobius_vesica_alternate_height_branch_is_obstructed
#   given: the exact quarter-turn height equation is split into its two trigonometric branches
#   then: the difference branch is rejected by the exact modulus contradiction two times radius not equal center separation
#   class: correctness
#   since: 2026-08-10
#
# id: mobius_vesica_certificate_is_nonselecting_and_zeta_firewalled
#   given: a machine receipt is serialized
#   then: it records selection effect none and denies electron ontology, Pauli derivation, whole-surface classification, link proof, spectral correspondence, and Riemann-hypothesis proof
#   class: doctrine
#   since: 2026-08-10
# === END CONTRACTS ===

"""Exact certificates for the canonical Möbius Vesica Piscis candidate."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from typing import Iterable, Sequence

from .mobius_vesica import (
    MOBIUS_VESICA_SCHEMA_ID,
    MOBIUS_VESICA_SCHEMA_VERSION,
    SOURCE_BOUNDARY_CLAIM_LINE,
    SOURCE_CENTERLINE_CLAIM_LINE,
    SOURCE_DOCUMENT_NAME,
    SOURCE_DOCUMENT_SHA256,
    MobiusVesica,
    MobiusVesicaError,
    Point3,
    build_mobius_vesica,
    fraction_text,
)

Polynomial = tuple[Fraction, ...]


class CertificateError(ValueError):
    """Raised when an exact certificate cannot be issued for the requested family."""


def _trim(poly: Sequence[Fraction]) -> Polynomial:
    values = list(poly)
    if not values:
        return (Fraction(0),)
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def _derivative(poly: Polynomial) -> Polynomial:
    if len(poly) <= 1:
        return (Fraction(0),)
    return _trim(tuple(Fraction(index) * value for index, value in enumerate(poly[1:], start=1)))


def _evaluate(poly: Polynomial, value: Fraction) -> Fraction:
    result = Fraction(0)
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def _divide_with_remainder(dividend: Polynomial, divisor: Polynomial) -> tuple[Polynomial, Polynomial]:
    numerator = list(_trim(dividend))
    denominator = _trim(divisor)
    if denominator == (Fraction(0),):
        raise ZeroDivisionError("polynomial division by zero")
    if len(numerator) < len(denominator):
        return (Fraction(0),), tuple(numerator)

    quotient = [Fraction(0)] * (len(numerator) - len(denominator) + 1)
    while len(numerator) >= len(denominator) and any(numerator):
        degree = len(numerator) - len(denominator)
        factor = numerator[-1] / denominator[-1]
        quotient[degree] = factor
        for index, coefficient in enumerate(denominator):
            numerator[index + degree] -= factor * coefficient
        numerator = list(_trim(tuple(numerator)))
    return _trim(tuple(quotient)), _trim(tuple(numerator))


def _negative(poly: Polynomial) -> Polynomial:
    return _trim(tuple(-coefficient for coefficient in poly))


def _primitive_sign_normalize(poly: Polynomial) -> Polynomial:
    """Scale a polynomial by a positive rational without changing signs."""

    poly = _trim(poly)
    if poly == (Fraction(0),):
        return poly
    leading = poly[-1]
    scale = abs(leading)
    return tuple(coefficient / scale for coefficient in poly)


def sturm_sequence(poly: Sequence[Fraction]) -> tuple[Polynomial, ...]:
    """Return the exact rational Sturm chain for ``poly``."""

    first = _trim(tuple(Fraction(value) for value in poly))
    if len(first) <= 1:
        raise CertificateError("Sturm certification requires a nonconstant polynomial")
    second = _derivative(first)
    if second == (Fraction(0),):
        raise CertificateError("polynomial derivative vanished")

    sequence: list[Polynomial] = [
        _primitive_sign_normalize(first),
        _primitive_sign_normalize(second),
    ]
    while sequence[-1] != (Fraction(0),):
        _, remainder = _divide_with_remainder(sequence[-2], sequence[-1])
        if remainder == (Fraction(0),):
            break
        sequence.append(_primitive_sign_normalize(_negative(remainder)))
    return tuple(sequence)


def _sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def _variations_at(sequence: Sequence[Polynomial], value: Fraction) -> int:
    signs = [_sign(_evaluate(poly, value)) for poly in sequence]
    nonzero = [item for item in signs if item]
    return sum(left != right for left, right in zip(nonzero, nonzero[1:]))


def count_real_roots(poly: Sequence[Fraction], lower: Fraction, upper: Fraction) -> int:
    """Count distinct real roots in ``(lower, upper)`` using Sturm's theorem.

    The endpoints must not themselves be roots.  The certified Möbius-vesica
    polynomial is positive at both -1 and +1 for every supported width.
    """

    polynomial = _trim(tuple(Fraction(value) for value in poly))
    if lower >= upper:
        raise CertificateError("root interval must have lower < upper")
    if _evaluate(polynomial, lower) == 0 or _evaluate(polynomial, upper) == 0:
        raise CertificateError("Sturm interval endpoints may not be roots")
    sequence = sturm_sequence(polynomial)
    return _variations_at(sequence, lower) - _variations_at(sequence, upper)


@dataclass(frozen=True, slots=True)
class RationalInterval:
    lower: Fraction
    upper: Fraction

    def __post_init__(self) -> None:
        if self.lower >= self.upper:
            raise CertificateError("rational interval must have positive width")

    @property
    def midpoint(self) -> Fraction:
        return (self.lower + self.upper) / 2

    @property
    def width(self) -> Fraction:
        return self.upper - self.lower

    def as_dict(self) -> dict[str, object]:
        return {
            "lower": fraction_text(self.lower),
            "upper": fraction_text(self.upper),
            "width": fraction_text(self.width),
            "midpoint_binary64": float(self.midpoint),
        }


def isolate_real_roots(
    poly: Sequence[Fraction],
    lower: Fraction,
    upper: Fraction,
    *,
    precision_bits: int = 36,
) -> tuple[RationalInterval, ...]:
    """Return disjoint dyadic intervals, each containing one distinct root."""

    if isinstance(precision_bits, bool) or not isinstance(precision_bits, int) or precision_bits < 4:
        raise CertificateError("precision_bits must be an integer >= 4")
    polynomial = _trim(tuple(Fraction(value) for value in poly))
    target_width = Fraction(1, 2**precision_bits)
    total = count_real_roots(polynomial, lower, upper)
    pending: list[tuple[Fraction, Fraction, int]] = [(lower, upper, total)]
    isolated: list[RationalInterval] = []

    while pending:
        left, right, count = pending.pop()
        if count == 0:
            continue
        if count == 1 and right - left <= target_width:
            isolated.append(RationalInterval(left, right))
            continue
        midpoint = (left + right) / 2
        if _evaluate(polynomial, midpoint) == 0:
            # This branch is not reached by the default irreducible cubic.  A
            # small asymmetric dyadic split keeps the routine total for future
            # rational-root candidates without treating a point as an interval.
            midpoint = left + (right - left) * Fraction(3, 7)
            if _evaluate(polynomial, midpoint) == 0:
                raise CertificateError("root isolation encountered a repeated rational split root")
        left_count = count_real_roots(polynomial, left, midpoint)
        right_count = count_real_roots(polynomial, midpoint, right)
        if left_count + right_count != count:
            raise CertificateError("Sturm subdivision failed to conserve the root count")
        pending.append((midpoint, right, right_count))
        pending.append((left, midpoint, left_count))

    isolated.sort(key=lambda interval: interval.midpoint)
    if len(isolated) != total:
        raise CertificateError("root isolation did not produce one interval per root")
    return tuple(isolated)


def _cross_norm(left: Point3, right: Point3) -> float:
    x = left.y * right.z - left.z * right.y
    y = left.z * right.x - left.x * right.z
    z = left.x * right.y - left.y * right.x
    return math.sqrt(x * x + y * y + z * z)


@dataclass(frozen=True, slots=True)
class SturmCertificate:
    polynomial: Polynomial
    sequence: tuple[Polynomial, ...]
    lower: Fraction
    upper: Fraction
    root_count: int
    isolating_intervals: tuple[RationalInterval, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "coefficient_order": "ascending",
            "polynomial": [fraction_text(value) for value in self.polynomial],
            "equation": "4*w*x^3 + 4*x^2 - 2*w*x - 3 = 0",
            "domain": {
                "lower": fraction_text(self.lower),
                "upper": fraction_text(self.upper),
            },
            "endpoint_values": {
                "lower": fraction_text(_evaluate(self.polynomial, self.lower)),
                "upper": fraction_text(_evaluate(self.polynomial, self.upper)),
            },
            "sturm_sequence": [
                [fraction_text(value) for value in polynomial]
                for polynomial in self.sequence
            ],
            "variation_lower": _variations_at(self.sequence, self.lower),
            "variation_upper": _variations_at(self.sequence, self.upper),
            "distinct_root_count": self.root_count,
            "isolating_intervals": [interval.as_dict() for interval in self.isolating_intervals],
        }


@dataclass(frozen=True, slots=True)
class BoundaryContactWitness:
    contact_id: str
    root_interval: RationalInterval
    cosine_half_angle: float
    left_turn: float
    right_turn: float
    point: Point3
    residual: float
    tangent_cross_norm: float

    def as_dict(self) -> dict[str, object]:
        return {
            "contact_id": self.contact_id,
            "root_interval": self.root_interval.as_dict(),
            "cosine_half_angle_binary64": self.cosine_half_angle,
            "left_boundary_turn": self.left_turn,
            "right_boundary_turn": self.right_turn,
            "point_binary64": self.point.as_dict(),
            "contact_residual_binary64": self.residual,
            "boundary_tangent_cross_norm_binary64": self.tangent_cross_norm,
        }


@dataclass(frozen=True, slots=True)
class MobiusVesicaCertificate:
    vesica: MobiusVesica
    sturm: SturmCertificate
    witnesses: tuple[BoundaryContactWitness, ...]
    seam_residual: float
    return_residual: float
    centerline_residuals: tuple[float, float]
    certificate_status: str = "certified-existence-in-standard-circular-ribbon-family"

    @property
    def centerline_contact_count(self) -> int:
        return len(self.vesica.centerline_contacts)

    @property
    def boundary_physical_contact_count(self) -> int:
        return len(self.witnesses)

    @property
    def payload(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "schema_id": f"{MOBIUS_VESICA_SCHEMA_ID}.certificate",
            "schema_version": MOBIUS_VESICA_SCHEMA_VERSION,
            "authority": "Erin Spencer",
            "recorded_on": "2026-08-10",
            "record_status": "authority-directed-exact-candidate-certificate",
            "selection_effect": "none",
            "certificate_status": self.certificate_status,
            "source_basis": {
                "name": SOURCE_DOCUMENT_NAME,
                "sha256": SOURCE_DOCUMENT_SHA256,
                "centerline_claim_line": SOURCE_CENTERLINE_CLAIM_LINE,
                "boundary_claim_line": SOURCE_BOUNDARY_CLAIM_LINE,
                "source_claims": {
                    "centerlines": "exactly two contacts",
                    "single_continuous_boundaries": "exactly four distinct physical contacts",
                },
            },
            "jurisdiction": {
                "construction_owner": "UCNS",
                "metapat_role": "later semantic consumer only; no geometry or theorem-status transfer",
                "edcm_activation": False,
                "metapat_activation": False,
            },
            "embedding": self.vesica.as_dict(),
            "quotient": {
                "one_turn_identification": "X(t+1,u)=X(t,-u)",
                "two_turn_return": "X(t+2,u)=X(t,u)",
                "maximum_sampled_seam_residual_binary64": self.seam_residual,
                "maximum_sampled_return_residual_binary64": self.return_residual,
                "analytic_standing": "follows identically from odd chirality in the frame angle",
            },
            "centerline_contacts": {
                "semantic_type": "physical equality of the two core curves",
                "exact_count": self.centerline_contact_count,
                "maximum_residual_binary64": max(self.centerline_residuals),
                "events": [contact.as_dict() for contact in self.vesica.centerline_contacts],
            },
            "boundary_contacts": {
                "semantic_type": "physical equality of the two single continuous boundary curves in R3",
                "exact_count": self.boundary_physical_contact_count,
                "height_equation_branches": {
                    "sum_branch": "t+s = 1/2 (mod 2), reduced to the certified cubic",
                    "difference_branch": "t-s = 1/2 (mod 2), obstructed because equality would require 2*radius=center_distance",
                    "difference_branch_obstructed": 2 * self.vesica.parameters.radius
                    != self.vesica.parameters.center_distance,
                },
                "root_to_contact_multiplicity": 2,
                "sturm_certificate": self.sturm.as_dict(),
                "witnesses": [witness.as_dict() for witness in self.witnesses],
                "maximum_witness_residual_binary64": max(w.residual for w in self.witnesses),
                "minimum_tangent_cross_norm_binary64": min(
                    w.tangent_cross_norm for w in self.witnesses
                ),
                "arbitrary_3d_perturbation_stability": "not claimed; isolated curve contacts in R3 are not generic",
                "symmetry_preserving_width_continuation": "handled separately by mobius_continuation",
            },
            "null_center": {
                "point": ["0", "0", "0"],
                "exact_clearance_lower_bound": fraction_text(
                    self.vesica.parameters.null_clearance_lower_bound
                ),
                "standing": "origin excluded from each band by triangle inequality; not promoted to a probability node or UCNS Structural Null",
            },
            "pair_surface_intersection_locus": {
                "standing": "unresolved",
                "reason": "this certificate counts the two centerlines and the two continuous boundaries, not every point where the two two-dimensional surfaces meet",
            },
            "nonclaims": [
                "not a classification of the complete two-surface intersection locus",
                "not a proof of arbitrary-perturbation stability",
                "not a linking-number, Hopf-link, or ambient-isotopy certificate",
                "not an established electron ontology or Pauli-exclusion derivation",
                "not a canonical seven-band phase law",
                "not a spectral operator or correspondence with zeta zeros",
                "not a proof of the Riemann hypothesis or any zeta-function theorem",
                "not EDCM measurement validity or METAPAT validity",
            ],
            "hmmm": [
                "the exact four-contact witness uses a quarter-turn phase offset, while the current seven-band candidate records a half-turn first-dyad phase",
                "the phase mismatch must be reconciled before the seven-band candidate inherits this physical-contact certificate",
                "physical boundary contacts are symmetry-supported and should not be confused with a stable link of disjoint curves",
            ],
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        payload["payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        return payload

    def json_text(self, *, indent: int = 2) -> str:
        return json.dumps(self.payload, indent=indent, ensure_ascii=False, sort_keys=True) + "\n"


def _build_witnesses(
    vesica: MobiusVesica,
    intervals: Iterable[RationalInterval],
) -> tuple[BoundaryContactWitness, ...]:
    witnesses: list[BoundaryContactWitness] = []
    for root_index, interval in enumerate(intervals):
        cosine = float(interval.midpoint)
        angle = math.acos(cosine)
        for branch_index, half_angle in enumerate((angle, math.tau - angle)):
            left_turn = half_angle / math.pi
            right_turn = (0.5 - left_turn) % 2.0
            left_point = vesica.left.boundary_point(left_turn)
            right_point = vesica.right.boundary_point(right_turn)
            left_tangent = vesica.left.boundary_tangent(left_turn)
            right_tangent = vesica.right.boundary_tangent(right_turn)
            witnesses.append(
                BoundaryContactWitness(
                    contact_id=f"BOUNDARY_{root_index}_{branch_index}",
                    root_interval=interval,
                    cosine_half_angle=cosine,
                    left_turn=left_turn,
                    right_turn=right_turn,
                    point=Point3(
                        (left_point.x + right_point.x) / 2,
                        (left_point.y + right_point.y) / 2,
                        (left_point.z + right_point.z) / 2,
                    ),
                    residual=left_point.distance_to(right_point),
                    tangent_cross_norm=_cross_norm(left_tangent, right_tangent),
                )
            )
    witnesses.sort(key=lambda witness: (-witness.point.y, -witness.point.z))
    return tuple(witnesses)


def certify_mobius_vesica(vesica: MobiusVesica | None = None) -> MobiusVesicaCertificate:
    """Issue an exact four-contact certificate for the supported family."""

    candidate = vesica or build_mobius_vesica()
    params = candidate.parameters
    if params.radius != 1 or params.center_distance != 1:
        raise CertificateError("exact certificate currently supports radius=separation=1")
    if params.left_phase_turns != 0 or params.right_phase_turns != Fraction(1, 4):
        raise CertificateError("exact certificate currently supports phases 0 and 1/4")
    if params.left_chirality.value != 1 or params.right_chirality.value != -1:
        raise CertificateError("exact certificate currently supports positive/negative chirality order")
    if params.half_width <= 0 or params.half_width >= Fraction(1, 2):
        raise CertificateError("certified null-preserving width range is 0 < w < 1/2")

    polynomial = candidate.boundary_contact_polynomial()
    sequence = sturm_sequence(polynomial)
    lower, upper = Fraction(-1), Fraction(1)
    root_count = count_real_roots(polynomial, lower, upper)
    if root_count != 2:
        raise CertificateError(f"expected two half-angle roots, observed {root_count}")
    intervals = isolate_real_roots(polynomial, lower, upper)
    sturm = SturmCertificate(
        polynomial=polynomial,
        sequence=sequence,
        lower=lower,
        upper=upper,
        root_count=root_count,
        isolating_intervals=intervals,
    )
    witnesses = _build_witnesses(candidate, intervals)
    if len(witnesses) != 4:
        raise CertificateError("two isolated roots must induce exactly four boundary contacts")
    if max(witness.residual for witness in witnesses) > 1e-9:
        raise CertificateError("binary64 witnesses failed the exact contact equations")
    if min(witness.tangent_cross_norm for witness in witnesses) <= 1e-8:
        raise CertificateError("boundary tangents became parallel at a certified contact")

    seam_residual, return_residual = candidate.seam_and_return_residuals()
    centerline_residuals = candidate.centerline_contact_residuals()
    if max(centerline_residuals) > 1e-12:
        raise CertificateError("centerline witness residual exceeded tolerance")
    if seam_residual > 1e-12 or return_residual > 1e-12:
        raise CertificateError("Möbius quotient witness residual exceeded tolerance")
    if params.null_clearance_lower_bound <= 0:
        raise CertificateError("origin clearance is not positive")

    return MobiusVesicaCertificate(
        vesica=candidate,
        sturm=sturm,
        witnesses=witnesses,
        seam_residual=seam_residual,
        return_residual=return_residual,
        centerline_residuals=centerline_residuals,
    )


def write_default_certificate(path: str | Path, *, indent: int = 2) -> Path:
    """Serialize the deterministic default certificate to ``path``."""

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(certify_mobius_vesica().json_text(indent=indent), encoding="utf-8")
    return output
