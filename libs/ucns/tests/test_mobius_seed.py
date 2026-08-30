# === CHECKS ===
# id: check_mobius_seed_projection_pair_completion
#   proves: mobius_seed_projection_is_exact_and_pair_complete
#   call: self::test_projection_retains_exact_seed_nodes_and_all_pairs
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_dyad_phase_schedule
#   proves: mobius_seed_dyad_is_anti_aligned_and_outer_phase_is_incremental
#   call: self::test_dyad_is_anti_aligned_and_outer_phases_increment
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_null_void
#   proves: mobius_seed_lift_preserves_null_as_nonvertex_void
#   call: self::test_null_lift_has_six_distinct_nonzero_lanes_and_origin_margin
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_surface_quotient
#   proves: mobius_seed_surface_obeys_360_seam_and_720_return
#   call: self::test_each_surface_obeys_mobius_seam_and_two_turn_return
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_braid_order
#   proves: mobius_seed_structural_pairs_have_alternating_braid_order
#   call: self::test_every_structural_pair_reverses_over_under_order
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_proof_firewall
#   proves: mobius_seed_candidate_is_nonselecting_and_proof_firewalled
#   call: self::test_receipt_and_obj_are_deterministic_nonselecting_candidates
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from fractions import Fraction
import json
import math

from ucns.mobius_seed import (
    MOBIUS_SEED_SCHEMA_ID,
    MOBIUS_SEED_SCHEMA_VERSION,
    BandSlot,
    NodeStanding,
    PairStanding,
    RING_SLOTS,
    TwistChirality,
    build_mobius_seed_of_life,
)


def _assert_point_close(left, right, tolerance: float = 1e-12) -> None:
    assert left.distance_to(right) <= tolerance


def test_projection_retains_exact_seed_nodes_and_all_pairs() -> None:
    seed = build_mobius_seed_of_life()

    assert len(seed.bands) == 7
    assert len(seed.relations) == 21
    assert len(seed.structural_relations) == 12
    assert len(seed.incidental_secants) == 6
    assert len(seed.incidental_tangencies) == 3
    assert len(seed.nodes) == 13
    assert seed.pairwise_projection_event_count == 39
    assert seed.declared_structural_boundary_event_count == 48

    null = seed.node_by_id["NULL"]
    assert null.standing is NodeStanding.NULL_PROJECTION
    assert null.is_vertex is False
    assert null.is_structural_null is False
    assert set(null.incident_slots) == set(RING_SLOTS)

    ring_nodes = tuple(seed.node_by_id[f"RING_{index}"] for index in range(6))
    petal_nodes = tuple(seed.node_by_id[f"PETAL_{index}"] for index in range(6))
    assert all(len(node.incident_slots) == 3 for node in ring_nodes)
    assert all(len(node.incident_slots) == 2 for node in petal_nodes)

    structural_degree = {slot: 0 for slot in BandSlot}
    for relation in seed.structural_relations:
        structural_degree[relation.left] += 1
        structural_degree[relation.right] += 1
        assert relation.center_distance_squared == 1
        assert len(relation.events) == 2
        assert relation.declared_boundary_relation_events == 4
    assert structural_degree[BandSlot.CENTER] == 6
    assert all(structural_degree[slot] == 3 for slot in RING_SLOTS)

    assert all(
        relation.center_distance_squared == 3
        and relation.standing is PairStanding.INCIDENTAL_SECANT
        for relation in seed.incidental_secants
    )
    assert all(
        relation.center_distance_squared == 4
        and relation.standing is PairStanding.INCIDENTAL_TANGENCY
        for relation in seed.incidental_tangencies
    )


def test_dyad_is_anti_aligned_and_outer_phases_increment() -> None:
    seed = build_mobius_seed_of_life()
    bands = seed.band_by_slot
    center = bands[BandSlot.CENTER]
    dyad = bands[BandSlot.RING_0]

    assert center.chirality is TwistChirality.POSITIVE
    assert center.twist_phase_turns == 0
    assert dyad.chirality is TwistChirality.NEGATIVE
    assert dyad.twist_phase_turns == Fraction(1, 2)

    phases = tuple(bands[slot].twist_phase_turns for slot in RING_SLOTS)
    assert phases == tuple(Fraction(1, 2) + Fraction(index, 12) for index in range(6))
    assert tuple(phases[index + 1] - phases[index] for index in range(5)) == (
        Fraction(1, 12),
    ) * 5


def test_null_lift_has_six_distinct_nonzero_lanes_and_origin_margin() -> None:
    seed = build_mobius_seed_of_life()
    occurrences = seed.lifted_occurrences("NULL")
    heights = tuple(height for _, _, height in occurrences)

    assert tuple(slot for slot, _, _ in occurrences) == RING_SLOTS
    assert len({height.exact_text() for height in heights}) == 6
    assert all(height.sign() != 0 for height in heights)

    # With H=1/5 the exact center lanes are sqrt(3)/25 times
    # (-1, +2, -2, +1, +3, -3).
    coefficients = tuple(height.sqrt3 for height in heights)
    assert coefficients == (
        Fraction(-1, 25),
        Fraction(2, 25),
        Fraction(-2, 25),
        Fraction(1, 25),
        Fraction(3, 25),
        Fraction(-3, 25),
    )
    assert all(height.rational == 0 for height in heights)
    assert seed.half_width == Fraction(1, 100)
    assert seed.origin_contact_margin_exact().sign() > 0
    assert math.isclose(
        seed.origin_contact_margin_exact().to_float(),
        (4.0 * math.sqrt(3.0) - 1.0) / 100.0,
        rel_tol=0,
        abs_tol=1e-15,
    )


def test_each_surface_obeys_mobius_seam_and_two_turn_return() -> None:
    seed = build_mobius_seed_of_life()
    sample_turns = (Fraction(0), Fraction(1, 7), Fraction(5, 13))
    sample_breadths = (-seed.half_width, Fraction(0), seed.half_width)

    for slot in BandSlot:
        for turn in sample_turns:
            for breadth in sample_breadths:
                point = seed.surface_point(slot, turn, breadth)
                after_one = seed.surface_point(slot, turn + 1, breadth)
                reversed_breadth = seed.surface_point(slot, turn, -breadth)
                after_two = seed.surface_point(slot, turn + 2, breadth)
                _assert_point_close(after_one, reversed_breadth)
                _assert_point_close(after_two, point)

        boundary_start = seed.boundary_point(slot, 0)
        boundary_after_one = seed.boundary_point(slot, 1)
        opposite_seam_side = seed.surface_point(slot, 0, -seed.half_width)
        boundary_after_two = seed.boundary_point(slot, 2)
        _assert_point_close(boundary_after_one, opposite_seam_side)
        _assert_point_close(boundary_after_two, boundary_start)


def test_every_structural_pair_reverses_over_under_order() -> None:
    seed = build_mobius_seed_of_life()

    for relation in seed.structural_relations:
        first, second = seed.structural_braid_differences(relation)
        assert first.sign() != 0
        assert second.sign() != 0
        assert first.sign() == -second.sign()
        assert "not verified" in relation.boundary_realization_standing


def test_receipt_and_obj_are_deterministic_nonselecting_candidates() -> None:
    seed = build_mobius_seed_of_life()
    receipt = seed.receipt()
    encoded = seed.receipt_json()
    decoded = json.loads(encoded)

    assert receipt == decoded
    assert receipt["schema_id"] == MOBIUS_SEED_SCHEMA_ID
    assert receipt["schema_version"] == MOBIUS_SEED_SCHEMA_VERSION
    assert receipt["selection_effect"] == "none"
    assert receipt["jurisdiction"]["construction_owner"] == "UCNS"
    assert receipt["jurisdiction"]["metapat_role"] == (
        "later semantic consumer only; no geometry or theorem-status transfer"
    )
    assert any("Riemann" in item for item in receipt["nonclaims"])
    assert any("spectral operator" in item for item in receipt["hmmm"])

    first = seed.obj_text(longitudinal_segments=12, breadth_segments=2)
    second = seed.obj_text(longitudinal_segments=12, breadth_segments=2)
    assert first == second
    assert "selection_effect none" in first
    assert first.count("\ng ") == 7
    assert first.count("\nv ") == 7 * 12 * 3
    assert first.count("\nf ") == 7 * 12 * 2
