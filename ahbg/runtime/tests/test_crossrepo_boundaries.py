"""Cross-repository boundary witnesses for the AHBG production runtime.

These tests are intentionally narrow.  They prove that AHBG consumes the
current pinned UCNS structural relation ledger for movement and that persisted
UCNS construction state fails closed when its evidence cannot replay.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

STACK_ROOT = Path(__file__).resolve().parents[3]
if str(STACK_ROOT) not in sys.path:
    sys.path.insert(0, str(STACK_ROOT))

from ahbg.runtime.construction import ConstructionError, ConstructionLedger
from ahbg.runtime.engine import load_engine
from ahbg.runtime.provenance import integration_provenance

_patch, _chain, _keep, _round = load_engine()
Field = _patch.Field
tile_from_ucns = _patch.tile_from_ucns

UCNS_SRC = STACK_ROOT / "libs" / "ucns" / "src"
if str(UCNS_SRC) not in sys.path:
    sys.path.insert(0, str(UCNS_SRC))

from ucns.mobius_seed import build_mobius_seed_of_life


class CrossRepositoryBoundaryTests(unittest.TestCase):
    def test_movement_adjacency_is_exactly_ucns_structural_relations(self) -> None:
        seed = build_mobius_seed_of_life()
        expected: set[frozenset[str]] = {
            frozenset((relation.left.value, relation.right.value))
            for relation in seed.structural_relations
        }

        opened = Field.open(
            101,
            tile_from_ucns(),
            [{"unit_id": "A0", "tile_id": "CENTER"}],
        )
        observed: set[frozenset[str]] = set()
        for tile_id in opened.cells:
            for neighbor in opened.neighbors(tile_id):
                observed.add(frozenset((tile_id, neighbor)))

        self.assertEqual(observed, expected)

    def test_axial_projection_cannot_change_movement_authority(self) -> None:
        tiles = tile_from_ucns()
        shifted = [
            {
                **tile,
                "q": int(tile["q"]) * 97 + 41,
                "r": int(tile["r"]) * -89 - 23,
            }
            for tile in tiles
        ]
        canonical = Field.open(
            102,
            tiles,
            [{"unit_id": "A0", "tile_id": "CENTER"}],
        )
        presentation_changed = Field.open(
            102,
            shifted,
            [{"unit_id": "A0", "tile_id": "CENTER"}],
        )

        self.assertEqual(
            {
                tile: tuple(canonical.neighbors(tile))
                for tile in canonical.cells
            },
            {
                tile: tuple(presentation_changed.neighbors(tile))
                for tile in presentation_changed.cells
            },
        )

    def test_run_provenance_binds_agent_and_work_graph_without_status_transfer(self) -> None:
        manifest = {
            "agent": "probe",
            "capabilities": ["observe", "plan", "relocate"],
            "source_commit": "0" * 40,
        }
        first = integration_provenance(manifest)
        second = integration_provenance(manifest)
        self.assertEqual(first, second)
        self.assertEqual(len(first["integration_work_graph_sha256"]), 64)
        self.assertEqual(first["agent_manifest"], manifest)
        self.assertTrue(first["boundaries"])
        self.assertTrue(all(value is False for value in first["boundaries"].values()))

    def test_integration_work_graph_keeps_authority_and_pin_drift_explicit(self) -> None:
        graph = json.loads(
            (STACK_ROOT / "ahbg" / "integration" / "work-graph.json").read_text(
                encoding="utf-8"
            )
        )
        participants = graph["participants"]
        by_repo = {item["repository"]: item for item in participants}
        self.assertEqual(len(by_repo), len(participants))
        self.assertTrue(
            {
                "The-Interdependency/ucns",
                "The-Interdependency/tiwcg",
                "The-Interdependency/a0",
                "The-Interdependency/edcm",
                "The-Interdependency/uchc",
                "The-Interdependency/metapat",
                "The-Interdependency/skill-lib",
                "The-Interdependency/epac",
            }.issubset(by_repo)
        )
        for participant in participants:
            reviewed = participant["reviewed_commit"]
            self.assertEqual(len(reviewed), 40)
            int(reviewed, 16)

        for field, value in graph["boundaries"].items():
            self.assertIs(
                value,
                False,
                msg=f"integration boundary {field} must fail closed",
            )

        manifest = json.loads(
            (STACK_ROOT / "stack-manifest.json").read_text(encoding="utf-8")
        )
        pinned = {
            item["repository"]: item["commit"]
            for item in manifest["repositories"]
        }
        for participant in participants:
            consumed = participant.get("consumed_commit")
            if consumed is not None:
                self.assertEqual(
                    consumed,
                    pinned[participant["repository"]],
                    msg=(
                        "AHBG integration record must move with a consumed stack pin: "
                        + participant["repository"]
                    ),
                )

    def _opened(self) -> object:
        return Field.open(
            103,
            tile_from_ucns(),
            [{"unit_id": "A0", "tile_id": "CENTER"}],
        )

    def _write_ledger(self, directory: Path, payload: dict) -> None:
        (directory / "construction.json").write_text(
            json.dumps(payload) + "\n",
            encoding="utf-8",
        )

    def test_construction_ledger_rejects_unknown_slot_instead_of_dropping_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            self._write_ledger(
                path,
                {
                    "schema": "interdependency.ahbg.construction-ledger/1",
                    "built": ["CENTER", "NOT_A_UCNS_SLOT"],
                    "buildable": [
                        "RING_0", "RING_1", "RING_2",
                        "RING_3", "RING_4", "RING_5",
                    ],
                },
            )
            with self.assertRaisesRegex(ConstructionError, "unknown UCNS slots"):
                ConstructionLedger.load(self._opened(), path)

    def test_construction_ledger_rejects_missing_center(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            self._write_ledger(
                path,
                {
                    "schema": "interdependency.ahbg.construction-ledger/1",
                    "built": ["RING_0"],
                    "buildable": [],
                },
            )
            with self.assertRaisesRegex(ConstructionError, "required CENTER"):
                ConstructionLedger.load(self._opened(), path)

    def test_construction_ledger_rejects_nonreplaying_buildable_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            self._write_ledger(
                path,
                {
                    "schema": "interdependency.ahbg.construction-ledger/1",
                    "built": ["CENTER"],
                    "buildable": ["RING_0"],
                },
            )
            with self.assertRaisesRegex(ConstructionError, "does not replay"):
                ConstructionLedger.load(self._opened(), path)


if __name__ == "__main__":
    unittest.main()
