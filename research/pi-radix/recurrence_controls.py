#!/usr/bin/env python3
"""Exploratory controls for the frozen pi-radix recurrence statistic.

Run from Stack: python research/pi-radix/recurrence_controls.py
Resolution bits measure radix cell width, not entropy. Same-number controls
preserve cross-radix dependence; per-profile shuffles are sensitivity checks.
"""
from __future__ import annotations

import hashlib
import json
import math
import statistics
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import pi_radix as scan

# === MODULE_BUILD ===
# id: pi_radix_recurrence_controls
#   module_name: recurrence_controls
#   module_kind: experiment
#   summary: Tests finite prime recurrence counts against shared-number and histogram controls.
#   owner: The-Interdependency/stack research
#   public_surface: run_controls, main
#   internal_surface: interval_digits, recurrence, summary, Draws
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/pi-radix/tests/test_recurrence_controls.py
#   rollout: explicit offline command
#   rollback: remove control module and its outputs; retain original scan
#   unresolved: held-out invariants and statistical power outside the fixed prefix
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: pi_control_same_number
#   given: a dyadic interval and a list of radices
#   then: every returned prefix describes that same interval; ambiguous boundaries fail
#
# id: pi_control_count_distinct
#   given: canonical blocks of lengths 2 through 4
#   then: count distinct prime values in at least two bases, not repeated occurrences within one base
#
# id: pi_control_shuffle_preserves
#   given: a radix stream and a deterministic draw source
#   then: the shuffled stream preserves its exact multiset and length
#
# id: pi_control_source_bound
#   given: valid source receipt, plan, and fixed seed
#   then: the deterministic control receipt binds sources, all replicate counts, and honest tail ranks
# === END CONTRACTS ===

ROOT = Path(__file__).resolve().parent
LOADED_SOURCE = Path(__file__).read_bytes()
TRIALS = 199
BITS = 8192
SEED = "stack/pi-radix/controls/v1"
RECEIPT = ROOT / "receipts/recurrence-controls-v1.json"
REPORT = ROOT / "docs/recurrence-controls-v1.md"
SOURCE_PATHS = (Path(__file__), ROOT / "pi_radix.py", scan.DEFAULT_CONFIG,
                scan.DEFAULT_RECEIPT, ROOT / "CONTROL_PLAN.md",
                ROOT / "tests/test_recurrence_controls.py", ROOT / "tests/test_pi_radix.py")


class Draws:
    """SHAKE256 counter stream; rejection sampling avoids modulo bias."""

    def __init__(self, label: str):
        self.label = label
        self.counter = 0

    def bytes(self, size: int) -> bytes:
        payload = scan.canonical_json_bytes([SEED, self.label, self.counter])
        self.counter += 1
        return hashlib.shake_256(payload).digest(size)

    def below(self, bound: int) -> int:
        if bound < 1:
            raise ValueError("positive bound required")
        size = max(1, (bound.bit_length() + 7) // 8)
        modulus = 1 << (8 * size)
        cutoff = modulus - modulus % bound
        while True:
            value = int.from_bytes(self.bytes(size), "big")
            if value < cutoff:
                return value % bound


def shuffled(digits: list[int], draws: Draws) -> list[int]:
    result = list(digits)
    for i in range(len(result) - 1, 0, -1):
        j = draws.below(i + 1)
        result[i], result[j] = result[j], result[i]
    return result


def interval_digits(j: int, bits: int, base: int, count: int) -> list[int]:
    """Certify a prefix for EVERY point in [j/2**bits, (j+1)/2**bits)."""
    if bits < 1 or base < 2 or count < 0 or not 0 <= j < 1 << bits:
        raise ValueError("invalid interval or radix")
    denominator = 1 << bits
    power = base**count
    low = j * power // denominator
    high = ((j + 1) * power - 1) // denominator
    if low != high:
        raise ArithmeticError("control interval straddles a requested radix boundary")
    result = []
    remainder = j
    for _ in range(count):
        digit, remainder = divmod(remainder * base, denominator)
        result.append(digit)
    return result


@lru_cache(maxsize=32_768)
def prime(value: int) -> bool:
    return scan.is_prime_u64(value)


def recurrence(streams: dict[int, list[int]]) -> dict:
    supports = defaultdict(set)
    for base, digits in streams.items():
        for length in (2, 3, 4):
            for start in range(len(digits) - length + 1):
                block = digits[start:start + length]
                if block[0] == 0:
                    continue
                value = scan.decode_block(block, base)
                # A canonical multi-symbol value is >= base. The sole prime
                # sharing a divisor with the radix can therefore be base itself.
                if value != base and math.gcd(block[-1], base) != 1:
                    continue
                if prime(value):
                    supports[value].add(base)
    rows = [{"prime": n, "bases": sorted(bases)}
            for n, bases in sorted(supports.items()) if len(bases) >= 2]
    return {"count": len(rows), "primes": rows}


def summary(observed: int, counts: list[int]) -> dict:
    if not counts:
        raise ValueError("control counts cannot be empty")
    values = sorted(counts)
    def quantile(p: float) -> int:
        return values[max(0, math.ceil(p * len(values)) - 1)]
    exceed = sum(n >= observed for n in counts)
    return {
        "observed": observed, "trials": len(counts),
        "mean": statistics.mean(counts), "median": statistics.median(counts),
        "min": values[0], "max": values[-1],
        "central_95_percent_empirical_range": [quantile(.025), quantile(.975)],
        "at_least_observed": exceed,
        "upper_tail_rank": [exceed + 1, len(counts) + 1],
        "observed_minus_control_mean": observed - statistics.mean(counts),
    }


def run_controls(trials: int = TRIALS) -> dict:
    if type(trials) is not int or not 1 <= trials <= TRIALS:
        raise ValueError("trial count outside fixed bounded plan")
    sources = scan.source_snapshot(SOURCE_PATHS)
    scan.require_loaded(Path(__file__), LOADED_SOURCE, sources)
    scan.require_loaded(ROOT / "pi_radix.py", scan.LOADED_SOURCE, sources)
    receipt = json.loads(sources[scan.DEFAULT_RECEIPT])
    payload = dict(receipt)
    claimed = payload.pop("receipt_sha256")
    if scan.sha256_bytes(scan.canonical_json_bytes(payload)) != claimed:
        raise ValueError("source receipt digest mismatch")
    if receipt["implementation_sha256"] != scan.sha256_bytes(sources[ROOT / "pi_radix.py"]):
        raise ValueError("source receipt is stale against scanner")
    if receipt["config_sha256"] != scan.sha256_bytes(sources[scan.DEFAULT_CONFIG]):
        raise ValueError("source receipt is stale against configuration")
    config = scan.validate_config(json.loads(sources[scan.DEFAULT_CONFIG]))
    if (config["bases"] != [30, 60, 359, 360, 361, 720, 2880]
            or config["fractional_symbol_count"] != 500
            or config["matched_information_horizon_bits"] != 2400
            or config["prime_block_lengths"] != [1, 2, 3, 4]):
        raise ValueError("control v1 requires the frozen experiment")
    streams = {r["base"]: r["digits"] for r in receipt["base_results"]}
    sizes = {b: scan.horizon_count(b, 2400) for b in streams}
    profiles = {"fixed500": streams,
                "matched2400": {b: d[:sizes[b]] for b, d in streams.items()}}
    observed = {name: recurrence(s) for name, s in profiles.items()}
    # Cross-check optimized classifier against the original recorded hit list.
    for name, original in (
        ("fixed500", receipt["cross_base_results"]),
        ("matched2400", receipt["matched_information_profile"]["cross_base_results"]),
    ):
        expected = [r["prime"] for r in original["decoded_prime_recurrences_minimum_block_length_2"]]
        if expected != [r["prime"] for r in observed[name]["primes"]]:
            raise ArithmeticError("recurrence classifier disagrees with source scan")
    rows = []
    for index in range(trials):
        j = int.from_bytes(Draws(f"shared/{index}").bytes(BITS // 8), "big")
        shared = {b: interval_digits(j, BITS, b, 500) for b in streams}
        row = {"trial": index,
               "common_interval_numerator_hex": format(j, "02048x"),
               "shared_number": {}, "histogram_shuffle": {}}
        for name, original in profiles.items():
            generated = {b: shared[b][:len(d)] for b, d in original.items()}
            mixed = {b: shuffled(d, Draws(f"shuffle/{index}/{name}/{b}"))
                     for b, d in original.items()}
            row["shared_number"][name] = recurrence(generated)["count"]
            row["histogram_shuffle"][name] = recurrence(mixed)["count"]
        rows.append(row)
    summaries = {control: {
        name: summary(observed[name]["count"], [r[control][name] for r in rows])
        for name in profiles} for control in ("shared_number", "histogram_shuffle")}
    result = {
        "schema": "stack.pi-radix-recurrence-controls", "version": "1.0.0",
        "standing": "COMPUTATION", "inference": "EXPLORATORY_MODEL_COMPARISON",
        "seed": SEED, "interval_bits": BITS, "trials": trials,
        "primary": "shared_number/matched2400 upper-tail recurrence count",
        "sources_sha256": {str(p.relative_to(ROOT)): scan.sha256_bytes(data)
                           for p, data in sources.items()},
        "observed": observed, "summaries": summaries, "replicates": rows,
        "hmmm": [
            "Pi was observed before this plan: ranks are exploratory, not confirmatory p-values.",
            "Uniform same-number and conditional histogram controls answer different questions.",
            "No claim of normality, randomness, or absence of every base-independent invariant.",
            "Resolution bits describe positional precision, not measured entropy.",
        ],
    }
    result["receipt_sha256"] = scan.sha256_bytes(scan.canonical_json_bytes(result))
    scan.require_unchanged(sources)
    return result


def render_report(result: dict) -> str:
    lines = ["# Cross-base recurrence controls v1", "", "Standing: **COMPUTATION**", "",
             "Question: is the observed recurrence count exceptional under the fixed controls?", "",
             "| Control | Profile | Pi | Mean | Median | Central 95% range | >= Pi | Upper-tail rank |",
             "|---|---|---:|---:|---:|---|---:|---|"]
    for control in ("shared_number", "histogram_shuffle"):
        for name in ("fixed500", "matched2400"):
            s = result["summaries"][control][name]
            low, high = s["central_95_percent_empirical_range"]
            numerator, denominator = s["upper_tail_rank"]
            lines.append(f'| {control} | {name} | {s["observed"]} | {s["mean"]:.3f} | '
                         f'{s["median"]} | {low}–{high} | {s["at_least_observed"]}/{s["trials"]} | '
                         f'{numerator}/{denominator} |')
    primary = result["summaries"]["shared_number"]["matched2400"]
    rank = primary["upper_tail_rank"]
    low, high = primary["central_95_percent_empirical_range"]
    inside = low <= primary["observed"] <= high
    lines += ["", "## Interpretation", "",
              f'Pi has {primary["observed"]} shared primes; the primary control median is '
              f'{primary["median"]}. The observed count is '
              f'{"inside" if inside else "outside"} the empirical central 95% range.',
              f'The primary upper-tail rank is {rank[0]}/{rank[1]}. '
              'This is a model-relative exploratory comparison, not a theorem or a confirmatory test.',
              "The shared-number control retains dependencies between bases by encoding the same",
              "8192-bit dyadic interval in all seven radices; interval-boundary checks certify",
              "that any real in that interval has the reported prefixes. SHAKE256 generates",
              "reproducible pseudorandom draws; ideal uniform draws are the modeling assumption.",
              "The shuffle control preserves each pi profile's exact digit frequencies but",
              "destroys order and common-number consistency. It is a separate sensitivity check.",
              "", "## Scope and reproduction", "",
              "Primary statistic: distinct prime values present in >=2 bases, lengths 2–4,",
              "canonical nonzero leading symbols, 2400-bit resolution horizon. Fixed-500 is",
              "secondary. Values are deduplicated within each base. The exact eight previously",
              "observed primes were not treated as a preselected significance target.",
              "All replicate counts and interval numerators are recorded in the JSON receipt.",
              "", "```bash", "python research/pi-radix/pi_radix.py scan",
              "python research/pi-radix/recurrence_controls.py",
              "python -m unittest discover -s research/pi-radix/tests -v", "```", "",
              f'Receipt payload SHA-256: `{result["receipt_sha256"]}`', "", "## hmmm", "",
              "A frequent pattern can still be useful. Its frequency alone does not distinguish",
              "pi from the comparison ensemble; a proposed invariant needs its own executable rule.", ""]
    return "\n".join(lines)


def main() -> None:
    result = run_controls()
    report = render_report(result)
    scan.publish_artifacts([(RECEIPT, (json.dumps(result, sort_keys=True, indent=2) + "\n").encode()),
                            (REPORT, report.encode())], SOURCE_PATHS)
    print(report)


if __name__ == "__main__":
    main()
