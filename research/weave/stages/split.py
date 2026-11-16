"""Explicit occurrence routing, not the missing native thread projection law.

Usage: Operator = explicit_route_operator(); context.parameters['split'] is
(thread_count, owners), with one owner per incoming bit occurrence. The cyclic
route helper is a named transport-only proposal. No native law is auto-bound.
No data copies per lane: every occurrence is assigned once, including empty lanes.
"""
from .api import Blocked, Operator, Step, Streams


def cyclic_route(size: int, count: int) -> tuple[int, ...]:
    """Provisional transport routing; gives no per-thread confidentiality."""
    if type(size) is not int or size < 0 or type(count) is not int or count < 3:
        raise ValueError('nonnegative length and thread count >= 3 required')
    return tuple(i % count for i in range(size))


def plan(context):
    value = context.parameters.get('split')
    if type(value) is not tuple or len(value) != 2:
        raise Blocked('split: provide (thread_count, occurrence_owners)')
    count, owners = value
    if type(count) is not int or count < 3 or type(owners) is not tuple:
        raise ValueError('invalid thread plan')
    if any(type(i) is not int or not 0 <= i < count for i in owners):
        raise ValueError('route contains an invalid owner')
    return count, owners


def forward(value, context):
    if not isinstance(value, Streams) or len(value.lanes) != 1:
        raise TypeError('split requires one serialized input stream; not a gonol substitute')
    count, owners = plan(context)
    if len(owners) != len(value.lanes[0]):
        raise ValueError('split route does not cover every input occurrence')
    lanes = [[] for _ in range(count)]
    for bit, owner in zip(value.lanes[0], owners):
        lanes[owner].append(bit)
    return Streams(tuple(tuple(lane) for lane in lanes))


def inverse(value, context):
    count, owners = plan(context)
    if not isinstance(value, Streams) or len(value.lanes) != count:
        raise ValueError('split inverse lane count mismatch')
    sizes = tuple(owners.count(i) for i in range(count))
    if tuple(map(len, value.lanes)) != sizes:
        raise ValueError('split inverse occurrence counts differ')
    cursors = [0] * count
    out = []
    for owner in owners:
        out.append(value.lanes[owner][cursors[owner]])
        cursors[owner] += 1
    return Streams((tuple(out),))


def explicit_route_operator() -> Operator:
    return Operator(forward, inverse, 'transport/explicit-occurrence-route-v1', scope='transport')


STEP = Step('split', ('Q3',), 'Native complementary thread law remains unresolved.')
