# === CHECKS ===
# id: check_prime_length4_commutator_gate
#   proves: prime_length4_magnus_gate_matches_frozen_commutator
#   call: self::test_frozen_degree_three_commutator_gate
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_prime_length4_lower_gates
#   proves: prime_p7_length4_target_is_frozen_and_lower_gated
#   call: self::test_frozen_target_and_lower_order_gates
#   requires: python3, mpmath
#   timeout: 60
#   mutates: none
#   cleanup: none
#
# id: check_prime_length4_cyclic_receipt
#   proves: prime_p7_length4_result_records_cyclic_conventions
#   call: self::test_result_records_primary_reverse_and_cyclic_coefficients
#   requires: python3, mpmath
#   timeout: 60
#   mutates: none
#   cleanup: none
#
# id: check_prime_length4_bounded_receipt
#   proves: prime_p7_length4_receipt_is_bounded
#   call: self::test_receipt_is_deterministic_and_bounded
#   requires: python3, mpmath
#   timeout: 60
#   mutates: temporary_path
#   cleanup: pytest temporary_path
# === END CHECKS ===

from __future__ import annotations

import json

from ucns.prime_length4_milnor import (
    TARGET,
    evaluate_p7_length_four_milnor,
    length_four_commutator_gate,
    write_p7_length_four_milnor_certificate,
)


def test_frozen_degree_three_commutator_gate() -> None:
    gate = length_four_commutator_gate()
    assert gate["passed"] is True
    assert gate["degree_three_coefficients"] == {
        "X1_X2_X3": 1,
        "X2_X1_X3": -1,
        "X3_X1_X2": -1,
        "X3_X2_X1": 1,
    }
    assert gate["lower_degree_nonzero_coefficients"] == {}


def test_frozen_target_and_lower_order_gates() -> None:
    result = evaluate_p7_length_four_milnor()
    assert TARGET == ("R0", "R1", "R4", "R5")
    assert result.pairwise_linking == (0, 0, 0, 0, 0, 0)
    assert result.triple_milnor == (0, 0, 0, 0)
    assert result.lower_degree_nonzero == ()


def test_result_records_primary_reverse_and_cyclic_coefficients() -> None:
    result = evaluate_p7_length_four_milnor()
    assert result.status in {"zero", "nonzero", "unresolved"}
    assert result.primary_coefficient is not None
    assert result.reverse_word_coefficient is not None
    assert len(result.cyclic_coefficients) == 4


def test_receipt_is_deterministic_and_bounded(tmp_path) -> None:
    first = evaluate_p7_length_four_milnor().as_dict()
    second = evaluate_p7_length_four_milnor().as_dict()
    assert first == second
    output = write_p7_length_four_milnor_certificate(tmp_path / "result.json")
    assert json.loads(output.read_text(encoding="utf-8")) == first
    text = json.dumps(first).lower()
    for forbidden in ("riemann hypothesis proof", "ambient-isotopy classification established"):
        assert forbidden not in text
