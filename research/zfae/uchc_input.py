# ratios: loc_comments=68:34 imports_exports=10:4 calls_definitions=37:4
"""Consume the installed UCHC input artifact, never the local forge copy.

Usage: python research/zfae/uchc_input.py --database /data/construct.db
 --source-id request:1 --text 'alpha letter alpha' --lock UCHC_INPUT.json
Exit 0 means complete input admission, not neural inference. Exit 2 preserves
an unadmitted input dossier or reports an artifact/configuration failure.
"""
# === MODULE_BUILD ===
# id: stack_zfae_uchc_input
#   module_name: uchc_input
#   module_kind: adapter
#   summary: verifies installed UCHC candidate identity and exposes its native input contract to ZFAE research
#   owner: Erin Spencer
#   public_surface: load_input, verify_install, main
#   internal_surface: installed wheel and RECORD verification
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   tests: integration.uchc.tests.test_input
#   rollout: explicit research input consumer; no a0 runtime or PTCNA gate change
#   rollback: remove consumer; retain historical gonol evidence without promoting its profile
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: zfae_consumes_exact_uchc_artifact
#   given: an installed candidate wheel and its immutable lock
#   then: source-shadowing altered files and mismatched artifact identities refuse before admission
#   class: correctness
# id: zfae_input_admission_is_not_neural_readiness
#   given: a structurally admitted input
#   then: no inference result geometry weight dimensions or learned quality claim is synthesized
#   class: safety
# === END CONTRACTS ===
from __future__ import annotations

import argparse
import base64
import hashlib
from importlib import metadata
import json
from pathlib import Path
import re

from english_gonol import inference_input
from english_gonol.inference_input import EnglishConstruct


class InputArtifactError(ValueError):
    """Installed input implementation does not match the pinned consumer lock."""


def verify_install(lock: dict) -> dict:
    if lock.get('schema') != 'stack.zfae.uchc-input' or lock.get('version') != '1.0.0':
        raise InputArtifactError('unsupported input lock')
    expected = lock.get('wheel_sha256')
    if type(expected) is not str or re.fullmatch(r'[0-9a-f]{64}', expected) is None:
        raise InputArtifactError('wheel SHA-256 is required')
    dist = metadata.distribution('uchc')
    if dist.version != lock.get('package_version'):
        raise InputArtifactError('installed UCHC version differs')
    direct = json.loads(dist.read_text('direct_url.json') or '{}')
    hashes = direct.get('archive_info', {}).get('hashes', {})
    if hashes.get('sha256') != expected or direct.get('dir_info', {}).get('editable'):
        raise InputArtifactError('install the exact locked wheel, not an editable checkout')
    installed = dist.locate_file('english_gonol/inference_input.py').resolve()
    if Path(inference_input.__file__).resolve() != installed:
        raise InputArtifactError('UCHC import is shadowed by a source directory')
    records = dist.files
    if not records:
        raise InputArtifactError('installed wheel RECORD is unavailable')
    checked = 0
    for entry in records:
        if not entry.hash:
            if str(entry).endswith(('.py', '.json', '.toml')):
                raise InputArtifactError(f'unhashed installed source/metadata: {entry}')
            continue
        if entry.hash.mode != 'sha256':
            raise InputArtifactError('unsupported installed file hash')
        path = dist.locate_file(entry)
        with path.open('rb') as stream:
            actual = base64.urlsafe_b64encode(hashlib.file_digest(stream, 'sha256').digest()).rstrip(b'=').decode()
        if actual != entry.hash.value:
            raise InputArtifactError(f'installed file changed: {entry}')
        checked += 1
    return {'package_version': dist.version, 'wheel_sha256': expected, 'verified_files': checked}


def load_input(database: Path, lock: dict) -> EnglishConstruct:
    verify_install(lock)
    return EnglishConstruct(database, database_sha256=lock['database_sha256'],
                            logical_receipt=lock['logical_receipt'])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, required=True)
    parser.add_argument('--source-id', required=True)
    parser.add_argument('--text', required=True)
    parser.add_argument('--lock', type=Path, default=Path(__file__).with_name('UCHC_INPUT.json'))
    args = parser.parse_args()
    try:
        lock = json.loads(args.lock.read_text())
        with load_input(args.database, lock) as corpus:
            frame = corpus.resolve_text(args.text, source_id=args.source_id)
            print(frame.to_bytes().decode())
            return 0 if frame.glyphs_admitted and frame.words_admitted else 2
    except (ValueError, KeyError, OSError, metadata.PackageNotFoundError) as exc:
        print(json.dumps({'status': 'BLOCKED', 'error': str(exc),
                          'hmmm': 'input admission failed; no inference was performed'}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
# ratios: loc_comments=68:34 imports_exports=10:4 calls_definitions=37:4
