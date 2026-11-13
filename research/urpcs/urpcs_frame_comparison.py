#!/usr/bin/env python3
# === MODULE_BUILD ===
# id: urpcs_frame_comparison_consumer
#   module_name: urpcs_frame_comparison
#   module_kind: experiment
#   summary: replay the complete sealed relational population using the exact UCNS comparison without changing URPCS v1
#   owner: The-Interdependency/stack research/urpcs
#   public_surface: load_geometry, read_population, compare_local, run, main
#   internal_surface: exact source admission and existing-edge replay
#   auth_boundary: none
#   storage_boundary: read sealed public evidence; write new receipt only
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/urpcs/frame_comparison_tests.py
#   rollout: explicit separate pinned-UCNS replay; never imported by the codec
#   rollback: remove this consumer, its tests, report, receipt, and dedicated workflow
#   since: 2026-09-25
#   unresolved: independent-origin alignment and all protocol adoption
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: frame_consumer_admits_exact_sources
#   given: a UCNS checkout and the sealed relational receipt
#   then: wrong commit or consumed bytes and altered receipt bytes are rejected before execution or interpretation
#   class: evidence
# id: frame_consumer_preserves_relation_scope
#   given: observations or a sealed attachment edge
#   then: comparisons use a shared gonol anchor or that explicit attachment and never invent a cross-origin relation
#   class: correctness
# id: frame_consumer_replays_complete_population
#   given: the sealed 2737-observation receipt
#   then: every observation is admitted, the original 120 checks and 44 failures replay, and corrected native comparisons reconstruct and remain invariant
#   class: evidence
# id: frame_consumer_deterministic_receipt
#   given: identical source bytes and sealed evidence
#   then: receipt bytes are identical and earlier evidence is unchanged
#   class: evidence
# === END CONTRACTS ===

"""Opt-in read-only consumer of the UCNS complete-state comparison.

Usage from the Stack root::

    python research/urpcs/urpcs_frame_comparison.py \
      --ucns-root /path/to/ucns-at-ee3df862 --out /tmp/frame-comparison.json

The supplied checkout must be the exact UCNS commit below. It is separate
from Stack's global UCNS pin and from the original analyzer's pinned source.
The input is the COMPLETE sealed #55 receipt, not newly authenticated data.
See docs/URPCS-frame-comparison-v1.md for admission and nonclaims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess  # nosec B404
import sys
import types
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path

UCNS_COMMIT = "ee3df862112811711b43afed4174592a241c373d"
UCNS_FILES = {
    "src/ucns/direct_mobius.py": "d8d1360c753dac7431071e007c5105a21b5396dd9e2f7e5ba4089d99e056a5bf",
    "src/ucns/mobius_comparison.py": "37b08603277e904fc9d2e78a12eaa8ac7e326a92ecb8952b38125d406dc8c861",
}
INPUT_GRAPH_SHA256 = "bd1059322ef8223d2a6531f84591e76970db67aa3982f1cbfd174d5039b5ecd5"
BASELINE_STACK_COMMIT = "4a03f68c1ea841da5767813c6a65c41620f561f6"
SEALED_PATH = "research/urpcs/receipts/urpcs-relational-carrier-v0.json"
SEALED_SHA256 = "f415c486df88cd3d0f8c6ad861d375e01553eba58f3f5a2807e1e23b097b419b"
SELF_PATH = "research/urpcs/urpcs_frame_comparison.py"
TEST_PATH = "research/urpcs/frame_comparison_tests.py"
WORKFLOW_PATH = ".github/workflows/urpcs-frame-comparison.yml"
M = 8


class FrameComparisonError(ValueError):
    """Evidence or chart eligibility failed closed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FrameComparisonError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n").encode()


def checked_bytes(path: Path, expected: str) -> bytes:
    require(not path.is_symlink(), f"symlink not admitted: {path}")
    data = path.read_bytes()
    require(digest(data) == expected, f"source digest mismatch: {path}")
    return data


def load_geometry(root: Path) -> tuple[types.ModuleType, types.ModuleType]:
    """Load only exact pinned UCNS bytes; bypass neither source identity nor pyc checks."""
    git = shutil.which("git")
    require(git is not None, "Git is required for producer identity")
    head = subprocess.check_output(  # nosec B603
        [git, "-C", str(root), "rev-parse", "HEAD"], text=True,
    ).strip()
    require(head == UCNS_COMMIT, "UCNS checkout is not the pinned comparison commit")
    buffers = {p: checked_bytes(root / p, sha) for p, sha in UCNS_FILES.items()}
    # Private namespace avoids running the UCNS package facade or loading stale
    # bytecode. Only these same, already verified byte buffers are executed.
    prefix = "_urpcs_verified_ucns_comparison"
    package = types.ModuleType(prefix)
    package.__path__ = []
    sys.modules[prefix] = package
    modules = []
    try:
        for path, data in buffers.items():
            name = prefix + "." + Path(path).stem
            module = types.ModuleType(name)
            module.__package__ = prefix
            module.__file__ = str(root / path)
            sys.modules[name] = module
            exec(compile(data, module.__file__, "exec", dont_inherit=True), module.__dict__)  # nosec B102
            setattr(package, Path(path).stem, module)
            modules.append(module)
    except BaseException:
        for name in (prefix + ".direct_mobius", prefix + ".mobius_comparison", prefix):
            sys.modules.pop(name, None)
        raise
    return modules[0], modules[1]


def native_state(row: dict, native: types.ModuleType):
    """Admit the exact sealed phase/frame and independently replay its displacement."""
    phase = row.get("phase")
    require(isinstance(phase, str), "phase must be a recorded rational pair")
    match = re.fullmatch(r"\(\s*(\d+)\s*,\s*(\d+)\s*\)", phase)
    require(match is not None, "invalid recorded phase")
    numerator, denominator = map(int, match.groups())
    require(denominator == M and 0 <= numerator < M, "phase outside the sealed lattice")
    state = native.NativeMobiusState(Fraction(numerator, denominator), native.NativeMobiusFrame(row["frame"]))
    displacement = row.get("S")
    require(type(displacement) is int, "recorded displacement must be an integer")
    require(native.native_mobius_state(Fraction(displacement, M)) == state, "recorded state disagrees with native displacement")
    return state


def read_population(path: Path, native: types.ModuleType) -> tuple[dict, list[dict]]:
    """Verify the sealed artifact before parsing and admit every observation."""
    receipt = json.loads(checked_bytes(path, SEALED_SHA256))
    require(receipt["classification"] == "RELATION_PRESENT_SHEET_RELATION_NOT_INVARIANT", "wrong baseline classification")
    records = []
    ids = set()
    for trace in receipt["measurement"]["traces"]:
        for row in trace["observations"]:
            require(row["case_id"] == trace["case_id"], "trace identity mismatch")
            require(row["id"] not in ids, "duplicate observation identity")
            require(all(isinstance(row[k], str) and row[k] for k in ("case_id", "origin", "gonol")), "missing chart provenance")
            native_state(row, native)
            ids.add(row["id"])
            records.append(row)
    require(len(records) == 2737, "incomplete sealed population")
    require(dict(Counter(row["kind"] for row in records)) == {"gonol-state": 948, "member-state": 1789}, "population kinds differ")
    return receipt, records


def compare_local(left: dict, right: dict, native: types.ModuleType, geometry: types.ModuleType):
    """Compare observations sharing the SAME recorded gonol anchor, not just an origin."""
    require(all(isinstance(left.get(k), str) and left.get(k) and left[k] == right.get(k)
                for k in ("case_id", "origin", "gonol")), "comparison requires the same case, origin, and gonol anchor")
    return geometry.compare_native_mobius(native_state(left, native), native_state(right, native))


def check_pair(a, b, geometry: types.ModuleType, motions: tuple[Fraction, ...]) -> tuple[int, int]:
    relation = geometry.compare_native_mobius(a, b)
    require(relation.transport(a) == b, "target reconstruction failed")
    require(relation.inverse().transport(b) == a, "inverse reconstruction failed")
    raw_changes = 0
    for motion in motions:
        aa, bb = a.advance(motion), b.advance(motion)
        require(geometry.compare_native_mobius(aa, bb) == relation, "corrected relation changed under common native motion")
        raw_changes += int(a.frame.sign * b.frame.sign != aa.frame.sign * bb.frame.sign)
    return len(motions), raw_changes


def run(stack_root: Path, ucns_root: Path) -> dict:
    """Replay the full sealed population; make no new protocol edges."""
    source_hashes = {path: digest((stack_root / path).read_bytes()) for path in (SELF_PATH, TEST_PATH, WORKFLOW_PATH)}
    native, geometry = load_geometry(ucns_root)
    baseline, records = read_population(stack_root / SEALED_PATH, native)
    old = baseline["measurement"]["torsor_rotation_check"]
    unique = sorted({(r["phase"], r["frame"]) for r in records})
    witnesses = {(r["phase"], r["frame"]): r for r in records}
    motions = tuple(Fraction(k, M) for k in range(M))
    checks = raw_changes = 0
    for left, right in combinations(unique, 2):
        a, b = native_state(witnesses[left], native), native_state(witnesses[right], native)
        n, raw = check_pair(a, b, geometry, motions)
        checks += n
        raw_changes += raw
    require(len(unique) == old["distinct_complete_local_states"] == 6, "baseline state census changed")
    require(checks == old["complete_state_pair_rotation_checks"] == 120, "baseline check census changed")
    require(raw_changes == old["sheet_product_changes"] == 44, "original falsification did not replay")
    groups = defaultdict(list)
    for row in records:
        groups[(row["case_id"], row["origin"], row["gonol"])].append(row)
    local_pairs = local_checks = local_raw_changes = 0
    for key in sorted(groups):
        rows = sorted(groups[key], key=lambda r: r["id"])
        for left, right in combinations(rows, 2):
            relation = compare_local(left, right, native, geometry)
            a, b = native_state(left, native), native_state(right, native)
            require(relation.transport(a) == b, "local consumer reconstruction failed")
            n, raw = check_pair(a, b, geometry, motions)
            local_pairs += 1
            local_checks += n
            local_raw_changes += raw
    # Existing attachment edges explicitly relate two gonols. They are NOT
    # inferred from equal origins, phase numbers, or serialization ancestry.
    gonols = {r["id"][:-6]: r for r in records if r["kind"] == "gonol-state"}
    attachment_count = attachment_checks = 0
    for trace in baseline["measurement"]["traces"]:
        for edge in trace["graph"]["edges"]:
            if edge["kind"] != "attaches":
                continue
            left, right = gonols[edge["source"]], gonols[edge["target"]]
            require(left["case_id"] == right["case_id"] == trace["case_id"] and left["origin"] == right["origin"], "attachment crossed its declared scope")
            a, b = native_state(left, native), native_state(right, native)
            delta = edge["relation"]["unreduced_delta"]
            require(type(delta) is int and a.advance(Fraction(delta, M)) == b, "attachment native displacement disagrees")
            n, _ = check_pair(a, b, geometry, motions)
            attachment_count += 1
            attachment_checks += n
    result = {
        "schema": "the-interdependency.stack.urpcs-frame-comparison.v1",
        "classification": "NATIVE_COMPARISON_INVARIANT_PROTOCOL_TRANSPORT_UNDEFINED",
        "standing": "complete sealed-population replay; not a protocol profile or selected UCNS carrier",
        "input_graph_sha256": INPUT_GRAPH_SHA256,
        "baseline_stack_commit": BASELINE_STACK_COMMIT,
        "sealed_receipt": {"path": SEALED_PATH, "sha256": SEALED_SHA256, "classification_preserved": baseline["classification"]},
        "ucns": {"commit": UCNS_COMMIT, "consumed_source_sha256": UCNS_FILES, "comparison_law": geometry.COMPARISON_LAW_ID + "@" + geometry.COMPARISON_LAW_VERSION},
        "consumer_source_sha256": source_hashes,
        "population": {"traces": len(baseline["measurement"]["traces"]), "observations": len(records), "kinds": dict(Counter(r["kind"] for r in records)), "shared_gonol_anchors": len(groups)},
        "original_geometry_probe": {"scope": "all distinct recorded state values; not cross-origin authorization", "complete_states": len(unique), "checks": checks, "naive_product_changes": raw_changes, "corrected_changes": 0},
        "shared_anchor_probe": {"pairs": local_pairs, "checks": local_checks, "naive_product_changes": local_raw_changes, "corrected_changes": 0},
        "existing_attachment_probe": {"edges": attachment_count, "checks": attachment_checks, "native_delta_reconstruction_failures": 0, "corrected_changes": 0},
        "nonclaims": ["new wire/spec/state behavior", "independent-origin alignment", "new peer-origin edges", "synchronization", "path winding beyond modulo two", "path holonomy", "typed event promotion", "security", "compression", "inference or traversal utility", "full UCNS selection"],
        "hmmm": ["A future protocol must separately specify origin alignment and transport; this replay neither supplies nor requires them."],
    }
    # Re-read consumed inputs after the measurement; changing source is an error.
    for path, sha in UCNS_FILES.items():
        checked_bytes(ucns_root / path, sha)
    checked_bytes(stack_root / SEALED_PATH, SEALED_SHA256)
    for path, sha in source_hashes.items():
        checked_bytes(stack_root / path, sha)
    result["payload_sha256"] = digest(json_bytes(result))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stack-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--ucns-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--check", type=Path, help="require byte-identical replay of this existing receipt")
    args = parser.parse_args()
    data = json_bytes(run(args.stack_root, args.ucns_root))
    if args.check is not None:
        require(args.check.read_bytes() == data, "receipt replay is not byte-identical")
    # An exclusive output prevents overwriting any prior receipt or source file.
    with args.out.open("xb") as output:
        output.write(data)
    print(data.decode(), end="")


if __name__ == "__main__":
    main()
