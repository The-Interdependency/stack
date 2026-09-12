# === CHECKS ===
# id: check_geometry_public_surface_exclusion
#   proves: geometry_public_surface_excludes_nongeometric_domains
#   call: self::test_geometry_public_surface_excludes_removed_domains
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===

import importlib.util

import ucns


_REMOVED_MODULES = (
    "bridge",
    "edcm",
    "laboratory",
    "lexical_word_gonols",
    "oewn_definition_recursion",
    "public_gonol_functions",
    "relational_carrier",
)


def test_geometry_public_surface_excludes_removed_domains() -> None:
    exported = set(ucns.__all__)
    assert {
        "MobiusVesica",
        "MobiusVesicaParameters",
        "build_mobius_vesica",
        "MobiusSeedOfLife",
        "MobiusBandSpec",
        "build_mobius_seed_of_life",
        "StandingWaveModel",
        "build_native_mobius_standing_wave",
        "evaluate_capacity_channel_induction",
        "MobiusBandStandingWaveModel",
        "build_mobius_band_standing_wave",
        "evaluate_band_capacity_channel_induction",
    }.issubset(exported)
    assert not exported.intersection({
        "PublicGonolFunctionTable",
        "OEWNDefinitionLayer",
        "EdcmWordGonolProfile",
        "RelationalCarrier",
    })
    for module_name in _REMOVED_MODULES:
        assert importlib.util.find_spec(f"ucns.{module_name}") is None
