"""Regression tests for the bounded URPCS v1 post-merge review repairs.

Usage:
    python -m unittest research.urpcs.tests.test_postmerge_review
    python -m unittest discover -s research/urpcs/tests -p 'test*.py'
"""

from __future__ import annotations

import sys
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch


WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE))

import urpcs_v1_reference as ref  # noqa: E402


class URPCSPostMergeReviewTests(unittest.TestCase):
    def test_decoder_rejects_unused_declared_origin(self) -> None:
        state = ref.vector_state(0)
        encrypted = ref.encrypt(b"", state, ref.VECTOR_AD)
        witness = ref.decode_dcbor(encrypted.beta)
        extra_origin = ref.origin_id(state, 0, 1)
        witness[1][0] = ref._row_sort(
            witness[1][0] + [[ref.n_bytes(0), ref.n_bytes(1), extra_origin]]
        )
        beta = ref.encode_witness(witness)
        body = encrypted.c0[ref.BOOT_HEADER_LEN + len(encrypted.beta):]
        c0 = ref.boot_header(len(beta)) + beta + body
        ciphertext = ref.frame(c0, ref.tag(state, c0, ref.VECTOR_AD))

        with self.assertRaisesRegex(ref.CodecFail, "origin/region completeness"):
            ref.decrypt(ciphertext, state, ref.VECTOR_AD)

    def test_oversized_c0_is_rejected_before_authentication(self) -> None:
        state = ref.vector_state(0)
        with patch.object(ref, "MAX_C0", 32):
            ciphertext = ref.frame_header(33) + (b"x" * 33) + (b"\x00" * ref.TAG_LEN)
            with patch.object(ref, "tag", side_effect=AssertionError("tag called")):
                with self.assertRaisesRegex(ref.CodecFail, "C0 cap"):
                    ref.decrypt(ciphertext, state, ref.VECTOR_AD)

    def test_state_slot_has_exactly_one_concurrent_winner(self) -> None:
        class SlowExpected:
            def __ne__(self, other: object) -> bool:
                time.sleep(0.05)
                return self is not other

        expected = SlowExpected()
        slot = ref.StateSlot(expected)  # type: ignore[arg-type]
        barrier = threading.Barrier(3)

        def contend(replacement: object) -> bool:
            barrier.wait()
            return slot.commit(expected, replacement)  # type: ignore[arg-type]

        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(contend, object()), pool.submit(contend, object())]
            barrier.wait()
            results = [future.result(timeout=2) for future in futures]

        self.assertEqual(sum(results), 1)


if __name__ == "__main__":
    unittest.main()
