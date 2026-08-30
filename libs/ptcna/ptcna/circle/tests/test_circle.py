"""Executable evidence for standalone circle composition."""

import pytest

from ptcna.circle import CircleTensor, compose_circle, star_polygon_order
from ptcna.neural import NeuralScalar

# === CHECKS ===
# id: check_circle_roundtrip
#   proves: circle_tensor_round_trips_payloads, circle_composition_preserves_order_and_identity
#   call: self::test_circle_preserves_exact_payload_objects
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_circle_non_differentiating
#   proves: circle_tensor_is_non_differentiating
#   call: self::test_circle_does_not_own_neural_payload_gradients
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_circle_rejects_empty
#   proves: circle_composition_rejects_empty_input
#   call: self::test_empty_circle_is_rejected
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_circle_identity_fallback
#   proves: circle_composition_preserves_order_and_identity
#   call: self::test_non_coprime_count_uses_identity_fallback
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===


def test_circle_preserves_exact_payload_objects() -> None:
    payloads = [object() for _ in range(7)]
    circle = compose_circle(payloads, identity="circle:0")
    assert isinstance(circle, CircleTensor)
    assert circle.anchor_order == tuple(star_polygon_order(2))
    for index, anchor in enumerate(circle.anchor_order):
        assert circle.at(anchor) is payloads[index]
    assert circle.tensor_payloads() == payloads


def test_circle_does_not_own_neural_payload_gradients() -> None:
    scalar = NeuralScalar(1.0)
    circle = compose_circle([scalar])
    assert scalar.requires_grad is True
    assert circle.requires_grad is False
    assert not hasattr(circle, "backward")
    assert circle.at(0) is scalar


def test_empty_circle_is_rejected() -> None:
    with pytest.raises(ValueError, match="zero neural payloads"):
        compose_circle([])


def test_non_coprime_count_uses_identity_fallback() -> None:
    circle = compose_circle(["a", "b"], routing_step=2)
    assert circle.anchor_order == (0, 1)
