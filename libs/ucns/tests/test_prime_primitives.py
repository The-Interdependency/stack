# === CHECKS ===
# id: check_prime_arithmetic_geometry_firewall
#   proves: prime_arithmetic_geometry_firewall
#   call: self::test_arithmetic_and_geometry_are_separate
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_prime_two_cycle_boundary
#   proves: prime_two_cycle_boundary
#   call: self::test_two_cycle_boundary_is_conditional
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_prime_p7_direct_signature
#   proves: prime_p7_direct_exact_signature
#   call: self::test_p7_exact_signature
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_prime_p7_uniform_relation
#   proves: prime_p7_uniform_structural_relation
#   call: self::test_p7_uniform_relation_and_uniqueness
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_prime_p5_direct_signature
#   proves: prime_p5_direct_exact_signature
#   call: self::test_p5_exact_signature
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_prime_restrictions_after_construction
#   proves: prime_restrictions_follow_construction
#   call: self::test_restrictions_are_readouts_not_parts
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
# === END CHECKS ===

import math

from ucns.prime_primitives import (
    build_prime_five,
    build_prime_seven,
    cycle_rank,
    dyadic_boundary,
    family_certificate,
    is_arithmetic_prime,
)


def test_arithmetic_and_geometry_are_separate() -> None:
    assert is_arithmetic_prime(2)
    assert is_arithmetic_prime(3)
    assert is_arithmetic_prime(5)
    assert is_arithmetic_prime(7)
    assert not is_arithmetic_prime(1)
    assert not is_arithmetic_prime(9)
    assert family_certificate()["selection_effect"] == "none"


def test_two_cycle_boundary_is_conditional() -> None:
    boundary = dyadic_boundary()
    assert boundary["arithmetic_prime"] is True
    assert boundary["cycle_rank"] == 0
    assert boundary["has_nontrivial_relational_cycle"] is False
    assert boundary["mobius_two_turn_return"] is True
    assert boundary["proof_boundary"].startswith("not a proof")
    assert cycle_rank(3, 3) == 1


def test_p7_exact_signature() -> None:
    p7 = build_prime_seven()
    assert len(p7.pair_distance_squared) == 21
    assert p7.relation_counts == {"unit-vesica": 12, "secant": 6, "tangent": 3}
    assert p7.pair_event_count == 39
    assert p7.hypernode_pair_count == 39
    assert len(p7.hypernodes) == 13
    assert p7.arity_spectrum == {"2": 6, "3": 6, "6": 1}
    assert next(node for node in p7.hypernodes if node.point == ("0", "0")).pair_count == 15


def test_p7_uniform_relation_and_uniqueness() -> None:
    p7 = build_prime_seven()
    assert len(p7.structural_pairs) == 12
    assert all(tuple(sorted(edge)) in {tuple(sorted(pair)) for pair in p7.unit_pairs} for edge in p7.structural_pairs)
    assert p7.structural_cycle_rank == 6
    assert len(p7.unit_triangles) == 6
    assert math.isclose(2 * math.sin(math.pi / 6), 1.0, abs_tol=1e-15)
    assert all(not math.isclose(2 * math.sin(math.pi / q), 1.0, abs_tol=1e-12) for q in range(3, 65) if q != 6)


def test_p5_exact_signature() -> None:
    p5 = build_prime_five()
    assert len(p5.pair_distance_squared) == 10
    assert p5.relation_counts == {"unit-vesica": 4, "secant": 4, "tangent": 2}
    assert p5.pair_event_count == 18
    assert p5.hypernode_pair_count == 18
    assert len(p5.hypernodes) == 13
    assert p5.arity_spectrum == {"2": 12, "4": 1}
    assert p5.structural_cycle_rank == 4
    assert len(p5.unit_triangles) == 0


def test_restrictions_are_readouts_not_parts() -> None:
    p7, p5 = build_prime_seven().payload(), build_prime_five().payload()
    assert "restrictions derived afterward" in p7["construction_lineage"]
    assert "restrictions derived afterward" in p5["construction_lineage"]
    assert p7["unit_pair_restrictions"] == 12
    assert p7["unit_triangle_restrictions"] == 6
    assert p5["unit_pair_restrictions"] == 4
    assert p5["unit_triangle_restrictions"] == 0
    assert family_certificate()["research_order"] == [7, 5]
