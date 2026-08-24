from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

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

    def test_wrong_kind_fails_closed(self) -> None:
        snapshot = copy.deepcopy(dict(load_snapshot()))
        snapshot["kind"] = "ahbg.plane"
        with self.assertRaisesRegex(PresentationSnapshotError, "kind must be"):
            validate_snapshot(snapshot)


if __name__ == "__main__":
    unittest.main()
