"""Real clean-wheel/full-corpus AHBG -> UCHC integration, no mocked producer.

Run only in the existing UCHC full-corpus acceptance job, with
UCHC_INPUT_DATABASE pointing to the verified complete construct.db.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "libs" / "ucns" / "src"))

from ahbg.integration.uchc import UchcConsumerError, UchcSession, UchcSettings
from ahbg.runtime import RuntimeConfig, run_plane


class RecordingAgent:
    def __init__(self):
        self.observations = []

    def manifest(self):
        return {"agent": "uchc-installed-test", "capabilities": ["observe", "plan"]}

    def plan(self, observation):
        self.observations.append(observation)
        return {"session_id": observation["session_id"], "turn": observation["turn"],
                "intents": [], "note": "candidate evidence is not a decision"}


class InstalledUchcTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = os.environ.get("UCHC_INPUT_DATABASE")
        if not raw:
            raise AssertionError("UCHC_INPUT_DATABASE is required: full-corpus gate not configured")
        cls.database = Path(raw)
        cls.lock = ROOT / "research" / "zfae" / "UCHC_INPUT.json"

    def settings(self, **extra):
        return UchcSettings(database=self.database, lock=self.lock, **extra)

    def test_recovery_all_definitions_query_replay_and_unknowns(self):
        with UchcSession(self.settings()) as session:
            provenance = session.provenance
            lock = json.loads(self.lock.read_text())
            self.assertEqual(provenance["wheel_sha256"], lock["wheel_sha256"])
            self.assertGreater(provenance["verified_installed_files"], 0)
            self.assertFalse(provenance["neural_inference"])
            frame = session.resolve_text("alpha letter alpha", source_id="ahbg:test:1")
            frame.require_complete()
            self.assertEqual(frame.recover_utf8(), b"alpha letter alpha")
            self.assertEqual(session.replay(frame.to_bytes()), frame)
            word = session.word("alpha")
            self.assertIsNotNone(word)
            self.assertTrue(word.definition_ids)
            for definition_id in word.definition_ids:
                definition = session.definition(definition_id)
                self.assertEqual(session.recover_definition(definition), definition.text)
            self.assertIsNone(session.word("🧪🧪"))
            partial = session.resolve_text("🧪🧪", source_id="ahbg:unknown")
            self.assertEqual(partial.recover_utf8(), "🧪🧪".encode())
            annotations = session.annotate_messages(
                [{"text": "alpha letter alpha"}, {"source": "none"},
                 {"text": "🧪🧪"}, {"text": "alpha letter alpha"}],
                source_prefix="ahbg:fixture"
            )
            self.assertEqual([e["message_ordinal"] for e in annotations], [0, 2, 3])
            self.assertEqual([e["admission"] for e in annotations],
                             ["COMPLETE", "PARTIAL", "COMPLETE"])
            self.assertNotEqual(annotations[0]["source_id"], annotations[2]["source_id"])
            self.assertEqual(annotations[0]["frame"]["text"], "alpha letter alpha")
            tampered = bytearray(frame.to_bytes())
            tampered[-3] ^= 1
            with self.assertRaises(ValueError):
                session.replay(bytes(tampered))
        with self.assertRaisesRegex(UchcConsumerError, "closed"):
            session.resolve_text("alpha", source_id="after-close")

    def test_strict_admission_refuses_unknown_but_not_full_recovery(self):
        with UchcSession(self.settings(require_complete=True)) as session:
            self.assertEqual(session.resolve_text("alpha", source_id="ok").recover_utf8(), b"alpha")
            with self.assertRaisesRegex(UchcConsumerError, "input refused"):
                session.resolve_text("🧪🧪", source_id="not-admitted")

    def test_bounded_max_bytes_is_explicit_refusal_not_silent_truncation(self):
        with UchcSession(self.settings(max_text_bytes=3)) as session:
            self.assertEqual(session.resolve_text("a", source_id="ok").recover_utf8(), b"a")
            with self.assertRaisesRegex(UchcConsumerError, "exceeds"):
                session.resolve_text("alpha", source_id="reject")

    def test_runtime_replays_with_native_language_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            agent = RecordingAgent()
            msg = {0: [{"text": "alpha letter alpha", "source": "peer"}],
                   1: [{"text": "🧪🧪", "source": "terrain"}]}
            result = run_plane(agent=agent, config=RuntimeConfig(
                seed=17, turns=2, turn_messages=msg,
                uchc_database=str(self.database), uchc_lock=str(self.lock)
            ), out_dir=tmp)
            self.assertEqual(result.final_turn, 2)
            self.assertEqual(agent.observations[0]["inbox"], msg[0])
            self.assertEqual(agent.observations[0]["language_evidence"][0]["admission"],
                             "COMPLETE")
            self.assertEqual(agent.observations[1]["language_evidence"][0]["admission"],
                             "PARTIAL")
            self.assertEqual(result.turn_records[0]["uchc_evidence"],
                             agent.observations[0]["language_evidence"])
            self.assertEqual(result.provenance["uchc"]["wheel_sha256"],
                             json.loads(self.lock.read_text())["wheel_sha256"])
            loaded = json.loads((Path(tmp) / "result.json").read_text())
            self.assertEqual(loaded["turn_records"], list(result.turn_records))
            self.assertEqual(result.turn_records[0]["plan"]["intents"], [])

    def test_invalid_package_lock_refused_before_runtime_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad_lock = Path(tmp) / "bad-lock.json"
            payload = json.loads(self.lock.read_text())
            payload["wheel_sha256"] = "0" * 64
            bad_lock.write_text(json.dumps(payload))
            out = Path(tmp) / "world"
            with self.assertRaisesRegex(UchcConsumerError, "verification/open refused"):
                run_plane(agent=RecordingAgent(), config=RuntimeConfig(
                    turns=1, uchc_database=str(self.database), uchc_lock=str(bad_lock)
                ), out_dir=out)
            self.assertFalse((out / "result.json").exists())


if __name__ == "__main__":
    unittest.main()
