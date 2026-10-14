"""Supported English construction entry point; retired profiles have no fallback.

Usage: python -m english_gonol profile
       python -m english_gonol build ADMISSION UCD NEW_OUTPUT
       python -m english_gonol verify OUTPUT
       python -m english_gonol query OUTPUT 'the geometry'

Build consumes verified source admission; admission alone is not completed
geometry. Writes and full-corpus replay remain owned by ordinal_construct.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

# === MODULE_BUILD ===
# id: english_active_construction_entrypoint
#   module_name: __main__
#   module_kind: adapter
#   summary: selects the ordinal constructor without restoring deprecated build routes
#   owner: Erin Spencer
#   public_surface: main
#   internal_surface: active_profile
#   tests: tests/test_active_construction.py
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   rollout: default package entrypoint selected by ACTIVE_CONSTRUCTION.json
#   rollback: revert selection explicitly; never silently substitute historical geometry
#   unresolved: historical consumer migration is separate from this source default
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: english_active_no_legacy_fallback
#   given: a build, verification or query through the supported package entrypoint
#   then: only the selected ordinal implementation runs; retired or inconsistent profiles fail closed
# id: english_profile_without_compute
#   given: a profile or help request
#   then: show selection or usage without loading geometry or replaying the corpus
# === END CONTRACTS ===


def active_profile() -> dict:
    """Read the source-owned selection, independent of installed geometry packages."""
    path = Path(__file__).resolve().parents[1] / 'ACTIVE_CONSTRUCTION.json'
    profile = json.loads(path.read_text(encoding='utf-8'))
    if (profile.get('schema') != 'english.active-construction/1'
            or profile.get('implementation') != 'english_gonol.ordinal_construct'
            or profile.get('fallback') != 'none'):
        raise ValueError('invalid active construction selection; no legacy fallback')
    return profile


def main(argv: list[str] | None = None) -> None:
    """Run only the current construction; historical commands are not selectable."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('profile', help='show selection and unresolved boundaries; no compute')
    build = commands.add_parser('build', help='complete ordinal geometry from source admission')
    for name in ('admission', 'ucd', 'output'):
        build.add_argument(name, type=Path)
    verify = commands.add_parser('verify', help='independently replay the complete construction')
    verify.add_argument('output', type=Path)
    query = commands.add_parser('query', help='verify then construct exact admitted text')
    query.add_argument('output', type=Path)
    query.add_argument('text')
    args = parser.parse_args(argv)
    profile = active_profile()
    if args.command == 'profile':
        value = profile
    else:
        from english_gonol import ordinal_construct as constructor
        if (profile['active_profile'] != constructor.PROFILE
                or profile['geometry_commit'] != constructor.UCNS_COMMIT):
            raise ValueError('active selection differs from constructor; no legacy fallback')
        if args.command == 'build':
            value = constructor.build(args.admission, args.ucd, args.output)
        elif args.command == 'verify':
            value = constructor.verify(args.output)
        else:
            value = constructor.query(args.output, args.text)
    print(json.dumps(value, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
