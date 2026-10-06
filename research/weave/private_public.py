# ratios: loc_comments=229:55 imports_exports=14:8 calls_definitions=121:16
# === MODULE_BUILD ===
# id: weave_private_public_boundary_experiment
#   module_name: private_public
#   module_kind: experiment
#   summary: falsifiable public/private input boundary on the unchanged native sequence cycle
#   owner: Erin Spencer
#   public_surface: partition, send, recover, public_recover, full_profile_control, experiment
#   internal_surface: strict serialized artifacts and fresh-process evidence
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   tests: tests/test_private_public.py
#   rollout: explicit experiment; BLOCKED is not asymmetric success
#   rollback: remove experiment and its tests, docs and CI invocation
#   unresolved: native private-gonol generation and public evaluation law
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: weave_public_artifact_boundary
#   given: a full cycle profile and actual corpus
#   then: whole-plus-one public export carries exactly two spaces per round and no private reference
# id: weave_sender_no_private_fallback
#   given: only the whole-plus-one projection
#   then: refuse the undefined public operation before cycle execution rather than guessing hidden spaces
# id: weave_private_reconstruction_inputs
#   given: a packet and the matching public and private reconstruction artifacts
#   then: recover exactly using only those inputs and locked source code
# id: weave_public_recovery_falsifier
#   given: full-profile public control and its packet
#   then: execute public-only recovery and report exact recovery as a counterexample to private necessity
# id: weave_process_evidence_boundary
#   given: an experiment run
#   then: isolate sender and recovery invocations in fresh processes with explicit input and source manifests
# id: weave_distinction_gate
#   given: a blocked public sender or an exact public recovery counterexample
#   then: the requested distinction remains unaccepted and its acceptance command exits nonzero
# === END CONTRACTS ===
"""Usage: python private_public.py --sources /checkouts [--require-distinction].

PRIVATE_PUBLIC.md freezes scope and acceptance criteria. This is an executable
boundary experiment, not a key generator. A private-argument check cannot prove
private-state necessity. The full-profile control deliberately tests that mistake.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import os
import re
import subprocess
import sys
import tempfile

import cycle
from cycle import Profile, CycleLimits, canonical, strict_json
from cycle_native import load_native
from numeral import Refused

ROOT = Path(__file__).resolve().parent
PUBLIC_SCHEMA = 'weave.public-cycle-input/v1'
PRIVATE_SCHEMA = 'weave.private-cycle-input/v1'
PROJECTION = 'whole-plus-one'
CONTROL = 'full-profile-control'
LIMITS = CycleLimits(input_bytes=256, round_bytes=131072, rounds=3)
ARTIFACT_BYTES = 32768
RUNTIME = ('private_public.py', 'cycle.py', 'cycle_native.py', 'native_binary.py',
           'numeral.py', 'affixiation.py', 'prime_schedule.py', 'safe_output.py',
           'CYCLE_NATIVE.json')


class MissingPublicRelation(Refused):
    """Q7 is blocked by a missing native operation, not a proven secret."""


def _object(data, fields):
    if type(data) is not bytes or len(data) > ARTIFACT_BYTES:
        raise Refused('bounded serialized artifact bytes required')
    obj = strict_json(data)
    if type(obj) is not dict or set(obj) != set(fields):
        raise Refused('artifact fields do not match schema')
    return obj


def _hex(value, maximum):
    if (type(value) is not str or len(value) > maximum * 2
            or re.fullmatch(r'(?:[0-9a-f]{2})*', value) is None):
        raise Refused('bounded canonical hexadecimal required')
    return bytes.fromhex(value)


def _projection(profile, circle):
    obj = Profile.as_dict(profile)
    for row in obj['rounds']:
        row['spaces'] = [value if i in (0, circle) else None
                         for i, value in enumerate(row['spaces'])]
    return obj


def _public(data):
    obj = _object(data, ('schema', 'disclosure', 'circle', 'profile',
                         'corpus_hex', 'native_lock_sha256'))
    if (obj['schema'] != PUBLIC_SCHEMA or type(obj['disclosure']) is not str
            or obj['disclosure'] not in (PROJECTION, CONTROL)
            or type(obj['circle']) is not int or not 1 <= obj['circle'] <= 7):
        raise Refused('unsupported public artifact')
    if obj['native_lock_sha256'] != sha256((ROOT/'CYCLE_NATIVE.json').read_bytes()).hexdigest():
        raise Refused('native lock identity mismatch')
    corpus = _hex(obj['corpus_hex'], 4096)
    if not corpus:
        raise Refused('actual nonempty public corpus required')
    profile = deepcopy(obj['profile'])
    if type(profile) is not dict or type(profile.get('rounds')) is not list:
        raise Refused('profile round list required')
    for row in profile['rounds']:
        if (type(row) is not dict or type(row.get('spaces')) is not list
                or len(row['spaces']) != 8):
            raise Refused('eight space positions required')
        for i, value in enumerate(row['spaces']):
            hidden = obj['disclosure'] == PROJECTION and i not in (0, obj['circle'])
            if hidden:
                if value is not None:
                    raise Refused('private space leaked into public projection')
                # Syntax validation only. Never return this placeholder profile.
                row['spaces'][i] = [0, 1]
            elif value is None:
                raise Refused('required public space absent')
    Profile.read(canonical(profile), LIMITS)
    return obj, corpus


def _complete(public):
    obj, corpus = _public(public)
    if obj['disclosure'] != CONTROL:
        try:
            Profile.read(canonical(obj['profile']), LIMITS)
        except Refused as exc:
            raise MissingPublicRelation('six spaces per round are private; native public evaluation law missing') from exc
        raise RuntimeError('cycle now admits partial profiles; reassess the experiment')
    return Profile.read(canonical(obj['profile']), LIMITS), corpus


def partition(profile: Profile, corpus: bytes, *, circle: int = 1) -> tuple[bytes, bytes]:
    """Export reconstruction inputs; no entropy, private gonol or trapdoor invented."""
    if type(corpus) is not bytes:
        raise Refused('actual corpus bytes required')
    obj = {'schema': PUBLIC_SCHEMA, 'disclosure': PROJECTION, 'circle': circle,
           'profile': _projection(profile, circle), 'corpus_hex': corpus.hex(),
           'native_lock_sha256': sha256((ROOT/'CYCLE_NATIVE.json').read_bytes()).hexdigest()}
    public = canonical(obj)
    _public(public)
    private = canonical({'schema': PRIVATE_SCHEMA, 'public_sha256': sha256(public).hexdigest(),
                         'profile': Profile.as_dict(profile)})
    _private(public, private)
    return public, private


def _private(public, private):
    pub, corpus = _public(public)
    obj = _object(private, ('schema', 'public_sha256', 'profile'))
    if obj['schema'] != PRIVATE_SCHEMA or obj['public_sha256'] != sha256(public).hexdigest():
        raise Refused('private artifact does not bind these exact public bytes')
    profile = Profile.read(canonical(obj['profile']), LIMITS)
    projected = (_projection(profile, pub['circle']) if pub['disclosure'] == PROJECTION
                 else Profile.as_dict(profile))
    if canonical(projected) != canonical(pub['profile']):
        raise Refused('private profile disagrees with public projection')
    return profile, corpus


def full_profile_control(public: bytes, private: bytes) -> bytes:
    """Publish all reconstruction fields explicitly as a negative control."""
    profile, _ = _private(public, private)
    obj, _ = _public(public)
    obj['profile'] = Profile.as_dict(profile)
    obj['disclosure'] = CONTROL
    result = canonical(obj)
    _public(result)
    return result


def send(message: bytes, public: bytes, sources: str | Path) -> bytes:
    """Public inputs only. A missing native law blocks before any forward work."""
    profile, corpus = _complete(public)
    return cycle.forward(message, corpus, profile, sources, LIMITS)[0]


def recover(packet: bytes, public: bytes, private: bytes, sources: str | Path) -> bytes:
    """Private-path exact recovery; accepting a private argument is not asymmetry."""
    profile, corpus = _private(public, private)
    return cycle.reverse(packet, corpus, profile, sources, LIMITS)


def public_recover(packet: bytes, public: bytes, sources: str | Path) -> bytes:
    """Actual public inverse attack, not a call to the private-path wrapper."""
    profile, corpus = _complete(public)
    return cycle.reverse(packet, corpus, profile, sources, LIMITS)


def _worker():
    request = strict_json(sys.stdin.buffer.read(1048577))
    if type(request) is not dict or request.get('operation') not in ('send', 'recover', 'public-recover'):
        raise Refused('unknown worker operation')
    operation = request['operation']
    fields = {'operation', 'public', 'data'} | ({'private'} if operation == 'recover' else set())
    if set(request) != fields:
        raise Refused('worker input manifest mismatch')
    public = _hex(request['public'], ARTIFACT_BYTES)
    data = _hex(request['data'], LIMITS.round_bytes + 128)
    try:
        if operation == 'send':
            result = send(data, public, ROOT/'inputs')
        elif operation == 'public-recover':
            result = public_recover(data, public, ROOT/'inputs')
        else:
            result = recover(data, public, _hex(request['private'], ARTIFACT_BYTES), ROOT/'inputs')
    except MissingPublicRelation as exc:
        return {'status': 'BLOCKED', 'reason': str(exc)}
    return {'status': 'COMPLETED', 'data': result.hex()}


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
    if type(response) is not dict or response.get('status') not in ('BLOCKED', 'COMPLETED'):
        raise RuntimeError('invalid worker response')
    return response


def experiment(message: bytes, profile: Profile, corpus: bytes, sources: str | Path) -> dict:
    """Run a bounded input-partition probe; return counts/identities, not secrets."""
    if type(message) is not bytes or len(message) > LIMITS.input_bytes:
        raise Refused('experiment message must be at most 256 bytes')
    public, private = partition(profile, corpus)
    control = full_profile_control(public, private)
    # Verify required sources first: missing geometry is an infrastructure error,
    # never evidence that an attacker cannot recover.
    load_native(sources)
    with tempfile.TemporaryDirectory(prefix='weave-public-private-') as directory:
        root = Path(directory)
        for name in RUNTIME:
            (root/name).write_bytes((ROOT/name).read_bytes())
        lock = strict_json((ROOT/'CYCLE_NATIVE.json').read_bytes())
        for name in lock['ucns_sources']:
            target = root/'inputs'/'ucns'/name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((Path(sources)/'ucns'/name).read_bytes())
        source_files = {str(p.relative_to(root)): sha256(p.read_bytes()).hexdigest()
                        for p in sorted(root.rglob('*')) if p.is_file()}
        # Public evaluation is tried before the private recovery input is sent to
        # any process. No profile fixture or private file exists in the bundle.
        candidate = _run(root, 'send', public, message)
        sent = _run(root, 'send', control, message)
        if sent['status'] != 'COMPLETED':
            raise RuntimeError('full-profile control did not produce a packet')
        packet = _hex(sent['data'], LIMITS.round_bytes + 128)
        recipient = _run(root, 'recover', public, packet, private)
        projected_attack = _run(root, 'public-recover', public, packet)
        control_attack = _run(root, 'public-recover', control, packet)
        after = {str(p.relative_to(root)): sha256(p.read_bytes()).hexdigest()
                 for p in sorted(root.rglob('*')) if p.is_file()}
        if source_files != after:
            raise RuntimeError('worker bundle changed during the experiment')
    recipient_exact = recipient['status'] == 'COMPLETED' and _hex(recipient['data'], LIMITS.input_bytes) == message
    attack_exact = control_attack['status'] == 'COMPLETED' and _hex(control_attack['data'], LIMITS.input_bytes) == message
    if not recipient_exact or not attack_exact or candidate['status'] != 'BLOCKED' or projected_attack['status'] != 'BLOCKED':
        raise RuntimeError('frozen cycle control behavior changed; reassess the experiment')
    return {
        'schema': 'weave.private-public-experiment/v1', 'execution': 'COMPLETED',
        'construction': 'INPUT_PARTITION_ONLY', 'distinction_established': False,
        'whole_plus_one': {'status': candidate['status'], 'reason': candidate['reason'],
                           'packet_created_by_public_sender': False,
                           'private_gonol_relation': 'UNIMPLEMENTED'},
        'full_profile_control': {'status': 'FALSIFIED', 'public_sender_completed': True,
                                 'recipient_exact': recipient_exact, 'public_only_exact': attack_exact,
                                 'whole_plus_one_preserved': False},
        'projected_public_recovery': {'status': projected_attack['status'],
                                     'scope': 'control packet; API refusal is not private necessity'},
        'inputs': {'sender': ['message', 'public'], 'recipient': ['packet', 'public', 'private'],
                   'attacker': ['packet', 'public'], 'shared': ['exact code', 'locked native sources'],
                   'corpus': 'actual bytes inside public artifact'},
        'accounting': {'message_bytes': len(message), 'packet_bytes': len(packet),
                       'public_bytes': len(public), 'private_bytes': len(private),
                       'full_profile_control_bytes': len(control)},
        'source_files': source_files,
        'source_sha256': sha256(canonical(source_files)).hexdigest(),
        'native_lock_sha256': sha256((ROOT/'CYCLE_NATIVE.json').read_bytes()).hexdigest(),
        'packet_sha256': sha256(packet).hexdigest(),
        'nonclaim': 'No falsification of intended Weave, no trapdoor or cryptographic security claim.',
        'hmmm': 'Native private-gonol constructor, public evaluation and private recovery law remain undefined.'}


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
            result = experiment(b'ABxABy\x00ABxABy\xff', profile, bytes(range(256)), args.sources)
        print(canonical(result).decode())
        return 1 if args.require_distinction and not result.get('distinction_established', False) else 0
    except (Refused, OSError, RuntimeError) as exc:
        print(f'private/public experiment error: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
# ratios: loc_comments=229:55 imports_exports=14:8 calls_definitions=121:16
