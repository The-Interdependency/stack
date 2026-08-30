"""Executable evidence for seed composition ownership contracts."""

import pytest

from ptcna.circle import CircleTensor, compose_circle
from ptcna.neural import NeuralScalar
from ptcna.seed import compose_seed

# === CHECKS ===
# id: check_seed_shared_circle_type
#   proves: seed_composition_uses_shared_circle_type, seed_hosts_shared_circle_type, seed_payload_roundtrip
#   call: self::test_seed_uses_shared_circle_type
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_seed_non_differentiating
#   proves: seed_composition_is_non_differentiating, seed_is_non_differentiating
#   call: self::test_seed_preserves_neural_scalar_without_owning_gradient
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_seed_rejects_empty
#   proves: seed_composition_rejects_empty
#   call: self::test_seed_rejects_empty_input
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===


def test_seed_uses_shared_circle_type() -> None:
    seed = compose_seed([compose_circle(["left"]), compose_circle(["right"])])
    assert all(type(circle) is CircleTensor for circle in seed.circles)
    assert seed.tensor_payloads() == ["left", "right"]


def test_seed_preserves_neural_scalar_without_owning_gradient() -> None:
    scalar = NeuralScalar(3.0)
    seed = compose_seed([compose_circle([scalar])])
    assert seed.requires_grad is False
    assert seed.tensor_payloads()[0] is scalar
    assert not hasattr(seed, "backward")


def test_seed_rejects_empty_input() -> None:
    with pytest.raises(ValueError, match="zero circles"):
        compose_seed([])
