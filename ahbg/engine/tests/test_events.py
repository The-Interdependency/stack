from __future__ import annotations

import dataclasses
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ahbg.engine.errors import ValidationError
from ahbg.engine.events import KIND_PLANE_INIT, KIND_TURN_BEGIN, EventLog
from ahbg.engine.persistence import new_game

TILES = [
    {"tile_id": "c", "q": 0, "r": 0},
    {"tile_id": "e", "q": 1, "r": 0},
]
UNITS = [{"unit_id": "A0", "tile_id": "c", "label": "A0"}]


def make_log() -> EventLog:
    _, log = new_game(seed=3, tiles=TILES, units=UNITS)
    log.append(KIND_TURN_BEGIN, turn=0, data={"turn": 0})
    return log


class EventLogTests(unittest.TestCase):
    def test_first_event_must_be_plane_init(self) -> None:
        log = EventLog()
        with self.assertRaisesRegex(ValidationError, "first event"):
            log.append(KIND_TURN_BEGIN, turn=0, data={})

    def test_hash_chain_verifies(self) -> None:
        log = make_log()
        log.verify()
        self.assertNotEqual(log.head_hash, "")
        self.assertEqual(log.events[0].prev_hash, "")
        self.assertEqual(log.events[1].prev_hash, log.events[0].digest())

    def test_tampered_event_breaks_verification(self) -> None:
        log = make_log()
        log._events[1] = dataclasses.replace(log._events[1], data={"turn": 99})
        with self.assertRaisesRegex(ValidationError, "hash chain|does not match its chain"):
            log.verify()

    def test_truncated_log_breaks_verification(self) -> None:
        log = make_log()
        log._events = log._events[:-1]
        with self.assertRaisesRegex(ValidationError, "head hash"):
            log.verify()

    def test_turns_must_be_non_decreasing(self) -> None:
        log = make_log()
        with self.assertRaisesRegex(ValidationError, "non-decreasing"):
            log.append(KIND_TURN_BEGIN, turn=-1, data={})

    def test_jsonl_round_trip(self) -> None:
        log = make_log()
        reloaded = EventLog.from_jsonl(log.to_jsonl())
        self.assertEqual(reloaded.head_hash, log.head_hash)
        self.assertEqual(reloaded.to_jsonl(), log.to_jsonl())

    def test_empty_log_round_trips(self) -> None:
        log = EventLog()
        self.assertEqual(EventLog.from_jsonl(log.to_jsonl()).head_hash, "")

    def test_kind_and_data_are_validated(self) -> None:
        _, log = new_game(seed=3, tiles=TILES, units=UNITS)
        with self.assertRaisesRegex(ValidationError, "non-empty string"):
            log.append("", turn=0, data={})
        with self.assertRaisesRegex(ValidationError, "must be an object"):
            log.append(KIND_TURN_BEGIN, turn=0, data=[])  # type: ignore[arg-type]

    def test_plane_init_is_the_only_first_kind(self) -> None:
        log = EventLog()
        log.append(KIND_PLANE_INIT, turn=0, data={"plane": {}})
        self.assertEqual(len(log), 1)


if __name__ == "__main__":
    unittest.main()
