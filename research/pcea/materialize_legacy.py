#!/usr/bin/env python3
"""Materialize the last pre-cleanup PCEA research snapshot into ./migrated.

Usage:
    python materialize_legacy.py
    python materialize_legacy.py --check
    python materialize_legacy.py --force

The source commit is immutable. Every file is verified using Git's blob SHA-1
before it is written. This script is research/provenance tooling, never PCEA
runtime code.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys
import urllib.parse
import urllib.request

SOURCE_REPO = "The-Interdependency/pcea"
SOURCE_COMMIT = "ecf2ca0dec38bef29382e02121b0edde66763aa9"
FILES = {
    "pcea-ucns/PLAN.md": "174018de5208397e191ed4b10aaa00c3cff43e84",
    "pcea-ucns/README.md": "fc1187dbaffd0a542287392e4e64a9553e3e42df",
    "pcea-ucns/asymmetric-paths-assessment.md": "708e68c4e00cc884c616333eae3df552981ac58f",
    "pcea-ucns/attack1_minkowski_break.py": "4378a28fdac9b59aa6bf2be1f11d0f2b5a359e84",
    "pcea-ucns/attack_harness.py": "79d70b4d3520a949bb75893fed7c30f41f972f38",
    "pcea-ucns/avenues.md": "d5ab74a84644b4e19095339ec5e5e8c2bdcf79bf",
    "pcea-ucns/candidate-ledger.json": "e0965b4b7fb24e83db5369dd16af29ff86c5bef6",
    "pcea-ucns/factor_count_sweep.py": "48ea5e802a660228733ec06f29cff6c99c437128",
    "pcea-ucns/feasibility-investigation.md": "2e2d7b6845990fd69e0f0989f9440cf6625dffbd",
    "pcea-ucns/gonal_architecture.py": "a24e31110521b30ca941bf151b99458a06c910af",
    "pcea-ucns/one_way_map_gate.py": "1cc2c3637dc93475a3f7edc19b7ecca68362d0ab",
    "pcea-ucns/option_d_ucns_map.py": "3bdc91e4975f3122cbfd3b6f5338049d4676d73c",
    "pcea-ucns/option_family_specs.py": "d5e7bcae866003c413119869d7be2ebd339892e3",
    "pcea-ucns/positional_attack.py": "30fce01b51bcb855105de7dc904a8ea7ed739919",
    "pcea-ucns/prefix_read_break.py": "2acd92b9fdd43f8b81662a154f76795664baf33c",
    "pcea-ucns/projection_action_candidate.py": "e9cdaa612c7c71b26456fcb9c2be908803e8f136",
    "pcea-ucns/pruning_scaling.py": "f820f87e4440a807739b8e948e629b13c1475671",
    "pcea-ucns/quotient_attack.py": "00d54912f14f0df52a16887671cf1759b155080d",
    "pcea-ucns/three_factor_attack.py": "e24a9618415316a1a9977d2cb9a9fdfe742e56e9",
    "pcea-ucns/ucns-crypto-domain-v0.md": "ffa79dc459e424a5f5654454b208bf1bc23a0b4d",
    "pcea-ucns/ucns_compat.py": "cdf8ee4996c390e5753003c1fc1b3b5e622a2fdb",
    "rec.md": "c2f576d7fb1077d78535d17672f05ac441114bce",
    "tests/test_attack1_minkowski_break.py": "291c392608f4acced36e31987b08aa1dd0cfc074",
    "tests/test_attack_harness.py": "06b776119d898ed7d0374ba3861a84a885310a9a",
    "tests/test_factor_count_sweep.py": "a6dd2fc8fb33cf179a57963b52075a8bc9472b58",
    "tests/test_gonal_architecture.py": "d622fc6e85543ad99ce3f374b4fbbc1971d82812",
    "tests/test_one_way_map_gate.py": "9e61ed890c53e4550100bade6f86b7f928b564c8",
    "tests/test_option_d_ucns_map.py": "641c08579ed34a769e43d4d199f331072b00ff7c",
    "tests/test_option_family_specs.py": "38922acd951468884b181d4f53ab0d42d4717374",
    "tests/test_positional_attack.py": "05b52ad0e6a791c70974d08e1ebc59d738d7ca11",
    "tests/test_prefix_read_break.py": "bcf4d57e32edf3669841948b92968372275b6e5c",
    "tests/test_projection_action_candidate.py": "1f841c57aff58b1a3ea0df5dd277add8d6dec677",
    "tests/test_pruning_scaling.py": "8db8d55799f1c050de2a6fb72625d0980b78bc4c",
    "tests/test_quotient_attack.py": "cb82d85de13e20d3ff14b5692164b0213a692c37",
    "tests/test_three_factor_attack.py": "7ed6d70c448630d2759a644547deeb1895e0108d",
    "tests/test_ucns_candidate_ledger.py": "3167d980fbeb5e285a056da59a595463f729b556",
}


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def raw_url(path: str) -> str:
    quoted = urllib.parse.quote(path)
    return f"https://raw.githubusercontent.com/{SOURCE_REPO}/{SOURCE_COMMIT}/{quoted}"


def fetch(path: str) -> bytes:
    request = urllib.request.Request(raw_url(path), headers={"User-Agent": "stack-pcea-research-migration/1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def verify(path: pathlib.Path, expected: str) -> tuple[bool, str]:
    if not path.is_file():
        return False, "missing"
    actual = git_blob_sha(path.read_bytes())
    return actual == expected, actual


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="migrated", help="materialization root relative to this script")
    parser.add_argument("--check", action="store_true", help="verify existing files; do not access network")
    parser.add_argument("--force", action="store_true", help="overwrite an existing mismatched file")
    args = parser.parse_args()

    root = pathlib.Path(__file__).resolve().parent / args.target
    failures: list[str] = []

    for source_path, expected in FILES.items():
        destination = root / source_path
        ok, observed = verify(destination, expected)
        if args.check:
            if not ok:
                failures.append(f"{source_path}: expected {expected}, observed {observed}")
            continue
        if ok:
            print(f"ok      {source_path}")
            continue
        if destination.exists() and not args.force:
            failures.append(f"{source_path}: local file differs ({observed}); use --force to replace")
            continue
        data = fetch(source_path)
        actual = git_blob_sha(data)
        if actual != expected:
            failures.append(f"{source_path}: downloaded blob {actual}, expected {expected}")
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        print(f"written {source_path}")

    if failures:
        print("hmmm: materialization incomplete", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print(f"verified {len(FILES)} files from {SOURCE_REPO}@{SOURCE_COMMIT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
