"""Executable evidence for the non-differentiating fiq host."""

from ptcna.core.prime_core import compose_circle, wrap_tensor_fiq
from ptcna.neural import NeuralScalar

# === CHECKS ===
# id: check_fiq_payload_identity
#   proves: fiq_payload_is_opaque_and_lossless
#   call: self::test_payload_roundtrip_identity
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_fiq_has_no_gradient_ownership
#   proves: fiq_never_owns_gradients
#   call: self::test_fiq_is_non_differentiating_with_neural_payload
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===


def test_payload_roundtrip_identity() -> None:
    first, second = object(), object()
    fiq = wrap_tensor_fiq([first, second], anchor=0)
    assert fiq.payload[0] is first
    assert fiq.payload[1] is second
    circle = compose_circle([fiq])
    assert circle.at(0) is fiq


def test_fiq_is_non_differentiating_with_neural_payload() -> None:
    scalar = NeuralScalar(0.5)
    fiq = wrap_tensor_fiq([scalar], anchor=0)
    assert fiq.payload[0] is scalar
    assert scalar.requires_grad is True
    assert fiq.requires_grad is False
    assert not hasattr(fiq, "grad")
    assert not hasattr(fiq, "backward")
