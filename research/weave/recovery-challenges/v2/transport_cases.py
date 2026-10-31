# ratios: loc_comments=86:28 imports_exports=3:5 calls_definitions=57:5
"""Typed historical transport experiments; none supplies native private binding.

X splits; J joins; C is the prior assistant-proposed corpus end route; I is the
balanced section candidate; W is the specified whole-stream last/first operation.
WLN1 is transparent lane serialization (count, bit lengths, MSB-first payloads).
Join-first fixtures begin with three contiguous input lanes, declared in parameters.
No implicit join or padding is used to make an invalid schedule pass.
"""
# === MODULE_BUILD ===
# id: challenge_transport
#   module_name: transport_cases
#   module_kind: adapter
#   summary: expose typed historical candidates as distinct layer experiments
#   owner: Erin Spencer
#   public_surface: run, contexts, encode_lanes, decode_lanes
#   internal_surface: shape replay independent of message bits
#   tests: test_harness.py
#   rollout: historical scope only
#   rollback: remove v2
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: read
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: typed_transport
#   given: a typed transport schedule
#   then: replay lane shapes from wire length and parameters or refuse an invalid order
# === END CONTRACTS ===
import operations as o
from stages import split, join, corpus, inter, whole
from stages.api import Streams, PublicContext

MODULES = {'X': split, 'J': join, 'C': corpus, 'I': inter, 'W': whole}


def encode_lanes(streams):
    out = bytearray(b'WLN1' + len(streams.lanes).to_bytes(2, 'big'))
    for lane in streams.lanes:
        out.extend(len(lane).to_bytes(4, 'big'))
        out.extend(o.packed(lane + (0,)*((-len(lane)) % 8)))
    return bytes(out)


def decode_lanes(data):
    if data[:4] != b'WLN1' or len(data) < 6:
        raise ValueError('lane frame required')
    count, pos, lanes = int.from_bytes(data[4:6], 'big'), 6, []
    if not 1 <= count <= 7:
        raise ValueError('invalid lane count')
    for _ in range(count):
        if pos+4 > len(data):
            raise ValueError('truncated lane length')
        size = int.from_bytes(data[pos:pos+4], 'big'); pos += 4
        width = (size+7)//8
        if pos+width > len(data):
            raise ValueError('truncated lane')
        raw = o.bits(data[pos:pos+width]); pos += width
        if any(raw[size:]):
            raise ValueError('nonzero serialization padding')
        lanes.append(raw[:size])
    if pos != len(data):
        raise ValueError('trailing lane bytes')
    return Streams(tuple(lanes))


def initial_lengths(size, count):
    q, r = divmod(size, count)
    return tuple(q+(i<r) for i in range(count))


def contexts(size, schedule, p):
    lengths = initial_lengths(size, p['initial_lanes'])
    result = []
    for op in schedule:
        params = {}
        if op == 'X':
            if len(lengths) != 1:
                raise ValueError('split requires one lane')
            count = p['thread_count']
            owners = split.cyclic_route(size, count)
            params['split'] = (count, owners)
            lengths = tuple(owners.count(i) for i in range(count))
        elif op == 'J':
            if len(lengths) < 3:
                raise ValueError('join experiment requires at least three lanes')
            r = p['lane_rotation'] % len(lengths)
            order = tuple(range(r, len(lengths))) + tuple(range(r))
            params['join'] = (lengths, order)
            lengths = (sum(lengths),)
        elif op == 'C':
            params['corpus'] = tuple(('material', p['corpus_bit_offset']+i) for i in range(len(lengths)))
        elif op == 'I':
            params['inter'] = tuple(inter.balanced_schedule(n, (p['inter_arity'],)) for n in lengths)
        elif op == 'W':
            if len(lengths) != 1:
                raise ValueError('whole requires an explicit preceding join')
        else:
            raise ValueError('unknown transport operation')
        result.append(PublicContext(None, parameters=params,
                      public_material={'material': bytes.fromhex(p['corpus_hex'])}))
    return result, lengths


def run(data, schedule, parameters, inverse=False):
    if not schedule or any(schedule.count(op)>3 for op in set(schedule)):
        raise ValueError('per-operation repetition cap')
    if inverse:
        state = decode_lanes(data)
        size = sum(map(len, state.lanes))
    else:
        raw = o.bits(data); size = len(raw); start = 0; lanes = []
        for n in initial_lengths(size, parameters['initial_lanes']):
            lanes.append(raw[start:start+n]); start += n
        state = Streams(tuple(lanes))
    plans, final_lengths = contexts(size, schedule, parameters)
    if inverse and tuple(map(len, state.lanes)) != final_lengths:
        raise ValueError('final lane shape differs from independently replayed schedule')
    work = list(zip(schedule, plans))
    for op, context in reversed(work) if inverse else work:
        state = (MODULES[op].inverse if inverse else MODULES[op].forward)(state, context)
    if inverse:
        if tuple(map(len, state.lanes)) != initial_lengths(size, parameters['initial_lanes']):
            raise ValueError('initial lane shape mismatch')
        return o.packed(tuple(b for lane in state.lanes for b in lane))
    return encode_lanes(state)
# ratios: loc_comments=86:28 imports_exports=3:5 calls_definitions=57:5
