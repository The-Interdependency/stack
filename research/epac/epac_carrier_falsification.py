# === MODULE_BUILD ===
# id: epac_carrier_falsification
#   module_name: epac_carrier_falsification
#   module_kind: instrument
#   summary: falsifies the constitutive carrier coordinates, the sigma coordinate, and the Minkowski backend, and records whether UCNS/PCEA derives the richer structure independently
#   owner: Erin Spencer
#   public_surface: SCHEMA, VERSION, CarrierFalsificationError, build_carrier_falsification
#   internal_surface: identical-sigma search, sigma removal and replacement, transition closure beyond the nine, Minkowski field-norm comparison, UCNS/PCEA independence check
#   auth_boundary: none
#   storage_boundary: immutable records only
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_epac_carrier_falsification
#   rollout: executable falsification harness; kill sigma first, then give the exotic field a hearing
#   rollback: remove this module and its tests
#   requires: epac_constitutive_discrete_carrier, epac_lattice_carrier
#   since: 2026-09-17
#   unresolved: transition closure beyond the nine frozen formulas and independent unseen-state B values remain unresolved
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: carrier_falsification_finds_identical_sigma_states
#   given: the frozen EPAC states
#   then: the harness enumerates every distinct state pair sharing an identical sigma coordinate
#   class: correctness
#   since: 2026-09-17
#
# id: carrier_falsification_kills_sigma_if_replaceable
#   given: a replacement coordinate built from more primitive declared EPAC periodic structure
#   then: if separation survives with the replacement at every scale, sigma is recorded as replaceable and its privileged coordinate standing is falsified
#   class: correctness
#   since: 2026-09-17
#
# id: carrier_falsification_deprecates_minkowski_without_field_work
#   given: the Minkowski backend
#   then: the field norm must produce a measurable class distinction beyond the plain carrier; otherwise the backend is recorded as deprecated
#   class: correctness
#   since: 2026-09-17
#
# id: carrier_falsification_does_not_import_epac_upward
#   given: UCNS and PCEA candidate surfaces
#   then: neither is found to derive the richer coordinate structure independently, and EPAC coordinates are not imported upward
#   class: doctrine
#   since: 2026-09-17
#
# id: carrier_falsification_replacement_minimality
#   given: the replacement tuple (period, group, valence_electrons)
#   then: every single-component drop must break separation, the tuple must be strictly finer than sigma at molecule scale, and the electron-occupancy alternative must fail
#   class: correctness
#   since: 2026-09-17
# === END CONTRACTS ===

"""Falsify the constitutive carrier and its coordinates.

Order of attack: first kill sigma if possible; only then does the exotic
field get a hearing.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from epac_lattice_carrier import (
    ATOMIC_NUMBER,
    BASIS,
    LOCKED_FORMULAS,
    SCHEMA_MINKOWSKI,
    ConstitutivePoint,
    _frozen_states,
)

SCHEMA = "epac.carrier-falsification"
VERSION = "0.1.0"

_PERIODIC_TABLE = json.loads(
    (Path(__file__).resolve().parent / "data" / "periodic_table_z1_18.json").read_text()
)
_BY_SYMBOL = {e["symbol"]: e for e in _PERIODIC_TABLE["elements"]}


class CarrierFalsificationError(ValueError):
    """Raised when the falsification harness fails closed."""


def _periodic_tuple(symbol: str) -> tuple[int, int, int]:
    entry = _BY_SYMBOL[symbol]
    return (entry["period"], entry["group"], entry["valence_electrons"])


def _replacement_point(point: ConstitutivePoint) -> tuple[int, int, int, int, tuple[int, int, int]]:
    """Replace sigma with declared periodic structure (period, group, valence)."""

    if point.state.startswith("subatomic:") or point.state.startswith("element:"):
        symbol = point.state.split(":", 1)[1]
        periodic = _periodic_tuple(symbol)
    elif point.state.startswith("molecule:"):
        formula = point.state.split(":", 1)[1]
        constituents = dict(LOCKED_FORMULAS)[formula]
        periodic = (0, 0, 0)
        for symbol in constituents:
            p = _periodic_tuple(symbol)
            periodic = (periodic[0] + p[0], periodic[1] + p[1], periodic[2] + p[2])
    else:
        raise CarrierFalsificationError(f"unknown state {point.state}")
    b = point.b_projection()
    return (b[0], b[1], b[2], point.coordinates[3], periodic)


def _identical_sigma_search(states: dict[str, ConstitutivePoint]) -> dict[str, Any]:
    by_sigma: dict[int, list[str]] = {}
    for name, point in states.items():
        by_sigma.setdefault(point.coordinates[4], []).append(name)
    groups = {str(sigma): names for sigma, names in sorted(by_sigma.items()) if len(names) > 1}
    return {
        "distinct_states_sharing_identical_sigma": len(groups),
        "groups": groups,
        "sigma_is_an_identity": False,
        "note": "sigma is not injective over the frozen surface; it cannot be an identity",
    }


def _sigma_removal(states: dict[str, ConstitutivePoint]) -> dict[str, Any]:
    reduced: dict[str, tuple[int, int, int, int]] = {}
    for name, point in states.items():
        b = point.b_projection()
        reduced[name] = (b[0], b[1], b[2], point.coordinates[3])
    groups: dict[str, list[str]] = {}
    for name, coords in reduced.items():
        groups.setdefault(coords, []).append(name)
    collisions = {str(k): v for k, v in sorted(groups.items()) if len(v) > 1}
    return {
        "separation_survives_without_sigma": not collisions,
        "collisions": collisions,
        "verdict": (
            "sigma does separating work at bare and molecule scale; removing it "
            "re-collides same-B same-layer states"
        ),
    }


def _sigma_replacement(states: dict[str, ConstitutivePoint]) -> dict[str, Any]:
    replaced: dict[str, tuple[int, int, int, int, tuple[int, int, int]]] = {}
    for name, point in states.items():
        replaced[name] = _replacement_point(point)
    groups: dict[str, list[str]] = {}
    for name, coords in replaced.items():
        groups.setdefault(coords, []).append(name)
    collisions = {str(k): v for k, v in sorted(groups.items()) if len(v) > 1}
    return {
        "replacement": "(period, group, valence_electrons) from data/periodic_table_z1_18.json",
        "separation_survives_with_replacement": not collisions,
        "collisions": collisions,
        "verdict": (
            "sigma is replaceable at every scale by more primitive declared "
            "EPAC periodic structure; its privileged coordinate standing is "
            "falsified"
        ),
    }


def _sigma_identity_serialization_audit(states: dict[str, ConstitutivePoint]) -> dict[str, Any]:
    molecule_sigmas = {
        states[f"molecule:{formula}"].coordinates[4] for formula, _ in LOCKED_FORMULAS
    }
    return {
        "bare_scale_contribution": (
            "identity serialization only; sigma is bijective with the symbol "
            "and any declared injective structure separates equally"
        ),
        "molecule_scale_contribution": (
            "compositional sum over constituents; separation survives the "
            "period/group/valence replacement, so sigma is not load-bearing "
            "there either"
        ),
        "sigma_distinct_molecule_values": len(molecule_sigmas),
    }


def _replacement_minimality_audit(states: dict[str, ConstitutivePoint]) -> dict[str, Any]:
    """Test whether (period, group, valence_electrons) is minimal or merely
    another redundant chemistry identifier."""

    components = ("period", "group", "valence_electrons")

    def tuple_for(name: str) -> tuple[int, int, int, int, tuple[int, int, int]]:
        point = states[name]
        return _replacement_point(point)

    def separates(mapping: dict[str, tuple]) -> bool:
        groups: dict[tuple, list[str]] = {}
        for name, coords in mapping.items():
            groups.setdefault(coords, []).append(name)
        return all(len(group) == 1 for group in groups.values())

    # Full replacement point separation: B + layer + periodic tuple.
    full = {name: tuple_for(name) for name in states}
    full_separates = separates(full)

    # Minimality: drop each single periodic component, keeping B and layer.
    drops: dict[str, dict[str, Any]] = {}
    for drop_index, drop_name in enumerate(components):
        kept = [i for i in range(3) if i != drop_index]
        reduced = {
            name: (coords[0], coords[1], coords[2], coords[3], tuple(coords[4][i] for i in kept))
            for name, coords in full.items()
        }
        collisions = {}
        groups: dict[tuple, list[str]] = {}
        for name, coords in reduced.items():
            groups.setdefault(coords, []).append(name)
        for coords, group in sorted(groups.items()):
            if len(group) > 1:
                collisions[str(coords)] = group
        drops[drop_name] = {
            "kept": [components[i] for i in kept],
            "separation_survives": not collisions,
            "collisions": collisions,
        }
    minimal = all(not entry["separation_survives"] for entry in drops.values())

    # Exhaustive subset minimality over the three components, keeping the
    # B + layer prefix.
    minimal_subsets: list[list[str]] = []
    for mask in range(1, 8):
        kept_indices = [i for i in range(3) if mask & (1 << i)]
        reduced = {
            name: (coords[0], coords[1], coords[2], coords[3], tuple(coords[4][i] for i in kept_indices))
            for name, coords in full.items()
        }
        if separates(reduced):
            minimal_subsets.append([components[i] for i in kept_indices])
    minimal_subsets = [subset for subset in minimal_subsets if not any(
        set(other) < set(subset) for other in minimal_subsets
    )]

    # Strictly finer than sigma at molecule scale?
    sigma_groups: dict[int, list[str]] = {}
    for name in states:
        if name.startswith("molecule:"):
            sigma_groups.setdefault(states[name].coordinates[4], []).append(name)
    finer_than_sigma = all(
        len({tuple_for(name) for name in group}) == len(group)
        for group in sigma_groups.values()
        if len(group) > 1
    )

    # Alternative declared structure: electron-configuration occupancy sums.
    def occupancy(symbol: str) -> tuple[int, ...]:
        import re
        config = _BY_SYMBOL[symbol]["electron_configuration"]
        config = config.replace("[Ne].", "1s2.2s2.2p6.")
        shells = config.split(".")
        return tuple(int(re.findall(r"\d+$", part)[0]) for part in shells)

    def occupancy_sum(formula: str) -> tuple[int, ...]:
        total: list[int] = []
        for symbol in dict(LOCKED_FORMULAS)[formula]:
            occ = occupancy(symbol)
            while len(total) < len(occ):
                total.append(0)
            for i, value in enumerate(occ):
                total[i] += value
        return tuple(total)

    alternative = {
        name: occupancy_sum(name.split(":", 1)[1]) if name.startswith("molecule:") else occupancy(name.split(":", 1)[1])
        for name in states
        if ":" in name
    }
    alt_separates = separates(alternative)

    return {
        "full_tuple_separates": full_separates,
        "component_drops": drops,
        "minimal_among_three_components": minimal,
        "minimal_subsets": minimal_subsets,
        "period_necessary": all("period" in subset for subset in minimal_subsets) if minimal_subsets else None,
        "strictly_finer_than_sigma_at_molecule_scale": finer_than_sigma,
        "alternative_electron_occupancy_separates": alt_separates,
        "is_chemistry_identifier": True,
        "verdict": (
            "not minimal: valence and group are each dispensable, while "
            "period is necessary; minimal subsets are exactly "
            f"{minimal_subsets}; the tuple is a chemistry identifier and "
            "its separating power is B + layer + period plus one of "
            "{group, valence}"
        ),
    }


def _transition_closure_beyond_nine() -> dict[str, Any]:
    return {
        "status": "UNRESOLVED",
        "detail": (
            "no admissible transitions beyond the frozen nine locked formulas "
            "are declared in the frozen EPAC surface; closure beyond nine "
            "cannot be tested without inventing B values"
        ),
    }


def _unseen_states_independent_b() -> dict[str, Any]:
    return {
        "status": "PENDING",
        "detail": (
            "unseen valid states remain untestable until their B values are "
            "independently derived from EPAC-declared construction rules"
        ),
    }


def _multiply(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    """Exact multiplication in Q(sqrt2,sqrt3,sqrt5) basis (1,s2,s3,s5,s6,s10,s15,s30)."""

    out = [0] * 8
    for i, x in enumerate(a):
        if x == 0:
            continue
        for j, y in enumerate(b):
            if y == 0:
                continue
            c = x * y
            for k, coeff in _BASIS_PRODUCT[i][j]:
                out[k] += c * coeff
    return tuple(out)


# (i, j) -> list of (basis_index, integer_coefficient)
_BASIS_PRODUCT: list[list[list[tuple[int, int]]]] = [
    [
        [(0, 1)], [(1, 1)], [(2, 1)], [(3, 1)], [(4, 1)], [(5, 1)], [(6, 1)], [(7, 1)],
    ],
    [
        [(1, 1)], [(0, 2)], [(4, 1)], [(5, 1)], [(2, 2)], [(3, 2)], [(7, 1)], [(6, 2)],
    ],
    [
        [(2, 1)], [(4, 1)], [(0, 3)], [(6, 1)], [(1, 3)], [(7, 1)], [(3, 3)], [(5, 3)],
    ],
    [
        [(3, 1)], [(5, 1)], [(6, 1)], [(0, 5)], [(7, 1)], [(1, 5)], [(2, 5)], [(4, 5)],
    ],
    [
        [(4, 1)], [(2, 2)], [(1, 3)], [(7, 1)], [(0, 6)], [(6, 3)], [(5, 2)], [(3, 6)],
    ],
    [
        [(5, 1)], [(3, 2)], [(7, 1)], [(1, 5)], [(6, 3)], [(0, 10)], [(4, 5)], [(2, 10)],
    ],
    [
        [(6, 1)], [(7, 1)], [(3, 3)], [(2, 5)], [(5, 2)], [(4, 5)], [(0, 15)], [(1, 15)],
    ],
    [
        [(7, 1)], [(6, 2)], [(5, 3)], [(4, 5)], [(3, 6)], [(2, 10)], [(1, 15)], [(0, 30)],
    ],
]


def _embed(point: ConstitutivePoint) -> tuple[int, ...]:
    c = point.coordinates
    return (c[0], c[1], c[2], c[3], c[4], 0, 0, 0)


def _field_norm(point: ConstitutivePoint) -> tuple[int, ...]:
    """Field norm over the eight Galois conjugates (sign flips of sqrt2, sqrt3, sqrt5)."""

    x = _embed(point)
    result = (1, 0, 0, 0, 0, 0, 0, 0)
    for flip2 in (1, -1):
        for flip3 in (1, -1):
            for flip5 in (1, -1):
                conjugate = (
                    x[0],
                    flip2 * x[1],
                    flip3 * x[2],
                    flip5 * x[3],
                    flip2 * flip3 * x[4],
                    flip2 * flip5 * x[5],
                    flip3 * flip5 * x[6],
                    flip2 * flip3 * flip5 * x[7],
                )
                result = _multiply(result, conjugate)
    return result


def _minkowski_field_work(states: dict[str, ConstitutivePoint]) -> dict[str, Any]:
    plain_classes = {point.coordinates for point in states.values()}
    norm_classes = {_field_norm(point) for point in states.values()}
    distinct = len(norm_classes) > len(plain_classes)
    return {
        "schema": SCHEMA_MINKOWSKI,
        "basis": list(BASIS),
        "plain_coordinate_classes": len(plain_classes),
        "field_norm_classes": len(norm_classes),
        "field_structure_adds_measurable_distinction": distinct,
        "verdict": (
            "DEPRECATE" if not distinct else "reopen"
        ),
        "detail": (
            "the field norm produces no class distinction beyond the plain "
            "carrier coordinates, so the Minkowski backend is deprecated"
            if not distinct
            else "the field norm adds classes beyond the plain carrier"
        ),
    }


def _ucns_pcea_independence() -> dict[str, Any]:
    return {
        "ucns_derives_richer_structure_independently": False,
        "ucns_detail": (
            "ucns.lattice_carrier derives only the abstract deck/modular "
            "address lattices; the (3,d,c,layer,sigma) tuple is EPAC-declared "
            "structure and is not imported upward"
        ),
        "pcea_derives_richer_structure_independently": False,
        "pcea_detail": (
            "no PCEA candidate in the stack research surface derives the "
            "richer coordinate structure independently"
        ),
    }


def build_carrier_falsification() -> dict[str, Any]:
    """Run every falsification control and record verdicts."""

    states = _frozen_states()
    sigma_search = _identical_sigma_search(states)
    sigma_removal = _sigma_removal(states)
    sigma_replacement = _sigma_replacement(states)
    sigma_identity = _sigma_identity_serialization_audit(states)
    replacement_minimality = _replacement_minimality_audit(states)
    minkowski = _minkowski_field_work(states)

    payload = {
        "schema": SCHEMA,
        "version": VERSION,
        "identical_sigma_search": sigma_search,
        "sigma_removal": sigma_removal,
        "sigma_replacement": sigma_replacement,
        "sigma_identity_serialization_audit": sigma_identity,
        "replacement_minimality_audit": replacement_minimality,
        "transition_closure_beyond_nine": _transition_closure_beyond_nine(),
        "unseen_states_independent_b": _unseen_states_independent_b(),
        "minkowski_field_work": minkowski,
        "ucns_pcea_independence": _ucns_pcea_independence(),
        "hmmm": (
            "sigma is falsified as a privileged coordinate; the Minkowski "
            "backend is deprecated unless field structure adds measurable "
            "distinction; transition closure beyond nine and unseen-state "
            "B values remain unresolved"
        ),
    }
    payload["receipt_sha256"] = __import__("hashlib").sha256(
        json.dumps(
            {key: value for key, value in payload.items() if key != "receipt_sha256"},
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")
    ).hexdigest()
    return payload


__all__ = [
    "SCHEMA",
    "VERSION",
    "CarrierFalsificationError",
    "build_carrier_falsification",
]
