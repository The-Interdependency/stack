# ratios: loc_comments=160:30 imports_exports=13:2 calls_definitions=87:17
"""Load the historical challenge inputs independently of the active checkout.

Usage: operations.py loads SOURCE_BUNDLE.json, SOURCE.json and frozen-sources.zip
beside this file. Every admitted byte is verified before source execution.
There is no network, Git, working-tree or bytecode fallback at runtime. This is
content-bound replay within the trusted process, not an OS sandbox or signature.
"""
from __future__ import annotations

# === MODULE_BUILD ===
# id: weave_challenge_frozen_source_loader
#   module_name: source_snapshot
#   module_kind: adapter
#   summary: validate and isolate the exact historical challenge source closure before import
#   owner: The-Interdependency/stack
#   public_surface: load_snapshot
#   internal_surface: bounded archive validation, temporary source view and checked-buffer imports
#   tests: test_source_snapshot.py
#   rollout: v2 challenge replay and source disclosures only
#   rollback: revert adapters and bundle together; never rewrite historical locks
#   auth_boundary: content identity under reviewed source metadata; no producer authentication
#   storage_boundary: private temporary source files cleaned on process exit
#   network_boundary: none
#   user_data_boundary: public source bytes only; no evaluator inputs
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: weave_challenge_frozen_source_closure
#   given: active checkout drift or absent Git/native checkouts
#   then: use only the complete verified frozen source bundle, or refuse before importing it
# id: weave_challenge_frozen_source_refusal
#   given: duplicate, escaped, symlinked, missing or altered archive members, or a conflicting import cache
#   then: refuse instead of falling back to active or cached source
# === END CONTRACTS ===

from hashlib import sha1, sha256
import importlib.abc
import importlib.util
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
from types import MappingProxyType
import zipfile

MAX_ARCHIVE = 4 * 1024 * 1024
MAX_MEMBER = 2 * 1024 * 1024
MAX_TOTAL = 8 * 1024 * 1024


def _unique(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('duplicate source metadata member: ' + key)
        value[key] = item
    return value


def _read(path, maximum):
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError('source bundle input must be a regular file: ' + str(path))
    with path.open('rb') as stream:
        data = stream.read(maximum + 1)
    if len(data) > maximum:
        raise ValueError('source bundle input exceeds declared byte budget')
    return data


def _path(name):
    if type(name) is not str or not name or len(name) > 512 or any(c in name for c in ('\\', ':', '\0')):
        raise ValueError('invalid frozen source path')
    path = PurePosixPath(name)
    if path.is_absolute() or path.as_posix() != name or any(p in ('.', '..') for p in path.parts):
        raise ValueError('escaped frozen source path')
    return path


def _blob(data):
    return sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


class _Loader(importlib.abc.Loader):
    def __init__(self, path, data):
        self.path, self.data = path, data

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        module.__file__ = str(self.path)
        module.__cached__ = None
        module.__source_sha256__ = sha256(self.data).hexdigest()
        exec(compile(self.data, str(self.path), 'exec', dont_inherit=True), module.__dict__)


class _Finder(importlib.abc.MetaPathFinder):
    def __init__(self, root, files):
        self.modules = {}
        for name, data in files.items():
            prefix = 'research/weave/'
            if not name.startswith(prefix) or not name.endswith('.py'):
                continue
            relative = PurePosixPath(name[len(prefix):])
            if relative.parts[0] == 'tests':
                continue
            package = relative.name == '__init__.py'
            parts = relative.parts[:-1] if package else (*relative.parts[:-1], relative.stem)
            if parts and all(p.isidentifier() for p in parts):
                self.modules['.'.join(parts)] = (root / name, data, package)
        self.roots = {name.split('.')[0] for name in self.modules}

    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] not in self.roots:
            return None
        if fullname not in self.modules:
            raise ImportError('module is outside frozen source closure: ' + fullname)
        source, data, package = self.modules[fullname]
        spec = importlib.util.spec_from_loader(fullname, _Loader(source, data), is_package=package)
        if package:
            spec.submodule_search_locations = [str(source.parent)]
        return spec


class Snapshot:
    def __init__(self, here, lock, files, identities):
        self.here, self.lock = here, lock
        self.files = MappingProxyType(files)
        self.identities = identities
        self.temporary = tempfile.TemporaryDirectory(prefix='weave-frozen-')
        self.root = Path(self.temporary.name)
        try:
            for name, data in self.files.items():
                target = self.root.joinpath(*_path(name).parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open('xb') as stream:
                    stream.write(data)
        except BaseException:
            self.temporary.cleanup()
            raise
        self.finder = _Finder(self.root, self.files)

    def install(self):
        for name, (path, data, _package) in self.finder.modules.items():
            prior = sys.modules.get(name)
            if prior is not None and (
                getattr(prior, '__file__', None) != str(path)
                or getattr(prior, '__source_sha256__', None) != sha256(data).hexdigest()
            ):
                raise ValueError('cached module is outside frozen source: ' + name)
        sys.meta_path.insert(0, self.finder)

    def verify(self):
        for name, digest in self.identities.items():
            if sha256(_read(self.here / name, MAX_ARCHIVE)).hexdigest() != digest:
                raise ValueError('frozen source bundle changed: ' + name)
        for name, expected in self.files.items():
            if _read(self.root / name, MAX_MEMBER) != expected:
                raise ValueError('materialized frozen source changed: ' + name)
        return len(self.lock['files'])

    def close(self):
        if self.finder in sys.meta_path:
            sys.meta_path.remove(self.finder)
        self.temporary.cleanup()


def load_snapshot(here):
    here = Path(here)
    raw = _read(here / 'SOURCE.json', 65536)
    metadata_raw = _read(here / 'SOURCE_BUNDLE.json', 65536)
    archive = _read(here / 'frozen-sources.zip', MAX_ARCHIVE)
    lock = json.loads(raw, object_pairs_hook=_unique)
    metadata = json.loads(metadata_raw, object_pairs_hook=_unique)
    if set(metadata) != {'schema', 'source_lock_sha256', 'archive_sha256', 'licenses'} or metadata['schema'] != 'weave.frozen-source-bundle/v1':
        raise ValueError('unsupported frozen source bundle metadata')
    if metadata['source_lock_sha256'] != sha256(raw).hexdigest() or metadata['archive_sha256'] != sha256(archive).hexdigest():
        raise ValueError('frozen source bundle identity mismatch')
    if set(lock) != {'schema', 'stack_commit', 'ucns_commit', 'files'} or lock['schema'] != 'weave.challenge-sources/v2':
        raise ValueError('unsupported challenge source lock')
    if any(type(lock[k]) is not str or re.fullmatch(r'[0-9a-f]{40}', lock[k]) is None for k in ('stack_commit', 'ucns_commit')):
        raise ValueError('frozen source commits must be exact identities')
    if type(lock['files']) is not list or not 1 <= len(lock['files']) <= 256 or type(metadata['licenses']) is not list or len(metadata['licenses']) > 8:
        raise ValueError('invalid frozen source census')
    expected = {}
    for row in [*lock['files'], *metadata['licenses']]:
        if type(row) is not dict or set(row) != {'path', 'git_blob'}:
            raise ValueError('invalid frozen source entry')
        name = _path(row['path']).as_posix()
        if name in expected or type(row['git_blob']) is not str or re.fullmatch(r'[0-9a-f]{40}', row['git_blob']) is None:
            raise ValueError('duplicate or invalid frozen source identity')
        expected[name] = row['git_blob']
    files, total = {}, 0
    with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
        entries = bundle.infolist()
        names = [entry.filename for entry in entries]
        if len(names) != len(set(names)) or set(names) != set(expected):
            raise ValueError('frozen source archive census mismatch')
        for entry in entries:
            _path(entry.filename)
            kind = stat.S_IFMT(entry.external_attr >> 16)
            if entry.is_dir() or kind not in (0, stat.S_IFREG) or entry.flag_bits & 1:
                raise ValueError('frozen source members must be regular unencrypted files')
            total += entry.file_size
            if entry.file_size > MAX_MEMBER or total > MAX_TOTAL:
                raise ValueError('frozen source archive exceeds declared byte budget')
            with bundle.open(entry) as stream:
                data = stream.read(MAX_MEMBER + 1)
            if len(data) != entry.file_size or _blob(data) != expected[entry.filename]:
                raise ValueError('frozen source blob mismatch: ' + entry.filename)
            files[entry.filename] = data
    identities = {name: sha256(data).hexdigest() for name, data in (
        ('SOURCE.json', raw), ('SOURCE_BUNDLE.json', metadata_raw), ('frozen-sources.zip', archive))}
    return Snapshot(here, lock, files, identities)
# ratios: loc_comments=160:30 imports_exports=13:2 calls_definitions=87:17
