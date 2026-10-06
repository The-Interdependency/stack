# ratios: loc_comments=184:111 imports_exports=14:1 calls_definitions=122:22
# === CHECKS ===
# id: check_private_public_exact_whole_plus_one_export_for_each_circle
#   proves: weave_public_artifact_boundary
#   call: self::test_exact_whole_plus_one_export_for_each_circle
#   mutates: none
#   cleanup: none
# id: check_private_public_sender_blocks_before_forward_or_native_loading
#   proves: weave_sender_no_private_fallback
#   call: self::test_sender_blocks_before_forward_or_native_loading
#   mutates: none
#   cleanup: none
# id: check_private_public_projected_public_recovery_refusal_is_not_security_evidence
#   proves: weave_sender_no_private_fallback
#   call: self::test_projected_public_recovery_refusal_is_not_security_evidence
#   mutates: none
#   cleanup: none
# id: check_private_public_private_recovery_exact_for_binary_edge_cases
#   proves: weave_private_reconstruction_inputs
#   call: self::test_private_recovery_exact_for_binary_edge_cases
#   mutates: none
#   cleanup: none
# id: check_private_public_public_only_inverse_is_a_real_counterexample
#   proves: weave_public_recovery_falsifier
#   call: self::test_public_only_inverse_is_a_real_counterexample
#   mutates: none
#   cleanup: none
# id: check_private_public_control_matches_unmodified_cycle_bytes
#   proves: weave_public_recovery_falsifier
#   call: self::test_control_matches_unmodified_cycle_bytes
#   mutates: none
#   cleanup: none
# id: check_private_public_private_input_is_required_by_recipient_interface
#   proves: weave_private_reconstruction_inputs
#   call: self::test_private_input_is_required_by_recipient_interface
#   mutates: none
#   cleanup: none
# id: check_private_public_wrong_hidden_private_space_fails_even_with_matching_public_projection
#   proves: weave_private_reconstruction_inputs
#   call: self::test_wrong_hidden_private_space_fails_even_with_matching_public_projection
#   mutates: none
#   cleanup: none
# id: check_private_public_wrong_pair_and_changed_visible_space_refused
#   proves: weave_private_reconstruction_inputs
#   call: self::test_wrong_pair_and_changed_visible_space_refused
#   mutates: none
#   cleanup: none
# id: check_private_public_private_leak_and_incomplete_control_are_refused
#   proves: weave_public_artifact_boundary
#   call: self::test_private_leak_and_incomplete_control_are_refused
#   mutates: none
#   cleanup: none
# id: check_private_public_strict_artifact_schema_and_types
#   proves: weave_public_artifact_boundary
#   call: self::test_strict_artifact_schema_and_types
#   mutates: none
#   cleanup: none
# id: check_private_public_invalid_public_profile_rejected_before_cycle
#   proves: weave_public_artifact_boundary
#   call: self::test_invalid_public_profile_rejected_before_cycle
#   mutates: none
#   cleanup: none
# id: check_private_public_artifact_sizes_and_corpus_limits
#   proves: weave_public_artifact_boundary
#   call: self::test_artifact_sizes_and_corpus_limits
#   mutates: none
#   cleanup: none
# id: check_private_public_corrupted_and_truncated_packet_are_not_recovery
#   proves: weave_private_reconstruction_inputs
#   call: self::test_corrupted_and_truncated_packet_are_not_recovery
#   mutates: none
#   cleanup: none
# id: check_private_public_three_round_fresh_process_input_manifests
#   proves: weave_process_evidence_boundary
#   call: self::test_three_round_fresh_process_input_manifests
#   mutates: filesystem
#   cleanup: tempdir_teardown
# id: check_private_public_report_does_not_include_private_artifact_or_plaintext
#   proves: weave_process_evidence_boundary
#   call: self::test_report_does_not_include_private_artifact_or_plaintext
#   mutates: filesystem
#   cleanup: tempdir_teardown
# id: check_private_public_missing_native_source_is_error_not_attacker_failure
#   proves: weave_distinction_gate
#   call: self::test_missing_native_source_is_error_not_attacker_failure
#   mutates: none
#   cleanup: none
# id: check_private_public_worker_crash_is_not_public_recovery_failure
#   proves: weave_distinction_gate
#   call: self::test_worker_crash_is_not_public_recovery_failure
#   mutates: filesystem
#   cleanup: tempdir_teardown
# id: check_private_public_acceptance_cli_exits_one_with_honest_report
#   proves: weave_distinction_gate
#   call: self::test_acceptance_cli_exits_one_with_honest_report
#   mutates: filesystem
#   cleanup: tempdir_teardown
# id: check_private_public_cli_infrastructure_error_exits_two
#   proves: weave_distinction_gate
#   call: self::test_cli_infrastructure_error_exits_two
#   mutates: none
#   cleanup: none
# === END CHECKS ===
"""Usage: WEAVE_SOURCES=/checkouts python -m unittest discover -s tests -p test_private_public.py -v.

These regressions protect honest experimental failure. They do not claim that
the intended asymmetric/private-gonol layer has been constructed.
"""
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import json
import os
import subprocess
import sys
import unittest
from unittest.mock import patch

import cycle
import private_public as pp
from cycle import Profile, canonical
from numeral import Refused

ROOT = Path(__file__).resolve().parents[1]
SOURCES = Path(os.environ.get('WEAVE_SOURCES', ROOT/'sources'))
BASE = Profile.read((ROOT/'profiles'/'cycle-v1.json').read_bytes())
# Hidden values deliberately differ from the checked-in example. The explicit
# private input has no public filename, path, fixture lookup or PRNG seed.
ROUND = replace(BASE.rounds[0], spaces=tuple(Fraction(13 + i * 11, 113) for i in range(8)))
PROFILE = replace(BASE, scope='private-public-test', rounds=(ROUND,))
CORPUS = b'actual shared corpus\x00\xff'


class PrivatePublicTests(unittest.TestCase):
    def setUp(self):
        self.public, self.private = pp.partition(PROFILE, CORPUS)
        self.control = pp.full_profile_control(self.public, self.private)

    def test_exact_whole_plus_one_export_for_each_circle(self):
        for circle in range(1, 8):
            public, private = pp.partition(BASE, CORPUS, circle=circle)
            obj = json.loads(public)
            for original, row in zip(BASE.as_dict()['rounds'], obj['profile']['rounds']):
                self.assertEqual([i for i, x in enumerate(row['spaces']) if x is not None], [0, circle])
                self.assertEqual(row['spaces'][0], original['spaces'][0])
                self.assertEqual(row['spaces'][circle], original['spaces'][circle])
                self.assertEqual({k: v for k, v in row.items() if k != 'spaces'},
                                 {k: v for k, v in original.items() if k != 'spaces'})
            self.assertEqual(json.loads(private)['profile'], BASE.as_dict())
            self.assertEqual(bytes.fromhex(obj['corpus_hex']), CORPUS)

    def test_sender_blocks_before_forward_or_native_loading(self):
        with patch.object(cycle, 'forward', side_effect=AssertionError('private-dependent forward called')):
            with self.assertRaisesRegex(pp.MissingPublicRelation, 'native public evaluation law missing'):
                pp.send(b'message', self.public, SOURCES)

    def test_projected_public_recovery_refusal_is_not_security_evidence(self):
        with patch.object(cycle, 'reverse', side_effect=AssertionError('guessed missing spaces')):
            with self.assertRaises(pp.MissingPublicRelation):
                pp.public_recover(b'not even a packet', self.public, SOURCES)

    def test_private_recovery_exact_for_binary_edge_cases(self):
        for message in (b'', b'\x00\x00\x01', bytes(range(256)), b'ABxABy' * 12):
            with self.subTest(length=len(message)):
                packet = pp.send(message, self.control, SOURCES)
                self.assertEqual(pp.recover(packet, self.public, self.private, SOURCES), message)

    def test_public_only_inverse_is_a_real_counterexample(self):
        message = b'ABxABy\x00ABxABy\xff'
        packet = pp.send(message, self.control, SOURCES)
        # The attacker bypasses the entire private-path API rather than making
        # that API accept a missing key. No private parameter goes to this call.
        with patch.object(pp, 'recover', side_effect=AssertionError('private API called')):
            self.assertEqual(pp.public_recover(packet, self.control, SOURCES), message)

    def test_control_matches_unmodified_cycle_bytes(self):
        message = b'ABxABy'
        expected, _ = cycle.forward(message, CORPUS, PROFILE, SOURCES, pp.LIMITS)
        self.assertEqual(pp.send(message, self.control, SOURCES), expected)
        control = json.loads(self.control)
        self.assertEqual(control['disclosure'], pp.CONTROL)
        self.assertEqual(control['profile'], PROFILE.as_dict())

    def test_private_input_is_required_by_recipient_interface(self):
        packet = pp.send(b'message', self.control, SOURCES)
        for absent in (None, b'', self.public, self.control):
            with self.assertRaises(Refused):
                pp.recover(packet, self.public, absent, SOURCES)
        # This interface refusal is deliberately paired with the public attack.
        self.assertEqual(pp.public_recover(packet, self.control, SOURCES), b'message')

    def test_wrong_hidden_private_space_fails_even_with_matching_public_projection(self):
        packet = pp.send(b'ABxABy', self.control, SOURCES)
        obj = json.loads(self.private)
        obj['profile']['rounds'][0]['spaces'][2] = [1, 97]
        with self.assertRaisesRegex(Refused, 'profile identity mismatch'):
            pp.recover(packet, self.public, canonical(obj), SOURCES)

    def test_wrong_pair_and_changed_visible_space_refused(self):
        packet = pp.send(b'message', self.control, SOURCES)
        other, _ = pp.partition(PROFILE, CORPUS + b'!')
        with self.assertRaisesRegex(Refused, 'exact public bytes'):
            pp.recover(packet, other, self.private, SOURCES)
        obj = json.loads(self.private)
        obj['profile']['rounds'][0]['spaces'][0] = [1, 97]
        with self.assertRaisesRegex(Refused, 'public projection'):
            pp.recover(packet, self.public, canonical(obj), SOURCES)

    def test_private_leak_and_incomplete_control_are_refused(self):
        obj = json.loads(self.public)
        obj['profile']['rounds'][0]['spaces'][2] = [0, 1]
        with self.assertRaisesRegex(Refused, 'leaked'):
            pp.send(b'hi', canonical(obj), SOURCES)
        obj = json.loads(self.control)
        obj['profile']['rounds'][0]['spaces'][2] = None
        with self.assertRaisesRegex(Refused, 'public space absent'):
            pp.send(b'hi', canonical(obj), SOURCES)

    def test_strict_artifact_schema_and_types(self):
        base = json.loads(self.public)
        cases = []
        for key, value in [('circle', True), ('circle', 0), ('circle', 8), ('schema', 'other'),
                           ('disclosure', 'asymmetric'), ('private', 'file://secret'),
                           ('corpus_hex', 'AA'), ('corpus_hex', '00 '), ('native_lock_sha256', '0' * 64)]:
            obj = deepcopy(base); obj[key] = value; cases.append(canonical(obj))
        cases += [b'[]', b'{"schema":1,"schema":2}', b'{"x":NaN}', b'\xff', b'x' * 32769]
        for data in cases:
            with self.subTest(data=data[:80]), self.assertRaises(Refused):
                pp.send(b'm', data, SOURCES)

    def test_invalid_public_profile_rejected_before_cycle(self):
        for field, value in [('spaces', []), ('end_order', 'sideways'), ('arities', [True]),
                             ('circle_order', [1] * 7), ('prime_path', {'seed': 1, 'steps': []})]:
            obj = json.loads(self.public)
            obj['profile']['rounds'][0][field] = value
            with self.assertRaises(Refused):
                pp.send(b'm', canonical(obj), SOURCES)
        obj = json.loads(self.public)
        obj['profile']['rounds'][0]['spaces'][0] = [2, 4]
        with self.assertRaises(Refused):
            pp.send(b'm', canonical(obj), SOURCES)

    def test_artifact_sizes_and_corpus_limits(self):
        for corpus in (b'', b'x' * 4097, 'corpus'):
            with self.assertRaises(Refused): pp.partition(PROFILE, corpus)
        with self.assertRaises(Refused):
            pp.partition(replace(BASE, rounds=BASE.rounds * 2), CORPUS)
        with self.assertRaises(Refused):
            pp.send(b'x' * 257, self.control, SOURCES)
        with self.assertRaises(Refused):
            pp.experiment(b'x' * 257, PROFILE, CORPUS, SOURCES)

    def test_corrupted_and_truncated_packet_are_not_recovery(self):
        packet = pp.send(b'message', self.control, SOURCES)
        damaged = bytearray(packet); damaged[36] ^= 1
        for bad in (packet[:-1], packet + b'!', bytes(damaged)):
            with self.assertRaises(Refused): pp.public_recover(bad, self.control, SOURCES)
            with self.assertRaises(Refused): pp.recover(bad, self.public, self.private, SOURCES)

    def test_three_round_fresh_process_input_manifests(self):
        calls = []
        original = pp._run
        def observe(root, operation, public, data, private=None):
            files = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
            self.assertFalse(any('profile' in p or 'test_' in p for p in files))
            self.assertEqual(private is not None, operation == 'recover')
            calls.append((operation, set(json.loads(public)), private is not None))
            return original(root, operation, public, data, private)
        with patch.object(pp, '_run', side_effect=observe):
            report = pp.experiment(b'ABxABy\x00ABxABy', BASE, CORPUS, SOURCES)
        self.assertEqual([c[0] for c in calls], ['send', 'send', 'recover', 'public-recover', 'public-recover'])
        self.assertFalse(report['distinction_established'])
        self.assertEqual(report['whole_plus_one']['status'], 'BLOCKED')
        self.assertEqual(report['full_profile_control']['status'], 'FALSIFIED')
        self.assertTrue(report['full_profile_control']['recipient_exact'])
        self.assertTrue(report['full_profile_control']['public_only_exact'])
        self.assertNotIn('private', report['inputs']['sender'])
        self.assertNotIn('private', report['inputs']['attacker'])
        self.assertNotIn('message', report['inputs']['recipient'])
        self.assertEqual(set(report['source_files']), set(pp.RUNTIME) | {
            'inputs/ucns/src/ucns/axis_circle.py', 'inputs/ucns/src/ucns/direct_mobius.py'})

    def test_report_does_not_include_private_artifact_or_plaintext(self):
        message = b'not-a-secret-but-must-not-enter-report'
        report = pp.experiment(message, PROFILE, CORPUS, SOURCES)
        rendered = canonical(report)
        self.assertNotIn(message, rendered)
        self.assertNotIn(message.hex().encode(), rendered)
        self.assertNotIn(self.private, rendered)
        self.assertNotIn(b'corpus_hex', rendered)
        self.assertEqual(report['accounting']['message_bytes'], len(message))

    def test_missing_native_source_is_error_not_attacker_failure(self):
        with patch.object(pp, 'load_native', side_effect=Refused('missing native source')):
            with self.assertRaisesRegex(Refused, 'missing native source'):
                pp.experiment(b'm', PROFILE, CORPUS, SOURCES)

    def test_worker_crash_is_not_public_recovery_failure(self):
        result = subprocess.CompletedProcess([], 2, b'', b'infrastructure failure')
        with patch.object(pp.subprocess, 'run', return_value=result):
            with self.assertRaisesRegex(RuntimeError, 'worker failed'):
                pp.experiment(b'm', PROFILE, CORPUS, SOURCES)

    def test_acceptance_cli_exits_one_with_honest_report(self):
        result = subprocess.run([sys.executable, str(ROOT/'private_public.py'), '--sources', str(SOURCES),
                                 '--require-distinction'], capture_output=True)
        self.assertEqual(result.returncode, 1, result.stderr.decode())
        report = json.loads(result.stdout)
        self.assertEqual(report['execution'], 'COMPLETED')
        self.assertFalse(report['distinction_established'])
        self.assertEqual(report['full_profile_control']['status'], 'FALSIFIED')

    def test_cli_infrastructure_error_exits_two(self):
        result = subprocess.run([sys.executable, str(ROOT/'private_public.py'), '--sources', '/nonexistent-weave-inputs'],
                                capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, b'')
        self.assertIn(b'experiment error', result.stderr)


if __name__ == '__main__':
    unittest.main()
# ratios: loc_comments=184:111 imports_exports=14:1 calls_definitions=122:22
