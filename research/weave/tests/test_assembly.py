"""Assembly witnesses, NOT a cipher/security test suite.

Usage: python -m unittest discover -s tests -p 'test_assembly.py'.
Finite preflight: 512 switch configurations over six synthetic bits; no corpus,
secrets, network or provider calls. Marker operators are explicitly WIRING_ONLY.
"""
from dataclasses import replace
from itertools import product
import unittest
from assembly import DEFAULTS, Pipeline, Switches
from stages import STEPS
from stages.api import Blocked, Operator, PrivateContext, PublicContext, Streams, Transition
from stages.key import keygen

DATA = Streams(((0, 1, 0, 1, 1, 0),))
PARAMS = {'inter': (((2, 2, 2),),)}
PUB = PublicContext('test-public-only', PARAMS)
PRIV = PrivateContext('test-public-only', 'test-private-only', PARAMS)


def markers(log):
    def pair(name):
        def f(value, context):
            log.append(('forward', name))
            return value
        def r(value, context):
            log.append(('inverse', name))
            return value
        return Operator(f, r, 'wiring-fixture/' + name, fixture=True)
    return {s.name: pair(s.name) for s in STEPS if s.builtin is None}


class AssemblyTests(unittest.TestCase):
    def test_all_on_is_blocked_before_input(self):
        touched = []
        handlers = markers(touched)
        del handlers['bind']
        with self.assertRaisesRegex(Blocked, 'bind: Q2/Q7/Q8'):
            Pipeline(operators=handlers, allow_fixtures=True).encrypt(DATA, PUB)
        self.assertEqual(touched, [])

    def test_default_scope_and_six_unresolved_bindings(self):
        plan = Pipeline().plan()
        self.assertFalse(plan['complete_cipher_implemented'])
        self.assertEqual(plan['status'], 'BLOCKED')
        self.assertEqual(len(plan['missing']), 6)
        self.assertFalse(plan['switches']['auth'])
        self.assertTrue(all(plan['switches'][s.name] for s in STEPS if s.required))

    def test_no_native_fixture_promotion(self):
        with self.assertRaisesRegex(Blocked, 'wiring fixture'):
            Pipeline(operators=markers([])).encrypt(DATA, PUB)

    def test_all_512_switches_keep_identity_or_report_incompatibility(self):
        for values in product((False, True), repeat=len(DEFAULTS)):
            flags = dict(zip(DEFAULTS, values))
            p = Pipeline(Switches(flags), markers([]), allow_fixtures=True)
            if flags['bind'] and not (flags['key'] and flags['gonol']):
                with self.assertRaisesRegex(Blocked, 'incompatible ablation'):
                    p.encrypt(DATA, PUB)
                continue
            forward = p.encrypt(DATA, PUB)
            inverse = p.decrypt(forward, PRIV)
            self.assertEqual(inverse.payload, DATA)
            self.assertEqual(dict((n, v) for n,v in p.switches.values.items()), flags)
            self.assertNotEqual(forward.classification, 'FULL_PROFILE_EXPERIMENT')
            for name, status in forward.events:
                self.assertEqual(status == 'OFF', not flags[name])

    def test_inverse_order(self):
        log = []
        p = Pipeline(operators=markers(log), allow_fixtures=True)
        e = p.encrypt(DATA, PUB)
        p.decrypt(e, PRIV)
        forward = [name for direction,name in log if direction == 'forward']
        inverse = [name for direction,name in log if direction == 'inverse']
        self.assertEqual(inverse, list(reversed(forward)))
        self.assertEqual(e.classification, 'WIRING_ONLY')

    def test_cipher_never_receives_private_context(self):
        with self.assertRaisesRegex(TypeError, 'PublicContext only'):
            Pipeline().encrypt(DATA, PRIV)
        self.assertFalse(hasattr(PUB, 'private_key'))

    def test_context_and_run_repr_do_not_expose_material(self):
        self.assertNotIn('test-private-only', repr(PRIV))
        p = Pipeline(Switches({n:False for n in DEFAULTS}))
        e = p.encrypt(b'test-plaintext-not-a-cipher', PUB)
        self.assertNotIn('test-plaintext', repr(e))
        self.assertEqual(e.classification, 'ABLATION_ONLY')

    def test_independent_switch_no_cascade(self):
        config = Switches({'corpus': False})
        self.assertTrue(config['split'])
        self.assertTrue(config['inter'])
        self.assertTrue(config['join'])

    def test_unknown_and_nonboolean_switches_fail(self):
        for flags in ({'corups': False}, {'inter': 0}, {'corpus': 'off'}):
            with self.assertRaises((ValueError, TypeError)):
                Switches(flags)

    def test_no_silent_literal_override(self):
        fake = Operator(lambda x,c:x, lambda x,c:x, 'fake')
        with self.assertRaisesRegex(ValueError, 'cannot be replaced'):
            Pipeline(operators={'inter':fake})

    def test_exact_one_stage_is_accepted_and_reversed(self):
        flags = {n:False for n in DEFAULTS}
        flags['inter'] = flags['whole'] = True
        p = Pipeline(Switches(flags))
        e = p.encrypt(DATA, PUB)
        self.assertEqual(p.decrypt(e, PRIV).payload, DATA)
        self.assertEqual(e.classification, 'ABLATION_ONLY')

    def test_missing_partition_never_guessed(self):
        flags = {n:False for n in DEFAULTS}; flags['inter'] = True
        with self.assertRaisesRegex(Blocked, 'explicit partitions'):
            Pipeline(Switches(flags)).encrypt(DATA, PublicContext(None))

    def test_whole_never_implicitly_joins_threads(self):
        flags = {n:False for n in DEFAULTS}; flags['whole'] = True
        with self.assertRaisesRegex(TypeError, 'already joined'):
            Pipeline(Switches(flags)).encrypt(Streams(((0,1),(1,0))), PUB)

    def test_changed_inverse_switch_mask_rejected(self):
        flags = {n:False for n in DEFAULTS}
        e = Pipeline(Switches(flags)).encrypt(DATA, PUB)
        flags['whole'] = True
        with self.assertRaisesRegex(ValueError, 'recipe'):
            Pipeline(Switches(flags)).decrypt(e, PRIV)

    def test_missing_key_relation_is_not_invented(self):
        with self.assertRaisesRegex(Blocked, 'KeyGen relation'):
            keygen(None, private_gonol=object(), material={}, randomness=b'')

    def test_stage_can_pass_derived_plan_without_exporting_it(self):
        log = []
        ops = markers(log)
        secret_plan = {'inter':PARAMS['inter'], 'do_not_publish':'secret-marker'}
        def forward(value, context):
            return Transition(value, secret_plan)
        ops['corpus'] = Operator(forward, lambda x,c:x, 'wiring-fixture/derived', fixture=True)
        e = Pipeline(operators=ops, allow_fixtures=True).encrypt(DATA, PublicContext('test-public'))
        self.assertNotIn('secret-marker', repr(e))
        self.assertFalse(hasattr(e, 'parameters'))

    def test_key_off_does_not_invoke_keygen(self):
        def forbidden(**kwargs):
            raise AssertionError('disabled generator was called')
        self.assertIsNone(keygen(forbidden, private_gonol=object(), material={},
                                 randomness=b'', enabled=False))

    def test_key_off_removes_keys_from_operator_contexts(self):
        seen = []
        def f(value, context):
            seen.append(context.public_key)
            return value
        def r(value, context):
            seen.extend((context.public_key, context.private_key))
            return value
        flags = {n:False for n in DEFAULTS}; flags['corpus'] = True
        p = Pipeline(Switches(flags), {'corpus':Operator(f,r,'wiring-fixture/keys-off',True)},
                     allow_fixtures=True)
        e = p.encrypt(DATA,PUB)
        p.decrypt(e,PRIV)
        self.assertEqual(seen,[None,None,None])

    def test_streams_reject_bool_and_mutable_input(self):
        for lanes in (((True,),), ([0,1],), []):
            with self.assertRaises(TypeError):
                Streams(lanes)


if __name__ == '__main__':
    unittest.main()
