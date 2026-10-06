# === CHECKS ===
# id: review_accounting_one_replay
#   proves: numeral_strict_input, numeral_accounting
#   call: self::test_accounting_reuses_the_single_validation
#   mutates: none
#   cleanup: none
# id: review_cli_aggregate_budget
#   proves: numeral_strict_input
#   call: self::test_cli_shares_prime_budget_through_inspect_and_recover
#   mutates: filesystem
#   cleanup: tempdir_teardown
# id: review_closure_owner
#   proves: discovery_closure_authority
#   call: self::test_discovery_documentation_preserves_closure_owner
#   mutates: none
#   cleanup: none
# id: review_native_objects_no_spoof
#   proves: binary_sequence_closure, binary_source_refusal
#   call: self::test_all_native_record_slots_reject_equality_spoofs
#   mutates: none
#   cleanup: none
# id: review_native_fields_no_spoof
#   proves: binary_sequence_closure, binary_source_refusal
#   call: self::test_native_scalar_fields_reject_spoofs_and_subclasses
#   mutates: none
#   cleanup: none
# id: review_native_geometry_instance
#   proves: binary_sequence_closure, binary_source_refusal
#   call: self::test_records_from_another_geometry_instance_are_not_substituted
#   mutates: none
#   cleanup: none
# id: review_native_export_revalidation
#   proves: binary_sequence_closure, binary_coordinate_recovery
#   call: self::test_all_export_paths_reject_bypassed_frozen_spoofs
#   mutates: none
#   cleanup: none
# id: review_decode_discovery_identity
#   proves: cycle_discovery_profile
#   call: self::test_unaffix_rejects_valid_alternate_partitions
#   mutates: none
#   cleanup: none
# id: review_reverse_discovery_identity
#   proves: cycle_discovery_profile
#   call: self::test_whole_cycle_reverse_rejects_alternate_selection
#   mutates: none
#   cleanup: none
# id: review_discovery_roundtrip
#   proves: cycle_discovery_profile, cycle_reversible_rounds
#   call: self::test_canonical_discovery_records_still_recover
#   mutates: none
#   cleanup: none
# id: review_inverse_discovery_budget
#   proves: cycle_discovery_profile, discovery_resource_refusal
#   call: self::test_inverse_discovery_honors_the_visit_budget
#   mutates: none
#   cleanup: none
# === END CHECKS ===
"""PR #77 final-review regressions, not cryptographic-strength tests.

Usage: WEAVE_SOURCES=/checkouts python -m unittest discover -s tests -p test_review_closure.py -v
Only temporary files are written. The original profile, UCNS geometry and wire
representation remain unchanged; invalid native records/false profile claims fail.
"""
from copy import copy
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import contextlib
import io
import os
import sys
import tempfile
import unittest

import affixiation
import cycle
import native_binary as native
import numeral
from affixiation import Partition, discover
from numeral import BitBlock, Entry, Packet, PrimePath, Limits, Refused, ResourceLimit

ROOT = Path(__file__).resolve().parents[1]
SOURCES = Path(os.environ['WEAVE_SOURCES'])
PROFILE = cycle.Profile.read((ROOT/'profiles/cycle-v1.json').read_bytes())
SPACES = tuple(Fraction(i, 9) for i in range(8))


class EqualitySpoof:
    calls = 0

    def __eq__(self, other):
        type(self).calls += 1
        return True

    def __ne__(self, other):
        type(self).calls += 1
        return False


class FractionSpoof(Fraction):
    def __eq__(self, other):
        return True

    def __ne__(self, other):
        type(self).calls += 1
        return False


class ReviewClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.geometry = native.Geometry(SOURCES/'ucns')

    def fixture(self):
        origin = native.ByteOrigin(b'ABxABy', 'review', 0, self.geometry)
        return native.close_sequences(origin, (b'AB', b'x', b'y'), (0,1,0,2), (1,2,3), SPACES)

    def recipe_packet(self):
        symbol = chr(0xE000)
        return Packet('budget', 0, (Entry(symbol, BitBlock(101,16), Fraction(1,7),
                                            1, PrimePath(101,())),), symbol)

    def test_accounting_reuses_the_single_validation(self):
        packet = self.recipe_packet()
        seen = []
        replay = PrimePath.replay
        def record(path, *args, **kwargs):
            seen.append(path)
            return replay(path, *args, **kwargs)
        with patch.object(PrimePath, 'replay', record):
            stats = numeral.accounting(packet, Limits(prime_work=5))
        self.assertEqual(len(seen), 1, 'accounting repeated the recipe validation')
        self.assertEqual(stats['source_bits'], 16)
        self.assertEqual(stats['total_bytes'], len(numeral.encode(packet)))
        with self.assertRaises(ResourceLimit):
            numeral.accounting(packet, Limits(prime_work=4))

    def test_cli_shares_prime_budget_through_inspect_and_recover(self):
        wire = numeral.encode(self.recipe_packet())
        # Decode charges 10, accounting 5, and restore a further 5 work units.
        for command, minimum in (('inspect',15), ('recover',20)):
            for budget, success in ((minimum-1,False), (minimum,True)):
                with self.subTest(command=command,budget=budget), tempfile.TemporaryDirectory() as directory:
                    root=Path(directory); src=root/'record'; dst=root/'out'; src.write_bytes(wire)
                    argv=['numeral.py',command,str(src)] + ([str(dst)] if command=='recover' else [])
                    with patch.object(sys,'argv',argv), patch.object(numeral,'Limits',return_value=Limits(prime_work=budget)):
                        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                            if success:
                                self.assertEqual(numeral.main(),0)
                            else:
                                with self.assertRaises(SystemExit) as failure:
                                    numeral.main()
                                self.assertEqual(failure.exception.code,2)
                    if command=='recover' and success:
                        self.assertEqual(dst.read_bytes(),b'\x00e')
                    else:
                        self.assertFalse(dst.exists())

    def test_discovery_documentation_preserves_closure_owner(self):
        self.assertNotIn('UCHC closes', affixiation.__doc__)
        self.assertIn('Stack-owned', affixiation.__doc__)
        self.assertIn('native_binary.py', affixiation.__doc__)
        self.assertIn('UCNS geometry', affixiation.__doc__)

    def test_all_native_record_slots_reject_equality_spoofs(self):
        for target, fields in (('definition',('attachment_axis','state')),
                               ('occurrence',('source_axis','circle_axis','state','source_state'))):
            for field in fields:
                with self.subTest(target=target,field=field):
                    table=self.fixture(); first=table.definitions[0]; EqualitySpoof.calls=0
                    if target=='definition':
                        forged=replace(first, **{field:EqualitySpoof()})
                    else:
                        occurrence=replace(first.occurrences[0], **{field:EqualitySpoof()})
                        forged=replace(first,occurrences=(occurrence,)+first.occurrences[1:])
                    with self.assertRaises(native.BinaryError):
                        replace(table,definitions=(forged,)+table.definitions[1:])
                    self.assertEqual(EqualitySpoof.calls,0,'untrusted equality was invoked')

    def test_native_scalar_fields_reject_spoofs_and_subclasses(self):
        cases=(('attachment_axis','origin_sha256',EqualitySpoof()),
               ('attachment_axis','identity_sha256',EqualitySpoof()),
               ('attachment_axis','axis_count',EqualitySpoof()),
               ('attachment_axis','axis_ordinal',EqualitySpoof()),
               ('attachment_axis','turn',FractionSpoof(0)),
               ('state','phase_turns',FractionSpoof(0)),
               ('state','frame',EqualitySpoof()))
        for slot, field, value in cases:
            with self.subTest(slot=slot,field=field):
                table=self.fixture(); first=table.definitions[0]
                forged=copy(getattr(first,slot)); object.__setattr__(forged,field,value)
                changed=replace(first,**{slot:forged})
                with self.assertRaises(native.BinaryError):
                    replace(table,definitions=(changed,)+table.definitions[1:])

    def test_records_from_another_geometry_instance_are_not_substituted(self):
        table=self.fixture(); first=table.definitions[0]
        other=native.Geometry(SOURCES/'ucns')
        axis=other.axis(table.origin.identity,len(table.origin.source),0)
        with self.assertRaises(native.BinaryError):
            replace(table,definitions=(replace(first,attachment_axis=axis),)+table.definitions[1:])
        self.assertEqual(table.restore(),b'ABxABy')

    def test_all_export_paths_reject_bypassed_frozen_spoofs(self):
        for method in ('restore','receipt','wire_occurrences'):
            with self.subTest(method=method):
                table=self.fixture()
                object.__setattr__(table.definitions[0],'attachment_axis',EqualitySpoof())
                with self.assertRaises(native.BinaryError): getattr(table,method)()

    def native_args(self, source):
        return dict(api=native,geometry=self.geometry,scope=PROFILE.scope,
                    root=native.ByteOrigin(source,PROFILE.scope,0,self.geometry).message_origin,
                    round_id=0,spec=PROFILE.rounds[0])

    def test_unaffix_rejects_valid_alternate_partitions(self):
        source=b'ABxABy'; canonical=discover(source)
        alternatives=(Partition((b'A',b'B',b'x',b'y'),(0,1,2,0,1,3),tuple(range(6)),0),
                      Partition((b'x',b'AB',b'y'),(1,0,1,2),(0,2,3,5),0),
                      Partition((source,),(0,),(0,),0))
        for alternative in alternatives:
            self.assertEqual(alternative.restore(),source)
            self.assertNotEqual((alternative.blocks,alternative.order),(canonical.blocks,canonical.order))
            with patch.object(cycle,'discover',return_value=alternative):
                wire,_=cycle.affix(source,**self.native_args(source))
            with self.assertRaisesRegex(Refused,'discovery profile'):
                cycle.unaffix(wire,**self.native_args(source))

    def test_whole_cycle_reverse_rejects_alternate_selection(self):
        profile=replace(PROFILE,rounds=PROFILE.rounds[:1])
        def single_literal(data,**kwargs):
            return Partition((data,),(0,),(0,),0)
        with patch.object(cycle,'discover',side_effect=single_literal):
            wire,_=cycle.forward(b'ABABABAB',b'corpus',profile,SOURCES)
        with self.assertRaisesRegex(Refused,'discovery profile'):
            cycle.reverse(wire,b'corpus',profile,SOURCES)

    def test_canonical_discovery_records_still_recover(self):
        for source in (b'',b'x',b'ABxABy',b'AAAAA',b'banana bandana banana',bytes(range(256))):
            with self.subTest(length=len(source)):
                wire,_=cycle.affix(source,**self.native_args(source))
                self.assertEqual(cycle.unaffix(wire,**self.native_args(source)),source)

    def test_inverse_discovery_honors_the_visit_budget(self):
        source=b'ABABABAB'; args=self.native_args(source)
        wire,_=cycle.affix(source,**args)
        with self.assertRaises(ResourceLimit):
            cycle.unaffix(wire,**args,limits=cycle.CycleLimits(discovery_visits=1))


if __name__=='__main__': unittest.main()
