from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ahbg.engine.errors import ValidationError
from ahbg.engine.plane import Plane, Tile, Unit

TILES = [
    {"tile_id": "c", "q": 0, "r": 0},
    {"tile_id": "e", "q": 1, "r": 0},
    {"tile_id": "ne", "q": 1, "r": -1},
]
UNITS = [{"unit_id": "A0", "tile_id": "c", "label": "A0"}]


def make_plane(seed: int = 7, turn: int = 0) -> Plane:
    plane = Plane.bootstrap(seed=seed, tiles=TILES, units=UNITS)
    plane.turn = turn
    return plane


class PlaneBootstrapTests(unittest.TestCase):
    def test_bootstrap_round_trips(self) -> None:
        plane = make_plane()
        self.assertEqual(plane.turn, 0)
        self.assertEqual(plane.tiles["c"].q, 0)
        self.assertEqual(plane.tiles["c"].r, 0)
        self.assertEqual(plane.units["A0"].tile_id, "c")

    def test_duplicate_tile_id_fails_closed(self) -> None:
        tiles = TILES + [{"tile_id": "c", "q": -1, "r": 0}]
        with self.assertRaisesRegex(ValidationError, "duplicate tile id"):
            Plane.bootstrap(seed=1, tiles=tiles, units=UNITS)

    def test_duplicate_coordinate_fails_closed(self) -> None:
        tiles = TILES + [{"tile_id": "other", "q": 0, "r": 0}]
        with self.assertRaisesRegex(ValidationError, "duplicate axial coordinate"):
            Plane.bootstrap(seed=1, tiles=tiles, units=UNITS)

    def test_unit_on_missing_tile_fails_closed(self) -> None:
        units = [{"unit_id": "A0", "tile_id": "missing", "label": "A0"}]
        with self.assertRaisesRegex(ValidationError, "missing tile"):
            Plane.bootstrap(seed=1, tiles=TILES, units=units)

    def test_empty_declarations_fail_closed(self) -> None:
        with self.assertRaisesRegex(ValidationError, "at least one tile"):
            Plane.bootstrap(seed=1, tiles=[], units=UNITS)
        with self.assertRaisesRegex(ValidationError, "at least one unit"):
            Plane.bootstrap(seed=1, tiles=TILES, units=[])

    def test_unknown_tile_field_fails_closed(self) -> None:
        tiles = [{"tile_id": "c", "q": 0, "r": 0, "color": "red"}]
        with self.assertRaisesRegex(ValidationError, "unknown fields"):
            Plane.bootstrap(seed=1, tiles=tiles, units=UNITS)

    def test_negative_seed_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValidationError, "non-negative"):
            Plane.bootstrap(seed=-1, tiles=TILES, units=UNITS)


class PlaneSerializationTests(unittest.TestCase):
    def test_canonical_dict_is_order_independent(self) -> None:
        plane_a = Plane.bootstrap(
            seed=1, tiles=list(reversed(TILES)), units=UNITS
        )
        plane_b = Plane.bootstrap(seed=1, tiles=TILES, units=UNITS)
        self.assertEqual(plane_a.canonical_dict(), plane_b.canonical_dict())

    def test_digest_is_stable(self) -> None:
        self.assertEqual(make_plane().digest(), make_plane().digest())

    def test_json_round_trip(self) -> None:
        plane = make_plane()
        loaded = Plane.from_json(plane.canonical_json())
        self.assertEqual(loaded.canonical_dict(), plane.canonical_dict())

    def test_bool_coordinates_fail_closed(self) -> None:
        with self.assertRaisesRegex(ValidationError, "non-integer"):
            Tile(tile_id="x", q=True, r=0)  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValidationError, "non-integer"):
            Tile.from_dict({"tile_id": "x", "q": True, "r": 0})

    def test_unit_label_defaults_to_empty(self) -> None:
        unit = Unit(unit_id="u", tile_id="t")
        self.assertEqual(unit.label, "")


if __name__ == "__main__":
    unittest.main()
