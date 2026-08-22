"""Executable evidence for shared-layer prime-core composition."""

import pytest

from ptcna.circle import CircleTensor
from ptcna.core.prime_core import CoreSpec, Fiq, build_core, heptagram_order
from ptcna.neural import NeuralScalar
from ptcna.seed import Seed
from ptcna.ucns_integration import UCNSIntegrationState

# === CHECKS ===
# id: check_prime_core_default_profile
#   proves: prime_core_default_profile_is_stable
#   call: self::test_canon_structure_counts
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_prime_core_shared_layer_types
#   proves: prime_core_uses_shared_layer_types
#   call: self::test_core_uses_circle_and_seed_owned_types
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_prime_core_no_gradient_ownership
#   proves: prime_core_is_non_differentiating
#   call: self::test_neural_payload_gradients_remain_neural_owned
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_prime_core_ucns_scope
#   proves: prime_core_ucns_receipt_scope_is_exact
#   call: self::test_ucns_attribution_is_exactly_shape_scoped
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_prime_core_payload_width
#   proves: prime_core_payload_width_matches_spec
#   call: self::test_payload_factory_width_is_checked
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#
# id: check_prime_core_positive_counts
#   proves: prime_core_counts_are_positive
#   call: self::test_core_spec_rejects_nonpositive_counts
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
# === END CHECKS ===

SMALL = CoreSpec(
    seed_count=2,
    circles_per_seed=2,
    tensors_per_circle=2,
    tensor_dim=2,
)


def test_canon_structure_counts() -> None:
    core = build_core()
    assert len(core.seeds) == 157
    assert len(core.tensor_leaves()) == 7_693
    assert core.spec.param_count == 407_729
    assert all(isinstance(fiq, Fiq) for fiq in core.tensor_leaves())


def test_core_uses_circle_and_seed_owned_types() -> None:
    core = build_core(SMALL)
    assert all(isinstance(seed, Seed) for seed in core.seeds)
    assert all(
        isinstance(circle, CircleTensor)
        for seed in core.seeds
        for circle in seed.circles
    )
    assert heptagram_order(2) == [0, 2, 4, 6, 1, 3, 5]
    assert heptagram_order(3) == [0, 3, 6, 2, 5, 1, 4]


def test_neural_payload_gradients_remain_neural_owned() -> None:
    def factory(
        _seed: int,
        _circle: int,
        _tensor: int,
        width: int,
        init: float,
    ) -> list[NeuralScalar]:
        return [NeuralScalar(init) for _ in range(width)]

    core = build_core(SMALL, payload_factory=factory)
    scalars = [
        scalar
        for fiq in core.tensor_leaves()
        for scalar in fiq.payload
    ]
    loss = NeuralScalar(0.0)
    for scalar in scalars:
        loss = loss + scalar
    loss.backward()

    assert all(scalar.grad == 1.0 for scalar in scalars)
    assert core.requires_grad is False
    assert all(seed.requires_grad is False for seed in core.seeds)
    assert all(
        circle.requires_grad is False
        for seed in core.seeds
        for circle in seed.circles
    )
    assert all(fiq.requires_grad is False for fiq in core.tensor_leaves())
    assert not hasattr(core, "backward")


def test_ucns_attribution_is_exactly_shape_scoped() -> None:
    exact = build_core(init=0.0)
    assert exact.ucns_status.state is UCNSIntegrationState.ACTIVE
    assert exact.ucns_status.adapter_active is True
    core = build_core(SMALL)
    assert core.ucns_status.state is UCNSIntegrationState.SUSPENDED
    assert core.ucns_status.adapter_active is False
    assert all(
        fiq.identity.startswith("ptcna-local:fiq:")
        for fiq in core.tensor_leaves()
    )


def test_payload_factory_width_is_checked() -> None:
    with pytest.raises(ValueError, match="expected 2"):
        build_core(SMALL, payload_factory=lambda *_args: [1.0])


def test_core_spec_rejects_nonpositive_counts() -> None:
    for field in [
        "seed_count",
        "circles_per_seed",
        "tensors_per_circle",
        "tensor_dim",
    ]:
        values = {
            "seed_count": 1,
            "circles_per_seed": 1,
            "tensors_per_circle": 1,
            "tensor_dim": 1,
        }
        values[field] = 0
        with pytest.raises(ValueError, match=field):
            CoreSpec(**values)
