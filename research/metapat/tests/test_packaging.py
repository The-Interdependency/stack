from __future__ import annotations

# === CHECKS ===
# id: check_package_version_matches_metadata
#   proves: metapat_package_version_matches_metadata
#   call: self::test_public_version_matches_distribution_metadata
#   mutates: none
#   cleanup: none
#
# id: check_typed_marker_packaged
#   proves: metapat_package_typed_marker
#   call: self::test_typed_marker_is_packaged
#   mutates: filesystem_read
#   cleanup: none
#
# id: check_base_import_without_ucns
#   proves: metapat_base_import_without_ucns
#   call: self::test_base_import_does_not_require_ucns
#   mutates: none
#   cleanup: none
#
# id: check_no_public_local_ucns
#   proves: metapat_no_public_local_ucns
#   call: self::test_public_surface_contains_no_local_ucns_object_class
#   mutates: none
#   cleanup: none
#
# id: check_root_fixture_packaged
#   proves: metapat_root_fixture_packaged
#   call: self::test_root_spine_fixture_is_packaged_and_exact
#   mutates: filesystem_read
#   cleanup: none
#
# id: check_pipe_fixture_packaged
#   proves: metapat_pipe_fixture_packaged
#   call: self::test_electromagnetic_pipe_fixture_is_packaged_and_exact
#   mutates: filesystem_read
#   cleanup: none
# === END CHECKS ===

from importlib.metadata import version
from importlib.resources import files

import metapat


def test_public_version_matches_distribution_metadata() -> None:
    assert metapat.__version__ == "0.7.0"
    assert version("metapat") == metapat.__version__


def test_typed_marker_is_packaged() -> None:
    assert files("metapat").joinpath("py.typed").is_file()


def test_base_import_does_not_require_ucns() -> None:
    assert callable(metapat.root_spine_module_envelope)
    assert callable(metapat.electromagnetic_pipe_design)
    envelope = metapat.root_spine_module_envelope()
    design = metapat.electromagnetic_pipe_design()
    assert envelope.module_id == "metapat.root_spine"
    assert envelope.provenance_digest
    assert design.phase_circuit_count == 18
    assert design.three_phase_system_count == 6


def test_public_surface_contains_no_local_ucns_object_class() -> None:
    assert "UCNSObject" not in metapat.__all__
    assert not hasattr(metapat, "UCNSObject")


def test_root_spine_fixture_is_packaged_and_exact() -> None:
    fixture = files("metapat").joinpath("fixtures/root-spine-envelope-v2.json")
    assert fixture.is_file()
    assert fixture.read_text(encoding="utf-8").strip() == metapat.root_spine_module_envelope().to_json()
    assert not files("metapat").joinpath("fixtures/root-spine-envelope-v1.json").is_file()


def test_electromagnetic_pipe_fixture_is_packaged_and_exact() -> None:
    fixture = files("metapat").joinpath("fixtures/three-phase-electromagnetic-pipe-v2.json")
    assert fixture.is_file()
    assert fixture.read_text(encoding="utf-8").strip() == metapat.electromagnetic_pipe_design().to_json()
    assert not files("metapat").joinpath("fixtures/three-phase-electromagnetic-pipe-v1.json").is_file()
