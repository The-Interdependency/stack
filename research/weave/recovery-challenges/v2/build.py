# ratios: loc_comments=234:44 imports_exports=16:15 calls_definitions=131:15
"""Freeze, generate and verify actual challenges without publishing their answers.

Usage: python build.py freeze --private /absolute/operator
       python build.py generate --private /absolute/operator --workers 4
       python build.py package --private /absolute/operator
Generation resumes hash-checked checkpoints and verifies orphaned ciphertexts
against the frozen result before reconstructing receipts. Conflicts are retained.
Private paths resolve outside the checkout; use an operator-owned directory.
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
# id: frozen_case_checkpoint_binding
#   given: a resumed, packaged, exported or graded case with changed inputs or an unbound historical receipt
#   then: refuse before accepting verification or publishing, preserving existing evidence
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


def case_digest(row):
    """Bind the complete frozen row, including message and receiver parameters."""
    case_id = row.get('id') if isinstance(row, dict) else None
    if not isinstance(case_id, str) or len(case_id) != 16 or any(c not in '0123456789abcdef' for c in case_id):
        raise ValueError('invalid opaque case ID')
    return sha256(canonical(row)).hexdigest()


def frozen_plan(root):
    plan = json.loads((root/'private.json').read_text())
    rows = plan['cases']
    if not isinstance(rows, list) or not rows:
        raise ValueError('frozen plan requires a nonempty case list')
    for row in rows:
        case_digest(row)
    if len({row['id'] for row in rows}) != len(rows):
        raise ValueError('duplicate frozen case ID')
    return plan


def load_verified_case(root, row):
    """Return the receipt and exact ciphertext buffer admitted for this frozen row."""
    digest = case_digest(row)
    receipt = json.loads(private_path(root, 'receipts', row['id']+'.json').read_text())
    if (not isinstance(receipt, dict)
            or receipt.get('schema') != 'weave.challenge-checkpoint/v1'
            or receipt.get('case_sha256') != digest
            or receipt.get('id') != row['id'] or receipt.get('status') != 'VERIFIED'
            or receipt.get('fresh_receiver') is not True):
        raise ValueError('checkpoint invalid, unbound or mismatched; preserve evidence and reverify separately')
    wire = private_path(root, 'ciphertexts', row['id']+'.bin').read_bytes()
    if (receipt.get('wire_sha256') != sha256(wire).hexdigest()
            or receipt.get('wire_bytes') != len(wire)
            or receipt.get('message_bytes') != len(bytes.fromhex(row['message_hex']))):
        raise ValueError('checkpoint invalid, unbound or mismatched; preserve evidence and reverify separately')
    return receipt, wire


def checked_checkpoint(root, row):
    """Resume and publication use the same admission rule as release and grading."""
    return load_verified_case(root, row)[0]


def save(path, value):
    publish(path, (json.dumps(value, indent=2)+'\n').encode())


def publish(path, data):
    """Publish a complete checkpoint exclusively; never replace existing evidence."""
    path = Path(path)
    fd, temporary = tempfile.mkstemp(prefix='.'+path.name+'.', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as out:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
        os.link(temporary, path)
    finally:
        os.unlink(temporary)


def outside_checkout(path):
    """Canonicalize parent traversal and symlinks before any private write."""
    path = Path(path).resolve()
    if path.is_relative_to(o.CHECKOUT.resolve()):
        raise ValueError('private artifacts must live outside the checkout')
    return path


def private_path(root, *parts):
    """Keep every private child in the admitted archive, including existing links."""
    root = outside_checkout(root)
    path = outside_checkout(root.joinpath(*parts))
    if not path.is_relative_to(root):
        raise ValueError('private artifact escapes the private archive')
    return path


def private_root(root):
    root = outside_checkout(root)
    for name in ('private.json', 'ciphertexts', 'receipts', 'generation.json'):
        private_path(root, name)
    return root


def freeze(root):
    if not root.is_absolute():
        raise ValueError('private fixtures require an absolute path')
    root = private_root(root)
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
    root = private_root(root_text); start = time.monotonic()
    digest = case_digest(row)
    case_id = row['id']
    identity = {'schema': 'weave.challenge-checkpoint/v1', 'id': case_id, 'case_sha256': digest}
    receipt_path = private_path(root, 'receipts', f'{case_id}.json')
    wire_path = private_path(root, 'ciphertexts', f'{case_id}.bin')
    if receipt_path.exists():
        return checked_checkpoint(root, row)
    try:
        message = bytes.fromhex(row['message_hex']); p = row['parameters']
        if row['family'] == 'cycle':
            wire, _ = o.cycle.forward(message, bytes.fromhex(p['corpus_hex']), o.profile(p), o.SOURCES)
        elif row['family'] == 'transport':
            wire = transport(message, row['schedule'], p)
        else:
            wire = o.execute(message, row['schedule'], p)
    except Exception as error:
        receipt = {**identity, 'status': 'FAILED', 'error': str(error),
                   'seconds': round(time.monotonic()-start, 6)}
        save(receipt_path, receipt)
        return receipt
    # Recompute from the frozen row, then compare actual bytes, not an absent
    # receipt or a claimed digest. A mismatch must not create a FAILED checkpoint.
    if wire_path.exists() and wire_path.read_bytes() != wire:
        raise ValueError('orphaned ciphertext conflicts with frozen result')
    try:
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
    except Exception as error:
        receipt = {**identity, 'status': 'FAILED', 'error': str(error),
                   'seconds': round(time.monotonic()-start, 6)}
        save(receipt_path, receipt)
        return receipt
    if wire_path.exists():
        if wire_path.read_bytes() != wire:
            raise ValueError('ciphertext changed during receiver verification')
    else:
        publish(wire_path, wire)
    receipt = {**identity, 'status': 'VERIFIED', 'wire_bytes': len(wire),
               'wire_sha256': sha256(wire).hexdigest(), 'message_bytes': len(message),
               'seconds': round(time.monotonic()-start, 6), 'fresh_receiver': True}
    save(receipt_path, receipt)
    return receipt


def generate(root, workers):
    root = private_root(root)
    if not 1 <= workers <= 4:
        raise ValueError('one through four workers allowed')
    plan = frozen_plan(root); rows = plan['cases']
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
    report_path = private_path(root, 'generation.json')
    if report_path.exists():
        previous = json.loads(report_path.read_text())
        if any(previous[key] != report[key] for key in ('planned', 'verified', 'failures')):
            raise ValueError('generation report conflicts with checked receipts')
        report = previous
    else:
        save(report_path, report)
    print(json.dumps(report), flush=True)
    return 0 if not report['failures'] else 1


def package(root):
    root = private_root(root)
    plan = frozen_plan(root)
    generation = json.loads((root/'generation.json').read_text())
    rows = plan['cases']; receipts = []
    if generation['planned'] != len(rows) or generation['verified'] != len(rows) or generation['failures']:
        raise ValueError('planned failures forbid a misleading complete archive')
    for row in rows:
        receipts.append(checked_checkpoint(root, row))
    with zipfile.ZipFile(o.HERE/'blind-pack.zip', 'x', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        archive.writestr('README.md', '# Exact-byte recovery challenge\n\nRecover the original bytes of each supplied file. '
            'Record your available inputs, methods, time and result. Submit bytes, not merely plausible prose. '
            'An evaluator can release additional information after you freeze each attempt.\n'
            '\nFor a genuinely independent first attempt, use a fresh context for each file and receive only that file.\n')
        sums = []
        for receipt in sorted(receipts, key=lambda r: r['id']):
            name = receipt['id']+'.bin'
            archive.write(private_path(root, 'ciphertexts', name), 'files/'+name)
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
# ratios: loc_comments=234:44 imports_exports=16:15 calls_definitions=131:15
