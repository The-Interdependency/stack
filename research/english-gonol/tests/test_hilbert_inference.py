# === CHECKS ===
# id: check_hilbert_axes_are_uchc_axes_not_cartesian
#   proves: hilbert_axes_are_uchc_axes_not_cartesian
#   call: self::test_origin_local_basis_uses_declared_axes
#   requires: python3
#   timeout: 30
#   mutates: tmp sqlite only
#   cleanup: pytest tmp_path
#
# id: check_hilbert_axis_identity_is_construct_bound
#   proves: hilbert_axis_identity_is_construct_bound
#   call: self::test_axis_identity_is_construct_bound
#   requires: python3
#   timeout: 30
#   mutates: tmp sqlite only
#   cleanup: pytest tmp_path
#
# id: check_hilbert_origin_local_inner_product
#   proves: hilbert_origin_local_inner_product
#   call: self::test_origin_local_inner_product_and_fail_closed_boundaries
#   requires: python3
#   timeout: 30
#   mutates: tmp sqlite only
#   cleanup: pytest tmp_path
#
# id: check_hilbert_word_promotion_preserves_order_and_multiplicity
#   proves: hilbert_word_promotion_preserves_order_and_multiplicity
#   call: self::test_word_promotion_preserves_order_and_multiplicity
#   requires: python3
#   timeout: 30
#   mutates: tmp sqlite only
#   cleanup: pytest tmp_path
#
# id: check_hilbert_dimension_queries_do_not_reconstruct_members
#   proves: hilbert_dimension_queries_do_not_reconstruct_members
#   call: self::test_dimension_queries_are_direct_counts
#   requires: python3
#   timeout: 30
#   mutates: tmp sqlite only
#   cleanup: pytest tmp_path
#
# id: check_hilbert_finite_origin_spaces_are_complete
#   proves: hilbert_finite_origin_spaces_are_complete
#   call: self::test_finite_spaces_require_explicit_field_and_are_complete
#   requires: python3
#   timeout: 30
#   mutates: tmp sqlite only
#   cleanup: pytest tmp_path
# === END CHECKS ===

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from english_gonol.hilbert_inference import (
    ConstructRef,
    HilbertInferenceError,
    basis_vector,
    definition_promotion,
    definition_space,
    glyph_axis,
    glyph_space,
    word_axis,
    word_promotion,
    word_space,
)
from english_gonol.hyperspace_construct import (
    glyph_inventory,
    promote_word,
)


REF_A = ConstructRef("0" * 64, "1" * 64)
REF_B = ConstructRef("0" * 64, "2" * 64)


def _fixture_db(tmp_path: Path) -> sqlite3.Connection:
    db = sqlite3.connect(tmp_path / "construct.db")
    db.executescript(
        """
        CREATE TABLE characters (
            id INTEGER PRIMARY KEY,
            scalar TEXT NOT NULL UNIQUE,
            public_position INTEGER
        );
        CREATE TABLE words (
            id INTEGER PRIMARY KEY,
            surface TEXT NOT NULL UNIQUE
        );
        CREATE TABLE word_characters (
            word_id INTEGER NOT NULL REFERENCES words(id),
            ordinal INTEGER NOT NULL,
            character_id INTEGER NOT NULL REFERENCES characters(id),
            PRIMARY KEY (word_id, ordinal)
        ) WITHOUT ROWID;
        CREATE TABLE definitions (
            id INTEGER PRIMARY KEY,
            origin_word_id INTEGER NOT NULL REFERENCES words(id),
            part_of_speech TEXT NOT NULL,
            ordinal INTEGER NOT NULL,
            sense_id TEXT NOT NULL,
            synset_id TEXT NOT NULL,
            definition_index INTEGER NOT NULL,
            text TEXT NOT NULL,
            previous_definition_id INTEGER REFERENCES definitions(id),
            UNIQUE (origin_word_id, ordinal)
        );
        CREATE TABLE definition_components (
            id INTEGER PRIMARY KEY,
            definition_id INTEGER NOT NULL REFERENCES definitions(id),
            ordinal INTEGER NOT NULL,
            kind TEXT NOT NULL,
            word_id INTEGER REFERENCES words(id),
            character_id INTEGER REFERENCES characters(id),
            start_offset INTEGER NOT NULL,
            end_offset INTEGER NOT NULL
        );
        """
    )
    db.executemany(
        "INSERT INTO characters VALUES (?, ?, ?)",
        [(1, "a", 0), (2, "b", 1), (3, " ", 2)],
    )
    db.executemany(
        "INSERT INTO words VALUES (?, ?)",
        [(1, "ab"), (2, "a"), (3, "aa")],
    )
    db.executemany(
        "INSERT INTO word_characters VALUES (?, ?, ?)",
        [
            (1, 0, 1),
            (1, 1, 2),
            (2, 0, 1),
            (3, 0, 1),
            (3, 1, 1),
        ],
    )
    db.execute(
        "INSERT INTO definitions VALUES "
        "(1, 1, 'noun', 1, 'sense', 'synset', 1, 'a a', NULL)"
    )
    db.executemany(
        "INSERT INTO definition_components "
        "(id, definition_id, ordinal, kind, word_id, character_id, start_offset, end_offset) "
        "VALUES (?, 1, ?, ?, ?, ?, ?, ?)",
        [
            (1, 0, "word", 2, None, 0, 1),
            (2, 1, "character", None, 3, 1, 2),
            (3, 2, "word", 2, None, 2, 3),
        ],
    )
    db.commit()
    return db


def test_origin_local_basis_uses_declared_axes(tmp_path: Path) -> None:
    db = _fixture_db(tmp_path)
    inventory = glyph_inventory(db)

    a_axis = glyph_axis(inventory["a"], REF_A)
    b_axis = glyph_axis(inventory["b"], REF_A)

    assert a_axis.identity == "a"
    assert a_axis.axis_index == inventory["a"].axis_index
    assert a_axis.space_id == "O_G"

    a = basis_vector(a_axis, scalar_field="R")
    b = basis_vector(b_axis, scalar_field="R")
    assert a.inner_product(a) == 1
    assert a.inner_product(b) == 0
    assert a.scale(2).add(b.scale(3)).norm_squared() == 13
    db.close()


def test_axis_identity_is_construct_bound(tmp_path: Path) -> None:
    db = _fixture_db(tmp_path)
    inventory = glyph_inventory(db)

    same_glyph_a = glyph_axis(inventory["a"], REF_A)
    same_glyph_b = glyph_axis(inventory["a"], REF_B)
    assert same_glyph_a != same_glyph_b

    vector_a = basis_vector(same_glyph_a, scalar_field="R")
    vector_b = basis_vector(same_glyph_b, scalar_field="R")
    with pytest.raises(HilbertInferenceError, match="cross-construct"):
        vector_a.inner_product(vector_b)
    db.close()


def test_origin_local_inner_product_and_fail_closed_boundaries(
    tmp_path: Path,
) -> None:
    db = _fixture_db(tmp_path)
    inventory = glyph_inventory(db)
    glyph = basis_vector(
        glyph_axis(inventory["a"], REF_A),
        scalar_field="C",
    )
    word, _axis_index = promote_word(db, 2)
    word_vector = basis_vector(
        word_axis(word, REF_A),
        scalar_field="C",
    )

    assert glyph.scale(1j).norm_squared() == 1
    with pytest.raises(HilbertInferenceError, match="cross-origin"):
        glyph.inner_product(word_vector)
    with pytest.raises(HilbertInferenceError, match="scalar fields"):
        glyph.inner_product(
            basis_vector(glyph_axis(inventory["a"], REF_A), scalar_field="R")
        )
    db.close()


def test_word_promotion_preserves_order_and_multiplicity(tmp_path: Path) -> None:
    db = _fixture_db(tmp_path)
    inventory = glyph_inventory(db)

    ab = word_promotion(
        db,
        inventory,
        1,
        REF_A,
        scalar_field="R",
    )
    assert [factor.identity for factor in ab.source.factors] == ["a", "b"]
    assert ab.target.identity_kind == "word"
    assert ab.target.identity == "1"

    aa = word_promotion(
        db,
        inventory,
        3,
        REF_A,
        scalar_field="R",
    )
    assert [factor.identity for factor in aa.source.factors] == ["a", "a"]
    assert len(aa.source.factors) == 2
    assert aa.target.identity == "3"

    definition = definition_promotion(
        db,
        inventory,
        1,
        REF_A,
        scalar_field="R",
    )
    assert [
        (factor.identity_kind, factor.identity)
        for factor in definition.source.factors
    ] == [
        ("word", "2"),
        ("glyph", " "),
        ("word", "2"),
    ]
    assert definition.target.space_id == "O_D:1"
    db.close()


def test_dimension_queries_are_direct_counts(tmp_path: Path) -> None:
    db = _fixture_db(tmp_path)
    inventory = glyph_inventory(db)
    queries: list[str] = []
    db.set_trace_callback(queries.append)

    words = word_space(db, REF_A, scalar_field="R")
    definitions = definition_space(db, REF_A, 1, scalar_field="R")
    glyphs = glyph_space(inventory, REF_A, scalar_field="R")

    db.set_trace_callback(None)
    normalized = [" ".join(query.upper().split()) for query in queries]
    assert words.dimension == 3
    assert definitions.dimension == 1
    assert glyphs.dimension == 3
    assert normalized.count("SELECT COUNT(*) FROM WORDS") == 1
    assert normalized.count(
        "SELECT COUNT(*) FROM DEFINITIONS WHERE ORIGIN_WORD_ID = 1"
    ) == 1
    assert not any("WORD_CHARACTERS" in query for query in normalized)
    db.close()


def test_finite_spaces_require_explicit_field_and_are_complete(
    tmp_path: Path,
) -> None:
    db = _fixture_db(tmp_path)
    inventory = glyph_inventory(db)

    real_space = glyph_space(inventory, REF_A, scalar_field="R")
    complex_space = word_space(db, REF_A, scalar_field="C")
    assert real_space.complete is True
    assert complex_space.complete is True
    assert real_space.scalar_field == "R"
    assert complex_space.scalar_field == "C"

    with pytest.raises(HilbertInferenceError, match="scalar_field"):
        glyph_space(inventory, REF_A, scalar_field="Q")
    with pytest.raises(HilbertInferenceError, match="imaginary"):
        basis_vector(
            glyph_axis(inventory["a"], REF_A),
            scalar_field="R",
        ).scale(1j)
    db.close()
