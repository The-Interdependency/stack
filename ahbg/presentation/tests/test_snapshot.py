from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from geometry import adjacent_center_pairs, axial_to_xy, center_distance
from snapshot import KIND, PresentationSnapshotError, load_snapshot, validate_snapshot


class PresentationSnapshotTest(unittest.TestCase):
    def test_sample_loads(self) -> None:
        snapshot = load_snapshot()
        self.assertEqual(snapshot["kind"], KIND)
        self.assertEqual(snapshot["standing"], "not-mechanics")
        self.assertEqual(len(snapshot["tiles"]), 7)
        self.assertEqual(snapshot["units"][0]["id"], "A0")

    def test_unknown_unit_tile_fails_closed(self) -> None:
        snapshot = copy.deepcopy(dict(load_snapshot()))
        snapshot["units"] = [{"id": "A0", "tile": "missing", "label": "A0"}]
        with self.assertRaisesRegex(PresentationSnapshotError, "not a presented tile"):
            validate_snapshot(snapshot)

    def test_seed_of_life_centers_are_one_radius_apart(self) -> None:
        radius = 10.0
        origin = axial_to_xy(0, 0, radius)
        east = axial_to_xy(1, 0, radius)
        self.assertAlmostEqual(center_distance(origin, east), radius)
        tiles = [(0, 0), (1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]
        pairs = adjacent_center_pairs(tiles, radius)
        self.assertEqual(len(pairs), 12)
        for left, right in pairs:
            self.assertAlmostEqual(
                center_distance(axial_to_xy(*left, radius), axial_to_xy(*right, radius)),
                radius,
            )

    def test_sample_motion_is_a_visual_trace_not_mechanics(self) -> None:
        snapshot = load_snapshot()
        self.assertEqual(snapshot["units"][0]["tile"], "ne")
        self.assertEqual(snapshot["motions"], [{"unit": "A0", "from": "c", "to": "ne"}])
        source = (ROOT / "snapshot.py").read_text(encoding="utf-8")
        self.assertNotIn("adjacent", source.lower())
        self.assertNotIn("war", source.lower())

    def test_unknown_motion_tile_fails_closed(self) -> None:
        snapshot = copy.deepcopy(dict(load_snapshot()))
        snapshot["motions"] = [{"unit": "A0", "from": "c", "to": "missing"}]
        with self.assertRaisesRegex(PresentationSnapshotError, "not a presented tile"):
            validate_snapshot(snapshot)

    def test_wrong_kind_fails_closed(self) -> None:
        snapshot = copy.deepcopy(dict(load_snapshot()))
        snapshot["kind"] = "ahbg.plane"
        with self.assertRaisesRegex(PresentationSnapshotError, "kind must be"):
            validate_snapshot(snapshot)


if __name__ == "__main__":
    unittest.main()
