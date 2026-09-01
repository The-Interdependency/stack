"""Checks for the asynchronous PCEA gonol key-state research candidate."""

# === CHECKS ===
# id: check_observed_gonol_transition_replays_handoff
#   proves: observed_gonol_transition_replays_handoff
#   call: self::test_observed_gonol_transition_replays_handoff
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#   class: correctness
#   since: 2026-08-31
#
# id: check_interpolation_prediction_is_not_derived_law
#   proves: interpolation_prediction_is_not_derived_law
#   call: self::test_interpolation_prediction_is_not_derived_law
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#   class: doctrine
#   since: 2026-08-31
#
# id: check_lazy_key_derivation_binds_secret_and_address
#   proves: lazy_key_derivation_binds_secret_and_address
#   call: self::test_lazy_key_derivation_binds_secret_and_address
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#   class: construction
#   since: 2026-08-31
#
# id: check_address_replay_cache_rejects_coordinate_reuse
#   proves: address_replay_cache_rejects_coordinate_reuse
#   call: self::test_address_replay_cache_rejects_coordinate_reuse
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#   class: security-control
#   since: 2026-08-31
#
# id: check_key_addressing_comparison_waits_for_actual_ucns_result
#   proves: key_addressing_comparison_waits_for_actual_ucns_result
#   call: self::test_key_addressing_comparison_waits_for_actual_ucns_result
#   requires: python3
#   timeout: 20
#   mutates: none
#   cleanup: none
#   class: doctrine
#   since: 2026-08-31
# === END CHECKS ===

from __future__ import annotations

import copy
from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest


RESEARCH_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RESEARCH_ROOT))

import async_gonol_keys as agk  # noqa: E402


class AsyncGonolKeyStateTests(unittest.TestCase):
    def address(self, **overrides: object) -> agk.GonolAddress:
        payload: dict[str, object] = {
            "epoch": 7,
            "gonol_size": agk.predict_next_gonol(),
            "message_counter": 11,
            "position": 42,
            "recursive_path": agk.OBSERVED_GONOL_SEQUENCE,
            "state_digest": agk.derive_state_digest({"last_state": [1, 2, 3]}),
            "transcript_digest": agk.derive_state_digest({"transcript": ["a", "b"]}),
        }
        payload.update(overrides)
        return agk.GonolAddress(**payload)  # type: ignore[arg-type]

    def test_observed_gonol_transition_replays_handoff(self) -> None:
        operator = agk.interpolation_baseline_operator()

        self.assertEqual(agk.replay_transition(), (157, 2881, 54837698421))
        self.assertEqual(operator["first_difference"], 2724)
        self.assertEqual(operator["second_difference"], 54837692816)
        self.assertEqual(operator["operator_id"], agk.OPERATOR_ID)
        self.assertFalse(hasattr(agk, "recover_transition_operator"))

    def test_interpolation_prediction_is_not_derived_law(self) -> None:
        freeze = agk.freeze_document()

        self.assertEqual(agk.predict_next_gonol(), 164513086777)
        self.assertEqual(agk.predict_next_gonol(), agk.PREDICTED_NEXT_GONOL)
        self.assertEqual(freeze["predicted_next_gonol"]["value"], 164513086777)
        self.assertIn("interpolation baseline", freeze["operator"]["operator_standing"])
        self.assertIn("not derived law", freeze["predicted_next_gonol"]["standing"])
        self.assertIn("not entropy from gonol size, geometry, or address space", freeze["nonclaims"])
        self.assertIn("exact UCNS recursive-scale transition law remains unresolved", freeze["hmmm"])

    def test_actual_ucns_constructor_status_gates_out_of_sample_test(self) -> None:
        status = agk.actual_ucns_constructor_status()
        comparison = agk.compare_prediction_to_actual_ucns(status["actual_next_gonol"])

        self.assertFalse(status["constructor_available"])
        self.assertIsNone(status["actual_next_gonol"])
        self.assertEqual(status["status"], "UNRESOLVED_ACTUAL_CONSTRUCTOR_MISSING")
        self.assertEqual(comparison["baseline_outcome"], "UNRESOLVED")
        self.assertEqual(comparison["prediction"], agk.PREDICTED_NEXT_GONOL)
        self.assertEqual(agk.compare_prediction_to_actual_ucns(1)["baseline_outcome"], "FALSIFIED")
        self.assertEqual(
            agk.compare_prediction_to_actual_ucns(agk.PREDICTED_NEXT_GONOL)["baseline_outcome"],
            "SURVIVED_ONE_OUT_OF_SAMPLE_TEST",
        )

    def test_freeze_json_matches_module_when_present(self) -> None:
        freeze_path = RESEARCH_ROOT / "async_gonol_key_state_freeze.json"
        if not freeze_path.is_file():
            self.fail("async_gonol_key_state_freeze.json is required evidence")

        on_disk = json.loads(freeze_path.read_text(encoding="utf-8"))
        self.assertEqual(on_disk, agk.freeze_document())
        self.assertEqual(on_disk["replay"]["values"], [157, 2881, 54837698421])
        self.assertTrue(on_disk["replay"]["matches_observation"])
        self.assertEqual(on_disk["schema"], "pcea.async-gonol-key-state.freeze.v2")
        self.assertEqual(on_disk["interpolation_prediction_test"]["baseline_outcome"], "UNRESOLVED")

    def test_lazy_key_derivation_binds_secret_and_address(self) -> None:
        secret = b"test root secret with external entropy basis"
        address = self.address()
        baseline = agk.derive_lazy_key(secret, address)

        self.assertEqual(baseline, agk.derive_lazy_key(secret, address))
        self.assertEqual(len(agk.derive_lazy_key(secret, address, length=80)), 80)

        changes = [
            {"position": address.position + 1},
            {"message_counter": address.message_counter + 1},
            {"recursive_path": address.recursive_path + (agk.predict_next_gonol(),)},
            {"state_digest": agk.derive_state_digest({"last_state": [1, 2, 4]})},
            {"transcript_digest": agk.derive_state_digest({"transcript": ["a", "c"]})},
        ]
        for change in changes:
            with self.subTest(change=change):
                self.assertNotEqual(baseline, agk.derive_lazy_key(secret, self.address(**change)))

    def test_address_replay_cache_rejects_coordinate_reuse(self) -> None:
        cache = agk.ReplayCache()
        first = self.address(position=5, message_counter=1)
        second = self.address(position=2, message_counter=0)

        self.assertTrue(cache.accept(first))
        self.assertTrue(cache.accept(second))
        self.assertEqual(cache.seen_count, 2)
        self.assertFalse(cache.accept(first))
        with self.assertRaises(agk.ReplayError):
            cache.require_fresh(second)

    def test_fresh_derivation_accepts_out_of_order_addresses(self) -> None:
        secret = b"test root secret with external entropy basis"
        cache = agk.ReplayCache()
        late = self.address(position=20, message_counter=20)
        early = self.address(position=3, message_counter=3)

        late_key = agk.derive_fresh_lazy_key(secret, late, cache)
        early_key = agk.derive_fresh_lazy_key(secret, early, cache)

        self.assertNotEqual(late_key, early_key)
        with self.assertRaises(agk.ReplayError):
            agk.derive_fresh_lazy_key(secret, late, cache)

    def test_key_addressing_comparison_waits_for_actual_ucns_result(self) -> None:
        matrix = agk.key_addressing_comparison()

        self.assertEqual(matrix["status"], "DEFERRED")
        self.assertEqual(matrix["security_basis"], "external secret entropy plus standard KDF only")
        self.assertEqual(matrix["gate"]["baseline_outcome"], "UNRESOLVED")
        self.assertIn("not entropy from gonol size, geometry, or address space", matrix["nonclaims"])

        available = agk.key_addressing_comparison(agk.PREDICTED_NEXT_GONOL)
        self.assertEqual(available["status"], "AVAILABLE_AFTER_BASELINE_SURVIVAL")
        self.assertEqual(available["standing"]["security_basis"], "external secret entropy plus standard KDF only")
        self.assertIn("standard KDF", available["comparison_scope"])

    def test_invalid_address_and_root_secret_fail_closed(self) -> None:
        with self.assertRaises(agk.AsyncGonolError):
            self.address(position=agk.predict_next_gonol())
        with self.assertRaises(agk.AsyncGonolError):
            self.address(state_digest="not-a-digest")
        with self.assertRaises(agk.AsyncGonolError):
            agk.derive_lazy_key(b"", self.address())
        with self.assertRaises(TypeError):
            agk.derive_lazy_key("not bytes", self.address())  # type: ignore[arg-type]

    def test_canonical_receipt_digest_is_stable(self) -> None:
        document = agk.freeze_document()
        payload = copy.deepcopy(document)
        receipt_digest = payload.pop("receipt_digest")

        self.assertEqual(document, agk.freeze_document())
        self.assertEqual(receipt_digest, sha256(agk.canonical_json_bytes(payload)).hexdigest())
        payload["operator"]["y_0"] = payload["operator"]["y_0"] + 1
        self.assertNotEqual(receipt_digest, sha256(agk.canonical_json_bytes(payload)).hexdigest())


if __name__ == "__main__":
    unittest.main()
