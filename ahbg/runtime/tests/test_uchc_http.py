"""Local-only AHBG/UHCH native HTTP contract and adversarial gateway tests."""
from __future__ import annotations

import http.client
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "libs" / "ucns" / "src"))

from ahbg.runtime.server import make_server


class FakeUchc:
    """HTTP transport witness only; real corpus acceptance is separate."""
    @property
    def provenance(self):
        return {"source_repository": "The-Interdependency/uchc",
                "neural_inference": False, "authority_transfer": False}

    @property
    def capabilities(self):
        return {"english.structural_construct": "AVAILABLE",
                "english.word": "AVAILABLE",
                "english.replay": "AVAILABLE",
                "semantic.sense_selection": "UNIMPLEMENTED"}

    def require_capability(self, operation):
        if self.capabilities.get(operation) != "AVAILABLE":
            raise ValueError(f"unsupported source-owned operation: {operation}")

    def construct(self, source):
        return {"source": source, "receipt_sha256": "a" * 64}

    def word(self, surface):
        return {"surface": surface, "origin": "O_W"}

    def replay(self, frame):
        if frame.get("receipt_sha256") != "a" * 64:
            raise ValueError("frame replay mismatch")
        return frame

    def annotate_messages(self, messages, *, source_prefix):
        return tuple({
            "schema": "interdependency.ahbg.uchc-structural-evidence/1",
            "message_ordinal": i, "source_id": f"{source_prefix}:message:{i}",
            "frame": self.construct(message["text"]), "admission": "COMPLETE"
        } for i, message in enumerate(messages))


class HttpUchcTests(unittest.TestCase):
    def setUp(self):
        self.srv = make_server(0, uchc=FakeUchc())
        self.thread = threading.Thread(target=self.srv.serve_forever, daemon=True)
        self.thread.start()
        self.conn = http.client.HTTPConnection("127.0.0.1", self.srv.server_port, timeout=10)

    def tearDown(self):
        self.conn.close()
        self.srv.shutdown()
        self.srv.server_close()
        self.thread.join(timeout=10)

    def request(self, method, path, data=None):
        body = json.dumps(data).encode() if data is not None else None
        headers = {"Content-Type": "application/json"} if body else {}
        self.conn.request(method, path, body=body, headers=headers)
        response = self.conn.getresponse()
        return response.status, json.loads(response.read())

    def test_local_gateway_query_and_refusal(self):
        status, available = self.request("GET", "/uchc/capabilities")
        self.assertEqual(status, 200)
        self.assertEqual(available["capabilities"]["semantic.sense_selection"],
                         "UNIMPLEMENTED")
        status, response = self.request("POST", "/uchc/query", {
            "operation": "english.structural_construct", "text": "geometry"
        })
        self.assertEqual(status, 200)
        self.assertEqual(response["result"]["source"], "geometry")
        status, denied = self.request("POST", "/uchc/query", {
            "operation": "semantic.sense_selection", "text": "geometry"
        })
        self.assertEqual(status, 422)
        self.assertIn("unsupported", denied["error"])

    def test_http_language_source_becomes_harness_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            status, created = self.request("POST", "/session", {
                "seed": 5, "turns": 2, "out_dir": tmp
            })
            self.assertEqual(status, 200)
            key = created["session_id"]
            status, response = self.request(
                "POST", f"/session/{key}/language", {"text": "geometry"}
            )
            self.assertEqual(status, 200)
            self.assertEqual(response["observation"]["inbox"][0]["text"], "geometry")
            self.assertEqual(response["observation"]["language_evidence"][0]
                             ["frame"]["source"], "geometry")
            recorded = (Path(tmp) / "language.jsonl").read_text().splitlines()
            self.assertEqual(len(recorded), 1)
            self.assertEqual(json.loads(recorded[0])["evidence"]["frame"]["source"],
                             "geometry")

    def test_http_transport_rejects_invalid_input(self):
        status, response = self.request("POST", "/uchc/query", {
            "operation": "english.structural_construct",
            "text": "x" * 65537
        })
        self.assertEqual(status, 422)
        self.assertIn("byte limit", response["error"])

    def test_remote_uchc_endpoint_denied_without_authentication(self):
        with self.assertRaisesRegex(ValueError, "loopback"):
            make_server(0, bind="0.0.0.0", uchc=FakeUchc())


if __name__ == "__main__":
    unittest.main()
