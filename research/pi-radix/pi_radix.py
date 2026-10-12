#!/usr/bin/env python3
"""Deterministic bounded scans of prime structure in radix expansions of pi.

Usage
-----
From the Stack repository root::

    python research/pi-radix/pi_radix.py scan

Custom output paths and experiment parameters are available through ``--help``.
The default invocation regenerates the committed v1 JSON receipt and Markdown
report. The implementation uses no network, storage service, or non-stdlib package.

The scan proves only the exact finite computations recorded by its receipt. It
does not infer normality, randomness, cryptographic entropy, or a base-independent
law from finite digit samples.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


# === MODULE_BUILD ===
# id: pi_radix_prime_scan
#   module_name: pi_radix
#   module_kind: experiment
#   summary: Computes exact bounded radix symbols of pi, angular coordinates, prime blocks, and cross-base recurrences.
#   owner: The-Interdependency/stack research
#   public_surface: angular_symbol, base_digits, decode_block, is_prime_u64, run_experiment, CLI scan
#   internal_surface: chudnovsky_pi, analyze_base, render_report
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: research/pi-radix/tests/test_pi_radix.py
#   rollout: explicit CLI execution; no runtime integration
#   rollback: remove research/pi-radix and its Stack research-participant projections
#   since: 2026-10-10
#   unresolved: base-independent segmentation criterion
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: pi_radix_precision_agreement
#   given: a requested base set and symbol count
#   then: two independently generated precision profiles must agree symbol-for-symbol before analysis
#   class: numerical_correctness
#   since: 2026-10-10
#
# id: pi_radix_exact_angular_identity
#   given: digit d in base b with 0 <= d < b
#   then: turn d/b, degrees 360*d/b, and pi-radian coefficient 2*d/b are returned as reduced exact fractions
#   class: representation
#   since: 2026-10-10
#
# id: pi_radix_prime_claim_bounded
#   given: a canonical block of at most four symbols in a configured base
#   then: its decoded value is tested deterministically below 2^64 and no finite result is promoted to a base-independent law
#   class: evidence_boundary
#   since: 2026-10-10
#
# id: pi_radix_receipt_deterministic
#   given: identical source, configuration, and Python integer semantics
#   then: canonical JSON payload and receipt_sha256 are byte-identical
#   class: reproducibility
#   since: 2026-10-10
#
# id: pi_radix_configuration_faithful
#   given: an admitted experiment configuration
#   then: bounded allocation and complete prefixes precede analysis; reports use configured counts and lengths
#   class: correctness
#
# id: pi_radix_overlap_complete
#   given: unequal radix prefix lengths
#   then: phase comparisons include every position present in at least two streams
#   class: correctness
# === END CONTRACTS ===


ROOT = Path(__file__).resolve().parent
LOADED_SOURCE = Path(__file__).read_bytes()
DEFAULT_CONFIG = ROOT / "EXPERIMENT.json"
DEFAULT_RECEIPT = ROOT / "receipts" / "pi-radix-scan-v1.json"
DEFAULT_REPORT = ROOT / "docs" / "pi-radix-scan-v1.md"
UINT64_LIMIT = 1 << 64
MAX_BASE = 100_000
# Admission budgets bound retained symbols, block decoding/hit storage, and
# repeated alphabet enumeration across both profiles. These are resource limits,
# not scientific stopping rules; the frozen seven-base experiment fits in full.
MAX_TOTAL_SYMBOLS = 100_000
MAX_BLOCK_DIGIT_WORK = 2_000_000
MAX_SIEVE_WORK = 2_000_000
MAX_DECIMAL_DIGITS = 10_000
MAX_GENERATION_DIGIT_WORK = 50_000_000
SUPPORTED_RULES = {
    "constant": "pi",
    "canonical_block_rule": "the first symbol is nonzero",
    "angular_symbol_rule": "digit d in base b maps to exp(2*pi*i*d/b); exact turn d/b, degrees 360*d/b, pi-radian coefficient 2*d/b",
    "precision_verification": "generate independently at required decimal precision plus 80 and plus 180 guard digits; all requested symbols must agree",
}
MR_BASES_64 = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_snapshot(paths: Iterable[Path]) -> dict[Path, bytes]:
    """Capture receipt inputs before computation; never hash later substitutes."""
    return {path: path.read_bytes() for path in paths}


def require_unchanged(sources: dict[Path, bytes]) -> None:
    for path, original in sources.items():
        if path.read_bytes() != original:
            raise ValueError(f"source changed during execution: {path}")


def require_loaded(path: Path, loaded: bytes, sources: dict[Path, bytes]) -> None:
    if sources[path] != loaded:
        raise ValueError(f"source differs from loaded implementation: {path}")


def n_fraction(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def chudnovsky_pi(decimal_digits: int) -> Decimal:
    """Return pi with ``decimal_digits`` significant decimal digits."""

    if decimal_digits < 32:
        raise ValueError("decimal_digits must be at least 32")
    with localcontext() as context:
        context.prec = decimal_digits + 20
        constant = Decimal(426880) * Decimal(10005).sqrt()
        multiplier = 1
        linear = 13591409
        exponential = 1
        step = 6
        series = Decimal(linear)
        for index in range(1, decimal_digits // 14 + 3):
            multiplier = (step**3 - 16 * step) * multiplier // index**3
            linear += 545140134
            exponential *= -262537412640768000
            series += Decimal(multiplier * linear) / Decimal(exponential)
            step += 12
        context.prec = decimal_digits
        return +(constant / series)


def base_digits(value: Decimal, base: int, count: int) -> tuple[int, list[int]]:
    """Return integer part and ``count`` fractional digits in ``base``."""

    if base < 2:
        raise ValueError("base must be at least 2")
    if count < 0:
        raise ValueError("count cannot be negative")
    # Decimal operations obey the *current* context rather than retaining the
    # precision used to construct ``value``. Preserve all supplied significant
    # digits here; otherwise the fractional tail silently becomes zero after
    # the caller's ambient (often 28-digit) precision is exhausted.
    supplied_precision = len(value.as_tuple().digits)
    with localcontext() as context:
        context.prec = max(32, supplied_precision + 10)
        integer = int(value)
        fraction = value - integer
        digits: list[int] = []
        for _ in range(count):
            fraction *= base
            digit = int(fraction)
            if not 0 <= digit < base:
                raise ArithmeticError("radix digit escaped its canonical range")
            digits.append(digit)
            fraction -= digit
        return integer, digits


def angular_symbol(base: int, digit: int) -> dict[str, Any]:
    """Return the exact unit-circle coordinate labels for one radix symbol."""

    if base < 2 or not 0 <= digit < base:
        raise ValueError("angular symbol requires base >= 2 and 0 <= digit < base")
    turn = Fraction(digit, base)
    degrees = 360 * turn
    pi_radians = 2 * turn
    return {
        "base": base,
        "digit": digit,
        "turn": n_fraction(turn),
        "degrees": n_fraction(degrees),
        "pi_radian_coefficient": n_fraction(pi_radians),
        "complex_form": f"exp(2*pi*i*{digit}/{base})",
    }


def decode_block(digits: Iterable[int], base: int) -> int:
    value = 0
    for digit in digits:
        if not 0 <= digit < base:
            raise ValueError("block digit outside base")
        value = value * base + digit
    return value


def is_prime_u64(number: int) -> bool:
    """Deterministic Miller-Rabin primality for ``0 <= number < 2**64``."""

    if not 0 <= number < UINT64_LIMIT:
        raise ValueError("deterministic v1 primality domain is unsigned 64-bit")
    if number < 2:
        return False
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if number % prime == 0:
            return number == prime
    odd_part = number - 1
    shifts = 0
    while odd_part % 2 == 0:
        shifts += 1
        odd_part //= 2
    for witness in MR_BASES_64:
        if witness % number == 0:
            continue
        candidate = pow(witness, odd_part, number)
        if candidate in (1, number - 1):
            continue
        for _ in range(shifts - 1):
            candidate = candidate * candidate % number
            if candidate == number - 1:
                break
        else:
            return False
    return True


def prime_sieve(limit: int) -> list[int]:
    if limit >= MAX_BASE:
        raise ValueError(f"sieve limit must be below {MAX_BASE}")
    if limit < 2:
        return []
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for candidate in range(2, math.isqrt(limit) + 1):
        if flags[candidate]:
            start = candidate * candidate
            flags[start : limit + 1 : candidate] = b"\x00" * (((limit - start) // candidate) + 1)
    return [index for index, flag in enumerate(flags) if flag]


def factorization(number: int) -> list[list[int]]:
    remaining = number
    result: list[list[int]] = []
    candidate = 2
    while candidate * candidate <= remaining:
        exponent = 0
        while remaining % candidate == 0:
            remaining //= candidate
            exponent += 1
        if exponent:
            result.append([candidate, exponent])
        candidate = 3 if candidate == 2 else candidate + 2
    if remaining > 1:
        result.append([remaining, 1])
    return result


def totient(number: int) -> int:
    result = number
    for prime, _ in factorization(number):
        result -= result // prime
    return result


def digit_stream_sha256(digits: list[int]) -> str:
    width = len(str(max(digits, default=0)))
    wire = (" ".join(f"{digit:0{width}d}" for digit in digits) + "\n").encode("ascii")
    return sha256_bytes(wire)


def analyze_base(base: int, digits: list[int], lengths: list[int]) -> dict[str, Any]:
    if not 2 <= base <= MAX_BASE:
        raise ValueError(f"base must be in 2..{MAX_BASE} for bounded alphabet enumeration")
    primes = set(prime_sieve(base - 1))
    prime_symbols = [
        {"position": position, "digit": digit}
        for position, digit in enumerate(digits, 1)
        if digit in primes
    ]
    blocks: dict[str, Any] = {}
    prefix_hits: dict[int, list[dict[str, int]]] = defaultdict(list)
    for length in lengths:
        if base**length > UINT64_LIMIT:
            raise ValueError(f"base {base}, block length {length} exceeds v1 primality domain")
        canonical_count = 0
        eligible_count = 0
        hits: list[dict[str, Any]] = []
        for start in range(0, len(digits) - length + 1):
            block = digits[start : start + length]
            if block[0] == 0:
                continue
            canonical_count += 1
            value = decode_block(block, base)
            if length == 1 or value == base or math.gcd(block[-1], base) == 1:
                eligible_count += 1
            if is_prime_u64(value):
                hit = {"position": start + 1, "digits": block, "value": value}
                hits.append(hit)
                prefix_hits[start + 1].append({"length": length, "value": value})
        blocks[str(length)] = {
            "window_count": max(0, len(digits) - length + 1),
            "canonical_count": canonical_count,
            "terminal_gcd_eligible_count": eligible_count,
            "prime_count": len(hits),
            "prime_hits": hits,
        }
    nested = [
        {"position": position, "prime_prefixes": hits}
        for position, hits in sorted(prefix_hits.items())
        if len(hits) >= 2
    ]
    return {
        "base": base,
        "base_factorization": factorization(base),
        "totient": totient(base),
        "symbol_count": len(digits),
        "information_depth_bits": format(len(digits) * math.log2(base), ".12f"),
        "integer_part": 3,
        "digits": digits,
        "digit_stream_sha256": digit_stream_sha256(digits),
        "angular_symbol_law": {
            "turn": "d/base",
            "degrees": "360*d/base",
            "pi_radian_coefficient": "2*d/base",
            "complex": "exp(2*pi*i*d/base)",
        },
        "first_symbol_angular_example": angular_symbol(base, digits[0]),
        "prime_digit_alphabet_count": len(primes),
        "prime_valued_symbol_count": len(prime_symbols),
        "uniform_symbol_expectation": n_fraction(Fraction(len(digits) * len(primes), base)),
        "prime_valued_symbols": prime_symbols,
        "blocks": blocks,
        "nested_prime_prefixes": nested,
    }


def cross_base_results(scans: list[dict[str, Any]]) -> dict[str, Any]:
    recurrence_index: dict[int, list[dict[str, int]]] = defaultdict(list)
    for scan in scans:
        for length_text, block_result in scan["blocks"].items():
            length = int(length_text)
            if length < 2:
                continue
            for hit in block_result["prime_hits"]:
                recurrence_index[hit["value"]].append(
                    {"base": scan["base"], "position": hit["position"], "length": length}
                )
    recurrences = []
    for value, occurrences in sorted(recurrence_index.items()):
        if len({item["base"] for item in occurrences}) >= 2:
            recurrences.append({"prime": value, "occurrences": occurrences})

    phase_collisions = []
    symbol_count = max((scan["symbol_count"] for scan in scans), default=0)
    for position in range(symbol_count):
        phases: dict[Fraction, list[dict[str, int]]] = defaultdict(list)
        for scan in scans:
            if position >= scan["symbol_count"]:
                continue
            digit = scan["digits"][position]
            phases[Fraction(digit, scan["base"])].append({"base": scan["base"], "digit": digit})
        for phase, symbols in sorted(phases.items()):
            if len(symbols) >= 2:
                phase_collisions.append(
                    {"position": position + 1, "turn": n_fraction(phase), "symbols": symbols}
                )
    return {
        "decoded_prime_recurrences_minimum_block_length_2": recurrences,
        "aligned_exact_angular_phase_matches": phase_collisions,
    }


def required_decimal_digits(max_base: int, symbol_count: int) -> int:
    return math.ceil(symbol_count * math.log10(max_base))


def horizon_count(base: int, bits: int) -> int:
    """Largest n with base**n <= 2**bits, corrected using exact integers."""
    n = math.floor(bits / math.log2(base))
    limit = 1 << bits
    while base**n > limit:
        n -= 1
    while base**(n + 1) <= limit:
        n += 1
    return n


def load_config(path: Path) -> dict[str, Any]:
    return validate_config(json.loads(path.read_bytes()))


def validate_config(config: Any) -> dict[str, Any]:
    if not isinstance(config, dict):
        raise ValueError("experiment configuration must be an object")
    if config.get("schema") != "stack.pi-radix-experiment" or config.get("version") != "1.0.0":
        raise ValueError("unsupported experiment schema or version")
    for field, implemented in SUPPORTED_RULES.items():
        if config.get(field) != implemented:
            raise ValueError(f"unsupported {field}: v1 implements {implemented!r}")
    for field in ("questions", "nonclaims"):
        values = config.get(field)
        if not isinstance(values, list) or not values or any(not isinstance(v, str) or not v.strip() for v in values):
            raise ValueError(f"{field} must contain nonempty text entries")
    bases = config.get("bases")
    lengths = config.get("prime_block_lengths")
    count = config.get("fractional_symbol_count")
    horizon = config.get("matched_information_horizon_bits")
    if not isinstance(bases, list) or not bases or any(type(base) is not int or base < 2 for base in bases):
        raise ValueError("bases must be a nonempty list of integers >= 2")
    if len(set(bases)) != len(bases):
        raise ValueError("bases must be unique")
    if max(bases) > MAX_BASE:
        raise ValueError(f"base limit is {MAX_BASE}")
    if type(count) is not int or count <= 0:
        raise ValueError("fractional_symbol_count must be positive")
    if type(horizon) is not int or horizon <= 0:
        raise ValueError("matched_information_horizon_bits must be positive")
    if count > 100_000 or horizon > 1_000_000:
        raise ValueError("bounded profile requires count <= 100000 and horizon <= 1000000")
    if len(bases) * count > MAX_TOTAL_SYMBOLS:
        raise ValueError(f"aggregate symbol limit is {MAX_TOTAL_SYMBOLS}")
    if 2 * sum(bases) > MAX_SIEVE_WORK:
        raise ValueError(f"aggregate sieve work limit is {MAX_SIEVE_WORK}")
    if not isinstance(lengths, list) or not lengths or any(type(length) is not int or length < 1 for length in lengths):
        raise ValueError("prime_block_lengths must be positive integers")
    if lengths != sorted(set(lengths)):
        raise ValueError("prime_block_lengths must be sorted and unique")
    if max(lengths) > 64 or max(bases) ** max(lengths) > UINT64_LIMIT:
        raise ValueError("configured block domain exceeds deterministic unsigned-64-bit primality")
    # Matched prefixes cannot exceed count, so this safely bounds both profiles
    # before expensive horizon arithmetic or pi generation begins.
    if 2 * len(bases) * count * sum(lengths) > MAX_BLOCK_DIGIT_WORK:
        raise ValueError(f"aggregate block digit work limit is {MAX_BLOCK_DIGIT_WORK}")
    required = required_decimal_digits(max(bases), count)
    if required > MAX_DECIMAL_DIGITS:
        raise ValueError(f"required decimal precision limit is {MAX_DECIMAL_DIGITS}")
    # Bound both the Chudnovsky precision/term count and repeated high-precision
    # extraction. Symbol count alone does not account for Decimal operand size.
    if 2 * len(bases) * count * (required + 180) > MAX_GENERATION_DIGIT_WORK:
        raise ValueError(f"aggregate generation digit work limit is {MAX_GENERATION_DIGIT_WORK}")
    # The smallest base has the longest horizon prefix. ceil(log2(b**(count+1)))
    # is exactly (b**(count+1)-1).bit_length(), without constructing 2**horizon
    # or any horizon-sized power. count/precision were already admitted above.
    if (min(bases) ** (count + 1) - 1).bit_length() <= horizon:
        raise ValueError("matched information horizon exceeds generated stream")
    matched_counts = [horizon_count(base, horizon) for base in bases]
    if min(matched_counts) < max(lengths):
        raise ValueError("matched information horizon is too small for configured blocks")
    if max(matched_counts) > count:
        raise ValueError("matched information horizon exceeds generated stream")
    return config


def run_experiment(config_path: Path = DEFAULT_CONFIG) -> dict[str, Any]:
    implementation = Path(__file__)
    sources = source_snapshot((config_path, implementation))
    require_loaded(implementation, LOADED_SOURCE, sources)
    config = validate_config(json.loads(sources[config_path]))
    bases = config["bases"]
    count = config["fractional_symbol_count"]
    lengths = config["prime_block_lengths"]
    required = required_decimal_digits(max(bases), count)
    precisions = [required + 80, required + 180]
    digit_runs: list[dict[int, list[int]]] = []
    integer_parts: list[int] = []
    for precision in precisions:
        pi_value = chudnovsky_pi(precision)
        run: dict[int, list[int]] = {}
        for base in bases:
            integer, digits = base_digits(pi_value, base, count)
            if integer != 3:
                raise ArithmeticError("pi integer part is not 3")
            run[base] = digits
            integer_parts.append(integer)
        digit_runs.append(run)
    mismatches = [base for base in bases if digit_runs[0][base] != digit_runs[1][base]]
    if mismatches:
        raise ArithmeticError(f"precision verification failed for bases {mismatches}")

    scans = [analyze_base(base, digit_runs[1][base], lengths) for base in bases]
    horizon = config["matched_information_horizon_bits"]
    matched_scans = []
    for base in bases:
        matched_count = horizon_count(base, horizon)
        matched_scans.append(analyze_base(base, digit_runs[1][base][:matched_count], lengths))
    matched_summaries = []
    for scan in matched_scans:
        matched_summaries.append(
            {
                "base": scan["base"],
                "symbol_count": scan["symbol_count"],
                "information_depth_bits": scan["information_depth_bits"],
                "prime_valued_symbol_count": scan["prime_valued_symbol_count"],
                "blocks": {
                    length: {
                        "canonical_count": block["canonical_count"],
                        "terminal_gcd_eligible_count": block["terminal_gcd_eligible_count"],
                        "prime_count": block["prime_count"],
                    }
                    for length, block in scan["blocks"].items()
                },
            }
        )
    payload: dict[str, Any] = {
        "schema": "stack.pi-radix-scan-receipt",
        "version": "1.0.0",
        "standing": "COMPUTATION",
        "classification": "BASE_DEPENDENT_STRUCTURE_MEASURED",
        "base_independent_digit_law": "NOT_ESTABLISHED",
        "config_sha256": sha256_bytes(sources[config_path]),
        "implementation_sha256": sha256_bytes(sources[implementation]),
        "precision_verification": {
            "required_decimal_digits": required,
            "executed_decimal_precisions": precisions,
            "all_symbol_streams_equal": True,
        },
        "experiment": config,
        "base_results": scans,
        "cross_base_results": cross_base_results(scans),
        "matched_information_profile": {
            "horizon_bits": horizon,
            "selection_rule": "largest whole-symbol prefix with symbol_count*log2(base) <= horizon_bits",
            "base_results": matched_summaries,
            "cross_base_results": cross_base_results(matched_scans),
        },
        "nonclaims": config["nonclaims"],
        "hmmm": [
            "The matched-information profile uses logarithmic bit depth; it does not create a base-independent segmentation.",
            "Cross-base recurrence of a decoded prime does not establish a generating law.",
            "No statistical claim about normality is licensed by this finite prefix."
        ],
    }
    payload["receipt_sha256"] = sha256_bytes(canonical_json_bytes(payload))
    require_unchanged(sources)
    return payload


def fraction_text(pair: list[int]) -> str:
    return str(pair[0]) if pair[1] == 1 else f"{pair[0]}/{pair[1]}"


def render_report(receipt: dict[str, Any]) -> str:
    count = receipt["experiment"]["fractional_symbol_count"]
    lengths = receipt["experiment"]["prime_block_lengths"]
    block_headers = " | ".join(f"L{length} eligible / prime" for length in lengths)
    horizon = receipt["matched_information_profile"]["horizon_bits"]
    lines = [
        "# Pi radix prime scan v1",
        "",
        "Classification: **BASE_DEPENDENT_STRUCTURE_MEASURED**",
        "",
        "Standing: **COMPUTATION**",
        "",
        "Base-independent digit law: **NOT_ESTABLISHED**",
        "",
        f"The first {count} fractional symbols of pi were generated twice at the recorded",
        "decimal precisions. Every symbol agreed before analysis. Each digit `d` in",
        "base `b` is also the exact unit-circle symbol",
        "`exp(2*pi*i*d/b)`; degrees and radians are derived coordinates, not identity.",
        "",
        "## Results",
        "",
        f"| Base | Factorization | phi(base) | Prime-valued symbols / prime digit-values | {block_headers} | Resolution bits |",
        "|---:|---|---:|---:|" + "---:|" * (len(lengths) + 1),
    ]
    for result in receipt["base_results"]:
        factors = " * ".join(
            str(prime) if exponent == 1 else f"{prime}^{exponent}"
            for prime, exponent in result["base_factorization"]
        )
        block_cells = []
        for length in lengths:
            block = result["blocks"][str(length)]
            block_cells.append(f'{block["terminal_gcd_eligible_count"]} / {block["prime_count"]}')
        lines.append(
            f'| {result["base"]} | {factors} | {result["totient"]} | '
            f'{result["prime_valued_symbol_count"]} / {result["prime_digit_alphabet_count"]} | '
            + " | ".join(block_cells) + f' | {result["information_depth_bits"]} |'
        )

    recurrences = receipt["cross_base_results"]["decoded_prime_recurrences_minimum_block_length_2"]
    phases = receipt["cross_base_results"]["aligned_exact_angular_phase_matches"]
    lines.extend(
        [
            "",
            "For multi-symbol values, the terminal digit gives an exact sieve:",
            "`gcd(value, base) = gcd(last_digit, base)`. A block whose terminal digit",
            "shares a factor with the base is composite except for `[1, 0]` in a",
            "prime radix, whose value is the radix itself. Eligibility retains this",
            "exception (and lets primality reject composite radices). The contrast",
            "between 359, 360, and 361 therefore measures base factorization rather than",
            "merely alphabet size.",
            "",
            "## Cross-base observations",
            "",
            f"- Decoded prime values recurring in at least two bases, using configured canonical blocks of length >= 2: **{len(recurrences)}**.",
            f"- Aligned positions with exactly equal reduced unit-circle phase in at least two bases: **{len({item['position'] for item in phases})}** (**{len(phases)}** phase groups).",
        ]
    )
    if recurrences:
        lines.extend(["", "### Recurrent decoded primes", "", "| Prime | Occurrences `(base, position, length)` |", "|---:|---|"])
        for item in recurrences:
            occurrences = ", ".join(
                f'({entry["base"]}, {entry["position"]}, {entry["length"]})'
                for entry in item["occurrences"]
            )
            lines.append(f'| {item["prime"]} | {occurrences} |')
    if phases:
        lines.extend(["", "### Aligned exact angular phases", "", "| Position | Turn | Symbols `(base:digit)` |", "|---:|---:|---|"])
        for item in phases:
            symbols = ", ".join(f'{entry["base"]}:{entry["digit"]}' for entry in item["symbols"])
            lines.append(f'| {item["position"]} | {fraction_text(item["turn"])} | {symbols} |')

    matched = receipt["matched_information_profile"]
    matched_recurrences = matched["cross_base_results"]["decoded_prime_recurrences_minimum_block_length_2"]
    lines.extend(
        [
            "",
            "## Common information-horizon profile",
            "",
            f'This profile uses the longest whole-symbol prefix at or below **{matched["horizon_bits"]} bits** in every base.',
            "",
            f"| Base | Symbols used | Resolution bits | {block_headers} |",
            "|" + "---:|" * (3 + len(lengths)),
        ]
    )
    for result in matched["base_results"]:
        block_cells = []
        for length in lengths:
            block = result["blocks"][str(length)]
            block_cells.append(f'{block["terminal_gcd_eligible_count"]} / {block["prime_count"]}')
        lines.append(
            f'| {result["base"]} | {result["symbol_count"]} | {result["information_depth_bits"]} | '
            + " | ".join(block_cells) + " |"
        )
    lines.extend(
        [
            "",
            f'- Recurrent decoded primes within the common information horizon: **{len(matched_recurrences)}**.',
        ]
    )
    if matched_recurrences:
        lines.extend(["", "| Prime | Occurrences `(base, position, length)` |", "|---:|---|"])
        for item in matched_recurrences:
            occurrences = ", ".join(
                f'({entry["base"]}, {entry["position"]}, {entry["length"]})'
                for entry in item["occurrences"]
            )
            lines.append(f'| {item["prime"]} | {occurrences} |')

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "Primality belongs to each decoded integer independently of its notation.",
            "Its occurrence as a selected block belongs to that radix representation.",
            "A recurrence across bases is therefore a valid observation and a candidate",
            "for a later law, not the law itself. Exact angular equality similarly shows",
            "shared circle position without making the surrounding digit streams identical.",
            "",
            f"The fixed {count}-symbol scans span different resolution depths. The common",
            f"{horizon:,}-bit profile changes the prefix length by base and keeps that second",
            "comparison separate. Neither profile supplies a sampling theorem.",
            "Resolution bits describe radix cell width, not measured entropy of pi.",
            "",
            "## Reproduction",
            "",
            "```bash",
            "python research/pi-radix/pi_radix.py scan",
            "python -m unittest discover -s research/pi-radix/tests -v",
            "```",
            "",
            f'Receipt SHA-256: `{receipt["receipt_sha256"]}`',
            "",
            "## hmmm",
            "",
            "A base-independent segmentation rule remains the next test. The same prime",
            "arriving through two doors is a witness;",
            "it has not yet testified that the doors share an architect.",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(receipt: dict[str, Any], output: Path, report: Path) -> None:
    # Complete both renderings before modifying either artifact.
    report_text = render_report(receipt)
    receipt_text = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    output.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(receipt_text, encoding="utf-8")
    report.write_text(report_text, encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    scan = subparsers.add_parser("scan", help="run the configured bounded scan")
    scan.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    scan.add_argument("--output", type=Path, default=DEFAULT_RECEIPT)
    scan.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "scan":
        receipt = run_experiment(args.config.resolve())
        write_outputs(receipt, args.output.resolve(), args.report.resolve())
        print(f'pi-radix: wrote {args.output} and {args.report}; receipt {receipt["receipt_sha256"]}')
        return 0
    raise AssertionError("unreachable command")


if __name__ == "__main__":
    raise SystemExit(main())
