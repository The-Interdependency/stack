# ratios: loc_comments=131:10 imports_exports=16:8 calls_definitions=73:8
"""Exercise corpus migration, intact recursive interiors, source custody and substituted artifacts."""
from contextlib import closing
from fractions import Fraction
from hashlib import sha256
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys

import pytest

from english_gonol import unicode_corpus as corpus
from english_gonol import unicode_corpus_inputs as inputs
from english_gonol import unicode_construction as unicode
from english_gonol.structural_rules import canonical
from english_gonol.structural_construct import SQL as SOURCE_SQL, _manifest
from english_gonol.language.character_definitions import load_character_definition_table

# === CHECKS ===
# id: unicode_corpus_object_source_and_replay
#   proves: unicode_corpus_preserves_ownership, unicode_corpus_replay, unicode_corpus_declared_placement
#   call: self::test_source_record_and_definitions, self::test_tampered_artifact, self::test_bearings_and_source_recovery
# id: unicode_corpus_admission_integrity
#   proves: english_corpus_inputs_exact, active_english_selects_unicode
#   call: self::test_manifest_special_files, self::test_real_entrypoint, self::test_schema_and_inputs
# === END CHECKS ===

NATIVE = Path(os.environ['UCHC_UNICODE_UCNS_ROOT'])


@pytest.fixture
def prepared(tmp_path, monkeypatch):
    # This small fixture signs only its own source. The production manifest and UCD hashes stay fixed.
    source, ucd, out = (tmp_path / n for n in ('source','ucd','corpus'))
    source.mkdir()
    ucd.mkdir()
    digits = [f'{i:04X};DIGIT;Nd;0;EN;;;;;N;;;;;' for i in range(48,58)]
    (ucd / 'UnicodeData.txt').write_text('\n'.join(digits) + '\n')
    (ucd / 'DerivedCoreProperties.txt').write_text('# DerivedCoreProperties-18.0.0.txt\n002B ; Math\n003C..003E ; Math\n')
    monkeypatch.setattr(inputs, 'UCD_RELEASE_SHA256', {n: sha256((ucd/n).read_bytes()).hexdigest() for n in inputs.UCD_FILES})
    registry = load_character_definition_table()
    words = sorted({'ë', 'e\u0308', '𐍈', 'the', *(e.number_name for e in registry.values() if e.number_name)})
    chars = sorted(set(' '.join(words)) | set(registry))
    word_id = {word: i+1 for i,word in enumerate(words)}
    char_id = {char: i+1 for i,char in enumerate(chars)}
    with closing(sqlite3.connect(source/'construct.db')) as db:
        db.executescript(SOURCE_SQL)
        db.executemany('INSERT INTO meta VALUES(?,?)', [
            ('producer', json.dumps({'carrier': list(registry)})),
            ('profile', '{"abbreviations":[]}'), ('source','{}')])
        db.executemany('INSERT INTO characters VALUES(?,?,NULL)', [(i,c) for c,i in char_id.items()])
        db.executemany('INSERT INTO words VALUES(?,?)', [(i,w) for w,i in word_id.items()])
        db.executemany('INSERT INTO word_characters VALUES(?,?,?)', [
            (i, j, char_id[c]) for w,i in word_id.items() for j,c in enumerate(w)])
        db.executemany('INSERT INTO records VALUES(?,?,?,?,?,?,?,?,?)', [
            (1,'lexical','the',None,word_id['the'],0,None,'{}','attached'),
            (2,'definition','the the',1,word_id['the'],0,None,'{"lex":"fixture"}','attached')])
        db.executemany('INSERT INTO components VALUES(?,?,?,?,?,?,?,?)', [
            (1,0,'word',word_id['the'],None,0,3,'{}'), (2,0,'word',word_id['the'],None,0,3,'{}'),
            (2,1,'character',None,char_id[' '],3,4,'{}'), (2,2,'word',word_id['the'],None,4,7,'{}')])
        db.commit()
        manifest = _manifest(db)
    raw = canonical(manifest) + b'\n'
    (source/'manifest.json').write_bytes(raw)
    monkeypatch.setattr(corpus,'ADMISSION_MANIFEST_SHA256',sha256(raw).hexdigest())
    monkeypatch.setattr(corpus,'ADMISSION_RECEIPT',manifest['receipt_sha256'])
    built = corpus.build(source,ucd,out,NATIVE)
    return out, built


def test_bearings_and_source_recovery(prepared):
    out, _ = prepared
    value = corpus.query(out, 'ë e\u0308 𐍈 ë', NATIVE, [0, Fraction(1,3), Fraction(1,5), 0])
    root = unicode._native(NATIVE).unicode_recursive.replay_unicode_graph(value['construction'])
    assert root.recover() == 'ë e\u0308 𐍈 ë'
    assert root.participants[0] is root.participants[-1]
    assert root.participants[0].receipt != root.participants[2].receipt
    assert all(p.radius == 1 for p in root.placements)
    assert root.participants[0].utf32_be == bytes.fromhex('000000eb')
    with pytest.raises(ValueError,match='2 explicit'):
        corpus.query(out, 'the the', NATIVE)
    with pytest.raises(ValueError,match='outside pinned'):
        corpus.query(out, 'quux', NATIVE, [0])


def test_source_record_and_definitions(prepared):
    out, report = prepared
    assert corpus.verify(out,NATIVE) == report
    result = corpus.record(out, 2, NATIVE, [0, Fraction(1,2)])
    assert result['recovered'] == 'the the'
    assert result['owner_record_id'] == 1 and result['attachment_reference'] == 'SPACE'
    assert [x['start'] for x in result['components']] == [0,3,4]
    assert result['components'][0]['receipt'] == result['components'][2]['receipt']
    with closing(sqlite3.connect(out/'geometry.db')) as db:
        ordinal, = db.execute("SELECT ordinal FROM definitions WHERE cp=51 AND relation='digit-number-name'").fetchone()
    named = corpus.definition(out,'3',ordinal,NATIVE,[0,Fraction(1,2)])
    assert named['recovered'] == '3three' and named['entry']['number_name'] == 'three'


@pytest.mark.parametrize('sql', [
    "UPDATE words SET receipt='forged' WHERE id=1",
    "DELETE FROM glyphs WHERE cp=32",
    "INSERT INTO words VALUES(10001,'forged','forged')",
    "UPDATE definitions SET relation='forged' WHERE cp=51",
    "CREATE VIEW forged AS SELECT * FROM words",
])
def test_tampered_artifact(prepared, sql):
    out,_ = prepared
    with closing(sqlite3.connect(out/'geometry.db')) as db:
        db.execute(sql)
        db.commit()
    with pytest.raises(ValueError):
        corpus.verify(out,NATIVE)


def test_schema_and_inputs(prepared):
    out,_ = prepared
    ucd = out/'ucd'/inputs.UCD_FILES[1]
    ucd.write_bytes(ucd.read_bytes() + b' ')
    with pytest.raises(ValueError,match='pinned Unicode'):
        corpus.verify(out,NATIVE)
    with pytest.raises(FileExistsError):
        corpus.build(out/'admission',out/'ucd',out,NATIVE)


@pytest.mark.parametrize('kind', ['fifo','symlink','oversized'])
def test_manifest_special_files(tmp_path,kind):
    manifest=tmp_path/'manifest.json'
    if kind=='fifo':
        os.mkfifo(manifest)
    elif kind=='symlink':
        target=tmp_path/'target'
        target.write_bytes(b'{}')
        manifest.symlink_to(target)
    else:
        with manifest.open('wb') as stream:
            stream.truncate(64_000_001)
    with pytest.raises(ValueError,match='regular nonsymlink|exceeds read budget'):
        with corpus.admission(tmp_path):
            pytest.fail('hostile manifest admitted')


def test_source_tampering(prepared):
    out,_=prepared
    with closing(sqlite3.connect(out/'admission'/'construct.db')) as db:
        db.execute("UPDATE records SET text='other' WHERE id=1")
        db.commit()
    with pytest.raises(ValueError,match='admission rows'):
        corpus.verify(out,NATIVE)


def test_real_entrypoint():
    env = {**os.environ,'PYTHONPATH':str(Path(corpus.__file__).resolve().parents[1])}
    p = subprocess.run([sys.executable,'-m','english_gonol','text','Aë','--ucns-source-root',str(NATIVE)],
                       env=env,check=True,capture_output=True,text=True)
    restored=unicode.replay_closed(json.loads(p.stdout),ucns_source_root=NATIVE)
    assert restored.recover()=='Aë'
    assert [item.radius for item in restored.placements] == [1,1]
    assert restored.glyphs[0].utf32_be == bytes.fromhex('00000041')
# ratios: loc_comments=131:10 imports_exports=16:8 calls_definitions=73:8
