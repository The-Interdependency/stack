# ratios: loc_comments=82:43 imports_exports=9:4 calls_definitions=35:4
"""Receipt integrity and audit mechanics; fixtures are not inclusion evidence."""

# === CHECKS ===
# id: check_full_views_complete_sealed_evidence
#   proves: full_views_scope_is_complete
#   call: self::test_complete_sealed_evidence
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
# id: check_full_views_count_meanings
#   proves: full_views_counts_and_controls
#   call: self::test_metrics_and_full_subsets
#   requires: python3
#   timeout: 30
#   mutates: none
#   cleanup: none
# id: check_full_views_reconstruction_boundaries
#   proves: full_views_exact_reconstruction
#   call: self::test_reconstruction_boundaries
#   requires: python3
#   timeout: 30
#   mutates: in-memory fixture only
#   cleanup: SQLite connection closed
# === END CHECKS ===

from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import sqlite3
import unittest

from english_gonol.full_view_audit import metrics, verify_sources
from english_gonol.view_replay import Corpus, VIEW_NAMES, canonical, freeze_views

WORKSPACE = Path(__file__).resolve().parents[1]
RESULTS = WORKSPACE / "experiments/hyperspace-views-full-v1"


def test_complete_sealed_evidence():
    native = json.loads((RESULTS / "native.json").read_text())
    replay = json.loads((RESULTS / "independent.json").read_text())
    evidence = native["evidence"]
    assert evidence == replay["evidence"]
    assert evidence["word_count"] == evidence["corpus_counts"]["words"] == 164864
    assert evidence["standing"] == "COMPLETE_SCOPE" and evidence["source_exhausted"] is True
    assert evidence["sampling"] is False and evidence["prefix"] is False
    assert native["execution"]["native_records_compared"] == 164864
    assert native["execution"]["engine"] == "native"
    assert replay["execution"]["engine"] == "independent"
    protocol_bytes = (WORKSPACE / "FULL_VIEW_AUDIT.json").read_bytes()
    protocol = json.loads(protocol_bytes)
    assert evidence["protocol_sha256"] == hashlib.sha256(protocol_bytes).hexdigest()
    assert evidence["work_graph_sha256"] == protocol["work_graph_sha256"]
    assert evidence["database_sha256"] == protocol["corpus"]["database_sha256"]
    assert evidence["corpus_counts"] == protocol["corpus"]["counts"]
    manifest = json.loads((WORKSPACE / "experiments/full-construct-v2/manifest.json").read_text())
    assert evidence["corpus_manifest_receipt"] == manifest["receipt_sha256"]
    verify_sources(WORKSPACE.parents[1], protocol["stack"]["files"])
    for name, digest in evidence["runner_sha256"].items():
        assert hashlib.sha256((WORKSPACE / "english_gonol" / name).read_bytes()).hexdigest() == digest
    for sealed in (evidence, evidence["legacy_report"]):
        body = {key: value for key, value in sealed.items() if key != "receipt_sha256"}
        assert hashlib.sha256(canonical(body)).hexdigest() == sealed["receipt_sha256"]


def test_metrics_and_full_subsets():
    values = ["a", "b", "a", "c", "b", "a"]
    observed = metrics(Counter(values))
    assert observed["collision_pairs"] == sum(a == b for a, b in combinations(values, 2)) == 4
    assert observed["repeated_records"] == 3
    assert observed["ambiguous_words"] == 5 and observed["singleton_words"] == 1
    assert observed["largest_bucket"] == 3 and observed["distinct_values"] == 3
    evidence = json.loads((RESULTS / "native.json").read_text())["evidence"]
    expected = {"+".join(map(str, subset)) for size in range(1, 5)
                for subset in combinations(range(1, 5), size)}
    assert set(evidence["subsets"]) == expected
    controls = evidence["renumbering_controls"]
    assert set(controls) == {"word_id_reverse", "word_id_affine_157", "glyph_id_reverse"}
    all_metrics = list(evidence["subsets"].values())
    for control in controls.values():
        assert set(control["views"]) == set(VIEW_NAMES)
        all_metrics.extend(control["views"].values())
        all_metrics.append(control["synthesis"])
        assert (evidence["subsets"]["1+2+3+4"]["collision_pairs"]
                - control["baseline_collision_pairs_split"]
                + control["new_collision_pairs_joined"] == control["synthesis"]["collision_pairs"])
    for row in all_metrics:
        assert row["word_count"] == 164864
        assert row["distinct_values"] + row["repeated_records"] == row["word_count"]
        assert row["singleton_words"] + row["ambiguous_words"] == row["word_count"]
        assert row["collision_pairs"] >= row["repeated_records"]
    for left, a in evidence["subsets"].items():
        for right, b in evidence["subsets"].items():
            if set(left.split("+")) <= set(right.split("+")):
                assert a["distinct_values"] <= b["distinct_values"]
                assert a["collision_pairs"] >= b["collision_pairs"]


def test_reconstruction_boundaries():
    db = sqlite3.connect(":memory:")
    try:
        db.executescript("""
            CREATE TABLE words (id INTEGER, surface TEXT);
            CREATE TABLE characters (id INTEGER, scalar TEXT, public_position INTEGER);
            CREATE TABLE word_characters (word_id INTEGER, ordinal INTEGER, character_id INTEGER);
            CREATE TABLE definitions (id INTEGER, origin_word_id INTEGER, ordinal INTEGER);
            CREATE TABLE definition_components (definition_id INTEGER, kind TEXT, word_id INTEGER);
            INSERT INTO words VALUES (1, 'ab'), (2, 'ba'), (3, 'a');
            INSERT INTO characters VALUES (1, 'a', 0), (2, 'b', 1);
            INSERT INTO word_characters VALUES (1,0,1), (1,1,2), (2,0,2), (2,1,1), (3,0,1);
            INSERT INTO definitions VALUES (1,1,0), (2,1,1), (3,3,0), (4,3,1);
            INSERT INTO definition_components VALUES (1,'word',2), (1,'word',2),
                (2,'word',3), (3,'word',2), (4,'word',2);
        """)
        corpus = Corpus(db)
        a, b, c = (corpus.views(i) for i in (1, 2, 3))
        assert a[0] == {"definition_count": 2, "pair_count": 1,
                        "orthogonal_pair_count": 1, "shared_sum": 0}
        assert b[0] is None and c[0]["shared_sum"] == 1
        assert freeze_views(a)[0] != freeze_views(b)[0]
        assert a[1] == b[1] == {"phase": "4/157", "frame": "positive-local-frame"}
        assert a[3] == {"residue": 4, "lift": 161}
        renamed = corpus.views(1, renamed_word_id=157)
        assert renamed[2] == {"deck": 1, "residue": 4, "lift": 161}
        assert renamed[:2] == a[:2] and renamed[3] == a[3]
    finally:
        db.close()


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(unittest.FunctionTestCase(check) for check in (
        test_complete_sealed_evidence, test_metrics_and_full_subsets,
        test_reconstruction_boundaries,
    ))
# ratios: loc_comments=82:43 imports_exports=9:4 calls_definitions=35:4
