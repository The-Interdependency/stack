from __future__ import annotations

import sys
import unittest
from pathlib import Path

GROK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GROK))

from fit_cost_controls import compare_action_models, evaluate  # noqa: E402


def _row(**kwargs):
    base = {
        "scenario_id": "x",
        "family": "baseline",
        "forced_turns": 0,
        "selected_actions": 3,
        "refusals": 0,
        "invalid_actions": 0,
        "evidence_standing": "SURVIVED",
        "scope": "local-seven",
        "allowed_to_be": 1.0,
        "wanted_here": 1.0,
        "allowed_to_do": 1.0,
        "wanted_to_do": 1.0,
        "C_structural": 0.0,
        "C_epistemic": 0.0,
        "C_transition": 0.0,
        "task_value": 0.0,
        "defer_all": False,
        "numeric_burden": False,
    }
    base.update(kwargs)
    return base


class CostControlTests(unittest.TestCase):
    def test_binary_veto_recovers_defer_and_additive_does_not(self) -> None:
        rows = [
            _row(scenario_id="move", family="baseline"),
            _row(
                scenario_id="veto_do",
                family="permission_gradient",
                allowed_to_do=0.0,
                C_transition=1.0,
                selected_actions=0,
                refusals=3,
                defer_all=True,
            ),
            _row(
                scenario_id="wanted_only",
                family="permission_gradient",
                wanted_here=0.0,
                C_structural=1.0,
                selected_actions=3,
                defer_all=False,
            ),
        ]
        scores = compare_action_models(rows)["scores"]
        self.assertEqual(scores["binary_occupancy_veto"]["accuracy"], 1.0)
        self.assertLess(scores["additive_shadow_cost_positive"]["accuracy"], 1.0)
        self.assertEqual(scores["wanted_axes_deficit"]["false_positive"], 1)

    def test_evaluate_falsifies_additive_and_blocks_burden(self) -> None:
        rows = [
            _row(scenario_id="affirmed_baseline"),
            _row(
                scenario_id="gradient_allowed_to_do",
                family="permission_gradient",
                allowed_to_do=0.0,
                C_transition=1.0,
                selected_actions=0,
                refusals=3,
                defer_all=True,
            ),
            _row(
                scenario_id="gradient_wanted_here",
                family="permission_gradient",
                wanted_here=0.0,
                C_structural=1.0,
            ),
            _row(scenario_id="known_neutral", family="epistemic"),
            _row(scenario_id="unknown_same_posterior", family="epistemic"),
            _row(scenario_id="high_capacity", family="capacity"),
            _row(scenario_id="low_capacity", family="capacity"),
            _row(
                scenario_id="repeated_hostility",
                family="history",
                allowed_to_do=0.0,
                C_transition=1.0,
                selected_actions=0,
                refusals=3,
                defer_all=True,
            ),
            _row(
                scenario_id="sudden_hostility",
                family="history",
                allowed_to_do=0.0,
                C_transition=1.0,
                selected_actions=0,
                refusals=3,
                defer_all=True,
            ),
            _row(scenario_id="adaptation", family="plasticity"),
            _row(scenario_id="sensitization", family="plasticity"),
            _row(scenario_id="scope_contraction", family="scope", scope="contracted"),
        ]
        payload = evaluate(rows)
        by_id = {item["id"]: item["standing"] for item in payload["components"]}
        self.assertEqual(by_id["runtime_burden_observables"], "BLOCKED")
        self.assertEqual(by_id["additive_shadow_cost_vs_binary_veto"], "FALSIFIED")
        self.assertEqual(by_id["wanted_axes_as_action_price"], "UNRESOLVED")
        self.assertEqual(by_id["hierarchical_coupling_vs_additive"], "BLOCKED")
        self.assertEqual(by_id["binary_occupancy_veto_vs_null"], "SURVIVED")
        self.assertEqual(by_id["hard_veto_removes_relocate"], "SURVIVED")


if __name__ == "__main__":
    unittest.main()
