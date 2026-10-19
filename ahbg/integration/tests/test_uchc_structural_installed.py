"""Native AHBG ↔ UCHC 0.1.0a2 structural corpus acceptance.

UCHC_STRUCTURAL_FIELD must point to the complete exact, clean-wheel-built
field; no partial fixture can satisfy this test.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "libs" / "ucns" / "src"))

from ahbg.integration.uchc_structural import (
    UchcStructuralSession, UchcStructuralSettings, UchcStructuralError
)
from ahbg.runtime import RuntimeConfig, run_plane


class Observer:
    def __init__(self):
        self.seen = []

    def manifest(self):
        return {"agent": "structural-consumer-test",
                "capabilities": ["observe", "plan"]}

    def plan(self, observation):
        self.seen.append(observation)
        return {"session_id": observation["session_id"], "turn": observation["turn"],
                "intents": [], "note": "no geometry or sense inference"}


class StructuralInstalledTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = os.getenv("UCHC_STRUCTURAL_FIELD")
        if not raw:
            raise AssertionError("UCHC_STRUCTURAL_FIELD is required (complete producer field)")
        cls.field_dir = Path(raw)
        cls.lock = ROOT / "ahbg" / "integration" / "UCHC_STRUCTURAL.json"

    def test_native_structural_construction_replay_and_all_public_queries(self):
        with UchcStructuralSession(UchcStructuralSettings(self.field_dir)) as session:
            provenance = session.provenance
            pinned = json.loads(self.lock.read_text())
            self.assertEqual(provenance["wheel_sha256"], pinned["wheel_sha256"])
            self.assertEqual(provenance["database_sha256"], pinned["database_sha256"])
            self.assertFalse(provenance["authority_transfer"])
            text = "Dr. creates geometry. Dr. creates 3.14..."
            graph = session.construct(text)
            self.assertEqual(graph["source"], text)
            self.assertEqual(session.replay(graph), graph)
            closed_word = session.word("geometry")
            self.assertTrue(closed_word["closed"])
            self.assertIn("glyph_axis_set", closed_word)
            with sqlite3.connect(f"file:{self.field_dir / 'construct.db'}?mode=ro",
                                 uri=True) as db:
                definition_id = db.execute(
                    "SELECT id FROM records WHERE kind='definition' ORDER BY id LIMIT 1"
                ).fetchone()[0]
            definition = session.definition(definition_id)
            self.assertEqual(definition["record_id"], definition_id)
            self.assertTrue(definition["parts"])
            result = session.compose(graph, relation="ordered-text")
            self.assertIsInstance(result, dict)
            with self.assertRaisesRegex(UchcStructuralError, "unlicensed"):
                session.compose(graph, relation="invented-global-transport")
            with self.assertRaisesRegex(UchcStructuralError, "UNIMPLEMENTED"):
                session.require_capability("ucns.global_displacement")
            unknown = session.construct("🧪🧪")
            self.assertTrue(unknown["refusals"])
            evidence = session.annotate_messages(
                [{"text": text}, {"kind": "metric"}, {"text": "🧪🧪"}],
                source_prefix="ahbg:structural")
            self.assertEqual([x["message_ordinal"] for x in evidence], [0, 2])
            self.assertEqual(evidence[0]["frame"]["source"], text)
            self.assertEqual(evidence[1]["admission"], "PARTIAL")
        with self.assertRaisesRegex(UchcStructuralError, "closed"):
            session.word("geometry")

    def test_strict_admission_refuses_and_preserves_approved_source(self):
        with UchcStructuralSession(UchcStructuralSettings(
            self.field_dir, require_complete=True
        )) as session:
            self.assertEqual(session.construct("geometry")["source"], "geometry")
            with self.assertRaisesRegex(UchcStructuralError, "incomplete"):
                session.construct("🧪🧪")

    def test_structural_runtime_and_persistence(self):
        with tempfile.TemporaryDirectory() as tmp:
            agent = Observer()
            result = run_plane(agent=agent, config=RuntimeConfig(
                turns=2, seed=23, uchc_structural_field=str(self.field_dir),
                turn_messages={0: [{"text": "geometry", "source": "peer"}],
                               1: [{"text": "🧪🧪", "source": "terrain"}]}
            ), out_dir=tmp)
            self.assertEqual(result.final_turn, 2)
            self.assertEqual(result.config["uchc"]["profile"], "english.structural/1")
            self.assertEqual(result.provenance["uchc"]["profile"], "english.structural/1")
            self.assertEqual(agent.seen[0]["inbox"][0]["text"], "geometry")
            self.assertEqual(agent.seen[0]["language_evidence"][0]["frame"]["source"],
                             "geometry")
            self.assertEqual(result.turn_records[1]["uchc_evidence"][0]["admission"],
                             "PARTIAL")
            self.assertEqual(len(result.turn_records[0]["plan"]["intents"]), 0)
            saved = json.loads((Path(tmp) / "result.json").read_text())
            self.assertEqual(saved["provenance"]["uchc"], result.provenance["uchc"])

    def test_wrong_structural_lock_fails_before_game_setup(self):
        with tempfile.TemporaryDirectory() as tmp:
            payload = json.loads(self.lock.read_text())
            payload["wheel_sha256"] = "0" * 64
            altered = Path(tmp) / "altered-lock.json"
            altered.write_text(json.dumps(payload))
            with self.assertRaisesRegex(UchcStructuralError, "refused"):
                with UchcStructuralSession(UchcStructuralSettings(
                    self.field_dir, lock=altered
                )):
                    self.fail("wrong wheel was admitted")

    def test_explicit_byte_limit_refuses_without_truncation(self):
        with UchcStructuralSession(UchcStructuralSettings(
            self.field_dir, max_text_bytes=3
        )) as session:
            self.assertEqual(session.construct("a")["source"], "a")
            with self.assertRaisesRegex(UchcStructuralError, "exceeds"):
                session.construct("geometry")


if __name__ == "__main__":
    unittest.main()
