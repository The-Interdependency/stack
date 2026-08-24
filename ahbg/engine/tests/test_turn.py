from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ahbg.engine.adapter import Plan, legal_observation
from ahbg.engine.errors import UnresolvedHmmm
from ahbg.engine.events import KIND_TURN_BEGIN, KIND_TURN_END
from ahbg.engine.persistence import load_plane, new_game, replay, save_plane
from ahbg.engine.turn import TurnEngine

TILES = [
    {"tile_id": "c", "q": 0, "r": 0},
    {"tile_id": "e", "q": 1, "r": 0},
    {"tile_id": "ne", "q": 1, "r": -1},
]
UNITS = [{"unit_id": "A0", "tile_id": "c", "label": "A0"}]


class TurnEnvelopeTests(unittest.TestCase):
    def test_begin_and_end_advance_the_turn(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        begin = engine.begin_turn()
        end = engine.end_turn()

        self.assertEqual(begin.kind, KIND_TURN_BEGIN)
        self.assertEqual(end.kind, KIND_TURN_END)
        self.assertEqual(plane.turn, 1)
        self.assertRegex(log.events[-1].data["state_digest"], r"^[0-9a-f]{64}$")

    def test_state_digest_records_pre_advance_plane(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        before_advance = plane.digest()
        engine.end_turn()
        self.assertEqual(log.events[-1].data["state_digest"], before_advance)

    def test_full_loop_repeats_from_persisted_state(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)

        with tempfile.TemporaryDirectory() as tmp:
            for _ in range(2):
                engine = TurnEngine(plane=plane, log=log)
                engine.begin_turn()
                engine.end_turn()
                save_plane(tmp, plane, log)
                plane, log = load_plane(tmp)
                self.assertEqual(replay(log).canonical_dict(), plane.canonical_dict())

        self.assertEqual(plane.turn, 2)

    def test_resolve_fails_closed_on_unresolved_mechanics(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        with self.assertRaisesRegex(UnresolvedHmmm, "not yet canonical"):
            engine.resolve([Plan(turn=0, actions=())])

    def test_observation_excludes_engine_internals(self) -> None:
        plane, _ = new_game(seed=7, tiles=TILES, units=UNITS)
        observation = legal_observation(plane)
        self.assertEqual(observation.turn, 0)
        self.assertEqual(len(observation.tiles), 3)
        self.assertEqual(observation.units[0]["unit_id"], "A0")
        self.assertNotIn("seed", observation.to_dict())
        self.assertNotIn("log", observation.to_dict())

    def test_empty_plan_round_trips_through_the_envelope(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        # The plan phase is the adapter's; an empty plan is structurally fine,
        # but resolving any plan is mechanics and remains fail-closed.
        engine.end_turn()
        self.assertEqual(plane.turn, 1)
        self.assertEqual(replay(log).turn, 1)


if __name__ == "__main__":
    unittest.main()
