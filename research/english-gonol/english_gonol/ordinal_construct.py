"""Build the replacement English angular/radial construction.

Usage (from research/english-gonol, with UCNS on PYTHONPATH):
    python -m english_gonol.ordinal_construct build ADMISSION UCD NEW_OUTPUT
    python -m english_gonol.ordinal_construct verify OUTPUT
    python -m english_gonol.ordinal_construct query OUTPUT 'the geometry'

ADMISSION is a complete, verified structural-profile field, used for source
admission and relations only. The new construction never consumes its old
public_position column. UCD contains UnicodeData.txt and DerivedCoreProperties.txt
from the explicitly declared Unicode release. No network occurs in this module.
"""
from __future__ import annotations

import argparse
from contextlib import closing
from functools import lru_cache
from hashlib import sha256
from itertools import groupby
import json
import os
from pathlib import Path
import shutil
import sqlite3
import stat
import tempfile

from ucns.ordinal_affixiation import Carrier, Participant, affixiate

# === MODULE_BUILD ===
# id: english_ordinal_construction
#   module_name: ordinal_construct
#   module_kind: engine
#   summary: expanded corpus/Unicode public gonol and exact recursive ordinal geometry
#   owner: Erin Spencer
#   public_surface: repertoire, Factory, build, verify, query, main
#   internal_surface: canonical artifact rows and strict corpus admission
#   auth_boundary: read-only exact complete structural source
#   storage_boundary: new caller-selected output; no overwrite
#   network_boundary: none
#   user_data_boundary: query text in memory unless explicitly saved by caller
#   admin_only: false
#   tests: tests/test_ordinal_construct.py
#   rollout: explicit replacement profile english.ordinal/1; legacy receipts remain historical
#   rollback: remove candidate import/output; no silent profile downgrade
#   unresolved: global SPACE-frame transport, source-uncovered definitions, semantic interpretation
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: english_expanded_repertoire
#   given: complete corpus scalars, exact inherited carrier, pinned Unicode properties
#   then: every required scalar is admitted once; registry is reproducible
# id: english_recursive_ordinal_geometry
#   given: closed words and exact source components
#   then: UCNS places by ordinal radius and declared carrier angle while interiors remain recoverable
# id: english_complete_geometry_replay
#   given: a complete replacement artifact
#   then: independently check every placement, source reference, closure receipt and raw source input
# === END CONTRACTS ===

PROFILE = 'english.ordinal/1'
UNICODE_VERSION = '18.0.0'
UCD_FILES = ('UnicodeData.txt', 'DerivedCoreProperties.txt')
UCD_MAX_BYTES = 10_000_000
JSON_MAX_BYTES = 64_000_000
# Exact complete Unicode 18.0.0 release bytes, retained in the full-corpus artifact.
# Admission pins content, not a header, local registry, or minimal ASCII subset.
UCD_RELEASE_SHA256 = {
    'UnicodeData.txt': '0736451de439ae7baf1425136617da495e09ee5afbe6e394374db7009ea08950',
    'DerivedCoreProperties.txt': '09c928886a178fcafd93c29e4bd59073a058e5a100b716d425cb563ab50f68c9',
}
MANIFEST_BOUNDARIES = (
    'Local frame placement is constructed; global origin attachment is not inferred.',
    'Layout recipes are explicit profile choices, not discovered semantic laws.',
    'Native Mobius lift is not required; inference quality remains untested.',
)
MANIFEST_KEYS = frozenset((
    'schema', 'source_receipt', 'source', 'ucns_commit', 'implementation_sha256',
    'public_sha256', 'glyph_carrier_receipt', 'word_carrier_receipt', 'counts',
    'geometry_receipt', 'character_definitions_receipt', 'hmmm',
))
LOGIC = tuple('¬∧∨⊻⊼⊽→←↔⇒⇐⇔∀∃∄⊢⊣⊤⊥⊨⊭⊬⊮⊯≡≠=<>≤≥')
LAYOUT = 'legacy-anchor-balanced-insertion/1'
WORD_LAYOUT = 'lexicographic-public-gonol-index-sequences/1'
UCNS_COMMIT = 'a7bfa0c96daca1f7445ba57c39fa6d8fd62e51eb'
UCNS_MODULE_SHA256 = '784cf61d185d2a54259c0e013af8c0ea2b6d79fad32beaffda7819f0c0e512ad'
SQL = '''
PRAGMA foreign_keys=ON;
PRAGMA journal_mode=DELETE;
CREATE TABLE frames(kind TEXT NOT NULL, id INTEGER NOT NULL, identity TEXT NOT NULL,
 origin TEXT NOT NULL, relation TEXT NOT NULL, source TEXT NOT NULL, receipt TEXT NOT NULL,
 length INTEGER NOT NULL CHECK(length>0), PRIMARY KEY(kind,id)) WITHOUT ROWID;
CREATE TABLE placements(kind TEXT NOT NULL, id INTEGER NOT NULL, ordinal INTEGER NOT NULL,
 participant_kind TEXT NOT NULL CHECK(participant_kind IN ('word','character')),
 participant_id INTEGER NOT NULL, carrier_index INTEGER NOT NULL,
 exponent INTEGER NOT NULL CHECK(exponent>0), interior_receipt TEXT,
 PRIMARY KEY(kind,id,ordinal), FOREIGN KEY(kind,id) REFERENCES frames(kind,id)) WITHOUT ROWID;
'''


def canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def digest(value: object) -> str:
    return sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    with path.open('rb') as stream:
        return sha256(stream.read()).hexdigest()


def _producer_check() -> None:
    import ucns.ordinal_affixiation as geometry
    if file_hash(Path(geometry.__file__)) != UCNS_MODULE_SHA256:
        raise ValueError('UCNS geometry source differs from the exact pinned producer')


def scalar(value: str) -> str:
    if (not isinstance(value, str) or len(value) != 1
            or 0xD800 <= ord(value) <= 0xDFFF):
        raise ValueError('one exact Unicode scalar required')
    return value


def _range(value: str) -> range:
    bounds = value.strip().split('..')
    first, last = int(bounds[0], 16), int(bounds[-1], 16)
    if len(bounds) > 2 or not 0 <= first <= last <= 0x10FFFF:
        raise ValueError('invalid Unicode property range')
    return range(first, last + 1)


def _parse_unicode_properties(blobs: dict[str, bytes], version: str):
    """Parse supplied property syntax; this helper establishes no release identity."""
    numbers: set[str] = set()
    maths: set[str] = set()
    pending = None
    if any(len(raw) > UCD_MAX_BYTES for raw in blobs.values()):
        raise ValueError('Unicode input exceeds per-file acquisition budget')
    data = blobs[UCD_FILES[0]].decode('utf-8')
    for line in data.splitlines():
        if not line.strip():
            continue
        fields = line.split(';')
        if len(fields) != 15:
            raise ValueError('invalid UnicodeData record')
        cp, name, category = int(fields[0], 16), fields[1], fields[2]
        if not 0 <= cp <= 0x10FFFF:
            raise ValueError('UnicodeData code point out of range')
        if name.endswith(', First>'):
            if pending is not None:
                raise ValueError('nested UnicodeData range')
            pending = (cp, category)
            continue
        if name.endswith(', Last>'):
            if pending is None or pending[1] != category or cp < pending[0]:
                raise ValueError('unmatched UnicodeData range')
            points = range(pending[0], cp + 1)
            pending = None
        else:
            if pending is not None:
                raise ValueError('unterminated UnicodeData range')
            points = (cp,)
        if category in ('Nd', 'Nl', 'No'):
            numbers.update(scalar(chr(p)) for p in points)
    if pending is not None:
        raise ValueError('unterminated UnicodeData range')
    derived = blobs[UCD_FILES[1]].decode('utf-8')
    if f'DerivedCoreProperties-{version}.txt' not in derived[:4096]:
        raise ValueError('Unicode release header mismatch')
    for line in derived.splitlines():
        body = line.split('#', 1)[0].strip()
        if not body:
            continue
        fields = [field.strip() for field in body.split(';')]
        if len(fields) >= 2 and fields[1] == 'Math':
            maths.update(scalar(chr(p)) for p in _range(fields[0]))
    if not set('0123456789') <= numbers or not set('+<=>') <= maths:
        raise ValueError('incomplete numeric or Math property input')
    return numbers, maths, {name: sha256(blobs[name]).hexdigest() for name in UCD_FILES}



def _read_unicode_file(path: Path) -> bytes:
    """Snapshot a bounded regular file; do not follow symlinks or block on FIFOs."""
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise ValueError(f'Unicode input must be a regular nonsymlink file: {path.name}')
    if before.st_size > UCD_MAX_BYTES:
        raise ValueError(f'Unicode input exceeds acquisition budget: {path.name}')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    try:
        fd = os.open(path, flags)
    except OSError as error:
        raise ValueError(f'Unicode input changed or cannot be opened: {path.name}') from error
    with os.fdopen(fd, 'rb') as stream:
        opened = os.fstat(stream.fileno())
        if (not stat.S_ISREG(opened.st_mode)
                or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)):
            raise ValueError(f'Unicode input changed or is not regular: {path.name}')
        if opened.st_size > UCD_MAX_BYTES:
            raise ValueError(f'Unicode input exceeds acquisition budget: {path.name}')
        raw = stream.read(UCD_MAX_BYTES + 1)
        after = os.fstat(stream.fileno())
        if len(raw) > UCD_MAX_BYTES:
            raise ValueError(f'Unicode input exceeds acquisition budget: {path.name}')
        if (len(raw) != opened.st_size
                or (after.st_size, after.st_mtime_ns) != (opened.st_size, opened.st_mtime_ns)):
            raise ValueError(f'Unicode input changed during bounded read: {path.name}')
    return raw


def _verified_unicode_blobs(ucd: Path) -> dict[str, bytes]:
    """Acquire and authenticate a bounded snapshot before any artifact copying."""
    blobs = {name: _read_unicode_file(ucd / name) for name in UCD_FILES}
    for name, raw in blobs.items():
        if sha256(raw).hexdigest() != UCD_RELEASE_SHA256[name]:
            raise ValueError(f'Unicode release hash mismatch: {name}; complete pinned release required')
    return blobs


def unicode_admission(ucd: Path) -> tuple[set[str], set[str], dict]:
    """Admit only the complete pinned release; never trust a self-declared header."""
    return _parse_unicode_properties(_verified_unicode_blobs(ucd), UNICODE_VERSION)


def _layout_repertoire(corpus, legacy, numbers, maths, hashes, unicode_version):
    """Lay out already admitted identities; fixture callers must label their source."""
    for c in (*corpus, *legacy):
        scalar(c)
    if len(set(legacy)) != len(legacy) or not legacy or legacy[0] != ' ':
        raise ValueError('legacy anchors must be unique with SPACE first')
    admitted = set(corpus) | set(legacy) | numbers | maths | set(LOGIC)
    extras = sorted(admitted - set(legacy), key=ord)
    order: list[str] = []
    for i, anchor in enumerate(legacy):
        order.append(anchor)
        order.extend(extras[i * len(extras) // len(legacy):
                            (i + 1) * len(extras) // len(legacy)])
    if len(order) != len(admitted) or set(order) != admitted:
        raise AssertionError('repertoire union lost or duplicated a scalar')
    return {'schema': 'english.public-gonol/1', 'unicode_version': unicode_version,
            'layout': LAYOUT, 'normalization': 'none', 'origin_scalar': ' ',
            'corpus_scalars': sorted(corpus, key=ord), 'legacy_anchors': list(legacy),
            'unicode_files_sha256': hashes, 'logical_supplement': list(LOGIC),
            'admission_counts': {'corpus': len(set(corpus)), 'legacy': len(legacy),
                                 'numbers': len(numbers), 'math': len(maths),
                                 'logical_supplement': len(set(LOGIC)),
                                 'additional_to_legacy': len(extras), 'union': len(order)},
            'identities': order}


def repertoire(corpus: tuple[str, ...], legacy: tuple[str, ...], ucd: Path) -> dict:
    """Expand the repertoire only after authenticating the complete Unicode release."""
    numbers, maths, hashes = unicode_admission(ucd)
    return _layout_repertoire(corpus, legacy, numbers, maths, hashes, UNICODE_VERSION)


class Factory:
    """Actual recursive constructions; carriers and closed interiors remain available."""
    def __init__(self, public: dict, words: dict[int, str], source_receipt: str):
        self.public = json.loads(canonical(public))
        self.words = dict(words)
        self.word_ids = {word: wid for wid, word in words.items()}
        self.source_receipt = source_receipt
        self.glyph_carrier = Carrier(tuple(public['identities']),
                                     f'{PROFILE}:public:{digest(public)}')
        ordered = tuple(sorted(words.values(), key=lambda w: tuple(
            self.glyph_carrier.index(c) for c in w)))
        if not ordered:
            raise ValueError('no closed words admitted')
        self.word_carrier = Carrier(ordered, f'{PROFILE}:{WORD_LAYOUT}:{source_receipt}')
        self._atoms = {c: Participant.atom(self.glyph_carrier, c)
                       for c in self.glyph_carrier.identities}

    @lru_cache(maxsize=8192)
    def word(self, wid: int):
        text = self.words[wid]
        return affixiate(text, tuple(self._atoms[c] for c in text), origin='SPACE',
                         relation='ordered-glyphs',
                         source=f'{self.source_receipt}:word:{wid}')

    def record(self, rid: int, kind: str, parts):
        participants = tuple(self._atoms[value] if pkind == 'character' else
                             Participant.closed(self.word_carrier, self.word(value))
                             for pkind, value in parts)
        return affixiate(f'{kind}:{rid}', participants, origin='SPACE',
                         relation=f'ordered-{kind}',
                         source=f'{self.source_receipt}:record:{rid}')


def _inventory(db):
    return dict(db.execute('SELECT id,scalar FROM characters ORDER BY id')), dict(
        db.execute('SELECT id,surface FROM words ORDER BY id'))


def _groups(db):
    rows = db.execute('SELECT record_id,ordinal,kind,word_id,character_id '
                      'FROM components ORDER BY record_id,ordinal')
    for rid, group in groupby(rows, key=lambda r: r[0]):
        yield rid, tuple(group)


def _geometry_receipt(db) -> str:
    result = sha256()
    for table, ordering in (('frames', 'kind,id'), ('placements', 'kind,id,ordinal')):
        result.update(canonical(table) + b'\n')
        for row in db.execute(f'SELECT * FROM {table} ORDER BY {ordering}'):
            result.update(canonical(row) + b'\n')
    return result.hexdigest()


def _write_frame(db, kind, identity, obj, refs):
    db.execute('INSERT INTO frames VALUES(?,?,?,?,?,?,?,?)',
               (kind, identity, obj.identity, obj.origin, obj.relation,
                obj.source, obj.receipt, len(obj.participants)))
    db.executemany('INSERT INTO placements VALUES(?,?,?,?,?,?,?,?)', (
        (kind, identity, i, pkind, pid,
         p.carrier.index(p.identity), obj.placement(i).exponent,
         None if p.interior is None else p.interior.receipt)
        for i, ((pkind, pid), p) in enumerate(zip(refs, obj.participants, strict=True))))


def _json_write(path, value):
    Path(path).write_bytes(canonical(value) + b'\n')


def _read_bounded_regular(path: Path, limit: int, label: str) -> bytes:
    """Snapshot one bounded regular file without following links or blocking on special files."""
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise ValueError(f'{label} must be a regular nonsymlink file: {path.name}')
    if before.st_size > limit:
        raise ValueError(f'{label} exceeds read budget: {path.name}')
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    try:
        fd = os.open(path, flags)
    except OSError as error:
        raise ValueError(f'{label} changed or cannot be opened: {path.name}') from error
    with os.fdopen(fd, 'rb') as stream:
        opened = os.fstat(stream.fileno())
        if (not stat.S_ISREG(opened.st_mode)
                or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino)):
            raise ValueError(f'{label} changed or is not regular: {path.name}')
        if opened.st_size > limit:
            raise ValueError(f'{label} exceeds read budget: {path.name}')
        raw = stream.read(limit + 1)
        after = os.fstat(stream.fileno())
        if len(raw) > limit:
            raise ValueError(f'{label} exceeds read budget: {path.name}')
        if (len(raw) != opened.st_size
                or (after.st_size, after.st_mtime_ns) != (opened.st_size, opened.st_mtime_ns)):
            raise ValueError(f'{label} changed during bounded read: {path.name}')
    return raw


def _json_read(path):
    raw = _read_bounded_regular(Path(path), JSON_MAX_BYTES, 'JSON artifact')
    value = json.loads(raw)
    if raw != canonical(value) + b'\n':
        raise ValueError('noncanonical JSON artifact')
    return value


def build(admission: Path, ucd: Path, output: Path) -> dict:
    """Consume complete source admission, create a fresh self-contained geometry bundle."""
    _producer_check()
    if output.exists():
        raise ValueError('output exists; select a new directory')
    unicode_blobs = _verified_unicode_blobs(ucd)
    from english_gonol.structural_construct import _verified_connection
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.ordinal-', dir=output.parent))
    try:
        with _verified_connection(admission) as verified:
            source_db, source_manifest = verified
            if source_manifest['metadata']['complete_corpus'] is not True:
                raise ValueError('replacement construction requires complete pinned source')
            (stage / 'admission').mkdir()
            with closing(sqlite3.connect(stage / 'admission' / 'construct.db')) as copy:
                source_db.backup(copy)
            _json_write(stage / 'admission' / 'manifest.json', source_manifest)
            (stage / 'ucd').mkdir()
            for name in UCD_FILES:
                (stage / 'ucd' / name).write_bytes(unicode_blobs[name])
            chars, words = _inventory(source_db)
            legacy = tuple(source_manifest['metadata']['producer']['carrier'])
            public = repertoire(tuple(chars.values()), legacy, stage / 'ucd')
            factory = Factory(public, words, source_manifest['receipt_sha256'])
            from english_gonol.ordinal_definitions import build_definitions
            definitions = build_definitions(factory)
            _json_write(stage / 'character-definitions.json', definitions)
            _json_write(stage / 'public-gonol.json', public)
            _json_write(stage / 'word-carrier.json', {
                'layout': WORD_LAYOUT, 'identities': list(factory.word_carrier.identities),
                'source': factory.word_carrier.source, 'receipt': factory.word_carrier.receipt})
            character_ids = {c: cid for cid, c in chars.items()}
            with closing(sqlite3.connect(stage / 'geometry.db')) as geometry:
                geometry.executescript(SQL)
                for wid, text in words.items():
                    _write_frame(geometry, 'word', wid, factory.word(wid),
                                 tuple(('character', character_ids[c]) for c in text))
                records = dict(source_db.execute('SELECT id,kind FROM records'))
                record_count = 0
                for rid, rows in _groups(source_db):
                    record_count += 1
                    obj = factory.record(rid, records[rid], tuple(
                        (pk, chars[cid] if pk == 'character' else wid)
                        for _, _, pk, wid, cid in rows))
                    refs = tuple((pk, cid if pk == 'character' else wid)
                                 for _, _, pk, wid, cid in rows)
                    _write_frame(geometry, 'record', rid, obj, refs)
                if record_count != len(records):
                    raise ValueError('source has empty records; empty closure is not licensed')
                geometry.commit()
                counts = {table: geometry.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
                          for table in ('frames', 'placements')}
                manifest = {'schema': PROFILE, 'source_receipt': source_manifest['receipt_sha256'],
                            'source': source_manifest['metadata']['source'],
                            'ucns_commit': UCNS_COMMIT, 'implementation_sha256': file_hash(Path(__file__)),
                            'public_sha256': digest(public),
                            'glyph_carrier_receipt': factory.glyph_carrier.receipt,
                            'word_carrier_receipt': factory.word_carrier.receipt,
                            'counts': counts, 'geometry_receipt': _geometry_receipt(geometry),
                            'character_definitions_receipt': digest(definitions),
                            'hmmm': list(MANIFEST_BOUNDARIES)}
            _json_write(stage / 'manifest.json', manifest)
        report = verify(stage)
        _json_write(stage / 'verification.json', report)
        stage.rename(output)
        return report
    except BaseException:
        shutil.rmtree(stage, ignore_errors=True)
        raise


def _independent_frame(kind, frame_id, identity, relation, source_receipt, refs,
                       factory, chars, word_receipts):
    """Reference checker: literal ordinal formula, no Placement/affixiate calls."""
    from fractions import Fraction
    positions, stored = [], []
    n = len(refs)
    for i, (pk, pid) in enumerate(refs):
        carrier = factory.glyph_carrier if pk == 'character' else factory.word_carrier
        name = chars[pid] if pk == 'character' else factory.words[pid]
        index = carrier.index(name)
        turn = Fraction(index, len(carrier.identities))
        interior = None if pk == 'character' else word_receipts[pid]
        positions.append({'identity': name, 'carrier_receipt': carrier.receipt,
                          'index': index, 'arity': len(carrier.identities),
                          'turn': [turn.numerator, turn.denominator],
                          'radius': {'numerator': 1, 'power_of_two_denominator': n-i},
                          'interior_receipt': interior})
        stored.append((kind, frame_id, i, pk, pid, index, n-i, interior))
    source = f'{source_receipt}:{kind}:{frame_id}'
    receipt = digest({'schema': 'ucns.ordinal-affixiation.v1', 'identity': identity,
                      'origin': 'SPACE', 'relation': relation, 'source': source,
                      'placements': positions})
    return (kind, frame_id, identity, 'SPACE', relation, source, receipt, n), stored


def _validate_manifest(manifest: object) -> None:
    """Reject unsupported claims before source replay; this alone proves no geometry."""
    if type(manifest) is not dict or set(manifest) != MANIFEST_KEYS:
        raise ValueError('manifest schema keys differ from the exact profile')
    if manifest['schema'] != PROFILE or manifest['ucns_commit'] != UCNS_COMMIT:
        raise ValueError('profile/geometry producer mismatch')
    if manifest['implementation_sha256'] != file_hash(Path(__file__)):
        raise ValueError('implementation changed; rebuild explicitly')
    if manifest['hmmm'] != list(MANIFEST_BOUNDARIES):
        raise ValueError('manifest boundary claims differ from the exact profile')
    counts = manifest['counts']
    if (type(counts) is not dict or set(counts) != {'frames', 'placements'}
            or any(type(v) is not int or v <= 0 for v in counts.values())):
        raise ValueError('manifest counts must be positive integer frame/placement counts')
    for key in ('source_receipt', 'public_sha256', 'glyph_carrier_receipt',
                'word_carrier_receipt', 'geometry_receipt', 'character_definitions_receipt'):
        value = manifest[key]
        if (type(value) is not str or len(value) != 64
                or any(c not in '0123456789abcdef' for c in value)):
            raise ValueError(f'manifest digest is invalid: {key}')


def verify(output: Path) -> dict:
    """Replay every source and placement; structural bytes alone never prove new geometry."""
    _producer_check()
    manifest = _json_read(output / 'manifest.json')
    _validate_manifest(manifest)
    from english_gonol.structural_construct import _verified_connection, open_readonly, _schema
    with _verified_connection(output / 'admission') as verified:
        source, source_manifest = verified
        if not source_manifest['metadata']['complete_corpus']:
            raise ValueError('partial source cannot verify the replacement')
        if (manifest['source_receipt'] != source_manifest['receipt_sha256'] or
                manifest['source'] != source_manifest['metadata']['source']):
            raise ValueError('source binding mismatch')
        chars, words = _inventory(source)
        public = repertoire(tuple(chars.values()), tuple(
            source_manifest['metadata']['producer']['carrier']), output / 'ucd')
        if public != _json_read(output / 'public-gonol.json') or digest(public) != manifest['public_sha256']:
            raise ValueError('public gonol mismatch')
        factory = Factory(public, words, manifest['source_receipt'])
        expected_words = {'layout': WORD_LAYOUT, 'identities': list(factory.word_carrier.identities),
                          'source': factory.word_carrier.source, 'receipt': factory.word_carrier.receipt}
        if _json_read(output / 'word-carrier.json') != expected_words:
            raise ValueError('word carrier mismatch')
        if (factory.glyph_carrier.receipt != manifest['glyph_carrier_receipt'] or
                factory.word_carrier.receipt != manifest['word_carrier_receipt']):
            raise ValueError('carrier receipt mismatch')
        from english_gonol.ordinal_definitions import verify_definitions
        definitions = _json_read(output / 'character-definitions.json')
        if digest(definitions) != manifest['character_definitions_receipt']:
            raise ValueError('character definition receipt mismatch')
        definition_layer = verify_definitions(factory, definitions)
        word_receipts = {}
        character_ids = {c: cid for cid, c in chars.items()}
        with closing(open_readonly(output / 'geometry.db')) as db:
            db.execute('BEGIN')
            with closing(sqlite3.connect(':memory:')) as expected:
                expected.executescript(SQL)
                if _schema(db) != _schema(expected):
                    raise ValueError('geometry schema mismatch')
            if db.execute('PRAGMA integrity_check').fetchone() != ('ok',) or db.execute('PRAGMA foreign_key_check').fetchone():
                raise ValueError('geometry integrity failure')
            frames_checked = placements_checked = 0

            def check(kind, frame_id, identity, relation, refs):
                nonlocal frames_checked, placements_checked
                frame, positions = _independent_frame(kind, frame_id, identity, relation,
                    manifest['source_receipt'], refs, factory, chars, word_receipts)
                actual_frame = db.execute('SELECT * FROM frames WHERE kind=? AND id=?', (kind, frame_id)).fetchone()
                actual = db.execute('SELECT * FROM placements WHERE kind=? AND id=? ORDER BY ordinal',
                                    (kind, frame_id)).fetchall()
                if actual_frame != frame or actual != positions:
                    raise ValueError(f'geometry mismatch at {kind}:{frame_id}')
                frames_checked += 1
                placements_checked += len(positions)
                return frame[6]

            for wid, text in words.items():
                word_receipts[wid] = check('word', wid, text, 'ordered-glyphs',
                                         tuple(('character', character_ids[c]) for c in text))
            records = dict(source.execute('SELECT id,kind FROM records'))
            for rid, rows in _groups(source):
                check('record', rid, f'{records[rid]}:{rid}', f'ordered-{records[rid]}',
                      tuple((pk, cid if pk == 'character' else wid) for _, _, pk, wid, cid in rows))
            counts = {table: db.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
                      for table in ('frames', 'placements')}
            if (frames_checked != len(words) + len(records) or counts != manifest['counts']
                    or counts != {'frames': frames_checked, 'placements': placements_checked}):
                raise ValueError('missing or extra geometry')
            if _geometry_receipt(db) != manifest['geometry_receipt']:
                raise ValueError('geometry receipt mismatch')
        return {'schema': 'english.ordinal-verification/1', 'status': 'SURVIVED',
                'scope': 'complete pinned corpus; source recovery plus every local placement',
                'public_gonol_size': len(public['identities']), 'words': len(words),
                **counts, 'character_definitions': dict(definition_layer.counts),
                'manifest_sha256': digest(manifest),
                'source_receipt': manifest['source_receipt'], 'hmmm': list(MANIFEST_BOUNDARIES)}


def query(output: Path, text: str) -> dict:
    """Construct exact ordered text from the sealed admission; never admit unknown words."""
    from english_gonol.structural_construct import _verified_connection
    from english_gonol.structural_rules import segment
    report = verify(output)
    geometry_manifest = _json_read(output / 'manifest.json')
    if digest(geometry_manifest) != report['manifest_sha256']:
        raise ValueError('manifest changed after verification')
    with _verified_connection(output / 'admission') as verified:
        source, manifest = verified
        _, words = _inventory(source)
        public = _json_read(output / 'public-gonol.json')
        if (digest(public) != geometry_manifest['public_sha256'] or
                manifest['receipt_sha256'] != geometry_manifest['source_receipt']):
            raise ValueError('query inputs changed after verification')
        factory = Factory(public, words, manifest['receipt_sha256'])
        parts = segment(text, manifest['metadata']['profile']['abbreviations'])
        participants = []
        interiors = {}
        for part in parts:
            if part.kind == 'word':
                if part.text not in factory.word_ids:
                    raise ValueError(f'word not admitted: {part.text!r}')
                word = factory.word(factory.word_ids[part.text])
                participants.append(Participant.closed(factory.word_carrier, word))
                interiors[word.receipt] = word.record()
            else:
                if part.text not in factory._atoms:
                    raise ValueError(f'scalar not admitted: U+{ord(part.text):04X}')
                participants.append(factory._atoms[part.text])
        obj = affixiate('query', tuple(participants), origin='SPACE', relation='ordered-text',
                         source=f'query:{digest(text)}:{manifest["receipt_sha256"]}')
        recovered = ''.join(obj.recover())
        if recovered != text:
            raise AssertionError('query source recovery failed')
        return {'construction': obj.record(), 'interiors': interiors, 'recovered': recovered,
                'public_gonol_sha256': digest(factory.public),
                'word_carrier_receipt': factory.word_carrier.receipt,
                'closure': 'ordered-text; no grammatical or semantic assertion'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    builder = sub.add_parser('build')
    for name in ('admission', 'ucd', 'output'):
        builder.add_argument(name, type=Path)
    checker = sub.add_parser('verify')
    checker.add_argument('output', type=Path)
    request = sub.add_parser('query')
    request.add_argument('output', type=Path)
    request.add_argument('text')
    args = parser.parse_args()
    if args.command == 'build':
        value = build(args.admission, args.ucd, args.output)
    elif args.command == 'verify':
        value = verify(args.output)
    else:
        value = query(args.output, args.text)
    print(json.dumps(value, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
