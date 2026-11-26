# ratios: loc_comments=138:2 imports_exports=6:2 calls_definitions=77:10
"""Check actual model history at the acknowledgement and delivery boundaries."""
import hashlib
import json
from io import StringIO
import unittest
from copy import deepcopy

from ahbg.integration.skill_context import SkillContext, serve_skill_planner


def digest(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


class SkillContextTests(unittest.TestCase):
    def setUp(self):
        self.adapter = SkillContext()
        self.view = {"schema": "ahbg.skill-view/1", "source": {"commit": "example"},
                     "roots": ["reader"], "discovery": [], "activated": [
                         {"name": name, "instructions": body, "sha256": hashlib.sha256(body.encode()).hexdigest(),
                          "reasons": [{"kind": "requested", "source": name}]}
                         for name, body in (("reader", "Read exactly this.\n"), ("writer", "Write ë."))]}
        self.reference = {"schema": "ahbg.skill-view-ref/1", "view_sha256": digest(self.view)}
        self.probe = {"session_id": "session1", "turn": 1, "view_sha256": digest(self.view)}
        self.other = {"role": "user", "content": "Keep my message."}
        self.history = self.prepare(self.view, [self.other])

    def prepare(self, view, history, session="session1"):
        return self.adapter.prepare({"session_id": session, "skill_library": view, "turn": 1}, history)

    def test_repeated_model_turn_keeps_actual_instructions_once(self):
        self.assertTrue(self.adapter.ack(self.probe, self.history)["full_view"])
        next_turn = self.prepare(self.reference, self.history)
        self.assertEqual(next_turn[:-1], self.history)
        self.assertEqual(next_turn[0], self.other)
        self.assertEqual(sum(m.get("name") == "ahbg_skill_body" for m in next_turn), 2)
        self.assertEqual(json.loads(next_turn[-1]["content"]), {"session_id": "session1", "turn": 1})

    def test_compaction_requires_partial_delivery_then_reacquires_all(self):
        first = self.view["activated"][0]
        compacted = [m for m in self.history if not m["content"].endswith(first["instructions"])]
        ack = self.adapter.ack(self.probe, compacted)
        self.assertFalse(ack["full_view"])
        self.assertEqual(ack["retained"], [{"name": "writer", "sha256": self.view["activated"][1]["sha256"]}])
        delta = {**deepcopy(self.view), "schema": "ahbg.skill-view-delta/1", "view_sha256": digest(self.view)}
        row = delta["activated"][1]
        del row["instructions"]
        row["instructions_retained"] = True
        with self.assertRaises(ValueError):
            self.prepare(self.reference, compacted)
        with self.assertRaises(ValueError):
            self.prepare(delta, [])
        changed = deepcopy(delta)
        changed["roots"] = ["something else"]
        with self.assertRaises(ValueError):
            self.prepare(changed, compacted)
        restored = self.prepare(delta, compacted)
        self.assertTrue(self.adapter.ack(self.probe, restored)["full_view"])
        self.assertEqual(sum(m["content"].endswith(first["instructions"]) for m in restored), 1)

    def test_wrong_role_stale_or_modified_messages_do_not_attest(self):
        for change in ("wrong-role", "name-only", "modified", "empty", "other-session", "restart"):
            with self.subTest(change=change):
                history = deepcopy(self.history)
                context = self.adapter
                probe = self.probe.copy()
                if change == "other-session":
                    probe["session_id"] = "new-session"
                elif change == "restart":
                    context = SkillContext()
                elif change == "empty":
                    history = []
                else:
                    for message in history:
                        if message.get("name") == "ahbg_skill_body":
                            if change == "wrong-role":
                                message["role"] = "assistant"
                            elif change == "name-only":
                                message.pop("name")
                            else:
                                message["content"] += " "
                ack = context.ack(probe, history)
                self.assertEqual(ack["retained"], [])
                self.assertFalse(ack["full_view"])

    def test_new_scope_removes_obsolete_instruction_messages(self):
        updated = deepcopy(self.view)
        updated["activated"] = updated["activated"][:1]
        first = updated["activated"][0]
        first.update(instructions="Use a new revision.", sha256=hashlib.sha256(b"Use a new revision.").hexdigest())
        self.assertFalse(self.adapter.ack({**self.probe, "view_sha256": digest(updated)}, self.history)["full_view"])
        next_turn = self.prepare(updated, self.history)
        self.assertTrue(any(m is self.other for m in next_turn))
        emitted = [m["content"] for m in next_turn if m.get("name") == "ahbg_skill_body"]
        self.assertEqual(len(emitted), 1)
        self.assertTrue(emitted[0].endswith(first["instructions"]))
        self.assertEqual(self.adapter.ack(self.probe, next_turn)["retained"], [])


    def test_server_compacts_before_probe_and_recovers_before_planning(self):
        requested = []
        compacted = []

        def compact(history, session_id, turn):
            compacted.append((session_id, turn))
            if turn == 2:
                return [m for m in history if "name" not in m]
            return history

        def plan(messages):
            board = json.loads(messages[-1]["content"])
            self.assertNotIn("skill_library", board)
            requested.append(messages)
            return {"session_id": board["session_id"], "turn": board["turn"], "intents": []}

        def observe(turn, view, session="a"):
            return {"type": "observe", "observation": {"session_id": session, "turn": turn,
                                                       "skill_library": view}}

        def probe(turn, session="a"):
            return {"type": "skill_context_probe", "session_id": session, "turn": turn,
                    "view_sha256": digest(self.view)}

        # An obsolete reference after compaction exercises same-turn recovery.
        events = [observe(0, self.view), probe(1), observe(1, self.reference), probe(2),
                  observe(2, self.reference), observe(2, self.view), probe(0, "b"),
                  observe(0, self.view, "b")]
        source = StringIO("".join(json.dumps(e) + "\n" for e in events))
        output = StringIO()
        serve_skill_planner(plan, prepare_history=compact, stdin=source, stdout=output)
        replies = [json.loads(line) for line in output.getvalue().splitlines()]
        self.assertEqual([p["type"] for p in replies],
                         ["plan", "skill_context_state", "plan", "skill_context_state", "skill_context_miss",
                          "plan", "skill_context_state", "plan"])
        self.assertTrue(replies[1]["full_view"])
        self.assertFalse(replies[3]["full_view"])
        self.assertFalse(replies[6]["full_view"])
        self.assertEqual(compacted, [("a", 0), ("a", 1), ("a", 2), ("b", 0)])
        self.assertEqual([sum(m.get("name") == "ahbg_skill_body" for m in batch)
                          for batch in requested], [2, 2, 2, 2])
        self.assertFalse(any(m["role"] == "assistant" for m in requested[-1]))
        self.assertEqual(len([m for m in requested[1] if m["role"] == "assistant"]), 1)

    def test_server_never_plans_on_a_mismatched_refresh(self):
        def reject(_messages):
            self.fail("provider must not run for an unverified skill view")
        base = {"session_id": "first", "turn": 0}
        altered = {**self.view, "roots": ["foreign"]}
        packets = [{"type": "observe", "observation": {**base, "skill_library": view}}
                   for view in (self.reference, altered)]
        output = StringIO()
        with self.assertRaisesRegex(ValueError, "refresh differs"):
            serve_skill_planner(reject, stdin=StringIO("".join(json.dumps(p) + "\n" for p in packets)),
                                stdout=output)
        self.assertEqual(json.loads(output.getvalue())["type"], "skill_context_miss")


if __name__ == "__main__":
    unittest.main()
# ratios: loc_comments=138:2 imports_exports=6:2 calls_definitions=77:10
