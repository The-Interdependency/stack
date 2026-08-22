"""Executable canon contract tests for the installed METAPAT surface."""

# === CHECKS ===
# id: check_root_spine_exact
#   proves: metapat_root_spine_exact
#   call: self::test_root_spine_contains_current_axioms
#   mutates: none
#   cleanup: none
#
# id: check_time_registration_separated
#   proves: metapat_time_not_registration
#   call: self::test_time_and_registration_are_separated
#   mutates: none
#   cleanup: none
#
# id: check_boundary_change_changes_outcome
#   proves: boundary_change_changes_outcome
#   call: self::test_boundary_change_changes_outcome
#   mutates: none
#   cleanup: none
#
# id: check_tensor_precedes_time
#   proves: tensor_before_time
#   call: self::test_tensor_precedes_time
#   mutates: none
#   cleanup: none
#
# id: check_registration_not_time
#   proves: registration_not_time
#   call: self::test_registration_is_not_time
#   mutates: none
#   cleanup: none
#
# id: check_observer_role_registration
#   proves: observer_role_requires_registration
#   call: self::test_observer_role_by_registration
#   mutates: none
#   cleanup: none
#
# id: check_consciousness_optional
#   proves: consciousness_optional_observer_mode
#   call: self::test_consciousness_is_optional
#   mutates: none
#   cleanup: none
# === END CHECKS ===

import unittest

from metapat import TIME_DEFINITION, definitions, root_spine
from metapat.validation import (
    boundary_earns_its_keep,
    consciousness_is_optional,
    observer_role_by_registration,
    registration_is_not_time,
    tensor_precedes_time,
)


def test_root_spine_contains_current_axioms() -> None:
    assert root_spine() == (
        "Legible difference is distinction.",
        "Distinction defines boundaries.",
        "Boundaries define simplex.",
        "Boundary is simplex of distinction.",
        "Simplex holds or modifies energy in a state of being.",
    )


def test_time_and_registration_are_separated() -> None:
    defs = definitions()
    assert defs["METAPAT"] == "Meta Energy Theory — Axioms, Postulates, Theorems, and Theories."
    assert defs["time"] == "Time is sequential tensor alteration."
    assert "preserve, express, or transmit" in defs["registration"]
    assert defs["time"] != defs["registration"]
    assert TIME_DEFINITION == defs["time"]


def test_boundary_change_changes_outcome() -> None:
    assert boundary_earns_its_keep(
        source_state="fixed_source",
        target_state="fixed_target",
        boundary_state_a="open",
        boundary_state_b="filtered",
        outcome_a="passes",
        outcome_b="delayed",
    )
    assert not boundary_earns_its_keep(
        source_state="fixed_source",
        target_state="fixed_target",
        boundary_state_a="same",
        boundary_state_b="same",
        outcome_a="passes",
        outcome_b="delayed",
    )


def test_tensor_precedes_time() -> None:
    tensor_state = {"a": "held", "b": "held"}
    sequenced = (tensor_state, {"a": "altered", "b": "held"})
    assert tensor_precedes_time(tensor_state, sequenced)
    assert not tensor_precedes_time(None, sequenced)
    assert not tensor_precedes_time(tensor_state, (tensor_state,))


def test_registration_is_not_time() -> None:
    sequence = ({"t": 0}, {"t": 1})
    assert registration_is_not_time(sequence, None)
    assert registration_is_not_time(sequence, sequence)
    assert not registration_is_not_time(({"t": 0},), None)


def test_observer_role_by_registration() -> None:
    sequence = ({"t": 0}, {"t": 1})
    observer_simplex = {"registered": sequence}
    merely_present_simplex = {"state": "present"}
    assert observer_role_by_registration(observer_simplex, sequence)
    assert not observer_role_by_registration(merely_present_simplex, sequence)


def test_consciousness_is_optional() -> None:
    nonconscious_registration = ({"layer": 1}, {"layer": 2})
    conscious_story = "I remember the alteration."
    assert consciousness_is_optional(nonconscious_registration)
    assert consciousness_is_optional(nonconscious_registration, None)
    assert consciousness_is_optional(nonconscious_registration, conscious_story)
    assert consciousness_is_optional(nonconscious_registration, "")
    assert not consciousness_is_optional(None, conscious_story)


class MetapatContractTests(unittest.TestCase):
    def test_root_spine_contains_current_axioms(self) -> None:
        test_root_spine_contains_current_axioms()

    def test_time_and_registration_are_separated(self) -> None:
        test_time_and_registration_are_separated()

    def test_01_boundary_earns_its_keep(self) -> None:
        test_boundary_change_changes_outcome()

    def test_02_tensor_precedes_time(self) -> None:
        test_tensor_precedes_time()

    def test_03_registration_is_not_time(self) -> None:
        test_registration_is_not_time()

    def test_04_observer_role_by_registration(self) -> None:
        test_observer_role_by_registration()

    def test_05_consciousness_is_optional(self) -> None:
        test_consciousness_is_optional()
