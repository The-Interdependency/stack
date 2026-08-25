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

    def test_occupied_target_fails_closed(self) -> None:
        world, log = new_world(
            101,
            units=[
                {"unit_id": "A0", "tile_id": "c", "label": "A0"},
                {"unit_id": "B0", "tile_id": "e", "label": "B0"},
            ],
        )
        controller = TurnController(world, log)
        controller.begin_turn()
        with self.assertRaises(UnresolvedHmmm):
            controller.resolve([
                {"turn": 0, "actions": [{"kind": "move", "data": {"unit_id": "A0", "to_tile_id": "e"}}]}
            ])
        self.assertEqual(world.units["A0"].tile_id, "c")

    def test_dual_target_fails_closed(self) -> None:
        world, log = new_world(
            101,
            units=[
                {"unit_id": "A0", "tile_id": "c", "label": "A0"},
                {"unit_id": "B0", "tile_id": "sw", "label": "B0"},
            ],
        )
        controller = TurnController(world, log)
        controller.begin_turn()
        with self.assertRaises(UnresolvedHmmm):
            controller.resolve([
                {
                    "turn": 0,
                    "actions": [
                        {"kind": "move", "data": {"unit_id": "A0", "to_tile_id": "se"}},
                        {"kind": "move", "data": {"unit_id": "B0", "to_tile_id": "se"}},
                    ],
                }
            ])

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
    def test_artifact_checker_reports_missing_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = check_artifact_dir(tmp)
        self.assertEqual(result["standing"], "FALSIFIED")
        self.assertTrue(result["findings"])

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
