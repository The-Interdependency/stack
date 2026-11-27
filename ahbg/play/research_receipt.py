"""Publish measurements from the named synthetic operator cases and native EPAC reconstruction."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect(evidence, epac):
    def read(name):
        return json.loads((evidence / name).read_text())
    commit = subprocess.check_output(["git", "-C", epac, "rev-parse", "HEAD"], text=True).strip()
    if commit != "86f183157d663926df4ede7ce5d6e5f8f260d19f":
        raise ValueError("unexpected EPAC source")
    source = epac / "epac_join_term.py"
    if source.read_bytes() != subprocess.check_output(["git","-C",epac,"show",commit+":epac_join_term.py"]):
        raise ValueError("EPAC module differs from commit")
    sys.path.insert(0, str(epac))
    import epac_join_term as native
    trees = []
    cases = []
    for order in [("core", "guest", "vacancy"), ("guest", "core", "vacancy")]:
        original = native.construct_epac_join_tree(s2_seating_order=order)
        recovered = native.recover_epac_join_tree(original.to_json())
        if recovered != original:
            raise ValueError("join reconstruction failed")
        trees.append(recovered)
        origin = recovered.origins[2]
        cases.append({"seats": [slot.to_dict() for slot in origin.slots],
                      "lineage": list(native.trace_origin_lineage(recovered, origin.origin_id)),
                      "digest": recovered.to_dict()["candidate_digest"]})
    if native.legacy_bag_projection(trees[0]) != native.legacy_bag_projection(trees[1]) or native.join_isomorphic(*trees):
        raise ValueError("named-seat distinction lost")
    uchc = read("uchc-readers.json")
    dispatch = read("a0-dispatch/dispatch.json")
    case = Path(__file__).parent / "evidence/contested.json"
    if case.read_bytes() != (evidence/"contested-restored.json").read_bytes():
        raise ValueError("Weave recovery changed recorded decisions")
    return {
        "epac": {"commit": commit, "module_sha256": sha(source), "cases": cases,
                 "license_binding": trees[0].to_dict()["semantic_license"]},
        "edcm": read("edcm-metrics.json"),
        "uchc": {k: uchc[k] for k in ("producer","test_examples_per_reader","method","totals","structural_reader")},
        "weave": {"payload_sha256": sha(case), "wire_sha256": sha(evidence/"contested.wvc"),
                  "bytes_restored": case.stat().st_size, "replayed": read("contested-replay.json")},
        "a0": {"commit": dispatch["a0_commit"], "native_files": dispatch["native_files"],
               "choice": dispatch["outcome"]["choice"], "outcome": dispatch["outcome"]["outcome"],
               "roles": [role["role"] for role in dispatch["roles"]]},
        "skill_catalog": "0375a146a05cd61bb924290c5427752a2c0ded67",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("operator_evidence","epac_checkout","output"):
        parser.add_argument(name,type=Path)
    args=parser.parse_args()
    args.output.write_text(json.dumps(collect(args.operator_evidence,args.epac_checkout),indent=2)+"\n")
