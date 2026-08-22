"""Tests for ptcna.seed.compose / ptcna.seed.tensor — the circles -> seed operator."""
from __future__ import annotations

import unittest

from ptcna.circle import compose_circle
from ptcna.seed import (
    CircleTensor,
    Seed,
    SeedMotion,
    build_seed,
    compose_seed,
    heptagram_order,
    seed_motion,
)


class TestHeptagramOrder(unittest.TestCase):
    def test_known_orders(self):
        self.assertEqual(heptagram_order(2), [0, 2, 4, 6, 1, 3, 5])
        self.assertEqual(heptagram_order(3), [0, 3, 6, 2, 5, 1, 4])

    def test_single_cycle_visits_every_vertex(self):
        self.assertEqual(sorted(heptagram_order(3)), list(range(7)))

    def test_non_coprime_step_rejected(self):
        # gcd(7, 7) == 7 -> not a single cycle.
        with self.assertRaises(ValueError):
            heptagram_order(7, 7)


class TestComposeSeed(unittest.TestCase):
    def _circles(self, n=7):
        return [
            compose_circle([f"w{i}"], identity=f"c{i}")
            for i in range(n)
        ]

    def test_empty_rejected(self):
        with self.assertRaises(ValueError):
            compose_seed([])  # a seed needs at least one circle

    def test_compose_assigns_heptagram_anchors(self):
        seed = compose_seed(self._circles(7))
        self.assertIsInstance(seed, Seed)
        self.assertEqual(seed.n_circles, 7)
        self.assertEqual(seed.anchor_order, tuple(heptagram_order(3)))
        # input circle i lands at the {7/3} heptagram position order[i]
        order = heptagram_order(3)
        for i in range(7):
            self.assertEqual(seed.at(order[i]).identity, f"c{i}")

    def test_variable_circle_counts(self):
        # Composition counts are variable — any number of circles composes; the
        # only invariant is that the seed is itself a tensor.
        for n in (1, 2, 3, 5, 7, 13):
            seed = compose_seed(self._circles(n))
            self.assertEqual(seed.n_circles, n)
            # every circle is recoverable losslessly at some anchor
            self.assertEqual(
                {c.identity for c in seed.circles},
                {f"c{i}" for i in range(n)},
            )

    def test_star_polygon_when_coprime_else_identity(self):
        # n=5, step 3: gcd(3,5)==1 -> {5/3} star order
        self.assertEqual(compose_seed(self._circles(5)).anchor_order,
                         tuple(heptagram_order(3, 5)))
        # n=3, step 3: gcd(3,3)!=1 -> identity order
        self.assertEqual(compose_seed(self._circles(3)).anchor_order, (0, 1, 2))

    def test_lossless_payload_roundtrip(self):
        seed = compose_seed(self._circles(7))
        payloads = {
            c.identity: c.tensor_payloads()[0]
            for c in seed.circles
        }
        self.assertEqual(payloads["c0"], "w0")
        self.assertEqual(payloads["c6"], "w6")

    def test_non_differentiable(self):
        seed = compose_seed(self._circles(7))
        self.assertFalse(seed.requires_grad)
        self.assertFalse(seed.circles[0].requires_grad)


class TestBuildSeedAndMotion(unittest.TestCase):
    def test_build_seed_from_payloads(self):
        seed = build_seed([f"weights{i}" for i in range(7)], identity="seed:13")
        self.assertEqual(seed.identity, "seed:13")
        self.assertEqual(seed.n_circles, 7)
        self.assertEqual(seed.at(0).identity, "seed:13.c0")

    def test_seed_motion_is_structural_only(self):
        seed = build_seed([f"w{i}" for i in range(7)], identity="seed:13")
        motion = seed_motion(seed)
        self.assertIsInstance(motion, SeedMotion)
        self.assertEqual(motion.seed_identity, "seed:13")
        self.assertEqual(motion.routing_step, 3)
        self.assertEqual(motion.anchor_order, tuple(heptagram_order(3)))
        # circle identities are reported in heptagram order, carrying no weights
        self.assertEqual(len(motion.circle_identities), 7)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
