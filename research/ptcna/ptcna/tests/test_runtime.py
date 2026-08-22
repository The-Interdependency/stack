"""Executable evidence for explicit target and fallback runtime behavior."""

import pytest

import ptcna
from ptcna.runtime import (
    FALLBACK_BACKEND,
    PTCNA_BACKEND,
    HashedLinearFallback,
    PTCNAEngine,
    PTCNARuntime,
)

# === CHECKS ===
# id: check_ptcna_target_four_layers
#   proves: ptcna_target_reports_four_live_layers
#   call: self::test_target_reports_all_four_live_layers
#   requires: python3, numpy
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_ptcna_fallback_determinism
#   proves: ptcna_fallback_is_distinct_and_deterministic
#   call: self::test_fallback_is_deterministic_bounded_and_distinct
#   requires: python3, numpy
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_ptcna_fallback_reward
#   proves: ptcna_fallback_reward_changes_selected_score
#   call: self::test_fallback_positive_reward_increases_selected_score
#   requires: python3, numpy
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_ptcna_explicit_failover
#   proves: ptcna_failover_is_explicit_and_attributed
#   call: self::test_target_failure_requires_explicit_attributed_failover
#   requires: python3, numpy
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_ptcna_reward_route
#   proves: ptcna_reward_follows_backend_receipt
#   call: self::test_reward_follows_the_recorded_backend
#   requires: python3, numpy
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_ptcna_root_runtime_exports
#   proves: ptcna_root_exports_runtime_boundary
#   call: self::test_root_exports_runtime_and_evaluation_surface
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===


class _FailingTarget:
    identity = PTCNA_BACKEND

    def infer(self, text: str) -> dict:
        raise RuntimeError("declared test failure")

    def reward(self, winner: str, outcome: float) -> dict:
        raise AssertionError("failed target must not receive fallback reward")

    def state(self) -> dict:
        return {"backend": self.identity}


def test_target_reports_all_four_live_layers() -> None:
    engine = PTCNAEngine()
    result = engine.infer("four layer receipt")
    assert result["backend"] == PTCNA_BACKEND
    assert tuple(result["layers"]) == ("neural", "circle", "seed", "core")
    assert result["layers"]["neural"]["requires_grad"] is True
    for layer in ("circle", "seed", "core"):
        assert result["layers"][layer]["requires_grad"] is False
    assert result["layers"]["core"]["seed_count"] == 157
    assert result["layers"]["core"]["tensor_leaves"] == 7693
    assert result["layers"]["core"]["param_positions"] == 407729
    assert result["layers"]["core"]["ucns_state"] == "active"
    assert result["layers"]["core"]["ucns_adapter_active"] is True
    assert result["layers"]["core"]["provenance"] == "ucns-candidate-state"


def test_fallback_is_deterministic_bounded_and_distinct() -> None:
    first = HashedLinearFallback().infer("same input")
    second = HashedLinearFallback().infer("same input")
    assert first["backend"] == FALLBACK_BACKEND
    assert first["architecture"] != "ptcna"
    assert first["winner"] == second["winner"]
    assert first["confidence"] == second["confidence"]
    assert 0.0 <= first["confidence"] <= 1.0


def test_fallback_positive_reward_increases_selected_score() -> None:
    fallback = HashedLinearFallback()
    before = fallback.infer("learn this")
    winner = before["winner"]
    fallback.reward(winner, 1.0)
    after = fallback.infer("learn this")
    assert after["scores"][winner] > before["scores"][winner]


def test_target_failure_requires_explicit_attributed_failover() -> None:
    runtime = PTCNARuntime(target=_FailingTarget())
    with pytest.raises(RuntimeError, match="declared test failure"):
        runtime.infer("fail closed")
    receipt = runtime.infer("continue explicitly", fallback_on_error=True)
    assert receipt["requested_backend"] == "ptcna"
    assert receipt["backend_used"] == FALLBACK_BACKEND
    assert receipt["fallback_used"] is True
    assert receipt["routing_reason"] == "target_failure"
    assert receipt["target_error"] == "RuntimeError"


def test_reward_follows_the_recorded_backend() -> None:
    runtime = PTCNARuntime(target=_FailingTarget())
    receipt = runtime.infer("reward fallback", fallback_on_error=True)
    rewarded = runtime.reward(receipt, 1.0)
    assert rewarded["backend"] == FALLBACK_BACKEND
    assert runtime.fallback.state()["reward_count"] == 1


def test_root_exports_runtime_and_evaluation_surface() -> None:
    assert ptcna.PTCNAEngine is PTCNAEngine
    assert ptcna.PTCNARuntime is PTCNARuntime
    assert ptcna.HashedLinearFallback is HashedLinearFallback
    assert callable(ptcna.evaluate)
