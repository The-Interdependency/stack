# === CHECKS ===
# id: check_density_counts_constructed_occurrence_relations
#   proves: density_counts_constructed_occurrence_relations
#   call: self::test_counts_come_from_constructed_occurrence_relations
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_density_is_determinable_at_every_scale
#   proves: density_is_determinable_at_every_scale
#   call: self::test_density_is_determinable_at_every_scale
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_density_fractions_are_exact
#   proves: density_fractions_are_exact
#   call: self::test_fractions_are_exact_reduced
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_density_ratios_are_reduced
#   proves: density_ratios_are_reduced
#   call: self::test_ratios_are_reduced_between_letters
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_density_records_provenance_and_receipt
#   proves: density_records_provenance_and_receipt
#   call: self::test_provenance_and_receipt_are_recorded
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_density_counts_are_semantic_valuation_inputs
#   proves: density_counts_are_semantic_valuation_inputs
#   call: self::test_counts_are_semantic_valuation_inputs
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_density_stays_outside_the_construct
#   proves: density_stays_outside_the_construct
#   call: self::test_density_stays_outside_the_construct
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_density_fails_closed_on_wrong_construct_schema
#   proves: density_fails_closed_on_wrong_construct_schema
#   call: self::test_fails_closed_on_wrong_construct_schema
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

from hashlib import sha256
import json
import sqlite3
from pathlib import Path

import pytest

from english_gonol.density_run import (
    SCHEMA,
    VERSION,
    DensityError,
    build_density,
    run,
)

CONSTRUCT_SCHEMA = "english-gonol.full-construct"


def _manifest() -> dict[str, object]:
    return {
        "schema": CONSTRUCT_SCHEMA,
        "version": "2.0.0",
        "receipt_sha256": "receipt-123",
        "corpus": {
            "repository": "globalwordnet/english-wordnet",
            "commit": "dc343f2683279ecbb13fab4e2fd778d7b162d287",
            "source_tree_sha256": "tree-123",
            "tag": "2025-edition",
        },
        "ucns": {
            "commit": "4f863ad37096b7baab8f62820ad5cb937b62a3a7",
            "public_gonol_sha256": "gonol-123",
        },
    }


def _make_construct(tmp_path: Path) -> tuple[Path, Path]:
    db_path = tmp_path / "construct.db"
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(_manifest()), encoding="utf-8")

    connection = sqlite3.connect(db_path)
    connection.execute(
        "CREATE TABLE characters (id INTEGER PRIMARY KEY, scalar TEXT NOT NULL, public_position INTEGER)"
    )
    connection.execute(
        "CREATE TABLE word_characters (word_id INTEGER NOT NULL, ordinal INTEGER NOT NULL, character_id INTEGER NOT NULL, PRIMARY KEY(word_id, ordinal))"
    )
    connection.execute(
        "CREATE TABLE definition_components (definition_id INTEGER NOT NULL, ordinal INTEGER NOT NULL, kind TEXT NOT NULL, word_id INTEGER, character_id INTEGER, start_offset INTEGER NOT NULL, end_offset INTEGER NOT NULL, PRIMARY KEY(definition_id, ordinal))"
    )
    connection.execute(
        "CREATE TABLE semantic_evidence (id INTEGER PRIMARY KEY, definition_id INTEGER NOT NULL, source_ordinal INTEGER NOT NULL, channel TEXT NOT NULL, relation TEXT NOT NULL, target_word_id INTEGER NOT NULL, target_ref TEXT NOT NULL)"
    )
    connection.executemany(
        "INSERT INTO characters(id, scalar, public_position) VALUES(?, ?, ?)",
        [(1, "a", 0), (2, "b", 1), (3, " ", None)],
    )
    # word 10 = a,b,a ; word 11 = b,b
    connection.executemany(
        "INSERT INTO word_characters(word_id, ordinal, character_id) VALUES(?, ?, ?)",
        [(10, 1, 1), (10, 2, 2), (10, 3, 1), (11, 1, 2), (11, 2, 2)],
    )
    # definition 100 = word 10, whitespace scalar, word 11
    connection.executemany(
        "INSERT INTO definition_components(definition_id, ordinal, kind, word_id, character_id, start_offset, end_offset) VALUES(?, ?, ?, ?, ?, ?, ?)",
        [
            (100, 1, "word", 10, None, 0, 3),
            (100, 2, "whitespace", None, 3, 3, 4),
            (100, 3, "word", 11, None, 4, 6),
        ],
    )
    # semantic evidence points at target words 10 and 11
    connection.executemany(
        "INSERT INTO semantic_evidence(id, definition_id, source_ordinal, channel, relation, target_word_id, target_ref) VALUES(?, ?, ?, ?, ?, ?, ?)",
        [
            (1, 100, 0, "semantic", "example:rel", 10, "ref-10"),
            (2, 100, 0, "semantic", "example:rel", 11, "ref-11"),
        ],
    )
    connection.commit()
    connection.close()
    return db_path, manifest_path


def _counts(result, scale: str) -> dict[str, int]:
    return {
        letter["scalar"]: letter["count"]
        for letter in result.scales[scale]["letters"]
    }


def test_counts_come_from_constructed_occurrence_relations(tmp_path: Path) -> None:
    db_path, manifest_path = _make_construct(tmp_path)
    result = build_density(db_path, manifest_path)

    word_counts = _counts(result, "word")
    assert word_counts["a"] == 2
    assert word_counts["b"] == 3
    assert word_counts[" "] == 0
    assert result.scales["word"]["total"] == 5


def test_density_is_determinable_at_every_scale(tmp_path: Path) -> None:
    db_path, manifest_path = _make_construct(tmp_path)
    result = build_density(db_path, manifest_path)

    assert set(result.scales) == {"character", "word", "definition", "semantic"}
    assert result.scales["character"]["total"] == 3
    assert _counts(result, "character") == {"a": 1, "b": 1, " ": 1}
    assert result.scales["word"]["total"] == 5
    assert result.scales["definition"]["total"] == 6
    assert _counts(result, "definition") == {"a": 2, "b": 3, " ": 1}
    assert result.scales["semantic"]["total"] == 5
    assert _counts(result, "semantic") == {"a": 2, "b": 3, " ": 0}


def test_fractions_are_exact_reduced(tmp_path: Path) -> None:
    db_path, manifest_path = _make_construct(tmp_path)
    result = build_density(db_path, manifest_path)

    fractions = {
        letter["scalar"]: letter["frequency_fraction"]
        for letter in result.scales["word"]["letters"]
    }
    assert fractions["a"] == "2/5"
    assert fractions["b"] == "3/5"
    assert fractions[" "] == "0/1"


def test_ratios_are_reduced_between_letters(tmp_path: Path) -> None:
    db_path, manifest_path = _make_construct(tmp_path)
    result = build_density(db_path, manifest_path)

    ratios = {
        (ratio["a"], ratio["b"]): ratio["reduced_ratio"]
        for ratio in result.scales["word"]["ratios"]
    }
    assert ratios[("a", "b")] == "2/3"
    assert ratios[("a", " ")] == "2/0"
    assert ratios[("b", " ")] == "3/0"


def test_provenance_and_receipt_are_recorded(tmp_path: Path) -> None:
    db_path, manifest_path = _make_construct(tmp_path)
    result = build_density(db_path, manifest_path)

    assert result.schema == SCHEMA
    assert result.version == VERSION
    assert result.corpus["commit"] == "dc343f2683279ecbb13fab4e2fd778d7b162d287"
    assert result.corpus["source_tree_sha256"] == "tree-123"
    assert result.builder["construct_schema"] == CONSTRUCT_SCHEMA
    assert result.builder["construct_receipt_sha256"] == "receipt-123"
    assert result.builder["construct_db_sha256"] == sha256(db_path.read_bytes()).hexdigest()
    assert result.builder["ucns_commit"] == "4f863ad37096b7baab8f62820ad5cb937b62a3a7"
    assert len(result.receipt_sha256) == 64

    again = build_density(db_path, manifest_path)
    assert again.receipt_sha256 == result.receipt_sha256
    assert again.receipt_bytes() == result.receipt_bytes()


def test_counts_are_semantic_valuation_inputs(tmp_path: Path) -> None:
    db_path, manifest_path = _make_construct(tmp_path)
    result = build_density(db_path, manifest_path)

    valuation = result.semantic_valuation
    assert valuation["determinable_at_scales"] == ["character", "word", "definition", "semantic"]
    assert valuation["scale_totals"] == {"character": 3, "word": 5, "definition": 6, "semantic": 5}
    assert valuation["valuation_weight"] is None
    assert "geometrically" in valuation["hmmm"]


def test_density_stays_outside_the_construct(tmp_path: Path) -> None:
    db_path, manifest_path = _make_construct(tmp_path)
    before = db_path.read_bytes()
    out_dir = tmp_path / "density"

    result = run(db_path, manifest_path, out_dir)

    assert db_path.read_bytes() == before
    density_json = json.loads((out_dir / "density.json").read_text(encoding="utf-8"))
    assert density_json["schema"] == SCHEMA
    assert density_json["receipt_sha256"] == result.receipt_sha256
    markdown = (out_dir / "density.md").read_text(encoding="utf-8")
    assert "outside the construct" in markdown
    assert "Semantic valuation" in markdown


def test_fails_closed_on_wrong_construct_schema(tmp_path: Path) -> None:
    db_path, manifest_path = _make_construct(tmp_path)
    bad_manifest = _manifest()
    bad_manifest["schema"] = "english-gonol.something-else"
    bad_path = tmp_path / "bad-manifest.json"
    bad_path.write_text(json.dumps(bad_manifest), encoding="utf-8")

    with pytest.raises(DensityError):
        build_density(db_path, bad_path)
