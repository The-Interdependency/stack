"""Full-corpus English Gonol definition re-affixiation run (experimental, v0).

Runs the complete pinned OEWN 2025 corpus through English Gonol Construction
while reusing every already-closed word gonol. This runner is not the earlier
1-7 hash-carrier sweep; that sweep remains unchanged as a control experiment
and supplies no placement rules here.

Boundary contract implemented by this runner
--------------------------------------------
- Do not sample: every sense/definition in the corpus is processed.
- Do not hash-place: gonol identity comes from exact source identities, never
  from a carrier/hash placement. No carrier or angle cell exists in this run.
- Do not stop on collisions: there is no collision concept in this run.
- Do not rebuild lexical identity: each unique single-token surface is closed
  exactly once and reused everywhere it appears.
- Do not invent semantic axes or assign meanings to orthogonal directions.
- If exact UCNS orthogonal-affixiation geometry is unresolved, implement no
  substitute: the run closes every definition gonol from its already-closed
  constituent word gonols (existing authority) and records each requested
  orthogonal affixiation step with ``geometry_state = hmmm``.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, replace
import hashlib
import json
import multiprocessing
from pathlib import Path
import pickle
from typing import Any, Mapping, Sequence

from english_gonol.gonol import (
    CONSTRUCTOR_ID,
    CONSTRUCTOR_VERSION,
    PINNED_PUBLIC_GONOL_SHA256,
    ClosedGonol,
    construct_gonol,
)
from english_gonol.language.relational_bridge import (
    UCNS_RELATIONAL_COMMIT,
    UCNS_RELATIONAL_MODULE_SHA256,
)
from english_gonol.language.source import (
    OEWN_COMMIT,
    OEWN_REPOSITORY,
    OEWN_TAG,
    WordnetSnapshot,
    load_oewn_2025,
)

SCHEMA = "english-gonol.oewn-orthogonal-affixiation"
VERSION = "0.1.0"
GEOMETRY_STATE = "hmmm"
GEOMETRY_REASON = (
    "exact UCNS orthogonal-affixiation geometry is unresolved; "
    "no substitute placement or invented orthogonal axis is implemented"
)

_WORD_SOURCE_PREFIX = "oewn:surface"
_LEMMA_SOURCE_PREFIX = "oewn:lemma-composition"
_DEFINITION_SOURCE_PREFIX = "oewn:def"
_SENSE_RELATION_PREFIX = "oewn:sense"


@dataclass(frozen=True, slots=True)
class WordRecord:
    type: str
    surface: str
    source_id: str
    atomic_id: str
    receipt_digest: str


@dataclass(frozen=True, slots=True)
class LemmaCompositionRecord:
    type: str
    lemma: str
    part_of_speech: str
    source_id: str
    relation: str
    constituent_source_ids: tuple[str, ...]
    atomic_id: str
    receipt_digest: str


@dataclass(frozen=True, slots=True)
class DefinitionRecord:
    type: str
    sense_id: str
    synset_id: str
    word_source_id: str
    definition_source_id: str
    order: int
    relation: str
    definition_text: str
    constituent_source_ids: tuple[str, ...]
    atomic_id: str
    receipt_digest: str


@dataclass(frozen=True, slots=True)
class AffixiationRecord:
    type: str
    word_source_id: str
    sense_id: str
    definition_source_id: str
    order: int
    orthogonal_to: str
    geometry_state: str
    reason: str


def _single_token(surface: str) -> bool:
    return bool(surface) and not any(character.isspace() for character in surface)


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def _digest_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


class GonolAffixiationRunError(RuntimeError):
    pass


def collect_surfaces(snapshot: WordnetSnapshot) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Return ``(single_token_surfaces, multiword_surfaces)`` in sorted order."""

    surfaces: set[str] = set()
    for record in snapshot.lexemes:
        surfaces.add(record.lemma)
        surfaces.update(record.lemma.split())
        surfaces.update(record.forms)
        for form in record.forms:
            surfaces.update(form.split())
    for synset in snapshot.synsets:
        for definition in synset.definitions:
            surfaces.update(definition.split())
    single = tuple(sorted(surface for surface in surfaces if _single_token(surface)))
    multi = tuple(sorted(surfaces - set(single)))
    return single, multi


def build_word_registry(
    surfaces: Sequence[str],
) -> tuple[dict[str, ClosedGonol], tuple[WordRecord, ...]]:
    """Close each surface exactly once and return the shared word registry."""

    registry: dict[str, ClosedGonol] = {}
    records: list[WordRecord] = []
    for surface in surfaces:
        if not _single_token(surface):
            raise GonolAffixiationRunError(f"word surface is not single-token: {surface!r}")
        source_id = f"{_WORD_SOURCE_PREFIX}:{surface}"
        receipt = construct_gonol(scale="word", source=surface, source_id=source_id)
        registry[surface] = receipt.gonol
        records.append(
            WordRecord(
                type="word",
                surface=surface,
                source_id=source_id,
                atomic_id=receipt.gonol.atomic_id,
                receipt_digest=receipt.receipt_digest,
            )
        )
    return registry, tuple(records)


def _lemma_gonol(
    lemma: str,
    part_of_speech: str,
    registry: Mapping[str, ClosedGonol],
) -> tuple[ClosedGonol, str, tuple[str, ...]]:
    """Return the lemma's gonol and its source identity.

    Single-token lemmas reuse the corpus word gonol directly. Multiword lemmas
    are composed from their ordered constituent word gonols through the
    existing recursive scale; the composition is recorded, not a redesign.
    """

    if _single_token(lemma):
        gonol = registry[lemma]
        return gonol, f"{_WORD_SOURCE_PREFIX}:{lemma}", (f"{_WORD_SOURCE_PREFIX}:{lemma}",)

    tokens = tuple(lemma.split())
    source_id = f"{_LEMMA_SOURCE_PREFIX}:{lemma}:{part_of_speech}"
    relation = f"oewn:lemma:{lemma}:{part_of_speech}"
    receipt = construct_gonol(
        scale="recursive",
        participants=tuple(registry[token] for token in tokens),
        relation=relation,
        source_id=source_id,
    )
    return receipt.gonol, source_id, tuple(f"{_WORD_SOURCE_PREFIX}:{token}" for token in tokens)


def build_lemma_gonols(
    snapshot: WordnetSnapshot,
    registry: Mapping[str, ClosedGonol],
) -> dict[tuple[str, str], tuple[ClosedGonol, str, tuple[str, ...]]]:
    """Compose or reuse one gonol per (lemma, part_of_speech) that owns senses."""

    result: dict[tuple[str, str], tuple[ClosedGonol, str, tuple[str, ...]]] = {}
    for lexeme in snapshot.lexemes:
        if not lexeme.senses:
            continue
        key = (lexeme.lemma, lexeme.part_of_speech)
        if key in result:
            continue
        result[key] = _lemma_gonol(lexeme.lemma, lexeme.part_of_speech, registry)
    return result


def _definition_tasks(
    snapshot: WordnetSnapshot,
    lemma_gonols: Mapping[tuple[str, str], tuple[ClosedGonol, str, tuple[str, ...]]],
) -> list[dict[str, Any]]:
    """Flatten every sense/definition into deterministic construction tasks."""

    synset_map = snapshot.synset_map()
    tasks: list[dict[str, Any]] = []
    for lexeme in snapshot.lexemes:
        _gonol, word_source_id, _lemma_constituents = lemma_gonols[
            (lexeme.lemma, lexeme.part_of_speech)
        ]
        for sense in lexeme.senses:
            synset = synset_map[sense.synset_id]
            for definition_index, definition_text in enumerate(synset.definitions):
                tasks.append(
                    {
                        "sense_id": sense.sense_id,
                        "synset_id": sense.synset_id,
                        "word_source_id": word_source_id,
                        "definition_index": definition_index,
                        "definition_text": definition_text,
                        "tokens": tuple(definition_text.split()),
                    }
                )
    tasks.sort(key=lambda item: (item["word_source_id"], item["sense_id"], item["definition_index"]))
    return tasks


def _build_definition(
    task: Mapping[str, Any],
    registry: Mapping[str, ClosedGonol],
) -> tuple[DefinitionRecord, tuple[str, ...]]:
    sense_id = str(task["sense_id"])
    definition_index = int(task["definition_index"])
    relation = f"{_SENSE_RELATION_PREFIX}:{sense_id}"
    definition_source_id = f"{_DEFINITION_SOURCE_PREFIX}:{sense_id}:{definition_index}"
    constituent_source_ids = tuple(f"{_WORD_SOURCE_PREFIX}:{token}" for token in task["tokens"])
    participants = tuple(registry[token] for token in task["tokens"])
    receipt = construct_gonol(
        scale="definition",
        participants=participants,
        relation=relation,
        source_id=definition_source_id,
    )
    record = DefinitionRecord(
        type="definition",
        sense_id=sense_id,
        synset_id=str(task["synset_id"]),
        word_source_id=str(task["word_source_id"]),
        definition_source_id=definition_source_id,
        order=0,  # per-word order is assigned after grouping in the worker
        relation=relation,
        definition_text=str(task["definition_text"]),
        constituent_source_ids=constituent_source_ids,
        atomic_id=receipt.gonol.atomic_id,
        receipt_digest=receipt.receipt_digest,
    )
    return record, constituent_source_ids


def _affixiation_records(
    word_source_id: str,
    definitions: Sequence[DefinitionRecord],
) -> tuple[AffixiationRecord, ...]:
    records: list[AffixiationRecord] = []
    previous = word_source_id
    for index, definition in enumerate(definitions, start=1):
        records.append(
            AffixiationRecord(
                type="affixiation",
                word_source_id=word_source_id,
                sense_id=definition.sense_id,
                definition_source_id=definition.definition_source_id,
                order=index,
                orthogonal_to=previous,
                geometry_state=GEOMETRY_STATE,
                reason=GEOMETRY_REASON,
            )
        )
        previous = definition.definition_source_id
    return tuple(records)


def _worker_process_tasks(
    tasks: Sequence[dict[str, Any]],
    output_path: str,
) -> dict[str, int]:
    """Build definition gonols for a task slice and stream records to JSONL."""

    # The shared word registry is inherited from the parent via fork.
    registry = _WORKER_REGISTRY
    if registry is None:
        raise GonolAffixiationRunError("worker registry is unavailable")

    built: list[DefinitionRecord] = []
    for task in tasks:
        record, _constituents = _build_definition(task, registry)
        built.append(record)

    # Group per owning word, assign the ordered affixiation sequence, and only
    # then write records so each definition carries its final per-word order.
    grouped: dict[str, list[DefinitionRecord]] = {}
    for record in built:
        grouped.setdefault(record.word_source_id, []).append(record)

    definition_count = 0
    affixiation_count = 0
    with open(output_path, "w", encoding="utf-8") as handle:
        for word_source_id, records in grouped.items():
            for index, record in enumerate(records, start=1):
                record = replace(record, order=index)
                handle.write(
                    json.dumps(asdict(record), ensure_ascii=False, sort_keys=True) + "\n"
                )
                definition_count += 1
            for affixiation in _affixiation_records(word_source_id, records):
                handle.write(
                    json.dumps(asdict(affixiation), ensure_ascii=False, sort_keys=True) + "\n"
                )
                affixiation_count += 1
    return {
        "definitions": definition_count,
        "affixiations": affixiation_count,
    }


_WORKER_REGISTRY: dict[str, ClosedGonol] | None = None


def _worker_initializer(registry: Mapping[str, ClosedGonol]) -> None:
    global _WORKER_REGISTRY
    _WORKER_REGISTRY = dict(registry)


def run(
    snapshot: WordnetSnapshot,
    *,
    out_dir: str | Path,
    workers: int = 1,
) -> dict[str, Any]:
    """Run the complete corpus and persist the construction records."""

    output = Path(out_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise GonolAffixiationRunError(f"output directory must be empty: {output}")

    single_surfaces, multiword_surfaces = collect_surfaces(snapshot)
    registry, word_records = build_word_registry(single_surfaces)

    # Compose or reuse one gonol per (lemma, part_of_speech) that owns senses.
    lemma_gonols = build_lemma_gonols(snapshot, registry)

    # Record multiword lemma compositions (single-token lemmas are word gonols).
    lemma_compositions: list[LemmaCompositionRecord] = []
    for (lemma, part_of_speech), (gonol, source_id, constituents) in sorted(lemma_gonols.items()):
        if not _single_token(lemma):
            lemma_compositions.append(
                LemmaCompositionRecord(
                    type="lemma",
                    lemma=lemma,
                    part_of_speech=part_of_speech,
                    source_id=source_id,
                    relation=f"oewn:lemma:{lemma}:{part_of_speech}",
                    constituent_source_ids=constituents,
                    atomic_id=gonol.atomic_id,
                    receipt_digest=gonol.receipt_digest,
                )
            )

    tasks = _definition_tasks(snapshot, lemma_gonols)

    worker_count = max(1, min(workers, multiprocessing.cpu_count()))
    if worker_count == 1:
        partial_paths = [output / "records.jsonl"]
        _worker_initializer(registry)
        summary = _worker_process_tasks(tasks, str(partial_paths[0]))
    else:
        chunk_size = (len(tasks) + worker_count - 1) // worker_count
        partial_paths = [output / f"records.worker-{index}.jsonl" for index in range(worker_count)]
        context = multiprocessing.get_context("fork")
        with context.Pool(
            processes=worker_count,
            initializer=_worker_initializer,
            initargs=(registry,),
        ) as pool:
            results = [
                pool.apply_async(
                    _worker_process_tasks,
                    (tasks[start : start + chunk_size], str(partial_paths[index])),
                )
                for index, start in enumerate(range(0, len(tasks), chunk_size))
            ]
            summaries = [result.get() for result in results]
        summary = {
            "definitions": sum(item["definitions"] for item in summaries),
            "affixiations": sum(item["affixiations"] for item in summaries),
        }

    # Merge word + lemma + worker partial records into one records file.
    records_path = output / "records.jsonl"
    if worker_count > 1:
        with open(records_path, "w", encoding="utf-8") as merged:
            for record in word_records:
                merged.write(
                    json.dumps(asdict(record), ensure_ascii=False, sort_keys=True) + "\n"
                )
            for record in lemma_compositions:
                merged.write(
                    json.dumps(asdict(record), ensure_ascii=False, sort_keys=True) + "\n"
                )
            for partial in partial_paths:
                merged.write(partial.read_text(encoding="utf-8"))
                partial.unlink()
    else:
        # Single worker wrote only definitions/affixiations; prepend word and
        # lemma records to the same file in canonical order.
        existing = records_path.read_text(encoding="utf-8")
        with open(records_path, "w", encoding="utf-8") as merged:
            for record in word_records:
                merged.write(
                    json.dumps(asdict(record), ensure_ascii=False, sort_keys=True) + "\n"
                )
            for record in lemma_compositions:
                merged.write(
                    json.dumps(asdict(record), ensure_ascii=False, sort_keys=True) + "\n"
                )
            merged.write(existing)

    records_sha256 = _digest_bytes(records_path.read_bytes())

    manifest_payload: dict[str, Any] = {
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
        "constructor": {
            "constructor_id": CONSTRUCTOR_ID,
            "constructor_version": CONSTRUCTOR_VERSION,
            "pinned_public_gonol_sha256": PINNED_PUBLIC_GONOL_SHA256,
        },
        "ucns": {
            "ucns_relational_commit": UCNS_RELATIONAL_COMMIT,
            "ucns_relational_module_sha256": UCNS_RELATIONAL_MODULE_SHA256,
            "orthogonal_affixiation_geometry": GEOMETRY_STATE,
            "orthogonal_affixiation_reason": GEOMETRY_REASON,
        },
        "counts": {
            "single_token_surfaces": len(single_surfaces),
            "multiword_surfaces": len(multiword_surfaces),
            "word_gonols": len(word_records),
            "lemma_compositions": len(lemma_compositions),
            "definition_gonols": summary["definitions"],
            "affixiation_records": summary["affixiations"],
        },
        "records_file": "records.jsonl",
        "records_sha256": records_sha256,
        "nonclaims": [
            "no orthogonal affixiation geometry is invented",
            "no carrier or bucket placement exists in this run",
            "not UCNS geometry canon",
            "not an English lexical truth claim",
            "not a measurement of semantic quality",
        ],
        "hmmm": [
            "exact UCNS orthogonal-affixiation geometry remains unresolved",
            "affixiation records expose the unresolved geometry boundary without a substitute",
            "emergent-relationship analysis is deferred until after construction",
        ],
    }
    manifest_payload["replay_digest"] = _digest_bytes(_canonical_json_bytes(manifest_payload))
    manifest_path = output / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return manifest_payload


def verify_replay(out_dir: str | Path) -> dict[str, Any]:
    """Verify a completed run byte-for-byte from its persisted records."""

    output = Path(out_dir).resolve()
    manifest_path = output / "manifest.json"
    records_path = output / "records.jsonl"
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    if json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8") + b"\n" != manifest_bytes:
        raise GonolAffixiationRunError("manifest is not canonical")
    if manifest.get("records_file") != "records.jsonl":
        raise GonolAffixiationRunError("records file identity mismatch")
    records_sha256 = _digest_bytes(records_path.read_bytes())
    if records_sha256 != manifest.get("records_sha256"):
        raise GonolAffixiationRunError("records file digest mismatch")
    expected_payload = dict(manifest)
    expected_payload.pop("replay_digest", None)
    replay_digest = _digest_bytes(_canonical_json_bytes(expected_payload))
    if replay_digest != manifest.get("replay_digest"):
        raise GonolAffixiationRunError("replay digest mismatch")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=str, help="OEWN src/yaml checkout path")
    parser.add_argument("--snapshot-pkl", type=str, help="pickled WordnetSnapshot path")
    parser.add_argument("--out-dir", type=str, required=True)
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()

    if args.snapshot_pkl:
        with open(args.snapshot_pkl, "rb") as handle:
            snapshot = pickle.load(handle)
    elif args.source_root:
        snapshot = load_oewn_2025(args.source_root)
    else:
        parser.error("one of --source-root or --snapshot-pkl is required")

    manifest = run(snapshot, out_dir=args.out_dir, workers=args.workers)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
