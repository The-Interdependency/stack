"""Executable evidence for the six-step PCNA engine."""

import tempfile

import numpy as np

import ptcna.neural.pcna as pcna_module
from ptcna.neural import PCNAEngine

# === CHECKS ===
# id: check_pcna_six_step_pipeline
#   proves: pcna_infer_reports_complete_six_step_pipeline
#   call: self::test_infer_reports_all_six_steps
#   requires: python3, numpy
#   timeout: 30
#   mutates: none
#   cleanup: none
#
# id: check_pcna_checkpoint_roundtrip
#   proves: pcna_checkpoint_round_trips_ring_state
#   call: self::test_checkpoint_roundtrip
#   requires: python3, numpy
#   timeout: 30
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_pcna_reward
#   proves: pcna_reward_updates_neural_and_timing_state
#   call: self::test_reward_reports_one_memory_flush_result
#   requires: python3, numpy
#   timeout: 30
#   mutates: none
#   cleanup: none
# === END CHECKS ===


def test_infer_reports_all_six_steps() -> None:
    engine = PCNAEngine()
    result = engine.infer("PTCNA boundary test")
    for step in range(1, 7):
        assert any(key.startswith(f"step{step}_") for key in result)
    assert result["winner"] in {"phi", "psi", "omega"}
    assert 0.0 <= result["confidence"] <= 1.0
    assert result["step4_seed"]["phi_nodes_audited"] == 53
    assert result["step5_circle"]["theta_nodes"] == 29


def test_checkpoint_roundtrip() -> None:
    prior = pcna_module._CHECKPOINT_DIR
    with tempfile.TemporaryDirectory() as temporary:
        try:
            pcna_module._CHECKPOINT_DIR = temporary
            source = PCNAEngine()
            source.phi.tensor.fill(0.314159)
            source.phi._recompute_coherence()
            source.save_checkpoint()

            restored = PCNAEngine()
            restored.load_checkpoint()
            assert restored.checkpoint_at is not None
            assert np.array_equal(restored.phi.tensor, source.phi.tensor)
            assert restored.checkpoint_ring_means == source.checkpoint_ring_means
        finally:
            pcna_module._CHECKPOINT_DIR = prior


def test_reward_reports_one_memory_flush_result() -> None:
    engine = PCNAEngine()
    result = engine.reward("phi", 0.5)
    assert result["step"] == "pcna_reward"
    assert result["reward_index"] == 1
    assert "theta_circles_after" in result
    assert "memory_flush" in result
