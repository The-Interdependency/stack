# ratios: loc_comments=66:22 imports_exports=10:2 calls_definitions=34:3
"""Rebuild the source bundle from the exact Git objects, without executing them.

Usage: python build_source_bundle.py --stack-root /stack --ucns-root /ucns --check
Use --out /new/directory instead of --check to write a candidate. Requires local
Git source objects at SOURCE.json's commits; it never updates source pins.
Stored ZIP members avoid compression-runtime dependence in the byte replay.
"""
from __future__ import annotations

# === MODULE_BUILD ===
# id: weave_challenge_source_bundle_builder
#   module_name: build_source_bundle
#   module_kind: generator
#   summary: reproduce the complete historical source bundle from explicit Git object identities
#   owner: The-Interdependency/stack
#   public_surface: build,main
#   internal_surface: fixed source mapping, blob verification and deterministic ZIP serialization
#   tests: test_source_snapshot.py and explicit --check replay
#   rollout: new candidate directory followed by content review
#   rollback: retain the prior accepted bundle and source lock
#   auth_boundary: source content identities only; no producer authentication
#   storage_boundary: read Git objects; write only a named new output directory
#   network_boundary: no explicit network operation; required Git objects must be available
#   user_data_boundary: public source files and their original licenses only
# === END MODULE_BUILD ===

from hashlib import sha256
import argparse
import io
import json
from pathlib import Path
import stat
import subprocess
import zipfile
from source_snapshot import _blob, _path, _unique

HERE = Path(__file__).resolve().parent


def _git(root, commit, path):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(root),
                                    'show', commit + ':' + path])


def build(stack, ucns, source=HERE / 'SOURCE.json'):
    raw = source.read_bytes()
    lock = json.loads(raw, object_pairs_hook=_unique)
    files = {}
    for row in lock['files']:
        name = _path(row['path']).as_posix()
        native = name.startswith('sources/ucns/')
        data = _git(ucns if native else stack,
                    lock['ucns_commit' if native else 'stack_commit'],
                    name[len('sources/ucns/'):] if native else name)
        if name in files or _blob(data) != row['git_blob']:
            raise ValueError('source Git blob mismatch or duplicate: ' + name)
        files[name] = data
    licenses = []
    for root, commit, name in ((stack, lock['stack_commit'], 'LICENSE'),
                                (ucns, lock['ucns_commit'], 'sources/ucns/LICENSE')):
        data = _git(root, commit, 'LICENSE')
        files[name] = data
        licenses.append({'path': name, 'git_blob': _blob(data)})
    memory = io.BytesIO()
    with zipfile.ZipFile(memory, 'w', compression=zipfile.ZIP_STORED) as archive:
        for name, data in sorted(files.items()):
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(entry, data)
    zipped = memory.getvalue()
    metadata = {'schema': 'weave.frozen-source-bundle/v1',
                'source_lock_sha256': sha256(raw).hexdigest(),
                'archive_sha256': sha256(zipped).hexdigest(), 'licenses': licenses}
    return {'frozen-sources.zip': zipped,
            'SOURCE_BUNDLE.json': (json.dumps(metadata, indent=2) + '\n').encode()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stack-root', type=Path, required=True)
    parser.add_argument('--ucns-root', type=Path, required=True)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--check', action='store_true')
    action.add_argument('--out', type=Path)
    args = parser.parse_args()
    outputs = build(args.stack_root, args.ucns_root)
    if args.check:
        if any((HERE / name).read_bytes() != data for name, data in outputs.items()):
            raise SystemExit('source bundle differs from its exact Git inputs')
        print('frozen source bundle: byte-identical Git-object replay')
    else:
        args.out.mkdir(parents=True, exist_ok=False)
        for name, data in outputs.items():
            (args.out / name).write_bytes(data)
        print('wrote candidate source bundle:', args.out)


if __name__ == '__main__':
    main()
# ratios: loc_comments=66:22 imports_exports=10:2 calls_definitions=34:3
