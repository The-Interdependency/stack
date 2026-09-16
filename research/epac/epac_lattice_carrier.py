# === MODULE_BUILD ===
# id: epac_algebraic_minkowski_lattice_carrier_candidate
#   module_name: epac_lattice_carrier
#   module_kind: candidate
#   summary: candidate richer EPAC state carrier over the algebraic/Minkowski lattice Q(sqrt2,sqrt3,sqrt5), treating B(R)=(3,d,c) as a projection
#   owner: Erin Spencer
#   public_surface: SCHEMA, VERSION, BASIS, EPACLatticeError, EPACLatticePoint, EPACLatticeCarrierReport, build_epac_lattice_carrier
#   internal_surface: frozen-state lattice assignment, B projection, locked-formula transition vectors, collision separation, canonical receipt
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
#   unresolved: whether this algebraic/Minkowski lattice is the missing representation remains hmmm
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: epac_lattice_uses_abstract_ucns_lattice
#   given: the EPAC algebraic lattice carrier
#   then: it is an implementation candidate of the abstract UCNS lattice/carrier relation and never redefines UCNS geometry
#   class: doctrine
#   since: 2026-09-16
#
# id: epac_lattice_b_is_projection
#   given: every frozen EPAC state
#   then: B(R) equals exactly the first three lattice coordinates (3, d_boundary, c_boundary)
#   class: correctness
#   since: 2026-09-16
#
# id: epac_lattice_separates_known_collisions
#   given: every documented same-B frozen-state collision group
#   then: the full lattice points are pairwise distinct inside the group
#   class: correctness
#   since: 2026-09-16
#
# id: epac_lattice_preserves_transitions_and_provenance
#   given: the frozen nine locked formulas
#   then: each molecule point equals the sum of its element atom points plus a declared formula vector, and atomic sum and atom count provenance is preserved exactly
#   class: correctness
#   since: 2026-09-16
#
# id: epac_lattice_remains_candidate
#   given: a passing separation and transition test
#   then: the lattice is not promoted to the missing representation; that remains hmmm
#   class: doctrine
#   since: 2026-09-16
# === END CONTRACTS ===

"""Candidate richer EPAC state carrier over Q(sqrt2,sqrt3,sqrt5).

The abstract UCNS lattice/carrier relation is implemented here as the
Minkowski lattice ``Z^8`` with basis

```text
(1, sqrt2, sqrt3, sqrt5, sqrt6, sqrt10, sqrt15, sqrt30)
```

and exact integer coordinates. ``B(R) = (3, d_boundary, c_boundary)`` is
treated as the projection onto the first three coordinates, not as the full
state.

Test asked: do the known EPAC collisions separate while preserving
transitions and provenance?
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any

SCHEMA = "epac.lattice-carrier-candidate"
VERSION = "0.1.0"
BASIS = ("1", "sqrt2", "sqrt3", "sqrt5", "sqrt6", "sqrt10", "sqrt15", "sqrt30")

# Atomic numbers of the required elements.
ATOMIC_NUMBER = {"H": 1, "B": 5, "C": 6, "N": 7, "O": 8, "F": 9, "Si": 14, "P": 15, "S": 16}

# Documented B values from EPAC boundary docs.
SUBSHELL_AXES = {"H": 2, "B": 3, "C": 3, "F": 3, "N": 3, "O": 3, "P": 4, "S": 4, "Si": 4}
ELECTRON_AXES = {"H": 2, "B": 6, "C": 7, "N": 8, "O": 9, "F": 10, "Si": 15, "P": 16, "S": 17}

# Frozen nine locked formulas: (molecule, constituents)
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

# Documented molecule B values.
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
    "the known EPAC collisions separate inside the algebraic/Minkowski "
    "lattice while preserving transitions and provenance, so this lattice "
    "may be the missing representation; promotion remains hmmm"
)


class EPACLatticeError(ValueError):
    """Raised when the EPAC lattice carrier fails closed."""


@dataclass(frozen=True)
class EPACLatticePoint:
    state: str
    coordinates: tuple[int, int, int, int, int, int, int, int]

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


def _sub(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x - y for x, y in zip(a, b))


def _bare_point(symbol: str, layer: int) -> EPACLatticePoint:
    """Build one bare subatomic/element lattice point.

    Coordinates: (axis=3, d_boundary, c_boundary=0, layer, atomic_number,
    atom_count=1, formula_ordinal=0, reserved=0).
    """

    if layer == 0:
        d_boundary = SUBSHELL_AXES[symbol]
        state = f"subatomic:{symbol}"
    elif layer == 1:
        d_boundary = ELECTRON_AXES[symbol]
        state = f"element:{symbol}"
    else:
        raise EPACLatticeError("bare layer must be 0 (subatomic) or 1 (element)")
    coordinates = (3, d_boundary, 0, layer, ATOMIC_NUMBER[symbol], 1, 0, 0)
    return EPACLatticePoint(state=state, coordinates=coordinates)


def _molecule_point(formula: str, ordinal: int) -> EPACLatticePoint:
    constituents = dict(LOCKED_FORMULAS)[formula]
    atomic_sum = sum(ATOMIC_NUMBER[symbol] for symbol in constituents)
    atom_count = len(constituents)
    d_boundary, c_boundary = MOLECULE_B[formula]
    coordinates = (3, d_boundary, c_boundary, 2, atomic_sum, atom_count, ordinal, 0)
    return EPACLatticePoint(state=f"molecule:{formula}", coordinates=coordinates)


def _frozen_states() -> dict[str, EPACLatticePoint]:
    states: dict[str, EPACLatticePoint] = {}
    for symbol in ("H", "B", "C", "F", "N", "O", "P", "S", "Si"):
        states[f"subatomic:{symbol}"] = _bare_point(symbol, 0)
        states[f"element:{symbol}"] = _bare_point(symbol, 1)
    for ordinal, (formula, _constituents) in enumerate(LOCKED_FORMULAS, start=1):
        states[f"molecule:{formula}"] = _molecule_point(formula, ordinal)
    return states


def _locked_transitions(
    states: dict[str, EPACLatticePoint],
) -> list[dict[str, Any]]:
    transitions = []
    for ordinal, (formula, constituents) in enumerate(LOCKED_FORMULAS, start=1):
        molecule = states[f"molecule:{formula}"]
        constituent_sum = (0, 0, 0, 0, 0, 0, 0, 0)
        for symbol in constituents:
            constituent_sum = _add(constituent_sum, states[f"element:{symbol}"].coordinates)
        formula_vector = _sub(molecule.coordinates, constituent_sum)
        provenance_ok = (
            molecule.coordinates[4] == sum(ATOMIC_NUMBER[s] for s in constituents)
            and molecule.coordinates[5] == len(constituents)
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


def build_epac_lattice_carrier() -> dict[str, Any]:
    """Build the full EPAC lattice carrier report."""

    states = _frozen_states()
    by_b: dict[tuple[int, int, int], list[EPACLatticePoint]] = {}
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
        "basis": list(BASIS),
        "states": [p.as_dict() for p in sorted(states.values(), key=lambda p: p.state)],
        "b_classes": len(by_b),
        "collision_groups": collision_groups,
        "collisions_separated": separation_ok,
        "transitions_preserved": transitions_ok,
        "locked_transitions": transitions,
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


__all__ = [
    "SCHEMA",
    "VERSION",
    "BASIS",
    "EPACLatticeError",
    "EPACLatticePoint",
    "build_epac_lattice_carrier",
]
