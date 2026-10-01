"""Native UCHC word inspection/recovery; whole-message gonol law remains open.

Usage: with NativeWords(source_path, construct_db, expected_db_sha256) as native:
           word = native.promote(b'word'); recovered = native.recover(word)
The inspected upstream source blob is checked BEFORE execution. The database is
opened read-only after matching the caller's snapshot digest. This adapter returns
actual upstream WordGonol objects; it does not construct a replacement gonol tree,
serialize arbitrary binary as fake glyphs, or automatically bind the full stage.
A matching database hash is provenance, not proof of full-corpus construction.
"""
from __future__ import annotations
import hashlib
import importlib.util
from pathlib import Path
import re
import sqlite3
import sys
from .api import Blocked, Step

SOURCE_BLOB = '8b55823805c87ad8c4cc9d7451dc2eb90bdedd3a'
SOURCE_REPOSITORY = 'The-Interdependency/uchc'
SOURCE_PATH = 'human/english/english_gonol/hyperspace_construct.py'


class NativeWords:
    """Read/replay native word records only. Not a general message encoder."""
    def __init__(self, source: Path, database: Path, expected_database_sha256: str):
        self.source, self.database = Path(source), Path(database)
        self.expected_database_sha256 = expected_database_sha256
        self.db, self.native = None, None

    def __enter__(self):
        if (type(self.expected_database_sha256) is not str
                or not re.fullmatch('[0-9a-f]{64}', self.expected_database_sha256)):
            raise ValueError('explicit lowercase database SHA-256 required')
        if not self.source.is_file() or not self.database.is_file():
            raise Blocked('native UCHC source and constructed corpus database are required')
        content = self.source.read_bytes()
        identity = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
        if identity != SOURCE_BLOB:
            raise Blocked('native source differs from inspected UCHC blob; not imported')
        with self.database.open('rb') as stream:
            actual = hashlib.file_digest(stream, 'sha256').hexdigest()
        if actual != self.expected_database_sha256:
            raise Blocked('native database snapshot mismatch')
        name = '_weave_uchc_' + SOURCE_BLOB
        spec = importlib.util.spec_from_file_location(name, self.source)
        if spec is None or spec.loader is None:
            raise Blocked('cannot load inspected native source')
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        try:
            # Execute precisely the verified bytes, not a later path reread or pyc.
            exec(compile(content, str(self.source), 'exec'), module.__dict__)
            self.db = sqlite3.connect(self.database.resolve().as_uri() + '?mode=ro', uri=True)
            self.db.execute('PRAGMA query_only = ON')
            self.db.execute('BEGIN')
            self.native = module
        except BaseException:
            if self.db is not None:
                self.db.close()
                self.db = None
            sys.modules.pop(name, None)
            raise
        return self

    def promote(self, value: bytes):
        if self.db is None or self.native is None:
            raise RuntimeError('native reader is not open')
        if type(value) is not bytes:
            raise TypeError('exact UTF-8 word bytes required')
        try:
            surface = value.decode('utf-8', errors='strict')
        except UnicodeDecodeError as exc:
            raise Blocked('arbitrary binary gonol admission remains unresolved') from exc
        rows = self.db.execute('SELECT id FROM words WHERE surface = ?', (surface,)).fetchall()
        if len(rows) != 1:
            raise Blocked('input must match exactly one already-constructed native word')
        return self.native.promote_word(self.db, rows[0][0])[0]

    def recover(self, word) -> bytes:
        if self.db is None or self.native is None:
            raise RuntimeError('native reader is not open')
        if type(word) is not self.native.WordGonol:
            raise TypeError('the original native WordGonol type is required')
        rebuilt = self.native.recover_word(self.db, word.word_id)
        if rebuilt != word:
            raise ValueError('native identity, constituents, order or surface differs')
        return rebuilt.surface.encode('utf-8')

    def __exit__(self, *exc):
        if self.db is not None:
            self.db.close()
        self.db, self.native = None, None


STEP = Step('gonol', ('Q1',), 'Complete native plaintext construction and exact recovery.')
