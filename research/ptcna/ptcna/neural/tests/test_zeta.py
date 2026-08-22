"""Executable evidence for externally measured Zeta evaluation."""

import asyncio
from pathlib import Path

import numpy as np

import ptcna.neural.zeta as zeta_module
from ptcna.neural.zeta import ZetaEngine

# === CHECKS ===
# id: check_zeta_suspends_without_provider
#   proves: zeta_requires_external_measurement_provider
#   call: self::test_evaluate_suspends_without_provider
#   requires: python3, numpy
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_zeta_no_shadow_edcm
#   proves: zeta_never_imports_shadow_edcm
#   call: self::test_removed_shadow_edcm_module_is_absent
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_zeta_external_metrics
#   proves: zeta_consumes_explicit_metrics
#   call: self::test_external_provider_drives_phi_nudge
#   requires: python3, numpy
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===


class _FakePhi:
    def __init__(self) -> None:
        self.calls: list[tuple[float, float]] = []

    def nudge(self, coherence: float, lr: float) -> None:
        self.calls.append((coherence, lr))


class _FakeTheta:
    gate_open = np.array([True, False], dtype=bool)


class _FakePCNA:
    def __init__(self) -> None:
        self.phi = _FakePhi()
        self.theta = _FakeTheta()


def test_evaluate_suspends_without_provider() -> None:
    fake = _FakePCNA()
    prior = zeta_module._default_pcna
    try:
        zeta_module._default_pcna = fake
        engine = ZetaEngine()
        event = asyncio.run(engine.evaluate("answer", "provider", "question"))
        assert event["status"] == "measurement_suspended"
        assert fake.phi.calls == []
        assert engine.eval_count == 0
    finally:
        zeta_module._default_pcna = prior


def test_removed_shadow_edcm_module_is_absent() -> None:
    assert not Path(zeta_module.__file__).with_name("edcm.py").exists()
    try:
        __import__("ptcna.neural.edcm")
    except ModuleNotFoundError:
        pass
    else:
        raise AssertionError("ptcna.neural.edcm must be removed")


def test_external_provider_drives_phi_nudge() -> None:
    fake = _FakePCNA()
    prior_pcna = zeta_module._default_pcna
    prior_factors = ZetaEngine._sigma_nudge_factors
    zeta_module._default_pcna = fake
    ZetaEngine._sigma_nudge_factors = lambda self: (1.0, 1.0)

    def provider(_assistant: str, _user: str) -> dict[str, float]:
        return {"cm": 0.8, "da": 0.6, "int_val": 0.7, "drift": 0.2}

    try:
        engine = ZetaEngine(metric_provider=provider)
        event = asyncio.run(engine.evaluate("answer", "provider", "question"))
        assert event["status"] == "external_measurement"
        assert engine.eval_count == 1
        assert len(fake.phi.calls) == 1
        assert fake.phi.calls[0][0] == event["coherence"]
    finally:
        zeta_module._default_pcna = prior_pcna
        ZetaEngine._sigma_nudge_factors = prior_factors
