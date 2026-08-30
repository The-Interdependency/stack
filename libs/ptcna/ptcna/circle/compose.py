# ratios: loc_comments=33:57 imports_exports=5:3 calls_definitions=14:2
"""Compose neural payloads into a non-differentiating circle tensor.

Usage:

    from ptcna.circle import compose_circle

    circle = compose_circle(["n0", "n1", "n2"], routing_step=2)
    assert circle.at(circle.anchor_order[0]) == "n0"

The routing is local PTCNA structure. The exact default aggregate may carry its
separate UCNS candidate-state receipt; this constructor does not grant that
provenance to arbitrary circles.
"""
from __future__ import annotations

from math import gcd
from typing import Optional, Sequence

from .tensor import CircleTensor

# === MODULE_BUILD ===
# id: ptcna_circle_composition
#   module_name: circle composition
#   module_kind: engine
#   summary: composes ordered neural payloads into a standalone non-differentiating circle tensor
#   owner: Erin Spencer
#   public_surface: star_polygon_order, compose_circle
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: ptcna/circle/tests/test_circle.py
#   rollout: default enabled as the neural-to-circle structural boundary
#   rollback: remove exports and restore audit-only circle behavior
#   requires: ptcna_circle_tensor, ptcna_ucns_integration
#   since: 0.1.1
#   unresolved: exact future UCNS carrier and higher-gonol composition profile
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: circle_composition_preserves_order_and_identity
#   given: one or more ordered payload objects and a routing step
#   then: composition assigns a deterministic complete anchor cycle or identity fallback and preserves every payload object
#   class: correctness
#
# id: circle_composition_rejects_empty_input
#   given: zero neural payloads
#   then: compose_circle raises ValueError instead of inventing an empty circle
#   class: safety
# === END CONTRACTS ===

# === BOUNDARIES ===
# id: circle_composition_runtime_boundary
#   summary: performs deterministic in-memory structural composition without activating UCNS or touching external state
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   pii: none
#   secrets: none
#   owner: Erin Spencer
#   since: 0.1.1
# === END BOUNDARIES ===


def star_polygon_order(step: int, n: int = 7) -> list[int]:
    """Return the complete ``{n/step}`` visitation order.

    A non-coprime step does not define one complete cycle and is rejected.
    """

    if n <= 0:
        raise ValueError("n must be positive")
    if gcd(step, n) != 1:
        raise ValueError(
            f"{{{n}/{step}}} is not a single cycle: gcd({step}, {n}) != 1"
        )
    return [(step * index) % n for index in range(n)]


def compose_circle(
    payloads: Sequence[object],
    *,
    routing_step: int = 2,
    identity: Optional[str] = None,
) -> CircleTensor:
    """Compose payloads into one standalone circle-layer tensor."""

    payloads = tuple(payloads)
    if not payloads:
        raise ValueError("cannot compose a circle from zero neural payloads")
    n = len(payloads)
    if gcd(routing_step, n) == 1:
        order = tuple(star_polygon_order(routing_step, n))
    else:
        order = tuple(range(n))
    return CircleTensor(
        payloads=payloads,
        routing_step=routing_step,
        anchor_order=order,
        identity=identity,
    )


__all__ = ["star_polygon_order", "compose_circle"]
# ratios: loc_comments=33:57 imports_exports=5:3 calls_definitions=14:2
