"""Full-corpus English gonol construction evidence builder.

This builder implements only the construction that is already specified:

* one exact character identity for each admitted Unicode scalar;
* one exact word identity for each admitted surface;
* words reference those character identities in exact order and multiplicity;
* every definition is anchored to the one shared origin word;
* definition ordinal evidence and OEWN semantic evidence remain distinct;
* the ordered words of the definition are retained as sentence-context evidence;
* resolution is by preponderance relative to that sentence context;
* no weight, direction, distance, radius, tangency, motion, closure graph,
  sentence singleton, sense singleton, synset singleton, or n-gram singleton
  is invented.

The corpus is evidence. Sense and synset identifiers are provenance locators,
not gonols. The exact UCNS law that turns the admitted evidence into spatial
displacement is still unresolved; that boundary is recorded as ``hmmm``.

The materialized artifact is one normalized SQLite database plus a small
manifest. It is never duplicated into a giant JSON serialization.
"""

# === MODULE_BUILD ===
# id: english_gonol_full_construct
#   module_name: full_construct_run
#   module_kind: builder
#   summary: full-corpus normalized English gonol construction evidence with one character identity, one word identity, word-origin definitions, ordinal and semantic evidence, and no invented geometry
#   owner: Erin Spencer
#   public_surface: SCHEMA, VERSION, UCNS_PUBLIC_GONOL_COMMIT, FullConstructError, build_construct, run, verify_replay
#   internal_surface: exact source admission, normalized sqlite construction, deterministic logical receipt, verified Public Gonol lookup
#   auth_boundary: OEWN supplies English evidence; UCNS supplies only established Public Gonol carrier positions; unresolved geometry stays hmmm
#   storage_boundary: one caller-selected construct.db plus manifest.json
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_full_construct_run
#   rollout: stack-local research construction; no geometry canon or semantic measurement promotion
#   rollback: delete this builder and its generated output directory
#   requires: edcm_language_oewn_source, ucns_public_gonol_geometry
#   since: 2026-09-14
#   unresolved: exact UCNS law mapping ordinal + semantic + sentence-context evidence to geometric displacement
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: full_construct_has_one_character_identity
#   given: the admitted corpus characters
#   then: each exact Unicode scalar occurs once in characters and every word reuses its character id
#   class: correctness
#   since: 2026-09-14
#
# id: full_construct_has_one_word_identity
#   given: the admitted corpus word surfaces
#   then: each exact surface occurs once in words and every definition reuses its word id
#   class: correctness
#   since: 2026-09-14
#
# id: full_construct_definitions_share_word_origin
#   given: all definitions for one word
#   then: every definition references that single word id as origin and carries source ordinal separately
#   class: correctness
#   since: 2026-09-14
#
# id: full_construct_keeps_probability_evidence_distinct
#   given: an admitted definition
#   then: ordinal evidence, semantic relations, and ordered sentence context are preserved without synthesized weights
#   class: correctness
#   since: 2026-09-14
#
# id: full_construct_does_not_promote_evidence_to_gonols
#   given: OEWN senses, synsets, definitions, and occurrences
#   then: no sentence, sense, synset, ngram, closure, attention, tangency, or relation-circle object is created
#   class: safety
#   since: 2026-09-14
#
# id: full_construct_never_invents_geometry
#   given: no established UCNS displacement law for this English evidence
#   then: weights, vectors, coordinates, centers, radii, tangencies, and motion are absent and geometry_state is hmmm
#   class: safety
#   since: 2026-09-14
#
# id: full_construct_replays_logically
#   given: the completed construct.db and manifest
#   then: a deterministic canonical walk of normalized rows reproduces the receipt sha256
#   class: evidence
#   since: 2026-09-14
# === END CONTRACTS ===

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import sqlite3
import subprocess
from pathlib import Path
from types import ModuleType
import unicodedata
from typing import Any, Callable, Iterator

from english_gonol.language.source import (
    OEWN_COMMIT,
    OEWN_REPOSITORY,
    OEWN_TAG,
    WordnetSnapshot,
    load_oewn_2025,
)

SCHEMA = "english-gonol.full-construct"
VERSION = "1.0.0"

UCNS_PUBLIC_GONOL_COMMIT = "4f863ad37096b7baab8f62820ad5cb937b62a3a7"
UCNS_PUBLIC_GONOL_MODULE_SHA256 = (
    "2da287ce9691b494fc921d14684a3bf7e0633f3a579ea040e3b6ddbaf0d92f27"
)
PUBLIC_GONOL_SHA256 = "55d10c84529a4d7bc7714786357e977b68d9df2ac3f73d20e229580b552c2ef5"

GEOMETRY_STATE = "hmmm"
HMMM = (
    "the exact UCNS law mapping ordinal + semantic + sentence-context evidence "
    "to geometric displacement is unresolved; no weight, direction, distance, "
    "radius, tangency, motion, or substitute geometry is synthesized"
)
RESOLUTION_RULE = "preponderance relative to the rest of the sentence in which the word appears"
WORD_ADMISSION_RULE = (
    "exact maximal Unicode letter/number spans, with apostrophe or hyphen "
    "connectors admitted only when flanked by letter/number characters; no normalization"
)

_FORBIDDEN_TABLES = frozenset(
    {
        "sentences",
        "senses",
        "synsets",
        "ngrams",
        "sequences",
        "closure_nodes",
        "closure_edges",
        "closure_cycles",
        "occurrences",
        "relation_circles",
        "tangencies",
        "attention_frames",
        "mobius_frames",
    }
)

_SCHEMA_SQL = """
PRAGMA foreign_keys=ON;
PRAGMA journal_mode=DELETE;
PRAGMA synchronous=FULL;
PRAGMA temp_store=FILE;

CREATE TABLE meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
) WITHOUT ROWID;

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
    UNIQUE (origin_word_id, part_of_speech, ordinal)
);

CREATE TABLE definition_words (
    definition_id INTEGER NOT NULL REFERENCES definitions(id),
    ordinal INTEGER NOT NULL,
    word_id INTEGER NOT NULL REFERENCES words(id),
    start_offset INTEGER NOT NULL,
    end_offset INTEGER NOT NULL,
    PRIMARY KEY (definition_id, ordinal)
) WITHOUT ROWID;

CREATE TABLE semantic_evidence (
    definition_id INTEGER NOT NULL REFERENCES definitions(id),
    source_ordinal INTEGER NOT NULL,
    channel TEXT NOT NULL,
    relation TEXT NOT NULL,
    target_word_id INTEGER NOT NULL REFERENCES words(id),
    target_ref TEXT NOT NULL,
    PRIMARY KEY (definition_id, source_ordinal, target_word_id)
) WITHOUT ROWID;

CREATE TABLE unresolved_semantic_evidence (
    definition_id INTEGER NOT NULL REFERENCES definitions(id),
    source_ordinal INTEGER NOT NULL,
    channel TEXT NOT NULL,
    relation TEXT NOT NULL,
    target_ref TEXT NOT NULL,
    PRIMARY KEY (definition_id, source_ordinal, target_ref)
) WITHOUT ROWID;

CREATE INDEX idx_definitions_origin ON definitions(origin_word_id, part_of_speech, ordinal);
CREATE INDEX idx_definition_words_word ON definition_words(word_id, definition_id);
CREATE INDEX idx_semantic_target ON semantic_evidence(target_word_id, definition_id);
"""


class FullConstructError(RuntimeError):
    pass


def _git(repo: Path, *arguments: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(repo), *arguments],
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()
    except (subprocess.CalledProcessError, OSError) as exc:
        raise FullConstructError(f"UCNS checkout verification failed: {exc}") from exc


def _load_verified_public_gonol(ucns_source_root: str | Path) -> ModuleType:
    root = Path(ucns_source_root).resolve()
    if _git(root, "rev-parse", "HEAD") != UCNS_PUBLIC_GONOL_COMMIT:
        raise FullConstructError(
            "UCNS checkout HEAD does not match the pinned Public Gonol authority "
            f"{UCNS_PUBLIC_GONOL_COMMIT}"
        )
    path = root / "src" / "ucns" / "public_gonol.py"
    if not path.is_file():
        raise FullConstructError("UCNS public_gonol.py is missing")
    working = path.read_bytes()
    try:
        committed = subprocess.check_output(
            ["git", "-C", str(root), "show", "HEAD:src/ucns/public_gonol.py"],
            stderr=subprocess.STDOUT,
        )
    except (subprocess.CalledProcessError, OSError) as exc:
        raise FullConstructError("cannot read committed UCNS Public Gonol bytes") from exc
    if working != committed:
        raise FullConstructError("UCNS public_gonol.py has uncommitted changes")
    if sha256(committed).hexdigest() != UCNS_PUBLIC_GONOL_MODULE_SHA256:
        raise FullConstructError("UCNS public_gonol.py module digest mismatch")

    module = ModuleType("_english_gonol_verified_public_gonol")
    module.__file__ = str(path)
    exec(compile(committed, str(path), "exec"), module.__dict__)
    if module.PUBLIC_GONOL_SHA256 != PUBLIC_GONOL_SHA256:
        raise FullConstructError("Public Gonol arrangement digest mismatch")
    return module


def _is_word_core(character: str) -> bool:
    category = unicodedata.category(character)
    return category.startswith("L") or category.startswith("N")


_CONNECTORS = frozenset({"'", "’", "-", "‐", "‑"})


def _word_spans(text: str) -> Iterator[tuple[int, int, str]]:
    """Yield exact orthographic word evidence without normalizing source text."""

    index = 0
    length = len(text)
    while index < length:
        if not _is_word_core(text[index]):
            index += 1
            continue
        start = index
        index += 1
        while index < length:
            character = text[index]
            if _is_word_core(character):
                index += 1
                continue
            if (
                character in _CONNECTORS
                and index + 1 < length
                and _is_word_core(text[index - 1])
                and _is_word_core(text[index + 1])
            ):
                index += 1
                continue
            break
        yield start, index, text[start:index]


def _collect_surfaces(snapshot: WordnetSnapshot) -> tuple[tuple[str, ...], tuple[str, ...]]:
    words: set[str] = set()
    characters: set[str] = set()

    for lexeme in snapshot.lexemes:
        words.add(lexeme.lemma)
        words.update(lexeme.forms)

    for synset in snapshot.synsets:
        words.update(synset.members)
        for definition in synset.definitions:
            characters.update(definition)
            for _start, _end, surface in _word_spans(definition):
                words.add(surface)

    for surface in words:
        characters.update(surface)

    return tuple(sorted(words)), tuple(sorted(characters, key=ord))


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _set_meta(db: sqlite3.Connection, key: str, value: Any) -> None:
    encoded = value if isinstance(value, str) else json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    db.execute("INSERT INTO meta(key, value) VALUES(?, ?)", (key, encoded))


def _insert_identities(
    db: sqlite3.Connection,
    snapshot: WordnetSnapshot,
    public_position: Callable[[str], int | None],
) -> tuple[dict[str, int], dict[str, int]]:
    words, characters = _collect_surfaces(snapshot)

    character_ids: dict[str, int] = {}
    for identifier, scalar in enumerate(characters, start=1):
        position = public_position(scalar)
        db.execute(
            "INSERT INTO characters(id, scalar, public_position) VALUES(?, ?, ?)",
            (identifier, scalar, position),
        )
        character_ids[scalar] = identifier

    word_ids: dict[str, int] = {}
    for identifier, surface in enumerate(words, start=1):
        db.execute(
            "INSERT INTO words(id, surface) VALUES(?, ?)",
            (identifier, surface),
        )
        word_ids[surface] = identifier
        db.executemany(
            "INSERT INTO word_characters(word_id, ordinal, character_id) VALUES(?, ?, ?)",
            (
                (identifier, ordinal, character_ids[scalar])
                for ordinal, scalar in enumerate(surface, start=1)
            ),
        )
    return character_ids, word_ids


def _semantic_target_word_ids(
    target_ref: str,
    *,
    sense_to_word: dict[str, int],
    synset_to_words: dict[str, tuple[int, ...]],
    surface_to_word: dict[str, int],
) -> tuple[int, ...]:
    if target_ref in sense_to_word:
        return (sense_to_word[target_ref],)
    if target_ref in synset_to_words:
        return synset_to_words[target_ref]
    if target_ref in surface_to_word:
        return (surface_to_word[target_ref],)
    return ()


def _insert_definitions(
    db: sqlite3.Connection,
    snapshot: WordnetSnapshot,
    word_ids: dict[str, int],
) -> None:
    synset_map = snapshot.synset_map()

    sense_to_word: dict[str, int] = {}
    for lexeme in snapshot.lexemes:
        origin_id = word_ids[lexeme.lemma]
        for sense in lexeme.senses:
            sense_to_word[sense.sense_id] = origin_id

    synset_to_words: dict[str, tuple[int, ...]] = {}
    for synset in snapshot.synsets:
        synset_to_words[synset.synset_id] = tuple(
            sorted(
                {
                    word_ids[member]
                    for member in synset.members
                    if member in word_ids
                }
            )
        )

    next_definition_id = 1
    grouped: dict[str, list[Any]] = {}
    for lexeme in snapshot.lexemes:
        grouped.setdefault(lexeme.lemma, []).append(lexeme)

    for lemma in sorted(grouped):
        origin_word_id = word_ids[lemma]
        for lexeme in sorted(grouped[lemma], key=lambda record: record.part_of_speech):
            definition_ordinal = 0
            for sense in lexeme.senses:
                synset = synset_map.get(sense.synset_id)
                if synset is None:
                    raise FullConstructError(
                        f"sense {sense.sense_id!r} references missing synset {sense.synset_id!r}"
                    )
                for definition_index, text in enumerate(synset.definitions):
                    definition_ordinal += 1
                    definition_id = next_definition_id
                    next_definition_id += 1
                    db.execute(
                        "INSERT INTO definitions("
                        "id, origin_word_id, part_of_speech, ordinal, sense_id, "
                        "synset_id, definition_index, text"
                        ") VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            definition_id,
                            origin_word_id,
                            lexeme.part_of_speech,
                            definition_ordinal,
                            sense.sense_id,
                            sense.synset_id,
                            definition_index,
                            text,
                        ),
                    )

                    for word_ordinal, (start, end, surface) in enumerate(
                        _word_spans(text), start=1
                    ):
                        db.execute(
                            "INSERT INTO definition_words("
                            "definition_id, ordinal, word_id, start_offset, end_offset"
                            ") VALUES(?, ?, ?, ?, ?)",
                            (
                                definition_id,
                                word_ordinal,
                                word_ids[surface],
                                start,
                                end,
                            ),
                        )

                    source_ordinal = 0

                    def add_evidence(
                        channel: str,
                        relation: str,
                        target_ref: str,
                    ) -> None:
                        nonlocal source_ordinal
                        source_ordinal += 1
                        targets = _semantic_target_word_ids(
                            target_ref,
                            sense_to_word=sense_to_word,
                            synset_to_words=synset_to_words,
                            surface_to_word=word_ids,
                        )
                        if not targets:
                            db.execute(
                                "INSERT INTO unresolved_semantic_evidence("
                                "definition_id, source_ordinal, channel, relation, target_ref"
                                ") VALUES(?, ?, ?, ?, ?)",
                                (
                                    definition_id,
                                    source_ordinal,
                                    channel,
                                    relation,
                                    target_ref,
                                ),
                            )
                            return
                        for target_word_id in targets:
                            db.execute(
                                "INSERT INTO semantic_evidence("
                                "definition_id, source_ordinal, channel, relation, "
                                "target_word_id, target_ref"
                                ") VALUES(?, ?, ?, ?, ?, ?)",
                                (
                                    definition_id,
                                    source_ordinal,
                                    channel,
                                    relation,
                                    target_word_id,
                                    target_ref,
                                ),
                            )

                    for relation, targets in sense.relations:
                        for target_ref in targets:
                            add_evidence("sense", relation, target_ref)

                    for relation, targets in synset.relations:
                        for target_ref in targets:
                            add_evidence("synset", relation, target_ref)

                    for member in synset.members:
                        if member == lemma:
                            continue
                        add_evidence("synset-membership", "co-member", member)


_TABLE_QUERIES: tuple[tuple[str, str], ...] = (
    ("meta", "SELECT key, value FROM meta ORDER BY key"),
    (
        "characters",
        "SELECT id, scalar, public_position FROM characters ORDER BY id",
    ),
    ("words", "SELECT id, surface FROM words ORDER BY id"),
    (
        "word_characters",
        "SELECT word_id, ordinal, character_id FROM word_characters "
        "ORDER BY word_id, ordinal",
    ),
    (
        "definitions",
        "SELECT id, origin_word_id, part_of_speech, ordinal, sense_id, "
        "synset_id, definition_index, text FROM definitions ORDER BY id",
    ),
    (
        "definition_words",
        "SELECT definition_id, ordinal, word_id, start_offset, end_offset "
        "FROM definition_words ORDER BY definition_id, ordinal",
    ),
    (
        "semantic_evidence",
        "SELECT definition_id, source_ordinal, channel, relation, target_word_id, target_ref "
        "FROM semantic_evidence "
        "ORDER BY definition_id, source_ordinal, target_word_id",
    ),
    (
        "unresolved_semantic_evidence",
        "SELECT definition_id, source_ordinal, channel, relation, target_ref "
        "FROM unresolved_semantic_evidence "
        "ORDER BY definition_id, source_ordinal, target_ref",
    ),
)


def _logical_receipt(db: sqlite3.Connection) -> str:
    digest = sha256()
    for table, query in _TABLE_QUERIES:
        digest.update(b"table:")
        digest.update(table.encode("utf-8"))
        digest.update(b"\0")
        for row in db.execute(query):
            digest.update(_canonical_bytes(list(row)))
            digest.update(b"\n")
    return digest.hexdigest()


def _assert_schema_boundary(db: sqlite3.Connection) -> None:
    observed = {
        row[0]
        for row in db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
    }
    forbidden = observed & _FORBIDDEN_TABLES
    if forbidden:
        raise FullConstructError(
            f"forbidden evidence-as-gonol tables exist: {sorted(forbidden)}"
        )
    expected = {table for table, _query in _TABLE_QUERIES}
    if observed != expected:
        raise FullConstructError(
            f"construct table set drift: expected {sorted(expected)}, got {sorted(observed)}"
        )


def build_construct(
    snapshot: WordnetSnapshot,
    *,
    db_path: str | Path,
    public_position: Callable[[str], int | None],
    public_gonol_sha256: str = PUBLIC_GONOL_SHA256,
    overwrite: bool = False,
) -> dict[str, Any]:
    """Build the normalized construction without inventing the missing geometry."""

    target = Path(db_path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if not overwrite:
            raise FullConstructError(f"construct database already exists: {target}")
        target.unlink()

    db = sqlite3.connect(str(target))
    try:
        db.executescript(_SCHEMA_SQL)
        _set_meta(db, "schema", SCHEMA)
        _set_meta(db, "version", VERSION)
        _set_meta(db, "corpus_repository", OEWN_REPOSITORY)
        _set_meta(db, "corpus_tag", OEWN_TAG)
        _set_meta(db, "corpus_commit", OEWN_COMMIT)
        _set_meta(db, "corpus_source_tree_sha256", snapshot.source_tree_sha256)
        _set_meta(db, "ucns_public_gonol_sha256", public_gonol_sha256)
        _set_meta(db, "geometry_state", GEOMETRY_STATE)
        _set_meta(db, "hmmm", HMMM)
        _set_meta(db, "definition_word_admission", WORD_ADMISSION_RULE)
        _set_meta(db, "evidence_channels", ["ordinal", "semantic", "sentence-context"])
        _set_meta(db, "resolution_rule", RESOLUTION_RULE)
        _set_meta(db, "character_identity", "one exact scalar -> one character id")
        _set_meta(db, "word_identity", "one exact surface -> one word id")
        _set_meta(db, "normalization", "none")
        _set_meta(db, "invented_geometry", "false")

        _character_ids, word_ids = _insert_identities(
            db, snapshot, public_position
        )
        _insert_definitions(db, snapshot, word_ids)
        db.commit()
        _assert_schema_boundary(db)
        receipt = _logical_receipt(db)

        counts = {
            table: db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in (
                "characters",
                "words",
                "word_characters",
                "definitions",
                "definition_words",
                "semantic_evidence",
                "unresolved_semantic_evidence",
            )
        }
        return {"receipt_sha256": receipt, "counts": counts}
    except Exception:
        db.close()
        if target.exists():
            target.unlink()
        raise
    finally:
        try:
            db.close()
        except Exception:
            pass


def run(
    snapshot: WordnetSnapshot,
    *,
    out_dir: str | Path,
    ucns_source_root: str | Path,
    overwrite: bool = False,
) -> dict[str, Any]:
    output = Path(out_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    public_gonol = _load_verified_public_gonol(ucns_source_root)

    result = build_construct(
        snapshot,
        db_path=output / "construct.db",
        public_position=public_gonol.public_gonol_position,
        public_gonol_sha256=public_gonol.PUBLIC_GONOL_SHA256,
        overwrite=overwrite,
    )

    manifest = {
        "schema": SCHEMA,
        "version": VERSION,
        "corpus": {
            "repository": OEWN_REPOSITORY,
            "tag": OEWN_TAG,
            "commit": OEWN_COMMIT,
            "source_tree_sha256": snapshot.source_tree_sha256,
            "source_file_count": snapshot.source_file_count,
            "lexeme_count": len(snapshot.lexemes),
            "synset_count": len(snapshot.synsets),
            "sense_count": snapshot.sense_count,
            "relation_count": snapshot.relation_count,
        },
        "ucns": {
            "commit": UCNS_PUBLIC_GONOL_COMMIT,
            "public_gonol_sha256": public_gonol.PUBLIC_GONOL_SHA256,
            "public_gonol_module_sha256": UCNS_PUBLIC_GONOL_MODULE_SHA256,
        },
        "construct_file": "construct.db",
        "receipt_sha256": result["receipt_sha256"],
        "counts": result["counts"],
        "geometry_state": GEOMETRY_STATE,
        "evidence_channels": ["ordinal", "semantic", "sentence-context"],
        "resolution_rule": RESOLUTION_RULE,
        "definition_word_admission": WORD_ADMISSION_RULE,
        "invented_geometry": False,
        "hmmm": HMMM,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def verify_replay(out_dir: str | Path) -> dict[str, Any]:
    output = Path(out_dir).resolve()
    manifest_path = output / "manifest.json"
    db_path = output / "construct.db"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema") != SCHEMA or manifest.get("version") != VERSION:
        raise FullConstructError("manifest schema/version mismatch")
    if manifest.get("construct_file") != "construct.db":
        raise FullConstructError("manifest construct file mismatch")
    db = sqlite3.connect(str(db_path))
    try:
        _assert_schema_boundary(db)
        observed = _logical_receipt(db)
    finally:
        db.close()
    if observed != manifest.get("receipt_sha256"):
        raise FullConstructError("construct logical receipt mismatch")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, help="OEWN 2025 src/yaml path")
    parser.add_argument("--ucns-source-root", required=True, help="UCNS checkout path")
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    snapshot = load_oewn_2025(args.source_root)
    manifest = run(
        snapshot,
        out_dir=args.out_dir,
        ucns_source_root=args.ucns_source_root,
        overwrite=args.overwrite,
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
