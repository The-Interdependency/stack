"""Tests for ptcna.seed.constants — composition counts and the coherence-prime guard."""
from __future__ import annotations

import unittest

from ptcna.seed.constants import (
    HEPTAGRAM_VERTICES,
    NOMINAL_CIRCLES_PER_SEED,
    SEED_ROUTING_STEP,
    coherence_primes_up_to,
    is_coherence_prime,
    nth_coherence_prime,
)


class TestRoutingMotif(unittest.TestCase):
    def test_routing_motif(self):
        # The heptagram is the routing motif (nominal n=7, {7/3}); it is NOT a
        # required circle count — composition counts are variable.
        self.assertEqual(HEPTAGRAM_VERTICES, 7)
        self.assertEqual(NOMINAL_CIRCLES_PER_SEED, 7)
        self.assertEqual(SEED_ROUTING_STEP, 3)


class TestCoherencePrimeGuard(unittest.TestCase):
    def test_base_set(self):
        for p in (3, 5, 7):
            self.assertTrue(is_coherence_prime(p))

    def test_ladder_prefix(self):
        # Canonical ladder: 3, 5, 7, 13, 29, 53, 61, 157, 349, 421, ...
        expected = [3, 5, 7, 13, 29, 53, 61, 157, 349, 421]
        self.assertEqual(coherence_primes_up_to(421), expected)

    def test_nth(self):
        self.assertEqual(nth_coherence_prime(0), 3)
        self.assertEqual(nth_coherence_prime(5), 53)
        self.assertEqual(nth_coherence_prime(6), 61)

    def test_p4373_regression(self):
        # The frozen-universe approximation (cap 421) diverges here: 4373's
        # kernel 1093 is itself a coherence prime above the cap. The recursive
        # rule must admit it.
        self.assertTrue(is_coherence_prime(4373))
        self.assertTrue(is_coherence_prime(1093))

    def test_non_members(self):
        self.assertFalse(is_coherence_prime(2))    # even; not p % 4 == 1
        self.assertFalse(is_coherence_prime(11))   # 11 % 4 == 3
        self.assertFalse(is_coherence_prime(9))    # not prime
        self.assertFalse(is_coherence_prime(1))
        self.assertFalse(is_coherence_prime(-5))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
