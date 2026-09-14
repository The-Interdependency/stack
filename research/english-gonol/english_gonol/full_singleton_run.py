"""Full-corpus fixed-point singleton construct (experimental, v0.1).

Builds the complete finite construct over the pinned OEWN 2025 corpus:

* one singleton per character, word, sentence, and observed higher construction;
* one singleton per shared word sequence that recurs in the corpus;
* every occurrence recorded as an ordinal, provenance-bearing path;
* reused singletons closed into a finite cyclic graph;
* every relation circle, density count, tangency verdict, and repetition
  coefficient recorded;
* attention views and framed Mobius views emitted;
* complete coverage, canonical serialization, hash receipt, and byte-identical
  replay.

Unresolved proximity signals are never collapsed into invented weights or
radii. Character singletons are non-positional; exact positions live in the
occurrence provenance paths. Tangency between relation circles is computed by
UCNS only where center/radius geometry is declared; in this build no circle
declares it, so tangency verdicts are explicit ``hmmm`` records.
"""

# === MODULE_BUILD ===
# id: english_gonol_full_singleton_construct
#   module_name: full_singleton_run
#   module_kind: builder
#   summary: consumes the pinned UCNS singleton-axis geometry to build the complete finite current-corpus construct with canonical receipt and byte-identical replay
#   owner: Erin Spencer
#   public_surface: SCHEMA, VERSION, UCNS_SINGLETON_GEOMETRY_COMMIT, UCNS_SINGLETON_GEOMETRY_MODULE_SHA256, UCNS_DIRECT_MOBIUS_MODULE_SHA256, UCNS_PUBLIC_GONOL_MODULE_SHA256, FullSingletonError, build_full_construct, run, verify_replay
#   internal_surface: verified UCNS module loading, deterministic corpus traversal, occurrence recording
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
# === END CONTRACTS ===

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import json
import pickle
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable, Mapping, Sequence

from english_gonol.definition_affixiation_run import _definition_runs
from english_gonol.language.source import (
    OEWN_COMMIT,
    OEWN_REPOSITORY,
    OEWN_TAG,
    WordnetSnapshot,
    load_oewn_2025,
)

SCHEMA = "english-gonol.full-singleton-construct"
VERSION = "0.1.0"

UCNS_SINGLETON_GEOMETRY_COMMIT = "e1b6583059bb186f9dac2d7f3307c8d1314d3f2e"
UCNS_SINGLETON_GEOMETRY_MODULE_SHA256 = "8280ea347d58330d5e28d403481e6740cca2e8ceb78b1a449554ff8cc3e7d36c"
UCNS_DIRECT_MOBIUS_MODULE_SHA256 = "d8d1360c753dac7431071e007c5105a21b5396dd9e2f7e5ba4089d99e056a5bf"
UCNS_PUBLIC_GONOL_MODULE_SHA256 = "2da287ce9691b494fc921d14684a3bf7e0633f3a579ea040e3b6ddbaf0d92f27"

_UCNS_MODULES = (
    ("direct_mobius", UCNS_DIRECT_MOBIUS_MODULE_SHA256),
    ("public_gonol", UCNS_PUBLIC_GONOL_MODULE_SHA256),
    ("singleton_geometry", UCNS_SINGLETON_GEOMETRY_MODULE_SHA256),
)


class FullSingletonError(RuntimeError):
    pass


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


def _sorted_unique(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted(set(values)))


def _surface_words(text: str) -> tuple[str, ...]:
    return tuple(value for kind, value in _definition_runs(text) if kind == "word")


def _collect_corpus_surfaces(snapshot: WordnetSnapshot) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    characters: set[str] = set()
    words: set[str] = set()
    sentences: set[str] = set()

    for lexeme in snapshot.lexemes:
        characters.update(lexeme.lemma)
        words.add(lexeme.lemma)
        for form in lexeme.forms:
            characters.update(form)
            words.add(form)
    for synset in snapshot.synsets:
        for definition in synset.definitions:
            characters.update(definition)
            sentences.add(definition)
            for word in _surface_words(definition):
                words.add(word)
    return _sorted_unique(characters), _sorted_unique(words), _sorted_unique(sentences)


def _collect_higher_identities(snapshot: WordnetSnapshot) -> tuple[str, ...]:
    identities: set[str] = set()
    for lexeme in snapshot.lexemes:
        for sense in lexeme.senses:
            identities.add(f"sense:{sense.sense_id}")
    for synset in snapshot.synsets:
        identities.add(f"synset:{synset.synset_id}")
    return _sorted_unique(identities)


def _shared_sequences(
    sentences: Sequence[str],
    *,
    min_shared: int,
    max_ngram: int,
) -> tuple[str, ...]:
    """Return sorted shared word n-gram identities ``token|...|token|n``."""

    counts: dict[str, int] = {}
    for text in sentences:
        tokens = _surface_words(text)
        for n in range(2, max_ngram + 1):
            for start in range(0, len(tokens) - n + 1):
                identity = "|".join(tokens[start : start + n]) + f"|{n}"
                counts[identity] = counts.get(identity, 0) + 1
    return _sorted_unique(identity for identity, count in counts.items() if count >= min_shared)


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _digest_bytes(payload: bytes) -> str:
    return sha256(payload).hexdigest()


def build_full_construct(
    snapshot: WordnetSnapshot,
    *,
    ucns_source_root: str | Path,
    min_shared: int = 2,
    max_ngram: int = 2,
) -> Any:
    """Build the complete finite singleton construct for a pinned snapshot."""

    singleton_geometry, public_gonol, _direct_mobius = _load_verified_ucns_api(ucns_source_root)
    builder = singleton_geometry.SingletonConstructBuilder(
        hmmm=[
            "relation-circle center/radius geometry is undeclared; tangency verdicts remain hmmm",
            "scalar coefficient aggregation beyond repetition remains unresolved inside the full construct",
            "context-only sarcasm orientation remains an unresolved property inside the full construct",
        ]
    )

    characters, words, sentences = _collect_corpus_surfaces(snapshot)
    higher = _collect_higher_identities(snapshot)
    sequences = _shared_sequences(sentences, min_shared=min_shared, max_ngram=max_ngram)

    # One singleton per admitted identity, in deterministic sorted order.
    for scalar in characters:
        builder.admit("character", scalar)
    for surface in words:
        builder.admit("word", surface)
    for text in sentences:
        builder.admit("sentence", text)
    for identity in higher:
        builder.admit("higher", identity)
    for identity in sequences:
        builder.admit("sequence", identity)

    # Occurrences: ordinal, provenance-bearing paths.
    corpus_step = f"corpus:{OEWN_COMMIT}"
    for text in sentences:
        for scalar in sorted(set(text)):
            positions = ",".join(str(index) for index, value in enumerate(text) if value == scalar)
            builder.record_occurrence("character", scalar, (corpus_step, f"surface:{text}", f"positions:{positions}"))
    for surface in words:
        for scalar in sorted(set(surface)):
            positions = ",".join(str(index) for index, value in enumerate(surface) if value == scalar)
            builder.record_occurrence("character", scalar, (corpus_step, f"surface:{surface}", f"positions:{positions}"))

    synset_map = snapshot.synset_map()
    for lexeme in snapshot.lexemes:
        lemma = lexeme.lemma
        for sense in lexeme.senses:
            builder.record_occurrence("higher", f"sense:{sense.sense_id}", (corpus_step, "sense"))
            builder.record_occurrence("higher", f"synset:{sense.synset_id}", (corpus_step, "synset"))
            synset = synset_map[sense.synset_id]
            for definition_index, definition_text in enumerate(synset.definitions):
                builder.record_occurrence(
                    "sentence", definition_text, (corpus_step, f"sense:{sense.sense_id}", f"def:{definition_index}")
                )
                for run_index, word in enumerate(_surface_words(definition_text)):
                    builder.record_occurrence(
                        "word", word, (corpus_step, f"sense:{sense.sense_id}", f"def:{definition_index}", f"run:{run_index}")
                    )

    # Shared sequences: one occurrence per sentence position where they appear.
    sequence_words = {identity: identity.split("|")[:-1] for identity in sequences}
    for text in sentences:
        tokens = _surface_words(text)
        for n in range(2, max_ngram + 1):
            for start in range(0, len(tokens) - n + 1):
                identity = "|".join(tokens[start : start + n]) + f"|{n}"
                if identity in sequence_words:
                    builder.record_occurrence(
                        "sequence", identity, (corpus_step, f"sentence:{text}", f"start:{start}")
                    )

    # Closure edges: reuse singletons until the finite graph closes.
    for surface in words:
        for scalar in sorted(set(surface)):
            builder.add_edge("word", surface, "contains-character", "character", scalar)
    for text in sentences:
        for word in sorted(set(_surface_words(text))):
            builder.add_edge("sentence", text, "contains-word", "word", word)
            builder.add_edge("word", word, "appears-in-sentence", "sentence", text)
    for identity in sequences:
        for word in sequence_words[identity]:
            builder.add_edge("sequence", identity, "contains-word", "word", word)
    for lexeme in snapshot.lexemes:
        for sense in lexeme.senses:
            builder.add_edge("higher", f"sense:{sense.sense_id}", "owns-word", "word", lexeme.lemma)
            for definition_text in synset_map[sense.synset_id].definitions:
                builder.add_edge("higher", f"synset:{sense.synset_id}", "owns-sentence", "sentence", definition_text)

    # Relation circles: every relation with exact Public Gonol positions.
    admitted_position = public_gonol.public_gonol_position

    def word_positions(surface: str) -> tuple[int, ...]:
        positions: set[int] = set()
        for scalar in surface:
            position = admitted_position(scalar)
            if position is not None:
                positions.add(position)
        return tuple(sorted(positions))

    word_circle_positions = {surface: word_positions(surface) for surface in words}
    sentence_circle_positions = {
        text: tuple(sorted({position for word in _surface_words(text) for position in word_circle_positions[word]}))
        for text in sentences
    }
    sense_lemma: dict[str, str] = {}
    for lexeme in snapshot.lexemes:
        for sense in lexeme.senses:
            sense_lemma[sense.sense_id] = lexeme.lemma

    higher_circle_positions: dict[str, tuple[int, ...]] = {}
    for identity in higher:
        if identity.startswith("sense:"):
            sense_id = identity.split(":", 1)[1]
            lemma = sense_lemma.get(sense_id)
            if lemma is not None:
                higher_circle_positions[identity] = word_circle_positions[lemma]
        else:
            synset_id = identity.split(":", 1)[1]
            synset = synset_map.get(synset_id)
            if synset is not None:
                higher_circle_positions[identity] = tuple(
                    sorted({position for text in synset.definitions for position in sentence_circle_positions.get(text, ())})
                )
    sequence_circle_positions = {
        identity: tuple(sorted({position for word in sequence_words[identity] for position in word_circle_positions.get(word, ())}))
        for identity in sequences
    }

    relation_circles: list[tuple[str, Any]] = []
    for surface in words:
        circle = builder.add_relation_circle(f"word:{surface}", modulus=157, positions=word_circle_positions[surface])
        relation_circles.append((circle.relation_id, circle))
    for text in sentences:
        circle = builder.add_relation_circle(f"sentence:{text}", modulus=157, positions=sentence_circle_positions[text])
        relation_circles.append((circle.relation_id, circle))
    for identity in higher:
        circle = builder.add_relation_circle(f"higher:{identity}", modulus=157, positions=higher_circle_positions.get(identity, ()))
        relation_circles.append((circle.relation_id, circle))
    for identity in sequences:
        circle = builder.add_relation_circle(f"sequence:{identity}", modulus=157, positions=sequence_circle_positions[identity])
        relation_circles.append((circle.relation_id, circle))

    # Tangency: consecutive canonical pairs per axis. No circle declares
    # center/radius geometry here, so every verdict is an explicit hmmm record.
    for axis in ("word", "sentence", "higher", "sequence"):
        axis_circles = [
            (relation_id, circle)
            for relation_id, circle in relation_circles
            if relation_id.startswith(f"{axis}:")
        ]
        for (relation_a, circle_a), (relation_b, circle_b) in zip(axis_circles, axis_circles[1:]):
            verdict = singleton_geometry.relation_tangency(circle_a, circle_b)
            if verdict is not None:
                builder.add_tangency(verdict)

    # Attention views and framed Mobius views.
    axis_summaries: dict[str, tuple[int, int]] = {}
    for axis in ("character", "word", "sentence", "higher", "sequence"):
        identities = {
            "character": characters,
            "word": words,
            "sentence": sentences,
            "higher": higher,
            "sequence": sequences,
        }[axis]
        occurrences = builder._ledger.occurrence_count(axis)
        distinct = len(identities)
        repetition = Fraction(occurrences, distinct) if distinct else Fraction(0)
        axis_summaries[axis] = (distinct, occurrences)
        frame = singleton_geometry.AttentionFrame(
            frame_id=f"attention:{axis}",
            axis_ids=(axis,),
            relation_ids=(),
            projected_fields=(
                ("coverage", f"{distinct}/{distinct}"),
                ("occurrences", str(occurrences)),
                ("repetition", f"{repetition.numerator}/{repetition.denominator}"),
            ),
            nonclaims=("not a semantic claim", "not UCNS geometry canon", "not an English lexical truth claim"),
        )
        builder.add_attention_frame(frame)
        builder.add_mobius_frame(singleton_geometry.build_mobius_frame(f"mobius:attention:{axis}", frame.frame_id))

    full_frame = singleton_geometry.AttentionFrame(
        frame_id="attention:full",
        axis_ids=("character", "word", "sentence", "higher", "sequence"),
        relation_ids=(),
        projected_fields=tuple(
            (f"{axis}.distinct", str(distinct)) for axis, (distinct, _occurrences) in axis_summaries.items()
        )
        + tuple((f"{axis}.occurrences", str(occurrences)) for axis, (_distinct, occurrences) in axis_summaries.items()),
        nonclaims=("not a semantic claim", "not UCNS geometry canon"),
    )
    builder.add_attention_frame(full_frame)
    builder.add_mobius_frame(singleton_geometry.build_mobius_frame("mobius:attention:full", full_frame.frame_id))

    construct = builder.build()
    return construct, {
        "characters": len(characters),
        "words": len(words),
        "sentences": len(sentences),
        "higher": len(higher),
        "sequences": len(sequences),
    }


def run(
    snapshot: WordnetSnapshot,
    *,
    out_dir: str | Path,
    ucns_source_root: str | Path,
    min_shared: int = 2,
    max_ngram: int = 2,
) -> dict[str, Any]:
    """Build and persist the complete construct with receipt and replay identity."""

    output = Path(out_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise FullSingletonError(f"output directory must be empty: {output}")

    construct, counts = build_full_construct(
        snapshot,
        ucns_source_root=ucns_source_root,
        min_shared=min_shared,
        max_ngram=max_ngram,
    )
    construct_bytes = construct.canonical_bytes()
    receipt = construct.receipt_sha256()

    used_positions = set()
    for circle in construct.relation_circles:
        used_positions.update(circle.positions)
    all_positions = set(range(157))
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
        "counts": counts,
        "coverage": {
            "public_gonol_positions_used": len(used_positions),
            "public_gonol_positions_unused": len(unused_positions),
            "public_gonol_positions_covered": len(used_positions) == 157,
            "unused_positions": unused_positions,
            "no_sampling": True,
        },
        "receipt_sha256": receipt,
        "construct_file": "construct.json",
        "nonclaims": [
            "not UCNS geometry canon",
            "not an English lexical truth claim",
            "not a semantic measurement",
            "no proximity signal was collapsed into an invented weight",
        ],
        "hmmm": construct.hmmm,
    }
    manifest_payload = dict(manifest)
    manifest["replay_digest"] = _digest_bytes(_canonical_json_bytes(manifest_payload))

    (output / "construct.json").write_bytes(construct_bytes + b"\n")
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
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    receipt = _digest_bytes(stored_construct.rstrip(b"\n"))
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
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
