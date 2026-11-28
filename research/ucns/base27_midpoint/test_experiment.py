"""Review witnesses. Usage: python -m unittest -v from the experiment directory."""
import unittest
from itertools import combinations
from math import isqrt
from unittest.mock import patch

import experiment as e


class Geometry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=e.geometry_report()

    def test_full_circle_cubes(self):
        actual=set()
        for c in range(e.M):
            a,b=pow(c-1,3,e.M),pow(c+1,3,e.M)
            if (b-a)%e.M==2:
                actual.add(c)
                self.assertEqual((a,b),((3*c-1)%e.M,(3*c+1)%e.M))
        self.assertEqual(actual,set(range(0,e.M,81)))
        self.assertEqual(self.report['cube_mismatch_count'],0)
        self.assertEqual(self.report['exhaustive_direct_cube_checks'],19683)

    def test_mutant_cube_formula_detected(self):
        original=e.pair_cubes
        def shifted_pair(c,modulus=e.M):
            a,b=original(c,modulus)
            return a,(b+1)%modulus
        with patch.object(e,'pair_cubes',side_effect=shifted_pair):
            self.assertGreater(e.geometry_report()['cube_mismatch_count'],0)

    def test_fibers(self):
        groups=e.partition(e.eligible(9),e.bearing)
        self.assertEqual(e.summarize(groups)['size_histogram'],{3:81})
        for group in groups:
            self.assertEqual(len(group),3)
            self.assertEqual(sorted((b-a)%e.M for a,b in combinations(group,2)),[6561,6561,13122])

    def test_worked_examples(self):
        self.assertEqual([r['input_spoke'] for r in self.report['worked_examples']],[7452,14013,891])
        self.assertEqual([tuple(r['cubes']) for r in self.report['worked_examples']],[(2672,2674)]*3)

    def test_radius_controls(self):
        r=self.report['radius_and_controls']
        self.assertEqual(r['bearing_only'],r['constant_radius'])
        self.assertEqual(r['bearing_only'],r['bearing_dependent_radius'])
        self.assertEqual(r['bearing_only'],r['bearing_repeated'])
        self.assertEqual(r['two_explicit_radial_layers']['size_histogram'],{1:81,2:81})
        self.assertEqual(r['three_explicit_radial_layers']['size_histogram'],{1:243})
        self.assertEqual(r['three_explicit_radial_layers'],r['identity_control'])
        self.assertEqual(r['constant_control']['size_histogram'],{243:1})

    def test_explicit_retained_label(self):
        for c in e.eligible(9):
            self.assertEqual(e.retained_label_roundtrip(e.bearing(c),e.exact_sector(c)),c)
            for wrong in range(3):
                if wrong!=e.exact_sector(c):
                    self.assertNotEqual(e.retained_label_roundtrip(e.bearing(c),wrong),c)
        self.assertEqual(self.report['retained_label'],{'correct':243,'total':243,'wrong_labels':486,'wrong_labels_equal_original':0})

    def test_invalid_input_rejected(self):
        for y,sector in ((1,0),(-243,0),(19683,0),(0,3),(0,-1),(False,0),(0,False),(0,1.0)):
            with self.subTest(y=y,sector=sector),self.assertRaises(ValueError):
                e.retained_label_roundtrip(y,sector)
        for c in (-81,1,19683,True,81.0):
            with self.subTest(c=c),self.assertRaises(ValueError):
                e.exact_sector(c)
        for n in (0,-1,1.0,True):
            with self.assertRaises(ValueError): e.eligible(n)
        for m in (0,1,-3,1.2):
            with self.assertRaises(ValueError): e.pair_cubes(81,m)

    def test_moduli(self):
        for m,control in self.report['moduli'].items():
            m=int(m)
            for scale,key in ((1,'canonical_midpoint_observation'),(3,'transformed_midpoint_observation')):
                step=scale*6561
                expected=({3:81} if step%m==0 else {1:81,2:81} if (2*step)%m==0 else {1:243})
                self.assertEqual(control[key]['size_histogram'],expected,(m,key))

    def test_recursion_saturation(self):
        for d in range(8):
            actual=self.report['recursion'][str(d)]
            self.assertEqual(actual['classes'],3**max(5-d,0))
            self.assertEqual(actual['size_histogram'],{3**min(d,5):3**max(5-d,0)})
        self.assertEqual(self.report['recursion']['5'],self.report['recursion']['7'])

    def test_interlacing_is_not_new_information(self):
        r=self.report['interlacing_control']
        self.assertTrue(r['swap_preserves_partition'])
        self.assertTrue(r['omission_only_coarsens'])
        self.assertEqual(r['two_coordinate_vector'],r['fixed_swap'])
        self.assertEqual(r['omit_first_coordinate']['size_histogram'],{243:1})
        ip=r['independent_product']
        self.assertTrue(ip['swap_preserves_partition'])
        self.assertTrue(ip['omission_only_coarsens'])
        self.assertEqual(ip['two_coordinate_vector']['size_histogram'],{9:6561})
        self.assertEqual(ip['fixed_swap'],ip['two_coordinate_vector'])
        self.assertEqual(ip['omit_first_coordinate']['size_histogram'],{729:81})
        # A false equality must be detected; a deletion is not a permutation.
        self.assertFalse(e.same_partition(e.partition(range(6),lambda i:i%2),e.partition(range(6),lambda i:0)))

    def test_scale_counts(self):
        for a in (5,7,9,11,13,15):
            d=e.eligible(a)
            v=e.summarize(e.partition(d,lambda c:e.bearing(c,3**a)))
            self.assertEqual(v['objects'],3**(a-a//2))
            self.assertEqual(v['size_histogram'],{3:len(d)//3})


class CensusTests(unittest.TestCase):
    def test_odd_sieve_against_trial_division(self):
        for limit in (5,6,31,100,101,1000):
            flags=e.odd_sieve(limit)
            test_prime=lambda n:n>=2 and all(n%k for k in range(2,isqrt(n)+1))
            self.assertEqual([2*i+1 for i,v in enumerate(flags) if v],[n for n in range(3,limit+1,2) if test_prime(n)])

    def test_twin_ordinals_independent_small_reference(self):
        limit=10000
        primes=[n for n in range(2,limit+1) if all(n%k for k in range(2,isqrt(n)+1))]
        reference=[(p+1,i) for i,(p,q) in enumerate(zip(primes,primes[1:]),1) if p>3 and q-p==2]
        self.assertEqual(list(e.twin_records(limit)),reference)
        self.assertEqual(list(e.twin_records(7)),[(6,3)])

    def test_census_accounting(self):
        r=e.census_report(100000)['first_interval']
        self.assertEqual(r['direct_cube_mismatches'],0)
        self.assertEqual(sum(x['total'] for x in r['all_output_families']),r['eligible_pairs'])
        for x in r['all_output_families']:
            self.assertEqual(len(x['family_counts']),3)
            self.assertEqual(sum(x['family_counts']),x['total'])
        self.assertEqual(r['ordinal_difference_counts'],{1:r['eligible_pairs']})

    def test_mutant_cube_census_detected(self):
        c=e.Census()
        with patch.object(e,'pair_cubes',return_value=(0,0)):
            c.add(46818,1)
        self.assertEqual(c.report()['direct_cube_mismatches'],1)

if __name__=='__main__':
    unittest.main()
