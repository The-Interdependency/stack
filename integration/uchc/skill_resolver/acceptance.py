# ratios: loc_comments=65:1 imports_exports=6:2 calls_definitions=26:3
"""Run the two catalog decisions against both representations and compare exact views."""

import argparse
import json
from pathlib import Path

from ahbg.integration.skill_harness import build_view
from .runtime import SkillResolver, digest


def _size(value):
    return len(json.dumps(value, sort_keys=True, ensure_ascii=False,
                          separators=(",", ":")).encode("utf-8"))


PUBLICATION = "distributed-publication"
FRONTEND = "typed-meta-frontend"
EXPECTED = {
    PUBLICATION: ["interdependent-work-graph", PUBLICATION],
    FRONTEND: ["msdmd", "doc-build", "meta-module-build", FRONTEND],
}
SCOPE = sorted({name for names in EXPECTED.values() for name in names})


def compare(catalog, native):
    arms = {arm: SkillResolver(catalog, ucns_source_root=native, experiment=arm)
            for arm in ("control", "uchc")}
    results = {}
    for root, expected in EXPECTED.items():
        evidence = {}
        for arm, resolver in arms.items():
            grants = [("msdmd", "msdmd/collect.py")] if root == FRONTEND else []
            view = build_view(resolver, visible=SCOPE, activate=[root], disclosed_runners=grants)
            plan = resolver.resolve([root])
            if plan["order"] != expected or [s["name"] for s in view["activated"]] != expected:
                raise AssertionError(f"{arm}: unexpected closure for {root}")
            if root == PUBLICATION and plan["reasons"][expected[0]] != [
                    {"kind": "load_with", "source": PUBLICATION}]:
                raise AssertionError("publication co-load reason missing")
            if root == FRONTEND and plan["reasons"]["msdmd"] != [
                    {"kind": "depends_on", "source": name}
                    for name in ("doc-build", "meta-module-build", FRONTEND)]:
                raise AssertionError("shared prerequisite lost a reason")
            for entry in view["activated"]:
                expected_body = resolver.read_body(entry["name"])
                if entry["instructions"] != expected_body:
                    raise AssertionError("planner received different instructions")
            record = {"records": [resolver.get(n) for n in plan["order"]],
                      "resolution": {"source": resolver.source, "decision": plan}}
            proof = record if arm == "control" else resolver.activation_packet
            evidence[arm] = {"plan": plan, "view_sha256": digest(view),
                             "view_bytes": _size(view), "record_bytes": _size(proof),
                             "record_sha256": digest(proof)}
        for field in ("plan", "view_sha256", "view_bytes"):
            if evidence["control"][field] != evidence["uchc"][field]:
                raise AssertionError(f"arms disagree about {root}: {field}")
        results[root] = {"order": expected, "view_bytes": evidence["uchc"]["view_bytes"],
                         "view_sha256": evidence["uchc"]["view_sha256"],
                         "records": {arm: {"bytes": arm_data["record_bytes"],
                                           "sha256": arm_data["record_sha256"]}
                                     for arm, arm_data in evidence.items()}}
    return {"source": arms["uchc"].source, "cases": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", type=Path)
    parser.add_argument("ucns_source", type=Path)
    args = parser.parse_args()
    results = compare(args.catalog, args.ucns_source)
    from .revision_probe import compare_revision
    results["revision_probe"] = compare_revision(
        SkillResolver(args.catalog, ucns_source_root=args.ucns_source))
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
# ratios: loc_comments=65:1 imports_exports=6:2 calls_definitions=26:3
