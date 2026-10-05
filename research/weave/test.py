#!/usr/bin/env python3
"""Run the full Weave workspace suite and emit a source-bound receipt.

Usage: python test.py --receipt /tmp/weave-check.json
Transport behavior, byte/star construction records and their boundaries are tested.
Native positional encryption and native corpus replay remain explicitly unexecuted.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import platform
import sys
import unittest
from assembly import Pipeline

ROOT = Path(__file__).resolve().parent


def snapshot():
    paths = list(ROOT.rglob('*.py')) + list((ROOT/'profiles').glob('*.json'))
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(paths) if '__pycache__' not in p.parts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    before = snapshot()
    report = io.StringIO()
    result = unittest.TextTestRunner(stream=report, verbosity=2).run(
        unittest.defaultTestLoader.discover(str(ROOT/'tests')))
    after = snapshot()
    # 52 unchanged transport/assembly methods + 12 byte/star + 10 message methods.
    passed = (result.wasSuccessful() and not result.skipped
              and not result.expectedFailures and not result.unexpectedSuccesses
              and result.testsRun == 74 and before == after)
    receipt = {
        'schema':'weave.transport-evidence/v1',
        'status':'PASSED' if passed else 'FAILED',
        'python':platform.python_version(),
        'tests':result.testsRun,
        'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
        'source_unchanged':before == after,
        'expected_test_methods':74,
        'coverage_status':'WITNESSED' if passed else 'NOT_ACCEPTED',
        'source_sha256':hashlib.sha256(json.dumps(before,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'source_files':before,
        'coverage':{'binary_messages':8191,'binary_lengths_inclusive':[0,12],
                    'assembly_switch_masks':512,'transport_switch_masks':32,
                    'valid_transport_masks':28,'incompatible_transport_masks':4,
                    'largest_roundtrip_bytes':65536,'separate_process_roundtrip_bytes':1026,
                    'byte_values':256,'bit_to_circle_assignments':40320,
                    'whole_part_key_views':7,'bit_placements_per_byte':8,
                    'message_participants_per_byte':1},
        'declared_ciphertext_bits_per_byte':16,
        'positional_cipher':'NOT_IMPLEMENTED: byte/star structure repaired; transform proposals await approval',
        'full_weave':Pipeline().plan(),
        'native_corpus_replay':'NOT_EXECUTED: no constructed database materialized by this suite',
        'native_adapter_tests':'missing-input/source-identity refusal only; not successful real-corpus replay',
        'security_observations':[
            'fixed-map recovery succeeds against the older transport candidate at 137 bits in 8 queries',
            'wrong material can yield wrong plaintext without an authentication error'
        ],
        'retired_substitutions':{
            'stack_pr_73':'REMOVED: per-bit two-sheet encoding was not the specified byte construction',
            'stack_pr_74':'REMOVED: bit-axis public feedback was not the specified whole-byte coupling',
            'evidence_scope':'their attacks concern those rejected implementations, not Weave',
            'private_perturbation_correction':'unchanged public encryption inputs cannot establish private-key noncausality'
        },
        'nonclaim':'Construction-source recovery is not decryption. No native Weave security result.'
    }
    sys.stderr.write(report.getvalue())
    if args.receipt:
        args.receipt.parent.mkdir(parents=True,exist_ok=True)
        args.receipt.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({key:receipt[key] for key in ('status','tests','failures','errors','skipped','source_sha256')}))
    return 0 if passed else 1


if __name__=='__main__':raise SystemExit(main())
