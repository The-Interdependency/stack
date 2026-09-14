# === CHECKS ===
# id: check_oewn_source_preserves_sense_order
#   proves: oewn_source_preserves_sense_order
#   call: self::test_loader_preserves_source_sense_order
#   requires: python3, pyyaml
#   timeout: 30
#   mutates: filesystem
#   cleanup: tempdir_teardown
# === END CHECKS ===

from __future__ import annotations

from pathlib import Path

import pytest

import english_gonol.language.source as source


def test_loader_preserves_source_sense_order(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pytest.importorskip("yaml")

    # The identifiers are intentionally reverse-lexicographic. Sorting them
    # would silently destroy the source ordinal evidence used by construction.
    (tmp_path / "frames.yaml").write_text("{}\n", encoding="utf-8")
    (tmp_path / "entries-test.yaml").write_text(
        """word:\n"
        "  n:\n"
        "    sense:\n"
        "      - id: z-sense\n"
        "        synset: s-z\n"
        "      - id: a-sense\n"
        "        synset: s-a\n"
        """,
        encoding="utf-8",
    )
    (tmp_path / "noun.test.yaml").write_text(
        """s-z:\n"
        "  partOfSpeech: n\n"
        "  members: [word]\n"
        "  definition: [first definition]\n"
        "s-a:\n"
        "  partOfSpeech: n\n"
        "  members: [word]\n"
        "  definition: [second definition]\n"
        """,
        encoding="utf-8",
    )

    monkeypatch.setattr(source, "OEWN_EXPECTED_WORD_COUNT", 1)
    monkeypatch.setattr(source, "OEWN_EXPECTED_SYNSET_COUNT", 2)

    snapshot = source.load_oewn_2025(tmp_path)
    assert len(snapshot.lexemes) == 1
    assert [sense.sense_id for sense in snapshot.lexemes[0].senses] == [
        "z-sense",
        "a-sense",
    ]
