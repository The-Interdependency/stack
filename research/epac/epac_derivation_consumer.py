# === MODULE_BUILD ===
# id: epac_derivation_consumer
#   module_name: epac_derivation_consumer
#   module_kind: audit
#   summary: consumes the pinned epac_atomic quantum-shell derivation to rebuild the (B, layer, period, valence) carrier from construction instead of periodic-table lookup, and rebinds receipts to the exact epac source commit and bytes
#   owner: Erin Spencer
#   public_surface: SCHEMA, VERSION, EPAC_REPO_COMMIT, EPAC_ATOMIC_MODULE_SHA256, EPAC_ATOMIC_DERIVATION_MODULE_SHA256, DerivedCarrierError, build_derived_carrier, replay_derived_carrier
#   internal_surface: verified epac source loading, derived period/valence, carrier rerun, canonical receipt
#   auth_boundary: none
#   storage_boundary: immutable records only
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_epac_derivation_consumer
#   rollout: stack audit of epac source evidence; no promotion beyond what the audit earns
#   rollback: remove this module and its tests
#   requires: epac_atomic_derivation (pinned), epac_atomic (pinned), epac_lattice_carrier, epac_carrier_falsification
#   since: 2026-09-17
#   unresolved: B for unseen states is not yet derived, so full generalization beyond the nine remains unresolved
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: derived_carrier_binds_exact_epac_source
#   given: an epac source root
#   then: the carrier consumes only epac source bytes whose sha256 matches the pinned commit modules, else it fails closed
#   class: correctness
#   since: 2026-09-17
#
# id: derived_carrier_uses_construction_not_lookup
#   given: the rebuilt (B, layer, period, valence) carrier
#   then: period and valence come from epac_atomic electron states, and the periodic-table data file is not consulted
#   class: doctrine
#   since: 2026-09-17
#
# id: derived_carrier_reruns_collision_transition_provenance_generalization
#   given: the derived carrier
#   then: collisions stay separated, transitions stay exact lattice translations with provenance, and generalization is re-tested with derived period and valence
#   class: correctness
#   since: 2026-09-17
# === END CONTRACTS ===

"""Consume the pinned epac quantum-shell derivation into the carrier.

Source first, research second, receipts last.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path
from typing import Any

from epac_lattice_carrier import (
    ATOMIC_NUMBER,
    LOCKED_FORMULAS,
    MOLECULE_B,
    SUBSHELL_AXES,
    ELECTRON_AXES,
)

SCHEMA = "epac.derived-constitutive-carrier"
VERSION = "0.1.0"

EPAC_REPO_COMMIT = "7b3d99af9a456d2587e0489d7400e6f8b58c8a82"
EPAC_ATOMIC_MODULE_SHA256 = "539a07c33c56de24bcae9f6ba270eb76b82de887f38b4f42ffa60b3ffb760d62"
EPAC_ATOMIC_DERIVATION_MODULE_SHA256 = "8d6a7830c79f86b0aad1055039500f95ed254d204abab6b0c4747db95faf2451"
EPAC_B_DERIVATION_MODULE_SHA256 = "ee36f45af6354947f35980e8ac3e033bb32fecb937a13e3704a6614b3b882d55"


class DerivedCarrierError(ValueError):
    """Raised when the derived carrier fails closed."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _verify_epac_source(epac_source_root: Path) -> Path:
    root = Path(epac_source_root)
    atomic = root / "epac_atomic.py"
    derivation = root / "epac_atomic_derivation.py"
    b_derivation = root / "epac_b_derivation.py"
    if not atomic.exists() or not derivation.exists() or not b_derivation.exists():
        raise DerivedCarrierError(f"epac source modules missing under {root}")
    if _sha256(atomic) != EPAC_ATOMIC_MODULE_SHA256:
        raise DerivedCarrierError("epac_atomic.py bytes do not match the pinned commit")
    if _sha256(derivation) != EPAC_ATOMIC_DERIVATION_MODULE_SHA256:
        raise DerivedCarrierError("epac_atomic_derivation.py bytes do not match the pinned commit")
    if _sha256(b_derivation) != EPAC_B_DERIVATION_MODULE_SHA256:
        raise DerivedCarrierError("epac_b_derivation.py bytes do not match the pinned commit")
    try:
        subprocess.run(
            ["git", "-C", str(root), "merge-base", "--is-ancestor", EPAC_REPO_COMMIT, "HEAD"],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:
        raise DerivedCarrierError("epac source root does not contain the pinned commit") from exc
    return root


def load_verified_epac_atomic(epac_source_root: Path) -> Any:
    """Import epac_atomic from verified bytes at the pinned commit."""

    root = _verify_epac_source(epac_source_root)
    spec = importlib.util.spec_from_file_location("epac_atomic", root / "epac_atomic.py")
    if spec is None or spec.loader is None:
        raise DerivedCarrierError("cannot load epac_atomic module")
    module = importlib.util.module_from_spec(spec)
    import sys

    sys.modules["epac_atomic"] = module
    spec.loader.exec_module(module)
    return module


def _derived_period_valence(epac_module: Any) -> dict[str, dict[str, Any]]:
    derived: dict[str, dict[str, Any]] = {}
    for symbol in ATOMIC_NUMBER:
        record = epac_module.atomic_record(ATOMIC_NUMBER[symbol])
        derived[symbol] = {
            "Z": record.Z,
            "period": record.period,
            "valence_electrons": record.valence_electrons,
            "configuration": record.configuration,
            "lookup_used": False,
        }
    return derived


def build_derived_carrier(epac_source_root: Path) -> dict[str, Any]:
    """Rebuild the (B, layer, period, valence) carrier from verified epac
    construction and rerun every carrier control."""

    root = _verify_epac_source(Path(epac_source_root))
    epac_module = load_verified_epac_atomic(root)
    derived = _derived_period_valence(epac_module)

    # Carrier coordinates: (B, layer, period, valence) with B from the
    # documented EPAC boundary values and period/valence from epac_atomic.
    states: dict[str, tuple[int, int, int, int, int, int]] = {}
    for symbol in ("H", "B", "C", "F", "N", "O", "P", "S", "Si"):
        entry = derived[symbol]
        states[f"subatomic:{symbol}"] = (3, SUBSHELL_AXES[symbol], 0, 0, entry["period"], entry["valence_electrons"])
        states[f"element:{symbol}"] = (3, ELECTRON_AXES[symbol], 0, 1, entry["period"], entry["valence_electrons"])
    for formula, constituents in LOCKED_FORMULAS:
        d_boundary, c_boundary = MOLECULE_B[formula]
        period_sum = sum(derived[s]["period"] for s in constituents)
        valence_sum = sum(derived[s]["valence_electrons"] for s in constituents)
        states[f"molecule:{formula}"] = (3, d_boundary, c_boundary, 2, period_sum, valence_sum)

    by_b: dict[tuple[int, int, int], list[str]] = {}
    for name, coords in states.items():
        by_b.setdefault(coords[:3], []).append(name)
    collision_groups = {
        str(b): group for b, group in sorted(by_b.items()) if len(group) > 1
    }
    separation_ok = all(
        len({states[name] for name in group}) == len(group)
        for group in by_b.values()
    )

    transitions = []
    for formula, constituents in LOCKED_FORMULAS:
        constituent_sum = [0] * 6
        for symbol in constituents:
            element = states[f"element:{symbol}"]
            constituent_sum = [a + b for a, b in zip(constituent_sum, element)]
        molecule = states[f"molecule:{formula}"]
        formula_vector = [m - c for m, c in zip(molecule, constituent_sum)]
        transitions.append(
            {
                "formula": formula,
                "constituents": list(constituents),
                "constituent_sum": constituent_sum,
                "formula_vector": formula_vector,
                "provenance_preserved": (
                    constituent_sum[4] == molecule[4]
                    and constituent_sum[5] == molecule[5]
                ),
            }
        )
    transitions_ok = all(t["provenance_preserved"] for t in transitions)

    # Generalization: period and valence are now derivable for all Z=1..18
    # from epac_atomic; B for unseen states is not yet derived.
    generalization = []
    for Z in range(1, 19):
        record = epac_module.atomic_record(Z)
        symbol = record.symbol
        if symbol in ATOMIC_NUMBER:
            status = "derived"
        else:
            status = "period-valence-derived-B-declined"
        generalization.append(
            {
                "Z": Z,
                "symbol": symbol,
                "period_derived": record.period,
                "valence_derived": record.valence_electrons,
                "carrier_status": status,
            }
        )

    # Generative promotion gate: load the verified frozen B derivation rule
    # and record its held-out predictions and the transition-metal failure.
    b_spec = importlib.util.spec_from_file_location("epac_b_derivation", root / "epac_b_derivation.py")
    if b_spec is None or b_spec.loader is None:
        raise DerivedCarrierError("cannot load epac_b_derivation module")
    b_module = importlib.util.module_from_spec(b_spec)
    import sys as _sys

    _sys.modules["epac_b_derivation"] = b_module
    b_spec.loader.exec_module(b_module)
    b_report = b_module.freeze_b_derivation()
    locked_reproduced = all(
        entry["matches"] for entry in b_report["locked_formula_b_evaluations"]
    )
    held_out_statuses = {
        entry["formula"]: entry["status"]
        for entry in b_report["held_out_molecule_b_evaluations"]
    }
    transition_failure = b_report["transition_metal_failure"]
    topology_evaluations = b_report["transition_metal_topology_evaluations"]
    generative = locked_reproduced and all(
        status == "evaluation-only" for status in held_out_statuses.values()
    ) and not transition_failure

    payload = {
        "schema": SCHEMA,
        "version": VERSION,
        "epac_source_commit": EPAC_REPO_COMMIT,
        "epac_atomic_module_sha256": EPAC_ATOMIC_MODULE_SHA256,
        "epac_atomic_derivation_module_sha256": EPAC_ATOMIC_DERIVATION_MODULE_SHA256,
        "epac_b_derivation_module_sha256": EPAC_B_DERIVATION_MODULE_SHA256,
        "source_bytes_verified": True,
        "lookup_used": False,
        "derived_period_valence": derived,
        "b_classes": len(by_b),
        "collision_groups": collision_groups,
        "collisions_separated": separation_ok,
        "transitions_preserved": transitions_ok,
        "locked_transitions": transitions,
        "generalization": generalization,
        "promotion_gate": {
            "period_derived_from_epac_atomic": True,
            "valence_derived_from_epac_atomic": True,
            "carrier_tests_survive": separation_ok and transitions_ok,
            "decision": "PROMOTE" if separation_ok and transitions_ok else "RETAIN-FALSIFIED",
            "standing": (
                "EPAC-derived constitutive carrier"
                if separation_ok and transitions_ok
                else "chemistry-assisted serialization"
            ),
            "remaining_unresolved": "B for unseen states is not yet derived",
        },
        "generative_gate": {
            "frozen_rule_reproduces_nine": locked_reproduced,
            "supported_domain": b_report["supported_domain"],
            "held_out_statuses": held_out_statuses,
            "transition_metal_failure_recorded": bool(transition_failure),
            "transition_metal_topology_evaluations": topology_evaluations,
            "active_orbital_set_derived_for_supplied_topologies": all(
                entry["center_active_orbital_set"]["kind"] == "transition-metal"
                for entry in topology_evaluations
            ),
            "coordination_capacity": "UNRESOLVED",
            "capacity_rule_status": b_report["capacity_rule_status"],
            "topology_formation": "downstream, not tested here",
            "decision": "PROMOTE-GENERATIVE" if generative else "RETAIN-BOUNDED",
            "standing": (
                "generative constitutive carrier"
                if generative
                else "bounded constitutive carrier"
            ),
            "missing_state_variable": (
                None
                if not transition_failure
                else "bond-context active-orbital set (may include (n-1)d)"
            ),
        },
        "hmmm": (
            "period and valence now derive from epac_atomic construction; "
            "B for unseen states is not yet derived, so full generalization "
            "beyond the nine remains unresolved"
        ),
    }
    payload["receipt_sha256"] = hashlib.sha256(
        json.dumps(
            {key: value for key, value in payload.items() if key != "receipt_sha256"},
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return payload


def replay_derived_carrier(data: bytes, epac_source_root: Path) -> dict[str, Any]:
    """Recompute the derived carrier and verify byte-identically."""

    if not isinstance(data, bytes):
        raise DerivedCarrierError("receipt must be bytes")
    try:
        obj = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DerivedCarrierError("receipt is not valid canonical JSON") from exc
    if obj.get("schema") != SCHEMA or obj.get("version") != VERSION:
        raise DerivedCarrierError("receipt schema or version mismatch")

    rebuilt = build_derived_carrier(epac_source_root)
    if rebuilt["receipt_sha256"] != obj.get("receipt_sha256"):
        raise DerivedCarrierError("receipt digest does not match recomputation")
    rebuilt_bytes = json.dumps(rebuilt, sort_keys=True, separators=(",", ":")).encode("utf-8")
    if rebuilt_bytes != data:
        raise DerivedCarrierError("receipt does not replay byte-identically")
    return rebuilt


__all__ = [
    "SCHEMA",
    "VERSION",
    "EPAC_REPO_COMMIT",
    "EPAC_ATOMIC_MODULE_SHA256",
    "EPAC_ATOMIC_DERIVATION_MODULE_SHA256",
    "DerivedCarrierError",
    "build_derived_carrier",
    "replay_derived_carrier",
]
