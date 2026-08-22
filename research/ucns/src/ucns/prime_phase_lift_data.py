# === MODULE_BUILD ===
# id: ucns_prime_phase_lift_data
#   module_name: prime_phase_lift_data
#   module_kind: experiment
#   summary: stores the exact P7 and P5 occurrence-turn, carrier-residue, node-generator, and projected-center ledgers consumed by the phase-and-lift witness
#   owner: Erin Spencer
#   public_surface: P7_TURNS, P5_TURNS, P7_CARRIER_RESIDUES, P5_CARRIER_RESIDUES, P7_NODE_GENERATORS, P5_NODE_GENERATORS, P7_CENTERS, P5_CENTERS
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_prime_phase_lift.py
#   rollout: exact static research ledger; selection effect none
#   rollback: remove with the complete prime phase-and-lift witness
#   requires: ucns_prime_primitives_p7_p5
#   since: 2026-08-11
#   unresolved: independently derived ledgers beyond the frozen P7/P5 construction
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: prime_phase_lift_data_covers_every_p7_p5_hypernode
#   given: the P7 and P5 phase-and-lift candidates consume their frozen ledgers
#   then: every primitive hypernode occurrence resolves to an exact carrier turn, residue lane, generator, and projected center
#   class: evidence
#   since: 2026-08-11
# === END CONTRACTS ===

# Exact occurrence, residue, generator, and center ledgers for the P7-first phase lift.

from fractions import Fraction

P7_TURNS = {'C': {'P7_N07': Fraction(0, 1),
       'P7_N10': Fraction(1, 6),
       'P7_N09': Fraction(1, 3),
       'P7_N05': Fraction(1, 2),
       'P7_N02': Fraction(2, 3),
       'P7_N03': Fraction(5, 6)},
 'R0': {'P7_N11': Fraction(1, 6),
        'P7_N10': Fraction(1, 3),
        'P7_N06': Fraction(1, 2),
        'P7_N03': Fraction(2, 3),
        'P7_N04': Fraction(5, 6)},
 'R1': {'P7_N11': Fraction(0, 1),
        'P7_N12': Fraction(1, 3),
        'P7_N09': Fraction(1, 2),
        'P7_N06': Fraction(2, 3),
        'P7_N07': Fraction(5, 6)},
 'R2': {'P7_N10': Fraction(0, 1),
        'P7_N12': Fraction(1, 6),
        'P7_N08': Fraction(1, 2),
        'P7_N05': Fraction(2, 3),
        'P7_N06': Fraction(5, 6)},
 'R3': {'P7_N06': Fraction(0, 1),
        'P7_N09': Fraction(1, 6),
        'P7_N08': Fraction(1, 3),
        'P7_N01': Fraction(2, 3),
        'P7_N02': Fraction(5, 6)},
 'R4': {'P7_N03': Fraction(0, 1),
        'P7_N06': Fraction(1, 6),
        'P7_N05': Fraction(1, 3),
        'P7_N01': Fraction(1, 2),
        'P7_N00': Fraction(5, 6)},
 'R5': {'P7_N04': Fraction(0, 1),
        'P7_N07': Fraction(1, 6),
        'P7_N06': Fraction(1, 3),
        'P7_N02': Fraction(1, 2),
        'P7_N00': Fraction(2, 3)}}

P5_TURNS = {'C': {'P5_N08': Fraction(1, 12),
       'P5_N10': Fraction(1, 6),
       'P5_N09': Fraction(1, 3),
       'P5_N07': Fraction(5, 12),
       'P5_N04': Fraction(7, 12),
       'P5_N02': Fraction(2, 3),
       'P5_N03': Fraction(5, 6),
       'P5_N05': Fraction(11, 12)},
 'R0': {'P5_N12': Fraction(1, 4),
        'P5_N10': Fraction(1, 3),
        'P5_N06': Fraction(1, 2),
        'P5_N03': Fraction(2, 3),
        'P5_N01': Fraction(3, 4)},
 'R1': {'P5_N12': Fraction(0, 1),
        'P5_N11': Fraction(1, 2),
        'P5_N07': Fraction(7, 12),
        'P5_N06': Fraction(3, 4),
        'P5_N08': Fraction(11, 12)},
 'R2': {'P5_N06': Fraction(0, 1),
        'P5_N09': Fraction(1, 6),
        'P5_N11': Fraction(1, 4),
        'P5_N00': Fraction(3, 4),
        'P5_N02': Fraction(5, 6)},
 'R3': {'P5_N01': Fraction(0, 1),
        'P5_N05': Fraction(1, 12),
        'P5_N06': Fraction(1, 4),
        'P5_N04': Fraction(5, 12),
        'P5_N00': Fraction(1, 2)}}

P7_CARRIER_RESIDUES = {'C': 0, 'R0': 1, 'R1': 3, 'R2': 2, 'R3': 6, 'R4': 4, 'R5': 5}

P5_CARRIER_RESIDUES = {'C': 0, 'R0': 1, 'R1': 2, 'R2': 4, 'R3': 3}

P7_NODE_GENERATORS = {'P7_N07': 1,
 'P7_N10': 3,
 'P7_N09': 2,
 'P7_N05': 6,
 'P7_N02': 4,
 'P7_N03': 5,
 'P7_N11': 1,
 'P7_N12': 3,
 'P7_N08': 2,
 'P7_N01': 6,
 'P7_N00': 4,
 'P7_N04': 5,
 'P7_N06': 1}

P5_NODE_GENERATORS = {'P5_N12': 1,
 'P5_N11': 2,
 'P5_N00': 4,
 'P5_N01': 3,
 'P5_N08': 1,
 'P5_N09': 2,
 'P5_N04': 4,
 'P5_N03': 3,
 'P5_N10': 1,
 'P5_N07': 2,
 'P5_N02': 4,
 'P5_N05': 3,
 'P5_N06': 1}

P7_CENTERS = {'C': (0.0, 0.0),
 'R0': (1.0, 0.0),
 'R1': (0.5, 0.8660254037844386),
 'R2': (-0.5, 0.8660254037844386),
 'R3': (-1.0, 0.0),
 'R4': (-0.5, -0.8660254037844386),
 'R5': (0.5, -0.8660254037844386)}

P5_CENTERS = {'C': (0.0, 0.0), 'R0': (1.0, 0.0), 'R1': (0.0, 1.0), 'R2': (-1.0, 0.0), 'R3': (0.0, -1.0)}
