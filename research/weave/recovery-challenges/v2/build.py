# ratios: loc_comments=159:32 imports_exports=16:7 calls_definitions=81:7
"""Freeze, generate and verify actual challenges without publishing their answers.

Usage: python build.py freeze --private /absolute/operator
       python build.py generate --private /absolute/operator --workers 4
       python build.py package --private /absolute/operator
Generation resumes only completed, hash-checked checkpoints. Failed planned cases
remain visible and prevent packaging; no cap relaxation or silent resampling.
"""
# === MODULE_BUILD ===
# id: challenge_build
#   module_name: build
#   module_kind: experiment
#   summary: generate measured ciphertexts with separate evaluator and receiver inputs
#   owner: Erin Spencer
#   public_surface: freeze, generate, package
#   internal_surface: per-case checkpoints and fresh receiver subprocess
#   tests: test_harness.py
#   rollout: private first, public ciphertext archive after verification
#   rollback: remove v2; preserve already released v1
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: write
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: exact_receiver_verification
#   given: every frozen planned challenge
#   then: compare fresh receiver output byte-for-byte with evaluator-only message
# id: separated_artifacts
#   given: verified private fixtures
#   then: publish only ciphertexts, ciphertext digests, opaque IDs and aggregate coverage
# === END CONTRACTS ===
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import Counter
from hashlib import sha256
from pathlib import Path
import argparse
import json
import os
import secrets
import subprocess
import sys
import tempfile
import time
import zipfile
import operations as o
import matrix
from transport_cases import run as transport


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def save(path, value):
    path = Path(path)
    with path.open('x') as out:
        json.dump(value, out, indent=2)
        out.write('\n')


def freeze(root):
    if not root.is_absolute() or root == o.CHECKOUT or root.is_relative_to(o.CHECKOUT):
        raise ValueError('private fixtures must live outside the checkout')
    root.mkdir(mode=0o700, parents=True, exist_ok=False)
    os.chmod(root, 0o700)
    rows = matrix.schedules()
    secrets.SystemRandom().shuffle(rows)
    for row in rows:
        row.update(id=secrets.token_hex(8), parameters=matrix.parameters(row),
                   message_hex=matrix.message(row).hex())
    if len({r['id'] for r in rows}) != len(rows):
        raise RuntimeError('opaque ID collision')
    plan = {'schema': 'weave.recovery-private/v2', 'cases': rows,
            'prediction_status': 'FROZEN_BEFORE_ENCODING_AND_ATTACKS',
            'salt': secrets.token_hex(32)}
    save(root/'private.json', plan)
    for name in ('ciphertexts', 'receipts'):
        (root/name).mkdir(mode=0o700)
    print(json.dumps({'frozen': len(rows), 'commitment': sha256(canonical(plan)).hexdigest()}), flush=True)


def one_case(root_text, row):
    root = Path(root_text); start = time.monotonic()
    receipt_path = root/'receipts'/f"{row['id']}.json"
    wire_path = root/'ciphertexts'/f"{row['id']}.bin"
    if receipt_path.exists():
        receipt = json.loads(receipt_path.read_text())
        if receipt['status'] == 'VERIFIED' and sha256(wire_path.read_bytes()).hexdigest() == receipt['wire_sha256']:
            return receipt
        raise ValueError('checkpoint invalid or failed; inspect without silently regenerating')
    try:
        message = bytes.fromhex(row['message_hex']); p = row['parameters']
        if row['family'] == 'cycle':
            wire, _ = o.cycle.forward(message, bytes.fromhex(p['corpus_hex']), o.profile(p), o.SOURCES)
        elif row['family'] == 'transport':
            wire = transport(message, row['schedule'], p)
        else:
            wire = o.execute(message, row['schedule'], p)
        request = {k: row[k] for k in ('family', 'schedule', 'parameters')}
        request['wire_hex'] = wire.hex()
        # The subprocess receives no message, answer digest, prediction salt or trace.
        with tempfile.TemporaryDirectory(prefix='receiver-', dir=root) as temp:
            folder = Path(temp); save(folder/'request.json', request)
            completed = subprocess.run([sys.executable, '-I', '-B', str(o.HERE/'operations.py'),
                'receive', '--request', str(folder/'request.json'), '--output', str(folder/'restored.bin')],
                capture_output=True, env={'PATH': os.environ.get('PATH', ''), 'LC_ALL': 'C.UTF-8'}, close_fds=True)
            if completed.returncode:
                raise RuntimeError('receiver failed: ' + completed.stderr.decode(errors='replace')[-2000:])
            if (folder/'restored.bin').read_bytes() != message:
                raise AssertionError('fresh receiver did not recover exact bytes')
        with wire_path.open('xb') as out:
            out.write(wire)
        receipt = {'id': row['id'], 'status': 'VERIFIED', 'wire_bytes': len(wire),
                   'wire_sha256': sha256(wire).hexdigest(), 'message_bytes': len(message),
                   'seconds': round(time.monotonic()-start, 6), 'fresh_receiver': True}
    except Exception as error:
        receipt = {'id': row['id'], 'status': 'FAILED', 'error': str(error),
                   'seconds': round(time.monotonic()-start, 6)}
    save(receipt_path, receipt)
    return receipt


def generate(root, workers):
    if not 1 <= workers <= 4:
        raise ValueError('one through four workers allowed')
    plan = json.loads((root/'private.json').read_text()); rows = plan['cases']
    started = time.monotonic(); results = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(one_case, str(root), row) for row in rows]
        for future in as_completed(futures):
            result = future.result(); results.append(result)
            if len(results) % 100 == 0 or result['status'] != 'VERIFIED':
                print(json.dumps({'completed': len(results), 'planned': len(rows),
                    'failed': sum(r['status']!='VERIFIED' for r in results),
                    'seconds': round(time.monotonic()-started, 1)}), flush=True)
    report = {'planned': len(rows), 'verified': sum(r['status']=='VERIFIED' for r in results),
              'failures': [r for r in results if r['status']!='VERIFIED'],
              'seconds': round(time.monotonic()-started, 3), 'workers': workers}
    save(root/'generation.json', report)
    print(json.dumps(report), flush=True)
    return 0 if not report['failures'] else 1


def package(root):
    plan = json.loads((root/'private.json').read_text())
    generation = json.loads((root/'generation.json').read_text())
    rows = plan['cases']; receipts = []
    if generation['verified'] != len(rows) or generation['failures']:
        raise ValueError('planned failures forbid a misleading complete archive')
    for row in rows:
        receipt = json.loads((root/'receipts'/f"{row['id']}.json").read_text())
        wire = (root/'ciphertexts'/f"{row['id']}.bin").read_bytes()
        if sha256(wire).hexdigest() != receipt['wire_sha256']:
            raise ValueError('checkpoint wire drift')
        receipts.append(receipt)
    with zipfile.ZipFile(o.HERE/'blind-pack.zip', 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        archive.writestr('README.md', '# Exact-byte recovery challenge\n\nRecover the original bytes of each supplied file. '
            'Record your available inputs, methods, time and result. Submit bytes, not merely plausible prose. '
            'An evaluator can release additional information after you freeze each attempt.\n'
            '\nFor a genuinely independent first attempt, use a fresh context for each file and receive only that file.\n')
        sums = []
        for receipt in sorted(receipts, key=lambda r: r['id']):
            name = receipt['id']+'.bin'
            archive.write(root/'ciphertexts'/name, 'files/'+name)
            sums.append(receipt['wire_sha256']+'  files/'+name)
        archive.writestr('SHA256SUMS', '\n'.join(sums)+'\n')
    accepted, refused = matrix.transport_schedules()
    coverage = {'schema': 'weave.recovery-coverage/v2', 'planned_files': len(rows),
        'verified_files': len(receipts), 'families': dict(Counter(r['family'] for r in rows)),
        'core_alphabet': list(matrix.CORE), 'pair_words_per_pair': 62, 'core_pairs': 15,
        'pair_words_covered': 930, 'max_instances_per_operation': 3,
        'higher_order_rule': 'PLAN.md; subset forward/reverse and repeat-in-context, not exhaustive all words',
        'transport_accepted': len(accepted), 'transport_typed_refusals': len(refused),
        'full_weave_coverage': 'INCOMPLETE', 'unimplemented_obligations': matrix.MISSING,
        'attacker_trials_run': 0, 'receiver_checks_are_attacks': False,
        'prediction_commitment_sha256': sha256(canonical(plan)).hexdigest(),
        'commitment_method': 'SHA256 of canonical private.json including independent 32-byte salt',
        'private_case_mapping': 'operator archive only'}
    results = {'generation': generation, 'ciphertext_bytes': sum(r['wire_bytes'] for r in receipts),
        'min_wire_bytes': min(r['wire_bytes'] for r in receipts),
        'max_wire_bytes': max(r['wire_bytes'] for r in receipts),
        'sum_case_seconds': round(sum(r['seconds'] for r in receipts), 3),
        'archive_bytes': (o.HERE/'blind-pack.zip').stat().st_size,
        'archive_sha256': sha256((o.HERE/'blind-pack.zip').read_bytes()).hexdigest(),
        'receiver_boundary': 'Fresh -I subprocess; explicit inputs, not an OS sandbox.',
        'security_result': 'NO_ATTACKS_RUN; selected-material round trips only.'}
    save(o.HERE/'COVERAGE.json', coverage); save(o.HERE/'RESULTS.json', results)
    print(json.dumps(results), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['freeze', 'generate', 'package'])
    parser.add_argument('--private', type=Path, required=True)
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    if args.command == 'freeze':
        freeze(args.private)
    elif args.command == 'generate':
        return generate(args.private, args.workers)
    else:
        package(args.private)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
# ratios: loc_comments=159:32 imports_exports=16:7 calls_definitions=81:7
