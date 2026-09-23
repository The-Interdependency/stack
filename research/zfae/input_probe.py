# ratios: loc_comments=117:44 imports_exports=9:3 calls_definitions=47:3
"""Replay the source-bound ZFAE input-distinction experiment.

Usage from Stack root (Python 3.12+, standard library)::

    python research/zfae/input_probe.py --source-file /tmp/zfae-parser.py

Read INPUT_PROBE.json before execution. Only the exact inspected upstream
module is executed; the module is loaded in isolation from its application.
Optional --output writes a complete JSON receipt. Exit 0 means completed
research (including FALSIFIED), 2 means BLOCKED. No training or network calls.
The scalar-sequence comparison is an identity witness, not a gonol constructor.
"""

# === MODULE_BUILD ===
# id: zfae_input_distinction_probe
#   module_name: input_probe
#   module_kind: experiment
#   summary: test whether an exact upstream heuristic parser preserves frozen character distinctions before considering it as a sole input boundary
#   owner: The-Interdependency/stack
#   public_surface: evaluate, run, CLI JSON receipt
#   internal_surface: source identity and plan validation
#   auth_boundary: none
#   storage_boundary: read, write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/zfae/tests/test_input_probe.py
#   rollout: manually invoked research probe and path-scoped CI
#   rollback: remove research workspace and its manifest projections as one transaction
#   unresolved: finite input distinctions do not prove neural inference or universal sufficiency
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: zfae_probe_pins_before_execution
#   given: supplied source bytes differ from the declared immutable Git blob
#   then: block before executing any supplied source code
#   class: evidence
# id: zfae_probe_controls_interpretation
#   given: a control fails or a repeated observation differs
#   then: report BLOCKED rather than interpreting a hypothesis outcome
#   class: evidence
# id: zfae_probe_preserves_counterexamples
#   given: valid controls and two different required inputs with equal complete feature records
#   then: record every collision and classify only the sole-input-boundary hypothesis as FALSIFIED
#   class: evidence
# === END CONTRACTS ===

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import types
from typing import Callable

HERE = Path(__file__).resolve().parent


def evaluate(pairs: list[dict], observe: Callable[[str], dict]) -> dict:
    """Evaluate every frozen pair; controls and replay outrank interpretation."""
    observations = []
    for pair in pairs:
        left = observe(pair["left"])
        left_again = observe(pair["left"])
        right = observe(pair["right"])
        right_again = observe(pair["right"])
        if not all(isinstance(v, dict) for v in (left, left_again, right, right_again)):
            raise ValueError("observation must be a complete feature dictionary")
        json.dumps([left, left_again, right, right_again], allow_nan=False)
        observations.append({
            **pair,
            "input_codepoints_equal": tuple(map(ord, pair["left"])) == tuple(map(ord, pair["right"])),
            "features_equal": left == right,
            "replay_equal": left == left_again and right == right_again,
            "left_features": left,
            "right_features": right,
        })
    controls_ok = all(
        row["replay_equal"] and (
            row["features_equal"] if row["kind"] == "equal-control"
            else not row["features_equal"] if row["kind"] == "distinct-control"
            else True
        ) for row in observations
    )
    collisions = [row["id"] for row in observations
                  if row["kind"] == "required-distinction" and row["features_equal"]]
    return {
        "standing": "BLOCKED" if not controls_ok else "FALSIFIED" if collisions else "SURVIVED",
        "controls_passed": controls_ok,
        "collision_ids": collisions,
        "observations": observations,
    }


def run(source_file: Path) -> dict:
    """Verify the plan/source/work graph and execute the selected parser only."""
    plan_bytes = (HERE / "INPUT_PROBE.json").read_bytes()
    plan = json.loads(plan_bytes)
    manifest = json.loads((HERE.parents[1] / "stack-manifest.json").read_text())
    graph_payload = {k: manifest[k] for k in ("repositories", "research_participants", "boundaries")}
    graph_hash = hashlib.sha256(json.dumps(graph_payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if graph_hash != manifest["work_graph_sha256"]:
        raise ValueError("Stack work-graph digest mismatch")
    source = plan["source"]
    matching = [r for r in manifest["research_participants"]
                if r["workspace"] == "research/zfae/" and r["repository"] == source["repository"]
                and r["commit"] == source["commit"] and r["authority_transfer"] is False]
    if len(matching) != 1:
        raise ValueError("probe source is not uniquely bound in Stack research participants")
    pairs = plan["pairs"]
    if not isinstance(pairs, list) or not pairs:
        raise ValueError("probe pairs must be a nonempty list")
    ids = set()
    kinds = set()
    for pair in pairs:
        if set(pair) != {"id", "kind", "left", "right"} or not all(isinstance(v, str) for v in pair.values()):
            raise ValueError("invalid pair fields or types")
        if not pair["id"] or pair["id"] in ids:
            raise ValueError("duplicate or empty pair identity")
        ids.add(pair["id"])
        kinds.add(pair["kind"])
        if (pair["left"] == pair["right"]) != (pair["kind"] == "equal-control"):
            raise ValueError("pair input identity disagrees with control role")
    if kinds != {"equal-control", "distinct-control", "required-distinction"}:
        raise ValueError("all control and hypothesis roles must be present")
    raw = source_file.read_bytes()
    blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    if blob != source["blob_sha"]:
        raise ValueError("source Git blob mismatch; execution refused")
    name = "_stack_zfae_probe_" + blob
    module = types.ModuleType(name)
    module.__file__ = str(source_file)
    previous = sys.modules.get(name)
    sys.modules[name] = module
    try:
        exec(compile(raw, str(source_file), "exec"), module.__dict__)
        result = evaluate(pairs, lambda text: module.parse_semantic(text).to_dict())
    finally:
        if previous is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = previous
    return {
        "schema": "stack.zfae.input-distinction-result", "version": "1.0.0",
        "claim": plan["question"], "scope": plan["scope"],
        "source": source, "source_sha256": hashlib.sha256(raw).hexdigest(),
        "plan_sha256": hashlib.sha256(plan_bytes).hexdigest(),
        "harness_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "work_graph_sha256": graph_hash, "python": platform.python_version(),
        **result, "next_action": plan["outcomes"][result["standing"]],
        "hmmm": plan["hmmm"],
    }


def main() -> int:
    """Report infrastructure failure separately from a completed falsifier."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = run(args.source_file)
    except Exception as exc:
        result = {"standing": "BLOCKED", "hmmm": [f"{type(exc).__name__}: {exc}"]}
    rendered = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 2 if result["standing"] == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
# ratios: loc_comments=117:44 imports_exports=9:3 calls_definitions=47:3
