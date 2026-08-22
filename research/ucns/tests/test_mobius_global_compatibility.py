# === CHECKS ===
# id: check_mobius_seed_surface_phase_quotient
#   proves: mobius_seed_incident_certified_dyads_are_state_incompatible
#   call: self::test_surface_phase_uses_the_unlabelled_half_turn_quotient
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_rigid_rotation_transport
#   proves: mobius_seed_incident_certified_dyads_are_state_incompatible
#   call: self::test_rigid_rotation_transport_is_exact_on_representative_spokes
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_direct_rotation_agreement
#   proves: mobius_seed_incident_certified_dyads_are_state_incompatible
#   call: self::test_rigid_rotation_phase_transport_matches_direct_surface_rotation
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_incident_dyad_state_incompatibility
#   proves: mobius_seed_incident_certified_dyads_are_state_incompatible
#   call: self::test_all_oriented_incident_edge_states_are_incompatible
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_single_state_capacity_three
#   proves: mobius_seed_single_state_certified_capacity_is_three
#   call: self::test_compatible_certified_pairs_have_exact_maximum_capacity_three
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_center_six_phase_channels
#   proves: mobius_seed_center_needs_six_phase_channels_for_six_spokes
#   call: self::test_center_spokes_require_six_distinct_surface_phases
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_contact_braid_exclusivity
#   proves: mobius_seed_physical_contact_and_strict_braid_are_event_exclusive
#   call: self::test_physical_contact_and_strict_braid_are_same_event_exclusive
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_pr174_zero_inheritance
#   proves: mobius_seed_pr174_inherits_no_exact_rigid_vesica_pairs
#   call: self::test_pinned_pr174_schedule_inherits_zero_complete_local_certificates
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_mobius_seed_global_certificate_firewall
#   proves: mobius_seed_global_compatibility_certificate_is_nonselecting
#   call: self::test_generated_certificate_is_deterministic_nonselecting_and_bounded
#   requires: python3
#   timeout: 10
#   mutates: temporary_path
#   cleanup: pytest temporary_path
# === END CHECKS ===

from fractions import Fraction
import json
import math

from ucns.mobius_global_compatibility import (
    EdgeOrientation,
    build_structural_edges,
    certified_edge_copies,
    contact_and_strict_braid_compatible,
    edge_inherits_certificate,
    pinned_pr174_assignment,
    prove_global_compatibility_boundary,
    surface_phase,
    write_global_compatibility_certificate,
)
from ucns.mobius_vesica import TwistChirality


def test_surface_phase_uses_the_unlabelled_half_turn_quotient() -> None:
    assert surface_phase(Fraction(0)) == 0
    assert surface_phase(Fraction(1, 2)) == 0
    assert surface_phase(Fraction(7, 12)) == Fraction(1, 12)
    assert surface_phase(Fraction(-1, 12)) == Fraction(5, 12)


def test_rigid_rotation_transport_is_exact_on_representative_spokes() -> None:
    edges = {edge.edge_id: edge for edge in build_structural_edges()}

    zero_axis = certified_edge_copies(edges["CENTER_RING_0"])
    assert zero_axis[0].orientation is EdgeOrientation.PLUS_AT_LEFT
    assert zero_axis[0].left_state.chirality is TwistChirality.POSITIVE
    assert zero_axis[0].left_state.phase_turns_mod_half == 0
    assert zero_axis[0].right_state.chirality is TwistChirality.NEGATIVE
    assert zero_axis[0].right_state.phase_turns_mod_half == Fraction(1, 4)

    one_sixth = certified_edge_copies(edges["CENTER_RING_1"])
    assert one_sixth[0].left_state.phase_turns_mod_half == Fraction(5, 12)
    assert one_sixth[0].right_state.phase_turns_mod_half == Fraction(1, 3)
    assert one_sixth[1].left_state.phase_turns_mod_half == Fraction(1, 12)
    assert one_sixth[1].right_state.phase_turns_mod_half == Fraction(1, 6)


def test_rigid_rotation_phase_transport_matches_direct_surface_rotation() -> None:
    rho = Fraction(1, 6)
    beta = math.tau * float(rho)
    cosine_beta = math.cos(beta)
    sine_beta = math.sin(beta)
    breadth = 0.01

    for chirality, phase in (
        (TwistChirality.POSITIVE, Fraction(0)),
        (TwistChirality.NEGATIVE, Fraction(1, 4)),
    ):
        transported_phase_raw = (
            phase - Fraction(chirality.value) * rho / 2
        )
        transported_phase = surface_phase(transported_phase_raw)
        assert transported_phase == transported_phase_raw % Fraction(1, 2)
        for turn in (0.0, 0.173, 0.731):
            local_theta = math.tau * turn
            local_twist = (
                chirality.value * math.pi * turn
                + math.tau * float(phase)
            )
            local_radius = 1.0 + breadth * math.cos(local_twist)
            local = (
                local_radius * math.cos(local_theta),
                local_radius * math.sin(local_theta),
                breadth * math.sin(local_twist),
            )
            rotated = (
                local[0] * cosine_beta - local[1] * sine_beta,
                local[0] * sine_beta + local[1] * cosine_beta,
                local[2],
            )

            global_turn = turn + float(rho)
            global_theta = math.tau * global_turn
            global_twist = (
                chirality.value * math.pi * global_turn
                + math.tau * float(transported_phase_raw)
            )
            global_radius = 1.0 + breadth * math.cos(global_twist)
            direct = (
                global_radius * math.cos(global_theta),
                global_radius * math.sin(global_theta),
                breadth * math.sin(global_twist),
            )
            assert all(
                math.isclose(left, right, rel_tol=0, abs_tol=1e-12)
                for left, right in zip(rotated, direct)
            )



def test_all_oriented_incident_edge_states_are_incompatible() -> None:
    boundary = prove_global_compatibility_boundary()

    assert boundary.total_structural_pairs == 12
    assert boundary.adjacent_edge_pair_count == 33
    assert boundary.oriented_adjacency_checks == 132
    assert boundary.compatible_oriented_adjacencies == 0


def test_compatible_certified_pairs_have_exact_maximum_capacity_three() -> None:
    boundary = prove_global_compatibility_boundary()
    edge_by_id = {edge.edge_id: edge for edge in boundary.edges}

    assert boundary.maximum_opposite_chirality_edges == 9
    assert len(boundary.maximum_cut_assignments) == 2
    assert boundary.maximum_matching_size == 3
    assert boundary.minimum_noninheriting_pairs == 9
    assert len(boundary.maximum_matchings) == 20
    for witness in boundary.maximum_matchings:
        assert len(witness) == 3
        used: set[str] = set()
        for edge_id in witness:
            edge = edge_by_id[edge_id]
            assert edge.left not in used
            assert edge.right not in used
            used.update((edge.left, edge.right))


def test_center_spokes_require_six_distinct_surface_phases() -> None:
    boundary = prove_global_compatibility_boundary()
    expected = (
        Fraction(0),
        Fraction(1, 12),
        Fraction(1, 6),
        Fraction(1, 4),
        Fraction(1, 3),
        Fraction(5, 12),
    )

    assert boundary.center_positive_spoke_phases == expected
    assert boundary.center_negative_spoke_phases == expected
    assert len(set(boundary.center_positive_spoke_phases)) == 6


def test_physical_contact_and_strict_braid_are_same_event_exclusive() -> None:
    assert contact_and_strict_braid_compatible(
        physical_contact=False,
        delta_z_nonzero=False,
    )
    assert contact_and_strict_braid_compatible(
        physical_contact=False,
        delta_z_nonzero=True,
    )
    assert contact_and_strict_braid_compatible(
        physical_contact=True,
        delta_z_nonzero=False,
    )
    assert not contact_and_strict_braid_compatible(
        physical_contact=True,
        delta_z_nonzero=True,
    )


def test_pinned_pr174_schedule_inherits_zero_complete_local_certificates() -> None:
    assignment = pinned_pr174_assignment()
    edges = build_structural_edges()

    assert assignment["CENTER"].chirality is TwistChirality.POSITIVE
    assert assignment["CENTER"].phase_turns_mod_half == 0
    assert all(
        assignment[f"RING_{index}"].chirality is TwistChirality.NEGATIVE
        for index in range(6)
    )
    assert tuple(
        assignment[f"RING_{index}"].phase_turns_mod_half
        for index in range(6)
    ) == (
        Fraction(0),
        Fraction(1, 12),
        Fraction(1, 6),
        Fraction(1, 4),
        Fraction(1, 3),
        Fraction(5, 12),
    )
    assert not any(edge_inherits_certificate(edge, assignment) for edge in edges)


def test_generated_certificate_is_deterministic_nonselecting_and_bounded(tmp_path) -> None:
    first = prove_global_compatibility_boundary().payload
    second = prove_global_compatibility_boundary().payload
    assert first == second

    output = write_global_compatibility_certificate(
        tmp_path / "mobius-seed-global-compatibility-certificate.json"
    )
    decoded = json.loads(output.read_text(encoding="utf-8"))
    assert decoded == first
    assert decoded["selection_effect"] == "none"
    assert decoded["status"].startswith("obstructed-under-single")
    assert decoded["chirality_only"][
        "maximum_opposite_edges"
    ] == 9
    assert decoded["full_state"]["maximum_simultaneous_exact_dyads"] == 3
    assert decoded["full_state"]["minimum_pairs_requiring_relaxation"] == 9
    assert decoded["full_state"]["maximum_fraction"] == "1/4"
    assert decoded["center_channel_bound"][
        "minimum_channels_for_six_rigid_spokes"
    ] == 6
    assert decoded["pr174"]["inherited_count"] == 0
    assert decoded["lift_boundary"]["same_event_compatible"] is False
    assert len(decoded["payload_sha256"]) == 64
    assert any("not an obstruction" in item for item in decoded["nonclaims"])
    assert any("Riemann" in item for item in decoded["nonclaims"])
