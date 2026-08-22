from __future__ import annotations

# === CHECKS ===
# id: check_canon_digest_deterministic
#   proves: metapat_canon_digest_deterministic
#   call: self::test_canon_digest_is_deterministic
#   mutates: none
#   cleanup: none
#
# id: check_envelope_exact_provenance
#   proves: metapat_envelope_exact_provenance
#   call: self::test_root_spine_envelope_preserves_exact_sources_and_constraints
#   mutates: none
#   cleanup: none
#
# id: check_envelope_roundtrip
#   proves: metapat_envelope_roundtrip
#   call: self::test_envelope_roundtrip_preserves_hmmm
#   mutates: none
#   cleanup: none
#
# id: check_envelope_rotation_visible
#   proves: metapat_envelope_rotation_visible
#   call: self::test_canon_or_constraint_rotation_changes_provenance
#   mutates: none
#   cleanup: none
#
# id: check_labels_not_measurements
#   proves: metapat_labels_not_measurements
#   call: self::test_envelope_contains_no_measurement_values
#   mutates: none
#   cleanup: none
#
# id: check_envelope_tamper_rejected
#   proves: metapat_envelope_tamper_rejected
#   call: self::test_tampered_provenance_digest_fails_closed
#   mutates: none
#   cleanup: none
#
# id: check_unknown_envelope_field_rejected
#   proves: metapat_envelope_unknown_field_rejected
#   call: self::test_unknown_schema_field_fails_closed
#   mutates: none
#   cleanup: none
#
# id: check_envelope_canonical_json
#   proves: metapat_envelope_canonical_json
#   call: self::test_serialized_envelope_is_canonical_json
#   mutates: none
#   cleanup: none
#
# id: check_envelope_scalar_types_strict
#   proves: metapat_envelope_type_strict
#   call: self::test_from_dict_rejects_scalar_field_coercion
#   mutates: none
#   cleanup: none
#
# id: check_envelope_sequence_types_strict
#   proves: metapat_envelope_type_strict
#   call: self::test_from_dict_rejects_string_for_sequence_fields
#   mutates: none
#   cleanup: none
# === END CHECKS ===

import json

import pytest

from metapat import (
    MODULE_ENVELOPE_SCHEMA_VERSION,
    MODULE_KINDS,
    ROOT_SPINE,
    MetapatModuleEnvelope,
    build_module_envelope,
    canon_digest,
    canonical_canon_data,
    root_spine_module_envelope,
)


def test_canon_digest_is_deterministic() -> None:
    first = canon_digest()
    second = canon_digest()
    assert first == second
    assert len(first) == 64
    assert canonical_canon_data()["root_spine"] == list(ROOT_SPINE)
    assert canonical_canon_data()["canon_file_blobs"]


def test_root_spine_envelope_preserves_exact_sources_and_constraints() -> None:
    envelope = root_spine_module_envelope()
    assert MODULE_ENVELOPE_SCHEMA_VERSION == "1.2.0"
    assert envelope.module_id == "metapat.root_spine"
    assert envelope.module_kind == "canon-module"
    assert envelope.source_statement_refs == (
        "AXIOMS.md#1-legible-difference::statement-1",
        "AXIOMS.md#2-boundary::statement-1",
        "AXIOMS.md#3-simplex::statement-1",
        "AXIOMS.md#2-boundary::statement-2",
        "AXIOMS.md#3-simplex::statement-3",
    )
    assert envelope.source_statements == ROOT_SPINE
    assert len(envelope.source_statement_refs) == len(ROOT_SPINE)
    assert {
        "canon-module",
        "distinction",
        "simplex",
        "boundary-simplex",
        "tensor",
        "energy-state",
        "scalar",
        "vector",
        "relation",
        "gradient",
        "transformation",
        "registration",
        "observer",
        "time",
        "question",
        "postulate",
        "theorem",
        "theory",
    } <= MODULE_KINDS
    assert envelope.constraints
    assert envelope.permitted_interpretations
    assert envelope.canon_digest == canon_digest()
    assert envelope.provenance_digest
    assert any(value.startswith("hmmm:") for value in envelope.unresolved_constraints)


def test_envelope_roundtrip_preserves_hmmm() -> None:
    envelope = root_spine_module_envelope()
    reconstructed = MetapatModuleEnvelope.from_json(envelope.to_json())
    assert reconstructed == envelope
    assert reconstructed.to_json() == envelope.to_json()
    assert reconstructed.unresolved_constraints == envelope.unresolved_constraints


def test_canon_or_constraint_rotation_changes_provenance() -> None:
    original = root_spine_module_envelope()
    rotated_canon = build_module_envelope(
        module_id=original.module_id,
        module_kind=original.module_kind,
        source_statement_refs=original.source_statement_refs,
        source_statements=original.source_statements,
        constraints=original.constraints,
        permitted_interpretations=original.permitted_interpretations,
        unresolved_constraints=original.unresolved_constraints,
        canon_version="metapat-canon-v2-test",
        canon_identity="0" * 64,
    )
    changed_constraint = build_module_envelope(
        module_id=original.module_id,
        module_kind=original.module_kind,
        source_statement_refs=original.source_statement_refs,
        source_statements=original.source_statements,
        constraints=(*original.constraints, "Test-only changed constraint."),
        permitted_interpretations=original.permitted_interpretations,
        unresolved_constraints=original.unresolved_constraints,
    )
    assert rotated_canon.provenance_digest != original.provenance_digest
    assert changed_constraint.provenance_digest != original.provenance_digest


def test_envelope_contains_no_measurement_values() -> None:
    data = root_spine_module_envelope().to_dict()
    forbidden = {
        "measurements",
        "measured_values",
        "metric_values",
        "edcm_readouts",
        "measurement_validity",
        "theorem_status",
    }
    assert forbidden.isdisjoint(data)


def test_tampered_provenance_digest_fails_closed() -> None:
    data = root_spine_module_envelope().to_dict()
    data["constraints"] = [*data["constraints"], "tampered"]
    with pytest.raises(ValueError, match="provenance_digest"):
        MetapatModuleEnvelope.from_dict(data)


def test_unknown_schema_field_fails_closed() -> None:
    data = root_spine_module_envelope().to_dict()
    data["measured_value"] = 1
    with pytest.raises(ValueError, match="unknown envelope fields"):
        MetapatModuleEnvelope.from_dict(data)


def test_serialized_envelope_is_canonical_json() -> None:
    encoded = root_spine_module_envelope().to_json()
    assert json.dumps(json.loads(encoded), ensure_ascii=False, sort_keys=True, separators=(",", ":")) == encoded


def test_from_dict_rejects_scalar_field_coercion() -> None:
    data = root_spine_module_envelope().to_dict()
    data["module_id"] = 7
    with pytest.raises(ValueError, match="module_id must be a string"):
        MetapatModuleEnvelope.from_dict(data)


def test_from_dict_rejects_string_for_sequence_fields() -> None:
    data = root_spine_module_envelope().to_dict()
    data["constraints"] = "not-an-array"
    with pytest.raises(ValueError, match="constraints must be an array"):
        MetapatModuleEnvelope.from_dict(data)
