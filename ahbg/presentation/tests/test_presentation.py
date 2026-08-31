from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ahbg.presentation.geometry import axial_to_xy, center_distance
from ahbg.presentation.project import snapshot_from_observation
from ahbg.presentation.snapshot import PresentationSnapshotError, load_snapshot, validate_snapshot


class PresentationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sample = dict(load_snapshot())

    def test_sample_is_valid(self) -> None:
        self.assertEqual(self.sample["standing"], "not-mechanics")
        self.assertEqual(self.sample["motions"][0]["to"], self.sample["units"][0]["tile"])

    def test_adjacent_visual_centers_are_one_radius_apart(self) -> None:
        radius = 64.0
        self.assertAlmostEqual(
            center_distance(axial_to_xy(0, 0, radius), axial_to_xy(1, 0, radius)),
            radius,
        )

    def test_duplicate_tile_id_and_coordinate_fail_closed(self) -> None:
        for mutation in ("id", "coord"):
            payload = copy.deepcopy(self.sample)
            if mutation == "id":
                payload["tiles"][1]["id"] = payload["tiles"][0]["id"]
            else:
                payload["tiles"][1]["q"] = payload["tiles"][0]["q"]
                payload["tiles"][1]["r"] = payload["tiles"][0]["r"]
            with self.assertRaises(PresentationSnapshotError):
                validate_snapshot(payload)

    def test_bad_unit_tile_and_label_fail_closed(self) -> None:
        payload = copy.deepcopy(self.sample)
        payload["units"][0]["tile"] = []
        with self.assertRaises(PresentationSnapshotError):
            validate_snapshot(payload)

        payload = copy.deepcopy(self.sample)
        payload["units"][0]["label"] = {"bad": True}
        with self.assertRaises(PresentationSnapshotError):
            validate_snapshot(payload)

    def test_motion_destination_must_equal_presented_unit_tile(self) -> None:
        payload = copy.deepcopy(self.sample)
        payload["motions"][0]["to"] = "e"
        with self.assertRaisesRegex(PresentationSnapshotError, "does not match"):
            validate_snapshot(payload)

    def test_projector_uses_package_relative_snapshot_and_validates(self) -> None:
        observation = {
            "turn": 2,
            "tiles": [
                {"tile_id": "c", "q": 0, "r": 0},
                {"tile_id": "ne", "q": 1, "r": -1},
            ],
            "units": [{"unit_id": "A0", "tile_id": "ne", "label": "A0"}],
            "seed": "must-not-leak",
        }
        move = {
            "kind": "move",
            "data": {"unit_id": "A0", "from_tile_id": "c", "to_tile_id": "ne"},
        }
        projected = snapshot_from_observation(
            observation, plane_id="plane-0", move_events=[move]
        )
        self.assertNotIn("seed", projected)
        self.assertEqual(projected["motions"], [{"unit": "A0", "from": "c", "to": "ne"}])

    def test_browser_source_contains_accessibility_and_layer_guards(self) -> None:
        source = (ROOT / "ahbg" / "presentation" / "board.js").read_text(encoding="utf-8")
        for phrase in (
            'hit.setAttribute("tabindex", "0")',
            'event.key === "Enter" || event.key === " "',
            "tile id repeats",
            "q,r must be integers",
            "motion destination for",
            'selectionRing.setAttribute("class", "selection-ring")',
            "tileGroups",
        ):
            self.assertIn(phrase, source)

    def test_sample_json_is_plain_data(self) -> None:
        path = ROOT / "ahbg" / "presentation" / "sample_snapshot.json"
        parsed = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(parsed, self.sample)


if __name__ == "__main__":
    unittest.main()
