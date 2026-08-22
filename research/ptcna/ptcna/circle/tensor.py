# ratios: loc_comments=28:57 imports_exports=3:2 calls_definitions=6:6
"""Circle-layer structural tensor.

A ``CircleTensor`` is the non-differentiating circle produced from ordered
neural payloads. It owns only routing structure and identity. Payloads are
retained verbatim and may include neural-owned objects, but the circle never
inspects or mutates their gradient state.

Use ``ptcna.circle.compose_circle`` rather than constructing this class
directly. A seed layer may assign the circle an outer ``anchor`` with
``with_anchor`` without changing its internal payloads or routing order.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Optional

# === MODULE_BUILD ===
# id: ptcna_circle_tensor
#   module_name: circle tensor
#   module_kind: schema
#   summary: represents the non-differentiating circle-layer output that structurally hosts ordered neural payloads
#   owner: Erin Spencer
#   public_surface: CircleTensor
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: ptcna/circle/tests/test_circle.py
#   rollout: constructed through ptcna.circle.compose_circle
#   rollback: remove circle composition and restore seed-local opaque circle wrappers
#   requires: none
#   since: 0.1.1
#   unresolved: exact future UCNS carrier profile
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: circle_tensor_is_non_differentiating
#   given: a circle hosting payloads that may themselves be neural-owned differentiable objects
#   then: the circle reports requires_grad false and never creates or executes gradient operations
#   class: safety
#
# id: circle_tensor_round_trips_payloads
#   given: payloads composed into a circle under a star-polygon anchor order
#   then: each payload is recoverable by its assigned inner anchor as the identical object
#   class: correctness
# === END CONTRACTS ===

# === BOUNDARIES ===
# id: circle_tensor_runtime_boundary
#   summary: stores caller-provided payload references in memory and performs no persistence, network, auth, or user-data operation
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


@dataclass(frozen=True)
class CircleTensor:
    """A circle tensor with inner routing and an optional outer seed anchor."""

    payloads: tuple[Any, ...]
    routing_step: int
    anchor_order: tuple[int, ...]
    anchor: int = 0
    identity: Optional[str] = None
    carrier_profile: str = "ptcna.local-star-polygon/1"

    @property
    def requires_grad(self) -> bool:
        return False

    @property
    def n_tensors(self) -> int:
        return len(self.payloads)

    def at(self, anchor: int) -> Any:
        """Return the exact payload assigned to an inner circle anchor."""

        try:
            index = self.anchor_order.index(anchor)
        except ValueError as exc:
            raise KeyError(anchor) from exc
        return self.payloads[index]

    def tensor_payloads(self) -> list[Any]:
        """Return payloads in star-polygon visitation order."""

        return [self.at(anchor) for anchor in self.anchor_order]

    def with_anchor(self, anchor: int) -> "CircleTensor":
        """Return the same circle assigned to an outer seed anchor."""

        return replace(self, anchor=anchor)


__all__ = ["CircleTensor"]
# ratios: loc_comments=28:57 imports_exports=3:2 calls_definitions=6:6
