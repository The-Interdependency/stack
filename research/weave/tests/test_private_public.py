# ratios: loc_comments=187:106 imports_exports=14:1 calls_definitions=131:22
# === CHECKS ===
# id: check_native_candidate_private_native_states_preserve_full_frame
#   proves: native_private_key_relation
#   call: self::test_private_native_states_preserve_full_frame
#   mutates: none
#   cleanup: none
# id: check_native_candidate_public_artifact_exposes_two_states_and_evaluation_coefficients
#   proves: native_private_key_relation
#   call: self::test_public_artifact_exposes_two_states_and_evaluation_coefficients
#   mutates: none
#   cleanup: none
# id: check_native_candidate_keygen_default_uses_fresh_material
#   proves: native_private_key_relation
#   call: self::test_keygen_default_uses_fresh_material
#   mutates: none
#   cleanup: none
# id: check_native_candidate_expanded_public_law_equals_private_composition
#   proves: native_private_exact_recovery
#   call: self::test_expanded_public_law_equals_private_composition
#   mutates: none
#   cleanup: none
# id: check_native_candidate_sender_never_calls_private_construction_or_inverse
#   proves: public_sender_evaluation
#   call: self::test_sender_never_calls_private_construction_or_inverse
#   mutates: none
#   cleanup: none
# id: check_native_candidate_private_exact_recovery_binary_edge_cases
#   proves: native_private_exact_recovery
#   call: self::test_private_exact_recovery_binary_edge_cases
#   mutates: none
#   cleanup: none
# id: check_native_candidate_every_native_state_materially_changes_binding
#   proves: native_private_key_relation
#   call: self::test_every_native_state_materially_changes_binding
#   mutates: none
#   cleanup: none
# id: check_native_candidate_public_only_attack_recovers_without_private_path
#   proves: public_inverse_falsification
#   call: self::test_public_only_attack_recovers_without_private_path
#   mutates: none
#   cleanup: none
# id: check_native_candidate_public_decomposition_recovers_equivalent_inverse_not_material
#   proves: public_inverse_falsification
#   call: self::test_public_decomposition_recovers_equivalent_inverse_not_material
#   mutates: none
#   cleanup: none
# id: check_native_candidate_private_api_rejects_missing_and_wrong_material
#   proves: candidate_artifact_admission
#   call: self::test_private_api_rejects_missing_and_wrong_material
#   mutates: none
#   cleanup: none
# id: check_native_candidate_non_exact_root_is_refused_without_rounding
#   proves: candidate_artifact_admission
#   call: self::test_non_exact_root_is_refused_without_rounding
#   mutates: none
#   cleanup: none
# id: check_native_candidate_malformed_public_artifacts_are_refused
#   proves: candidate_artifact_admission
#   call: self::test_malformed_public_artifacts_are_refused
#   mutates: none
#   cleanup: none
# id: check_native_candidate_packet_identity_length_and_framing_are_checked
#   proves: candidate_artifact_admission
#   call: self::test_packet_identity_length_and_framing_are_checked
#   mutates: none
#   cleanup: none
# id: check_native_candidate_budgets_and_private_material_admission
#   proves: candidate_artifact_admission
#   call: self::test_budgets_and_private_material_admission
#   mutates: none
#   cleanup: none
# id: check_native_candidate_decomposition_refuses_non_candidate_polynomial
#   proves: candidate_artifact_admission
#   call: self::test_decomposition_refuses_non_candidate_polynomial
#   mutates: none
#   cleanup: none
# id: check_native_candidate_three_round_fresh_process_construction_and_attack
#   proves: candidate_process_boundary
#   call: self::test_three_round_fresh_process_construction_and_attack
#   mutates: filesystem
#   cleanup: tempdir_teardown
# id: check_native_candidate_source_failure_is_error_not_attack_resistance
#   proves: candidate_process_boundary
#   call: self::test_source_failure_is_error_not_attack_resistance
#   mutates: none
#   cleanup: none
# id: check_native_candidate_worker_failure_is_error_not_attack_resistance
#   proves: candidate_process_boundary
#   call: self::test_worker_failure_is_error_not_attack_resistance
#   mutates: filesystem
#   cleanup: tempdir_teardown
# id: check_native_candidate_acceptance_command_fails_on_actual_public_recovery
#   proves: public_inverse_falsification
#   call: self::test_acceptance_command_fails_on_actual_public_recovery
#   mutates: filesystem
#   cleanup: tempdir_teardown
# id: check_native_candidate_cli_infrastructure_error_exits_two
#   proves: candidate_process_boundary
#   call: self::test_cli_infrastructure_error_exits_two
#   mutates: none
#   cleanup: none
# === END CHECKS ===
"""Usage: WEAVE_SOURCES=/checkouts python -m unittest discover -s tests -p test_private_public.py -v.

This suite constructs the explicit native-shift polynomial candidate and records
its public coefficient attack. Green tests mean the falsification is reproduced.
"""
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
import json
import os
import random
import subprocess
import sys
import unittest
from unittest.mock import patch

import private_public as pp
from cycle import Profile, canonical
from numeral import Refused, _blob, _uint

ROOT = Path(__file__).resolve().parents[1]
SOURCES = Path(os.environ.get('WEAVE_SOURCES', ROOT/'sources'))
BASE = Profile.read((ROOT/'profiles'/'cycle-v1.json').read_bytes())
PROFILE = replace(BASE, rounds=BASE.rounds[:1])
CORPUS = b'actual corpus\x00\xff'
MATERIAL = bytes((i*73+41)%256 for i in range(256))


class PrivatePublicTests(unittest.TestCase):
    def setUp(self):
        self.public, self.private = pp.keygen(PROFILE, CORPUS, SOURCES, material=MATERIAL)

    def test_private_native_states_preserve_full_frame(self):
        origin, turns = pp._native(MATERIAL, SOURCES)
        self.assertEqual(len(origin), 64)
        self.assertEqual(len(turns), 8)
        self.assertEqual(turns, tuple(Fraction(MATERIAL[i],256)+(MATERIAL[8+i]&1) for i in range(8)))
        changed = bytearray(MATERIAL); changed[10] ^= 1
        _, other = pp._native(bytes(changed), SOURCES)
        self.assertEqual(abs(other[2]-turns[2]), 1)
        self.assertEqual(abs(pp._offsets(other)[2]-pp._offsets(turns)[2]), 256)

    def test_public_artifact_exposes_two_states_and_evaluation_coefficients(self):
        obj = json.loads(self.public)
        self.assertEqual(set(obj), {'law','key_origin','public_turns','coefficients','profile','corpus_hex','native_lock_sha256'})
        self.assertEqual(len(obj['public_turns']), 2)
        self.assertEqual(len(obj['coefficients']), 65)
        self.assertNotIn('material_hex', obj)
        self.assertEqual(json.loads(self.private), {'law':pp.LAW,'material_hex':MATERIAL.hex()})
        self.assertEqual(obj['profile'], PROFILE.as_dict())
        self.assertEqual(bytes.fromhex(obj['corpus_hex']), CORPUS)

    def test_keygen_default_uses_fresh_material(self):
        alternative = bytes((x+1)%256 for x in MATERIAL)
        with patch.object(pp.secrets,'token_bytes',side_effect=[MATERIAL,alternative]) as entropy:
            a = pp.keygen(PROFILE,CORPUS,SOURCES)
            b = pp.keygen(PROFILE,CORPUS,SOURCES)
        self.assertEqual(entropy.call_args_list[0].args,(256,))
        self.assertNotEqual(a,b)

    def test_expanded_public_law_equals_private_composition(self):
        rng = random.Random(20261006)
        for _ in range(32):
            shifts = tuple(rng.randint(1,512) for _ in range(6))
            coefficients = pp._expand(shifts)
            for x in (0,1,255,65536):
                value = x
                for shift in shifts: value = (value+shift)**2
                self.assertEqual(pp._evaluate(coefficients,x),value)
                self.assertEqual(pp._invert(value,shifts),x)
            self.assertEqual(pp.decompose(coefficients),shifts)

    def test_sender_never_calls_private_construction_or_inverse(self):
        with patch.object(pp,'keygen',side_effect=AssertionError('keygen in sender')), \
             patch.object(pp,'_native',side_effect=AssertionError('private state in sender')), \
             patch.object(pp,'decompose',side_effect=AssertionError('inverse in sender')), \
             patch.object(pp,'recover',side_effect=AssertionError('private recovery in sender')):
            packet = pp.send(b'ABxABy',self.public,SOURCES)
        self.assertEqual(pp.recover(packet,self.public,self.private,SOURCES),b'ABxABy')

    def test_private_exact_recovery_binary_edge_cases(self):
        for message in (b'',b'\x00\x00\x01',bytes(range(256)),b'ABxABy'*8):
            with self.subTest(length=len(message)):
                packet = pp.send(message,self.public,SOURCES)
                self.assertEqual(pp.recover(packet,self.public,self.private,SOURCES),message)

    def test_every_native_state_materially_changes_binding(self):
        packet = pp.send(b'ABxABy',self.public,SOURCES)
        value = pp._packet(packet,self.public)[1]
        for i in range(8):
            changed = bytearray(MATERIAL); changed[i] = (changed[i]+1)%256
            public, private = pp.keygen(PROFILE,CORPUS,SOURCES,material=bytes(changed))
            other = pp.send(b'ABxABy',public,SOURCES)
            self.assertNotEqual(pp._packet(other,public)[1],value)
            self.assertEqual(pp.recover(other,public,private,SOURCES),b'ABxABy')

    def test_public_only_attack_recovers_without_private_path(self):
        message = b'ABxABy\x00ABxABy'
        packet = pp.send(message,self.public,SOURCES)
        with patch.object(pp,'keygen',side_effect=AssertionError('attacker keygen')), \
             patch.object(pp,'_native',side_effect=AssertionError('attacker private states')), \
             patch.object(pp,'recover',side_effect=AssertionError('attacker private API')):
            self.assertEqual(pp.public_recover(packet,self.public,SOURCES),message)

    def test_public_decomposition_recovers_equivalent_inverse_not_material(self):
        _, turns = pp._native(MATERIAL,SOURCES)
        recovered = pp.decompose(json.loads(self.public)['coefficients'])
        self.assertEqual(recovered,pp._offsets(turns)[2:])
        self.assertEqual(len(recovered),6)
        self.assertNotEqual(recovered,tuple(MATERIAL))

    def test_private_api_rejects_missing_and_wrong_material(self):
        packet = pp.send(b'message',self.public,SOURCES)
        for private in (None,b'',self.public,canonical({'law':pp.LAW,'material_hex':'00'*256})):
            with self.assertRaises(Refused): pp.recover(packet,self.public,private,SOURCES)
        self.assertEqual(pp.public_recover(packet,self.public,SOURCES),b'message')

    def test_non_exact_root_is_refused_without_rounding(self):
        packet = pp.send(b'message',self.public,SOURCES)
        length,y = pp._packet(packet,self.public)
        encoded = (y+1).to_bytes(((y+1).bit_length()+7)//8,'big')
        damaged = packet[:36]+_uint(length)+_blob(encoded)
        with self.assertRaisesRegex(Refused,'non-exact square'):
            pp.recover(damaged,self.public,self.private,SOURCES)
        with self.assertRaises(Refused): pp.public_recover(damaged,self.public,SOURCES)

    def test_malformed_public_artifacts_are_refused(self):
        obj = json.loads(self.public)
        variants=[]
        for key,value in [('law','other'),('material_hex',MATERIAL.hex()),('public_turns',[[0,1]]),
                          ('coefficients',[1]),('native_lock_sha256','0'*64),('corpus_hex','AA'),
                          ('key_origin','ab')]:
            bad=deepcopy(obj); bad[key]=value; variants.append(canonical(bad))
        bad=deepcopy(obj); bad['public_turns'][0]=[2,4]; variants.append(canonical(bad))
        bad=deepcopy(obj); bad['coefficients'][0]=True; variants.append(canonical(bad))
        bad=deepcopy(obj); bad['coefficients'][0]=-1; variants.append(canonical(bad))
        variants += [b'{"law":1,"law":2}',b'[]',b'\xff',b'x'*65537,json.dumps(obj,indent=2).encode()]
        for value in variants:
            with self.assertRaises(Refused): pp.send(b'm',value,SOURCES)

    def test_packet_identity_length_and_framing_are_checked(self):
        packet=pp.send(b'message',self.public,SOURCES)
        variants=[packet[:-1],packet+b'!',packet[:36]+_uint(pp.MAX_RECORD+1)+_blob(b'\x01'),
                  packet[:36]+_uint(1)+_blob(b'\x00\x01'),b'x'*(pp.MAX_WIRE+1)]
        corrupted=bytearray(packet); corrupted[4]^=1; variants.append(bytes(corrupted))
        for value in variants:
            with self.assertRaises(Refused): pp.public_recover(value,self.public,SOURCES)

    def test_budgets_and_private_material_admission(self):
        for material in (b'',b'x'*255,b'x'*257,'text'):
            with self.assertRaises(Refused): pp.keygen(PROFILE,CORPUS,SOURCES,material=material)
        for corpus in (b'',b'x'*4097,'text'):
            with self.assertRaises(Refused): pp.keygen(PROFILE,corpus,SOURCES,material=MATERIAL)
        with self.assertRaises(Refused): pp.send(b'x'*257,self.public,SOURCES)
        with self.assertRaises(Refused): pp.keygen(replace(BASE,rounds=BASE.rounds*2),CORPUS,SOURCES,material=MATERIAL)

    def test_decomposition_refuses_non_candidate_polynomial(self):
        coefficients=json.loads(self.public)['coefficients']
        for index in (0,1,63):
            altered=coefficients.copy(); altered[index]+=1
            with self.assertRaises(Refused): pp.decompose(altered)

    def test_three_round_fresh_process_construction_and_attack(self):
        calls=[]
        private_inputs=[]
        original=pp._run
        def observe(root,operation,public,data,private=None):
            self.assertEqual(private is not None,operation=='recover')
            files={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
            self.assertFalse(any('profile' in p or 'test_' in p for p in files))
            if private is not None:
                private_inputs.append(json.loads(private)['material_hex'])
            calls.append(operation)
            return original(root,operation,public,data,private)
        with patch.object(pp,'_run',side_effect=observe):
            report=pp.experiment(b'ABxABy\x00ABxABy',BASE,CORPUS,SOURCES)
        self.assertEqual(calls,['send','recover','public-recover'])
        self.assertEqual(report['status'],'FALSIFIED')
        self.assertTrue(report['public_sender_completed'])
        self.assertTrue(report['private_recovery_exact'])
        self.assertTrue(report['public_recovery_exact'])
        self.assertFalse(report['private_material_given_to_attacker'])
        self.assertFalse(report['distinction_established'])
        self.assertEqual(set(report['source_files']),set(pp.RUNTIME)|{
            'inputs/ucns/src/ucns/axis_circle.py','inputs/ucns/src/ucns/direct_mobius.py'})
        self.assertEqual(len(private_inputs),1)
        self.assertNotIn(private_inputs[0].encode(),canonical(report))

    def test_source_failure_is_error_not_attack_resistance(self):
        with patch.object(pp,'load_native',side_effect=Refused('missing native source')):
            with self.assertRaisesRegex(Refused,'missing native source'):
                pp.experiment(b'm',PROFILE,CORPUS,SOURCES,material=MATERIAL)

    def test_worker_failure_is_error_not_attack_resistance(self):
        result=subprocess.CompletedProcess([],2,b'',b'infrastructure failure')
        with patch.object(pp.subprocess,'run',return_value=result):
            with self.assertRaisesRegex(RuntimeError,'worker failed'):
                pp.experiment(b'm',PROFILE,CORPUS,SOURCES,material=MATERIAL)

    def test_acceptance_command_fails_on_actual_public_recovery(self):
        result=subprocess.run([sys.executable,str(ROOT/'private_public.py'),'--sources',str(SOURCES),
                               '--require-distinction'],capture_output=True)
        self.assertEqual(result.returncode,1,result.stderr.decode())
        report=json.loads(result.stdout)
        self.assertEqual(report['status'],'FALSIFIED')
        self.assertTrue(report['public_recovery_exact'])
        self.assertFalse(report['distinction_established'])

    def test_cli_infrastructure_error_exits_two(self):
        result=subprocess.run([sys.executable,str(ROOT/'private_public.py'),'--sources','/missing-weave-sources'],
                              capture_output=True)
        self.assertEqual(result.returncode,2)
        self.assertEqual(result.stdout,b'')
        self.assertIn(b'experiment error',result.stderr)


if __name__=='__main__': unittest.main()
# ratios: loc_comments=187:106 imports_exports=14:1 calls_definitions=131:22
