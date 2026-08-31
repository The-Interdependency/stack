from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WORKSPACE = Path(__file__).resolve().parents[2]
for entry in list(sys.path):
    if Path(entry or ".").resolve() == WORKSPACE:
        sys.path.remove(entry)
sys.path.insert(0, str(ROOT))

from ahbg.codex.ahbg import (
    EventLog,
    KIND_WAR,
    ReplayError,
    TurnController,
    UnresolvedHmmm,
    ValidationError,
    check_artifact_dir,
    load_world,
    new_world,
    replay,
    save_world,
    seed_of_life_tiles,
)


class GeometryTests(unittest.TestCase):
    def test_seed_of_life_tiles_are_projected_from_ucns(self) -> None:
        self.assertEqual(
            [(tile["tile_id"], tile["q"], tile["r"]) for tile in seed_of_life_tiles()],
            [
                ("c", 0, 0),
                ("e", 1, 0),
                ("se", 0, 1),
                ("sw", -1, 1),
                ("w", -1, 0),
                ("nw", 0, -1),
                ("ne", 1, -1),
            ],
        )


class WorldReplayTests(unittest.TestCase):
    def test_new_world_replays_to_itself(self) -> None:
        world, log = new_world(101)
        self.assertEqual(replay(log).canonical_dict(), world.canonical_dict())

    def test_observation_excludes_seed(self) -> None:
        world, _ = new_world(101)
        observation = world.legal_observation(context={"standing": "known-neutral"})
        self.assertNotIn("seed", observation)
        self.assertEqual(observation["context"]["standing"], "known-neutral")

    def test_save_load_round_trip(self) -> None:
        world, log = new_world(101)
        controller = TurnController(world, log)
        controller.begin_turn()
        controller.resolve([{"turn": 0, "actions": [{"kind": "move", "data": {"unit_id": "A0", "to_tile_id": "e"}}]}])
        controller.end_turn()
        with tempfile.TemporaryDirectory() as tmp:
            save_world(tmp, world, log)
            loaded, loaded_log = load_world(tmp)
        self.assertEqual(loaded.canonical_dict(), world.canonical_dict())
        self.assertEqual(replay(loaded_log).canonical_dict(), world.canonical_dict())

    def test_replay_rejects_open_turn(self) -> None:
        world, log = new_world(101)
        TurnController(world, log).begin_turn()
        with self.assertRaisesRegex(ReplayError, "before turn.end"):
            replay(log)


class TurnTests(unittest.TestCase):
    def test_move_resolves_and_replays(self) -> None:
        world, log = new_world(101)
        controller = TurnController(world, log)
        controller.begin_turn()
        events = controller.resolve([
            {"turn": 0, "actions": [{"kind": "move", "data": {"unit_id": "A0", "to_tile_id": "e"}}]}
        ])
        controller.end_turn()
        self.assertEqual(len(events), 1)
        self.assertEqual(world.units["A0"].tile_id, "e")
        self.assertEqual(replay(log).canonical_dict(), world.canonical_dict())

    def test_unknown_action_fails_closed(self) -> None:
        world, log = new_world(101)
        controller = TurnController(world, log)
        controller.begin_turn()
        with self.assertRaises(UnresolvedHmmm):
            controller.resolve([{"turn": 0, "actions": [{"kind": "build", "data": {}}]}])

    def test_occupied_target_resolves_defender_holds(self) -> None:
        world, log = new_world(
            101,
            units=[
                {"unit_id": "A0", "tile_id": "c", "label": "A0"},
                {"unit_id": "B0", "tile_id": "e", "label": "B0"},
            ],
        )
        controller = TurnController(world, log)
        controller.begin_turn()
        events = controller.resolve([
            {"turn": 0, "actions": [{"kind": "move", "data": {"unit_id": "A0", "to_tile_id": "e"}}]}
        ])
        controller.end_turn()
        war_events = [event for event in events if event.kind == KIND_WAR]
        self.assertEqual(len(war_events), 1)
        self.assertEqual(war_events[0].data["reason"], "occupied")
        self.assertEqual(war_events[0].data["outcome"], "defender_holds")
        self.assertEqual(world.units["A0"].tile_id, "c")
        self.assertEqual(world.units["B0"].tile_id, "e")
        self.assertEqual(replay(log).canonical_dict(), world.canonical_dict())

    def test_dual_target_resolves_priority(self) -> None:
        world, log = new_world(
            101,
            units=[
                {"unit_id": "A0", "tile_id": "c", "label": "A0"},
                {"unit_id": "B0", "tile_id": "sw", "label": "B0"},
            ],
        )
        controller = TurnController(world, log)
        controller.begin_turn()
        events = controller.resolve([
            {
                "turn": 0,
                "actions": [
                    {"kind": "move", "data": {"unit_id": "A0", "to_tile_id": "se"}},
                    {"kind": "move", "data": {"unit_id": "B0", "to_tile_id": "se"}},
                ],
            }
        ])
        controller.end_turn()
        outcomes = {
            (event.data["unit_id"], event.data["outcome"])
            for event in events
            if event.kind == KIND_WAR
        }
        self.assertEqual(outcomes, {("A0", "priority_win"), ("B0", "priority_loss")})
        self.assertEqual(world.units["A0"].tile_id, "se")
        self.assertEqual(world.units["B0"].tile_id, "sw")
        self.assertEqual(replay(log).canonical_dict(), world.canonical_dict())

    def test_non_adjacent_move_is_invalid(self) -> None:
        tiles = seed_of_life_tiles() + [{"tile_id": "far", "q": 2, "r": 0, "label": "far"}]
        world, log = new_world(101, tiles=tiles)
        controller = TurnController(world, log)
        controller.begin_turn()
        with self.assertRaises(ValidationError):
            controller.resolve([
                {"turn": 0, "actions": [{"kind": "move", "data": {"unit_id": "A0", "to_tile_id": "far"}}]}
            ])


class ArtifactCheckerTests(unittest.TestCase):
    def _write_json(self, path: Path, data: dict[str, object]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, sort_keys=True) + "\n", encoding="utf-8")

    def _write_build_manifest(self, target: Path) -> None:
        self._write_json(target / "BUILD_MANIFEST.json", {"schema": "test.build/1.0.0"})

    def _write_run_artifacts(
        self,
        artifact_root: Path,
        *,
        aggregate_events: bool = True,
        summary: dict[str, object] | None = None,
    ) -> None:
        self._write_json(artifact_root / "RUN_MANIFEST.json", {"schema": "test.run/1.0.0"})
        self._write_json(
            artifact_root / "CALIBRATION_RESULT.json",
            {"schema": "test.result/1.0.0", "summary": summary or {"falsified": 0, "survived": 1}},
        )
        (artifact_root / "CALIBRATION_REPORT.md").write_text("# test report\n", encoding="utf-8")
        events_path = (
            artifact_root / "EVENTS.jsonl"
            if aggregate_events
            else artifact_root / "plain_move_loop" / "events.jsonl"
        )
        events_path.parent.mkdir(parents=True, exist_ok=True)
        events_path.write_text('{"data":{},"kind":"test","seq":0,"turn":0}\n', encoding="utf-8")

    def test_artifact_checker_reports_missing_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = check_artifact_dir(tmp)
        self.assertEqual(result["standing"], "FALSIFIED")
        self.assertTrue(result["findings"])

    def test_artifact_checker_accepts_artifacts_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self._write_build_manifest(target)
            self._write_run_artifacts(target / "artifacts")
            result = check_artifact_dir(target)
        self.assertEqual(result["standing"], "SURVIVED")
        self.assertEqual(result["layout"], "artifacts:aggregate-events")

    def test_artifact_checker_accepts_top_level_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self._write_build_manifest(target)
            self._write_run_artifacts(target)
            result = check_artifact_dir(target)
        self.assertEqual(result["standing"], "SURVIVED")
        self.assertEqual(result["layout"], "top-level:aggregate-events")

    def test_artifact_checker_accepts_per_scenario_events(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self._write_build_manifest(target)
            self._write_run_artifacts(
                target / "artifacts",
                aggregate_events=False,
                summary={"FALSIFIED": 0, "SURVIVED": 1},
            )
            result = check_artifact_dir(target)
        self.assertEqual(result["standing"], "SURVIVED")
        self.assertEqual(result["layout"], "artifacts:per-scenario-events")

    def test_artifact_checker_prefers_latest_corpus_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self._write_build_manifest(target)
            self._write_run_artifacts(target / "artifacts")
            self._write_run_artifacts(target / "corpus-run" / "calibration-family-1.0.1-proposal-1")
            result = check_artifact_dir(target)
        self.assertEqual(result["standing"], "SURVIVED")
        self.assertEqual(result["layout"], "corpus-run/calibration-family-1.0.1-proposal-1:aggregate-events")

    def test_event_log_rejects_tamper(self) -> None:
        world, log = new_world(101)
        controller = TurnController(world, log)
        controller.begin_turn()
        controller.end_turn()
        lines = log.to_jsonl().splitlines()
        data = json.loads(lines[0])
        data["data"]["world"]["seed"] = 999
        tampered = json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n" + "\n".join(lines[1:]) + "\n"
        with self.assertRaises(ValueError):
            EventLog.from_jsonl(tampered)


if __name__ == "__main__":
    unittest.main()
