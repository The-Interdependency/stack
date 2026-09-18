"""Post-freeze arithmetic gate for rooted rotation/closure candidates.

All observed cardinalities live here, outside the constructor module.  The
constructor source, target-free receipt, and explicit assumption set are frozen
first.  Only then are the observed retained structures constructed and compared.
"""

# === MODULE_BUILD ===
# id: ucns_rooted_rotation_successor_gate
#   module_name: rooted_rotation_successor_gate
#   module_kind: experiment
#   summary: freezes the rooted ribbon constructors before testing their cellular readouts against the observed gonol progression and records the first surviving canonical assumption separately
#   owner: The Interdependency
#   public_surface: Observation, freeze_payload, freeze_digest, audit_payload, receipt_bytes, receipt_digest, render_markdown, write_receipts
#   internal_surface: observation state binding, candidate diagnostics, first-transition stop gate, exact source identity ledger
#   auth_boundary: none
#   storage_boundary: optional deterministic JSON and Markdown receipts
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/ucns/tests/test_rooted_rotation_closure_constructor.py
#   rollout: stack-local post-freeze falsification only; no UCNS canon, PCEA runtime, or cryptographic promotion
#   rollback: remove this module, its tests, report, and receipts
#   requires: ucns_rooted_rotation_closure_constructor, pcea_crypto_audit_0b49672, ucns_trapdoor_lift_falsification_v0
#   since: 2026-09-18
#   unresolved: canon-authorized pointed attachment; selected rotation; global torsion presentation; successor-prime selector
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: rooted_successor_gate_freezes_before_observations
#   given: the observed progression is evaluated
#   then: the freeze payload binds only constructor bytes, target-free constructor receipt, and assumption definitions, with no observed gonol value
#   class: safety
#
# id: rooted_successor_gate_preserves_observed_R
#   given: each observed factor multiset is admitted after freeze
#   then: its complete coefficient vector, ordered role relation, multiplicity, recoverable constituents, and provenance are retained and its top coefficient equals the observation
#   class: correctness
#
# id: rooted_successor_gate_stops_failed_recursion
#   given: a frozen constructor does not produce the first successor comparator
#   then: that candidate is FALSIFIED and the recursive second transition is not executed as a prediction
#   class: falsification
#
# id: rooted_successor_gate_separates_geometry_from_security
#   given: deterministic ribbon closure succeeds under assumptions
#   then: geometric correctness does not alter the independently replayed PCEA cryptographic FALSIFIED standing or the trapdoor candidate result
#   class: doctrine
#
# id: rooted_successor_gate_receipts_replay
#   given: exact sources, frozen constructors, and observed fixtures are unchanged
#   then: canonical JSON and Markdown receipts replay byte-identically
#   class: correctness
# === END CONTRACTS ===

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
import argparse
import json
from pathlib import Path
from typing import Any

import rooted_rotation_closure_constructor as constructor


SCHEMA_ID = "the-interdependency.stack-research.ucns.rooted-rotation-successor-gate"
SCHEMA_VERSION = "0.1.0"
STANDING = "stack-local-post-freeze-falsification"

SOURCE_IDENTITIES = {
    "skill_lib": "dd5027d99516831c0dcb83a176a67140d3819b66",
    "metapat": "e4165b0cac9eca41daef9c2f941881028ca55d48",
    "ucns": "d8f0c505e6f5132e9711de0e7c24e4718e77e51a",
    "pcea": "1595842abd1a5b443c6a601a2afe935b60c4adf7",
    "stack_pr_42_head": "57e3f047c092a6df5435ed4f502347664513a0ff",
    "pcea_crypto_audit_commit": "0b49672862a30cec0a0ee24e39a34241c9626f27",
    "trapdoor_audit_stack_base": "82dc5e39f1e0c3f162138c2e7b642814df14dd98",
}

UNPUBLISHED_EVIDENCE = {
    "pcea_crypto_audit": {
        "source": "local Git object 0b49672862a30cec0a0ee24e39a34241c9626f27",
        "original_receipt_sha256": "402980af924b89ae7b7dde10e8cc8f6d7d423994c13739ea7a5230217b1e3e72",
        "verdict": "FALSIFIED",
        "replay": "6 tests passed against exact PCEA PR 41 source; local parity extension also passed 6 tests and retained FALSIFIED across eight failed criteria",
    },
    "trapdoor_lift_falsification_v0": {
        "source": "unpublished files over Stack base 82dc5e39f1e0c3f162138c2e7b642814df14dd98",
        "producer_sha256": "9039d55c3d6230327338fd6c1d004a351ed5f9084f22ac546d675151ecfd8903",
        "test_sha256": "d129cc090b06893f412bc05e31320838578a4b9d9f22d073a027b64d054f12f8",
        "canonical_receipt_sha256": "4d8ae8cbe68344c6f4847fefd6659f228a3112e3810ee997af1dfa807eeaed7f",
        "replay": "10 tests passed including exhaustive unit-domain fiber profile",
        "overall": "UNRESOLVED_NOT_RECONSTRUCTED",
        "minimal_fourth_power_candidate": "FALSIFIED",
    },
}


@dataclass(frozen=True, slots=True)
class Observation:
    scale: int
    cardinality: int
    factors: tuple[int, ...]

    def to_payload(self) -> dict[str, Any]:
        return {
            "scale": self.scale,
            "cardinality": self.cardinality,
            "factors": list(self.factors),
        }


OBSERVATIONS = (
    Observation(1, 157, (157,)),
    Observation(2, 2881, (43, 67)),
    Observation(3, 54837698421, (3, 11, 1661748437)),
)


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")


def freeze_payload() -> dict[str, Any]:
    """Bind only target-free constructor material."""

    path = Path(constructor.__file__).resolve()
    target_free = constructor.receipt_payload()
    if target_free["observed_successor_inputs"] is not None:
        raise AssertionError("constructor receipt contains observation inputs")
    return {
        "constructor_path": "research/ucns/rooted_rotation_closure_constructor.py",
        "constructor_sha256": sha256(path.read_bytes()).hexdigest(),
        "constructor_receipt_sha256": constructor.receipt_digest(target_free),
        "frozen_assumptions": [item.to_payload() for item in constructor.frozen_assumptions()],
        "observed_values": None,
        "observed_factors": None,
    }


def freeze_digest() -> str:
    return sha256(_canonical_bytes(freeze_payload())).hexdigest()


def _state(observation: Observation) -> constructor.RetainedStructure:
    if observation.cardinality != _product(observation.factors):
        raise AssertionError("observation factorization does not reproduce cardinality")
    return constructor.retained_structure(
        f"observed-scale-{observation.scale}",
        observation.factors,
        provenance=(
            "operator-supplied-observation-fixture",
            f"post-freeze-gate-scale:{observation.scale}",
        ),
    )


def _product(values: tuple[int, ...]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


@lru_cache(maxsize=1)
def audit_payload() -> dict[str, Any]:
    frozen = freeze_payload()
    frozen_sha = freeze_digest()
    states = tuple(_state(observation) for observation in OBSERVATIONS)
    diagnostics: list[dict[str, Any]] = []
    first_transition: list[dict[str, Any]] = []

    for assumptions in constructor.frozen_assumptions():
        certificates = tuple(
            constructor.construct(
                state,
                assumptions,
                rotation_relation_id=state.relations[0].relation_id,
            )
            for state in states
        )
        diagnostics.append(
            {
                "assumption_id": assumptions.assumption_id,
                "scale_diagnostics_not_recursive_predictions": [
                    {
                        "scale": observation.scale,
                        "input_cardinality": observation.cardinality,
                        "retained_structure_sha256": state.digest,
                        "coefficients": list(state.coefficients),
                        "complete_product": state.complete_product,
                        "certificate_sha256": certificate.digest,
                        "face_count": len(certificate.face_cycles),
                        "genus": certificate.genus,
                        "cellular_boundary_rank": certificate.cellular_boundary_rank,
                        "finite_cokernel_order": certificate.finite_cokernel_order,
                        "successor_prime_selector": None,
                    }
                    for observation, state, certificate in zip(
                        OBSERVATIONS, states, certificates, strict=True
                    )
                ],
            }
        )
        first_output = certificates[0].finite_cokernel_order
        expected = OBSERVATIONS[1].cardinality
        first_transition.append(
            {
                "assumption_id": assumptions.assumption_id,
                "input": OBSERVATIONS[0].cardinality,
                "expected_comparator": expected,
                "derived_cellular_order": first_output,
                "verdict": "SURVIVED" if first_output == expected else "FALSIFIED",
                "second_recursive_transition_executed": first_output == expected,
                "next_prediction": None,
            }
        )

    if any(item["verdict"] != "FALSIFIED" for item in first_transition):
        raise AssertionError("a frozen candidate unexpectedly survived the first comparator")
    if any(item["second_recursive_transition_executed"] for item in first_transition):
        raise AssertionError("a falsified recursion advanced to the second prediction")

    return {
        "schema_id": SCHEMA_ID,
        "schema_version": SCHEMA_VERSION,
        "standing": STANDING,
        "source_identities": dict(sorted(SOURCE_IDENTITIES.items())),
        "unpublished_evidence": UNPUBLISHED_EVIDENCE,
        "freeze": frozen,
        "freeze_sha256": frozen_sha,
        "observations_applied_after_freeze": [item.to_payload() for item in OBSERVATIONS],
        "candidate_diagnostics": diagnostics,
        "recursive_successor_gate": first_transition,
        "dependency_audit": [
            {
                "field": "origin_attachment",
                "necessity": "chooses a target object for Structural Null; an address or model basepoint is not a morphism",
                "current_status": "MATHEMATICAL_OBSTRUCTION_ON_UNFRAMED_Q_MOD_Z_PLUS_MISSING_CANON_OPERATION",
                "candidate_status": "SUPPLIED_EXPLICITLY_NOT_SELECTED",
            },
            {
                "field": "directed_tangent_or_chirality",
                "necessity": "distinguishes a word from its reversal while preserving the native one-turn frame flip and two-turn return",
                "current_status": "MISSING_SELECTION_UNDER_REVERSAL_SYMMETRY",
                "candidate_status": "SUPPLIED_EXPLICITLY_USING_EXISTING_NATIVE_TRACE",
            },
            {
                "field": "rotation_system",
                "necessity": "orders incident return germs cyclically; graph incidence and linear provenance do not determine a ribbon embedding",
                "current_status": "MISSING_SELECTION_WITH_EXACT_COMPETING_ROTATIONS",
                "candidate_status": "IMPLEMENTED_TWO_COMPETING_ASSUMPTIONS",
            },
            {
                "field": "marked_outgoing_dart",
                "necessity": "turns cyclic closure into a based word rather than a cyclic-conjugacy class",
                "current_status": "MISSING_SELECTION_UNDER_CYCLIC_START_SYMMETRY",
                "candidate_status": "FIRST_DECLARED_OCCURRENCE_ASSUMPTION",
            },
            {
                "field": "closure_rule",
                "necessity": "declares which orbit is complete and whether it is traversed only or attached as a filled relation",
                "current_status": "MISSING_TOPOLOGICAL_SELECTION; FACE_ORBIT_IMPLEMENTATION_EXISTS_ONCE_ALPHA_AND_SIGMA_ARE_SUPPLIED",
                "candidate_status": "ALL_FACE_ORBITS_FILLED_BY_EXPLICIT_ASSUMPTION",
            },
        ],
        "verdicts": {
            "explicit_assumption_ribbon_constructor": "SURVIVED_LOCALLY",
            "paired_germs_as_successor_law": "FALSIFIED",
            "sign_blocks_as_successor_law": "FALSIFIED",
            "canonical_ucns_based_traversal": "UNRESOLVED",
            "ucns_prime_successor_selector": "UNRESOLVED",
            "minimal_fourth_power_trapdoor": "FALSIFIED",
            "pcea_cryptographic_security": "FALSIFIED",
        },
        "first_remaining_irreducible_assumption": {
            "name": "geometry-owned pointed origin attachment",
            "statement": "UCNS must add or derive one carrier-owned incidence from singular Structural Null to a native traversable object; the homogeneous unframed Q/Z candidate has no equivariant point selector",
            "why_irreducible_now": "current canon supplies neither the attachment morphism nor an invariant singularity, and provenance or coordinate zero cannot manufacture one",
        },
        "next_experiment": {
            "name": "native attachment target stabilizer comparison",
            "inputs": [
                "visible phase basepoint as an unframed target",
                "the C2-invariant two-lift fiber as a set-valued target",
                "a singly framed lift only as an explicitly stronger control",
            ],
            "falsifier": "if every native target retains a transitive or reversal symmetry and no current incidence fixes one target, origin attachment remains unresolved; no downstream field is promoted",
            "survival_gate": "one target must be well-typed, carrier-owned, invariantly distinguished, and replayable without source order, hashes, observed gonols, or PCEA expectations",
        },
        "structural_consequence": "even after the five explicit assumptions, ordinary orientable ribbon-face closure yields only a trivial or non-finite abelian cellular readout here; a separate geometry-derived torsion/monodromy presentation is required before any prime successor can exist",
        "nonclaims": list(constructor.NONCLAIMS),
    }


def receipt_bytes(payload: dict[str, Any] | None = None) -> bytes:
    return _canonical_bytes(payload if payload is not None else audit_payload()) + b"\n"


def receipt_digest(payload: dict[str, Any] | None = None) -> str:
    return sha256(receipt_bytes(payload)).hexdigest()


def render_markdown(payload: dict[str, Any] | None = None) -> str:
    value = payload if payload is not None else audit_payload()
    lines = [
        "# Rooted rotation/closure successor gate v0",
        "",
        "Standing: **Stack-local explicit-assumption experiment**.",
        "",
        f"Freeze SHA-256: `{value['freeze_sha256']}`.",
        f"Receipt SHA-256: `{receipt_digest(value)}`.",
        "",
        "## Outcome",
        "",
        "The rooted ribbon carrier closes deterministically under its named assumptions, but neither frozen rotation candidate derives the first observed successor.",
        "",
        "| Candidate | Derived order from 157-state | Comparator | Verdict |",
        "|---|---:|---:|---|",
    ]
    for item in value["recursive_successor_gate"]:
        lines.append(
            f"| `{item['assumption_id']}` | {item['derived_cellular_order']} | {item['expected_comparator']} | `{item['verdict']}` |"
        )
    lines.extend(
        (
            "",
            "The second recursive transition was not executed for either falsified candidate. Scale-two and scale-three records are retained only as post-freeze structural diagnostics, not predictions.",
            "",
            "## Dependency result",
            "",
        )
    )
    for item in value["dependency_audit"]:
        lines.append(
            f"- `{item['field']}` — {item['necessity']} Current: `{item['current_status']}`; candidate: `{item['candidate_status']}`."
        )
    first = value["first_remaining_irreducible_assumption"]
    next_experiment = value["next_experiment"]
    lines.extend(
        (
            "",
            "## First remaining irreducible assumption",
            "",
            f"**{first['name']}**: {first['statement']}",
            "",
            "## Next experiment",
            "",
            f"**{next_experiment['name']}**. {next_experiment['survival_gate']}",
            "",
            "## Separate cryptographic standing",
            "",
            "PCEA cryptographic security remains `FALSIFIED`; the unpublished trapdoor audit remains `UNRESOLVED_NOT_RECONSTRUCTED` overall and `FALSIFIED` for the minimal fourth-power candidate. Geometric replay does not alter either result.",
            "",
            "hmmm: a rooted carrier can be represented; current UCNS still does not select its root, ribbon rotation, or torsion-producing arithmetic presentation.",
            "",
        )
    )
    return "\n".join(lines)


def write_receipts(directory: Path) -> tuple[Path, Path]:
    directory.mkdir(parents=True, exist_ok=True)
    payload = audit_payload()
    json_path = directory / "rooted-rotation-successor-gate-v0.json"
    md_path = directory / "rooted-rotation-successor-gate-v0.md"
    json_path.write_bytes(json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True).encode("ascii") + b"\n")
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    return json_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--write-receipts", type=Path)
    args = parser.parse_args()
    if args.write_receipts is not None:
        for path in write_receipts(args.write_receipts):
            print(path)
        return
    payload = audit_payload()
    if args.format == "markdown":
        print(render_markdown(payload), end="")
    else:
        print(json.dumps({"receipt_sha256": receipt_digest(payload), "receipt": payload}, ensure_ascii=True, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
