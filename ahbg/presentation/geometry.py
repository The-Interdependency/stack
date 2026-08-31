"""Seed of Life presentation geometry.

The tile is the centerpoint. Each circle has radius equal to the distance
between adjacent centers. This module renders geometry; it does not define game
movement or adjacency authority.
"""

from __future__ import annotations

import math
from typing import Sequence


def axial_to_xy(q: int, r: int, radius: float) -> tuple[float, float]:
    """Map already-supplied axial coordinates into presentation pixels."""

    if radius <= 0:
        raise ValueError("radius must be positive")
    return (radius * (q + r / 2), radius * (math.sqrt(3) / 2) * r)


def center_distance(left: tuple[float, float], right: tuple[float, float]) -> float:
    return math.hypot(left[0] - right[0], left[1] - right[1])


def visual_one_radius_pairs(
    tiles: Sequence[tuple[int, int]], radius: float
) -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
    """Return center pairs one display radius apart; presentation use only."""

    points = {item: axial_to_xy(item[0], item[1], radius) for item in tiles}
    pairs = []
    items = list(tiles)
    for index, left in enumerate(items):
        for right in items[index + 1 :]:
            if math.isclose(
                center_distance(points[left], points[right]),
                radius,
                rel_tol=1e-9,
                abs_tol=1e-9,
            ):
                pairs.append((left, right))
    return tuple(pairs)
