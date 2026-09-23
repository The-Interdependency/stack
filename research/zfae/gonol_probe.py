# ratios: loc_comments=72:27 imports_exports=7:2 calls_definitions=27:2
"""Replay all declared glyph admissions and the original collision fixture.

Usage: python research/zfae/gonol_probe.py --ucns-source-file /tmp/public_gonol.py
Optional --output writes complete pair observations and source-bound recovery
evidence. Exit 0: finite scope survived; exit 2: failed/blocked. No inference.
"""

# === MODULE_BUILD ===
# id: zfae_gonol_probe
#   module_name: gonol_probe
#   module_kind: experiment
#   summary: complete finite admission and recovery experiment for the gonol input parser
#   owner: The-Interdependency/stack
#   public_surface: run, CLI
#   auth_boundary: none
#   storage_boundary: explicit source reads and optional result write
#   network_boundary: none
#   user_data_boundary: synthetic fixtures only
#   tests: research/zfae/tests/test_gonol_parser.py, CI sealed replay
#   rollout: explicit research run
#   rollback: revert parser experiment; preserve its historical receipts
#   unresolved: a finite recovery witness establishes no universal admission or inference
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: zfae_gonol_probe_exhausts_profile
#   given: verified producers and a consistent work graph
#   then: execute every frozen recovery case and every inventory glyph, preserve complete pair observations, and block on failed recovery or admission expectations
#   class: evidence
# === END CONTRACTS ===

import argparse
import hashlib
import json
from pathlib import Path
import platform

from gonol_parser import load_parser
from input_probe import evaluate

HERE = Path(__file__).resolve().parent


def run(ucns_source_file: Path) -> dict:
    parser = load_parser(ucns_source_file)
    profile = json.loads((HERE / "GONOL_PARSER.json").read_text(encoding="utf-8"))
    manifest = json.loads((HERE.parents[1] / "stack-manifest.json").read_text(encoding="utf-8"))
    graph = {k: manifest[k] for k in ("repositories", "research_participants", "boundaries")}
    digest = hashlib.sha256(json.dumps(graph, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if digest != manifest["work_graph_sha256"]:
        raise ValueError("work graph mismatch")
    for source in (profile["ucns"], profile["producer"]):
        if not any(p["workspace"] == "research/zfae/" and p["repository"] == source["repository"]
                   and p["commit"] == source["commit"] and p["authority_transfer"] is False
                   for p in manifest["research_participants"]):
            raise ValueError("producer absent from research work graph")
    pairs = json.loads((HERE / "INPUT_PROBE.json").read_text(encoding="utf-8"))["pairs"]
    result = evaluate(pairs, lambda text: parser.parse_text(text, source_id="fixture:pair").to_dict())
    cases = []
    scope = profile["cases"] + [{"text": "".join(parser.inventory), "admitted": True}]
    for index, case in enumerate(scope):
        text = case["text"]
        parsed = parser.parse_text(text, source_id=f"fixture:recovery:{index}")
        restored = parser.replay(json.loads(json.dumps(parsed.to_dict())))
        native_equal = None
        if parsed.admitted:
            native_equal = parser.parse_gonols(parsed.require_gonols(), source_id=parsed.source_id) == parsed
        cases.append({"text": text, "admitted": parsed.admitted,
                      "admission_expected": case["admitted"],
                      "missing_offsets": [o.ordinal for o in parsed.unadmitted],
                      "source_recovered": parsed.recover_text() == text,
                      "utf8_recovered": parser.parse_utf8(text.encode(), source_id=parsed.source_id) == parsed,
                      "json_replayed": restored == parsed,
                      "native_gonols_replayed": native_equal})
    if not all(c["admitted"] is c["admission_expected"] and c["source_recovered"]
               and c["utf8_recovered"] and c["json_replayed"]
               and c["native_gonols_replayed"] is not False for c in cases):
        result["standing"] = "BLOCKED"
    return {
        "schema": "stack.zfae.gonol-parser-result", "version": "1.0.0",
        "scope": "complete declared finite input profile; source preservation, not neural inference",
        "python": platform.python_version(), "work_graph_sha256": digest,
        "profile_sha256": parser.profile_sha256, "inventory_sha256": parser.inventory_sha256,
        "source_sha256": {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest()
                          for name in ("gonol_parser.py", "gonol_probe.py", "input_probe.py", "INPUT_PROBE.json")},
        "ucns": profile["ucns"], "producer": profile["producer"],
        "carrier_glyph_count": sum(g.carrier_position is not None for g in parser.inventory.values()),
        "admitted_scalar_count": len(parser.inventory),
        "recovery_cases": cases, **result, "hmmm": profile["hmmm"],
    }


def main() -> int:
    options = argparse.ArgumentParser(description=__doc__)
    options.add_argument("--ucns-source-file", type=Path, required=True)
    options.add_argument("--output", type=Path)
    args = options.parse_args()
    try:
        result = run(args.ucns_source_file)
    except Exception as exc:
        result = {"standing": "BLOCKED", "hmmm": [f"{type(exc).__name__}: {exc}"]}
    rendered = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0 if result["standing"] == "SURVIVED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
# ratios: loc_comments=72:27 imports_exports=7:2 calls_definitions=27:2
