#!/usr/bin/env python3
"""Run the full repository Weave suite and emit a source-bound receipt.

Usage: WEAVE_SOURCES=/checkouts python test.py --receipt /tmp/weave-check.json
The exact source lock is required for the native cycle tests. All remaining old
transport tests retain their scope; no cycle result establishes cipher security.
This runner belongs to the full Stack checkout, not the smaller standalone bundle.
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
EXPECTED_TESTS = 137  # 125 existing + 12 final-review closure regressions.


def snapshot():
    paths = list(ROOT.rglob('*.py')) + list((ROOT/'profiles').glob('*.json'))
    paths += [ROOT/'CYCLE_NATIVE.json', ROOT/'CYCLE_WORK_GRAPH.json']
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(set(paths)) if '__pycache__' not in p.parts and 'sources' not in p.parts}


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
              and result.testsRun == EXPECTED_TESTS and before == after)
    receipt = {
        'schema': 'weave.sequence-cycle-suite/v1',
        'status': 'PASSED' if passed else 'FAILED',
        'python': platform.python_version(),
        'tests': result.testsRun,
        'failures': len(result.failures), 'errors': len(result.errors), 'skipped': len(result.skipped),
        'expected_test_methods': EXPECTED_TESTS,
        'source_unchanged': before == after,
        'source_sha256': hashlib.sha256(json.dumps(before, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
        'source_files': before,
        'native_sources': json.loads((ROOT/'CYCLE_NATIVE.json').read_text()),
        'work_graph_sha256': json.loads((ROOT/'CYCLE_WORK_GRAPH.json').read_text())['work_graph_sha256'],
        'coverage_status': 'WITNESSED' if passed else 'NOT_ACCEPTED',
        'coverage': {
            'old_transport_binary_messages': 8191, 'assembly_switch_masks': 512,
            'transport_switch_masks': 32, 'valid_transport_masks': 28,
            'incompatible_transport_masks': 4, 'old_transport_largest_roundtrip_bytes': 65536,
            'numeral_short_bitblocks': 8191, 'numeral_large_block_bits': 8388608,
            'numeral_repeated_roundtrip_bytes': 4194304, 'numeral_review_regressions': 3,
            'discovery_binary_alphabet_byte_strings': 8191,
            'small_compositions': 4083, 'cycle_largest_roundtrip_bytes': 65536,
            'cycle_sample_rounds': 3, 'native_occurrence_circles': 7,
            'prime_jump_trace': [5381, 53, 241, 1523],
            'native_origin_methods': 13, 'cycle_repair_methods': 12,
            'review_closure_methods': 12
        },
        'cycle': 'EXPLICIT_CANDIDATE: corpus normalization once; native sequence affixiation and prime-derived bit interleave; exact reverse',
        'full_weave': Pipeline().plan(),
        'asymmetric_cipher': 'NOT_IMPLEMENTED: cycle/profile recovery is not a public/private trapdoor',
        'native_language_corpus_replay': 'NOT_EXECUTED: binary construction does not use or replace a language corpus',
        'security_observations': [
            'The older fixed transport map remains recoverable in its declared attack experiment.',
            'The cycle is deterministic from the same source, corpus and profile; syntax/digest checks are not authentication.'
        ],
        'retired_substitutions': {
            'stack_pr_73': 'REMOVED: per-bit public sheet substitution',
            'stack_pr_74': 'REMOVED: bit-axis public feedback',
            'stack_pr_76': 'SUPERSEDED: one-bit-per-circle byte records replaced by native sequence-cycle construction',
            'evidence_scope': 'Rejected encoders do not falsify the corrected sequence construction.'
        },
        'nonclaim': 'No fixed total expansion, universal compression, cryptographic strength, or language-graduation result.'
    }
    sys.stderr.write(report.getvalue())
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({k: receipt[k] for k in ('status','tests','failures','errors','skipped','source_sha256')}))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
