# ratios: loc_comments=215:34 imports_exports=23:2 calls_definitions=136:14
"""Independent coverage/disclosure witnesses; no attacker success is inferred.

Run: python test_harness.py --private /operator --receipt /operator/harness.json
Add --require-full-weave to enforce the unmet complete-system obligations (exit 2).
The normal harness can pass while that separate completeness gate fails.
"""
# === CHECKS ===
# id: matrix_denominator
#   proves: declared_census
#   call: self::Harness.test_exhaustive_pairs_and_cap
#   mutates: none
#   cleanup: none
# id: message_boundary
#   proves: frozen_prediction
#   call: self::Harness.test_frozen_messages_and_fresh_receivers
#   mutates: temporary directory
#   cleanup: TemporaryDirectory
# id: disclosure_boundary
#   proves: staged_disclosure, exact_grading
#   call: self::Harness.test_export_levels_and_standalone_receiver
#   mutates: temporary directory
#   cleanup: TemporaryDirectory
# id: native_components
#   proves: exact_operations, receiver_inputs_only
#   call: self::Harness.test_native_eight_circle_roundtrip
#   mutates: none
#   cleanup: none
# id: typed_order_refusal
#   proves: typed_transport
#   call: self::Harness.test_all_declared_transport_refusals
#   mutates: none
#   cleanup: none
# === END CHECKS ===
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
import zipfile
import operations as o
import matrix
import release
import transport_cases as t
from affixiation import discover
from assembly import Pipeline
from stages import key, bind, auth
from stages.api import Blocked
from twin_ray_engine import TwinRayEngine

PRIVATE = None
OBSERVATIONS = {}


class Harness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = json.loads((PRIVATE/'private.json').read_text())['cases']
        cls.p = matrix.parameters({'family': 'byte'})
        cls.raw = bytes(range(256))*3

    def test_exhaustive_pairs_and_cap(self):
        schedules = {tuple(r['schedule']) for r in self.rows if r['family']=='byte'}
        for a, b in combinations(matrix.CORE, 2):
            expected = {word for n in range(2, 7) for word in product((a,b), repeat=n)
                        if 1 <= word.count(a) <= 3 and 1 <= word.count(b) <= 3}
            self.assertEqual(len(expected), 62)
            self.assertTrue(expected <= schedules)
        for op in matrix.CORE:
            for n in (1,2,3):
                self.assertIn((op,)*n, schedules)
        self.assertEqual(len(self.rows), len(matrix.schedules()))
        for row in self.rows:
            self.assertLessEqual(max(Counter(row['schedule']).values()), 3)
        for invalid in ([], ['B']*4):
            with self.assertRaises(ValueError):
                o.execute(b'123', invalid, self.p)

    def test_frozen_messages_and_fresh_receivers(self):
        self.assertEqual(len({r['id'] for r in self.rows}), len(self.rows))
        nonces = set()
        for row in self.rows:
            message = bytes.fromhex(row['message_hex'])
            first, second, end = message.decode().split('\n')
            self.assertEqual(second, matrix.LINE); self.assertEqual(end, '')
            self.assertTrue(first.startswith('Prediction '))
            nonce = first[11:43]
            self.assertEqual(len(bytes.fromhex(nonce)), 16); nonces.add(nonce)
            r = json.loads((PRIVATE/'receipts'/f"{row['id']}.json").read_text())
            self.assertEqual(r['status'], 'VERIFIED'); self.assertTrue(r['fresh_receiver'])
            wire = (PRIVATE/'ciphertexts'/f"{row['id']}.bin").read_bytes()
            self.assertEqual(sha256(wire).hexdigest(), r['wire_sha256'])
        self.assertEqual(len(nonces), len(self.rows))

    def test_all_declared_transport_refusals(self):
        accepted, refused = matrix.transport_schedules()
        for seq, initial in refused:
            p = {**self.p, 'initial_lanes': initial}
            with self.assertRaises(ValueError):
                t.contexts(1024, seq, p)
        for seq, initial in accepted:
            t.contexts(1024, seq, {**self.p, 'initial_lanes': initial})
        OBSERVATIONS['typed_order_refusals'] = len(refused)

    def test_no_implicit_reflection_padding(self):
        with self.assertRaises(ValueError):
            o.transform(b'four', 'R', self.p)
        for op in ('R', 'B'):
            once = o.transform(self.raw, op, self.p)
            twice = o.transform(once, op, self.p)
            self.assertEqual(twice, self.raw)
            self.assertNotEqual(once, self.raw)
        self.assertEqual(o.execute(self.raw, ['B','R'], self.p), o.execute(self.raw, ['R','B'], self.p))
        OBSERVATIONS['equivalent_schedules_witnessed'] = ['BB=identity', 'RR=identity', 'BR=RB', 'BBB=B', 'RRR=R']

    def test_discovery_independent_and_in_affixiation(self):
        samples = [b'', b'ABxABy', b'ABCD'*20, bytes(range(256)), b'aaaaaaa']
        for raw in samples:
            partition = discover(raw)
            self.assertEqual(b''.join(partition.blocks[i] for i in partition.order), raw)
            if raw:
                self.assertEqual(o.transform(o.transform(raw, 'A', self.p), 'A', self.p, True), raw)
        repeated = discover(b'ABCD'*20)
        self.assertTrue(repeated.repeat_ids)
        OBSERVATIONS['sequence_discovery'] = 'Independent partition restoration and native A composition witnessed.'

    def test_native_eight_circle_roundtrip(self):
        api, geometry = o.native()
        blocks = tuple(bytes([i, i+32]) for i in range(1, 8))
        order = tuple(range(7))+tuple(reversed(range(7)))
        raw = b''.join(blocks[i] for i in order)
        origin = api.ByteOrigin(raw, 'component-eight-circles', 0, geometry)
        circles = tuple(range(1,8)); spaces = tuple(Fraction(i+1, 19) for i in range(8))
        table = api.close_sequences(origin, blocks, order, circles, spaces)
        items = table.wire_occurrences()
        counts = tuple(sum(item.circle==c for _,item in items) for c in range(1,8))
        recovered = api.recover_sequences(geometry, scope=origin.scope,
            message_origin=origin.message_origin, round_id=0, origin_identity=origin.identity,
            byte_length=len(raw), blocks=blocks, circles=circles, spaces=spaces, counts=counts,
            wire_order=tuple(i for i,_ in items),
            source_turns=tuple(api.Geometry.lift(geometry,item.source_state) for _,item in items))
        self.assertEqual(recovered.restore(), raw); self.assertTrue(all(counts))
        OBSERVATIONS['native_circles'] = {'whole_origin_circle': True, 'occurrence_circles': list(range(1,8))}

    def test_numerals_radix_spans_and_prime_index(self):
        examples = [(o.numeral.PrimePath(13, (('span',2,0,2),('next',))), (13,3,5)),
                    (o.numeral.PrimePath(5381, (('span',10,0,2),('next',),('next',))), (5381,53,241,1523))]
        for path, expected in examples:
            self.assertEqual(path.replay(), expected)
            block = o.numeral.BitBlock(expected[-1], expected[-1].bit_length())
            entry = o.numeral.Entry('\ue000', block, Fraction(1,7), 2, path)
            packet = o.numeral.Packet('recipe-component', 0, (entry,), entry.symbol*3)
            self.assertEqual(o.numeral.decode(o.numeral.encode(packet)).restore(), packet.restore())
            route = o.prime.Route.evaluate(path)
            for arities in ((3,), (5,), (7,), (3,5,7)):
                plan = o.prime.plan(len(self.raw)*8, route, arities)
                for ends in ('first-last', 'last-first'):
                    wire = o.prime.interleave(self.raw, plan, end_order=ends)
                    self.assertEqual(o.prime.interleave(wire, plan, inverse=True, end_order=ends), self.raw)
        OBSERVATIONS['prime_components'] = 'Exact base-2/base-10 spans, prime-index recursion, recipe numeral and section routes witnessed.'

    def test_corpus_refusal_does_not_imply_secrecy(self):
        wire = o.transform(self.raw, 'N', self.p)
        wrong = {**self.p, 'corpus_hex': '00'}
        with self.assertRaises(ValueError):
            o.transform(wire, 'N', wrong, True)
        with self.assertRaises(ValueError):
            o.transform(wire, 'N', {**self.p, 'corpus_hex': ''}, True)
        size = int.from_bytes(wire[4:12], 'big')
        self.assertEqual(wire[44:44+size], self.raw)
        self.assertEqual(o.transform(o.transform(self.raw, 'U', self.p), 'U', {}, True), self.raw)
        OBSERVATIONS['corpus_boundary'] = 'Official wrong/missing corpus refusal; corpus-free extraction from normalized frame still succeeds.'

    def test_missing_laws_and_lossy_carrier_stay_unmet(self):
        with self.assertRaises(Blocked):
            key.keygen(None, private_gonol=None, material=None, randomness=b'')
        self.assertFalse(hasattr(bind, 'forward')); self.assertFalse(hasattr(auth, 'forward'))
        self.assertTrue(Pipeline().problems())
        engine = TwinRayEngine([3,5,7])
        left, right = engine.encrypt(b'one'), engine.encrypt(b'two')
        self.assertEqual(engine.public_face(left), engine.public_face(right))
        self.assertEqual(engine.decrypt(left), b'one')
        self.assertEqual(engine.decrypt(right), b'two')
        OBSERVATIONS['unmet_full_weave'] = matrix.MISSING
        OBSERVATIONS['twin_ray'] = 'Different messages have identical public faces; full private records contain message-bearing fields. No recoverable public-face challenge claimed.'

    def test_export_levels_and_standalone_receiver(self):
        # Evaluate every case's clue projections; copied artifacts are additionally
        # exercised end-to-end on each distinct family and every release level.
        for row in self.rows:
            p = row['parameters']
            for level in range(7):
                text = release.clue_text(row, level)
                self.assertNotIn(row['message_hex'], text)
                self.assertNotIn(p['corpus_hex'], text)
                self.assertEqual(matrix.LINE in text, level >= 4)
            self.assertNotIn('corpus_hex', release.structural(p))
        for family in sorted({r['family'] for r in self.rows}):
            row = next(r for r in self.rows if r['family']==family)
            with tempfile.TemporaryDirectory() as temporary:
                base = Path(temporary)
                for level in range(7):
                    out = release.export(PRIVATE, row['id'], level, base/f'l{level}')
                    self.assertEqual((out/'source').exists(), level >= 2)
                    self.assertEqual((out/'structure.json').exists(), level >= 3)
                    self.assertEqual((out/'parameters-without-corpus.json').exists(), level >= 5)
                    self.assertEqual((out/'request.json').exists(), level >= 6)
                    if level == 0:
                        self.assertEqual({p.name for p in out.iterdir()}, {'README.md','challenge.bin'})
                    with self.assertRaises(ValueError):
                        release.export(PRIVATE, row['id'], level, out)
                out = base/'l6'
                command = [sys.executable, '-I', '-B', str(out/'source/research/weave/recovery-challenges/v2/operations.py'),
                           'receive', '--request', str(out/'request.json'), '--output', str(out/'restored.bin')]
                ran = subprocess.run(command, capture_output=True, close_fds=True)
                self.assertEqual(ran.returncode, 0, ran.stderr.decode())
                self.assertTrue(release.grade(PRIVATE, row['id'], out/'restored.bin')['exact'])
                (out/'partial.bin').write_text(matrix.LINE)
                self.assertFalse(release.grade(PRIVATE, row['id'], out/'partial.bin')['exact'])
                with self.assertRaises(ValueError):
                    release.export(PRIVATE, row['id'], 0, PRIVATE/'bad-release')
                with self.assertRaises(ValueError):
                    release.export(PRIVATE, row['id'], 7, base/'l7')
        OBSERVATIONS['disclosures'] = {'case_level_text_checks': len(self.rows)*7,
            'materialized_family_level_exports': 28, 'standalone_last_level_receivers': 4}

    def test_public_archive_contains_only_admitted_artifacts(self):
        with zipfile.ZipFile(o.HERE/'blind-pack.zip') as archive:
            expected = {'README.md', 'SHA256SUMS'} | {f"files/{r['id']}.bin" for r in self.rows}
            self.assertEqual(set(archive.namelist()), expected)
            self.assertEqual(len(archive.namelist()), len(expected))
            for row in self.rows:
                name = row['id']+'.bin'
                self.assertEqual(archive.read('files/'+name), (PRIVATE/'ciphertexts'/name).read_bytes())
            readme = archive.read('README.md').decode()
            self.assertNotIn(matrix.LINE, readme)
            self.assertNotIn('Weave', readme)
        OBSERVATIONS['public_boundary'] = 'All 1841 exact wire outputs plus only generic README and ciphertext checksums; no extra answer artifacts.'


def main():
    global PRIVATE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--private', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--require-full-weave', action='store_true')
    args = parser.parse_args(); PRIVATE = args.private
    start = time.monotonic()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Harness))
    receipt = {'tests': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
        'harness_passed': result.wasSuccessful(), 'full_weave_coverage': 'INCOMPLETE',
        'seconds': round(time.monotonic()-start, 3), 'observations': OBSERVATIONS}
    args.receipt.write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({k: v for k,v in receipt.items() if k!='observations'}))
    if not result.wasSuccessful():
        return 1
    return 2 if args.require_full_weave else 0


if __name__ == '__main__':
    raise SystemExit(main())
# ratios: loc_comments=215:34 imports_exports=23:2 calls_definitions=136:14
