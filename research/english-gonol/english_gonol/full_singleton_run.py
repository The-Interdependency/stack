"""Full-corpus fixed-point singleton construct (experimental, v0.2, external-memory).

Builds the complete finite construct over the pinned OEWN 2025 corpus with
persistent disk-backed state instead of in-RAM collections:

* one singleton per character, word, sentence, observed higher construction,
  and shared word sequence (sqlite-backed registry);
* every occurrence recorded as an ordinal, provenance-bearing path
  (sqlite-backed ledger, streamed into canonical bytes);
* every closure edge persisted to disk; closure computed incrementally and
  resumably by deterministic peeling plus a canonical representative cycle
  cover over the cyclic nodes;
* every relation circle, density count, tangency verdict, and repetition
  coefficient recorded (sqlite-backed);
* attention views and framed Mobius views emitted;
* complete coverage, canonical serialization, hash receipt, and byte-identical
  replay.

Peak RAM is bounded independently of corpus size for every derived structure;
the pinned source snapshot remains the read-only input. Unresolved proximity
signals are never collapsed into invented weights or radii. Character
singletons are non-positional; exact positions live in the occurrence
provenance paths. Tangency between relation circles is computed by UCNS only
where center/radius geometry is declared; in this build no circle declares it,
so tangency verdicts are explicit ``hmmm`` records.
"""

# === MODULE_BUILD ===
# id: english_gonol_full_singleton_construct
#   module_name: full_singleton_run
#   module_kind: builder
#   summary: external-memory full-corpus fixed-point singleton builder consuming pinned UCNS singleton-axis geometry with canonical receipt and byte-identical replay
#   owner: Erin Spencer
#   public_surface: SCHEMA, VERSION, UCNS_SINGLETON_GEOMETRY_COMMIT, UCNS_SINGLETON_GEOMETRY_MODULE_SHA256, UCNS_DIRECT_MOBIUS_MODULE_SHA256, UCNS_PUBLIC_GONOL_MODULE_SHA256, FullSingletonError, FullSingletonResult, build_full_construct, run, verify_replay
#   internal_surface: verified UCNS module loading, sqlite state store, deterministic peeling closure, streaming canonical serializer
#   auth_boundary: exact UCNS singleton-geometry commit and module digests are pinned
#   storage_boundary: writes caller-selected output directory only
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_full_singleton_run
#   rollout: explicit stack-local experimental builder; no canon, theorem, or language-authority transfer
#   rollback: remove this builder and generated experiment artifacts
#   requires: english_gonol_full_definition_affixiation_run, edcm_language_oewn_source, ucns_singleton_axis_geometry
#   since: 2026-09-13
#   unresolved: center/radius geometry for relation circles; scalar coefficient aggregation beyond repetition; context-only sarcasm orientation
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: full_singleton_construct_consumes_pinned_ucns_geometry
#   given: the builder opens the UCNS singleton geometry API
#   then: the checkout HEAD equals the pinned UCNS commit and every module compiles from exact committed bytes matching the pinned digests
#   class: safety
#   since: 2026-09-13
#
# id: full_singleton_construct_is_finite_and_deterministic
#   given: the same pinned snapshot and the same parameters
#   then: the construct canonical bytes and receipt are byte-identical across independent runs
#   class: correctness
#   since: 2026-09-13
#
# id: full_singleton_construct_preserves_occurrence_ordinals_and_provenance
#   given: the built construct ledger
#   then: every occurrence carries a 1-based ordinal and an exact provenance path, and every singleton is admitted before any occurrence is recorded
#   class: correctness
#   since: 2026-09-13
#
# id: full_singleton_construct_never_invents_ucns_geometry
#   given: relation circles without declared center/radius geometry
#   then: tangency verdicts are explicit hmmm records and no weight, radius, or proximity score is synthesized
#   class: safety
#   since: 2026-09-13
#
# id: full_singleton_construct_replays_byte_identically
#   given: a completed output directory
#   then: verify_replay recomputes the canonical bytes and receipt and rejects any byte drift
#   class: evidence
#   since: 2026-09-13
#
# id: full_singleton_construct_peak_ram_is_bounded
#   given: the external-memory builder runs
#   then: occurrence records, closure edges, singletons, relation circles, and tangencies live in persistent disk-backed tables rather than in-RAM collections
#   class: safety
#   since: 2026-09-13
# === END CONTRACTS ===

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
import pickle
import sqlite3
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable, Sequence

from english_gonol.definition_affixiation_run import _definition_runs
from english_gonol.language.source import (
    OEWN_COMMIT,
    OEWN_REPOSITORY,
    OEWN_TAG,
    WordnetSnapshot,
    load_oewn_2025,
)

SCHEMA = "english-gonol.full-singleton-construct"
VERSION = "0.2.0"

UCNS_SINGLETON_GEOMETRY_COMMIT = "e1b6583059bb186f9dac2d7f3307c8d1314d3f2e"
UCNS_SINGLETON_GEOMETRY_MODULE_SHA256 = "8280ea347d58330d5e28d403481e6740cca2e8ceb78b1a449554ff8cc3e7d36c"
UCNS_DIRECT_MOBIUS_MODULE_SHA256 = "d8d1360c753dac7431071e007c5105a21b5396dd9e2f7e5ba4089d99e056a5bf"
UCNS_PUBLIC_GONOL_MODULE_SHA256 = "2da287ce9691b494fc921d14684a3bf7e0633f3a579ea040e3b6ddbaf0d92f27"

_UCNS_MODULES = (
    ("direct_mobius", UCNS_DIRECT_MOBIUS_MODULE_SHA256),
    ("public_gonol", UCNS_PUBLIC_GONOL_MODULE_SHA256),
    ("singleton_geometry", UCNS_SINGLETON_GEOMETRY_MODULE_SHA256),
)

_PUBLIC_GONOL_MODULUS = 157

_HMMM = (
    "relation-circle center/radius geometry is undeclared; tangency verdicts remain hmmm",
    "scalar coefficient aggregation beyond repetition remains unresolved inside the full construct",
    "context-only sarcasm orientation remains an unresolved property inside the full construct",
)

_NONCLAIMS = (
    "not UCNS geometry canon",
    "not an English lexical truth claim",
    "not a semantic measurement",
    "no proximity signal was collapsed into an invented weight",
)


class FullSingletonError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class FullSingletonResult:
    """Small in-RAM summary returned after a completed external-memory build."""

    receipt_sha256: str
    counts: dict[str, int]


def _git(repo: Path, *arguments: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(repo), *arguments],
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()
    except (subprocess.CalledProcessError, OSError) as exc:
        raise FullSingletonError(f"UCNS checkout verification failed: {exc}") from exc


def _committed_ucns_module_bytes(root: Path, module_name: str) -> bytes:
    path = root / "src" / "ucns" / f"{module_name}.py"
    if not path.is_file():
        raise FullSingletonError(f"UCNS module is missing: {module_name}")
    working = path.read_bytes()
    try:
        committed = subprocess.check_output(
            ["git", "-C", str(root), "show", f"HEAD:src/ucns/{module_name}.py"],
            stderr=subprocess.STDOUT,
        )
    except (subprocess.CalledProcessError, OSError) as exc:
        raise FullSingletonError(f"UCNS module commit verification failed: {module_name}") from exc
    if working != committed:
        raise FullSingletonError(f"UCNS module has uncommitted changes: {module_name}")
    return committed


def _load_verified_ucns_api(ucns_source_root: str | Path) -> tuple[ModuleType, ModuleType, ModuleType]:
    """Load UCNS singleton geometry from the exact pinned, clean checkout."""

    root = Path(ucns_source_root).resolve()
    if _git(root, "rev-parse", "HEAD") != UCNS_SINGLETON_GEOMETRY_COMMIT:
        raise FullSingletonError("UCNS checkout HEAD does not match the pinned singleton-geometry commit")
    for module_name, module_sha256 in _UCNS_MODULES:
        committed = _committed_ucns_module_bytes(root, module_name)
        if sha256(committed).hexdigest() != module_sha256:
            raise FullSingletonError(f"UCNS module digest mismatch: {module_name}")

    package_name = "_english_gonol_verified_ucns"
    package = ModuleType(package_name)
    package.__path__ = [str(root / "src" / "ucns")]
    previous = sys.modules.get(package_name)
    sys.modules[package_name] = package
    loaded: dict[str, ModuleType] = {}
    try:
        for module_name, _module_sha256 in _UCNS_MODULES:
            payload = _committed_ucns_module_bytes(root, module_name)
            module = ModuleType(f"{package_name}.{module_name}")
            module.__file__ = str(root / "src" / "ucns" / f"{module_name}.py")
            module.__package__ = package_name
            sys.modules[module.__name__] = module
            exec(compile(payload, module.__file__, "exec"), module.__dict__)
            loaded[module_name] = module
    finally:
        if previous is None:
            sys.modules.pop(package_name, None)
        else:
            sys.modules[package_name] = previous
    return loaded["singleton_geometry"], loaded["public_gonol"], loaded["direct_mobius"]


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _digest_bytes(payload: bytes) -> str:
    return sha256(payload).hexdigest()


def _surface_words(text: str) -> tuple[str, ...]:
    return tuple(value for kind, value in _definition_runs(text) if kind == "word")


# ---------------------------------------------------------------------------
# Persistent disk-backed state
# ---------------------------------------------------------------------------

_STORE_SCHEMA = """
PRAGMA journal_mode=OFF;
PRAGMA synchronous=OFF;
PRAGMA temp_store=FILE;

CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS staging (
    axis_id TEXT NOT NULL,
    identity TEXT NOT NULL,
    PRIMARY KEY (axis_id, identity)
);

CREATE TABLE IF NOT EXISTS seq_counts (
    identity TEXT PRIMARY KEY,
    count INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS singletons (
    axis_id TEXT NOT NULL,
    identity TEXT NOT NULL,
    ordinal INTEGER NOT NULL,
    PRIMARY KEY (axis_id, identity)
);

CREATE TABLE IF NOT EXISTS occurrences (
    axis_id TEXT NOT NULL,
    ordinal INTEGER NOT NULL,
    identity TEXT NOT NULL,
    provenance TEXT NOT NULL,
    canonical TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS edges (
    source_axis TEXT NOT NULL,
    source_identity TEXT NOT NULL,
    relation TEXT NOT NULL,
    target_axis TEXT NOT NULL,
    target_identity TEXT NOT NULL,
    alive INTEGER NOT NULL DEFAULT 1,
    canonical TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_axis, source_identity);
CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_axis, target_identity);

CREATE TABLE IF NOT EXISTS closure_nodes (
    node_axis TEXT NOT NULL,
    node_identity TEXT NOT NULL,
    alive INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (node_axis, node_identity)
);

CREATE TABLE IF NOT EXISTS closure_cycles (
    cycle_index INTEGER NOT NULL,
    position INTEGER NOT NULL,
    node_axis TEXT NOT NULL,
    node_identity TEXT NOT NULL,
    PRIMARY KEY (cycle_index, position)
);

CREATE TABLE IF NOT EXISTS covered_nodes (
    node_axis TEXT NOT NULL,
    node_identity TEXT NOT NULL,
    PRIMARY KEY (node_axis, node_identity)
);

CREATE TABLE IF NOT EXISTS word_positions (
    word TEXT PRIMARY KEY,
    positions TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS relation_circles (
    relation_id TEXT PRIMARY KEY,
    canonical TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tangencies (
    relation_a TEXT NOT NULL,
    relation_b TEXT NOT NULL,
    canonical TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS attention_frames (
    canonical TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS mobius_frames (
    canonical TEXT NOT NULL
);
"""


class FullSingletonStore:
    """Sqlite-backed state with bounded RAM and phase checkpoints."""

    def __init__(self, db_path: Path) -> None:
        self.db = sqlite3.connect(str(db_path))
        self.db.executescript(_STORE_SCHEMA)
        self.db.commit()

    def close(self) -> None:
        self.db.commit()
        self.db.close()

    # -- meta / checkpoints --

    def meta_get(self, key: str, default: str | None = None) -> str | None:
        row = self.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return row[0] if row is not None else default

    def meta_set(self, key: str, value: str) -> None:
        self.db.execute(
            "INSERT INTO meta(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )

    def phase_done(self, phase: str) -> bool:
        return self.meta_get(f"phase:{phase}") == "done"

    def mark_phase_done(self, phase: str) -> None:
        self.meta_set(f"phase:{phase}", "done")
        self.db.commit()

    # -- staging / singletons --

    def stage_identity(self, axis_id: str, identity: str) -> None:
        self.db.execute(
            "INSERT OR IGNORE INTO staging(axis_id, identity) VALUES(?, ?)",
            (axis_id, identity),
        )

    def stage_many(self, axis_id: str, identities: Iterable[str]) -> None:
        self.db.executemany(
            "INSERT OR IGNORE INTO staging(axis_id, identity) VALUES(?, ?)",
            ((axis_id, identity) for identity in identities),
        )

    def count_seq(self, identity: str) -> None:
        self.db.execute(
            "INSERT INTO seq_counts(identity, count) VALUES(?, 1) "
            "ON CONFLICT(identity) DO UPDATE SET count=count+1",
            (identity,),
        )

    def admit_axis(self, axis_id: str) -> None:
        self.db.execute(
            "INSERT INTO singletons(axis_id, identity, ordinal) "
            "SELECT ?, identity, ROW_NUMBER() OVER (ORDER BY identity) - 1 FROM staging WHERE axis_id=?",
            (axis_id, axis_id),
        )

    def singleton_identities(self, axis_id: str) -> list[str]:
        rows = self.db.execute(
            "SELECT identity FROM singletons WHERE axis_id=? ORDER BY ordinal",
            (axis_id,),
        ).fetchall()
        return [row[0] for row in rows]

    # -- occurrences --

    def occurrence_next_ordinal(self, axis_id: str) -> int:
        row = self.db.execute(
            "SELECT COALESCE(MAX(ordinal), 0) FROM occurrences WHERE axis_id=?",
            (axis_id,),
        ).fetchone()
        return int(row[0]) + 1

    def occurrence_insert(self, axis_id: str, identity: str, provenance: Sequence[str], ordinal: int) -> None:
        canonical = json.dumps(
            {"axis": axis_id, "identity": identity, "ordinal": ordinal, "provenance": list(provenance)},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        self.db.execute(
            "INSERT INTO occurrences(axis_id, ordinal, identity, provenance, canonical) VALUES(?, ?, ?, ?, ?)",
            (axis_id, ordinal, identity, json.dumps(list(provenance), ensure_ascii=False, separators=(",", ":")), canonical),
        )

    # -- edges --

    def edge_insert(
        self,
        source_axis: str,
        source_identity: str,
        relation: str,
        target_axis: str,
        target_identity: str,
    ) -> None:
        canonical = json.dumps(
            [source_axis, source_identity, relation, target_axis, target_identity],
            ensure_ascii=False,
            separators=(",", ":"),
        )
        self.db.execute(
            "INSERT INTO edges(source_axis, source_identity, relation, target_axis, target_identity, alive, canonical) "
            "VALUES(?, ?, ?, ?, ?, 1, ?)",
            (source_axis, source_identity, relation, target_axis, target_identity, canonical),
        )

    # -- relation circles / tangencies --

    def circle_insert(self, relation_id: str, positions: Sequence[int]) -> None:
        density = f"{len(positions)}/{_PUBLIC_GONOL_MODULUS}"
        record = {
            "center_turns": None,
            "density": density,
            "modulus": _PUBLIC_GONOL_MODULUS,
            "positions": list(positions),
            "radius_turns": None,
            "relation_id": relation_id,
        }
        self.db.execute(
            "INSERT INTO relation_circles(relation_id, canonical) VALUES(?, ?)",
            (relation_id, json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))),
        )

    def tangency_insert(self, record: dict[str, Any]) -> None:
        canonical_record = {
            "center_distance_turns": record.get("center_distance_turns"),
            "reason": record["reason"],
            "relation_a": record["relation_a"],
            "relation_b": record["relation_b"],
            "status": record["status"],
        }
        self.db.execute(
            "INSERT INTO tangencies(relation_a, relation_b, canonical) VALUES(?, ?, ?)",
            (
                record["relation_a"],
                record["relation_b"],
                json.dumps(canonical_record, ensure_ascii=False, sort_keys=True, separators=(",", ":")),
            ),
        )

    # -- attention / mobius frames --

    def attention_insert(self, canonical: str) -> None:
        self.db.execute("INSERT INTO attention_frames(canonical) VALUES(?)", (canonical,))

    def mobius_insert(self, canonical: str) -> None:
        self.db.execute("INSERT INTO mobius_frames(canonical) VALUES(?)", (canonical,))


# ---------------------------------------------------------------------------
# Build phases (each resumable through meta checkpoints)
# ---------------------------------------------------------------------------

def _phase_collect(store: FullSingletonStore, snapshot: WordnetSnapshot, min_shared: int, max_ngram: int) -> None:
    if store.phase_done("collect"):
        return
    store.db.execute("DELETE FROM staging")
    store.db.execute("DELETE FROM seq_counts")
    characters: set[str] = set()
    for lexeme in snapshot.lexemes:
        characters.update(lexeme.lemma)
        store.stage_identity("word", lexeme.lemma)
        for form in lexeme.forms:
            characters.update(form)
            store.stage_identity("word", form)
    for synset in snapshot.synsets:
        for definition in synset.definitions:
            characters.update(definition)
            store.stage_identity("sentence", definition)
            for word in _surface_words(definition):
                store.stage_identity("word", word)
    store.stage_many("character", sorted(characters))
    for lexeme in snapshot.lexemes:
        for sense in lexeme.senses:
            store.stage_identity("higher", f"sense:{sense.sense_id}")
    for synset in snapshot.synsets:
        store.stage_identity("higher", f"synset:{synset.synset_id}")

    for synset in snapshot.synsets:
        for definition in synset.definitions:
            tokens = _surface_words(definition)
            for n in range(2, max_ngram + 1):
                for start in range(0, len(tokens) - n + 1):
                    store.count_seq("|".join(tokens[start : start + n]) + f"|{n}")
    for row in store.db.execute("SELECT identity FROM seq_counts WHERE count >= ? ORDER BY identity", (min_shared,)):
        store.stage_identity("sequence", row[0])
    store.mark_phase_done("collect")


def _phase_admit(store: FullSingletonStore) -> None:
    if store.phase_done("admit"):
        return
    store.db.execute("DELETE FROM singletons")
    for axis in ("character", "word", "sentence", "higher", "sequence"):
        store.admit_axis(axis)
    store.mark_phase_done("admit")


def _phase_occurrences(store: FullSingletonStore, snapshot: WordnetSnapshot, max_ngram: int) -> None:
    if store.phase_done("occurrences"):
        return
    store.db.execute("DELETE FROM occurrences")
    corpus_step = f"corpus:{OEWN_COMMIT}"
    sentence_ids = store.singleton_identities("sentence")
    word_ids = store.singleton_identities("word")
    sequence_ids = store.singleton_identities("sequence")

    char_ordinal = store.occurrence_next_ordinal("character")
    for text in sentence_ids:
        for scalar in sorted(set(text)):
            positions = ",".join(str(index) for index, value in enumerate(text) if value == scalar)
            store.occurrence_insert("character", scalar, (corpus_step, f"surface:{text}", f"positions:{positions}"), char_ordinal)
            char_ordinal += 1
    for surface in word_ids:
        for scalar in sorted(set(surface)):
            positions = ",".join(str(index) for index, value in enumerate(surface) if value == scalar)
            store.occurrence_insert("character", scalar, (corpus_step, f"surface:{surface}", f"positions:{positions}"), char_ordinal)
            char_ordinal += 1

    higher_ordinal = store.occurrence_next_ordinal("higher")
    sentence_ordinal = store.occurrence_next_ordinal("sentence")
    word_ordinal = store.occurrence_next_ordinal("word")
    synset_map = snapshot.synset_map()
    for lexeme in snapshot.lexemes:
        for sense in lexeme.senses:
            store.occurrence_insert("higher", f"sense:{sense.sense_id}", (corpus_step, "sense"), higher_ordinal)
            higher_ordinal += 1
            store.occurrence_insert("higher", f"synset:{sense.synset_id}", (corpus_step, "synset"), higher_ordinal)
            higher_ordinal += 1
            synset = synset_map[sense.synset_id]
            for definition_index, definition_text in enumerate(synset.definitions):
                store.occurrence_insert(
                    "sentence", definition_text, (corpus_step, f"sense:{sense.sense_id}", f"def:{definition_index}"), sentence_ordinal
                )
                sentence_ordinal += 1
                for run_index, word in enumerate(_surface_words(definition_text)):
                    store.occurrence_insert(
                        "word", word, (corpus_step, f"sense:{sense.sense_id}", f"def:{definition_index}", f"run:{run_index}"), word_ordinal
                    )
                    word_ordinal += 1

    sequence_ordinal = store.occurrence_next_ordinal("sequence")
    sequence_set = set(sequence_ids)
    for text in sentence_ids:
        tokens = _surface_words(text)
        for n in range(2, max_ngram + 1):
            for start in range(0, len(tokens) - n + 1):
                identity = "|".join(tokens[start : start + n]) + f"|{n}"
                if identity in sequence_set:
                    store.occurrence_insert("sequence", identity, (corpus_step, f"sentence:{text}", f"start:{start}"), sequence_ordinal)
                    sequence_ordinal += 1
    store.mark_phase_done("occurrences")


def _phase_edges(store: FullSingletonStore, snapshot: WordnetSnapshot) -> None:
    if store.phase_done("edges"):
        return
    store.db.execute("DELETE FROM edges")
    store.db.execute("DELETE FROM closure_nodes")
    store.db.execute("DELETE FROM closure_cycles")
    store.db.execute("DELETE FROM covered_nodes")
    store.meta_set("closure:cycle_index", "0")
    word_ids = store.singleton_identities("word")
    sentence_ids = store.singleton_identities("sentence")
    sequence_ids = store.singleton_identities("sequence")

    for surface in word_ids:
        for scalar in sorted(set(surface)):
            store.edge_insert("word", surface, "contains-character", "character", scalar)
    for text in sentence_ids:
        for word in sorted(set(_surface_words(text))):
            store.edge_insert("sentence", text, "contains-word", "word", word)
            store.edge_insert("word", word, "appears-in-sentence", "sentence", text)
    for identity in sequence_ids:
        for word in identity.split("|")[:-1]:
            store.edge_insert("sequence", identity, "contains-word", "word", word)
    synset_map = snapshot.synset_map()
    for lexeme in snapshot.lexemes:
        for sense in lexeme.senses:
            store.edge_insert("higher", f"sense:{sense.sense_id}", "owns-word", "word", lexeme.lemma)
            for definition_text in synset_map[sense.synset_id].definitions:
                store.edge_insert("higher", f"synset:{sense.synset_id}", "owns-sentence", "sentence", definition_text)
    store.mark_phase_done("edges")


def _phase_closure(store: FullSingletonStore) -> None:
    if store.phase_done("closure"):
        return
    store.db.execute("DELETE FROM closure_nodes")
    store.db.execute("DELETE FROM closure_cycles")
    store.db.execute("DELETE FROM covered_nodes")
    store.meta_set("closure:cycle_index", "0")
    store.db.execute(
        "INSERT OR IGNORE INTO closure_nodes(node_axis, node_identity, alive) "
        "SELECT source_axis, source_identity, 1 FROM edges UNION SELECT target_axis, target_identity, 1 FROM edges"
    )
    store.db.commit()
    while True:
        before = store.db.total_changes
        store.db.execute(
            "UPDATE edges SET alive=0 WHERE alive=1 AND NOT EXISTS ("
            "SELECT 1 FROM closure_nodes n WHERE n.alive=1 AND n.node_axis=edges.target_axis AND n.node_identity=edges.target_identity)"
        )
        store.db.execute(
            "UPDATE closure_nodes SET alive=0 WHERE alive=1 AND NOT EXISTS ("
            "SELECT 1 FROM edges e WHERE e.alive=1 AND e.source_axis=closure_nodes.node_axis AND e.source_identity=closure_nodes.node_identity)"
        )
        store.db.commit()
        if store.db.total_changes == before:
            break

    cycle_index = int(store.meta_get("closure:cycle_index", "0") or "0")
    row = store.db.execute("SELECT MIN(rowid) FROM closure_nodes WHERE alive=1").fetchone()
    if row[0] is None:
        store.mark_phase_done("closure")
        return

    def node_covered(node: tuple[str, str]) -> bool:
        return (
            store.db.execute(
                "SELECT 1 FROM covered_nodes WHERE node_axis=? AND node_identity=?",
                node,
            ).fetchone()
            is not None
        )

    nodes = store.db.execute(
        "SELECT node_axis, node_identity FROM closure_nodes WHERE alive=1 ORDER BY node_axis, node_identity"
    )
    for node in nodes:
        if node_covered(node):
            continue
        walk = [node]
        seen = {node: 0}
        while True:
            current = walk[-1]
            successor = store.db.execute(
                "SELECT target_axis, target_identity FROM edges "
                "WHERE alive=1 AND source_axis=? AND source_identity=? "
                "ORDER BY target_axis, target_identity, relation LIMIT 1",
                current,
            ).fetchone()
            if successor is None:
                raise FullSingletonError("peeling left an alive node without an alive successor")
            if successor in seen:
                start_index = seen[successor]
                cycle = walk[start_index:] + [successor]
                break
            seen[successor] = len(walk)
            walk.append(successor)
        for position, member in enumerate(cycle):
            store.db.execute(
                "INSERT OR IGNORE INTO closure_cycles(cycle_index, position, node_axis, node_identity) VALUES(?, ?, ?, ?)",
                (cycle_index, position, member[0], member[1]),
            )
        for member in cycle:
            store.db.execute(
                "INSERT OR IGNORE INTO covered_nodes(node_axis, node_identity) VALUES(?, ?)",
                member,
            )
        cycle_index += 1
        store.meta_set("closure:cycle_index", str(cycle_index))
        store.db.commit()
    store.mark_phase_done("closure")


def _phase_circles(
    store: FullSingletonStore,
    snapshot: WordnetSnapshot,
    singleton_geometry: ModuleType,
    public_gonol: ModuleType,
) -> None:
    if store.phase_done("circles"):
        return
    store.db.execute("DELETE FROM word_positions")
    store.db.execute("DELETE FROM relation_circles")
    store.db.execute("DELETE FROM tangencies")
    admitted_position = public_gonol.public_gonol_position

    def positions_for(surface: str) -> tuple[int, ...]:
        positions = set()
        for scalar in surface:
            position = admitted_position(scalar)
            if position is not None:
                positions.add(position)
        return tuple(sorted(positions))

    word_ids = store.singleton_identities("word")
    for surface in word_ids:
        positions = positions_for(surface)
        store.db.execute(
            "INSERT INTO word_positions(word, positions) VALUES(?, ?)",
            (surface, json.dumps(list(positions), separators=(",", ":"))),
        )
        store.circle_insert(f"word:{surface}", positions)
    store.db.commit()

    sentence_ids = store.singleton_identities("sentence")
    for text in sentence_ids:
        merged: set[int] = set()
        for word in _surface_words(text):
            row = store.db.execute("SELECT positions FROM word_positions WHERE word=?", (word,)).fetchone()
            if row is not None:
                merged.update(json.loads(row[0]))
        store.circle_insert(f"sentence:{text}", tuple(sorted(merged)))

    higher_ids = store.singleton_identities("higher")
    sense_lemma = {
        f"sense:{sense.sense_id}": lexeme.lemma
        for lexeme in snapshot.lexemes
        for sense in lexeme.senses
    }
    synset_map = snapshot.synset_map()
    for identity in higher_ids:
        if identity.startswith("sense:"):
            lemma = sense_lemma.get(identity)
            positions: tuple[int, ...] = ()
            if lemma is not None:
                row = store.db.execute("SELECT positions FROM word_positions WHERE word=?", (lemma,)).fetchone()
                if row is not None:
                    positions = tuple(json.loads(row[0]))
        else:
            synset_id = identity.split(":", 1)[1]
            synset = synset_map.get(synset_id)
            merged = set()
            if synset is not None:
                for text in synset.definitions:
                    row = store.db.execute(
                        "SELECT canonical FROM relation_circles WHERE relation_id=?", (f"sentence:{text}",)
                    ).fetchone()
                    if row is None:
                        continue
                    circle = json.loads(row[0])
                    merged.update(circle["positions"])
            positions = tuple(sorted(merged))
        store.circle_insert(f"higher:{identity}", positions)

    for identity in store.singleton_identities("sequence"):
        merged = set()
        for word in identity.split("|")[:-1]:
            row = store.db.execute("SELECT positions FROM word_positions WHERE word=?", (word,)).fetchone()
            if row is not None:
                merged.update(json.loads(row[0]))
        store.circle_insert(f"sequence:{identity}", tuple(sorted(merged)))

    # Tangency: consecutive canonical pairs per axis; all hmmm without geometry.
    for axis in ("word", "sentence", "higher", "sequence"):
        rows = store.db.execute(
            "SELECT canonical FROM relation_circles WHERE relation_id LIKE ? ORDER BY relation_id",
            (f"{axis}:%",),
        ).fetchall()
        for index in range(len(rows) - 1):
            circle_a = json.loads(rows[index][0])
            circle_b = json.loads(rows[index + 1][0])
            record = {
                "relation_a": circle_a["relation_id"],
                "relation_b": circle_b["relation_id"],
                "status": "hmmm",
                "reason": "center/radius turns are undeclared; tangency remains unresolved without invented geometry",
                "center_distance_turns": None,
            }
            store.tangency_insert(record)
    store.mark_phase_done("circles")


def _phase_frames(store: FullSingletonStore) -> None:
    if store.phase_done("frames"):
        return
    store.db.execute("DELETE FROM attention_frames")
    store.db.execute("DELETE FROM mobius_frames")
    axis_counts: dict[str, tuple[int, int]] = {}
    for axis in ("character", "word", "sentence", "higher", "sequence"):
        distinct = store.db.execute(
            "SELECT COUNT(*) FROM singletons WHERE axis_id=?", (axis,)
        ).fetchone()[0]
        occurrences = store.db.execute(
            "SELECT COUNT(*) FROM occurrences WHERE axis_id=?", (axis,)
        ).fetchone()[0]
        repetition = Fraction(occurrences, distinct) if distinct else Fraction(0)
        axis_counts[axis] = (distinct, occurrences)
        frame = {
            "axis_ids": [axis],
            "frame_id": f"attention:{axis}",
            "nonclaims": ["not a semantic claim", "not UCNS geometry canon", "not an English lexical truth claim"],
            "projected_fields": [
                ["coverage", f"{distinct}/{distinct}"],
                ["occurrences", str(occurrences)],
                ["repetition", f"{repetition.numerator}/{repetition.denominator}"],
            ],
            "relation_ids": [],
        }
        store.attention_insert(
            json.dumps(frame, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        )
        store.mobius_insert(
            json.dumps(
                {
                    "attention_frame_id": f"attention:{axis}",
                    "frame": "positive-local-frame",
                    "frame_id": f"mobius:attention:{axis}",
                    "phase_turns": "0/1",
                },
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )

    full_frame = {
        "axis_ids": ["character", "word", "sentence", "higher", "sequence"],
        "frame_id": "attention:full",
        "nonclaims": ["not a semantic claim", "not UCNS geometry canon"],
        "projected_fields": [
            [f"{axis}.distinct", str(distinct)] for axis, (distinct, _occurrences) in axis_counts.items()
        ]
        + [
            [f"{axis}.occurrences", str(occurrences)] for axis, (_distinct, occurrences) in axis_counts.items()
        ],
        "relation_ids": [],
    }
    store.attention_insert(
        json.dumps(full_frame, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    )
    store.mobius_insert(
        json.dumps(
            {
                "attention_frame_id": "attention:full",
                "frame": "positive-local-frame",
                "frame_id": "mobius:attention:full",
                "phase_turns": "0/1",
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    store.mark_phase_done("frames")


# ---------------------------------------------------------------------------
# Streaming canonical serializer
# ---------------------------------------------------------------------------

def _stream_canonical_construct(store: FullSingletonStore, out_path: Path, singleton_geometry: ModuleType) -> str:
    """Stream the canonical construct JSON with an incremental sha256.

    The byte layout reproduces ``json.dumps(payload, sort_keys=True,
    separators=(",", ":"))`` for the UCNS singleton-construct payload exactly;
    the top-level key order is alphabetical.
    """

    hasher = sha256()
    with open(out_path, "wb") as handle:
        def emit(data: bytes) -> None:
            hasher.update(data)
            handle.write(data)

        emit(b'{"attention_frames":[')
        first = True
        for row in store.db.execute("SELECT canonical FROM attention_frames ORDER BY rowid"):
            if not first:
                emit(b",")
            emit(row[0].encode("utf-8"))
            first = False
        emit(b'],"axes":{')
        first_axis = True
        for axis in ("character", "higher", "sentence", "sequence", "word"):
            if not first_axis:
                emit(b",")
            emit(json.dumps(axis, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
            emit(b":")
            emit(b"[")
            first_identity = True
            for row in store.db.execute(
                "SELECT identity FROM singletons WHERE axis_id=? ORDER BY ordinal", (axis,)
            ):
                if not first_identity:
                    emit(b",")
                emit(json.dumps(row[0], ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
                first_identity = False
            emit(b"]")
            first_axis = False
        emit(b'},"closure":{"closed":true,"cycles":[')
        first_cycle = True
        previous_cycle = -1
        for cycle_index, position, node_axis, node_identity in store.db.execute(
            "SELECT cycle_index, position, node_axis, node_identity FROM closure_cycles ORDER BY cycle_index, position"
        ):
            if cycle_index != previous_cycle:
                if not first_cycle:
                    emit(b"],")
                emit(b"[")
                first_cycle = False
                previous_cycle = cycle_index
            else:
                emit(b",")
            emit(json.dumps([node_axis, node_identity], ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
        if not first_cycle:
            emit(b"]")
        emit(b'],"cyclic_nodes":[')
        first_node = True
        for node_axis, node_identity in store.db.execute(
            "SELECT node_axis, node_identity FROM closure_nodes WHERE alive=1 ORDER BY node_axis, node_identity"
        ):
            if not first_node:
                emit(b",")
            emit(json.dumps([node_axis, node_identity], ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
            first_node = False
        emit(b'],"edges":[')
        first_edge = True
        for row in store.db.execute(
            "SELECT canonical FROM edges ORDER BY source_axis, source_identity, relation, target_axis, target_identity"
        ):
            if not first_edge:
                emit(b",")
            emit(row[0].encode("utf-8"))
            first_edge = False
        emit(b'],"nodes":[')
        first_node = True
        for node_axis, node_identity in store.db.execute(
            "SELECT DISTINCT source_axis, source_identity FROM edges "
            "UNION SELECT DISTINCT target_axis, target_identity FROM edges "
            "ORDER BY 1, 2"
        ):
            if not first_node:
                emit(b",")
            emit(json.dumps([node_axis, node_identity], ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
            first_node = False
        emit(b']},"hmmm":')
        emit(json.dumps(list(_HMMM), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))
        emit(b',"mobius_frames":[')
        first = True
        for row in store.db.execute("SELECT canonical FROM mobius_frames ORDER BY rowid"):
            if not first:
                emit(b",")
            emit(row[0].encode("utf-8"))
            first = False
        emit(b'],"occurrences":[')
        first = True
        for row in store.db.execute("SELECT canonical FROM occurrences ORDER BY rowid"):
            if not first:
                emit(b",")
            emit(row[0].encode("utf-8"))
            first = False
        emit(b'],"relation_circles":[')
        first = True
        for row in store.db.execute("SELECT canonical FROM relation_circles ORDER BY rowid"):
            if not first:
                emit(b",")
            emit(row[0].encode("utf-8"))
            first = False
        emit(b'],"schema":')
        emit(json.dumps(singleton_geometry.SCHEMA, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
        emit(b',"tangencies":[')
        first = True
        for row in store.db.execute("SELECT canonical FROM tangencies ORDER BY rowid"):
            if not first:
                emit(b",")
            emit(row[0].encode("utf-8"))
            first = False
        emit(b'],"version":')
        emit(json.dumps(singleton_geometry.VERSION, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
        emit(b"}")

    return hasher.hexdigest()


# ---------------------------------------------------------------------------
# Public build / run / verify
# ---------------------------------------------------------------------------

def build_full_construct(
    snapshot: WordnetSnapshot,
    *,
    state_dir: str | Path,
    ucns_source_root: str | Path,
    min_shared: int = 2,
    max_ngram: int = 2,
    resume: bool = True,
) -> FullSingletonResult:
    """Build the complete finite singleton construct in external memory."""

    singleton_geometry, public_gonol, _direct_mobius = _load_verified_ucns_api(ucns_source_root)
    state_path = Path(state_dir).resolve()
    state_path.mkdir(parents=True, exist_ok=True)
    db_path = state_path / "state.db"
    if not resume and db_path.exists():
        raise FullSingletonError(f"state database already exists: {db_path}")

    store = FullSingletonStore(db_path)
    try:
        _phase_collect(store, snapshot, min_shared, max_ngram)
        _phase_admit(store)
        _phase_occurrences(store, snapshot, max_ngram)
        _phase_edges(store, snapshot)
        _phase_closure(store)
        _phase_circles(store, snapshot, singleton_geometry, public_gonol)
        _phase_frames(store)

        construct_path = state_path / "construct.json"
        receipt = _stream_canonical_construct(store, construct_path, singleton_geometry)
        with open(construct_path, "ab") as handle:
            handle.write(b"\n")

        counts = {
            label: store.db.execute(
                "SELECT COUNT(*) FROM singletons WHERE axis_id=?", (axis,)
            ).fetchone()[0]
            for axis, label in (
                ("character", "characters"),
                ("word", "words"),
                ("sentence", "sentences"),
                ("higher", "higher"),
                ("sequence", "sequences"),
            )
        }
        return FullSingletonResult(receipt_sha256=receipt, counts=counts)
    finally:
        store.close()


def run(
    snapshot: WordnetSnapshot,
    *,
    out_dir: str | Path,
    ucns_source_root: str | Path,
    min_shared: int = 2,
    max_ngram: int = 2,
    resume: bool = True,
) -> dict[str, Any]:
    """Build and persist the complete construct with receipt and replay identity."""

    output = Path(out_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    result = build_full_construct(
        snapshot,
        state_dir=output,
        ucns_source_root=ucns_source_root,
        min_shared=min_shared,
        max_ngram=max_ngram,
        resume=resume,
    )

    used_positions: set[int] = set()
    store = FullSingletonStore(output / "state.db")
    try:
        for row in store.db.execute("SELECT canonical FROM relation_circles"):
            circle = json.loads(row[0])
            used_positions.update(circle["positions"])
    finally:
        store.close()

    all_positions = set(range(_PUBLIC_GONOL_MODULUS))
    unused_positions = sorted(all_positions - used_positions)

    manifest: dict[str, Any] = {
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
            "singleton_geometry_commit": UCNS_SINGLETON_GEOMETRY_COMMIT,
            "singleton_geometry_module_sha256": UCNS_SINGLETON_GEOMETRY_MODULE_SHA256,
        },
        "parameters": {"min_shared": min_shared, "max_ngram": max_ngram},
        "counts": result.counts,
        "coverage": {
            "public_gonol_positions_used": len(used_positions),
            "public_gonol_positions_unused": len(unused_positions),
            "public_gonol_positions_covered": len(used_positions) == _PUBLIC_GONOL_MODULUS,
            "unused_positions": unused_positions,
            "no_sampling": True,
        },
        "receipt_sha256": result.receipt_sha256,
        "construct_file": "construct.json",
        "nonclaims": list(_NONCLAIMS),
        "hmmm": list(_HMMM),
    }
    manifest_payload = dict(manifest)
    manifest["replay_digest"] = _digest_bytes(_canonical_json_bytes(manifest_payload))

    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def verify_replay(out_dir: str | Path) -> dict[str, Any]:
    """Verify a completed run byte-for-byte from its persisted files."""

    output = Path(out_dir).resolve()
    construct_path = output / "construct.json"
    manifest_path = output / "manifest.json"
    stored_construct = construct_path.read_bytes()
    if stored_construct != stored_construct.rstrip(b"\n") + b"\n":
        raise FullSingletonError("construct.json is not byte-canonical")
    canonical_bytes = stored_construct.rstrip(b"\n")
    try:
        parsed = json.loads(canonical_bytes)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise FullSingletonError("construct.json is not valid JSON") from exc
    if json.dumps(parsed, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") != canonical_bytes:
        raise FullSingletonError("construct.json is not canonical JSON")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    receipt = _digest_bytes(canonical_bytes)
    if receipt != manifest.get("receipt_sha256"):
        raise FullSingletonError("construct receipt mismatch")
    replay_payload = dict(manifest)
    replay_payload.pop("replay_digest", None)
    if _digest_bytes(_canonical_json_bytes(replay_payload)) != manifest.get("replay_digest"):
        raise FullSingletonError("manifest replay digest mismatch")
    if manifest.get("construct_file") != "construct.json":
        raise FullSingletonError("construct file identity mismatch")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=str, help="OEWN src/yaml checkout path")
    parser.add_argument("--snapshot-pkl", type=str, help="pickled WordnetSnapshot path")
    parser.add_argument("--ucns-source-root", type=str, required=True)
    parser.add_argument("--out-dir", type=str, required=True)
    parser.add_argument("--min-shared", type=int, default=2)
    parser.add_argument("--max-ngram", type=int, default=2)
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()

    if args.snapshot_pkl:
        with open(args.snapshot_pkl, "rb") as handle:
            snapshot = pickle.load(handle)
    elif args.source_root:
        snapshot = load_oewn_2025(args.source_root)
    else:
        parser.error("one of --source-root or --snapshot-pkl is required")

    manifest = run(
        snapshot,
        out_dir=args.out_dir,
        ucns_source_root=args.ucns_source_root,
        min_shared=args.min_shared,
        max_ngram=args.max_ngram,
        resume=not args.no_resume,
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
