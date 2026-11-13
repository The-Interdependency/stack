"""Explicit stable lane interlacing; not an invented secret native join law.

Usage: parameters['join'] = (lane_lengths, lane_order). Visit each named lane once
per cycle and skip only exhausted lanes. Exact lengths/order come independently
from the research profile on both sides, not from an encoder trace or ciphertext.
"""
from .api import Blocked, Operator, Step, Streams


def route(lengths: tuple[int, ...], order: tuple[int, ...]) -> tuple[int, ...]:
    if (type(lengths) is not tuple or not lengths
            or any(type(n) is not int or n < 0 for n in lengths)):
        raise ValueError('invalid lane lengths')
    if (type(order) is not tuple or any(type(i) is not int for i in order)
            or sorted(order) != list(range(len(lengths)))):
        raise ValueError('lane order must visit every lane exactly once per cycle')
    left, out = list(lengths), []
    while any(left):
        for owner in order:
            if left[owner]:
                out.append(owner)
                left[owner] -= 1
    return tuple(out)


def plan(context):
    value = context.parameters.get('join')
    if type(value) is not tuple or len(value) != 2:
        raise Blocked('join: explicit lengths and lane order required')
    lengths, order = value
    return lengths, route(lengths, order)


def forward(value, context):
    lengths, owners = plan(context)
    if not isinstance(value, Streams) or tuple(map(len, value.lanes)) != lengths:
        raise ValueError('join input lengths differ from declared route')
    cursors, out = [0] * len(lengths), []
    for owner in owners:
        out.append(value.lanes[owner][cursors[owner]])
        cursors[owner] += 1
    return Streams((tuple(out),))


def inverse(value, context):
    lengths, owners = plan(context)
    if not isinstance(value, Streams) or len(value.lanes) != 1:
        raise TypeError('join inverse requires one interlaced stream')
    if len(value.lanes[0]) != len(owners):
        raise ValueError('joined length differs from declared route')
    lanes = [[] for _ in lengths]
    for bit, owner in zip(value.lanes[0], owners):
        lanes[owner].append(bit)
    return Streams(tuple(tuple(lane) for lane in lanes))


def explicit_join_operator() -> Operator:
    return Operator(forward, inverse, 'transport/explicit-stable-join-v1', scope='transport')


STEP = Step('join', ('Q5', 'Q8'), 'Native key/context-derived join law remains unresolved.')
