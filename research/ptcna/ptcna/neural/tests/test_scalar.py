"""Executable evidence for neural-owned scalar back-propagation."""

from ptcna.neural import NeuralScalar

# === CHECKS ===
# id: check_neural_scalar_backprop
#   proves: neural_scalar_owns_backprop
#   call: self::test_backward_accumulates_expected_gradient
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_neural_scalar_tape_ops
#   proves: neural_scalar_uses_no_structural_operator
#   call: self::test_tape_contains_only_neural_scalar_ops
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===


def test_backward_accumulates_expected_gradient() -> None:
    value = NeuralScalar(2.0)
    loss = value * 3.0 + value
    loss.backward()
    assert value.grad == 4.0


def test_tape_contains_only_neural_scalar_ops() -> None:
    left = NeuralScalar(2.0)
    right = NeuralScalar(4.0)
    loss = left * right + left
    seen: set[int] = set()
    stack = [loss]
    ops: set[str] = set()
    while stack:
        node = stack.pop()
        if id(node) in seen:
            continue
        seen.add(id(node))
        ops.add(node._op)
        stack.extend(node._prev)
    assert ops <= {"", "+", "*"}
    assert "compose" not in ops
    assert "⊠" not in ops
