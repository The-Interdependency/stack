# === CHECKS ===
# id: english_ordinal_union_and_layout
#   proves: english_expanded_repertoire
#   call: self::test_union_and_layout
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary fixture files only
#   cleanup: pytest tmp_path
# id: english_ordinal_supplementary_scalar_not_utf16_units
#   proves: english_expanded_repertoire
#   call: self::test_supplementary_scalar_not_utf16_units
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary fixture files only
#   cleanup: pytest tmp_path
# id: english_ordinal_no_normalization
#   proves: english_expanded_repertoire
#   call: self::test_no_normalization
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary fixture files only
#   cleanup: pytest tmp_path
# id: english_ordinal_wrong_version_refuses
#   proves: english_expanded_repertoire
#   call: self::test_wrong_version_refuses
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary fixture files only
#   cleanup: pytest tmp_path
# id: english_ordinal_missing_property_data_refuses
#   proves: english_expanded_repertoire
#   call: self::test_missing_property_data_refuses
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary fixture files only
#   cleanup: pytest tmp_path
# id: english_ordinal_unclosed_unicode_range_refuses
#   proves: english_expanded_repertoire
#   call: self::test_unclosed_unicode_range_refuses
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary fixture files only
#   cleanup: pytest tmp_path
# id: english_ordinal_invalid_scalar_and_anchor_refusal
#   proves: english_expanded_repertoire
#   call: self::test_invalid_scalar_and_anchor_refusal
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary fixture files only
#   cleanup: pytest tmp_path
# id: english_ordinal_word_and_recursive_record
#   proves: english_recursive_ordinal_geometry
#   call: self::test_word_and_recursive_record
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary fixture files only
#   cleanup: pytest tmp_path
# id: english_ordinal_append_does_not_change_angle
#   proves: english_recursive_ordinal_geometry
#   call: self::test_append_does_not_change_angle
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary fixture files only
#   cleanup: pytest tmp_path
# id: english_ordinal_sql_materialization_and_independent_replay
#   proves: english_complete_geometry_replay
#   call: self::test_sql_materialization_and_independent_replay
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary fixture files only
#   cleanup: pytest tmp_path
# id: english_ordinal_unknown_word_refuses
#   proves: english_recursive_ordinal_geometry
#   call: self::test_unknown_word_refuses
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary fixture files only
#   cleanup: pytest tmp_path
# id: english_ordinal_geometry_producer_bytes_are_bound
#   proves: english_complete_geometry_replay
#   call: self::test_geometry_producer_bytes_are_bound
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary fixture files only
#   cleanup: pytest tmp_path
# === END CHECKS ===

"""Fixture tests are not full Unicode or corpus receipts; hosted build supplies those."""
from fractions import Fraction
import sqlite3
import pytest
from english_gonol.ordinal_construct import (
    Factory, LOGIC, SQL, UNICODE_VERSION, repertoire, scalar, unicode_admission,
    _write_frame, _independent_frame, _producer_check,
)
from ucns.ordinal_affixiation import Carrier, Participant, affixiate


def ucd_fixture(tmp_path):
    rows = []
    for c in '0123456789':
        rows.append(';'.join([f'{ord(c):04X}', 'DIGIT', 'Nd'] + [''] * 12))
    rows.extend([';'.join(['00B2', 'SUPERSCRIPT TWO', 'No'] + [''] * 12),
                 ';'.join(['2160', 'ROMAN NUMERAL ONE', 'Nl'] + [''] * 12)])
    (tmp_path / 'UnicodeData.txt').write_text('\n'.join(rows) + '\n')
    (tmp_path / 'DerivedCoreProperties.txt').write_text(
        f'# DerivedCoreProperties-{UNICODE_VERSION}.txt\n002B ; Math\n003C..003E ; Math\n2200 ; Math\n')
    return tmp_path


def factory_fixture(tmp_path):
    public = repertoire(tuple(' ABCé\u0301'), tuple(' ABC'), ucd_fixture(tmp_path))
    return Factory(public, {1: 'ABA', 2: 'C', 3: 'é', 4: 'A\u0301'}, 'fixture-source')


def test_union_and_layout(tmp_path):
    ucd = ucd_fixture(tmp_path)
    public = repertoire(tuple(' é\u0301'), tuple(' ABC'), ucd)
    values = public['identities']
    assert values[0] == ' '
    assert [c for c in values if c in ' ABC'] == list(' ABC')
    assert set('0123456789²Ⅰé\u0301') | set(LOGIC) <= set(values)
    assert len(values) == len(set(values)) == public['admission_counts']['union']
    anchors = [values.index(c) for c in ' ABC'] + [len(values)]
    counts = [b-a-1 for a,b in zip(anchors, anchors[1:])]
    assert max(counts) - min(counts) <= 1
    assert public == repertoire(tuple(' é\u0301'), tuple(' ABC'), ucd)


def test_supplementary_scalar_not_utf16_units(tmp_path):
    public = repertoire(('𝟠',), tuple(' A'), ucd_fixture(tmp_path))
    assert public['identities'].count('𝟠') == 1
    assert scalar('𝟠') == '𝟠'


def test_no_normalization(tmp_path):
    public = repertoire(('é','e','\u0301'), tuple(' A'), ucd_fixture(tmp_path))
    assert all(c in public['identities'] for c in ('é','e','\u0301'))


def test_wrong_version_refuses(tmp_path):
    root = ucd_fixture(tmp_path)
    path = root / 'DerivedCoreProperties.txt'
    path.write_text(path.read_text().replace(UNICODE_VERSION, '17.0.0'))
    with pytest.raises(ValueError, match='release'):
        unicode_admission(root)


def test_missing_property_data_refuses(tmp_path):
    root = ucd_fixture(tmp_path)
    (root / 'UnicodeData.txt').write_text('')
    with pytest.raises(ValueError, match='incomplete'):
        unicode_admission(root)


def test_unclosed_unicode_range_refuses(tmp_path):
    root = ucd_fixture(tmp_path)
    with (root / 'UnicodeData.txt').open('a') as stream:
        stream.write(';'.join(['3000', '<FIXTURE, First>', 'No'] + ['']*12) + '\n')
    with pytest.raises(ValueError, match='unterminated'):
        unicode_admission(root)


def test_invalid_scalar_and_anchor_refusal(tmp_path):
    root = ucd_fixture(tmp_path)
    for bad in ('', 'ab', '\ud800'):
        with pytest.raises(ValueError):
            repertoire((bad,), tuple(' A'), root)
    for bad in (('A',), (' ', 'A', 'A')):
        with pytest.raises(ValueError):
            repertoire(('A',), bad, root)


def test_word_and_recursive_record(tmp_path):
    factory = factory_fixture(tmp_path)
    word = factory.word(1)
    assert word.recover() == tuple('ABA')
    assert [word.placement(i).radius() for i in range(3)] == [Fraction(1,8),Fraction(1,4),Fraction(1,2)]
    obj = factory.record(1, 'definition', (('word',1),('character',' '),('word',1)))
    assert ''.join(obj.recover()) == 'ABA ABA'
    assert obj.participants[0].interior is obj.participants[2].interior is word
    assert obj.placement(0).turn == factory.word_carrier.turn('ABA')
    assert obj.placement(1).turn == factory.glyph_carrier.turn(' ')
    higher = Carrier((obj.identity,), 'fixture-higher')
    triple = affixiate('higher', (Participant.closed(higher,obj),),
                       origin='SPACE', relation='declared-nesting', source='fixture')
    assert ''.join(triple.recover()) == 'ABA ABA'


def test_append_does_not_change_angle(tmp_path):
    factory = factory_fixture(tmp_path)
    before = factory.record(1,'definition',(('word',1),))
    after = factory.record(2,'definition',(('word',1),('word',2)))
    assert after.placement(0).turn == before.placement(0).turn
    assert after.placement(0).radius() == before.placement(0).radius()/2
    assert after.placement(1).radius() == Fraction(1,2)


def test_sql_materialization_and_independent_replay(tmp_path):
    factory = factory_fixture(tmp_path)
    chars = {i:c for i,c in enumerate(factory.glyph_carrier.identities)}
    ids = {c:i for i,c in chars.items()}
    receipts = {}
    with sqlite3.connect(':memory:') as db:
        db.executescript(SQL)
        for wid, text in factory.words.items():
            refs = tuple(('character',ids[c]) for c in text)
            obj = factory.word(wid)
            _write_frame(db,'word',wid,obj,refs)
            expected, positions = _independent_frame('word',wid,text,'ordered-glyphs',
                factory.source_receipt,refs,factory,chars,receipts)
            assert db.execute('SELECT * FROM frames WHERE kind=? AND id=?',('word',wid)).fetchone() == expected
            assert db.execute('SELECT * FROM placements WHERE kind=? AND id=? ORDER BY ordinal',('word',wid)).fetchall() == positions
            receipts[wid] = obj.receipt
        refs = (('word',1),('character',ids[' ']),('word',2),('word',1))
        obj = factory.record(7,'definition',(('word',1),('character',' '),('word',2),('word',1)))
        _write_frame(db,'record',7,obj,refs)
        expected, positions = _independent_frame('record',7,'definition:7','ordered-definition',
            factory.source_receipt,refs,factory,chars,receipts)
        assert db.execute('SELECT * FROM frames WHERE kind=? AND id=?',('record',7)).fetchone() == expected
        assert db.execute('SELECT * FROM placements WHERE kind=? AND id=? ORDER BY ordinal',('record',7)).fetchall() == positions
        db.execute("UPDATE placements SET exponent=exponent+1 WHERE kind='record' AND ordinal=0")
        assert db.execute('SELECT * FROM placements WHERE kind=? AND id=? ORDER BY ordinal',('record',7)).fetchall() != positions


def test_unknown_word_refuses(tmp_path):
    factory = factory_fixture(tmp_path)
    with pytest.raises(KeyError):
        factory.word(999)


def test_geometry_producer_bytes_are_bound():
    _producer_check()
