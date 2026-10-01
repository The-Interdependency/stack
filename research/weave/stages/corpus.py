"""Actual-material traversal candidate; native corpus-origin binding remains open.

Usage: content_route_operator(); parameters['corpus'] = ((material_id, bit_offset), ...).
Selected material bytes are supplied in context.public_material, never taken from a
filename hash. Bit 0 consumes the current left end; bit 1 consumes the right end.
Material bits are MSB-first and repeat cyclically. This concrete rule is a NEW,
explicit assistant proposal for correction, not a recovered requirement or cipher.
Inverse recomputes the traversal from material, without an encoder trace.
"""
from collections import deque
from .api import Blocked, Operator, Step, Streams


def route(size: int, material: bytes, offset: int = 0) -> tuple[int, ...]:
    if type(size) is not int or size < 0:
        raise ValueError('nonnegative bit length required')
    if type(material) is not bytes or not material:
        raise ValueError('nonempty actual corpus bytes required')
    if type(offset) is not int or offset < 0:
        raise ValueError('nonnegative corpus bit offset required')
    remaining = deque(range(size))
    out = []
    for i in range(size):
        p = (offset + i) % (8 * len(material))
        right = (material[p // 8] >> (7 - p % 8)) & 1
        out.append(remaining.pop() if right else remaining.popleft())
    return tuple(out)


def transform(value, context, reverse=False):
    if not isinstance(value, Streams):
        raise TypeError('corpus traversal requires Streams')
    choices = context.parameters.get('corpus')
    if type(choices) is not tuple or len(choices) != len(value.lanes):
        raise Blocked('corpus: select material and bit offset for every lane')
    out = []
    for lane, choice in zip(value.lanes, choices):
        if type(choice) is not tuple or len(choice) != 2 or type(choice[0]) is not str:
            raise ValueError('invalid corpus choice')
        label, offset = choice
        if label not in context.public_material:
            raise Blocked('corpus: forward-accessible material is missing')
        order = route(len(lane), context.public_material[label], offset)
        if reverse:
            restored = [0] * len(lane)
            for destination, source in enumerate(order):
                restored[source] = lane[destination]
            out.append(tuple(restored))
        else:
            out.append(tuple(lane[i] for i in order))
    return Streams(tuple(out))


def forward(value, context):
    return transform(value, context)


def inverse(value, context):
    return transform(value, context, True)


def content_route_operator() -> Operator:
    return Operator(forward, inverse, 'transport/corpus-end-route-v1', scope='transport')


STEP = Step('corpus', ('Q4', 'Q7', 'Q8'), 'Native corpus/thread relation remains unresolved.')
