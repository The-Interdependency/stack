# === CHECKS ===
# id: check_metapat_base_survives_ucns_profile
#   proves: metapat_ucns_ordered_occurrence_provenance
#   call: self::test_base_metapat_remains_available
#   mutates: none
#   cleanup: none
#
# id: check_metapat_ucns_exact_identity
#   proves: metapat_ucns_exact_identity_or_inactive
#   call: self::test_missing_or_legacy_package_stays_inactive
#   mutates: process_import_state
#   cleanup: monkeypatch_restore
#
# id: check_metapat_ucns_order_and_no_transfer
#   proves: metapat_ucns_ordered_occurrence_provenance, metapat_ucns_no_authority_transfer
#   call: self::test_exact_profile_activates_and_preserves_order
#   mutates: process_import_state
#   cleanup: monkeypatch_restore
#
# id: check_metapat_ucns_archived_operations
#   proves: metapat_ucns_archived_operations_rejected
#   call: self::test_record_round_trip_and_legacy_boundaries
#   mutates: process_import_state
#   cleanup: monkeypatch_restore
# === END CHECKS ===

from __future__ import annotations

import sys
from types import ModuleType

import pytest

import metapat
import metapat.ucns as adapter_module
from metapat import root_spine_module_envelope


def _fake_exact_ucns() -> ModuleType:
    module = ModuleType("ucns")
    module.PRODUCER_EPOCH = adapter_module.SUPPORTED_PRODUCER_EPOCH
    module.PROFILE_ID, module.PROFILE_VERSION = adapter_module.SUPPORTED_PROFILE
    module.BRIDGE_SCHEMA_ID, module.BRIDGE_SCHEMA_VERSION = adapter_module.SUPPORTED_BRIDGE_SCHEMA

    class Cell:
        def __init__(self, *, payload=None, provenance=None):
            self.payload = payload
            self.provenance = provenance

    class Bound:
        def __init__(self, cells):
            self.cells = tuple(cells)

    class Bridge:
        schema_id = module.BRIDGE_SCHEMA_ID
        schema_version = module.BRIDGE_SCHEMA_VERSION
        producer_epoch = module.PRODUCER_EPOCH
        profile_id = module.PROFILE_ID
        profile_version = module.PROFILE_VERSION
        theorem_status_transfer = False
        edcm_measurement_validity_transfer = False
        metapat_validity_transfer = False

        def __init__(self, cells):
            self.cells = tuple(cells)
            self.stable_identity = "stable-" + str(len(cells))

        def to_json_bytes(self):
            return b'{"exact":true}'

        @classmethod
        def from_json_bytes(cls, raw):
            assert raw == b'{"exact":true}'
            return current_bridge[0]

        def __eq__(self, other):
            return self is other

    current_bridge = [None]

    class Profile:
        def bind(self, carrier):
            return Bound(carrier)

        def to_bridge(self, bound, *, source_commit, operator_history):
            assert source_commit == adapter_module.PINNED_UCNS_COMMIT
            assert operator_history == ("metapat-envelope-ordered-occurrence",)
            current_bridge[0] = Bridge(bound.cells)
            return current_bridge[0]

    module.Cell = Cell
    module.make_carrier = lambda cells: tuple(cells)
    module.EdcmMetapatOrderedOccurrenceProfile = Profile
    module.EdcmMetapatBridgeRecord = Bridge
    return module


def test_base_metapat_remains_available() -> None:
    assert metapat.root_spine()
    assert metapat.canonical_semantic_catalog()


def test_missing_or_legacy_package_stays_inactive(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(adapter_module, "_package_present", lambda: False)
    assert adapter_module.ucns_consumer_status().adapter_active is False

    legacy = ModuleType("ucns")
    legacy.UCNSObject = object
    monkeypatch.setitem(sys.modules, "ucns", legacy)
    monkeypatch.setattr(adapter_module.importlib, "import_module", lambda name: legacy)
    with pytest.raises(adapter_module.UCNSAdapterError, match="surface missing"):
        adapter_module.require_ucns()


def test_exact_profile_activates_and_preserves_order(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _fake_exact_ucns()
    monkeypatch.setattr(adapter_module, "_package_present", lambda: True)
    monkeypatch.setattr(adapter_module.importlib, "import_module", lambda name: module)
    status = adapter_module.ucns_consumer_status()
    assert status.producer_recognized and status.profile_supported and status.adapter_active

    envelope = root_spine_module_envelope()
    adaptation = adapter_module.adapt_envelope_to_ucns(envelope)
    assert len(adaptation.ucns_object.cells) == len(envelope.source_statements)
    assert [cell.provenance["source_ref"] for cell in adaptation.ucns_object.cells] == list(envelope.source_statement_refs)
    assert all(cell.payload is None for cell in adaptation.ucns_object.cells)
    assert adaptation.record.source_statements == envelope.source_statements
    assert adaptation.record.ucns_source_commit == adapter_module.PINNED_UCNS_COMMIT
    assert adaptation.record.theorem_status_transfer is False
    assert adaptation.record.measurement_validity_claim is False
    assert adaptation.record.metapat_validity_claim is False


def test_record_round_trip_and_legacy_boundaries(monkeypatch: pytest.MonkeyPatch) -> None:
    module = _fake_exact_ucns()
    monkeypatch.setattr(adapter_module.importlib, "import_module", lambda name: module)
    record = adapter_module.adapt_envelope_to_ucns(root_spine_module_envelope()).record
    assert adapter_module.UCNSAdaptationRecord.from_json(record.to_json()) == record
    assert "ucns-canonical-json-v1" in adapter_module.REJECTED_LEGACY_SCHEMAS
    with pytest.raises(adapter_module.UCNSAdapterError, match="not authorized"):
        adapter_module.compose(object(), object())
    with pytest.raises(adapter_module.UCNSAdapterError, match="archived adapter"):
        adapter_module.adapt_envelope_to_ucns(root_spine_module_envelope(), face_bits=(0,))
