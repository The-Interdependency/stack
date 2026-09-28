"""Executable provisional composition tests, not native Weave security acceptance.

Usage: python -m unittest discover -s tests. Fixed scope: 8,191 binary messages;
32 transport switch masks; separate-process byte recovery; bounded resource and
malformed-input checks. Temporary nonsecret corpus fixtures only. No network.
"""
from copy import deepcopy
from dataclasses import replace
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from assembly import DEFAULTS, Pipeline, Switches
from stages.api import Blocked, Operator, PrivateContext, PublicContext, Streams
from stages.gonol import NativeWords
from stages import corpus, inter, join, split
from transport import build, byte_stream, recover_bytes, LIMIT
from lab import wire, unwire, strict_json, parse_lanes
from probe import inward, section_stage, recover_fixed_map, recover_with_map

ROOT = Path(__file__).resolve().parents[1]
PROFILE = json.loads((ROOT/'profiles/transport.json').read_text())
MATERIAL = {'a': b'Actual literary-like fixture.', 'b': bytes(range(64)), 'c': b'\x00\xff\x55\xaa'}


def flags(**changes):
    p = deepcopy(PROFILE)
    p['switches'].update(changes)
    return p


def two_way(data, profile=PROFILE, material=MATERIAL):
    p, public, _ = build(deepcopy(profile), len(data), dict(material))
    encoded = p.encrypt(Streams((data,)), public)
    # Build an independent context; pass no earlier Transition or stage snapshot.
    q, _, private = build(deepcopy(profile), len(data), dict(material))
    decoded = q.decrypt(unwire(wire(encoded), q), private)
    return encoded, decoded


class TransportTests(unittest.TestCase):
    def test_complete_profile_still_refuses(self):
        with self.assertRaises(Blocked):
            Pipeline().encrypt(b'not touched', PublicContext(None))
        self.assertEqual(len(Pipeline().plan()['missing']), 6)

    def test_no_native_promotion_by_switching_flags(self):
        p = flags(key=True, gonol=True, bind=True)
        with self.assertRaises(Blocked):
            build(p, 32, MATERIAL)

    def test_full_transport_all_8191_binary_messages(self):
        count = 0
        for n in range(13):
            for value in range(1 << n):
                data = tuple((value >> i) & 1 for i in range(n))
                encoded, decoded = two_way(data)
                self.assertEqual(decoded.payload, Streams((data,)))
                self.assertEqual(encoded.classification, 'TRANSPORT_CANDIDATE')
                self.assertEqual(sum(map(len, encoded.payload.lanes)), n)
                count += 1
        self.assertEqual(count, 8191)

    def test_all_32_transport_masks(self):
        valid = invalid = 0
        names = ('split','corpus','inter','join','whole')
        data = tuple((i*i + i//3) % 2 for i in range(137))
        for bits in product((False, True), repeat=5):
            p = flags(**dict(zip(names, bits)))
            if not p['switches']['split']:
                # Explicitly adapt this test recipe to one lane; no runner cascade.
                p['corpus'], p['arities'], p['join_order'] = [['a',0]], [[5,7,3]], [0]
            if p['switches']['split'] and not p['switches']['join'] and p['switches']['whole']:
                with self.assertRaisesRegex(ValueError, 'incompatible ablation'):
                    build(p, len(data), MATERIAL)
                invalid += 1
                continue
            encoded, decoded = two_way(data, p)
            self.assertEqual(decoded.payload, Streams((data,)))
            for name, status in encoded.events:
                self.assertEqual(status == 'EXECUTED', p['switches'][name])
            valid += 1
        self.assertEqual((valid, invalid), (28,4))

    def test_balanced_sizes_and_empty_sections(self):
        for n in range(513):
            for a in (3,5,7,11,31):
                plan = inter.balanced_partition(n,a)
                self.assertEqual(sum(plan), n)
                self.assertEqual(len(plan), a)
                self.assertLessEqual(max(plan)-min(plan),1)
                ids = tuple(range(n))
                self.assertEqual(inter.section(inter.section(ids,plan),plan,True),ids)
        self.assertEqual(inter.balanced_partition(2,5),(1,1,0,0,0))
        self.assertEqual(inter.balanced_partition(0,3),(0,0,0))

    def test_old_equal_section_behavior_preserved(self):
        for n in (105,210,840):
            for a in (3,5,7):
                ids = tuple(range(n)); lengths = (n//a,)*a
                self.assertEqual(inter.section(ids,lengths),section_stage(ids,lengths))

    def test_one_stage_not_three_stages(self):
        p = deepcopy(PROFILE); p['arities'] = [[3],[5],[7]]
        data = tuple(i%2 for i in range(61))
        self.assertEqual(two_way(data,p)[1].payload,Streams((data,)))

    def test_corpus_content_really_changes_route(self):
        self.assertEqual(corpus.route(7,b'\x00'),tuple(range(7)))
        self.assertEqual(corpus.route(7,b'\xff'),tuple(reversed(range(7))))
        self.assertEqual(corpus.route(7,b'\xaa'),(6,0,5,1,4,2,3))
        data = tuple([1,0,1,1,0,0,0]*17)
        a = two_way(data,material={'a':b'\x00','b':b'\x00','c':b'\x00'})[0]
        b = two_way(data,material={'a':b'\xff','b':b'\xff','c':b'\xff'})[0]
        self.assertNotEqual(a.payload,b.payload)

    def test_material_names_do_not_act_as_keys(self):
        p = deepcopy(PROFILE)
        p['corpus'] = [['x',0],['y',1],['z',2]]
        renamed = dict(zip(('x','y','z'),(MATERIAL['a'],MATERIAL['b'],MATERIAL['c'])))
        data = tuple(i%2 for i in range(137))
        self.assertEqual(two_way(data)[0].payload,two_way(data,p,renamed)[0].payload)

    def test_corpus_off_has_no_material_influence(self):
        p = flags(corpus=False)
        data = tuple(i%2 for i in range(137))
        self.assertEqual(two_way(data,p,{})[0].payload,two_way(data,p,MATERIAL)[0].payload)
        _, public, private = build(p,len(data),MATERIAL)
        self.assertEqual(dict(public.public_material),{})
        self.assertEqual(dict(private.public_material),{})
        self.assertNotIn('corpus',public.parameters)

    def test_disabled_stage_not_called(self):
        def forbidden(*args):
            raise AssertionError('disabled stage executed')
        off = {n:False for n in DEFAULTS}
        p = Pipeline(Switches(off), {'corpus':Operator(forbidden,forbidden,'test/forbidden')})
        value = b'exact unchanged opaque object'
        e = p.encrypt(value,PublicContext(None))
        self.assertIs(e.payload,value)

    def test_join_order_and_empty_lanes(self):
        self.assertEqual(join.route((2,0,1),(2,0,1)),(2,0,0))
        self.assertEqual(join.route((0,0,0),(0,1,2)),())
        for sizes in product(range(4),repeat=3):
            r = join.route(sizes,(2,0,1))
            self.assertEqual(tuple(r.count(i) for i in range(3)),sizes)

    def test_bad_routes_and_partitions_refused(self):
        for bad in ((0,0,1),(True,1,2),(3,1,0)):
            with self.assertRaises(ValueError):join.route((1,2,3),bad)
        for bad in ((1,1,-1),(True,1,1),(1,1),(0,0,0)):
            with self.assertRaises(ValueError):inter.section((0,1,0),bad)
        for n,a in ((True,3),(1,True),(-1,3),(1,2)):
            with self.assertRaises(ValueError):inter.balanced_partition(n,a)
        with self.assertRaises(ValueError):corpus.route(3,b'')
        with self.assertRaises(ValueError):corpus.route(3,b'a',True)

    def test_unknown_and_nonboolean_profile_fields_refused(self):
        for p in (flags(corups=False),flags(inter=0),flags(corpus='false')):
            with self.assertRaises((ValueError,TypeError)):build(p,16,MATERIAL)
        p=deepcopy(PROFILE);p['typo']=1
        with self.assertRaises(ValueError):build(p,16,MATERIAL)

    def test_missing_material_never_an_identity(self):
        with self.assertRaises(Blocked):build(PROFILE,32,{})

    def test_wrong_material_is_not_authenticated(self):
        data = tuple([1,0,1,1,0,0,0]*17)
        p,pub,_ = build(PROFILE,len(data),{'a':b'\x00','b':b'\x00','c':b'\x00'})
        e = p.encrypt(Streams((data,)),pub)
        q,_,priv = build(PROFILE,len(data),{'a':b'\xff','b':b'\xff','c':b'\xff'})
        decoded = q.decrypt(e,priv)
        self.assertNotEqual(decoded.payload,Streams((data,)))
        self.assertNotEqual(decoded.classification,'FULL_PROFILE_EXPERIMENT')

    def test_fixed_map_attack_only_on_this_complete_transport_profile(self):
        n=137
        p,pub,_=build(PROFILE,n,MATERIAL)
        def oracle(bits):return p.encrypt(Streams((bits,)),pub).payload.lanes[0]
        mapping,queries=recover_fixed_map(oracle,n)
        data=tuple((i*i+i//3)%2 for i in range(n))
        self.assertEqual(recover_with_map(oracle(data),mapping),data)
        self.assertEqual(queries,8)

    def test_packet_rejects_malformed_data_and_recipe(self):
        p,pub,_=build(PROFILE,8,MATERIAL)
        e=p.encrypt(byte_stream(b'A'),pub)
        obj=json.loads(wire(e));obj['recipe'][0][1]='invented'
        with self.assertRaises(ValueError):unwire(json.dumps(obj).encode(),p)
        for records in ([{'bits':1,'hex':'ff'}],[{'bits':True,'hex':'00'}],[],
                        [{'bits':8,'hex':'FF'}],[{'bits':8,'hex':'00','other':1}]):
            with self.assertRaises(ValueError):parse_lanes(records)
        with self.assertRaises(ValueError):strict_json('{"x":1,"x":2}')

    def test_byte_admission_is_explicit_not_a_gonol(self):
        data=bytes(range(256))+b'\x00\xff'
        self.assertEqual(recover_bytes(byte_stream(data)),data)
        self.assertIsInstance(byte_stream(data),Streams)
        with self.assertRaises(ValueError):recover_bytes(Streams(((1,),)))

    def test_native_missing_and_wrong_source_refuse_before_execution(self):
        with self.assertRaises(Blocked):
            with NativeWords(Path('/nonexistent/source'),Path('/nonexistent/db'),'0'*64):pass
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'native.py';database=root/'construct.db'
            marker=root/'executed'
            source.write_text(f"open({str(marker)!r}, 'w').write('bad')")
            database.write_bytes(b'not a real constructed database')
            with self.assertRaisesRegex(Blocked,'not imported'):
                with NativeWords(source,database,'0'*64):pass
            self.assertFalse(marker.exists())

    def test_resource_boundary_is_explicit(self):
        with self.assertRaisesRegex(ValueError,'resource limit'):build(PROFILE,LIMIT*8+1,MATERIAL)
        p=deepcopy(PROFILE);p['arities'][0]=[4097]
        with self.assertRaisesRegex(ValueError,'resource profile'):build(p,8,MATERIAL)

    def test_full_resource_limit_roundtrip(self):
        data = bytes(range(256)) * 256
        p, public, _ = build(PROFILE, len(data)*8, MATERIAL)
        e = p.encrypt(byte_stream(data), public)
        q, _, private = build(deepcopy(PROFILE), len(data)*8, dict(MATERIAL))
        restored = q.decrypt(unwire(wire(e), q), private)
        self.assertEqual(recover_bytes(restored.payload), data)

    def test_fresh_process_roundtrip_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config=root/'p.json';src=root/'i.bin';dst=root/'o.lab';out=root/'r.bin'
            config.write_text(json.dumps(PROFILE)); data=bytes(range(256))*4+b'\x00\xff'
            src.write_bytes(data);args=[]
            for label,content in MATERIAL.items():
                path=root/(label+'.bin');path.write_bytes(content)
                args+=['--material',f'{label}={path}']
            enc=[sys.executable,str(ROOT/'run.py'),'enc',str(config),str(src),str(dst),*args]
            dec=[sys.executable,str(ROOT/'run.py'),'dec',str(config),str(dst),str(out),*args]
            first=subprocess.run(enc,capture_output=True,text=True)
            self.assertEqual(first.returncode,0,first.stderr)
            src.unlink() # The original input is not available to the recovery process.
            second=subprocess.run(dec,capture_output=True,text=True)
            self.assertEqual(second.returncode,0,second.stderr)
            self.assertEqual(out.read_bytes(),data)
            again=subprocess.run(dec,capture_output=True,text=True)
            self.assertEqual(again.returncode,2)
            self.assertEqual(out.read_bytes(),data)

    def test_off_corpus_does_not_read_supplied_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config=root/'p.json';src=root/'i';dst=root/'o'
            config.write_text(json.dumps(flags(corpus=False)));src.write_bytes(b'test')
            result=subprocess.run([sys.executable,str(ROOT/'run.py'),'enc',str(config),str(src),
                str(dst),'--material','a=/nonexistent/never-read'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)


if __name__=='__main__':unittest.main()
