from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from ahbg.deepseek.a0 import (
    A0Instance,
    Boundary,
    DEEPSEEK_SPEC,
    EnergyResult,
    Lineage,
    PermissionField,
    ProviderSpec,
    plan_with_energy,
    register_provider,
    resolve_energy,
)
from ahbg.deepseek.a0.energy import EnergyUnavailable

OBSERVATION = {
    "turn": 0,
    "tiles": [
        {"tile_id": "c", "q": 0, "r": 0},
        {"tile_id": "e", "q": 1, "r": 0},
        {"tile_id": "se", "q": 0, "r": 1},
    ],
    "units": [{"unit_id": "A0", "tile_id": "c"}],
}


class FakeEnergy:
    def __init__(self, result: EnergyResult) -> None:
        self.spec = ProviderSpec(name="fake", base_url="http://fake", api_key_env="FAKE_KEY", model="fake")
        self._result = result

    def complete(self, messages, max_tokens=256):
        return self._result


def _instance() -> A0Instance:
    return A0Instance(
        lineage=Lineage("a0.1", "run-1", None, "deepseek-v4-pro"),
        boundary=Boundary(self_unit_id="A0"),
        permissions=PermissionField(),
    )


class EnergyPlannerTests(unittest.TestCase):
    def test_accepts_legal_energy_move(self) -> None:
        energy = FakeEnergy(EnergyResult(ok=True, text='{"kind":"move","to_tile_id":"e"}', prompt_tokens=10, completion_tokens=4, latency_ms=12.0))
        instance = _instance()
        result = plan_with_energy(OBSERVATION, energy=energy, instance=instance)
        self.assertEqual(result.source, "energy")
        self.assertEqual(result.plan["actions"][0]["data"]["to_tile_id"], "e")
        self.assertEqual(instance.capacity.tokens_used, 14)
        self.assertEqual(instance.capacity.tool_calls, 1)

    def test_illegal_energy_move_falls_back(self) -> None:
        energy = FakeEnergy(EnergyResult(ok=True, text='{"kind":"move","to_tile_id":"far"}', prompt_tokens=5, completion_tokens=2))
        result = plan_with_energy(OBSERVATION, energy=energy)
        self.assertEqual(result.source, "fallback")
        self.assertIn("illegal move", result.refusal)
        # Fallback plan is the deterministic legal move.
        self.assertEqual(result.plan["actions"][0]["data"]["to_tile_id"], "e")

    def test_non_canonical_kind_falls_back(self) -> None:
        energy = FakeEnergy(EnergyResult(ok=True, text='{"kind":"construct"}'))
        result = plan_with_energy(OBSERVATION, energy=energy)
        self.assertEqual(result.source, "fallback")
        self.assertIn("non-canonical", result.refusal)

    def test_unavailable_energy_falls_back(self) -> None:
        energy = FakeEnergy(EnergyResult(ok=False, error="boom"))
        result = plan_with_energy(OBSERVATION, energy=energy)
        self.assertEqual(result.source, "fallback")
        self.assertIn("boom", result.refusal)

    def test_garbage_reply_falls_back(self) -> None:
        energy = FakeEnergy(EnergyResult(ok=True, text="not json at all"))
        result = plan_with_energy(OBSERVATION, energy=energy)
        self.assertEqual(result.source, "fallback")
        self.assertIn("JSON", result.refusal)

    def test_pass_reply_is_accepted(self) -> None:
        energy = FakeEnergy(EnergyResult(ok=True, text='{"kind":"pass"}'))
        result = plan_with_energy(OBSERVATION, energy=energy)
        self.assertEqual(result.source, "energy")
        self.assertEqual(result.plan["actions"], [])


class EnergyRegistryTests(unittest.TestCase):
    def test_default_provider_is_deepseek(self) -> None:
        self.assertEqual(DEEPSEEK_SPEC.api_key_env, "DEEPSEEK_API_KEY")

    def test_unknown_provider_fails_closed(self) -> None:
        with self.assertRaises(EnergyUnavailable):
            resolve_energy("does-not-exist")

    def test_registered_provider_is_resolvable_by_name(self) -> None:
        import os

        os.environ["A0_TEST_FAKE_KEY"] = "test-key"
        register_provider(ProviderSpec(name="a0-test", base_url="http://fake", api_key_env="A0_TEST_FAKE_KEY", model="fake"))
        client = resolve_energy("a0-test")
        self.assertEqual(client.spec.name, "a0-test")


if __name__ == "__main__":
    unittest.main()
