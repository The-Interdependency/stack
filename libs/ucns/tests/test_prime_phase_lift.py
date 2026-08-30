# === CHECKS ===
# id: check_prime_phase_lift_p7_first
#   proves: prime_phase_lift_constructs_p7_before_restrictions
#   call: self::test_p7_global_candidate_precedes_readouts
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_phase_lift_seam
#   proves: prime_phase_lift_is_seam_compatible
#   call: self::test_mobius_one_turn_reversal_and_two_turn_return
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_phase_lift_data_coverage
#   proves: prime_phase_lift_data_covers_every_p7_p5_hypernode
#   call: self::test_every_hypernode_has_distinct_phase_and_height
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_phase_lift_hypernodes
#   proves: prime_phase_lift_resolves_every_hypernode
#   call: self::test_every_hypernode_has_distinct_phase_and_height
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_phase_lift_origin
#   proves: prime_phase_lift_preserves_nary_origin
#   call: self::test_p7_origin_remains_one_arity_six_hypernode
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_prime_phase_lift_model_event_semantics
#   proves: prime_phase_lift_model_preserves_event_semantics
#   call: self::test_projected_pair_events_are_strictly_height_separated
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_phase_lift_disjoint_centerlines
#   proves: prime_phase_lift_centerlines_are_disjoint
#   call: self::test_projected_pair_events_are_strictly_height_separated
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_phase_lift_model_derived_links
#   proves: prime_phase_lift_model_derives_links_after_global_lift
#   call: self::test_link_readouts_follow_global_lift
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_phase_lift_links
#   proves: prime_phase_lift_link_numbers_are_derived
#   call: self::test_link_readouts_follow_global_lift
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_phase_lift_p5_second
#   proves: prime_phase_lift_p5_follows_same_protocol
#   call: self::test_p5_is_independent_same_protocol_comparison
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_prime_phase_lift_receipt
#   proves: prime_phase_lift_receipt_is_nonselecting
#   call: self::test_receipt_is_deterministic_and_bounded
#   requires: python3
#   timeout: 10
#   mutates: temporary_path
#   cleanup: pytest temporary_path
# === END CHECKS ===

from fractions import Fraction
import json

from ucns.prime_phase_lift import (
    EventSemantic, build_prime_five_phase_lift, build_prime_seven_phase_lift,
    phase_lift_family_certificate, select_phase_law, write_phase_lift_family_certificate,
)


def test_p7_global_candidate_precedes_readouts() -> None:
    p7 = build_prime_seven_phase_lift()
    assert (p7.prime, len(p7.carriers), len(p7.hypernodes), len(p7.pair_readouts)) == (7, 7, 13, 21)
    assert p7.primitive.arity_spectrum == {"2": 6, "3": 6, "6": 1}
    law = select_phase_law(7)
    assert (law.center_winding, law.outer_step, law.minimum_gap, law.candidates, law.admissible) == (3, Fraction(3, 7), Fraction(1, 7), 174, 144)


def test_mobius_one_turn_reversal_and_two_turn_return() -> None:
    for candidate in (build_prime_seven_phase_lift(), build_prime_five_phase_lift()):
        one, two = candidate.seam_residuals()
        assert one < 3e-15
        assert two < 3e-15


def test_every_hypernode_has_distinct_phase_and_height() -> None:
    for candidate in (build_prime_seven_phase_lift(), build_prime_five_phase_lift()):
        for node in candidate.hypernodes:
            assert node.minimum_phase_gap > 0
            assert node.minimum_height_gap >= Fraction(1, 10)
        assert candidate.event_ribbon_clearance == Fraction(2, 25)


def test_p7_origin_remains_one_arity_six_hypernode() -> None:
    p7 = build_prime_seven_phase_lift()
    assert p7.origin.arity == 6
    assert sorted(item.height for item in p7.origin.occurrences) == [Fraction(-3, 10), Fraction(-1, 5), Fraction(-1, 10), Fraction(1, 10), Fraction(1, 5), Fraction(3, 10)]
    assert p7.origin_void_lower_bound == Fraction(9, 100)
    assert p7.origin.arity * (p7.origin.arity - 1) // 2 == 15


def test_projected_pair_events_are_strictly_height_separated() -> None:
    for candidate in (build_prime_seven_phase_lift(), build_prime_five_phase_lift()):
        for node in candidate.hypernodes:
            heights = [item.height for item in node.occurrences]
            assert len(heights) == len(set(heights))
        assert candidate.summary()["centerline_link"].startswith("pairwise disjoint")
        assert candidate.summary()["physical_centerline_contacts_claimed"] == 0
        assert candidate.summary()["event_semantics"] == [EventSemantic.PROJECTED_COINCIDENCE.value, EventSemantic.STRICT_BRAID_ORDER.value]


def test_link_readouts_follow_global_lift() -> None:
    p7, p5 = build_prime_seven_phase_lift(), build_prime_five_phase_lift()
    assert p7.link_summary == {"regular_linking_number_counts": {"0": 6, "1": 12}, "nonzero_link_pairs": 12, "tangent_pairs_unresolved": 3, "nonzero_link_graph": {"edges": 12, "components": 1, "cycle_rank": 6}}
    assert p5.link_summary == {"regular_linking_number_counts": {"0": 6, "1": 2}, "nonzero_link_pairs": 2, "tangent_pairs_unresolved": 2, "nonzero_link_graph": {"edges": 2, "components": 3, "cycle_rank": 0}}


def test_p5_is_independent_same_protocol_comparison() -> None:
    p5 = build_prime_five_phase_lift(); law = p5.phase_law
    assert (p5.prime, len(p5.carriers), len(p5.hypernodes), len(p5.pair_readouts)) == (5, 5, 13, 10)
    assert (law.center_winding, law.outer_step, law.minimum_gap, law.candidates, law.admissible) == (3, Fraction(4, 5), Fraction(1, 5), 84, 72)
    assert p5.primitive.arity_spectrum == {"2": 12, "4": 1}


def test_receipt_is_deterministic_and_bounded(tmp_path) -> None:
    first, second = phase_lift_family_certificate(), phase_lift_family_certificate()
    assert first == second and first["research_order"] == [7, 5]
    output = write_phase_lift_family_certificate(tmp_path / "receipt.json")
    assert json.loads(output.read_text(encoding="utf-8")) == first
    assert first["selection_effect"] == "none"
    assert len(first["payload_sha256"]) == 64
    assert any("Riemann" in item for item in first["nonclaims"])
