# === CHECKS ===
# id: check_metric_origin_instrument_boundary
#   proves: metric_origin_words_define_instrument_not_evidence
#   call: self::test_origin_record_contains_no_measurement_value
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_metric_origin_order_provenance
#   proves: metric_origin_preserves_order_identity_provenance
#   call: self::test_resolved_origin_uses_word_and_glyph_axes_in_order
#   requires: python3
#   timeout: 10
#   mutates: temporary sqlite fixture
#   cleanup: pytest tmp_path
#
# id: check_metric_origin_construct_identity
#   proves: metric_origin_preserves_order_identity_provenance
#   call: self::test_wrong_construct_receipt_fails_closed
#   requires: python3
#   timeout: 10
#   mutates: temporary sqlite fixture
#   cleanup: pytest tmp_path
#
# id: check_metric_origin_hmmm
#   proves: metric_origin_unresolved_fails_open_as_hmmm_not_closed
#   call: self::test_unresolved_origin_does_not_construct_components
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_metric_origin_receipt_schema
#   proves: metric_origin_receipt_binds_schema
#   call: self::test_receipt_hashes_complete_payload_except_receipt
#   requires: python3
#   timeout: 10
#   mutates: temporary sqlite fixture
#   cleanup: pytest tmp_path
# id: check_metric_origin_pinned_corpus_admission
#   proves: metric_origin_terms_admitted_by_pinned_corpus
#   call: self::test_all_resolved_terms_are_admitted_by_pinned_oewn
#   requires: python3, PyYAML, exact OEWN 2025 source
#   timeout: 60
#   mutates: none
#   cleanup: none
# id: check_metric_origin_source_fixture
#   proves: metric_origin_source_fixture_matches_pinned_edcm
#   call: self::test_stack_fixture_matches_exact_edcm_producer
#   requires: python3, exact EDCM metric-origin producer
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from hashlib import sha256
import importlib.util
import json
import os
import sqlite3
import sys
from pathlib import Path

import pytest

import english_gonol.edcm_metric_origins as origins
from english_gonol.hyperspace_construct import V2_MANIFEST_RECEIPT


def _fixture(tmp_path: Path, metric="F", standing="resolved"):
    source = {
        "schema":"edcm.metric-origin-spec-fixture","version":"0.3.0",
        "producer_repository":"The-Interdependency/edcm","producer_commit":"a"*40,
        "specs":{metric:{
            "surface_terms":["Fixation"],
            "construction_terms":["fixation","persistence","repetition"],
            "semantic_definition":"fixation is persistence across states",
            "standing":standing,"measurement_alignment":"proxy",
            "unresolved":["proxy gap"] if standing=="resolved" else ["collision"]}}
    }
    path=tmp_path/"source.json"
    path.write_text(json.dumps(source),encoding="utf-8")
    return path


def _db(tmp_path: Path):
    db=sqlite3.connect(tmp_path/"construct.db")
    db.executescript("""
    CREATE TABLE characters (id INTEGER PRIMARY KEY, scalar TEXT, public_position INTEGER);
    CREATE TABLE words (id INTEGER PRIMARY KEY, surface TEXT);
    CREATE TABLE word_characters (word_id INTEGER, ordinal INTEGER, character_id INTEGER);
    """)
    chars={}
    next_id=1
    words=["fixation","persistence","repetition"]
    for surface in words:
        for ch in surface+" ":
            if ch not in chars:
                chars[ch]=next_id
                db.execute("INSERT INTO characters VALUES (?,?,NULL)",(next_id,ch))
                next_id+=1
    for wid,surface in enumerate(words,1):
        db.execute("INSERT INTO words VALUES (?,?)",(wid,surface))
        for ordinal,ch in enumerate(surface):
            db.execute("INSERT INTO word_characters VALUES (?,?,?)",(wid,ordinal,chars[ch]))
    db.commit(); db.close()


def _verified(monkeypatch):
    monkeypatch.setattr(origins, "_assert_schema_boundary", lambda _db: None)
    monkeypatch.setattr(origins, "_logical_receipt", lambda _db: V2_MANIFEST_RECEIPT)


def test_resolved_origin_uses_word_and_glyph_axes_in_order(tmp_path, monkeypatch):
    _db(tmp_path); _verified(monkeypatch)
    record=origins.build_metric_origin_set(tmp_path,"F",fixture_path=_fixture(tmp_path))
    assert record.closed
    assert record.construct_receipt==V2_MANIFEST_RECEIPT
    assert record.source_text=="fixation persistence repetition"
    assert record.components[0].axis_origin=="O_W"
    assert any(x.axis_origin=="O_G" and x.surface==" " for x in record.components)
    assert record.producer_repository=="The-Interdependency/edcm"
    assert "proxy gap" in record.unresolved


def test_origin_record_contains_no_measurement_value(tmp_path, monkeypatch):
    _db(tmp_path); _verified(monkeypatch)
    record=origins.build_metric_origin_set(tmp_path,"F",fixture_path=_fixture(tmp_path))
    keys=record.to_dict()
    assert "value" not in keys
    assert "measurement" not in keys
    assert "score" not in keys
    assert record.source_text=="fixation persistence repetition"


def test_wrong_construct_receipt_fails_closed(tmp_path, monkeypatch):
    _db(tmp_path)
    monkeypatch.setattr(origins, "_assert_schema_boundary", lambda _db: None)
    monkeypatch.setattr(origins, "_logical_receipt", lambda _db: "0"*64)
    with pytest.raises(ValueError,match="construct receipt mismatch"):
        origins.build_metric_origin_set(tmp_path,"F",fixture_path=_fixture(tmp_path))


def test_unresolved_origin_does_not_construct_components(tmp_path):
    record=origins.build_metric_origin_set(
        tmp_path,"F",fixture_path=_fixture(tmp_path,standing="hmmm")
    )
    assert record.closed is False
    assert record.components==()
    assert record.construct_receipt=="hmmm"
    assert record.unresolved==("collision",)


def test_receipt_hashes_complete_payload_except_receipt(tmp_path, monkeypatch):
    _db(tmp_path); _verified(monkeypatch)
    record=origins.build_metric_origin_set(tmp_path,"F",fixture_path=_fixture(tmp_path))
    payload=record.to_dict()
    receipt=payload.pop("receipt_sha256")
    expected=sha256(json.dumps(
        payload,sort_keys=True,ensure_ascii=False,separators=(",",":"),allow_nan=False
    ).encode("utf-8")).hexdigest()
    assert receipt==expected
    assert payload["schema"]==origins.SCHEMA
    assert payload["version"]==origins.VERSION


def test_all_resolved_terms_are_admitted_by_pinned_oewn():
    root=os.environ.get("OEWN_SOURCE_ROOT")
    if not root:
        pytest.skip("exact OEWN source not present; authoritative CI supplies it")
    snapshot=load_oewn_2025(Path(root))
    words,_characters=_collect_surfaces(snapshot)
    admitted=set(words)
    fixture=origins.load_metric_origin_specs()
    missing={}
    for metric,spec in fixture["specs"].items():
        if spec["standing"]!="resolved":
            continue
        absent=[term for term in spec["construction_terms"] if term not in admitted]
        if absent:
            missing[metric]=absent
    assert missing=={}


def test_stack_fixture_matches_exact_edcm_producer():
    root=os.environ.get("EDCM_METRIC_ORIGIN_ROOT")
    if not root:
        pytest.skip("exact EDCM metric-origin producer not present; authoritative CI supplies it")
    module_path=Path(root)/"edcm"/"metric_origin_spec.py"
    spec=importlib.util.spec_from_file_location("_pinned_edcm_metric_origin_spec",module_path)
    assert spec is not None and spec.loader is not None
    module=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=module
    spec.loader.exec_module(module)
    fixture=origins.load_metric_origin_specs()
    assert fixture["producer_commit"]=="ed1b6e42b72c47f9383bd20b65e49a6c39a1a747"
    assert tuple(fixture["specs"])==tuple(module.METRIC_ORIGIN_SPECS)
    for metric,source_spec in module.METRIC_ORIGIN_SPECS.items():
        record=fixture["specs"][metric]
        assert record["surface_terms"]==list(source_spec.surface_terms)
        assert record["construction_terms"]==list(source_spec.construction_terms)
        assert record["semantic_definition"]==source_spec.semantic_definition
        assert record["standing"]==source_spec.standing
        assert record["measurement_alignment"]==source_spec.measurement_alignment
        assert record["unresolved"]==list(source_spec.unresolved)
