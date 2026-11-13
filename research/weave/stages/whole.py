"""Specified last/first operation over one complete joined stream.

Usage: bind no additional law; supply Streams((joined_bits,)). Multiple lanes are an
incompatible ablation until a real join law exists; this stage never joins implicitly.
No network/storage. Disable only 'whole' to measure its contribution.
"""
from probe import inward, inverse_inward
from .api import Operator, Step, Streams


def transform(value, reverse=False):
    if not isinstance(value, Streams) or len(value.lanes) != 1:
        raise TypeError('whole requires one already joined stream; no implicit join')
    return Streams(((inverse_inward if reverse else inward)(value.lanes[0]),))


def forward(value, context):
    return transform(value)


def inverse(value, context):
    return transform(value, True)


STEP = Step('whole', ('Q5',), 'Last/first interleave over the complete joined stream.',
            builtin=Operator(forward, inverse, 'literal-whole-inward-v1'))
