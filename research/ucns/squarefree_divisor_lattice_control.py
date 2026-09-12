"""Squarefree divisor-lattice control for recursive gonol observations.

This module classifies the three observed gonol cardinalities by exact integer
factorization.  It preregisters only the structural next observation
``omega=4, tau=16, mu=+1`` (equivalently a squarefree ``B_4`` divisor lattice),
not a numerical successor.  It also audits whether the current executable UCNS
research mechanics derive that structure.  They do not: the mapping from
recursive gonol geometry to independent multiplicative factors remains absent.
"""

# === MODULE_BUILD ===
# id: ucns_squarefree_divisor_lattice_control
#   module_name: squarefree_divisor_lattice_control
#   module_kind: experiment
#   summary: freezes exact squarefree divisor-lattice witnesses for the three observed gonols, preregisters a nonnumeric B4 control, and audits whether current UCNS mechanics derive one added prime-factor dimension per scale
#   owner: The Interdependency
#   public_surface: OBSERVED_GONOLS, StructuralControl, DivisorLatticeWitness, MechanicsDimensionAudit, StructuralComparison, factor_integer, analyze_integer, observed_witnesses, structural_control, audit_ucns_mechanics, compare_actual_next, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _stack_root, _canonical_bytes, _load_json, _file_digest, _source_file_digests, _validated_positive_integer, _divisors, _subset_products, _rank_counts, _producer_code_reference, main
#   auth_boundary: none; reads stack-pinned UCNS authority and stack-local UCNS research mechanics only
#   storage_boundary: read-only at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_squarefree_divisor_lattice_control.py
#   rollout: stack-local post-observation structural control only; no UCNS canon, stack libs, or PCEA promotion
#   rollback: remove this module, its tests, report, and receipt
#   requires: ucns_public_gonol_geometry, ucns_prime_primitives_p7_p5, ucns_public_gonol_functional_operations, ucns_affinization_coupling_geometry, ucns_recursive_scale_transition, ucns_event_pair_quotient_candidate, gonol-build construction discipline
#   since: 2026-09-02
#   unresolved: whether gonol cardinality has geometric factor semantics; whether closed gonols decompose into independent multiplicative components; why apparent divisor-lattice rank increases by one while event-pair recursion fails; numerical value of the next gonol
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: squarefree_control_factors_observations_exactly
#   given: the three external gonol observations are classified
#   then: exact trial factorization reconstructs each value from prime factors without interpolation or a successor formula
#   class: correctness
#   since: 2026-09-02
#
# id: squarefree_control_witnesses_boolean_divisor_lattices
#   given: the exact observed factorizations are analyzed
#   then: the values are squarefree with omega 1, 2, 3; tau 2, 4, 8; mu -1, +1, -1; and divisor lattices B1, B2, B3
#   class: evidence
#   since: 2026-09-02
#
# id: squarefree_control_preregisters_structure_not_number
#   given: the observed B1 to B2 to B3 pattern is frozen before any fourth observation
#   then: the control predicts squarefree B4 with omega 4, tau 16, and mu +1 while numerical_value remains null
#   class: doctrine
#   since: 2026-09-02
#
# id: squarefree_control_has_out_of_sample_falsification_gate
#   given: an actual fourth gonol is later supplied
#   then: exact factor analysis returns SURVIVED_ONE_OUT_OF_SAMPLE_TEST only for the full preregistered invariant tuple and FALSIFIED otherwise
#   class: correctness
#   since: 2026-09-02
#
# id: squarefree_control_does_not_upgrade_arithmetic_to_ucns_mechanics
#   given: current executable UCNS research mechanics are audited
#   then: fixed-carrier transformations, caller-declared coupling arity, and whole-to-atom promotion are distinguished from an undeclared product decomposition or added-prime-dimension law, leaving explanation status UNRESOLVED
#   class: safety
#   since: 2026-09-02
#
# id: squarefree_control_retains_failed_local_mechanism
#   given: the structural control receipt is built
#   then: the exact 39 to 720 event-pair identity and its unchanged 720 to 258819 failure remain bound as a falsified local mechanism rather than discarded
#   class: evidence
#   since: 2026-09-02
#
# id: squarefree_control_receipt_replays
#   given: the same pinned sources and observations are evaluated twice
#   then: canonical receipt bytes and their digest replay byte-identically
#   class: correctness
#   since: 2026-09-02
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
import json
from math import prod
from pathlib import Path
from typing import Any

import affinization_coupling_geometry as acg
import composed_successor_constructor as composed
import event_pair_quotient_candidate as event_pair
import public_gonol_functional_operations as pgfo
import recursive_scale_transition as rst


SCHEMA_ID = "the-interdependency.stack-research.ucns.squarefree-divisor-lattice-control"
SCHEMA_VERSION = "0.1.0"
STANDING = "PREREGISTERED_STRUCTURAL_CONTROL"
SELECTION_EFFECT = "none"
PINNED_UCNS_COMMIT = "1975fe70cf4e0826a8020c2da3047569e277af64"

OBSERVED_GONOLS: tuple[int, int, int] = (157, 2881, 54837698421)
STATUS_PENDING = "PENDING_FOURTH_OBSERVATION"
STATUS_FALSIFIED = "FALSIFIED"
STATUS_SURVIVED_ONE = "SURVIVED_ONE_OUT_OF_SAMPLE_TEST"
MECHANICS_STATUS = "UNRESOLVED_NO_DECLARED_FACTOR_MAPPING"

NONCLAIMS: tuple[str, ...] = (
    "not UCNS canon",
    "not a recovered or surviving gonol successor constructor",
    "not a numerical prediction for the fourth gonol",
    "not evidence that arithmetic factors are UCNS geometric components",
    "not evidence that divisor-lattice independence is geometric independence",
    "not PCEA key, entropy, hardness, replay-resistance, recovery, or public-authenticity evidence",
)

HMMM: tuple[str, ...] = (
    "39 to 720 is retained as an exact but nonrecursive local accounting mechanism: C(39,2)-21=720, while the unchanged next step is 258819 and the lifted gonol is 1035277",
    "the observed cardinalities have squarefree divisor lattices B1, B2, and B3, but this is post-observation arithmetic classification rather than UCNS construction",
    "independent prime-factor dimension currently means Boolean divisor-lattice rank only; geometric independence has not been established",
    "current UCNS mechanics do not declare a product decomposition of a closed gonol, a prime label for each component, or a transition that preserves all factors and adds one new factor",
    "the live question is why apparent divisor-lattice rank increases by one while the obvious event-pair construction fails to recurse",
    "the numerical value and prime factors of the fourth gonol remain unresolved",
)

FALSIFICATION_CONDITIONS: tuple[str, ...] = (
    "any frozen observed factorization fails exact multiplication or primality replay",
    "any observed value is not squarefree or does not have the recorded omega, tau, and mu invariants",
    "the fourth observed gonol is not squarefree with exactly four distinct prime factors",
    "the fourth observed gonol has tau other than 16 or number-theoretic mu other than +1",
    "the structural control is later presented as a numerical successor prediction or as a UCNS-derived constructor",
    "a claimed UCNS explanation cannot execute a product decomposition and one-new-independent-factor transition without target-derived tuning",
)

PROMOTION_EVIDENCE: tuple[str, ...] = (
    "define a UCNS geometric decomposition whose independent component cardinalities multiply to each gonol cardinality",
    "identify each component and its arithmetic-prime cardinality from geometry rather than from post-observation factorization",
    "execute one unchanged recursive transition that preserves prior components and adds exactly one independently derived component",
    "reconstruct 157, 2881, and 54837698421 under that transition and freeze the fourth numerical output before comparison",
    "survive the fourth observation while keeping arithmetic primality separate from UCNS primitive standing",
)


class SquarefreeControlError(ValueError):
    """Raised when structural-control inputs or pinned provenance are invalid."""


def _stack_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _file_digest(root: Path, relative_path: str) -> tuple[str, str]:
    return (relative_path, sha256((root / relative_path).read_bytes()).hexdigest())


def _source_file_digests(root: Path) -> tuple[tuple[str, str], ...]:
    return tuple(
        _file_digest(root, path)
        for path in (
            "research/ucns/BASE.json",
            "stack-manifest.json",
            "libs/ucns/CANON.md",
            "libs/ucns/docs/GEOMETRY.md",
            "libs/ucns/src/ucns/carrier.py",
            "libs/ucns/src/ucns/public_gonol.py",
            "libs/ucns/src/ucns/prime_primitives.py",
            "research/ucns/public_gonol_functional_operations.py",
            "research/ucns/affinization_coupling_geometry.py",
            "research/ucns/recursive_scale_transition.py",
            "research/ucns/composed_successor_constructor.py",
            "research/ucns/event_pair_quotient_candidate.py",
        )
    )


def _validated_positive_integer(value: int, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise SquarefreeControlError(f"{field} must be a positive integer")
    return value


def factor_integer(value: int) -> tuple[tuple[int, int], ...]:
    """Return an exact prime-exponent factorization by deterministic division."""

    remaining = _validated_positive_integer(value, "value")
    factors: list[tuple[int, int]] = []
    divisor = 2
    while divisor * divisor <= remaining:
        exponent = 0
        while remaining % divisor == 0:
            remaining //= divisor
            exponent += 1
        if exponent:
            factors.append((divisor, exponent))
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors.append((remaining, 1))
    return tuple(factors)


def _divisors(factorization: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    values = [1]
    for prime, exponent in factorization:
        prior = tuple(values)
        power = 1
        for _ in range(exponent):
            power *= prime
            values.extend(value * power for value in prior)
    return tuple(sorted(values))


def _subset_products(
    factorization: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, int, int], ...]:
    if any(exponent != 1 for _, exponent in factorization):
        return ()
    primes = tuple(prime for prime, _ in factorization)
    rows = []
    for mask in range(1 << len(primes)):
        chosen = tuple(prime for index, prime in enumerate(primes) if mask & (1 << index))
        rows.append((mask, prod(chosen, start=1), len(chosen)))
    return tuple(rows)


def _rank_counts(rows: tuple[tuple[int, int, int], ...]) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for _, _, rank in rows:
        counts[rank] = counts.get(rank, 0) + 1
    return tuple(sorted(counts.items()))


@dataclass(frozen=True, slots=True)
class DivisorLatticeWitness:
    """Exact arithmetic witness for one observed gonol cardinality."""

    observation_index: int
    value: int
    factorization: tuple[tuple[int, int], ...]
    squarefree: bool
    omega: int
    tau: int
    mobius_mu: int
    divisors: tuple[int, ...]
    subset_products: tuple[tuple[int, int, int], ...]
    lattice_name: str | None
    lattice_rank_counts: tuple[tuple[int, int], ...]

    def to_payload(self) -> dict[str, Any]:
        return {
            "observation_index": self.observation_index,
            "value": self.value,
            "factorization": [
                {"prime": prime, "exponent": exponent}
                for prime, exponent in self.factorization
            ],
            "reconstructed_value": prod(
                (prime**exponent for prime, exponent in self.factorization),
                start=1,
            ),
            "squarefree": self.squarefree,
            "omega": self.omega,
            "tau": self.tau,
            "mobius_mu": self.mobius_mu,
            "divisors": list(self.divisors),
            "divisor_lattice": {
                "name": self.lattice_name,
                "rank": self.omega if self.squarefree else None,
                "rank_counts": [
                    {"rank": rank, "count": count}
                    for rank, count in self.lattice_rank_counts
                ],
                "subset_product_bijection": [
                    {"subset_mask": mask, "divisor": divisor, "rank": rank}
                    for mask, divisor, rank in self.subset_products
                ],
            },
        }


def analyze_integer(value: int, *, observation_index: int = 0) -> DivisorLatticeWitness:
    """Compute exact factor, divisor, Mobius, and Boolean-lattice invariants."""

    _validated_positive_integer(value, "value")
    if isinstance(observation_index, bool) or not isinstance(observation_index, int) or observation_index < 0:
        raise SquarefreeControlError("observation_index must be a nonnegative integer")
    factorization = factor_integer(value)
    reconstructed = prod((prime**exponent for prime, exponent in factorization), start=1)
    if reconstructed != value:
        raise SquarefreeControlError("factorization does not reconstruct input")
    squarefree = all(exponent == 1 for _, exponent in factorization)
    omega = len(factorization)
    tau = prod((exponent + 1 for _, exponent in factorization), start=1)
    mobius_mu = 0 if not squarefree else (-1 if omega % 2 else 1)
    divisors = _divisors(factorization)
    rows = _subset_products(factorization)
    if len(divisors) != tau:
        raise SquarefreeControlError("divisor enumeration disagrees with tau")
    if squarefree and tuple(sorted(divisor for _, divisor, _ in rows)) != divisors:
        raise SquarefreeControlError("subset products do not biject with squarefree divisors")
    return DivisorLatticeWitness(
        observation_index=observation_index,
        value=value,
        factorization=factorization,
        squarefree=squarefree,
        omega=omega,
        tau=tau,
        mobius_mu=mobius_mu,
        divisors=divisors,
        subset_products=rows,
        lattice_name=f"B_{omega}" if squarefree else None,
        lattice_rank_counts=_rank_counts(rows),
    )


@lru_cache(maxsize=1)
def observed_witnesses() -> tuple[DivisorLatticeWitness, ...]:
    """Return the frozen exact arithmetic witnesses for observations one to three."""

    return tuple(
        analyze_integer(value, observation_index=index)
        for index, value in enumerate(OBSERVED_GONOLS, start=1)
    )


@dataclass(frozen=True, slots=True)
class StructuralControl:
    """Nonnumeric fourth-observation control frozen from B1 -> B2 -> B3."""

    observation_index: int
    numerical_value: None
    squarefree: bool
    omega: int
    tau: int
    mobius_mu: int
    lattice_name: str
    standing: str
    basis: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "observation_index": self.observation_index,
            "numerical_value": self.numerical_value,
            "squarefree": self.squarefree,
            "omega": self.omega,
            "tau": self.tau,
            "mobius_mu": self.mobius_mu,
            "divisor_lattice": self.lattice_name,
            "standing": self.standing,
            "basis": self.basis,
        }


def structural_control() -> StructuralControl:
    """Return the preregistered fourth-observation structural control."""

    witnesses = observed_witnesses()
    if tuple(witness.omega for witness in witnesses) != (1, 2, 3):
        raise SquarefreeControlError("observed omega sequence changed")
    if not all(witness.squarefree for witness in witnesses):
        raise SquarefreeControlError("observed squarefree standing changed")
    return StructuralControl(
        observation_index=4,
        numerical_value=None,
        squarefree=True,
        omega=4,
        tau=16,
        mobius_mu=1,
        lattice_name="B_4",
        standing=STANDING,
        basis="post-observation structural extrapolation from exact B_1 -> B_2 -> B_3 divisor lattices",
    )


@dataclass(frozen=True, slots=True)
class MechanicsDimensionAudit:
    """Executable boundary audit for factor semantics in current mechanics."""

    public_gonol_arity: int
    mechanic1_identity_output_arity: int
    mechanic1_cyclic_output_arity: int
    mechanic1_preserves_fixed_carrier: bool
    mechanic2_sample_coupling_arity: int
    mechanic2_explicit_three_participant_arity: int
    mechanic2_arity_source: str
    mechanic3_promoted_atomic_participants: int
    mechanic3_next_carrier_cardinality: int | None
    composed_first_output: int
    composed_first_target: int
    composed_status: str
    declared_product_decomposition_operation: bool
    declared_arithmetic_factor_to_geometry_operation: bool
    declared_add_one_prime_dimension_transition: bool
    explanation_status: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "public_gonol_arity": self.public_gonol_arity,
            "mechanic_1": {
                "identity_output_arity": self.mechanic1_identity_output_arity,
                "cyclic_output_arity": self.mechanic1_cyclic_output_arity,
                "preserves_fixed_carrier": self.mechanic1_preserves_fixed_carrier,
                "cardinality_effect": "fixed n -> n over the pinned 157-position carrier",
            },
            "mechanic_2": {
                "sample_coupling_arity": self.mechanic2_sample_coupling_arity,
                "explicit_three_participant_arity": self.mechanic2_explicit_three_participant_arity,
                "arity_source": self.mechanic2_arity_source,
                "cardinality_effect": "arity equals the explicit caller-supplied participant tuple",
            },
            "mechanic_3": {
                "promoted_atomic_participants": self.mechanic3_promoted_atomic_participants,
                "next_carrier_cardinality": self.mechanic3_next_carrier_cardinality,
                "cardinality_effect": "one closed affinization -> one atomic participant; next carrier size is not defined",
            },
            "smallest_composed_constructor": {
                "first_input": OBSERVED_GONOLS[0],
                "first_output": self.composed_first_output,
                "first_target": self.composed_first_target,
                "status": self.composed_status,
            },
            "declared_product_decomposition_operation": self.declared_product_decomposition_operation,
            "declared_arithmetic_factor_to_geometry_operation": self.declared_arithmetic_factor_to_geometry_operation,
            "declared_add_one_prime_dimension_transition": self.declared_add_one_prime_dimension_transition,
            "explanation_status": self.explanation_status,
        }


@lru_cache(maxsize=1)
def audit_ucns_mechanics() -> MechanicsDimensionAudit:
    """Audit declared cardinality effects without inventing factor semantics."""

    carrier = pgfo.load_carrier()
    identity = pgfo.identity_operation(carrier)
    cyclic = pgfo.cyclic_order_motion(1, carrier)
    sample_affinization = acg.sample_public_operation_affinization()
    digest = sha256(b"squarefree-control-explicit-arity-audit").hexdigest()
    explicit_three = acg.coupling(
        "squarefree-control.explicit-three-participant-audit",
        tuple(
            acg.CouplingParticipant(
                participant_id=f"squarefree-control.audit.occurrence-{index}",
                scale="audit-only",
                role=f"slot-{index}",
                source_digest=digest,
            )
            for index in range(3)
        ),
        source_refs=("research.ucns.squarefree-divisor-lattice-control.audit",),
    )
    promoted = rst.sample_recursive_transition()
    first = composed.construct_successor_once(OBSERVED_GONOLS[0], sample_limit=0)
    composed_status = (
        composed.STATUS_SURVIVED_FIRST
        if first.output_size == OBSERVED_GONOLS[1]
        else composed.STATUS_FALSIFIED
    )
    return MechanicsDimensionAudit(
        public_gonol_arity=carrier.arity,
        mechanic1_identity_output_arity=len(identity.transform),
        mechanic1_cyclic_output_arity=len(cyclic.transform),
        mechanic1_preserves_fixed_carrier=(
            identity.is_bijective
            and cyclic.is_bijective
            and len(identity.transform) == carrier.arity
            and len(cyclic.transform) == carrier.arity
        ),
        mechanic2_sample_coupling_arity=sample_affinization.coupling.arity,
        mechanic2_explicit_three_participant_arity=explicit_three.arity,
        mechanic2_arity_source="explicit caller-supplied ordered participant tuple",
        mechanic3_promoted_atomic_participants=1 if promoted.atomic_participant else 0,
        mechanic3_next_carrier_cardinality=None,
        composed_first_output=first.output_size,
        composed_first_target=OBSERVED_GONOLS[1],
        composed_status=composed_status,
        declared_product_decomposition_operation=False,
        declared_arithmetic_factor_to_geometry_operation=False,
        declared_add_one_prime_dimension_transition=False,
        explanation_status=MECHANICS_STATUS,
    )


@dataclass(frozen=True, slots=True)
class StructuralComparison:
    """Later out-of-sample comparison against the frozen structural control."""

    status: str
    actual: DivisorLatticeWitness
    control: StructuralControl
    mismatches: tuple[str, ...]

    def to_payload(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "actual": self.actual.to_payload(),
            "control": self.control.to_payload(),
            "mismatches": list(self.mismatches),
            "claim_boundary": "tests the structural control only; does not validate a gonol constructor",
        }


def compare_actual_next(actual_value: int) -> StructuralComparison:
    """Compare a later fourth observation with the frozen nonnumeric control."""

    actual = analyze_integer(actual_value, observation_index=4)
    control = structural_control()
    mismatches = []
    if actual.squarefree != control.squarefree:
        mismatches.append("squarefree")
    if actual.omega != control.omega:
        mismatches.append("omega")
    if actual.tau != control.tau:
        mismatches.append("tau")
    if actual.mobius_mu != control.mobius_mu:
        mismatches.append("mobius_mu")
    if actual.lattice_name != control.lattice_name:
        mismatches.append("divisor_lattice")
    return StructuralComparison(
        status=STATUS_FALSIFIED if mismatches else STATUS_SURVIVED_ONE,
        actual=actual,
        control=control,
        mismatches=tuple(mismatches),
    )


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_bytes()).hexdigest()


def receipt_payload() -> dict[str, Any]:
    """Return the deterministic structural-control preregistration receipt."""

    root = _stack_root()
    base = _load_json(root / "research" / "ucns" / "BASE.json")
    if base["source_commit"] != PINNED_UCNS_COMMIT:
        raise SquarefreeControlError("UCNS source commit mismatch")
    local_failure = event_pair.evaluate()
    if local_failure.status != event_pair.STATUS_FALSIFIED:
        raise SquarefreeControlError("event-pair predecessor standing changed")
    witnesses = observed_witnesses()
    control = structural_control()
    audit = audit_ucns_mechanics()
    frozen_mechanics = composed.freeze_mechanics()
    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "producer_code_reference": _producer_code_reference(),
        "source": {
            "authority": "The-Interdependency/ucns",
            "ucns_base_commit": base["source_commit"],
            "source_file_digests": [
                {"path": path, "sha256": digest}
                for path, digest in _source_file_digests(root)
            ],
            "frozen_mechanics": [item.to_payload() for item in frozen_mechanics],
        },
        "observations": [witness.to_payload() for witness in witnesses],
        "theorem_used": {
            "statement": "the positive divisors of a squarefree integer with k distinct prime factors form a Boolean lattice B_k under divisibility",
            "witness": "subset masks map bijectively to products of selected distinct prime factors",
            "scope": "elementary integer arithmetic only; no UCNS geometric interpretation is transferred",
        },
        "structural_control": control.to_payload(),
        "comparison": {
            "status": STATUS_PENDING,
            "actual_fourth_value": None,
            "falsified_if": "the full squarefree=true, omega=4, tau=16, mu=+1, divisor_lattice=B_4 tuple fails",
            "survives_if": "the full tuple matches one independently obtained fourth observation",
            "claim_boundary": "one match would let this structural control survive one out-of-sample test; it would not recover a constructor",
        },
        "mechanics_audit": audit.to_payload(),
        "retained_falsified_local_mechanism": {
            "producer_path": "research/ucns/event_pair_quotient_candidate.py",
            "producer_sha256": sha256(Path(event_pair.__file__).read_bytes()).hexdigest(),
            "receipt_sha256": event_pair.receipt_digest(),
            "first_local_state": local_failure.event_state_count,
            "first_relation_constraint_rank": local_failure.relation_constraint_rank,
            "first_output_state": local_failure.first_quotient_state,
            "first_lifted_gonol": local_failure.first_lifted_gonol,
            "unchanged_second_output_state": local_failure.second_quotient_state,
            "unchanged_second_lifted_gonol": local_failure.second_lifted_gonol,
            "status": local_failure.status,
            "standing": "useful falsified local mechanism, not recursive law",
        },
        "promotion_evidence": list(PROMOTION_EVIDENCE),
        "falsification_conditions": list(FALSIFICATION_CONDITIONS),
        "hmmm": list(HMMM),
        "nonclaims": list(NONCLAIMS),
    }


def receipt_bytes() -> bytes:
    return _canonical_bytes(receipt_payload()) + b"\n"


def receipt_digest() -> str:
    return sha256(receipt_bytes()).hexdigest()


def main() -> None:
    payload = receipt_payload()
    payload["receipt_sha256"] = receipt_digest()
    print(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
