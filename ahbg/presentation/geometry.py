"""Seed of Life presentation geometry.

The tile is the centerpoint. Each circle has radius equal to the distance
between adjacent centers, so a circle passes through neighboring tile points.
This is graphics, not game mechanics.
"""

from __future__ import annotations

import math
from typing import Sequence


def axial_to_xy(q: int, r: int, radius: float) -> tuple[float, float]:
    """Map axial coordinates so adjacent centers are `radius` apart."""

    if radius <= 0:
        raise ValueError("radius must be positive")
    x = radius * (q + r / 2)
    y = radius * (math.sqrt(3) / 2) * r
    return (x, y)


def center_distance(left: tuple[float, float], right: tuple[float, float]) -> float:
    dx = left[0] - right[0]
    dy = left[1] - right[1]
    return math.hypot(dx, dy)


def adjacent_center_pairs(tiles: Sequence[tuple[int, int]], radius: float) -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
    """Pairs of axial tiles whose centers are one radius apart."""

    points = {item: axial_to_xy(item[0], item[1], radius) for item in tiles}
    pairs = []
    items = list(tiles)
    for i, left in enumerate(items):
        for right in items[i + 1 :]:
            if math.isclose(center_distance(points[left], points[right]), radius, rel_tol=1e-9, abs_tol=1e-9):
                pairs.append((left, right))
    return tuple(pairs)
