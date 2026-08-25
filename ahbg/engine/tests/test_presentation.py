from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ahbg.engine import (
    MOVE_ACTION,
    Action,
    Plan,
    ReplayMismatch,
    TurnEngine,
    ValidationError,
    new_game,
    snapshot_from_plane,
)
from ahbg.presentation.snapshot import KIND, validate_snapshot

TILES = [
    {"tile_id": "c", "q": 0, "r": 0},
    {"tile_id": "e", "q": 1, "r": 0},
    {"tile_id": "ne", "q": 1, "r": -1},
]
UNITS = [{"unit_id": "A0", "tile_id": "c", "label": "A0"}]


def move_plan(turn: int, unit_id: str, to_tile_id: str) -> Plan:
    return Plan(turn=turn, actions=(Action(MOVE_ACTION, {
        "unit_id": unit_id,
        "to_tile_id": to_tile_id,
    }),))


class PresentationProjectionTests(unittest.TestCase):
    def test_engine_plane_exports_valid_presentation_snapshot(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        engine.resolve([move_plan(0, "A0", "ne")])
        engine.end_turn()

        snapshot = snapshot_from_plane(plane, log, plane_id="plane-0")

        self.assertEqual(snapshot["kind"], KIND)
        self.assertEqual(snapshot["turn"], 1)
        self.assertEqual(snapshot["units"], [{"id": "A0", "tile": "ne", "label": "A0"}])
        self.assertEqual(snapshot["selected_tile"], "ne")
        self.assertEqual(snapshot["motions"], [{"unit": "A0", "from": "c", "to": "ne"}])
        self.assertIn({"turn": 0, "text": "A0 move c to ne"}, snapshot["feed"])
        validate_snapshot(snapshot)

    def test_default_motion_traces_are_last_completed_turn_only(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        engine.resolve([move_plan(0, "A0", "e")])
        engine.end_turn()
        engine.begin_turn()
        engine.resolve([move_plan(1, "A0", "ne")])
        engine.end_turn()

        snapshot = snapshot_from_plane(plane, log)

        self.assertEqual(snapshot["turn"], 2)
        self.assertEqual(snapshot["motions"], [{"unit": "A0", "from": "e", "to": "ne"}])
        validate_snapshot(snapshot)

    def test_unreplayed_log_refuses_presentation_snapshot(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        plane.turn = 3

        with self.assertRaisesRegex(ReplayMismatch, "does not replay"):
            snapshot_from_plane(plane, log)

    def test_unknown_selected_tile_fails_closed(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)

        with self.assertRaisesRegex(ValidationError, "selected_tile_id"):
            snapshot_from_plane(plane, log, selected_tile_id="missing")


if __name__ == "__main__":
    unittest.main()
