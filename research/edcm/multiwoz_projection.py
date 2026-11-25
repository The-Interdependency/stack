# ratios: loc_comments=606:35 imports_exports=16:15 calls_definitions=226:23
"""Full admitted MultiWOZ projection; aggregate evidence, no raw corpus publication.

Run from Stack: python -m research.edcm.multiwoz_projection --archive /path/MULTIWOZ2.1.zip
  --checkpoint /path/to/checkpoint.jsonl --output /path/to/report.json --workers 8
"""

# === MODULE_BUILD ===
# id: stack_edcm_multiwoz_projection
#   module_name: multiwoz_projection
#   module_kind: instrument
#   summary: resolves all eleven native origin directions across the admitted dialogue corpus and evaluates frozen booking-outcome scores
#   owner: The-Interdependency/stack
#   public_surface: CLI aggregate experiment
#   auth_boundary: none
#   storage_boundary: explicit aggregate and non-text checkpoint paths
#   network_boundary: none
#   user_data_boundary: admitted public MultiWOZ source; no raw text publication
#   admin_only: false
#   tests: research/edcm/tests/test_multiwoz_projection.py
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: multiwoz_native_exact_display
#   given: the released UCHC graph and verified native UCNS Point expressions
#   then: batched evaluation preserves native placement, additive, recursive norm and addressed numeric values
#   class: correctness
# id: multiwoz_before_response_only
#   given: an admitted source-native labelled booking event
#   then: every candidate score uses only exact preceding source turns; test labels do not fit origins or calibration
#   class: correctness
# id: multiwoz_source_and_checkpoint_reconciliation
#   given: the exact admitted archive, frozen protocol and source-bound checkpoint
#   then: all source dialogues, turns, rounds and outcome counts reconcile before complete aggregate output
#   class: provenance
# === END CONTRACTS ===
from __future__ import annotations
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import io
import json
import math
import multiprocessing as mp
from pathlib import Path
import re
import time

import numpy as np
from edcm.corpora import multiwoz21 as corpus
from edcm.corpora import multiwoz21_booking_holdout as holdout
from research.edcm import epicycle_projection as e

WORKSPACE = Path(__file__).resolve().parent
PROTOCOL = WORKSPACE / "MULTIWOZ_PROJECTION_PROTOCOL.json"
h = e.geometry
P_INDEX = e.AXES.index("P")
NATIVE = None
SUPPORT = None
BASIS = None
INVERSE = None
CANON = None
SEPARATOR = None


def initialize():
    global NATIVE, SUPPORT, BASIS, INVERSE, CANON, SEPARATOR
    identity, _, _, _, origins = e.prepared_origins()
    # The release verifies the exact UCNS sources before loading these class
    # identities. The numeric cache below consumes the native Point expressions.
    NATIVE = h._native(None).attachment_stack
    fields = [origins[axis]["recursive"] for axis in e.AXES]
    SUPPORT = sorted(set().union(*(field.keys() for field in fields)))
    matrix = np.array(
        [
            [
                v
                for key in SUPPORT
                for z in [field[key].value if key in field else 0j]
                for v in (z.real, z.imag)
            ]
            for field in fields
        ]
    ).T
    BASIS = matrix / np.linalg.norm(matrix, axis=0)
    singular = np.linalg.svd(BASIS, compute_uv=False)
    e.require(
        int(np.sum(singular > singular[0] * 1e-10)) == len(e.AXES),
        "origin field lost rank",
    )
    INVERSE = np.linalg.pinv(BASIS, rcond=1e-10)
    CANON = holdout.CanonLoader()
    SEPARATOR = h.construct_text("\n", source="edcm:observation-separator")
    return identity["identity"], {
        "rank": len(e.AXES),
        "dimensions": len(SUPPORT) * 2,
        "singular_values": singular.tolist(),
        "condition_number": float(singular[0] / singular[-1]),
        "axis_order": list(e.AXES),
    }


@lru_cache(maxsize=4096)
def term(text):
    return h.construct_text(text, source="edcm:observation-member")


def close_round(text):
    return h.construct_sequence(
        tuple(term(part) for part in re.findall(r"\s+|\S+", text)),
        source="edcm:observation-round",
    )


def close_prefix(parts):
    return h.construct_sequence(tuple(parts), source="edcm:observation-prefix")


class DisplayCache:
    """Batch evaluation equivalent to UCNS display on the native exact points."""

    def __init__(self):
        self.points, self.units, self.values, self.norms = {}, {}, {}, {}

    def endpoint(self, node):
        if node.receipt not in self.points:
            self.points[node.receipt] = NATIVE.Point(
                tuple((ray.heading, ray.radius) for ray in node.rays)
            )
        return self.points[node.receipt]

    def unit(self, node):
        if node.receipt not in self.units:
            value = self.evaluate(
                self.endpoint(node).scaled(1 / max(ray.radius for ray in node.rays))
            )
            if abs(value) == 0:
                raise ArithmeticError("DISPLAY_ZERO_DIRECTION")
            self.units[node.receipt] = value / abs(value)
        return self.units[node.receipt]

    def evaluate(self, point):
        terms = []
        for direction, coefficient in point.terms:
            value, turn = float(coefficient), float(direction.turn)
            if (
                value == 0
                or not math.isfinite(value)
                or direction.turn
                and turn in (0, 1)
            ):
                raise ArithmeticError("DISPLAY_RANGE")
            angle = math.tau * turn
            factor = complex(math.cos(angle), math.sin(angle))
            for child, power in direction.endpoints:
                factor *= self.unit(child) ** power
            terms.append(value * factor)
        result = complex(
            math.fsum(v.real for v in terms), math.fsum(v.imag for v in terms)
        )
        if (
            not math.isfinite(result.real)
            or not math.isfinite(result.imag)
            or terms
            and result == 0
        ):
            raise ArithmeticError("DISPLAY_RANGE_OR_COLLAPSE")
        return result

    def value(self, node, role, index=0):
        key = (node.receipt, role, index)
        if key not in self.values:
            point = (
                node.rays[-index].vector
                if role == "ray"
                else (
                    self.endpoint(node) if role == "placed" else node.additive_resultant
                )
            )
            self.values[key] = self.evaluate(point)
        return self.values[key]

    def norm_squared(self, node):
        if node.receipt not in self.norms:
            values = [
                abs(self.value(node, role)) ** 2 for role in ("placed", "additive")
            ]
            values.extend(float(ray.radius) ** 2 for ray in node.rays)
            values.extend(
                self.norm_squared(part.interior)
                for part in node.participants
                if isinstance(part, NATIVE.Closed)
            )
            self.norms[node.receipt] = math.fsum(values)
        return self.norms[node.receipt]

    def addressed(self, root, *, verify=False):
        values, present = [], 0
        for path, role in SUPPORT:
            node = root
            for depth in path[:-1] if role == "ray" else path:
                if depth > len(node.participants) or not isinstance(
                    node.participants[-depth], NATIVE.Closed
                ):
                    node = None
                    break
                node = node.participants[-depth].interior
            if node is None or (role == "ray" and path[-1] > len(node.rays)):
                value = 0j
            else:
                index = path[-1] if role == "ray" else 0
                value = self.value(node, role, index)
                present += 1
                if verify:
                    point = (
                        node.rays[-index].vector
                        if role == "ray"
                        else (
                            node.endpoint
                            if role == "placed"
                            else node.additive_resultant
                        )
                    )
                    e.require(
                        value == NATIVE.display(point), "cached native display differs"
                    )
                    if role == "placed":
                        e.require(
                            self.endpoint(node).record() == node.endpoint.record(),
                            "cached native endpoint differs",
                        )
            values.extend((value.real, value.imag))
        return np.array(values), present

    def measure(self, root):
        x, present = self.addressed(root)
        coordinates = INVERSE @ x
        projected = BASIS @ coordinates
        norm = self.norm_squared(root)
        fraction = float(projected @ projected / norm) if norm else None
        e.require(
            fraction is None or 0 <= fraction <= 1 + 1e-10,
            "projection norm exceeds full field",
        )
        identity = e.digest(
            [
                root.receipt,
                self.endpoint(root).record(),
                root.additive_resultant.record(),
            ]
        )
        return {
            "coordinates": coordinates.tolist(),
            "energy_fraction": fraction,
            "origin_support_present": present,
            "native_digest": identity,
        }


def replay(obj, raw):
    packet = h.closed_record(obj)
    root = h.replay_closed(packet)
    e.require(
        root.receipt == obj.receipt and "".join(root.recover()) == raw,
        "native source replay differs",
    )
    return root, packet["graph"]["receipt"]


def labelled_lines(texts, *, presentation=False):
    return [
        f"{'USER' if i%2 == 0 else 'SYSTEM'}: "
        + (text.replace("\r", " ").replace("\n", " ") if presentation else text)
        for i, text in enumerate(texts)
    ]


def observe_dialogue(task):
    index, key, partition, source_hash, texts, eligible = task
    lines = labelled_lines(texts)
    rounds = ["\n".join(lines[i : i + 2]) for i in range(0, len(lines), 2)]
    e.require(
        len(texts) > 0 and len(texts) % 2 == 0,
        "source dialogue is not complete paired rounds",
    )
    parts = []
    for raw in rounds:
        if parts:
            parts.append(SEPARATOR)
        parts.append(close_round(raw))
    full, graph_digest = replay(close_prefix(parts), "\n".join(lines))
    members = tuple(p.interior for p in full.participants)
    e.require(len(members) == 2 * len(rounds) - 1, "native round membership differs")
    presented = "\n".join(labelled_lines(texts, presentation=True))
    parsed = e.measurement.parse_transcript(presented, canon=CANON)
    metrics = e.measurement.compute_transcript(parsed, canon=CANON)
    e.require(
        len(parsed.turns) == len(texts)
        and len(metrics) == len(rounds)
        and all(len(r.turns) == 2 for r in parsed.rounds),
        "maintained parser cycle differs",
    )
    e.require(
        [t.speaker for t in parsed.turns]
        == ["USER" if i % 2 == 0 else "SYSTEM" for i in range(len(texts))],
        "maintained parser speaker order differs",
    )
    cache = DisplayCache()
    previous = np.zeros(len(e.AXES))
    rows, prefixes = [], []
    prefix_characters = 0
    for i, raw in enumerate(rounds):
        round_root = members[2 * i]
        prefix = full if i == len(rounds) - 1 else close_prefix(members[: 2 * i + 1])
        e.require(
            "".join(round_root.recover()) == raw
            and "".join(prefix.recover()) == "\n".join(rounds[: i + 1]),
            "round or prefix recovery differs",
        )
        round_measurement, prefix_measurement = cache.measure(
            round_root
        ), cache.measure(prefix)
        current = np.array(prefix_measurement["coordinates"])
        prefix_characters += len(raw) + (1 if i else 0)
        rows.append(
            {
                "round": round_measurement,
                "prefix": prefix_measurement,
                "delta": (current - previous).tolist(),
                "baseline": metrics[i].vector(),
                "prefix_chars": prefix_characters,
                "round_chars": len(raw),
            }
        )
        prefixes.append(current)
        previous = current
    events = []
    for response_index, label in eligible:
        i = (response_index - 1) // 2
        raw = lines[response_index - 1]
        partial, _ = replay(close_round(raw), raw)
        context = close_prefix(members[: 2 * i] + (partial,))
        expected = "\n".join(lines[:response_index])
        e.require(
            "".join(context.recover()) == expected,
            "labelled response or later source entered prefix",
        )
        measure = cache.measure(context)
        before = prefixes[i - 1] if i else np.zeros(len(e.AXES))
        score = holdout._candidate_score(texts[:response_index], canon=CANON)
        events.append(
            {
                "turn": response_index,
                "label": label,
                "context_turns": response_index,
                "native_digest": measure["native_digest"],
                "context_sha256": hashlib.sha256(expected.encode()).hexdigest(),
                "scores": [
                    score,
                    measure["coordinates"][P_INDEX],
                    measure["coordinates"][P_INDEX] - float(before[P_INDEX]),
                    math.log1p(len(expected)),
                ],
            }
        )
    return {
        "index": index,
        "dialogue": e.digest(key),
        "partition": partition,
        "source_sha256": source_hash,
        "turns": len(texts),
        "graph_digest": graph_digest,
        "multiline": sum("\r" in t or "\n" in t for t in texts),
        "rows": rows,
        "events": events,
    }


def source_tasks(archive_path):
    manifest = corpus.load_admission_manifest()
    identity, archive = corpus._archive_identity(archive_path, manifest)
    tasks, seen, ambiguous = [], set(), Counter()
    counts, turns, labels = Counter(), Counter(), Counter()
    with archive:
        test = set(corpus._load_partition_ids(archive, manifest.source["test_member"]))
        validation = set(
            corpus._load_partition_ids(archive, manifest.source["validation_member"])
        )
        e.require(not test.intersection(validation), "overlapping source partitions")
        acts = holdout._load_json_member(archive, "MULTIWOZ2.1/dialogue_acts.json")
        with io.TextIOWrapper(
            archive.open(manifest.source["data_member"]), encoding="utf-8", newline=""
        ) as stream:
            for index, (key, dialogue, source_hash) in enumerate(
                corpus.iter_top_level_object(stream)
            ):
                e.require(
                    key not in seen and isinstance(dialogue.get("log"), list),
                    "invalid or duplicate dialogue",
                )
                seen.add(key)
                partition = holdout._partition_name(key, test, validation)
                texts = tuple(t["text"] for t in dialogue["log"])
                e.require(all(type(t) is str for t in texts), "invalid source turn")
                base = key[:-5] if key.endswith(".json") else key
                mapping = acts.get(base, acts.get(key))
                e.require(isinstance(mapping, dict), "missing dialogue acts")
                events = []
                for source_turn, act in sorted(
                    mapping.items(), key=holdout._source_turn_sort_key
                ):
                    if not isinstance(act, dict):
                        continue
                    outcome = {
                        holdout.POSITIVE_LABEL,
                        holdout.NEGATIVE_LABEL,
                    }.intersection(act)
                    if not outcome:
                        continue
                    if len(outcome) == 2:
                        ambiguous[partition] += 1
                        continue
                    response = 2 * int(source_turn) - 1
                    e.require(
                        0 < response < len(texts), "invalid labelled response mapping"
                    )
                    label = int(holdout.POSITIVE_LABEL in outcome)
                    labels[partition, label] += 1
                    events.append((response, label))
                counts[partition] += 1
                turns[partition] += len(texts)
                tasks.append((index, key, partition, source_hash, texts, tuple(events)))
    normalized_seen = {key[:-5] if key.endswith(".json") else key for key in seen}
    e.require(
        {key[:-5] if key.endswith(".json") else key for key in test | validation}
        <= normalized_seen,
        "partition IDs missing from source",
    )
    protocol = json.loads(PROTOCOL.read_text())
    e.require(
        dict(counts) == protocol["source"]["partitions"]
        and sum(turns.values()) == protocol["source"]["turns"],
        "admitted source counts differ",
    )
    for name, inventory in protocol["booking_outcome"]["event_inventory"].items():
        e.require(
            (labels[name, 1], labels[name, 0], ambiguous[name])
            == (inventory["positive"], inventory["negative"], inventory["ambiguous"]),
            "booking event inventory differs",
        )
    return tasks, {
        "archive_sha256": identity["sha256"],
        "admission_digest": manifest.digest,
        "partition_dialogues": dict(counts),
        "partition_turns": dict(turns),
        "ambiguous_events": dict(ambiguous),
    }


def correlation(a, b):
    a, b = np.asarray(a), np.asarray(b)
    if not len(a) or np.all(a == a[0]) or np.all(b == b[0]):
        return None
    a, b = a - a.mean(), b - b.mean()
    denominator = float(np.linalg.norm(a) * np.linalg.norm(b))
    return float(a @ b / denominator) if denominator else None


def ranks(values):
    _, inverse, counts = np.unique(values, return_inverse=True, return_counts=True)
    return (np.cumsum(counts) - (counts + 1) / 2)[inverse]


def aggregate(results, identity, basis):
    partitions = {}
    for partition in ("development", "validation", "test"):
        dialogues = [d for d in results if d["partition"] == partition]
        rows = [r for d in dialogues for r in d["rows"]]
        y = np.array([r["baseline"] for r in rows])
        fractions = {}
        stats = {}
        for grain in ("round", "prefix", "delta"):
            x = np.array(
                [
                    r[grain] if grain == "delta" else r[grain]["coordinates"]
                    for r in rows
                ]
            )
            stats[grain] = {}
            for i, axis in enumerate(e.AXES):
                stats[grain][axis] = {
                    "pearson": correlation(x[:, i], y[:, i]),
                    "spearman": correlation(ranks(x[:, i]), ranks(y[:, i])),
                    "baseline_nonzero": int(np.count_nonzero(y[:, i])),
                    "baseline_stddev": float(np.std(y[:, i])),
                    "coordinate_stddev": float(np.std(x[:, i])),
                }
            if grain != "delta":
                values = [r[grain]["energy_fraction"] for r in rows]
                fractions[grain] = {
                    "median": float(np.median(values)),
                    "p10": float(np.quantile(values, 0.1)),
                    "p90": float(np.quantile(values, 0.9)),
                    "median_origin_support_present": float(
                        np.median([r[grain]["origin_support_present"] for r in rows])
                    ),
                }
        partitions[partition] = {
            "dialogues": len(dialogues),
            "turns": sum(d["turns"] for d in dialogues),
            "rounds": len(rows),
            "multiline_turns": sum(d["multiline"] for d in dialogues),
            "origin_span_energy_fraction": fractions,
            "readout_correlations": stats,
        }
    names = json.loads(PROTOCOL.read_text())["booking_outcome"]["scores"]
    booking = {}
    for i, name in enumerate(names):
        events = {
            partition: [
                holdout.OutcomeEvent(
                    d["dialogue"],
                    r["turn"],
                    r["label"],
                    r["scores"][i],
                    r["context_turns"],
                )
                for d in results
                if d["partition"] == partition
                for r in d["events"]
            ]
            for partition in partitions
        }
        event_counts = {
            p: dict(Counter("positive" if v.label else "negative" for v in ev))
            for p, ev in events.items()
        }
        try:
            calibration = holdout.fit_platt_calibration(events["development"])
            threshold, counts, candidates = holdout.select_operating_threshold(
                events["validation"], calibration
            )
            booking[name] = {
                "calibration": calibration.as_dict(),
                "validation_threshold": threshold,
                "validation_confusion": counts,
                "threshold_candidates": candidates,
                "test": holdout.evaluate_outcomes(
                    events["test"], calibration, threshold
                ),
                "counts": event_counts,
            }
        except holdout.OutcomeHoldoutError as exc:
            booking[name] = {
                "status": "BLOCKED",
                "reason": str(exc.code),
                "counts": event_counts,
            }
    chain = hashlib.sha256()
    for result in results:
        chain.update(e.canonical(result))
        chain.update(b"\n")
    report = {
        "schema": "edcm.multiwoz-epicycle-projection-result/1",
        "standing": "Stack candidate research",
        "identity": identity,
        "basis": basis,
        "partitions": partitions,
        "booking": booking,
        "dialogue_result_chain_sha256": chain.hexdigest(),
        "hmmm": json.loads(PROTOCOL.read_text())["hmmm"],
    }
    report["receipt_sha256"] = e.digest(report)
    return report


def checkpoint_rows(path, identity, tasks):
    if not path.exists():
        path.write_bytes(e.canonical({"identity": identity}) + b"\n")
        return []
    rows = []
    with path.open("rb") as handle:
        e.require(
            json.loads(handle.readline()) == {"identity": identity},
            "checkpoint source identity differs",
        )
        for line in handle:
            e.require(
                line.endswith(b"\n"),
                "incomplete checkpoint line; retain original and repair tail before resumption",
            )
            item = json.loads(line)
            row = item["row"]
            i = len(rows)
            e.require(
                item["digest"] == e.digest(row)
                and row["index"] == i
                and i < len(tasks)
                and row["source_sha256"] == tasks[i][3]
                and row["dialogue"] == e.digest(tasks[i][1]),
                "checkpoint row identity differs",
            )
            rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=1)
    args = parser.parse_args()
    e.require(args.workers > 0, "positive worker count required")
    e.require(
        len({args.archive.resolve(), args.checkpoint.resolve(), args.output.resolve()})
        == 3,
        "archive, checkpoint, and report must be distinct",
    )
    producer, basis = initialize()
    tasks, source = source_tasks(args.archive)
    identity = {
        "producer": producer,
        "source": source,
        "protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
        "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    rows = checkpoint_rows(args.checkpoint, identity, tasks)
    print(
        f"Admitted {len(tasks)} dialogues, {sum(len(t[4]) for t in tasks)} turns; resuming at {len(rows)}",
        flush=True,
    )
    started = time.monotonic()
    try:
        run_remaining(args, rows, tasks, identity, basis, started)
    except Exception as exc:
        failure = {
            "status": "incomplete",
            "identity": identity,
            "completed_dialogues": len(rows),
            "error_type": type(exc).__name__,
            "error_code": getattr(exc, "code", None),
        }
        args.output.write_text(json.dumps(failure, indent=2, sort_keys=True) + "\n")
        raise


def run_remaining(args, rows, tasks, identity, basis, started):
    if len(rows) < len(tasks):
        with mp.get_context("fork").Pool(args.workers) as pool, args.checkpoint.open(
            "ab"
        ) as checkpoint:
            for row in pool.imap(observe_dialogue, tasks[len(rows) :], chunksize=4):
                e.require(row["index"] == len(rows), "out-of-order corpus result")
                checkpoint.write(
                    e.canonical({"row": row, "digest": e.digest(row)}) + b"\n"
                )
                rows.append(row)
                if len(rows) % 100 == 0:
                    checkpoint.flush()
                if len(rows) % 500 == 0:
                    print(
                        f"{len(rows)}/{len(tasks)} dialogues; elapsed {time.monotonic()-started:.0f}s",
                        flush=True,
                    )
    e.require(
        len(rows) == len(tasks)
        and sum(r["turns"] for r in rows) == 143048
        and sum(len(r["rows"]) for r in rows) == 71524,
        "full corpus reconciliation differs",
    )
    print(
        "All native dialogue and round states complete; evaluating fixed statistical readouts",
        flush=True,
    )
    report = aggregate(rows, identity, basis)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(
        json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n"
    )
    temporary.replace(args.output)
    print("Complete aggregate receipt:", report["receipt_sha256"], flush=True)


if __name__ == "__main__":
    main()

# ratios: loc_comments=606:35 imports_exports=16:15 calls_definitions=226:23
