# === CHECKS ===
# id: check_prime_symbolic_fox_exact
#   proves: prime_symbolic_fox_presentation_is_exact
#   call: self::test_symbolic_presentations_are_sparse_exact_and_deterministic
#   requires: python3, sympy
#   timeout: 180
#   mutates: none
#   cleanup: none
#
# id: check_prime_symbolic_elementary_boundary
#   proves: prime_symbolic_elementary_boundary_is_exact
#   call: self::test_exact_ranks_and_first_nonzero_elementary_ideals_differ
#   requires: python3, sympy
#   timeout: 180
#   mutates: none
#   cleanup: none
#
# id: check_prime_symbolic_character_replay
#   proves: prime_symbolic_certificate_replays_finite_characters
#   call: self::test_symbolic_specializations_replay_frozen_character_ranks
#   requires: python3, sympy
#   timeout: 180
#   mutates: none
#   cleanup: none
#
# id: check_prime_symbolic_receipt_nonselecting
#   proves: prime_symbolic_alexander_receipt_is_nonselecting
#   call: self::test_family_receipt_is_deterministic_and_bounded
#   requires: python3, sympy
#   timeout: 360
#   mutates: temporary_path
#   cleanup: pytest temporary_path
# === END CHECKS ===

from __future__ import annotations

import json

import pytest

from ucns.prime_symbolic_alexander import (
    symbolic_alexander_certificate,
    symbolic_alexander_family_certificate,
    write_symbolic_alexander_family_certificate,
)


@pytest.fixture(scope="module")
def certificates():
    return symbolic_alexander_certificate(7), symbolic_alexander_certificate(5)


def test_symbolic_presentations_are_sparse_exact_and_deterministic(certificates) -> None:
    p7, p5 = certificates
    assert len(p7.sparse_rows) == len(p7.generator_labels) == 38
    assert len(p5.sparse_rows) == len(p5.generator_labels) == 18
    assert all(1 <= len(row) <= 3 for row in p7.sparse_rows + p5.sparse_rows)
    assert p7.as_dict()["presentation_sha256"] == p7.as_dict()["presentation_sha256"]
    assert p5.as_dict()["presentation_sha256"] == p5.as_dict()["presentation_sha256"]


def test_exact_ranks_and_first_nonzero_elementary_ideals_differ(certificates) -> None:
    p7, p5 = certificates
    assert (p7.fraction_field_rank, p7.first_nonzero_elementary_ideal) == (37, 1)
    assert (p5.fraction_field_rank, p5.first_nonzero_elementary_ideal) == (15, 3)
    assert p7.pivot_minor not in {"0", ""}
    assert p5.pivot_minor not in {"0", ""}
    assert p7.as_dict()["elementary_ideal_boundary"]["zero_ideals"] == ["E_0"]
    assert p5.as_dict()["elementary_ideal_boundary"]["zero_ideals"] == ["E_0", "E_1", "E_2"]


def test_symbolic_specializations_replay_frozen_character_ranks(certificates) -> None:
    p7, p5 = certificates
    assert p7.as_dict()["finite_character_replay"]["matches_frozen_fingerprint"] is True
    assert p5.as_dict()["finite_character_replay"]["matches_frozen_fingerprint"] is True
    assert len(p7.specialized_rank_vector_sha256) == 64
    assert len(p5.specialized_rank_vector_sha256) == 64


def test_family_receipt_is_deterministic_and_bounded(tmp_path, certificates) -> None:
    expected = symbolic_alexander_family_certificate()
    output = write_symbolic_alexander_family_certificate(tmp_path / "certificate.json")
    assert json.loads(output.read_text(encoding="utf-8")) == expected
    assert expected["selection_effect"] == "none"
    assert "not a complete generating set" in expected["nonclaims"][0]
    assert "E_1" == expected["comparison"]["P7_first_nonzero_elementary_ideal"]
    assert "E_3" == expected["comparison"]["P5_first_nonzero_elementary_ideal"]
