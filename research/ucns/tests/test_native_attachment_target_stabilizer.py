"""Adversarial witnesses for native attachment-target stabilizers."""

# === CHECKS ===
# id: check_attachment_target_uses_exact_complete_state_carrier
#   proves: attachment_target_uses_exact_complete_state_carrier
#   call: self::test_complete_state_has_visible_and_complete_return
#   mutates: none
#   cleanup: none
#
# id: check_attachment_target_compares_full_unoriented_stabilizer
#   proves: attachment_target_compares_full_unoriented_stabilizer
#   call: self::test_exact_target_stabilizers_include_reflections
#   mutates: none
#   cleanup: none
#
# id: check_attachment_target_exposes_visible_fiber_collision
#   proves: attachment_target_exposes_visible_fiber_collision
#   call: self::test_visible_target_and_full_fiber_are_the_same_information
#   mutates: none
#   cleanup: none
#
# id: check_attachment_target_minimal_refinements_are_exact
#   proves: attachment_target_minimal_refinements_are_exact
#   call: self::test_lift_then_germ_remove_stabilizers_one_at_a_time
#   mutates: none
#   cleanup: none
#
# id: check_attachment_target_does_not_confuse_construction_with_selection
#   proves: attachment_target_does_not_confuse_construction_with_selection
#   call: self::test_every_control_is_constructible_but_intrinsic_selection_remains_unresolved
#   mutates: none
#   cleanup: none
#
# id: check_attachment_target_preserves_downstream_stop
#   proves: attachment_target_preserves_downstream_stop
#   call: self::test_no_successor_or_security_promotion_is_emitted
#   mutates: none
#   cleanup: none
#
# id: check_attachment_target_receipt_replays
#   proves: attachment_target_receipt_replays
#   call: self::test_receipts_replay_byte_identically
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
import importlib.util
from pathlib import Path
import sys
import unittest


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
COMMITTED_JSON = RESEARCH_ROOT / "receipts" / "native-attachment-target-stabilizer-v0.json"
COMMITTED_MARKDOWN = RESEARCH_ROOT / "receipts" / "native-attachment-target-stabilizer-v0.md"
sys.path.insert(0, str(RESEARCH_ROOT))

import native_attachment_target_stabilizer as m


class NativeAttachmentTargetStabilizerTest(unittest.TestCase):
    def _by_kind(self) -> dict[str, m.AttachmentTarget]:
        return {target.kind: target for target in m.candidate_targets()}

    def test_complete_state_has_visible_and_complete_return(self) -> None:
        start = m.CompleteCarrierState.from_coordinate(Fraction(1, 3))
        one = start.advance(1)
        two = start.advance(2)
        self.assertEqual(start.visible_phase, one.visible_phase)
        self.assertNotEqual(start.frame, one.frame)
        self.assertEqual(two, start)
        self.assertEqual(start.advance(Fraction(7, 5)).advance(Fraction(-7, 5)), start)

    def test_q_mod_two_model_matches_pinned_native_mobius_runtime(self) -> None:
        source = RESEARCH_ROOT.parents[1] / "libs" / "ucns" / "src" / "ucns" / "direct_mobius.py"
        spec = importlib.util.spec_from_file_location("pinned_direct_mobius_for_target_test", source)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        for coordinate in (Fraction(0), Fraction(1, 3), Fraction(1), Fraction(5, 3)):
            model = m.CompleteCarrierState.from_coordinate(coordinate)
            frame = (
                module.NativeMobiusFrame.POSITIVE
                if model.frame == "positive-local-frame"
                else module.NativeMobiusFrame.REVERSED
            )
            runtime = module.NativeMobiusState(model.visible_phase, frame)
            for displacement in (Fraction(-7, 5), Fraction(-1), Fraction(0), Fraction(2, 3), Fraction(1), Fraction(2)):
                model_after = model.advance(displacement)
                runtime_after = runtime.advance(displacement)
                self.assertEqual(model_after.visible_phase, runtime_after.phase_turns)
                self.assertEqual(model_after.frame, runtime_after.frame.value)

    def test_exact_target_stabilizers_include_reflections(self) -> None:
        targets = self._by_kind()
        expected = {
            m.VISIBLE_PHASE: ("rho_0", "rho_1", "tau_0", "tau_1"),
            m.TWO_LIFT_FIBER: ("rho_0", "rho_1", "tau_0", "tau_1"),
            m.SINGLE_LIFT: ("rho_0", "tau_0"),
            m.DIRECTED_GERM: ("tau_0",),
        }
        for kind, ids in expected.items():
            observed = tuple(item.symmetry_id for item in m.target_stabilizer(targets[kind]))
            self.assertEqual(observed, ids)

        nonzero = m.AttachmentTarget(
            "nonzero-single-control",
            m.SINGLE_LIFT,
            state=m.CompleteCarrierState.from_coordinate(Fraction(2, 3)),
        )
        self.assertEqual(
            tuple(item.symmetry_id for item in m.target_stabilizer(nonzero)),
            ("rho_4/3", "tau_0"),
        )

        for phase in (Fraction(1, 3), Fraction(2, 5), Fraction(7, 11)):
            visible = m.AttachmentTarget(
                f"visible-{phase}", m.VISIBLE_PHASE, visible_phase=phase
            )
            fiber = m.AttachmentTarget(
                f"fiber-{phase}", m.TWO_LIFT_FIBER, visible_phase=phase
            )
            self.assertEqual(visible.complete_state_subset, fiber.complete_state_subset)
            self.assertEqual(m.target_stabilizer(visible), m.target_stabilizer(fiber))
            self.assertEqual(len(m.target_stabilizer(visible)), 4)
            self.assertEqual(sum(item.sign == -1 for item in m.target_stabilizer(visible)), 2)

    def test_visible_target_and_full_fiber_are_the_same_information(self) -> None:
        targets = self._by_kind()
        visible = targets[m.VISIBLE_PHASE]
        fiber = targets[m.TWO_LIFT_FIBER]
        self.assertEqual(visible.complete_state_subset, fiber.complete_state_subset)
        self.assertEqual(m.target_stabilizer(visible), m.target_stabilizer(fiber))
        collision = m.audit_payload()["exact_collision"]
        self.assertTrue(collision["same_complete_state_subset"])
        self.assertTrue(collision["same_stabilizer"])
        self.assertEqual(collision["verdict"], "FALSIFIED")
        self.assertEqual(collision["deprecated_status"], "DEPRECATED")

    def test_lift_then_germ_remove_stabilizers_one_at_a_time(self) -> None:
        targets = self._by_kind()
        visible = m.target_stabilizer(targets[m.VISIBLE_PHASE])
        single = m.target_stabilizer(targets[m.SINGLE_LIFT])
        germ = m.target_stabilizer(targets[m.DIRECTED_GERM])
        self.assertEqual((len(visible), len(single), len(germ)), (4, 2, 1))
        self.assertTrue(any(item.sign == 1 and item.offset == 1 for item in visible))
        self.assertFalse(any(item.sign == 1 and item.offset == 1 for item in single))
        self.assertTrue(any(item.sign == -1 for item in single))
        self.assertFalse(any(item.sign == -1 for item in germ))

    def test_every_control_is_constructible_but_intrinsic_selection_remains_unresolved(self) -> None:
        payload = m.audit_payload()
        self.assertEqual(len(payload["candidate_evaluations"]), 4)
        for result in payload["candidate_evaluations"]:
            self.assertEqual(result["intrinsic_selection"], "UNRESOLVED")
            self.assertIn("explicit coordinate-zero control", result["target"]["selection_basis"])
        verdicts = payload["result_classifications"]
        self.assertEqual(verdicts["directed_germ_explicit_constructor"], "SURVIVED_LOCALLY")
        self.assertEqual(verdicts["intrinsic_directed_germ_selection"], "UNRESOLVED")

    def test_no_successor_or_security_promotion_is_emitted(self) -> None:
        payload = m.audit_payload()
        gate = payload["observed_successor_gate"]
        self.assertFalse(gate["observed_values_present_in_constructor"])
        self.assertFalse(gate["successor_selector_derived"])
        self.assertFalse(gate["observed_successor_values_evaluated"])
        self.assertIsNone(payload["security_separation"]["security_promotion"])
        source = Path(m.__file__).read_text(encoding="utf-8")
        for forbidden in ("2881", "54837698421", "164513086777"):
            self.assertNotIn(forbidden, source)

    def test_malformed_states_symmetries_and_targets_fail_closed(self) -> None:
        with self.assertRaises(m.AttachmentTargetError):
            m.CompleteCarrierState(Fraction(2))
        with self.assertRaises(m.AttachmentTargetError):
            m.CompleteCarrierState.from_coordinate(True)
        with self.assertRaises(m.AttachmentTargetError):
            m.AffineCarrierSymmetry.create(0, 0)
        with self.assertRaises(m.AttachmentTargetError):
            replace(m.candidate_targets()[0], state=m.CompleteCarrierState.from_coordinate(0))
        with self.assertRaises(m.AttachmentTargetError):
            replace(m.candidate_targets()[-1], direction=0)

    def test_receipts_replay_byte_identically(self) -> None:
        first = m.audit_payload()
        second = m.audit_payload()
        self.assertEqual(first, second)
        self.assertEqual(m.receipt_bytes(first), m.receipt_bytes(second))
        self.assertEqual(m.receipt_digest(first), m.receipt_digest(second))
        self.assertEqual(m.render_markdown(first), m.render_markdown(second))
        self.assertEqual(COMMITTED_JSON.read_bytes(), m.formatted_receipt_bytes(first))
        self.assertEqual(COMMITTED_MARKDOWN.read_bytes(), m.markdown_receipt_bytes(first))


if __name__ == "__main__":
    unittest.main()
