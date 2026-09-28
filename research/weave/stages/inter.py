"""Specified section-local last/first operation, with explicit sequential partitions.

Usage: PublicContext/PrivateContext.parameters['inter'] = tuple of per-lane stage
partitions; each partition is the exact tuple of positive section lengths.
No default arity schedule, remainder rule, thread route or minimum stage count.
This explicit sequential profile is a proposal, not an additional user requirement.
No network/storage; rollback by disabling 'inter' for a labelled ablation.
"""
from probe import section_stage
from .api import Blocked, Operator, Step, Streams


def transform(value, context, reverse=False):
    if not isinstance(value, Streams):
        raise TypeError('inter requires Streams from the selected upstream native law')
    plans = context.parameters.get('inter')
    if type(plans) is not tuple or len(plans) != len(value.lanes):
        raise Blocked('inter: Q6 requires explicit partitions for every lane')
    out = []
    for lane, stages in zip(value.lanes, plans):
        if type(stages) is not tuple or not stages:
            raise Blocked('inter: supply a nonempty explicit stage sequence per lane')
        for partition in reversed(stages) if reverse else stages:
            lane = section_stage(lane, partition, reverse=reverse)
        out.append(lane)
    return Streams(tuple(out))


def forward(value, context):
    return transform(value, context)


def inverse(value, context):
    return transform(value, context, True)


STEP = Step('inter', ('Q6',), 'Exact section-local last/first interleave.',
            builtin=Operator(forward, inverse, 'literal-section/sequential-explicit-v1'))
