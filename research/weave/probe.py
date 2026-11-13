#!/usr/bin/env python3
"""Weave evidence runner: literal operations, not a substitute cryptosystem.

Usage: python probe.py > receipt.json
       python probe.py --check receipt.json
Python standard library only. The frozen scope and cases are in PLAN.md.
Network/auth/user-secret boundaries: none. Storage: stdout, or read-only --check.
Rollout: manually invoked research evidence. Rollback: remove this runner and
its unaccepted receipt; do not alter any upstream geometry or old sealed evidence.
Scientific criteria: PLAN.md. Full-system state is always reported separately.
"""
from __future__ import annotations

import argparse
from collections import deque
import hashlib
import itertools
import json
from math import gcd
from pathlib import Path
import random
import sys
from typing import Callable, Sequence, TypeVar

T = TypeVar("T")
Partitions = tuple[tuple[int, ...], ...]


def require(condition: bool, detail: str) -> None:
    """Raise on a failed witness even when Python assertions are optimized out."""
    if not condition:
        raise ValueError(detail)


def inward(items: Sequence[T]) -> tuple[T, ...]:
    """Literal user operation: rightmost, leftmost, and continue inward."""
    remaining = deque(items)
    out: list[T] = []
    while remaining:
        out.append(remaining.pop())
        if remaining:
            out.append(remaining.popleft())
    return tuple(out)


def inverse_inward(items: Sequence[T]) -> tuple[T, ...]:
    """Independently structured inverse, using the analytic index relation."""
    n = len(items)
    return tuple(items[2*i + 1] if i < n//2 else items[2*(n-1-i)]
                 for i in range(n))


def check_partition(lengths: tuple[int, ...], n: int) -> None:
    """Require every boundary explicitly; invent no remainder or empty-section rule."""
    require(isinstance(lengths, tuple), "partition must be an immutable tuple")
    require(len(lengths) >= 3, "this explicit experiment uses arities >= 3")
    require(all(type(v) is int and v > 0 for v in lengths),
            "section lengths must be positive non-Boolean integers")
    require(sum(lengths) == n, "section lengths do not cover the input exactly")


def section_stage(items: Sequence[T], lengths: tuple[int, ...], *,
                  reverse: bool = False) -> tuple[T, ...]:
    """Apply exactly one section operation, preserving explicit section order."""
    check_partition(lengths, len(items))
    transform = inverse_inward if reverse else inward
    offset = 0
    out: list[T] = []
    for length in lengths:
        out.extend(transform(items[offset:offset+length]))
        offset += length
    return tuple(out)


def forward(items: Sequence[T], partitions: Partitions) -> tuple[T, ...]:
    """Explicit sequential component profile; this is not Weave encryption."""
    require(isinstance(partitions, tuple) and len(partitions) > 0,
            "supply an explicit nonempty stage sequence")
    out = tuple(items)
    for lengths in partitions:
        out = section_stage(out, lengths)
    return inward(out)


def backward(items: Sequence[T], partitions: Partitions) -> tuple[T, ...]:
    """Undo final interleave, then invert all supplied stages in reverse order."""
    require(isinstance(partitions, tuple) and len(partitions) > 0,
            "supply an explicit nonempty stage sequence")
    out = inverse_inward(items)
    for lengths in reversed(partitions):
        out = section_stage(out, lengths, reverse=True)
    return out


def equal_partitions(n: int, schedule: tuple[int, ...]) -> Partitions:
    """Experimental profile only: exact equal division; refuse all remainders."""
    require(type(n) is int and n > 0, "positive non-Boolean length required")
    require(isinstance(schedule, tuple) and len(schedule) > 0, "empty schedule")
    result = []
    for arity in schedule:
        require(type(arity) is int and arity >= 3, "arity must be an integer >= 3")
        require(n % arity == 0, "uneven partition remains unselected")
        result.append((n//arity,) * arity)
    return tuple(result)


def bits(value: int, n: int) -> tuple[int, ...]:
    """Synthetic test data, not plaintext admission to the native gonol layer."""
    return tuple((value >> i) & 1 for i in range(n))


def digest(value: object) -> str:
    """Evidence identity only; never a key derivation or confidentiality step."""
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                          separators=(",", ":")).encode()).hexdigest()


def permutation_order(permutation: tuple[int, ...]) -> int:
    """Exact least positive period from the complete disjoint cycle lengths."""
    require(sorted(permutation) == list(range(len(permutation))), "not bijective")
    seen: set[int] = set()
    result = 1
    for start in range(len(permutation)):
        if start in seen:
            continue
        current, length = start, 0
        while current not in seen:
            seen.add(current)
            current = permutation[current]
            length += 1
        result = result * length // gcd(result, length)
    return result


def recover_fixed_map(oracle: Callable[[tuple[int, ...]], tuple[int, ...]],
                      n: int) -> tuple[tuple[int, ...], int]:
    """Attack receives only an oracle and length, never the arity schedule.

    Bit j of the i-th input position encodes i's j-th binary digit. Reassemble
    these labels at each output position. The attack requires a fixed positional
    map across its queries; it is not applied to the unimplemented full design.
    """
    labels = [0] * n
    query_count = (n-1).bit_length()
    for digit in range(query_count):
        answer = oracle(tuple((i >> digit) & 1 for i in range(n)))
        require(len(answer) == n, "oracle changed length")
        require(all(type(v) is int and v in (0, 1) for v in answer), "oracle not bits")
        for i, value in enumerate(answer):
            labels[i] |= value << digit
    require(sorted(labels) == list(range(n)),
            "probe observations do not identify a fixed positional bijection")
    return tuple(labels), query_count


def recover_with_map(output: Sequence[T], mapping: tuple[int, ...]) -> tuple[T, ...]:
    """Use the attack's inferred map, without any schedule or private state."""
    require(len(output) == len(mapping), "map length mismatch")
    positions = sorted(range(len(mapping)), key=mapping.__getitem__)
    return tuple(output[i] for i in positions)


def run() -> dict[str, object]:
    """Execute all preregistered finite domains; no skipped assertions or partial pass."""
    exhaustive_binary = 0
    for n in range(13):
        for value in range(1 << n):
            data = bits(value, n)
            require(inverse_inward(inward(data)) == data, "end operation inverse")
            exhaustive_binary += 1

    partition_cases = 0
    for n in range(3, 13):
        for mask in range(1 << (n-1)):
            boundaries = [0] + [i+1 for i in range(n-1) if mask & (1 << i)] + [n]
            lengths = tuple(b-a for a, b in zip(boundaries, boundaries[1:]))
            if len(lengths) < 3:
                continue
            data = tuple(range(n))
            encoded = section_stage(data, lengths)
            require(sorted(encoded) == list(data), "section bijection")
            require(section_stage(encoded, lengths, reverse=True) == data,
                    "section independent inverse")
            require(backward(forward(data, (lengths,)), (lengths,)) == data,
                    "final whole interleave inverse")
            partition_cases += 1

    n = 105
    maps: dict[tuple[int, ...], tuple[int, ...]] = {}
    collision_examples: list[dict[str, object]] = []
    total_schedules = 0
    by_depth = []
    # Only source-labelled inputs to the direct operation generate these maps.
    # No generic permutation generator stands in for the mechanism.
    for depth in range(1, 9):
        depth_maps: set[tuple[int, ...]] = set()
        for schedule in itertools.product((3, 5, 7), repeat=depth):
            partitions = equal_partitions(n, schedule)
            mapping = forward(tuple(range(n)), partitions)
            require(backward(mapping, partitions) == tuple(range(n)), "schedule inverse")
            if mapping in maps and len(collision_examples) < 5:
                first = maps[mapping]
                collision_examples.append({"first": first, "second": schedule,
                                           "map_sha256": digest(mapping)})
            else:
                maps.setdefault(mapping, schedule)
            depth_maps.add(mapping)
            total_schedules += 1
        by_depth.append({"depth": depth, "schedules": 3**depth,
                         "distinct_at_depth": len(depth_maps),
                         "distinct_up_to_depth": len(maps)})
    periods = {str(a): permutation_order(section_stage(tuple(range(n)), (n//a,)*a))
               for a in (3, 5, 7)}

    # A constructive collision exists at every finite stage period, regardless
    # of whether the bounded schedule census reaches that period.
    period_witnesses = []
    for arity in (3, 5, 7):
        period = periods[str(arity)]
        first = (5, 7, 3)
        second = first + (arity,) * period
        left = forward(tuple(range(n)), equal_partitions(n, first))
        right = forward(tuple(range(n)), equal_partitions(n, second))
        require(left == right, "cycle-period equivalent schedule witness")
        period_witnesses.append({"arity": arity, "period": period,
                                 "first": first, "second": second,
                                 "exact_maps_equal": True, "map_sha256": digest(left)})

    scale_cases = []
    for length in (105, 210, 420, 840, 8400, 67200):
        partitions = equal_partitions(length, (5, 7, 3))
        data = tuple(range(length))
        encoded = forward(data, partitions)
        require(backward(encoded, partitions) == data, "large independent recovery")
        scale_cases.append({"bits": length, "recovered_exactly": True,
                            "map_sha256": digest(encoded)})

    attack_cases = []
    weight_cases = 0
    for length in (105, 840, 8400):
        partitions = equal_partitions(length, (5, 7, 3))
        def oracle(x: tuple[int, ...]) -> tuple[int, ...]:
            return forward(x, partitions)
        mapping, queries = recover_fixed_map(oracle, length)
        rng = random.Random(20260928 + length)  # Test fixture only, not cryptographic entropy.
        for _ in range(64):
            data = tuple(rng.randrange(2) for _ in range(length))
            output = oracle(data)
            require(recover_with_map(output, mapping) == data, "held-out map attack")
            require(sum(output) == sum(data), "permutation weight invariant")
            weight_cases += 1
        for constant in (0, 1):
            data = (constant,) * length
            require(oracle(data) == data, "constant input invariant")
        attack_cases.append({"bits": length, "oracle_queries": queries,
                             "held_out_recoveries": 64, "schedule_given_to_attacker": False,
                             "actual_schedule_recovered": False,
                             "equivalent_inverse_recovered": True,
                             "map_sha256": digest(mapping)})

    rejected = 0
    invalid = [lambda: equal_partitions(8, (3,)), lambda: equal_partitions(105, ()),
               lambda: equal_partitions(105, (True,)), lambda: equal_partitions(105, (2,)),
               lambda: section_stage((0, 1, 2), (1, 1, 0)),
               lambda: section_stage((0, 1, 2), (1, 1, 2)),
               lambda: section_stage((0, 1, 2), (True, 1, 1)),
               lambda: forward((0, 1, 2), ())]
    for example in invalid:
        try:
            example()
        except ValueError:
            rejected += 1
        else:
            raise ValueError("invalid experimental input silently accepted")

    root = Path(__file__).resolve().parent
    sources = {name: hashlib.sha256((root/name).read_bytes()).hexdigest()
               for name in ("probe.py", "PLAN.md")}
    return {
        "schema": "weave.source-bound-evaluation", "version": "0.1.0",
        "source_inputs": {"stack_head": "247af26527d0d76558dac1dd7fd05e41ce83112e",
                          "uchc_inspected_blob": "8b55823805c87ad8c4cc9d7451dc2eb90bdedd3a",
                          "local_sha256": sources},
        "execution": {"status": "COMPLETED", "skipped_checks": 0,
                      "python_requirement": ">=3.10", "dependencies": "stdlib only"},
        "full_design": {"classification": "BLOCKED_NOT_EXECUTED",
                        "validated": False, "falsified": False,
                        "why": "No retrieved executable binding for private-gonol recovery, thread/corpus relation and public/private key relation.",
                        "not_substituted": ["gonol construction", "private gonol", "threads",
                                            "corpus binding", "asymmetric key relation"]},
        "profile_choices": {"stage_input": "previous-stage output: explicit experimental interpretation",
                            "section_order": "preserved: explicit experimental interpretation",
                            "remainders": "refused, not given a default",
                            "minimum_stage_count_claim": "none; arity is not depth",
                            "whole_system_claims": False},
        "inversion": {"classification": "SURVIVED_IN_DECLARED_COMPONENT_DOMAIN",
                      "exhaustive_binary_inputs": exhaustive_binary,
                      "all_positive_partitions_with_at_least_three_parts_through_n12": partition_cases,
                      "scale_cases": scale_cases},
        "schedules": {"length_bits": n, "arities": [3, 5, 7],
                      "depth_range_inclusive": [1, 8], "tested": total_schedules,
                      "distinct_maps": len(maps), "by_depth": by_depth,
                      "first_collision_examples": collision_examples,
                      "single_stage_periods": periods,
                      "exact_period_collision_witnesses": period_witnesses,
                      "claim": "Different schedules need not induce different maps; no whole-design verdict."},
        "fixed_map_attack": {"classification": "EQUIVALENT_INVERSE_RECOVERED_FOR_FIXED_MAP_PROFILE",
                             "assumption": "same length-preserving position map for all oracle calls",
                             "cases": attack_cases,
                             "not_tested": ["message-dependent transformation", "changing map per encryption", "full Weave"]},
        "bit_only_invariants": {"weight_checks": weight_cases,
                                "all_zero_and_all_one_fixed": True,
                                "scope": "bit rearrangement only, not unspecified gonol/corpus operations"},
        "input_refusals": {"rejected": rejected, "total": len(invalid)},
        "hmmm": ["Original pre-substitution thirteen-law transcript not recovered.",
                 "Private-gonol recovery binding remains unimplemented in inspected Weave source.",
                 "Native hyperspace producer inspected, not executed against its full corpus.",
                 "All required full-design relations remain in scope; these component results do not replace them."]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, help="recompute and compare a saved receipt byte-for-byte")
    args = parser.parse_args()
    try:
        result = run()
        data = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode()
        if args.check is not None:
            require(args.check.read_bytes() == data, "receipt differs from complete replay")
            print("receipt replay: exact match; whole-design status remains BLOCKED_NOT_EXECUTED")
        else:
            sys.stdout.buffer.write(data)
    except (OSError, ValueError) as exc:
        print(f"EVALUATION_ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
