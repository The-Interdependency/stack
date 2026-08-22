# === CHECKS ===
# id: check_prime_replay_receipt_interval
#   proves: prime_replay_receipt_preserves_independent_interval_result
#   call: self::test_independent_decimal_replay_is_pinned
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_prime_replay_receipt_phase
#   proves: prime_replay_receipt_exposes_phase_imposition
#   call: self::test_phase_winding_is_shared_not_prime_specific
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_prime_replay_receipt_milnor
#   proves: prime_replay_receipt_freezes_p7_milnor_values
#   call: self::test_all_five_length_three_values_are_zero
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_prime_replay_receipt_nonselecting
#   proves: prime_replay_receipt_is_nonselecting
#   call: self::test_receipt_is_deterministic_and_nonselecting
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
# id: check_prime_replay_data_receipt
#   proves: prime_replay_data_is_receipt_witnessed
#   call: self::test_receipt_is_deterministic_and_nonselecting
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# === END CHECKS ===

from ucns.prime_replay_phase_milnor_receipt import SPLIT_TRIPLES, boundary_knot, build_receipt, validate_receipt


def test_independent_decimal_replay_is_pinned() -> None:
    replay = build_receipt()["independent_decimal_replay"]
    assert replay["p7"]["pair_count"] == 21
    assert replay["p7"]["boxes_evaluated"] == 6173
    assert replay["p5"]["pair_count"] == 10
    assert replay["p5"]["boxes_evaluated"] == 4340
    assert float(replay["p7"]["minimum_outward_lower_endpoint"]) > 0.09
    assert float(replay["p5"]["minimum_outward_lower_endpoint"]) > 0.09


def test_phase_winding_is_shared_not_prime_specific() -> None:
    phase = build_receipt()["phase_sensitivity"]
    assert boundary_knot(3) == "T(2,7)"
    assert phase["p7"]["selected_center_winding"] == phase["p5"]["selected_center_winding"] == 3
    assert phase["p7"]["center_boundary"] == phase["p5"]["center_boundary"] == "T(2,7)"


def test_all_five_length_three_values_are_zero() -> None:
    audit = build_receipt()["p7_milnor_audit"]
    assert tuple(tuple(item) for item in audit["triples"]) == SPLIT_TRIPLES
    assert audit["fixture"]["mu_bar_123"] == -1
    assert audit["mu_bar_123_values"] == [0, 0, 0, 0, 0]
    assert audit["crossing_counts"] == [38, 42, 38, 42, 32]


def test_receipt_is_deterministic_and_nonselecting() -> None:
    first = build_receipt()
    assert first == build_receipt()
    validate_receipt(first)
    assert first["selection_effect"] == "none"
    assert len(first["payload_sha256"]) == 64
    assert any("Riemann" in item for item in first["nonclaims"])
