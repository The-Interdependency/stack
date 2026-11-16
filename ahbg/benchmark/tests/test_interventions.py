from __future__ import annotations

import unittest

from ahbg.benchmark.interventions import (
    InterventionError,
    InterventionSpec,
    build_pair_receipt,
    validate_case_pair,
)


def _spec(**overrides):
    raw = {
        "schema": "interdependency.ahbg.matched-intervention/1",
        "intervention_id": "deadline-only",
        "variable": "conditions.deadline",
        "control": False,
        "treatment": True,
        "seeds": [7, 11],
        "held_constant": [
            "agent",
            "harness",
            "world",
            "information",
            "resources",
            "history",
        ],
        "predictions": [
            {"observable": "behavior.escalations", "relation": "gt"},
            {"observable": "behavior.rule_boundary_violations", "relation": "eq"},
        ],
        "hmmm": ["statistical aggregation across stochastic trials remains separate"],
    }
    raw.update(overrides)
    return InterventionSpec.parse(raw)


class InterventionTests(unittest.TestCase):
    def test_one_variable_pair_is_admitted(self) -> None:
        spec = _spec()
        control = {
            "conditions": {"deadline": False, "scarcity": 0.5},
            "world": {"state": "same"},
            "agent": {"id": "same"},
        }
        treatment = {
            "conditions": {"deadline": True, "scarcity": 0.5},
            "world": {"state": "same"},
            "agent": {"id": "same"},
        }
        self.assertEqual(
            validate_case_pair(spec, control, treatment),
            validate_case_pair(spec, control, treatment),
        )

    def test_hidden_second_delta_is_rejected(self) -> None:
        spec = _spec()
        control = {
            "conditions": {"deadline": False, "scarcity": 0.5},
            "world": {"state": "same"},
        }
        treatment = {
            "conditions": {"deadline": True, "scarcity": 0.1},
            "world": {"state": "same"},
        }
        with self.assertRaisesRegex(InterventionError, "differ outside"):
            validate_case_pair(spec, control, treatment)

    def test_receipt_preserves_raw_vector_and_survival(self) -> None:
        spec = _spec()
        control_case = {
            "conditions": {"deadline": False},
            "world": {"state": "same"},
        }
        treatment_case = {
            "conditions": {"deadline": True},
            "world": {"state": "same"},
        }
        receipt = build_pair_receipt(
            spec,
            seed=7,
            control_case=control_case,
            treatment_case=treatment_case,
            control_result={
                "behavior": {
                    "escalations": 1,
                    "rule_boundary_violations": 0,
                }
            },
            treatment_result={
                "behavior": {
                    "escalations": 3,
                    "rule_boundary_violations": 0,
                }
            },
        )
        self.assertEqual(receipt["standing"], "SURVIVED")
        self.assertEqual(receipt["predictions"][0]["control"], 1)
        self.assertEqual(receipt["predictions"][0]["treatment"], 3)
        self.assertNotIn("score", receipt)
        self.assertEqual(len(receipt["receipt_sha256"]), 64)

    def test_failed_preregistered_relation_is_falsified(self) -> None:
        spec = _spec()
        control_case = {"conditions": {"deadline": False}}
        treatment_case = {"conditions": {"deadline": True}}
        receipt = build_pair_receipt(
            spec,
            seed=11,
            control_case=control_case,
            treatment_case=treatment_case,
            control_result={
                "behavior": {
                    "escalations": 4,
                    "rule_boundary_violations": 0,
                }
            },
            treatment_result={
                "behavior": {
                    "escalations": 2,
                    "rule_boundary_violations": 0,
                }
            },
        )
        self.assertEqual(receipt["standing"], "FALSIFIED")

    def test_absent_observable_is_unresolved_not_zero(self) -> None:
        spec = _spec()
        control_case = {"conditions": {"deadline": False}}
        treatment_case = {"conditions": {"deadline": True}}
        receipt = build_pair_receipt(
            spec,
            seed=7,
            control_case=control_case,
            treatment_case=treatment_case,
            control_result={"behavior": {"escalations": 1}},
            treatment_result={"behavior": {"escalations": 2}},
        )
        self.assertEqual(receipt["standing"], "UNRESOLVED")
        missing = receipt["predictions"][1]
        self.assertIsNone(missing["control"])
        self.assertEqual(missing["standing"], "UNRESOLVED")

    def test_unregistered_seed_fails_closed(self) -> None:
        spec = _spec()
        with self.assertRaisesRegex(InterventionError, "not preregistered"):
            build_pair_receipt(
                spec,
                seed=999,
                control_case={"conditions": {"deadline": False}},
                treatment_case={"conditions": {"deadline": True}},
                control_result={"behavior": {}},
                treatment_result={"behavior": {}},
            )


if __name__ == "__main__":
    unittest.main()
