from __future__ import annotations

import importlib
import sys
import unittest
from pathlib import Path

STACK = Path(__file__).resolve().parents[3]
PRESENTATION = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STACK))
sys.path.insert(0, str(PRESENTATION))

from ahbg.engine import Action, Plan, TurnEngine, legal_observation, new_game
from project import snapshot_from_observation
from snapshot import KIND, validate_snapshot


SEED_TILES = [
    {"tile_id": "c", "q": 0, "r": 0},
    {"tile_id": "ne", "q": 1, "r": -1},
    {"tile_id": "e", "q": 1, "r": 0},
    {"tile_id": "se", "q": 0, "r": 1},
    {"tile_id": "sw", "q": -1, "r": 1},
    {"tile_id": "w", "q": -1, "r": 0},
    {"tile_id": "nw", "q": 0, "r": -1},
]
UNITS = [{"unit_id": "A0", "tile_id": "c", "label": "A0"}]


class ObservationProjectionTest(unittest.TestCase):
    def test_package_import_path_projects_observation(self) -> None:
        module = importlib.import_module("ahbg.presentation.project")
        plane, _log = new_game(seed=7, tiles=SEED_TILES, units=UNITS)

        snapshot = module.snapshot_from_observation(
            legal_observation(plane).to_dict(),
            plane_id="plane-0",
        )

        validate_snapshot(snapshot)
        self.assertEqual(snapshot["units"][0]["tile"], "c")

    def test_new_game_observation_projects_without_seed_or_motions(self) -> None:
        plane, _log = new_game(seed=7, tiles=SEED_TILES, units=UNITS)
        snapshot = snapshot_from_observation(
            legal_observation(plane).to_dict(),
            plane_id="plane-0",
            feed=[{"turn": 0, "text": "plane loaded; A0 at origin"}],
        )
        validate_snapshot(snapshot)
        self.assertEqual(snapshot["kind"], KIND)
        self.assertEqual(snapshot["standing"], "not-mechanics")
        self.assertEqual(snapshot["turn"], 0)
        self.assertEqual(snapshot["units"][0]["tile"], "c")
        self.assertNotIn("seed", snapshot)
        self.assertNotIn("schema", snapshot)
        self.assertNotIn("motions", snapshot)

    def test_resolved_move_projects_as_visual_trace(self) -> None:
        plane, log = new_game(seed=7, tiles=SEED_TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        events = engine.resolve(
            [Plan(turn=0, actions=(Action("move", {"unit_id": "A0", "to_tile_id": "ne"}),))]
        )
        engine.end_turn()
        snapshot = snapshot_from_observation(
            legal_observation(plane).to_dict(),
            plane_id="plane-0",
            feed=[{"turn": 1, "text": "A0 trace origin to ne"}],
            move_events=[event.canonical_dict() for event in events],
        )
        self.assertEqual(snapshot["turn"], 1)
        self.assertEqual(snapshot["units"][0]["tile"], "ne")
        self.assertEqual(snapshot["motions"], [{"unit": "A0", "from": "c", "to": "ne"}])
        self.assertNotIn("adjacent", str(snapshot).lower())

    def test_plane_dict_drops_internal_fields(self) -> None:
        plane, _log = new_game(seed=99, tiles=SEED_TILES, units=UNITS)
        snapshot = snapshot_from_observation(plane.canonical_dict(), plane_id="plane-0")
        self.assertNotIn("seed", snapshot)
        self.assertEqual(snapshot["plane_id"], "plane-0")
        self.assertEqual({tile["id"] for tile in snapshot["tiles"]}, {item["tile_id"] for item in SEED_TILES})


if __name__ == "__main__":
    unittest.main()
