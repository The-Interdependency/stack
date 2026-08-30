# === MODULE_BUILD ===
# id: ucns_prime_replay_phase_milnor_data
#   module_name: prime_replay_phase_milnor_data
#   module_kind: experiment
#   summary: immutable independent replay, phase-sensitivity, and numerical Milnor receipt data
#   owner: Erin Spencer
#   public_surface: internal readable implementation used through the declared facade
#   internal_surface: module implementation
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_replay_phase_milnor_receipt.py
#   rollout: readable implementation; authority remains with the facade contracts
#   rollback: remove only with the owning consolidated research layer
#   requires: ucns_prime_smooth_ribbons_p7_p5
#   since: 2026-08-11
#   unresolved: see owning facade contracts and research document
# === END MODULE_BUILD ===

# === CONTRACTS ===
# Internal helper: behavioral obligations are declared by the owning facade and witnessed by its tests.
# id: prime_replay_data_is_receipt_witnessed
#   given: the owning facade invokes this readable helper
#   then: the helper behavior is exercised through the named facade test without becoming a separate certificate
#   class: evidence
#   since: 2026-08-11
#
# === END CONTRACTS ===

"""Frozen data for the compact P7 independent-replay/phase/Milnor receipt."""

SPLIT_TRIPLES = (
    ("R0", "R1", "R4"),
    ("R0", "R1", "R5"),
    ("R0", "R2", "R5"),
    ("R0", "R4", "R5"),
    ("R1", "R4", "R5"),
)

BASE_RECEIPT = {
    "schema_id": "ucns.prime-replay-phase-milnor.receipt",
    "schema_version": "0.1.0",
    "authority": "Erin Spencer",
    "recorded_on": "2026-08-11",
    "selection_effect": "none",
    "research_order": [7, 5],
    "independent_decimal_replay": {
        "backend": "python-decimal-directed; no mpmath import",
        "precision_decimal_digits": 90,
        "p7": {
            "pair_count": 21,
            "boxes_evaluated": 6173,
            "maximum_depth": 20,
            "minimum_outward_lower_endpoint": "0.090005150000754974092035106362967",
            "accepted_leaf_ledger_sha256": "7b5b6249ce1592632c313b12148fad59cdf46f86d817191b5d053989cebe65d8",
        },
        "p5": {
            "pair_count": 10,
            "boxes_evaluated": 4340,
            "maximum_depth": 20,
            "minimum_outward_lower_endpoint": "0.090008623538792625962610625869402",
            "accepted_leaf_ledger_sha256": "321077fa87c0d41bb921276aba6156978c5373ea33e741f93c6161b202b2d3c8",
        },
        "centerline_target": "9/100",
        "finite_width_ribbon_separation_lower_bound": "7/100",
    },
    "phase_sensitivity": {
        "p7": {"admissible_laws": 144, "selected_center_winding": 3, "selected_outer_step": "3/7", "selected_minimum_gap": "1/7", "center_boundary": "T(2,7)"},
        "p5": {"admissible_laws": 72, "selected_center_winding": 3, "selected_outer_step": "4/5", "selected_minimum_gap": "1/5", "center_boundary": "T(2,7)"},
        "conclusion": "T(2,7) is imposed by the shared selected winding three and is not presently prime-seven-specific evidence",
    },
    "p7_milnor_audit": {
        "fixture": {"link": "Borromean closure of (sigma1 sigma2^-1)^3", "mu_bar_123": -1},
        "triples": [list(item) for item in SPLIT_TRIPLES],
        "mu_bar_123_values": [0, 0, 0, 0, 0],
        "projection_ids": ["P0", "P1", "P2", "P3", "P4"],
        "crossing_counts": [38, 42, 38, 42, 32],
        "sampling_resolutions": [512, 1024, 2048, 4096],
        "basepoint_offset_sweeps": 10,
        "projection_payload_sha256": "862151539ffaf328df83519cc7d69c00ad46d4ce5b422fcf90e189956fbf6c9c",
        "standing": "crossing extraction numerical; integer Magnus expansion exact on each frozen crossing table",
    },
    "nonclaims": [
        "not a proof-assistant interval theorem",
        "not an analytic proof that every P7 triple Milnor invariant vanishes",
        "not a complete ambient-isotopy or higher-order link classification",
        "not an arithmetic redefinition of primality",
        "not a spectral or zeta-function theorem",
        "not a proof of the Riemann hypothesis",
    ],
}
