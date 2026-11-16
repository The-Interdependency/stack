# ratios: loc_comments=129:38 imports_exports=19:1 calls_definitions=73:7
"""Frozen-source replay, refusal and standalone-export witnesses.

Usage: python test_source_snapshot.py. No original operator archive is needed.
The nine synthetic vectors were sealed using the unchanged #94 adapters in a
temporary checkout containing every original SOURCE.json byte. They establish
source/replay compatibility, not attacker recovery or cryptographic security.
"""
from pathlib import Path
from hashlib import sha256
from unittest import mock
import copy
import io
import json
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import warnings
import zipfile
import operations as o
import build
import release
import transport_cases as transport

# === CHECKS ===
# id: frozen_source_checkout_independence
#   proves: weave_challenge_frozen_source_closure
#   call: self::FrozenSources.test_checkout_drift_does_not_select_algorithm_bytes
#   mutates: temporary directory
#   cleanup: TemporaryDirectory
# id: frozen_source_original_vector_replay
#   proves: weave_challenge_frozen_source_closure, exact_operations, receiver_inputs_only
#   call: self::FrozenSources.test_original_adapter_vectors_replay_in_both_directions
#   mutates: none
#   cleanup: none
# id: frozen_source_standalone_receiver
#   proves: weave_challenge_frozen_source_closure, staged_disclosure
#   call: self::FrozenSources.test_exported_receivers_run_without_git_or_native_checkouts
#   mutates: temporary directory
#   cleanup: TemporaryDirectory
# id: frozen_source_refusals
#   proves: weave_challenge_frozen_source_refusal
#   call: self::FrozenSources.test_archive_and_metadata_mutations_refuse
#   mutates: temporary directory
#   cleanup: TemporaryDirectory
# id: frozen_source_import_boundary
#   proves: weave_challenge_frozen_source_refusal
#   call: self::FrozenSources.test_conflicting_import_cache_refuses_and_bytecode_is_ignored
#   mutates: temporary directory
#   cleanup: TemporaryDirectory
# === END CHECKS ===


class FrozenSources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vectors = json.loads((o.HERE / 'SOURCE_REPLAY_VECTORS.json').read_text())['vectors']
        if len(cls.vectors) != 9:
            raise ValueError('the sealed nine-vector census must remain complete')

    def test_checkout_drift_does_not_select_algorithm_bytes(self):
        with tempfile.TemporaryDirectory() as directory, mock.patch.object(o, 'CHECKOUT', Path(directory)):
            self.assertEqual(o.verify_sources(), 61)
            self.assertNotEqual(o.FROZEN_ROOT, o.CHECKOUT)
            self.assertFalse((o.CHECKOUT / 'sources').exists())
        for name in ('cycle', 'numeral', 'prime_schedule'):
            module = sys.modules[name]
            self.assertTrue(Path(module.__file__).is_relative_to(o.FROZEN_ROOT))
            key = Path(module.__file__).relative_to(o.FROZEN_ROOT).as_posix()
            self.assertEqual(module.__source_sha256__, sha256(o.SNAPSHOT.files[key]).hexdigest())

    def test_original_adapter_vectors_replay_in_both_directions(self):
        for row in self.vectors:
            with self.subTest(family=row['family'], schedule=row['schedule']):
                raw, expected = bytes.fromhex(row['input_hex']), bytes.fromhex(row['wire_hex'])
                if row['family'] == 'cycle':
                    actual, _ = o.cycle.forward(raw, bytes.fromhex(row['parameters']['corpus_hex']),
                                               o.profile(row['parameters']), o.SOURCES)
                elif row['family'] == 'transport':
                    actual = transport.run(raw, row['schedule'], row['parameters'])
                else:
                    actual = o.execute(raw, row['schedule'], row['parameters'])
                self.assertEqual(actual, expected)
                request = {key: row[key] for key in ('family', 'schedule', 'parameters', 'wire_hex')}
                self.assertEqual(o.receive(request), raw)

    def test_exported_receivers_run_without_git_or_native_checkouts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            operator = root / 'operator'
            operator.mkdir(mode=0o700)
            (operator / 'ciphertexts').mkdir()
            rows = [{**row, 'id': f'{index:016x}', 'message_hex': row['input_hex']}
                    for index, row in enumerate(self.vectors)]
            build.save(operator / 'private.json', {'cases': rows})
            for row in rows:
                with self.subTest(family=row['family'], schedule=row['schedule']):
                    (operator / 'ciphertexts' / (row['id'] + '.bin')).write_bytes(bytes.fromhex(row['wire_hex']))
                    out = release.export(operator, row['id'], 6, root / ('attempt-' + row['id']))
                    script = out / 'source/research/weave/recovery-challenges/v2/operations.py'
                    result = subprocess.run([sys.executable, '-I', '-B', str(script), 'receive',
                                             '--request', str(out / 'request.json'),
                                             '--output', str(out / 'restored.bin')],
                                            cwd=root, capture_output=True, text=True, timeout=30)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual((out / 'restored.bin').read_bytes(), bytes.fromhex(row['input_hex']))
                    self.assertTrue(release.grade(operator, row['id'], out / 'restored.bin')['exact'])
                    self.assertFalse((out / 'source/.git').exists())
                    request = json.loads((out / 'request.json').read_text())
                    self.assertEqual(set(request), {'family', 'schedule', 'parameters', 'wire_hex'})

    def test_archive_and_metadata_mutations_refuse(self):
        with zipfile.ZipFile(o.HERE / 'frozen-sources.zip') as archive:
            original = [(entry, archive.read(entry)) for entry in archive.infolist()]
        for mutation in ('alter', 'missing', 'duplicate', 'unexpected', 'symlink', 'escape', 'duplicate_json'):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as directory:
                here = Path(directory)
                for name in ('SOURCE.json', 'SOURCE_BUNDLE.json', 'frozen-sources.zip'):
                    shutil.copyfile(o.HERE / name, here / name)
                entries = [(copy.copy(entry), data) for entry, data in original]
                if mutation == 'alter':
                    entries[0] = (entries[0][0], entries[0][1] + b'altered')
                elif mutation == 'missing':
                    entries.pop()
                elif mutation == 'duplicate':
                    entries.append(entries[0])
                elif mutation == 'unexpected':
                    entries.append((zipfile.ZipInfo('private.json'), b'not admitted'))
                elif mutation == 'symlink':
                    entries[0][0].external_attr = (stat.S_IFLNK | 0o777) << 16
                elif mutation == 'escape':
                    lock = json.loads((here / 'SOURCE.json').read_text())
                    lock['files'][0]['path'] = '../escaped'
                    (here / 'SOURCE.json').write_text(json.dumps(lock))
                elif mutation == 'duplicate_json':
                    text = (here / 'SOURCE.json').read_text()
                    (here / 'SOURCE.json').write_text(text.replace('{', '{"stack_commit":"' + '0' * 40 + '",', 1))
                memory = io.BytesIO()
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore', UserWarning)
                    with zipfile.ZipFile(memory, 'w') as archive:
                        for entry, data in entries:
                            archive.writestr(entry, data)
                (here / 'frozen-sources.zip').write_bytes(memory.getvalue())
                metadata = json.loads((here / 'SOURCE_BUNDLE.json').read_text())
                metadata['archive_sha256'] = sha256(memory.getvalue()).hexdigest()
                metadata['source_lock_sha256'] = sha256((here / 'SOURCE.json').read_bytes()).hexdigest()
                (here / 'SOURCE_BUNDLE.json').write_text(json.dumps(metadata))
                with self.assertRaises((ValueError, zipfile.BadZipFile)):
                    snapshot = o._loader.load_snapshot(here)
                    snapshot.close()

    def test_conflicting_import_cache_refuses_and_bytecode_is_ignored(self):
        preface = 'import sys\nsys.path.insert(0, ' + repr(str(o.HERE)) + ')\n'
        poison = preface + 'from types import ModuleType\nsys.modules["cycle"]=ModuleType("cycle")\nimport operations\n'
        result = subprocess.run([sys.executable, '-I', '-B', '-c', poison], capture_output=True, text=True, timeout=30)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('cached module is outside frozen source: cycle', result.stderr)
        source = preface + '''import importlib, importlib.util, py_compile
import operations as o
path=o.WEAVE/'prime_schedule.py'
poison=o.FROZEN_ROOT/'poison.py'
poison.write_text("raise RuntimeError('unchecked bytecode executed')\\n")
cached=importlib.util.cache_from_source(str(path))
py_compile.compile(str(poison),cfile=cached,invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH)
del sys.modules['prime_schedule']
module=importlib.import_module('prime_schedule')
assert hasattr(module,'Route')
assert module.__source_sha256__ == o.prime.__source_sha256__
'''
        result = subprocess.run([sys.executable, '-I', '-B', '-c', source], capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
# ratios: loc_comments=129:38 imports_exports=19:1 calls_definitions=73:7
