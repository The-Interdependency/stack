import { defineMsdmdCollection } from "./.agents/skills/msdmd/collection";

export default defineMsdmdCollection({
  "declarations": [
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "the active ucns package facade is imported",
        "since": "2026-08-20",
        "then": "its declared public surface contains geometry only and removed lexical, semantic, EDCM, PTCNA, evaluator, and bridge modules are absent from the package tree"
      },
      "file": "src/ucns/__init__.py",
      "id": "geometry_public_surface_excludes_nongeometric_domains"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "facade",
        "module_name": "__init__",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "carrier geometry, framed Mobius root loop, exact Public Gonol carrier, Mobius vesica and seed geometry",
        "requires": "directed_carrier_floor, ucns_native_mobius_geometry, ucns_public_gonol_geometry, ucns_mobius_vesica_candidate, ucns_mobius_seed_of_life_candidate",
        "rollback": "restore prior facade from Git history",
        "rollout": "active geometry-only package facade",
        "since": "2026-08-20",
        "storage_boundary": "none",
        "summary": "geometry-only UCNS public surface",
        "tests": "tests.test_public_gonol, tests.test_geometry_public_surface, tests.test_carrier",
        "unresolved": "canonical completion of the full UCNS geometric construction",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/__init__.py",
      "id": "ucns_geometry_public_surface"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a non-null carrier retains structure while an external payload value is numerically zero",
        "since": "2026-07-21",
        "then": "carrier identity remains non-null because payload algebra is outside the carrier floor"
      },
      "file": "src/ucns/carrier.py",
      "id": "algebraic_zero_is_not_structural_null"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "any finite angular coordinate on a non-null carrier",
        "since": "2026-07-21",
        "then": "the coordinate is normalized modulo four pi and returns only after two visible laps"
      },
      "file": "src/ucns/carrier.py",
      "id": "lifted_period_is_720_degrees"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "a non-null lifted carrier point is constructed",
        "since": "2026-07-21",
        "then": "breadth is finite and strictly positive and radius lies strictly between zero and one"
      },
      "file": "src/ucns/carrier.py",
      "id": "non_null_carrier_has_positive_breadth"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a non-null lifted carrier point translated by two pi",
        "since": "2026-07-21",
        "then": "its visible projection is unchanged while its lifted representative is distinct"
      },
      "file": "src/ucns/carrier.py",
      "id": "one_visible_lap_is_deck_translation_only"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the carrier is constructed with zero faithful breadth",
        "since": "2026-07-21",
        "then": "the result is the unique Structural Null and exposes no angular coordinate"
      },
      "file": "src/ucns/carrier.py",
      "id": "structural_null_is_unique_and_coordinate_free"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a 360-degree deck translation",
        "since": "2026-07-21",
        "then": "no negation, reflection, parity, chirality, frame inversion, or payload operation is inferred by the carrier API"
      },
      "file": "src/ucns/carrier.py",
      "id": "topology_does_not_invent_orientation_algebra"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a non-null lifted carrier point translated twice by two pi",
        "since": "2026-07-21",
        "then": "the original lifted representative is restored"
      },
      "file": "src/ucns/carrier.py",
      "id": "two_visible_laps_complete_return"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a non-null lifted carrier point",
        "since": "2026-07-21",
        "then": "projection is normalized modulo two pi and has exactly two lifted representatives"
      },
      "file": "src/ucns/carrier.py",
      "id": "visible_projection_is_360_degrees"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_StructuralNull, _normalize_angle",
        "module_kind": "schema",
        "module_name": "carrier",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "STRUCTURAL_NULL, LiftedCarrierPoint, VisibleCarrierPoint, radius_from_breadth, carrier_from_breadth, project, deck_translate, lifted_preimages, same_lifted_position, same_visible_position",
        "requires": "canonical_chapter_one",
        "rollback": "remove public exports and this module",
        "rollout": "importable prototype only; no arithmetic or theorem promotion",
        "since": "2026-07-21",
        "storage_boundary": "none",
        "summary": "represents the directed twofold branched angular carrier without defining full UCNS object semantics",
        "tests": "tests/test_carrier.py",
        "unresolved": "canonical evaluators for mu, W, M, and B; complete UCNS object schema",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/carrier.py",
      "id": "directed_carrier_floor"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "an exact rational turn displacement is applied and then negated",
        "since": "2026-08-20",
        "then": "the complete framed state is restored exactly"
      },
      "file": "src/ucns/direct_mobius.py",
      "id": "native_mobius_motion_is_exactly_invertible"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "any framed Mobius state advances one full visible turn",
        "since": "2026-08-20",
        "then": "visible phase is unchanged and local frame is reversed"
      },
      "file": "src/ucns/direct_mobius.py",
      "id": "native_mobius_one_turn_reverses_frame"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "any framed Mobius state advances two full visible turns",
        "since": "2026-08-20",
        "then": "phase and local frame both return exactly"
      },
      "file": "src/ucns/direct_mobius.py",
      "id": "native_mobius_two_turns_restore_complete_state"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_coerce_turns",
        "module_kind": "geometry",
        "module_name": "direct_mobius",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "StructuralNullIdentity, STRUCTURAL_NULL_ORIGIN, NativeMobiusFrame, NativeMobiusState, native_mobius_state",
        "requires": "none",
        "rollback": "restore the prior mixed experiment module from Git history",
        "rollout": "geometry-only UCNS root-loop primitive",
        "since": "2026-08-20",
        "storage_boundary": "immutable exact rational state only",
        "summary": "exact framed Mobius root-loop quotient with 360-degree visible return and 720-degree complete return",
        "tests": "tests.test_direct_mobius",
        "unresolved": "attachment to higher-dimensional circle, epicycle, disk, sphere, and full gonol constructions",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/direct_mobius.py",
      "id": "ucns_native_mobius_geometry"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "the exact quarter-turn height equation is split into its two trigonometric branches",
        "since": "2026-08-10",
        "then": "the difference branch is rejected by the exact modulus contradiction two times radius not equal center separation"
      },
      "file": "src/ucns/mobius_certificates.py",
      "id": "mobius_vesica_alternate_height_branch_is_obstructed"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a machine receipt is serialized",
        "since": "2026-08-10",
        "then": "it records selection effect none and denies electron ontology, Pauli derivation, whole-surface classification, link proof, spectral correspondence, and Riemann-hypothesis proof"
      },
      "file": "src/ucns/mobius_certificates.py",
      "id": "mobius_vesica_certificate_is_nonselecting_and_zeta_firewalled"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a certificate is emitted",
        "since": "2026-08-10",
        "then": "physical boundary contacts, centerline contacts, projected crossings, and the unresolved full surface-intersection locus remain distinct fields"
      },
      "file": "src/ucns/mobius_certificates.py",
      "id": "mobius_vesica_contact_semantics_are_not_flattened"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "the normalized radius-one, separation-one, half-width-one-hundredth, opposite-chirality, quarter-turn dyad is constructed",
        "since": "2026-08-10",
        "then": "exact Sturm arithmetic proves two roots of the boundary-contact cubic in minus one to one and each root induces two distinct physical contacts, for exactly four"
      },
      "file": "src/ucns/mobius_certificates.py",
      "id": "mobius_vesica_sturm_proves_four_physical_boundary_contacts"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "rational polynomial arithmetic, branch obstruction, deterministic witness realization, payload hashing",
        "module_kind": "experiment",
        "module_name": "mobius_certificates",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "RationalInterval, SturmCertificate, BoundaryContactWitness, MobiusVesicaCertificate, sturm_sequence, count_real_roots, isolate_real_roots, certify_mobius_vesica, write_default_certificate",
        "requires": "ucns_mobius_vesica_exact_embedding",
        "rollback": "remove with mobius_vesica and mobius_continuation without changing the seven-band candidate",
        "rollout": "exact certificate for the normalized circular-ribbon quarter-turn family only; selection effect none",
        "since": "2026-08-10",
        "storage_boundary": "caller-supplied local paths only through write_default_certificate",
        "summary": "certifies the canonical Mobius Vesica centerline count, physical boundary-contact count, quotient return, null clearance, and proof firewall using exact rational Sturm arithmetic plus residual witnesses",
        "tests": "tests/test_mobius_vesica_exact.py",
        "unresolved": "full surface-pair intersection locus, general-phase classification, arbitrary-perturbation stability, linking, ambient isotopy, zeta operator",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/mobius_certificates.py",
      "id": "ucns_mobius_vesica_certificates"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "the standard circular family has opposite chirality, phase pair zero and one half, and width below one half",
        "since": "2026-08-10",
        "then": "exact branch equations admit zero physical boundary contacts"
      },
      "file": "src/ucns/mobius_continuation.py",
      "id": "mobius_vesica_half_turn_phase_has_exact_contact_obstruction"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the Seed-of-Life wheel relation graph is requested",
        "since": "2026-08-10",
        "then": "six center-to-ring and six adjacent-ring rigid placements are emitted, each preserving the local two-plus-four certificate in isolation"
      },
      "file": "src/ucns/mobius_continuation.py",
      "id": "mobius_vesica_rigid_placements_cover_seed_structural_pairs"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the exact quarter-turn dyad is compared with the current PR-174 half-turn first dyad",
        "since": "2026-08-10",
        "then": "chirality and width matches are retained, phase mismatch is explicit, and the four-contact certificate is not transferred"
      },
      "file": "src/ucns/mobius_continuation.py",
      "id": "mobius_vesica_seed_phase_mismatch_blocks_certificate_inheritance"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "a sequence of rational widths strictly between zero and one half is requested at quarter-turn phase",
        "since": "2026-08-10",
        "then": "every stage is independently Sturm-certified rather than inheriting a sampled contact count"
      },
      "file": "src/ucns/mobius_continuation.py",
      "id": "mobius_vesica_width_continuation_recertifies_each_stage"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "exact width stages, half-turn obstruction, rigid pair placement, deterministic combined receipt",
        "module_kind": "experiment",
        "module_name": "mobius_continuation",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "ContinuationStage, PhaseStage, SeedDyadComparison, VesicaPlacement, MobiusVesicaContinuationEngine, build_default_continuation_report, build_artifact_payload, write_default_artifact",
        "requires": "ucns_mobius_vesica_certificates, ucns_mobius_seed_of_life_candidate",
        "rollback": "remove with mobius_vesica and mobius_certificates",
        "rollout": "research continuation only; does not rewrite PR 174 phase law or select the seven-band candidate",
        "since": "2026-08-10",
        "storage_boundary": "caller-supplied local paths only through write_default_artifact",
        "summary": "continues the exact Mobius Vesica across rational widths, replicates it into the twelve rigid Seed-of-Life pair placements, and firewalls the quarter-turn certificate from the current half-turn seed phase",
        "tests": "tests/test_mobius_vesica_exact.py",
        "unresolved": "general phase classification, compatible seven-band global phase assignment, simultaneous twelve-pair realization, link invariants, spectral bridge",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/mobius_continuation.py",
      "id": "ucns_mobius_vesica_continuation"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "all six spokes are rigid copies while the center retains one chirality",
        "since": "2026-08-10",
        "then": "they demand six distinct center phases modulo one half turn"
      },
      "file": "src/ucns/mobius_global_compatibility.py",
      "id": "mobius_seed_center_needs_six_phase_channels_for_six_spokes"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the certificate is serialized",
        "since": "2026-08-10",
        "then": "selection effect is none and the obstruction remains bounded to its declared assumptions"
      },
      "file": "src/ucns/mobius_global_compatibility.py",
      "id": "mobius_seed_global_compatibility_certificate_is_nonselecting"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "two wheel-W7 structural pairs share a band and each is a rigid copy of the certified quarter-turn anti-chiral vesica",
        "since": "2026-08-10",
        "then": "all four orientation combinations demand different chirality-phase states at the shared band"
      },
      "file": "src/ucns/mobius_global_compatibility.py",
      "id": "mobius_seed_incident_certified_dyads_are_state_incompatible"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the same occurrences at one event are declared both physically equal and strictly height-separated",
        "since": "2026-08-10",
        "then": "delta-z equals zero contradicts delta-z nonzero"
      },
      "file": "src/ucns/mobius_global_compatibility.py",
      "id": "mobius_seed_physical_contact_and_strict_braid_are_event_exclusive"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the pinned PR-174 phase/chirality schedule is compared with both exact rigid-copy orientations",
        "since": "2026-08-10",
        "then": "zero of twelve structural pairs inherit the complete local certificate"
      },
      "file": "src/ucns/mobius_global_compatibility.py",
      "id": "mobius_seed_pr174_inherits_no_exact_rigid_vesica_pairs"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "each band has one chirality and one constant surface phase modulo one half turn",
        "since": "2026-08-10",
        "then": "compatible certified pairs form a matching and W7 has maximum matching size three"
      },
      "file": "src/ucns/mobius_global_compatibility.py",
      "id": "mobius_seed_single_state_certified_capacity_is_three"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "exact half-turn phase quotient, rigid-rotation transport, W7 cut and matching enumeration, pinned PR-174 comparison",
        "module_kind": "experiment",
        "module_name": "mobius_global_compatibility",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "EdgeOrientation, SurfacePhaseState, StructuralEdge, CertifiedEdgeCopy, CompatibilityBoundary, surface_phase, build_structural_edges, certified_edge_copies, pinned_pr174_assignment, edge_inherits_certificate, contact_and_strict_braid_compatible, prove_global_compatibility_boundary, write_global_compatibility_certificate",
        "requires": "ucns_mobius_vesica_continuation, ucns_mobius_seed_of_life_candidate",
        "rollback": "remove this module, its test, documentation, and generated certificate",
        "rollout": "stacked nonselecting UCNS obstruction certificate; does not alter PR 174 or PR 175",
        "since": "2026-08-10",
        "storage_boundary": "caller-supplied local path only",
        "summary": "proves the single-state phase/chirality capacity and contact-versus-braid boundary for assembling the certified Mobius Vesica across the twelve structural Seed-of-Life pairs",
        "tests": "tests/test_mobius_global_compatibility.py",
        "unresolved": "nonconstant phase fields, recursive or multichannel carriers, other local dyad families, simultaneous surface embedding, complete lift equations, spectral operator, zeta correspondence",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/mobius_global_compatibility.py",
      "id": "ucns_mobius_seed_global_compatibility"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a receipt or OBJ realization is emitted",
        "since": "2026-08-10",
        "then": "the artifact records selection effect none and explicitly denies zeta proof, electron ontology, Pauli-derived geometry, verified linking, and canonical UCNS completion"
      },
      "file": "src/ucns/mobius_seed.py",
      "id": "mobius_seed_candidate_is_nonselecting_and_proof_firewalled"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the default seven-band schedule is inspected",
        "since": "2026-08-10",
        "then": "the central band and first outer band have opposite chirality and half-turn seam displacement while the six outer seam phases advance by one twelfth turn"
      },
      "file": "src/ucns/mobius_seed.py",
      "id": "mobius_seed_dyad_is_anti_aligned_and_outer_phase_is_incremental"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "coincident projected occurrences are lifted into three dimensions",
        "since": "2026-08-10",
        "then": "every incident band has a distinct exact lift height, the six outer strands occupy nonzero one-two-three lane pairs at the center, and exact origin exclusion plus compactness preserves a positive three-dimensional void"
      },
      "file": "src/ucns/mobius_seed.py",
      "id": "mobius_seed_lift_preserves_null_as_nonvertex_void"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "the default Mobius Seed of Life candidate is constructed",
        "since": "2026-08-10",
        "then": "seven equal-radius operands, all twenty-one unordered pairs, thirteen unique projection nodes, twelve structural vesicas, six incidental secants, and three incidental tangencies are retained without hidden pair deletion"
      },
      "file": "src/ucns/mobius_seed.py",
      "id": "mobius_seed_projection_is_exact_and_pair_complete"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "either projected crossing of each structural vesica is inspected",
        "since": "2026-08-10",
        "then": "the exact lift-height difference is nonzero at both events and changes sign between them without claiming physical contact or a verified boundary-edge intersection"
      },
      "file": "src/ucns/mobius_seed.py",
      "id": "mobius_seed_structural_pairs_have_alternating_braid_order"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "any default band surface point is advanced one or two carrier turns",
        "since": "2026-08-10",
        "then": "one turn equals the seam-identified point at reversed breadth and two turns restore the complete sampled point"
      },
      "file": "src/ucns/mobius_seed.py",
      "id": "mobius_seed_surface_obeys_360_seam_and_720_return"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "exact sextant trigonometry, incidence construction, candidate validation, deterministic OBJ serialization",
        "module_kind": "experiment",
        "module_name": "mobius_seed",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "Qsqrt3, ExactPoint2, Point3, BandSlot, TwistChirality, PairStanding, NodeStanding, ProjectionNode, PairProjectionEvent, PairRelation, MobiusBandSpec, MobiusSeedOfLife, build_mobius_seed_of_life",
        "requires": "ucns_gonol_relationship_display_v1, edcm_native_direct_mobius_candidate",
        "rollback": "remove this module, its tests, and MOBIUS_SEED_OF_LIFE_V1 documents without altering arity-one, arity-two, or arity-three relationship-display primitives",
        "rollout": "explicit UCNS-only implemented candidate; selection effect none; no canonical seven-gonol composition, zeta proof, physical-model validation, EDCM activation, or METAPAT activation",
        "since": "2026-08-10",
        "storage_boundary": "caller-supplied local paths only through write_obj and write_receipt",
        "summary": "constructs the seven-band Mobius Seed of Life as an exact projection ledger plus a deterministic nonselecting three-dimensional braid-lift candidate",
        "tests": "tests/test_mobius_seed.py",
        "unresolved": "smooth boundary-edge intersection realization, pairwise linking matrix, ambient-isotopy lock proof, canonical seven-gonol composition, spectral operator, zeta-zero correspondence, proof-assistant formalization",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/mobius_seed.py",
      "id": "ucns_mobius_seed_of_life_candidate"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "the canonical equal-radius vesica embedding is constructed",
        "since": "2026-08-10",
        "then": "the two circular centerlines meet at exactly two exact points, zero plus or minus sqrt(3)/2 in the projection plane"
      },
      "file": "src/ucns/mobius_vesica.py",
      "id": "mobius_vesica_has_exact_two_centerline_contacts"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "radius one, center separation one, and half width one hundredth",
        "since": "2026-08-10",
        "then": "the origin is excluded from both individual bands by an exact lower clearance bound of forty-nine hundredths"
      },
      "file": "src/ucns/mobius_vesica.py",
      "id": "mobius_vesica_null_origin_has_positive_clearance"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "either band is evaluated at any admissible breadth",
        "since": "2026-08-10",
        "then": "one carrier turn reverses breadth under the quotient and two turns restore the full point"
      },
      "file": "src/ucns/mobius_vesica.py",
      "id": "mobius_vesica_obeys_one_turn_seam_and_two_turn_return"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the source note is used to define the dyad research target",
        "since": "2026-08-10",
        "then": "two centerline contacts and four physical continuous-boundary contacts remain explicit hypotheses to prove or falsify without being replaced by projected or abstract events"
      },
      "file": "src/ucns/mobius_vesica.py",
      "id": "mobius_vesica_preserves_source_claims_as_testable_geometry"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "exact vesica parameters, circular ribbon frame, quotient validation, boundary-contact polynomial",
        "module_kind": "experiment",
        "module_name": "mobius_vesica",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "VesicaBand, TwistChirality, Point3, CenterlineContact, MobiusBandEmbedding, MobiusVesicaParameters, MobiusVesica, build_mobius_vesica",
        "requires": "ucns_mobius_seed_of_life_candidate",
        "rollback": "remove this module, mobius_certificates, mobius_continuation, their tests, documentation, and generated receipt",
        "rollout": "UCNS-only exact candidate; selection effect none; does not alter the seven-band candidate or select a canonical zeta operator",
        "since": "2026-08-10",
        "storage_boundary": "none",
        "summary": "defines the canonical two-band Mobius Vesica Piscis embedding whose centerlines meet twice and whose single continuous boundaries admit an exact four-contact certificate",
        "tests": "tests/test_mobius_vesica_exact.py",
        "unresolved": "full pair-surface intersection set, arbitrary-perturbation stability, linking data, ambient-isotopy class, seven-band phase reconciliation, spectral operator, zeta correspondence",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/mobius_vesica.py",
      "id": "ucns_mobius_vesica_exact_embedding"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the frozen P7/P5 partition is replayed",
        "since": "2026-08-11",
        "then": "direct system MPFR is used instead of the primary mpmath interval backend and the pinned partition identities match"
      },
      "file": "src/ucns/mpfr_interval.py",
      "id": "prime_mpfr_replay_is_backend_independent"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "every frozen pair box is replayed with directed MPFR endpoints",
        "since": "2026-08-11",
        "then": "both prime candidates retain lower endpoints above the declared centerline margin"
      },
      "file": "src/ucns/mpfr_interval.py",
      "id": "prime_mpfr_replay_recertifies_ribbon_margin"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "ctypes MPFR bindings with explicit directed rounding modes",
        "module_kind": "experiment",
        "module_name": "mpfr_interval",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "MPNumber, MPInterval, mpfr_version, atan2_interval, flat_step_interval",
        "requires": "system libmpfr",
        "rollback": "remove with prime_independent_phase_milnor and its tests",
        "rollout": "independent interval backend only; certificate status does not transfer",
        "since": "2026-08-11",
        "storage_boundary": "none",
        "summary": "provides direct system-MPFR outward-rounded interval primitives for an independent P7/P5 separation replay",
        "tests": "tests/test_prime_independent_phase_milnor.py",
        "unresolved": "proof-assistant verification of the MPFR binding",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/mpfr_interval.py",
      "id": "ucns_mpfr_interval"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the owning facade invokes this readable helper",
        "since": "2026-08-11",
        "then": "the helper behavior is exercised through the named facade test without becoming a separate certificate"
      },
      "file": "src/ucns/prime_boundary_link_invariants.py",
      "id": "prime_boundary_helper_is_facade_witnessed"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "module implementation",
        "module_kind": "experiment",
        "module_name": "prime_boundary_link_invariants",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "internal readable implementation used through the declared facade",
        "requires": "ucns_prime_interval_boundary_links_p7_p5",
        "rollback": "remove only with the owning consolidated research layer",
        "rollout": "readable implementation; authority remains with the facade contracts",
        "since": "2026-08-11",
        "storage_boundary": "none",
        "summary": "readable exact boundary-component and integer linking invariant implementation",
        "tests": "tests/test_prime_interval_boundary_links.py",
        "unresolved": "see owning facade contracts and research document",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_boundary_link_invariants.py",
      "id": "ucns_prime_boundary_link_invariants"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the complete rational-Laurent determinantal generator family is accepted",
        "then": "component-variable saturation and exact lex reduction return a monic reduced basis for the complete ideal"
      },
      "file": "src/ucns/prime_determinantal_grobner.py",
      "id": "prime_grobner_basis_is_complete_reduced_and_saturated"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "P7 E1 or P5 E3 generators are constructed",
        "then": "every rank-size row/column subset pair is accounted for through the exact compound identity with no non-monomial denominator, and the frozen anchor, pivot-neighbor, and SHA-selected full minors agree under both direct determinant paths"
      },
      "file": "src/ucns/prime_determinantal_grobner.py",
      "id": "prime_grobner_generators_cover_every_maximal_minor"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "regression",
        "given": "primary and independent computations finish within frozen bounds",
        "then": "generator digests, mutual reductions, and canonical reduced basis maps agree exactly"
      },
      "file": "src/ucns/prime_determinantal_grobner.py",
      "id": "prime_grobner_independent_replay_agrees"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a determinantal basis computation begins",
        "then": "the committed preregistration bytes have the frozen SHA-256 identity and the parent presentation digest matches"
      },
      "file": "src/ucns/prime_determinantal_grobner.py",
      "id": "prime_grobner_protocol_identity_is_frozen"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the family receipt is serialized",
        "then": "rational ideal evidence does not escalate phase, isotopy, prime-forcing, spectral, zeta, or theorem standing"
      },
      "file": "src/ucns/prime_determinantal_grobner.py",
      "id": "prime_grobner_receipt_preserves_nonclaims"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "compound maximal-minor coordinates, frozen direct full-minor audit, Laurent normalization, saturation, exact reduced lex bases, independent Buchberger replay",
        "module_kind": "experiment",
        "module_name": "prime_determinantal_grobner",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "determinantal_grobner_certificate, determinantal_grobner_family_certificate, write_determinantal_grobner_family_certificate",
        "requires": "ucns_prime_symbolic_alexander_p7_p5, sympy==1.14.0",
        "rollback": "remove this module, its tests, result document, and generated receipt while retaining preregistration and prior rank/onset evidence",
        "rollout": "protocol 7841af16; P7 first and P5 second; selection effect none",
        "since": "2026-08-15",
        "storage_boundary": "caller-supplied local paths only through writer functions",
        "summary": "executes the preregistered complete rational-Laurent determinantal-ideal Groebner protocol for the frozen P7 and P5 Fox matrices",
        "tests": "tests/test_prime_determinantal_grobner.py",
        "unresolved": "integral-Laurent strong bases, length-four Milnor invariants, finite nilpotent quotients, preregistered phase-co-winner separator",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_determinantal_grobner.py",
      "id": "ucns_prime_determinantal_grobner_p7_p5"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the family certificate is serialized",
        "since": "2026-08-11",
        "then": "it claims no arithmetic redefinition, electron ontology, zeta theorem, or Riemann-hypothesis proof"
      },
      "file": "src/ucns/prime_exact_milnor_alexander.py",
      "id": "prime_exact_milnor_alexander_receipt_is_nonselecting"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a P7 or P5 whole-link fingerprint is issued",
        "since": "2026-08-11",
        "then": "every distinct phase-induced prime character has a rank and excess-nullity value committed by SHA-256"
      },
      "file": "src/ucns/prime_exact_milnor_alexander.py",
      "id": "prime_fox_fingerprint_covers_all_prime_characters"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the P7 or P5 diagram is constructed",
        "since": "2026-08-11",
        "then": "every component uses the preregistered rational planar translation and the straight-line isotopy remains inside the prior seven-hundredths ribbon clearance"
      },
      "file": "src/ucns/prime_exact_milnor_alexander.py",
      "id": "prime_generic_diagram_is_fixed_before_invariants"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "all generic double crossings are signed",
        "since": "2026-08-11",
        "then": "their half-sums reproduce the previously certified complete P7 and P5 pairwise linking matrices"
      },
      "file": "src/ucns/prime_exact_milnor_alexander.py",
      "id": "prime_generic_diagram_preserves_pairwise_linking"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "the closure of the braid sigma-one sigma-two-inverse cubed is evaluated",
        "since": "2026-08-11",
        "then": "the degree-two preferred-longitude Magnus coefficient has absolute value one"
      },
      "file": "src/ucns/prime_exact_milnor_alexander.py",
      "id": "prime_magnus_benchmark_recovers_borromean_integer"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the five pairwise-zero P7 triples are evaluated in the fixed generic diagram",
        "since": "2026-08-11",
        "then": "every degree-two Magnus coefficient is exactly the integer zero"
      },
      "file": "src/ucns/prime_exact_milnor_alexander.py",
      "id": "prime_p7_five_milnor_candidates_are_exact_zero_in_diagram"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the phase selector is evaluated",
        "since": "2026-08-11",
        "then": "its document hash equals the preregistered hash and no post-evaluation criterion is added"
      },
      "file": "src/ucns/prime_exact_milnor_alexander.py",
      "id": "prime_phase_selector_matches_frozen_preregistration"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "an admissible phase law is scored",
        "since": "2026-08-11",
        "then": "the score uses maximum phase gap, finite-field Fox-Alexander excess nullity, and exact phase-lift alignment energy before neutral tie breakers"
      },
      "file": "src/ucns/prime_exact_milnor_alexander.py",
      "id": "prime_phase_selector_uses_whole_link_character"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "fixed planar translations, high-precision circle intersections, Wirtinger arcs, degree-two Magnus algebra, finite-field Fox derivatives, exact rational phase-lift energy",
        "module_kind": "experiment",
        "module_name": "prime_exact_milnor_alexander",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "DiagramCrossing, GenericLinkDiagram, MilnorIntegerCertificate, FoxRankFingerprint, PhaseSelectorResult, build_generic_prime_seven_diagram, build_generic_prime_five_diagram, exact_p7_milnor_certificates, fox_rank_fingerprint, common_field_fox_rank_fingerprint, evaluate_preregistered_phase_selector, exact_milnor_alexander_family_certificate, write_exact_milnor_alexander_family_certificate",
        "requires": "ucns_prime_independent_phase_milnor_p7_p5, mpmath>=1.3",
        "rollback": "remove this module, its tests, documentation, preregistration, and generated certificate",
        "rollout": "P7 first, P5 same-protocol comparison second; preregistration SHA-256 frozen before evaluation; selection effect none",
        "since": "2026-08-11",
        "storage_boundary": "caller-supplied local paths only through writer functions",
        "summary": "generically resolves the P7/P5 centerline diagrams, replaces the five numerical Milnor-zero candidates with exact degree-two Magnus coefficients, freezes and evaluates a prime-character Fox-Alexander phase selector, and issues whole-link rank fingerprints",
        "tests": "tests/test_prime_exact_milnor_alexander.py",
        "unresolved": "proof-assistant replay of diagram signs, full multivariable Alexander polynomial, ambient-isotopy classification, higher Milnor invariants, spectral operator, prime-power law, zeta correspondence",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_exact_milnor_alexander.py",
      "id": "ucns_prime_exact_milnor_alexander_p7_p5"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the owning facade invokes this readable helper",
        "since": "2026-08-11",
        "then": "the helper behavior is exercised through the named facade test without becoming a separate certificate"
      },
      "file": "src/ucns/prime_generic_diagram.py",
      "id": "prime_generic_helper_is_facade_witnessed"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "module implementation",
        "module_kind": "experiment",
        "module_name": "prime_generic_diagram",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "internal readable implementation used through the declared facade",
        "requires": "ucns_prime_interval_boundary_links_p7_p5",
        "rollback": "remove only with the owning consolidated research layer",
        "rollout": "readable implementation; authority remains with the facade contracts",
        "since": "2026-08-11",
        "storage_boundary": "none",
        "summary": "readable clearance-preserving generic diagram implementation",
        "tests": "tests/test_prime_interval_boundary_links.py",
        "unresolved": "see owning facade contracts and research document",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_generic_diagram.py",
      "id": "ucns_prime_generic_diagram"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "every reconstructed crossing has interval-certified height ordering and tangent determinant",
        "since": "2026-08-15",
        "then": "all P7-first and P5-second crossing signs agree with the frozen generic diagrams"
      },
      "file": "src/ucns/prime_generic_interval_certificate.py",
      "id": "prime_generic_crossing_signs_are_interval_certified"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the family certificate is serialized",
        "since": "2026-08-15",
        "then": "it retains method, backend, complete crossing coverage, source identities, information boundary, and selection effect none"
      },
      "file": "src/ucns/prime_generic_interval_certificate.py",
      "id": "prime_generic_interval_receipt_is_nonselecting"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "each incident turn interval lies within one declared smooth-field segment",
        "since": "2026-08-15",
        "then": "the complete smooth-field interval difference excludes zero and agrees with the frozen over-under ordering"
      },
      "file": "src/ucns/prime_generic_interval_certificate.py",
      "id": "prime_generic_smooth_signs_are_interval_certified"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "every frozen P7/P5 generic equal-circle crossing is reconstructed",
        "since": "2026-08-15",
        "then": "direct system MPFR encloses both incident turns through directed-rounded atan2 without a branch-cut ambiguity"
      },
      "file": "src/ucns/prime_generic_interval_certificate.py",
      "id": "prime_generic_turns_are_outward_atan2_enclosed"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "shifted-center, equal-circle intersection, turn, smooth-field, and transversality interval construction",
        "module_kind": "experiment",
        "module_name": "prime_generic_interval_certificate",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "GenericIntervalCrossingCertificate, GenericIntervalDiagramCertificate, certify_generic_prime_diagram, generic_interval_family_certificate, write_generic_interval_family_certificate",
        "requires": "ucns_mpfr_interval, ucns_prime_exact_milnor_alexander_p7_p5",
        "rollback": "remove this module, its tests, document, and generated certificate",
        "rollout": "nonselecting certificate over the already frozen P7/P5 generic diagrams",
        "since": "2026-08-15",
        "storage_boundary": "caller-supplied local paths only through the writer function",
        "summary": "independently replays the frozen P7/P5 generic crossing diagram with outward-rounded MPFR atan2 and smooth-field intervals",
        "tests": "tests/test_prime_generic_interval_certificate.py",
        "unresolved": "proof-assistant replay and symbolic validation of every interval primitive",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_generic_interval_certificate.py",
      "id": "ucns_prime_generic_interval_certificate"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "independent replay findings are summarized",
        "since": "2026-08-11",
        "then": "negative and numerical results retain explicit nonclaims"
      },
      "file": "src/ucns/prime_independent_phase_milnor.py",
      "id": "prime_independent_phase_milnor_receipt_is_nonselecting"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "numerical estimates resolve near integers",
        "since": "2026-08-11",
        "then": "numerical resolution is not represented as an exact theorem"
      },
      "file": "src/ucns/prime_independent_phase_milnor.py",
      "id": "prime_milnor_exactness_boundary_is_preserved"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the numerical Fourier extractor is benchmarked",
        "since": "2026-08-11",
        "then": "it converges to the declared Borromean value under the recorded convention"
      },
      "file": "src/ucns/prime_independent_phase_milnor.py",
      "id": "prime_milnor_fourier_benchmark_recovers_borromean"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the five split P7 triples are evaluated across increasing resolutions",
        "since": "2026-08-11",
        "then": "every estimate converges numerically toward zero"
      },
      "file": "src/ucns/prime_independent_phase_milnor.py",
      "id": "prime_milnor_p7_split_triples_resolve_numerically_to_zero"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "every equal-gap phase alternative is enumerated",
        "since": "2026-08-11",
        "then": "the selected winding is identified without treating it as prime-specific emergence"
      },
      "file": "src/ucns/prime_independent_phase_milnor.py",
      "id": "prime_phase_sensitivity_separates_selection_from_emergence"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "falsifier",
        "given": "P7 and P5 maximum-gap candidates are compared",
        "since": "2026-08-11",
        "then": "their shared knot-degree alternatives preserve the negative result that T two-seven is not forced by prime alone"
      },
      "file": "src/ucns/prime_independent_phase_milnor.py",
      "id": "prime_phase_sensitivity_torus_seven_is_not_forced"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "zlib-compressed byte-exact validated readable implementation",
        "module_kind": "experiment",
        "module_name": "prime_independent_phase_milnor",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "independent MPFR replay, phase sensitivity report, Fourier Milnor estimate, P7 triple resolution",
        "requires": "ucns_mpfr_interval, ucns_prime_smooth_ribbons_p7_p5",
        "rollback": "remove with its tests and independent research documents",
        "rollout": "independent replay and negative-result evidence; numerical extraction is not promoted to exact computation",
        "since": "2026-08-11",
        "storage_boundary": "none",
        "summary": "compact executable representation of the independent interval replay, phase sensitivity, and numerical Milnor extraction",
        "tests": "tests/test_prime_independent_phase_milnor.py",
        "unresolved": "analytic proof of all numerical zero resolutions",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_independent_phase_milnor.py",
      "id": "ucns_prime_independent_phase_milnor"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "the selected phase law is evaluated over the two-turn boundary traversal",
        "since": "2026-08-11",
        "then": "the center boundary has cable class two-seven and each outer boundary has cable class two-one in the declared framing"
      },
      "file": "src/ucns/prime_interval_boundaries.py",
      "id": "prime_boundary_cable_winding_is_derived_from_phase"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "one finite-width M\u00f6bius ribbon is restricted to positive half-width",
        "since": "2026-08-11",
        "then": "its boundary closes only after two carrier turns and retracts with longitudinal degree two"
      },
      "file": "src/ucns/prime_interval_boundaries.py",
      "id": "prime_boundary_curve_is_single_two_turn_component"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "boundary components retract to degree-two traversals of their cores inside pairwise-disjoint ribbons",
        "since": "2026-08-11",
        "then": "every inter-ribbon boundary linking number is four times the corresponding core linking number"
      },
      "file": "src/ucns/prime_interval_boundaries.py",
      "id": "prime_boundary_linking_scales_by_four"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "triples of boundary components are classified by pairwise support",
        "since": "2026-08-11",
        "then": "algebraically split triples are enumerated while Milnor and complete-link invariants remain explicitly unresolved"
      },
      "file": "src/ucns/prime_interval_boundaries.py",
      "id": "prime_higher_order_boundary_is_explicit"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the family certificate is built",
        "since": "2026-08-11",
        "then": "P7 interval and boundary invariants are completed before the same protocol is applied independently to P5"
      },
      "file": "src/ucns/prime_interval_boundaries.py",
      "id": "prime_interval_boundaries_p7_precedes_p5"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the family receipt is serialized",
        "since": "2026-08-11",
        "then": "it records the interval-kernel boundary and claims no arithmetic redefinition, electron ontology, zeta theorem, or Riemann-hypothesis proof"
      },
      "file": "src/ucns/prime_interval_boundaries.py",
      "id": "prime_interval_boundary_compact_receipt_is_nonselecting"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "every complete pair-parameter torus is recursively covered",
        "since": "2026-08-11",
        "then": "high-precision interval point values and interval speed majorants certify the same nine-hundredths centerline target without a binary64 subtraction heuristic"
      },
      "file": "src/ucns/prime_interval_boundaries.py",
      "id": "prime_interval_replay_uses_outward_endpoints"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "core-core, core-boundary, and boundary-boundary linking laws are combined",
        "since": "2026-08-11",
        "then": "a complete two-p by two-p integer matrix and exact rank and determinant are issued"
      },
      "file": "src/ucns/prime_interval_boundaries.py",
      "id": "prime_mixed_core_boundary_matrix_is_complete"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "recovered legacy types and payloads over readable PR 181 interval and boundary certificates",
        "module_kind": "experiment",
        "module_name": "prime_interval_boundaries",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "IntervalPairReplay, IntervalReplayCertificate, BoundaryComponentCertificate, BoundaryInvariantCertificate, replay_prime_seven_intervals, replay_prime_five_intervals, certify_prime_seven_boundaries, certify_prime_five_boundaries, interval_boundary_family_certificate, write_interval_boundary_family_certificate, render_boundary_obj, render_core_boundary_obj",
        "requires": "ucns_prime_smooth_ribbons_p7_p5, mpmath>=1.3",
        "rollback": "remove this module, its test, documentation, generated certificate, and boundary exports",
        "rollout": "P7 first, P5 same-protocol comparison second; selection effect none; does not alter prior smooth-ribbon receipts",
        "since": "2026-08-11",
        "storage_boundary": "caller-supplied local paths only through writer functions",
        "summary": "replays the P7-first smooth-ribbon separation certificate with outward interval endpoints, extracts each M\u00f6bius strip's single two-turn boundary curve, and derives exact boundary-cable and mixed core-boundary invariants before P5 comparison",
        "tests": "tests/test_prime_interval_boundaries.py",
        "unresolved": "independently verified interval kernel, proof-assistant replay, Milnor invariants of algebraically split triples, multivariable Alexander polynomial of the complete boundary link, ambient isotopy, spectral operator, prime-power law, zeta correspondence",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_interval_boundaries.py",
      "id": "ucns_prime_interval_boundaries_p7_p5"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "each centerline is a vertical graph over a circle and hence an unknot",
        "since": "2026-08-11",
        "then": "each boundary component is assigned its exact two-by-odd torus-cable type and Alexander, genus, determinant, and crossing-number readouts"
      },
      "file": "src/ucns/prime_interval_boundary_links.py",
      "id": "prime_boundary_component_knot_types_are_derived"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "one M\u00f6bius ribbon is evaluated at positive boundary breadth over two carrier turns",
        "since": "2026-08-11",
        "then": "it yields one closed boundary component with longitudinal winding two and odd meridional winding one plus twice the phase winding"
      },
      "file": "src/ucns/prime_interval_boundary_links.py",
      "id": "prime_boundary_curve_is_single_and_closed"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "distinct boundary components each carry longitudinal coefficient two",
        "since": "2026-08-11",
        "then": "their pairwise linking matrix equals four times the core linking matrix and the mixed core-boundary off-diagonal block equals twice the core matrix"
      },
      "file": "src/ucns/prime_interval_boundary_links.py",
      "id": "prime_boundary_linking_matrix_follows_cable_homology"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the family certificate is built",
        "since": "2026-08-11",
        "then": "P7 is interval-certified and analyzed first and P5 is independently processed second"
      },
      "file": "src/ucns/prime_interval_boundary_links.py",
      "id": "prime_interval_boundary_p7_precedes_p5"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the family receipt is serialized",
        "since": "2026-08-11",
        "then": "it records dependency, precision, generic-projection, and invariant boundaries and claims no arithmetic redefinition, electron ontology, zeta theorem, or Riemann-hypothesis proof"
      },
      "file": "src/ucns/prime_interval_boundary_links.py",
      "id": "prime_interval_boundary_receipt_is_nonselecting"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "every complete P7 or P5 pair-parameter torus is replayed",
        "since": "2026-08-11",
        "then": "elementary evaluations use directed interval endpoints and every accepted leaf has a rigorous lower endpoint strictly above nine hundredths at the declared precision"
      },
      "file": "src/ucns/prime_interval_boundary_links.py",
      "id": "prime_interval_replay_is_outward_rounded"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "interval centerline clearance exceeds nine hundredths and half width is one hundredth",
        "since": "2026-08-11",
        "then": "all distinct complete ribbons remain separated by more than seven hundredths"
      },
      "file": "src/ucns/prime_interval_boundary_links.py",
      "id": "prime_interval_replay_preserves_finite_width_disjointness"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a clearance-preserving simultaneous generic projection is constructed",
        "since": "2026-08-11",
        "then": "pairwise linking is unchanged and every integer-valued length-three Milnor invariant is computed by a truncated Magnus expansion validated on the Borromean braid"
      },
      "file": "src/ucns/prime_interval_boundary_links.py",
      "id": "prime_length_three_milnor_profile_is_computed_after_global_lift"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "core, boundary, and own-core boundary linkings are combined",
        "since": "2026-08-11",
        "then": "rank, nullity, determinant, factorization, and Smith invariant factors are computed over the integers"
      },
      "file": "src/ucns/prime_interval_boundary_links.py",
      "id": "prime_mixed_linking_matrix_has_exact_integer_invariants"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "prime_interval_common, prime_interval_replay, prime_boundary_link_invariants, prime_generic_diagram, prime_milnor_invariants",
        "module_kind": "experiment",
        "module_name": "prime_interval_boundary_links",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "IntervalPairCertificate, IntervalSeparationCertificate, BoundaryComponentInvariant, IntegerMatrixInvariant, BoundaryLinkCertificate, DiagramCrossing, GenericCoreDiagram, MilnorTripleInvariant, MilnorProfile, IntervalBoundaryCertificate, replay_interval_separation, extract_boundary_components, build_boundary_link_certificate, build_generic_core_diagram, compute_milnor_profile, certify_interval_boundary_prime_seven, certify_interval_boundary_prime_five, interval_boundary_family_certificate, interval_boundary_family_summary, write_interval_boundary_family_certificate, write_interval_boundary_family_summary, render_boundary_curve_obj",
        "requires": "ucns_prime_smooth_ribbons_p7_p5",
        "rollback": "remove this facade and its five helper modules, test, documentation, generated certificate, and boundary models; revert the research/test optional dependencies",
        "rollout": "P7 first, P5 same-protocol comparison second; selection effect none; does not alter prior smooth-ribbon receipts",
        "since": "2026-08-11",
        "storage_boundary": "caller-supplied local paths only through writer and renderer functions",
        "summary": "replays P7-first smooth-ribbon separation with outward-rounded interval arithmetic, extracts each M\u00f6bius ribbon's single continuous boundary, and computes boundary, mixed, component-knot, and length-three Milnor readouts before any spectral construction",
        "tests": "tests/test_prime_interval_boundary_links.py",
        "unresolved": "proof-assistant replay, simultaneous global projection regularization, length-four-and-higher Milnor invariants, whole-link ambient isotopy, multivariable Alexander or HOMFLYPT invariants, spectral operator, prime-power law, zeta correspondence",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_interval_boundary_links.py",
      "id": "ucns_prime_interval_boundary_links_p7_p5"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the owning facade invokes this readable helper",
        "since": "2026-08-11",
        "then": "the helper behavior is exercised through the named facade test without becoming a separate certificate"
      },
      "file": "src/ucns/prime_interval_common.py",
      "id": "prime_interval_common_is_facade_witnessed"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "module implementation",
        "module_kind": "experiment",
        "module_name": "prime_interval_common",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "internal readable implementation used through the declared facade",
        "requires": "ucns_prime_smooth_ribbons_p7_p5",
        "rollback": "remove only with the owning consolidated research layer",
        "rollout": "readable implementation; authority remains with the facade contracts",
        "since": "2026-08-11",
        "storage_boundary": "none",
        "summary": "shared constants and dependency guards for readable interval and boundary research",
        "tests": "tests/test_prime_interval_boundary_links.py",
        "unresolved": "see owning facade contracts and research document",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_interval_common.py",
      "id": "ucns_prime_interval_common"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the owning facade invokes this readable helper",
        "since": "2026-08-11",
        "then": "the helper behavior is exercised through the named facade test without becoming a separate certificate"
      },
      "file": "src/ucns/prime_interval_replay.py",
      "id": "prime_interval_replay_helper_is_facade_witnessed"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "module implementation",
        "module_kind": "experiment",
        "module_name": "prime_interval_replay",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "internal readable implementation used through the declared facade",
        "requires": "ucns_prime_interval_common",
        "rollback": "remove only with the owning consolidated research layer",
        "rollout": "readable implementation; authority remains with the facade contracts",
        "since": "2026-08-11",
        "storage_boundary": "none",
        "summary": "readable outward-directed interval replay implementation",
        "tests": "tests/test_prime_interval_boundary_links.py",
        "unresolved": "see owning facade contracts and research document",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_interval_replay.py",
      "id": "ucns_prime_interval_replay"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "the degree-three Magnus engine evaluates [[x1,x2],x3]",
        "since": "2026-08-15",
        "then": "the four frozen degree-three coefficients and every lower degree coefficient match the preregistration"
      },
      "file": "src/ucns/prime_length4_milnor.py",
      "id": "prime_length4_magnus_gate_matches_frozen_commutator"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the result is serialized",
        "since": "2026-08-15",
        "then": "it preserves computer-assisted diagram standing and makes no isotopy-classification, phase, spectral, zeta, or theorem-status claim"
      },
      "file": "src/ucns/prime_length4_milnor.py",
      "id": "prime_p7_length4_receipt_is_bounded"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the frozen target passes its lower-order gates",
        "since": "2026-08-15",
        "then": "the canonical, reverse-word, and four cyclic-rotation coefficients are retained without changing the primary target"
      },
      "file": "src/ucns/prime_length4_milnor.py",
      "id": "prime_p7_length4_result_records_cyclic_conventions"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the minimal P7 length-four experiment is evaluated",
        "since": "2026-08-15",
        "then": "only R0,R1,R4,R5 is targeted and all six linking, four triple-Milnor, and required longitude lower-degree gates are exact zero"
      },
      "file": "src/ucns/prime_length4_milnor.py",
      "id": "prime_p7_length4_target_is_frozen_and_lower_gated"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "degree-three noncommutative series, fixed-diagram Wirtinger longitude replay",
        "module_kind": "experiment",
        "module_name": "prime_length4_milnor",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "LengthFourMilnorCertificate, length_four_commutator_gate, evaluate_p7_length_four_milnor, write_p7_length_four_milnor_certificate",
        "requires": "ucns_prime_exact_milnor_alexander_p7_p5",
        "rollback": "remove this module, its tests, result document, and generated certificate",
        "rollout": "frozen ordered target R0,R1,R4,R5 only; accept nonzero, zero, or unresolved without retargeting",
        "since": "2026-08-15",
        "storage_boundary": "caller-supplied local paths only through writer function",
        "summary": "evaluates the frozen minimal P7 length-four Milnor experiment with exact degree-three Magnus arithmetic",
        "tests": "tests/test_prime_length4_milnor.py",
        "unresolved": "repeated-index Milnor invariants, higher nilpotent quotients, whole-link length-four program",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_length4_milnor.py",
      "id": "ucns_prime_length4_milnor_p7"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the owning facade invokes this readable helper",
        "since": "2026-08-11",
        "then": "the helper behavior is exercised through the named facade test without becoming a separate certificate"
      },
      "file": "src/ucns/prime_milnor_invariants.py",
      "id": "prime_milnor_helper_is_facade_witnessed"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "module implementation",
        "module_kind": "experiment",
        "module_name": "prime_milnor_invariants",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "internal readable implementation used through the declared facade",
        "requires": "ucns_prime_generic_diagram",
        "rollback": "remove only with the owning consolidated research layer",
        "rollout": "readable implementation; authority remains with the facade contracts",
        "since": "2026-08-11",
        "storage_boundary": "none",
        "summary": "readable length-three Milnor extraction and benchmark implementation",
        "tests": "tests/test_prime_interval_boundary_links.py",
        "unresolved": "see owning facade contracts and research document",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_milnor_invariants.py",
      "id": "ucns_prime_milnor_invariants"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "P7 and P5 higher signatures are compared",
        "since": "2026-08-15",
        "then": "component count and weight-one rank alone cannot produce distinguish"
      },
      "file": "src/ucns/prime_nilpotent_discriminator.py",
      "id": "prime_nilpotent_comparison_excludes_known_rank"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "substantive phase co-winners bind identical group and peripheral inputs",
        "since": "2026-08-15",
        "then": "their nilpotent comparison is no-distinguish"
      },
      "file": "src/ucns/prime_nilpotent_discriminator.py",
      "id": "prime_nilpotent_phase_binding_is_topological"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "GAP/NQ emits a class-four marked quotient",
        "since": "2026-08-15",
        "then": "exact degree-four Magnus replay reconstructs every marked meridian and longitude from NQ pc-generator preimages"
      },
      "file": "src/ucns/prime_nilpotent_discriminator.py",
      "id": "prime_nilpotent_primary_and_replay_agree"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a quotient computation starts",
        "since": "2026-08-15",
        "then": "the preregistration SHA-256, class four, backend versions, component orders, and resource bounds match PR 191"
      },
      "file": "src/ucns/prime_nilpotent_discriminator.py",
      "id": "prime_nilpotent_protocol_identity_is_frozen"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "deterministic GAP/NQ script, exact degree-four Magnus replay, frozen higher-signature comparison",
        "module_kind": "experiment",
        "module_name": "prime_nilpotent_discriminator",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "compute_nilpotent_discriminator, write_nilpotent_discriminator_receipt",
        "requires": "ucns_prime_exact_milnor_alexander_p7_p5, GAP 4.12.1, NQ 2.5.11",
        "rollback": "remove this module, tests, result document, and generated receipt",
        "rollout": "protocol ffaecb935e8086200fa9a27c5d55ba6e759721107d8c4979049eed760eae8aee; P7 then P5 then phase bindings",
        "since": "2026-08-15",
        "storage_boundary": "caller-supplied local output path and private temporary GAP script",
        "summary": "computes the frozen class-four marked peripheral nilpotent quotients for the complete P7 and P5 core links",
        "tests": "tests/test_prime_nilpotent_discriminator.py",
        "unresolved": "classes above four, repeated-index classification, ambient isotopy",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_nilpotent_discriminator.py",
      "id": "ucns_prime_nilpotent_discriminator_p7_p5"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "the complete projected pair-event ledger",
        "since": "2026-08-11",
        "then": "every projected coincidence has nonzero height separation"
      },
      "file": "src/ucns/prime_phase_lift.py",
      "id": "prime_phase_lift_centerlines_are_disjoint"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the phase-lift family is built",
        "since": "2026-08-11",
        "then": "P7 is solved globally on seven carriers and thirteen hypernodes before pair or triad readouts"
      },
      "file": "src/ucns/prime_phase_lift.py",
      "id": "prime_phase_lift_constructs_p7_before_restrictions"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "a carrier surface is evaluated",
        "since": "2026-08-11",
        "then": "one turn reverses breadth and two turns return the same point"
      },
      "file": "src/ucns/prime_phase_lift.py",
      "id": "prime_phase_lift_is_seam_compatible"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a pair has a regular two-crossing projection",
        "since": "2026-08-11",
        "then": "linking number is computed only after the global lift is fixed"
      },
      "file": "src/ucns/prime_phase_lift.py",
      "id": "prime_phase_lift_link_numbers_are_derived"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "P7 is complete",
        "since": "2026-08-11",
        "then": "P5 is solved independently by the same protocol"
      },
      "file": "src/ucns/prime_phase_lift.py",
      "id": "prime_phase_lift_p5_follows_same_protocol"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the P7 origin is evaluated",
        "since": "2026-08-11",
        "then": "it remains one arity-six hypernode with six nonzero lanes and fifteen derived pair comparisons"
      },
      "file": "src/ucns/prime_phase_lift.py",
      "id": "prime_phase_lift_preserves_nary_origin"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the family receipt is serialized",
        "since": "2026-08-11",
        "then": "it claims no arithmetic redefinition, electron ontology, zeta theorem, or proof of the Riemann hypothesis"
      },
      "file": "src/ucns/prime_phase_lift.py",
      "id": "prime_phase_lift_receipt_is_nonselecting"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "any P7 or P5 hypernode",
        "since": "2026-08-11",
        "then": "every occurrence has a distinct exact phase and lift lane"
      },
      "file": "src/ucns/prime_phase_lift.py",
      "id": "prime_phase_lift_resolves_every_hypernode"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "exact phase-law search, finite-field lane assignment, deterministic certificate serialization",
        "module_kind": "experiment",
        "module_name": "prime_phase_lift",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "EventSemantic, PhaseLaw, LiftOccurrence, LiftHypernode, PairLinkReadout, PrimePhaseLiftCandidate, select_phase_law, build_prime_seven_phase_lift, build_prime_five_phase_lift, phase_lift_family_certificate, write_phase_lift_family_certificate",
        "requires": "ucns_prime_primitives_p7_p5",
        "rollback": "remove this module with prime_phase_lift_data, prime_phase_lift_model, their test, document, and generated certificate",
        "rollout": "nonselecting P7-first witness; pair and triad readouts follow the global solution",
        "since": "2026-08-11",
        "storage_boundary": "caller-supplied local path only through write_phase_lift_family_certificate",
        "summary": "solves P7 globally with an exact seam-compatible phase law and finite-field lift over all thirteen hypernodes, then applies the same protocol independently to P5",
        "tests": "tests/test_prime_phase_lift.py",
        "unresolved": "smooth lift replacement, whole-ribbon disjointness, tangent regularization, boundary topology, ambient isotopy, spectral operator, zeta correspondence",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_phase_lift.py",
      "id": "ucns_prime_phase_lift_p7_p5"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the P7 and P5 phase-and-lift candidates consume their frozen ledgers",
        "since": "2026-08-11",
        "then": "every primitive hypernode occurrence resolves to an exact carrier turn, residue lane, generator, and projected center"
      },
      "file": "src/ucns/prime_phase_lift_data.py",
      "id": "prime_phase_lift_data_covers_every_p7_p5_hypernode"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "experiment",
        "module_name": "prime_phase_lift_data",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "P7_TURNS, P5_TURNS, P7_CARRIER_RESIDUES, P5_CARRIER_RESIDUES, P7_NODE_GENERATORS, P5_NODE_GENERATORS, P7_CENTERS, P5_CENTERS",
        "requires": "ucns_prime_primitives_p7_p5",
        "rollback": "remove with the complete prime phase-and-lift witness",
        "rollout": "exact static research ledger; selection effect none",
        "since": "2026-08-11",
        "storage_boundary": "none",
        "summary": "stores the exact P7 and P5 occurrence-turn, carrier-residue, node-generator, and projected-center ledgers consumed by the phase-and-lift witness",
        "tests": "tests/test_prime_phase_lift.py",
        "unresolved": "independently derived ledgers beyond the frozen P7/P5 construction",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_phase_lift_data.py",
      "id": "ucns_prime_phase_lift_data"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "pair readouts are requested from a complete phase-and-lift candidate",
        "since": "2026-08-11",
        "then": "link readouts are derived from the globally fixed occurrence heights rather than used as construction inputs"
      },
      "file": "src/ucns/prime_phase_lift_model.py",
      "id": "prime_phase_lift_model_derives_links_after_global_lift"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "a lifted projected event is represented",
        "since": "2026-08-11",
        "then": "projected coincidence and strict braid order remain typed separately and no physical contact is inferred"
      },
      "file": "src/ucns/prime_phase_lift_model.py",
      "id": "prime_phase_lift_model_preserves_event_semantics"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "exact modular phase helpers, height-gap calculation, component and cycle-rank readouts",
        "module_kind": "experiment",
        "module_name": "prime_phase_lift_model",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "EventSemantic, PhaseLaw, LiftOccurrence, LiftHypernode, PairLinkReadout, PrimePhaseLiftCandidate, PhaseLiftError",
        "requires": "ucns_prime_phase_lift_data, ucns_prime_primitives_p7_p5",
        "rollback": "remove with the complete prime phase-and-lift witness",
        "rollout": "typed research model; projected coincidence remains distinct from physical contact",
        "since": "2026-08-11",
        "storage_boundary": "none",
        "summary": "defines the typed exact phase, lift, event-semantic, geometric, and derived pair-link readouts for the P7-first witness",
        "tests": "tests/test_prime_phase_lift.py",
        "unresolved": "smooth lift replacement, whole-ribbon disjointness, tangent regularization, ambient isotopy",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_phase_lift_model.py",
      "id": "ucns_prime_phase_lift_model"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "arithmetic primality and UCNS primitive standing are evaluated",
        "since": "2026-08-11",
        "then": "the predicates remain separate and two remains arithmetic-prime"
      },
      "file": "src/ucns/prime_primitives.py",
      "id": "prime_arithmetic_geometry_firewall"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "P5 is constructed directly from one center plus four outer carriers",
        "since": "2026-08-11",
        "then": "ten pairs, eighteen projected pair events, and arity spectrum two-twelve four-one reconcile exactly"
      },
      "file": "src/ucns/prime_primitives.py",
      "id": "prime_p5_direct_exact_signature"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "P7 is constructed directly from one center plus six outer carriers",
        "since": "2026-08-11",
        "then": "twenty-one pairs, thirty-nine projected pair events, and arity spectrum two-six three-six six-one reconcile exactly"
      },
      "file": "src/ucns/prime_primitives.py",
      "id": "prime_p7_direct_exact_signature"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "P7 spoke and adjacent-rim separations are measured",
        "since": "2026-08-11",
        "then": "all twelve structural edges are unit-vesica relations and q equals six is the unique equal-spoke-rim ring order"
      },
      "file": "src/ucns/prime_primitives.py",
      "id": "prime_p7_uniform_structural_relation"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "dyadic and triadic readouts are reported",
        "since": "2026-08-11",
        "then": "they are derived restrictions and never treated as construction lineage"
      },
      "file": "src/ucns/prime_primitives.py",
      "id": "prime_restrictions_follow_construction"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "K2 is tested under a closure axiom requiring a nontrivial relational cycle",
        "since": "2026-08-11",
        "then": "its cycle rank is zero and it conditionally fails closed-primitive standing without changing arithmetic primality"
      },
      "file": "src/ucns/prime_primitives.py",
      "id": "prime_two_cycle_boundary"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "exact pair-distance ledgers, hypernode reconciliation, restriction counts, deterministic hashing",
        "module_kind": "experiment",
        "module_name": "prime_primitives",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "RelationKind, Hypernode, PrimePrimitive, is_arithmetic_prime, cycle_rank, dyadic_boundary, build_prime_seven, build_prime_five, family_certificate",
        "requires": "none",
        "rollback": "remove this module, its test, and documentation",
        "rollout": "nonselecting P7-first research artifact; lower-prime forms are restrictions, not construction parts",
        "since": "2026-08-11",
        "storage_boundary": "none",
        "summary": "constructs P7 first and P5 second as direct exact projected carrier complexes, preserves n-ary hypernodes, and separates arithmetic primality from UCNS closed-primitive standing",
        "tests": "tests/test_prime_primitives.py",
        "unresolved": "P2 ontology, P3 artifact, smooth M\u00f6bius lift, phase field, physical event semantics, braid topology, spectral operator, zeta correspondence",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_primitives.py",
      "id": "ucns_prime_primitives_p7_p5"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the owning facade invokes this readable helper",
        "since": "2026-08-11",
        "then": "the helper behavior is exercised through the named facade test without becoming a separate certificate"
      },
      "file": "src/ucns/prime_replay_phase_milnor_data.py",
      "id": "prime_replay_data_is_receipt_witnessed"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "module implementation",
        "module_kind": "experiment",
        "module_name": "prime_replay_phase_milnor_data",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "internal readable implementation used through the declared facade",
        "requires": "ucns_prime_smooth_ribbons_p7_p5",
        "rollback": "remove only with the owning consolidated research layer",
        "rollout": "readable implementation; authority remains with the facade contracts",
        "since": "2026-08-11",
        "storage_boundary": "none",
        "summary": "immutable independent replay, phase-sensitivity, and numerical Milnor receipt data",
        "tests": "tests/test_prime_replay_phase_milnor_receipt.py",
        "unresolved": "see owning facade contracts and research document",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_replay_phase_milnor_data.py",
      "id": "ucns_prime_replay_phase_milnor_data"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "P7 and P5 selected phase laws are compared",
        "since": "2026-08-11",
        "then": "both use center winding three and therefore both produce T two-seven"
      },
      "file": "src/ucns/prime_replay_phase_milnor_receipt.py",
      "id": "prime_replay_receipt_exposes_phase_imposition"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the five algebraically split outer triples are audited",
        "since": "2026-08-11",
        "then": "each length-three mu-bar value is zero across the frozen projection, resolution, and basepoint sweeps"
      },
      "file": "src/ucns/prime_replay_phase_milnor_receipt.py",
      "id": "prime_replay_receipt_freezes_p7_milnor_values"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the compact receipt is serialized",
        "since": "2026-08-11",
        "then": "no phase law, arithmetic redefinition, electron ontology, zeta theorem, or Riemann-hypothesis proof is selected"
      },
      "file": "src/ucns/prime_replay_phase_milnor_receipt.py",
      "id": "prime_replay_receipt_is_nonselecting"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the compact receipt is loaded",
        "since": "2026-08-11",
        "then": "P7 and P5 pair counts, box counts, margins, and independent Decimal ledger hashes remain pinned"
      },
      "file": "src/ucns/prime_replay_phase_milnor_receipt.py",
      "id": "prime_replay_receipt_preserves_independent_interval_result"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "immutable base receipt validation and deterministic payload hashing",
        "module_kind": "experiment",
        "module_name": "prime_replay_phase_milnor_receipt",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "boundary_knot, validate_receipt, build_receipt",
        "requires": "ucns_prime_smooth_ribbons_p7_p5",
        "rollback": "remove this module, its test, documents, and generated summary",
        "rollout": "compact GitHub publication surface; selection effect none",
        "since": "2026-08-11",
        "storage_boundary": "none",
        "summary": "freezes the independent P7/P5 interval replay, phase-winding sensitivity, and length-three P7 Milnor audit while preserving the executable reference packet as the producing evidence",
        "tests": "tests/test_prime_replay_phase_milnor_receipt.py",
        "unresolved": "proof-assistant interval replay, analytic crossing extraction, length-four and higher Milnor invariants, multivariable Alexander polynomial, spectral operator, zeta correspondence",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_replay_phase_milnor_receipt.py",
      "id": "ucns_prime_replay_phase_milnor_receipt"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "centerline separation exceeds nine hundredths and ribbon half-width is one hundredth",
        "since": "2026-08-11",
        "then": "the complete finite-width ribbons have pairwise separation greater than seven hundredths by the triangle inequality"
      },
      "file": "src/ucns/prime_smooth_ribbons.py",
      "id": "prime_smooth_ribbons_are_globally_disjoint_at_declared_width"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "every unordered pair of P7 or P5 carriers is subdivided over the complete parameter torus",
        "since": "2026-08-11",
        "then": "a deterministic Lipschitz certificate establishes centerline separation greater than nine hundredths under the declared binary64 roundoff boundary"
      },
      "file": "src/ucns/prime_smooth_ribbons.py",
      "id": "prime_smooth_ribbons_have_global_centerline_margin"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "regular secant readouts and tangent regularizations are combined",
        "since": "2026-08-11",
        "then": "every pair receives an integer linking number and matrix rank, nullity, determinant, and nonzero-link graph readouts are derived"
      },
      "file": "src/ucns/prime_smooth_ribbons.py",
      "id": "prime_smooth_ribbons_issue_complete_linking_matrix"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "any carrier and admissible breadth",
        "since": "2026-08-11",
        "then": "the smoothed surface obeys one-turn breadth reversal and two-turn return"
      },
      "file": "src/ucns/prime_smooth_ribbons.py",
      "id": "prime_smooth_ribbons_obey_mobius_return"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the family certificate is built",
        "since": "2026-08-11",
        "then": "P7 is certified first and P5 is independently processed second under the same smoothing and separation protocol"
      },
      "file": "src/ucns/prime_smooth_ribbons.py",
      "id": "prime_smooth_ribbons_p7_precedes_p5"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "the piecewise-linear P7 or P5 lift knots are replaced",
        "since": "2026-08-11",
        "then": "one periodic C-infinity field per carrier reproduces every exact event height without overshoot"
      },
      "file": "src/ucns/prime_smooth_ribbons.py",
      "id": "prime_smooth_ribbons_preserve_all_event_lanes"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the family receipt is serialized",
        "since": "2026-08-11",
        "then": "it records the numerical proof boundary and claims no arithmetic redefinition, electron ontology, zeta theorem, or Riemann-hypothesis proof"
      },
      "file": "src/ucns/prime_smooth_ribbons.py",
      "id": "prime_smooth_ribbons_receipt_is_nonselecting"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a projected pair is externally tangent",
        "since": "2026-08-11",
        "then": "a one-hundredth outward pair-specific isotopy remains inside the global clearance, makes the projected circles disjoint, and certifies linking number zero"
      },
      "file": "src/ucns/prime_smooth_ribbons.py",
      "id": "prime_smooth_ribbons_regularize_tangent_pairs"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "flat C-infinity interpolation, exact derivative majorant, binary64 Lipschitz subdivision, pair-specific tangent isotopy, rational matrix rank",
        "module_kind": "experiment",
        "module_name": "prime_smooth_ribbons",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "SmoothPeriodicField, SmoothPrimeRibbon, PairSeparationCertificate, TangentRegularization, LinkingMatrixCertificate, SmoothRibbonCertificate, flat_step, flat_step_derivative, build_smooth_prime_seven, build_smooth_prime_five, certify_smooth_prime_seven, certify_smooth_prime_five, smooth_ribbon_family_certificate, write_smooth_ribbon_family_certificate, render_smooth_centerline_obj, render_smooth_ribbon_obj",
        "requires": "ucns_prime_phase_lift_p7_p5",
        "rollback": "remove this module, its test, documentation, generated certificate, and generated meshes",
        "rollout": "P7 first, P5 same-protocol comparison second; selection effect none; does not alter prior phase or lift receipts",
        "since": "2026-08-11",
        "storage_boundary": "caller-supplied local paths only through writer functions",
        "summary": "replaces the P7-first piecewise-linear lift by a C-infinity event-preserving field, certifies global finite-width ribbon separation by deterministic Lipschitz subdivision, regularizes tangent projections, and applies the same protocol to P5 second",
        "tests": "tests/test_prime_smooth_ribbons.py",
        "unresolved": "formal interval or proof-assistant replay, whole-link ambient isotopy, higher-order link invariants, boundary-link invariants, spectral operator, prime-power law, zeta correspondence",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_smooth_ribbons.py",
      "id": "ucns_prime_smooth_ribbons_p7_p5"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "the family certificate is serialized",
        "since": "2026-08-15",
        "then": "it distinguishes presentation and ideal-boundary evidence from a complete ideal basis, link classification, phase selection, or spectral claim"
      },
      "file": "src/ucns/prime_symbolic_alexander.py",
      "id": "prime_symbolic_alexander_receipt_is_nonselecting"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "regression",
        "given": "the symbolic matrix is specialized at every previously frozen prime-order character",
        "since": "2026-08-15",
        "then": "every modular rank equals the independently retained Fox-character fingerprint"
      },
      "file": "src/ucns/prime_symbolic_alexander.py",
      "id": "prime_symbolic_certificate_replays_finite_characters"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "the exact symbolic presentation is evaluated over its Laurent-polynomial fraction field",
        "since": "2026-08-15",
        "then": "exact rank and a nonzero pivot minor certify every earlier elementary ideal as zero and the declared first nonzero ideal as nonzero"
      },
      "file": "src/ucns/prime_symbolic_alexander.py",
      "id": "prime_symbolic_elementary_boundary_is_exact"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "the frozen P7 or P5 Wirtinger diagram is abelianized over one Laurent variable per component",
        "since": "2026-08-15",
        "then": "every sparse Fox entry has exact integer Laurent coefficients and every row satisfies the Fox fundamental identity"
      },
      "file": "src/ucns/prime_symbolic_alexander.py",
      "id": "prime_symbolic_fox_presentation_is_exact"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "exact Laurent Fox derivatives, rational-function rank, pivot minor, Fox fundamental identity",
        "module_kind": "experiment",
        "module_name": "prime_symbolic_alexander",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "SymbolicAlexanderCertificate, symbolic_alexander_certificate, symbolic_alexander_family_certificate, write_symbolic_alexander_family_certificate",
        "requires": "ucns_prime_exact_milnor_alexander_p7_p5, sympy>=1.12,<2",
        "rollback": "remove this module, its tests, documentation, and generated certificate",
        "rollout": "P7 first and P5 same-construction comparison second; selection effect none",
        "since": "2026-08-15",
        "storage_boundary": "caller-supplied local paths only through writer functions",
        "summary": "derives the exact multivariable Fox-Alexander presentations and certifies their first nonzero elementary-ideal boundaries for the frozen P7 and P5 diagrams",
        "tests": "tests/test_prime_symbolic_alexander.py",
        "unresolved": "complete generating sets and Groebner bases for the first nonzero ideals, higher elementary ideals, phase-co-winner separation, higher Milnor invariants",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/prime_symbolic_alexander.py",
      "id": "ucns_prime_symbolic_alexander_p7_p5"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "any admitted Public Gonol glyph or index",
        "since": "2026-08-20",
        "then": "one PublicGonolPosition is returned without letter, digit, punctuation, lexical, or semantic subclassing"
      },
      "file": "src/ucns/public_gonol.py",
      "id": "every_public_gonol_glyph_is_a_function_position"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "the Public Gonol carrier is imported",
        "since": "2026-08-20",
        "then": "exactly 157 unique one-scalar glyphs retain their exact order and pinned digest"
      },
      "file": "src/ucns/public_gonol.py",
      "id": "public_gonol_has_exactly_157_unique_positions"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "exact inherited Public Gonol arrangement and digest",
        "internal_surface": "_POSITION",
        "module_kind": "geometry",
        "module_name": "public_gonol",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "PUBLIC_GONOL_157, PUBLIC_GONOL_SHA256, PublicGonolPosition, public_gonol_position, public_gonol_function, public_gonol_sha256",
        "requires": "none",
        "rollback": "restore the prior file from Git history",
        "rollout": "geometry-only UCNS carrier floor",
        "since": "2026-08-20",
        "storage_boundary": "immutable constants only",
        "summary": "exact 157-position Public Gonol carrier; every glyph position is a Public Gonol function position without linguistic subclassing",
        "tests": "tests.test_public_gonol",
        "unresolved": "the exact geometric operation expressed by each function position beyond its carrier identity",
        "user_data_boundary": "none"
      },
      "file": "src/ucns/public_gonol.py",
      "id": "ucns_public_gonol_geometry"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_lifted_period",
        "cleanup": "none",
        "mutates": "none",
        "proves": "lifted_period_is_720_degrees, two_visible_laps_complete_return",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_carrier.py",
      "id": "check_lifted_period"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_non_null_validation_and_radius",
        "cleanup": "none",
        "mutates": "none",
        "proves": "non_null_carrier_has_positive_breadth",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_carrier.py",
      "id": "check_non_null_validation_and_radius"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_one_lap_is_deck_translation",
        "cleanup": "none",
        "mutates": "none",
        "proves": "one_visible_lap_is_deck_translation_only, topology_does_not_invent_orientation_algebra",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_carrier.py",
      "id": "check_one_lap_is_deck_translation"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_payload_zero_does_not_collapse_carrier",
        "cleanup": "none",
        "mutates": "none",
        "proves": "algebraic_zero_is_not_structural_null",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_carrier.py",
      "id": "check_payload_zero_does_not_collapse_carrier"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_structural_null_identity",
        "cleanup": "none",
        "mutates": "none",
        "proves": "structural_null_is_unique_and_coordinate_free",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_carrier.py",
      "id": "check_structural_null_identity"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_visible_projection_and_branch_law",
        "cleanup": "none",
        "mutates": "none",
        "proves": "visible_projection_is_360_degrees",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_carrier.py",
      "id": "check_visible_projection_and_branch_law"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_native_mobius_return_and_inverse",
        "cleanup": "none",
        "mutates": "none",
        "proves": "native_mobius_one_turn_reverses_frame, native_mobius_two_turns_restore_complete_state, native_mobius_motion_is_exactly_invertible",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_direct_mobius.py",
      "id": "native_mobius_return_check"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_geometry_public_surface_excludes_removed_domains",
        "cleanup": "none",
        "mutates": "none",
        "proves": "geometry_public_surface_excludes_nongeometric_domains",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_geometry_public_surface.py",
      "id": "check_geometry_public_surface_exclusion"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_center_spokes_require_six_distinct_surface_phases",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_seed_center_needs_six_phase_channels_for_six_spokes",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_global_compatibility.py",
      "id": "check_mobius_seed_center_six_phase_channels"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_physical_contact_and_strict_braid_are_same_event_exclusive",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_seed_physical_contact_and_strict_braid_are_event_exclusive",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_global_compatibility.py",
      "id": "check_mobius_seed_contact_braid_exclusivity"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_rigid_rotation_phase_transport_matches_direct_surface_rotation",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_seed_incident_certified_dyads_are_state_incompatible",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_global_compatibility.py",
      "id": "check_mobius_seed_direct_rotation_agreement"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_generated_certificate_is_deterministic_nonselecting_and_bounded",
        "cleanup": "pytest temporary_path",
        "mutates": "temporary_path",
        "proves": "mobius_seed_global_compatibility_certificate_is_nonselecting",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_mobius_global_compatibility.py",
      "id": "check_mobius_seed_global_certificate_firewall"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_all_oriented_incident_edge_states_are_incompatible",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_seed_incident_certified_dyads_are_state_incompatible",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_mobius_global_compatibility.py",
      "id": "check_mobius_seed_incident_dyad_state_incompatibility"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_pinned_pr174_schedule_inherits_zero_complete_local_certificates",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_seed_pr174_inherits_no_exact_rigid_vesica_pairs",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_global_compatibility.py",
      "id": "check_mobius_seed_pr174_zero_inheritance"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_rigid_rotation_transport_is_exact_on_representative_spokes",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_seed_incident_certified_dyads_are_state_incompatible",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_global_compatibility.py",
      "id": "check_mobius_seed_rigid_rotation_transport"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_compatible_certified_pairs_have_exact_maximum_capacity_three",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_seed_single_state_certified_capacity_is_three",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_mobius_global_compatibility.py",
      "id": "check_mobius_seed_single_state_capacity_three"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_surface_phase_uses_the_unlabelled_half_turn_quotient",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_seed_incident_certified_dyads_are_state_incompatible",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_global_compatibility.py",
      "id": "check_mobius_seed_surface_phase_quotient"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_every_structural_pair_reverses_over_under_order",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_seed_structural_pairs_have_alternating_braid_order",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_seed.py",
      "id": "check_mobius_seed_braid_order"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_dyad_is_anti_aligned_and_outer_phases_increment",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_seed_dyad_is_anti_aligned_and_outer_phase_is_incremental",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_seed.py",
      "id": "check_mobius_seed_dyad_phase_schedule"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_null_lift_has_six_distinct_nonzero_lanes_and_origin_margin",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_seed_lift_preserves_null_as_nonvertex_void",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_seed.py",
      "id": "check_mobius_seed_null_void"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_projection_retains_exact_seed_nodes_and_all_pairs",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_seed_projection_is_exact_and_pair_complete",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_seed.py",
      "id": "check_mobius_seed_projection_pair_completion"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_receipt_and_obj_are_deterministic_nonselecting_candidates",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_seed_candidate_is_nonselecting_and_proof_firewalled",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_seed.py",
      "id": "check_mobius_seed_proof_firewall"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_each_surface_obeys_mobius_seam_and_two_turn_return",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_seed_surface_obeys_360_seam_and_720_return",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_seed.py",
      "id": "check_mobius_seed_surface_quotient"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_sturm_certificate_proves_exactly_four_physical_boundary_contacts",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_vesica_alternate_height_branch_is_obstructed",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_vesica_exact.py",
      "id": "check_mobius_vesica_alternate_branch_obstruction"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_centerlines_have_exactly_two_contacts_and_positive_null_clearance",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_vesica_has_exact_two_centerline_contacts",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_vesica_exact.py",
      "id": "check_mobius_vesica_centerline_contacts"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_contact_semantics_and_global_surface_boundary_remain_distinct",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_vesica_contact_semantics_are_not_flattened",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_vesica_exact.py",
      "id": "check_mobius_vesica_contact_semantics"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_sturm_certificate_proves_exactly_four_physical_boundary_contacts",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_vesica_sturm_proves_four_physical_boundary_contacts",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_vesica_exact.py",
      "id": "check_mobius_vesica_four_boundary_contacts"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_seed_half_turn_phase_is_obstructed_and_cannot_inherit_certificate",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_vesica_half_turn_phase_has_exact_contact_obstruction",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_vesica_exact.py",
      "id": "check_mobius_vesica_half_turn_obstruction"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_centerlines_have_exactly_two_contacts_and_positive_null_clearance",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_vesica_null_origin_has_positive_clearance",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_vesica_exact.py",
      "id": "check_mobius_vesica_null_clearance"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_each_band_obeys_one_turn_seam_and_two_turn_return",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_vesica_obeys_one_turn_seam_and_two_turn_return",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_vesica_exact.py",
      "id": "check_mobius_vesica_quotient_return"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_combined_receipt_is_deterministic_nonselecting_and_firewalled",
        "cleanup": "pytest temporary_path",
        "mutates": "temporary_path",
        "proves": "mobius_vesica_certificate_is_nonselecting_and_zeta_firewalled",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_mobius_vesica_exact.py",
      "id": "check_mobius_vesica_receipt_firewall"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_seed_half_turn_phase_is_obstructed_and_cannot_inherit_certificate",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_vesica_seed_phase_mismatch_blocks_certificate_inheritance",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_vesica_exact.py",
      "id": "check_mobius_vesica_seed_phase_firewall"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_sturm_certificate_proves_exactly_four_physical_boundary_contacts",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_vesica_preserves_source_claims_as_testable_geometry",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_vesica_exact.py",
      "id": "check_mobius_vesica_source_claims"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_rigid_placement_plan_covers_all_twelve_structural_pairs",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_vesica_rigid_placements_cover_seed_structural_pairs",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_mobius_vesica_exact.py",
      "id": "check_mobius_vesica_structural_placements"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_width_continuation_recertifies_four_contacts_at_every_stage",
        "cleanup": "none",
        "mutates": "none",
        "proves": "mobius_vesica_width_continuation_recertifies_each_stage",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_mobius_vesica_exact.py",
      "id": "check_mobius_vesica_width_continuation"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_complete_minor_accounting_is_sealed",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_grobner_generators_cover_every_maximal_minor",
        "requires": "python3, sympy",
        "timeout": "5"
      },
      "file": "tests/test_prime_determinantal_grobner.py",
      "id": "check_prime_grobner_complete_accounting"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_result_document_preserves_research_boundary",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_grobner_receipt_preserves_nonclaims",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_determinantal_grobner.py",
      "id": "check_prime_grobner_nonclaims"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_protocol_and_parent_presentations_are_frozen",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_grobner_protocol_identity_is_frozen",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_determinantal_grobner.py",
      "id": "check_prime_grobner_protocol_frozen"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_sealed_reduced_bases_have_expected_digests",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_grobner_basis_is_complete_reduced_and_saturated",
        "requires": "python3, sympy",
        "timeout": "5"
      },
      "file": "tests/test_prime_determinantal_grobner.py",
      "id": "check_prime_grobner_reduced_bases"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_independent_replay_is_exact",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_grobner_independent_replay_agrees",
        "requires": "python3, sympy",
        "timeout": "5"
      },
      "file": "tests/test_prime_determinantal_grobner.py",
      "id": "check_prime_grobner_replay"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_borromean_magnus_benchmark_is_unit",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_magnus_benchmark_recovers_borromean_integer",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_exact_milnor_alexander.py",
      "id": "check_prime_borromean_magnus"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_family_receipt_is_deterministic_bounded_and_nonselecting",
        "cleanup": "pytest temporary_path",
        "mutates": "temporary_path",
        "proves": "prime_exact_milnor_alexander_receipt_is_nonselecting",
        "requires": "python3, mpmath",
        "timeout": "180"
      },
      "file": "tests/test_prime_exact_milnor_alexander.py",
      "id": "check_prime_exact_receipt_nonselecting"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_fox_rank_fingerprints_cover_every_prime_character",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_fox_fingerprint_covers_all_prime_characters",
        "requires": "python3, mpmath",
        "timeout": "120"
      },
      "file": "tests/test_prime_exact_milnor_alexander.py",
      "id": "check_prime_fox_complete_fingerprint"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_generic_projection_preserves_positive_isotopy_clearance",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_generic_diagram_is_fixed_before_invariants",
        "requires": "python3, mpmath",
        "timeout": "30"
      },
      "file": "tests/test_prime_exact_milnor_alexander.py",
      "id": "check_prime_generic_diagram_fixed"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_generic_diagrams_reproduce_complete_linking_matrices",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_generic_diagram_preserves_pairwise_linking",
        "requires": "python3, mpmath",
        "timeout": "60"
      },
      "file": "tests/test_prime_exact_milnor_alexander.py",
      "id": "check_prime_generic_pairwise_linking"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_all_five_p7_milnor_coefficients_are_exact_zero",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_p7_five_milnor_candidates_are_exact_zero_in_diagram",
        "requires": "python3, mpmath",
        "timeout": "60"
      },
      "file": "tests/test_prime_exact_milnor_alexander.py",
      "id": "check_prime_p7_exact_milnor_zero"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_preregistration_hash_and_selector_order_are_frozen",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_phase_selector_matches_frozen_preregistration",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_exact_milnor_alexander.py",
      "id": "check_prime_phase_preregistration_hash"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_preregistered_selector_outputs_are_not_target_fitted",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_phase_selector_uses_whole_link_character",
        "requires": "python3, mpmath",
        "timeout": "120"
      },
      "file": "tests/test_prime_exact_milnor_alexander.py",
      "id": "check_prime_phase_whole_link_selector"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_all_frozen_turns_are_inside_outward_atan2_intervals",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_generic_turns_are_outward_atan2_enclosed",
        "requires": "python3, system-libmpfr, mpmath",
        "timeout": "60"
      },
      "file": "tests/test_prime_generic_interval_certificate.py",
      "id": "check_prime_generic_interval_atan2"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_all_p7_first_p5_second_crossing_signs_are_certified",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_generic_crossing_signs_are_interval_certified",
        "requires": "python3, system-libmpfr, mpmath",
        "timeout": "60"
      },
      "file": "tests/test_prime_generic_interval_certificate.py",
      "id": "check_prime_generic_interval_crossing_signs"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_family_receipt_is_deterministic_complete_and_nonselecting",
        "cleanup": "pytest temporary_path",
        "mutates": "temporary_path",
        "proves": "prime_generic_interval_receipt_is_nonselecting",
        "requires": "python3, system-libmpfr, mpmath",
        "timeout": "120"
      },
      "file": "tests/test_prime_generic_interval_certificate.py",
      "id": "check_prime_generic_interval_receipt"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_all_smooth_height_intervals_exclude_zero_and_preserve_order",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_generic_smooth_signs_are_interval_certified",
        "requires": "python3, system-libmpfr, mpmath",
        "timeout": "60"
      },
      "file": "tests/test_prime_generic_interval_certificate.py",
      "id": "check_prime_generic_interval_smooth_signs"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_research_boundaries_remain_explicit",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_independent_phase_milnor_receipt_is_nonselecting",
        "requires": "python3",
        "timeout": "60"
      },
      "file": "tests/test_prime_independent_phase_milnor.py",
      "id": "check_prime_independent_receipt_nonselecting"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_fourier_milnor_benchmark_converges_to_minus_one",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_milnor_fourier_benchmark_recovers_borromean",
        "requires": "python3, numpy",
        "timeout": "20"
      },
      "file": "tests/test_prime_independent_phase_milnor.py",
      "id": "check_prime_milnor_borromean_benchmark"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_numerical_resolution_is_not_promoted_to_exact_theorem",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_milnor_exactness_boundary_is_preserved",
        "requires": "python3",
        "timeout": "60"
      },
      "file": "tests/test_prime_independent_phase_milnor.py",
      "id": "check_prime_milnor_exactness_boundary"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_all_five_p7_triples_converge_numerically_to_zero",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_milnor_p7_split_triples_resolve_numerically_to_zero",
        "requires": "python3, numpy",
        "timeout": "30"
      },
      "file": "tests/test_prime_independent_phase_milnor.py",
      "id": "check_prime_milnor_p7_zero_resolution"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_direct_mpfr_replay_matches_frozen_partition",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_mpfr_replay_is_backend_independent",
        "requires": "python3, libmpfr",
        "timeout": "120"
      },
      "file": "tests/test_prime_independent_phase_milnor.py",
      "id": "check_prime_mpfr_backend_independence"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_direct_mpfr_replay_recertifies_both_primes",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_mpfr_replay_recertifies_ribbon_margin",
        "requires": "python3, libmpfr",
        "timeout": "120"
      },
      "file": "tests/test_prime_independent_phase_milnor.py",
      "id": "check_prime_mpfr_ribbon_margin"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_phase_sensitivity_enumerates_all_equal_gap_alternatives",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_phase_sensitivity_separates_selection_from_emergence",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_independent_phase_milnor.py",
      "id": "check_prime_phase_sensitivity_selection"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_p7_and_p5_share_the_same_maximum_gap_knot_degrees",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_phase_sensitivity_torus_seven_is_not_forced",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_independent_phase_milnor.py",
      "id": "check_prime_phase_torus_seven_not_forced"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_boundary_cable_classes_and_component_knot_invariants",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_boundary_cable_winding_is_derived_from_phase",
        "requires": "python3",
        "timeout": "60"
      },
      "file": "tests/test_prime_interval_boundaries.py",
      "id": "check_prime_boundary_cable_winding"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_boundary_linking_matrices_are_four_times_core_matrices",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_boundary_linking_scales_by_four",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "tests/test_prime_interval_boundaries.py",
      "id": "check_prime_boundary_linking_fourfold"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_each_mobius_boundary_is_one_two_turn_component",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_boundary_curve_is_single_two_turn_component",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_interval_boundaries.py",
      "id": "check_prime_boundary_single_two_turn_component"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_algebraically_split_triples_are_enumerated_without_fake_milnor_values",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_higher_order_boundary_is_explicit",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "tests/test_prime_interval_boundaries.py",
      "id": "check_prime_higher_order_boundary"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_family_receipt_preserves_p7_first_order",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_interval_boundaries_p7_precedes_p5",
        "requires": "python3, mpmath",
        "timeout": "30"
      },
      "file": "tests/test_prime_interval_boundaries.py",
      "id": "check_prime_interval_boundaries_p7_first"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_receipt_and_boundary_exports_are_deterministic_and_firewalled",
        "cleanup": "pytest temporary_path",
        "mutates": "temporary_path",
        "proves": "prime_interval_boundary_compact_receipt_is_nonselecting",
        "requires": "python3, mpmath",
        "timeout": "40"
      },
      "file": "tests/test_prime_interval_boundaries.py",
      "id": "check_prime_interval_boundary_compact_receipt"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_interval_replay_closes_every_complete_parameter_torus",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_interval_replay_uses_outward_endpoints",
        "requires": "python3, mpmath",
        "timeout": "30"
      },
      "file": "tests/test_prime_interval_boundaries.py",
      "id": "check_prime_interval_replay_outward_endpoints"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_legacy_surface_is_an_explicit_adapter_over_readable_evidence",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_interval_replay_uses_outward_endpoints",
        "requires": "python3, mpmath, sympy",
        "timeout": "40"
      },
      "file": "tests/test_prime_interval_boundaries.py",
      "id": "check_prime_legacy_readable_adapter"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_mixed_core_boundary_matrices_are_full_rank_with_exact_determinants",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_mixed_core_boundary_matrix_is_complete",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "tests/test_prime_interval_boundaries.py",
      "id": "check_prime_mixed_core_boundary_matrix"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_boundary_component_cable_and_knot_invariants",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_boundary_component_knot_types_are_derived",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_interval_boundary_links.py",
      "id": "check_prime_boundary_component_knot_types"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_boundary_and_mixed_linking_blocks_follow_cable_homology",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_boundary_helper_is_facade_witnessed",
        "requires": "python3, sympy",
        "timeout": "20"
      },
      "file": "tests/test_prime_interval_boundary_links.py",
      "id": "check_prime_boundary_helper_facade"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_boundary_and_mixed_linking_blocks_follow_cable_homology",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_boundary_linking_matrix_follows_cable_homology",
        "requires": "python3, sympy",
        "timeout": "20"
      },
      "file": "tests/test_prime_interval_boundary_links.py",
      "id": "check_prime_boundary_linking_matrix"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_each_mobius_ribbon_has_one_closed_two_turn_boundary",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_boundary_curve_is_single_and_closed",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_interval_boundary_links.py",
      "id": "check_prime_boundary_single_closed_component"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_generic_diagram_and_length_three_milnor_profile",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_generic_helper_is_facade_witnessed",
        "requires": "python3, mpmath",
        "timeout": "20"
      },
      "file": "tests/test_prime_interval_boundary_links.py",
      "id": "check_prime_generic_helper_facade"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_receipt_and_boundary_models_are_deterministic_and_bounded",
        "cleanup": "pytest temporary_path",
        "mutates": "temporary_path",
        "proves": "prime_interval_boundary_receipt_is_nonselecting",
        "requires": "python3, mpmath, sympy",
        "timeout": "60"
      },
      "file": "tests/test_prime_interval_boundary_links.py",
      "id": "check_prime_interval_boundary_receipt"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_family_certificate_preserves_p7_first_order",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_interval_boundary_p7_precedes_p5",
        "requires": "python3, mpmath, sympy",
        "timeout": "60"
      },
      "file": "tests/test_prime_interval_boundary_links.py",
      "id": "check_prime_interval_boundary_research_order"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_outward_interval_replay_covers_every_pair",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_interval_common_is_facade_witnessed",
        "requires": "python3, mpmath",
        "timeout": "30"
      },
      "file": "tests/test_prime_interval_boundary_links.py",
      "id": "check_prime_interval_common_facade"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_interval_margin_implies_complete_ribbon_disjointness",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_interval_replay_preserves_finite_width_disjointness",
        "requires": "python3, mpmath",
        "timeout": "30"
      },
      "file": "tests/test_prime_interval_boundary_links.py",
      "id": "check_prime_interval_finite_width_disjointness"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_outward_interval_replay_covers_every_pair",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_interval_replay_is_outward_rounded",
        "requires": "python3, mpmath",
        "timeout": "30"
      },
      "file": "tests/test_prime_interval_boundary_links.py",
      "id": "check_prime_interval_outward_replay"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_outward_interval_replay_covers_every_pair",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_interval_replay_helper_is_facade_witnessed",
        "requires": "python3, mpmath",
        "timeout": "30"
      },
      "file": "tests/test_prime_interval_boundary_links.py",
      "id": "check_prime_interval_replay_helper_facade"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_generic_diagram_and_length_three_milnor_profile",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_length_three_milnor_profile_is_computed_after_global_lift",
        "requires": "python3, mpmath",
        "timeout": "20"
      },
      "file": "tests/test_prime_interval_boundary_links.py",
      "id": "check_prime_length_three_milnor_profile"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_generic_diagram_and_length_three_milnor_profile",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_milnor_helper_is_facade_witnessed",
        "requires": "python3, mpmath",
        "timeout": "20"
      },
      "file": "tests/test_prime_interval_boundary_links.py",
      "id": "check_prime_milnor_helper_facade"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_full_core_boundary_integer_invariants_distinguish_p7_and_p5",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_mixed_linking_matrix_has_exact_integer_invariants",
        "requires": "python3, sympy",
        "timeout": "20"
      },
      "file": "tests/test_prime_interval_boundary_links.py",
      "id": "check_prime_mixed_integer_invariants"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_receipt_is_deterministic_and_bounded",
        "cleanup": "pytest temporary_path",
        "mutates": "temporary_path",
        "proves": "prime_p7_length4_receipt_is_bounded",
        "requires": "python3, mpmath",
        "timeout": "60"
      },
      "file": "tests/test_prime_length4_milnor.py",
      "id": "check_prime_length4_bounded_receipt"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_frozen_degree_three_commutator_gate",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_length4_magnus_gate_matches_frozen_commutator",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_length4_milnor.py",
      "id": "check_prime_length4_commutator_gate"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_result_records_primary_reverse_and_cyclic_coefficients",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_p7_length4_result_records_cyclic_conventions",
        "requires": "python3, mpmath",
        "timeout": "60"
      },
      "file": "tests/test_prime_length4_milnor.py",
      "id": "check_prime_length4_cyclic_receipt"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_frozen_target_and_lower_order_gates",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_p7_length4_target_is_frozen_and_lower_gated",
        "requires": "python3, mpmath",
        "timeout": "60"
      },
      "file": "tests/test_prime_length4_milnor.py",
      "id": "check_prime_length4_lower_gates"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_phase_co_winners_bind_identical_inputs",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_nilpotent_phase_binding_is_topological",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_nilpotent_discriminator.py",
      "id": "check_nilpotent_phase_binding"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_checked_in_receipt_records_exact_replay",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_nilpotent_primary_and_replay_agree",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_nilpotent_discriminator.py",
      "id": "check_nilpotent_primary_replay"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_protocol_identity_and_frozen_receipt",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_nilpotent_protocol_identity_is_frozen",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_nilpotent_discriminator.py",
      "id": "check_nilpotent_protocol_identity"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_comparison_excludes_weight_one_rank",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_nilpotent_comparison_excludes_known_rank",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_nilpotent_discriminator.py",
      "id": "check_nilpotent_rank_exclusion"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_every_hypernode_has_distinct_phase_and_height",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_phase_lift_data_covers_every_p7_p5_hypernode",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_phase_lift.py",
      "id": "check_prime_phase_lift_data_coverage"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_projected_pair_events_are_strictly_height_separated",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_phase_lift_centerlines_are_disjoint",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_phase_lift.py",
      "id": "check_prime_phase_lift_disjoint_centerlines"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_every_hypernode_has_distinct_phase_and_height",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_phase_lift_resolves_every_hypernode",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_phase_lift.py",
      "id": "check_prime_phase_lift_hypernodes"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_link_readouts_follow_global_lift",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_phase_lift_link_numbers_are_derived",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_phase_lift.py",
      "id": "check_prime_phase_lift_links"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_link_readouts_follow_global_lift",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_phase_lift_model_derives_links_after_global_lift",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_phase_lift.py",
      "id": "check_prime_phase_lift_model_derived_links"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_projected_pair_events_are_strictly_height_separated",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_phase_lift_model_preserves_event_semantics",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_phase_lift.py",
      "id": "check_prime_phase_lift_model_event_semantics"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_p7_origin_remains_one_arity_six_hypernode",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_phase_lift_preserves_nary_origin",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_phase_lift.py",
      "id": "check_prime_phase_lift_origin"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_p5_is_independent_same_protocol_comparison",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_phase_lift_p5_follows_same_protocol",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_phase_lift.py",
      "id": "check_prime_phase_lift_p5_second"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_p7_global_candidate_precedes_readouts",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_phase_lift_constructs_p7_before_restrictions",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_phase_lift.py",
      "id": "check_prime_phase_lift_p7_first"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_receipt_is_deterministic_and_bounded",
        "cleanup": "pytest temporary_path",
        "mutates": "temporary_path",
        "proves": "prime_phase_lift_receipt_is_nonselecting",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_phase_lift.py",
      "id": "check_prime_phase_lift_receipt"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_mobius_one_turn_reversal_and_two_turn_return",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_phase_lift_is_seam_compatible",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_phase_lift.py",
      "id": "check_prime_phase_lift_seam"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_arithmetic_and_geometry_are_separate",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_arithmetic_geometry_firewall",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_primitives.py",
      "id": "check_prime_arithmetic_geometry_firewall"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_p5_exact_signature",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_p5_direct_exact_signature",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_primitives.py",
      "id": "check_prime_p5_direct_signature"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_p7_exact_signature",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_p7_direct_exact_signature",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_primitives.py",
      "id": "check_prime_p7_direct_signature"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_p7_uniform_relation_and_uniqueness",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_p7_uniform_structural_relation",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_primitives.py",
      "id": "check_prime_p7_uniform_relation"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_restrictions_are_readouts_not_parts",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_restrictions_follow_construction",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_primitives.py",
      "id": "check_prime_restrictions_after_construction"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_two_cycle_boundary_is_conditional",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_two_cycle_boundary",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_primitives.py",
      "id": "check_prime_two_cycle_boundary"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_receipt_is_deterministic_and_nonselecting",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_replay_data_is_receipt_witnessed",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_replay_phase_milnor_receipt.py",
      "id": "check_prime_replay_data_receipt"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_independent_decimal_replay_is_pinned",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_replay_receipt_preserves_independent_interval_result",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_replay_phase_milnor_receipt.py",
      "id": "check_prime_replay_receipt_interval"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_all_five_length_three_values_are_zero",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_replay_receipt_freezes_p7_milnor_values",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_replay_phase_milnor_receipt.py",
      "id": "check_prime_replay_receipt_milnor"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_receipt_is_deterministic_and_nonselecting",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_replay_receipt_is_nonselecting",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_replay_phase_milnor_receipt.py",
      "id": "check_prime_replay_receipt_nonselecting"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_phase_winding_is_shared_not_prime_specific",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_replay_receipt_exposes_phase_imposition",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_prime_replay_phase_milnor_receipt.py",
      "id": "check_prime_replay_receipt_phase"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_complete_parameter_tori_certify_nine_hundredths_centerline_margin",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_smooth_ribbons_have_global_centerline_margin",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "tests/test_prime_smooth_ribbons.py",
      "id": "check_prime_smooth_ribbons_centerline_margin"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_flat_step_fields_are_c_infinity_bounded_and_event_preserving",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_smooth_ribbons_preserve_all_event_lanes",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_smooth_ribbons.py",
      "id": "check_prime_smooth_ribbons_event_lanes"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_triangle_inequality_certifies_seven_hundredths_ribbon_margin",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_smooth_ribbons_are_globally_disjoint_at_declared_width",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_smooth_ribbons.py",
      "id": "check_prime_smooth_ribbons_finite_width_disjointness"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_complete_pairwise_linking_matrices_have_expected_invariants",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_smooth_ribbons_issue_complete_linking_matrix",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_smooth_ribbons.py",
      "id": "check_prime_smooth_ribbons_linking_matrix"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_smoothed_surfaces_obey_one_turn_reversal_and_two_turn_return",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_smooth_ribbons_obey_mobius_return",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_smooth_ribbons.py",
      "id": "check_prime_smooth_ribbons_mobius_return"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_family_receipt_preserves_p7_first_p5_second_order",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_smooth_ribbons_p7_precedes_p5",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_smooth_ribbons.py",
      "id": "check_prime_smooth_ribbons_p7_first"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_receipt_and_smooth_meshes_are_deterministic_and_firewalled",
        "cleanup": "pytest temporary_path",
        "mutates": "temporary_path",
        "proves": "prime_smooth_ribbons_receipt_is_nonselecting",
        "requires": "python3",
        "timeout": "30"
      },
      "file": "tests/test_prime_smooth_ribbons.py",
      "id": "check_prime_smooth_ribbons_receipt"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_tangent_pairs_receive_clearance_preserving_zero_link_regularizations",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_smooth_ribbons_regularize_tangent_pairs",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_prime_smooth_ribbons.py",
      "id": "check_prime_smooth_ribbons_tangent_regularization"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_symbolic_specializations_replay_frozen_character_ranks",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_symbolic_certificate_replays_finite_characters",
        "requires": "python3, sympy",
        "timeout": "180"
      },
      "file": "tests/test_prime_symbolic_alexander.py",
      "id": "check_prime_symbolic_character_replay"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_exact_ranks_and_first_nonzero_elementary_ideals_differ",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_symbolic_elementary_boundary_is_exact",
        "requires": "python3, sympy",
        "timeout": "180"
      },
      "file": "tests/test_prime_symbolic_alexander.py",
      "id": "check_prime_symbolic_elementary_boundary"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_symbolic_presentations_are_sparse_exact_and_deterministic",
        "cleanup": "none",
        "mutates": "none",
        "proves": "prime_symbolic_fox_presentation_is_exact",
        "requires": "python3, sympy",
        "timeout": "180"
      },
      "file": "tests/test_prime_symbolic_alexander.py",
      "id": "check_prime_symbolic_fox_exact"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_family_receipt_is_deterministic_and_bounded",
        "cleanup": "pytest temporary_path",
        "mutates": "temporary_path",
        "proves": "prime_symbolic_alexander_receipt_is_nonselecting",
        "requires": "python3, sympy",
        "timeout": "360"
      },
      "file": "tests/test_prime_symbolic_alexander.py",
      "id": "check_prime_symbolic_receipt_nonselecting"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_public_gonol_exact_and_unclassified",
        "cleanup": "none",
        "mutates": "none",
        "proves": "public_gonol_has_exactly_157_unique_positions, every_public_gonol_glyph_is_a_function_position",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_public_gonol.py",
      "id": "public_gonol_geometry_check"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_audit_gap_prevents_execution",
        "cleanup": "pytest temporary_path",
        "mutates": "temporary_path",
        "proves": "boundary_runner_audits_before_execution",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_skill_lib_boundary_runner.py",
      "id": "check_boundary_runner_audit_gate"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_missing_capability_and_timeout_are_enforced",
        "cleanup": "pytest temporary_path",
        "mutates": "temporary_path",
        "proves": "boundary_runner_consumes_capabilities_and_timeouts",
        "requires": "python3",
        "timeout": "15"
      },
      "file": "tests/test_skill_lib_boundary_runner.py",
      "id": "check_boundary_runner_capability_timeout_consumption"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_passing_receipt_has_no_activation_or_selection_effect",
        "cleanup": "pytest temporary_path",
        "mutates": "temporary_path",
        "proves": "boundary_runner_has_no_activation_effect",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_skill_lib_boundary_runner.py",
      "id": "check_boundary_runner_nonactivation"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_receipt_binds_declarations_outputs_and_identity",
        "cleanup": "pytest temporary_path",
        "mutates": "temporary_path",
        "proves": "boundary_runner_receipt_is_bounded_and_bound",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_skill_lib_boundary_runner.py",
      "id": "check_boundary_runner_receipt_binding"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_registered_posix_capabilities_are_detected",
        "cleanup": "none",
        "mutates": "none",
        "proves": "boundary_runner_consumes_capabilities_and_timeouts",
        "requires": "python3",
        "timeout": "10"
      },
      "file": "tests/test_skill_lib_boundary_runner.py",
      "id": "check_boundary_runner_registered_capability_detection"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_runner_classifies_all_outcomes_and_continues",
        "cleanup": "pytest temporary_path",
        "mutates": "temporary_path",
        "proves": "boundary_runner_classifies_and_continues",
        "requires": "python3",
        "timeout": "20"
      },
      "file": "tests/test_skill_lib_boundary_runner.py",
      "id": "check_boundary_runner_status_continuation"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_contract_audit_detects_gaps",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "contract_audit_reports_graph_gaps",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_skill_lib_contracts.py",
      "id": "check_contract_audit_detects_gaps"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_contract_audit_no_exec",
        "cleanup": "tempdir_teardown",
        "mutates": "filesystem",
        "proves": "contract_audit_is_no_exec",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_skill_lib_contracts.py",
      "id": "check_contract_audit_no_exec"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_repository_contract_graph",
        "cleanup": "none",
        "mutates": "none",
        "proves": "contract_audit_accepts_closed_graph",
        "requires": "python3",
        "timeout": "5"
      },
      "file": "tests/test_skill_lib_contracts.py",
      "id": "check_repository_contract_graph"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "declared skill-lib checks are requested for execution",
        "since": "2026-08-15",
        "then": "the no-exec contract graph audit must close before any check process starts"
      },
      "file": "tools/run_skill_lib_boundaries.py",
      "id": "boundary_runner_audits_before_execution"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "one declared check passes, fails an assertion, raises unexpectedly, or times out",
        "since": "2026-08-15",
        "then": "the runner records PASS, FAIL, ERROR, or TIMEOUT respectively and continues with remaining selected checks"
      },
      "file": "tools/run_skill_lib_boundaries.py",
      "id": "boundary_runner_classifies_and_continues"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "a CHECKS declaration names requires and timeout fields",
        "since": "2026-08-15",
        "then": "execution refuses missing capabilities and applies the positive timeout to the spawned pytest process group"
      },
      "file": "tools/run_skill_lib_boundaries.py",
      "id": "boundary_runner_consumes_capabilities_and_timeouts"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "doctrine",
        "given": "every selected check passes",
        "since": "2026-08-15",
        "then": "the receipt closes only the declared executable evidence boundary and cannot select UCNS options, activate EDCM, or confer canon status"
      },
      "file": "tools/run_skill_lib_boundaries.py",
      "id": "boundary_runner_has_no_activation_effect"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a boundary run completes",
        "since": "2026-08-15",
        "then": "its receipt binds declarations, commands, capabilities, outcomes, output digests, declared mutation and cleanup, bounded output excerpts, and an identity digest"
      },
      "file": "tools/run_skill_lib_boundaries.py",
      "id": "boundary_runner_receipt_is_bounded_and_bound"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "capability resolution, subprocess classification, receipt hashing",
        "module_kind": "instrument",
        "module_name": "run_skill_lib_boundaries",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "command-line boundary runner, run_boundaries, write_receipt",
        "requires": "skill_lib_contract_audit",
        "rollback": "remove this tool, its tests, and documentation",
        "rollout": "explicit local and CI evidence runner; no product, EDCM, or canon activation",
        "since": "2026-08-15",
        "storage_boundary": "optional caller-selected JSON receipt path",
        "summary": "audits and executes declared skill-lib CHECKS as isolated pytest boundaries with capability, timeout, and receipt enforcement",
        "tests": "tests/test_skill_lib_boundary_runner.py",
        "unresolved": "mutation verification and non-pytest CHECKS call schemes",
        "user_data_boundary": "captured test output is bounded and retained only in the caller-selected receipt"
      },
      "file": "tools/run_skill_lib_boundaries.py",
      "id": "skill_lib_boundary_runner"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "every declared contract has a resolving check and every check names known contracts",
        "since": "2026-07-21",
        "then": "the audit exits successfully"
      },
      "file": "tools/verify_skill_lib_contracts.py",
      "id": "contract_audit_accepts_closed_graph"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "safety",
        "given": "the repository contract graph is audited",
        "since": "2026-07-21",
        "then": "Python source is parsed without importing product or test modules"
      },
      "file": "tools/verify_skill_lib_contracts.py",
      "id": "contract_audit_is_no_exec"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "evidence",
        "given": "a contract, check target, or self call is missing or unknown",
        "since": "2026-07-21",
        "then": "the audit reports the gap and exits nonzero"
      },
      "file": "tools/verify_skill_lib_contracts.py",
      "id": "contract_audit_reports_graph_gaps"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "parse_blocks, audit_repository",
        "module_kind": "instrument",
        "module_name": "verify_skill_lib_contracts",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "command-line audit",
        "rollback": "remove workflow invocation and script",
        "rollout": "required CI gate",
        "since": "2026-07-21",
        "storage_boundary": "read",
        "summary": "performs a no-exec reconciliation of skill-lib MODULE_BUILD, CONTRACTS, and CHECKS declarations",
        "tests": "tests/test_skill_lib_contracts.py",
        "unresolved": "mutation-level verification beyond planted graph gaps",
        "user_data_boundary": "none"
      },
      "file": "tools/verify_skill_lib_contracts.py",
      "id": "skill_lib_contract_audit"
    }
  ],
  "edges": [
    {
      "from": "check_boundary_runner_audit_gate",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_audit_gate",
      "to": "self::test_audit_gap_prevents_execution"
    },
    {
      "from": "check_boundary_runner_audit_gate",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_audit_gate",
      "to": "boundary_runner_audits_before_execution"
    },
    {
      "from": "check_boundary_runner_audit_gate",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_audit_gate",
      "to": "python3"
    },
    {
      "from": "check_boundary_runner_capability_timeout_consumption",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_capability_timeout_consumption",
      "to": "self::test_missing_capability_and_timeout_are_enforced"
    },
    {
      "from": "check_boundary_runner_capability_timeout_consumption",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_capability_timeout_consumption",
      "to": "boundary_runner_consumes_capabilities_and_timeouts"
    },
    {
      "from": "check_boundary_runner_capability_timeout_consumption",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_capability_timeout_consumption",
      "to": "python3"
    },
    {
      "from": "check_boundary_runner_nonactivation",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_nonactivation",
      "to": "self::test_passing_receipt_has_no_activation_or_selection_effect"
    },
    {
      "from": "check_boundary_runner_nonactivation",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_nonactivation",
      "to": "boundary_runner_has_no_activation_effect"
    },
    {
      "from": "check_boundary_runner_nonactivation",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_nonactivation",
      "to": "python3"
    },
    {
      "from": "check_boundary_runner_receipt_binding",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_receipt_binding",
      "to": "self::test_receipt_binds_declarations_outputs_and_identity"
    },
    {
      "from": "check_boundary_runner_receipt_binding",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_receipt_binding",
      "to": "boundary_runner_receipt_is_bounded_and_bound"
    },
    {
      "from": "check_boundary_runner_receipt_binding",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_receipt_binding",
      "to": "python3"
    },
    {
      "from": "check_boundary_runner_registered_capability_detection",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_registered_capability_detection",
      "to": "self::test_registered_posix_capabilities_are_detected"
    },
    {
      "from": "check_boundary_runner_registered_capability_detection",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_registered_capability_detection",
      "to": "boundary_runner_consumes_capabilities_and_timeouts"
    },
    {
      "from": "check_boundary_runner_registered_capability_detection",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_registered_capability_detection",
      "to": "python3"
    },
    {
      "from": "check_boundary_runner_status_continuation",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_status_continuation",
      "to": "self::test_runner_classifies_all_outcomes_and_continues"
    },
    {
      "from": "check_boundary_runner_status_continuation",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_status_continuation",
      "to": "boundary_runner_classifies_and_continues"
    },
    {
      "from": "check_boundary_runner_status_continuation",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_boundary_runner_status_continuation",
      "to": "python3"
    },
    {
      "from": "check_contract_audit_detects_gaps",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_detects_gaps",
      "to": "self::test_contract_audit_detects_gaps"
    },
    {
      "from": "check_contract_audit_detects_gaps",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_detects_gaps",
      "to": "contract_audit_reports_graph_gaps"
    },
    {
      "from": "check_contract_audit_detects_gaps",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_detects_gaps",
      "to": "python3"
    },
    {
      "from": "check_contract_audit_no_exec",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_no_exec",
      "to": "self::test_contract_audit_no_exec"
    },
    {
      "from": "check_contract_audit_no_exec",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_no_exec",
      "to": "contract_audit_is_no_exec"
    },
    {
      "from": "check_contract_audit_no_exec",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_contract_audit_no_exec",
      "to": "python3"
    },
    {
      "from": "check_geometry_public_surface_exclusion",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_geometry_public_surface_exclusion",
      "to": "self::test_geometry_public_surface_excludes_removed_domains"
    },
    {
      "from": "check_geometry_public_surface_exclusion",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_geometry_public_surface_exclusion",
      "to": "geometry_public_surface_excludes_nongeometric_domains"
    },
    {
      "from": "check_geometry_public_surface_exclusion",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_geometry_public_surface_exclusion",
      "to": "python3"
    },
    {
      "from": "check_lifted_period",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_lifted_period",
      "to": "self::test_lifted_period"
    },
    {
      "from": "check_lifted_period",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_lifted_period",
      "to": "lifted_period_is_720_degrees"
    },
    {
      "from": "check_lifted_period",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_lifted_period",
      "to": "two_visible_laps_complete_return"
    },
    {
      "from": "check_lifted_period",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_lifted_period",
      "to": "python3"
    },
    {
      "from": "check_mobius_seed_braid_order",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_braid_order",
      "to": "self::test_every_structural_pair_reverses_over_under_order"
    },
    {
      "from": "check_mobius_seed_braid_order",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_braid_order",
      "to": "mobius_seed_structural_pairs_have_alternating_braid_order"
    },
    {
      "from": "check_mobius_seed_braid_order",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_braid_order",
      "to": "python3"
    },
    {
      "from": "check_mobius_seed_center_six_phase_channels",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_center_six_phase_channels",
      "to": "self::test_center_spokes_require_six_distinct_surface_phases"
    },
    {
      "from": "check_mobius_seed_center_six_phase_channels",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_center_six_phase_channels",
      "to": "mobius_seed_center_needs_six_phase_channels_for_six_spokes"
    },
    {
      "from": "check_mobius_seed_center_six_phase_channels",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_center_six_phase_channels",
      "to": "python3"
    },
    {
      "from": "check_mobius_seed_contact_braid_exclusivity",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_contact_braid_exclusivity",
      "to": "self::test_physical_contact_and_strict_braid_are_same_event_exclusive"
    },
    {
      "from": "check_mobius_seed_contact_braid_exclusivity",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_contact_braid_exclusivity",
      "to": "mobius_seed_physical_contact_and_strict_braid_are_event_exclusive"
    },
    {
      "from": "check_mobius_seed_contact_braid_exclusivity",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_contact_braid_exclusivity",
      "to": "python3"
    },
    {
      "from": "check_mobius_seed_direct_rotation_agreement",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_direct_rotation_agreement",
      "to": "self::test_rigid_rotation_phase_transport_matches_direct_surface_rotation"
    },
    {
      "from": "check_mobius_seed_direct_rotation_agreement",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_direct_rotation_agreement",
      "to": "mobius_seed_incident_certified_dyads_are_state_incompatible"
    },
    {
      "from": "check_mobius_seed_direct_rotation_agreement",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_direct_rotation_agreement",
      "to": "python3"
    },
    {
      "from": "check_mobius_seed_dyad_phase_schedule",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_dyad_phase_schedule",
      "to": "self::test_dyad_is_anti_aligned_and_outer_phases_increment"
    },
    {
      "from": "check_mobius_seed_dyad_phase_schedule",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_dyad_phase_schedule",
      "to": "mobius_seed_dyad_is_anti_aligned_and_outer_phase_is_incremental"
    },
    {
      "from": "check_mobius_seed_dyad_phase_schedule",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_dyad_phase_schedule",
      "to": "python3"
    },
    {
      "from": "check_mobius_seed_global_certificate_firewall",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_global_certificate_firewall",
      "to": "self::test_generated_certificate_is_deterministic_nonselecting_and_bounded"
    },
    {
      "from": "check_mobius_seed_global_certificate_firewall",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_global_certificate_firewall",
      "to": "mobius_seed_global_compatibility_certificate_is_nonselecting"
    },
    {
      "from": "check_mobius_seed_global_certificate_firewall",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_global_certificate_firewall",
      "to": "python3"
    },
    {
      "from": "check_mobius_seed_incident_dyad_state_incompatibility",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_incident_dyad_state_incompatibility",
      "to": "self::test_all_oriented_incident_edge_states_are_incompatible"
    },
    {
      "from": "check_mobius_seed_incident_dyad_state_incompatibility",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_incident_dyad_state_incompatibility",
      "to": "mobius_seed_incident_certified_dyads_are_state_incompatible"
    },
    {
      "from": "check_mobius_seed_incident_dyad_state_incompatibility",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_incident_dyad_state_incompatibility",
      "to": "python3"
    },
    {
      "from": "check_mobius_seed_null_void",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_null_void",
      "to": "self::test_null_lift_has_six_distinct_nonzero_lanes_and_origin_margin"
    },
    {
      "from": "check_mobius_seed_null_void",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_null_void",
      "to": "mobius_seed_lift_preserves_null_as_nonvertex_void"
    },
    {
      "from": "check_mobius_seed_null_void",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_null_void",
      "to": "python3"
    },
    {
      "from": "check_mobius_seed_pr174_zero_inheritance",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_pr174_zero_inheritance",
      "to": "self::test_pinned_pr174_schedule_inherits_zero_complete_local_certificates"
    },
    {
      "from": "check_mobius_seed_pr174_zero_inheritance",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_pr174_zero_inheritance",
      "to": "mobius_seed_pr174_inherits_no_exact_rigid_vesica_pairs"
    },
    {
      "from": "check_mobius_seed_pr174_zero_inheritance",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_pr174_zero_inheritance",
      "to": "python3"
    },
    {
      "from": "check_mobius_seed_projection_pair_completion",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_projection_pair_completion",
      "to": "self::test_projection_retains_exact_seed_nodes_and_all_pairs"
    },
    {
      "from": "check_mobius_seed_projection_pair_completion",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_projection_pair_completion",
      "to": "mobius_seed_projection_is_exact_and_pair_complete"
    },
    {
      "from": "check_mobius_seed_projection_pair_completion",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_projection_pair_completion",
      "to": "python3"
    },
    {
      "from": "check_mobius_seed_proof_firewall",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_proof_firewall",
      "to": "self::test_receipt_and_obj_are_deterministic_nonselecting_candidates"
    },
    {
      "from": "check_mobius_seed_proof_firewall",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_proof_firewall",
      "to": "mobius_seed_candidate_is_nonselecting_and_proof_firewalled"
    },
    {
      "from": "check_mobius_seed_proof_firewall",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_proof_firewall",
      "to": "python3"
    },
    {
      "from": "check_mobius_seed_rigid_rotation_transport",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_rigid_rotation_transport",
      "to": "self::test_rigid_rotation_transport_is_exact_on_representative_spokes"
    },
    {
      "from": "check_mobius_seed_rigid_rotation_transport",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_rigid_rotation_transport",
      "to": "mobius_seed_incident_certified_dyads_are_state_incompatible"
    },
    {
      "from": "check_mobius_seed_rigid_rotation_transport",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_rigid_rotation_transport",
      "to": "python3"
    },
    {
      "from": "check_mobius_seed_single_state_capacity_three",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_single_state_capacity_three",
      "to": "self::test_compatible_certified_pairs_have_exact_maximum_capacity_three"
    },
    {
      "from": "check_mobius_seed_single_state_capacity_three",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_single_state_capacity_three",
      "to": "mobius_seed_single_state_certified_capacity_is_three"
    },
    {
      "from": "check_mobius_seed_single_state_capacity_three",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_single_state_capacity_three",
      "to": "python3"
    },
    {
      "from": "check_mobius_seed_surface_phase_quotient",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_surface_phase_quotient",
      "to": "self::test_surface_phase_uses_the_unlabelled_half_turn_quotient"
    },
    {
      "from": "check_mobius_seed_surface_phase_quotient",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_surface_phase_quotient",
      "to": "mobius_seed_incident_certified_dyads_are_state_incompatible"
    },
    {
      "from": "check_mobius_seed_surface_phase_quotient",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_surface_phase_quotient",
      "to": "python3"
    },
    {
      "from": "check_mobius_seed_surface_quotient",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_surface_quotient",
      "to": "self::test_each_surface_obeys_mobius_seam_and_two_turn_return"
    },
    {
      "from": "check_mobius_seed_surface_quotient",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_surface_quotient",
      "to": "mobius_seed_surface_obeys_360_seam_and_720_return"
    },
    {
      "from": "check_mobius_seed_surface_quotient",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_seed_surface_quotient",
      "to": "python3"
    },
    {
      "from": "check_mobius_vesica_alternate_branch_obstruction",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_alternate_branch_obstruction",
      "to": "self::test_sturm_certificate_proves_exactly_four_physical_boundary_contacts"
    },
    {
      "from": "check_mobius_vesica_alternate_branch_obstruction",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_alternate_branch_obstruction",
      "to": "mobius_vesica_alternate_height_branch_is_obstructed"
    },
    {
      "from": "check_mobius_vesica_alternate_branch_obstruction",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_alternate_branch_obstruction",
      "to": "python3"
    },
    {
      "from": "check_mobius_vesica_centerline_contacts",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_centerline_contacts",
      "to": "self::test_centerlines_have_exactly_two_contacts_and_positive_null_clearance"
    },
    {
      "from": "check_mobius_vesica_centerline_contacts",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_centerline_contacts",
      "to": "mobius_vesica_has_exact_two_centerline_contacts"
    },
    {
      "from": "check_mobius_vesica_centerline_contacts",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_centerline_contacts",
      "to": "python3"
    },
    {
      "from": "check_mobius_vesica_contact_semantics",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_contact_semantics",
      "to": "self::test_contact_semantics_and_global_surface_boundary_remain_distinct"
    },
    {
      "from": "check_mobius_vesica_contact_semantics",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_contact_semantics",
      "to": "mobius_vesica_contact_semantics_are_not_flattened"
    },
    {
      "from": "check_mobius_vesica_contact_semantics",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_contact_semantics",
      "to": "python3"
    },
    {
      "from": "check_mobius_vesica_four_boundary_contacts",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_four_boundary_contacts",
      "to": "self::test_sturm_certificate_proves_exactly_four_physical_boundary_contacts"
    },
    {
      "from": "check_mobius_vesica_four_boundary_contacts",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_four_boundary_contacts",
      "to": "mobius_vesica_sturm_proves_four_physical_boundary_contacts"
    },
    {
      "from": "check_mobius_vesica_four_boundary_contacts",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_four_boundary_contacts",
      "to": "python3"
    },
    {
      "from": "check_mobius_vesica_half_turn_obstruction",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_half_turn_obstruction",
      "to": "self::test_seed_half_turn_phase_is_obstructed_and_cannot_inherit_certificate"
    },
    {
      "from": "check_mobius_vesica_half_turn_obstruction",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_half_turn_obstruction",
      "to": "mobius_vesica_half_turn_phase_has_exact_contact_obstruction"
    },
    {
      "from": "check_mobius_vesica_half_turn_obstruction",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_half_turn_obstruction",
      "to": "python3"
    },
    {
      "from": "check_mobius_vesica_null_clearance",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_null_clearance",
      "to": "self::test_centerlines_have_exactly_two_contacts_and_positive_null_clearance"
    },
    {
      "from": "check_mobius_vesica_null_clearance",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_null_clearance",
      "to": "mobius_vesica_null_origin_has_positive_clearance"
    },
    {
      "from": "check_mobius_vesica_null_clearance",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_null_clearance",
      "to": "python3"
    },
    {
      "from": "check_mobius_vesica_quotient_return",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_quotient_return",
      "to": "self::test_each_band_obeys_one_turn_seam_and_two_turn_return"
    },
    {
      "from": "check_mobius_vesica_quotient_return",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_quotient_return",
      "to": "mobius_vesica_obeys_one_turn_seam_and_two_turn_return"
    },
    {
      "from": "check_mobius_vesica_quotient_return",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_quotient_return",
      "to": "python3"
    },
    {
      "from": "check_mobius_vesica_receipt_firewall",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_receipt_firewall",
      "to": "self::test_combined_receipt_is_deterministic_nonselecting_and_firewalled"
    },
    {
      "from": "check_mobius_vesica_receipt_firewall",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_receipt_firewall",
      "to": "mobius_vesica_certificate_is_nonselecting_and_zeta_firewalled"
    },
    {
      "from": "check_mobius_vesica_receipt_firewall",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_receipt_firewall",
      "to": "python3"
    },
    {
      "from": "check_mobius_vesica_seed_phase_firewall",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_seed_phase_firewall",
      "to": "self::test_seed_half_turn_phase_is_obstructed_and_cannot_inherit_certificate"
    },
    {
      "from": "check_mobius_vesica_seed_phase_firewall",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_seed_phase_firewall",
      "to": "mobius_vesica_seed_phase_mismatch_blocks_certificate_inheritance"
    },
    {
      "from": "check_mobius_vesica_seed_phase_firewall",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_seed_phase_firewall",
      "to": "python3"
    },
    {
      "from": "check_mobius_vesica_source_claims",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_source_claims",
      "to": "self::test_sturm_certificate_proves_exactly_four_physical_boundary_contacts"
    },
    {
      "from": "check_mobius_vesica_source_claims",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_source_claims",
      "to": "mobius_vesica_preserves_source_claims_as_testable_geometry"
    },
    {
      "from": "check_mobius_vesica_source_claims",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_source_claims",
      "to": "python3"
    },
    {
      "from": "check_mobius_vesica_structural_placements",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_structural_placements",
      "to": "self::test_rigid_placement_plan_covers_all_twelve_structural_pairs"
    },
    {
      "from": "check_mobius_vesica_structural_placements",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_structural_placements",
      "to": "mobius_vesica_rigid_placements_cover_seed_structural_pairs"
    },
    {
      "from": "check_mobius_vesica_structural_placements",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_structural_placements",
      "to": "python3"
    },
    {
      "from": "check_mobius_vesica_width_continuation",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_width_continuation",
      "to": "self::test_width_continuation_recertifies_four_contacts_at_every_stage"
    },
    {
      "from": "check_mobius_vesica_width_continuation",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_width_continuation",
      "to": "mobius_vesica_width_continuation_recertifies_each_stage"
    },
    {
      "from": "check_mobius_vesica_width_continuation",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_mobius_vesica_width_continuation",
      "to": "python3"
    },
    {
      "from": "check_nilpotent_phase_binding",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_nilpotent_phase_binding",
      "to": "self::test_phase_co_winners_bind_identical_inputs"
    },
    {
      "from": "check_nilpotent_phase_binding",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_nilpotent_phase_binding",
      "to": "prime_nilpotent_phase_binding_is_topological"
    },
    {
      "from": "check_nilpotent_phase_binding",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_nilpotent_phase_binding",
      "to": "python3"
    },
    {
      "from": "check_nilpotent_primary_replay",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_nilpotent_primary_replay",
      "to": "self::test_checked_in_receipt_records_exact_replay"
    },
    {
      "from": "check_nilpotent_primary_replay",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_nilpotent_primary_replay",
      "to": "prime_nilpotent_primary_and_replay_agree"
    },
    {
      "from": "check_nilpotent_primary_replay",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_nilpotent_primary_replay",
      "to": "python3"
    },
    {
      "from": "check_nilpotent_protocol_identity",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_nilpotent_protocol_identity",
      "to": "self::test_protocol_identity_and_frozen_receipt"
    },
    {
      "from": "check_nilpotent_protocol_identity",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_nilpotent_protocol_identity",
      "to": "prime_nilpotent_protocol_identity_is_frozen"
    },
    {
      "from": "check_nilpotent_protocol_identity",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_nilpotent_protocol_identity",
      "to": "python3"
    },
    {
      "from": "check_nilpotent_rank_exclusion",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_nilpotent_rank_exclusion",
      "to": "self::test_comparison_excludes_weight_one_rank"
    },
    {
      "from": "check_nilpotent_rank_exclusion",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_nilpotent_rank_exclusion",
      "to": "prime_nilpotent_comparison_excludes_known_rank"
    },
    {
      "from": "check_nilpotent_rank_exclusion",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_nilpotent_rank_exclusion",
      "to": "python3"
    },
    {
      "from": "check_non_null_validation_and_radius",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_non_null_validation_and_radius",
      "to": "self::test_non_null_validation_and_radius"
    },
    {
      "from": "check_non_null_validation_and_radius",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_non_null_validation_and_radius",
      "to": "non_null_carrier_has_positive_breadth"
    },
    {
      "from": "check_non_null_validation_and_radius",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_non_null_validation_and_radius",
      "to": "python3"
    },
    {
      "from": "check_one_lap_is_deck_translation",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_one_lap_is_deck_translation",
      "to": "self::test_one_lap_is_deck_translation"
    },
    {
      "from": "check_one_lap_is_deck_translation",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_one_lap_is_deck_translation",
      "to": "one_visible_lap_is_deck_translation_only"
    },
    {
      "from": "check_one_lap_is_deck_translation",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_one_lap_is_deck_translation",
      "to": "topology_does_not_invent_orientation_algebra"
    },
    {
      "from": "check_one_lap_is_deck_translation",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_one_lap_is_deck_translation",
      "to": "python3"
    },
    {
      "from": "check_payload_zero_does_not_collapse_carrier",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_payload_zero_does_not_collapse_carrier",
      "to": "self::test_payload_zero_does_not_collapse_carrier"
    },
    {
      "from": "check_payload_zero_does_not_collapse_carrier",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_payload_zero_does_not_collapse_carrier",
      "to": "algebraic_zero_is_not_structural_null"
    },
    {
      "from": "check_payload_zero_does_not_collapse_carrier",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_payload_zero_does_not_collapse_carrier",
      "to": "python3"
    },
    {
      "from": "check_prime_arithmetic_geometry_firewall",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_arithmetic_geometry_firewall",
      "to": "self::test_arithmetic_and_geometry_are_separate"
    },
    {
      "from": "check_prime_arithmetic_geometry_firewall",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_arithmetic_geometry_firewall",
      "to": "prime_arithmetic_geometry_firewall"
    },
    {
      "from": "check_prime_arithmetic_geometry_firewall",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_arithmetic_geometry_firewall",
      "to": "python3"
    },
    {
      "from": "check_prime_borromean_magnus",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_borromean_magnus",
      "to": "self::test_borromean_magnus_benchmark_is_unit"
    },
    {
      "from": "check_prime_borromean_magnus",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_borromean_magnus",
      "to": "prime_magnus_benchmark_recovers_borromean_integer"
    },
    {
      "from": "check_prime_borromean_magnus",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_borromean_magnus",
      "to": "python3"
    },
    {
      "from": "check_prime_boundary_cable_winding",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_cable_winding",
      "to": "self::test_boundary_cable_classes_and_component_knot_invariants"
    },
    {
      "from": "check_prime_boundary_cable_winding",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_cable_winding",
      "to": "prime_boundary_cable_winding_is_derived_from_phase"
    },
    {
      "from": "check_prime_boundary_cable_winding",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_cable_winding",
      "to": "python3"
    },
    {
      "from": "check_prime_boundary_component_knot_types",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_component_knot_types",
      "to": "self::test_boundary_component_cable_and_knot_invariants"
    },
    {
      "from": "check_prime_boundary_component_knot_types",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_component_knot_types",
      "to": "prime_boundary_component_knot_types_are_derived"
    },
    {
      "from": "check_prime_boundary_component_knot_types",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_component_knot_types",
      "to": "python3"
    },
    {
      "from": "check_prime_boundary_helper_facade",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_helper_facade",
      "to": "self::test_boundary_and_mixed_linking_blocks_follow_cable_homology"
    },
    {
      "from": "check_prime_boundary_helper_facade",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_helper_facade",
      "to": "prime_boundary_helper_is_facade_witnessed"
    },
    {
      "from": "check_prime_boundary_helper_facade",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_helper_facade",
      "to": "python3"
    },
    {
      "from": "check_prime_boundary_helper_facade",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_helper_facade",
      "to": "sympy"
    },
    {
      "from": "check_prime_boundary_linking_fourfold",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_linking_fourfold",
      "to": "self::test_boundary_linking_matrices_are_four_times_core_matrices"
    },
    {
      "from": "check_prime_boundary_linking_fourfold",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_linking_fourfold",
      "to": "prime_boundary_linking_scales_by_four"
    },
    {
      "from": "check_prime_boundary_linking_fourfold",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_linking_fourfold",
      "to": "python3"
    },
    {
      "from": "check_prime_boundary_linking_matrix",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_linking_matrix",
      "to": "self::test_boundary_and_mixed_linking_blocks_follow_cable_homology"
    },
    {
      "from": "check_prime_boundary_linking_matrix",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_linking_matrix",
      "to": "prime_boundary_linking_matrix_follows_cable_homology"
    },
    {
      "from": "check_prime_boundary_linking_matrix",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_linking_matrix",
      "to": "python3"
    },
    {
      "from": "check_prime_boundary_linking_matrix",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_linking_matrix",
      "to": "sympy"
    },
    {
      "from": "check_prime_boundary_single_closed_component",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_single_closed_component",
      "to": "self::test_each_mobius_ribbon_has_one_closed_two_turn_boundary"
    },
    {
      "from": "check_prime_boundary_single_closed_component",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_single_closed_component",
      "to": "prime_boundary_curve_is_single_and_closed"
    },
    {
      "from": "check_prime_boundary_single_closed_component",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_single_closed_component",
      "to": "python3"
    },
    {
      "from": "check_prime_boundary_single_two_turn_component",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_single_two_turn_component",
      "to": "self::test_each_mobius_boundary_is_one_two_turn_component"
    },
    {
      "from": "check_prime_boundary_single_two_turn_component",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_single_two_turn_component",
      "to": "prime_boundary_curve_is_single_two_turn_component"
    },
    {
      "from": "check_prime_boundary_single_two_turn_component",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_boundary_single_two_turn_component",
      "to": "python3"
    },
    {
      "from": "check_prime_exact_receipt_nonselecting",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_exact_receipt_nonselecting",
      "to": "self::test_family_receipt_is_deterministic_bounded_and_nonselecting"
    },
    {
      "from": "check_prime_exact_receipt_nonselecting",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_exact_receipt_nonselecting",
      "to": "prime_exact_milnor_alexander_receipt_is_nonselecting"
    },
    {
      "from": "check_prime_exact_receipt_nonselecting",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_exact_receipt_nonselecting",
      "to": "mpmath"
    },
    {
      "from": "check_prime_exact_receipt_nonselecting",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_exact_receipt_nonselecting",
      "to": "python3"
    },
    {
      "from": "check_prime_fox_complete_fingerprint",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_fox_complete_fingerprint",
      "to": "self::test_fox_rank_fingerprints_cover_every_prime_character"
    },
    {
      "from": "check_prime_fox_complete_fingerprint",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_fox_complete_fingerprint",
      "to": "prime_fox_fingerprint_covers_all_prime_characters"
    },
    {
      "from": "check_prime_fox_complete_fingerprint",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_fox_complete_fingerprint",
      "to": "mpmath"
    },
    {
      "from": "check_prime_fox_complete_fingerprint",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_fox_complete_fingerprint",
      "to": "python3"
    },
    {
      "from": "check_prime_generic_diagram_fixed",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_diagram_fixed",
      "to": "self::test_generic_projection_preserves_positive_isotopy_clearance"
    },
    {
      "from": "check_prime_generic_diagram_fixed",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_diagram_fixed",
      "to": "prime_generic_diagram_is_fixed_before_invariants"
    },
    {
      "from": "check_prime_generic_diagram_fixed",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_diagram_fixed",
      "to": "mpmath"
    },
    {
      "from": "check_prime_generic_diagram_fixed",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_diagram_fixed",
      "to": "python3"
    },
    {
      "from": "check_prime_generic_helper_facade",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_helper_facade",
      "to": "self::test_generic_diagram_and_length_three_milnor_profile"
    },
    {
      "from": "check_prime_generic_helper_facade",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_helper_facade",
      "to": "prime_generic_helper_is_facade_witnessed"
    },
    {
      "from": "check_prime_generic_helper_facade",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_helper_facade",
      "to": "mpmath"
    },
    {
      "from": "check_prime_generic_helper_facade",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_helper_facade",
      "to": "python3"
    },
    {
      "from": "check_prime_generic_interval_atan2",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_atan2",
      "to": "self::test_all_frozen_turns_are_inside_outward_atan2_intervals"
    },
    {
      "from": "check_prime_generic_interval_atan2",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_atan2",
      "to": "prime_generic_turns_are_outward_atan2_enclosed"
    },
    {
      "from": "check_prime_generic_interval_atan2",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_atan2",
      "to": "mpmath"
    },
    {
      "from": "check_prime_generic_interval_atan2",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_atan2",
      "to": "python3"
    },
    {
      "from": "check_prime_generic_interval_atan2",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_atan2",
      "to": "system-libmpfr"
    },
    {
      "from": "check_prime_generic_interval_crossing_signs",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_crossing_signs",
      "to": "self::test_all_p7_first_p5_second_crossing_signs_are_certified"
    },
    {
      "from": "check_prime_generic_interval_crossing_signs",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_crossing_signs",
      "to": "prime_generic_crossing_signs_are_interval_certified"
    },
    {
      "from": "check_prime_generic_interval_crossing_signs",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_crossing_signs",
      "to": "mpmath"
    },
    {
      "from": "check_prime_generic_interval_crossing_signs",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_crossing_signs",
      "to": "python3"
    },
    {
      "from": "check_prime_generic_interval_crossing_signs",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_crossing_signs",
      "to": "system-libmpfr"
    },
    {
      "from": "check_prime_generic_interval_receipt",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_receipt",
      "to": "self::test_family_receipt_is_deterministic_complete_and_nonselecting"
    },
    {
      "from": "check_prime_generic_interval_receipt",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_receipt",
      "to": "prime_generic_interval_receipt_is_nonselecting"
    },
    {
      "from": "check_prime_generic_interval_receipt",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_receipt",
      "to": "mpmath"
    },
    {
      "from": "check_prime_generic_interval_receipt",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_receipt",
      "to": "python3"
    },
    {
      "from": "check_prime_generic_interval_receipt",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_receipt",
      "to": "system-libmpfr"
    },
    {
      "from": "check_prime_generic_interval_smooth_signs",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_smooth_signs",
      "to": "self::test_all_smooth_height_intervals_exclude_zero_and_preserve_order"
    },
    {
      "from": "check_prime_generic_interval_smooth_signs",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_smooth_signs",
      "to": "prime_generic_smooth_signs_are_interval_certified"
    },
    {
      "from": "check_prime_generic_interval_smooth_signs",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_smooth_signs",
      "to": "mpmath"
    },
    {
      "from": "check_prime_generic_interval_smooth_signs",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_smooth_signs",
      "to": "python3"
    },
    {
      "from": "check_prime_generic_interval_smooth_signs",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_interval_smooth_signs",
      "to": "system-libmpfr"
    },
    {
      "from": "check_prime_generic_pairwise_linking",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_pairwise_linking",
      "to": "self::test_generic_diagrams_reproduce_complete_linking_matrices"
    },
    {
      "from": "check_prime_generic_pairwise_linking",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_pairwise_linking",
      "to": "prime_generic_diagram_preserves_pairwise_linking"
    },
    {
      "from": "check_prime_generic_pairwise_linking",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_pairwise_linking",
      "to": "mpmath"
    },
    {
      "from": "check_prime_generic_pairwise_linking",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_generic_pairwise_linking",
      "to": "python3"
    },
    {
      "from": "check_prime_grobner_complete_accounting",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_complete_accounting",
      "to": "self::test_complete_minor_accounting_is_sealed"
    },
    {
      "from": "check_prime_grobner_complete_accounting",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_complete_accounting",
      "to": "prime_grobner_generators_cover_every_maximal_minor"
    },
    {
      "from": "check_prime_grobner_complete_accounting",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_complete_accounting",
      "to": "python3"
    },
    {
      "from": "check_prime_grobner_complete_accounting",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_complete_accounting",
      "to": "sympy"
    },
    {
      "from": "check_prime_grobner_nonclaims",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_nonclaims",
      "to": "self::test_result_document_preserves_research_boundary"
    },
    {
      "from": "check_prime_grobner_nonclaims",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_nonclaims",
      "to": "prime_grobner_receipt_preserves_nonclaims"
    },
    {
      "from": "check_prime_grobner_nonclaims",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_nonclaims",
      "to": "python3"
    },
    {
      "from": "check_prime_grobner_protocol_frozen",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_protocol_frozen",
      "to": "self::test_protocol_and_parent_presentations_are_frozen"
    },
    {
      "from": "check_prime_grobner_protocol_frozen",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_protocol_frozen",
      "to": "prime_grobner_protocol_identity_is_frozen"
    },
    {
      "from": "check_prime_grobner_protocol_frozen",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_protocol_frozen",
      "to": "python3"
    },
    {
      "from": "check_prime_grobner_reduced_bases",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_reduced_bases",
      "to": "self::test_sealed_reduced_bases_have_expected_digests"
    },
    {
      "from": "check_prime_grobner_reduced_bases",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_reduced_bases",
      "to": "prime_grobner_basis_is_complete_reduced_and_saturated"
    },
    {
      "from": "check_prime_grobner_reduced_bases",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_reduced_bases",
      "to": "python3"
    },
    {
      "from": "check_prime_grobner_reduced_bases",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_reduced_bases",
      "to": "sympy"
    },
    {
      "from": "check_prime_grobner_replay",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_replay",
      "to": "self::test_independent_replay_is_exact"
    },
    {
      "from": "check_prime_grobner_replay",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_replay",
      "to": "prime_grobner_independent_replay_agrees"
    },
    {
      "from": "check_prime_grobner_replay",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_replay",
      "to": "python3"
    },
    {
      "from": "check_prime_grobner_replay",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_grobner_replay",
      "to": "sympy"
    },
    {
      "from": "check_prime_higher_order_boundary",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_higher_order_boundary",
      "to": "self::test_algebraically_split_triples_are_enumerated_without_fake_milnor_values"
    },
    {
      "from": "check_prime_higher_order_boundary",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_higher_order_boundary",
      "to": "prime_higher_order_boundary_is_explicit"
    },
    {
      "from": "check_prime_higher_order_boundary",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_higher_order_boundary",
      "to": "python3"
    },
    {
      "from": "check_prime_independent_receipt_nonselecting",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_independent_receipt_nonselecting",
      "to": "self::test_research_boundaries_remain_explicit"
    },
    {
      "from": "check_prime_independent_receipt_nonselecting",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_independent_receipt_nonselecting",
      "to": "prime_independent_phase_milnor_receipt_is_nonselecting"
    },
    {
      "from": "check_prime_independent_receipt_nonselecting",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_independent_receipt_nonselecting",
      "to": "python3"
    },
    {
      "from": "check_prime_interval_boundaries_p7_first",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundaries_p7_first",
      "to": "self::test_family_receipt_preserves_p7_first_order"
    },
    {
      "from": "check_prime_interval_boundaries_p7_first",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundaries_p7_first",
      "to": "prime_interval_boundaries_p7_precedes_p5"
    },
    {
      "from": "check_prime_interval_boundaries_p7_first",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundaries_p7_first",
      "to": "mpmath"
    },
    {
      "from": "check_prime_interval_boundaries_p7_first",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundaries_p7_first",
      "to": "python3"
    },
    {
      "from": "check_prime_interval_boundary_compact_receipt",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundary_compact_receipt",
      "to": "self::test_receipt_and_boundary_exports_are_deterministic_and_firewalled"
    },
    {
      "from": "check_prime_interval_boundary_compact_receipt",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundary_compact_receipt",
      "to": "prime_interval_boundary_compact_receipt_is_nonselecting"
    },
    {
      "from": "check_prime_interval_boundary_compact_receipt",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundary_compact_receipt",
      "to": "mpmath"
    },
    {
      "from": "check_prime_interval_boundary_compact_receipt",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundary_compact_receipt",
      "to": "python3"
    },
    {
      "from": "check_prime_interval_boundary_receipt",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundary_receipt",
      "to": "self::test_receipt_and_boundary_models_are_deterministic_and_bounded"
    },
    {
      "from": "check_prime_interval_boundary_receipt",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundary_receipt",
      "to": "prime_interval_boundary_receipt_is_nonselecting"
    },
    {
      "from": "check_prime_interval_boundary_receipt",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundary_receipt",
      "to": "mpmath"
    },
    {
      "from": "check_prime_interval_boundary_receipt",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundary_receipt",
      "to": "python3"
    },
    {
      "from": "check_prime_interval_boundary_receipt",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundary_receipt",
      "to": "sympy"
    },
    {
      "from": "check_prime_interval_boundary_research_order",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundary_research_order",
      "to": "self::test_family_certificate_preserves_p7_first_order"
    },
    {
      "from": "check_prime_interval_boundary_research_order",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundary_research_order",
      "to": "prime_interval_boundary_p7_precedes_p5"
    },
    {
      "from": "check_prime_interval_boundary_research_order",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundary_research_order",
      "to": "mpmath"
    },
    {
      "from": "check_prime_interval_boundary_research_order",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundary_research_order",
      "to": "python3"
    },
    {
      "from": "check_prime_interval_boundary_research_order",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_boundary_research_order",
      "to": "sympy"
    },
    {
      "from": "check_prime_interval_common_facade",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_common_facade",
      "to": "self::test_outward_interval_replay_covers_every_pair"
    },
    {
      "from": "check_prime_interval_common_facade",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_common_facade",
      "to": "prime_interval_common_is_facade_witnessed"
    },
    {
      "from": "check_prime_interval_common_facade",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_common_facade",
      "to": "mpmath"
    },
    {
      "from": "check_prime_interval_common_facade",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_common_facade",
      "to": "python3"
    },
    {
      "from": "check_prime_interval_finite_width_disjointness",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_finite_width_disjointness",
      "to": "self::test_interval_margin_implies_complete_ribbon_disjointness"
    },
    {
      "from": "check_prime_interval_finite_width_disjointness",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_finite_width_disjointness",
      "to": "prime_interval_replay_preserves_finite_width_disjointness"
    },
    {
      "from": "check_prime_interval_finite_width_disjointness",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_finite_width_disjointness",
      "to": "mpmath"
    },
    {
      "from": "check_prime_interval_finite_width_disjointness",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_finite_width_disjointness",
      "to": "python3"
    },
    {
      "from": "check_prime_interval_outward_replay",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_outward_replay",
      "to": "self::test_outward_interval_replay_covers_every_pair"
    },
    {
      "from": "check_prime_interval_outward_replay",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_outward_replay",
      "to": "prime_interval_replay_is_outward_rounded"
    },
    {
      "from": "check_prime_interval_outward_replay",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_outward_replay",
      "to": "mpmath"
    },
    {
      "from": "check_prime_interval_outward_replay",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_outward_replay",
      "to": "python3"
    },
    {
      "from": "check_prime_interval_replay_helper_facade",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_replay_helper_facade",
      "to": "self::test_outward_interval_replay_covers_every_pair"
    },
    {
      "from": "check_prime_interval_replay_helper_facade",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_replay_helper_facade",
      "to": "prime_interval_replay_helper_is_facade_witnessed"
    },
    {
      "from": "check_prime_interval_replay_helper_facade",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_replay_helper_facade",
      "to": "mpmath"
    },
    {
      "from": "check_prime_interval_replay_helper_facade",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_replay_helper_facade",
      "to": "python3"
    },
    {
      "from": "check_prime_interval_replay_outward_endpoints",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_replay_outward_endpoints",
      "to": "self::test_interval_replay_closes_every_complete_parameter_torus"
    },
    {
      "from": "check_prime_interval_replay_outward_endpoints",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_replay_outward_endpoints",
      "to": "prime_interval_replay_uses_outward_endpoints"
    },
    {
      "from": "check_prime_interval_replay_outward_endpoints",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_replay_outward_endpoints",
      "to": "mpmath"
    },
    {
      "from": "check_prime_interval_replay_outward_endpoints",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_interval_replay_outward_endpoints",
      "to": "python3"
    },
    {
      "from": "check_prime_legacy_readable_adapter",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_legacy_readable_adapter",
      "to": "self::test_legacy_surface_is_an_explicit_adapter_over_readable_evidence"
    },
    {
      "from": "check_prime_legacy_readable_adapter",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_legacy_readable_adapter",
      "to": "prime_interval_replay_uses_outward_endpoints"
    },
    {
      "from": "check_prime_legacy_readable_adapter",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_legacy_readable_adapter",
      "to": "mpmath"
    },
    {
      "from": "check_prime_legacy_readable_adapter",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_legacy_readable_adapter",
      "to": "python3"
    },
    {
      "from": "check_prime_legacy_readable_adapter",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_legacy_readable_adapter",
      "to": "sympy"
    },
    {
      "from": "check_prime_length4_bounded_receipt",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_length4_bounded_receipt",
      "to": "self::test_receipt_is_deterministic_and_bounded"
    },
    {
      "from": "check_prime_length4_bounded_receipt",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_length4_bounded_receipt",
      "to": "prime_p7_length4_receipt_is_bounded"
    },
    {
      "from": "check_prime_length4_bounded_receipt",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_length4_bounded_receipt",
      "to": "mpmath"
    },
    {
      "from": "check_prime_length4_bounded_receipt",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_length4_bounded_receipt",
      "to": "python3"
    },
    {
      "from": "check_prime_length4_commutator_gate",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_length4_commutator_gate",
      "to": "self::test_frozen_degree_three_commutator_gate"
    },
    {
      "from": "check_prime_length4_commutator_gate",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_length4_commutator_gate",
      "to": "prime_length4_magnus_gate_matches_frozen_commutator"
    },
    {
      "from": "check_prime_length4_commutator_gate",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_length4_commutator_gate",
      "to": "python3"
    },
    {
      "from": "check_prime_length4_cyclic_receipt",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_length4_cyclic_receipt",
      "to": "self::test_result_records_primary_reverse_and_cyclic_coefficients"
    },
    {
      "from": "check_prime_length4_cyclic_receipt",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_length4_cyclic_receipt",
      "to": "prime_p7_length4_result_records_cyclic_conventions"
    },
    {
      "from": "check_prime_length4_cyclic_receipt",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_length4_cyclic_receipt",
      "to": "mpmath"
    },
    {
      "from": "check_prime_length4_cyclic_receipt",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_length4_cyclic_receipt",
      "to": "python3"
    },
    {
      "from": "check_prime_length4_lower_gates",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_length4_lower_gates",
      "to": "self::test_frozen_target_and_lower_order_gates"
    },
    {
      "from": "check_prime_length4_lower_gates",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_length4_lower_gates",
      "to": "prime_p7_length4_target_is_frozen_and_lower_gated"
    },
    {
      "from": "check_prime_length4_lower_gates",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_length4_lower_gates",
      "to": "mpmath"
    },
    {
      "from": "check_prime_length4_lower_gates",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_length4_lower_gates",
      "to": "python3"
    },
    {
      "from": "check_prime_length_three_milnor_profile",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_length_three_milnor_profile",
      "to": "self::test_generic_diagram_and_length_three_milnor_profile"
    },
    {
      "from": "check_prime_length_three_milnor_profile",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_length_three_milnor_profile",
      "to": "prime_length_three_milnor_profile_is_computed_after_global_lift"
    },
    {
      "from": "check_prime_length_three_milnor_profile",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_length_three_milnor_profile",
      "to": "mpmath"
    },
    {
      "from": "check_prime_length_three_milnor_profile",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_length_three_milnor_profile",
      "to": "python3"
    },
    {
      "from": "check_prime_milnor_borromean_benchmark",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_milnor_borromean_benchmark",
      "to": "self::test_fourier_milnor_benchmark_converges_to_minus_one"
    },
    {
      "from": "check_prime_milnor_borromean_benchmark",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_milnor_borromean_benchmark",
      "to": "prime_milnor_fourier_benchmark_recovers_borromean"
    },
    {
      "from": "check_prime_milnor_borromean_benchmark",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_milnor_borromean_benchmark",
      "to": "numpy"
    },
    {
      "from": "check_prime_milnor_borromean_benchmark",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_milnor_borromean_benchmark",
      "to": "python3"
    },
    {
      "from": "check_prime_milnor_exactness_boundary",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_milnor_exactness_boundary",
      "to": "self::test_numerical_resolution_is_not_promoted_to_exact_theorem"
    },
    {
      "from": "check_prime_milnor_exactness_boundary",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_milnor_exactness_boundary",
      "to": "prime_milnor_exactness_boundary_is_preserved"
    },
    {
      "from": "check_prime_milnor_exactness_boundary",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_milnor_exactness_boundary",
      "to": "python3"
    },
    {
      "from": "check_prime_milnor_helper_facade",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_milnor_helper_facade",
      "to": "self::test_generic_diagram_and_length_three_milnor_profile"
    },
    {
      "from": "check_prime_milnor_helper_facade",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_milnor_helper_facade",
      "to": "prime_milnor_helper_is_facade_witnessed"
    },
    {
      "from": "check_prime_milnor_helper_facade",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_milnor_helper_facade",
      "to": "mpmath"
    },
    {
      "from": "check_prime_milnor_helper_facade",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_milnor_helper_facade",
      "to": "python3"
    },
    {
      "from": "check_prime_milnor_p7_zero_resolution",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_milnor_p7_zero_resolution",
      "to": "self::test_all_five_p7_triples_converge_numerically_to_zero"
    },
    {
      "from": "check_prime_milnor_p7_zero_resolution",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_milnor_p7_zero_resolution",
      "to": "prime_milnor_p7_split_triples_resolve_numerically_to_zero"
    },
    {
      "from": "check_prime_milnor_p7_zero_resolution",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_milnor_p7_zero_resolution",
      "to": "numpy"
    },
    {
      "from": "check_prime_milnor_p7_zero_resolution",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_milnor_p7_zero_resolution",
      "to": "python3"
    },
    {
      "from": "check_prime_mixed_core_boundary_matrix",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_mixed_core_boundary_matrix",
      "to": "self::test_mixed_core_boundary_matrices_are_full_rank_with_exact_determinants"
    },
    {
      "from": "check_prime_mixed_core_boundary_matrix",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_mixed_core_boundary_matrix",
      "to": "prime_mixed_core_boundary_matrix_is_complete"
    },
    {
      "from": "check_prime_mixed_core_boundary_matrix",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_mixed_core_boundary_matrix",
      "to": "python3"
    },
    {
      "from": "check_prime_mixed_integer_invariants",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_mixed_integer_invariants",
      "to": "self::test_full_core_boundary_integer_invariants_distinguish_p7_and_p5"
    },
    {
      "from": "check_prime_mixed_integer_invariants",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_mixed_integer_invariants",
      "to": "prime_mixed_linking_matrix_has_exact_integer_invariants"
    },
    {
      "from": "check_prime_mixed_integer_invariants",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_mixed_integer_invariants",
      "to": "python3"
    },
    {
      "from": "check_prime_mixed_integer_invariants",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_mixed_integer_invariants",
      "to": "sympy"
    },
    {
      "from": "check_prime_mpfr_backend_independence",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_mpfr_backend_independence",
      "to": "self::test_direct_mpfr_replay_matches_frozen_partition"
    },
    {
      "from": "check_prime_mpfr_backend_independence",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_mpfr_backend_independence",
      "to": "prime_mpfr_replay_is_backend_independent"
    },
    {
      "from": "check_prime_mpfr_backend_independence",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_mpfr_backend_independence",
      "to": "libmpfr"
    },
    {
      "from": "check_prime_mpfr_backend_independence",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_mpfr_backend_independence",
      "to": "python3"
    },
    {
      "from": "check_prime_mpfr_ribbon_margin",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_mpfr_ribbon_margin",
      "to": "self::test_direct_mpfr_replay_recertifies_both_primes"
    },
    {
      "from": "check_prime_mpfr_ribbon_margin",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_mpfr_ribbon_margin",
      "to": "prime_mpfr_replay_recertifies_ribbon_margin"
    },
    {
      "from": "check_prime_mpfr_ribbon_margin",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_mpfr_ribbon_margin",
      "to": "libmpfr"
    },
    {
      "from": "check_prime_mpfr_ribbon_margin",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_mpfr_ribbon_margin",
      "to": "python3"
    },
    {
      "from": "check_prime_p5_direct_signature",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_p5_direct_signature",
      "to": "self::test_p5_exact_signature"
    },
    {
      "from": "check_prime_p5_direct_signature",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_p5_direct_signature",
      "to": "prime_p5_direct_exact_signature"
    },
    {
      "from": "check_prime_p5_direct_signature",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_p5_direct_signature",
      "to": "python3"
    },
    {
      "from": "check_prime_p7_direct_signature",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_p7_direct_signature",
      "to": "self::test_p7_exact_signature"
    },
    {
      "from": "check_prime_p7_direct_signature",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_p7_direct_signature",
      "to": "prime_p7_direct_exact_signature"
    },
    {
      "from": "check_prime_p7_direct_signature",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_p7_direct_signature",
      "to": "python3"
    },
    {
      "from": "check_prime_p7_exact_milnor_zero",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_p7_exact_milnor_zero",
      "to": "self::test_all_five_p7_milnor_coefficients_are_exact_zero"
    },
    {
      "from": "check_prime_p7_exact_milnor_zero",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_p7_exact_milnor_zero",
      "to": "prime_p7_five_milnor_candidates_are_exact_zero_in_diagram"
    },
    {
      "from": "check_prime_p7_exact_milnor_zero",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_p7_exact_milnor_zero",
      "to": "mpmath"
    },
    {
      "from": "check_prime_p7_exact_milnor_zero",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_p7_exact_milnor_zero",
      "to": "python3"
    },
    {
      "from": "check_prime_p7_uniform_relation",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_p7_uniform_relation",
      "to": "self::test_p7_uniform_relation_and_uniqueness"
    },
    {
      "from": "check_prime_p7_uniform_relation",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_p7_uniform_relation",
      "to": "prime_p7_uniform_structural_relation"
    },
    {
      "from": "check_prime_p7_uniform_relation",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_p7_uniform_relation",
      "to": "python3"
    },
    {
      "from": "check_prime_phase_lift_data_coverage",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_data_coverage",
      "to": "self::test_every_hypernode_has_distinct_phase_and_height"
    },
    {
      "from": "check_prime_phase_lift_data_coverage",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_data_coverage",
      "to": "prime_phase_lift_data_covers_every_p7_p5_hypernode"
    },
    {
      "from": "check_prime_phase_lift_data_coverage",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_data_coverage",
      "to": "python3"
    },
    {
      "from": "check_prime_phase_lift_disjoint_centerlines",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_disjoint_centerlines",
      "to": "self::test_projected_pair_events_are_strictly_height_separated"
    },
    {
      "from": "check_prime_phase_lift_disjoint_centerlines",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_disjoint_centerlines",
      "to": "prime_phase_lift_centerlines_are_disjoint"
    },
    {
      "from": "check_prime_phase_lift_disjoint_centerlines",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_disjoint_centerlines",
      "to": "python3"
    },
    {
      "from": "check_prime_phase_lift_hypernodes",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_hypernodes",
      "to": "self::test_every_hypernode_has_distinct_phase_and_height"
    },
    {
      "from": "check_prime_phase_lift_hypernodes",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_hypernodes",
      "to": "prime_phase_lift_resolves_every_hypernode"
    },
    {
      "from": "check_prime_phase_lift_hypernodes",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_hypernodes",
      "to": "python3"
    },
    {
      "from": "check_prime_phase_lift_links",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_links",
      "to": "self::test_link_readouts_follow_global_lift"
    },
    {
      "from": "check_prime_phase_lift_links",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_links",
      "to": "prime_phase_lift_link_numbers_are_derived"
    },
    {
      "from": "check_prime_phase_lift_links",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_links",
      "to": "python3"
    },
    {
      "from": "check_prime_phase_lift_model_derived_links",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_model_derived_links",
      "to": "self::test_link_readouts_follow_global_lift"
    },
    {
      "from": "check_prime_phase_lift_model_derived_links",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_model_derived_links",
      "to": "prime_phase_lift_model_derives_links_after_global_lift"
    },
    {
      "from": "check_prime_phase_lift_model_derived_links",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_model_derived_links",
      "to": "python3"
    },
    {
      "from": "check_prime_phase_lift_model_event_semantics",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_model_event_semantics",
      "to": "self::test_projected_pair_events_are_strictly_height_separated"
    },
    {
      "from": "check_prime_phase_lift_model_event_semantics",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_model_event_semantics",
      "to": "prime_phase_lift_model_preserves_event_semantics"
    },
    {
      "from": "check_prime_phase_lift_model_event_semantics",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_model_event_semantics",
      "to": "python3"
    },
    {
      "from": "check_prime_phase_lift_origin",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_origin",
      "to": "self::test_p7_origin_remains_one_arity_six_hypernode"
    },
    {
      "from": "check_prime_phase_lift_origin",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_origin",
      "to": "prime_phase_lift_preserves_nary_origin"
    },
    {
      "from": "check_prime_phase_lift_origin",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_origin",
      "to": "python3"
    },
    {
      "from": "check_prime_phase_lift_p5_second",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_p5_second",
      "to": "self::test_p5_is_independent_same_protocol_comparison"
    },
    {
      "from": "check_prime_phase_lift_p5_second",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_p5_second",
      "to": "prime_phase_lift_p5_follows_same_protocol"
    },
    {
      "from": "check_prime_phase_lift_p5_second",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_p5_second",
      "to": "python3"
    },
    {
      "from": "check_prime_phase_lift_p7_first",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_p7_first",
      "to": "self::test_p7_global_candidate_precedes_readouts"
    },
    {
      "from": "check_prime_phase_lift_p7_first",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_p7_first",
      "to": "prime_phase_lift_constructs_p7_before_restrictions"
    },
    {
      "from": "check_prime_phase_lift_p7_first",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_p7_first",
      "to": "python3"
    },
    {
      "from": "check_prime_phase_lift_receipt",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_receipt",
      "to": "self::test_receipt_is_deterministic_and_bounded"
    },
    {
      "from": "check_prime_phase_lift_receipt",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_receipt",
      "to": "prime_phase_lift_receipt_is_nonselecting"
    },
    {
      "from": "check_prime_phase_lift_receipt",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_receipt",
      "to": "python3"
    },
    {
      "from": "check_prime_phase_lift_seam",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_seam",
      "to": "self::test_mobius_one_turn_reversal_and_two_turn_return"
    },
    {
      "from": "check_prime_phase_lift_seam",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_seam",
      "to": "prime_phase_lift_is_seam_compatible"
    },
    {
      "from": "check_prime_phase_lift_seam",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_lift_seam",
      "to": "python3"
    },
    {
      "from": "check_prime_phase_preregistration_hash",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_preregistration_hash",
      "to": "self::test_preregistration_hash_and_selector_order_are_frozen"
    },
    {
      "from": "check_prime_phase_preregistration_hash",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_preregistration_hash",
      "to": "prime_phase_selector_matches_frozen_preregistration"
    },
    {
      "from": "check_prime_phase_preregistration_hash",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_preregistration_hash",
      "to": "python3"
    },
    {
      "from": "check_prime_phase_sensitivity_selection",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_sensitivity_selection",
      "to": "self::test_phase_sensitivity_enumerates_all_equal_gap_alternatives"
    },
    {
      "from": "check_prime_phase_sensitivity_selection",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_sensitivity_selection",
      "to": "prime_phase_sensitivity_separates_selection_from_emergence"
    },
    {
      "from": "check_prime_phase_sensitivity_selection",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_sensitivity_selection",
      "to": "python3"
    },
    {
      "from": "check_prime_phase_torus_seven_not_forced",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_torus_seven_not_forced",
      "to": "self::test_p7_and_p5_share_the_same_maximum_gap_knot_degrees"
    },
    {
      "from": "check_prime_phase_torus_seven_not_forced",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_torus_seven_not_forced",
      "to": "prime_phase_sensitivity_torus_seven_is_not_forced"
    },
    {
      "from": "check_prime_phase_torus_seven_not_forced",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_torus_seven_not_forced",
      "to": "python3"
    },
    {
      "from": "check_prime_phase_whole_link_selector",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_whole_link_selector",
      "to": "self::test_preregistered_selector_outputs_are_not_target_fitted"
    },
    {
      "from": "check_prime_phase_whole_link_selector",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_whole_link_selector",
      "to": "prime_phase_selector_uses_whole_link_character"
    },
    {
      "from": "check_prime_phase_whole_link_selector",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_whole_link_selector",
      "to": "mpmath"
    },
    {
      "from": "check_prime_phase_whole_link_selector",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_phase_whole_link_selector",
      "to": "python3"
    },
    {
      "from": "check_prime_replay_data_receipt",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_replay_data_receipt",
      "to": "self::test_receipt_is_deterministic_and_nonselecting"
    },
    {
      "from": "check_prime_replay_data_receipt",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_replay_data_receipt",
      "to": "prime_replay_data_is_receipt_witnessed"
    },
    {
      "from": "check_prime_replay_data_receipt",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_replay_data_receipt",
      "to": "python3"
    },
    {
      "from": "check_prime_replay_receipt_interval",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_replay_receipt_interval",
      "to": "self::test_independent_decimal_replay_is_pinned"
    },
    {
      "from": "check_prime_replay_receipt_interval",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_replay_receipt_interval",
      "to": "prime_replay_receipt_preserves_independent_interval_result"
    },
    {
      "from": "check_prime_replay_receipt_interval",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_replay_receipt_interval",
      "to": "python3"
    },
    {
      "from": "check_prime_replay_receipt_milnor",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_replay_receipt_milnor",
      "to": "self::test_all_five_length_three_values_are_zero"
    },
    {
      "from": "check_prime_replay_receipt_milnor",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_replay_receipt_milnor",
      "to": "prime_replay_receipt_freezes_p7_milnor_values"
    },
    {
      "from": "check_prime_replay_receipt_milnor",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_replay_receipt_milnor",
      "to": "python3"
    },
    {
      "from": "check_prime_replay_receipt_nonselecting",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_replay_receipt_nonselecting",
      "to": "self::test_receipt_is_deterministic_and_nonselecting"
    },
    {
      "from": "check_prime_replay_receipt_nonselecting",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_replay_receipt_nonselecting",
      "to": "prime_replay_receipt_is_nonselecting"
    },
    {
      "from": "check_prime_replay_receipt_nonselecting",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_replay_receipt_nonselecting",
      "to": "python3"
    },
    {
      "from": "check_prime_replay_receipt_phase",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_replay_receipt_phase",
      "to": "self::test_phase_winding_is_shared_not_prime_specific"
    },
    {
      "from": "check_prime_replay_receipt_phase",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_replay_receipt_phase",
      "to": "prime_replay_receipt_exposes_phase_imposition"
    },
    {
      "from": "check_prime_replay_receipt_phase",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_replay_receipt_phase",
      "to": "python3"
    },
    {
      "from": "check_prime_restrictions_after_construction",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_restrictions_after_construction",
      "to": "self::test_restrictions_are_readouts_not_parts"
    },
    {
      "from": "check_prime_restrictions_after_construction",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_restrictions_after_construction",
      "to": "prime_restrictions_follow_construction"
    },
    {
      "from": "check_prime_restrictions_after_construction",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_restrictions_after_construction",
      "to": "python3"
    },
    {
      "from": "check_prime_smooth_ribbons_centerline_margin",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_centerline_margin",
      "to": "self::test_complete_parameter_tori_certify_nine_hundredths_centerline_margin"
    },
    {
      "from": "check_prime_smooth_ribbons_centerline_margin",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_centerline_margin",
      "to": "prime_smooth_ribbons_have_global_centerline_margin"
    },
    {
      "from": "check_prime_smooth_ribbons_centerline_margin",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_centerline_margin",
      "to": "python3"
    },
    {
      "from": "check_prime_smooth_ribbons_event_lanes",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_event_lanes",
      "to": "self::test_flat_step_fields_are_c_infinity_bounded_and_event_preserving"
    },
    {
      "from": "check_prime_smooth_ribbons_event_lanes",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_event_lanes",
      "to": "prime_smooth_ribbons_preserve_all_event_lanes"
    },
    {
      "from": "check_prime_smooth_ribbons_event_lanes",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_event_lanes",
      "to": "python3"
    },
    {
      "from": "check_prime_smooth_ribbons_finite_width_disjointness",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_finite_width_disjointness",
      "to": "self::test_triangle_inequality_certifies_seven_hundredths_ribbon_margin"
    },
    {
      "from": "check_prime_smooth_ribbons_finite_width_disjointness",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_finite_width_disjointness",
      "to": "prime_smooth_ribbons_are_globally_disjoint_at_declared_width"
    },
    {
      "from": "check_prime_smooth_ribbons_finite_width_disjointness",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_finite_width_disjointness",
      "to": "python3"
    },
    {
      "from": "check_prime_smooth_ribbons_linking_matrix",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_linking_matrix",
      "to": "self::test_complete_pairwise_linking_matrices_have_expected_invariants"
    },
    {
      "from": "check_prime_smooth_ribbons_linking_matrix",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_linking_matrix",
      "to": "prime_smooth_ribbons_issue_complete_linking_matrix"
    },
    {
      "from": "check_prime_smooth_ribbons_linking_matrix",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_linking_matrix",
      "to": "python3"
    },
    {
      "from": "check_prime_smooth_ribbons_mobius_return",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_mobius_return",
      "to": "self::test_smoothed_surfaces_obey_one_turn_reversal_and_two_turn_return"
    },
    {
      "from": "check_prime_smooth_ribbons_mobius_return",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_mobius_return",
      "to": "prime_smooth_ribbons_obey_mobius_return"
    },
    {
      "from": "check_prime_smooth_ribbons_mobius_return",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_mobius_return",
      "to": "python3"
    },
    {
      "from": "check_prime_smooth_ribbons_p7_first",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_p7_first",
      "to": "self::test_family_receipt_preserves_p7_first_p5_second_order"
    },
    {
      "from": "check_prime_smooth_ribbons_p7_first",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_p7_first",
      "to": "prime_smooth_ribbons_p7_precedes_p5"
    },
    {
      "from": "check_prime_smooth_ribbons_p7_first",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_p7_first",
      "to": "python3"
    },
    {
      "from": "check_prime_smooth_ribbons_receipt",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_receipt",
      "to": "self::test_receipt_and_smooth_meshes_are_deterministic_and_firewalled"
    },
    {
      "from": "check_prime_smooth_ribbons_receipt",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_receipt",
      "to": "prime_smooth_ribbons_receipt_is_nonselecting"
    },
    {
      "from": "check_prime_smooth_ribbons_receipt",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_receipt",
      "to": "python3"
    },
    {
      "from": "check_prime_smooth_ribbons_tangent_regularization",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_tangent_regularization",
      "to": "self::test_tangent_pairs_receive_clearance_preserving_zero_link_regularizations"
    },
    {
      "from": "check_prime_smooth_ribbons_tangent_regularization",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_tangent_regularization",
      "to": "prime_smooth_ribbons_regularize_tangent_pairs"
    },
    {
      "from": "check_prime_smooth_ribbons_tangent_regularization",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_smooth_ribbons_tangent_regularization",
      "to": "python3"
    },
    {
      "from": "check_prime_symbolic_character_replay",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_symbolic_character_replay",
      "to": "self::test_symbolic_specializations_replay_frozen_character_ranks"
    },
    {
      "from": "check_prime_symbolic_character_replay",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_symbolic_character_replay",
      "to": "prime_symbolic_certificate_replays_finite_characters"
    },
    {
      "from": "check_prime_symbolic_character_replay",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_symbolic_character_replay",
      "to": "python3"
    },
    {
      "from": "check_prime_symbolic_character_replay",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_symbolic_character_replay",
      "to": "sympy"
    },
    {
      "from": "check_prime_symbolic_elementary_boundary",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_symbolic_elementary_boundary",
      "to": "self::test_exact_ranks_and_first_nonzero_elementary_ideals_differ"
    },
    {
      "from": "check_prime_symbolic_elementary_boundary",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_symbolic_elementary_boundary",
      "to": "prime_symbolic_elementary_boundary_is_exact"
    },
    {
      "from": "check_prime_symbolic_elementary_boundary",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_symbolic_elementary_boundary",
      "to": "python3"
    },
    {
      "from": "check_prime_symbolic_elementary_boundary",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_symbolic_elementary_boundary",
      "to": "sympy"
    },
    {
      "from": "check_prime_symbolic_fox_exact",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_symbolic_fox_exact",
      "to": "self::test_symbolic_presentations_are_sparse_exact_and_deterministic"
    },
    {
      "from": "check_prime_symbolic_fox_exact",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_symbolic_fox_exact",
      "to": "prime_symbolic_fox_presentation_is_exact"
    },
    {
      "from": "check_prime_symbolic_fox_exact",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_symbolic_fox_exact",
      "to": "python3"
    },
    {
      "from": "check_prime_symbolic_fox_exact",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_symbolic_fox_exact",
      "to": "sympy"
    },
    {
      "from": "check_prime_symbolic_receipt_nonselecting",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_symbolic_receipt_nonselecting",
      "to": "self::test_family_receipt_is_deterministic_and_bounded"
    },
    {
      "from": "check_prime_symbolic_receipt_nonselecting",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_symbolic_receipt_nonselecting",
      "to": "prime_symbolic_alexander_receipt_is_nonselecting"
    },
    {
      "from": "check_prime_symbolic_receipt_nonselecting",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_symbolic_receipt_nonselecting",
      "to": "python3"
    },
    {
      "from": "check_prime_symbolic_receipt_nonselecting",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_symbolic_receipt_nonselecting",
      "to": "sympy"
    },
    {
      "from": "check_prime_two_cycle_boundary",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_prime_two_cycle_boundary",
      "to": "self::test_two_cycle_boundary_is_conditional"
    },
    {
      "from": "check_prime_two_cycle_boundary",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_prime_two_cycle_boundary",
      "to": "prime_two_cycle_boundary"
    },
    {
      "from": "check_prime_two_cycle_boundary",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_prime_two_cycle_boundary",
      "to": "python3"
    },
    {
      "from": "check_repository_contract_graph",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_repository_contract_graph",
      "to": "self::test_repository_contract_graph"
    },
    {
      "from": "check_repository_contract_graph",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_repository_contract_graph",
      "to": "contract_audit_accepts_closed_graph"
    },
    {
      "from": "check_repository_contract_graph",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_repository_contract_graph",
      "to": "python3"
    },
    {
      "from": "check_structural_null_identity",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_structural_null_identity",
      "to": "self::test_structural_null_identity"
    },
    {
      "from": "check_structural_null_identity",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_structural_null_identity",
      "to": "structural_null_is_unique_and_coordinate_free"
    },
    {
      "from": "check_structural_null_identity",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_structural_null_identity",
      "to": "python3"
    },
    {
      "from": "check_visible_projection_and_branch_law",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_visible_projection_and_branch_law",
      "to": "self::test_visible_projection_and_branch_law"
    },
    {
      "from": "check_visible_projection_and_branch_law",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_visible_projection_and_branch_law",
      "to": "visible_projection_is_360_degrees"
    },
    {
      "from": "check_visible_projection_and_branch_law",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "check_visible_projection_and_branch_law",
      "to": "python3"
    },
    {
      "from": "native_mobius_return_check",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "native_mobius_return_check",
      "to": "self::test_native_mobius_return_and_inverse"
    },
    {
      "from": "native_mobius_return_check",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "native_mobius_return_check",
      "to": "native_mobius_motion_is_exactly_invertible"
    },
    {
      "from": "native_mobius_return_check",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "native_mobius_return_check",
      "to": "native_mobius_one_turn_reverses_frame"
    },
    {
      "from": "native_mobius_return_check",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "native_mobius_return_check",
      "to": "native_mobius_two_turns_restore_complete_state"
    },
    {
      "from": "native_mobius_return_check",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "native_mobius_return_check",
      "to": "python3"
    },
    {
      "from": "public_gonol_geometry_check",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "public_gonol_geometry_check",
      "to": "self::test_public_gonol_exact_and_unclassified"
    },
    {
      "from": "public_gonol_geometry_check",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "public_gonol_geometry_check",
      "to": "every_public_gonol_glyph_is_a_function_position"
    },
    {
      "from": "public_gonol_geometry_check",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "public_gonol_geometry_check",
      "to": "public_gonol_has_exactly_157_unique_positions"
    },
    {
      "from": "public_gonol_geometry_check",
      "kind": "requires",
      "source_block": "CHECKS",
      "source_id": "public_gonol_geometry_check",
      "to": "python3"
    },
    {
      "from": "directed_carrier_floor",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "directed_carrier_floor",
      "to": "Erin Spencer"
    },
    {
      "from": "directed_carrier_floor",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "directed_carrier_floor",
      "to": "canonical_chapter_one"
    },
    {
      "from": "skill_lib_boundary_runner",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "skill_lib_boundary_runner",
      "to": "Erin Spencer"
    },
    {
      "from": "skill_lib_boundary_runner",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "skill_lib_boundary_runner",
      "to": "skill_lib_contract_audit"
    },
    {
      "from": "skill_lib_contract_audit",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "skill_lib_contract_audit",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_geometry_public_surface",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_geometry_public_surface",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_geometry_public_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_geometry_public_surface",
      "to": "directed_carrier_floor"
    },
    {
      "from": "ucns_geometry_public_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_geometry_public_surface",
      "to": "ucns_mobius_seed_of_life_candidate"
    },
    {
      "from": "ucns_geometry_public_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_geometry_public_surface",
      "to": "ucns_mobius_vesica_candidate"
    },
    {
      "from": "ucns_geometry_public_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_geometry_public_surface",
      "to": "ucns_native_mobius_geometry"
    },
    {
      "from": "ucns_geometry_public_surface",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_geometry_public_surface",
      "to": "ucns_public_gonol_geometry"
    },
    {
      "from": "ucns_mobius_seed_global_compatibility",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mobius_seed_global_compatibility",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_mobius_seed_global_compatibility",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mobius_seed_global_compatibility",
      "to": "ucns_mobius_seed_of_life_candidate"
    },
    {
      "from": "ucns_mobius_seed_global_compatibility",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mobius_seed_global_compatibility",
      "to": "ucns_mobius_vesica_continuation"
    },
    {
      "from": "ucns_mobius_seed_of_life_candidate",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mobius_seed_of_life_candidate",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_mobius_seed_of_life_candidate",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mobius_seed_of_life_candidate",
      "to": "edcm_native_direct_mobius_candidate"
    },
    {
      "from": "ucns_mobius_seed_of_life_candidate",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mobius_seed_of_life_candidate",
      "to": "ucns_gonol_relationship_display_v1"
    },
    {
      "from": "ucns_mobius_vesica_certificates",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mobius_vesica_certificates",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_mobius_vesica_certificates",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mobius_vesica_certificates",
      "to": "ucns_mobius_vesica_exact_embedding"
    },
    {
      "from": "ucns_mobius_vesica_continuation",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mobius_vesica_continuation",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_mobius_vesica_continuation",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mobius_vesica_continuation",
      "to": "ucns_mobius_seed_of_life_candidate"
    },
    {
      "from": "ucns_mobius_vesica_continuation",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mobius_vesica_continuation",
      "to": "ucns_mobius_vesica_certificates"
    },
    {
      "from": "ucns_mobius_vesica_exact_embedding",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mobius_vesica_exact_embedding",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_mobius_vesica_exact_embedding",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mobius_vesica_exact_embedding",
      "to": "ucns_mobius_seed_of_life_candidate"
    },
    {
      "from": "ucns_mpfr_interval",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mpfr_interval",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_mpfr_interval",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_mpfr_interval",
      "to": "system libmpfr"
    },
    {
      "from": "ucns_native_mobius_geometry",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_native_mobius_geometry",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_native_mobius_geometry",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_native_mobius_geometry",
      "to": "none"
    },
    {
      "from": "ucns_prime_boundary_link_invariants",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_boundary_link_invariants",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_boundary_link_invariants",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_boundary_link_invariants",
      "to": "ucns_prime_interval_boundary_links_p7_p5"
    },
    {
      "from": "ucns_prime_determinantal_grobner_p7_p5",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_determinantal_grobner_p7_p5",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_determinantal_grobner_p7_p5",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_determinantal_grobner_p7_p5",
      "to": "sympy==1.14.0"
    },
    {
      "from": "ucns_prime_determinantal_grobner_p7_p5",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_determinantal_grobner_p7_p5",
      "to": "ucns_prime_symbolic_alexander_p7_p5"
    },
    {
      "from": "ucns_prime_exact_milnor_alexander_p7_p5",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_exact_milnor_alexander_p7_p5",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_exact_milnor_alexander_p7_p5",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_exact_milnor_alexander_p7_p5",
      "to": "mpmath>=1.3"
    },
    {
      "from": "ucns_prime_exact_milnor_alexander_p7_p5",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_exact_milnor_alexander_p7_p5",
      "to": "ucns_prime_independent_phase_milnor_p7_p5"
    },
    {
      "from": "ucns_prime_generic_diagram",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_generic_diagram",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_generic_diagram",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_generic_diagram",
      "to": "ucns_prime_interval_boundary_links_p7_p5"
    },
    {
      "from": "ucns_prime_generic_interval_certificate",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_generic_interval_certificate",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_generic_interval_certificate",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_generic_interval_certificate",
      "to": "ucns_mpfr_interval"
    },
    {
      "from": "ucns_prime_generic_interval_certificate",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_generic_interval_certificate",
      "to": "ucns_prime_exact_milnor_alexander_p7_p5"
    },
    {
      "from": "ucns_prime_independent_phase_milnor",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_independent_phase_milnor",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_independent_phase_milnor",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_independent_phase_milnor",
      "to": "ucns_mpfr_interval"
    },
    {
      "from": "ucns_prime_independent_phase_milnor",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_independent_phase_milnor",
      "to": "ucns_prime_smooth_ribbons_p7_p5"
    },
    {
      "from": "ucns_prime_interval_boundaries_p7_p5",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_interval_boundaries_p7_p5",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_interval_boundaries_p7_p5",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_interval_boundaries_p7_p5",
      "to": "mpmath>=1.3"
    },
    {
      "from": "ucns_prime_interval_boundaries_p7_p5",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_interval_boundaries_p7_p5",
      "to": "ucns_prime_smooth_ribbons_p7_p5"
    },
    {
      "from": "ucns_prime_interval_boundary_links_p7_p5",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_interval_boundary_links_p7_p5",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_interval_boundary_links_p7_p5",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_interval_boundary_links_p7_p5",
      "to": "ucns_prime_smooth_ribbons_p7_p5"
    },
    {
      "from": "ucns_prime_interval_common",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_interval_common",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_interval_common",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_interval_common",
      "to": "ucns_prime_smooth_ribbons_p7_p5"
    },
    {
      "from": "ucns_prime_interval_replay",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_interval_replay",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_interval_replay",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_interval_replay",
      "to": "ucns_prime_interval_common"
    },
    {
      "from": "ucns_prime_length4_milnor_p7",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_length4_milnor_p7",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_length4_milnor_p7",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_length4_milnor_p7",
      "to": "ucns_prime_exact_milnor_alexander_p7_p5"
    },
    {
      "from": "ucns_prime_milnor_invariants",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_milnor_invariants",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_milnor_invariants",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_milnor_invariants",
      "to": "ucns_prime_generic_diagram"
    },
    {
      "from": "ucns_prime_nilpotent_discriminator_p7_p5",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_nilpotent_discriminator_p7_p5",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_nilpotent_discriminator_p7_p5",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_nilpotent_discriminator_p7_p5",
      "to": "GAP 4.12.1"
    },
    {
      "from": "ucns_prime_nilpotent_discriminator_p7_p5",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_nilpotent_discriminator_p7_p5",
      "to": "NQ 2.5.11"
    },
    {
      "from": "ucns_prime_nilpotent_discriminator_p7_p5",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_nilpotent_discriminator_p7_p5",
      "to": "ucns_prime_exact_milnor_alexander_p7_p5"
    },
    {
      "from": "ucns_prime_phase_lift_data",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_phase_lift_data",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_phase_lift_data",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_phase_lift_data",
      "to": "ucns_prime_primitives_p7_p5"
    },
    {
      "from": "ucns_prime_phase_lift_model",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_phase_lift_model",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_phase_lift_model",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_phase_lift_model",
      "to": "ucns_prime_phase_lift_data"
    },
    {
      "from": "ucns_prime_phase_lift_model",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_phase_lift_model",
      "to": "ucns_prime_primitives_p7_p5"
    },
    {
      "from": "ucns_prime_phase_lift_p7_p5",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_phase_lift_p7_p5",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_phase_lift_p7_p5",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_phase_lift_p7_p5",
      "to": "ucns_prime_primitives_p7_p5"
    },
    {
      "from": "ucns_prime_primitives_p7_p5",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_primitives_p7_p5",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_primitives_p7_p5",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_primitives_p7_p5",
      "to": "none"
    },
    {
      "from": "ucns_prime_replay_phase_milnor_data",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_replay_phase_milnor_data",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_replay_phase_milnor_data",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_replay_phase_milnor_data",
      "to": "ucns_prime_smooth_ribbons_p7_p5"
    },
    {
      "from": "ucns_prime_replay_phase_milnor_receipt",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_replay_phase_milnor_receipt",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_replay_phase_milnor_receipt",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_replay_phase_milnor_receipt",
      "to": "ucns_prime_smooth_ribbons_p7_p5"
    },
    {
      "from": "ucns_prime_smooth_ribbons_p7_p5",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_smooth_ribbons_p7_p5",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_smooth_ribbons_p7_p5",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_smooth_ribbons_p7_p5",
      "to": "ucns_prime_phase_lift_p7_p5"
    },
    {
      "from": "ucns_prime_symbolic_alexander_p7_p5",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_symbolic_alexander_p7_p5",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_prime_symbolic_alexander_p7_p5",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_symbolic_alexander_p7_p5",
      "to": "<2"
    },
    {
      "from": "ucns_prime_symbolic_alexander_p7_p5",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_symbolic_alexander_p7_p5",
      "to": "sympy>=1.12"
    },
    {
      "from": "ucns_prime_symbolic_alexander_p7_p5",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_prime_symbolic_alexander_p7_p5",
      "to": "ucns_prime_exact_milnor_alexander_p7_p5"
    },
    {
      "from": "ucns_public_gonol_geometry",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_public_gonol_geometry",
      "to": "Erin Spencer"
    },
    {
      "from": "ucns_public_gonol_geometry",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "ucns_public_gonol_geometry",
      "to": "none"
    }
  ],
  "gaps": [],
  "repo": "The-Interdependency/ucns",
  "source_commit": "The-Interdependency/skill-lib@a1c6a7124af537ee9937b6fc6084940091982fe5"
});
