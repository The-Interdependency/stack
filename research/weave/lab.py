#!/usr/bin/env python3
"""Phone-length CLI for explicit transport experiments, not a secure cipher.

Usage: python lab.py demo
       python lab.py enc profile.json input.bin output.lab --material a=path ...
       python lab.py dec profile.json output.lab recovered.bin --material a=path ...
Profiles must explicitly turn absent native stages off. All outputs are new files;
existing paths are never overwritten. A lab record discloses experiment switches
and operator identities, not corpus content or private native controls.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
from assembly import Run
from stages.api import Blocked, Streams
from transport import build, byte_stream, recover_bytes, LIMIT


def read(path, limit=LIMIT):
    with Path(path).open('rb') as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError('input exceeds declared resource limit')
    return data


def strict_json(data):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError('duplicate JSON field')
            out[key] = value
        return out
    return json.loads(data, object_pairs_hook=pairs)


def wire(result: Run) -> bytes:
    lanes = []
    for lane in result.payload.lanes:
        padding = (-len(lane)) % 8
        packed = recover_bytes(Streams((lane + (0,) * padding,)))
        lanes.append({'bits': len(lane), 'hex': packed.hex()})
    obj = {'schema': 'weave.lab-record/v1', 'classification': result.classification,
           'recipe': result.recipe, 'lanes': lanes}
    return json.dumps(obj, separators=(',', ':')).encode('utf-8')


def unwire(data: bytes, pipeline) -> Run:
    obj = strict_json(data)
    if (type(obj) is not dict or set(obj) != {'schema','classification','recipe','lanes'}
            or obj['schema'] != 'weave.lab-record/v1'
            or obj['classification'] not in ('TRANSPORT_CANDIDATE', 'ABLATION_ONLY')):
        raise ValueError('invalid lab record; not a Weave cipher format')
    if obj['recipe'] != json.loads(json.dumps(pipeline.recipe())):
        raise ValueError('experiment switch/operator recipe mismatch')
    lanes = parse_lanes(obj['lanes'])
    return Run(lanes, pipeline.recipe(), obj['classification'], (), 'encrypt')


def parse_lanes(records):
    if type(records) is not list or not 1 <= len(records) <= 63:
        raise ValueError('invalid lane count')
    out, total = [], 0
    for lane in records:
        if type(lane) is not dict or set(lane) != {'bits', 'hex'}:
            raise ValueError('invalid lane record')
        n, h = lane['bits'], lane['hex']
        if type(n) is not int or n < 0 or type(h) is not str or len(h) != 2*((n+7)//8):
            raise ValueError('invalid packed bit length')
        total += n
        if total > LIMIT * 8:
            raise ValueError('message exceeds resource limit')
        raw = bytes.fromhex(h)
        if raw.hex() != h:
            raise ValueError('noncanonical hexadecimal')
        bits = byte_stream(raw).lanes[0]
        if any(bits[n:]):
            raise ValueError('nonzero bit padding')
        out.append(bits[:n])
    return Streams(tuple(out))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('demo', 'enc', 'dec'))
    parser.add_argument('profile', nargs='?')
    parser.add_argument('input', nargs='?')
    parser.add_argument('output', nargs='?')
    parser.add_argument('--material', action='append', default=[], metavar='ID=PATH')
    args = parser.parse_args(argv)
    try:
        if args.mode == 'demo':
            profile = strict_json((Path(__file__).parent/'profiles/transport.json').read_bytes())
            material = {'a': b'literary test material', 'b': bytes(range(64)), 'c': b'\x00\xff\x55\xaa'}
            data = b'Weave: complete specified mechanisms remain the target.\x00\xff'
            p, public, _ = build(profile, len(data)*8, material)
            record = wire(p.encrypt(byte_stream(data), public))
            # Rebuild from declared inputs, and decode only the serialized result.
            q, _, private = build(strict_json(json.dumps(profile)), len(data)*8, dict(material))
            recovered = recover_bytes(q.decrypt(unwire(record, q), private).payload)
            if recovered != data:
                raise ValueError('demo recovery failed')
            print(json.dumps({'status':'PASSED', 'classification':'TRANSPORT_CANDIDATE',
                              'bytes':len(data), 'exact_recovery':True,
                              'complete_weave':False, 'active':['split','corpus','inter','join','whole']}))
            return 0
        if not args.profile or not args.input or not args.output:
            parser.error('enc/dec require profile, input and new output path')
        profile = strict_json(read(args.profile))
        if type(profile) is not dict or type(profile.get('switches')) is not dict:
            raise ValueError('profile and switches must be objects')
        material = {}
        # Off really means off: unused material paths are not read.
        if profile.get('switches', {}).get('corpus', True):
            for entry in args.material:
                label, sep, path = entry.partition('=')
                if not label or not sep or not path or label in material:
                    raise ValueError('supply unique ID=PATH material choices')
                material[label] = read(path)
        data = read(args.input, LIMIT if args.mode == 'enc' else 4*LIMIT + 32768)
        if args.mode == 'enc':
            p, public, _ = build(profile, len(data)*8, material)
            result = p.encrypt(byte_stream(data), public)
            output = wire(result)
        else:
            obj = strict_json(data)
            if type(obj) is not dict or 'lanes' not in obj:
                raise ValueError('invalid lab record')
            lanes = parse_lanes(obj['lanes'])
            n = sum(map(len, lanes.lanes))
            p, _, private = build(profile, n, material)
            result = p.decrypt(unwire(data, p), private)
            output = recover_bytes(result.payload)
        with Path(args.output).open('xb') as target:
            target.write(output)
        print(json.dumps({'status':'WRITTEN','classification':result.classification,
                          'complete_weave':False,'authenticated':False}))
        return 0
    except (OSError, ValueError, TypeError, Blocked, KeyError) as exc:
        print(json.dumps({'status':'REFUSED','reason':str(exc)}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
