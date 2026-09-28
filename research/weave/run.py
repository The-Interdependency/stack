#!/usr/bin/env python3
"""Phone-sized Weave entrypoint: python run.py demo; python run.py --off corpus.

The default full plan reports missing native laws. demo/enc/dec explicitly select
the separate transport experiment CLI. Neither is a production cipher.
"""
import argparse
import json
import sys
from assembly import DEFAULTS, Pipeline, Switches


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ('demo', 'enc', 'dec'):
        from lab import main as experiment
        return experiment(sys.argv[1:])
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
