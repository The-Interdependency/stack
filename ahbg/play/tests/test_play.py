import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from ahbg.play.game import Plane, canonical
from ahbg.play.store import Rejected, Store
from ahbg.runtime.protocol import ProtocolError
from ahbg.runtime.server import field_to_presentation


class PlayTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.path = Path(temp.name) / "rooms.db"
        self.store = Store(self.path)

    def start(self, mode):
        return self.store.create("first", "local", mode, "a-unique-request")

    def test_existing_planes_retain_their_original_fauna_controller(self):
        rooms = {mode: self.store.create("first", "local", mode, "existing-room-" + mode)["room"]
                 for mode in ("environment", "duel", "smol", "granite")}
        # Reopen the prior release's schema, with one completed turn to replay.
        room = rooms["environment"]
        self.store.commit("first", room, {"session_id": room, "turn": 0, "intents": []})
        before = self.store.state("first", room)
        with self.store.connection(True) as db:
            db.execute("DROP TABLE fauna_controllers")
        restored = Store(self.path)
        self.assertEqual(restored.state("first", room), before)
        for mode, key in rooms.items():
            expected = "environment" if mode == "duel" else mode
            self.assertEqual(restored.state("first", key)["fauna_mode"], expected)

    def test_live_geometry_identifies_stack_pin(self):
        root = Path(__file__).resolve().parents[3]
        manifest = json.loads((root / "stack-manifest.json").read_text())
        geometry = Plane("test", 1).observe("amber")["presentation"]["geometry_source"]
        pin = next(r["commit"] for r in manifest["repositories"] if r["repository"] == geometry["repository"])
        self.assertEqual(geometry["commit"], pin)

    def test_scout_returns_and_only_the_builder_receives_the_sighting(self):
        plane = Plane("scout", 126)
        def resolve(*, move=None, report=None):
            plans = {seat: {"session_id": "scout", "turn": plane.field.turn, "intents": []}
                     for seat in ("amber", "indigo", "wild")}
            if move:
                plans["amber"]["intents"] = [next(i for i in plane.observe("amber", "explorer")["legal"]
                                                   if i["to_tile_id"] == move)]
            if report:
                plans["amber"]["report_tile"] = report
            plane.resolve(plans)

        initial = plane.observe("amber", "explorer")
        self.assertIn("RING_3", [t["tile_id"] for t in initial["field"]["tiles"]])
        self.assertNotIn("RING_3", initial["scouting"]["explorer"]["discovered"])
        self.assertNotIn("rival", [u["unit_id"] for u in initial["field"]["units"]])
        self.assertNotIn("PETAL_0", [t["tile_id"] for t in initial["field"]["tiles"]])
        for target in ("RING_3", "PETAL_0"):
            with self.assertRaises(ProtocolError):
                resolve(report=target)
            plan = {"session_id": "scout", "turn": 0, "intents": [
                dict(initial["legal"][0], to_tile_id=target)]}
            with self.assertRaises(ProtocolError):
                plane.validate("amber", plan)
        with self.assertRaises(ProtocolError):
            plane.validate("indigo", {"session_id": "scout", "turn": 0, "intents": [],
                                       "report_tile": "CENTER"})
        ledger = plane.ledger.as_dict()
        resolve(move="RING_2")
        self.assertFalse(plane.observe("amber", "builder")["inbox"])
        resolve(move="RING_1", report="RING_3")
        scout = plane.observe("amber", "explorer")["scouting"]["explorer"]
        self.assertIn("RING_3", scout["discovered"])
        self.assertNotIn("RING_3", scout["visible"])
        builder = plane.observe("amber", "builder")
        self.assertNotIn("RING_3", builder["scouting"]["builder"]["discovered"])
        report, = builder["inbox"]
        self.assertEqual((report["from"], report["turn"], report["tile"], report["occupant"], report["built"]),
                         ("explorer", 1, "RING_3", "rival", False))
        self.assertFalse(plane.observe("indigo")["inbox"])
        self.assertEqual(plane.ledger.as_dict(), ledger)
        self.assertEqual(plane.field.occupants["builder"].tile_id, "RING_0")

    def test_unknown_position_cannot_render_on_top_of_center(self):
        plane = Plane("scout", 126)
        cell = plane.field.cells["RING_1"]
        plane.field.cells["RING_1"] = replace(cell, ucns_slot="no-source-position")
        with self.assertRaisesRegex(ValueError, "no UCNS display position"):
            field_to_presentation(plane.field)

    def test_turn_receipt_detects_changed_discovery_without_a_board_change(self):
        plane, changed = Plane("memory", 126), Plane("memory", 126)
        changed.discovered["builder"].add("RING_3")
        hold = {seat: {"session_id": "memory", "turn": 0, "intents": []}
                for seat in ("amber", "indigo", "wild")}
        original, different = plane.resolve(hold), changed.resolve(hold)
        self.assertEqual(original["events"], different["events"])
        self.assertEqual(plane.field.snapshot(), changed.field.snapshot())
        self.assertNotEqual(original["digest"], different["digest"])

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
