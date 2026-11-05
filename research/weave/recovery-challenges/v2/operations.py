# ratios: loc_comments=119:35 imports_exports=13:10 calls_definitions=71:10
"""Pinned-source byte adapters; CLI receives no plaintext or encoder trace.

Run: python operations.py receive --request request.json --output restored.bin
Requests contain wire_hex, schedule, parameters, family; all are receiver inputs.
WRA1 adds only the native origin root required by standalone affixiation. U is a
literal packet, not a new encryption claim. R is exact three-byte-record reversal.
"""
# === MODULE_BUILD ===
# id: challenge_operations
#   module_name: operations
#   module_kind: adapter
#   summary: execute exact existing operations and explicit serialization adapters
#   owner: Erin Spencer
#   public_surface: transform, receive, verify_sources
#   internal_surface: profile conversion and native loader
#   tests: test_harness.py
#   rollout: research challenge v2 only
#   rollback: remove v2
#   auth_boundary: none
#   storage_boundary: read
#   network_boundary: none
#   user_data_boundary: read
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: receiver_inputs_only
#   given: ciphertext, selected parameters and pinned source
#   then: reverse without original bytes or encoder trace
# id: exact_operations
#   given: an admitted schedule
#   then: preserve actual operations, order, repetition and source identity
# === END CONTRACTS ===
from pathlib import Path
from hashlib import sha1
from fractions import Fraction
import argparse
import json
import sys

HERE = Path(__file__).resolve().parent
WEAVE = HERE.parents[1]
CHECKOUT = WEAVE.parents[1]
SOURCES = CHECKOUT / 'sources'


def verify_sources():
    """Refuse any byte drift before importing the experimental algorithms."""
    lock = json.loads((HERE / 'SOURCE.json').read_text())
    for row in lock['files']:
        data = (CHECKOUT / row['path']).read_bytes()
        actual = sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if actual != row['git_blob']:
            raise ValueError('source identity mismatch: ' + row['path'])
    return len(lock['files'])


verify_sources()
sys.path.insert(0, str(WEAVE))
sys.path.insert(0, str(HERE))
import cycle
import numeral
import prime_schedule as prime
from cycle_native import load_native
from stages.api import Streams
from stages import whole

_NATIVE = None
BIT_REVERSE = bytes(int(f'{i:08b}'[::-1], 2) for i in range(256))


def native():
    """One checked native instance per process; no wire-owned executable objects."""
    global _NATIVE
    if _NATIVE is None:
        _NATIVE = load_native(SOURCES)
    return _NATIVE


def spec(row):
    return cycle.RoundSpec(numeral.PrimePath(row['prime_path']['seed'],
        tuple(tuple(s) for s in row['prime_path']['steps'])), tuple(row['arities']),
        tuple(row['circle_order']), tuple(Fraction(*x) for x in row['spaces']),
        row['end_order'])


def profile(parameters, rounds=None):
    selected = parameters.get('rounds', [parameters['spec']]) if rounds is None else rounds
    return cycle.Profile(parameters['scope'], parameters['bucket_bytes'],
        parameters['corpus_bit_offset'], tuple(spec(s) for s in selected))


def bits(data):
    return tuple((b >> shift) & 1 for b in data for shift in range(7, -1, -1))


def packed(values):
    if len(values) % 8:
        raise ValueError('byte alignment required')
    return bytes(sum(values[i + k] << (7-k) for k in range(8))
                 for i in range(0, len(values), 8))


def transform(data, name, parameters, inverse=False):
    """No automatic padding, joining, substitution or invented secret relation."""
    if type(data) is not bytes or not data:
        raise ValueError('nonempty bytes required')
    if len(data) > cycle.CycleLimits().round_bytes:
        raise numeral.ResourceLimit('adapter input exceeds unchanged round budget')
    if name == 'N':
        material = bytes.fromhex(parameters['corpus_hex'])
        return (cycle.denormalize if inverse else cycle.normalize)(data, material, profile(parameters))
    if name == 'A':
        api, geometry = native()
        if inverse:
            if data[:4] != b'WRA1' or len(data) < 37:
                raise ValueError('standalone native-root envelope required')
            root, wire = data[4:36].hex(), data[36:]
            return cycle.unaffix(wire, api=api, geometry=geometry,
                scope=parameters['scope'], root=root, round_id=0, spec=spec(parameters['spec']))
        root = api.ByteOrigin(data, parameters['scope'], 0, geometry).message_origin
        wire, _ = cycle.affix(data, api=api, geometry=geometry,
            scope=parameters['scope'], root=root, round_id=0, spec=spec(parameters['spec']))
        return b'WRA1' + bytes.fromhex(root) + wire
    if name == 'U':
        if inverse:
            return numeral.decode(data).restore().to_bytes()
        entry = numeral.Entry('\ue000', numeral.BitBlock.from_bytes(data), Fraction(0), 1)
        return numeral.encode(numeral.Packet(parameters['scope'], 0, (entry,), entry.symbol))
    if name == 'S':
        selected = spec(parameters['spec'])
        split = prime.plan(len(data)*8, prime.Route.evaluate(selected.path), selected.arities)
        return prime.interleave(data, split, inverse=inverse, end_order=selected.end_order)
    if name == 'W':
        streams = Streams((bits(data),))
        result = (whole.inverse if inverse else whole.forward)(streams, None)
        return packed(result.lanes[0])
    if name == 'B':
        return data.translate(BIT_REVERSE)
    if name == 'R':
        if len(data) % 3:
            raise ValueError('R: exact three-byte records required; no implicit padding')
        return b''.join(data[i:i+3][::-1] for i in range(0, len(data), 3))
    raise ValueError('unknown operation: ' + str(name))


def execute(data, schedule, parameters, inverse=False):
    """Enforce the user's per-operation cap, including repeated mixed schedules."""
    if not schedule or any(schedule.count(op) > 3 for op in set(schedule)):
        raise ValueError('each operation may appear at most three times')
    for op in reversed(schedule) if inverse else schedule:
        data = transform(data, op, parameters, inverse)
    return data


def receive(request):
    """Reverse only; family selection is supplied receiver material, not plaintext."""
    data = bytes.fromhex(request['wire_hex'])
    if request['family'] == 'cycle':
        p = request['parameters']
        return cycle.reverse(data, bytes.fromhex(p['corpus_hex']), profile(p), SOURCES)
    if request['family'] == 'transport':
        from transport_cases import run
        return run(data, request['schedule'], request['parameters'], inverse=True)
    return execute(data, request['schedule'], request['parameters'], inverse=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['receive'])
    parser.add_argument('--request', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    request = json.loads(args.request.read_text())
    if set(request) != {'wire_hex', 'schedule', 'parameters', 'family'}:
        raise ValueError('receiver request contains unadmitted fields')
    result = receive(request)
    with args.output.open('xb') as out:
        out.write(result)


if __name__ == '__main__':
    main()
# ratios: loc_comments=119:35 imports_exports=13:10 calls_definitions=71:10
