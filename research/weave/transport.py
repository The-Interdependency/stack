"""Explicit provisional composition; native whole-Weave profile stays separate.

Usage: build(profile, bit_length, materials) independently on each side. Returned
contexts contain freshly compiled controls, not captured encoder state. Profile
files are research inputs, NOT a public key or a proposed ciphertext header.
The CLI limits one message to 64 KiB as an implementation resource guard.
"""
from assembly import Pipeline, Switches
from stages.api import Blocked, PrivateContext, PublicContext, Streams
from stages.split import cyclic_route, explicit_route_operator
from stages.corpus import content_route_operator
from stages.inter import balanced_schedule
from stages.join import explicit_join_operator

SCHEMA = 'weave.transport-profile/v1'
LIMIT = 65536
REQUIRED = {'schema', 'switches', 'threads', 'arities', 'join_order', 'corpus'}


def build(profile: dict, size: int, materials: dict):
    if type(profile) is not dict or set(profile) != REQUIRED or profile['schema'] != SCHEMA:
        raise ValueError('unknown, missing or unsupported transport profile fields')
    if type(size) is not int or not 0 <= size <= LIMIT * 8:
        raise ValueError('transport resource limit: at most 64 KiB per message')
    if type(profile['switches']) is not dict:
        raise TypeError('switches must be an object')
    switches = Switches(profile['switches'])
    if any(switches[s] for s in ('key', 'gonol', 'bind', 'auth')):
        raise Blocked('transport profile cannot supply key/gonol/bind/auth native laws')
    count = profile['threads']
    if type(count) is not int or not 3 <= count <= 63:
        raise ValueError('transport resource profile admits 3..63 threads')
    params = {}
    if switches['split']:
        owners = cyclic_route(size, count)
        params['split'] = (count, owners)
        lengths = tuple(owners.count(i) for i in range(count))
    else:
        lengths = (size,)
    if switches['corpus']:
        choices = profile['corpus']
        if type(choices) is not list or len(choices) != len(lengths):
            raise ValueError('choose actual material/offset for each active lane')
        clean = []
        for choice in choices:
            if (type(choice) is not list or len(choice) != 2 or type(choice[0]) is not str
                    or type(choice[1]) is not int or choice[1] < 0):
                raise ValueError('invalid corpus choice')
            if choice[0] not in materials or type(materials[choice[0]]) is not bytes or not materials[choice[0]]:
                raise Blocked('missing nonempty corpus material')
            clean.append(tuple(choice))
        params['corpus'] = tuple(clean)
        used_material = {label: materials[label] for label, offset in clean}
    else:
        used_material = {}
    if switches['inter']:
        arities = profile['arities']
        if type(arities) is not list or len(arities) != len(lengths):
            raise ValueError('one arity schedule per active lane required')
        for schedule in arities:
            if (type(schedule) is not list or not 1 <= len(schedule) <= 64
                    or any(type(a) is not int or not 3 <= a <= 4096 for a in schedule)):
                raise ValueError('resource profile: 1..64 stages with arities 3..4096')
        params['inter'] = tuple(balanced_schedule(n, tuple(a)) for n, a in zip(lengths, arities))
    if switches['join']:
        order = profile['join_order']
        if (type(order) is not list or any(type(i) is not int for i in order)
                or sorted(order) != list(range(len(lengths)))):
            raise ValueError('join_order must visit all active lanes')
        params['join'] = (lengths, tuple(order))
    elif switches['whole'] and len(lengths) != 1:
        raise ValueError('incompatible ablation: whole needs one lane; join is OFF')
    pipeline = Pipeline(switches, {
        'split': explicit_route_operator(),
        'corpus': content_route_operator(),
        'join': explicit_join_operator(),
    })
    public = PublicContext(None, params, public_material=used_material)
    private = PrivateContext(None, None, params, public_material=used_material)
    return pipeline, public, private


def byte_stream(data: bytes) -> Streams:
    if type(data) is not bytes or len(data) > LIMIT:
        raise ValueError('transport input must be bytes of at most 64 KiB')
    return Streams((tuple((byte >> shift) & 1 for byte in data for shift in range(7, -1, -1)),))


def recover_bytes(streams: Streams) -> bytes:
    if not isinstance(streams, Streams) or len(streams.lanes) != 1 or len(streams.lanes[0]) % 8:
        raise ValueError('recovered input is not one byte-aligned stream')
    bits = streams.lanes[0]
    return bytes(sum(bits[i + j] << (7-j) for j in range(8)) for i in range(0, len(bits), 8))
