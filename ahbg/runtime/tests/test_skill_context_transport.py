# ratios: loc_comments=121:2 imports_exports=5:4 calls_definitions=66:11
"""Wire tests for adapter negotiation, context loss and restarting a subprocess."""

import json
import sys
import unittest

from ahbg.runtime.harness import SkillContextMiss, SubprocessHarness
from ahbg.runtime.protocol import ProtocolError

VIEW = "a" * 64


def probe(turn):
    return {"session_id": "test", "turn": turn, "view_sha256": VIEW}


def observe(turn, compact=False):
    return {
        "session_id": "test", "turn": turn,
        "skill_library": {"schema": "ahbg.skill-view-ref/1" if compact else "ahbg.skill-view/1",
                          "view_sha256": VIEW},
    }


def adapter(mode):
    """Respond as a distinct line-oriented process with its own lifetime."""
    probes = 0
    for line in sys.stdin:
        message = json.loads(line)
        if message["type"] == "observe":
            obs = message["observation"]
            if mode == "exit-during-observe" and obs["skill_library"]["schema"] == "ahbg.skill-view-ref/1":
                return
            reply = {"type": "plan", "plan": {"turn": obs["turn"]}}
            if mode == "legacy":
                reply["plan"]["skill_context_protocol"] = 1
            else:
                reply["skill_context_protocol"] = 1
            if mode == "miss" and obs["skill_library"]["schema"] == "ahbg.skill-view-ref/1":
                reply = {"type": "skill_context_miss", **probe(obs["turn"])}
        elif message["type"] == "skill_context_probe":
            if mode == "exit-during-probe":
                return
            if mode == "legacy":
                raise ValueError("unexpected probe to a legacy planner")
            if set(message) != {"type", "session_id", "turn", "view_sha256"}:
                raise ValueError("unexpected data in probe")
            probes += 1
            reply = {**message, "type": "skill_context_state", "retained": [],
                     "full_view": probes == 1}
            if mode == "stale":
                reply["turn"] -= 1
        else:
            raise ValueError("unknown adapter message")
        print(json.dumps(reply), flush=True)
        if mode == "exit" and message["type"] == "observe":
            return
        if mode == "exit-after-probe" and message["type"] == "skill_context_probe":
            return


class ContextTransportTests(unittest.TestCase):
    def harness(self, mode):
        command = [sys.executable, "-m", "ahbg.runtime.tests.test_skill_context_transport",
                   "adapter", mode]
        harness = SubprocessHarness(command)
        self.addCleanup(harness.close)
        return harness

    def test_only_outer_opt_in_enables_probes(self):
        agent = self.harness("legacy")
        self.assertIsNone(agent.retained_skill_context(probe(0)))
        self.assertIsNone(agent._process)
        agent.plan(observe(0))
        self.assertIsNone(agent.retained_skill_context(probe(1)))
        self.assertEqual(agent.plan(observe(1))["turn"], 1)

    def test_fresh_probe_uses_current_adapter_state_without_forwarding_extras(self):
        agent = self.harness("opt-in")
        agent.plan(observe(0))
        first = agent.retained_skill_context({**probe(1), "instructions": "host-only"})
        self.assertTrue(first["full_view"])
        self.assertEqual(agent.plan(observe(1, True)), {"turn": 1})
        second = agent.retained_skill_context(probe(2))
        self.assertFalse(second["full_view"])
        agent.plan(observe(2))
        agent.close()
        self.assertIsNone(agent.retained_skill_context(probe(3)))

    def test_exited_process_restarts_only_with_full_delivery(self):
        agent = self.harness("exit")
        agent.plan(observe(0))
        agent._process.wait(timeout=5)
        self.assertIsNone(agent.retained_skill_context(probe(1)))
        self.assertEqual(agent.plan(observe(1)), {"turn": 1})

        agent = self.harness("exit-after-probe")
        agent.plan(observe(0))
        self.assertTrue(agent.retained_skill_context(probe(1))["full_view"])
        agent._process.wait(timeout=5)
        with self.assertRaises(SkillContextMiss) as miss:
            agent.plan(observe(1, True))
        self.assertFalse(miss.exception.sent)
        self.assertEqual(agent.plan(observe(1)), {"turn": 1})

    def test_only_a_preflight_disconnect_allows_safe_restart(self):
        agent = self.harness("exit-during-probe")
        agent.plan(observe(0))
        self.assertIsNone(agent.retained_skill_context(probe(1)))
        self.assertIsNone(agent._process)
        self.assertEqual(agent.plan(observe(1)), {"turn": 1})

        agent = self.harness("exit-during-observe")
        agent.plan(observe(0))
        self.assertTrue(agent.retained_skill_context(probe(1))["full_view"])
        with self.assertRaises(ProtocolError) as disconnected:
            agent.plan(observe(1, True))
        self.assertNotIsInstance(disconnected.exception, SkillContextMiss)

    def test_stale_echo_never_authorizes_a_reference(self):
        agent = self.harness("stale")
        agent.plan(observe(0))
        self.assertIsNone(agent.retained_skill_context(probe(1)))
        with self.assertRaises(ProtocolError):
            agent.plan(observe(1, True))
        self.assertEqual(agent.plan(observe(1)), {"turn": 1})

    def test_explicit_preplan_miss_allows_full_retry_once(self):
        agent = self.harness("miss")
        agent.plan(observe(0))
        agent.retained_skill_context(probe(1))
        with self.assertRaises(SkillContextMiss) as miss:
            agent.plan(observe(1, True))
        self.assertTrue(miss.exception.sent)
        with self.assertRaises(ProtocolError):
            agent.plan(observe(1, True))
        self.assertEqual(agent.plan(observe(1)), {"turn": 1})


if __name__ == "__main__":
    if sys.argv[1:2] == ["adapter"]:
        adapter(sys.argv[2])
    else:
        unittest.main()
# ratios: loc_comments=121:2 imports_exports=5:4 calls_definitions=66:11
