# === MODULE_BUILD ===
# id: ucns_prime_interval_common
#   module_name: prime_interval_common
#   module_kind: experiment
#   summary: shared constants and dependency guards for readable interval and boundary research
#   owner: Erin Spencer
#   public_surface: internal readable implementation used through the declared facade
#   internal_surface: module implementation
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_interval_boundary_links.py
#   rollout: readable implementation; authority remains with the facade contracts
#   rollback: remove only with the owning consolidated research layer
#   requires: ucns_prime_smooth_ribbons_p7_p5
#   since: 2026-08-11
#   unresolved: see owning facade contracts and research document
# === END MODULE_BUILD ===

# === CONTRACTS ===
# Internal helper: behavioral obligations are declared by the owning facade and witnessed by its tests.
# id: prime_interval_common_is_facade_witnessed
#   given: the owning facade invokes this readable helper
#   then: the helper behavior is exercised through the named facade test without becoming a separate certificate
#   class: evidence
#   since: 2026-08-11
#
# === END CONTRACTS ===

"""Shared constants and dependency boundaries for interval and link research."""
from __future__ import annotations

from fractions import Fraction

from .prime_smooth_ribbons import (
    CENTERLINE_SEPARATION_TARGET,
    RIBBON_SEPARATION_LOWER_BOUND,
)

SCHEMA_ID = "ucns.prime-interval-boundary-links"
SCHEMA_VERSION = "0.1.0"
SOURCE_NAME = "Möbius Strips and Quantum Geometry.txt"
SOURCE_SHA256 = "dc3a94ca5070ffff8f2a246f48db77192b08f521e721bc7c2a011aa05ddeb9a1"
SOURCE_LINES = (5, 6, 13, 14, 15, 16, 17)
INTERVAL_DPS = 70
INTERVAL_MAX_DEPTH = 40
INTERVAL_MAX_BOXES_PER_PAIR = 100_000
GENERIC_PROJECTION_DPS = 80
GENERIC_TRANSLATION_BOUND = Fraction(7, 5000)
GENERIC_ISOTOPY_CLEARANCE = (
    RIBBON_SEPARATION_LOWER_BOUND - 2 * GENERIC_TRANSLATION_BOUND
)
GENERIC_CENTER_X = Fraction(137, 10_000_000)
GENERIC_CENTER_Y = Fraction(-223, 10_000_000)


class IntervalBoundaryError(ValueError):
    """Raised when a certificate leaves its declared mathematical boundary."""


def fraction_text(value: Fraction) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def require_mpmath():
    try:
        import mpmath as mp
    except ImportError as error:
        raise IntervalBoundaryError(
            "interval replay requires mpmath>=1.3,<2"
        ) from error
    return mp


def require_sympy():
    try:
        import sympy as sp
        from sympy.matrices.normalforms import smith_normal_form
        from sympy.polys.domains import ZZ
    except ImportError as error:
        raise IntervalBoundaryError(
            "integer normal forms require sympy>=1.12,<2"
        ) from error
    return sp, smith_normal_form, ZZ
