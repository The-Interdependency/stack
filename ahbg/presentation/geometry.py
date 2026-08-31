# === MODULE_BUILD ===
# id: ahbg_presentation_display_transform
#   module_name: geometry
#   module_kind: adapter
#   summary: scales already-supplied UCNS source coordinates into SVG display coordinates without reconstructing or selecting geometry
#   owner: AHBG presentation
#   public_surface: source_to_display, center_distance
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: ahbg/presentation/tests/test_presentation.py
#   rollout: used only by presentation tests and equivalent browser transform
#   rollback: inline display scaling or remove presentation package; no mechanics effect
#   requires: caller-supplied UCNS-derived x/y source coordinates
#   since: 2026-08-31
#   unresolved: none
# === END MODULE_BUILD ===

"""Presentation-only transform of source-backed center coordinates.

This module does not derive Seed-of-Life centers, adjacency, orientation, or
nesting. It only scales coordinates already supplied by the declared UCNS source
into display pixels; optional y inversion is the SVG screen-coordinate transform.

Usage guidance:
    ``source_to_display(x, y, scale=64.0)`` after validating the snapshot.
"""

from __future__ import annotations

import math


def source_to_display(
    x: float,
    y: float,
    scale: float,
    *,
    invert_y: bool = True,
) -> tuple[float, float]:
    """Scale source coordinates for display without changing their topology."""

    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise ValueError("x must be numeric and nonboolean")
    if isinstance(y, bool) or not isinstance(y, (int, float)):
        raise ValueError("y must be numeric and nonboolean")
    if isinstance(scale, bool) or not isinstance(scale, (int, float)) or scale <= 0:
        raise ValueError("scale must be positive numeric and nonboolean")
    return float(x) * float(scale), (-float(y) if invert_y else float(y)) * float(scale)


def center_distance(left: tuple[float, float], right: tuple[float, float]) -> float:
    """Measure distance between already-supplied source/display points."""

    return math.hypot(left[0] - right[0], left[1] - right[1])
