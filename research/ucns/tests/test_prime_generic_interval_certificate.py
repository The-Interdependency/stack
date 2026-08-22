# === CHECKS ===
# id: check_prime_generic_interval_atan2
#   proves: prime_generic_turns_are_outward_atan2_enclosed
#   call: self::test_all_frozen_turns_are_inside_outward_atan2_intervals
#   requires: python3, system-libmpfr, mpmath
#   timeout: 60
#   mutates: none
#   cleanup: none
#
# id: check_prime_generic_interval_smooth_signs
#   proves: prime_generic_smooth_signs_are_interval_certified
#   call: self::test_all_smooth_height_intervals_exclude_zero_and_preserve_order
#   requires: python3, system-libmpfr, mpmath
#   timeout: 60
#   mutates: none
#   cleanup: none
#
# id: check_prime_generic_interval_crossing_signs
#   proves: prime_generic_crossing_signs_are_interval_certified
#   call: self::test_all_p7_first_p5_second_crossing_signs_are_certified
#   requires: python3, system-libmpfr, mpmath
#   timeout: 60
#   mutates: none
#   cleanup: none
#
# id: check_prime_generic_interval_receipt
#   proves: prime_generic_interval_receipt_is_nonselecting
#   call: self::test_family_receipt_is_deterministic_complete_and_nonselecting
#   requires: python3, system-libmpfr, mpmath
#   timeout: 120
#   mutates: temporary_path
#   cleanup: pytest temporary_path
# === END CHECKS ===

from __future__ import annotations

import json

import pytest

from ucns.prime_generic_interval_certificate import (
    certify_generic_prime_diagram,
    generic_interval_family_certificate,
    write_generic_interval_family_certificate,
)


@pytest.fixture(scope="module")
def certificates():
    return certify_generic_prime_diagram(7), certify_generic_prime_diagram(5)


def test_all_frozen_turns_are_inside_outward_atan2_intervals(certificates) -> None:
    p7, p5 = certificates
    assert p7.all_turns_enclosed is True
    assert p5.all_turns_enclosed is True
    assert (p7.crossing_count, p5.crossing_count) == (38, 18)


def test_all_smooth_height_intervals_exclude_zero_and_preserve_order(certificates) -> None:
    for certificate in certificates:
        assert certificate.all_height_orders_agree is True
        for crossing in certificate.crossings:
            lower = float(crossing.height_difference_lower.replace("e", "E"))
            upper = float(crossing.height_difference_upper.replace("e", "E"))
            assert lower > 0 or upper < 0


def test_all_p7_first_p5_second_crossing_signs_are_certified(certificates) -> None:
    p7, p5 = certificates
    assert p7.all_crossing_signs_agree is True
    assert p5.all_crossing_signs_agree is True
    assert all(row.certified_sign in {-1, 1} for row in (*p7.crossings, *p5.crossings))


def test_family_receipt_is_deterministic_complete_and_nonselecting(tmp_path) -> None:
    first = generic_interval_family_certificate()
    second = generic_interval_family_certificate()
    assert first == second
    output = write_generic_interval_family_certificate(tmp_path / "certificate.json")
    assert json.loads(output.read_text(encoding="utf-8")) == first
    assert first["research_order"] == ["P7", "P5"]
    assert first["complete_crossing_count"] == 56
    assert first["selection_effect"] == "none"
    assert "not proof-assistant" in first["standing"]
    assert len(first["payload_sha256"]) == 64
