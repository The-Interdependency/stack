from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from ahbg.engine.errors import ValidationError
from ahbg.engine.rng import DM_DOMAIN, RngStream

SAMPLE = [1, 2, 3, 4, 5]


class RngStreamTests(unittest.TestCase):
    def test_same_seed_same_sequence(self) -> None:
        a = RngStream(seed=42)
        b = RngStream(seed=42)
        self.assertEqual([a.next_u64() for _ in range(8)], [b.next_u64() for _ in range(8)])

    def test_different_seed_different_sequence(self) -> None:
        a = [RngStream(seed=1).next_u64() for _ in range(4)]
        b = [RngStream(seed=2).next_u64() for _ in range(4)]
        self.assertNotEqual(a, b)

    def test_substream_is_deterministic_and_independent(self) -> None:
        parent = RngStream(seed=9)
        child_a = parent.substream("war")
        parent.next_u64()  # drawing from the parent must not move the child
        child_b = RngStream(seed=9).substream("war")
        self.assertEqual(
            [child_a.next_u64() for _ in range(5)],
            [child_b.next_u64() for _ in range(5)],
        )

    def test_randbelow_bounds_and_determinism(self) -> None:
        a = RngStream(seed=5)
        b = RngStream(seed=5)
        for _ in range(20):
            value_a = a.randbelow(6)
            value_b = b.randbelow(6)
            self.assertIn(value_a, range(6))
            self.assertEqual(value_a, value_b)

    def test_choice_is_deterministic(self) -> None:
        a = RngStream(seed=11)
        b = RngStream(seed=11)
        self.assertEqual([a.choice(SAMPLE) for _ in range(6)], [b.choice(SAMPLE) for _ in range(6)])

    def test_domain_constants_exist(self) -> None:
        self.assertEqual(DM_DOMAIN, "dm")
        self.assertIsInstance(RngStream(seed=0).substream("dm"), RngStream)

    def test_invalid_seed_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValidationError, "non-negative"):
            RngStream(seed=-1)

    def test_invalid_randbelow_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValidationError, "positive"):
            RngStream(seed=1).randbelow(0)


if __name__ == "__main__":
    unittest.main()
