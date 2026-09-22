# ratios: loc_comments=206:35 imports_exports=15:6 calls_definitions=90:6
"""Exhaustive four-view audit; run native and independent modes over all words.

Usage from Stack with PYTHONPATH=research/english-gonol:
python -m english_gonol.full_view_audit --state-dir /path/to/construct \
    --ucns-source-root /path/to/pinned/ucns --engine native --output /tmp/native.json
Repeat with --engine independent. Compare the evidence objects, not timings.
FULL_VIEW_AUDIT.json freezes scope, source identities, and interpretation rules.
"""

# === MODULE_BUILD ===
# id: english_full_view_audit
#   module_name: full_view_audit
#   module_kind: audit
#   summary: exhaustive native execution, every view subset, exact per-word reconstruction, and address-renumbering controls
#   owner: The-Interdependency/stack
#   public_surface: run, metrics, CLI
#   storage_boundary: exact source/corpus reads and optional aggregate receipt write
#   network_boundary: none
#   user_data_boundary: pinned public corpus only
#   tests: tests.test_full_view_audit; complete native and independent execution receipts
#   rollout: explicitly invoked full-corpus audit
#   rollback: revert runner and registration; preserve sealed receipts
#   unresolved: utility for inference requires its own workload and acceptance criterion
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: full_views_scope_is_complete
#   given: the exact source and corpus declared by the frozen protocol
#   then: process every word with no limit or sampling switch, verify source/database identities and bind an ordered observation digest
#   class: evidence
# id: full_views_counts_and_controls
#   given: all four views for every word
#   then: count all fifteen nonempty subsets and all declared renumberings with explicit repeated-record, collision-pair, singleton and missingness meanings
#   class: correctness
# === END CONTRACTS ===

import argparse
from collections import Counter, defaultdict
import hashlib
import importlib
from itertools import combinations
import json
from math import gcd
from pathlib import Path
import platform
import resource
import sqlite3
import sys
import time
from types import ModuleType

from .view_replay import Corpus, VIEW_NAMES, canonical, freeze_views, record_from_views

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
STACK = WORKSPACE.parents[1]


def file_digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify_sources(root, sources):
    for source in sources:
        raw = (root / source["path"]).read_bytes()
        observed = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        if observed != source["blob_sha"]:
            raise ValueError("source Git blob mismatch: " + source["path"])


def load_native(ucns_root):
    """Load only verified dependency files; bind motion once for this run."""
    if any(name == "ucns" or name.startswith("ucns.") for name in sys.modules):
        raise ValueError("run the audit in a fresh interpreter without ambient UCNS imports")
    package = ModuleType("ucns")
    package.__path__ = [str(ucns_root / "src/ucns")]
    sys.modules["ucns"] = package
    motion = importlib.import_module("ucns.motion")
    geometry = importlib.import_module("english_gonol.hyperspace_geometry")
    views = importlib.import_module("english_gonol.hyperspace_views")
    # Exact source hashes are verified before imports, once per complete run.
    # This replaces repeated file hashing/Git ancestry queries, not computation.
    original_loader = geometry._load_verified_motion
    geometry._load_verified_motion = lambda root: motion.build_motion
    return views.word_views, geometry, original_loader


def metrics(counts):
    n = sum(counts.values())
    return {
        "word_count": n, "distinct_values": len(counts),
        "repeated_records": n - len(counts),
        "singleton_words": sum(count == 1 for count in counts.values()),
        "ambiguous_words": sum(count for count in counts.values() if count > 1),
        "collision_pairs": sum(count * (count - 1) // 2 for count in counts.values()),
        "largest_bucket": max(counts.values(), default=0),
    }


def run(state_dir, ucns_root, engine):
    started = time.monotonic()
    protocol_bytes = (WORKSPACE / "FULL_VIEW_AUDIT.json").read_bytes()
    protocol = json.loads(protocol_bytes)
    verify_sources(STACK, protocol["stack"]["files"])
    verify_sources(ucns_root, protocol["ucns"]["files"])
    database = state_dir / "construct.db"
    database_sha = file_digest(database)
    if database_sha != protocol["corpus"]["database_sha256"]:
        raise ValueError("corpus database hash mismatch")
    manifest = json.loads((state_dir / "manifest.json").read_text())
    if manifest != json.loads((WORKSPACE / "experiments/full-construct-v2/manifest.json").read_text()):
        raise ValueError("corpus manifest differs from the committed full construct")
    graph = json.loads((STACK / "stack-manifest.json").read_text())
    graph_digest = hashlib.sha256(canonical({
        key: graph[key] for key in ("repositories", "research_participants", "boundaries")
    })).hexdigest()
    if graph_digest != graph["work_graph_sha256"]:
        raise ValueError("work graph digest mismatch")
    if graph_digest != protocol["work_graph_sha256"]:
        raise ValueError("work graph differs from the frozen protocol")
    connection = sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)
    native = geometry = original_loader = None
    try:
        if connection.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
            raise ValueError("SQLite integrity failure")
        actual_counts = {table: connection.execute("SELECT count(*) FROM " + table).fetchone()[0]
                         for table in protocol["corpus"]["counts"]}
        if actual_counts != protocol["corpus"]["counts"]:
            raise ValueError("corpus row counts differ from the declared complete scope")
        corpus = Corpus(connection)
        n = len(corpus.words)
        if [word_id for word_id, _ in corpus.words] != list(range(1, n + 1)):
            raise ValueError("renumbering controls require the declared contiguous word IDs")
        if [row[0] for row in corpus.characters] != list(range(1, len(corpus.characters) + 1)):
            raise ValueError("renumbering controls require contiguous glyph IDs")
        if gcd(157, n) != 1:
            raise ValueError("declared affine word-ID control is not bijective")
        if engine == "native":
            native, geometry, original_loader = load_native(ucns_root)
        elif engine != "independent":
            raise ValueError("unknown execution engine")
        subsets = [indices for size in range(1, 5) for indices in combinations(range(4), size)]
        counts = {indices: Counter() for indices in subsets}
        controls = {name: {"views": [Counter() for _ in range(4)], "synthesis": Counter(),
                           "joint": Counter(), "changed": [0] * 4}
                    for name in ("word_id_reverse", "word_id_affine_157", "glyph_id_reverse")}
        observations = hashlib.sha256()
        absent = 0
        bag_counts = Counter()
        bag_states = defaultdict(set)
        for ordinal, (word_id, surface) in enumerate(corpus.words, 1):
            independent_views = corpus.views(word_id)
            expected = record_from_views(word_id, independent_views)
            record = native(connection, word_id, ucns_root) if native else expected
            if record != expected:
                raise ValueError(f"native/independent disagreement at word {word_id}")
            observations.update(canonical(record) + b"\n")
            views = tuple(record["views"][name] for name in VIEW_NAMES)
            key = freeze_views(views)
            absent += views[0] is None
            for indices, counter in counts.items():
                counter[tuple(key[i] for i in indices)] += 1
            bag = tuple(sorted(char for _, char in corpus.glyphs[word_id]))
            bag_counts[bag] += 1
            bag_states[bag].add(key[1])
            for name, control in controls.items():
                if name == "glyph_id_reverse":
                    changed_views = corpus.views(word_id, reverse_glyph_ids=True, overlap=views[0])
                else:
                    renamed_id = n + 1 - word_id if name == "word_id_reverse" else 1 + (157 * (word_id - 1)) % n
                    deck = renamed_id // 157
                    residue = views[2]["residue"]
                    changed_views = (views[0], views[1],
                                     {"deck": deck, "residue": residue, "lift": 157 * deck + residue}, views[3])
                changed_key = freeze_views(changed_views)
                for i in range(4):
                    control["views"][i][changed_key[i]] += 1
                    control["changed"][i] += key[i] != changed_key[i]
                control["synthesis"][changed_key] += 1
                control["joint"][(key, changed_key)] += 1
            if ordinal % 10000 == 0 or ordinal == n:
                print(f"{engine}: {ordinal}/{n} words", file=sys.stderr, flush=True)
        primary = metrics(counts[(0, 1, 2, 3)])
        control_results = {}
        for name, control in controls.items():
            combined = metrics(control["synthesis"])
            shared_pairs = metrics(control["joint"])["collision_pairs"]
            control_results[name] = {
                "changed_word_counts_by_view": dict(zip(VIEW_NAMES, control["changed"])),
                "views": {name: metrics(counter) for name, counter in zip(VIEW_NAMES, control["views"])},
                "synthesis": combined,
                "baseline_collision_pairs_split": primary["collision_pairs"] - shared_pairs,
                "new_collision_pairs_joined": combined["collision_pairs"] - shared_pairs,
            }
        subset_results = {"+".join(str(i + 1) for i in indices): metrics(counter)
                          for indices, counter in counts.items()}
        legacy_names = VIEW_NAMES + ("synthesis",)
        legacy_keys = ("1", "2", "3", "4", "1+2+3+4")
        legacy_metrics = dict(zip(legacy_names, (subset_results[key] for key in legacy_keys)))
        ranking = sorted(legacy_metrics, key=lambda name: (legacy_metrics[name]["distinct_values"],
                         -legacy_metrics[name]["repeated_records"]), reverse=True)
        legacy = {
            "schema": "english-gonol.hyperspace-views", "version": "0.1.0", "word_count": n,
            "distinct_values": {name: value["distinct_values"] for name, value in legacy_metrics.items()},
            "collisions": {name: value["repeated_records"] for name, value in legacy_metrics.items()},
            "ranking_by_distinctness": [{"view": name, "distinct": legacy_metrics[name]["distinct_values"],
                                         "collisions": legacy_metrics[name]["repeated_records"]} for name in ranking],
            "hmmm": "one doctor or four? The corpus adjudicates which views merit retainment or whether the differential synthesis is most useful; this report ranks, it does not select",
        }
        legacy["receipt_sha256"] = hashlib.sha256(canonical(legacy)).hexdigest()
        evidence = {
            "schema": "english-gonol.full-view-audit", "version": "1.0.0",
            "standing": "COMPLETE_SCOPE", "sampling": False, "prefix": False,
            "word_count": n, "source_exhausted": True,
            "protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
            "work_graph_sha256": graph_digest,
            "database_sha256": database_sha, "corpus_counts": actual_counts,
            "corpus_manifest_receipt": manifest["receipt_sha256"],
            "runner_sha256": {p.name: file_digest(p) for p in (Path(__file__), HERE / "view_replay.py")},
            "ordered_observation_sha256": observations.hexdigest(),
            "view1_missing": absent, "view1_available": n - absent,
            "subsets": subset_results, "renumbering_controls": control_results,
            "same_glyph_multiset": {
                "multiword_groups": sum(count > 1 for count in bag_counts.values()),
                "word_count_in_multiword_groups": sum(count for count in bag_counts.values() if count > 1),
                "multiword_groups_with_different_view2": sum(bag_counts[bag] > 1 and len(states) > 1 for bag, states in bag_states.items()),
            },
            "unique_word_address_baseline": {"distinct_values": n, "repeated_records": 0},
            "legacy_report": legacy,
            "selected": [], "hmmm": protocol["hmmm"],
        }
        evidence["receipt_sha256"] = hashlib.sha256(canonical(evidence)).hexdigest()
    finally:
        connection.close()
        if geometry is not None:
            geometry._load_verified_motion = original_loader
    if file_digest(database) != database_sha:
        raise ValueError("database changed during execution")
    return {"evidence": evidence, "execution": {
        "engine": engine, "python": platform.python_version(),
        "native_records_compared": n if engine == "native" else 0,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--ucns-source-root", type=Path, required=True)
    parser.add_argument("--engine", choices=("native", "independent"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.state_dir, args.ucns_source_root, args.engine)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["execution"], sort_keys=True))


if __name__ == "__main__":
    main()
# ratios: loc_comments=206:35 imports_exports=15:6 calls_definitions=90:6
