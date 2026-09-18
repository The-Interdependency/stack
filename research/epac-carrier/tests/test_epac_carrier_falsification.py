# === CHECKS ===
# id: check_carrier_falsification_finds_identical_sigma_states
#   proves: carrier_falsification_finds_identical_sigma_states
#   call: self::test_finds_identical_sigma_states
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_carrier_falsification_kills_sigma_if_replaceable
#   proves: carrier_falsification_kills_sigma_if_replaceable
#   call: self::test_kills_sigma_if_replaceable
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_carrier_falsification_deprecates_minkowski_without_field_work
#   proves: carrier_falsification_deprecates_minkowski_without_field_work
#   call: self::test_deprecates_minkowski_without_field_work
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_carrier_falsification_does_not_import_epac_upward
#   proves: carrier_falsification_does_not_import_epac_upward
#   call: self::test_does_not_import_epac_upward
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_carrier_falsification_replacement_minimality
#   proves: carrier_falsification_replacement_minimality
#   call: self::test_replacement_minimality
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_carrier_falsification_pair_primitive
#   proves: carrier_falsification_pair_primitive
#   call: self::test_pair_primitive
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_carrier_falsification_period_valence_derivation
#   proves: carrier_falsification_period_valence_derivation
#   call: self::test_period_valence_derivation
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from epac_carrier_falsification import SCHEMA, build_carrier_falsification


def test_finds_identical_sigma_states() -> None:
    report = build_carrier_falsification()
    search = report["identical_sigma_search"]
    assert search["sigma_is_an_identity"] is False
    assert search["distinct_states_sharing_identical_sigma"] > 0
    # subatomic:H and element:H share sigma 1
    assert any("subatomic:H" in names and "element:H" in names for names in search["groups"].values())


def test_kills_sigma_if_replaceable() -> None:
    report = build_carrier_falsification()
    removal = report["sigma_removal"]
    assert removal["separation_survives_without_sigma"] is False
    replacement = report["sigma_replacement"]
    assert replacement["separation_survives_with_replacement"] is True
    assert replacement["collisions"] == {}
    identity = report["sigma_identity_serialization_audit"]
    assert "identity serialization" in identity["bare_scale_contribution"]


def test_deprecates_minkowski_without_field_work() -> None:
    report = build_carrier_falsification()
    minkowski = report["minkowski_field_work"]
    assert minkowski["plain_coordinate_classes"] == minkowski["field_norm_classes"]
    assert minkowski["field_structure_adds_measurable_distinction"] is False
    assert minkowski["verdict"] == "DEPRECATE"


def test_does_not_import_epac_upward() -> None:
    report = build_carrier_falsification()
    independence = report["ucns_pcea_independence"]
    assert independence["ucns_derives_richer_structure_independently"] is False
    assert independence["pcea_derives_richer_structure_independently"] is False
    assert report["schema"] == SCHEMA
    assert report["receipt_sha256"]


def test_replacement_minimality() -> None:
    report = build_carrier_falsification()
    audit = report["replacement_minimality_audit"]
    assert audit["full_tuple_separates"] is True
    # not minimal: group and valence are each dispensable
    assert audit["minimal_among_three_components"] is False
    assert audit["period_necessary"] is True
    minimal_subsets = {tuple(sorted(subset)) for subset in audit["minimal_subsets"]}
    assert minimal_subsets == {("group", "period"), ("period", "valence_electrons")}
    # period drop is the one that breaks separation
    assert audit["component_drops"]["period"]["separation_survives"] is False
    assert audit["strictly_finer_than_sigma_at_molecule_scale"] is True
    assert audit["alternative_electron_occupancy_separates"] is False


def test_period_valence_derivation() -> None:
    report = build_carrier_falsification()
    audit = report["period_valence_derivation_audit"]
    assert audit["Z_derivable_from_construction"] is True
    assert audit["period_derivable_from_stack_local_construction"] is False
    assert audit["valence_derivable_from_stack_local_construction"] is False
    assert audit["generating_receipts_location"].startswith("The-Interdependency/epac")
    assert "imported" in audit["verdict"]
    assert "UNRESOLVED" in audit["verdict"]


def test_pair_primitive() -> None:
    report = build_carrier_falsification()
    audit = report["pair_primitive_audit"]
    assert audit["column_equals_declared_valence_electrons"] is True
    assert audit["group_is_column_plus_ten_for_p_block"] is True
    assert audit["collapsed_coordinate_separates"] is True
    assert audit["collapsed_collisions"] == {}
    assert "outermost-shell" in audit["hat"]
