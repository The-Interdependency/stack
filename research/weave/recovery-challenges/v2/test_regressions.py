# ratios: loc_comments=204:5 imports_exports=14:1 calls_definitions=130:19
"""PR #94 integrity regressions, using synthetic private fixtures only.

Run from any directory: python research/weave/recovery-challenges/v2/test_regressions.py
No operator archive or attacker answers are needed. Temporary checkouts witness
rejected disclosure; receiver subprocesses exercise the actual frozen algorithms.
"""
from pathlib import Path
from unittest import mock
import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
import build
import matrix
import operations as o
import release
import test_harness as harness


class Integrity(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.checkout = self.base/'public'
        self.checkout.mkdir()
        self.root = self.base/'operator'
        self.root.mkdir(mode=0o700)
        for name in ('ciphertexts', 'receipts'):
            (self.root/name).mkdir()
        self.row = {'id': '0123456789abcdef', 'family': 'byte', 'schedule': ['B'],
                    'parameters': matrix.parameters({'family': 'byte'}),
                    'message_hex': b'Prediction synthetic fixture\nmy human needs my help\n'.hex()}
        build.save(self.root/'private.json', {'cases': [self.row]})
        self.patch = mock.patch.object(o, 'CHECKOUT', self.checkout)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def paths_into_checkout(self):
        parent = self.base/'external'
        parent.mkdir(exist_ok=True)
        link = self.base/'alias'
        if not link.is_symlink():
            link.symlink_to(self.checkout, target_is_directory=True)
        return (self.checkout/'leak', parent/'..'/'public'/'leak', link/'leak')

    def test_freeze_rejects_public_parent_and_symlink_traversal(self):
        for path in self.paths_into_checkout():
            with self.subTest(path=path), mock.patch.object(matrix, 'schedules', return_value=[]):
                try:
                    with self.assertRaises(ValueError):
                        build.freeze(path)
                    self.assertFalse((self.checkout/'leak').exists())
                finally:
                    shutil.rmtree(self.checkout/'leak', ignore_errors=True)

    def test_release_rejects_checkout_disclosure_at_every_level(self):
        build.one_case(str(self.root), self.row)
        for path in self.paths_into_checkout():
            for level in range(7):
                with self.subTest(path=path, level=level), mock.patch.object(release, 'copy_sources'):
                    try:
                        with self.assertRaises(ValueError):
                            release.export(self.root, self.row['id'], level, path)
                        self.assertFalse((self.checkout/'leak').exists())
                    finally:
                        shutil.rmtree(self.checkout/'leak', ignore_errors=True)

    def test_orphan_ciphertext_rebuilds_receipt_and_repeats_without_mutation(self):
        wire = o.execute(bytes.fromhex(self.row['message_hex']), ['B'], self.row['parameters'])
        path = self.root/'ciphertexts'/f"{self.row['id']}.bin"
        path.write_bytes(wire)
        stat = path.stat()
        receipt = build.one_case(str(self.root), self.row)
        self.assertEqual(receipt['status'], 'VERIFIED')
        self.assertTrue(receipt['fresh_receiver'])
        self.assertEqual(path.read_bytes(), wire)
        self.assertEqual((path.stat().st_ino, path.stat().st_mtime_ns), (stat.st_ino, stat.st_mtime_ns))
        self.assertEqual(build.one_case(str(self.root), self.row), receipt)

    def test_conflicting_orphan_is_not_overwritten_or_marked_failed(self):
        path = self.root/'ciphertexts'/f"{self.row['id']}.bin"
        path.write_bytes(b'conflicting evidence')
        with self.assertRaises(ValueError):
            build.one_case(str(self.root), self.row)
        self.assertEqual(path.read_bytes(), b'conflicting evidence')
        self.assertFalse((self.root/'receipts'/f"{self.row['id']}.json").exists())

    def test_all_entry_points_reject_private_checkout_alias(self):
        alias = self.base/'public-alias'
        alias.symlink_to(self.checkout, target_is_directory=True)
        for call in (lambda: build.generate(alias, 1), lambda: build.package(alias),
                     lambda: build.one_case(str(alias), self.row),
                     lambda: release.export(alias, self.row['id'], 0, self.base/'attempt'),
                     lambda: release.grade(alias, self.row['id'], self.base/'candidate')):
            with self.subTest(call=call), self.assertRaises(ValueError):
                call()
        self.assertEqual(list(self.checkout.iterdir()), [])

    def test_private_children_cannot_redirect_outside_archive(self):
        for name in ('private.json', 'ciphertexts', 'receipts', 'generation.json'):
            child = self.root/name
            held = self.root/(name+'.held')
            if child.exists():
                child.rename(held)
            for destination in (self.checkout/'stolen', self.base/'elsewhere'):
                child.symlink_to(destination, target_is_directory=True)
                try:
                    with self.subTest(name=name, destination=destination), self.assertRaises(ValueError):
                        build.one_case(str(self.root), self.row)
                    self.assertFalse(destination.exists())
                finally:
                    child.unlink()
            if held.exists():
                held.rename(child)

    def test_leaf_links_cannot_redirect_ciphertexts_or_receipts(self):
        for directory, extension in (('ciphertexts', 'bin'), ('receipts', 'json')):
            path = self.root/directory/f"{self.row['id']}.{extension}"
            path.symlink_to(self.checkout/'stolen')
            try:
                with self.subTest(directory=directory), self.assertRaises(ValueError):
                    build.one_case(str(self.root), self.row)
                self.assertFalse((self.checkout/'stolen').exists())
            finally:
                path.unlink()

    def test_release_preserves_refusal_of_internal_ciphertext_symlinks(self):
        build.one_case(str(self.root), self.row)
        path = self.root/'ciphertexts'/f"{self.row['id']}.bin"
        target = self.root/'held.bin'
        path.rename(target)
        path.symlink_to(target)
        with self.assertRaises(ValueError):
            release.export(self.root, self.row['id'], 0, self.base/'attempt')
        self.assertFalse((self.base/'attempt').exists())

    def test_harness_rejects_public_receipt_before_running(self):
        for path in self.paths_into_checkout():
            argv = ['test_harness.py', '--private', str(self.root), '--receipt', str(path)]
            with self.subTest(path=path), mock.patch.object(sys, 'argv', argv), \
                    mock.patch.object(harness.unittest.TextTestRunner, 'run') as run:
                with self.assertRaises(ValueError):
                    harness.main()
                run.assert_not_called()
                self.assertFalse((self.checkout/'leak').exists())

    def test_freeze_uses_canonical_path_after_alias_changes(self):
        outside = self.base/'outside'
        outside.mkdir()
        alias = self.base/'outside-alias'
        alias.symlink_to(outside, target_is_directory=True)
        def move_alias():
            alias.unlink()
            alias.symlink_to(self.checkout, target_is_directory=True)
            return []
        with mock.patch.object(matrix, 'schedules', side_effect=move_alias), contextlib.redirect_stdout(io.StringIO()):
            build.freeze(alias/'new')
        self.assertTrue((outside/'new'/'private.json').is_file())
        self.assertFalse((self.checkout/'new').exists())

    def test_case_id_traversal_is_rejected_without_writes(self):
        for case_id in ('../../escape', '/tmp/absolute', 'a'*15, 'G'*16):
            with self.subTest(case_id=case_id), self.assertRaises(ValueError):
                build.one_case(str(self.root), {**self.row, 'id': case_id})
        self.assertEqual(list((self.root/'receipts').iterdir()), [])
        self.assertEqual(list((self.root/'ciphertexts').iterdir()), [])

    def test_interruption_between_wire_and_receipt_is_resumable(self):
        original_save = build.save
        def interrupt_receipt(path, value):
            if Path(path).parent.name == 'receipts':
                raise KeyboardInterrupt('simulated interruption')
            original_save(path, value)
        with mock.patch.object(build, 'save', side_effect=interrupt_receipt):
            with self.assertRaises(KeyboardInterrupt):
                build.one_case(str(self.root), self.row)
        path = self.root/'ciphertexts'/f"{self.row['id']}.bin"
        wire = path.read_bytes()
        self.assertEqual(build.one_case(str(self.root), self.row)['status'], 'VERIFIED')
        self.assertEqual(path.read_bytes(), wire)

    def test_interrupted_atomic_publication_can_retry(self):
        path = self.root/'checkpoint.json'
        with mock.patch.object(build.os, 'link', side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                build.save(path, {'complete': True})
        self.assertFalse(path.exists())
        self.assertFalse(list(self.root.glob('.checkpoint.json.*')))
        build.save(path, {'complete': True})
        with self.assertRaises(FileExistsError):
            build.save(path, {'complete': False})
        self.assertEqual(json.loads(path.read_text()), {'complete': True})

    def test_existing_failed_or_malformed_receipt_is_not_overwritten(self):
        path = self.root/'receipts'/f"{self.row['id']}.json"
        for data in ('{"id":"0123456789abcdef","status":"FAILED"}', '{partial'):
            path.write_text(data)
            with self.subTest(data=data), self.assertRaises(ValueError):
                build.one_case(str(self.root), self.row)
            self.assertEqual(path.read_text(), data)

    def test_orphan_must_pass_fresh_receiver_check(self):
        wire = o.execute(bytes.fromhex(self.row['message_hex']), ['B'], self.row['parameters'])
        path = self.root/'ciphertexts'/f"{self.row['id']}.bin"
        path.write_bytes(wire)
        with mock.patch.object(build.subprocess, 'run', return_value=mock.Mock(returncode=1, stderr=b'refused')):
            self.assertEqual(build.one_case(str(self.root), self.row)['status'], 'FAILED')
        self.assertEqual(path.read_bytes(), wire)

    def test_generation_repeat_preserves_report_and_rejects_conflicts(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(build.generate(self.root, 1), 0)
            path = self.root/'generation.json'
            original = path.read_bytes()
            self.assertEqual(build.generate(self.root, 1), 0)
            self.assertEqual(path.read_bytes(), original)
            conflict = json.loads(original)
            conflict['verified'] = 0
            path.write_text(json.dumps(conflict))
            before = path.read_bytes()
            with self.assertRaises(ValueError):
                build.generate(self.root, 1)
            self.assertEqual(path.read_bytes(), before)


if __name__ == '__main__':
    unittest.main(verbosity=2)
# ratios: loc_comments=204:5 imports_exports=14:1 calls_definitions=130:19
