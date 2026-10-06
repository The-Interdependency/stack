# ratios: loc_comments=271:50 imports_exports=16:7 calls_definitions=157:19
# === MODULE_BUILD ===
# id: weave_native_shift_polynomial
#   module_name: private_public
#   module_kind: experiment
#   summary: proposed public polynomial evaluation and native-private exact-root recovery after the unchanged Weave cycle
#   owner: Erin Spencer
#   public_surface: keygen, send, recover, public_recover, decompose, experiment
#   internal_surface: exact scalar binding, serialized artifacts and fresh-process witness
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   tests: tests/test_private_public.py
#   rollout: research CLI only; public recovery falsifies this candidate
#   rollback: remove candidate and its tests, evidence and links
#   unresolved: surviving asymmetry, confidentiality, authentication and replay
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: native_private_key_relation
#   given: private source material and the exact native geometry
#   then: eight complete native states determine two public displacements and six privately factored operations
# id: public_sender_evaluation
#   given: public artifact and message only
#   then: evaluate the published polynomial on the complete real Weave cycle record without recipient-private input
# id: native_private_exact_recovery
#   given: matching private material, public artifact and packet
#   then: native-derived inverse operations recover the exact cycle record and original bytes
# id: public_inverse_falsification
#   given: published coefficients and packet only
#   then: test coefficient decomposition and report exact public recovery as candidate falsification
# id: candidate_artifact_admission
#   given: malformed, oversized or mismatched data
#   then: reject without inventing keys, accepting approximate roots or returning partial plaintext
# id: candidate_process_boundary
#   given: a research experiment
#   then: sender, private receiver and public attack run in fresh processes with only their declared inputs
# === END CONTRACTS ===
"""Usage: python private_public.py --sources /checkouts [--require-distinction].

PRIVATE_PUBLIC.md defines the proposed law, geometry boundary and algebraic attack.
This is a candidate construction, not a security implementation. The old input-
partition-only experiment is replaced, not advertised as completing this work.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
from math import comb, isqrt
from pathlib import Path
import os
import re
import secrets
import subprocess
import sys
import tempfile

import cycle
from cycle import Profile, CycleLimits, canonical, strict_json
from cycle_native import load_native
from numeral import Refused, _Reader, _uint, _blob

ROOT = Path(__file__).resolve().parent
LAW = 'weave.native-shift-polynomial/v1'
MAGIC = b'WPP\x01'
LIMITS = CycleLimits(input_bytes=256, round_bytes=16384, rounds=3)
MAX_RECORD = LIMITS.round_bytes + 128
MAX_BOUND_BITS = 64 * (8 * MAX_RECORD + 16) + 16
MAX_WIRE = MAX_BOUND_BITS // 8 + 256
RUNTIME = ('private_public.py', 'cycle.py', 'cycle_native.py', 'native_binary.py',
           'numeral.py', 'affixiation.py', 'prime_schedule.py', 'safe_output.py', 'CYCLE_NATIVE.json')


def _object(data, fields):
    if type(data) is not bytes or len(data) > 65536:
        raise Refused('bounded serialized artifact required')
    obj = strict_json(data)
    if type(obj) is not dict or set(obj) != set(fields) or canonical(obj) != data:
        raise Refused('exact canonical artifact schema required')
    return obj


def _hex(value, maximum):
    if (type(value) is not str or len(value) > maximum * 2
            or re.fullmatch(r'(?:[0-9a-f]{2})*', value) is None):
        raise Refused('bounded canonical hexadecimal required')
    return bytes.fromhex(value)


def _native(material, sources):
    if type(material) is not bytes or len(material) != 256:
        raise Refused('exactly 256 private material bytes required')
    api, geometry = load_native(sources)
    origin = api.ByteOrigin(material, LAW + '/key-origin', 0, geometry)
    turns = []
    for i in range(8):
        axis = origin.byte_axis(material[i])
        state = api.Geometry.placed(geometry, axis, Fraction(-(material[8+i] & 1)))
        turns.append(api.Geometry.lift(geometry, state))
    return origin.identity, tuple(turns)


def _offsets(turns):
    return tuple(1 + int(t * 256) for t in turns)


def _expand(shifts):
    coefficients = [0, 1]
    for shift in shifts:
        coefficients[0] += shift
        squared = [0] * (2 * len(coefficients) - 1)
        for i, a in enumerate(coefficients):
            for j, b in enumerate(coefficients):
                squared[i+j] += a*b
        coefficients = squared
    return coefficients


def _evaluate(coefficients, x):
    value = 0
    for coefficient in reversed(coefficients):
        value = value*x + coefficient
    return value


def _public(data):
    obj = _object(data, ('law', 'key_origin', 'public_turns', 'coefficients', 'profile',
                         'corpus_hex', 'native_lock_sha256'))
    if obj['law'] != LAW or obj['native_lock_sha256'] != sha256((ROOT/'CYCLE_NATIVE.json').read_bytes()).hexdigest():
        raise Refused('law or native source identity mismatch')
    if len(_hex(obj['key_origin'], 32)) != 32:
        raise Refused('key origin identity required')
    rows = obj['public_turns']
    if type(rows) is not list or len(rows) != 2:
        raise Refused('exactly whole-plus-one native complete turns required')
    turns = []
    for row in rows:
        if (type(row) is not list or len(row) != 2 or any(type(v) is not int for v in row)
                or not 1 <= row[1] <= 256 or not 0 <= row[0] < 2*row[1]):
            raise Refused('invalid complete turn')
        t = Fraction(*row)
        if [t.numerator, t.denominator] != row or (t*256).denominator != 1:
            raise Refused('turn must be a canonical native key-axis position')
        turns.append(t)
    c = obj['coefficients']
    if (type(c) is not list or len(c) != 65 or c[-1] != 1
            or any(type(v) is not int or v < 0 or v.bit_length() > 4096 for v in c)):
        raise Refused('bounded exact monic degree-64 public polynomial required')
    profile = Profile.read(canonical(obj['profile']), LIMITS)
    corpus = _hex(obj['corpus_hex'], 4096)
    if not corpus:
        raise Refused('actual nonempty public corpus required')
    return obj, profile, corpus, _offsets(turns)


def keygen(profile: Profile, corpus: bytes, sources: str | Path, *, material: bytes | None = None):
    """Construct this candidate's native private configuration and public law."""
    if material is None:
        material = secrets.token_bytes(256)
    origin, turns = _native(material, sources)
    if type(corpus) is not bytes:
        raise Refused('actual corpus bytes required')
    public = canonical({'law': LAW, 'key_origin': origin,
                        'public_turns': [[t.numerator, t.denominator] for t in turns[:2]],
                        'coefficients': _expand(_offsets(turns)[2:]),
                        'profile': Profile.as_dict(profile), 'corpus_hex': corpus.hex(),
                        'native_lock_sha256': sha256((ROOT/'CYCLE_NATIVE.json').read_bytes()).hexdigest()})
    _public(public)
    private = canonical({'law': LAW, 'material_hex': material.hex()})
    return public, private


def send(message: bytes, public: bytes, sources: str | Path) -> bytes:
    """Evaluate the expanded public law; no private material or keygen call."""
    obj, profile, corpus, (whole, one) = _public(public)
    record = cycle.forward(message, corpus, profile, sources, LIMITS)[0]
    x = int.from_bytes(record, 'big')
    y = _evaluate(obj['coefficients'], x + whole) + one
    if y.bit_length() > MAX_BOUND_BITS:
        raise Refused('public evaluation exceeds bound integer budget')
    encoded = y.to_bytes((y.bit_length()+7)//8, 'big')
    return MAGIC + sha256(public).digest() + _uint(len(record)) + _blob(encoded)


def _packet(packet, public):
    if type(packet) is not bytes or len(packet) > MAX_WIRE:
        raise Refused('bounded packet bytes required')
    reader = _Reader(packet)
    if reader.take(4) != MAGIC or reader.take(32) != sha256(public).digest():
        raise Refused('packet law/key identity mismatch')
    length = reader.uint()
    if not 1 <= length <= MAX_RECORD:
        raise Refused('cycle record length outside budget')
    encoded = reader.blob(MAX_WIRE)
    if reader.pos != len(packet) or not encoded or encoded[0] == 0:
        raise Refused('noncanonical or trailing bound integer')
    y = int.from_bytes(encoded, 'big')
    if y.bit_length() > MAX_BOUND_BITS:
        raise Refused('bound integer exceeds bit budget')
    return length, y


def _invert(y, shifts):
    for shift in reversed(shifts):
        if y < 0:
            raise Refused('negative inverse state')
        root = isqrt(y)
        if root*root != y:
            raise Refused('non-exact square in private relation')
        y = root - shift
    return y


def _restore(packet, public, shifts, sources):
    _, profile, corpus, (whole, one) = _public(public)
    length, y = _packet(packet, public)
    x = _invert(y-one, shifts) - whole
    if x < 0 or x.bit_length() > length*8:
        raise Refused('inverse does not fit declared record length')
    return cycle.reverse(x.to_bytes(length, 'big'), corpus, profile, sources, LIMITS)


def recover(packet: bytes, public: bytes, private: bytes, sources: str | Path) -> bytes:
    """Use actual private native states for exact square-root recovery."""
    _, profile, corpus, _ = _public(public)
    secret = _object(private, ('law', 'material_hex'))
    if secret['law'] != LAW:
        raise Refused('private law mismatch')
    material = _hex(secret['material_hex'], 256)
    rebuilt, _ = keygen(profile, corpus, sources, material=material)
    if rebuilt != public:
        raise Refused('private material belongs to a different key')
    _, turns = _native(material, sources)
    return _restore(packet, public, _offsets(turns)[2:], sources)


def decompose(coefficients):
    """Public algebraic attack: peel inner native displacements from coefficients."""
    if (type(coefficients) not in (list, tuple) or len(coefficients) != 65
            or any(type(v) is not int or v < 0 or v.bit_length() > 4096 for v in coefficients)):
        raise Refused('bounded exact degree-64 coefficient list required')
    p = list(coefficients)
    shifts = []
    for _ in range(6):
        degree = len(p)-1
        if degree < 2 or p[-1] != 1 or p[-2] % degree:
            raise Refused('polynomial does not admit the candidate decomposition')
        shift = p[-2] // degree
        if not 1 <= shift <= 512:
            raise Refused('recovered displacement outside native candidate domain')
        # F(z-shift) = H(z^2). Exact cancellation, no numeric root estimates.
        translated = [sum(p[j]*comb(j,i)*(-shift)**(j-i) for j in range(i,degree+1))
                      for i in range(degree+1)]
        if any(translated[1::2]):
            raise Refused('public polynomial has nonzero odd residuals')
        p = translated[::2]
        shifts.append(shift)
    if p != [0, 1]:
        raise Refused('public decomposition did not end at identity')
    return tuple(shifts)


def public_recover(packet: bytes, public: bytes, sources: str | Path) -> bytes:
    """Recover via public coefficients alone; never consume the private artifact."""
    obj, _, _, _ = _public(public)
    return _restore(packet, public, decompose(obj['coefficients']), sources)


def _worker():
    request = strict_json(sys.stdin.buffer.read(2*MAX_WIRE+262145))
    if type(request) is not dict or request.get('operation') not in ('send', 'recover', 'public-recover'):
        raise Refused('unknown worker operation')
    operation = request['operation']
    fields = {'operation', 'public', 'data'} | ({'private'} if operation == 'recover' else set())
    if set(request) != fields:
        raise Refused('worker input manifest mismatch')
    public = _hex(request['public'], 65536)
    data = _hex(request['data'], MAX_WIRE)
    if operation == 'send':
        result = send(data, public, ROOT/'inputs')
    elif operation == 'public-recover':
        result = public_recover(data, public, ROOT/'inputs')
    else:
        result = recover(data, public, _hex(request['private'], 65536), ROOT/'inputs')
    return {'data': result.hex()}


def _run(root, operation, public, data, private=None):
    request = {'operation': operation, 'public': public.hex(), 'data': data.hex()}
    if private is not None:
        request['private'] = private.hex()
    result = subprocess.run([sys.executable, '-S', '-B', '-E', str(root/'private_public.py'), '--worker'],
                            input=canonical(request), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            cwd=root, env={})
    if result.returncode:
        raise RuntimeError(f'{operation} worker failed: {result.stderr.decode(errors="replace")}')
    response = strict_json(result.stdout)
    if type(response) is not dict or set(response) != {'data'}:
        raise RuntimeError('invalid worker response')
    return _hex(response['data'], MAX_WIRE)


def experiment(message, profile, corpus, sources, *, material=None):
    """Execute the actual candidate and its public inverse attack, with scoped evidence."""
    public, private = keygen(profile, corpus, sources, material=material)
    with tempfile.TemporaryDirectory(prefix='weave-native-key-') as directory:
        root = Path(directory)
        for name in RUNTIME:
            (root/name).write_bytes((ROOT/name).read_bytes())
        lock = strict_json((ROOT/'CYCLE_NATIVE.json').read_bytes())
        for name in lock['ucns_sources']:
            target = root/'inputs'/'ucns'/name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((Path(sources)/'ucns'/name).read_bytes())
        files = lambda: {str(p.relative_to(root)): sha256(p.read_bytes()).hexdigest()
                         for p in sorted(root.rglob('*')) if p.is_file()}
        source_files = files()
        packet = _run(root, 'send', public, message)
        restored = _run(root, 'recover', public, packet, private)
        attacked = _run(root, 'public-recover', public, packet)
        if files() != source_files:
            raise RuntimeError('worker bundle changed during execution')
    if restored != message:
        raise RuntimeError('candidate private recovery failed')
    exact = attacked == message
    return {'schema': 'weave.private-public-experiment/v2', 'law': LAW,
            'status': 'FALSIFIED' if exact else 'UNRESOLVED', 'distinction_established': False,
            'public_sender_completed': True, 'private_recovery_exact': True,
            'public_recovery_exact': exact, 'attack': 'exact public coefficient decomposition',
            'private_material_given_to_attacker': False, 'equivalent_inverse_recovered': exact,
            'inputs': {'sender': ['message', 'public'], 'recipient': ['packet', 'public', 'private'],
                       'attacker': ['packet', 'public'], 'shared': ['exact code', 'locked native sources']},
            'accounting': {'message_bytes': len(message), 'packet_bytes': len(packet),
                           'public_bytes': len(public), 'private_bytes': len(private),
                           'inner_cycle_bytes': _packet(packet, public)[0]},
            'source_files': source_files, 'source_sha256': sha256(canonical(source_files)).hexdigest(),
            'public_sha256': sha256(public).hexdigest(), 'packet_sha256': sha256(packet).hexdigest(),
            'native_lock_sha256': sha256((ROOT/'CYCLE_NATIVE.json').read_bytes()).hexdigest(),
            'scope': 'This candidate only; no verdict on all native private/public relations.',
            'hmmm': 'A surviving asymmetric relation and cryptographic security remain unestablished.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', type=Path, default=Path(os.environ.get('WEAVE_SOURCES', ROOT/'sources')))
    parser.add_argument('--require-distinction', action='store_true')
    parser.add_argument('--worker', action='store_true', help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        if args.worker:
            result = _worker()
        else:
            profile = Profile.read((ROOT/'profiles'/'cycle-v1.json').read_bytes(), LIMITS)
            result = experiment(b'ABxABy\x00ABxABy\xff', profile, bytes(range(256)), args.sources,
                                material=bytes((i*73+41)%256 for i in range(256)))
        print(canonical(result).decode())
        return 1 if args.require_distinction and not result.get('distinction_established', False) else 0
    except (Refused, OSError, RuntimeError) as exc:
        print(f'private/public experiment error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
# ratios: loc_comments=271:50 imports_exports=16:7 calls_definitions=157:19
