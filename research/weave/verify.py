#!/usr/bin/env python3
"""Independent implementation of the positional checks; does not import probe.py.
Usage: python verify.py receipt.json > verified.json
Reads local source/receipt bytes; no network, no secrets, no system write except stdout.
Owner: Erin Spencer's Stack research. Rollback: remove this evidence verifier.
This is a second implementation by the same assistant, not an independent author review.
"""
from __future__ import annotations
import hashlib
import itertools
import json
from pathlib import Path
import sys


# Sealed run-1 provenance; receipt-controlled subsets cannot select what is verified.
EXPECTED_SOURCE_INPUTS = {'stack_head': '247af26527d0d76558dac1dd7fd05e41ce83112e', 'uchc_inspected_blob': '8b55823805c87ad8c4cc9d7451dc2eb90bdedd3a', 'local_sha256': {'probe.py': '9649f8ed463ceaa2ad466d8caa9af235bfe7fc3567fc2c17d94ed83f2853ae63', 'PLAN.md': '2d268639ef65a50083fd7737579ca893110e10765864f77237fdc9b187385f54'}}

def must(test: bool, message: str) -> None:
    if not test:
        raise ValueError(message)


def sha(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                          separators=(",", ":")).encode()).hexdigest()


def end_map(n: int) -> tuple[int, ...]:
    # Analytic forward index at output j; no deque and no encoder import.
    return tuple(n-1-j//2 if j % 2 == 0 else j//2 for j in range(n))


def transform_map(n: int, arities: tuple[int, ...]) -> tuple[int, ...]:
    p = tuple(range(n))
    for arity in arities:
        must(n % arity == 0, "not equal partition")
        width = n // arity
        local = end_map(width)
        q = tuple((j//width)*width + local[j % width] for j in range(n))
        p = tuple(p[index] for index in q)
    return tuple(p[index] for index in end_map(n))


def verify_sources(receipt):
    """Reject omission, substitution and drift before numerical evidence checks."""
    must(receipt.get("source_inputs") == EXPECTED_SOURCE_INPUTS,
         "complete source hash set and exact provenance identities required")
    root = Path(__file__).resolve().parent
    for name, expected in EXPECTED_SOURCE_INPUTS["local_sha256"].items():
        must(hashlib.sha256((root / name).read_bytes()).hexdigest() == expected,
             f"source mismatch: {name}")


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "receipt.json").resolve()
    r = json.loads(path.read_text())
    verify_sources(r)
    must(end_map(5) == (4, 0, 3, 1, 2), "literal odd golden vector")
    must(end_map(6) == (5, 0, 4, 1, 3, 2), "literal even golden vector")
    must(transform_map(6, (3,)) == (4, 1, 5, 0, 2, 3), "three-section golden vector")
    seen: set[tuple[int, ...]] = set()
    count = 0
    for depth, recorded in enumerate(r["schedules"]["by_depth"], start=1):
        at_depth = {transform_map(105, schedule)
                    for schedule in itertools.product((3, 5, 7), repeat=depth)}
        seen.update(at_depth)
        count += 3**depth
        must(recorded["distinct_at_depth"] == len(at_depth), "depth census mismatch")
        must(recorded["distinct_up_to_depth"] == len(seen), "cumulative census mismatch")
    must(count == r["schedules"]["tested"] == 9840, "schedule coverage mismatch")
    must(len(seen) == r["schedules"]["distinct_maps"], "map count mismatch")
    for collision in (r["schedules"]["first_collision_examples"] +
                      r["schedules"]["exact_period_collision_witnesses"]):
        p = transform_map(105, tuple(collision["first"]))
        q = transform_map(105, tuple(collision["second"]))
        must(p == q, "false schedule collision")
        must(sha(p) == collision["map_sha256"], "collision map digest mismatch")
    for case in r["inversion"]["scale_cases"]:
        must(sha(transform_map(case["bits"], (5, 7, 3))) == case["map_sha256"],
             "large map mismatch")
    for case in r["fixed_map_attack"]["cases"]:
        must(case["oracle_queries"] == (case["bits"]-1).bit_length(), "query count")
        must(sha(transform_map(case["bits"], (5, 7, 3))) == case["map_sha256"],
             "attack inferred map differs from independently constructed map")
    orders = {transform_map(105, order) for order in itertools.permutations((3, 5, 7))}
    must(len(orders) == 6, "example stage orders unexpectedly coincide")
    must(r["full_design"]["classification"] == "BLOCKED_NOT_EXECUTED" and
         not r["full_design"]["validated"] and not r["full_design"]["falsified"],
         "unsupported whole-system verdict")
    out = {"verification": "SURVIVED_SECOND_IMPLEMENTATION",
           "same_author": True, "independent_author_review": False,
           "imports_primary_runner": False,
           "receipt_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
           "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           "schedules_recomputed": count, "distinct_maps": len(seen),
           "distinct_orderings_of_3_5_7": len(orders),
           "full_design_verdict": "NOT_EVALUATED"}
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as exc:
        print(f"VERIFICATION_ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
