# === MODULE_BUILD ===
# id: ucns_mpfr_interval
#   module_name: mpfr_interval
#   module_kind: experiment
#   summary: provides direct system-MPFR outward-rounded interval primitives for an independent P7/P5 separation replay
#   owner: Erin Spencer
#   public_surface: MPNumber, MPInterval, mpfr_version, atan2_interval, flat_step_interval
#   internal_surface: ctypes MPFR bindings with explicit directed rounding modes
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_independent_phase_milnor.py
#   rollout: independent interval backend only; certificate status does not transfer
#   rollback: remove with prime_independent_phase_milnor and its tests
#   requires: system libmpfr
#   since: 2026-08-11
#   unresolved: proof-assistant verification of the MPFR binding
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: prime_mpfr_replay_is_backend_independent
#   given: the frozen P7/P5 partition is replayed
#   then: direct system MPFR is used instead of the primary mpmath interval backend and the pinned partition identities match
#   class: evidence
#   since: 2026-08-11
#
# id: prime_mpfr_replay_recertifies_ribbon_margin
#   given: every frozen pair box is replayed with directed MPFR endpoints
#   then: both prime candidates retain lower endpoints above the declared centerline margin
#   class: evidence
#   since: 2026-08-11
# === END CONTRACTS ===

"""Minimal outward-rounded interval arithmetic backed directly by system MPFR.

This module deliberately avoids ``mpmath.iv``.  It calls ``libmpfr`` through
``ctypes`` and passes an explicit directed rounding mode to every primitive
operation used by the P7/P5 separation replay.
"""

from __future__ import annotations

import ctypes
import ctypes.util
from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Iterable

MPFR_RNDN = 0
MPFR_RNDZ = 1
MPFR_RNDU = 2
MPFR_RNDD = 3
MPFR_RNDA = 4
DEFAULT_PRECISION_BITS = 256


class MPFRError(RuntimeError):
    pass


class _MPFRStruct(ctypes.Structure):
    _fields_ = [
        ("_mpfr_prec", ctypes.c_long),
        ("_mpfr_sign", ctypes.c_int),
        ("_mpfr_exp", ctypes.c_long),
        ("_mpfr_d", ctypes.POINTER(ctypes.c_ulong)),
    ]


_LIB_NAME = ctypes.util.find_library("mpfr")
if not _LIB_NAME:
    raise MPFRError("libmpfr was not found")
_LIB = ctypes.CDLL(_LIB_NAME)
_PTR = ctypes.POINTER(_MPFRStruct)


def _bind(name: str, restype: object, *argtypes: object) -> object:
    fn = getattr(_LIB, name)
    fn.restype = restype
    fn.argtypes = list(argtypes)
    return fn


_mpfr_init2 = _bind("mpfr_init2", None, _PTR, ctypes.c_long)
_mpfr_clear = _bind("mpfr_clear", None, _PTR)
_mpfr_set_si = _bind("mpfr_set_si", ctypes.c_int, _PTR, ctypes.c_long, ctypes.c_int)
_mpfr_set_str = _bind("mpfr_set_str", ctypes.c_int, _PTR, ctypes.c_char_p, ctypes.c_int, ctypes.c_int)
_mpfr_set = _bind("mpfr_set", ctypes.c_int, _PTR, _PTR, ctypes.c_int)
_mpfr_neg = _bind("mpfr_neg", ctypes.c_int, _PTR, _PTR, ctypes.c_int)
_mpfr_add = _bind("mpfr_add", ctypes.c_int, _PTR, _PTR, _PTR, ctypes.c_int)
_mpfr_sub = _bind("mpfr_sub", ctypes.c_int, _PTR, _PTR, _PTR, ctypes.c_int)
_mpfr_mul = _bind("mpfr_mul", ctypes.c_int, _PTR, _PTR, _PTR, ctypes.c_int)
_mpfr_div = _bind("mpfr_div", ctypes.c_int, _PTR, _PTR, _PTR, ctypes.c_int)
_mpfr_sqrt = _bind("mpfr_sqrt", ctypes.c_int, _PTR, _PTR, ctypes.c_int)
_mpfr_exp = _bind("mpfr_exp", ctypes.c_int, _PTR, _PTR, ctypes.c_int)
_mpfr_sin = _bind("mpfr_sin", ctypes.c_int, _PTR, _PTR, ctypes.c_int)
_mpfr_cos = _bind("mpfr_cos", ctypes.c_int, _PTR, _PTR, ctypes.c_int)
_mpfr_atan2 = _bind("mpfr_atan2", ctypes.c_int, _PTR, _PTR, _PTR, ctypes.c_int)
_mpfr_const_pi = _bind("mpfr_const_pi", ctypes.c_int, _PTR, ctypes.c_int)
_mpfr_cmp = _bind("mpfr_cmp", ctypes.c_int, _PTR, _PTR)
_mpfr_sgn = _bind("mpfr_sgn", ctypes.c_int, _PTR)
_mpfr_get_d = _bind("mpfr_get_d", ctypes.c_double, _PTR, ctypes.c_int)
_mpfr_get_str = _bind(
    "mpfr_get_str",
    ctypes.c_void_p,
    ctypes.c_void_p,
    ctypes.POINTER(ctypes.c_long),
    ctypes.c_int,
    ctypes.c_size_t,
    _PTR,
    ctypes.c_int,
)
_mpfr_free_str = _bind("mpfr_free_str", None, ctypes.c_void_p)
_mpfr_get_version = _bind("mpfr_get_version", ctypes.c_char_p)


class MPNumber:
    """One owned MPFR number."""

    __slots__ = ("value", "precision", "_active")

    def __init__(self, precision: int = DEFAULT_PRECISION_BITS) -> None:
        if isinstance(precision, bool) or not isinstance(precision, int) or precision < 64:
            raise MPFRError("precision must be an integer >= 64")
        self.value = _MPFRStruct()
        self.precision = precision
        self._active = True
        _mpfr_init2(ctypes.byref(self.value), precision)

    def __del__(self) -> None:  # pragma: no cover - interpreter shutdown varies
        if getattr(self, "_active", False):
            _mpfr_clear(ctypes.byref(self.value))
            self._active = False

    @property
    def ptr(self) -> _PTR:
        return ctypes.byref(self.value)

    def copy(self, rounding: int = MPFR_RNDN) -> "MPNumber":
        out = MPNumber(self.precision)
        _mpfr_set(out.ptr, self.ptr, rounding)
        return out

    @classmethod
    def integer(
        cls,
        value: int,
        *,
        precision: int = DEFAULT_PRECISION_BITS,
        rounding: int = MPFR_RNDN,
    ) -> "MPNumber":
        if isinstance(value, bool) or not isinstance(value, int):
            raise MPFRError("MPFR integer input must be a nonboolean int")
        if not -(2**62) < value < 2**62:
            raise MPFRError("integer exceeds direct signed-long boundary")
        out = cls(precision)
        _mpfr_set_si(out.ptr, value, rounding)
        return out

    @classmethod
    def rational(
        cls,
        value: Fraction | int,
        *,
        precision: int = DEFAULT_PRECISION_BITS,
        rounding: int,
    ) -> "MPNumber":
        item = value if isinstance(value, Fraction) else Fraction(value)
        numerator = cls.integer(item.numerator, precision=precision)
        denominator = cls.integer(item.denominator, precision=precision)
        out = cls(precision)
        _mpfr_div(out.ptr, numerator.ptr, denominator.ptr, rounding)
        return out

    @classmethod
    def decimal_value(
        cls,
        value: str,
        *,
        precision: int = DEFAULT_PRECISION_BITS,
        rounding: int,
    ) -> "MPNumber":
        out = cls(precision)
        if _mpfr_set_str(out.ptr, value.encode("ascii"), 10, rounding) != 0:
            raise MPFRError(f"invalid MPFR decimal input: {value!r}")
        return out

    @classmethod
    def pi(cls, *, precision: int = DEFAULT_PRECISION_BITS, rounding: int) -> "MPNumber":
        out = cls(precision)
        _mpfr_const_pi(out.ptr, rounding)
        return out

    def compare(self, other: "MPNumber") -> int:
        return int(_mpfr_cmp(self.ptr, other.ptr))

    @property
    def sign(self) -> int:
        return int(_mpfr_sgn(self.ptr))

    def to_float(self, rounding: int = MPFR_RNDN) -> float:
        return float(_mpfr_get_d(self.ptr, rounding))

    def decimal(self, *, digits: int = 0, rounding: int = MPFR_RNDN) -> str:
        exponent = ctypes.c_long()
        raw = _mpfr_get_str(None, ctypes.byref(exponent), 10, digits, self.ptr, rounding)
        if not raw:
            raise MPFRError("mpfr_get_str failed")
        try:
            mantissa = ctypes.string_at(raw).decode("ascii")
        finally:
            _mpfr_free_str(raw)
        sign = ""
        if mantissa.startswith("-"):
            sign, mantissa = "-", mantissa[1:]
        if not mantissa:
            return "0"
        exp = exponent.value
        if mantissa == "0":
            return "0"
        return f"{sign}0.{mantissa}e{exp}"


def _binary(name: str, left: MPNumber, right: MPNumber, rounding: int) -> MPNumber:
    out = MPNumber(max(left.precision, right.precision))
    fn = {"add": _mpfr_add, "sub": _mpfr_sub, "mul": _mpfr_mul, "div": _mpfr_div}[name]
    fn(out.ptr, left.ptr, right.ptr, rounding)
    return out


def _unary(name: str, value: MPNumber, rounding: int) -> MPNumber:
    out = MPNumber(value.precision)
    fn = {"neg": _mpfr_neg, "sqrt": _mpfr_sqrt, "exp": _mpfr_exp, "sin": _mpfr_sin, "cos": _mpfr_cos}[name]
    fn(out.ptr, value.ptr, rounding)
    return out


def _minimum(values: Iterable[MPNumber]) -> MPNumber:
    rows = list(values)
    if not rows:
        raise MPFRError("minimum of empty sequence")
    best = rows[0]
    for item in rows[1:]:
        if item.compare(best) < 0:
            best = item
    return best.copy(MPFR_RNDD)


def _maximum(values: Iterable[MPNumber]) -> MPNumber:
    rows = list(values)
    if not rows:
        raise MPFRError("maximum of empty sequence")
    best = rows[0]
    for item in rows[1:]:
        if item.compare(best) > 0:
            best = item
    return best.copy(MPFR_RNDU)


@dataclass(frozen=True, slots=True)
class MPInterval:
    lo: MPNumber
    hi: MPNumber

    def __post_init__(self) -> None:
        if self.lo.compare(self.hi) > 0:
            raise MPFRError("interval endpoints are reversed")

    @property
    def precision(self) -> int:
        return max(self.lo.precision, self.hi.precision)

    @classmethod
    def rational(
        cls,
        value: Fraction | int,
        *,
        precision: int = DEFAULT_PRECISION_BITS,
    ) -> "MPInterval":
        return cls(
            MPNumber.rational(value, precision=precision, rounding=MPFR_RNDD),
            MPNumber.rational(value, precision=precision, rounding=MPFR_RNDU),
        )

    @classmethod
    def pi(cls, *, precision: int = DEFAULT_PRECISION_BITS) -> "MPInterval":
        return cls(
            MPNumber.pi(precision=precision, rounding=MPFR_RNDD),
            MPNumber.pi(precision=precision, rounding=MPFR_RNDU),
        )

    @classmethod
    def decimal(cls, value: str, *, precision: int = DEFAULT_PRECISION_BITS) -> "MPInterval":
        return cls(
            MPNumber.decimal_value(value, precision=precision, rounding=MPFR_RNDD),
            MPNumber.decimal_value(value, precision=precision, rounding=MPFR_RNDU),
        )

    @classmethod
    def exact_zero(cls, *, precision: int = DEFAULT_PRECISION_BITS) -> "MPInterval":
        return cls.rational(0, precision=precision)

    def __neg__(self) -> "MPInterval":
        return MPInterval(_unary("neg", self.hi, MPFR_RNDD), _unary("neg", self.lo, MPFR_RNDU))

    def __add__(self, other: "MPInterval") -> "MPInterval":
        return MPInterval(
            _binary("add", self.lo, other.lo, MPFR_RNDD),
            _binary("add", self.hi, other.hi, MPFR_RNDU),
        )

    def __sub__(self, other: "MPInterval") -> "MPInterval":
        return MPInterval(
            _binary("sub", self.lo, other.hi, MPFR_RNDD),
            _binary("sub", self.hi, other.lo, MPFR_RNDU),
        )

    def __mul__(self, other: "MPInterval") -> "MPInterval":
        down = [
            _binary("mul", a, b, MPFR_RNDD)
            for a in (self.lo, self.hi)
            for b in (other.lo, other.hi)
        ]
        up = [
            _binary("mul", a, b, MPFR_RNDU)
            for a in (self.lo, self.hi)
            for b in (other.lo, other.hi)
        ]
        return MPInterval(_minimum(down), _maximum(up))

    def __truediv__(self, other: "MPInterval") -> "MPInterval":
        if other.lo.sign <= 0 <= other.hi.sign:
            raise MPFRError("interval division by an interval containing zero")
        down = [
            _binary("div", a, b, MPFR_RNDD)
            for a in (self.lo, self.hi)
            for b in (other.lo, other.hi)
        ]
        up = [
            _binary("div", a, b, MPFR_RNDU)
            for a in (self.lo, self.hi)
            for b in (other.lo, other.hi)
        ]
        return MPInterval(_minimum(down), _maximum(up))

    def square(self) -> "MPInterval":
        zero = MPNumber.integer(0, precision=self.precision)
        if self.lo.sign >= 0:
            return MPInterval(
                _binary("mul", self.lo, self.lo, MPFR_RNDD),
                _binary("mul", self.hi, self.hi, MPFR_RNDU),
            )
        if self.hi.sign <= 0:
            return MPInterval(
                _binary("mul", self.hi, self.hi, MPFR_RNDD),
                _binary("mul", self.lo, self.lo, MPFR_RNDU),
            )
        upper = _maximum(
            (
                _binary("mul", self.lo, self.lo, MPFR_RNDU),
                _binary("mul", self.hi, self.hi, MPFR_RNDU),
            )
        )
        return MPInterval(zero, upper)

    def sqrt(self) -> "MPInterval":
        if self.lo.sign < 0:
            raise MPFRError("square root of interval extending below zero")
        return MPInterval(_unary("sqrt", self.lo, MPFR_RNDD), _unary("sqrt", self.hi, MPFR_RNDU))

    def exp(self) -> "MPInterval":
        return MPInterval(_unary("exp", self.lo, MPFR_RNDD), _unary("exp", self.hi, MPFR_RNDU))

    def lower_exceeds(self, other: "MPInterval") -> bool:
        return self.lo.compare(other.hi) > 0

    def upper_compare(self, other: "MPInterval") -> int:
        return self.hi.compare(other.hi)

    def lower_float(self) -> float:
        return self.lo.to_float(MPFR_RNDD)

    def upper_float(self) -> float:
        return self.hi.to_float(MPFR_RNDU)

    def lower_decimal(self) -> str:
        return self.lo.decimal(rounding=MPFR_RNDD)

    def upper_decimal(self) -> str:
        return self.hi.decimal(rounding=MPFR_RNDU)


def mpfr_version() -> str:
    return _mpfr_get_version().decode("ascii")


def sin_turn(turn: Fraction, *, precision: int = DEFAULT_PRECISION_BITS) -> MPInterval:
    target = turn % 1
    exact = {
        Fraction(0): Fraction(0),
        Fraction(1, 4): Fraction(1),
        Fraction(1, 2): Fraction(0),
        Fraction(3, 4): Fraction(-1),
    }
    if target in exact:
        return MPInterval.rational(exact[target], precision=precision)
    angle = MPInterval.pi(precision=precision) * MPInterval.rational(2 * target, precision=precision)
    lows = (_unary("sin", angle.lo, MPFR_RNDD), _unary("sin", angle.hi, MPFR_RNDD))
    highs = (_unary("sin", angle.lo, MPFR_RNDU), _unary("sin", angle.hi, MPFR_RNDU))
    return MPInterval(_minimum(lows), _maximum(highs))


def cos_turn(turn: Fraction, *, precision: int = DEFAULT_PRECISION_BITS) -> MPInterval:
    target = turn % 1
    exact = {
        Fraction(0): Fraction(1),
        Fraction(1, 4): Fraction(0),
        Fraction(1, 2): Fraction(-1),
        Fraction(3, 4): Fraction(0),
    }
    if target in exact:
        return MPInterval.rational(exact[target], precision=precision)
    angle = MPInterval.pi(precision=precision) * MPInterval.rational(2 * target, precision=precision)
    lows = (_unary("cos", angle.lo, MPFR_RNDD), _unary("cos", angle.hi, MPFR_RNDD))
    highs = (_unary("cos", angle.lo, MPFR_RNDU), _unary("cos", angle.hi, MPFR_RNDU))
    return MPInterval(_minimum(lows), _maximum(highs))


def flat_step_point(value: Fraction, *, precision: int = DEFAULT_PRECISION_BITS) -> MPInterval:
    if value <= 0:
        return MPInterval.rational(0, precision=precision)
    if value >= 1:
        return MPInterval.rational(1, precision=precision)
    x = MPInterval.rational(value, precision=precision)
    one = MPInterval.rational(1, precision=precision)
    minus_one = MPInterval.rational(-1, precision=precision)
    left = (minus_one / x).exp()
    right = (minus_one / (one - x)).exp()
    return left / (left + right)


def flat_step_interval(value: MPInterval) -> MPInterval:
    """Enclose the standard flat step on an interval contained in ``(0, 1)``.

    The flat step is strictly increasing on that domain, so evaluating its
    interval expression with directed rounding gives a valid enclosure.
    Endpoint values zero and one are handled exactly; an interval crossing an
    endpoint fails closed because the generic-diagram replay never needs that
    wider case.
    """

    zero = MPInterval.rational(0, precision=value.precision)
    one = MPInterval.rational(1, precision=value.precision)
    if value.lo.compare(zero.lo) == 0 and value.hi.compare(zero.hi) == 0:
        return zero
    if value.lo.compare(one.lo) == 0 and value.hi.compare(one.hi) == 0:
        return one
    if value.lo.sign <= 0 or value.hi.compare(one.lo) >= 0:
        raise MPFRError("flat-step interval must be strictly inside (0, 1)")
    minus_one = MPInterval.rational(-1, precision=value.precision)
    left = (minus_one / value).exp()
    right = (minus_one / (one - value)).exp()
    return left / (left + right)


def atan2_interval(y: MPInterval, x: MPInterval) -> MPInterval:
    """Return a directed-rounded principal ``atan2(y, x)`` enclosure.

    Corner extrema enclose ``atan2`` on a rectangle that excludes the origin
    and does not cross its negative-real-axis branch cut.  Those conditions are
    checked explicitly.  This bounded primitive is sufficient for the narrow
    circle-intersection boxes used by the generic-diagram certificate.
    """

    if x.lo.sign <= 0 <= x.hi.sign and y.lo.sign <= 0 <= y.hi.sign:
        raise MPFRError("atan2 interval rectangle contains the origin")
    if x.hi.sign < 0 and y.lo.sign <= 0 <= y.hi.sign:
        raise MPFRError("atan2 interval crosses the negative-axis branch cut")
    precision = max(x.precision, y.precision)
    down: list[MPNumber] = []
    up: list[MPNumber] = []
    for y_endpoint in (y.lo, y.hi):
        for x_endpoint in (x.lo, x.hi):
            lower = MPNumber(precision)
            upper = MPNumber(precision)
            _mpfr_atan2(lower.ptr, y_endpoint.ptr, x_endpoint.ptr, MPFR_RNDD)
            _mpfr_atan2(upper.ptr, y_endpoint.ptr, x_endpoint.ptr, MPFR_RNDU)
            down.append(lower)
            up.append(upper)
    return MPInterval(_minimum(down), _maximum(up))
