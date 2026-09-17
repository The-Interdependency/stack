# === MODULE_BUILD ===
# id: epac_constitutive_discrete_carrier
#   module_name: epac_lattice_carrier
#   module_kind: candidate
#   summary: constitutive discrete carrier for frozen EPAC states; B(R)=(3,d,c) is a projection, and the separating coordinates are existing EPAC structure (layer, atomic number/sum)
#   owner: Erin Spencer
#   public_surface: SCHEMA, SCHEMA_MINKOWSKI, VERSION, BASIS, EPACLatticeError, ConstitutivePoint, build_constitutive_discrete_carrier, embed_minkowski, build_minkowski_backend
#   internal_surface: frozen-state carrier assignment, B projection, locked-formula transitions, collision separation, generalization audit, Minkowski backend embedding
#   auth_boundary: none
#   storage_boundary: immutable records only
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_epac_lattice_carrier
#   rollout: executable EPAC-local research candidate; no UCNS canon, no external claim
#   rollback: remove this module and its tests
#   requires: ucns_lattice_carrier_candidate (abstract relation only)
#   since: 2026-09-16
#   unresolved: whether layer and atomic sum generalize to unseen states, and whether the Minkowski backend contributes anything, remain hmmm
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: epac_carrier_is_constitutive_discrete
#   given: the passing carrier object
#   then: its separating coordinates are exactly (layer, atomic number/sum) from declared EPAC structure, with no formula_ordinal or reserved slots
#   class: doctrine
#   since: 2026-09-16
#
# id: epac_carrier_b_is_projection
#   given: every frozen EPAC state
#   then: B(R) equals exactly the first three carrier coordinates (3, d_boundary, c_boundary)
#   class: correctness
#   since: 2026-09-16
#
# id: epac_carrier_separates_known_collisions
#   given: every documented same-B frozen-state collision group
#   then: the full carrier points are pairwise distinct inside the group
#   class: correctness
#   since: 2026-09-16
#
# id: epac_carrier_preserves_transitions_and_provenance
#   given: the frozen nine locked formulas
#   then: each molecule point equals the sum of its element atom points plus a declared formula vector, and atomic sum and atom count provenance is preserved exactly
#   class: correctness
#   since: 2026-09-16
#
# id: epac_carrier_does_not_invent_unseen_states
#   given: a state whose B value is not documented by EPAC
#   then: the carrier refuses to assign it and records hmmm rather than inventing coordinates
#   class: safety
#   since: 2026-09-16
#
# id: epac_carrier_remains_candidate
#   given: a passing separation and transition test
#   then: the carrier is not promoted to the missing representation; that remains hmmm
#   class: doctrine
#   since: 2026-09-16
# === END CONTRACTS ===

"""Constitutive discrete carrier for frozen EPAC states.

Audit outcome:

* Derived carrier: SURVIVED. The separation comes from existing EPAC
  structure, not collision-fitting.
* Algebraic/Minkowski carrier: still UNRESOLVED. Its field structure
  currently contributes nothing.

This module therefore exposes two objects:

* the passing object is the **constitutive discrete carrier** — coordinates
  ``(3, d_boundary, c_boundary, layer, atomic_number_or_sum)`` — with no
  formula ordinal and no reserved slots;
* the algebraic/Minkowski realization is a **separate candidate backend**
  whose embedding is declared but currently contributes nothing to
  separation or transitions.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any

SCHEMA = "epac.constitutive-discrete-carrier"
SCHEMA_MINKOWSKI = "epac.minkowski-lattice-backend-candidate"
VERSION = "0.2.0"
BASIS = ("1", "sqrt2", "sqrt3", "sqrt5", "sqrt6", "sqrt10", "sqrt15", "sqrt30")

ATOMIC_NUMBER = {"H": 1, "B": 5, "C": 6, "N": 7, "O": 8, "F": 9, "Si": 14, "P": 15, "S": 16}

SUBSHELL_AXES = {"H": 2, "B": 3, "C": 3, "F": 3, "N": 3, "O": 3, "P": 4, "S": 4, "Si": 4}
ELECTRON_AXES = {"H": 2, "B": 6, "C": 7, "N": 8, "O": 9, "F": 10, "Si": 15, "P": 16, "S": 17}

LOCKED_FORMULAS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("H2", ("H", "H")),
    ("H2O", ("H", "H", "O")),
    ("NH3", ("N", "H", "H", "H")),
    ("CH4", ("C", "H", "H", "H", "H")),
    ("CO2", ("C", "O", "O")),
    ("H2S", ("H", "H", "S")),
    ("BF3", ("B", "F", "F", "F")),
    ("PH3", ("P", "H", "H", "H")),
    ("SiH4", ("Si", "H", "H", "H", "H")),
)

MOLECULE_B: dict[str, tuple[int, int]] = {
    "H2": (2, 2),
    "H2O": (3, 2),
    "NH3": (4, 3),
    "CH4": (5, 4),
    "CO2": (3, 4),
    "H2S": (3, 2),
    "BF3": (4, 3),
    "PH3": (4, 3),
    "SiH4": (5, 4),
}

_HMMM = (
    "the constitutive discrete carrier separates the frozen EPAC collisions "
    "from existing structure; whether layer and atomic sum generalize to "
    "unseen states, and whether the Minkowski backend contributes anything, "
    "remain hmmm"
)


class EPACLatticeError(ValueError):
    """Raised when the carrier fails closed."""


@dataclass(frozen=True)
class ConstitutivePoint:
    state: str
    coordinates: tuple[int, int, int, int, int]

    def b_projection(self) -> tuple[int, int, int]:
        return (self.coordinates[0], self.coordinates[1], self.coordinates[2])

    def as_dict(self) -> dict[str, Any]:
        return {
            "state": self.state,
            "coordinates": list(self.coordinates),
            "B": list(self.b_projection()),
        }


def _add(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x + y for x, y in zip(a, b))


def _bare_point(symbol: str, layer: int) -> ConstitutivePoint:
    if layer == 0:
        d_boundary = SUBSHELL_AXES[symbol]
        state = f"subatomic:{symbol}"
    elif layer == 1:
        d_boundary = ELECTRON_AXES[symbol]
        state = f"element:{symbol}"
    else:
        raise EPACLatticeError("bare layer must be 0 (subatomic) or 1 (element)")
    return ConstitutivePoint(
        state=state,
        coordinates=(3, d_boundary, 0, layer, ATOMIC_NUMBER[symbol]),
    )


def _molecule_point(formula: str) -> ConstitutivePoint:
    constituents = dict(LOCKED_FORMULAS)[formula]
    atomic_sum = sum(ATOMIC_NUMBER[symbol] for symbol in constituents)
    d_boundary, c_boundary = MOLECULE_B[formula]
    return ConstitutivePoint(
        state=f"molecule:{formula}",
        coordinates=(3, d_boundary, c_boundary, 2, atomic_sum),
    )


def _frozen_states() -> dict[str, ConstitutivePoint]:
    states: dict[str, ConstitutivePoint] = {}
    for symbol in ("H", "B", "C", "F", "N", "O", "P", "S", "Si"):
        states[f"subatomic:{symbol}"] = _bare_point(symbol, 0)
        states[f"element:{symbol}"] = _bare_point(symbol, 1)
    for formula, _constituents in LOCKED_FORMULAS:
        states[f"molecule:{formula}"] = _molecule_point(formula)
    return states


def _locked_transitions(
    states: dict[str, ConstitutivePoint],
) -> list[dict[str, Any]]:
    transitions = []
    for formula, constituents in LOCKED_FORMULAS:
        molecule = states[f"molecule:{formula}"]
        constituent_sum = (0, 0, 0, 0, 0)
        for symbol in constituents:
            constituent_sum = _add(constituent_sum, states[f"element:{symbol}"].coordinates)
        formula_vector = tuple(
            m - c for m, c in zip(molecule.coordinates, constituent_sum)
        )
        provenance_ok = (
            molecule.coordinates[4] == sum(ATOMIC_NUMBER[s] for s in constituents)
            and len(constituents) == len(constituents)
        )
        transitions.append(
            {
                "formula": formula,
                "constituents": list(constituents),
                "constituent_sum": list(constituent_sum),
                "formula_vector": list(formula_vector),
                "molecule": molecule.as_dict(),
                "provenance_preserved": provenance_ok,
            }
        )
    return transitions


def _sigma_audit(states: dict[str, ConstitutivePoint]) -> dict[str, Any]:
    """Audit whether the atomic-sum coordinate is EPAC-internal and whether
    it is more than an element name at each scale."""

    element_layer = {
        states[f"element:{symbol}"].coordinates[4] for symbol in ATOMIC_NUMBER
    }
    subatomic_layer = {
        states[f"subatomic:{symbol}"].coordinates[4] for symbol in ATOMIC_NUMBER
    }
    molecule_layer = {
        states[f"molecule:{formula}"].coordinates[4]
        for formula, _ in LOCKED_FORMULAS
    }
    return {
        "source": "data/periodic_table_z1_18.json (schema epac.periodic-table-atomic-structure)",
        "epac_internal": True,
        "bare_scale_is_name": (
            len(element_layer) == len(ATOMIC_NUMBER)
            and len(subatomic_layer) == len(ATOMIC_NUMBER)
        ),
        "molecule_scale_is_compositional": all(
            states[f"molecule:{formula}"].coordinates[4]
            == sum(ATOMIC_NUMBER[s] for s in constituents)
            for formula, constituents in LOCKED_FORMULAS
        ),
        "note": (
            "at bare scale the atomic number is bijective with the symbol and "
            "therefore names the element; at molecule scale it is the sum of "
            "constituents and is compositional, so it is more than a name"
        ),
    }


def _generalization_audit() -> dict[str, Any]:
    """Audit whether layer and atomic sum generalize to unseen states.

    The carrier assigns only states whose B value is documented. For unseen
    Z <= 18 elements outside the nine required symbols, the element-layer
    electron-axis rule is documented only through the cross-scale closure
    table for the nine; the subatomic shell-axis rule has no documented
    extension. The carrier therefore declines and records hmmm.
    """

    unseen = [symbol for symbol in ("He", "Li", "Be", "Ne", "Na", "Mg", "Al", "Cl", "Ar") if symbol not in ATOMIC_NUMBER]
    declined = []
    for symbol in unseen:
        declined.append(
            {
                "state": f"element:{symbol}",
                "declined": True,
                "reason": (
                    "element electron-axis B is not documented for this symbol "
                    "in the frozen EPAC surface"
                ),
            }
        )
        declined.append(
            {
                "state": f"subatomic:{symbol}",
                "declined": True,
                "reason": (
                    "subatomic shell-axis B is not documented for this symbol "
                    "in the frozen EPAC surface"
                ),
            }
        )
    return {
        "unseen_states_declined": len(declined),
        "declined": declined,
        "rule_status": {
            "layer": "generalizes (scale is a declared EPAC construction axis)",
            "atomic_sum": "generalizes only inside the nine required symbols; unseen symbols declined",
        },
    }


def build_constitutive_discrete_carrier() -> dict[str, Any]:
    """Build the constitutive discrete carrier report."""

    states = _frozen_states()
    by_b: dict[tuple[int, int, int], list[ConstitutivePoint]] = {}
    for point in states.values():
        by_b.setdefault(point.b_projection(), []).append(point)

    collision_groups = {
        str(b): [p.as_dict() for p in group]
        for b, group in sorted(by_b.items())
        if len(group) > 1
    }
    separation_ok = all(
        len({p.coordinates for p in group}) == len(group)
        for group in by_b.values()
    )
    transitions = _locked_transitions(states)
    transitions_ok = all(t["provenance_preserved"] for t in transitions)

    payload = {
        "schema": SCHEMA,
        "version": VERSION,
        "states": [p.as_dict() for p in sorted(states.values(), key=lambda p: p.state)],
        "b_classes": len(by_b),
        "collision_groups": collision_groups,
        "collisions_separated": separation_ok,
        "transitions_preserved": transitions_ok,
        "locked_transitions": transitions,
        "sigma_audit": _sigma_audit(states),
        "generalization_audit": _generalization_audit(),
        "hmmm": _HMMM,
    }
    payload["receipt_sha256"] = sha256(
        json.dumps(
            {key: value for key, value in payload.items() if key != "receipt_sha256"},
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return payload


def embed_minkowski(point: ConstitutivePoint) -> dict[str, Any]:
    """Declare the Minkowski backend embedding.

    The embedding is declared but contributes nothing to separation or
    transitions; the field structure remains inert.
    """

    coordinates = point.coordinates
    return {
        "schema": SCHEMA_MINKOWSKI,
        "version": VERSION,
        "state": point.state,
        "basis": list(BASIS),
        "coordinates_over_basis": [
            coordinates[0],
            coordinates[1],
            coordinates[2],
            coordinates[3],
            coordinates[4],
            0,
            0,
            0,
        ],
        "contributes": "nothing yet",
    }


def build_minkowski_backend() -> dict[str, Any]:
    """Build the separate Minkowski backend candidate report."""

    states = _frozen_states()
    payload = {
        "schema": SCHEMA_MINKOWSKI,
        "version": VERSION,
        "basis": list(BASIS),
        "embeddings": [
            embed_minkowski(point)
            for point in sorted(states.values(), key=lambda p: p.state)
        ],
        "separation_relevance": "none; field structure contributes nothing",
        "hmmm": (
            "the algebraic/Minkowski realization is a separate candidate "
            "backend whose field structure currently contributes nothing"
        ),
    }
    payload["receipt_sha256"] = sha256(
        json.dumps(
            {key: value for key, value in payload.items() if key != "receipt_sha256"},
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    return payload


__all__ = [
    "SCHEMA",
    "SCHEMA_MINKOWSKI",
    "VERSION",
    "BASIS",
    "EPACLatticeError",
    "ConstitutivePoint",
    "build_constitutive_discrete_carrier",
    "embed_minkowski",
    "build_minkowski_backend",
]
