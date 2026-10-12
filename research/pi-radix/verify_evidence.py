#!/usr/bin/env python3
"""Verify the full frozen experiment with GNU factor and an independent counter.

Usage from Stack: python research/pi-radix/verify_evidence.py [--write]
Default: compare the source-bound verification receipt without modifying files.
--write: save it only after full replay and independent comparisons succeed.
Requires GNU coreutils factor on PATH; no third-party Python packages or network.
The control draw/interval/shuffle code is reused; block decoding, primality,
phase matching, and recurrence counting are checked independently below.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import subprocess
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import pi_radix as scan
import recurrence_controls as controls

# === MODULE_BUILD ===
# id: pi_radix_independent_verifier
#   module_name: verify_evidence
#   module_kind: instrument
#   summary: Independently factors canonical blocks and counts all frozen scan/control recurrences.
#   owner: The-Interdependency/stack research
#   public_surface: CLI, verify
#   internal_surface: Oracle, recurrent, phase_pairs, require
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: full execution in pi-radix-research workflow
#   rollout: read-only default; explicit evidence regeneration
#   rollback: revert verifier and its receipt together
#   unresolved: control generation is reused; no mathematical generalization
# === END MODULE_BUILD ===

ROOT = Path(__file__).resolve().parent
LOADED_SOURCE = Path(__file__).read_bytes()
OUTPUT = ROOT / "receipts/independent-verification-v1.json"
SOURCE_PATHS = (Path(__file__), ROOT / "pi_radix.py", ROOT / "recurrence_controls.py",
                scan.DEFAULT_CONFIG, scan.DEFAULT_RECEIPT, controls.RECEIPT,
                scan.DEFAULT_REPORT, controls.REPORT, ROOT / "CONTROL_PLAN.md",
                ROOT / "tests/test_pi_radix.py", ROOT / "tests/test_recurrence_controls.py")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


class Oracle:
    """Factor each distinct integer once; storage is bounded by the frozen plan."""

    def __init__(self):
        self.primes = {}

    def classify(self, values):
        missing = sorted(set(values) - self.primes.keys())
        for offset in range(0, len(missing), 4096):
            batch = missing[offset:offset + 4096]
            result = subprocess.run(["factor"], input="\n".join(map(str, batch)) + "\n",
                                    text=True, capture_output=True, check=True)
            lines = result.stdout.splitlines()
            require(len(lines) == len(batch), "factor omitted results")
            for value, line in zip(batch, lines):
                number, factors = line.split(":", 1)
                factors = list(map(int, factors.split()))
                require(int(number) == value and math.prod(factors) == value,
                        f"factor identity mismatch for {value}")
                self.primes[value] = value >= 2 and factors == [value]
                require(scan.is_prime_u64(value) == self.primes[value],
                        f"primality classification differs for {value}")

    def blocks(self, streams, lengths):
        windows = []
        for base, digits in streams.items():
            for width in lengths:
                for start in range(len(digits) - width + 1):
                    if digits[start] == 0:
                        continue
                    # Direct place-value sum, with no production decoder or sieve.
                    value = sum(digits[start + i] * base**(width - i - 1) for i in range(width))
                    windows.append((base, width, start + 1, value))
        self.classify(row[3] for row in windows)
        return [row for row in windows if self.primes[row[3]]]


def recurrent(hits):
    support = defaultdict(set)
    for base, width, position, value in hits:
        if width >= 2:
            support[value].add(base)
    return [{"prime": value, "bases": sorted(bases)}
            for value, bases in sorted(support.items()) if len(bases) >= 2]


def phase_pairs(streams):
    matches = set()
    for left, right in itertools.combinations(sorted(streams), 2):
        for position, (a, b) in enumerate(zip(streams[left], streams[right]), 1):
            if a * right == b * left:
                matches.add((position, Fraction(a, left), left, right))
    return matches


def verify():
    sources = scan.source_snapshot(SOURCE_PATHS)
    for path, loaded in ((Path(__file__), LOADED_SOURCE), (ROOT / "pi_radix.py", scan.LOADED_SOURCE),
                         (ROOT / "recurrence_controls.py", controls.LOADED_SOURCE)):
        scan.require_loaded(path, loaded, sources)
    source = json.loads(sources[scan.DEFAULT_RECEIPT])
    control = json.loads(sources[controls.RECEIPT])
    require(scan.run_experiment() == source, "scan full replay differs")
    require(controls.run_controls() == control, "control full replay differs")
    require(scan.render_report(source) == sources[scan.DEFAULT_REPORT].decode(), "scan report differs")
    require(controls.render_report(control) == sources[controls.REPORT].decode(), "control report differs")
    oracle = Oracle()
    streams = {row["base"]: row["digits"] for row in source["base_results"]}
    sizes = {row["base"]: row["symbol_count"] for row in source["matched_information_profile"]["base_results"]}
    profiles = {"fixed500": streams, "matched2400": {b: d[:sizes[b]] for b, d in streams.items()}}
    observed = {}
    for profile, digits in profiles.items():
        hits = oracle.blocks(digits, (1, 2, 3, 4))
        observed[profile] = recurrent(hits)
        require(observed[profile] == control["observed"][profile]["primes"], f"{profile} recurrence differs")
        recorded = source if profile == "fixed500" else source["matched_information_profile"]
        for row in recorded["base_results"]:
            for width, block in row["blocks"].items():
                found = sorted((pos, value) for b, w, pos, value in hits if b == row["base"] and w == int(width))
                require(len(found) == block["prime_count"], "prime count differs")
                if "prime_hits" in block:
                    require(found == sorted((h["position"], h["value"]) for h in block["prime_hits"]),
                            "prime hit classification differs")
        actual_pairs = set()
        for match in recorded["cross_base_results"]["aligned_exact_angular_phase_matches"]:
            for left, right in itertools.combinations(sorted(s["base"] for s in match["symbols"]), 2):
                actual_pairs.add((match["position"], Fraction(*match["turn"]), left, right))
        require(actual_pairs == phase_pairs(digits), "pairwise phases differ")
    rows = []
    for row in control["replicates"]:
        index = row["trial"]
        j = int(row["common_interval_numerator_hex"], 16)
        shared = {b: controls.interval_digits(j, controls.BITS, b, len(d)) for b, d in streams.items()}
        result = {"trial": index, "shared_number": {}, "histogram_shuffle": {}}
        for profile, original in profiles.items():
            generated = {b: shared[b][:len(d)] for b, d in original.items()}
            mixed = {b: controls.shuffled(d, controls.Draws(f"shuffle/{index}/{profile}/{b}"))
                     for b, d in original.items()}
            for name, sample in (("shared_number", generated), ("histogram_shuffle", mixed)):
                hits = oracle.blocks(sample, (2, 3, 4))
                independent = recurrent(hits)
                require(independent == controls.recurrence(sample)["primes"],
                        f"trial {index} {name}/{profile}: classifications differ")
                result[name][profile] = len(independent)
                require(len(independent) == row[name][profile], f"trial {index}: receipt count differs")
        rows.append(result)
        if (index + 1) % 25 == 0:
            print(f"independent verification: {index + 1}/199 trials", flush=True)
    scan.require_unchanged(sources)
    return {
        "schema": "stack.pi-radix-independent-verification", "version": "1.0.0",
        "standing": "COMPUTATION", "oracle": "GNU coreutils factor; complete integer factorization",
        "sources_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(data).hexdigest() for p, data in sources.items()},
        "distinct_values_factored": len(oracle.primes), "control_counts_compared": len(rows) * 4,
        "classification_disagreements": 0, "recurrence_disagreements": 0,
        "observed": observed, "replicates": rows,
        "hmmm": ["Draw, interval, and shuffle generation reuse production code; classifier and counter are independent.",
                 "Finite-prefix agreement establishes neither pi normality nor base-independent laws nor cryptographic security."],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    receipt = verify()
    rendered = json.dumps(receipt, sort_keys=True, indent=2) + "\n"
    if args.write:
        scan.publish_artifacts([(OUTPUT, rendered.encode())], SOURCE_PATHS)
    else:
        require(OUTPUT.read_text() == rendered, "independent verification receipt differs")
    print(f"Verified {receipt['distinct_values_factored']} distinct integers and {receipt['control_counts_compared']} control counts")
