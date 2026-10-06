# === CHECKS ===
# id: native_closed_records_reject_forgery
#   proves: binary_sequence_closure, binary_coordinate_recovery
#   call: self::test_closed_table_rejects_order_source_and_definition_mutations
# id: native_modules_are_fresh
#   proves: binary_source_refusal, cycle_native_source_pinned
#   call: self::test_geometry_instances_ignore_mutated_earlier_modules
# id: output_write_failures_leave_no_partial_destination
#   proves: weave_output_atomic_no_clobber, cycle_strict_refusal
#   call: self::test_write_flush_and_close_failures_leave_no_partial_output
# id: empty_attachment_arguments_are_validated
#   proves: numeral_strict_input
#   call: self::test_empty_bind_rejects_invalid_attachments
# === END CHECKS ===
"""Regression replay: WEAVE_SOURCES=/checkouts python -m unittest discover -s tests -p test_cycle_repairs.py.

Temporary data only. These exercise genuine failure modes, not encryption claims.
"""
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from unittest.mock import patch
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest

import cycle
import cycle_native
import native_binary as native
import safe_output
from numeral import Refused

ROOT = Path(__file__).resolve().parents[1]
SOURCES = Path(os.environ['WEAVE_SOURCES'])
SPACES = tuple(Fraction(i,9) for i in range(8))


class CycleRepairTests(unittest.TestCase):
    def fixture(self):
        geometry = native.Geometry(SOURCES/'ucns')
        origin = native.ByteOrigin(b'ABxABy', 'repair', 0, geometry)
        return native.close_sequences(origin, (b'AB', b'x', b'y'), (0,1,0,2), (1,2,3), SPACES)

    def test_closed_table_rejects_order_source_and_definition_mutations(self):
        table = self.fixture()
        wrong_origin = native.ByteOrigin(b'ABxABy!', 'repair', 0, table.origin.geometry)
        changes = (dict(order=()), dict(order=(2,0,1,0)), dict(definitions=list(table.definitions)),
                   dict(definitions=table.definitions[:-1]), dict(origin=wrong_origin),
                   dict(spaces=(Fraction(0),)*8))
        for change in changes:
            with self.subTest(change=tuple(change)):
                with self.assertRaises(native.BinaryError): replace(table, **change)
        direct = native.SequenceTable(table.origin, table.definitions, table.order, table.spaces)
        self.assertEqual(direct.receipt(), table.receipt())

    def test_closed_table_rejects_native_axes_frames_and_occurrence_mutations(self):
        table = self.fixture()
        first = table.definitions[0]
        occurrence = first.occurrences[0]
        bad_occurrences = (
            replace(occurrence, ordinal=1),
            replace(occurrence, source_offset=1),
            replace(occurrence, circle=2),
            replace(occurrence, source_axis=table.origin.byte_axis(1)),
            replace(occurrence, source_state=occurrence.source_state.advance(1)),
            replace(occurrence, state=occurrence.state.advance(1)),
        )
        bad_definitions = [replace(first, occurrences=(o,)+first.occurrences[1:]) for o in bad_occurrences]
        bad_definitions += [replace(first, data=b'ZZ'), replace(first, state=first.state.advance(1)),
                            replace(first, attachment_axis=table.origin.byte_axis(1)),
                            replace(first, occurrences=first.occurrences[::-1])]
        for definition in bad_definitions:
            with self.assertRaises(native.BinaryError):
                replace(table, definitions=(definition,)+table.definitions[1:])

    def test_receipt_and_restore_recheck_even_bypassed_frozen_records(self):
        table = self.fixture()
        object.__setattr__(table, 'order', ())
        for operation in (table.restore, table.receipt, table.wire_occurrences):
            with self.assertRaises(native.BinaryError): operation()
        table = self.fixture()
        object.__setattr__(table.origin, '_identity', '0'*64)
        with self.assertRaises(native.BinaryError): table.receipt()

    def test_empty_and_invalid_native_record_types_refuse(self):
        table = self.fixture()
        definition = table.definitions[0]
        for changes in (dict(data=b''), dict(occurrences=()), dict(occurrences=[])):
            with self.assertRaises(native.BinaryError): replace(definition, **changes)
        for changes in (dict(circle=True), dict(circle=8), dict(ordinal=-1), dict(source_offset=True)):
            with self.assertRaises(native.BinaryError): replace(definition.occurrences[0], **changes)

    def test_geometry_instances_ignore_mutated_earlier_modules(self):
        first = native.Geometry(SOURCES/'ucns')
        first.axis_module.build_axis_circle_position = lambda **kw: 'not native'
        first.mobius_module.native_mobius_state = lambda *a,**kw: 'not native'
        poisoned = {'_uchc_ucns_'+sha: ModuleType('poison') for sha in native.UCNS_BLOBS.values()}
        with patch.dict(sys.modules, poisoned):
            second = native.Geometry(SOURCES/'ucns')
            axis = second.axis('0'*64, 8, 3)
            state = second.placed(axis,Fraction(1,7))
            self.assertEqual(type(axis).__name__, 'AxisCirclePosition')
            self.assertEqual(type(state).__name__, 'NativeMobiusState')
            self.assertEqual(axis.turn,Fraction(3,8))
        self.assertIsNot(first.axis_module, second.axis_module)

    def test_cycle_loads_fresh_candidate_and_has_no_uchc_runtime_dependency(self):
        api,geometry = cycle_native.load_native(SOURCES)
        api.close_sequences = lambda *a,**kw: 'poisoned candidate'
        geometry.axis_module.build_axis_circle_position = lambda **kw: 'poisoned geometry'
        with tempfile.TemporaryDirectory() as directory:
            src = Path(directory)
            (src/'ucns').symlink_to(SOURCES/'ucns',target_is_directory=True)
            newer,geom = cycle_native.load_native(src)
            origin = newer.ByteOrigin(b'ABAB','fresh',0,geom)
            self.assertEqual(newer.close_sequences(origin,(b'AB',),(0,0),(1,),SPACES).restore(),b'ABAB')
            self.assertIsNot(newer,api)
        self.assertFalse(any(name.startswith('_weave_binary_') or name.startswith('_weave_ucns_') for name in sys.modules))

    def test_write_success_is_owner_only_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'out'
            safe_output.write_new(path,b'complete')
            self.assertEqual(path.read_bytes(),b'complete')
            self.assertEqual(path.stat().st_mode & 0o777,0o600)
            with self.assertRaises(FileExistsError): safe_output.write_new(path,b'replace')
            self.assertEqual(path.read_bytes(),b'complete')
            self.assertEqual(list(Path(directory).iterdir()),[path])
            link=Path(directory)/'symlink'
            link.symlink_to(path)
            with self.assertRaises(FileExistsError): safe_output.write_new(link,b'replace')
            self.assertTrue(link.is_symlink())
            self.assertEqual(path.read_bytes(),b'complete')

    def test_write_flush_and_close_failures_leave_no_partial_output(self):
        original = os.fdopen
        class Broken:
            def __init__(self, fd, mode, stage): self.raw,self.stage=original(fd,mode),stage
            def __enter__(self): return self
            def write(self,data):
                if self.stage=='write':
                    self.raw.write(data[:2]); raise OSError('disk full')
                if self.stage=='short': return self.raw.write(data[:2])
                return self.raw.write(data)
            def flush(self):
                if self.stage=='flush': raise OSError('flush failure')
                self.raw.flush()
            def fileno(self): return self.raw.fileno()
            def __exit__(self,*args):
                self.raw.close()
                if self.stage=='close': raise OSError('close failure')
        for stage in ('write','short','flush','close','fsync'):
            with self.subTest(stage=stage),tempfile.TemporaryDirectory() as directory:
                path=Path(directory)/'out'
                with patch.object(safe_output.os,'fdopen',side_effect=lambda fd,mode:Broken(fd,mode,stage)):
                    cm=patch.object(safe_output.os,'fsync',side_effect=OSError('quota')) if stage=='fsync' else contextlib.nullcontext()
                    with cm,self.assertRaises(OSError): safe_output.write_new(path,b'complete record')
                self.assertFalse(path.exists())
                self.assertEqual(list(Path(directory).iterdir()),[])

    def test_atomic_install_failure_preserves_other_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); path=root/'out'; other=root/'other'; other.write_bytes(b'unchanged')
            with patch.object(safe_output.os,'link',side_effect=OSError('unsupported atomic link')):
                with self.assertRaises(OSError): safe_output.write_new(path,b'complete')
            self.assertEqual(list(root.iterdir()),[other])
            self.assertEqual(other.read_bytes(),b'unchanged')

    def test_cli_both_directions_refuse_failed_output_without_partial_files(self):
        for command in ('forward','reverse'):
            with tempfile.TemporaryDirectory() as directory:
                root=Path(directory); src=root/'input'; dst=root/'output'; corpus=root/'corpus'
                src.write_bytes(b'input');corpus.write_bytes(b'corpus')
                argv=['cycle.py',command,str(src),str(dst),'--corpus',str(corpus)]
                effect=(b'full record',{}) if command=='forward' else b'restored'
                with patch.object(sys,'argv',argv),patch.object(cycle,command,return_value=effect):
                    with patch.object(safe_output.os,'fsync',side_effect=OSError('quota')):
                        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit) as failure: cycle.main()
                self.assertEqual(failure.exception.code,2)
                self.assertFalse(dst.exists())
                self.assertEqual({p.name for p in root.iterdir()},{'input','corpus'})

    def test_empty_bind_rejects_invalid_attachments(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);src=root/'empty';src.write_bytes(b'')
            for angle,circle in (('99','1'),('1/7','999'),('99','999'),('-1','2')):
                out=root/'record'
                run=subprocess.run([sys.executable,str(ROOT/'numeral.py'),'bind',str(src),str(out),
                    '--origin','empty','--angle',angle,'--circle',circle],capture_output=True)
                self.assertEqual(run.returncode,2,run.stderr)
                self.assertNotIn(b'Traceback',run.stderr)
                self.assertFalse(out.exists())
            run=subprocess.run([sys.executable,str(ROOT/'numeral.py'),'bind',str(src),str(root/'valid'),
                '--origin','empty','--angle','1/7','--circle','3'],capture_output=True)
            self.assertEqual(run.returncode,0,run.stderr)

    def test_native_edges_and_forge_ownership_match_root_manifest(self):
        manifest=json.loads((ROOT.parents[1]/'stack-manifest.json').read_text())
        human=(ROOT.parents[1]/'STACK_MANIFEST.md').read_text()
        lock=json.loads((ROOT/'CYCLE_NATIVE.json').read_text())
        participants={p['participant_id']:p for p in manifest['research_participants'] if p['workspace']=='research/weave/'}
        self.assertEqual(participants['weave-ucns-geometry']['commit'],lock['ucns_commit'])
        self.assertEqual(participants['weave-uchc-architecture']['commit'],lock['uchc_architecture']['commit'])
        self.assertIn('Stack-owned binary',participants['weave']['relation'])
        self.assertIn('native_binary.py',human)
        self.assertNotIn('uchc_source',lock)


if __name__=='__main__': unittest.main()
