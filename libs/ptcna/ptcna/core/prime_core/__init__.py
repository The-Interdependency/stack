# ratios: loc_comments=44:12 imports_exports=4:1 calls_definitions=1:0
"""Prime-core composition using the shared PTCNA circle and seed layers.

Public surface (handoff §2 MODULE_BUILD):
    build_core, CoreSpec

Fiqs host payload vectors opaquely. The core, seeds, circles, and fiqs are all
non-differentiating. Neural-owned payloads may be supplied with
``build_core(..., payload_factory=...)`` without moving gradient ownership out
of ``ptcna.neural``. UCNS attribution is exact-shape and receipt scoped.
"""
from __future__ import annotations

from .constants import (
    CIRCLE_ROUTING_STEP,
    CIRCLES_PER_SEED,
    PARAM_COUNT,
    SEED_COUNT,
    SEED_ROUTING_STEP,
    TENSOR_DIM,
    TENSOR_LEAVES,
    TENSORS_PER_CIRCLE,
    is_coherence_prime,
)
from .core import (
    Circle,
    Core,
    CoreSpec,
    Seed,
    build_core,
    compose_circle,
    compose_seed,
    heptagram_order,
)
from .fiq import Fiq, wrap_tensor_fiq

__all__ = [
    # public surface
    "build_core",
    "CoreSpec",
    # strata
    "Core",
    "Seed",
    "Circle",
    "Fiq",
    # composition
    "compose_circle",
    "compose_seed",
    "wrap_tensor_fiq",
    "heptagram_order",
    # constants / guard
    "SEED_COUNT",
    "CIRCLES_PER_SEED",
    "TENSORS_PER_CIRCLE",
    "TENSOR_DIM",
    "TENSOR_LEAVES",
    "PARAM_COUNT",
    "CIRCLE_ROUTING_STEP",
    "SEED_ROUTING_STEP",
    "is_coherence_prime",
]
# ratios: loc_comments=44:12 imports_exports=4:1 calls_definitions=1:0
