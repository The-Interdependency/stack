# === MODULE_BUILD ===
# id: ucns_prime_generic_interval_certificate
#   module_name: prime_generic_interval_certificate
#   module_kind: experiment
#   summary: independently replays the frozen P7/P5 generic crossing diagram with outward-rounded MPFR atan2 and smooth-field intervals
#   owner: Erin Spencer
#   public_surface: GenericIntervalCrossingCertificate, GenericIntervalDiagramCertificate, certify_generic_prime_diagram, generic_interval_family_certificate, write_generic_interval_family_certificate
#   internal_surface: shifted-center, equal-circle intersection, turn, smooth-field, and transversality interval construction
#   auth_boundary: none
#   storage_boundary: caller-supplied local paths only through the writer function
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_generic_interval_certificate.py
#   rollout: nonselecting certificate over the already frozen P7/P5 generic diagrams
#   rollback: remove this module, its tests, document, and generated certificate
#   requires: ucns_mpfr_interval, ucns_prime_exact_milnor_alexander_p7_p5
#   since: 2026-08-15
#   unresolved: proof-assistant replay and symbolic validation of every interval primitive
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: prime_generic_turns_are_outward_atan2_enclosed
#   given: every frozen P7/P5 generic equal-circle crossing is reconstructed
#   then: direct system MPFR encloses both incident turns through directed-rounded atan2 without a branch-cut ambiguity
#   class: evidence
#   since: 2026-08-15
#
# id: prime_generic_smooth_signs_are_interval_certified
#   given: each incident turn interval lies within one declared smooth-field segment
#   then: the complete smooth-field interval difference excludes zero and agrees with the frozen over-under ordering
#   class: evidence
#   since: 2026-08-15
#
# id: prime_generic_crossing_signs_are_interval_certified
#   given: every reconstructed crossing has interval-certified height ordering and tangent determinant
#   then: all P7-first and P5-second crossing signs agree with the frozen generic diagrams
#   class: evidence
#   since: 2026-08-15
#
# id: prime_generic_interval_receipt_is_nonselecting
#   given: the family certificate is serialized
#   then: it retains method, backend, complete crossing coverage, source identities, information boundary, and selection effect none
#   class: doctrine
#   since: 2026-08-15
# === END CONTRACTS ===

"""Outward-rounded replay of the frozen P7/P5 generic crossing diagram.

Usage::

    PYTHONPATH=src python -m ucns.prime_generic_interval_certificate \
      generated/prime-generic-interval-family-certificate.json

The certificate reconstructs the fixed translated equal-circle projection.  It
does not reuse stored turn, height, or sign values as numerical inputs.  Stored
crossings are used only as the comparison target after interval evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
from typing import Sequence

from .mpfr_interval import (
    DEFAULT_PRECISION_BITS,
    MPFRError,
    MPInterval,
    atan2_interval,
    flat_step_interval,
    mpfr_version,
)
from .prime_exact_milnor_alexander import (
    PROJECTION_EPSILON,
    SHIFT_VECTORS,
    SOURCE_NAME,
    SOURCE_SHA256,
    build_generic_prime_five_diagram,
    build_generic_prime_seven_diagram,
)
from .prime_smooth_ribbons import (
    SmoothPrimeRibbon,
    build_smooth_prime_five,
    build_smooth_prime_seven,
)

SCHEMA_ID = "ucns.prime-generic-interval-certificate"
SCHEMA_VERSION = "0.1.0"
DEFAULT_CERTIFICATE_PRECISION_BITS = 512


class GenericIntervalCertificateError(ValueError):
    """Raised when a generic crossing cannot be certified without ambiguity."""


def _canonical_json_sha256(payload: object) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _i(value: Fraction | int, precision: int) -> MPInterval:
    return MPInterval.rational(value, precision=precision)


def _centers(prime: int, precision: int) -> dict[str, tuple[MPInterval, MPInterval]]:
    zero = _i(0, precision)
    one = _i(1, precision)
    if prime == 5:
        base = {
            "C": (zero, zero), "R0": (one, zero), "R1": (zero, one),
            "R2": (-one, zero), "R3": (zero, -one),
        }
    elif prime == 7:
        half = _i(Fraction(1, 2), precision)
        root_three_half = _i(3, precision).sqrt() / _i(2, precision)
        base = {
            "C": (zero, zero), "R0": (one, zero),
            "R1": (half, root_three_half), "R2": (-half, root_three_half),
            "R3": (-one, zero), "R4": (-half, -root_three_half),
            "R5": (half, -root_three_half),
        }
    else:
        raise GenericIntervalCertificateError("only P7 and P5 are supported")
    epsilon = _i(PROJECTION_EPSILON, precision)
    return {
        carrier: (
            point[0] + epsilon * _i(SHIFT_VECTORS[carrier][0], precision),
            point[1] + epsilon * _i(SHIFT_VECTORS[carrier][1], precision),
        )
        for carrier, point in base.items()
    }


def _circle_intersections(
    left: tuple[MPInterval, MPInterval],
    right: tuple[MPInterval, MPInterval],
    precision: int,
) -> tuple[tuple[MPInterval, MPInterval], ...]:
    dx, dy = right[0] - left[0], right[1] - left[1]
    distance = (dx.square() + dy.square()).sqrt()
    two = _i(2, precision)
    if distance.lo.compare(two.hi) >= 0:
        return ()
    if distance.hi.compare(two.lo) >= 0:
        raise GenericIntervalCertificateError("circle intersection count is interval-ambiguous")
    if distance.lo.sign <= 0:
        raise GenericIntervalCertificateError("circle centers are not interval-separated")
    half = _i(Fraction(1, 2), precision)
    height = (_i(1, precision) - (distance * half).square()).sqrt()
    midpoint = ((left[0] + right[0]) * half, (left[1] + right[1]) * half)
    perpendicular = (-dy / distance, dx / distance)
    offset = (height * perpendicular[0], height * perpendicular[1])
    return (
        (midpoint[0] + offset[0], midpoint[1] + offset[1]),
        (midpoint[0] - offset[0], midpoint[1] - offset[1]),
    )


def _turn_interval(
    point: tuple[MPInterval, MPInterval],
    center: tuple[MPInterval, MPInterval],
    precision: int,
) -> MPInterval:
    angle = atan2_interval(point[1] - center[1], point[0] - center[0])
    zero = _i(0, precision)
    two_pi = _i(2, precision) * MPInterval.pi(precision=precision)
    if angle.hi.sign < 0:
        angle = angle + two_pi
    elif angle.lo.sign < 0:
        raise GenericIntervalCertificateError("turn interval straddles the atan2 zero seam")
    turn = angle / two_pi
    if turn.lo.sign < 0 or turn.hi.compare(_i(1, precision).hi) >= 0:
        raise GenericIntervalCertificateError("turn interval escaped [0, 1)")
    return turn


def _smooth_field_interval(
    ribbon: SmoothPrimeRibbon,
    carrier: str,
    turn: MPInterval,
    precision: int,
) -> tuple[MPInterval, int]:
    one = _i(1, precision)
    for index, segment in enumerate(ribbon.field(carrier).segments):
        adjusted = turn
        left = _i(segment.left_turn, precision)
        right = _i(segment.right_turn, precision)
        if index == len(ribbon.field(carrier).segments) - 1 and turn.hi.compare(left.lo) < 0:
            adjusted = turn + one
        if adjusted.lo.compare(left.hi) >= 0 and adjusted.hi.compare(right.lo) <= 0:
            width = _i(segment.right_turn - segment.left_turn, precision)
            local = (adjusted - left) / width
            step = flat_step_interval(local)
            left_value = _i(segment.left_value, precision)
            delta = _i(segment.right_value - segment.left_value, precision)
            return left_value + delta * step, index
    raise GenericIntervalCertificateError(
        f"turn interval for {carrier} does not lie inside one smooth segment"
    )


def _sign_excluding_zero(value: MPInterval, label: str) -> int:
    if value.lo.sign > 0:
        return 1
    if value.hi.sign < 0:
        return -1
    raise GenericIntervalCertificateError(f"{label} interval contains zero")


@dataclass(frozen=True, slots=True)
class GenericIntervalCrossingCertificate:
    crossing_id: str
    left_turn_lower: str
    left_turn_upper: str
    right_turn_lower: str
    right_turn_upper: str
    left_smooth_segment: int
    right_smooth_segment: int
    height_difference_lower: str
    height_difference_upper: str
    transversality_lower: str
    transversality_upper: str
    certified_over: str
    certified_under: str
    certified_sign: int

    def as_dict(self) -> dict[str, object]:
        return {
            "crossing_id": self.crossing_id,
            "turn_intervals": {
                "left": [self.left_turn_lower, self.left_turn_upper],
                "right": [self.right_turn_lower, self.right_turn_upper],
            },
            "smooth_segments": {
                "left": self.left_smooth_segment,
                "right": self.right_smooth_segment,
            },
            "height_difference_interval": [
                self.height_difference_lower, self.height_difference_upper,
            ],
            "transversality_interval": [
                self.transversality_lower, self.transversality_upper,
            ],
            "certified_over": self.certified_over,
            "certified_under": self.certified_under,
            "certified_sign": self.certified_sign,
        }


@dataclass(frozen=True, slots=True)
class GenericIntervalDiagramCertificate:
    prime: int
    precision_bits: int
    crossing_count: int
    frozen_crossing_count: int
    all_turns_enclosed: bool
    all_height_orders_agree: bool
    all_crossing_signs_agree: bool
    crossings: tuple[GenericIntervalCrossingCertificate, ...]

    def as_dict(self, *, include_crossings: bool = True) -> dict[str, object]:
        payload: dict[str, object] = {
            "prime": self.prime,
            "precision_bits": self.precision_bits,
            "crossing_count": self.crossing_count,
            "frozen_crossing_count": self.frozen_crossing_count,
            "all_turns_enclosed": self.all_turns_enclosed,
            "all_height_orders_agree": self.all_height_orders_agree,
            "all_crossing_signs_agree": self.all_crossing_signs_agree,
        }
        if include_crossings:
            payload["crossings"] = [row.as_dict() for row in self.crossings]
        return payload


def _contains_decimal(interval: MPInterval, value: str) -> bool:
    # Decimal comparison is evidentiary only; the sign calculation does not use
    # the frozen value.  The frozen diagram stores ``mp.nstr`` rounded decimal
    # text, so compare against its half-unit-in-last-place rounding cell rather
    # than pretending the displayed decimal is the unrounded mathematical turn.
    exact = MPInterval.decimal(value, precision=interval.precision)
    decimal_value = Decimal(value)
    significant_digits = len(decimal_value.as_tuple().digits)
    half_ulp = Decimal(5).scaleb(decimal_value.adjusted() - significant_digits)
    tolerance = MPInterval.decimal(str(half_ulp), precision=interval.precision)
    display_cell = MPInterval((exact - tolerance).lo, (exact + tolerance).hi)
    return interval.lo.compare(display_cell.hi) <= 0 and interval.hi.compare(display_cell.lo) >= 0


def certify_generic_prime_diagram(
    prime: int,
    *,
    precision_bits: int = DEFAULT_CERTIFICATE_PRECISION_BITS,
) -> GenericIntervalDiagramCertificate:
    if precision_bits < DEFAULT_PRECISION_BITS:
        raise GenericIntervalCertificateError(
            f"precision_bits must be at least {DEFAULT_PRECISION_BITS}"
        )
    ribbon = build_smooth_prime_seven() if prime == 7 else build_smooth_prime_five()
    frozen = (
        build_generic_prime_seven_diagram()
        if prime == 7
        else build_generic_prime_five_diagram()
    )
    centers = _centers(prime, precision_bits)
    reconstructed: list[tuple[str, str, MPInterval, MPInterval, MPInterval, MPInterval, int, int]] = []
    for left, right in itertools.combinations(ribbon.carriers, 2):
        local = []
        for point in _circle_intersections(centers[left], centers[right], precision_bits):
            left_turn = _turn_interval(point, centers[left], precision_bits)
            right_turn = _turn_interval(point, centers[right], precision_bits)
            left_height, left_segment = _smooth_field_interval(
                ribbon, left, left_turn, precision_bits
            )
            right_height, right_segment = _smooth_field_interval(
                ribbon, right, right_turn, precision_bits
            )
            height_difference = left_height - right_height
            left_radius = (point[0] - centers[left][0], point[1] - centers[left][1])
            right_radius = (point[0] - centers[right][0], point[1] - centers[right][1])
            determinant = (
                left_radius[0] * right_radius[1]
                - left_radius[1] * right_radius[0]
            )
            local.append((
                left_turn, right_turn, height_difference, determinant,
                left_segment, right_segment,
            ))
        local.sort(key=lambda row: row[0].lower_float())
        for row in local:
            reconstructed.append((left, right, *row))
    if len(reconstructed) != len(frozen.crossings):
        raise GenericIntervalCertificateError(
            f"crossing count differs: reconstructed {len(reconstructed)}, frozen {len(frozen.crossings)}"
        )
    frozen_by_id = {crossing.crossing_id: crossing for crossing in frozen.crossings}
    rows: list[GenericIntervalCrossingCertificate] = []
    turns_enclosed = True
    height_agreement = True
    sign_agreement = True
    pair_counts: dict[tuple[str, str], int] = {}
    for left, right, left_turn, right_turn, height_difference, determinant, left_segment, right_segment in reconstructed:
        key = (left, right)
        index = pair_counts.get(key, 0)
        pair_counts[key] = index + 1
        crossing_id = f"{left}::{right}::{index}"
        expected = frozen_by_id[crossing_id]
        height_sign = _sign_excluding_zero(height_difference, f"{crossing_id} height")
        determinant_sign = _sign_excluding_zero(determinant, f"{crossing_id} transversality")
        over, under = (left, right) if height_sign > 0 else (right, left)
        crossing_sign = height_sign * determinant_sign
        turn_match = (
            _contains_decimal(left_turn, expected.left_turn)
            and _contains_decimal(right_turn, expected.right_turn)
        )
        turns_enclosed = turns_enclosed and turn_match
        height_agreement = height_agreement and over == expected.over and under == expected.under
        sign_agreement = sign_agreement and crossing_sign == expected.sign
        rows.append(GenericIntervalCrossingCertificate(
            crossing_id=crossing_id,
            left_turn_lower=left_turn.lower_decimal(),
            left_turn_upper=left_turn.upper_decimal(),
            right_turn_lower=right_turn.lower_decimal(),
            right_turn_upper=right_turn.upper_decimal(),
            left_smooth_segment=left_segment,
            right_smooth_segment=right_segment,
            height_difference_lower=height_difference.lower_decimal(),
            height_difference_upper=height_difference.upper_decimal(),
            transversality_lower=determinant.lower_decimal(),
            transversality_upper=determinant.upper_decimal(),
            certified_over=over,
            certified_under=under,
            certified_sign=crossing_sign,
        ))
    if not turns_enclosed:
        raise GenericIntervalCertificateError("a frozen turn is outside its reconstructed enclosure")
    if not height_agreement:
        raise GenericIntervalCertificateError("interval height order differs from frozen diagram")
    if not sign_agreement:
        raise GenericIntervalCertificateError("interval crossing sign differs from frozen diagram")
    return GenericIntervalDiagramCertificate(
        prime=prime,
        precision_bits=precision_bits,
        crossing_count=len(rows),
        frozen_crossing_count=len(frozen.crossings),
        all_turns_enclosed=turns_enclosed,
        all_height_orders_agree=height_agreement,
        all_crossing_signs_agree=sign_agreement,
        crossings=tuple(rows),
    )


def generic_interval_family_certificate() -> dict[str, object]:
    p7 = certify_generic_prime_diagram(7)
    p5 = certify_generic_prime_diagram(5)
    payload: dict[str, object] = {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "research_order": ["P7", "P5"],
        "source": {"name": SOURCE_NAME, "sha256": SOURCE_SHA256},
        "method": (
            "direct system-MPFR outward-rounded reconstruction of shifted equal-circle "
            "intersections, atan2 turns, smooth-field values, and tangent determinants"
        ),
        "mpfr_version": mpfr_version(),
        "p7": p7.as_dict(),
        "p5": p5.as_dict(),
        "complete_crossing_count": p7.crossing_count + p5.crossing_count,
        "selection_effect": "none",
        "standing": "computer-assisted interval certificate; not proof-assistant verified",
        "information_boundary": [
            "MPFR calls and interval formulas are readable and directed-rounded but not proof-assistant verified",
            "the replay certifies the frozen projection crossing combinatorics, not complete ambient isotopy",
            "no arithmetic, physical, spectral, or prime-emergence status transfers",
        ],
        "usage_guidance": {
            "test": "PYTHONPATH=src python -m pytest -q tests/test_prime_generic_interval_certificate.py",
            "regenerate": (
                "PYTHONPATH=src python -m ucns.prime_generic_interval_certificate "
                "generated/prime-generic-interval-family-certificate.json"
            ),
        },
        "next": [
            "derive the symbolic multivariable Alexander presentation and elementary ideals",
            "calculate length-four and higher Milnor invariants or finite nilpotent quotients",
            "preregister an invariant that may separate the two substantive phase co-winners",
        ],
    }
    payload["payload_sha256"] = _canonical_json_sha256(payload)
    return payload


def write_generic_interval_family_certificate(path: str | Path, *, indent: int = 2) -> Path:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(generic_interval_family_certificate(), indent=indent, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    write_generic_interval_family_certificate(args.output)
