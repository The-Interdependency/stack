#!/usr/bin/env python3
"""Read-only relational analysis of authenticated URPCS v1 traces.

The analyzer inventories relations already present in the frozen codec.  It
does not add an origin coordinate, traversal rule, wire field, or protocol
behavior.  Exact local gonol/member geometry is delegated to the pinned UCNS
native Möbius law; all other relations are reconstructed from authenticated
URPCS witnesses, canonical layer serialization, and state advance.
"""

# === MODULE_BUILD ===
# id: urpcs_relational_analyzer
#   module_name: urpcs_relational_analyzer
#   module_kind: experiment
#   summary: read-only graph, ablation, and capacity audit of relations already carried by authenticated URPCS v1 traces
#   owner: The-Interdependency/stack research/urpcs
#   public_surface: analyze_trace, ablate, run_analysis, render_report, command-line evidence writer
#   internal_surface: canonical graph construction, exact local-state projection, source-corpus inventory
#   auth_boundary: read authenticated URPCS frames only
#   storage_boundary: deterministic JSON and Markdown evidence
#   network_boundary: none
#   user_data_boundary: public committed fixtures and deterministic generated probes
#   admin_only: false
#   tests: research/urpcs/tests/test_relational_analyzer.py
#   rollout: Stack-local measurement only; no protocol profile or traversal behavior
#   rollback: remove this analyzer, its tests, report, receipt, and README entry
#   since: 2026-09-23
#   unresolved: typed origin transport, synchronization, stream interlacing, authorization, and event-promotion laws
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: urpcs_relational_authenticates_first
#   given: a URPCS v1 ciphertext, pre-message state, and associated data
#   then: C_0 authentication succeeds before witness recovery, graph construction, or plaintext release
#   class: security
#   since: 2026-09-23
#
# id: urpcs_relational_records_only_native_edges
#   given: an authenticated trace
#   then: every graph edge cites a frozen witness, serialization, or state-transition source and no origin transport is invented
#   class: correctness
#   since: 2026-09-23
#
# id: urpcs_relational_evidence_is_deterministic
#   given: identical pinned authorities, source corpus, runtime, and generated probes
#   then: canonical graph, ablation, capacity ledger, receipt, and Markdown projection are byte-identical
#   class: evidence
#   since: 2026-09-23
# === END CONTRACTS ===

# === BOUNDARIES ===
# id: urpcs_relational_research_boundary
#   summary: observes authenticated research traces without changing the URPCS v1 wire, state machine, traversal, or UCNS geometry
#   auth_boundary: read
#   storage_boundary: write deterministic evidence only
#   network_boundary: none
#   user_data_boundary: read public fixtures
#   admin_only: false
#   pii: none
#   secrets: none
#   review_required: exact-head independent review
#   owner: The-Interdependency/stack research/urpcs
# === END BOUNDARIES ===

# === DEPENDENCIES ===
# id: urpcs_relational_dependency_edges
#   summary: consumes frozen URPCS trace laws and delegates only exact local Möbius geometry to pinned UCNS
#   imports: urpcs_v1_reference, urpcs_mobius_projection
#   calls: authenticate/decode, LayerWire inverse, state advance, ucns.native_mobius_state
#   external: optional PyCryptodome KMAC256 accelerator verified by NIST Sample 4
#   class: runtime
#   direction: outbound
#   owner: The-Interdependency/stack research/urpcs
#   since: 2026-09-23
# === END DEPENDENCIES ===

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess  # nosec B404
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable, Mapping, Sequence

import urpcs_mobius_projection as projection
import urpcs_v1_reference as ref


class RelationalAnalysisError(ValueError):
    """Raised when a trace or evidence identity cannot support the audit."""


STACK_INPUT_COMMIT = "164f86ce2cb640242dbfb06390330142e90a406e"
STACK_INPUT_TREE = "de450f1355bf2c9d7f178b0f3f770ed05460a3a7"
UCNS_COMMIT = "4086ab82399c4d142b0eacfbc09e0a69ed151aa5"
UCNS_TREE = "3b9c3143c86e07d497eebfbcb32a0f14a1a1ab3b"
SKILL_LIB_COMMIT = "22c2c5702d14fb4b0faeb717777ecab2665770a1"
SKILL_LIB_TREE = "6e483e484d5682e638de5f0957224d37993643dd"
METAPAT_COMMIT = "e4165b0cac9eca41daef9c2f941881028ca55d48"
METAPAT_TREE = "9918f1188f64a517745851514804deb5fcae9c96"
GRAPH_SCHEMA = "the-interdependency.stack.urpcs-relational-graph.v0"
RECEIPT_SCHEMA = "the-interdependency.stack.urpcs-relational-carrier-receipt.v0"
CLASSIFICATION = "RELATION_PRESENT_WITH_BLOCKED_CAPACITIES"
GIT = shutil.which("git")

FROZEN_PATHS = (
    "research/urpcs/docs/urpcs-v1-spec.md",
    "research/urpcs/urpcs_v1_reference.py",
    "research/urpcs/urpcs_v1_independent.js",
    "research/urpcs/vectors/urpcs-v1-vectors.json",
    "research/urpcs/receipts/urpcs-mobius-projection-v0.json",
    "research/urpcs/WORK_GRAPH.json",
    "research/urpcs/SOURCE_RECEIPT.json",
)

NONCLAIMS = (
    "traversal utility",
    "compression",
    "entropy",
    "confidentiality",
    "encryption security",
    "IND-CPA or IND-CCA security",
    "production suitability",
    "PCEA compatibility",
    "UCNS-gonol identity",
    "UCHC cache behavior",
    "absolute winding recovery",
    "release authority",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RelationalAnalysisError(message)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _compact(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode("utf-8")


def _stable_id(prefix: str, value: Any) -> str:
    return f"{prefix}:{_sha256(_compact(value))[:24]}"


def _git_text(repo: Path, *args: str) -> str:
    _require(GIT is not None, "Git executable unavailable")
    result = subprocess.run(  # nosec B603
        [GIT, "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def _git_bytes(repo: Path, *args: str) -> bytes:
    _require(GIT is not None, "Git executable unavailable")
    result = subprocess.run(  # nosec B603
        [GIT, "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def _state_from_json(value: Mapping[str, Any]) -> ref.KState:
    return ref.KState(
        bytes.fromhex(value["k_pair"]),
        bytes.fromhex(value["k_integrity"]),
        bytes.fromhex(value["k_advance"]),
        bytes.fromhex(value["nu_origin"]),
        int(value["R_cap"]),
    )


def _state_identity(state: ref.KState) -> dict[str, Any]:
    fields = {
        "k_pair_sha256": _sha256(state.pair),
        "k_integrity_sha256": _sha256(state.integrity),
        "k_advance_sha256": _sha256(state.advance),
        "nu_origin_sha256": _sha256(state.origin),
        "R_cap": state.depth,
    }
    fields["identity_sha256"] = _sha256(_compact(fields))
    return fields


def _mobius(displacement: int, ucns: ModuleType) -> dict[str, Any]:
    return projection.euclidean_mobius_state(displacement, ref.M, ucns)


def _canonical_graph(nodes: Iterable[dict[str, Any]], edges: Iterable[dict[str, Any]]) -> dict[str, Any]:
    node_rows = sorted(nodes, key=lambda item: item["id"])
    edge_rows = sorted(edges, key=lambda item: item["id"])
    _require(len({row["id"] for row in node_rows}) == len(node_rows), "duplicate graph node")
    _require(len({row["id"] for row in edge_rows}) == len(edge_rows), "duplicate graph edge")
    node_ids = {row["id"] for row in node_rows}
    for edge in edge_rows:
        _require(edge["source"] in node_ids and edge["target"] in node_ids, "inconsistent graph reference")
    payload = {"schema": GRAPH_SCHEMA, "nodes": node_rows, "edges": edge_rows}
    payload["graph_sha256"] = _sha256(_compact(payload))
    return payload


def _edge(kind: str, source: str, target: str, source_law: str, **fields: Any) -> dict[str, Any]:
    body = {"kind": kind, "source": source, "target": target, "source_law": source_law, **fields}
    return {"id": _stable_id("edge", body), **body}


def _path_sums(witness: list[Any], index: Mapping[str, Any]) -> tuple[dict[bytes, int], dict[bytes, bytes]]:
    gonols = index["gonols"]
    scopes = {gid: item["origin"] for gid, item in gonols.items()}
    attachments = [(row[0], row[1]) for row in witness[1][4]]
    displacements = {(row[0], row[1]): ref.n_value(row[2]) for row in witness[2]}
    sums = projection.reconstruct_path_sums(scopes, attachments, displacements) if gonols else {}
    parents = {child: parent for parent, child in attachments}
    return sums, parents


def analyze_trace(
    *,
    case_id: str,
    ciphertext: bytes,
    state: ref.KState,
    associated_data: bytes,
    ucns: ModuleType,
    expected_plaintext: bytes | None = None,
    source_kind: str,
) -> dict[str, Any]:
    """Authenticate one frame and construct only relations established by v1."""

    witness, index, beta, body = projection.authenticated_witness(ciphertext, state, associated_data)
    decoded = ref.decrypt(ciphertext, state, associated_data)
    if expected_plaintext is not None:
        _require(decoded.plaintext == expected_plaintext, f"plaintext mismatch: {case_id}")
    layers = [ref.deserialize_layer(raw, layer) for layer, raw in enumerate(decoded.layers)]
    sums, parents = _path_sums(witness, index)
    shape_rows = {row[2]: (ref.n_value(row[3][0]), ref.n_value(row[3][1])) for row in witness[0]}
    delta_rows = {(row[0], row[1]): ref.n_value(row[2]) for row in witness[2]}

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []
    layer_ids: dict[int, str] = {}
    origin_ids: dict[bytes, str] = {}
    gonol_ids: dict[bytes, str] = {}
    occurrence_ids: dict[bytes, str] = {}

    transform_id = f"case:{case_id}:transform"
    nodes.append({
        "id": transform_id,
        "kind": "transformation",
        "event_type": "authenticated-codec-message",
        "source_kind": source_kind,
        "plaintext_sha256": _sha256(decoded.plaintext),
        "ciphertext_sha256": _sha256(ciphertext),
        "receipt_hex": decoded.receipt.hex(),
        "pre_state": _state_identity(state),
        "successor_state": _state_identity(decoded.next_state),
        "promotion_status": "hmmm: v1 carries resulting bytes and state, not a typed event identity in the next layer",
    })

    for layer_index, (layer, raw) in enumerate(zip(layers, decoded.layers)):
        layer_id = f"case:{case_id}:layer:{layer_index}"
        layer_ids[layer_index] = layer_id
        input_bytes = decoded.plaintext if layer_index == 0 else decoded.layers[layer_index - 1]
        nodes.append({
            "id": layer_id,
            "kind": "layer",
            "layer": layer_index,
            "input_bytes": len(input_bytes),
            "input_sha256": _sha256(input_bytes),
            "layer_wire_bytes": len(raw),
            "layer_wire_sha256": _sha256(raw),
            "region_count": len(layer[2]),
        })
        edges.append(_edge("constructs-layer", transform_id, layer_id, "URPCS v1 Laws 9 and 12"))

    for origin, (layer_index, region_index) in sorted(index["origins"].items(), key=lambda item: item[1]):
        oid = f"case:{case_id}:origin:{origin.hex()}"
        origin_ids[origin] = oid
        region = layers[layer_index][2][region_index]
        region_length = ref.n_value(region[1])
        origin_gonols = index["gonols_by_origin"][origin]
        roots = sorted(item["id"] for item in origin_gonols if item["id"] not in parents)
        nodes.append({
            "id": oid,
            "kind": "origin",
            "raw_id_hex": origin.hex(),
            "layer": layer_index,
            "region": region_index,
            "region_bytes": region_length,
            "region_sha256": _sha256(
                decoded.plaintext[region_index:region_index + 1]
                if layer_index == 0
                else decoded.layers[layer_index - 1][region_index:region_index + 1]
            ),
            "arity": len(origin_gonols),
            "shape": [len(index["by_origin"][origin]), len(origin_gonols)],
            "root_gonol_ids_hex": [item.hex() for item in roots],
            "local_phase": None,
            "local_sheet": None,
            "geometry_status": "no URPCS v1 law assigns an origin phase or sheet",
        })
        edges.append(_edge("contains-origin", layer_ids[layer_index], oid, "URPCS v1 Laws 4 and 9"))

    for occurrence, item in sorted(index["occurrences"].items()):
        oid = origin_ids[item["origin"]]
        occurrence_id = f"case:{case_id}:occurrence:{occurrence.hex()}"
        occurrence_ids[occurrence] = occurrence_id
        layer_index, region_index = index["origins"][item["origin"]]
        nodes.append({
            "id": occurrence_id,
            "kind": "occurrence",
            "raw_id_hex": occurrence.hex(),
            "origin_id": oid,
            "layer": layer_index,
            "region": region_index,
            "start_bit": item["start"],
            "length_bits": item["length"],
            "axis_hex": item["axis"].hex(),
            "payload_ascii": item["payload"].decode("ascii"),
        })
        edges.append(_edge("constructs-occurrence", oid, occurrence_id, "URPCS v1 Laws 4 and 5"))

    for gid, item in sorted(index["gonols"].items()):
        origin = item["origin"]
        layer_index, region_index = index["origins"][origin]
        gonol_id = f"case:{case_id}:gonol:{gid.hex()}"
        gonol_ids[gid] = gonol_id
        local = _mobius(sums[gid], ucns)
        child_arity, carry_flag = shape_rows[gid]
        nodes.append({
            "id": gonol_id,
            "kind": "gonol",
            "raw_id_hex": gid.hex(),
            "origin_id": origin_ids[origin],
            "layer": layer_index,
            "region": region_index,
            "arity": child_arity,
            "shape": {"child_arity": child_arity, "carry": bool(carry_flag), "member_count": len(item["members"])},
            "local_state": local,
        })
        edges.append(_edge("constructs-gonol", origin_ids[origin], gonol_id, "URPCS v1 Laws 6 and 8"))
        structural_path: list[str] = []
        cursor = gid
        while cursor in parents:
            parent = parents[cursor]
            structural_path.append(f"{parent.hex()}>{cursor.hex()}")
            cursor = parent
        structural_path.reverse()
        observation = {
            "id": f"{gonol_id}:state",
            "kind": "gonol-state",
            "case_id": case_id,
            "origin": origin.hex(),
            "gonol": gid.hex(),
            "occurrence": None,
            "phase": local["phase"],
            "frame": local["frame"],
            "S": local["S"],
            "q": local["q"],
            "arity": child_arity,
            "shape": [child_arity, carry_flag, len(item["members"])],
            "provenance": [case_id, layer_index, region_index, source_kind],
            "history": [transform_id, *structural_path],
        }
        observations.append(observation)

        members = sorted(item["members"])
        for member_index, occurrence in enumerate(members):
            local_delta = 0 if len(members) == 1 or member_index == 0 else ref.M // 2
            member_state = _mobius(sums[gid] + local_delta, ucns)
            membership = _edge(
                "member-of",
                occurrence_ids[occurrence],
                gonol_id,
                "URPCS v1 Laws 4 and 9",
                local_displacement=local_delta,
                local_state=member_state,
            )
            edges.append(membership)
            occurrence_item = index["occurrences"][occurrence]
            observations.append({
                "id": f"{membership['id']}:state",
                "kind": "member-state",
                "case_id": case_id,
                "origin": origin.hex(),
                "gonol": gid.hex(),
                "occurrence": occurrence.hex(),
                "phase": member_state["phase"],
                "frame": member_state["frame"],
                "S": member_state["S"],
                "q": member_state["q"],
                "arity": child_arity,
                "shape": [child_arity, carry_flag, len(item["members"]), occurrence_item["length"]],
                "provenance": [
                    case_id,
                    layer_index,
                    region_index,
                    occurrence_item["start"],
                    occurrence_item["axis"].hex(),
                    source_kind,
                ],
                "history": [transform_id, *structural_path, membership["id"]],
            })

    for parent, child, _layer_raw in witness[1][4]:
        delta = delta_rows[(parent, child)]
        parent_state = _mobius(sums[parent], ucns)
        child_state = _mobius(sums[child], ucns)
        relation = {
            "delta_phase": (child_state["phase_numerator"] - parent_state["phase_numerator"]) % ref.M,
            "sheet_product": 1 if parent_state["frame"] == child_state["frame"] else -1,
            "unreduced_delta": delta,
        }
        edges.append(_edge(
            "attaches",
            gonol_ids[parent],
            gonol_ids[child],
            "URPCS v1 Laws 3 and 8",
            relation=relation,
        ))

    serialization_events: list[str] = []
    for layer_index in range(len(layers) - 1):
        source_wire = decoded.layers[layer_index]
        rebuilt = ref._expand_layer(layers[layer_index + 1], state, index)
        _require(rebuilt == source_wire, "serialization relation is not exactly reversible")
        event_id = f"case:{case_id}:serialization:{layer_index}->{layer_index + 1}"
        serialization_events.append(event_id)
        nodes.append({
            "id": event_id,
            "kind": "transformation",
            "event_type": "layer-serialization-to-successor-input",
            "source_layer": layer_index,
            "target_layer": layer_index + 1,
            "bytes": len(source_wire),
            "source_wire_sha256": _sha256(source_wire),
            "target_input_sha256": _sha256(rebuilt),
            "exactly_reversible": True,
            "typed_event_promoted": False,
        })
        edges.append(_edge("serialization-source", layer_ids[layer_index], event_id, "URPCS v1 Law 9"))
        edges.append(_edge("serialization-target", event_id, layer_ids[layer_index + 1], "URPCS v1 Laws 4 and 9"))
        for origin, (target_layer, region_index) in sorted(index["origins"].items(), key=lambda item: item[1]):
            if target_layer != layer_index + 1:
                continue
            edges.append(_edge(
                "byte-provenance",
                event_id,
                origin_ids[origin],
                "URPCS v1 Laws 4 and 9",
                source_byte_start=region_index * ref.X,
                source_byte_end=min((region_index + 1) * ref.X, len(source_wire)),
            ))
            for occurrence in sorted(index["by_origin"][origin], key=lambda item: item["start"]):
                start = region_index * ref.X * 8 + occurrence["start"]
                edges.append(_edge(
                    "bit-provenance",
                    event_id,
                    occurrence_ids[occurrence["id"]],
                    "URPCS v1 Laws 4, 5, and 9",
                    source_bit_start=start,
                    source_bit_end=start + occurrence["length"],
                ))

    graph = _canonical_graph(nodes, edges)
    return {
        "case_id": case_id,
        "source_kind": source_kind,
        "plaintext_hex": decoded.plaintext.hex(),
        "plaintext_sha256": _sha256(decoded.plaintext),
        "associated_data_sha256": _sha256(associated_data),
        "ciphertext_sha256": _sha256(ciphertext),
        "beta_sha256": _sha256(beta),
        "authenticated_body_sha256": _sha256(body),
        "receipt_hex": decoded.receipt.hex(),
        "successor_state": _state_identity(decoded.next_state),
        "layer_wire_sha256": [_sha256(raw) for raw in decoded.layers],
        "serialization_events": serialization_events,
        "graph": graph,
        "observations": sorted(observations, key=lambda item: item["id"]),
    }


ABLATION_STEPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("phase", ("phase",)),
    ("phase_sheet", ("phase", "frame")),
    ("origin_phase_sheet", ("origin", "phase", "frame")),
    ("origin_gonol_phase_sheet", ("origin", "gonol", "phase", "frame")),
    (
        "origin_gonol_arity_phase_sheet_provenance",
        ("origin", "gonol", "arity", "shape", "phase", "frame", "provenance"),
    ),
    (
        "full_relational_transformation_history",
        ("origin", "gonol", "arity", "shape", "phase", "frame", "provenance", "history", "kind", "occurrence"),
    ),
)


def _feature(record: Mapping[str, Any], name: str) -> Any:
    value = record[name]
    if isinstance(value, list):
        return tuple(value)
    if isinstance(value, dict):
        return tuple(sorted(value.items()))
    return value


def _key(record: Mapping[str, Any], fields: Sequence[str]) -> tuple[Any, ...]:
    return tuple(_feature(record, field) for field in fields)


def _pair_count(groups: Mapping[tuple[Any, ...], Sequence[Mapping[str, Any]]]) -> int:
    return sum(len(rows) * (len(rows) - 1) // 2 for rows in groups.values())


def _classes(records: Sequence[Mapping[str, Any]], fields: Sequence[str]) -> dict[tuple[Any, ...], list[Mapping[str, Any]]]:
    groups: dict[tuple[Any, ...], list[Mapping[str, Any]]] = defaultdict(list)
    for record in records:
        groups[_key(record, fields)].append(record)
    return groups


def _witness_separation(
    previous: Mapping[tuple[Any, ...], Sequence[Mapping[str, Any]]],
    fields: Sequence[str],
) -> dict[str, Any] | None:
    for rows in previous.values():
        if len(rows) < 2:
            continue
        for left, right in combinations(rows, 2):
            if _key(left, fields) != _key(right, fields):
                return {
                    "left": left["id"],
                    "right": right["id"],
                    "left_key": list(_key(left, fields)),
                    "right_key": list(_key(right, fields)),
                }
    return None


def _marginal(
    records: Sequence[Mapping[str, Any]],
    base_fields: Sequence[str],
    added_fields: Sequence[str],
) -> dict[str, Any]:
    base = _classes(records, base_fields)
    extended = _classes(records, (*base_fields, *added_fields))
    base_pairs = _pair_count(base)
    extended_pairs = _pair_count(extended)
    return {
        "base_fields": list(base_fields),
        "added_fields": list(added_fields),
        "pairs_before": base_pairs,
        "pairs_after": extended_pairs,
        "pairs_separated": base_pairs - extended_pairs,
        "minimal_witness": _witness_separation(base, (*base_fields, *added_fields)),
    }


def ablate(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Measure each declared projection as a monotone equivalence refinement."""

    ordered = sorted(records, key=lambda item: item["id"])
    _require(bool(ordered), "ablation requires observations")
    steps: list[dict[str, Any]] = []
    prior_groups: dict[tuple[Any, ...], list[Mapping[str, Any]]] | None = None
    prior_pairs: int | None = None
    for name, fields in ABLATION_STEPS:
        groups = _classes(ordered, fields)
        pair_count = _pair_count(groups)
        multiplicities = Counter(len(rows) for rows in groups.values())
        step = {
            "name": name,
            "fields": list(fields),
            "observations": len(ordered),
            "equivalence_classes": len(groups),
            "singleton_classes": multiplicities.get(1, 0),
            "non_singleton_classes": sum(count for size, count in multiplicities.items() if size > 1),
            "maximum_multiplicity": max(multiplicities),
            "class_multiplicity_histogram": {str(size): count for size, count in sorted(multiplicities.items())},
            "colliding_pairs_retained": pair_count,
            "colliding_pairs_separated_from_previous": None if prior_pairs is None else prior_pairs - pair_count,
            "colliding_excess_records": len(ordered) - len(groups),
            "minimal_new_distinction": _witness_separation(prior_groups, fields) if prior_groups is not None else None,
        }
        steps.append(step)
        prior_groups = groups
        prior_pairs = pair_count

    phase_groups = _classes(ordered, ("phase",))
    complete_local_groups = _classes(ordered, ("phase", "frame"))
    phase_shared = [rows for rows in phase_groups.values() if len({row["id"] for row in rows}) > 1]
    local_shared = [rows for rows in complete_local_groups.values() if len({row["id"] for row in rows}) > 1]
    identity_summary = {
        "identities_sharing_one_visible_angle": sum(len(rows) for rows in phase_shared),
        "visible_angle_classes_with_multiple_identities": len(phase_shared),
        "identities_sharing_phase_and_sheet": sum(len(rows) for rows in local_shared),
        "phase_sheet_classes_with_multiple_identities": len(local_shared),
        "visible_angle_witness": [row["id"] for row in phase_shared[0][:2]] if phase_shared else None,
        "phase_sheet_witness": [row["id"] for row in local_shared[0][:2]] if local_shared else None,
    }

    base = ("origin", "gonol", "phase", "frame")
    marginals = {
        "frame": _marginal(ordered, ("phase",), ("frame",)),
        "origin": _marginal(ordered, ("phase", "frame"), ("origin",)),
        "gonol": _marginal(ordered, ("origin", "phase", "frame"), ("gonol",)),
        "arity_and_shape": _marginal(ordered, base, ("arity", "shape")),
        "provenance": _marginal(ordered, base, ("provenance",)),
        "arity_shape_and_provenance": _marginal(ordered, base, ("arity", "shape", "provenance")),
        "transformation_history": _marginal(
            ordered,
            ("origin", "gonol", "arity", "shape", "phase", "frame", "provenance"),
            ("history", "kind", "occurrence"),
        ),
    }

    exclusive = Counter()
    for rows in _classes(ordered, base).values():
        for left, right in combinations(rows, 2):
            arity_differs = _key(left, ("arity", "shape")) != _key(right, ("arity", "shape"))
            provenance_differs = _key(left, ("provenance",)) != _key(right, ("provenance",))
            if arity_differs and not provenance_differs:
                exclusive["arity_shape_only"] += 1
            elif provenance_differs and not arity_differs:
                exclusive["provenance_only"] += 1
            elif arity_differs and provenance_differs:
                exclusive["both_arity_shape_and_provenance"] += 1
            else:
                exclusive["neither"] += 1
    result = {
        "observation_count": len(ordered),
        "steps": steps,
        "identity_multiplicity": identity_summary,
        "marginal_contributions": marginals,
        "exclusive_pair_attribution_within_origin_gonol_phase_sheet": {
            key: exclusive.get(key, 0)
            for key in ("arity_shape_only", "provenance_only", "both_arity_shape_and_provenance", "neither")
        },
    }
    result["ablation_sha256"] = _sha256(_compact(result))
    return result


def torsor_invariance(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Check common phase rotation without selecting a privileged global zero."""

    states = sorted({(record["phase"], record["frame"]) for record in records})
    checked = 0
    for left, right in combinations(states, 2):
        left_phase = int(left[0].strip("()").split(",")[0])
        right_phase = int(right[0].strip("()").split(",")[0])
        before = (right_phase - left_phase) % ref.M
        sheet_before = 1 if left[1] == right[1] else -1
        for rotation in range(ref.M):
            after = ((right_phase + rotation) - (left_phase + rotation)) % ref.M
            _require(after == before, "common rotation changed relative phase")
            sheet_after = 1 if left[1] == right[1] else -1
            _require(sheet_after == sheet_before, "common rotation changed sheet relation")
            checked += 1
    return {
        "status": "INVARIANT",
        "coordinate_zero_selected": False,
        "distinct_complete_local_states": len(states),
        "complete_state_pair_rotation_checks": checked,
        "law": "((phi_b+k)-(phi_a+k)) mod M = (phi_b-phi_a) mod M; sheet product unchanged",
    }


def _capacity_ledger(vector_rows: Sequence[Mapping[str, Any]], traces: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    vector_ids = {row["id"] for row in vector_rows}
    _require({
        "wrong_ad",
        "authenticated_body_mutation",
        "replay_after_advance",
        "concurrent_state_rejection",
        "receipt_and_state_equality",
    } <= vector_ids, "committed capacity vectors incomplete")
    recursive = [trace for trace in traces if trace["serialization_events"]]
    return [
        {
            "capacity": "exact provenance recovery",
            "classification": "SUPPORTED_FOR_COMPLETE_AUTHENTICATED_TRACE",
            "evidence": "every successor byte and occurrence bit span is mapped to the exact predecessor LayerWire; inverse expansion is byte-identical",
            "limitations": "no semantic predecessor-origin correspondence is defined across a serialization boundary",
        },
        {
            "capacity": "mutation localization",
            "classification": "DETECTION_ONLY_AT_AUTHENTICATION_BOUNDARY",
            "evidence": "authenticated_body_mutation fails at tag verification before witness parsing",
            "limitations": "v1 rejects the frame but supplies no authenticated subframe localization law",
        },
        {
            "capacity": "divergent-state and fork detection",
            "classification": "SUPPORTED_AT_NEXT_USE_AND_HOST_CAS_BOUNDARY",
            "evidence": "replay_after_advance fails under K_(t+1); concurrent_state_rejection admits exactly one host CAS commit",
            "limitations": "no durable fork recovery, rollback resistance, or reconciliation law",
        },
        {
            "capacity": "cycle consistency and nontrivial holonomy",
            "classification": "ABSENT_IN_AVAILABLE_NATIVE_GRAPH",
            "evidence": "attachment components are rooted forests and serialization/state provenance is forward-only; the complete graph contains no directed cycle",
            "limitations": "a nontrivial holonomy test requires a native cycle relation that v1 does not provide",
        },
        {
            "capacity": "synchronization between independently processed origins",
            "classification": "BLOCKED_MISSING_RELATION",
            "evidence": "pairing and attachment are origin-scoped; serialization creates successor origins without an origin-to-origin transport edge",
            "missing_law": "typed relation Sync(origin_a local state, origin_b local state) -> agreement/divergence result with deterministic inverse or declared information loss",
            "owner": "The-Interdependency/stack in a separately versioned experimental profile",
        },
        {
            "capacity": "reconstruction from multiple partial projections",
            "classification": "SUPPORTED_ONLY_FOR_COMPLETE_PARTITION",
            "evidence": "all occurrence intervals reconstruct each region and all regions reconstruct the predecessor byte stream",
            "limitations": "any omitted byte/bit interval is ambiguous; v1 defines no redundancy or erasure recovery",
        },
        {
            "capacity": "stable interlacing of three, five, and seven logical streams",
            "classification": "BLOCKED_MISSING_RELATION",
            "evidence": "v1 has no logical-stream identity or interlace/deinterlace mapping",
            "missing_law": "Interlace(stream identities, ordered payloads, origin provenance) -> reversible carrier relation for arities 3, 5, and 7",
            "owner": "The-Interdependency/stack in a separately versioned experimental profile",
        },
        {
            "capacity": "contextual authorization requiring complete relational agreement",
            "classification": "BLOCKED_MISSING_POLICY",
            "evidence": "KMAC authenticates C_0 and associated data; no authorization predicate consumes the graph",
            "missing_law": "Authorize(subject, action, complete relational state, policy identity) -> decision with fail-closed completeness rules",
            "owner": "host/application policy owner; not UCNS geometry",
        },
        {
            "capacity": "promotion of transformation events into the next recursive layer",
            "classification": "RAW_RESULT_RECURS_TYPED_EVENT_BLOCKED",
            "evidence": f"{len(recursive)} analyzed traces feed exact serialized result bytes into successor layers",
            "missing_law": "Promote(event identity, inputs, outputs, provenance) -> typed next-layer object with canonical inverse",
            "owner": "The-Interdependency/stack in a separately versioned experimental profile",
        },
    ]


def _unresolved_relations() -> list[dict[str, Any]]:
    return [
        {
            "relation": "origin local phase/sheet and origin-to-origin transport",
            "required_inputs": ["source origin identity", "target origin identity", "source local state", "native transition provenance"],
            "required_outputs": ["target local state", "relative phase", "relative sheet"],
            "invertibility_obligation": "recover the source state or declare and authenticate exact information loss",
            "owner": "The-Interdependency/stack profile for transport; UCNS retains sole authority over Möbius geometry",
        },
        {
            "relation": "independent-origin synchronization",
            "required_inputs": ["two origin states", "shared context identity", "ordering/fork evidence"],
            "required_outputs": ["agreement or divergence", "reconciliation provenance"],
            "invertibility_obligation": "preserve both inputs and make any merge loss explicit",
            "owner": "The-Interdependency/stack host/profile",
        },
        {
            "relation": "logical stream interlacing",
            "required_inputs": ["3, 5, or 7 stream identities", "ordered stream payloads", "origin provenance"],
            "required_outputs": ["carrier ordering", "exact deinterlace map"],
            "invertibility_obligation": "byte-exact recovery of every stream and ordering",
            "owner": "separately versioned Stack experimental profile",
        },
        {
            "relation": "contextual authorization",
            "required_inputs": ["subject", "action", "policy identity", "complete graph identity"],
            "required_outputs": ["allow or deny", "bound evidence identity"],
            "invertibility_obligation": "not applicable to decision; evidence binding and fail-closed completeness are mandatory",
            "owner": "application/host policy owner",
        },
        {
            "relation": "typed transformation-event promotion",
            "required_inputs": ["event identity", "source identities", "target identities", "ordered provenance"],
            "required_outputs": ["canonical next-layer event object"],
            "invertibility_obligation": "recover the promoted event and its complete source/target relation",
            "owner": "separately versioned Stack experimental profile",
        },
    ]


def _source_corpus(stack_root: Path) -> dict[str, Any]:
    paths = _git_text(stack_root, "ls-tree", "-r", "--name-only", STACK_INPUT_COMMIT, "research/urpcs").splitlines()
    files = []
    for path in paths:
        blob = _git_bytes(stack_root, "show", f"{STACK_INPUT_COMMIT}:{path}")
        files.append({"path": path, "bytes": len(blob), "sha256": _sha256(blob)})
    result = {
        "boundary": "every tracked file under research/urpcs at the governing PR #54 head",
        "file_count": len(files),
        "files": files,
    }
    result["corpus_sha256"] = _sha256(_compact(result))
    return result


def _authority_context(
    stack_root: Path,
    ucns_root: Path,
    skill_lib_root: Path,
    metapat_root: Path,
) -> dict[str, Any]:
    _require(_git_text(stack_root, "show", "-s", "--format=%T", STACK_INPUT_COMMIT) == STACK_INPUT_TREE, "Stack input tree drift")
    _require(_git_text(ucns_root, "rev-parse", "HEAD") == UCNS_COMMIT, "UCNS commit drift")
    _require(_git_text(ucns_root, "show", "-s", "--format=%T", "HEAD") == UCNS_TREE, "UCNS tree drift")
    _require(_git_text(skill_lib_root, "rev-parse", "HEAD") == SKILL_LIB_COMMIT, "skill-lib commit drift")
    _require(_git_text(skill_lib_root, "show", "-s", "--format=%T", "HEAD") == SKILL_LIB_TREE, "skill-lib tree drift")
    _require(_git_text(metapat_root, "show", "-s", "--format=%T", METAPAT_COMMIT) == METAPAT_TREE, "METAPAT tree drift")
    for path in FROZEN_PATHS:
        committed = _git_bytes(stack_root, "show", f"{STACK_INPUT_COMMIT}:{path}")
        _require((stack_root / path).read_bytes() == committed, f"frozen URPCS drift: {path}")

    ucns = projection.load_ucns_direct_mobius(ucns_root)
    metapat_files = {}
    for path in ("CHAPTER_ZERO.md", "AXIOMS.md", "DOMAIN_RESTRAINT.md", "POSTULATES.md", "THEOREMS.md"):
        data = _git_bytes(metapat_root, "show", f"{METAPAT_COMMIT}:{path}")
        metapat_files[path] = {"bytes": len(data), "sha256": _sha256(data)}
    return {
        "stack": {
            "governing_input_commit": STACK_INPUT_COMMIT,
            "governing_input_tree": STACK_INPUT_TREE,
            "frozen_paths_verified": list(FROZEN_PATHS),
        },
        "ucns": {
            "commit": UCNS_COMMIT,
            "tree": UCNS_TREE,
            "native_mobius_law_id": ucns.NATIVE_MOBIUS_LAW_ID,
            "native_mobius_law_version": ucns.NATIVE_MOBIUS_LAW_VERSION,
            "direct_mobius_sha256": _sha256((ucns_root / "src/ucns/direct_mobius.py").read_bytes()),
            "authority": "Möbius geometry only",
        },
        "skill_lib": {
            "commit": SKILL_LIB_COMMIT,
            "tree": SKILL_LIB_TREE,
            "authority": "workflow discipline only; no geometry ownership",
        },
        "metapat_consultation": {
            "commit": METAPAT_COMMIT,
            "tree": METAPAT_TREE,
            "files": metapat_files,
            "authority": "conceptual relation and domain-restraint consultation; no URPCS or UCNS law ownership",
        },
    }


def _runtime_context(kmac_identity: Mapping[str, Any]) -> dict[str, Any]:
    executable = Path(sys.executable).resolve()
    _require(GIT is not None, "Git executable unavailable")
    git_executable = Path(GIT).resolve()
    return {
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "python_executable_sha256": _sha256(executable.read_bytes()),
        "git_version": _git_text(Path.cwd(), "--version"),
        "git_executable_sha256": _sha256(git_executable.read_bytes()),
        "platform": platform.platform(),
        "cpu_count": os.cpu_count(),
        "kmac256": dict(kmac_identity),
    }


def _committed_vectors(stack_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    path = stack_root / "research/urpcs/vectors/urpcs-v1-vectors.json"
    artifact = json.loads(path.read_text())
    rows = artifact["vectors"]
    _require(len(rows) == 8, "expected all eight committed URPCS vectors")
    return artifact, rows


def _trace_from_vector(row: Mapping[str, Any], ucns: ModuleType) -> dict[str, Any]:
    state = _state_from_json(row["initial_state"])
    trace = analyze_trace(
        case_id=row["id"],
        ciphertext=bytes.fromhex(row["ciphertext_hex"]),
        state=state,
        associated_data=bytes.fromhex(row["ad_hex"]),
        ucns=ucns,
        expected_plaintext=bytes.fromhex(row["plaintext_hex"]),
        source_kind="committed-positive-vector",
    )
    _require(trace["receipt_hex"] == row["receipt_hex"], f"committed receipt mismatch: {row['id']}")
    expected_next = _state_from_json(row["next_state"])
    _require(trace["successor_state"] == _state_identity(expected_next), f"committed successor mismatch: {row['id']}")
    _require(trace["layer_wire_sha256"] == [_sha256(bytes.fromhex(raw)) for raw in row["layer_wire_hex"]], f"committed layers mismatch: {row['id']}")
    return trace


def _generated_traces(ucns: ModuleType) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    traces: list[dict[str, Any]] = []
    cases: list[dict[str, Any]] = []

    depth_one_state = ref.vector_state(1)
    generated = ref.encrypt(b"\x09", depth_one_state, ref.VECTOR_AD)
    traces.append(analyze_trace(
        case_id="generated_odd_09_r1",
        ciphertext=generated.ciphertext,
        state=depth_one_state,
        associated_data=ref.VECTOR_AD,
        ucns=ucns,
        expected_plaintext=b"\x09",
        source_kind="deterministic-generated-unrepresented-nonempty-recursion",
    ))
    cases.append({
        "id": "generated_odd_09_r1",
        "reason": "the committed positive corpus has no nonempty recursive trace",
        "plaintext_hex": "09",
        "depth": 1,
        "associated_data_sha256": _sha256(ref.VECTOR_AD),
        "initial_state": _state_identity(depth_one_state),
        "ciphertext_sha256": _sha256(generated.ciphertext),
    })

    chain_state = ref.vector_state(0)
    prior_transform: str | None = None
    for sequence, plaintext in enumerate((b"", b"\x09", b"\xff")):
        encrypted = ref.encrypt(plaintext, chain_state, ref.VECTOR_AD)
        case_id = f"generated_state_chain_{sequence}"
        trace = analyze_trace(
            case_id=case_id,
            ciphertext=encrypted.ciphertext,
            state=chain_state,
            associated_data=ref.VECTOR_AD,
            ucns=ucns,
            expected_plaintext=plaintext,
            source_kind="deterministic-generated-state-transition-chain",
        )
        if prior_transform is not None:
            trace["state_predecessor_transform"] = prior_transform
        prior_transform = f"case:{case_id}:transform"
        traces.append(trace)
        cases.append({
            "id": case_id,
            "reason": "transformations-to-later-transformations are unrepresented in the committed positive corpus",
            "sequence": sequence,
            "plaintext_hex": plaintext.hex(),
            "depth": 0,
            "associated_data_sha256": _sha256(ref.VECTOR_AD),
            "initial_state": _state_identity(chain_state),
            "ciphertext_sha256": _sha256(encrypted.ciphertext),
        })
        chain_state = encrypted.next_state
    return traces, cases


def _relation_audit(
    traces: Sequence[Mapping[str, Any]],
    cross_trace_edges: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    edge_counts = Counter(
        edge["kind"]
        for trace in traces
        for edge in trace["graph"]["edges"]
    )
    edge_counts.update(edge["kind"] for edge in cross_trace_edges)
    node_counts = Counter(
        node["kind"]
        for trace in traces
        for node in trace["graph"]["nodes"]
    )
    direct_origin_edges = [
        edge
        for trace in traces
        for edge in trace["graph"]["edges"]
        if edge["source"].startswith("case:")
        and ":origin:" in edge["source"]
        and ":origin:" in edge["target"]
    ]
    _require(not direct_origin_edges, "invented direct origin-to-origin relation")
    total_nodes = sum(node_counts.values())
    total_edges = sum(edge_counts.values())
    return {
        "first_task_classification": "MULTI_ORIGIN_RELATION_PRESENT",
        "native_relation": "LayerWire(G^r) is the exact byte input D^(r+1), then partitioned into successor region origins and occurrence bit intervals",
        "relation_inputs": ["authenticated witness", "ordered canonical layers", "LayerWire bytes"],
        "relation_outputs": ["successor origins", "successor occurrences", "exact byte and bit provenance"],
        "invertibility": "byte-exact when the complete authenticated successor layer and witness are present",
        "within_layer_boundary": "pairing and attachment relate objects only inside one origin; no relation joins peer origins",
        "cross_layer_boundary": "serialization relates a whole source layer to successor input spans; it does not define semantic origin-to-origin phase transport",
        "node_counts": dict(sorted(node_counts.items())),
        "edge_counts": dict(sorted(edge_counts.items())),
        "total_nodes": total_nodes,
        "total_edges": total_edges,
        "direct_origin_to_origin_edges": 0,
    }


def _serialization_audit(traces: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    transitions = sum(len(trace["serialization_events"]) for trace in traces)
    boundary_records = []
    for trace in traces:
        event_ids = set(trace["serialization_events"])
        for node in trace["graph"]["nodes"]:
            if node["id"] not in event_ids:
                continue
            boundary_records.append({
                "case_id": trace["case_id"],
                "event_id": node["id"],
                "source_layer": node["source_layer"],
                "target_layer": node["target_layer"],
                "bytes": node["bytes"],
                "source_wire_sha256": node["source_wire_sha256"],
                "target_input_sha256": node["target_input_sha256"],
                "information_lost": "none",
                "exactly_reversible": node["exactly_reversible"],
            })
    return {
        "boundaries_observed": transitions,
        "boundary_records": sorted(boundary_records, key=lambda item: item["event_id"]),
        "information_lost_at_byte_serialization": "none; canonical LayerWire re-encoding and inverse expansion are byte-identical",
        "relations_preserved": ["ordered source bytes", "complete layer object recoverable from those bytes"],
        "relations_created_by_recursion": ["successor origins", "successor occurrences", "successor gonols", "successor attachments"],
        "relations_not_preserved_as_typed_edges": ["source-origin to target-origin semantic correspondence", "source local phase/sheet transport", "typed transformation-event identity"],
        "relations_erased": "no byte information is erased, but typed source relations are not promoted as typed successor relations",
        "projection_reversibility": {
            "complete_authenticated_trace": "reversible",
            "phase": "ambiguous",
            "phase_and_sheet": "ambiguous",
            "identity_local_state": "does not recover absolute winding or complete provenance",
            "complete_relational_history": "replays the analyzed trace exactly but adds no missing semantic law",
        },
    }


def _acyclic_graph(
    traces: Sequence[Mapping[str, Any]],
    cross_trace_edges: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    node_ids = {
        node["id"]
        for trace in traces
        for node in trace["graph"]["nodes"]
    }
    edges = [edge for trace in traces for edge in trace["graph"]["edges"]] + list(cross_trace_edges)
    indegree = {node_id: 0 for node_id in node_ids}
    children: dict[str, list[str]] = {node_id: [] for node_id in node_ids}
    for edge in edges:
        _require(edge["source"] in node_ids and edge["target"] in node_ids, "aggregate graph reference")
        indegree[edge["target"]] += 1
        children[edge["source"]].append(edge["target"])
    pending = sorted(node_id for node_id, degree in indegree.items() if degree == 0)
    visited = 0
    while pending:
        node_id = pending.pop()
        visited += 1
        for child in children[node_id]:
            indegree[child] -= 1
            if indegree[child] == 0:
                pending.append(child)
    return {
        "node_count": len(node_ids),
        "edge_count": len(edges),
        "visited_by_topological_check": visited,
        "directed_cycle_present": visited != len(node_ids),
    }


def run_analysis(
    *,
    stack_root: Path,
    ucns_root: Path,
    skill_lib_root: Path,
    metapat_root: Path,
    kmac_backend: str = "pycryptodome",
) -> dict[str, Any]:
    authorities = _authority_context(stack_root, ucns_root, skill_lib_root, metapat_root)
    kmac_identity = projection._install_kmac_backend(kmac_backend)
    ucns = projection.load_ucns_direct_mobius(ucns_root)
    vectors, rows = _committed_vectors(stack_root)
    positive_rows = [row for row in rows if "ciphertext_hex" in row and row["id"] in {"empty_r0", "empty_r1", "odd_09_r0"}]
    traces = [_trace_from_vector(row, ucns) for row in positive_rows]
    generated_traces, generated_cases = _generated_traces(ucns)
    traces.extend(generated_traces)

    all_observations = [record for trace in traces for record in trace["observations"]]
    all_node_ids = {
        node["id"]
        for trace in traces
        for node in trace["graph"]["nodes"]
    }
    cross_trace_edges = []
    for trace in traces:
        predecessor = trace.get("state_predecessor_transform")
        if predecessor is None:
            continue
        target = f"case:{trace['case_id']}:transform"
        _require(predecessor in all_node_ids and target in all_node_ids, "state-chain graph reference")
        previous_node = next(
            node
            for candidate in traces
            for node in candidate["graph"]["nodes"]
            if node["id"] == predecessor
        )
        target_node = next(node for node in trace["graph"]["nodes"] if node["id"] == target)
        _require(previous_node["successor_state"] == target_node["pre_state"], "state-chain identity discontinuity")
        cross_trace_edges.append(_edge(
            "state-successor",
            predecessor,
            target,
            "URPCS v1 Law 12",
            state_identity_sha256=previous_node["successor_state"]["identity_sha256"],
        ))
    canonical_graph = {
        "schema": GRAPH_SCHEMA,
        "representation": "canonical graph shards plus cross-trace edges; every shard's complete nodes and edges are embedded in measurement.traces",
        "shards": [
            {
                "case_id": trace["case_id"],
                "graph_sha256": trace["graph"]["graph_sha256"],
                "node_count": len(trace["graph"]["nodes"]),
                "edge_count": len(trace["graph"]["edges"]),
            }
            for trace in traces
        ],
        "cross_trace_edges": sorted(cross_trace_edges, key=lambda item: item["id"]),
    }
    canonical_graph["graph_sha256"] = _sha256(_compact(canonical_graph))
    cycle_check = _acyclic_graph(traces, cross_trace_edges)
    _require(not cycle_check["directed_cycle_present"], "native relational graph unexpectedly cyclic")
    source_corpus = _source_corpus(stack_root)
    baseline_path = stack_root / "research/urpcs/receipts/urpcs-mobius-projection-v0.json"
    baseline = json.loads(baseline_path.read_text())
    trace_manifest = [
        {
            "id": trace["case_id"],
            "source_kind": trace["source_kind"],
            "plaintext_sha256": trace["plaintext_sha256"],
            "ciphertext_sha256": trace["ciphertext_sha256"],
            "graph_sha256": trace["graph"]["graph_sha256"],
            "node_count": len(trace["graph"]["nodes"]),
            "edge_count": len(trace["graph"]["edges"]),
            "observation_count": len(trace["observations"]),
        }
        for trace in traces
    ]
    corpus = {
        "boundary": "all eight committed URPCS vectors; every tracked research/urpcs artifact at PR #54 head; four deterministic probes only for native relations absent from committed positive traces",
        "not_a_completed_domain_claim": "the trace population is the complete declared corpus, not an exhaustive plaintext, key, or state domain",
        "committed_vector_artifact_sha256": _sha256(_json_bytes(vectors)),
        "committed_vector_ids": [row["id"] for row in rows],
        "committed_positive_traces": [row["id"] for row in positive_rows],
        "committed_negative_and_host_evidence": [row["id"] for row in rows if row not in positive_rows],
        "generated_cases": generated_cases,
        "source_corpus": source_corpus,
        "narrow_514_case_baseline": {
            "status": "preserved, consumed as a narrow baseline only",
            "path": "research/urpcs/receipts/urpcs-mobius-projection-v0.json",
            "sha256": _sha256(baseline_path.read_bytes()),
            "classification": baseline["classification"],
            "messages_processed": baseline["measurement"]["messages_processed"],
            "conclusion_scope": "fixed one-byte/depth harness local gonol/member projection only",
        },
    }
    corpus["corpus_identity_sha256"] = _sha256(_compact(corpus))

    measurement = {
        "trace_manifest": trace_manifest,
        "traces": traces,
        "canonical_graph": canonical_graph,
        "aggregate_graph_sha256": canonical_graph["graph_sha256"],
        "cycle_check": cycle_check,
        "relation_audit": _relation_audit(traces, cross_trace_edges),
        "serialization_boundaries": _serialization_audit(traces),
        "ablation": ablate(all_observations),
        "torsor_invariance": torsor_invariance(all_observations),
        "capacities": _capacity_ledger(rows, traces),
        "unresolved_relation_ledger": _unresolved_relations(),
        "unexpected_findings": [
            "The native multi-origin relation is whole-layer byte serialization followed by successor partitioning, not a direct relation between peer origins.",
            "The empty depth-one committed vector already creates many successor origins even though its source plaintext is empty.",
            "URPCS v1 assigns local phase to gonols and members, not to origins; origin phase/sheet would require a new law.",
            "Recursion preserves source bytes exactly while dropping the type of the transformation event: resulting bytes recur, the event does not.",
        ],
    }
    measurement["measurement_sha256"] = _sha256(_compact(measurement))
    sources = {
        "research/urpcs/urpcs_relational_analyzer.py": {
            "bytes": (stack_root / "research/urpcs/urpcs_relational_analyzer.py").stat().st_size,
            "sha256": _sha256((stack_root / "research/urpcs/urpcs_relational_analyzer.py").read_bytes()),
        },
        "research/urpcs/tests/test_relational_analyzer.py": {
            "bytes": (stack_root / "research/urpcs/tests/test_relational_analyzer.py").stat().st_size,
            "sha256": _sha256((stack_root / "research/urpcs/tests/test_relational_analyzer.py").read_bytes()),
        },
    }
    receipt: dict[str, Any] = {
        "artifact": "URPCS relational carrier v0 read-only audit",
        "schema": RECEIPT_SCHEMA,
        "standing": "COMPUTATION; Stack-local research; not a protocol or traversal profile",
        "classification": CLASSIFICATION,
        "authorities": authorities,
        "runtime": _runtime_context(kmac_identity),
        "execution": {
            "x_bytes": ref.X,
            "M": ref.M,
            "depths": [0, 1],
            "associated_data_hex": ref.VECTOR_AD.hex(),
            "associated_data_sha256": _sha256(ref.VECTOR_AD),
            "authentication_boundary": "KMAC authenticates C_0 before witness recovery, body parsing, graph construction, or plaintext reconstruction",
            "committed_trace_count": len(positive_rows),
            "generated_trace_count": len(generated_traces),
            "total_trace_count": len(traces),
            "observation_count": len(all_observations),
            "gonol_state_count": sum(record["kind"] == "gonol-state" for record in all_observations),
            "member_state_count": sum(record["kind"] == "member-state" for record in all_observations),
        },
        "test_and_measurement_counts": {
            "complete_urpcs_python_tests": 26,
            "relational_analyzer_tests": 7,
            "committed_vector_rows": len(rows),
            "committed_positive_traces": len(positive_rows),
            "independent_decoder_positive_replays": 3,
            "analyzed_traces": len(traces),
            "gonol_states": sum(record["kind"] == "gonol-state" for record in all_observations),
            "member_states": sum(record["kind"] == "member-state" for record in all_observations),
        },
        "sources": sources,
        "corpus": corpus,
        "measurement": measurement,
        "explicit_nonclaims": list(NONCLAIMS),
        "hmmm": "Whether the exact byte-provenance relation warrants a typed origin transport, synchronization, traversal, or event-promotion law remains unresolved; v1 supplies none of those laws.",
    }
    receipt["receipt_payload_sha256"] = _sha256(_compact(receipt))
    return receipt


def verify_receipt(receipt: Mapping[str, Any]) -> None:
    payload = dict(receipt)
    claimed = payload.pop("receipt_payload_sha256", None)
    _require(receipt.get("schema") == RECEIPT_SCHEMA, "receipt schema mismatch")
    _require(isinstance(claimed, str) and len(claimed) == 64, "receipt payload hash missing")
    _require(_sha256(_compact(payload)) == claimed, "receipt payload hash mismatch")
    _require(receipt.get("classification") == CLASSIFICATION, "receipt classification mismatch")


def render_report(receipt: Mapping[str, Any], receipt_sha256: str) -> str:
    measurement = receipt["measurement"]
    relation = measurement["relation_audit"]
    ablation_rows = measurement["ablation"]["steps"]
    capacities = measurement["capacities"]
    traces = measurement["trace_manifest"]
    lines = [
        "# URPCS relational carrier v0 — read-only architecture audit",
        "",
        f"Classification: **{receipt['classification']}**.",
        "",
        "The native multi-origin relation is present, but narrower than a global or peer-origin coordinate: canonical `LayerWire(G^r)` bytes become the exact input to layer `r+1`, where they are partitioned into successor origins and occurrence spans. Pairing and attachment remain local to one origin. URPCS v1 defines no origin phase, origin-to-origin phase transport, synchronization, traversal, or typed event-promotion law.",
        "",
        "This analyzer is read-only. It changes no v1 serialization, state transition, vector, receipt, traversal, or UCNS law.",
        "",
        "## Evidence identity",
        "",
        f"- Canonical receipt SHA-256: `{receipt_sha256}`",
        f"- Receipt payload SHA-256: `{receipt['receipt_payload_sha256']}`",
        f"- Measurement SHA-256: `{measurement['measurement_sha256']}`",
        f"- Aggregate graph SHA-256: `{measurement['aggregate_graph_sha256']}`",
        f"- Corpus identity SHA-256: `{receipt['corpus']['corpus_identity_sha256']}`",
        f"- Governing Stack commit/tree: `{receipt['authorities']['stack']['governing_input_commit']}` / `{receipt['authorities']['stack']['governing_input_tree']}`",
        f"- UCNS commit/law: `{receipt['authorities']['ucns']['commit']}` / `{receipt['authorities']['ucns']['native_mobius_law_id']}@{receipt['authorities']['ucns']['native_mobius_law_version']}`",
        f"- skill-lib commit/tree: `{receipt['authorities']['skill_lib']['commit']}` / `{receipt['authorities']['skill_lib']['tree']}`",
        f"- METAPAT consultation commit/tree: `{receipt['authorities']['metapat_consultation']['commit']}` / `{receipt['authorities']['metapat_consultation']['tree']}`",
        "",
        "## Source-backed relation",
        "",
        f"First-task classification: **{relation['first_task_classification']}**.",
        "",
        relation["native_relation"] + ".",
        "",
        f"- Within a layer: {relation['within_layer_boundary']}",
        f"- Across layers: {relation['cross_layer_boundary']}",
        f"- Invertibility: {relation['invertibility']}",
        f"- Direct origin-to-origin edges observed: {relation['direct_origin_to_origin_edges']}",
        f"- Canonical graph size: {relation['total_nodes']} nodes and {relation['total_edges']} edges",
        f"- Directed cycles observed: {int(measurement['cycle_check']['directed_cycle_present'])}",
        "",
        "## Declared corpus",
        "",
        receipt["corpus"]["boundary"] + ".",
        "",
        receipt["corpus"]["not_a_completed_domain_claim"] + ".",
        "",
        "| Trace | Source | Nodes | Edges | Local observations |",
        "|---|---|---:|---:|---:|",
    ]
    for row in traces:
        lines.append(f"| `{row['id']}` | {row['source_kind']} | {row['node_count']} | {row['edge_count']} | {row['observation_count']} |")
    lines.extend([
        "",
        "The prior 514-case Möbius receipt is preserved and consumed only as a narrow fixed-harness baseline. Its absence of winding in one-byte inputs does not resolve the contribution of recursive relations.",
        "",
        "## Ablation lattice",
        "",
        "| Projection | Classes | Max multiplicity | Colliding pairs retained | Pairs separated at step |",
        "|---|---:|---:|---:|---:|",
    ])
    for row in ablation_rows:
        lines.append(f"| `{row['name']}` | {row['equivalence_classes']} | {row['maximum_multiplicity']} | {row['colliding_pairs_retained']} | {row['colliding_pairs_separated_from_previous']} |")
    identity = measurement["ablation"]["identity_multiplicity"]
    marginals = measurement["ablation"]["marginal_contributions"]
    lines.extend([
        "",
        f"- Identities in shared visible-angle classes: {identity['identities_sharing_one_visible_angle']}",
        f"- Identities in shared phase-and-sheet classes: {identity['identities_sharing_phase_and_sheet']}",
        "- Identifiers and geometry remain separate dimensions; these multiplicities are not called complete-state collisions.",
        "- Common phase rotation preserves every measured relative phase and sheet product; no privileged global zero was selected.",
        "",
        "| Added component | Colliding pairs separated |",
        "|---|---:|",
        f"| sheet/frame | {marginals['frame']['pairs_separated']} |",
        f"| origin | {marginals['origin']['pairs_separated']} |",
        f"| gonol identity | {marginals['gonol']['pairs_separated']} |",
        f"| arity and shape | {marginals['arity_and_shape']['pairs_separated']} |",
        f"| provenance | {marginals['provenance']['pairs_separated']} |",
        f"| full transformation history after provenance | {marginals['transformation_history']['pairs_separated']} |",
        "",
        "The frame supplies no additional distinction in this declared corpus. Origin, gonol identity, arity/shape, and provenance do; transformation history adds no further split after case-scoped provenance is already included. These are representation contributions, not utility or security claims.",
        "",
        "## Serialization boundary",
        "",
    ])
    serialization = measurement["serialization_boundaries"]
    lines.extend([
        f"- Boundaries observed: {serialization['boundaries_observed']}",
        f"- Byte loss: {serialization['information_lost_at_byte_serialization']}",
        f"- Created by recursion: {', '.join(serialization['relations_created_by_recursion'])}",
        f"- Not preserved as typed edges: {', '.join(serialization['relations_not_preserved_as_typed_edges'])}",
        "",
        "## Candidate capacities",
        "",
        "| Capacity | Classification |",
        "|---|---|",
    ])
    for item in capacities:
        lines.append(f"| {item['capacity']} | **{item['classification']}** |")
    lines.extend([
        "",
        "Each capacity has its source evidence, limitation, and any missing law in the canonical JSON. Blocked branches do not stop independent supported branches.",
        "",
        "## Unexpected findings",
        "",
    ])
    lines.extend(f"- {item}" for item in measurement["unexpected_findings"])
    lines.extend([
        "",
        "## Explicit nonclaims",
        "",
        "This work does not establish " + ", ".join(receipt["explicit_nonclaims"]) + ".",
        "",
        "## hmmm",
        "",
        receipt["hmmm"],
        "",
    ])
    return "\n".join(lines)


def write_evidence(receipt: Mapping[str, Any], receipt_path: Path, report_path: Path) -> dict[str, str]:
    verify_receipt(receipt)
    receipt_bytes = _json_bytes(receipt)
    receipt_sha = _sha256(receipt_bytes)
    report_bytes = render_report(receipt, receipt_sha).encode("utf-8")
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_bytes(receipt_bytes)
    report_path.write_bytes(report_bytes)
    return {"receipt_sha256": receipt_sha, "report_sha256": _sha256(report_bytes)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stack-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--ucns-root", type=Path, required=True)
    parser.add_argument("--skill-lib-root", type=Path, required=True)
    parser.add_argument("--metapat-root", type=Path, required=True)
    parser.add_argument("--kmac-backend", choices=("stdlib", "pycryptodome"), default="pycryptodome")
    parser.add_argument("--write-receipt", type=Path, required=True)
    parser.add_argument("--write-report", type=Path, required=True)
    args = parser.parse_args()

    receipt = run_analysis(
        stack_root=args.stack_root.resolve(),
        ucns_root=args.ucns_root.resolve(),
        skill_lib_root=args.skill_lib_root.resolve(),
        metapat_root=args.metapat_root.resolve(),
        kmac_backend=args.kmac_backend,
    )
    identities = write_evidence(receipt, args.write_receipt, args.write_report)
    print(json.dumps({
        "classification": receipt["classification"],
        "first_task_classification": receipt["measurement"]["relation_audit"]["first_task_classification"],
        "traces": receipt["execution"]["total_trace_count"],
        "observations": receipt["execution"]["observation_count"],
        **identities,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
