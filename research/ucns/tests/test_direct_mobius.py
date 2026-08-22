# === CHECKS ===
# id: native_mobius_return_check
#   proves: native_mobius_one_turn_reverses_frame, native_mobius_two_turns_restore_complete_state, native_mobius_motion_is_exactly_invertible
#   call: self::test_native_mobius_return_and_inverse
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from fractions import Fraction

from ucns.direct_mobius import (
    NativeMobiusFrame,
    STRUCTURAL_NULL_ORIGIN,
    native_mobius_state,
)


def test_native_mobius_return_and_inverse() -> None:
    origin = native_mobius_state()
    one = origin.advance(1)
    two = origin.advance(2)

    assert one.phase_turns == origin.phase_turns == Fraction(0)
    assert one.frame is NativeMobiusFrame.REVERSED
    assert one.visible_key == origin.visible_key
    assert one.complete_key != origin.complete_key
    assert two == origin

    displaced = origin.advance(Fraction(7, 3))
    assert displaced.advance(Fraction(-7, 3)) == origin
    assert STRUCTURAL_NULL_ORIGIN.carrier_position == 0
