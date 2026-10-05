# === MODULE_BUILD ===
# id: weave_prime_schedule
#   module_name: prime_schedule
#   module_kind: engine
#   summary: executed prime-index and embedded-span routes determine nonempty bit partitions and reversible first/last interleaving
#   owner: Erin Spencer
#   public_surface: Route, SplitPlan, plan, interleave
#   internal_surface: exact composition unranking
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   tests: tests/test_cycle.py
#   rollout: explicit prime-route-compositions-v1 profile only
#   rollback: remove scheduler and its cycle bindings
#   requires: weave_numeral_construction
#   unresolved: distinct routes can induce identical maps; no key entropy or asymmetry claim
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: prime_split_replay
#   given: a verified prime route, admissible arities and current bit length
#   then: exact deterministic nonempty sections cover the stream and reproduce without source plaintext
# id: first_last_inverse
#   given: admitted sections and an explicit first-last or last-first order
#   then: every source bit appears once and reversing the operation restores exact bytes
# === END CONTRACTS ===
"""Usage: route = Route.evaluate(PrimePath(53, (('next',),)))
       split = plan(128, route, (3,5,7))
       assert interleave(interleave(data, split), split, inverse=True) == data

This is a named candidate determinant, not a universal arity law. The actual
prime-index/span route is evaluated, including source, base, span and step order.
A prefix-bearing radix numeral of that route selects an arity and a ranked
composition. Routes remain distinct records even when their resulting maps agree.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import comb
from numeral import PrimePath, Limits, Refused

PROFILE = 'prime-route-compositions-v1'


@dataclass(frozen=True)
class Route:
    path: PrimePath
    trace: tuple[int, ...]
    determinant: int

    @classmethod
    def evaluate(cls, path: PrimePath, limits: Limits = Limits(), *, engine=None):
        if type(path) is not PrimePath:
            raise Refused('PrimePath required')
        trace = path.replay(limits, _engine=engine)
        tokens = [path.seed, len(path.steps)]
        for step, value in zip(path.steps, trace[1:]):
            tokens.extend((0, value) if step == ('next',) else (1, *step[1:], value))
        base = max(tokens)+2
        determinant = 1  # Retains leading zero tokens and sequence length.
        for token in tokens:
            determinant = determinant*base + token
        return cls(path, trace, determinant)


@dataclass(frozen=True)
class SplitPlan:
    bit_length: int
    lengths: tuple[int, ...]
    rank: int


def _composition(n: int, arity: int, rank: int) -> tuple[int, ...]:
    """Unrank ordered nonempty sections via lexicographic gap combinations."""
    total = comb(n-1, arity-1)
    if not 0 <= rank < total:
        raise Refused('composition rank outside domain')
    gaps, minimum, remaining = [], 1, arity-1
    while remaining:
        low, high = minimum, n-remaining
        all_remaining = comb(n-minimum, remaining)
        while low < high:
            middle = (low+high+1)//2
            skipped = all_remaining - comb(n-middle, remaining)
            if skipped <= rank:
                low = middle
            else:
                high = middle-1
        selected = low
        rank -= all_remaining - comb(n-selected, remaining)
        gaps.append(selected)
        minimum, remaining = selected+1, remaining-1
    points = (0, *gaps, n)
    return tuple(b-a for a,b in zip(points, points[1:]))


def plan(bit_length: int, route: Route, arities: tuple[int, ...]) -> SplitPlan:
    if type(bit_length) is not int or bit_length < 1:
        raise Refused('positive bit length required')
    if type(route) is not Route:
        raise Refused('executed Route required')
    if (type(arities) is not tuple or not arities
            or any(type(a) is not int or not 2 <= a <= min(64,bit_length) for a in arities)
            or len(set(arities)) != len(arities)):
        raise Refused('distinct admissible arities must be integers 2..min(64, bit_length)')
    arity = arities[route.determinant % len(arities)]
    rank = (route.determinant//len(arities)) % comb(bit_length-1, arity-1)
    return SplitPlan(bit_length, _composition(bit_length, arity, rank), rank)


def interleave(data: bytes, split: SplitPlan, *, inverse: bool = False,
               end_order: str = 'first-last') -> bytes:
    """Rearrange bits; do not reinterpret the output as bytes until the pass ends."""
    if type(data) is not bytes or type(split) is not SplitPlan:
        raise Refused('bytes and SplitPlan required')
    if type(inverse) is not bool or end_order not in ('first-last','last-first'):
        raise Refused('explicit Boolean inverse and supported end order required')
    if (type(split.bit_length) is not int or split.bit_length != len(data)*8
            or type(split.lengths) is not tuple or not split.lengths
            or any(type(n) is not int or n <= 0 for n in split.lengths)
            or sum(split.lengths) != split.bit_length):
        raise Refused('sections must cover every input bit exactly once')
    out = bytearray(len(data))
    offset = 0
    for length in split.lengths:
        left, right = offset, offset+length-1
        first = end_order == 'first-last'
        for destination in range(offset, offset+length):
            if first:
                source = left
                left += 1
            else:
                source = right
                right -= 1
            first = not first
            if inverse:
                read, write = destination, source
            else:
                read, write = source, destination
            bit = (data[read//8] >> (7-read%8)) & 1
            out[write//8] |= bit << (7-write%8)
        offset += length
    return bytes(out)
