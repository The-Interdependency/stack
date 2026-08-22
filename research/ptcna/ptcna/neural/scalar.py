# ratios: loc_comments=62:61 imports_exports=4:2 calls_definitions=21:7
"""Neural-owned reverse-mode scalar.

This is the only scalar type in PTCNA that owns gradient state or
back-propagation. Circle, seed, fiq, and core objects may carry instances
opaquely, but those structural hosts never inspect gradients and always report
``requires_grad = False``.

Usage:

    from ptcna.neural import NeuralScalar

    weight = NeuralScalar(2.0)
    loss = weight * 3.0
    loss.backward()
    assert weight.grad == 3.0

Create losses and call ``backward`` in neural-layer code. Passing a
``NeuralScalar`` through a structural layer does not transfer gradient
ownership to that layer.
"""
from __future__ import annotations

from collections.abc import Iterable
from typing import Callable

# === MODULE_BUILD ===
# id: ptcna_neural_scalar
#   module_name: neural scalar
#   module_kind: engine
#   summary: owns PTCNA reverse-mode scalar operations and back-propagation exclusively inside the neural layer
#   owner: Erin Spencer
#   public_surface: NeuralScalar
#   internal_surface: NeuralScalar._backward, NeuralScalar._prev, NeuralScalar._op
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: ptcna/neural/tests/test_scalar.py
#   rollout: default enabled as the sole PTCNA differentiable leaf type
#   rollback: remove neural scalar exports and all neural call sites
#   requires: none
#   since: 0.1.1
#   unresolved: none
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: neural_scalar_owns_backprop
#   given: a loss graph composed from NeuralScalar addition and multiplication
#   then: backward accumulates gradients only on NeuralScalar nodes
#   class: correctness
#
# id: neural_scalar_uses_no_structural_operator
#   given: a NeuralScalar computation graph
#   then: every recorded operation is scalar addition, scalar multiplication, or a leaf; structural composition never enters the tape
#   class: safety
# === END CONTRACTS ===

# === BOUNDARIES ===
# id: neural_scalar_runtime_boundary
#   summary: performs in-memory scalar arithmetic without persistence, network access, or user-data handling
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


class NeuralScalar:
    """Minimal reverse-mode autodiff scalar owned by ``ptcna.neural``."""

    __slots__ = ("data", "grad", "_backward", "_prev", "_op")

    def __init__(
        self,
        data: float,
        _children: Iterable["NeuralScalar"] = (),
        _op: str = "",
    ) -> None:
        self.data = float(data)
        self.grad = 0.0
        self._backward: Callable[[], None] = lambda: None
        self._prev = tuple(_children)
        self._op = _op

    @property
    def requires_grad(self) -> bool:
        return True

    def __add__(self, other: "NeuralScalar | float") -> "NeuralScalar":
        other = other if isinstance(other, NeuralScalar) else NeuralScalar(other)
        out = NeuralScalar(self.data + other.data, (self, other), "+")

        def _backward() -> None:
            self.grad += out.grad
            other.grad += out.grad

        out._backward = _backward
        return out

    __radd__ = __add__

    def __mul__(self, other: "NeuralScalar | float") -> "NeuralScalar":
        other = other if isinstance(other, NeuralScalar) else NeuralScalar(other)
        out = NeuralScalar(self.data * other.data, (self, other), "*")

        def _backward() -> None:
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad

        out._backward = _backward
        return out

    __rmul__ = __mul__

    def backward(self) -> None:
        """Accumulate reverse-mode gradients without recursive traversal."""

        topo: list[NeuralScalar] = []
        visited: set[int] = set()
        stack: list[tuple[NeuralScalar, bool]] = [(self, False)]
        while stack:
            node, processed = stack.pop()
            if processed:
                topo.append(node)
                continue
            if id(node) in visited:
                continue
            visited.add(id(node))
            stack.append((node, True))
            for child in node._prev:
                if id(child) not in visited:
                    stack.append((child, False))
        self.grad = 1.0
        for node in reversed(topo):
            node._backward()

    def __repr__(self) -> str:
        return (
            f"NeuralScalar(data={self.data:.6g}, grad={self.grad:.6g}, "
            f"op={self._op!r})"
        )


__all__ = ["NeuralScalar"]
# ratios: loc_comments=62:61 imports_exports=4:2 calls_definitions=21:7
