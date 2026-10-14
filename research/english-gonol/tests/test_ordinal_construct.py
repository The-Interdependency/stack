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
# id: english_ordinal_release_hash_binding
#   proves: english_expanded_repertoire
#   call: self::test_fixture_cannot_claim_production_release
#   requires: python3, pytest
#   timeout: 60
#   mutates: temporary fixture files only
#   cleanup: pytest tmp_path
# id: english_ordinal_manifest_claim_binding
#   proves: english_complete_geometry_replay
#   call: self::test_modified_manifest_refuses_before_source_replay
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
    Factory, LOGIC, SQL, UCD_FILES, scalar, _parse_unicode_properties, _layout_repertoire,
    _write_frame, _independent_frame, _producer_check,
)
from ucns.ordinal_affixiation import Carrier, Participant, affixiate
from english_gonol import ordinal_construct as implementation

FIXTURE_VERSION = 'fixture-not-a-unicode-release'


def ucd_fixture(tmp_path):
    rows = []
    for c in '0123456789':
        rows.append(';'.join([f'{ord(c):04X}', 'DIGIT', 'Nd'] + [''] * 12))
    rows.extend([';'.join(['00B2', 'SUPERSCRIPT TWO', 'No'] + [''] * 12),
                 ';'.join(['2160', 'ROMAN NUMERAL ONE', 'Nl'] + [''] * 12)])
    (tmp_path / 'UnicodeData.txt').write_text('\n'.join(rows) + '\n')
    (tmp_path / 'DerivedCoreProperties.txt').write_text(
        f'# DerivedCoreProperties-{FIXTURE_VERSION}.txt\n002B ; Math\n003C..003E ; Math\n2200 ; Math\n')
    return tmp_path


def parse_fixture(path):
    return _parse_unicode_properties({name: (path / name).read_bytes() for name in UCD_FILES},
                                     FIXTURE_VERSION)


def fixture_repertoire(corpus, legacy, path):
    numbers, maths, hashes = parse_fixture(path)
    return _layout_repertoire(corpus, legacy, numbers, maths, hashes, FIXTURE_VERSION)


def factory_fixture(tmp_path):
    public = fixture_repertoire(tuple(' ABCé\u0301'), tuple(' ABC'), ucd_fixture(tmp_path))
    return Factory(public, {1: 'ABA', 2: 'C', 3: 'é', 4: 'A\u0301'}, 'fixture-source')


def test_union_and_layout(tmp_path):
    ucd = ucd_fixture(tmp_path)
    public = fixture_repertoire(tuple(' é\u0301'), tuple(' ABC'), ucd)
    values = public['identities']
    assert values[0] == ' '
    assert [c for c in values if c in ' ABC'] == list(' ABC')
    assert set('0123456789²Ⅰé\u0301') | set(LOGIC) <= set(values)
    assert len(values) == len(set(values)) == public['admission_counts']['union']
    anchors = [values.index(c) for c in ' ABC'] + [len(values)]
    counts = [b-a-1 for a,b in zip(anchors, anchors[1:])]
    assert max(counts) - min(counts) <= 1
    assert public == fixture_repertoire(tuple(' é\u0301'), tuple(' ABC'), ucd)


def test_supplementary_scalar_not_utf16_units(tmp_path):
    public = fixture_repertoire(('𝟠',), tuple(' A'), ucd_fixture(tmp_path))
    assert public['identities'].count('𝟠') == 1
    assert scalar('𝟠') == '𝟠'


def test_no_normalization(tmp_path):
    public = fixture_repertoire(('é','e','\u0301'), tuple(' A'), ucd_fixture(tmp_path))
    assert all(c in public['identities'] for c in ('é','e','\u0301'))


def test_wrong_version_refuses(tmp_path):
    root = ucd_fixture(tmp_path)
    path = root / 'DerivedCoreProperties.txt'
    path.write_text(path.read_text().replace(FIXTURE_VERSION, '17.0.0'))
    with pytest.raises(ValueError, match='release'):
        parse_fixture(root)


def test_missing_property_data_refuses(tmp_path):
    root = ucd_fixture(tmp_path)
    (root / 'UnicodeData.txt').write_text('')
    with pytest.raises(ValueError, match='incomplete'):
        parse_fixture(root)


def test_unclosed_unicode_range_refuses(tmp_path):
    root = ucd_fixture(tmp_path)
    with (root / 'UnicodeData.txt').open('a') as stream:
        stream.write(';'.join(['3000', '<FIXTURE, First>', 'No'] + ['']*12) + '\n')
    with pytest.raises(ValueError, match='unterminated'):
        parse_fixture(root)


def test_invalid_scalar_and_anchor_refusal(tmp_path):
    root = ucd_fixture(tmp_path)
    for bad in ('', 'ab', '\ud800'):
        with pytest.raises(ValueError):
            fixture_repertoire((bad,), tuple(' A'), root)
    for bad in (('A',), (' ', 'A', 'A')):
        with pytest.raises(ValueError):
            fixture_repertoire(('A',), bad, root)


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


def test_fixture_cannot_claim_production_release(tmp_path):
    root = ucd_fixture(tmp_path)
    # Even the expected production header and minimum ASCII values are insufficient.
    path = root / 'DerivedCoreProperties.txt'
    path.write_text(path.read_text().replace(FIXTURE_VERSION, implementation.UNICODE_VERSION))
    with pytest.raises(ValueError, match='release hash mismatch'):
        implementation.unicode_admission(root)
    with pytest.raises(ValueError, match='release hash mismatch'):
        implementation.repertoire(('A',), (' ', 'A'), root)


def test_fixture_layout_is_not_labelled_as_unicode_release(tmp_path):
    assert factory_fixture(tmp_path).public['unicode_version'] == FIXTURE_VERSION


def manifest_fixture():
    from pathlib import Path
    return {
        'schema': implementation.PROFILE, 'source_receipt': 'a' * 64,
        'source': {'fixture': True}, 'ucns_commit': implementation.UCNS_COMMIT,
        'implementation_sha256': implementation.file_hash(Path(implementation.__file__)),
        'public_sha256': 'b' * 64, 'glyph_carrier_receipt': 'c' * 64,
        'word_carrier_receipt': 'd' * 64, 'counts': {'frames': 1, 'placements': 1},
        'geometry_receipt': 'e' * 64, 'character_definitions_receipt': 'f' * 64,
        'hmmm': list(implementation.MANIFEST_BOUNDARIES),
    }


def test_manifest_shape_check_is_not_full_verification():
    # This checks only the schema. No source or geometry survival claim is emitted.
    assert implementation._validate_manifest(manifest_fixture()) is None


@pytest.mark.parametrize('mutation', [
    lambda m: m.pop('hmmm'),
    lambda m: m.update(hmmm=[]),
    lambda m: m.update(hmmm=['everything is proven']),
    lambda m: m.update(canonical=True),
    lambda m: m.update(proof_status='SURVIVED'),
    lambda m: m.update(counts={'frames': True, 'placements': 1}),
    lambda m: m.update(counts={'frames': 1, 'placements': 1, 'extra': 1}),
    lambda m: m.update(source_receipt='not a digest'),
])
def test_modified_manifest_refuses_before_source_replay(tmp_path, mutation):
    value = manifest_fixture()
    mutation(value)
    implementation._json_write(tmp_path / 'manifest.json', value)
    with pytest.raises(ValueError, match='manifest'):
        implementation.verify(tmp_path)


def test_nonobject_manifest_refuses(tmp_path):
    implementation._json_write(tmp_path / 'manifest.json', [])
    with pytest.raises(ValueError, match='manifest schema'):
        implementation.verify(tmp_path)


def test_second_unicode_file_is_independently_hash_bound(tmp_path, monkeypatch):
    from hashlib import sha256
    root = ucd_fixture(tmp_path)
    # Allow only the first synthetic file, then prove the second still refuses.
    monkeypatch.setitem(implementation.UCD_RELEASE_SHA256, 'UnicodeData.txt',
                        sha256((root / 'UnicodeData.txt').read_bytes()).hexdigest())
    with pytest.raises(ValueError, match='DerivedCoreProperties.txt'):
        implementation.unicode_admission(root)


def test_unicode_read_refuses_oversize_before_open(tmp_path, monkeypatch):
    path = tmp_path / 'oversize.txt'
    with path.open('wb') as stream:
        stream.truncate(implementation.UCD_MAX_BYTES + 1)
    def forbidden_open(*args, **kwargs):
        raise AssertionError('oversize file was opened')
    monkeypatch.setattr(implementation.os, 'open', forbidden_open)
    with pytest.raises(ValueError, match='acquisition budget'):
        implementation._read_unicode_file(path)


@pytest.mark.parametrize('kind', ['symlink', 'directory', 'fifo'])
def test_unicode_read_refuses_nonregular_inputs(tmp_path, kind):
    path = tmp_path / 'input'
    if kind == 'symlink':
        target = tmp_path / 'target'
        target.write_bytes(b'not a release')
        path.symlink_to(target)
    elif kind == 'directory':
        path.mkdir()
    else:
        if not hasattr(implementation.os, 'mkfifo'):
            pytest.skip('platform has no FIFO filesystem objects')
        implementation.os.mkfifo(path)
    with pytest.raises(ValueError, match='regular nonsymlink'):
        implementation._read_unicode_file(path)


def test_unicode_stream_read_is_capped_even_when_file_grows(tmp_path, monkeypatch):
    from contextlib import contextmanager
    path = tmp_path / 'growing.txt'
    path.write_bytes(b'x')
    monkeypatch.setattr(implementation, 'UCD_MAX_BYTES', 32)
    fdopen = implementation.os.fdopen
    requested = []
    @contextmanager
    def tracked_open(fd, mode):
        with fdopen(fd, mode) as stream:
            class Tracked:
                def fileno(self):
                    return stream.fileno()
                def read(self, count):
                    requested.append(count)
                    with path.open('ab') as writer:
                        writer.write(b'x' * 64)
                    return stream.read(count)
            yield Tracked()
    monkeypatch.setattr(implementation.os, 'fdopen', tracked_open)
    with pytest.raises(ValueError, match='acquisition budget'):
        implementation._read_unicode_file(path)
    assert requested == [33]


def test_unicode_input_replacement_during_open_refuses(tmp_path, monkeypatch):
    path = tmp_path / 'swapped.txt'
    path.write_bytes(b'first')
    replacement = tmp_path / 'replacement'
    replacement.write_bytes(b'second')
    original_open = implementation.os.open
    def replacing_open(name, flags):
        replacement.replace(path)
        return original_open(name, flags)
    monkeypatch.setattr(implementation.os, 'open', replacing_open)
    with pytest.raises(ValueError, match='changed'):
        implementation._read_unicode_file(path)


def test_bounded_unicode_snapshot_preserves_exact_bytes(tmp_path):
    path = tmp_path / 'regular.txt'
    path.write_bytes(b'exact\x00bytes\n')
    assert implementation._read_unicode_file(path) == b'exact\x00bytes\n'


def test_build_refuses_oversize_ucd_before_source_or_copy(tmp_path):
    path = tmp_path / 'ucd'
    path.mkdir()
    with (path / 'UnicodeData.txt').open('wb') as stream:
        stream.truncate(implementation.UCD_MAX_BYTES + 1)
    output = tmp_path / 'must-not-be-created' / 'output'
    with pytest.raises(ValueError, match='acquisition budget'):
        implementation.build(tmp_path / 'missing-admission', path, output)
    assert not output.parent.exists()


@pytest.mark.parametrize('kind', ['symlink', 'directory', 'fifo'])
def test_json_read_refuses_nonregular_inputs(tmp_path, kind):
    path = tmp_path / 'manifest.json'
    if kind == 'symlink':
        target = tmp_path / 'target.json'
        target.write_bytes(b'{}\n')
        path.symlink_to(target)
    elif kind == 'directory':
        path.mkdir()
    else:
        if not hasattr(implementation.os, 'mkfifo'):
            pytest.skip('platform has no FIFO filesystem objects')
        implementation.os.mkfifo(path)
    with pytest.raises(ValueError, match='regular nonsymlink'):
        implementation._json_read(path)


def test_json_read_refuses_oversize_before_open(tmp_path, monkeypatch):
    path = tmp_path / 'manifest.json'
    with path.open('wb') as stream:
        stream.truncate(65)
    monkeypatch.setattr(implementation, 'JSON_MAX_BYTES', 64)
    def forbidden_open(*args, **kwargs):
        raise AssertionError('oversize JSON artifact was opened')
    monkeypatch.setattr(implementation.os, 'open', forbidden_open)
    with pytest.raises(ValueError, match='read budget'):
        implementation._json_read(path)


def test_json_stream_read_is_capped_if_file_grows(tmp_path, monkeypatch):
    from contextlib import contextmanager
    path = tmp_path / 'manifest.json'
    path.write_bytes(b'{}\n')
    monkeypatch.setattr(implementation, 'JSON_MAX_BYTES', 32)
    fdopen = implementation.os.fdopen
    requested = []
    @contextmanager
    def tracked_open(fd, mode):
        with fdopen(fd, mode) as stream:
            class Tracked:
                def fileno(self):
                    return stream.fileno()
                def read(self, count):
                    requested.append(count)
                    with path.open('ab') as writer:
                        writer.write(b'x' * 64)
                    return stream.read(count)
            yield Tracked()
    monkeypatch.setattr(implementation.os, 'fdopen', tracked_open)
    with pytest.raises(ValueError, match='read budget'):
        implementation._json_read(path)
    assert requested == [33]
