from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ahbg.benchmark.experiment import run_matched_pair
from ahbg.benchmark.interventions import InterventionError, InterventionSpec
from ahbg.runtime.runtime import RuntimeConfig


class DeadlineHarness:
    def manifest(self):
        return {
            "agent": "deadline-probe",
            "capabilities": ["observe", "plan", "relocate"],
        }

    def plan(self, observation):
        legal = observation.get("legal") or []
        intents = []
        if observation["deadline_ms"] <= 1000 and legal:
            intents = [legal[0]]
        return {
            "schema": "interdependency.ahbg.harness.plan/1",
            "session_id": observation["session_id"],
            "turn": observation["turn"],
            "intents": intents,
            "note": "deadline-probe",
        }


class ConfoundedFactory:
    def __call__(self, arm):
        harness = DeadlineHarness()
        if arm == "treatment":
            harness.manifest = lambda: {
                "agent": "different-agent",
                "capabilities": ["observe", "plan", "relocate"],
            }
        return harness


def deadline_spec():
    return InterventionSpec.parse(
        {
            "schema": "interdependency.ahbg.matched-intervention/1",
            "intervention_id": "deadline-only",
            "variable": "runtime.deadline_ms",
            "control": 5000,
            "treatment": 1000,
            "seeds": [23],
            "held_constant": [
                "agent",
                "runtime.seed",
                "runtime.turns",
                "runtime.turn_messages",
                "runtime.forced_plans",
            ],
            "predictions": [
                {
                    "observable": "phenotype.no_intent_turns",
                    "relation": "lt",
                }
            ],
            "hmmm": [
                "one paired deterministic seed is a causal witness, not a population effect size"
            ],
        }
    )


class ExperimentTests(unittest.TestCase):
    def test_deadline_only_pair_produces_survived_receipt_and_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "pair"
            receipt = run_matched_pair(
                deadline_spec(),
                seed=23,
                control_config=RuntimeConfig(
                    seed=23,
                    turns=1,
                    deadline_ms=5000,
                    injection_handling="observe-only",
                ),
                treatment_config=RuntimeConfig(
                    seed=23,
                    turns=1,
                    deadline_ms=1000,
                    injection_handling="observe-only",
                ),
                harness_factory=lambda _arm: DeadlineHarness(),
                out_dir=root,
            )
            self.assertEqual(receipt["standing"], "SURVIVED")
            prediction = receipt["predictions"][0]
            self.assertEqual(prediction["control"], 1)
            self.assertEqual(prediction["treatment"], 0)
            for name in (
                "control-case.json",
                "treatment-case.json",
                "control-phenotype.json",
                "treatment-phenotype.json",
                "receipt.json",
            ):
                self.assertTrue((root / name).exists(), name)
            self.assertTrue((root / "control" / "result.json").exists())
            self.assertTrue((root / "treatment" / "result.json").exists())

    def test_agent_identity_delta_is_rejected_before_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(
                InterventionError,
                "differ outside",
            ):
                run_matched_pair(
                    deadline_spec(),
                    seed=23,
                    control_config=RuntimeConfig(
                        seed=23,
                        turns=1,
                        deadline_ms=5000,
                    ),
                    treatment_config=RuntimeConfig(
                        seed=23,
                        turns=1,
                        deadline_ms=1000,
                    ),
                    harness_factory=ConfoundedFactory(),
                    out_dir=Path(tmp) / "pair",
                )

    def test_second_runtime_delta_is_rejected_before_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(
                InterventionError,
                "differ outside",
            ):
                run_matched_pair(
                    deadline_spec(),
                    seed=23,
                    control_config=RuntimeConfig(
                        seed=23,
                        turns=1,
                        deadline_ms=5000,
                    ),
                    treatment_config=RuntimeConfig(
                        seed=23,
                        turns=2,
                        deadline_ms=1000,
                    ),
                    harness_factory=lambda _arm: DeadlineHarness(),
                    out_dir=Path(tmp) / "pair",
                )

    def test_nonempty_output_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "pair"
            root.mkdir()
            (root / "foreign.txt").write_text("contamination", encoding="utf-8")
            with self.assertRaisesRegex(InterventionError, "must be empty"):
                run_matched_pair(
                    deadline_spec(),
                    seed=23,
                    control_config=RuntimeConfig(
                        seed=23,
                        turns=1,
                        deadline_ms=5000,
                    ),
                    treatment_config=RuntimeConfig(
                        seed=23,
                        turns=1,
                        deadline_ms=1000,
                    ),
                    harness_factory=lambda _arm: DeadlineHarness(),
                    out_dir=root,
                )


if __name__ == "__main__":
    unittest.main()
