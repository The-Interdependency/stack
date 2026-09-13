# ratios: loc_comments=84:43 imports_exports=5:5 calls_definitions=39:5
# === CHECKS ===
# id: check_modular_orbit_mod9_times_two
#   proves: modular_orbit_action_decomposes_exact_permutation, modular_orbit_circle_embedding_is_exact
#   call: self::test_mod9_times_two_decomposes_expected_orbits
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_modular_orbit_mod9_times_seven
#   proves: modular_orbit_action_decomposes_exact_permutation
#   call: self::test_mod9_times_seven_decomposes_expected_orbits
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_modular_orbit_fails_closed
#   proves: modular_orbit_fails_closed_outside_permutation_boundary
#   call: self::test_invalid_carriers_fail_closed
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_modular_orbit_semantic_boundary
#   proves: modular_orbit_carries_geometry_not_domain_semantics
#   call: self::test_serialized_surface_contains_geometry_only
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_modular_orbit_candidate_standing
#   proves: modular_orbit_remains_candidate_until_ratified
#   call: self::test_modular_orbit_is_candidate_scoped_in_canon
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from ucns.modular_orbit import ModularOrbitError, build_modular_orbit_geometry


def test_mod9_times_two_decomposes_expected_orbits() -> None:
    geometry = build_modular_orbit_geometry(9, 2, range(1, 9))

    assert geometry.positions == (1, 2, 3, 4, 5, 6, 7, 8)
    assert geometry.orbits == ((1, 2, 4, 8, 7, 5), (3, 6))
    assert geometry.periods == (6, 2)
    assert geometry.target(7) == 5
    assert geometry.turn_of(1) == Fraction(1, 9)
    assert geometry.turn_of(8) == Fraction(8, 9)

    full = build_modular_orbit_geometry(9, 2)
    assert full.orbits == ((0,), (1, 2, 4, 8, 7, 5), (3, 6))


def test_mod9_times_seven_decomposes_expected_orbits() -> None:
    geometry = build_modular_orbit_geometry(9, 7, range(1, 9))

    assert geometry.orbits == ((1, 7, 4), (2, 5, 8), (3,), (6,))
    assert geometry.periods == (3, 3, 1, 1)


def test_invalid_carriers_fail_closed() -> None:
    with pytest.raises(ModularOrbitError):
        build_modular_orbit_geometry(1, 2)
    with pytest.raises(ModularOrbitError):
        build_modular_orbit_geometry(9, 2, ())
    with pytest.raises(ModularOrbitError):
        build_modular_orbit_geometry(9, 2, (1, 1))
    with pytest.raises(ModularOrbitError):
        build_modular_orbit_geometry(9, 2, (1, 2, 4))
    with pytest.raises(ModularOrbitError):
        build_modular_orbit_geometry(9, 3)

    valid = build_modular_orbit_geometry(9, 2, range(1, 9))
    with pytest.raises(ModularOrbitError):
        type(valid)(
            modulus=valid.modulus,
            multiplier=valid.multiplier,
            positions=valid.positions,
            action=valid.action,
            orbits=valid.orbits,
            periods=(99, 99),
            embedding=valid.embedding,
        )

    # Direct restoration must reject malformed position elements through the
    # declared ModularOrbitError boundary before sorting or hashing them.
    with pytest.raises(ModularOrbitError, match="noncanonical residue"):
        replace(valid, positions=(0, "x"))  # type: ignore[arg-type]
    with pytest.raises(ModularOrbitError, match="noncanonical residue"):
        replace(valid, positions=(0, []))  # type: ignore[arg-type]

    identity = build_modular_orbit_geometry(3, 1)
    for patch in (
        {"action": ((False, False), (True, True), (2.0, 2.0))},
        {"orbits": ((False,), (True,), (2.0,))},
        {"orbits": [list(orbit) for orbit in identity.orbits]},
        {"periods": (True, 1.0, 1)},
        {"orbits": None},
        {"orbits": ((0,), None, (2,))},
    ):
        with pytest.raises(ModularOrbitError):
            replace(identity, **patch)
    for query in (True, False, 1.0, Fraction(1), "1", []):
        with pytest.raises(ModularOrbitError):
            identity.target(query)
        with pytest.raises(ModularOrbitError):
            identity.turn_of(query)


def test_serialized_surface_contains_geometry_only() -> None:
    payload = build_modular_orbit_geometry(9, 2, range(1, 9)).as_dict()

    assert set(payload) == {
        "modulus",
        "multiplier",
        "positions",
        "action",
        "orbits",
        "periods",
        "embedding",
    }
    assert payload["embedding"][0] == {
        "residue": 1,
        "turn": {"numerator": 1, "denominator": 9},
    }


def test_modular_orbit_is_candidate_scoped_in_canon() -> None:
    canon = (Path(__file__).resolve().parents[1] / "CANON.md").read_text(encoding="utf-8")
    section = canon.split("## Modular orbit geometry", 1)[1].split(
        "## Continuum wave / gonal boundary trace", 1
    )[0]

    assert "candidate" in section.lower()
    assert "not ratified" in section.lower()
    assert "active cycle primitive" not in section.lower()
# ratios: loc_comments=84:43 imports_exports=5:5 calls_definitions=39:5
