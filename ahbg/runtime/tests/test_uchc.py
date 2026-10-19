"""AHBG UCHC boundary tests with and without the optional installed wheel."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "libs" / "ucns" / "src"))

from ahbg.integration.uchc import UchcConsumerError, UchcSession, UchcSettings
from ahbg.runtime import RuntimeConfig, ProtocolError, run_plane


class Agent:
    def __init__(self):
        self.observations = []

    def manifest(self):
        return {"agent": "native-language-probe", "capabilities": ["observe", "plan", "relocate"]}

    def plan(self, observation):
        self.observations.append(observation)
        return {"session_id": observation["session_id"], "turn": observation["turn"],
                "intents": [], "note": "no semantic action"}


class FakeVerifiedSession:
    """Unit witness for the runtime wiring, not a substitute UCHC corpus."""

    def __init__(self):
        self.prefixes = []

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        pass

    @property
    def provenance(self):
        return {"schema": "interdependency.ahbg.uchc-provenance/1",
                "authority_transfer": False, "neural_inference": False}

    def annotate_messages(self, messages, *, source_prefix):
        self.prefixes.append(source_prefix)
        return tuple({
            "schema": "interdependency.ahbg.uchc-evidence/1",
            "source_id": f"{source_prefix}:message:{ordinal}",
            "message_ordinal": ordinal,
            "admission": "COMPLETE",
            "frame": {"text": message["text"], "receipt_sha256": "0" * 64},
        } for ordinal, message in enumerate(messages) if "text" in message)


class UchcRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_runtime_consumes_evidence_on_each_turn_without_changing_actions(self):
        agent = Agent()
        fake = FakeVerifiedSession()
        messages = {
            0: [{"text": "alpha letter alpha", "source": "peer"},
                {"source": "nonlexical", "kind": "metric"}],
            1: [{"text": "alpha letter alpha", "source": "peer"}],
        }
        with patch("ahbg.integration.uchc.UchcSession", return_value=fake) as opened:
            result = run_plane(agent=agent, config=RuntimeConfig(
                seed=5, turns=2, turn_messages=messages,
                uchc_database="/data/construct.db", uchc_require_complete=True
            ), out_dir=self.root)
        self.assertEqual(opened.call_count, 1)
        self.assertTrue(opened.call_args.args[0].require_complete)
        self.assertEqual(len(fake.prefixes), 2)
        self.assertEqual(result.final_turn, 2)
        self.assertEqual(len(agent.observations[0]["language_evidence"]), 1)
        self.assertEqual(agent.observations[0]["inbox"], messages[0])
        self.assertEqual(result.turn_records[0]["plan"]["intents"], [])
        self.assertEqual(result.turn_records[0]["uchc_evidence"],
                         agent.observations[0]["language_evidence"])
        self.assertTrue(result.provenance["uchc"]["schema"].endswith("provenance/1"))
        self.assertEqual(json.loads((self.root / "result.json").read_text())
                         ["turn_records"][0]["uchc_evidence"],
                         result.turn_records[0]["uchc_evidence"])

    def test_without_uchc_preserves_old_observation_and_receipt_shape(self):
        agent = Agent()
        result = run_plane(agent=agent, config=RuntimeConfig(turns=1), out_dir=self.root)
        self.assertNotIn("language_evidence", agent.observations[0])
        self.assertNotIn("uchc", result.provenance)
        self.assertNotIn("uchc_evidence", result.turn_records[0])
        self.assertNotIn("uchc", result.config)

    def test_uchc_settings_without_database_fail_closed(self):
        for settings in (
            RuntimeConfig(turns=0, uchc_lock="custom.json"),
            RuntimeConfig(turns=0, uchc_require_complete=True),
            RuntimeConfig(turns=0, uchc_max_text_bytes=128),
        ):
            with self.assertRaisesRegex(ProtocolError, "UCHC settings require"):
                run_plane(agent=Agent(), config=settings, out_dir=self.root)

    def test_absent_or_invalid_lock_refuses_before_gameplay(self):
        settings = UchcSettings(database=self.root / "missing.db",
                               lock=self.root / "missing.json")
        with self.assertRaisesRegex(UchcConsumerError, "verification/open refused"):
            with UchcSession(settings):
                self.fail("invalid artifact was admitted")

    def test_bad_limits_and_closed_handle_refuse(self):
        with self.assertRaises(UchcConsumerError):
            UchcSession(UchcSettings(self.root / "unused", max_text_bytes=0))
        session = UchcSession(UchcSettings(self.root / "unused"))
        with self.assertRaisesRegex(UchcConsumerError, "closed"):
            session.word("alpha")
        with self.assertRaisesRegex(UchcConsumerError, "closed"):
            session.replay(b"{}")


if __name__ == "__main__":
    unittest.main()
