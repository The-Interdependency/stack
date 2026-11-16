# ratios: loc_comments=58:29 imports_exports=7:5 calls_definitions=33:5
"""Qualify the declared English source-construction profile.

Usage: python tools/qualify_english_gonols.py compare FIRST SECOND
Historical evidence remains scoped to its original implementation.
"""
# === MODULE_BUILD ===
# id: english_gonol_qualification
#   module_name: qualify_english_gonols
#   module_kind: instrument
#   summary: compare complete English constructions and reject incomplete test outcomes
#   owner: Stack English construction research
#   public_surface: compare and check-tests commands
#   internal_surface: exact manifests and XML outcome checks
#   auth_boundary: read-only corpus artifacts
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: supplied corpus artifacts
#   admin_only: false
#   tests: tools/tests/test_english_qualification.py
#   rollout: English qualification workflow
#   rollback: preserve frozen evidence
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: english_qualification_test_outcomes
#   given: supplied JUnit outcome files
#   then: require nonempty passing cases with matching declared aggregates and no skips
# id: english_qualification_distinct_artifacts
#   given: two claimed construction artifacts
#   then: refuse identical paths and aliased evidence files before comparison
# === END CONTRACTS ===
import argparse
import json
from pathlib import Path
import sqlite3
import sys
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]


def require(condition, reason):
    if not condition:
        raise ValueError(reason)



def distinct_outputs(a, b, files):
    require(a.resolve() != b.resolve(), "two distinct execution directories required")
    for name in files:
        require(not (a / name).samefile(b / name), "aliased evidence file: " + name)



def english_compare(a, b):
    distinct_outputs(a, b, ("construct.db", "manifest.json"))
    sys.path.insert(0, str(ROOT / "research/english-gonol"))
    from english_gonol.full_construct_run import verify_replay
    first, second = verify_replay(a), verify_replay(b)
    require(first == second, "English manifests differ")
    expected = json.loads((ROOT / "research/english-gonol/experiments/full-construct-v2/manifest.json").read_text())
    require(first == expected, "English build differs from frozen complete-corpus receipt")
    for root in (a, b):
        with sqlite3.connect(f"file:{root / 'construct.db'}?mode=ro", uri=True) as db:
            require(db.execute("PRAGMA integrity_check").fetchone()[0] == "ok", "SQLite integrity")
            for table, count in first["counts"].items():
                require(db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == count, "count mismatch")
    print(json.dumps({"status": "SURVIVED", "matching_distinct_artifacts": 2, "independent_execution": "not established by artifact comparison alone", "manifest": first}, indent=2))



def check_tests(paths):
    count = 0
    for path in paths:
        tree = ET.parse(path)
        cases = tree.findall(".//testcase")
        require(bool(cases), "empty test suite")
        require(not tree.findall(".//skipped") and not tree.findall(".//failure") and not tree.findall(".//error"), "unpassed test outcomes")
        for suite in tree.getroot().iter():
            if suite.tag not in ("testsuite", "testsuites"):
                continue
            if suite.tag == "testsuite" or "tests" in suite.attrib:
                require(int(suite.attrib.get("tests", -1)) == len(list(suite.iter("testcase"))), "JUnit declared count mismatch")
            for key in ("skipped", "failures", "errors"):
                if suite.tag == "testsuite" or key in suite.attrib:
                    require(int(suite.attrib.get(key, -1)) == 0, "JUnit aggregate reports unpassed outcomes")
        count += len(cases)
    print(json.dumps({"passed": count, "skipped": 0, "failed": 0}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('compare')
    p.add_argument('a', type=Path); p.add_argument('b', type=Path)
    p = commands.add_parser('check-tests'); p.add_argument('paths', type=Path, nargs='+')
    args = parser.parse_args()
    if args.command == 'compare':
        english_compare(args.a, args.b)
    else:
        check_tests(args.paths)


if __name__ == '__main__':
    main()
# ratios: loc_comments=58:29 imports_exports=7:5 calls_definitions=33:5
