#!/usr/bin/env python3
"""Bounded, read-only Möbius-state measurement for URPCS v1 witnesses.

This adapter authenticates a frozen URPCS v1 frame before recovering its
witness, reconstructs unreduced root-to-gonol displacements, and projects those
exact integers through UCNS's native Möbius law.  It does not change or extend
the URPCS wire format or operational codec behavior.
"""

# === MODULE_BUILD ===
# id: urpcs_mobius_projection
#   module_name: urpcs_mobius_projection
#   module_kind: experiment
#   summary: read-only bounded measurement of UCNS native Mobius state derivable from authenticated URPCS v1 witnesses
#   owner: The-Interdependency/stack research/urpcs
#   public_surface: project_authenticated_frame, reconstruct_path_sums, run_measurement, command-line receipt writer
#   internal_surface: exact UCNS loader, deterministic split-record encoding, bounded harness runner
#   auth_boundary: read
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   tests: research/urpcs/tests/test_mobius_projection.py
#   rollout: stack-local measurement only; no protocol profile or traversal behavior
#   rollback: remove this adapter, its tests, report, receipt, and README entry
#   since: 2026-09-23
#   unresolved: whether an opposite-frame phase distinction exists outside the fixed bounded harness
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: urpcs_projection_authenticates_first
#   given: a URPCS v1 ciphertext, pre-message state, and associated data
#   then: C_0 authentication succeeds before bootstrap parsing, witness recovery, or state projection
#   class: security
#   since: 2026-09-23
#
# id: urpcs_projection_matches_ucns
#   given: a valid authenticated witness and exact unreduced displacement S under modulus M
#   then: the projected phase and frame equal UCNS native_mobius_state(Fraction(S, M))
#   class: correctness
#   since: 2026-09-23
#
# id: urpcs_projection_evidence_is_deterministic
#   given: identical source identities, harness inputs, runtime, and dependency identities
#   then: the canonical measurement payload and generated Markdown report are byte-identical
#   class: evidence
#   since: 2026-09-23
# === END CONTRACTS ===

# === BOUNDARIES ===
# id: urpcs_projection_research_boundary
#   summary: consumes authenticated Stack-local research witnesses and emits public measurement evidence without modifying codec behavior
#   auth_boundary: read
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   pii: none
#   secrets: none
#   review_required: exact source-identity and frozen-wire review before evidence regeneration
#   owner: The-Interdependency/stack research/urpcs
# === END BOUNDARIES ===

# === DEPENDENCIES ===
# id: urpcs_mobius_projection_dependency_edges
#   summary: the adapter consumes the frozen URPCS witness contract and delegates exact local-state geometry to the pinned UCNS native Möbius law
#   imports: urpcs_v1_reference
#   calls: urpcs_v1_reference.tag, urpcs_v1_reference.decode_witness, ucns.native_mobius_state
#   external: PyCryptodome KMAC256 3.23.0 as an optional measured-run accelerator
#   class: runtime
#   direction: outbound
#   owner: The-Interdependency/stack research/urpcs
#   since: 2026-09-23
# === END DEPENDENCIES ===

# === DOCS ===
# id: urpcs_mobius_projection_measurement_docs
#   summary: authority, reproduction, measured result, interpretation boundary, and nonclaims for the bounded projection
#   audience: developer
#   source: research/urpcs/docs/URPCS-mobius-projection-v0.md
#   covers: project_authenticated_frame, reconstruct_path_sums, run_measurement, canonical receipt
#   status: current
#   owner: The-Interdependency/stack research/urpcs
#   since: 2026-09-23
# === END DOCS ===

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import importlib.util
import json
import multiprocessing
import os
import platform
import shutil
import struct
# Subprocesses below are fixed-argv Git identity checks, never a shell.
import subprocess  # nosec B404
import sys
import zlib
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable, Mapping, Sequence

import urpcs_v1_reference as ref


class ProjectionError(ValueError):
    """Raised when authenticated witness geometry cannot be projected exactly."""


STACK_INPUT_COMMIT = "2fadd145db09e352f84146fa490be03dbfa708d4"
STACK_INPUT_TREE = "1d0aa08624ccb6c618b852779b5f1688514f8cdc"
STACK_EQUIVALENCE_COMMIT = "1f9a35eb355296fc88d09784c7a3e2e95511ca31"
UCNS_COMMIT = "4086ab82399c4d142b0eacfbc09e0a69ed151aa5"
UCNS_TREE = "3b9c3143c86e07d497eebfbcb32a0f14a1a1ab3b"
UCNS_DIRECT_MOBIUS_BLOB = "14a4cee36b5bbfa72cf3c03703c427abdac7f33d"
UCNS_DIRECT_MOBIUS_SHA256 = "d8d1360c753dac7431071e007c5105a21b5396dd9e2f7e5ba4089d99e056a5bf"
UCNS_LAW_ID = "ucns.native-mobius-root-loop"
UCNS_LAW_VERSION = "1.0.0"
SKILL_LIB_COMMIT = "abd259b4722901317e4388d774a20d6819d959c2"
SKILL_LIB_TREE = "a037194960130e07d3a5cbd7d1cf8918c6422e50"

PHASE_FRAMES = ("positive-local-frame", "reversed-local-frame")
CLASSIFICATIONS = (
    "DISTINCTION_PRESENT",
    "DISTINCTION_ABSENT_IN_BOUNDED_DOMAIN",
    "INCOMPLETE",
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
GIT_EXECUTABLE = shutil.which("git")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ProjectionError(message)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _file_sha256(path: Path) -> str:
    return _sha256(path.read_bytes())


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode("utf-8")


def _compact_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def _git(repo: Path, *args: str) -> str:
    _require(GIT_EXECUTABLE is not None, "Git executable unavailable")
    # Repository paths and fixed Git arguments are separate argv entries; no shell.
    result = subprocess.run(  # nosec B603
        [GIT_EXECUTABLE, "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def load_ucns_direct_mobius(ucns_root: Path) -> ModuleType:
    """Load the exact producer module without importing unrelated UCNS surfaces."""

    source = ucns_root / "src" / "ucns" / "direct_mobius.py"
    _require(source.is_file(), f"missing UCNS native Möbius source: {source}")
    _require(_file_sha256(source) == UCNS_DIRECT_MOBIUS_SHA256, "UCNS native Möbius source hash drift")
    name = "_urpcs_pinned_ucns_direct_mobius"
    spec = importlib.util.spec_from_file_location(name, source)
    _require(spec is not None and spec.loader is not None, "cannot load UCNS native Möbius source")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    _require(module.NATIVE_MOBIUS_LAW_ID == UCNS_LAW_ID, "UCNS native Möbius law identity drift")
    _require(module.NATIVE_MOBIUS_LAW_VERSION == UCNS_LAW_VERSION, "UCNS native Möbius law version drift")
    return module


def euclidean_mobius_state(displacement: int, modulus: int, ucns: ModuleType) -> dict[str, Any]:
    """Project an integer displacement and prove exact agreement with UCNS."""

    _require(isinstance(displacement, int) and not isinstance(displacement, bool), "displacement must be an integer")
    _require(isinstance(modulus, int) and not isinstance(modulus, bool) and modulus > 0, "invalid modulus")
    quotient, remainder = divmod(displacement, modulus)
    expected_frame = PHASE_FRAMES[quotient & 1]
    native = ucns.native_mobius_state(Fraction(displacement, modulus))
    _require(native.phase_turns == Fraction(remainder, modulus), "UCNS phase disagreement")
    _require(native.frame.value == expected_frame, "UCNS frame disagreement")
    return {
        "S": displacement,
        "q": quotient,
        "phase": f"({remainder},{modulus})",
        "phase_numerator": remainder,
        "phase_modulus": modulus,
        "frame": expected_frame,
    }


def reconstruct_path_sums(
    node_scopes: Mapping[bytes, bytes],
    attachments: Iterable[tuple[bytes, bytes]],
    displacements: Mapping[tuple[bytes, bytes], int],
) -> dict[bytes, int]:
    """Validate a scoped rooted forest and return exact root-to-node sums."""

    nodes = set(node_scopes)
    edges = list(attachments)
    _require(len(edges) == len(set(edges)), "duplicate attachment")
    children: dict[bytes, list[bytes]] = {node: [] for node in nodes}
    parent: dict[bytes, bytes] = {}
    edge_set = set(edges)
    _require(set(displacements) == edge_set, "missing or extra displacement")
    for parent_id, child_id in edges:
        _require(parent_id in nodes and child_id in nodes, "inconsistent witness reference")
        _require(parent_id != child_id, "self attachment")
        _require(node_scopes[parent_id] == node_scopes[child_id], "cross-scope attachment")
        _require(child_id not in parent, "duplicate parent")
        delta = displacements[(parent_id, child_id)]
        _require(isinstance(delta, int) and not isinstance(delta, bool), "displacement must be an integer")
        parent[child_id] = parent_id
        children[parent_id].append(child_id)

    scopes: dict[bytes, set[bytes]] = {}
    for node, scope in node_scopes.items():
        scopes.setdefault(scope, set()).add(node)

    sums: dict[bytes, int] = {}
    for scope in sorted(scopes):
        scoped_nodes = scopes[scope]
        roots = sorted(node for node in scoped_nodes if node not in parent)
        _require(len(roots) == 1, "malformed forest root count")
        root = roots[0]
        sums[root] = 0
        pending = [root]
        visited: set[bytes] = set()
        while pending:
            node = pending.pop()
            _require(node not in visited, "attachment cycle")
            visited.add(node)
            for child in sorted(children[node], reverse=True):
                sums[child] = sums[node] + displacements[(node, child)]
                pending.append(child)
        _require(visited == scoped_nodes, "malformed forest is disconnected or cyclic")
    return sums


def authenticated_witness(ciphertext: bytes, state: ref.KState, associated_data: bytes) -> tuple[list[Any], dict[str, Any], bytes, bytes]:
    """Authenticate C_0, then and only then parse the bootstrap and witness."""

    state.validate()
    c0, received_tag = ref.unframe(ciphertext)
    expected_tag = ref.tag(state, c0, associated_data)
    ref.require(hmac.compare_digest(received_tag, expected_tag), "tag verification")

    # No bootstrap or witness byte is inspected above this boundary.
    ref.require(len(c0) >= ref.BOOT_HEADER_LEN, "short bootstrap")
    magic, version, header_len, beta_len, flags = struct.unpack(">8sHHQI", c0[:ref.BOOT_HEADER_LEN])
    ref.require(
        magic == ref.BOOT_MAGIC and version == 1 and header_len == ref.BOOT_HEADER_LEN and flags == 0,
        "bootstrap identity",
    )
    ref.require(beta_len <= len(c0) - ref.BOOT_HEADER_LEN, "bootstrap length overflow")
    beta = c0[ref.BOOT_HEADER_LEN:ref.BOOT_HEADER_LEN + beta_len]
    body = c0[ref.BOOT_HEADER_LEN + beta_len:]
    witness, index = ref.decode_witness(beta, state)
    return witness, index, beta, body


def _record_bytes(
    *,
    kind: str,
    case_index: int,
    layer: int,
    region: int,
    displacement: int,
    gonol_id: bytes,
    occurrence_id: bytes | None = None,
    local_displacement: int | None = None,
) -> bytes:
    _require(0 <= case_index <= 0xFFFF, "case index range")
    _require(0 <= layer <= 0xFFFFFFFF and 0 <= region <= 0xFFFFFFFF, "layer/region range")
    _require(-(1 << 63) <= displacement < (1 << 63), "displacement encoding range")
    _require(len(gonol_id) <= 0xFFFF, "gonol identifier encoding range")
    payload = struct.pack(">HIIqH", case_index, layer, region, displacement, len(gonol_id)) + gonol_id
    if kind == "member":
        _require(occurrence_id is not None and local_displacement is not None, "member record fields")
        _require(len(occurrence_id) <= 0xFFFF, "occurrence identifier encoding range")
        payload += struct.pack(">H", len(occurrence_id)) + occurrence_id + struct.pack(">q", local_displacement)
    else:
        _require(kind == "gonol" and occurrence_id is None and local_displacement is None, "gonol record fields")
    return struct.pack(">I", len(payload)) + payload


def _record_preview(
    *,
    kind: str,
    case_index: int,
    layer: int,
    region: int,
    displacement: int,
    state: Mapping[str, Any],
    gonol_id: bytes,
    occurrence_id: bytes | None = None,
    local_displacement: int | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "case_index": case_index,
        "layer": layer,
        "region": region,
        "gonol_id_hex": gonol_id.hex(),
        "S": displacement,
        "q": state["q"],
        "phase": state["phase"],
        "frame": state["frame"],
    }
    if kind == "member":
        result["occurrence_id_hex"] = occurrence_id.hex() if occurrence_id is not None else None
        result["local_displacement"] = local_displacement
    return result


def project_witness(
    witness: list[Any],
    index: Mapping[str, Any],
    case_index: int,
    modulus: int,
    ucns: ModuleType,
) -> dict[str, Any]:
    """Reconstruct and project gonol/member states from validated witness rows."""

    _require(modulus > 0, "invalid modulus")
    gonols: Mapping[bytes, Mapping[str, Any]] = index["gonols"]
    origins: Mapping[bytes, tuple[int, int]] = index["origins"]
    node_scopes = {gid: item["origin"] for gid, item in gonols.items()}

    attach_rows = witness[1][4]
    delta_rows = witness[2]
    attachments: list[tuple[bytes, bytes]] = []
    for parent, child, layer_raw in attach_rows:
        _require(parent in gonols and child in gonols, "inconsistent witness reference")
        layer = ref.n_value(layer_raw)
        _require(origins[gonols[parent]["origin"]][0] == layer, "attachment layer mismatch")
        attachments.append((parent, child))
    displacements: dict[tuple[bytes, bytes], int] = {}
    for parent, child, delta_raw in delta_rows:
        edge = (parent, child)
        _require(edge not in displacements, "duplicate displacement")
        displacements[edge] = ref.n_value(delta_raw)

    sums = reconstruct_path_sums(node_scopes, attachments, displacements) if gonols else {}
    buckets: dict[str, dict[str, bytearray]] = {
        "gonol": {},
        "member": {},
    }
    previews: dict[str, dict[str, dict[str, Any]]] = {"gonol": {}, "member": {}}
    stats = {
        "gonol": {"states": 0, "maximum_S": None, "maximum_q": None},
        "member": {"states": 0, "maximum_S": None, "maximum_q": None},
    }

    def add(
        kind: str,
        gid: bytes,
        occurrence: bytes | None,
        local: int | None,
        displacement: int,
    ) -> None:
        origin = gonols[gid]["origin"]
        layer, region = origins[origin]
        state = euclidean_mobius_state(displacement, modulus, ucns)
        bucket_key = state["phase"] + "|" + state["frame"]
        encoded = _record_bytes(
            kind=kind,
            case_index=case_index,
            layer=layer,
            region=region,
            displacement=displacement,
            gonol_id=gid,
            occurrence_id=occurrence,
            local_displacement=local,
        )
        buckets[kind].setdefault(bucket_key, bytearray()).extend(encoded)
        previews[kind].setdefault(
            bucket_key,
            _record_preview(
                kind=kind,
                case_index=case_index,
                layer=layer,
                region=region,
                displacement=displacement,
                state=state,
                gonol_id=gid,
                occurrence_id=occurrence,
                local_displacement=local,
            ),
        )
        item = stats[kind]
        item["states"] += 1
        item["maximum_S"] = displacement if item["maximum_S"] is None else max(item["maximum_S"], displacement)
        item["maximum_q"] = state["q"] if item["maximum_q"] is None else max(item["maximum_q"], state["q"])

    ordered_gonols = sorted(
        gonols,
        key=lambda gid: (origins[gonols[gid]["origin"]], gid),
    )
    for gid in ordered_gonols:
        baseline = sums[gid]
        add("gonol", gid, None, None, baseline)
        members = sorted(gonols[gid]["members"])
        for member_index, occurrence in enumerate(members):
            _require(occurrence in index["occurrences"], "inconsistent witness reference")
            local = 0 if len(members) == 1 or member_index == 0 else modulus // 2
            add("member", gid, occurrence, local, baseline + local)

    return {
        "buckets": {kind: {key: bytes(value) for key, value in sorted(kind_buckets.items())} for kind, kind_buckets in buckets.items()},
        "previews": {kind: dict(sorted(values.items())) for kind, values in previews.items()},
        "stats": stats,
    }


def project_authenticated_frame(
    ciphertext: bytes,
    state: ref.KState,
    associated_data: bytes,
    case_index: int,
    modulus: int,
    ucns: ModuleType,
) -> tuple[dict[str, Any], dict[str, str]]:
    witness, index, beta, body = authenticated_witness(ciphertext, state, associated_data)
    projected = project_witness(witness, index, case_index, modulus, ucns)
    identities = {
        "ciphertext_sha256": _sha256(ciphertext),
        "c0_sha256": _sha256(ref.unframe(ciphertext)[0]),
        "witness_beta_sha256": _sha256(beta),
        "authenticated_body_sha256": _sha256(body),
    }
    return projected, identities


def _install_kmac_backend(name: str) -> dict[str, Any]:
    """Install an explicitly identified KMAC backend after exact KAT checks."""

    stdlib_kmac = ref.kmac256
    sample_key = bytes(range(0x40, 0x60))
    sample_message = bytes.fromhex("00010203")
    sample_expected = bytes.fromhex(
        "2ebd1622de2de44174e3477206060d7f64489a639b7545649132317609fa214f"
        "4c8ac90630fb4c757fba074b15186fe452ae71b6a1e443bf54059e090c11ae20"
    )
    _require(stdlib_kmac(sample_key, sample_message, 64, b"") == sample_expected, "stdlib KMAC256 KAT failure")
    if name == "stdlib":
        return {
            "name": "URPCS dependency-free KMAC256",
            "version": "frozen-v1",
            "official_sample_4_sha256": _sha256(sample_expected),
            "official_sample_4_output_hex": sample_expected.hex(),
        }
    _require(name == "pycryptodome", f"unknown KMAC backend: {name}")
    try:
        import Crypto
        # Bandit B413 conflates PyCryptodome's maintained ``Crypto`` namespace
        # with abandoned PyCrypto.  The exact distribution/version and module
        # hash are recorded below and the implementation must pass NIST Sample 4.
        from Crypto.Hash import KMAC256  # nosec B413
    except ImportError as exc:
        raise ProjectionError("pycryptodome backend unavailable") from exc

    def fast_kmac(key: bytes, data: bytes, output_len: int, custom: bytes) -> bytes:
        return KMAC256.new(key=key, data=data, mac_len=output_len, custom=custom).digest()

    _require(fast_kmac(sample_key, sample_message, 64, b"") == sample_expected, "external KMAC256 KAT failure")
    probes = (
        (bytes(range(32)), b"", 32, b"URPCS/PAIR/v1"),
        (bytes(range(32, 64)), b"probe", 32, b"URPCS/TAG/v1"),
    )
    for args in probes:
        _require(fast_kmac(*args) == stdlib_kmac(*args), "external KMAC256/URPCS implementation disagreement")
    ref.kmac256 = fast_kmac
    module_path = Path(KMAC256.__file__).resolve()
    return {
        "name": "pycryptodome Crypto.Hash.KMAC256",
        "version": Crypto.__version__,
        "module_path": str(module_path),
        "module_sha256": _file_sha256(module_path),
        "official_sample_4_sha256": _sha256(sample_expected),
        "official_sample_4_output_hex": sample_expected.hex(),
        "agrees_with_urpcs_reference_probes": len(probes),
    }


_WORKER_UCNS: ModuleType | None = None
_WORKER_MODULUS = ref.M


def _worker_init(ucns_root: str, modulus: int, kmac_backend: str) -> None:
    global _WORKER_UCNS, _WORKER_MODULUS
    _install_kmac_backend(kmac_backend)
    _WORKER_UCNS = load_ucns_direct_mobius(Path(ucns_root))
    _WORKER_MODULUS = modulus


def _state_identity(state: ref.KState) -> dict[str, Any]:
    fields = {
        "k_pair_sha256": _sha256(state.pair),
        "k_integrity_sha256": _sha256(state.integrity),
        "k_advance_sha256": _sha256(state.advance),
        "nu_origin_sha256": _sha256(state.origin),
        "R_cap": state.depth,
    }
    fields["identity_sha256"] = _sha256(_compact_json_bytes(fields))
    return fields


def bounded_cases(depths: Sequence[int] = (0, 1), values: Sequence[bytes] | None = None) -> list[dict[str, Any]]:
    plaintexts = [b""] + [bytes([value]) for value in range(256)] if values is None else list(values)
    cases: list[dict[str, Any]] = []
    for depth in depths:
        _require(depth in (0, 1), "depth outside frozen harness")
        state_identity = _state_identity(ref.vector_state(depth))
        for plaintext in plaintexts:
            _require(len(plaintext) <= 1, "plaintext outside frozen harness")
            item = {
                "case_index": len(cases),
                "case_id": f"r{depth}-" + ("empty" if not plaintext else plaintext.hex()),
                "R_cap": depth,
                "plaintext_hex": plaintext.hex(),
                "plaintext_sha256": _sha256(plaintext),
                "initial_state_identity_sha256": state_identity["identity_sha256"],
            }
            item["input_identity_sha256"] = _sha256(_compact_json_bytes(item))
            cases.append(item)
    return cases


def _worker_case(case: Mapping[str, Any]) -> dict[str, Any]:
    _require(_WORKER_UCNS is not None, "worker UCNS law not initialized")
    plaintext = bytes.fromhex(case["plaintext_hex"])
    state = ref.vector_state(case["R_cap"])
    encrypted = ref.encrypt(plaintext, state, ref.VECTOR_AD)
    projected, identities = project_authenticated_frame(
        encrypted.ciphertext,
        state,
        ref.VECTOR_AD,
        case["case_index"],
        _WORKER_MODULUS,
        _WORKER_UCNS,
    )
    case_projection = {
        "case_index": case["case_index"],
        "case_id": case["case_id"],
        **identities,
        "urpcs_trace_receipt_hex": encrypted.receipt.hex(),
        "urpcs_trace_receipt_sha256": _sha256(encrypted.receipt),
        "gonol_states": projected["stats"]["gonol"]["states"],
        "member_states": projected["stats"]["member"]["states"],
        "gonol_projection_sha256": _sha256(b"".join(projected["buckets"]["gonol"].values())),
        "member_projection_sha256": _sha256(b"".join(projected["buckets"]["member"].values())),
    }
    case_projection["result_identity_sha256"] = _sha256(_compact_json_bytes(case_projection))
    return {
        "case": dict(case),
        "case_projection": case_projection,
        "buckets": projected["buckets"],
        "previews": projected["previews"],
        "stats": projected["stats"],
    }


def _bucket_count(blob: bytes) -> int:
    position = 0
    count = 0
    while position < len(blob):
        _require(position + 4 <= len(blob), "truncated record length")
        size = struct.unpack(">I", blob[position:position + 4])[0]
        position += 4
        _require(position + size <= len(blob), "truncated record payload")
        position += size
        count += 1
    _require(position == len(blob), "record encoding length mismatch")
    return count


def _split_key(key: str) -> tuple[str, str]:
    phase, frame = key.split("|", 1)
    _require(frame in PHASE_FRAMES, "invalid frame bucket")
    return phase, frame


def _finalize_kind(
    kind: str,
    bucket_blobs: Mapping[str, bytes],
    previews: Mapping[str, Mapping[str, Any]],
    states: int,
    maximum_s: int | None,
    maximum_q: int | None,
) -> dict[str, Any]:
    phase_frames: dict[str, set[str]] = {}
    counts = {key: _bucket_count(blob) for key, blob in bucket_blobs.items()}
    _require(sum(counts.values()) == states, f"{kind} state count mismatch")
    for key in bucket_blobs:
        phase, frame = _split_key(key)
        phase_frames.setdefault(phase, set()).add(frame)
    split_phases = sorted(phase for phase, frames in phase_frames.items() if len(frames) == 2)
    split_records = sum(counts[f"{phase}|{frame}"] for phase in split_phases for frame in PHASE_FRAMES)
    split_evidence = []
    for phase in split_phases:
        frame_entries = []
        for frame in PHASE_FRAMES:
            key = f"{phase}|{frame}"
            raw = bucket_blobs[key]
            compressed = zlib.compress(raw, level=9)
            frame_entries.append({
                "frame": frame,
                "record_count": counts[key],
                "records_uncompressed_bytes": len(raw),
                "records_uncompressed_sha256": _sha256(raw),
                "records_zlib_bytes": len(compressed),
                "records_zlib_sha256": _sha256(compressed),
                "records_zlib_base64": base64.b64encode(compressed).decode("ascii"),
                "first_record": previews[key],
            })
        split_evidence.append({"phase": phase, "frames": frame_entries})
    all_records = b"".join(bucket_blobs[key] for key in sorted(bucket_blobs))
    return {
        "states": states,
        "distinct_phase_buckets": len(phase_frames),
        "distinct_phase_frame_buckets": len(bucket_blobs),
        "opposite_frame_phase_buckets": len(split_phases),
        "records_in_opposite_frame_phase_buckets": split_records,
        "maximum_S": maximum_s,
        "maximum_q": maximum_q,
        "all_records_sha256": _sha256(all_records),
        "opposite_frame_phase_splits": split_evidence,
    }


def run_measurement(
    *,
    ucns_root: Path,
    jobs: int,
    kmac_backend: str,
    depths: Sequence[int] = (0, 1),
    values: Sequence[bytes] | None = None,
    modulus: int = ref.M,
) -> dict[str, Any]:
    """Run the declared deterministic domain and return its canonical measurement."""

    _require(jobs >= 1, "jobs must be positive")
    _require(modulus > 0, "invalid modulus")
    cases = bounded_cases(depths, values)
    aggregate: dict[str, dict[str, bytearray]] = {"gonol": {}, "member": {}}
    previews: dict[str, dict[str, dict[str, Any]]] = {"gonol": {}, "member": {}}
    totals = {
        "gonol": {"states": 0, "maximum_S": None, "maximum_q": None},
        "member": {"states": 0, "maximum_S": None, "maximum_q": None},
    }
    case_results: list[dict[str, Any]] = []

    def consume(result: Mapping[str, Any]) -> None:
        expected_index = len(case_results)
        _require(result["case"]["case_index"] == expected_index, "case ordering drift")
        case_results.append(result["case_projection"])
        for kind in ("gonol", "member"):
            for key, blob in result["buckets"][kind].items():
                aggregate[kind].setdefault(key, bytearray()).extend(blob)
                previews[kind].setdefault(key, result["previews"][kind][key])
            current = totals[kind]
            observed = result["stats"][kind]
            current["states"] += observed["states"]
            if observed["maximum_S"] is not None:
                current["maximum_S"] = observed["maximum_S"] if current["maximum_S"] is None else max(current["maximum_S"], observed["maximum_S"])
                current["maximum_q"] = observed["maximum_q"] if current["maximum_q"] is None else max(current["maximum_q"], observed["maximum_q"])

    if jobs == 1:
        _worker_init(str(ucns_root), modulus, kmac_backend)
        for case in cases:
            consume(_worker_case(case))
    else:
        context = multiprocessing.get_context("spawn")
        with context.Pool(
            processes=jobs,
            initializer=_worker_init,
            initargs=(str(ucns_root), modulus, kmac_backend),
        ) as pool:
            for result in pool.imap(_worker_case, cases, chunksize=1):
                consume(result)

    _require(len(case_results) == len(cases), "bounded domain incomplete")
    summaries = {}
    for kind in ("gonol", "member"):
        blobs = {key: bytes(value) for key, value in aggregate[kind].items()}
        summaries[kind] = _finalize_kind(
            kind,
            blobs,
            previews[kind],
            totals[kind]["states"],
            totals[kind]["maximum_S"],
            totals[kind]["maximum_q"],
        )
    distinction = any(summaries[kind]["opposite_frame_phase_buckets"] for kind in summaries)
    classification = "DISTINCTION_PRESENT" if distinction else "DISTINCTION_ABSENT_IN_BOUNDED_DOMAIN"
    _require(classification in CLASSIFICATIONS, "classification law")
    domain = {
        "definition": "({epsilon} union {00,...,ff}) x (R_cap in {0,1})" if values is None and tuple(depths) == (0, 1) else "test subset",
        "case_order": "R_cap ascending; empty first; one-byte values 00 through ff ascending",
        "cases_expected": len(cases),
        "cases_completed": len(case_results),
        "cases": cases,
    }
    domain["input_domain_sha256"] = _sha256(_compact_json_bytes(domain["cases"]))
    output_identity = {
        "case_result_hashes": [item["result_identity_sha256"] for item in case_results],
        "gonol_records_sha256": summaries["gonol"]["all_records_sha256"],
        "member_records_sha256": summaries["member"]["all_records_sha256"],
        "classification": classification,
    }
    return {
        "classification": classification,
        "messages_processed": len(case_results),
        "input_domain": domain,
        "case_results": case_results,
        "gonol_measurement": summaries["gonol"],
        "member_measurement": summaries["member"],
        "aggregate_result_sha256": _sha256(_compact_json_bytes(output_identity)),
    }


def _authority_context(stack_root: Path, ucns_root: Path, skill_lib_root: Path) -> dict[str, Any]:
    _require(GIT_EXECUTABLE is not None, "Git executable unavailable")
    stack_commit = _git(stack_root, "rev-parse", f"{STACK_INPUT_COMMIT}^{{commit}}")
    stack_tree = _git(stack_root, "rev-parse", f"{STACK_INPUT_COMMIT}^{{tree}}")
    _require(stack_commit == STACK_INPUT_COMMIT and stack_tree == STACK_INPUT_TREE, "Stack input authority drift")
    _require(_git(stack_root, "rev-parse", STACK_EQUIVALENCE_COMMIT) == STACK_EQUIVALENCE_COMMIT, "Stack equivalence commit unavailable")
    # Fixed Git argv; the caller-supplied repository path is never shell-parsed.
    ancestry = subprocess.run(  # nosec B603
        [GIT_EXECUTABLE, "-C", str(stack_root), "merge-base", "--is-ancestor", STACK_INPUT_COMMIT, "HEAD"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    _require(ancestry.returncode == 0, "Stack input commit is not an ancestor of the measurement source")
    governed_paths = (
        "research/urpcs/docs/urpcs-v1-spec.md",
        "research/urpcs/urpcs_v1_reference.py",
        "research/urpcs/urpcs_v1_independent.js",
        "research/urpcs/tests/test_independent_decoder.js",
        "research/urpcs/tests/test_reference.py",
        "research/urpcs/vectors/urpcs-v1-vectors.json",
    )
    # Fixed Git argv; governed paths and commits are source constants.
    equivalence = subprocess.run(  # nosec B603
        [GIT_EXECUTABLE, "-C", str(stack_root), "diff", "--quiet", STACK_EQUIVALENCE_COMMIT, STACK_INPUT_COMMIT, "--", *governed_paths],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    _require(equivalence.returncode == 0, "governing URPCS blobs drifted from the equivalence commit")
    ucns_commit = _git(ucns_root, "rev-parse", "HEAD")
    ucns_tree = _git(ucns_root, "rev-parse", "HEAD^{tree}")
    _require(ucns_commit == UCNS_COMMIT and ucns_tree == UCNS_TREE, "UCNS authority drift")
    source = ucns_root / "src" / "ucns" / "direct_mobius.py"
    _require(_git(ucns_root, "hash-object", str(source)) == UCNS_DIRECT_MOBIUS_BLOB, "UCNS native Möbius blob drift")
    skill_commit = _git(skill_lib_root, "rev-parse", "HEAD")
    skill_tree = _git(skill_lib_root, "rev-parse", "HEAD^{tree}")
    _require(skill_commit == SKILL_LIB_COMMIT and skill_tree == SKILL_LIB_TREE, "skill-lib authority drift")
    return {
        "stack": {
            "repository": "The-Interdependency/stack",
            "input_commit": stack_commit,
            "input_tree": stack_tree,
            "urpcs_equivalence_commit": STACK_EQUIVALENCE_COMMIT,
            "authority": "bounded adapter and measurement only",
        },
        "ucns": {
            "repository": "The-Interdependency/ucns",
            "commit": ucns_commit,
            "tree": ucns_tree,
            "source_path": "src/ucns/direct_mobius.py",
            "source_blob": UCNS_DIRECT_MOBIUS_BLOB,
            "source_sha256": _file_sha256(source),
            "native_mobius_law_id": UCNS_LAW_ID,
            "native_mobius_law_version": UCNS_LAW_VERSION,
            "authority": "Möbius geometry only",
        },
        "skill_lib": {
            "repository": "The-Interdependency/skill-lib",
            "commit": skill_commit,
            "tree": skill_tree,
            "authority": "work discipline only; no geometry or measurement result",
        },
    }


def _runtime_context(kmac_identity: Mapping[str, Any]) -> dict[str, Any]:
    executable = Path(sys.executable).resolve()
    return {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "python_executable": str(executable),
        "python_executable_sha256": _file_sha256(executable),
        "platform": platform.platform(),
        "byteorder": sys.byteorder,
        "kmac_backend": dict(kmac_identity),
        "zlib_version": zlib.ZLIB_VERSION,
    }


def _source_context(stack_root: Path) -> dict[str, Any]:
    relative_paths = (
        "research/urpcs/urpcs_mobius_projection.py",
        "research/urpcs/tests/test_mobius_projection.py",
        "research/urpcs/docs/urpcs-v1-spec.md",
        "research/urpcs/urpcs_v1_reference.py",
        "research/urpcs/urpcs_v1_independent.js",
        "research/urpcs/tests/test_independent_decoder.js",
        "research/urpcs/vectors/urpcs-v1-vectors.json",
    )
    return {
        path: {"sha256": _file_sha256(stack_root / path), "bytes": (stack_root / path).stat().st_size}
        for path in relative_paths
    }


def build_receipt(
    *,
    measurement: Mapping[str, Any],
    authorities: Mapping[str, Any],
    runtime: Mapping[str, Any],
    sources: Mapping[str, Any],
    jobs: int,
) -> dict[str, Any]:
    state_identities = {str(depth): _state_identity(ref.vector_state(depth)) for depth in (0, 1)}
    receipt: dict[str, Any] = {
        "artifact": "URPCS Möbius projection v0 bounded measurement",
        "standing": "COMPUTATION; stack-local research; not a protocol profile",
        "schema": "the-interdependency.stack.urpcs-mobius-projection-receipt.v0",
        "authorities": dict(authorities),
        "sources": dict(sources),
        "runtime": dict(runtime),
        "execution": {
            "jobs": jobs,
            "x_bytes": ref.X,
            "M": ref.M,
            "depths": [0, 1],
            "associated_data_hex": ref.VECTOR_AD.hex(),
            "associated_data_sha256": _sha256(ref.VECTOR_AD),
            "initial_state_identities": state_identities,
            "fixed_key_identity": "public frozen URPCS v1 vector-state keys, identified only by per-field SHA-256",
            "authentication_boundary": "KMAC authenticates C_0 before bootstrap parsing, witness recovery, body parsing, or plaintext reconstruction",
        },
        "record_encoding": {
            "version": "urpcs-mobius-split-record-v0",
            "common": "u32be payload_length || u16be case_index || u32be layer || u32be region || i64be S || u16be gonol_id_length || gonol_id",
            "member_suffix": "u16be occurrence_id_length || occurrence_id || i64be local_displacement",
            "bucket_context": "record class, canonical phase (r,M), and frame are supplied by the enclosing JSON bucket",
            "compression": "zlib level 9 followed by base64; lossless evidence storage only, not a URPCS compression claim",
        },
        "measurement": dict(measurement),
        "test_and_measurement_counts": {
            "messages_processed": measurement["messages_processed"],
            "gonol_states": measurement["gonol_measurement"]["states"],
            "member_states": measurement["member_measurement"]["states"],
            "ucns_conformance_fixture_count": 10,
            "declared_bounded_case_count": 514,
        },
        "classification": measurement["classification"],
        "explicit_nonclaims": list(NONCLAIMS),
        "hmmm": "No opposite-frame phase split occurred in the complete bounded domain, so integration ends for this bounded profile. Whether such a distinction exists outside this fixed harness remains unresolved and authorizes no traversal change.",
    }
    _require(receipt["classification"] in CLASSIFICATIONS, "receipt classification law")
    receipt["receipt_payload_sha256"] = _sha256(_compact_json_bytes(receipt))
    return receipt


def verify_receipt_payload(receipt: Mapping[str, Any]) -> None:
    payload = dict(receipt)
    claimed = payload.pop("receipt_payload_sha256", None)
    _require(isinstance(claimed, str) and len(claimed) == 64, "receipt payload hash missing")
    _require(_sha256(_compact_json_bytes(payload)) == claimed, "receipt payload hash mismatch")


def render_report(receipt: Mapping[str, Any], receipt_sha256: str) -> str:
    measurement = receipt["measurement"]
    gonol = measurement["gonol_measurement"]
    member = measurement["member_measurement"]
    lines = [
        "# URPCS Möbius projection v0 — bounded measurement",
        "",
        f"Classification: **{receipt['classification']}**.",
        "",
        "This is a read-only measurement of UCNS native Möbius state already derivable from authenticated URPCS v1 witnesses. It is not a traversal profile and does not modify the frozen URPCS v1 wire or codec behavior.",
        "",
        "## Exact evidence identity",
        "",
        f"- Canonical receipt SHA-256: `{receipt_sha256}`",
        f"- Receipt payload SHA-256: `{receipt['receipt_payload_sha256']}`",
        f"- Aggregate result SHA-256: `{measurement['aggregate_result_sha256']}`",
        f"- Input domain SHA-256: `{measurement['input_domain']['input_domain_sha256']}`",
        f"- Stack input commit/tree: `{receipt['authorities']['stack']['input_commit']}` / `{receipt['authorities']['stack']['input_tree']}`",
        f"- UCNS commit/law: `{receipt['authorities']['ucns']['commit']}` / `{receipt['authorities']['ucns']['native_mobius_law_id']}@{receipt['authorities']['ucns']['native_mobius_law_version']}`",
        f"- skill-lib commit: `{receipt['authorities']['skill_lib']['commit']}`",
        "",
        "## Complete bounded domain",
        "",
        f"The run completed all **{measurement['messages_processed']}** cases in `({{epsilon}} union {{00,...,ff}}) x (R_cap in {{0,1}})` under the frozen vector state and associated data.",
        "",
        "| Record class | States | Phase buckets | (phase, frame) buckets | Opposite-frame phase splits | Records in split buckets | Maximum S | Maximum q |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
        f"| Gonol | {gonol['states']} | {gonol['distinct_phase_buckets']} | {gonol['distinct_phase_frame_buckets']} | {gonol['opposite_frame_phase_buckets']} | {gonol['records_in_opposite_frame_phase_buckets']} | {gonol['maximum_S']} | {gonol['maximum_q']} |",
        f"| Member | {member['states']} | {member['distinct_phase_buckets']} | {member['distinct_phase_frame_buckets']} | {member['opposite_frame_phase_buckets']} | {member['records_in_opposite_frame_phase_buckets']} | {member['maximum_S']} | {member['maximum_q']} |",
        "",
        "Phase is represented canonically as `(r,M)` and all projection arithmetic is exact. The canonical JSON retains every source-case and structural identifier in each opposite-frame phase split using the documented lossless record encoding.",
        "",
        "Gonol and occurrence identifiers distinguish structural objects only within their declared message/session construction. Native complete local state intentionally does not retain absolute winding count: for example, `S=2` and `S=18` have the same phase and frame at `M=8`. URPCS-derived displacements in this run are nonnegative; negative values occur only in mathematical conformance fixtures.",
        "",
        "## Authentication and interpretation boundary",
        "",
        "KMAC256 authenticates `C_0` before witness recovery, body parsing, or plaintext reconstruction. The frame is public and deterministically derived from authenticated witness rows. It supplies no entropy or confidentiality and adds no replay protection, rollback resistance, or state-reuse protection. Same-phase/opposite-frame observations are **opposite-frame phase splits**: visible phases coincide while complete local states remain distinct.",
        "",
        "## Explicit nonclaims",
        "",
        "This work does not establish " + ", ".join(receipt["explicit_nonclaims"]) + ".",
        "",
        "## hmmm",
        "",
        receipt["hmmm"],
        "",
    ]
    return "\n".join(lines)


def write_evidence(receipt: Mapping[str, Any], receipt_path: Path, report_path: Path) -> tuple[str, str]:
    receipt_bytes = _json_bytes(receipt)
    receipt_sha = _sha256(receipt_bytes)
    report = render_report(receipt, receipt_sha)
    report_bytes = report.encode("utf-8")
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_bytes(receipt_bytes)
    report_path.write_bytes(report_bytes)
    return receipt_sha, _sha256(report_bytes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stack-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--ucns-root", type=Path, required=True)
    parser.add_argument("--skill-lib-root", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=max(1, min(2, os.cpu_count() or 1)))
    parser.add_argument("--kmac-backend", choices=("stdlib", "pycryptodome"), default="pycryptodome")
    parser.add_argument("--write-receipt", type=Path, required=True)
    parser.add_argument("--write-report", type=Path, required=True)
    args = parser.parse_args()

    stack_root = args.stack_root.resolve()
    ucns_root = args.ucns_root.resolve()
    skill_lib_root = args.skill_lib_root.resolve()
    authorities = _authority_context(stack_root, ucns_root, skill_lib_root)
    kmac_identity = _install_kmac_backend(args.kmac_backend)
    # Workers install and verify the same backend independently.
    measurement = run_measurement(
        ucns_root=ucns_root,
        jobs=args.jobs,
        kmac_backend=args.kmac_backend,
    )
    receipt = build_receipt(
        measurement=measurement,
        authorities=authorities,
        runtime=_runtime_context(kmac_identity),
        sources=_source_context(stack_root),
        jobs=args.jobs,
    )
    verify_receipt_payload(receipt)
    receipt_sha, report_sha = write_evidence(receipt, args.write_receipt, args.write_report)
    print(json.dumps({
        "classification": receipt["classification"],
        "messages_processed": measurement["messages_processed"],
        "receipt_sha256": receipt_sha,
        "report_sha256": report_sha,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
