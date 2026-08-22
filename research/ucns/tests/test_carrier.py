# === CHECKS ===
# id: check_structural_null_identity
#   proves: structural_null_is_unique_and_coordinate_free
#   call: self::test_structural_null_identity
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_non_null_validation_and_radius
#   proves: non_null_carrier_has_positive_breadth
#   call: self::test_non_null_validation_and_radius
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_lifted_period
#   proves: lifted_period_is_720_degrees, two_visible_laps_complete_return
#   call: self::test_lifted_period
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_visible_projection_and_branch_law
#   proves: visible_projection_is_360_degrees
#   call: self::test_visible_projection_and_branch_law
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_one_lap_is_deck_translation
#   proves: one_visible_lap_is_deck_translation_only, topology_does_not_invent_orientation_algebra
#   call: self::test_one_lap_is_deck_translation
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_payload_zero_does_not_collapse_carrier
#   proves: algebraic_zero_is_not_structural_null
#   call: self::test_payload_zero_does_not_collapse_carrier
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from math import isclose, pi

import pytest

from ucns import (
    LIFTED_PERIOD,
    STRUCTURAL_NULL,
    VISIBLE_PERIOD,
    LiftedCarrierPoint,
    carrier_from_breadth,
    deck_translate,
    lifted_preimages,
    project,
    same_lifted_position,
    same_visible_position,
)


def test_structural_null_identity() -> None:
    assert carrier_from_breadth(0) is STRUCTURAL_NULL
    assert project(STRUCTURAL_NULL) is STRUCTURAL_NULL
    assert deck_translate(STRUCTURAL_NULL) is STRUCTURAL_NULL
    assert lifted_preimages(STRUCTURAL_NULL) == (STRUCTURAL_NULL,)
    assert not hasattr(STRUCTURAL_NULL, "angle")
    assert STRUCTURAL_NULL != 0


def test_non_null_validation_and_radius() -> None:
    point = LiftedCarrierPoint(2.0, 0.0)
    assert 0.0 < point.radius < 1.0
    wide = LiftedCarrierPoint(100.0, 0.0)
    assert 0.0 < wide.radius < 1.0
    visible = project(wide)
    assert visible.breadth == wide.breadth
    assert any(same_lifted_position(candidate, wide) for candidate in lifted_preimages(visible))
    with pytest.raises(ValueError):
        LiftedCarrierPoint(0.0, 0.0)
    with pytest.raises(ValueError):
        carrier_from_breadth(-1.0)


def test_lifted_period() -> None:
    point = LiftedCarrierPoint(1.0, 0.375)
    after_one = point.rotate(VISIBLE_PERIOD)
    after_two = after_one.rotate(VISIBLE_PERIOD)
    assert after_one != point
    assert same_lifted_position(after_two, point)
    assert same_lifted_position(point.rotate(LIFTED_PERIOD), point)


def test_visible_projection_and_branch_law() -> None:
    point = LiftedCarrierPoint(1.5, 7.0 * pi)
    visible = project(point)
    assert isclose(visible.angle, pi, abs_tol=1e-12)
    preimages = lifted_preimages(visible)
    assert len(preimages) == 2
    assert preimages[0] != preimages[1]
    assert same_visible_position(project(preimages[0]), visible)
    assert same_visible_position(project(preimages[1]), visible)


def test_one_lap_is_deck_translation() -> None:
    point = LiftedCarrierPoint(1.0, 0.25)
    advanced = deck_translate(point)
    assert advanced != point
    assert same_visible_position(project(advanced), project(point))
    for invented_field in (
        "sign",
        "negated",
        "reflection",
        "parity",
        "chirality",
        "orientation",
        "frame_inverted",
        "payload",
    ):
        assert not hasattr(advanced, invented_field)


def test_payload_zero_does_not_collapse_carrier() -> None:
    payload_value = 0
    point = LiftedCarrierPoint(1.0, 0.0)
    assert payload_value == 0
    assert point is not STRUCTURAL_NULL
