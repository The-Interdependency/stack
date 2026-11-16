# === CHECKS ===
# id: byte_origin_dispatch_is_trusted
#   proves: binary_sequence_closure, binary_coordinate_recovery
#   call: self::test_byte_axis_shadow_cannot_change_closure
# id: profile_serialization_is_trusted
#   proves: cycle_strict_refusal
#   call: self::test_profile_and_round_serializers_cannot_change_identity
# id: capped_candidates_preserve_occurrences
#   proves: discovery_repeat_selection
#   call: self::test_capped_candidate_collects_all_disjoint_occurrences
# id: cycle_definitions_are_literal
#   proves: cycle_discovery_profile
#   call: self::test_cycle_rejects_recipe_backed_definition
# id: scheduler_replay_is_trusted
#   proves: prime_split_replay
#   call: self::test_scheduler_ignores_record_owned_replay
# === END CHECKS ===
"""Five follow-up findings on PR #77; replay without network or user data.

Usage: WEAVE_SOURCES=/checkouts python -m unittest discover -s tests -p test_final_findings.py -v
The closure/profile tests mutate supplied records, never trusted runtime classes.
The repetition tests exercise the declared selection rule, not a new compressor.
"""
from copy import copy
from dataclasses import replace
from fractions import Fraction
from itertools import product
from pathlib import Path
from unittest.mock import patch
import os
import unittest

import affixiation
import cycle
import native_binary as native
import numeral
from prime_schedule import Route
from numeral import PrimePath, Refused, ResourceLimit, Limits

ROOT = Path(__file__).resolve().parents[1]
SOURCES = Path(os.environ['WEAVE_SOURCES'])
SPACES = tuple(Fraction(i, 9) for i in range(8))


class FinalFindingsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.geometry = native.Geometry(SOURCES/'ucns')

    def profile(self):
        return cycle.Profile.read((ROOT/'profiles/cycle-v1.json').read_bytes())

    def test_byte_axis_shadow_cannot_change_closure(self):
        origin = native.ByteOrigin(b'ABxABy', 'review', 0, self.geometry)
        args = ((b'AB', b'x', b'y'), (0,1,0,2), (1,2,3), SPACES)
        expected = native.close_sequences(origin, *args)
        other = native.ByteOrigin(origin.source, 'other', 0, self.geometry)
        called = []
        object.__setattr__(origin, 'byte_axis', lambda n: called.append(n) or other.byte_axis(n))
        actual = native.close_sequences(origin, *args)
        self.assertEqual(actual.receipt(), expected.receipt())
        self.assertEqual(called, [])
        self.assertTrue(all(d.attachment_axis.origin_sha256 == origin.identity for d in actual.definitions))

    def test_forged_origin_axes_are_rejected_by_all_exports(self):
        origin = native.ByteOrigin(b'ABxABy', 'review', 0, self.geometry)
        table = native.close_sequences(origin,(b'AB',b'x',b'y'),(0,1,0,2),(1,2,3),SPACES)
        other = native.ByteOrigin(origin.source, 'other', 0, self.geometry)
        object.__setattr__(origin, 'byte_axis', other.byte_axis)
        definitions = []
        for d in table.definitions:
            axis = other.byte_axis(d.occurrences[0].source_offset)
            occurrences = []
            for o in d.occurrences:
                src = other.byte_axis(o.source_offset)
                occurrences.append(replace(o,source_axis=src,source_state=self.geometry.placed(src,SPACES[o.circle])))
            definitions.append(replace(d,attachment_axis=axis,state=self.geometry.placed(axis,SPACES[0]),occurrences=tuple(occurrences)))
        object.__setattr__(table,'definitions',tuple(definitions))
        for operation in (table.restore,table.receipt,table.wire_occurrences):
            with self.subTest(operation=operation.__name__), self.assertRaises(native.BinaryError):
                operation()

    def test_profile_and_round_serializers_cannot_change_identity(self):
        for slot in ('profile','round'):
            p = self.profile(); identity = p.identity; called = []
            target = p if slot == 'profile' else p.rounds[0]
            object.__setattr__(target,'as_dict',lambda: called.append(1) or {'spoof':'unexecuted'})
            self.assertEqual(p.identity,identity)
            self.assertEqual(called,[])
            wire,_ = cycle.forward(b'ABxABy',b'corpus',replace(p,rounds=p.rounds[:1]),SOURCES)
            clean=replace(self.profile(),rounds=self.profile().rounds[:1])
            self.assertEqual(cycle.reverse(wire,b'corpus',clean,SOURCES),b'ABxABy')

    def test_profile_revalidates_mutated_record_fields(self):
        cases = (('profile','bucket_bytes',0),('profile','corpus_bit_offset',True),
                 ('round','arities',(True,)),('round','end_order','unknown'),
                 ('round','circle_order',(1,)*7),('round','spaces',(Fraction(0),)*7),
                 ('path','seed',True),('path','steps',(('span',True,0,1),)))
        for slot,name,value in cases:
            p=self.profile(); target = p if slot=='profile' else p.rounds[0] if slot=='round' else p.rounds[0].path
            object.__setattr__(target,name,value)
            object.__setattr__(target,'__post_init__',lambda:None)
            with self.subTest(slot=slot,name=name),self.assertRaises(Refused):
                _ = p.identity

    def test_scheduler_ignores_record_owned_replay(self):
        path=PrimePath(53,(('next',),));expected=Route.evaluate(path);called=[]
        object.__setattr__(path,'replay',lambda *a,**k:called.append(1) or (53,999))
        self.assertEqual(Route.evaluate(path),expected)
        self.assertEqual(called,[])
        object.__setattr__(path,'seed',4)
        with self.assertRaises(Refused):Route.evaluate(path)
        self.assertEqual(called,[])

    def test_scheduler_shadow_cannot_bypass_work_budget(self):
        path=PrimePath(101,());called=[]
        object.__setattr__(path,'replay',lambda *a,**k:called.append(1) or (101,))
        with self.assertRaises(ResourceLimit):Route.evaluate(path,Limits(prime_work=1))
        self.assertEqual(called,[])

    def test_capped_candidate_collects_all_disjoint_occurrences(self):
        p=affixiation.discover(b'\x00\x01\x00\x01\x00\x01\x01')
        self.assertEqual(p.blocks,(b'\x00\x01',b'\x01'))
        self.assertEqual(p.order,(0,0,0,1))
        self.assertEqual(p.starts,(0,2,4,6))
        self.assertEqual(p.restore(),b'\x00\x01\x00\x01\x00\x01\x01')

    def test_capped_suffix_intervals_match_full_prefix_occurrences(self):
        # Check the existing LCP-derived candidate family, not all substring sizes.
        # The oracle expands each candidate with byte comparisons and checks the
        # leftmost nonoverlapping result under the declared longest-first rule.
        for n in range(1,10):
            for values in product(range(2),repeat=n):
                data=bytes(values);suffixes=affixiation._suffix_array(data)
                common=affixiation._lcp(data,suffixes);stack=[];patterns=set()
                for i in range(1,n+1):
                    depth=common[i] if i<n else 0;left=i-1
                    while stack and stack[-1][0]>depth:
                        size,begin=stack.pop();positions=suffixes[begin:i]
                        size=min(size,max(positions)-min(positions))
                        if size>=2:patterns.add(data[positions[0]:positions[0]+size])
                        left=begin
                    if depth and (not stack or stack[-1][0]<depth):stack.append((depth,left))
                used=set();chosen=[]
                for block in sorted(patterns,key=lambda b:(-len(b),data.find(b))):
                    starts=[i for i in range(n-len(block)+1) if data.startswith(block,i)]
                    selected=[];end=-1
                    for start in starts:
                        if start>=end and not used.intersection(range(start,start+len(block))):
                            selected.append(start);end=start+len(block)
                    if len(selected)>=2:
                        for start in selected:
                            used.update(range(start,start+len(block)));chosen.append((start,len(block)))
                result=affixiation.discover(data)
                for start,size in chosen:
                    self.assertIn(start,result.starts,(data,start,size,result))
                    self.assertEqual(result.blocks[result.order[result.starts.index(start)]],data[start:start+size])
                self.assertEqual(result.restore(),data)

    def test_cycle_rejects_recipe_backed_definition(self):
        source=b'\x00eX\x00eY';p=self.profile()
        args=dict(api=native,geometry=self.geometry,scope=p.scope,
                  root=native.ByteOrigin(source,p.scope,0,self.geometry).message_origin,
                  round_id=0,spec=p.rounds[0])
        wire,_=cycle.affix(source,**args);r=numeral._Reader(wire)
        magic=r.take(4);size=r.uint();packet=numeral.decode(r.blob(cycle.CycleLimits().round_bytes))
        tail=wire[r.pos:];entries=[];changed=0
        for e in packet.entries:
            if numeral.BitBlock.to_bytes(e.block)==b'\x00e':
                e=replace(e,recipe=PrimePath(101,()));changed+=1
            entries.append(e)
        self.assertEqual(changed,1)
        variant=replace(packet,entries=tuple(entries))
        self.assertEqual(numeral.decode(numeral.encode(variant)).restore(),packet.restore())
        altered=magic+numeral._uint(size)+numeral._blob(numeral.encode(variant))+tail
        with self.assertRaisesRegex(Refused,'literal|recipe'):
            cycle.unaffix(altered,**args)
        self.assertEqual(cycle.unaffix(wire,**args),source)


if __name__=='__main__':unittest.main()
