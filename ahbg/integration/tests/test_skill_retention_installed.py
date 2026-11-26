# ratios: loc_comments=129:3 imports_exports=10:2 calls_definitions=53:5
"""Exercise skill retention on the installed JSON-lines planner across six turns."""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from ahbg.integration.tests.test_skill_harness_installed import PERMITTED, ROOTS, STACK


def _bytes(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def _prompt_bodies(messages):
    bodies = {}
    for message in messages:
        if message.get("name") == "ahbg_skill_body":
            header, content = message["content"].split("\n", 1)
            name = json.loads(header)["name"]
            if name in bodies:
                raise ValueError(f"duplicate instruction body for {name} in the model prompt")
            bodies[name] = content
    return bodies


def observe(retention):
    from ahbg.integration.skill_context import SkillContext

    ctx = SkillContext()
    messages = []
    turns = 0
    missed = False
    for line in sys.stdin:
        wire = json.loads(line)
        if wire["type"] == "skill_context_probe":
            if not retention:
                raise ValueError("legacy planner received an unsolicited context probe")
            if turns == 3:
                messages = [m for m in messages if m.get("name") != "ahbg_skill_body" or
                            json.loads(m["content"].split("\n", 1)[0])["name"] != "doc-build"]
            elif turns == 4:
                messages = []
                ctx = SkillContext()
            print(json.dumps(ctx.ack(wire, messages)), flush=True)
            continue

        observation = wire["observation"]
        view = observation["skill_library"]
        if retention and turns == 5 and not missed:
            # Model context is compacted after the positive probe, before inference.
            messages = []
            if view["schema"] != "ahbg.skill-view-ref/1":
                raise ValueError("expected to exercise the in-flight reference")
            try:
                ctx.prepare(observation, messages)
            except ValueError:
                missed = True
                print(json.dumps({"type": "skill_context_miss", "session_id": observation["session_id"],
                                  "turn": observation["turn"], "view_sha256": view["view_sha256"]}), flush=True)
                continue
            raise ValueError("accepted a stale reference after in-flight context loss")
        previous = {m["content"] for m in messages if m.get("name") in ("ahbg_skill_body", "ahbg_skill_index")}
        messages = ctx.prepare(observation, messages)
        new_skill_messages = [m for m in messages if m.get("name") in ("ahbg_skill_body", "ahbg_skill_index")
                              and m["content"] not in previous]
        bodies = _prompt_bodies(messages)
        # Derive this answer from the prompt actually assembled for the model.
        first_read = next(s for s in bodies["doc-build"].splitlines() if s.startswith("Read `"))
        note = {
            "schema": view["schema"],
            "wire_sha256": sha256(_bytes(view)).hexdigest(),
            "wire_bytes": len(_bytes(view)),
            "new_skill_messages": len(new_skill_messages),
            "received": [s["name"] for s in view.get("activated", []) if "instructions" in s],
            "body_digests": {n: sha256(s.encode()).hexdigest() for n, s in bodies.items()},
            "first_read": first_read.split("`")[1],
            "same_turn_repair": missed,
        }
        plan = {"session_id": observation["session_id"], "turn": observation["turn"],
                "intents": [], "note": json.dumps(note)}
        reply = {"type": "plan", "plan": plan}
        if retention:
            reply["skill_context_protocol"] = 1
        print(json.dumps(reply), flush=True)
        turns += 1


@unittest.skipUnless(os.environ.get("AHBG_SKILL_CATALOG"), "set AHBG_SKILL_CATALOG to the pinned checkout")
class InstalledRetentionTests(unittest.TestCase):
    def test_full_reference_eviction_and_reset(self):
        catalog = Path(os.environ["AHBG_SKILL_CATALOG"]).resolve()
        expected = {name: sha256((catalog / name / "SKILL.md").read_bytes()).hexdigest()
                    for name in PERMITTED}
        with tempfile.TemporaryDirectory() as work:
            for mode, count in (("retaining", 6), ("legacy", 2)):
                out = Path(work, mode)
                command = [sys.executable, "-m", "ahbg.runtime", "play", "--turns", str(count),
                           "--out", str(out), "--agent-subprocess",
                           ",".join((sys.executable, str(Path(__file__).resolve()), mode)),
                           "--skill-catalog", str(catalog), "--visible-skills", *PERMITTED,
                           "--activate-skills", *ROOTS, "--disclose-runner", "msdmd=msdmd/collect.py"]
                source = os.environ.get("AHBG_SKILL_UCNS_SOURCE")
                if source:
                    command.extend(("--skill-ucns-source", str(Path(source).resolve())))
                environment = {**os.environ, "PYTHONPATH": os.pathsep.join(
                    (str(STACK), str(STACK / "libs/ucns/src"), os.environ.get("PYTHONPATH", "")))}
                result = subprocess.run(command, cwd=STACK, env=environment, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                turns = json.loads((out / "result.json").read_bytes())["turn_records"]
                self.assertEqual(len(turns), count)
                expected_forms = ["ahbg.skill-view/1"] * count
                if mode == "retaining":
                    expected_forms[1:4] = ["ahbg.skill-view-ref/1"] * 2 + ["ahbg.skill-view-delta/1"]
                for i, turn in enumerate(turns):
                    note = json.loads(turn["submitted_plan"]["note"])
                    receipt = turn["agent_provenance"]["skill_library"]
                    self.assertEqual(note["schema"], expected_forms[i])
                    self.assertEqual(note["first_read"], "msdmd/SKILL.md")
                    self.assertEqual(note["body_digests"], expected)
                    self.assertEqual(note["same_turn_repair"], mode == "retaining" and i == 5)
                    self.assertEqual(note["wire_sha256"], receipt["delivery_sha256"])
                    self.assertEqual(note["wire_bytes"], receipt["delivery_bytes"])
                    self.assertEqual(note["received"], receipt["sent_bodies"])
                    if mode == "retaining":
                        self.assertEqual(note["new_skill_messages"], (7, 0, 0, 1, 7, 7)[i])
                        if i == 5:
                            self.assertGreater(receipt["retry_bytes"], 0)
                    if note["schema"] == "ahbg.skill-view/1":
                        self.assertEqual(set(note["received"]), set(PERMITTED))
                    elif note["schema"] == "ahbg.skill-view-delta/1":
                        self.assertEqual(note["received"], ["doc-build"])
                    else:
                        self.assertEqual(note["received"], [])
                        self.assertLess(note["wire_bytes"], receipt["view_bytes"])


if __name__ == "__main__":
    if sys.argv[1:] in (["retaining"], ["legacy"]):
        observe(sys.argv[1] == "retaining")
    else:
        unittest.main()
# ratios: loc_comments=129:3 imports_exports=10:2 calls_definitions=53:5
