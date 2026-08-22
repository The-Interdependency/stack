"""Executable witnesses for the symbol-abbreviation coupling."""

# === CHECKS ===
# id: check_symbol_every_letter_instance_has_oriented_hub_coupling
#   proves: symbol_every_letter_instance_has_oriented_hub_coupling
#   call: self::test_every_letter_instance_has_zx_and_zy
#   mutates: none
#   cleanup: none
#
# id: check_symbol_gonol_preserves_exact_abbreviation
#   proves: symbol_gonol_preserves_exact_abbreviation
#   call: self::test_symbol_gonol_preserves_exact_abbreviation
#   mutates: none
#   cleanup: none
#
# id: check_symbol_coupling_arity_two
#   proves: symbol_coupling_arity_two
#   call: self::test_symbol_coupling_arity_two
#   mutates: none
#   cleanup: none
#
# id: check_symbol_coupling_replays_byte_identical
#   proves: symbol_coupling_replays_byte_identical
#   call: self::test_symbol_coupling_replays_byte_identical
#   mutates: none
#   cleanup: none
#
# id: check_symbol_coupling_stays_cross_domain_hypothesis
#   proves: symbol_coupling_stays_cross_domain_hypothesis
#   call: self::test_symbol_coupling_stays_cross_domain_hypothesis
#   mutates: none
#   cleanup: none
# === END CHECKS ===

import symbol_coupling as m


def test_every_letter_instance_has_zx_and_zy():
    hydrogen = m.construct_symbol_gonol("H")
    helium = m.construct_symbol_gonol("He")
    iron = m.construct_symbol_gonol("Fe")
    h_ids = [item["declared_ids"] for item in hydrogen.gonol.couplings]
    assert len(h_ids) == 1
    assert h_ids[0][0] == hydrogen.gonol.source_id
    assert h_ids[0][1] == hydrogen.gonol.participants[0].source_id
    assert helium.gonol.structure["participating_dimension_count"] == 3
    assert helium.gonol.structure["ternary_coupling_declared"] is False
    assert [item["declared_ids"][0] for item in helium.gonol.couplings] == [
        helium.gonol.source_id,
        helium.gonol.source_id,
    ]
    assert [item["declared_ids"][1] for item in helium.gonol.couplings] == [
        helium.gonol.participants[0].source_id,
        helium.gonol.participants[1].source_id,
    ]
    assert [item["slot_charges"] for item in helium.gonol.couplings] == [[2, None], [2, None]]
    assert [item["slot_charges"] for item in iron.gonol.couplings] == [[26, None], [26, None]]


def test_symbol_gonol_preserves_exact_abbreviation():
    h = m.construct_symbol_gonol("H").gonol
    assert h.identity_glyph is None  # two participants? no — H closes from one char
    assert len(h.participants) == 1
    assert dict(h.carried_options)["abbreviation-length"] == "1"

    he = m.construct_symbol_gonol("He").gonol
    assert len(he.participants) == 2
    assert [p.identity_glyph for p in he.participants] == ["H", "e"]
    assert dict(he.carried_options)["abbreviation-length"] == "2"

    fe = m.construct_symbol_gonol("Fe").gonol
    assert [p.identity_glyph for p in fe.participants] == ["F", "e"]


def test_symbol_coupling_arity_two():
    for symbol in ("H", "He", "Fe"):
        receipt = m.couple_symbol(symbol)
        assert len(receipt.gonol.participants) == 2
        assert dict(receipt.gonol.carried_options)["symbol"] == symbol
        coupling = receipt.gonol.couplings[0]
        assert coupling["relation"] == "epac.symbol-coupling"
        assert coupling["arity"] == 2
        assert len(coupling["dimensions"]) == 2


def test_symbol_coupling_replays_byte_identical():
    digests = set()
    for symbol in m.SUPPORTED_SYMBOLS:
        receipt = m.couple_symbol(symbol)
        assert m.replay_symbol_coupling(receipt) == receipt.receipt_digest
        digests.add(receipt.receipt_digest)
    assert len(digests) == len(m.SUPPORTED_SYMBOLS)


def test_symbol_coupling_stays_cross_domain_hypothesis():
    receipt = m.couple_symbol("Fe")
    assert receipt.standing == "implemented-candidate"
    assert receipt.selection_effect == "none"
