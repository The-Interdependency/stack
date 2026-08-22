# ratios: loc_comments=48:80 imports_exports=6:4 calls_definitions=16:4
"""The layer-2 composition operator: circles -> seed.

`compose_seed` is the structural ``⊠`` operator for layer 2. It is **purely
structural**: it grafts circle-tensors into a seed carrier and assigns their
star-polygon anchor order. It creates no scalar and registers no autodiff node, so
``∂(⊠)`` never appears on a tape (back-propagation lives only in the neural
layer, `ptcna.neural`). See `docs`/the stack canon for the boundary.

Use ``compose_seed`` for already-formed circles or ``build_seed`` for raw opaque
payloads. The result is local PTCNA structure and makes no UCNS claim.
"""
from __future__ import annotations

from math import gcd
from typing import Optional, Sequence

from ..circle import CircleTensor, compose_circle, star_polygon_order
from .constants import HEPTAGRAM_VERTICES, SEED_ROUTING_STEP
from .tensor import Seed, SeedMotion

# === MODULE_BUILD ===
# module_id: ptcna.seed.compose
# purpose: compose shared circle tensors into variable-width seed structure
# inputs: CircleTensor sequence, routing step, optional identity
# outputs: Seed, SeedMotion
# nondeterminism: none
# side_effects: none
# public_surface: heptagram_order, compose_seed, build_seed, seed_motion
# internal_deps: ptcna.circle, ptcna.seed.constants, ptcna.seed.tensor
# external_deps: python standard library
# rollout: default enabled
# hmmm:
#   unresolved: exact future UCNS higher-gonol producer composition law
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: seed_composition_uses_shared_circle_type
#   given: a non-empty sequence of ptcna.circle.CircleTensor objects
#   then: compose_seed returns a Seed whose circles remain that shared type
#
# id: seed_composition_is_non_differentiating
#   given: opaque payloads including neural scalars
#   then: composition creates no gradient node and preserves payload references
#
# id: seed_composition_rejects_empty
#   given: an empty circle sequence
#   then: compose_seed raises ValueError
# === END CONTRACTS ===

# === BOUNDARIES ===
# trust_zone: in_process
# data_classification: opaque caller payloads
# authn: none
# authz: none
# secrets: none
# network_boundary: none
# storage_boundary: none
# user_data: opaque payload references supplied by caller
# sandboxing: caller process
# privileged_ops: none
# abuse_cases: empty composition or labeling local routing as UCNS output
# mitigations: non-empty validation and explicit local ownership language
# unresolved: exact future UCNS producer profile and higher-gonol composition law
# === END BOUNDARIES ===


def heptagram_order(step: int, n: int = HEPTAGRAM_VERTICES) -> list[int]:
    """Vertex visitation order of the ``{n/step}`` star polygon.

    For ``n = 7``: ``step 2 -> [0,2,4,6,1,3,5]``; ``step 3 -> [0,3,6,2,5,1,4]``.
    Requires ``gcd(step, n) == 1`` so every vertex is visited exactly once.
    """
    return star_polygon_order(step, n)


def compose_seed(
    circles: Sequence[CircleTensor],
    *,
    routing_step: int = SEED_ROUTING_STEP,
    identity: Optional[str] = None,
) -> Seed:
    """Compose circle-tensors into a seed (the structural ``⊠`` operator).

    The circle count is **variable** — a seed may carry any number of circles
    (the invariant is only that every circle is a tensor and the seed is itself a
    tensor). Each circle is (re)assigned an ``anchor`` from the
    ``{n/routing_step}`` star-polygon order, preserving input order at the
    assigned positions; for the nominal ``n=7`` case this is the ``{7/3}``
    heptagram. Structural only — no autodiff node is created.
    """
    circles = list(circles)
    n = len(circles)
    if n == 0:
        raise ValueError("cannot compose a seed from zero circles")

    # Apply the {n/step} star-polygon order when it forms a single cycle
    # (gcd(step, n) == 1, e.g. the nominal {7/3} heptagram); otherwise fall back
    # to identity order — the star polygon is undefined when step and n share a
    # factor.
    if gcd(routing_step, n) == 1:
        order = heptagram_order(routing_step, n)
    else:
        order = list(range(n))
    # Assign anchors: the i-th input circle lands at heptagram position order[i].
    anchored = [circle.with_anchor(order[index]) for index, circle in enumerate(circles)]
    return Seed(
        circles=anchored,
        routing_step=routing_step,
        anchor_order=tuple(order),
        identity=identity,
    )


def build_seed(
    payloads: Sequence[object],
    *,
    routing_step: int = SEED_ROUTING_STEP,
    identity: Optional[str] = None,
) -> Seed:
    """Convenience builder: wrap raw circle payloads as ``CircleTensor``s and
    compose them into a seed. ``payloads[i]`` becomes the i-th input circle with
    identity ``"{identity}.c{i}"`` (or ``"c{i}"`` if no seed identity is given).
    Any number of payloads is accepted (composition counts are variable).
    """
    prefix = f"{identity}." if identity else ""
    circles = [
        compose_circle([payload], identity=f"{prefix}c{index}")
        for index, payload in enumerate(payloads)
    ]
    return compose_seed(circles, routing_step=routing_step, identity=identity)


def seed_motion(seed: Seed) -> SeedMotion:
    """Extract the structural **motion** a seed hands upward (toward the core
    composition and ultimately ZFAE inference).

    Returns the observable structure only — identity + star-polygon order — never
    weights or autodiff gradients. Formally, motion is the Fickian gradient flux
    ``J = −D ∇φ`` (Fick's first law) — the seed's composed field diffusing down
    its gradient; this carrier holds the structure that flux rides on.
    """
    return SeedMotion(
        seed_identity=seed.identity,
        routing_step=seed.routing_step,
        anchor_order=seed.anchor_order,
        circle_identities=tuple(c.identity for c in seed.circle_tensors()),
    )
# ratios: loc_comments=48:80 imports_exports=6:4 calls_definitions=16:4
