# === CHECKS ===
# id: numeral_metadata_before_prime_work
#   proves: numeral_strict_input
#   call: self::test_recipe_metadata_rejected_before_any_replay
# id: numeral_late_metadata_before_prime_work
#   proves: numeral_strict_input
#   call: self::test_late_entry_failure_does_not_replay_earlier_recipe
# id: numeral_shapes_before_prime_work
#   proves: numeral_strict_input, numeral_recipe_replay
#   call: self::test_all_recipe_shapes_checked_before_replay
# id: numeral_deferred_same_budget
#   proves: numeral_exact_recovery, numeral_recipe_replay
#   call: self::test_deferred_decode_replays_once_at_same_limit
# id: normalization_validates_public_profile
#   proves: cycle_normalize_once, cycle_strict_refusal
#   call: self::test_direct_normalization_rejects_mutated_profiles
# id: normalization_trusted_validation
#   proves: cycle_strict_refusal
#   call: self::test_normalization_uses_class_validator
# id: affixiation_validates_public_round
#   proves: cycle_strict_refusal
#   call: self::test_public_affixiation_rejects_mutated_round_before_work
# id: public_helpers_preserve_valid_cycle
#   proves: cycle_normalize_once, cycle_reversible_rounds
#   call: self::test_valid_helpers_preserve_cycle_output
# === END CHECKS ===
"""Run: WEAVE_SOURCES=/checkouts python -m unittest discover -s tests -p test_admission_order.py -v.

Cheap complete input admission precedes prime work. Public normalization and
round helpers validate caller-supplied profiles through trusted class operations.
Nonsecret fixtures only; no mutation of trusted runtime code outside scoped mocks.
"""
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch
import os
import unittest

import cycle
import native_binary as native
import numeral as n

ROOT = Path(__file__).resolve().parents[1]
SOURCES = Path(os.environ['WEAVE_SOURCES'])
A, B = chr(0xE000), chr(0xE001)


def definition(symbol=A, angle=(1,7), circle=1, length=16, seed=101, steps=()):
    encoded = (n._blob(symbol.encode()) + n._uint(angle[0])+n._uint(angle[1])
               + n._uint(circle)+n._uint(length)+b'\x01'+n._uint(seed)+n._uint(len(steps)))
    for step in steps:
        if step == ('next',): encoded += b'\x00'
        else: encoded += b'\x01' + b''.join(n._uint(x) for x in step[1:])
    return encoded


def wire(rows, symbols=A, declared=16, origin=b'admission'):
    return (n.MAGIC+n._blob(origin)+n._uint(0)+n._uint(declared)+n._uint(len(rows))
            + b''.join(rows)+n._blob(symbols.encode()))


class AdmissionOrderTests(unittest.TestCase):
    def assert_cheap_refusal(self, data):
        with patch.object(n.PrimePath,'replay',side_effect=AssertionError('recipe ran before admission')) as replay:
            with self.assertRaises(n.Refused) as failure:
                n.decode(data,n.Limits(prime_work=4))
            self.assertNotIsInstance(failure.exception,n.ResourceLimit)
            replay.assert_not_called()

    def test_recipe_metadata_rejected_before_any_replay(self):
        cases=(wire([definition(circle=0)]),wire([definition(circle=8)]),
               wire([definition(angle=(2,1))]),wire([definition(angle=(2,2))]),
               wire([definition(length=0)]),wire([definition()],origin=b''),
               wire([definition()],symbols=B),wire([definition()],declared=17),
               wire([definition()])+b'extra',wire([definition()])[:-1])
        for i,data in enumerate(cases):
            with self.subTest(case=i):self.assert_cheap_refusal(data)

    def test_late_entry_failure_does_not_replay_earlier_recipe(self):
        cases=(definition(symbol=B,circle=0),definition(symbol=B,angle=(2,1)),
               definition(symbol=A,angle=(2,7)),definition(symbol=B,angle=(1,7)),
               definition(symbol=B,angle=(2,7),length=0))
        for i,second in enumerate(cases):
            with self.subTest(case=i):self.assert_cheap_refusal(wire([definition(),second],symbols=A+B,declared=32))
        self.assert_cheap_refusal(wire([definition(),definition(symbol=B,angle=(2,7))],symbols=A+B,declared=31))

    def test_all_recipe_shapes_checked_before_replay(self):
        cases=(dict(seed=1),dict(steps=(('span',3,0,1),)),dict(steps=(('span',10,0,0),)))
        for i,changes in enumerate(cases):
            data=wire([definition(),definition(symbol=B,angle=(2,7),**changes)],symbols=A+B,declared=32)
            with self.subTest(case=i):self.assert_cheap_refusal(data)
        # A malformed late step in a public recipe also refuses before the first
        # expensive nth-prime operation or prime-work charge.
        path=n.PrimePath(101,(('next',),('span',3,0,1)))
        with patch.object(n._Primes,'charge',side_effect=AssertionError('charged before shape admission')):
            with self.assertRaises(n.Refused) as failure:n.PrimePath.replay(path,n.Limits(prime_work=1))
            self.assertNotIsInstance(failure.exception,n.ResourceLimit)

    def test_deferred_decode_replays_once_at_same_limit(self):
        limits=n.Limits(prime_work=10)
        data=wire([definition(),definition(symbol=B,angle=(2,7),seed=103)],symbols=A+B,declared=32)
        engine=n._Primes(limits)
        with patch.object(n.PrimePath,'replay',autospec=True,side_effect=n.PrimePath.replay) as replay:
            packet=n.decode(data,limits,_engine=engine)
        self.assertEqual(replay.call_count,2)
        self.assertEqual(engine.work,10)
        self.assertEqual(n.encode(packet,limits),data)
        self.assertEqual(n.Packet.restore(packet,limits).to_bytes(),b'\x00e\x00g')
        with self.assertRaises(n.ResourceLimit):n.decode(data,n.Limits(prime_work=9))

    def profile(self):
        return cycle.Profile.read((ROOT/'profiles/cycle-v1.json').read_bytes())

    def test_direct_normalization_rejects_mutated_profiles(self):
        original=self.profile();frame=cycle.normalize(b'AB',b'corpus',original)
        for field,value in (('bucket_bytes',0),('bucket_bytes',True),('corpus_bit_offset',True),
                            ('corpus_bit_offset',-1),('scope',''),('rounds',[])):
            p=self.profile();object.__setattr__(p,field,value)
            with self.subTest(field=field),self.assertRaises(n.Refused):cycle.normalize(b'AB',b'corpus',p)
            with self.subTest(field=field),self.assertRaises(n.Refused):cycle.denormalize(frame,b'corpus',p)
        p=self.profile();object.__setattr__(p.rounds[0],'circle_order',(1,)*7)
        with self.assertRaises(n.Refused):cycle.normalize(b'AB',b'corpus',p)
        with self.assertRaises(n.Refused):cycle.denormalize(frame,b'corpus',p)

    def test_normalization_uses_class_validator(self):
        p=self.profile();called=[]
        object.__setattr__(p,'__post_init__',lambda:called.append(True))
        frame=cycle.normalize(b'AB',b'corpus',p)
        self.assertEqual(cycle.denormalize(frame,b'corpus',p),b'AB')
        self.assertEqual(called,[])
        object.__setattr__(p,'corpus_bit_offset',True)
        for operation,args in ((cycle.normalize,(b'AB',b'corpus',p)),(cycle.denormalize,(frame,b'corpus',p))):
            with self.assertRaises(n.Refused):operation(*args)
        self.assertEqual(called,[])

    def test_public_affixiation_rejects_mutated_round_before_work(self):
        for field,value in (('circle_order',(1,)*7),('spaces',()),('arities',(True,)),('end_order','unknown')):
            spec=self.profile().rounds[0];object.__setattr__(spec,field,value)
            kwargs=dict(api=None,geometry=None,scope='x',root='0'*64,round_id=0,spec=spec)
            with self.subTest(field=field),patch.object(cycle,'discover',side_effect=AssertionError('discovery before round admission')):
                with self.assertRaises(n.Refused):cycle.affix(b'ABAB',**kwargs)
            with self.subTest(field=field),patch.object(cycle,'decode_numeral',side_effect=AssertionError('decode before round admission')):
                with self.assertRaises(n.Refused):cycle.unaffix(cycle.AFFIX_MAGIC+b'\x00',**kwargs)

    def test_valid_helpers_preserve_cycle_output(self):
        p=self.profile();g=native.Geometry(SOURCES/'ucns')
        for offset in (0,1,7,8,19):
            profile=replace(p,corpus_bit_offset=offset)
            for data in (b'',b'ABxABy',bytes(range(256))):
                frame=cycle.normalize(data,b'corpus',profile)
                self.assertEqual(cycle.denormalize(frame,b'corpus',profile),data)
        data=b'ABxABy';root=native.ByteOrigin(data,p.scope,0,g).message_origin
        kwargs=dict(api=native,geometry=g,scope=p.scope,root=root,round_id=0,spec=p.rounds[0])
        record,_=cycle.affix(data,**kwargs)
        self.assertEqual(cycle.unaffix(record,**kwargs),data)


if __name__=='__main__':unittest.main()
