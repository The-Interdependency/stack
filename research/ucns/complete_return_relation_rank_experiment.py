"""Observation gate for the frozen complete-return relation extension.

The geometric candidate is frozen before this module compares anything.  This
experiment applies it unchanged from the pinned Public Gonol carrier through
three observed scale slots, then once more to freeze the next relation rank.
Observed arithmetic omega values are comparison data only.  Matching ranks do
not supply a map from topological cycles to arithmetic prime factors and do not
produce a numerical successor.
"""

# === MODULE_BUILD ===
# id: ucns_complete_return_relation_rank_experiment
#   module_name: complete_return_relation_rank_experiment
#   module_kind: experiment
#   summary: freezes the target-free complete-return extension, applies it unchanged across observed scale slots, compares generated relation ranks with arithmetic omega only afterward, and preserves the missing factor-cardinality map
#   owner: The Interdependency
#   public_surface: FrozenCandidate, ScaleRankComparison, RelationRankExperiment, freeze_candidate, evaluate, receipt_payload, receipt_bytes, receipt_digest
#   internal_surface: _stack_root, _canonical_bytes, _file_digest, _extension_digest, _producer_code_reference, main
#   auth_boundary: none; consumes one frozen stack-local UCNS geometric candidate and the frozen squarefree divisor-lattice control
#   storage_boundary: read-only at runtime
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_complete_return_relation_rank_experiment.py
#   rollout: stack-local post-observation rank comparison only; no UCNS canon, stack libs, PCEA, factor interpretation, or successor-cardinality promotion
#   rollback: remove this module, its tests, report, and receipt without changing the frozen geometric candidate or structural control
#   requires: ucns_complete_return_relation_extension, ucns_squarefree_divisor_lattice_control, gonol-build construction discipline
#   since: 2026-09-02
#   unresolved: geometric authorization of complete-return attachment at every recursive scale; relation-cycle to arithmetic-factor map; cardinality of a new factor; numerical next gonol
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: complete_return_rank_gate_freezes_candidate_first
#   given: observation-gate evaluation begins
#   then: exact candidate code and receipt identities with validation state NOT_COMPARED are bound before relation outputs or observed omega values are compared
#   class: safety
#   since: 2026-09-02
#
# id: complete_return_rank_gate_runs_unchanged_operation
#   given: the frozen operation advances through the declared scale slots
#   then: every step uses the same complete-return trace identity, has rank delta one, preserves prior relation ids, and emits a distinct new relation id
#   class: correctness
#   since: 2026-09-02
#
# id: complete_return_rank_gate_compares_only_after_generation
#   given: the first three generated relation ranks are frozen
#   then: they are compared with observed arithmetic omega 1, 2, 3 and labeled target-free retrodictive rank matches rather than a factor constructor
#   class: doctrine
#   since: 2026-09-02
#
# id: complete_return_rank_gate_freezes_nonnumeric_next_rank
#   given: all three rank comparisons match
#   then: one unchanged further extension freezes relation rank four while numerical next gonol and factor cardinalities remain null
#   class: evidence
#   since: 2026-09-02
#
# id: complete_return_rank_gate_preserves_factor_boundary
#   given: topological relation ranks match arithmetic omega values
#   then: factor interpretation remains UNRESOLVED because no UCNS operation maps a return-cycle generator to a new arithmetic-prime component whose cardinality multiplies the gonol
#   class: safety
#   since: 2026-09-02
#
# id: complete_return_rank_gate_receipt_replays
#   given: the frozen candidate, structural control, and scale count are unchanged
#   then: canonical receipt bytes and digest replay byte-identically
#   class: correctness
#   since: 2026-09-02
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

import complete_return_relation_extension as extension
import squarefree_divisor_lattice_control as lattice


SCHEMA_ID = "the-interdependency.stack-research.ucns.complete-return-relation-rank-experiment"
SCHEMA_VERSION = "0.1.0"
STANDING = "stack-local-post-observation-relation-rank-gate"
SELECTION_EFFECT = "none"

STATUS_MATCH = "TARGET_FREE_RETRODICTIVE_RELATION_RANK_MATCH"
STATUS_FALSIFIED = "FALSIFIED_RELATION_RANK_GATE"
FACTOR_MAPPING_STATUS = "UNRESOLVED_NO_CYCLE_TO_ARITHMETIC_FACTOR_MAP"

NONCLAIMS: tuple[str, ...] = (
    "not UCNS canon",
    "not an out-of-sample validation of the complete-return candidate",
    "not evidence that topological first-homology rank equals arithmetic omega in UCNS",
    "not a successor-cardinality or prime-factor constructor",
    "not a numerical next-gonol prediction",
    "not PCEA key, entropy, hardness, replay-resistance, recovery, or public-authenticity evidence",
)

HMMM: tuple[str, ...] = (
    "the complete-return operation is target-free in code but was selected after the B1 to B2 to B3 pattern was known, so the three rank matches are retrodictive",
    "the exact native return loop supplies one new topological cycle, but UCNS does not yet map that generator to a multiplicative arithmetic-prime component",
    "higher-dimensional closure may fill the return loop or induce nontrivial monodromy, either of which can falsify the retained-rank candidate",
    "the unchanged fourth extension produces relation rank four but no factor values and no numerical next gonol",
    "a future independently observed fourth gonol remains the first structural out-of-sample gate",
)

FALSIFICATION_CONDITIONS: tuple[str, ...] = (
    "the frozen candidate code or receipt identity changes before comparison",
    "any extension changes trace identity, has rank delta other than one, or drops a prior relation id",
    "any generated relation rank fails its corresponding observed arithmetic omega comparison",
    "the fourth relation rank is read from the structural control instead of generated by one unchanged extension",
    "a relation-rank match is reported as an arithmetic factor construction without an executable geometric factor map",
    "a numerical next gonol is emitted without independently deriving all new factor cardinalities",
)


class CompleteReturnRankExperimentError(ValueError):
    """Raised when the frozen relation-rank experiment violates its protocol."""


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


def _file_digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _extension_digest(item: extension.CompleteReturnExtension) -> str:
    return sha256(_canonical_bytes(item.to_payload())).hexdigest()


@dataclass(frozen=True, slots=True)
class FrozenCandidate:
    """Exact geometric-candidate identity frozen before observation gates."""

    module_path: str
    code_sha256: str
    receipt_sha256: str
    producer_code_reference: str
    validation_state: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "module_path": self.module_path,
            "code_sha256": self.code_sha256,
            "receipt_sha256": self.receipt_sha256,
            "producer_code_reference": self.producer_code_reference,
            "validation_state": self.validation_state,
        }


def freeze_candidate() -> FrozenCandidate:
    """Bind exact target-free candidate identities before generating gate outputs."""

    root = _stack_root()
    path = Path(extension.__file__).resolve()
    code_sha256 = _file_digest(path)
    payload = extension.receipt_payload()
    if payload["producer_code_reference"] != "sha256:" + code_sha256:
        raise CompleteReturnRankExperimentError("candidate producer code reference mismatch")
    if payload["validation_state"] != "NOT_COMPARED_WITH_OBSERVED_SCALES":
        raise CompleteReturnRankExperimentError("candidate was not frozen before observation comparison")
    return FrozenCandidate(
        module_path=str(path.relative_to(root)),
        code_sha256=code_sha256,
        receipt_sha256=extension.receipt_digest(),
        producer_code_reference=payload["producer_code_reference"],
        validation_state=payload["validation_state"],
    )


@dataclass(frozen=True, slots=True)
class ScaleRankComparison:
    """One generated relation rank compared with one external omega witness."""

    observation_index: int
    generated_relation_rank: int
    observed_arithmetic_omega: int
    match: bool
    standing: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "observation_index": self.observation_index,
            "generated_relation_rank": self.generated_relation_rank,
            "observed_arithmetic_omega": self.observed_arithmetic_omega,
            "match": self.match,
            "standing": self.standing,
        }


@dataclass(frozen=True, slots=True)
class RelationRankExperiment:
    """Frozen generated ranks, post-generation comparisons, and boundaries."""

    status: str
    frozen_candidate: FrozenCandidate
    generated_extensions: tuple[extension.CompleteReturnExtension, ...]
    generated_output_sha256: str
    comparisons: tuple[ScaleRankComparison, ...]
    next_relation_rank: int | None
    next_relation_output_sha256: str | None
    preregistered_structural_omega: int
    next_rank_matches_preregistered_omega: bool
    arithmetic_factor_mapping_status: str
    new_factor_cardinalities: None
    numerical_next_gonol: None

    def to_payload(self) -> dict[str, Any]:
        generated = []
        for index, item in enumerate(self.generated_extensions, start=1):
            generated.append({
                "scale_index": index,
                "source_rank": item.source.relation_rank,
                "output_rank": item.output.relation_rank,
                "rank_delta": item.rank_delta,
                "new_relation_id": item.new_relation_id,
                "trace_sha256": sha256(_canonical_bytes(item.trace.to_payload())).hexdigest(),
                "extension_sha256": _extension_digest(item),
                "prior_relation_ids_preserved": item.output.relation_basis[:-1] == item.source.relation_basis,
            })
        return {
            "status": self.status,
            "frozen_candidate": self.frozen_candidate.to_payload(),
            "generation_frozen_before_comparison": {
                "extensions": generated,
                "generated_output_sha256": self.generated_output_sha256,
            },
            "comparisons": [item.to_payload() for item in self.comparisons],
            "next": {
                "relation_rank": self.next_relation_rank,
                "relation_output_sha256": self.next_relation_output_sha256,
                "preregistered_structural_omega": self.preregistered_structural_omega,
                "rank_matches_preregistered_omega": self.next_rank_matches_preregistered_omega,
                "new_factor_cardinalities": self.new_factor_cardinalities,
                "numerical_gonol": self.numerical_next_gonol,
            },
            "arithmetic_factor_mapping_status": self.arithmetic_factor_mapping_status,
            "claim_boundary": "topological relation-rank correspondence only; no arithmetic factor or cardinality construction",
        }


@lru_cache(maxsize=1)
def evaluate() -> RelationRankExperiment:
    """Generate all relation outputs first, then open arithmetic comparison gates."""

    frozen = freeze_candidate()

    # Generation is complete before observation witnesses or the structural
    # control are read below.
    generated = extension.iterate_complete_return(
        4,
        scale_prefix="complete-return-rank-gate-scale",
    )
    generated_payload = [item.to_payload() for item in generated]
    generated_output_sha256 = sha256(_canonical_bytes(generated_payload)).hexdigest()

    if any(item.rank_delta != 1 for item in generated):
        raise CompleteReturnRankExperimentError("unchanged complete-return rank delta failed")
    if any(item.output.relation_basis[:-1] != item.source.relation_basis for item in generated):
        raise CompleteReturnRankExperimentError("prior relation basis changed")
    if len({item.new_relation_id for item in generated}) != len(generated):
        raise CompleteReturnRankExperimentError("return relation ids must remain distinct by scale")
    trace_digests = {
        sha256(_canonical_bytes(item.trace.to_payload())).hexdigest()
        for item in generated
    }
    if len(trace_digests) != 1:
        raise CompleteReturnRankExperimentError("complete-return trace changed across scales")

    witnesses = lattice.observed_witnesses()
    comparisons = tuple(
        ScaleRankComparison(
            observation_index=witness.observation_index,
            generated_relation_rank=item.output.relation_rank,
            observed_arithmetic_omega=witness.omega,
            match=item.output.relation_rank == witness.omega,
            standing=STATUS_MATCH if item.output.relation_rank == witness.omega else STATUS_FALSIFIED,
        )
        for item, witness in zip(generated[:3], witnesses, strict=True)
    )
    status = STATUS_MATCH if all(item.match for item in comparisons) else STATUS_FALSIFIED
    next_extension = generated[3] if status == STATUS_MATCH else None
    structural = lattice.structural_control()
    next_rank = None if next_extension is None else next_extension.output.relation_rank
    return RelationRankExperiment(
        status=status,
        frozen_candidate=frozen,
        generated_extensions=generated,
        generated_output_sha256=generated_output_sha256,
        comparisons=comparisons,
        next_relation_rank=next_rank,
        next_relation_output_sha256=None if next_extension is None else _extension_digest(next_extension),
        preregistered_structural_omega=structural.omega,
        next_rank_matches_preregistered_omega=next_rank == structural.omega,
        arithmetic_factor_mapping_status=FACTOR_MAPPING_STATUS,
        new_factor_cardinalities=None,
        numerical_next_gonol=None,
    )


def _producer_code_reference() -> str:
    return "sha256:" + sha256(Path(__file__).read_bytes()).hexdigest()


def receipt_payload() -> dict[str, Any]:
    """Return the deterministic rank-gate receipt."""

    root = _stack_root()
    result = evaluate()
    control_path = Path(lattice.__file__).resolve()
    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "standing": STANDING,
        "selection_effect": SELECTION_EFFECT,
        "producer_code_reference": _producer_code_reference(),
        "source": {
            "frozen_geometric_candidate": result.frozen_candidate.to_payload(),
            "structural_control": {
                "module_path": str(control_path.relative_to(root)),
                "code_sha256": _file_digest(control_path),
                "receipt_sha256": lattice.receipt_digest(),
                "standing": lattice.STANDING,
            },
        },
        "experiment": result.to_payload(),
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
