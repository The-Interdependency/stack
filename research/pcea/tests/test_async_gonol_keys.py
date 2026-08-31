"""Checks for the asynchronous PCEA gonol key-state research candidate."""

# === CHECKS ===
# id: check_observed_gonol_transition_replays_handoff
#   contract: observed_gonol_transition_replays_handoff
#   module: async_gonol_keys
#   then: observed replay returns exactly 157, 2881, 54837698421
#   class: correctness
#   since: 2026-08-31
#
# id: check_candidate_next_gonol_is_derived_not_canon
#   contract: candidate_next_gonol_is_derived_not_canon
#   module: async_gonol_keys
#   then: the next gonol is frozen under OPERATOR_ID and nonclaims reject UCNS canon/security promotion
#   class: doctrine
#   since: 2026-08-31
#
# id: check_lazy_key_derivation_binds_secret_and_address
#   contract: lazy_key_derivation_binds_secret_and_address
#   module: async_gonol_keys
#   then: equal inputs reproduce and path, state, transcript, position, and message changes alter the key
#   class: construction
#   since: 2026-08-31
#
# id: check_address_replay_cache_rejects_coordinate_reuse
#   contract: address_replay_cache_rejects_coordinate_reuse
#   module: async_gonol_keys
#   then: out-of-order fresh coordinates are accepted and repeated coordinates are rejected
#   class: security-control
#   since: 2026-08-31
#
# id: check_comparison_keeps_security_basis_external
#   contract: comparison_keeps_security_basis_external
#   module: async_gonol_keys
#   then: the comparison matrix credits only external secret entropy and explicit receiver controls
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
            "gonol_size": agk.derive_next_gonol(),
            "message_counter": 11,
            "position": 42,
            "recursive_path": agk.OBSERVED_GONOL_SEQUENCE,
            "state_digest": agk.derive_state_digest({"last_state": [1, 2, 3]}),
            "transcript_digest": agk.derive_state_digest({"transcript": ["a", "b"]}),
        }
        payload.update(overrides)
        return agk.GonolAddress(**payload)  # type: ignore[arg-type]

    def test_observed_gonol_transition_replays_handoff(self) -> None:
        operator = agk.recover_transition_operator()

        self.assertEqual(agk.replay_transition(), (157, 2881, 54837698421))
        self.assertEqual(operator["first_difference"], 2724)
        self.assertEqual(operator["second_difference"], 54837692816)
        self.assertEqual(operator["operator_id"], agk.OPERATOR_ID)

    def test_candidate_next_gonol_is_derived_not_canon(self) -> None:
        freeze = agk.freeze_document()

        self.assertEqual(agk.derive_next_gonol(), 164513086777)
        self.assertEqual(agk.derive_next_gonol(), agk.DERIVED_NEXT_GONOL)
        self.assertEqual(freeze["derived_next_gonol"]["value"], 164513086777)
        self.assertIn("not UCNS recursive-scale canon", freeze["operator"]["operator_standing"])
        self.assertIn("not entropy from gonol size, geometry, or address space", freeze["nonclaims"])
        self.assertIn("exact UCNS recursive-scale transition law remains unresolved", freeze["hmmm"])

    def test_freeze_json_matches_module_when_present(self) -> None:
        freeze_path = RESEARCH_ROOT / "async_gonol_key_state_freeze.json"
        if not freeze_path.is_file():
            self.fail("async_gonol_key_state_freeze.json is required evidence")

        on_disk = json.loads(freeze_path.read_text(encoding="utf-8"))
        self.assertEqual(on_disk, agk.freeze_document())
        self.assertEqual(on_disk["replay"]["values"], [157, 2881, 54837698421])
        self.assertTrue(on_disk["replay"]["matches_observation"])

    def test_lazy_key_derivation_binds_secret_and_address(self) -> None:
        secret = b"test root secret with external entropy basis"
        address = self.address()
        baseline = agk.derive_lazy_key(secret, address)

        self.assertEqual(baseline, agk.derive_lazy_key(secret, address))
        self.assertEqual(len(agk.derive_lazy_key(secret, address, length=80)), 80)

        changes = [
            {"position": address.position + 1},
            {"message_counter": address.message_counter + 1},
            {"recursive_path": address.recursive_path + (agk.derive_next_gonol(),)},
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

    def test_comparison_keeps_security_basis_external(self) -> None:
        matrix = agk.comparison_matrix()
        standing = matrix["standing"]

        self.assertEqual(standing["security_basis"], "external secret entropy plus approved KDF only")
        self.assertIn("explicit replay cache", standing["replay_resistance"])
        self.assertIn("not entropy from gonol size, geometry, or address space", matrix["nonclaims"])
        self.assertIn("tree KDF", standing["compromise_containment"])

    def test_invalid_address_and_root_secret_fail_closed(self) -> None:
        with self.assertRaises(agk.AsyncGonolError):
            self.address(position=agk.derive_next_gonol())
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
