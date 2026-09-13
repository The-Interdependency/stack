# ratios: loc_comments=29:18 imports_exports=4:2 calls_definitions=20:2
# === CHECKS ===
# id: check_mpfr_nan_is_not_ordered_evidence
#   proves: mpfr_rejects_nan_ordering
#   call: self::test_nan_cannot_be_an_interval_or_an_ordering_witness
#   requires: python3, libmpfr
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_mpfr_exact_rational_admission
#   proves: mpfr_rational_inputs_are_exact
#   call: self::test_rational_admission_preserves_exact_input_boundary
#   requires: python3, libmpfr
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===

"""Run with pytest tests/test_mpfr_input_boundaries.py; requires system libmpfr."""

from fractions import Fraction
import math

import pytest

from ucns.mpfr_interval import MPFRError, MPInterval, MPNumber, MPFR_RNDD


def test_nan_cannot_be_an_interval_or_an_ordering_witness() -> None:
    for value in ("nan", "NaN", "@NaN@"):
        with pytest.raises(MPFRError):
            MPInterval.decimal(value)
    uninitialized = MPNumber()  # MPFR initializes a number to NaN.
    zero = MPNumber.integer(0)
    with pytest.raises(MPFRError):
        uninitialized.compare(zero)
    with pytest.raises(MPFRError):
        zero.compare(uninitialized)
    with pytest.raises(MPFRError):
        _ = uninitialized.sign
    with pytest.raises(MPFRError):
        MPInterval(uninitialized, zero)
    assert MPInterval.rational(0).lo.sign == 0


def test_rational_admission_preserves_exact_input_boundary() -> None:
    for invalid in (True, False, 0.1, "1/3"):
        with pytest.raises(MPFRError):
            MPInterval.rational(invalid)
    for value in (0, -3, Fraction(1, 3), Fraction(-7, 11)):
        interval = MPInterval.rational(value)
        assert Fraction.from_float(interval.lower_float()) <= value
        assert Fraction.from_float(interval.upper_float()) >= value
        assert math.isfinite(interval.lower_float())
    assert MPNumber.rational(Fraction(1, 2), rounding=MPFR_RNDD).to_float() == 0.5
# ratios: loc_comments=29:18 imports_exports=4:2 calls_definitions=20:2
