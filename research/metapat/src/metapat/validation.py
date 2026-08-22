"""Deterministic METAPAT canon contract checks.

These helpers test encoded conditions associated with current METAPAT
statements. A ``True`` result means only that the supplied Python values satisfy
the named deterministic condition. It does not empirically validate Meta
Energy Theory, formally prove the ontology, or transfer UCNS theorem status.
"""

# === MODULE_BUILD ===
# id: metapat_canon_contract_checks
#   module_name: metapat.validation
#   module_kind: service
#   summary: deterministic canon contract checks retained at the compatibility module path; not theorem verification or empirical validation
#   owner: The Interdependency
#   public_surface: boundary_earns_its_keep, tensor_precedes_time, registration_is_not_time, observer_role_by_registration, consciousness_is_optional
#   internal_surface: none
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_contracts
#   rollout: importable_package
#   rollback: restore prior metadata wording without changing function behavior
#   requires: none
#   since: 2026-07-12
#   unresolved: whether a future major version moves these helpers to metapat.contracts
# === END MODULE_BUILD ===

# === DOCS ===
# id: metapat_canon_contract_docs
#   summary: documents deterministic encoded conditions and their non-validation boundary
#   audience: developer
#   source: THEOREMS.md, docs/claims-ledger.md
#   covers: boundary_earns_its_keep, tensor_precedes_time, registration_is_not_time, observer_role_by_registration, consciousness_is_optional
#   status: current
# === END DOCS ===

# === CAPABILITIES ===
# id: metapat_canon_contract_checks
#   summary: checks deterministic Python conditions associated with METAPAT statements without claiming proof or empirical validation
#   exposes: metapat.validation.boundary_earns_its_keep, metapat.validation.tensor_precedes_time, metapat.validation.registration_is_not_time, metapat.validation.observer_role_by_registration, metapat.validation.consciousness_is_optional
#   inputs: source_state, target_state, boundary_state, outcome, tensor_state, sequence, registration, story
#   outputs: bool
#   boundaries: auth:none, storage:none, network:none, user_data:none
# === END CAPABILITIES ===

# === OWNERS ===
# id: metapat_contract_owner
#   owner: The Interdependency
#   steward: Erin Spencer
#   review_required_for: public_api, tests, canon
#   escalation: hmmm
# === END OWNERS ===

# === BOUNDARIES ===
# id: metapat_contract_boundaries
#   summary: pure deterministic conditions; no external effects, theorem verification, or empirical validity claim
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
# === END BOUNDARIES ===

# === CONTRACTS ===
# id: boundary_change_changes_outcome
#   given: source and target are fixed while boundary state changes
#   then: encoded boundary condition passes only when outcome changes
#   class: canon_contract
#
# id: tensor_before_time
#   given: one tensor state and then an ordered pair of tensor states
#   then: encoded tensor-before-sequence condition passes
#   class: canon_contract
#
# id: registration_not_time
#   given: a tensor alteration sequence and an optional registration
#   then: encoded condition allows sequence without registration and checks exact preservation when present
#   class: canon_contract
#
# id: observer_role_requires_registration
#   given: a simplex and a tensor alteration sequence
#   then: encoded observer-role condition passes only when the sequence is registered
#   class: canon_contract
#
# id: consciousness_optional_observer_mode
#   given: non-conscious registration with or without a separate conscious story
#   then: encoded condition requires registration but does not require conscious narrative
#   class: canon_contract
# === END CONTRACTS ===


def boundary_earns_its_keep(
    source_state: object,
    target_state: object,
    boundary_state_a: object,
    boundary_state_b: object,
    outcome_a: object,
    outcome_b: object,
) -> bool:
    if source_state is None or target_state is None:
        return False
    if boundary_state_a == boundary_state_b:
        return False
    return outcome_a != outcome_b


def tensor_precedes_time(tensor_state: object, sequenced_tensor_states: tuple[object, ...]) -> bool:
    if tensor_state is None:
        return False
    return len(sequenced_tensor_states) >= 2


def registration_is_not_time(sequence: tuple[object, ...], registration: object | None) -> bool:
    time_exists = len(sequence) >= 2
    if not time_exists:
        return False
    if registration is None:
        return True
    return tuple(registration) == tuple(sequence) if isinstance(registration, (tuple, list)) else False


def observer_role_by_registration(simplex: dict[str, object], sequence: tuple[object, ...]) -> bool:
    if len(sequence) < 2:
        return False
    registered = simplex.get("registered")
    if registered is None:
        return False
    return tuple(registered) == tuple(sequence) if isinstance(registered, (tuple, list)) else False


def consciousness_is_optional(
    nonconscious_registration: object,
    conscious_story: object | None = None,
) -> bool:
    if nonconscious_registration is None:
        return False
    return conscious_story is None or isinstance(conscious_story, str)


__all__ = [
    "boundary_earns_its_keep",
    "consciousness_is_optional",
    "observer_role_by_registration",
    "registration_is_not_time",
    "tensor_precedes_time",
]
