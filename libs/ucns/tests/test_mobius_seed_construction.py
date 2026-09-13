"""Regression tests for UCNS Mobius Seed construction state.

Usage guidance:
    Focused: ``python -m pytest tests/test_mobius_seed_construction.py``
    Full repo: ``python -m pytest``
"""

# === CHECKS ===
# id: check_mobius_seed_construction_center_start
#   proves: mobius_seed_construction_starts_at_the_center
#   call: self::test_initial_state_builds_only_the_center
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_construction_structural_vesica_rule
#   proves: mobius_seed_construction_is_adjacency_from_seed_relations
#   call: self::test_buildable_next_derives_from_structural_vesicas_only
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_construction_no_game_semantics
#   proves: mobius_seed_construction_never_invents_game_semantics
#   call: self::test_receipt_carries_no_game_semantics
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_construction_fail_closed
#   proves: mobius_seed_construction_is_adjacency_from_seed_relations
#   call: self::test_unbuildable_slot_fails_closed
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_construction_state_boundary
#   proves: mobius_seed_construction_state_boundary_is_immutable_and_centered
#   call: self::test_state_normalizes_built_collection_and_requires_center
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_construction_full_completion
#   proves: mobius_seed_construction_completes_and_replays
#   call: self::test_full_construction_completes_all_seven_slots
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_construction_replay
#   proves: mobius_seed_construction_completes_and_replays
#   call: self::test_from_built_replays_a_persisted_slot_list
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_construction_serialized_replay
#   proves: mobius_seed_construction_completes_and_replays
#   call: self::test_serialized_built_values_round_trip_and_unknown_fails
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from ucns.mobius_seed import BandSlot, MobiusSeedError, build_mobius_seed_of_life
from ucns.mobius_seed_construction import (
    ConstructionState,
    buildable_slots,
    construct,
    from_built,
    initial_construction_state,
)


def _seed():
    return build_mobius_seed_of_life()


def _must_raise_mobius_seed_error(callable_) -> None:
    try:
        callable_()
    except MobiusSeedError:
        return
    raise AssertionError("expected MobiusSeedError")


def test_initial_state_builds_only_the_center() -> None:
    state = initial_construction_state(_seed())
    assert state.built == frozenset((BandSlot.CENTER,))
    # Every ring is a structural vesica of the center, so all six rings are
    # buildable next. This is the full one-step frontier of the seven-band
    # seed; later Flower-of-Life rings remain hmmm in UCNS.
    assert buildable_slots(state) == tuple(BandSlot)[1:]


def test_buildable_next_derives_from_structural_vesicas_only() -> None:
    state = construct(initial_construction_state(_seed()), BandSlot.RING_0)
    assert BandSlot.RING_0 in state.built
    # All other rings remain buildable from the built center; the incidental
    # RING_0-RING_2 secant must not add a second-layer rule.
    assert buildable_slots(state) == tuple(
        slot for slot in BandSlot if slot not in (BandSlot.CENTER, BandSlot.RING_0)
    )


def test_unbuildable_slot_fails_closed() -> None:
    state = construct(initial_construction_state(_seed()), BandSlot.RING_0)
    for slot in (BandSlot.RING_0, BandSlot.CENTER):
        _must_raise_mobius_seed_error(lambda slot=slot: construct(state, slot))


def test_state_normalizes_built_collection_and_requires_center() -> None:
    mutable = {BandSlot.CENTER, BandSlot.RING_0}
    state = ConstructionState(seed=_seed(), built=mutable)  # type: ignore[arg-type]
    mutable.clear()
    assert state.built == frozenset((BandSlot.CENTER, BandSlot.RING_0))
    assert isinstance(state.built, frozenset)
    _must_raise_mobius_seed_error(
        lambda: ConstructionState(seed=_seed(), built={BandSlot.RING_0})  # type: ignore[arg-type]
    )


def test_full_construction_completes_all_seven_slots() -> None:
    state = initial_construction_state(_seed())
    while buildable_slots(state):
        state = construct(state, buildable_slots(state)[0])
    assert state.built == set(BandSlot)
    assert buildable_slots(state) == ()


def test_from_built_replays_a_persisted_slot_list() -> None:
    state = construct(construct(initial_construction_state(_seed()), BandSlot.RING_3), BandSlot.RING_2)
    replayed = from_built([BandSlot.CENTER, BandSlot.RING_3, BandSlot.RING_2], _seed())
    assert replayed.built == state.built


def test_serialized_built_values_round_trip_and_unknown_fails() -> None:
    state = construct(construct(initial_construction_state(_seed()), BandSlot.RING_3), BandSlot.RING_2)
    serialized = state.as_dict()["built"]
    assert isinstance(serialized, list)
    assert from_built(serialized, _seed()).built == state.built
    _must_raise_mobius_seed_error(lambda: from_built(["RING_0"], _seed()))
    _must_raise_mobius_seed_error(lambda: from_built(["CENTER", "NOPE"], _seed()))


def test_receipt_carries_no_game_semantics() -> None:
    payload = construct(initial_construction_state(_seed()), BandSlot.RING_1).as_dict()
    assert payload["schema_id"] == "ucns.mobius-seed-construction"
    assert payload["selection_effect"] == "none"
    for key in ("tile", "unit", "turn", "permission", "ahbg"):
        assert key not in str(payload).lower()
