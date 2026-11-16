# === MODULE_BUILD ===
# id: weave_sequence_discovery
#   module_name: affixiation
#   module_kind: engine
#   summary: deterministic repeated-multibyte discovery and exact nonoverlapping partition for the Weave sequence cycle
#   owner: Erin Spencer
#   public_surface: Partition, discover
#   internal_surface: suffix array, LCP intervals, occurrence selection
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   tests: tests/test_cycle.py
#   rollout: explicitly selected maximal-lcp-longest-first-v1 profile
#   rollback: remove this module and its round-runner binding
#   unresolved: selection is a declared executable profile, not optimal compression or a universal affixiation rule
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: discovery_exact_partition
#   given: an admitted byte stream
#   then: selected repeated sequences and residual literals partition every source byte exactly once in order
# id: discovery_repeat_selection
#   given: competing and overlapping repeated multi-byte candidates
#   then: deterministic longest-first selection records nonoverlapping occurrences without erasing residual data
# id: discovery_resource_refusal
#   given: input or candidate-visit work exceeding the configured budget
#   then: refuse instead of silently truncating the candidate search
# id: discovery_closure_authority
#   given: sequence participants selected by this module
#   then: closure remains Stack-owned, consuming UCNS geometry; UCHC is the architecture reference
# === END CONTRACTS ===
"""Usage: partition = discover(raw_bytes); partition.restore() == raw_bytes.

This explicit profile selects maximal LCP candidates, longest first, breaking ties
by earliest source occurrence. When overlaps compete it retains leftmost available
nonoverlapping occurrences. Occurrence counts mean selected partition occurrences,
not every possible overlapping substring match. No maximum sequence-length heuristic
or fixed byte chunks are imposed. Residual runs remain exact literal definitions.
This module discovers participants. Stack-owned native_binary.py closes them
using native UCNS geometry; UCHC supplies the origin/axis architecture reference.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from numeral import Refused, ResourceLimit

PROFILE = 'maximal-lcp-longest-first-v1'


@dataclass(frozen=True)
class Partition:
    blocks: tuple[bytes, ...] = field(repr=False)
    order: tuple[int, ...]
    starts: tuple[int, ...]
    candidate_visits: int

    def restore(self) -> bytes:
        return b''.join(self.blocks[i] for i in self.order)

    @property
    def repeat_ids(self) -> tuple[int, ...]:
        counts = [0] * len(self.blocks)
        for i in self.order:
            counts[i] += 1
        return tuple(i for i, b in enumerate(self.blocks) if len(b) >= 2 and counts[i] >= 2)


def _suffix_array(data: bytes) -> list[int]:
    n = len(data)
    suffixes, ranks, width = list(range(n)), list(data), 1
    while width < n:
        suffixes.sort(key=lambda i: (ranks[i], ranks[i+width] if i+width < n else -1))
        next_ranks = [0] * n
        for j in range(1, n):
            a, b = suffixes[j-1], suffixes[j]
            different = ((ranks[a], ranks[a+width] if a+width < n else -1) !=
                         (ranks[b], ranks[b+width] if b+width < n else -1))
            next_ranks[b] = next_ranks[a] + int(different)
        ranks = next_ranks
        if ranks[suffixes[-1]] == n-1:
            break
        width *= 2
    return suffixes


def _lcp(data: bytes, suffixes: list[int]) -> list[int]:
    n, common = len(data), 0
    rank, values = [0]*n, [0]*n
    for i, pos in enumerate(suffixes):
        rank[pos] = i
    for start in range(n):
        i = rank[start]
        if i == 0:
            common = 0
            continue
        other = suffixes[i-1]
        while start+common < n and other+common < n and data[start+common] == data[other+common]:
            common += 1
        values[i] = common
        common = max(0, common-1)
    return values


class _Ranges:
    """Range min/max over suffix starts, with linear storage."""
    def __init__(self, values: list[int]):
        self.size = 1 << max(0, (len(values)-1).bit_length())
        self.low = [len(values)] * (2*self.size)
        self.high = [-1] * (2*self.size)
        self.low[self.size:self.size+len(values)] = values
        self.high[self.size:self.size+len(values)] = values
        for i in range(self.size-1, 0, -1):
            self.low[i] = min(self.low[2*i], self.low[2*i+1])
            self.high[i] = max(self.high[2*i], self.high[2*i+1])

    def query(self, start: int, end: int) -> tuple[int, int]:
        low, high = self.size, -1
        start, end = start+self.size, end+self.size
        while start < end:
            if start & 1:
                low, high = min(low, self.low[start]), max(high, self.high[start])
                start += 1
            if end & 1:
                end -= 1
                low, high = min(low, self.low[end]), max(high, self.high[end])
            start //= 2
            end //= 2
        return low, high


def _matching_interval(common: _Ranges, begin: int, end: int,
                       length: int, size: int) -> tuple[int, int]:
    """Expand a suffix interval to all occurrences of its shortened prefix.

    Adjacent suffixes share a length-L prefix exactly when all intervening LCP
    values are at least L. Range minima and binary search retain linear storage
    and avoid copying/enumerating long prefixes to locate their full interval.
    """
    low, high = 0, begin
    while low < high:
        middle = (low+high)//2
        if common.query(middle+1, begin+1)[0] >= length:
            high = middle
        else:
            low = middle+1
    expanded_begin = low
    low, high = end, size
    while low < high:
        middle = (low+high+1)//2
        if common.query(end, middle)[0] >= length:
            low = middle
        else:
            high = middle-1
    return expanded_begin, low


class _Occupied:
    def __init__(self, size: int):
        self.tree = [0] * (size+1)

    def prefix(self, end: int) -> int:
        total = 0
        while end:
            total += self.tree[end]
            end -= end & -end
        return total

    def free(self, start: int, length: int) -> bool:
        return self.prefix(start+length) == self.prefix(start)

    def mark(self, start: int, length: int) -> None:
        # Each source byte is marked at most once during a complete run.
        for pos in range(start+1, start+length+1):
            while pos < len(self.tree):
                self.tree[pos] += 1
                pos += pos & -pos


def discover(data: bytes, *, max_bytes: int = 1048576,
             visit_budget: int = 16000000) -> Partition:
    """Discover a complete deterministic partition or refuse its resource profile."""
    if type(data) is not bytes:
        raise Refused('byte-aligned source required for sequence discovery')
    if any(type(v) is not int or v < 1 for v in (max_bytes, visit_budget)):
        raise Refused('positive integer discovery budgets required')
    if len(data) > max_bytes:
        raise ResourceLimit('sequence source exceeds discovery byte budget')
    n = len(data)
    if n == 0:
        return Partition((), (), (), 0)
    suffixes = _suffix_array(data)
    common = _lcp(data, suffixes)
    ranges = _Ranges(suffixes)
    common_ranges = _Ranges(common)
    stack, candidates = [], set()
    for i in range(1, n+1):
        depth = common[i] if i < n else 0
        left = i-1
        while stack and stack[-1][0] > depth:
            length, begin = stack.pop()
            first, last = ranges.query(begin, i)
            capped = min(length, last-first)  # At least two disjoint occurrences.
            if capped >= 2:
                start, end = begin, i
                if capped != length:
                    start, end = _matching_interval(common_ranges, begin, i, capped, n)
                    first, _ = ranges.query(start, end)
                candidates.add((-capped, first, start, end))
            left = begin
        if depth and (not stack or stack[-1][0] < depth):
            stack.append((depth, left))
    candidates = sorted(candidates)
    occupied = _Occupied(n)
    chosen, patterns = [], set()
    covered = visits = 0
    for negative, first, begin, end in candidates:
        length = -negative
        if n-covered < 2*length:
            continue
        visits += end-begin
        if visits > visit_budget:
            raise ResourceLimit('candidate occurrence visits exceed discovery budget')
        selected, previous_end = [], -1
        for start in sorted(suffixes[begin:end]):
            if start >= previous_end and occupied.free(start, length):
                selected.append(start)
                previous_end = start+length
        if len(selected) < 2:
            continue
        block = data[selected[0]:selected[0]+length]
        if block in patterns:
            continue
        patterns.add(block)
        for start in selected:
            chosen.append((start, length))
            occupied.mark(start, length)
            covered += length
        if covered == n:
            break
    chosen.sort()
    segments, offset = [], 0
    for start, length in chosen:
        if start > offset:
            segments.append((offset, start-offset))
        segments.append((start, length))
        offset = start+length
    if offset < n:
        segments.append((offset, n-offset))
    blocks, order, starts, ids = [], [], [], {}
    for start, length in segments:
        block = data[start:start+length]
        if block not in ids:
            ids[block] = len(blocks)
            blocks.append(block)
        order.append(ids[block])
        starts.append(start)
    return Partition(tuple(blocks), tuple(order), tuple(starts), visits)
