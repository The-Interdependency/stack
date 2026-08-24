from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ahbg.engine.errors import ReplayMismatch, ValidationError
from ahbg.engine.events import EventLog
from ahbg.engine.persistence import (
    EVENTS_FILE,
    PLANE_FILE,
    load_plane,
    new_game,
    replay,
    save_plane,
)
from ahbg.engine.plane import Plane
from ahbg.engine.turn import TurnEngine

TILES = [
    {"tile_id": "c", "q": 0, "r": 0},
    {"tile_id": "e", "q": 1, "r": 0},
    {"tile_id": "ne", "q": 1, "r": -1},
]
UNITS = [{"unit_id": "A0", "tile_id": "c", "label": "A0"}]


def run_turns(plane: Plane, log: EventLog, count: int) -> None:
    engine = TurnEngine(plane=plane, log=log)
    for _ in range(count):
        engine.begin_turn()
        engine.end_turn()


class PersistenceTests(unittest.TestCase):
    def test_new_game_replays_to_itself(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        replayed = replay(log)
        self.assertEqual(replayed.canonical_dict(), plane.canonical_dict())

    def test_save_load_round_trip_after_turns(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        run_turns(plane, log, count=3)
        self.assertEqual(plane.turn, 3)

        with tempfile.TemporaryDirectory() as tmp:
            save_plane(tmp, plane, log)
            loaded_plane, loaded_log = load_plane(tmp)
            self.assertEqual(loaded_plane.canonical_dict(), plane.canonical_dict())
            self.assertEqual(loaded_log.head_hash, log.head_hash)

    def test_save_writes_expected_files(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        with tempfile.TemporaryDirectory() as tmp:
            save_plane(tmp, plane, log)
            self.assertTrue((Path(tmp) / PLANE_FILE).is_file())
            self.assertTrue((Path(tmp) / EVENTS_FILE).is_file())

    def test_divergent_snapshot_refuses_to_save(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        plane.turn = 5  # snapshot no longer matches the log replay
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ReplayMismatch, "does not match"):
                save_plane(tmp, plane, log)

    def test_tampered_log_refuses_to_load(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        run_turns(plane, log, count=1)
        with tempfile.TemporaryDirectory() as tmp:
            save_plane(tmp, plane, log)
            events_path = Path(tmp) / EVENTS_FILE
            lines = events_path.read_text(encoding="utf-8").splitlines()
            lines[1] = lines[1].replace('"turn":0', '"turn":99', 1)
            events_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ValidationError, "hash chain"):
                load_plane(tmp)

    def test_tampered_snapshot_refuses_to_load(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        with tempfile.TemporaryDirectory() as tmp:
            save_plane(tmp, plane, log)
            plane_path = Path(tmp) / PLANE_FILE
            plane_path.write_text('{"schema":"bogus"}', encoding="utf-8")
            with self.assertRaises(ValidationError):
                load_plane(tmp)

    def test_missing_files_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValidationError, "missing"):
                load_plane(tmp)

    def test_replay_rejects_unknown_event_kinds(self) -> None:
        _, log = new_game(seed=7, tiles=TILES, units=UNITS)
        log.append("move", turn=0, data={})
        with self.assertRaisesRegex(ReplayMismatch, "not canonical"):
            replay(log)

    def test_replay_rejects_turn_phase_violations(self) -> None:
        _, log = new_game(seed=7, tiles=TILES, units=UNITS)
        log.append("turn.end", turn=0, data={"turn": 0, "state_digest": "00" * 32})
        with self.assertRaisesRegex(ReplayMismatch, "awaiting_begin"):
            replay(log)


if __name__ == "__main__":
    unittest.main()
