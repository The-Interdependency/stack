import json
import tempfile
import unittest
from pathlib import Path
from ahbg.play.game import Plane, canonical
from ahbg.play.store import Rejected, Store
from ahbg.runtime.protocol import ProtocolError


class PlayTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.path = Path(temp.name) / "rooms.db"
        self.store = Store(self.path)

    def start(self, mode):
        return self.store.create("first", "local", mode, "a-unique-request")

    def test_live_geometry_identifies_stack_pin(self):
        root = Path(__file__).resolve().parents[3]
        manifest = json.loads((root / "stack-manifest.json").read_text())
        geometry = Plane("test", 1).observe("amber")["presentation"]["geometry_source"]
        pin = next(r["commit"] for r in manifest["repositories"] if r["repository"] == geometry["repository"])
        self.assertEqual(geometry["commit"], pin)

    def test_seats_contention_replay_and_private_commit(self):
        created = self.start("duel")
        room = created["room"]
        self.store.join("second", created["invite"])
        with self.assertRaises(Rejected):
            self.store.join("third", created["invite"])
        with self.assertRaises(Rejected):
            self.store.state("third", room)
        a = self.store.state("first", room)["observation"]
        b = self.store.state("second", room)["observation"]
        self.assertNotIn("rival", [u["unit_id"] for u in a["field"]["units"]])
        self.assertNotIn("builder", [u["id"] for u in b["presentation"]["units"]])
        move = lambda view, unit: next(i for i in view["legal"] if i["unit_id"] == unit and i["action"] == "relocate" and i["to_tile_id"] == "CENTER")
        plan = {"session_id": room, "turn": 0, "intents": [move(a, "builder"),
                next(i for i in a["legal"] if i["unit_id"] == "explorer" and i["to_tile_id"] != "CENTER")],
                "messages": {"builder": "ë"*256}}
        self.store.commit("first", room, plan)
        self.assertTrue(self.store.state("first", room)["committed"])
        self.assertEqual(self.store.state("first", room)["own_commit"], plan)
        self.assertIsNone(self.store.state("second", room)["own_commit"])
        self.assertNotIn("ë", canonical(self.store.state("second", room)))
        self.store.commit("second", room, {"session_id":room, "turn":0, "intents":[move(b,"rival")]})
        self.store.commit("first", room, plan)
        state = self.store.state("first", room)
        self.assertEqual(state["observation"]["turn"], 1)
        with self.store.connection() as db:
            receipt = json.loads(db.execute("SELECT result FROM turns").fetchone()[0])
        self.assertIn("war", [e["kind"] for e in receipt["events"]])
        self.assertEqual(Store(self.path).state("first", room), state)
        self.assertNotIn("ë", canonical(self.store.state("second", room)))

    def test_invalid_plan_rollback_construction_and_fork(self):
        room = self.start("environment")["room"]
        a = self.store.state("first", room)["observation"]
        build = next(i for i in a["legal"] if i["action"] == "construct")
        plan = {"session_id": room, "turn": 0, "intents":[build]}
        for invalid in (dict(plan, intents=[dict(build,unit_id="rival")]),
                        dict(plan,intents=[build,build]),dict(plan,messages={"builder":"🌿"*257})):
            with self.assertRaises(ProtocolError):
                self.store.commit("first", room, invalid)
        self.assertFalse(self.store.state("first",room)["committed"])
        self.store.commit("first",room,plan)
        self.store.commit("first",room,{"session_id":room,"turn":1,"intents":[]})
        fork = self.store.create("first","local","environment","new-fork-request",room,1)["room"]
        forked = self.store.state("first",fork)
        self.assertEqual(forked["observation"]["turn"],1)
        self.assertIn(build["to_tile_id"],forked["observation"]["built"])
        self.assertEqual(forked["history"],self.store.state("first",room)["history"][:1])
        with self.store.connection(True) as db:
            db.execute("UPDATE turns SET result='{}' WHERE room=? AND turn=0",(room,))
        with self.assertRaisesRegex(RuntimeError,"deterministic replay"):
            self.store.state("first",room)
