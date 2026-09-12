from __future__ import annotations

import json
from pathlib import Path

import pytest

from english_gonol.definition_affixiation_run import (
    GEOMETRY_REASON,
    GEOMETRY_STATE,
    GonolAffixiationRunError,
    run,
    verify_replay,
)
from english_gonol.language.source import (
    LexemeRecord,
    SenseRecord,
    SynsetRecord,
    WordnetSnapshot,
)


def _snapshot() -> WordnetSnapshot:
    return WordnetSnapshot(
        lexemes=(
            LexemeRecord(
                "kind",
                "n",
                ("kinder",),
                (SenseRecord("kind%1", "kind-n", ()),),
            ),
            LexemeRecord(
                "ice cream",
                "n",
                (),
                (SenseRecord("ice_cream%1", "ice-cream-n", ()),),
            ),
        ),
        synsets=(
            SynsetRecord(
                "kind-n",
                "n",
                ("kind",),
                ("having a friendly generous nature",),
                (),
            ),
            SynsetRecord(
                "ice-cream-n",
                "n",
                ("ice cream",),
                ("a frozen dessert made from cream",),
                (),
            ),
        ),
        source_tree_sha256="0" * 64,
        source_file_count=2,
    )


def _read_lines(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_full_fixture_run_persists_and_replays(tmp_path: Path) -> None:
    manifest = run(_snapshot(), out_dir=tmp_path, workers=1)
    records = _read_lines(tmp_path / "records.jsonl")

    words = [record for record in records if record["type"] == "word"]
    definitions = [record for record in records if record["type"] == "definition"]
    affixiations = [record for record in records if record["type"] == "affixiation"]
    lemmas = [record for record in records if record["type"] == "lemma"]

    # No sampling: every sense and every definition is processed.
    assert manifest["counts"]["definition_gonols"] == 2
    assert len(definitions) == 2
    assert len(affixiations) == 2
    # One multiword lemma composition for "ice cream".
    assert len(lemmas) == 1
    assert lemmas[0]["lemma"] == "ice cream"
    assert lemmas[0]["constituent_source_ids"] == ["oewn:surface:ice", "oewn:surface:cream"]

    # No hash placement: word identity is the exact surface source id.
    word_sources = {record["source_id"] for record in words}
    assert "oewn:surface:kind" in word_sources
    assert "oewn:surface:kinder" in word_sources
    assert "oewn:surface:a" in word_sources
    for record in words:
        assert record["atomic_id"] and len(record["atomic_id"]) == 64

    # Definitions preserve sense identity, order, and constituent identities.
    by_sense = {record["sense_id"]: record for record in definitions}
    assert by_sense["kind%1"]["constituent_source_ids"][0] == "oewn:surface:having"
    assert by_sense["ice_cream%1"]["word_source_id"] == "oewn:lemma-composition:ice cream:n"

    # Orthogonal affixiation boundary is exposed with no invented substitute.
    for record in affixiations:
        assert record["geometry_state"] == GEOMETRY_STATE
        assert "UCNS orthogonal-affixiation geometry is unresolved" in record["reason"]
    assert manifest["ucns"]["orthogonal_affixiation_geometry"] == GEOMETRY_STATE
    assert manifest["ucns"]["orthogonal_affixiation_reason"] == GEOMETRY_REASON

    # Per-word definition order is sequential and starts at 1.
    assert [record["order"] for record in definitions if record["word_source_id"].endswith("kind")] == [1]

    # Deterministic replay verifies; a tampered records file fails closed.
    assert verify_replay(tmp_path)["schema"] == manifest["schema"]
    (tmp_path / "records.jsonl").write_text("tampered\n", encoding="utf-8")
    with pytest.raises(GonolAffixiationRunError):
        verify_replay(tmp_path)


def test_run_requires_empty_output_directory(tmp_path: Path) -> None:
    (tmp_path / "stale.txt").write_text("x", encoding="utf-8")
    with pytest.raises(GonolAffixiationRunError):
        run(_snapshot(), out_dir=tmp_path, workers=1)


def test_workers_path_is_deterministic(tmp_path: Path) -> None:
    single = tmp_path / "single"
    multi = tmp_path / "multi"
    single_manifest = run(_snapshot(), out_dir=single, workers=1)
    multi_manifest = run(_snapshot(), out_dir=multi, workers=2)
    assert single_manifest["records_sha256"] == multi_manifest["records_sha256"]
    assert verify_replay(multi)["replay_digest"] == multi_manifest["replay_digest"]
