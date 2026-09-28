#!/usr/bin/env python3
"""Phone-sized Weave plan entrypoint. Usage: python run.py --off corpus --on auth.

Prints exact switches and missing laws. No file writes, network, automatic native
imports or encryption claims. Exit 2 = unresolved; exit 0 = plan has no blockers.
"""
import argparse
import json
from assembly import DEFAULTS, Pipeline, Switches


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--off', action='append', choices=tuple(DEFAULTS), default=[])
    parser.add_argument('--on', action='append', choices=tuple(DEFAULTS), default=[])
    args = parser.parse_args()
    overlap = set(args.off) & set(args.on)
    if overlap:
        parser.error('both on and off requested: ' + ','.join(sorted(overlap)))
    flags = {**{name: False for name in args.off}, **{name: True for name in args.on}}
    result = Pipeline(Switches(flags)).plan()
    print(json.dumps(result, indent=2))
    return 2 if result['status'] == 'BLOCKED' else 0


if __name__ == '__main__':
    raise SystemExit(main())
