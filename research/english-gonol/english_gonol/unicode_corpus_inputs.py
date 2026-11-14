# ratios: loc_comments=106:18 imports_exports=4:4 calls_definitions=64:6
"""Pinned Unicode 18 repertoire evidence for the English corpus. UCNS owns bearings.

Usage: repertoire(corpus_scalars, historical_anchors, ucd_directory).
"""
from hashlib import sha256
import os
from pathlib import Path
import stat

# === MODULE_BUILD ===
# id: english_unicode_corpus_inputs
#   module_name: unicode_corpus_inputs
#   summary: authenticates release inputs and returns the corpus repertoire
#   public_surface: repertoire, bounded_bytes
#   tests: unicode_tests/test_unicode_corpus.py
#   owner: Erin Spencer
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: english_corpus_inputs_exact
#   given: a verified corpus and the complete pinned Unicode release
#   then: preserve historical admission members and property-derived members as scalars while rejecting substituted or nonregular files
# === END CONTRACTS ===
UNICODE_VERSION = '18.0.0'
UCD_FILES = ('UnicodeData.txt', 'DerivedCoreProperties.txt')
UCD_MAX_BYTES = 10_000_000
UCD_RELEASE_SHA256 = {
    'UnicodeData.txt': '0736451de439ae7baf1425136617da495e09ee5afbe6e394374db7009ea08950',
    'DerivedCoreProperties.txt': '09c928886a178fcafd93c29e4bd59073a058e5a100b716d425cb563ab50f68c9',
}
LOGIC = tuple('¬∧∨⊻⊼⊽→←↔⇒⇐⇔∀∃∄⊢⊣⊤⊥⊨⊭⊬⊮⊯≡≠=<>≤≥')


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


def bounded_bytes(path: Path, limit: int, label: str) -> bytes:
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


def unicode_blobs(directory):
    data = {name: bounded_bytes(Path(directory) / name, UCD_MAX_BYTES, 'Unicode input') for name in UCD_FILES}
    if {name: sha256(raw).hexdigest() for name, raw in data.items()} != UCD_RELEASE_SHA256:
        raise ValueError('complete pinned Unicode 18.0.0 release required')
    return data


def repertoire(corpus, anchors, blobs):
    numbers, maths, hashes = _parse_unicode_properties(blobs, UNICODE_VERSION)
    if hashes != UCD_RELEASE_SHA256:
        raise ValueError('Unicode release hash mismatch')
    return sorted({scalar(c) for c in (*corpus, *anchors)} | numbers | maths | set(LOGIC), key=ord)
# ratios: loc_comments=106:18 imports_exports=4:4 calls_definitions=64:6
