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
# id: check_metric_origin_hmmm
#   proves: metric_origin_unresolved_fails_open_as_hmmm_not_closed
#   call: self::test_unresolved_origin_does_not_construct_components
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===

import json
import sqlite3
from pathlib import Path

from english_gonol.edcm_metric_origins import build_metric_origin_set

def _fixture(tmp_path: Path, metric="F", standing="resolved"):
    source = {
        "schema":"edcm.metric-origin-spec-fixture","version":"0.1.0",
        "producer_repository":"The-Interdependency/edcm","producer_commit":"a"*40,
        "specs":{metric:{
            "surface_terms":["Fixation"],"defining_statement":"is persistence",
            "formula_or_rule":"across states","standing":standing,
            "unresolved":[] if standing=="resolved" else ["collision"]}}
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
    words=["Fixation","is","persistence","across","states"]
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

def test_resolved_origin_uses_word_and_glyph_axes_in_order(tmp_path):
    _db(tmp_path)
    record=build_metric_origin_set(tmp_path,"F",construct_receipt="r"*64,
                                   fixture_path=_fixture(tmp_path))
    assert record.closed
    assert record.components[0].axis_origin=="O_W"
    assert any(x.axis_origin=="O_G" and x.surface==" " for x in record.components)
    assert record.producer_repository=="The-Interdependency/edcm"

def test_origin_record_contains_no_measurement_value(tmp_path):
    _db(tmp_path)
    record=build_metric_origin_set(tmp_path,"F",construct_receipt="r"*64,
                                   fixture_path=_fixture(tmp_path))
    keys=record.to_dict()
    assert "value" not in keys
    assert "measurement" not in keys
    assert "score" not in keys

def test_unresolved_origin_does_not_construct_components(tmp_path):
    record=build_metric_origin_set(tmp_path,"F",construct_receipt="r"*64,
                                   fixture_path=_fixture(tmp_path,standing="hmmm"))
    assert record.closed is False
    assert record.components==()
    assert record.unresolved==("collision",)
