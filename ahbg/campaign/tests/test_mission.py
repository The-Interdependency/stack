import json
import unittest
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory

from ahbg.campaign.__main__ import Campaign
from ahbg.campaign.controllers import ORDERS, Scripted
from ahbg.campaign.mission import Case, play, replay
from ahbg.runtime.entitlements import EntitlementError, EntitlementGate


class MissionTests(unittest.TestCase):
    def setUp(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.i = 0

    def run_case(self, case, controller=None):
        self.i += 1
        target = self.root / str(self.i)
        result = play(case, controller or Scripted(), target)
        self.assertEqual(result, replay(target))
        return result

    def test_balanced_and_menu_permutation(self):
        for occupied in (True, False):
            for n, order in enumerate(ORDERS):
                expected = ("AB" if occupied else "BA")[n]
                for reverse in (False, True):
                    result = self.run_case(
                        Case(occupied=occupied, order=order, reverse_menu=reverse)
                    )
                    self.assertEqual(
                        (result["choice"], result["outcome"]), (expected, "arrived")
                    )

    def test_private_view_and_competition(self):
        c = Case()
        baseline = self.run_case(c)
        rival = self.run_case(replace(c, competitor=True))
        self.assertEqual(baseline["builder_view"], rival["builder_view"])
        self.assertEqual((rival["choice"], rival["outcome"]), ("A", "displaced"))
        hidden = self.run_case(replace(c, visibility="withheld"))
        other = self.run_case(replace(c, visibility="withheld", occupied=False))
        self.assertEqual(hidden["builder_view"], other["builder_view"])
        self.assertEqual(hidden["choice"], "HOLD")
        reported = self.run_case(replace(c, visibility="report"))
        self.assertEqual(reported["choice"], "A")
        self.assertEqual(
            self.run_case(replace(c, recipient="explorer"))["choice"], "HOLD"
        )

    def test_orders_history_and_code_points(self):
        self.assertEqual(
            self.run_case(Case(order="", standing_order=ORDERS[1]))["choice"], "B"
        )
        self.assertEqual(
            self.run_case(Case(order=ORDERS[0], standing_order=ORDERS[1]))["choice"],
            "A",
        )
        Case(order="🐦" * 256)
        with self.assertRaises(ValueError):
            Case(order="🐦" * 255 + "e\u0308")

    def test_invalid_separate_from_hold_and_replay_checks_decision(self):
        class Invalid(Scripted):
            def choose(self, view):
                return '"A"'

        self.assertEqual(self.run_case(Case(), Invalid())["outcome"], "invalid")
        self.run_case(Case())
        dest = self.root / "2" / "result.json"
        result = json.loads(dest.read_text())
        result["turn_records"][0]["submitted_plan"]["intents"] = []
        dest.write_text(json.dumps(result))
        with self.assertRaisesRegex(ValueError, "decision"):
            replay(dest.parent)

    def test_reopen_fork_without_changing_parent_and_gate(self):
        free = Campaign(self.root, EntitlementGate())
        parent = free.save(Case())
        with self.assertRaises(EntitlementError):
            free.fork(parent["id"], "order")
        lab = Campaign(self.root, EntitlementGate.from_claims(["benchmark_lab"]))
        changed = lab.fork(parent["id"], "order")
        self.assertEqual(lab.record(parent["id"])["position"], "RING_1")
        self.assertEqual(changed["position"], "RING_5")
        self.assertEqual(
            changed["fork"],
            {
                "parent_id": parent["id"],
                "parent_digest": parent["state_digest"],
                "variable": "order",
            },
        )
        self.assertEqual(
            free.save(Case())["state_digest"], lab.save(Case())["state_digest"]
        )
