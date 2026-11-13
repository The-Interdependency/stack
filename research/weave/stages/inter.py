"""Literal last/first interleave with explicit or proposed balanced partitions.

Usage: parameters['inter'] = per-lane tuples of exact partition tuples.
Use balanced_schedule(n, arities) to select the provisional quotient/remainder
rule: first r sections gain one bit, including explicit empty sections if a > n.
Stages consume prior output; section order and all supplied repetitions survive.
There is no three-stage minimum. The sealed run-1 probe is left unchanged.
"""
from probe import inward, inverse_inward
from .api import Blocked, Operator, Step, Streams


def balanced_partition(size: int, arity: int) -> tuple[int, ...]:
    if type(size) is not int or size < 0 or type(arity) is not int or arity < 3:
        raise ValueError('nonnegative size and arity >= 3 required')
    q, r = divmod(size, arity)
    return tuple(q + (i < r) for i in range(arity))


def balanced_schedule(size: int, arities: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    if type(arities) is not tuple or not arities:
        raise ValueError('supply a nonempty schedule; switch inter off for omission')
    return tuple(balanced_partition(size, a) for a in arities)


def section(items: tuple, lengths: tuple[int, ...], reverse=False) -> tuple:
    if (type(lengths) is not tuple or len(lengths) < 3
            or any(type(v) is not int or v < 0 for v in lengths)
            or sum(lengths) != len(items)):
        raise ValueError('partition must account for all bits with nonnegative lengths')
    transform = inverse_inward if reverse else inward
    out, start = [], 0
    for length in lengths:
        out.extend(transform(items[start:start + length]))
        start += length
    return tuple(out)


def transform(value, context, reverse=False):
    if not isinstance(value, Streams):
        raise TypeError('inter requires Streams from an explicit upstream law/profile')
    plans = context.parameters.get('inter')
    if type(plans) is not tuple or len(plans) != len(value.lanes):
        raise Blocked('inter: explicit partitions required for every lane')
    out = []
    for lane, stages in zip(value.lanes, plans):
        if type(stages) is not tuple or not stages:
            raise Blocked('inter: a nonempty stage sequence is required')
        for partition in reversed(stages) if reverse else stages:
            lane = section(lane, partition, reverse)
        out.append(lane)
    return Streams(tuple(out))


def forward(value, context):
    return transform(value, context)


def inverse(value, context):
    return transform(value, context, True)


STEP = Step('inter', ('Q6',), 'Literal section-local last/first interleave.',
            builtin=Operator(forward, inverse, 'literal-section/sequential-empty-aware-v2'))
