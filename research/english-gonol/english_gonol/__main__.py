# ratios: loc_comments=49:14 imports_exports=6:1 calls_definitions=22:1
"""Stack English Unicode construction. Run python -m english_gonol --help."""
import argparse
from fractions import Fraction
import json
from pathlib import Path

# === MODULE_BUILD ===
# id: english_active_unicode_entry
#   module_name: __main__
#   public_surface: main
#   summary: dispatch profile, corpus and text operations to the active UCNS Unicode producer
#   tests: unicode_tests/test_unicode_corpus.py
#   owner: Erin Spencer
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: active_english_selects_unicode
#   given: a request at the supported package entry point
#   then: show the selected Unicode profile or execute its validated corpus API
# === END CONTRACTS ===


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='action', required=True)
    commands.add_parser('profile')
    for name in ('text', 'build', 'verify', 'query', 'record', 'definition'):
        command = commands.add_parser(name)
        command.add_argument('--ucns-source-root', required=True, type=Path)
        if name == 'build':
            command.add_argument('admission', type=Path)
            command.add_argument('ucd', type=Path)
        if name != 'text':
            command.add_argument('output', type=Path)
        if name in ('text', 'query'):
            command.add_argument('text')
        if name == 'record':
            command.add_argument('id', type=int)
        if name == 'definition':
            command.add_argument('scalar')
            command.add_argument('ordinal', type=int)
        if name in ('query', 'record', 'definition'):
            command.add_argument('--bearing', action='append', type=Fraction,
                                 help='exact turn for each closed child, in occurrence order')
    args = parser.parse_args(argv)
    from . import unicode_construction as unicode
    if args.action == 'profile':
        value = {'active_profile': unicode.PROFILE, 'recursive_profile': unicode.RECURSIVE_PROFILE,
                 'geometry': unicode.authority(), 'parent_bearings': 'caller-declared'}
    elif args.action == 'text':
        value = unicode.closed_record(unicode.construct_text(args.text, ucns_source_root=args.ucns_source_root),
                                      ucns_source_root=args.ucns_source_root)
    else:
        from . import unicode_corpus as corpus
        if args.action == 'build':
            value = corpus.build(args.admission, args.ucd, args.output, args.ucns_source_root)
        elif args.action == 'verify':
            value = corpus.verify(args.output, args.ucns_source_root)
        elif args.action == 'query':
            value = corpus.query(args.output, args.text, args.ucns_source_root, args.bearing)
        elif args.action == 'record':
            value = corpus.record(args.output, args.id, args.ucns_source_root, args.bearing)
        else:
            value = corpus.definition(args.output, args.scalar, args.ordinal, args.ucns_source_root, args.bearing)
    print(json.dumps(value, ensure_ascii=True, sort_keys=True))


if __name__ == '__main__':
    main()
# ratios: loc_comments=49:14 imports_exports=6:1 calls_definitions=22:1
