# ratios: loc_comments=54:71 imports_exports=6:2 calls_definitions=9:9
"""Seed-layer tensor objects for composing circle tensors into seeds.

The seed layer imports the circle type owned by ``ptcna.circle`` and organizes
a variable number of those circles into a seed tensor. It never defines a
second circle type.

Usage:

    from ptcna.circle import compose_circle
    from ptcna.seed import compose_seed

    seed = compose_seed([compose_circle(["n0"])])

The seed preserves payload identity and ordering; it does not create gradients
or claim a UCNS representation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Tuple

from ..circle import CircleTensor

# === MODULE_BUILD ===
# module_id: ptcna.seed.tensor
# purpose: host shared circle tensors in a non-differentiating seed structure
# inputs: CircleTensor sequences, routing step, anchor order, optional identity
# outputs: Seed, SeedMotion
# nondeterminism: none
# side_effects: none
# public_surface: Seed, SeedMotion
# internal_deps: ptcna.circle.CircleTensor
# external_deps: python standard library
# rollout: default enabled
# hmmm:
#   unresolved: exact future UCNS carrier profile
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: seed_hosts_shared_circle_type
#   given: a sequence of ptcna.circle.CircleTensor objects
#   then: Seed stores and returns those shared circle values without a duplicate circle class
#
# id: seed_payload_roundtrip
#   given: hosted circles with opaque payloads
#   then: tensor_payloads returns the exact payload objects in structural anchor order
#
# id: seed_is_non_differentiating
#   given: any valid Seed
#   then: requires_grad is false and the seed owns no backward operation
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
# abuse_cases: treating structural routing as a differentiable or UCNS-owned computation
# mitigations: immutable structural flags and explicit ownership boundary
# unresolved: exact future UCNS carrier and producer profile
# === END BOUNDARIES ===


class Seed:
    """A seed tensor: a star-polygon grouping of a variable number of circles.

    The seed is itself a tensor (it can be hosted by a core-layer core exactly
    as a circle is hosted here). Its geometry — the anchor visitation order — is
    frozen structural scaffold produced by ``compose_seed``; it does not learn.
    """

    __slots__ = (
        "circles",
        "routing_step",
        "anchor_order",
        "n_min",
        "face_state",
        "identity",
    )

    def __init__(
        self,
        circles: Sequence[CircleTensor],
        routing_step: int,
        anchor_order: Tuple[int, ...],
        identity: Optional[str] = None,
    ) -> None:
        self.circles: List[CircleTensor] = list(circles)
        self.routing_step = routing_step
        self.anchor_order = anchor_order
        self.n_min = len(self.circles)
        self.face_state = 0
        self.identity = identity

    @property
    def requires_grad(self) -> bool:
        return False

    @property
    def n_circles(self) -> int:
        return len(self.circles)

    def at(self, anchor: int) -> CircleTensor:
        """Retrieve the circle hosted at ``anchor`` (lossless round-trip)."""
        for c in self.circles:
            if c.anchor == anchor:
                return c
        raise KeyError(anchor)

    def circle_tensors(self) -> List[CircleTensor]:
        """The hosted circles in star-polygon anchor order (O(n))."""
        by_anchor = {c.anchor: c for c in self.circles}
        return [by_anchor[a] for a in self.anchor_order]

    def tensor_payloads(self) -> List[object]:
        """Flatten exact circle payloads without inspecting their contents."""

        payloads: List[object] = []
        for circle in self.circle_tensors():
            payloads.extend(circle.tensor_payloads())
        return payloads

    def __repr__(self) -> str:  # pragma: no cover - convenience only
        ident = f" {self.identity!r}" if self.identity else ""
        return f"<Seed{ident} circles={self.n_circles} order={self.anchor_order}>"


@dataclass(frozen=True)
class SeedMotion:
    """The structural **motion** a seed hands upward (to core-layer
    composition, and ultimately ZFAE inference).

    Formally, motion is the **Fickian flux** of the seed's composed field across
    the compose boundary — Fick's first law ``J = −D ∇φ`` (structure diffuses
    down its field gradient). This carrier captures the observable structure that
    flux rides on: the seed's identity and the star-polygon order its circles
    were routed in. It holds no weights and no autodiff gradient (those are
    the neural layer's `weights`, a separate channel); the ``∇φ`` is the spatial field
    gradient that drives diffusion, not a backprop gradient.
    """

    seed_identity: Optional[str]
    routing_step: int
    anchor_order: Tuple[int, ...]
    circle_identities: Tuple[Optional[str], ...] = field(default_factory=tuple)
# ratios: loc_comments=54:71 imports_exports=6:2 calls_definitions=9:9
