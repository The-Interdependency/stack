# ratios: loc_comments=90:2 imports_exports=9:2 calls_definitions=45:3
"""Exercise the installed UCHC and graph arms through AHBG's JSON-lines planner."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

STACK = Path(__file__).resolve().parents[3]
ROOTS = ("distributed-publication", "typed-meta-frontend")
PERMITTED = (*ROOTS, "interdependent-work-graph", "msdmd", "meta-module-build", "doc-build")


def observe():
    """This child sees only AHBG's ordinary wire observation."""
    for line in sys.stdin:
        message = json.loads(line)
        observation = message["observation"]
        view = observation["skill_library"]
        active = {item["name"]: item for item in view["activated"]}
        if set(active) != set(PERMITTED) or len(view["activated"]) != len(PERMITTED):
            raise ValueError("expected the complete six-skill pilot")
        if active["msdmd"].get("runner") != "msdmd/collect.py":
            raise ValueError("allowlisted MSDMD runner is missing")
        if any("runner" in item for name, item in active.items() if name != "msdmd"):
            raise ValueError("undeclared runner disclosed")
        for item in active.values():
            if hashlib.sha256(item["instructions"].encode()).hexdigest() != item["sha256"]:
                raise ValueError("planner received modified instructions")
        if {r["source"] for r in active["msdmd"]["reasons"]} != {
            "typed-meta-frontend", "meta-module-build", "doc-build"
        }:
            raise ValueError("shared prerequisite lost a reason")
        if active["interdependent-work-graph"]["reasons"] != [
            {"source": "distributed-publication", "kind": "load_with"}
        ]:
            raise ValueError("missing publication co-load")
        raw = json.dumps(view, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
        plan = {"session_id": observation["session_id"], "turn": observation["turn"],
                "intents": [], "note": hashlib.sha256(raw).hexdigest()}
        print(json.dumps({"type": "plan", "plan": plan}), flush=True)


@unittest.skipUnless(os.environ.get("AHBG_SKILL_CATALOG"), "set AHBG_SKILL_CATALOG to the pinned checkout")
class InstalledSkillHarnessTests(unittest.TestCase):
    def test_both_experiments_and_denied_runner(self):
        catalog = Path(os.environ["AHBG_SKILL_CATALOG"]).resolve()
        command = [sys.executable, "-m", "ahbg.runtime", "play", "--turns", "1",
                   "--agent-subprocess", ",".join((sys.executable, str(Path(__file__).resolve()), "observe")),
                   "--skill-catalog", str(catalog), "--visible-skills", *PERMITTED,
                   "--activate-skills", *ROOTS]
        source = os.environ.get("AHBG_SKILL_UCNS_SOURCE")
        if source:
            command.extend(("--skill-ucns-source", str(Path(source).resolve())))
        environment = os.environ.copy()
        environment["PYTHONPATH"] = os.pathsep.join((str(STACK), str(STACK / "libs/ucns/src"),
                                                     environment.get("PYTHONPATH", "")))
        with tempfile.TemporaryDirectory() as work:
            receipts = {}
            for arm in ("control", "uchc"):
                out = Path(work, arm)
                result = subprocess.run([*command, "--out", str(out), "--skill-experiment", arm,
                                         "--disclose-runner", "msdmd=msdmd/collect.py"],
                                        env=environment, cwd=STACK, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                turn, = json.loads((out / "result.json").read_bytes())["turn_records"]
                receipt = turn["agent_provenance"]["skill_library"]
                self.assertEqual(turn["submitted_plan"]["note"], receipt["view_sha256"])
                self.assertEqual(receipt["experiment"], arm)
                if arm == "uchc":
                    from integration.uchc.skill_resolver.runtime import SkillResolver
                    artifact = out / "skill-activations" / (receipt["activation_root"] + ".json")
                    encoded = json.loads(artifact.read_bytes())
                    self.assertEqual(encoded["graph"]["root"], receipt["activation_root"])
                    verifier = SkillResolver(catalog, ucns_source_root=source)
                    replayed = verifier.replay_activation(encoded, expected_roots=ROOTS)
                    self.assertEqual(replayed["order"], receipt["activation_order"])
                else:
                    self.assertFalse((out / "skill-activations").exists())
                receipts[arm] = receipt

            for key in ("source", "activation_order", "view_sha256", "view_bytes"):
                self.assertEqual(receipts["uchc"][key], receipts["control"][key], key)
            self.assertNotIn("activation_root", receipts["control"])
            self.assertRegex(receipts["uchc"]["activation_root"], r"^[0-9a-f]{64}$")

            denied = Path(work, "denied")
            result = subprocess.run([*command, "--out", str(denied), "--skill-experiment", "uchc"],
                                    env=environment, cwd=STACK, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("outside the session disclosure policy", result.stderr)
            self.assertFalse(denied.exists())


if __name__ == "__main__":
    if sys.argv[1:] == ["observe"]:
        observe()
    else:
        unittest.main()
# ratios: loc_comments=90:2 imports_exports=9:2 calls_definitions=45:3
