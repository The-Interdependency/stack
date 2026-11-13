# === CHECKS ===
# id: check_all_8191_short_binary_alphabet_byte_strings
#   proves: discovery_exact_partition, discovery_repeat_selection
#   call: self::test_all_8191_short_binary_alphabet_byte_strings
#   mutates: none
#   cleanup: none
#
# id: check_repeated_multibyte_and_residuals
#   proves: discovery_exact_partition, discovery_repeat_selection
#   call: self::test_repeated_multibyte_and_residuals
#   mutates: none
#   cleanup: none
#
# id: check_competing_overlaps_are_deterministic
#   proves: discovery_exact_partition, discovery_repeat_selection
#   call: self::test_competing_overlaps_are_deterministic
#   mutates: none
#   cleanup: none
#
# id: check_nonrepeated_and_single_byte_remain_literal
#   proves: discovery_exact_partition, discovery_repeat_selection
#   call: self::test_nonrepeated_and_single_byte_remain_literal
#   mutates: none
#   cleanup: none
#
# id: check_discovery_budget_refuses_not_truncates
#   proves: discovery_resource_refusal
#   call: self::test_discovery_budget_refuses_not_truncates
#   mutates: none
#   cleanup: none
#
# id: check_normalization_exact_bucket_and_corpus_bits
#   proves: cycle_normalize_once
#   call: self::test_normalization_exact_bucket_and_corpus_bits
#   mutates: none
#   cleanup: none
#
# id: check_exact_bucket_input_still_uses_corpus
#   proves: cycle_normalize_once
#   call: self::test_exact_bucket_input_still_uses_corpus
#   mutates: none
#   cleanup: none
#
# id: check_normalization_source_zeroes_and_empty
#   proves: cycle_normalize_once
#   call: self::test_normalization_source_zeroes_and_empty
#   mutates: none
#   cleanup: none
#
# id: check_wrong_corpus_and_padding_are_rejected
#   proves: cycle_normalize_once
#   call: self::test_wrong_corpus_and_padding_are_rejected
#   mutates: none
#   cleanup: none
#
# id: check_all_small_composition_ranks
#   proves: prime_split_replay
#   call: self::test_all_small_composition_ranks
#   mutates: none
#   cleanup: none
#
# id: check_actual_prime_recursion_and_jumps
#   proves: prime_split_replay
#   call: self::test_actual_prime_recursion_and_jumps
#   mutates: none
#   cleanup: none
#
# id: check_route_occurrence_identity_is_not_destination_only
#   proves: prime_split_replay
#   call: self::test_route_occurrence_identity_is_not_destination_only
#   mutates: none
#   cleanup: none
#
# id: check_split_controls_replay_without_source
#   proves: prime_split_replay
#   call: self::test_split_controls_replay_without_source
#   mutates: none
#   cleanup: none
#
# id: check_both_end_orders_preserve_each_bit
#   proves: first_last_inverse
#   call: self::test_both_end_orders_preserve_each_bit
#   mutates: none
#   cleanup: none
#
# id: check_all_256_byte_values_interleave_inverse
#   proves: first_last_inverse
#   call: self::test_all_256_byte_values_interleave_inverse
#   mutates: none
#   cleanup: none
#
# id: check_invalid_split_parameters_refused
#   proves: first_last_inverse
#   call: self::test_invalid_split_parameters_refused
#   mutates: none
#   cleanup: none
#
# id: check_native_objects_and_720_return_are_used
#   proves: cycle_native_occurrence_recovery
#   call: self::test_native_objects_and_720_return_are_used
#   mutates: none
#   cleanup: none
#
# id: check_native_affix_and_coordinate_recovery
#   proves: cycle_native_occurrence_recovery
#   call: self::test_native_affix_and_coordinate_recovery
#   mutates: none
#   cleanup: none
#
# id: check_spaces_are_effective_native_inputs
#   proves: cycle_native_occurrence_recovery
#   call: self::test_spaces_are_effective_native_inputs
#   mutates: none
#   cleanup: none
#
# id: check_one_round_empty_and_all_byte_values
#   proves: cycle_reversible_rounds
#   call: self::test_one_round_empty_and_all_byte_values
#   mutates: none
#   cleanup: none
#
# id: check_three_round_cycle_exact_and_once_normalized
#   proves: cycle_reversible_rounds
#   call: self::test_three_round_cycle_exact_and_once_normalized
#   mutates: none
#   cleanup: none
#
# id: check_seeded_random_mixed_data_two_rounds
#   proves: cycle_reversible_rounds
#   call: self::test_seeded_random_mixed_data_two_rounds
#   mutates: none
#   cleanup: none
#
# id: check_65536_byte_declared_case_roundtrip
#   proves: cycle_reversible_rounds
#   call: self::test_65536_byte_declared_case_roundtrip
#   mutates: none
#   cleanup: none
#
# id: check_every_outer_truncation_and_trailing_bytes_refused
#   proves: cycle_strict_refusal
#   call: self::test_every_outer_truncation_and_trailing_bytes_refused
#   mutates: none
#   cleanup: none
#
# id: check_profile_material_native_identity_mismatches_refused
#   proves: cycle_native_occurrence_recovery
#   call: self::test_profile_material_native_identity_mismatches_refused
#   mutates: none
#   cleanup: none
#
# id: check_profile_strict_fields_and_types
#   proves: cycle_strict_refusal
#   call: self::test_profile_strict_fields_and_types
#   mutates: none
#   cleanup: none
#
# id: check_cycle_budgets_fail_without_partial_results
#   proves: cycle_strict_refusal
#   call: self::test_cycle_budgets_fail_without_partial_results
#   mutates: none
#   cleanup: none
#
# id: check_source_tampering_refused_before_execution
#   proves: cycle_native_source_pinned
#   call: self::test_source_tampering_refused_before_execution
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_cli_fresh_process_source_deleted_and_no_overwrite
#   proves: cycle_reversible_rounds
#   call: self::test_cli_fresh_process_source_deleted_and_no_overwrite
#   mutates: filesystem
#   cleanup: tempdir_teardown
#
# id: check_profile_roundtrip_and_all_accounting_fields
#   proves: cycle_complete_accounting
#   call: self::test_profile_roundtrip_and_all_accounting_fields
#   mutates: none
#   cleanup: none
#
# === END CHECKS ===
"""Run: WEAVE_SOURCES=/checkouts python -m unittest discover -s tests -p test_cycle.py -v.

The suite exercises the declared complete sequence cycle and real locked producers.
It is not a test of public-key secrecy. Files are isolated in temporary directories.
"""
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from affixiation import discover
from prime_schedule import Route, SplitPlan, plan, interleave, _composition
from numeral import PrimePath, Refused, ResourceLimit
import cycle
from cycle import Profile, CycleLimits, normalize, denormalize, affix, unaffix, forward, reverse
from cycle_native import load_native
import cycle_native

ROOT = Path(__file__).resolve().parents[1]
SOURCES = Path(os.environ.get('WEAVE_SOURCES', ROOT/'sources'))
PROFILE = Profile.read((ROOT/'profiles/cycle-v1.json').read_bytes())
CORPUS = bytes(range(256)) + b'actual corpus bytes'


def one_round():
    return replace(PROFILE, rounds=PROFILE.rounds[:1])


class CycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api, cls.geometry = load_native(SOURCES)

    def test_all_8191_short_binary_alphabet_byte_strings(self):
        count = 0
        for n in range(13):
            for value in range(1 << n):
                data = bytes((value >> i) & 1 for i in range(n))
                part = discover(data)
                self.assertEqual(part.restore(), data)
                self.assertEqual(part.starts, tuple(sum(len(part.blocks[j]) for j in part.order[:i])
                                                   for i in range(len(part.order))))
                count += 1
        self.assertEqual(count, 8191)

    def test_repeated_multibyte_and_residuals(self):
        p = discover(b'ABxABy')
        self.assertEqual(p.blocks, (b'AB', b'x', b'y'))
        self.assertEqual(p.order, (0,1,0,2))
        self.assertEqual(p.starts, (0,2,3,5))
        self.assertEqual(p.repeat_ids, (0,))

    def test_competing_overlaps_are_deterministic(self):
        for data in (b'AAAAA', b'ABABABA', b'banana bandana banana', b'abcabcabcab'):
            p = discover(data)
            self.assertEqual(p, discover(data))
            self.assertEqual(p.restore(), data)
            for a,b,i in zip(p.starts,p.starts[1:],p.order):
                self.assertLessEqual(a+len(p.blocks[i]), b)
        self.assertEqual(discover(b'AAAAA').blocks, (b'AA', b'A'))
        self.assertEqual(discover(b'AAAAA').order, (0,0,1))

    def test_nonrepeated_and_single_byte_remain_literal(self):
        data = bytes(range(256))
        self.assertEqual(discover(data).blocks, (data,))
        self.assertEqual(discover(b'x').blocks, (b'x',))
        self.assertEqual(discover(b'').restore(), b'')
        self.assertEqual(discover(b'abaca').repeat_ids, ())

    def test_discovery_budget_refuses_not_truncates(self):
        with self.assertRaises(ResourceLimit):
            discover(b'ABABAB',visit_budget=1)
        with self.assertRaises(ResourceLimit):
            discover(b'ABABAB',max_bytes=5)
        for bad in ('abc', bytearray(b'abc'), None):
            with self.assertRaises(Refused): discover(bad)

    def test_normalization_exact_bucket_and_corpus_bits(self):
        profile = one_round()
        data = normalize(b'abc', CORPUS, profile)
        self.assertEqual(len(data), 256)
        bits = ''.join(format(x,'08b') for x in CORPUS)
        n = len(data)-47
        expected = ''.join(bits[(profile.corpus_bit_offset+i)%len(bits)] for i in range(n*8))
        self.assertEqual(data[47:], int(expected,2).to_bytes(n,'big'))
        self.assertEqual(denormalize(data,CORPUS,profile),b'abc')

    def test_exact_bucket_input_still_uses_corpus(self):
        profile = one_round()
        data = normalize(b'x'*212,b'\xa5',profile)
        self.assertEqual(len(data),512)
        self.assertEqual(denormalize(data,b'\xa5',profile),b'x'*212)

    def test_normalization_source_zeroes_and_empty(self):
        for raw in (b'',b'\x00',b'\x00\x00\x01',bytes(range(256))):
            for offset in (0,1,7,8,15,100003):
                p = replace(one_round(),corpus_bit_offset=offset)
                self.assertEqual(denormalize(normalize(raw,CORPUS,p),CORPUS,p),raw)

    def test_wrong_corpus_and_padding_are_rejected(self):
        profile = one_round()
        data = normalize(b'abc',CORPUS,profile)
        with self.assertRaises(Refused): denormalize(data,CORPUS+b'!',profile)
        with self.assertRaises(Refused): denormalize(data[:-1]+bytes([data[-1]^1]),CORPUS,profile)
        with self.assertRaises(Refused): normalize(b'abc',b'',profile)
        with self.assertRaises(ResourceLimit): normalize(b'abc',CORPUS,profile,CycleLimits(round_bytes=100))

    def test_all_small_composition_ranks(self):
        cases = 0
        for n in range(2,13):
            for arity in range(2,n+1):
                for rank,gaps in enumerate(combinations(range(1,n),arity-1)):
                    points = (0,*gaps,n)
                    self.assertEqual(_composition(n,arity,rank),tuple(b-a for a,b in zip(points,points[1:])))
                    cases += 1
        self.assertEqual(cases,4083)

    def test_actual_prime_recursion_and_jumps(self):
        route = Route.evaluate(PROFILE.rounds[0].path)
        self.assertEqual(route.trace,(5381,53,241,1523))
        self.assertEqual(Route.evaluate(PrimePath(2, (('next',),)*7)).trace,
                         (2,3,5,11,31,127,709,5381))
        self.assertEqual(Route.evaluate(PrimePath(5381,(('span',2,0,3),))).trace,(5381,5))

    def test_route_occurrence_identity_is_not_destination_only(self):
        a = Route.evaluate(PrimePath(313,(('span',10,0,1),)))
        b = Route.evaluate(PrimePath(313,(('span',10,2,1),)))
        self.assertEqual(a.trace,b.trace)
        self.assertNotEqual(a.determinant,b.determinant)
        self.assertNotEqual(plan(1024,a,(3,5,7)),plan(1024,b,(3,5,7)))

    def test_split_controls_replay_without_source(self):
        route = Route.evaluate(PROFILE.rounds[0].path)
        for n in (8,16,128,1024,65536):
            split = plan(n,route,(3,5,7))
            self.assertEqual(sum(split.lengths),n)
            self.assertTrue(all(x>0 for x in split.lengths))
            self.assertEqual(plan(n,route,(3,5,7)),split)
            self.assertLess(split.rank,comb(n-1,len(split.lengths)-1))

    def test_both_end_orders_preserve_each_bit(self):
        split = SplitPlan(24,(7,5,12),0)
        for end in ('first-last','last-first'):
            mapped=[]
            for index in range(24):
                data = (1 << (23-index)).to_bytes(3,'big')
                out = interleave(data,split,end_order=end)
                self.assertEqual(int.from_bytes(out,'big').bit_count(),1)
                self.assertEqual(interleave(out,split,inverse=True,end_order=end),data)
                mapped.append(out)
            self.assertEqual(len(set(mapped)),24)

    def test_all_256_byte_values_interleave_inverse(self):
        for v in range(256):
            data = bytes([v])
            for end in ('first-last','last-first'):
                for split in (SplitPlan(8,(1,7),0),SplitPlan(8,(3,2,3),0)):
                    self.assertEqual(interleave(interleave(data,split,end_order=end),split,inverse=True,end_order=end),data)

    def test_invalid_split_parameters_refused(self):
        route = Route.evaluate(PrimePath(53,()))
        for arities in ((1,), (9,), (3,3), (True,), ([3],), [3]):
            with self.assertRaises(Refused): plan(8,route,arities)
        for lengths in ((3,3),(0,8),(True,7),(-1,9)):
            with self.assertRaises(Refused): interleave(b'a',SplitPlan(8,lengths,0))

    def test_native_objects_and_720_return_are_used(self):
        origin = self.api.ByteOrigin(b'ABxABy','native-test',0,self.geometry)
        axis = origin.byte_axis(3)
        self.assertEqual(type(axis).__name__,'AxisCirclePosition')
        self.assertEqual(axis.turn,Fraction(1,2))
        state = self.geometry.placed(axis,Fraction(1,7))
        self.assertEqual(type(state).__name__,'NativeMobiusState')
        self.assertNotEqual(state.complete_key,state.advance(1).complete_key)
        self.assertEqual(state.complete_key,state.advance(2).complete_key)

    def test_native_affix_and_coordinate_recovery(self):
        raw = b'ABxABy'
        origin = self.api.ByteOrigin(raw,'native-test',0,self.geometry)
        spec = PROFILE.rounds[0]
        wire,stats = affix(raw,api=self.api,geometry=self.geometry,scope=origin.scope,
                          root=origin.message_origin,round_id=0,spec=spec)
        restored = unaffix(wire,api=self.api,geometry=self.geometry,scope=origin.scope,
                           root=origin.message_origin,round_id=0,spec=spec)
        self.assertEqual(restored,raw)
        self.assertEqual(stats['repeated_definitions'],1)
        self.assertEqual(stats['occurrences'],4)
        self.assertEqual(stats['output_bytes'],stats['numeral_bytes']+stats['native_coordinate_and_frame_bytes'])

    def test_spaces_are_effective_native_inputs(self):
        raw = b'ABxABy'
        root = self.api.ByteOrigin(raw,'native-test',0,self.geometry).message_origin
        a = PROFILE.rounds[0]
        b = replace(a,spaces=tuple((x+Fraction(1,3))%2 for x in a.spaces))
        kwargs = dict(api=self.api,geometry=self.geometry,scope='native-test',root=root,round_id=0)
        wa,_ = affix(raw,spec=a,**kwargs)
        wb,_ = affix(raw,spec=b,**kwargs)
        self.assertNotEqual(wa,wb)
        self.assertEqual(unaffix(wa,spec=a,**kwargs),raw)
        self.assertEqual(unaffix(wb,spec=b,**kwargs),raw)
        with self.assertRaises(ValueError): unaffix(wa,spec=b,**kwargs)

    def test_one_round_empty_and_all_byte_values(self):
        for raw in (b'',b'\x00',b'\xff',bytes(range(256)),b'ababababcabc'):
            wire,stats = forward(raw,CORPUS,one_round(),SOURCES)
            self.assertEqual(reverse(wire,CORPUS,one_round(),SOURCES),raw)
            self.assertEqual(len(stats['rounds']),1)

    def test_three_round_cycle_exact_and_once_normalized(self):
        raw = b'Weave repeats byte sequences. '*24 + bytes(range(64))
        with patch.object(cycle,'normalize',wraps=normalize) as call:
            wire,stats = forward(raw,CORPUS,PROFILE,SOURCES)
        self.assertEqual(call.call_count,1)
        self.assertEqual(reverse(wire,CORPUS,PROFILE,SOURCES),raw)
        self.assertEqual(len(stats['rounds']),3)
        for left,right in zip(stats['rounds'],stats['rounds'][1:]):
            self.assertEqual(left['output_bytes'],right['input_bytes'])
        self.assertEqual(stats['total_bytes'],len(wire))
        self.assertEqual(stats['final_payload_bytes']+stats['outer_frame_bytes'],len(wire))

    def test_seeded_random_mixed_data_two_rounds(self):
        rng = random.Random(20261005)
        p = replace(PROFILE,rounds=PROFILE.rounds[:2])
        for n in (0,7,31,128,511):
            raw = rng.randbytes(n)+b'\x00xy\x00xy'*7
            wire,_ = forward(raw,CORPUS,p,SOURCES)
            self.assertEqual(reverse(wire,CORPUS,p,SOURCES),raw)

    def test_65536_byte_declared_case_roundtrip(self):
        raw = bytes(range(256))*256
        p = replace(PROFILE,bucket_bytes=4096,rounds=PROFILE.rounds[:2])
        wire,stats = forward(raw,CORPUS,p,SOURCES)
        self.assertEqual(reverse(wire,CORPUS,p,SOURCES),raw)
        self.assertEqual(stats['source_bytes'],65536)

    def test_every_outer_truncation_and_trailing_bytes_refused(self):
        wire,_ = forward(b'ABxABy',CORPUS,one_round(),SOURCES)
        for length in range(len(wire)):
            with self.assertRaises(ValueError): reverse(wire[:length],CORPUS,one_round(),SOURCES)
        with self.assertRaises(Refused): reverse(wire+b'!',CORPUS,one_round(),SOURCES)

    def test_profile_material_native_identity_mismatches_refused(self):
        wire,_ = forward(b'test',CORPUS,one_round(),SOURCES)
        with self.assertRaises(Refused): reverse(wire,CORPUS,replace(one_round(),scope='other'),SOURCES)
        with self.assertRaises(Refused): reverse(wire,CORPUS+b'!',one_round(),SOURCES)
        for pos in (4,36,68,100):
            damaged = bytearray(wire); damaged[pos] ^= 1
            with self.assertRaises(ValueError): reverse(bytes(damaged),CORPUS,one_round(),SOURCES)

    def test_profile_strict_fields_and_types(self):
        obj = PROFILE.as_dict()
        cases=[]
        c=deepcopy(obj); c['unknown']=True; cases.append(c)
        c=deepcopy(obj); c['rounds'][0]['spaces'][0]=[1,0]; cases.append(c)
        c=deepcopy(obj); c['rounds'][0]['spaces'][0]=[2,4]; cases.append(c)
        c=deepcopy(obj); c['rounds'][0]['arities']=[True]; cases.append(c)
        c=deepcopy(obj); c['rounds'][0]['arities']=[[3]]; cases.append(c)
        c=deepcopy(obj); c['rounds'][0]['circle_order']=[1]*7; cases.append(c)
        c=deepcopy(obj); c['rounds'][0]['end_order']='arbitrary'; cases.append(c)
        for c in cases:
            with self.assertRaises(ValueError): Profile.read(json.dumps(c).encode())
        with self.assertRaises(Refused): Profile.read(b'{"schema":1,"schema":2}')
        with self.assertRaises(ResourceLimit): Profile.read(json.dumps(obj).encode(),CycleLimits(rounds=2))

    def test_cycle_budgets_fail_without_partial_results(self):
        with self.assertRaises(ResourceLimit): forward(b'1234',CORPUS,PROFILE,SOURCES,CycleLimits(input_bytes=3))
        with self.assertRaises(ResourceLimit): forward(b'1234',CORPUS,PROFILE,SOURCES,CycleLimits(rounds=2))
        with self.assertRaises(ResourceLimit): forward(b'1234',CORPUS,PROFILE,SOURCES,CycleLimits(prime_work=1))
        with self.assertRaises(ResourceLimit): forward(b'ABxABy',CORPUS,one_round(),SOURCES,CycleLimits(native_occurrences=1))

    def test_source_tampering_refused_before_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            shutil.copy2(ROOT/'CYCLE_NATIVE.json',root/'CYCLE_NATIVE.json')
            marker=root/'executed'
            (root/'native_binary.py').write_text(f"open({str(marker)!r},'w').write('oops')\n")
            with patch.object(cycle_native,'ROOT',root):
                with self.assertRaises(Refused): load_native(SOURCES)
            self.assertFalse(marker.exists())

    def test_cli_fresh_process_source_deleted_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            src,wire,out,corpus,profile = (root/x for x in ('source','packet','restored','corpus','profile.json'))
            raw=bytes(range(256))*4+b'\x00AB\x00AB'*17
            src.write_bytes(raw);corpus.write_bytes(CORPUS)
            profile.write_bytes(cycle.canonical(PROFILE.as_dict()))
            args=['--sources',str(SOURCES),'--profile',str(profile),'--corpus',str(corpus)]
            command=[sys.executable,str(ROOT/'cycle.py')]
            enc=subprocess.run(command+['forward',str(src),str(wire),*args],capture_output=True)
            self.assertEqual(enc.returncode,0,enc.stderr.decode())
            src.unlink()
            dec=subprocess.run(command+['reverse',str(wire),str(out),*args],capture_output=True)
            self.assertEqual(dec.returncode,0,dec.stderr.decode())
            self.assertEqual(out.read_bytes(),raw)
            again=subprocess.run(command+['reverse',str(wire),str(out),*args],capture_output=True)
            self.assertEqual(again.returncode,2)
            self.assertEqual(out.read_bytes(),raw)

    def test_profile_roundtrip_and_all_accounting_fields(self):
        lock = json.loads((ROOT/'CYCLE_NATIVE.json').read_text())
        graph = json.loads((ROOT/'CYCLE_WORK_GRAPH.json').read_text())
        payload = {k: graph[k] for k in ('repositories', 'boundaries')}
        from hashlib import sha256
        digest = sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        self.assertEqual(digest, graph['work_graph_sha256'])
        repositories = {x['repository']: x for x in graph['repositories']}
        self.assertEqual(repositories['The-Interdependency/uchc']['commit'], lock['uchc_architecture']['commit'])
        self.assertEqual(repositories['The-Interdependency/ucns']['commit'], lock['ucns_commit'])
        self.assertEqual(lock['binary_source']['owner'], 'The-Interdependency/stack')
        self.assertFalse(graph['boundaries']['authority_transfer'])
        self.assertEqual(Profile.read(cycle.canonical(PROFILE.as_dict())),PROFILE)
        wire,stats=forward(b'ABCD'*64,CORPUS,PROFILE,SOURCES)
        for row in stats['rounds']:
            self.assertEqual(row['input_bytes']*8 % 8,0)
            self.assertEqual(row['permutation_bit_count'],row['output_bytes']*8)
            self.assertEqual(row['numeral_bytes']+row['native_coordinate_and_frame_bytes'],row['output_bytes'])
        self.assertEqual(len(wire),stats['total_bytes'])
        self.assertEqual(reverse(wire,CORPUS,PROFILE,SOURCES),b'ABCD'*64)


if __name__=='__main__': unittest.main()
