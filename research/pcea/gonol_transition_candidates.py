"""Stack-local recursive gonol transition candidates.

This module treats ``157 -> 2881 -> 54837698421`` as observed research data.
It does not import UCNS, does not import PCEA, and does not search for or claim
an existing UCNS constructor. Candidate rules are evaluated as provisional
transition controls only.
"""

# === MODULE_BUILD ===
# id: pcea_gonol_transition_candidates
#   module_name: gonol_transition_candidates
#   module_kind: experiment
#   summary: derives falsified stack-local transition families and one interpolation control from the observed three-value sequence without claiming UCNS or PCEA canon
#   owner: The Interdependency
#   public_surface: OBSERVED_GONOLS, CandidateResult, evaluate_candidates, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _require_three_observations, _result_payload, _constant_delta, _constant_ratio, _integer_affine, _rational_affine_integer_output, _constant_square_offset, _quadratic_forward_difference
#   auth_boundary: none; consumes research/pcea/BASE.json and user-supplied observed data only
#   storage_boundary: read research/pcea/BASE.json; no writes at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research.pcea.tests.test_gonol_transition_candidates
#   rollout: stack-local research module; not promoted to PCEA runtime, UCNS canon, or stack libs
#   rollback: remove this module, its tests, and its research report
#   requires: none
#   since: 2026-09-02
#   unresolved: actual UCNS recursive geometry; public authenticity receipts; whether any control prediction matches a future independently constructed gonol
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: transition_candidates_use_only_observed_sequence
#   given: the default candidate evaluation runs
#   then: the only numeric inputs are the three observed gonol values and the stack-local BASE.json identity
#   class: safety
#   since: 2026-09-02
#
# id: transition_candidates_falsify_failed_families
#   given: simple additive, ratio, affine, rational-affine integer-output, and square-offset families are evaluated
#   then: each family that fails exact replay or integer next-value discipline is rejected with an explicit reason
#   class: evidence
#   since: 2026-09-02
#
# id: quadratic_forward_difference_is_control_only
#   given: the observed three-value sequence is evaluated under consecutive scale indices
#   then: the constant-second-difference quadratic is labeled as an interpolation control and emits one integer next-gonol prediction without empirical-confirmation language
#   class: evidence
#   since: 2026-09-02
#
# id: gonol_transition_receipt_replays_byte_identical
#   given: the same observed sequence and BASE.json identity
#   then: receipt bytes and receipt digest are identical across independent constructions
#   class: correctness
#   since: 2026-09-02
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Iterable


OBSERVED_GONOLS: tuple[int, int, int] = (157, 2881, 54837698421)
SCHEMA = "the-interdependency.stack-research.pcea.gonol-transition-candidates"
VERSION = "0.1.0"
STANDING = "stack-local-research"
CONTROL_STANDING = "interpolation-control-only"
STATUS_FALSIFIED = "FALSIFIED"
STATUS_CONTROL = "CONTROL"

NONCLAIMS: tuple[str, ...] = (
    "not a recovered UCNS constructor",
    "not PCEA runtime behavior",
    "not stack libs canon",
    "not cryptographic security evidence",
    "not entropy or hardness evidence",
    "not public authenticity or provenance proof",
    "not compared to any withheld PCEA prediction inside the receipt",
)

HMMM: tuple[str, ...] = (
    "actual UCNS recursive geometry that should own gonol construction",
    "whether any control prediction matches a future independently constructed gonol",
    "public authenticity receipts and verifier layer",
    "whether scale index 0,1,2 is the right independent variable",
)


@dataclass(frozen=True, slots=True)
class CandidateResult:
    """One candidate family result after exact replay and prediction checks."""

    candidate_id: str
    status: str
    standing: str
    rule: str
    replayed_observed: bool
    prediction: int | None
    rejection_reason: str | None
    parameters: tuple[tuple[str, str], ...]
    hmmm: tuple[str, ...]


def _fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _require_three_observations(values: Iterable[int]) -> tuple[int, int, int]:
    observed = tuple(values)
    if len(observed) != 3:
        raise ValueError("exactly three observed gonol values are required")
    if any(isinstance(value, bool) or not isinstance(value, int) for value in observed):
        raise TypeError("observed gonol values must be integers")
    if any(value <= 0 for value in observed):
        raise ValueError("observed gonol values must be positive")
    if len(set(observed)) != 3:
        raise ValueError("observed gonol values must be distinct for transition testing")
    return observed


def _result_payload(result: CandidateResult) -> dict[str, Any]:
    return {
        "candidate_id": result.candidate_id,
        "status": result.status,
        "standing": result.standing,
        "rule": result.rule,
        "replayed_observed": result.replayed_observed,
        "prediction": result.prediction,
        "rejection_reason": result.rejection_reason,
        "parameters": [[key, value] for key, value in result.parameters],
        "hmmm": list(result.hmmm),
    }


def _constant_delta(a: int, b: int, c: int) -> CandidateResult:
    first_delta = b - a
    second_delta = c - b
    if first_delta != second_delta:
        return CandidateResult(
            candidate_id="constant_delta",
            status=STATUS_FALSIFIED,
            standing="rejected",
            rule="g[n+1] = g[n] + d",
            replayed_observed=False,
            prediction=None,
            rejection_reason="observed deltas differ",
            parameters=(
                ("delta_0_to_1", str(first_delta)),
                ("delta_1_to_2", str(second_delta)),
            ),
            hmmm=(),
        )
    return CandidateResult(
        candidate_id="constant_delta",
        status=STATUS_CONTROL,
        standing=CONTROL_STANDING,
        rule="g[n+1] = g[n] + d",
        replayed_observed=True,
        prediction=c + second_delta,
        rejection_reason=None,
        parameters=(("delta", str(first_delta)),),
        hmmm=("only two transitions tested",),
    )


def _constant_ratio(a: int, b: int, c: int) -> CandidateResult:
    ratio_0 = Fraction(b, a)
    ratio_1 = Fraction(c, b)
    if ratio_0 != ratio_1:
        return CandidateResult(
            candidate_id="constant_ratio",
            status=STATUS_FALSIFIED,
            standing="rejected",
            rule="g[n+1] = r * g[n]",
            replayed_observed=False,
            prediction=None,
            rejection_reason="observed ratios differ",
            parameters=(
                ("ratio_0_to_1", _fraction_text(ratio_0)),
                ("ratio_1_to_2", _fraction_text(ratio_1)),
            ),
            hmmm=(),
        )
    prediction = ratio_1 * c
    return CandidateResult(
        candidate_id="constant_ratio",
        status=STATUS_CONTROL if prediction.denominator == 1 else STATUS_FALSIFIED,
        standing=CONTROL_STANDING if prediction.denominator == 1 else "rejected",
        rule="g[n+1] = r * g[n]",
        replayed_observed=True,
        prediction=prediction.numerator if prediction.denominator == 1 else None,
        rejection_reason=None if prediction.denominator == 1 else "next value is not an integer",
        parameters=(("ratio", _fraction_text(ratio_1)),),
        hmmm=("only two transitions tested",),
    )


def _integer_affine(a: int, b: int, c: int) -> CandidateResult:
    denominator = b - a
    numerator = c - b
    if denominator == 0 or numerator % denominator != 0:
        return CandidateResult(
            candidate_id="integer_affine",
            status=STATUS_FALSIFIED,
            standing="rejected",
            rule="g[n+1] = m * g[n] + k, m and k integers",
            replayed_observed=False,
            prediction=None,
            rejection_reason="no integer slope replays both observed transitions",
            parameters=(
                ("slope_numerator", str(numerator)),
                ("slope_denominator", str(denominator)),
            ),
            hmmm=(),
        )
    slope = numerator // denominator
    intercept = b - slope * a
    return CandidateResult(
        candidate_id="integer_affine",
        status=STATUS_CONTROL,
        standing=CONTROL_STANDING,
        rule="g[n+1] = m * g[n] + k, m and k integers",
        replayed_observed=True,
        prediction=slope * c + intercept,
        rejection_reason=None,
        parameters=(("m", str(slope)), ("k", str(intercept))),
        hmmm=("affine state-map assumption has no UCNS geometry",),
    )


def _rational_affine_integer_output(a: int, b: int, c: int) -> CandidateResult:
    denominator = b - a
    if denominator == 0:
        raise ValueError("affine denominator cannot be zero for distinct observations")
    slope = Fraction(c - b, denominator)
    intercept = Fraction(b) - slope * a
    prediction = slope * c + intercept
    if prediction.denominator != 1:
        return CandidateResult(
            candidate_id="rational_affine_integer_output",
            status=STATUS_FALSIFIED,
            standing="rejected",
            rule="g[n+1] = m * g[n] + k, m and k rational, next gonol must be integer",
            replayed_observed=True,
            prediction=None,
            rejection_reason="exact affine replay predicts a non-integer next gonol",
            parameters=(
                ("m", _fraction_text(slope)),
                ("k", _fraction_text(intercept)),
                ("raw_next", _fraction_text(prediction)),
            ),
            hmmm=(),
        )
    return CandidateResult(
        candidate_id="rational_affine_integer_output",
        status=STATUS_CONTROL,
        standing=CONTROL_STANDING,
        rule="g[n+1] = m * g[n] + k, m and k rational, next gonol must be integer",
        replayed_observed=True,
        prediction=prediction.numerator,
        rejection_reason=None,
        parameters=(("m", _fraction_text(slope)), ("k", _fraction_text(intercept))),
        hmmm=("rational coefficients have no UCNS geometry",),
    )


def _constant_square_offset(a: int, b: int, c: int) -> CandidateResult:
    offset_0 = b - a * a
    offset_1 = c - b * b
    if offset_0 != offset_1:
        return CandidateResult(
            candidate_id="constant_square_offset",
            status=STATUS_FALSIFIED,
            standing="rejected",
            rule="g[n+1] = g[n]^2 + k",
            replayed_observed=False,
            prediction=None,
            rejection_reason="square offsets differ",
            parameters=(
                ("offset_0_to_1", str(offset_0)),
                ("offset_1_to_2", str(offset_1)),
            ),
            hmmm=(),
        )
    return CandidateResult(
        candidate_id="constant_square_offset",
        status=STATUS_CONTROL,
        standing=CONTROL_STANDING,
        rule="g[n+1] = g[n]^2 + k",
        replayed_observed=True,
        prediction=c * c + offset_1,
        rejection_reason=None,
        parameters=(("k", str(offset_0)),),
        hmmm=("quadratic self-map assumption has no UCNS geometry",),
    )


def _quadratic_forward_difference(a: int, b: int, c: int) -> CandidateResult:
    delta_0 = b - a
    delta_1 = c - b
    second_difference = delta_1 - delta_0
    next_delta = delta_1 + second_difference
    prediction = c + next_delta
    coefficient_a = Fraction(second_difference, 2)
    coefficient_b = Fraction(delta_0) - coefficient_a
    return CandidateResult(
        candidate_id="quadratic_forward_difference_baseline",
        status=STATUS_CONTROL,
        standing=CONTROL_STANDING,
        rule="scale indices are consecutive and second finite difference is constant",
        replayed_observed=True,
        prediction=prediction,
        rejection_reason=None,
        parameters=(
            ("delta_0_to_1", str(delta_0)),
            ("delta_1_to_2", str(delta_1)),
            ("constant_second_difference", str(second_difference)),
            ("next_delta", str(next_delta)),
            ("index_polynomial_a", _fraction_text(coefficient_a)),
            ("index_polynomial_b", _fraction_text(coefficient_b)),
            ("index_polynomial_c", str(a)),
        ),
        hmmm=(
            "every three distinct indexed observations admit a quadratic",
            "no UCNS geometry selects constant second finite difference",
            "not empirical evidence until an independent gonol constructor lands here",
        ),
    )


def evaluate_candidates(values: Iterable[int] = OBSERVED_GONOLS) -> tuple[CandidateResult, ...]:
    """Evaluate candidate transition families against the observed sequence."""

    a, b, c = _require_three_observations(values)
    return (
        _constant_delta(a, b, c),
        _constant_ratio(a, b, c),
        _integer_affine(a, b, c),
        _rational_affine_integer_output(a, b, c),
        _constant_square_offset(a, b, c),
        _quadratic_forward_difference(a, b, c),
    )


def _load_base(base_path: Path | None = None) -> dict[str, Any]:
    path = base_path or Path(__file__).with_name("BASE.json")
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _producer_code_reference() -> str:
    path = Path(__file__)
    text = path.read_text(encoding="utf-8")
    return "sha256:" + sha256(text.encode("utf-8")).hexdigest()


def receipt_payload(
    values: Iterable[int] = OBSERVED_GONOLS,
    *,
    base_path: Path | None = None,
) -> dict[str, Any]:
    """Return the deterministic research receipt payload."""

    observed = _require_three_observations(values)
    candidates = evaluate_candidates(observed)
    controls = [item for item in candidates if item.status == STATUS_CONTROL]
    return {
        "schema": SCHEMA,
        "version": VERSION,
        "standing": STANDING,
        "producer_code_reference": _producer_code_reference(),
        "base": _load_base(base_path),
        "observed_data": {
            "sequence": list(observed),
            "origin": "user-corrected handoff observed data, 2026-09-02",
            "ucns_constructor_identity": "hmmm",
        },
        "candidate_policy": {
            "numeric_inputs": "observed_data.sequence only",
            "scale_indices": "consecutive 0,1,2 baseline only",
            "required_output_type": "positive integer gonol value",
            "falsification": "reject exact replay failures and non-integer next values",
            "control_vocab": "CONTROL means interpolation output, not empirical evidence",
            "withheld_prediction_comparison": "not performed inside this receipt",
            "first_actual_constructor_test": (
                "derive an operation from the 157-gonol constituent relations/closure "
                "to produce 2881, then apply the same operation to 2881 without using "
                "54837698421 as a target"
            ),
        },
        "candidates": [_result_payload(item) for item in candidates],
        "control_predictions": [
            {
                "candidate_id": item.candidate_id,
                "standing": item.standing,
                "next_gonol": item.prediction,
            }
            for item in controls
        ],
        "nonclaims": list(NONCLAIMS),
        "hmmm": list(HMMM),
    }


def receipt_bytes(payload: dict[str, Any] | None = None) -> bytes:
    """Serialize a receipt payload as canonical JSON bytes."""

    receipt = payload if payload is not None else receipt_payload()
    return json.dumps(
        receipt,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8") + b"\n"


def receipt_digest(payload: dict[str, Any] | None = None) -> str:
    """Return the SHA-256 digest of canonical receipt bytes."""

    return sha256(receipt_bytes(payload)).hexdigest()


def main() -> None:
    payload = receipt_payload()
    envelope = {
        "receipt_sha256": receipt_digest(payload),
        "receipt": payload,
    }
    print(json.dumps(envelope, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
