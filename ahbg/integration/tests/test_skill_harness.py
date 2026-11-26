# ratios: loc_comments=100:1 imports_exports=6:3 calls_definitions=47:16
"""Skill disclosure through AHBG's ordinary observation/plan boundary."""

from hashlib import sha256
import json
import tempfile
import unittest

from ahbg.integration.skill_harness import SkillHarness, build_view
from ahbg.runtime import RuntimeConfig, run_plane


class ResolverFixture:
    source = {"commit": "fixture"}
    declared_runners = (("reader", "reader/run.py"), ("task", "task/run.py"))

    def __init__(self):
        self.body_reads = []

    def resolve(self, roots):
        assert roots == ["task"]
        return {"order": ["reader", "task"],
                "reasons": {"reader": [{"source": "task", "kind": "depends_on"}],
                            "task": [{"source": "task", "kind": "requested"}]}}

    def get(self, name):
        return {
            "name": name,
            "description": "trigger for " + name,
            "sha256": sha256(("instructions for " + name).encode()).hexdigest(),
            "runner": f"{name}/run.py",
        }

    def read_body(self, name):
        self.body_reads.append(name)
        return "instructions for " + name


class RecordingPlanner:
    def __init__(self):
        self.observations = []

    def manifest(self):
        return {"agent": "observer", "capabilities": ["observe", "plan"]}

    def plan(self, observation):
        self.observations.append(observation)
        return {"session_id": observation["session_id"], "turn": observation["turn"],
                "intents": [], "note": observation["skill_library"]["activated"][0]["instructions"]}

    def turn_provenance(self):
        return {"planner": "observer"}


class SkillHarnessTests(unittest.TestCase):
    def test_discovery_skips_bodies_and_tools(self):
        resolver = ResolverFixture()
        view = build_view(resolver, visible=["reader"],
                          disclosed_runners=[("reader", "reader/run.py")])
        self.assertEqual(view["discovery"], [{"name": "reader", "description": "trigger for reader"}])
        self.assertEqual(view["activated"], [])
        self.assertEqual(resolver.body_reads, [])
        self.assertNotIn("run.py", json.dumps(view))

    def test_hidden_prerequisite_blocks_before_read(self):
        resolver = ResolverFixture()
        with self.assertRaisesRegex(ValueError, "required skill"):
            build_view(resolver, visible=["task"], activate=["task"])
        self.assertEqual(resolver.body_reads, [])

    def test_actual_planner_receives_scoped_view_without_changing_actions(self):
        resolver = ResolverFixture()
        view = build_view(resolver, visible=["task", "reader", "unused"],
                          activate=["task"], disclosed_runners=[("reader", "reader/run.py")])
        self.assertEqual(resolver.body_reads, ["reader", "task"])
        planner = RecordingPlanner()
        agent = SkillHarness(planner, view, experiment="control")
        with tempfile.TemporaryDirectory() as work:
            result = run_plane(agent=agent, config=RuntimeConfig(turns=1), out_dir=work)
        observation, = planner.observations
        self.assertEqual(observation["capabilities"], ["observe", "plan"])
        reader, task = observation["skill_library"]["activated"]
        self.assertEqual(reader["runner"], "reader/run.py")
        self.assertNotIn("runner", task)
        self.assertNotIn("instructions for unused", json.dumps(observation))
        turn, = result.turn_records
        self.assertEqual(turn["submitted_plan"]["note"], "instructions for reader")
        self.assertEqual(turn["agent_provenance"]["planner"], "observer")
        receipt = turn["agent_provenance"]["skill_library"]
        self.assertEqual(receipt["activation_order"], ["reader", "task"])
        serialized = json.dumps(observation["skill_library"], ensure_ascii=False, sort_keys=True,
                                separators=(",", ":")).encode()
        self.assertEqual(receipt["view_sha256"], sha256(serialized).hexdigest())

    def test_protects_a_runner_referenced_by_other_skills(self):
        class CrossReference(ResolverFixture):
            def get(self, name):
                record = super().get(name)
                text = "see reader/run.py"
                if name == "task":
                    record.update(description=text, sha256=sha256(text.encode()).hexdigest())
                return record

            def read_body(self, name):
                return "see reader/run.py" if name == "task" else super().read_body(name)

        resolver = CrossReference()
        discovery = build_view(resolver, visible=["task"])
        self.assertIn("description_withheld", discovery["discovery"][0])
        self.assertNotIn("reader/run.py", json.dumps(discovery))
        with self.assertRaisesRegex(ValueError, "outside the session disclosure policy"):
            build_view(resolver, visible=["task", "reader"], activate=["task"])
        view = build_view(resolver, visible=["task", "reader"], activate=["task"],
                          disclosed_runners=[("reader", "reader/run.py")])
        self.assertEqual(view["activated"][1]["instructions"], "see reader/run.py")

    def test_activation_rejects_body_mismatch(self):
        resolver = ResolverFixture()
        resolver.read_body = lambda name: "modified"
        with self.assertRaisesRegex(ValueError, "revision"):
            build_view(resolver, visible=["reader", "task"], activate=["task"])


if __name__ == "__main__":
    unittest.main()
# ratios: loc_comments=100:1 imports_exports=6:3 calls_definitions=47:16
