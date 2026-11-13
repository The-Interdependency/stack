from __future__ import annotations

import unittest

from ahbg.benchmark.phenotype import PhenotypeError, derive_run_phenotype


class PhenotypeTests(unittest.TestCase):
    def _run(self):
        return {
            "turn_records": [
                {
                    "turn": 0,
                    "plan": {
                        "intents": [
                            {
                                "unit_id": "A0",
                                "action": "relocate",
                                "from_tile_id": "CENTER",
                                "to_tile_id": "RING_0",
                            }
                        ]
                    },
                    "effect": {
                        "events": [
                            {"kind": "move"},
                            {
                                "kind": "war",
                                "resolution": "defender_holds",
                            },
                        ]
                    },
                    "injection_detected": True,
                    "injected_refused": False,
                },
                {
                    "turn": 1,
                    "plan": {"intents": []},
                    "effect": {"events": [{"kind": "turn.end"}]},
                    "injection_detected": False,
                    "injected_refused": False,
                },
            ],
            "final_snapshot": {
                "units": [{"unit_id": "A0", "tile_id": "RING_0"}]
            },
            "construction": {"built": ["CENTER", "RING_0"]},
        }

    def test_vector_preserves_independent_dimensions(self) -> None:
        result = derive_run_phenotype(self._run())
        self.assertEqual(result["turns_observed"], 2)
        self.assertEqual(result["action_counts"], {"relocate": 1})
        self.assertEqual(result["event_kind_counts"]["war"], 1)
        self.assertEqual(
            result["war_resolution_counts"],
            {"defender_holds": 1},
        )
        self.assertEqual(result["no_intent_turns"], 1)
        self.assertEqual(result["injection_detected_turns"], 1)
        self.assertEqual(result["injection_refused_turns"], 0)
        self.assertEqual(result["construction_built_count"], 2)
        self.assertEqual(result["final_positions"], {"A0": "RING_0"})
        self.assertEqual(len(result["plan_trace_sha256"]), 64)
        self.assertNotIn("score", result)

    def test_runtime_intervention_does_not_erase_submitted_behavior(self) -> None:
        run = self._run()
        run["turn_records"][0]["submitted_plan"] = {
            "intents": [
                {
                    "unit_id": "A0",
                    "action": "relocate",
                    "from_tile_id": "CENTER",
                    "to_tile_id": "RING_0",
                }
            ]
        }
        run["turn_records"][0]["plan"] = {"intents": []}
        result = derive_run_phenotype(run)
        self.assertEqual(result["action_counts"], {"relocate": 1})
        self.assertEqual(result["executed_action_counts"], {})

    def test_malformed_run_fails_closed(self) -> None:
        with self.assertRaisesRegex(PhenotypeError, "turn_records"):
            derive_run_phenotype({"final_snapshot": {"units": []}})


if __name__ == "__main__":
    unittest.main()
