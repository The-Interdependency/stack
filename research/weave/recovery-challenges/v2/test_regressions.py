# ratios: loc_comments=389:54 imports_exports=17:1 calls_definitions=257:28
"""PR #94 integrity regressions, using synthetic private fixtures only.

Run from any directory: python research/weave/recovery-challenges/v2/test_regressions.py
No operator archive or attacker answers are needed. Temporary checkouts witness
rejected disclosure; receiver subprocesses exercise the actual frozen algorithms.
"""
from pathlib import Path
from unittest import mock
import contextlib
import copy
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

# === CHECKS ===
# id: publication_verified_wire_buffer
#   proves: complete_publication_census, frozen_case_checkpoint_binding, separated_artifacts
#   call: self::Integrity.test_package_writes_the_verified_wire_buffer
#   mutates: temporary operator and publication fixtures
#   cleanup: TemporaryDirectory
# id: full_matrix_publication_census
#   proves: complete_publication_census, declared_census
#   call: self::Integrity.test_publication_requires_exact_matrix_and_controls
#   mutates: synthetic in-memory plan only
#   cleanup: none
# id: incomplete_publication_refusal
#   proves: complete_publication_census, separated_artifacts
#   call: self::Integrity.test_package_refuses_verified_subset_before_publication
#   mutates: temporary operator fixture
#   cleanup: TemporaryDirectory
# id: checkpoint_release_wire_binding
#   proves: frozen_case_checkpoint_binding, staged_disclosure, exact_grading
#   call: self::Integrity.test_release_and_grade_require_current_ciphertext_binding
#   mutates: temporary operator fixture
#   cleanup: TemporaryDirectory
# id: checkpoint_release_verified_buffer
#   proves: frozen_case_checkpoint_binding, staged_disclosure
#   call: self::Integrity.test_release_uses_verified_wire_buffer
#   mutates: temporary operator fixture
#   cleanup: TemporaryDirectory
# id: checkpoint_frozen_row_binding
#   proves: frozen_case_checkpoint_binding
#   call: self::Integrity.test_changed_case_inputs_cannot_reuse_or_publish_checkpoint
#   mutates: temporary operator fixture
#   cleanup: TemporaryDirectory
# id: checkpoint_legacy_binding_refusal
#   proves: frozen_case_checkpoint_binding
#   call: self::Integrity.test_unbound_or_mismatched_receipts_are_preserved_and_refused
#   mutates: temporary operator fixture
#   cleanup: TemporaryDirectory
# id: checkpoint_plan_census
#   proves: frozen_case_checkpoint_binding
#   call: self::Integrity.test_duplicate_or_empty_plans_refuse_before_generation_or_publication
#   mutates: temporary operator fixture
#   cleanup: TemporaryDirectory
# id: checkpoint_legacy_separate_reverification
#   proves: frozen_case_checkpoint_binding
#   call: self::Integrity.test_legacy_evidence_can_be_reverified_in_separate_archive
#   mutates: temporary operator fixtures
#   cleanup: TemporaryDirectory
# === END CHECKS ===


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

    def test_changed_case_inputs_cannot_reuse_or_publish_checkpoint(self):
        receipt = build.one_case(str(self.root), self.row)
        self.assertEqual(receipt['case_sha256'], build.case_digest(self.row))
        wire = self.root/'ciphertexts'/f"{self.row['id']}.bin"
        checkpoint = self.root/'receipts'/f"{self.row['id']}.json"
        original = (wire.read_bytes(), checkpoint.read_bytes(), wire.stat().st_mtime_ns,
                    checkpoint.stat().st_mtime_ns)
        (self.root/'generation.json').write_text(json.dumps({'planned': 1, 'verified': 1, 'failures': []}))
        for field in ('message_hex', 'schedule', 'parameters', 'family'):
            changed = copy.deepcopy(self.row)
            if field == 'message_hex':
                changed[field] = b'changed answer with unchanged ciphertext'.hex()
            elif field == 'schedule':
                changed[field] = ['W']
            elif field == 'parameters':
                changed[field]['corpus_hex'] = '00'
            else:
                changed[field] = 'transport'
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, 'checkpoint invalid'):
                    build.one_case(str(self.root), changed)
                (self.root/'private.json').write_text(json.dumps({'cases': [changed]}))
                with mock.patch.object(build.zipfile, 'ZipFile') as publish:
                    with self.assertRaisesRegex(ValueError, 'checkpoint invalid'):
                        build.package(self.root)
                    publish.assert_not_called()
                candidate = self.base/'candidate.bin'
                candidate.write_bytes(bytes.fromhex(self.row['message_hex']))
                for level in range(7):
                    out = self.base/f'rejected-{field}-{level}'
                    with self.assertRaisesRegex(ValueError, 'checkpoint invalid'):
                        release.export(self.root, self.row['id'], level, out)
                    self.assertFalse(out.exists())
                with self.assertRaisesRegex(ValueError, 'checkpoint invalid'):
                    release.grade(self.root, self.row['id'], candidate)
                self.assertEqual((wire.read_bytes(), checkpoint.read_bytes(), wire.stat().st_mtime_ns,
                                  checkpoint.stat().st_mtime_ns), original)
        self.assertEqual(build.one_case(str(self.root), copy.deepcopy(self.row)), receipt)

    def test_unbound_or_mismatched_receipts_are_preserved_and_refused(self):
        receipt = build.one_case(str(self.root), self.row)
        checkpoint = self.root/'receipts'/f"{self.row['id']}.json"
        (self.root/'generation.json').write_text(json.dumps({'planned': 1, 'verified': 1, 'failures': []}))
        for field in ('schema', 'case_sha256', 'wire_bytes', 'message_bytes', 'fresh_receiver'):
            changed = dict(receipt)
            changed.pop(field)
            data = json.dumps(changed).encode()
            checkpoint.write_bytes(data)
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, 'checkpoint invalid'):
                    build.one_case(str(self.root), self.row)
                with mock.patch.object(build.zipfile, 'ZipFile') as publish:
                    with self.assertRaisesRegex(ValueError, 'checkpoint invalid'):
                        build.package(self.root)
                    publish.assert_not_called()
                self.assertEqual(checkpoint.read_bytes(), data)

    def test_release_and_grade_require_current_ciphertext_binding(self):
        build.one_case(str(self.root), self.row)
        wire = self.root/'ciphertexts'/f"{self.row['id']}.bin"
        original = wire.read_bytes()
        candidate = self.base/'candidate.bin'
        candidate.write_bytes(bytes.fromhex(self.row['message_hex']))
        self.assertTrue(release.grade(self.root, self.row['id'], candidate)['exact'])
        wire.write_bytes(bytes([original[0] ^ 1]) + original[1:])
        corrupted = wire.read_bytes()
        for level in range(7):
            out = self.base/f'rejected-wire-{level}'
            with self.subTest(level=level), self.assertRaisesRegex(ValueError, 'checkpoint invalid'):
                release.export(self.root, self.row['id'], level, out)
            self.assertFalse(out.exists())
        with self.assertRaisesRegex(ValueError, 'checkpoint invalid'):
            release.grade(self.root, self.row['id'], candidate)
        self.assertEqual(wire.read_bytes(), corrupted)

    def test_release_uses_verified_wire_buffer(self):
        build.one_case(str(self.root), self.row)
        path = self.root/'ciphertexts'/f"{self.row['id']}.bin"
        original = path.read_bytes()
        checked = build.load_verified_case
        def checked_then_changed(root, row):
            snapshot = checked(root, row)
            path.write_bytes(b'changed after the checked buffer was captured')
            return snapshot
        with mock.patch.object(build, 'load_verified_case', side_effect=checked_then_changed):
            out = release.export(self.root, self.row['id'], 6, self.base/'admitted-snapshot')
        self.assertEqual((out/'challenge.bin').read_bytes(), original)
        self.assertEqual(json.loads((out/'request.json').read_text())['wire_hex'], original.hex())

    def test_publication_requires_exact_matrix_and_controls(self):
        rows = [{**row, 'id': f'{index:016x}', 'message_hex': '', 'parameters': {
                    'initial_lanes': row.get('initial_lanes', 1),
                    'rounds': [{} for _ in range(row.get('round_count', 1))]}}
                for index, row in enumerate(matrix.schedules())]
        self.assertEqual(len(rows), 1841)
        plan = {'schema': 'weave.recovery-private/v2', 'cases': rows,
                'prediction_status': 'FROZEN_BEFORE_ENCODING_AND_ATTACKS', 'salt': 'ab'*32}
        build.validate_publication_plan(plan)
        build.validate_publication_plan({**plan, 'cases': list(reversed(rows))})
        same_family_substitution = copy.deepcopy(rows)
        same_family_substitution[1] = {**same_family_substitution[0], 'id': rows[1]['id']}
        variants = [rows[:-1], [rows[0]], rows + [rows[0]], rows[:-1] + [rows[0]],
                    same_family_substitution]
        for changed in variants:
            with self.subTest(cases=len(changed)), self.assertRaisesRegex(ValueError, 'complete matrix census'):
                build.validate_publication_plan({**plan, 'cases': changed})
        for family, control in (('transport', 'initial_lanes'), ('cycle', 'rounds')):
            changed = copy.deepcopy(plan)
            row = next(row for row in changed['cases'] if row['family'] == family)
            row['parameters'][control] = 2 if family == 'transport' else []
            with self.subTest(family=family), self.assertRaisesRegex(ValueError, 'controls disagree'):
                build.validate_publication_plan(changed)
        for field in ('schema', 'prediction_status', 'salt'):
            changed = {**plan, field: 'invalid'}
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'publication metadata'):
                build.validate_publication_plan(changed)

    def test_package_refuses_verified_subset_before_publication(self):
        build.one_case(str(self.root), self.row)
        (self.root/'generation.json').write_text(json.dumps({'planned': 1, 'verified': 1, 'failures': []}))
        originals = {path: (path.read_bytes(), path.stat().st_mtime_ns)
                     for path in self.root.rglob('*') if path.is_file()}
        with mock.patch.object(build.zipfile, 'ZipFile') as publish:
            with self.assertRaisesRegex(ValueError, 'complete matrix census'):
                build.package(self.root)
            publish.assert_not_called()
        self.assertEqual({path: (path.read_bytes(), path.stat().st_mtime_ns)
                          for path in self.root.rglob('*') if path.is_file()}, originals)

    def test_package_writes_the_verified_wire_buffer(self):
        build.one_case(str(self.root), self.row)
        (self.root/'generation.json').write_text(json.dumps({'planned': 1, 'verified': 1, 'failures': []}))
        wire_path = self.root/'ciphertexts'/f"{self.row['id']}.bin"
        original = wire_path.read_bytes()
        output = self.checkout/'new-publication'
        output.mkdir()
        checked = build.load_verified_case
        calls = 0
        def checked_then_changed(root, row):
            nonlocal calls
            calls += 1
            admitted = checked(root, row)
            if calls == 2:
                wire_path.write_bytes(b'changed after publication buffer validation')
            return admitted
        # Census admission is tested independently above; isolate byte emission
        # here without claiming a new full-corpus recovery from this tiny fixture.
        with mock.patch.object(build, 'validate_publication_plan'), \
                mock.patch.object(build, 'load_verified_case', side_effect=checked_then_changed), \
                mock.patch.object(o, 'HERE', output), contextlib.redirect_stdout(io.StringIO()):
            build.package(self.root)
        self.assertEqual(calls, 2)
        import hashlib
        import zipfile
        with zipfile.ZipFile(output/'blind-pack.zip') as archive:
            name = 'files/'+self.row['id']+'.bin'
            self.assertEqual(archive.read(name), original)
            self.assertEqual(archive.read('SHA256SUMS').decode().strip(),
                             hashlib.sha256(original).hexdigest()+'  '+name)

    def test_duplicate_or_empty_plans_refuse_before_generation_or_publication(self):
        for rows in ([], [self.row, self.row], [{**self.row, 'id': '../escape'}]):
            (self.root/'private.json').write_text(json.dumps({'cases': rows}))
            with self.subTest(rows=len(rows)), mock.patch.object(build, 'ProcessPoolExecutor') as pool, \
                    mock.patch.object(build.zipfile, 'ZipFile') as publish:
                with self.assertRaises(ValueError):
                    build.generate(self.root, 1)
                with self.assertRaises(ValueError):
                    build.package(self.root)
                pool.assert_not_called()
                publish.assert_not_called()
        self.assertEqual(list((self.root/'receipts').iterdir()), [])

    def test_legacy_evidence_can_be_reverified_in_separate_archive(self):
        receipt = build.one_case(str(self.root), self.row)
        receipt.pop('schema')
        receipt.pop('case_sha256')
        checkpoint = self.root/'receipts'/f"{self.row['id']}.json"
        checkpoint.write_text(json.dumps(receipt))
        wire = self.root/'ciphertexts'/f"{self.row['id']}.bin"
        before = (checkpoint.read_bytes(), wire.read_bytes(), checkpoint.stat().st_mtime_ns,
                  wire.stat().st_mtime_ns, wire.stat().st_ino)
        new = self.base/'reverified'
        new.mkdir(mode=0o700)
        (new/'receipts').mkdir(mode=0o700)
        shutil.copyfile(self.root/'private.json', new/'private.json')
        shutil.copytree(self.root/'ciphertexts', new/'ciphertexts', symlinks=True)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(build.generate(new, 1), 0)
        checked = build.checked_checkpoint(new, self.row)
        self.assertEqual(checked['case_sha256'], build.case_digest(self.row))
        self.assertEqual((new/'ciphertexts'/wire.name).read_bytes(), wire.read_bytes())
        self.assertEqual((checkpoint.read_bytes(), wire.read_bytes(), checkpoint.stat().st_mtime_ns,
                          wire.stat().st_mtime_ns, wire.stat().st_ino), before)


if __name__ == '__main__':
    unittest.main(verbosity=2)
# ratios: loc_comments=389:54 imports_exports=17:1 calls_definitions=257:28
