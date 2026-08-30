"""Checks for strict METAPAT semantic relation records."""

# === CHECKS ===
# id: check_relation_vocabulary_bounded
#   proves: metapat_relation_vocabulary_bounded
#   call: self::test_relation_vocabularies_are_bounded
#   mutates: none
#   cleanup: none
#
# id: check_relation_roundtrip_strict
#   proves: metapat_relation_roundtrip_strict
#   call: self::test_relation_roundtrip_and_types_are_strict
#   mutates: none
#   cleanup: none
#
# id: check_relation_tamper_rejected
#   proves: metapat_relation_tamper_rejected
#   call: self::test_relation_tamper_is_rejected
#   mutates: none
#   cleanup: none
#
# id: check_relation_no_status_transfer
#   proves: metapat_relation_no_status_transfer
#   call: self::test_relation_contains_no_status_transfer_surface
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from dataclasses import replace

import pytest

from metapat.relations import (
    CLAIM_STATUSES,
    RELATION_KINDS,
    MetapatModuleRelation,
    build_relation,
)


def _relation() -> MetapatModuleRelation:
    return build_relation(
        subject_module_id="metapat.theory.1",
        relation_kind="derived-from",
        object_module_id="metapat.axiom.1",
        evidence_status="INTERNAL-DERIVATION",
        source_statement_refs=("THEORIES.md#1::derived-from",),
        source_statements=("Derived from: Axiom 1.",),
        unresolved_constraints=("hmmm: no formal proof object",),
    )


def test_relation_vocabularies_are_bounded() -> None:
    assert RELATION_KINDS == {
        "defines",
        "derived-from",
        "constrains",
        "organizes",
        "applies",
        "constitutive-simultaneous",
    }
    assert "WORKING-POSTULATE" in CLAIM_STATUSES
    with pytest.raises(ValueError):
        build_relation(
            subject_module_id="a",
            relation_kind="resembles",
            object_module_id="b",
            evidence_status="DEFINITION",
            source_statement_refs=("x#y::z",),
            source_statements=("x",),
        )


def test_relation_roundtrip_and_types_are_strict() -> None:
    record = _relation()
    assert MetapatModuleRelation.from_json(record.to_json()) == record
    data = record.to_dict()
    data["extra"] = "no"
    with pytest.raises(ValueError, match="unknown"):
        MetapatModuleRelation.from_dict(data)
    data = record.to_dict()
    data["source_statement_refs"] = "not-an-array"
    with pytest.raises(ValueError, match="array"):
        MetapatModuleRelation.from_dict(data)


def test_relation_tamper_is_rejected() -> None:
    record = _relation()
    with pytest.raises(ValueError, match="digest"):
        replace(record, object_module_id="metapat.axiom.2")
    data = record.to_dict()
    data["source_statements"] = ["different"]
    with pytest.raises(ValueError, match="digest"):
        MetapatModuleRelation.from_dict(data)


def test_relation_contains_no_status_transfer_surface() -> None:
    data = _relation().to_dict()
    forbidden = {
        "theorem_status_transfer",
        "measurement_value",
        "metapat_validity_claim",
        "topology_validity_claim",
    }
    assert forbidden.isdisjoint(data)
