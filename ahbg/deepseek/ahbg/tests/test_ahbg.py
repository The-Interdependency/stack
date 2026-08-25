from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from ahbg.deepseek.ahbg import (
    DeterministicRng,
    EventLog,
    TurnLoop,
    UnresolvedHmmm,
    ValidationError,
    load_world,
    new_game,
    replay,
    save_world,
)
from ahbg.deepseek.run import ucns_seed_board

SEED_TILES = [
    {"tile_id": "c", "q": 0, "r": 0},
    {"tile_id": "e", "q": 1, "r": 0},
    {"tile_id": "se", "q": 0, "r": 1},
    {"tile_id": "sw", "q": -1, "r": 1},
    {"tile_id": "far", "q": 1, "r": 1},
]
SEED_UNITS = [{"unit_id": "A0", "tile_id": "c"}]


def _plan(turn: int, *moves: dict) -> dict:
    return {"turn": turn, "actions": [{"kind": "move", "data": move} for move in moves]}


class WorldTests(unittest.TestCase):
    def test_ucns_seed_board_projects_canonical_ring_centers(self) -> None:
        self.assertEqual(
            ucns_seed_board(),
            [
                {"tile_id": "c", "q": 0, "r": 0},
                {"tile_id": "e", "q": 1, "r": 0},
                {"tile_id": "se", "q": 0, "r": 1},
                {"tile_id": "sw", "q": -1, "r": 1},
                {"tile_id": "w", "q": -1, "r": 0},
                {"tile_id": "nw", "q": 0, "r": -1},
                {"tile_id": "ne", "q": 1, "r": -1},
            ],
        )

    def test_new_game_replays_to_itself(self) -> None:
        world, log = new_game(seed=7, tiles=SEED_TILES, units=SEED_UNITS)
        self.assertEqual(replay(log).canonical_dict(), world.canonical_dict())

    def test_observation_excludes_seed_and_log(self) -> None:
        world, _ = new_game(seed=7, tiles=SEED_TILES, units=SEED_UNITS)
        observation = world.legal_observation()
        self.assertNotIn("seed", observation)
        self.assertEqual(observation["units"][0]["unit_id"], "A0")


class TurnLoopTests(unittest.TestCase):
    def test_simultaneous_moves_resolve_atomically(self) -> None:
        world, log = new_game(
            seed=7,
            tiles=SEED_TILES,
            units=[{"unit_id": "A0", "tile_id": "c"}, {"unit_id": "B0", "tile_id": "sw"}],
        )
        loop = TurnLoop(world=world, log=log)
        loop.begin_turn()
        events = loop.resolve(
            [
                _plan(0, {"unit_id": "A0", "to_tile_id": "e"}),
                _plan(0, {"unit_id": "B0", "to_tile_id": "se"}),
            ]
        )
        self.assertEqual(len(events), 2)
        loop.end_turn()
        self.assertEqual(world.units["A0"].tile_id, "e")
        self.assertEqual(world.units["B0"].tile_id, "se")
        self.assertEqual(replay(log).canonical_dict(), world.canonical_dict())

    def test_occupied_target_fails_closed(self) -> None:
        world, log = new_game(
            seed=7,
            tiles=SEED_TILES,
            units=[{"unit_id": "A0", "tile_id": "c"}, {"unit_id": "B0", "tile_id": "e"}],
        )
        loop = TurnLoop(world=world, log=log)
        loop.begin_turn()
        with self.assertRaises(UnresolvedHmmm):
            loop.resolve([_plan(0, {"unit_id": "A0", "to_tile_id": "e"})])
        # World unchanged after fail-closed resolution.
        self.assertEqual(world.units["A0"].tile_id, "c")

    def test_dual_target_fails_closed(self) -> None:
        world, log = new_game(
            seed=7,
            tiles=SEED_TILES,
            units=[{"unit_id": "A0", "tile_id": "c"}, {"unit_id": "B0", "tile_id": "sw"}],
        )
        loop = TurnLoop(world=world, log=log)
        loop.begin_turn()
        with self.assertRaises(UnresolvedHmmm):
            loop.resolve(
                [
                    _plan(0, {"unit_id": "A0", "to_tile_id": "se"}),
                    _plan(0, {"unit_id": "B0", "to_tile_id": "se"}),
                ]
            )

    def test_unknown_action_kind_fails_closed(self) -> None:
        world, log = new_game(seed=7, tiles=SEED_TILES, units=SEED_UNITS)
        loop = TurnLoop(world=world, log=log)
        loop.begin_turn()
        with self.assertRaises(UnresolvedHmmm):
            loop.resolve([{"turn": 0, "actions": [{"kind": "construct", "data": {}}]}])

    def test_non_adjacent_move_is_rejected(self) -> None:
        world, log = new_game(seed=7, tiles=SEED_TILES, units=SEED_UNITS)
        loop = TurnLoop(world=world, log=log)
        loop.begin_turn()
        with self.assertRaises(ValidationError):
            loop.resolve([_plan(0, {"unit_id": "A0", "to_tile_id": "far"})])
        self.assertEqual(world.units["A0"].tile_id, "c")


class PersistenceTests(unittest.TestCase):
    def test_save_load_replay_round_trip(self) -> None:
        world, log = new_game(seed=7, tiles=SEED_TILES, units=SEED_UNITS)
        with tempfile.TemporaryDirectory() as tmp:
            for step in range(2):
                loop = TurnLoop(world=world, log=log)
                loop.begin_turn()
                target = "e" if step % 2 == 0 else "c"
                loop.resolve([_plan(world.turn, {"unit_id": "A0", "to_tile_id": target})])
                loop.end_turn()
                save_world(tmp, world, log)
                world, log = load_world(tmp)
                self.assertEqual(replay(log).canonical_dict(), world.canonical_dict())
        self.assertEqual(world.turn, 2)

    def test_tampered_events_fail_closed(self) -> None:
        world, log = new_game(seed=7, tiles=SEED_TILES, units=SEED_UNITS)
        with tempfile.TemporaryDirectory() as tmp:
            save_world(tmp, world, log)
            events_path = Path(tmp) / "events.jsonl"
            lines = events_path.read_text(encoding="utf-8").splitlines()
            import json

            first = json.loads(lines[0])
            first["data"]["world"]["seed"] = 999
            events_path.write_text(
                json.dumps(first, sort_keys=True, separators=(",", ":")) + "\n" + "\n".join(lines[1:]) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(Exception):
                load_world(tmp)


class RngTests(unittest.TestCase):
    def test_stream_is_deterministic_and_substreams_are_independent(self) -> None:
        first = DeterministicRng(seed=42, domain="")
        second = DeterministicRng(seed=42, domain="")
        self.assertEqual([first.next_u64() for _ in range(5)], [second.next_u64() for _ in range(5)])
        war = DeterministicRng(seed=42, domain="war")
        dm = DeterministicRng(seed=42, domain="dm")
        self.assertNotEqual(war.next_u64(), dm.next_u64())

    def test_choice_is_within_bounds(self) -> None:
        rng = DeterministicRng(seed=7, domain="test")
        values = [rng.randbelow(10) for _ in range(100)]
        self.assertTrue(all(0 <= value < 10 for value in values))


if __name__ == "__main__":
    unittest.main()
