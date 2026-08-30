# ratios: loc_comments=145:89 imports_exports=10:5 calls_definitions=28:11
"""Compose fiqs through the shared circle and seed layers into a core.

This module no longer defines duplicate ``Circle`` or ``Seed`` classes.
``ptcna.circle.CircleTensor`` owns circles and ``ptcna.seed.Seed`` owns seeds.
The core hosts those structural objects and remains non-differentiating.

Usage:

    from ptcna.core.prime_core import CoreSpec, build_core

    core = build_core(CoreSpec(
        seed_count=2,
        circles_per_seed=2,
        tensors_per_circle=2,
        tensor_dim=3,
    ))
    assert core.requires_grad is False

Pass a ``payload_factory`` when neural-owned payload objects are required. The
factory owns their construction; PTCNA core composition carries them opaquely.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Optional

from ...circle import CircleTensor, compose_circle, star_polygon_order
from ...seed import Seed, compose_seed
from ...ucns_integration import (
    UCNSIntegrationStatus,
    ucns_integration_status,
)
from .constants import (
    CIRCLE_ROUTING_STEP,
    CIRCLES_PER_SEED,
    SEED_COUNT,
    SEED_ROUTING_STEP,
    TENSOR_DIM,
    TENSORS_PER_CIRCLE,
)
from .fiq import Fiq, wrap_tensor_fiq

# === MODULE_BUILD ===
# id: ptcna_prime_core_composition
#   module_name: prime core composition
#   module_kind: engine
#   summary: composes opaque fiqs through the shared circle and seed types into a non-differentiating core
#   owner: Erin Spencer
#   public_surface: CoreSpec, Core, build_core, compose_circle, compose_seed, heptagram_order
#   internal_surface: _local_fiq_identity
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: ptcna/core/prime_core/tests/test_ptca_core_stratified.py
#   rollout: exact default shape consumes the pinned UCNS candidate receipt; all other shapes remain locally attributed
#   rollback: remove prime-core exports; shared circle and seed layers remain available
#   requires: ptcna_fiq_host, ptcna_circle_composition, ptcna_seed_composition, ptcna_ucns_integration
#   since: 0.1.1
#   unresolved: continuous seven-fold geometry, representative efficacy, production privacy, and sustained-load behavior
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: prime_core_uses_shared_layer_types
#   given: a core is built from a CoreSpec
#   then: every circle is ptcna.circle.CircleTensor and every seed is ptcna.seed.Seed with no duplicate core-local layer types
#   class: correctness
#
# id: prime_core_is_non_differentiating
#   given: a core hosts payloads including neural-owned differentiable objects
#   then: core, seed, circle, and fiq hosts report requires_grad false and core exposes no backward operation
#   class: safety
#
# id: prime_core_ucns_receipt_scope_is_exact
#   given: a core is built with the exact 157x7x7x53 receipt-covered shape or a different shape
#   then: only the exact shape carries active UCNS state provenance while every different shape remains suspended and locally attributed
#   class: evidence
#
# id: prime_core_default_profile_is_stable
#   given: build_core is called with the default CoreSpec
#   then: the historical default profile contains 157 seeds, 7693 fiqs, and 407729 opaque payload values
#   class: compatibility
#
# id: prime_core_payload_width_matches_spec
#   given: a payload factory returns a vector whose length differs from tensor_dim
#   then: build_core raises ValueError before constructing an invalid fiq
#   class: safety
#
# id: prime_core_counts_are_positive
#   given: any CoreSpec composition count is zero or negative
#   then: CoreSpec raises ValueError naming the invalid field
#   class: safety
# === END CONTRACTS ===

# === BOUNDARIES ===
# id: prime_core_composition_runtime_boundary
#   summary: performs deterministic in-memory composition and creates no network, storage, auth, user-data, or external package effect
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

PayloadFactory = Callable[[int, int, int, int, float], Sequence[object]]


def heptagram_order(step: int, n: int = 7) -> list[int]:
    """Compatibility name for the shared star-polygon order."""

    return star_polygon_order(step, n)


def _local_fiq_identity(seed: int, circle: int, tensor: int) -> str:
    """Return a PTCNA-local identity with no UCNS representation claim."""

    return f"ptcna-local:fiq:{seed}.{circle}.{tensor}"


@dataclass(frozen=True)
class CoreSpec:
    """Variable composition counts for a core construction."""

    seed_count: int = SEED_COUNT
    circles_per_seed: int = CIRCLES_PER_SEED
    tensors_per_circle: int = TENSORS_PER_CIRCLE
    tensor_dim: int = TENSOR_DIM
    circle_routing_step: int = CIRCLE_ROUTING_STEP
    seed_routing_step: int = SEED_ROUTING_STEP

    def __post_init__(self) -> None:
        for field_name in (
            "seed_count",
            "circles_per_seed",
            "tensors_per_circle",
            "tensor_dim",
        ):
            if getattr(self, field_name) <= 0:
                raise ValueError(f"{field_name} must be positive")

    @property
    def tensor_leaves(self) -> int:
        return self.seed_count * self.circles_per_seed * self.tensors_per_circle

    @property
    def param_count(self) -> int:
        return self.tensor_leaves * self.tensor_dim


class Core:
    """A non-differentiating core tensor composed from shared seed objects."""

    __slots__ = ("seeds", "spec", "ucns_status")

    def __init__(
        self,
        seeds: Sequence[Seed],
        spec: CoreSpec,
        *,
        ucns_status: UCNSIntegrationStatus,
    ) -> None:
        self.seeds = list(seeds)
        self.spec = spec
        self.ucns_status = ucns_status

    @property
    def requires_grad(self) -> bool:
        return False

    def tensor_leaves(self) -> list[Fiq]:
        """Return hosted fiqs without inspecting their payload vectors."""

        leaves: list[Fiq] = []
        for seed in self.seeds:
            for payload in seed.tensor_payloads():
                if not isinstance(payload, Fiq):
                    raise TypeError(
                        "prime core circles must host Fiq payloads; "
                        f"received {type(payload).__name__}"
                    )
                leaves.append(payload)
        return leaves


def build_core(
    spec: Optional[CoreSpec] = None,
    *,
    init: float = 1.0,
    payload_factory: Optional[PayloadFactory] = None,
) -> Core:
    """Build a complete PTCNA core with shape-scoped UCNS attribution.

    ``payload_factory(seed, circle, tensor, tensor_dim, init)`` may return
    neural-owned objects. When omitted, each fiq hosts plain floats.
    """

    spec = spec or CoreSpec()
    seeds: list[Seed] = []
    for seed_index in range(spec.seed_count):
        circles: list[CircleTensor] = []
        for circle_index in range(spec.circles_per_seed):
            fiqs: list[Fiq] = []
            for tensor_index in range(spec.tensors_per_circle):
                if payload_factory is None:
                    values: Sequence[object] = [init] * spec.tensor_dim
                else:
                    values = payload_factory(
                        seed_index,
                        circle_index,
                        tensor_index,
                        spec.tensor_dim,
                        init,
                    )
                    if len(values) != spec.tensor_dim:
                        raise ValueError(
                            "payload_factory returned "
                            f"{len(values)} values; expected {spec.tensor_dim}"
                        )
                fiqs.append(
                    wrap_tensor_fiq(
                        values,
                        anchor=tensor_index,
                        identity=_local_fiq_identity(
                            seed_index,
                            circle_index,
                            tensor_index,
                        ),
                    )
                )
            circles.append(
                compose_circle(
                    fiqs,
                    routing_step=spec.circle_routing_step,
                    identity=f"ptcna-local:circle:{seed_index}.{circle_index}",
                )
            )
        seeds.append(
            compose_seed(
                circles,
                routing_step=spec.seed_routing_step,
                identity=f"ptcna-local:seed:{seed_index}",
            )
        )
    state_shape = (
        spec.seed_count,
        spec.circles_per_seed,
        spec.tensors_per_circle,
        spec.tensor_dim,
    )
    return Core(seeds, spec, ucns_status=ucns_integration_status(state_shape))


Circle = CircleTensor

__all__ = [
    "PayloadFactory",
    "CoreSpec",
    "Core",
    "Circle",
    "Seed",
    "build_core",
    "compose_circle",
    "compose_seed",
    "heptagram_order",
]
# ratios: loc_comments=145:89 imports_exports=10:5 calls_definitions=28:11
