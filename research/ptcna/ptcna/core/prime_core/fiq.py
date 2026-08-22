# ratios: loc_comments=29:58 imports_exports=4:3 calls_definitions=5:6
"""Non-differentiating fiq payload host.

A fiq preserves an ordered payload vector and carrier-local identity. It does
not create scalar objects, inspect gradients, or participate in
back-propagation. Neural-owned objects such as ``ptcna.neural.NeuralScalar``
may travel inside the payload unchanged.

Usage:

    from ptcna.core.prime_core import wrap_tensor_fiq

    value = object()
    fiq = wrap_tensor_fiq([value], anchor=0, identity="fiq:0")
    assert fiq.payload[0] is value
    assert fiq.requires_grad is False
"""
from __future__ import annotations

from collections.abc import Iterable
from typing import Any, Optional

# === MODULE_BUILD ===
# id: ptcna_fiq_host
#   module_name: fiq
#   module_kind: schema
#   summary: preserves opaque payload vectors inside a non-differentiating core timing host
#   owner: Erin Spencer
#   public_surface: Fiq, wrap_tensor_fiq
#   internal_surface: Fiq._payload
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: ptcna/core/prime_core/tests/test_fiq_opaque.py
#   rollout: default enabled for prime-core construction
#   rollback: remove prime-core construction and fiq exports
#   requires: none
#   since: 0.1.1
#   unresolved: exact future UCNS carrier attachment
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: fiq_payload_is_opaque_and_lossless
#   given: arbitrary payload objects are wrapped in a fiq
#   then: each retrieved payload element is the identical object supplied by the caller
#   class: correctness
#
# id: fiq_never_owns_gradients
#   given: a fiq carries neural-owned differentiable objects
#   then: the fiq reports requires_grad false and exposes no backward operation or gradient state
#   class: safety
# === END CONTRACTS ===

# === BOUNDARIES ===
# id: fiq_runtime_boundary
#   summary: retains caller-provided object references in memory without inspecting content or touching external state
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


class Fiq:
    """Opaque payload vector at one local circle input position."""

    __slots__ = ("anchor", "_payload", "identity")

    def __init__(
        self,
        payload: Iterable[Any],
        anchor: int,
        identity: Optional[str] = None,
    ) -> None:
        self.anchor = anchor
        self._payload = list(payload)
        self.identity = identity

    @property
    def payload(self) -> list[Any]:
        return self._payload

    @property
    def requires_grad(self) -> bool:
        return False

    def __len__(self) -> int:
        return len(self._payload)


def wrap_tensor_fiq(
    values: Iterable[Any],
    anchor: int,
    identity: Optional[str] = None,
) -> Fiq:
    """Host values unchanged; never lift them into a core-owned scalar type."""

    return Fiq(payload=values, anchor=anchor, identity=identity)


__all__ = ["Fiq", "wrap_tensor_fiq"]
# ratios: loc_comments=29:58 imports_exports=4:3 calls_definitions=5:6
