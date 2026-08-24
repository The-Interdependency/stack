from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ahbg.engine import (
    KIND_MOVE,
    MOVE_ACTION,
    Action,
    Plan,
    TurnEngine,
    UnresolvedHmmm,
    ValidationError,
    load_plane,
    new_game,
    replay,
    save_plane,
)
from ahbg.engine.errors import ReplayMismatch

# Hex ring around center c (0,0) plus one far tile.
TILES = [
    {"tile_id": "c", "q": 0, "r": 0},
    {"tile_id": "e", "q": 1, "r": 0},
    {"tile_id": "ne", "q": 1, "r": -1},
    {"tile_id": "nw", "q": 0, "r": -1},
    {"tile_id": "w", "q": -1, "r": 0},
    {"tile_id": "sw", "q": -1, "r": 1},
    {"tile_id": "se", "q": 0, "r": 1},
    {"tile_id": "far", "q": 3, "r": 0},
]
UNITS = [{"unit_id": "A0", "tile_id": "c", "label": "A0"}]

TWO_UNITS = UNITS + [{"unit_id": "B0", "tile_id": "ne", "label": "B0"}]


def move_plan(turn: int, *actions: Action) -> Plan:
    return Plan(turn=turn, actions=tuple(actions))


def move(unit_id: str, to_tile_id: str) -> Action:
    return Action(MOVE_ACTION, {"unit_id": unit_id, "to_tile_id": to_tile_id})


class MovementResolutionTests(unittest.TestCase):
    def test_legal_move_applies_and_emits_event(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        events = engine.resolve([move_plan(0, move("A0", "e"))])

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].kind, KIND_MOVE)
        self.assertEqual(plane.units["A0"].tile_id, "e")
        self.assertEqual(
            events[0].data,
            {"unit_id": "A0", "from_tile_id": "c", "to_tile_id": "e"},
        )

    def test_empty_plan_resolves_to_no_events(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        self.assertEqual(engine.resolve([move_plan(0)]), [])

    def test_two_legal_moves_apply_atomically(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=TWO_UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        events = engine.resolve(
            [move_plan(0, move("A0", "e"), move("B0", "nw"))]
        )
        self.assertEqual(len(events), 2)
        self.assertEqual(plane.units["A0"].tile_id, "e")
        self.assertEqual(plane.units["B0"].tile_id, "nw")
        self.assertEqual(events[0].data["unit_id"], "A0")  # canonical order

    def test_non_adjacent_move_fails_closed(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        with self.assertRaisesRegex(ValidationError, "not adjacent"):
            engine.resolve([move_plan(0, move("A0", "far"))])
        self.assertEqual(plane.units["A0"].tile_id, "c")  # untouched

    def test_unknown_target_fails_closed(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        with self.assertRaisesRegex(ValidationError, "unknown tile"):
            engine.resolve([move_plan(0, move("A0", "missing"))])

    def test_move_to_self_fails_closed(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        with self.assertRaisesRegex(ValidationError, "must change tiles"):
            engine.resolve([move_plan(0, move("A0", "c"))])

    def test_occupied_target_is_war_and_fails_closed(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=TWO_UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        with self.assertRaisesRegex(UnresolvedHmmm, "War collision"):
            engine.resolve([move_plan(0, move("A0", "ne"))])
        self.assertEqual(plane.units["A0"].tile_id, "c")  # untouched

    def test_two_moves_same_target_are_war_and_fail_closed(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=TWO_UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        with self.assertRaisesRegex(UnresolvedHmmm, "War collision"):
            engine.resolve(
                [move_plan(0, move("A0", "e"), move("B0", "e"))]
            )
        self.assertEqual(plane.units["A0"].tile_id, "c")
        self.assertEqual(plane.units["B0"].tile_id, "ne")

    def test_duplicate_unit_moves_fail_closed(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        with self.assertRaisesRegex(ValidationError, "at most one move"):
            engine.resolve([move_plan(0, move("A0", "e"), move("A0", "w"))])

    def test_unknown_unit_fails_closed(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        with self.assertRaisesRegex(ValidationError, "unknown unit"):
            engine.resolve([move_plan(0, move("Z9", "e"))])

    def test_unknown_action_kind_fails_closed(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        with self.assertRaisesRegex(UnresolvedHmmm, "not yet canonical"):
            engine.resolve([move_plan(0, Action("construct", {}))])

    def test_plan_turn_mismatch_fails_closed(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        with self.assertRaisesRegex(ValidationError, "does not match"):
            engine.resolve([move_plan(1, move("A0", "e"))])

    def test_unknown_move_action_field_fails_closed(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        action = Action(MOVE_ACTION, {"unit_id": "A0", "to_tile_id": "e", "speed": 2})
        with self.assertRaisesRegex(ValidationError, "unknown fields"):
            engine.resolve([move_plan(0, action)])


class MovementReplayTests(unittest.TestCase):
    def test_move_replays_and_persists(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        engine.resolve([move_plan(0, move("A0", "e"))])
        engine.end_turn()

        replayed = replay(log)
        self.assertEqual(replayed.canonical_dict(), plane.canonical_dict())
        self.assertEqual(replayed.units["A0"].tile_id, "e")

        with tempfile.TemporaryDirectory() as tmp:
            save_plane(tmp, plane, log)
            loaded_plane, loaded_log = load_plane(tmp)
            self.assertEqual(loaded_plane.units["A0"].tile_id, "e")
            self.assertEqual(loaded_log.head_hash, log.head_hash)

    def test_move_outside_open_turn_fails_replay(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        engine.resolve([move_plan(0, move("A0", "e"))])
        engine.end_turn()
        # Append a stray move after turn.end: replay must reject it.
        log.append(KIND_MOVE, turn=1, data={
            "unit_id": "A0", "from_tile_id": "e", "to_tile_id": "ne",
        })
        with self.assertRaisesRegex(ReplayMismatch, "outside an open turn"):
            replay(log)

    def test_tampered_move_event_fails_replay(self) -> None:
        plane, log = new_game(seed=7, tiles=TILES, units=UNITS)
        engine = TurnEngine(plane=plane, log=log)
        engine.begin_turn()
        engine.resolve([move_plan(0, move("A0", "e"))])
        engine.end_turn()

        # Rewrite the move event to a chain-consistent but wrong move
        # (c -> nw instead of c -> e). The chain verifies, but the turn.end
        # state digest no longer matches the replayed plane.
        events = list(log.events)
        events[2] = events[2].__class__(
            seq=events[2].seq,
            turn=events[2].turn,
            kind=events[2].kind,
            data={"unit_id": "A0", "from_tile_id": "c", "to_tile_id": "nw"},
            prev_hash=events[1].digest(),
        )
        events[3] = events[3].__class__(
            seq=events[3].seq,
            turn=events[3].turn,
            kind=events[3].kind,
            data=events[3].data,
            prev_hash=events[2].digest(),
        )
        rebuilt = log.__class__()
        for event in events:
            rebuilt._events.append(event)
        rebuilt._head_hash = events[-1].digest()
        rebuilt.verify()  # chain-consistent tamper
        with self.assertRaisesRegex(ReplayMismatch, "state digest"):
            replay(rebuilt)


if __name__ == "__main__":
    unittest.main()
