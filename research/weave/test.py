#!/usr/bin/env python3
"""Run all local assembly/transport tests and emit an honest source-bound receipt.

Usage: python test.py --receipt /tmp/weave-check.json
No dependency installation or network. Native corpus replay is NOT executed by
this suite, and missing native encryption laws are reported separately from PASS.
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
    passed = (result.wasSuccessful() and not result.skipped
              and not result.expectedFailures and not result.unexpectedSuccesses
              and result.testsRun == 54 and before == after)
    receipt = {
        'schema':'weave.transport-evidence/v1',
        'status':'PASSED' if passed else 'FAILED',
        'python':platform.python_version(),
        'tests':result.testsRun,
        'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
        'source_unchanged':before == after,
        'expected_test_methods':54,
        'coverage_status':'WITNESSED' if passed else 'NOT_ACCEPTED',
        'source_sha256':hashlib.sha256(json.dumps(before,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'source_files':before,
        'coverage':{'binary_messages':8191,'binary_lengths_inclusive':[0,12],
                    'assembly_switch_masks':512,'transport_switch_masks':32,
                    'valid_transport_masks':28,'incompatible_transport_masks':4,
                    'largest_roundtrip_bytes':65536,'separate_process_roundtrip_bytes':1026},
        'full_weave':Pipeline().plan(),
        'native_corpus_replay':'NOT_EXECUTED: source inspected; no constructed database materialized here',
        'native_adapter_tests':'missing-input/source-identity refusal only; not successful real-corpus replay',
        'security_observations':['fixed-map recovery succeeds against this transport candidate at 137 bits in 8 queries',
                                 'wrong material can yield wrong plaintext without an authentication error'],
        'nonclaim':'No complete native Weave or asymmetric security result; no independent researcher review.'
    }
    sys.stderr.write(report.getvalue())
    if args.receipt:
        args.receipt.parent.mkdir(parents=True,exist_ok=True)
        args.receipt.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({key:receipt[key] for key in ('status','tests','failures','errors','skipped','source_sha256')}))
    return 0 if passed else 1


if __name__=='__main__':raise SystemExit(main())
