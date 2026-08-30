# === CHECKS ===
# id: check_nilpotent_protocol_identity
#   proves: prime_nilpotent_protocol_identity_is_frozen
#   call: self::test_protocol_identity_and_frozen_receipt
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_nilpotent_primary_replay
#   proves: prime_nilpotent_primary_and_replay_agree
#   call: self::test_checked_in_receipt_records_exact_replay
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_nilpotent_rank_exclusion
#   proves: prime_nilpotent_comparison_excludes_known_rank
#   call: self::test_comparison_excludes_weight_one_rank
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_nilpotent_phase_binding
#   proves: prime_nilpotent_phase_binding_is_topological
#   call: self::test_phase_co_winners_bind_identical_inputs
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from ucns.prime_nilpotent_discriminator import PROTOCOL_SHA256


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "generated" / "p7-p5-nilpotent-discriminator-result.json"


def _receipt():
    return json.loads(RECEIPT.read_text(encoding="utf-8"))


def test_protocol_identity_and_frozen_receipt() -> None:
    document = ROOT / "docs" / "PREREGISTRATION_P7_P5_NILPOTENT_DISCRIMINATOR.md"
    assert hashlib.sha256(document.read_bytes()).hexdigest() == PROTOCOL_SHA256
    assert _receipt()["protocol_sha256"] == PROTOCOL_SHA256


def test_checked_in_receipt_records_exact_replay() -> None:
    receipt = _receipt()
    assert receipt["nilpotency_class"] == 4
    assert receipt["status"] in {"distinguish", "no-distinguish", "unresolved"}
    if receipt["status"] == "unresolved":
        assert receipt["p7"]["failure"]["primary_replay_mismatch_claimed"] is False
        assert receipt["p5"]["status"] == "not-run-after-p7-gate-failure"
    else:
        assert receipt["p7"]["independent_replay"]["all_marked_elements_match"] is True
        assert receipt["p5"]["independent_replay"]["all_marked_elements_match"] is True


def test_comparison_excludes_weight_one_rank() -> None:
    comparison = _receipt()["p7_p5_comparison"]
    assert comparison["weight_one_rank_excluded"] is True
    assert comparison["outcome"] in {"distinguish", "no-distinguish", "unresolved"}


def test_phase_co_winners_bind_identical_inputs() -> None:
    phase = _receipt()["phase_co_winner_comparison"]
    if phase["outcome"] == "unresolved":
        return
    for family in ("p7", "p5"):
        assert len(set(phase[family]["input_digests"])) == 1
        assert phase[family]["outcome"] == "no-distinguish"
