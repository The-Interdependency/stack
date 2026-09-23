"""Executable evidence for the bounded URPCS v1 reference profile."""

# === CHECKS ===
# id: check_urpcs_reference_self_test
#   proves: urpcs_bounded_roundtrip, urpcs_authenticated_fail_closed
#   call: self::check_reference_self_test
#   requires: python3
#   timeout: 120
#   mutates: none
#   cleanup: none
#
# id: check_urpcs_committed_vectors
#   proves: urpcs_vectors_are_canonical
#   call: self::check_committed_vectors
#   requires: python3
#   timeout: 120
#   mutates: none
#   cleanup: none
#
# id: check_urpcs_one_byte_domain
#   proves: urpcs_bounded_roundtrip
#   call: self::check_all_one_byte_roundtrips
#   requires: python3
#   timeout: 120
#   mutates: none
#   cleanup: none
# === END CHECKS ===

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE))

import urpcs_v1_reference as ref  # noqa: E402


def check_reference_self_test() -> None:
    ref.self_test()


def check_committed_vectors() -> None:
    expected = (WORKSPACE / "vectors" / "urpcs-v1-vectors.json").read_text(
        encoding="utf-8"
    )
    generated = json.dumps(ref.generate_vectors(), indent=2, sort_keys=True) + "\n"
    assert generated == expected


def check_all_one_byte_roundtrips() -> None:
    state = ref.vector_state(0)
    for value in range(256):
        plaintext = bytes([value])
        encrypted = ref.encrypt(plaintext, state, ref.VECTOR_AD)
        decrypted = ref.decrypt(encrypted.ciphertext, state, ref.VECTOR_AD)
        assert decrypted.plaintext == plaintext
        assert decrypted.receipt == encrypted.receipt
        assert decrypted.next_state == encrypted.next_state


class URPCSReferenceTests(unittest.TestCase):
    def test_reference_self_test(self) -> None:
        check_reference_self_test()

    def test_committed_vectors(self) -> None:
        check_committed_vectors()

    def test_all_one_byte_roundtrips(self) -> None:
        check_all_one_byte_roundtrips()


if __name__ == "__main__":
    unittest.main()
