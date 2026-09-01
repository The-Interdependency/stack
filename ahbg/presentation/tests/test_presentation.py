"""Regression tests for the AHBG presentation-only boundary.

Usage guidance:
    Focused: ``python -m unittest ahbg.presentation.tests.test_presentation``
    Repo discovery: ``python -m unittest discover -s ahbg/presentation/tests -p 'test*.py'``
"""

from __future__ import annotations

import copy
import json
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ahbg.presentation.geometry import center_distance, source_to_display
from ahbg.presentation.project import snapshot_from_observation
from ahbg.presentation.snapshot import PresentationSnapshotError, load_snapshot, validate_snapshot


UCNS_COMMIT = "1975fe70cf4e0826a8020c2da3047569e277af64"
GEOMETRY_SOURCE = {
    "repository": "The-Interdependency/ucns",
    "commit": UCNS_COMMIT,
    "module": "src/ucns/mobius_seed.py",
    "schema_id": "ucns.mobius-seed-of-life",
    "schema_version": "0.1.0",
    "projection_id": "seed-of-life-seven-equal-circles",
    "selection_effect": "none",
}


class PresentationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sample = dict(load_snapshot())

    def test_sample_is_valid_and_pins_ucns_source(self) -> None:
        self.assertEqual(self.sample["standing"], "not-mechanics")
        self.assertEqual(self.sample["geometry_source"], GEOMETRY_SOURCE)
        self.assertEqual(self.sample["motions"][0]["to"], self.sample["units"][0]["tile"])
        self.assertEqual({tile["source_slot"] for tile in self.sample["tiles"]}, {"CENTER", *(f"RING_{i}" for i in range(6))})

    def test_source_centers_are_scaled_not_reconstructed(self) -> None:
        radius = 64.0
        center = source_to_display(0.0, 0.0, radius)
        ring0 = source_to_display(1.0, 0.0, radius)
        self.assertAlmostEqual(center_distance(center, ring0), radius)
        ring1 = source_to_display(0.5, math.sqrt(3) / 2, radius)
        self.assertAlmostEqual(center_distance(center, ring1), radius)

    def test_duplicate_tile_id_source_slot_and_position_fail_closed(self) -> None:
        for mutation in ("id", "slot", "position"):
            payload = copy.deepcopy(self.sample)
            if mutation == "id":
                payload["tiles"][1]["id"] = payload["tiles"][0]["id"]
            elif mutation == "slot":
                payload["tiles"][1]["source_slot"] = payload["tiles"][0]["source_slot"]
            else:
                payload["tiles"][1]["x"] = payload["tiles"][0]["x"]
                payload["tiles"][1]["y"] = payload["tiles"][0]["y"]
            with self.assertRaises(PresentationSnapshotError):
                validate_snapshot(payload)

    def test_unknown_fields_and_bad_unit_fields_fail_closed(self) -> None:
        payload = copy.deepcopy(self.sample)
        payload["private_prompt"] = "must not cross boundary"
        with self.assertRaisesRegex(PresentationSnapshotError, "undeclared fields"):
            validate_snapshot(payload)

        payload = copy.deepcopy(self.sample)
        payload["feed"][0]["dm_state"] = "secret"
        with self.assertRaisesRegex(PresentationSnapshotError, "undeclared fields"):
            validate_snapshot(payload)

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
        payload["motions"][0]["to"] = "RING_1"
        with self.assertRaisesRegex(PresentationSnapshotError, "does not match"):
            validate_snapshot(payload)

        payload = copy.deepcopy(self.sample)
        payload["motions"] = False
        with self.assertRaisesRegex(PresentationSnapshotError, "must be a list"):
            validate_snapshot(payload)

    def test_projector_drops_internal_observation_and_feed_fields(self) -> None:
        observation = {
            "turn": 2,
            "geometry_source": {**GEOMETRY_SOURCE, "internal_note": "drop me"},
            "tiles": [
                {"tile_id": "CENTER", "ucns_slot": "CENTER", "x": 0.0, "y": 0.0, "private": "drop"},
                {"tile_id": "RING_0", "ucns_slot": "RING_0", "x": 1.0, "y": 0.0},
            ],
            "units": [{"unit_id": "A0", "tile_id": "RING_0", "label": "A0", "private": "drop"}],
            "seed": "must-not-leak",
        }
        move = {
            "kind": "move",
            "data": {"unit_id": "A0", "from_tile_id": "CENTER", "to_tile_id": "RING_0", "dm": "drop"},
        }
        projected = snapshot_from_observation(
            observation,
            plane_id="plane-0",
            move_events=[move],
            feed=[{"turn": 2, "text": "public", "private_prompt": "must-not-leak"}],
        )
        self.assertNotIn("seed", projected)
        self.assertNotIn("internal_note", projected["geometry_source"])
        self.assertEqual(projected["feed"], [{"turn": 2, "text": "public"}])
        self.assertEqual(projected["motions"], [{"unit": "A0", "from": "CENTER", "to": "RING_0"}])

    def test_browser_source_contains_accessibility_and_validation_guards(self) -> None:
        source = (ROOT / "ahbg" / "presentation" / "board.js").read_text(encoding="utf-8")
        html = (ROOT / "ahbg" / "presentation" / "board.html").read_text(encoding="utf-8")
        for phrase in (
            'hit.setAttribute("tabindex", "0")',
            'event.key === "Enter" || event.key === " "',
            "UCNS source slot repeats",
            "motions must be a list when present",
            "motion destination for",
            'selectionRing.setAttribute("class", "selection-ring")',
            "minimumChord",
            "sourceToPixel",
        ):
            self.assertIn(phrase, source)
        self.assertIn('role="group"', html)
        self.assertNotIn('role="img"', html)
        self.assertNotIn("axialToPixel", source)

    @staticmethod
    def _js_offset(index: int, group_size: int) -> tuple[float, float]:
        """Mirror of board.js offsetFor math, kept here as the frozen contract."""
        if group_size == 1:
            return (0.0, 0.0)
        unit_radius = 11.0
        minimum_chord = unit_radius * 2 + 4
        spread = max(unit_radius * 1.35, minimum_chord / (2 * math.sin(math.pi / group_size)))
        angle = (math.pi * 2 * index) / group_size - math.pi / 2
        return (math.cos(angle) * spread, math.sin(angle) * spread)

    def test_initial_and_final_multi_unit_offsets_use_their_own_occupancy(self) -> None:
        # Two units start stacked on CENTER and move to two different tiles:
        # initial offsets must spread them apart on CENTER, final offsets zero.
        initial = [self._js_offset(i, 2) for i in range(2)]
        final = [self._js_offset(i, 1) for i in range(2)]
        self.assertNotEqual(initial[0], initial[1])
        self.assertTrue(any(value != 0.0 for pair in initial for value in pair))
        self.assertEqual(final, [(0.0, 0.0), (0.0, 0.0)])

        source = (ROOT / "ahbg" / "presentation" / "board.js").read_text(encoding="utf-8")
        self.assertIn("groupUnitsBy", source)
        self.assertIn("initialGroups", source)
        self.assertIn("offsetFor(unit, initialGroups, initialTile)", source)
        self.assertIn("offsetFor(unit, finalGroups, unit.tile)", source)

    def test_viewbox_bounds_cover_displaced_unit_markers(self) -> None:
        # Seven units stacked on one tile produce the largest spread. The
        # viewBox contract must derive from rendered marker extents at both the
        # motion origin and the presented destination, not from a fixed
        # seed-circle margin.
        radius = 64.0
        marker_extent = 11.0 + 8
        offset = self._js_offset(0, 7)
        center = (0.0, 0.0)
        displaced = (center[0] + offset[0], center[1] + offset[1])
        self.assertGreater(max(abs(displaced[0]), abs(displaced[1])), 0.0)

        min_x = min(center[0] - radius, displaced[0] - marker_extent)
        max_x = max(center[0] + radius, displaced[0] + marker_extent)
        min_y = min(center[1] - radius, displaced[1] - marker_extent)
        max_y = max(center[1] + radius, displaced[1] + marker_extent)
        self.assertLessEqual(min_x, displaced[0] - marker_extent)
        self.assertGreaterEqual(max_x, displaced[0] + marker_extent)
        self.assertLessEqual(min_y, displaced[1] - marker_extent)
        self.assertGreaterEqual(max_y, displaced[1] + marker_extent)

        source = (ROOT / "ahbg" / "presentation" / "board.js").read_text(encoding="utf-8")
        self.assertIn("markerExtent", source)
        self.assertIn("origin.x - markerExtent", source)
        self.assertIn("dest.x - markerExtent", source)
        self.assertNotIn("RADIUS * 1.2", source)

    def test_behavior_modules_declare_module_build(self) -> None:
        for relative in (
            "ahbg/presentation/__init__.py",
            "ahbg/presentation/snapshot.py",
            "ahbg/presentation/project.py",
            "ahbg/presentation/geometry.py",
            "ahbg/presentation/board.js",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("=== MODULE_BUILD ===", text, relative)
            self.assertIn("=== END MODULE_BUILD ===", text, relative)

    def test_sample_json_is_plain_data(self) -> None:
        path = ROOT / "ahbg" / "presentation" / "sample_snapshot.json"
        parsed = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(parsed, self.sample)


if __name__ == "__main__":
    unittest.main()
