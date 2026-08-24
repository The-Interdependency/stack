# ratios: loc_comments=143:4 imports_exports=9:3 calls_definitions=86:21
"""Stdlib-only tests for the a0min harness and CLI.

Run from the a0min project root:

    python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

from a0min import (  # noqa: E402  (project root on sys.path via test runner)
    Harness,
    SpawnCapExceeded,
    candidate_platonic_agent,
)


class PlatonicImportTests(unittest.TestCase):
    def test_candidate_superpotential_loads(self) -> None:
        agent = candidate_platonic_agent()
        self.assertEqual(agent.agent_id, "a0.agent.platonic")
        self.assertEqual(len(agent.dimensions), 13)
        self.assertEqual(len(agent.regions), 11)

    def test_every_region_is_a_potential_sub_agent_option(self) -> None:
        harness = Harness()
        options = harness.potential_sub_agents()
        self.assertEqual(
            tuple(option.region for option in options),
            harness.superpotential.region_names,
        )


class HarnessCreationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.harness = Harness()

    def test_create_any_declared_region(self) -> None:
        harness = Harness(max_concurrent_live=20, max_fanout=20)
        for region in harness.superpotential.region_names:
            with self.subTest(region=region):
                sub_agent = harness.create(region)
                self.assertEqual(sub_agent.region, region)
                self.assertEqual(sub_agent.status, "spawned")
                self.assertTrue(sub_agent.sub_agent_id.startswith("a0z-"))

    def test_create_projects_region_dimensions_explicitly(self) -> None:
        sub_agent = self.harness.create(
            "definition",
            {"identity": {"definition_id": "def-1"}},
            task="minimal definition",
        )
        self.assertEqual(
            sub_agent.selected, self.harness.superpotential.region("definition").dimensions
        )
        self.assertEqual(sub_agent.bindings["identity"], {"definition_id": "def-1"})
        self.assertIn("boundaries", sub_agent.unresolved)
        self.assertEqual(sub_agent.task, "minimal definition")

    def test_unknown_region_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            self.harness.create("telepathy")

    def test_unknown_orchestration_mode_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            self.harness.create("definition", orchestration_mode="hive_mind")

    def test_depth_cap_enforced(self) -> None:
        harness = Harness(max_depth=1)
        parent = harness.create("run")
        with self.assertRaises(SpawnCapExceeded):
            harness.create("definition", parent=parent)

    def test_fanout_cap_enforced(self) -> None:
        harness = Harness(max_fanout=1)
        harness.create("run")
        with self.assertRaises(SpawnCapExceeded):
            harness.create("definition")

    def test_concurrent_live_cap_and_merge_release(self) -> None:
        harness = Harness(max_concurrent_live=1)
        first = harness.create("run")
        with self.assertRaises(SpawnCapExceeded):
            harness.create("definition")
        harness.merge(first.sub_agent_id)
        second = harness.create("definition")
        self.assertEqual(second.status, "spawned")

    def test_merge_marks_merged(self) -> None:
        sub_agent = self.harness.create("definition")
        merged = self.harness.merge(sub_agent.sub_agent_id)
        self.assertEqual(merged.status, "merged")
        self.assertEqual(self.harness.live_count(sub_agent.parent_run_id), 0)

    def test_children_lineage(self) -> None:
        parent = self.harness.create("run")
        child = self.harness.create("run_artifacts", parent=parent)
        self.assertEqual(child.parent_run_id, parent.run_id)
        self.assertEqual(child.root_run_id, parent.root_run_id)
        self.assertEqual(child.depth, 2)
        self.assertEqual(self.harness.children_of(parent.run_id), (child,))

    def test_save_load_roundtrip(self) -> None:
        import tempfile

        sub_agent = self.harness.create("definition", {"identity": {"id": "def-1"}})
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.json"
            self.harness.save(state)
            restored = Harness.load(state)
            self.assertEqual(restored.list_sub_agents()[0].as_dict(), sub_agent.as_dict())
            self.assertEqual(restored._index, self.harness._index)


class CliSmokeTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "a0min", *args],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
        )

    def test_list_json(self) -> None:
        result = self.run_cli("list", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload), 11)
        self.assertEqual(payload[0]["region"], "definition")

    def test_create_show_merge_roundtrip(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            state = str(Path(tmp) / "state.json")
            created = self.run_cli(
                "--state",
                state,
                "create",
                "definition",
                "--bind",
                'identity={"definition_id":"def-1"}',
                "--json",
            )
            self.assertEqual(created.returncode, 0, created.stderr)
            sub_agent = json.loads(created.stdout)
            self.assertEqual(sub_agent["region"], "definition")
            sub_agent_id = sub_agent["sub_agent_id"]

            shown = self.run_cli("--state", state, "show", sub_agent_id, "--json")
            self.assertEqual(shown.returncode, 0, shown.stderr)
            self.assertEqual(json.loads(shown.stdout)["run_id"], sub_agent["run_id"])

            merged = self.run_cli("--state", state, "merge", sub_agent_id, "--json")
            self.assertEqual(merged.returncode, 0, merged.stderr)
            self.assertEqual(json.loads(merged.stdout)["status"], "merged")

    def test_create_unknown_region_fails(self) -> None:
        result = self.run_cli("create", "telepathy", "--json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown region", result.stderr)

    def test_superpotential_json(self) -> None:
        result = self.run_cli("superpotential", "--json")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["agent_id"], "a0.agent.platonic")
        self.assertEqual(len(payload["dimensions"]), 13)
        self.assertEqual(len(payload["regions"]), 11)


if __name__ == "__main__":
    unittest.main()
# ratios: loc_comments=143:4 imports_exports=9:3 calls_definitions=86:21
