"""Explicit METAPAT authority, runtime-data, and proof-status flows.

Usage guidance
--------------
Consumers may display these constants or use them in architecture checks. They
are declarations of responsibility, not runtime execution or empirical proof.
"""

# === MODULE_BUILD ===
# id: metapat_flow_plan
#   module_name: metapat.flow_plan
#   module_kind: schema
#   summary: separates METAPAT semantic authority flow, EDCM/UCNS runtime data flow, and proof-status non-transfer
#   owner: The Interdependency
#   public_surface: AUTHORITY_FLOW, RUNTIME_DATA_FLOW, PROOF_STATUS_FLOW, UCNS_SIDE_STATUS, EDCM_SIDE_STATUS
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_contracts, tests.test_envelope, tests.test_ucns_bridge
#   rollout: documentation_and_contract
#   rollback: restore prior architecture declarations
#   requires: metapat_module_envelope, metapat_ucns_adapter
#   since: 2026-07-12
#   unresolved: EDCM consumer implementation and shared-stack result envelope until merged cross-repository
# === END MODULE_BUILD ===

# === CAPABILITIES ===
# id: metapat_flow_status
#   summary: exposes distinct authority, runtime-data, and proof-status architecture declarations
#   exposes: metapat.flow_plan.AUTHORITY_FLOW, metapat.flow_plan.RUNTIME_DATA_FLOW, metapat.flow_plan.PROOF_STATUS_FLOW
#   inputs: none
#   outputs: str
#   boundaries: auth:none, storage:none, network:none, user_data:none
# === END CAPABILITIES ===

# === DEPENDENCIES ===
# id: metapat_flow_edges
#   summary: METAPAT constrains interpretation while actual UCNS carries geometry and EDCM measures source evidence
#   internal: metapat.envelope, metapat.ucns
#   external: The-Interdependency/ucns, The-Interdependency/edcm
#   provides: metapat_flow_plan
#   class: architecture
#   direction: authority and runtime data are separate
#   owner: The Interdependency
# === END DEPENDENCIES ===

# === OWNERS ===
# id: metapat_flow_owner
#   owner: The Interdependency
#   steward: Erin Spencer
#   review_required_for: dependency, public_api, canon
#   escalation: hmmm
# === END OWNERS ===

# === BOUNDARIES ===
# id: metapat_flow_boundaries
#   summary: architecture status constants with no active external calls
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
# === END BOUNDARIES ===

AUTHORITY_FLOW = """METAPAT canon
    |
    +-- constrains terms, interpretation, allowed derivations, and claim status
    v
UCNS adapters and EDCM consumers"""

RUNTIME_DATA_FLOW = """source evidence -> EDCM parsing -> actual UCNS representation -> EDCM readouts
                                     ^
                                     |
                          METAPAT-derived semantic constraints"""

PROOF_STATUS_FLOW = (
    "UCNS theorem or domain status remains UCNS evidence and does not transfer "
    "into METAPAT ontology validity or EDCM measurement validity."
)

UCNS_SIDE_STATUS = (
    "implemented: optional adapter constructs actual ucns.UCNSObject geometry; "
    "METAPAT statements remain external provenance; no local UCNS algebra"
)
EDCM_SIDE_STATUS = (
    "hmmm: immutable MetapatModuleEnvelope is implemented; EDCM consumer and "
    "shared-stack fixture must be merged in The-Interdependency/edcm"
)

__all__ = [
    "AUTHORITY_FLOW",
    "RUNTIME_DATA_FLOW",
    "PROOF_STATUS_FLOW",
    "UCNS_SIDE_STATUS",
    "EDCM_SIDE_STATUS",
]
