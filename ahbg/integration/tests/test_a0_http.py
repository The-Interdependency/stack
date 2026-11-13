from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from ahbg.integration.a0_http import A0AdapterError, A0HTTPHarness
from ahbg.runtime.runtime import RuntimeConfig, run_plane

A0_SHA = "ad958a4e5f4cdb17ba815539d2e6a545034db161"


class FakeA0:
    def __init__(self, *, provider: str = "deepseek") -> None:
        self.provider = provider
        self.calls: list[tuple[str, str, dict | None]] = []

    def __call__(self, method: str, path: str, payload):
        copied = None if payload is None else dict(payload)
        self.calls.append((method, path, copied))
        if method == "POST" and path == "/api/v1/conversations":
            return {"id": 17}
        if method == "PUT" and path == "/api/v1/conversations/17/boost":
            return {"ok": True, "conversation_id": 17}
        if method == "PATCH" and path == "/api/v1/conversations/17/inference-settings":
            return {"ok": True, "conversation_id": 17, **copied}
        if method == "POST" and path == "/api/v1/conversations/17/messages":
            raw = copied["content"]
            assert raw.startswith("AHBG_OBSERVATION\n")
            observation = json.loads(raw.split("\n", 1)[1])
            legal = observation.get("legal") or []
            intents = [legal[0]] if legal else []
            plan = {
                "schema": "interdependency.ahbg.harness.plan/1",
                "session_id": observation["session_id"],
                "turn": observation["turn"],
                "intents": intents,
                "note": "fake-a0-plan",
            }
            pinned = copied.get("model")
            harness_mode = "explicit-pin" if pinned else "continuous-auto"
            attempted = [pinned] if pinned else ["auto-seed", self.provider]
            return {
                "conversation_id": 17,
                "assistant_message": {
                    "content": json.dumps(plan),
                    "model": self.provider,
                    "metadata": {
                        "inference_mode": "direct",
                        "usage": {
                            "model_id": pinned or "resolved-model",
                            "input_tokens": 101,
                            "output_tokens": 17,
                            "harness": {
                                "mode": harness_mode,
                                "attempted_models": attempted,
                                "fallback_count": max(0, len(attempted) - 1),
                                "actual_provider": self.provider,
                                "tool_executions": 0,
                            },
                        },
                    },
                },
            }
        raise AssertionError(f"unexpected fake request {method} {path}")


class A0HTTPHarnessTests(unittest.TestCase):
    def test_model_trial_is_explicitly_pinned_and_provenanced(self) -> None:
        fake = FakeA0(provider="openai")
        harness = A0HTTPHarness(
            base_url="https://a0.example",
            user_id="benchmark-user",
            a0_source_commit=A0_SHA,
            execution_mode="model",
            model="gpt-test",
            request_json=fake,
        )
        with tempfile.TemporaryDirectory() as tmp:
            result = run_plane(
                agent=harness,
                config=RuntimeConfig(seed=41, turns=2),
                out_dir=Path(tmp),
            )

        sends = [
            payload
            for method, path, payload in fake.calls
            if method == "POST" and path.endswith("/messages")
        ]
        self.assertEqual(len(sends), 2)
        self.assertTrue(all(row["model"] == "gpt-test" for row in sends))
        self.assertEqual(
            result.provenance["agent_manifest"]["execution_mode"],
            "model",
        )
        for record in result.turn_records:
            provenance = record["agent_provenance"]
            self.assertEqual(provenance["assistant_model"], "openai")
            self.assertEqual(provenance["harness"]["mode"], "explicit-pin")
            self.assertEqual(provenance["harness"]["fallback_count"], 0)
            self.assertEqual(provenance["a0_source_commit"], A0_SHA)

    def test_a0_continuity_omits_model_pin_and_retains_fallback_provenance(self) -> None:
        fake = FakeA0(provider="deepseek")
        harness = A0HTTPHarness(
            base_url="https://a0.example",
            user_id="benchmark-user",
            a0_source_commit=A0_SHA,
            execution_mode="a0-continuity",
            request_json=fake,
        )
        observation = {
            "schema": "interdependency.ahbg.harness.observation/1",
            "session_id": "s1",
            "turn": 0,
            "field": {"units": []},
            "capabilities": ["observe", "plan", "relocate", "construct"],
            "legal": [],
            "feed": [],
            "inbox": [],
            "entitlements": ["basic"],
            "deadline_ms": 5000,
        }
        plan = harness.plan(observation)
        self.assertEqual(plan["intents"], [])

        create = fake.calls[0][2]
        send = next(
            payload
            for method, path, payload in fake.calls
            if method == "POST" and path.endswith("/messages")
        )
        self.assertNotIn("model", create)
        self.assertNotIn("model", send)
        provenance = harness.turn_provenance()
        self.assertEqual(provenance["execution_mode"], "a0-continuity")
        self.assertEqual(
            provenance["harness"]["attempted_models"],
            ["auto-seed", "deepseek"],
        )
        self.assertEqual(provenance["harness"]["fallback_count"], 1)

    def test_continuity_rejects_accidental_model_pin(self) -> None:
        with self.assertRaisesRegex(A0AdapterError, "must not carry"):
            A0HTTPHarness(
                base_url="https://a0.example",
                user_id="benchmark-user",
                a0_source_commit=A0_SHA,
                execution_mode="a0-continuity",
                model="should-not-be-here",
                request_json=FakeA0(),
            )

    def test_source_identity_is_exact_commit(self) -> None:
        with self.assertRaisesRegex(A0AdapterError, "40-hex"):
            A0HTTPHarness(
                base_url="https://a0.example",
                user_id="benchmark-user",
                a0_source_commit="main",
                execution_mode="model",
                model="gpt-test",
                request_json=FakeA0(),
            )


if __name__ == "__main__":
    unittest.main()
