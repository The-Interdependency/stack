# ratios: loc_comments=814:41 imports_exports=21:31 calls_definitions=245:31
"""Replay the frozen EDCM epicycle experiment from installed public producers.

Usage: python -m research.edcm.epicycle_projection --output receipt.json
       python -m research.edcm.epicycle_projection --verify receipt.json
Exact native graphs are evidence. Numeric comparisons are research readouts.
"""
# === MODULE_BUILD ===
# id: stack_edcm_epicycle_projection
#   module_name: epicycle_projection
#   module_kind: instrument
#   summary: compares independently maintained EDCM readouts with released UCHC geometric fields at round and prefix scale
#   owner: The-Interdependency/stack
#   public_surface: verify_producers, validate_record, build_views, compare_fields, observe_rounds, experiment, main
#   internal_surface: origin construction, local field extraction, contrast and orthogonality audit
#   auth_boundary: none
#   storage_boundary: explicit receipt and summary output paths
#   network_boundary: none
#   user_data_boundary: public frozen fixtures
#   admin_only: false
#   tests: research/edcm/tests/test_epicycle_projection.py
#   rollout: stack-local measurement candidate only
#   rollback: retire candidate while preserving receipts
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: edcm_epicycle_native_replay
#   given: pinned installed producers and a native v2 record
#   then: both exact vector expressions and recoverable source are verified before comparison
#   class: correctness
# id: edcm_epicycle_comparison_boundary
#   given: a geometric field and an independently computed metric readout
#   then: field support, typed absence, numeric tolerance and the tested contrast remain explicit; no metric calibration is implied
#   class: correctness
# id: edcm_epicycle_frozen_protocol
#   given: exact code, protocol, producer versions and the same numeric runtime
#   then: every fixture, control, classification and receipt digest replays
#   class: provenance
# === END CONTRACTS ===
from __future__ import annotations

import argparse
import base64
from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
from importlib import import_module, metadata
import json
import math
from pathlib import Path
import platform
import re

import numpy as np
import uchc_halving as geometry
from edcm import measurement
from edcm.metric_origin_spec import metric_origin_spec
from edcm.semantic_metric_space import VECTOR_ORDER
from english_gonol import edcm_metric_origins
from ucns import attachment_codec, attachment_stack
from ucns.attachment_stack import Closed, DiskStack, display

WORKSPACE = Path(__file__).resolve().parent
VIEWS = ("additive", "ordinal", "paired", "recursive")
AXES = tuple(VECTOR_ORDER)


def canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("utf-8")


def digest(value):
    return sha256(canonical(value)).hexdigest()


def load(name):
    return json.loads((WORKSPACE / name).read_text(encoding="utf-8"))


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def verify_producers():
    base = load("BASE.json")["epicycle_projection"]
    graph = load("EPICYCLE_WORK_GRAPH.json")
    require(
        digest({k: graph[k] for k in ("repositories", "boundaries")})
        == graph["work_graph_sha256"]
        == base["work_graph_sha256"],
        "work graph differs from lock",
    )
    expected_commits = {
        "edcm": base["edcm_commit"],
        "ucns": base["ucns_commit"],
        "uchc": base["uchc_source_commit"],
    }
    projected = [
        item
        for item in json.loads(
            (WORKSPACE.parents[1] / "stack-manifest.json").read_text()
        )["research_participants"]
        if item["workspace"] == "research/edcm/"
        and item["participant_id"].startswith("epicycle-")
    ]
    for record in graph["repositories"]:
        project = record["repository"].rsplit("/", 1)[-1]
        rows = [
            row for row in projected if row["participant_id"] == f"epicycle-{project}"
        ]
        require(
            len(rows) == 1
            and all(
                rows[0][key] == record[key]
                for key in ("repository", "commit", "authority", "relation")
            )
            and rows[0]["authority_transfer"] is False,
            "root work graph projection differs: " + project,
        )
        if project in expected_commits:
            require(
                record["commit"] == expected_commits[project],
                "source identity differs: " + project,
            )
    wheels = [
        row for row in projected if row["participant_id"] == "epicycle-uchc-wheel"
    ]
    require(
        len(wheels) == 1
        and wheels[0]["artifact_sha256"] == base["uchc_wheel_sha256"]
        and wheels[0]["canonical_release"] is True
        and wheels[0]["authority_transfer"] is False,
        "wheel projection differs",
    )
    require(
        len(projected) == len(graph["repositories"]) + 1
        and base["authority_transfer"] is False
        and graph["boundaries"]["authority_transfer"] is False,
        "participant boundary differs",
    )
    imports = {
        "edcm": (
            measurement,
            import_module("edcm.metric_origin_spec"),
            import_module("edcm.semantic_metric_space"),
        ),
        "ucns": (attachment_codec, attachment_stack),
        "uchc": (geometry, edcm_metric_origins),
    }
    result = {}
    for project, modules in imports.items():
        dist = metadata.distribution(project)
        direct = json.loads(dist.read_text("direct_url.json") or "{}")
        require(
            not direct.get("dir_info", {}).get("editable"),
            "editable producer: " + project,
        )
        if project == "uchc":
            require(
                dist.version == base["uchc_version"]
                and direct.get("archive_info", {}).get("hashes", {}).get("sha256")
                == base["uchc_wheel_sha256"],
                "exact UCHC wheel required",
            )
        else:
            require(
                direct.get("url")
                == f"https://github.com/The-Interdependency/{project}.git"
                and direct.get("vcs_info", {}).get("commit_id")
                == expected_commits[project],
                "exact VCS producer required: " + project,
            )
        entries = dist.files
        require(bool(entries), "missing installed RECORD: " + project)
        verified_paths = set()
        for entry in entries:
            if entry.hash is None:
                require(
                    Path(str(entry)).suffix not in {".py", ".json", ".toml"},
                    "unhashed installed source: " + str(entry),
                )
                continue
            path = dist.locate_file(entry).resolve()
            require(
                entry.hash.mode == "sha256" and path.is_file(),
                "invalid installed source identity: " + str(entry),
            )
            actual = (
                base64.urlsafe_b64encode(sha256(path.read_bytes()).digest())
                .decode()
                .rstrip("=")
            )
            require(
                actual == entry.hash.value, "installed source differs: " + str(entry)
            )
            verified_paths.add(path)
        for module in modules:
            require(
                Path(module.__file__).resolve() in verified_paths,
                "shadowed producer: " + module.__name__,
            )
        result[project] = {
            "version": dist.version,
            "commit": expected_commits[project],
            "verified_record_entries": len(verified_paths),
        }
    authority = geometry.authority()
    require(
        authority["commit"] == base["ucns_commit"], "native geometry authority differs"
    )
    for name, expected in authority["source_sha256s"].items():
        require(
            sha256(
                (Path(attachment_stack.__file__).parent / (name + ".py")).read_bytes()
            ).hexdigest()
            == expected,
            "native UCNS source differs: " + name,
        )
    result["uchc"]["wheel_sha256"] = base["uchc_wheel_sha256"]
    return result


def validate_record(
    packet, *, expected_text, expected_terms=None, expected_source=None, radius=None
):
    require(packet.get("record_version") == 2, "both native vector readouts required")
    replayed = geometry.replay_closed(packet)
    require(geometry.closed_record(replayed) == packet, "UCHC record does not replay")
    root = attachment_codec.replay_graph(packet["graph"])
    require(
        isinstance(root, DiskStack)
        and attachment_codec.export_graph(root) == packet["graph"],
        "UCNS graph does not replay",
    )
    require(
        root.endpoint.record() == packet["vectors"]["placement_endpoint"]
        and root.additive_resultant.record() == packet["vectors"]["additive_resultant"],
        "native vector mismatch",
    )
    require("".join(root.recover()) == expected_text, "source text mismatch")
    if expected_source is not None:
        require(root.source == expected_source, "source identity mismatch")
    if radius is not None:
        require(root.radius == radius, "frame radius mismatch")
    if expected_terms is not None:
        require(
            root.relation == geometry.PROFILE + ":sequence"
            and all(isinstance(p, Closed) for p in root.participants)
            and tuple("".join(p.interior.recover()) for p in root.participants)
            == tuple(expected_terms),
            "ordered members mismatch",
        )
    return root


def origin_specs():
    released = edcm_metric_origins.load_metric_origin_specs()["specs"]
    require(set(released) == set(AXES), "released metric carrier set differs")
    result = {}
    for axis in AXES:
        spec = metric_origin_spec(axis)
        require(
            spec.canonical_metric_id == released[axis]["canonical_metric_id"]
            and list(spec.construction_terms) == released[axis]["construction_terms"],
            "released metric origin differs: " + axis,
        )
        result[axis] = {
            "canonical_id": spec.canonical_metric_id,
            "terms": list(spec.construction_terms),
            "semantic_definition": spec.semantic_definition,
            "measurement_alignment": spec.measurement_alignment,
        }
    return result


def construct_terms(terms, source, radius=1):
    children = tuple(
        geometry.construct_text(term, source=source + ":member") for term in terms
    )
    obj = geometry.construct_sequence(children, source=source, placement_radius=radius)
    packet = geometry.closed_record(obj)
    return packet, validate_record(
        packet,
        expected_text="".join(terms),
        expected_terms=terms,
        expected_source=source,
        radius=radius,
    )


def origin_records(specs):
    return {
        axis: construct_terms(
            specs[axis]["terms"], "edcm:metric-origin:" + specs[axis]["canonical_id"]
        )
        for axis in AXES
    }


def verify_origins(records, specs):
    require(tuple(records) == AXES, "metric carrier order differs")
    return {
        axis: validate_record(
            records[axis],
            expected_text="".join(specs[axis]["terms"]),
            expected_terms=specs[axis]["terms"],
            expected_source="edcm:metric-origin:" + specs[axis]["canonical_id"],
            radius=1,
        )
        for axis in AXES
    }


@dataclass(frozen=True)
class Coordinate:
    exact: list
    value: complex


def coordinate(point):
    return Coordinate(point.record(), display(point))


def build_views(root):
    # Each recursive coordinate is in its own parent-local frame. The path uses
    # the actual ordinal depth, not a word index or deduplicated graph node ID.
    recursive = {}
    pending = [((), root)]
    while pending:
        path, closed = pending.pop()
        recursive[path, "placed"] = coordinate(closed.endpoint)
        recursive[path, "additive"] = coordinate(closed.additive_resultant)
        for i, (member, ray) in enumerate(
            zip(closed.participants, closed.rays, strict=True)
        ):
            address = path + (closed.depth(i),)
            recursive[address, "ray"] = coordinate(ray.vector)
            if isinstance(member, Closed):
                pending.append((address, member.interior))
    additive = {((), "additive"): recursive[(), "additive"]}
    ordinal = {((), "placed"): recursive[(), "placed"]}
    return {
        "additive": additive,
        "ordinal": ordinal,
        "paired": additive | ordinal,
        "recursive": recursive,
    }


def field_record(field):
    return [
        {
            "path": list(path),
            "role": role,
            "exact": field[path, role].exact,
            "numeric": [field[path, role].value.real, field[path, role].value.imag],
        }
        for path, role in sorted(field)
    ]


def norm(values):
    return math.hypot(*(x for z in values for x in (z.real, z.imag)))


def compare_fields(left, right):
    shared = left.keys() & right.keys()
    a = {key: entry.value for key, entry in left.items()}
    b = {key: entry.value for key, entry in right.items()}
    keys = sorted(a.keys() | b.keys())
    u, v = norm(a.values()), norm(b.values())
    if v:
        projection = math.fsum(
            (a[key].real * (b[key].real / v) + a[key].imag * (b[key].imag / v))
            for key in sorted(shared)
        )
    else:
        projection = None
    if u and v:
        cosine = math.fsum(
            (
                (a[key].real / u) * (b[key].real / v)
                + (a[key].imag / u) * (b[key].imag / v)
            )
            for key in sorted(shared)
        )
    else:
        cosine = None
    return {
        "distance": norm(a.get(key, 0j) - b.get(key, 0j) for key in keys),
        "projection": projection,
        "cosine": cosine,
        "left_norm": u,
        "right_norm": v,
        "support": {
            "shared": len(shared),
            "left_only": len(left) - len(shared),
            "right_only": len(right) - len(shared),
        },
        "exact_equal": left.keys() == right.keys()
        and all(left[key].exact == right[key].exact for key in shared),
    }


def compare_views(left, right):
    return {view: compare_fields(left[view], right[view]) for view in VIEWS}


def origin_analysis(fields, comparison):
    result = {}
    for view in VIEWS:
        rows = [fields[axis][view] for axis in AXES]
        support = sorted(set().union(*(row.keys() for row in rows)))
        values = [
            [
                x
                for key in support
                for z in [row[key].value if key in row else 0j]
                for x in (z.real, z.imag)
            ]
            for row in rows
        ]
        normalized = np.asarray(
            [
                row / n if n else row
                for row in map(np.asarray, values)
                for n in [math.hypot(*row)]
            ]
        )
        singular = np.linalg.svd(normalized, compute_uv=False).tolist()
        pairs = [[compare_fields(left, right) for right in rows] for left in rows]
        nonorthogonal = sum(
            pair["cosine"] is not None
            and abs(pair["cosine"]) > comparison["comparison_tolerance"]
            for i, row in enumerate(pairs)
            for pair in row[i + 1 :]
        )
        result[view] = {
            "dimensions": 2 * len(support),
            "rank": sum(
                s > singular[0] * comparison["rank_relative_tolerance"]
                for s in singular
            ),
            "singular_values": singular,
            "nonzero_origins": sum(
                pairs[i][i]["left_norm"] > 0 for i in range(len(rows))
            ),
            "nonorthogonal_pairs": nonorthogonal,
            "pair_count": len(rows) * (len(rows) - 1) // 2,
            "axis_order": list(AXES),
            "pairs": pairs,
            "orthogonality": "FALSIFIED" if nonorthogonal else "UNRESOLVED",
        }
    return result


def vector(metrics):
    values = dict(zip(AXES, metrics.vector(), strict=True))
    require(all(math.isfinite(v) for v in values.values()), "nonfinite measurement")
    return values


def observation(raw_rounds, origins, objects):
    require(
        isinstance(raw_rounds, (tuple, list))
        and bool(raw_rounds)
        and all(isinstance(raw, str) and raw for raw in raw_rounds),
        "nonempty exact raw rounds required",
    )
    raw = "\n".join(raw_rounds)
    parsed = measurement.parse_transcript(raw)
    require(
        parsed.source_text == raw and len(parsed.rounds) == len(raw_rounds),
        "parser does not preserve declared rounds",
    )
    metrics = measurement.compute_transcript(parsed)
    records, fields, prefix_objects = [], [], []
    for i, raw_round in enumerate(raw_rounds):
        separate = measurement.parse_transcript(raw_round)
        require(
            len(separate.rounds) == 1
            and [(t.speaker, t.text) for t in separate.rounds[0].turns]
            == [(t.speaker, t.text) for t in parsed.rounds[i].turns],
            "raw round differs from parser cycle",
        )
        # Native construction can be reused by exact raw text; occurrences are
        # still separately retained when the objects participate in the prefix.
        if raw_round not in objects:
            terms = tuple(re.findall(r"\s+|\S+", raw_round))
            children = tuple(
                geometry.construct_text(term, source="edcm:observation-member")
                for term in terms
            )
            obj = geometry.construct_sequence(children, source="edcm:observation-round")
            packet = geometry.closed_record(obj)
            root = validate_record(
                packet,
                expected_text=raw_round,
                expected_terms=terms,
                expected_source="edcm:observation-round",
                radius=1,
            )
            objects[raw_round] = obj, packet, build_views(root)
        obj, packet, round_fields = objects[raw_round]
        if i:
            prefix_objects.append(
                geometry.construct_text("\n", source="edcm:observation-separator")
            )
        prefix_objects.append(obj)
        prefix = geometry.closed_record(
            geometry.construct_sequence(
                tuple(prefix_objects), source="edcm:observation-prefix"
            )
        )
        prefix_text = "\n".join(raw_rounds[: i + 1])
        prefix_root = validate_record(
            prefix,
            expected_text=prefix_text,
            expected_source="edcm:observation-prefix",
            radius=1,
        )
        prefix_fields = build_views(prefix_root)
        views = {"round": round_fields, "prefix": prefix_fields}
        records.append(
            {
                "round_index": i,
                "raw_text": raw_round,
                "raw_sha256": sha256(raw_round.encode("utf-8")).hexdigest(),
                "prefix_sha256": sha256(prefix_text.encode("utf-8")).hexdigest(),
                "metrics": vector(metrics[i]),
                "graphs": {"round": packet, "prefix": prefix},
                "fields": {
                    grain: {v: field_record(f) for v, f in view_fields.items()}
                    for grain, view_fields in views.items()
                },
                "origin_comparisons": {
                    grain: {
                        axis: compare_views(view_fields, origin_fields)
                        for axis, origin_fields in origins.items()
                    }
                    for grain, view_fields in views.items()
                },
            }
        )
        fields.append(views)
    return {"raw": raw, "rounds": records}, fields[-1]


def relation(a, b):
    return "greater" if a > b else "less" if a < b else "equal"


def distinction(pair, tolerance):
    if pair["exact_equal"]:
        return "FALSIFIED"
    return "SURVIVED" if pair["distance"] > tolerance else "UNRESOLVED"


def monotonic(left, right, delta, statistic, tolerance, signed, same_field):
    if signed or left is None or right is None:
        return "UNRESOLVED"
    change = left - right
    if same_field:
        return "FALSIFIED"
    if abs(change) <= tolerance:
        return "UNRESOLVED"
    expected = -1 if statistic == "distance" else 1
    return "SURVIVED" if change * delta * expected > 0 else "FALSIFIED"


def contrasts(protocol, origins):
    comparisons, objects = [], {}
    tolerance = protocol["comparison"]["comparison_tolerance"]
    for fixture in protocol["fixtures"]:
        left, left_views = observation(fixture["left"], origins, objects)
        right, right_views = observation(fixture["right"], origins, objects)
        if fixture.get("same_multiset"):
            require(
                Counter(left["raw"]) == Counter(right["raw"]),
                "fixture scalar multiset differs",
            )
        if fixture.get("same_final_round"):
            require(
                left["rounds"][-1]["raw_text"] == right["rounds"][-1]["raw_text"],
                "fixture final round differs",
            )
        l, r = left["rounds"][-1], right["rounds"][-1]
        pair = {
            grain: compare_views(left_views[grain], right_views[grain])
            for grain in left_views
        }
        witnesses = {}
        for axis, expected in fixture["changed"].items():
            a, b = l["metrics"][axis], r["metrics"][axis]
            baseline = "SURVIVED" if relation(a, b) == expected else "BLOCKED"
            witness = {
                "left": a,
                "right": b,
                "expected": expected,
                "actual": relation(a, b),
                "baseline": baseline,
                "grains": {},
            }
            for grain in pair:
                witness["grains"][grain] = {}
                for view in VIEWS:
                    target_left = l["origin_comparisons"][grain][axis][view]
                    target_right = r["origin_comparisons"][grain][axis][view]
                    geometric = distinction(pair[grain][view], tolerance)
                    hypotheses = {
                        stat: monotonic(
                            target_left[stat],
                            target_right[stat],
                            a - b,
                            stat,
                            tolerance,
                            axis == "O",
                            pair[grain][view]["exact_equal"],
                        )
                        for stat in ("distance", "projection", "cosine")
                    }
                    witness["grains"][grain][view] = {
                        "distinction": (
                            geometric if baseline == "SURVIVED" else "BLOCKED"
                        ),
                        "monotonic": (
                            hypotheses
                            if baseline == "SURVIVED"
                            else {key: "BLOCKED" for key in hypotheses}
                        ),
                    }
            witnesses[axis] = witness
        format_control = None
        if fixture.get("all_equal"):
            format_control = {
                "baseline": "SURVIVED" if l["metrics"] == r["metrics"] else "BLOCKED",
                "unchanged_axes": [
                    axis for axis in AXES if l["metrics"][axis] == r["metrics"][axis]
                ],
                "source_differs": left["raw"] != right["raw"],
            }
        comparisons.append(
            {
                "id": fixture["id"],
                "left": left,
                "right": right,
                "pair": pair,
                "witnesses": witnesses,
                "formatting_control": format_control,
            }
        )
    return comparisons


def expect_rejection(action):
    try:
        action()
    except (ValueError, TypeError, KeyError, ArithmeticError):
        return "SURVIVED"
    return "FALSIFIED"


def controls(specs, records, fields):
    from copy import deepcopy

    reversals = {}
    for axis in AXES:
        terms = specs[axis]["terms"][::-1]
        packet, root = construct_terms(
            terms, "edcm:metric-origin:" + specs[axis]["canonical_id"]
        )
        forward = records[axis][1]
        reversals[axis] = {
            "graph": packet,
            "exact_additive_equal": forward.additive_resultant.record()
            == root.additive_resultant.record(),
            "comparisons": compare_views(fields[axis], build_views(root)),
        }
    spec = specs["R"]
    packet, scaled = construct_terms(
        spec["terms"], "edcm:metric-origin:" + spec["canonical_id"], radius=2
    )
    old = records["R"][1]
    scale = {
        "graph": packet,
        "placement_scales_exactly": scaled.endpoint.record()
        == old.endpoint.scaled(2).record(),
        "additive_scales_exactly": scaled.additive_resultant.record()
        == old.additive_resultant.scaled(2).record(),
        "comparisons": compare_views(fields["R"], build_views(scaled)),
    }
    cancel_text = " " + chr(0x88020)
    cancelled = geometry.closed_record(
        geometry.construct_text(cancel_text, source="edcm:cancellation-control")
    )
    root = validate_record(cancelled, expected_text=cancel_text)
    field = build_views(root)
    zero = {
        "graph": cancelled,
        "exact_additive_zero": not root.additive_resultant.terms,
        "nonzero_placement": bool(root.endpoint.terms),
        "self": compare_views(field, field),
        "against_origin": compare_views(field, fields["R"]),
        "origin_against_zero": compare_views(fields["R"], field),
    }
    tampered = deepcopy(records["R"][0])
    tampered["vectors"]["placement_endpoint"] = []
    packets = {axis: records[axis][0] for axis in AXES}
    refusals = {
        "tampered_vector": expect_rejection(
            lambda: validate_record(tampered, expected_text="".join(spec["terms"]))
        ),
        "wrong_source": expect_rejection(
            lambda: validate_record(records["R"][0], expected_text="wrong")
        ),
        "metric_order": expect_rejection(
            lambda: verify_origins(dict(reversed(tuple(packets.items()))), specs)
        ),
        "wrong_terms": expect_rejection(
            lambda: validate_record(
                records["R"][0],
                expected_text="".join(spec["terms"]),
                expected_terms=spec["terms"][::-1],
            )
        ),
    }
    return {
        "reversals": reversals,
        "scale": scale,
        "cancellation": zero,
        "refusals": refusals,
    }


def summarize(report):
    summary = {
        "schema": "edcm.epicycle-projection-summary/1",
        "identity": report["identity"],
        "origin_analysis": {},
        "controls": {},
        "contrasts": [],
        "coverage": {},
        "outcomes": {},
        "hmmm": report["hmmm"],
        "receipt_sha256": report["receipt_sha256"],
    }
    summary["origin_analysis"] = {
        view: {
            key: data[key]
            for key in (
                "dimensions",
                "rank",
                "nonzero_origins",
                "nonorthogonal_pairs",
                "pair_count",
                "orthogonality",
            )
        }
        for view, data in report["origin_analysis"].items()
    }
    control = report["controls"]
    summary["controls"] = {
        "reversals_exact_additive_equal": sum(
            x["exact_additive_equal"] for x in control["reversals"].values()
        ),
        "reversals_distinguished": {
            view: sum(
                x["comparisons"][view]["distance"]
                > report["comparison"]["comparison_tolerance"]
                for x in control["reversals"].values()
            )
            for view in VIEWS
        },
        "scale": {k: v for k, v in control["scale"].items() if k.endswith("_exactly")},
        "cancellation": {
            "exact_additive_zero": control["cancellation"]["exact_additive_zero"],
            "nonzero_placement": control["cancellation"]["nonzero_placement"],
            "undefined_origin_direction": control["cancellation"][
                "origin_against_zero"
            ]["additive"]["projection"]
            is None,
        },
        "refusals": control["refusals"],
    }
    outcomes = {
        grain: {
            view: {
                "distinction": Counter(),
                **{key: Counter() for key in ("distance", "projection", "cosine")},
            }
            for view in VIEWS
        }
        for grain in ("round", "prefix")
    }
    coverage = {}
    for item in report["contrasts"]:
        summary["contrasts"].append(
            {
                "id": item["id"],
                "witnesses": item["witnesses"],
                "pair": item["pair"],
                "formatting_control": item["formatting_control"],
            }
        )
        for axis, witness in item["witnesses"].items():
            coverage.setdefault(axis, []).append(witness["baseline"])
            for grain, views in witness["grains"].items():
                for view, result in views.items():
                    target = outcomes[grain][view]
                    target["distinction"][result["distinction"]] += 1
                    for key, state in result["monotonic"].items():
                        target[key][state] += 1
    summary["coverage"] = {
        axis: "SURVIVED" if "SURVIVED" in coverage.get(axis, []) else "BLOCKED"
        for axis in AXES
    }
    summary["outcomes"] = outcomes
    return summary


def prepared_origins():
    producers = verify_producers()
    protocol = load("EPICYCLE_PROTOCOL.json")
    require(tuple(protocol["views"]) == VIEWS, "view order differs from protocol")
    specs = origin_specs()
    records = origin_records(specs)
    roots = verify_origins({axis: records[axis][0] for axis in AXES}, specs)
    fields = {axis: build_views(root) for axis, root in roots.items()}
    report = {
        "identity": {
            "work_graph_sha256": load("EPICYCLE_WORK_GRAPH.json")["work_graph_sha256"],
            "protocol_sha256": sha256(
                (WORKSPACE / "EPICYCLE_PROTOCOL.json").read_bytes()
            ).hexdigest(),
            "instrument_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
            "producers": producers,
            "numeric_runtime": {
                "python": platform.python_version(),
                "numpy": np.__version__,
                "platform": platform.system(),
                "machine": platform.machine(),
            },
        },
        "standing": "Stack-local candidate research",
        "axis_order": list(AXES),
        "view_order": list(VIEWS),
        "comparison": protocol["comparison"],
        "origin_specs": specs,
        "origins": {
            axis: {
                "graph": records[axis][0],
                "fields": {
                    view: field_record(field) for view, field in fields[axis].items()
                },
            }
            for axis in AXES
        },
        "hmmm": protocol["hmmm"],
    }
    return report, protocol, specs, records, fields


def observe_rounds(raw_rounds):
    """Measure any explicitly delimited exact source rounds under this candidate."""
    report, _, _, _, fields = prepared_origins()
    result, _ = observation(raw_rounds, fields, {})
    report.update(schema="edcm.epicycle-observation/1", observation=result)
    report["receipt_sha256"] = digest(report)
    return report


def experiment():
    report, protocol, specs, records, fields = prepared_origins()
    report.update(
        schema="edcm.epicycle-projection-receipt/1",
        origin_analysis=origin_analysis(fields, protocol["comparison"]),
        controls=controls(specs, records, fields),
        contrasts=contrasts(protocol, fields),
    )
    report["receipt_sha256"] = digest(report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--output", type=Path)
    mode.add_argument("--verify", type=Path)
    parser.add_argument("--summary", type=Path)
    parser.add_argument(
        "--rounds",
        type=Path,
        help="JSON list of exact one-round raw transcripts; omit for frozen experiment",
    )
    args = parser.parse_args()
    if args.rounds and args.summary:
        parser.error("--summary applies to the frozen experiment only")
    report = (
        observe_rounds(json.loads(args.rounds.read_text(encoding="utf-8")))
        if args.rounds
        else experiment()
    )
    if args.verify:
        require(
            args.verify.read_bytes() == canonical(report) + b"\n",
            "receipt replay differs",
        )
        print("Receipt replay verified: " + report["receipt_sha256"])
    else:
        args.output.write_bytes(canonical(report) + b"\n")
        print("Receipt generated: " + report["receipt_sha256"])
    if args.summary:
        args.summary.write_bytes(
            json.dumps(
                summarize(report), indent=2, sort_keys=True, allow_nan=False
            ).encode()
            + b"\n"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# ratios: loc_comments=814:41 imports_exports=21:31 calls_definitions=245:31
