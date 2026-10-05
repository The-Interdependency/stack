# === MODULE_BUILD ===
# id: weave_iterative_sequence_cycle
#   module_name: cycle
#   module_kind: engine
#   summary: corpus normalization once followed by native repeated-sequence affixiation and prime-determined bit interleaving, with exact reverse recovery
#   owner: Erin Spencer
#   public_surface: CycleLimits, RoundSpec, Profile, normalize, denormalize, affix, unaffix, forward, reverse, main
#   internal_surface: versioned research records and complete size accounting
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   tests: tests/test_cycle.py
#   rollout: explicit research cycle API and CLI; no full-profile cipher promotion
#   rollback: remove cycle, profile, tests, native binding and workflow additions
#   requires: weave_numeral_construction, weave_sequence_discovery, weave_prime_schedule, weave_native_binary_binding
#   unresolved: private/public key generation and cryptographic security; automatic short prime-recipe search
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: cycle_normalize_once
#   given: exact message bytes and actual corpus bytes
#   then: normalize once into a corpus-filled bit-length bucket with recoverable original length
# id: cycle_reversible_rounds
#   given: an admitted profile with native inputs
#   then: reverse every round from the final record, corpus and profile without the original message or encoder trace
# id: cycle_native_occurrence_recovery
#   given: seven occurrence-circle streams and their native complete positions
#   then: inverse native displacement restores ordered byte-sequence placement at the retained message-origin
# id: cycle_complete_accounting
#   given: a complete cycle record
#   then: count normalization, dictionaries, references, coordinates and outer framing without asserting a fixed expansion
# id: cycle_strict_refusal
#   given: malformed records, mismatched configuration/material, or exhausted budgets
#   then: refuse clearly without overwrite, partial recovery or silent truncation
# === END CONTRACTS ===
"""Usage: python cycle.py demo --sources /checkouts
       python cycle.py forward INPUT OUTPUT --profile cycle-profile.json --corpus CORPUS --sources /checkouts
       python cycle.py reverse INPUT OUTPUT --profile cycle-profile.json --corpus CORPUS --sources /checkouts

/checkouts contains the source-locked ucns/ tree; CYCLE_NATIVE.json names
exact modules. No packages beyond Python's standard library are required by this
consumer. The runnable profile is explicit construction research, not secure storage.
The newest sequence cycle replaces the historical one-bit-per-circle interpretation.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
from safe_output import write_new
import os

from numeral import (BitBlock, Entry, Packet, PrimePath, Limits, Refused, ResourceLimit,
                     encode as encode_numeral, decode as decode_numeral,
                     accounting, _Reader, _uint, _blob, _Primes)
from affixiation import discover, PROFILE as SELECTION_PROFILE
from prime_schedule import Route, plan, interleave, PROFILE as SPLIT_PROFILE
from cycle_native import load_native

ROOT = Path(__file__).resolve().parent
MAGIC, AFFIX_MAGIC, NORMAL_MAGIC = b'WVC\x01', b'WAF\x01', b'WNM\x01'
PROFILE_SCHEMA = 'weave.sequence-cycle-profile/v1'


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False).encode('utf-8')


def strict_json(data: bytes):
    def pairs(items):
        result = {}
        for key,value in items:
            if key in result:
                raise Refused('duplicate JSON key')
            result[key] = value
        return result
    try:
        return json.loads(data.decode('utf-8'), object_pairs_hook=pairs,
                          parse_constant=lambda s: (_ for _ in ()).throw(Refused('nonfinite JSON')))
    except (UnicodeError, ValueError, RecursionError) as exc:
        if isinstance(exc, Refused):
            raise
        raise Refused('invalid profile JSON') from exc


def _fields(value, fields):
    if type(value) is not dict or set(value) != set(fields):
        raise Refused('profile fields do not match the selected schema')


def _positive(value, maximum: int, name: str, *, zero: bool = False):
    if type(value) is not int or not (0 if zero else 1) <= value <= maximum:
        raise Refused(f'{name} outside its admitted integer domain')
    return value


@dataclass(frozen=True)
class CycleLimits:
    input_bytes: int = 262144
    round_bytes: int = 1048576
    rounds: int = 32
    discovery_visits: int = 16000000
    prime_work: int = 16000000
    native_occurrences: int = 131072

    def __post_init__(self):
        if any(type(v) is not int or v < 1 for v in vars(self).values()):
            raise Refused('positive integer execution budgets required')

    def numeral(self):
        return Limits(output_bits=self.round_bytes*8, wire_bytes=self.round_bytes,
                      occurrences=self.round_bytes, prime_work=self.prime_work)


@dataclass(frozen=True)
class RoundSpec:
    path: PrimePath
    arities: tuple[int, ...]
    circle_order: tuple[int, ...]
    spaces: tuple[Fraction, ...]
    end_order: str

    def __post_init__(self):
        if type(self.path) is not PrimePath or type(self.path.steps) is not tuple:
            raise Refused('exact immutable PrimePath required')
        if (type(self.arities) is not tuple or not self.arities
                or any(type(a) is not int or not 2 <= a <= 64 for a in self.arities)
                or len(set(self.arities)) != len(self.arities)):
            raise Refused('distinct candidate section arities must be integers 2..64')
        if (type(self.circle_order) is not tuple or len(self.circle_order) != 7
                or any(type(c) is not int for c in self.circle_order)
                or set(self.circle_order) != set(range(1,8))):
            raise Refused('circle_order must be a permutation of 1..7')
        if (type(self.spaces) is not tuple or len(self.spaces) != 8
                or any(type(x) is not Fraction or not 0 <= x < 2 or x.denominator >= 2**32
                       for x in self.spaces)):
            raise Refused('eight exact canonical space turns with denominators below 2^32 required')
        if self.end_order not in ('first-last','last-first'):
            raise Refused('explicit first-last or last-first order required')

    def as_dict(self):
        return {'prime_path': {'seed': self.path.seed, 'steps': [list(x) for x in self.path.steps]},
                'arities': list(self.arities), 'circle_order': list(self.circle_order),
                'spaces': [[x.numerator,x.denominator] for x in self.spaces],
                'end_order': self.end_order}


@dataclass(frozen=True)
class Profile:
    scope: str
    bucket_bytes: int
    corpus_bit_offset: int
    rounds: tuple[RoundSpec, ...]

    def __post_init__(self):
        if type(self.scope) is not str or not self.scope or len(self.scope.encode('utf-8')) > 1024:
            raise Refused('nonempty UTF-8 message scope of at most 1024 bytes required')
        _positive(self.bucket_bytes, 1048576, 'normalization bucket')
        _positive(self.corpus_bit_offset, 2**64-1, 'corpus bit offset', zero=True)
        if type(self.rounds) is not tuple or not self.rounds or any(type(r) is not RoundSpec for r in self.rounds):
            raise Refused('nonempty immutable round specification required')

    def as_dict(self):
        return {'schema': PROFILE_SCHEMA, 'selection': SELECTION_PROFILE, 'split': SPLIT_PROFILE,
                'scope': self.scope, 'bucket_bytes': self.bucket_bytes,
                'corpus_bit_offset': self.corpus_bit_offset, 'rounds': [r.as_dict() for r in self.rounds]}

    @property
    def identity(self):
        return sha256(canonical(self.as_dict())).digest()

    @classmethod
    def read(cls, data: bytes, limits: CycleLimits = CycleLimits()):
        if type(data) is not bytes or len(data) > 65536:
            raise Refused('profile must be at most 65536 bytes')
        obj = strict_json(data)
        _fields(obj, ('schema','selection','split','scope','bucket_bytes','corpus_bit_offset','rounds'))
        if obj['schema'] != PROFILE_SCHEMA or obj['selection'] != SELECTION_PROFILE or obj['split'] != SPLIT_PROFILE:
            raise Refused('unsupported profile construction')
        if type(obj['rounds']) is not list or not obj['rounds']:
            raise Refused('round list required')
        if len(obj['rounds']) > limits.rounds:
            raise ResourceLimit('profile exceeds round budget')
        rounds = []
        for row in obj['rounds']:
            _fields(row, ('prime_path','arities','circle_order','spaces','end_order'))
            path = row['prime_path']
            _fields(path, ('seed','steps'))
            if type(path['steps']) is not list or any(type(x) is not list for x in path['steps']):
                raise Refused('prime steps must be arrays')
            for name in ('arities','circle_order','spaces'):
                if type(row[name]) is not list:
                    raise Refused(f'{name} must be an array')
            spaces = []
            for pair in row['spaces']:
                if type(pair) is not list or len(pair) != 2 or any(type(x) is not int for x in pair):
                    raise Refused('space coordinate requires numerator/denominator integers')
                if pair[0] < 0 or not 1 <= pair[1] < 2**32:
                    raise Refused('space coordinate outside rational wire domain')
                value = Fraction(*pair)
                if [value.numerator,value.denominator] != pair:
                    raise Refused('space fraction must be canonical')
                spaces.append(value)
            rounds.append(RoundSpec(PrimePath(path['seed'],tuple(tuple(s) for s in path['steps'])),
                                    tuple(row['arities']),tuple(row['circle_order']),tuple(spaces),row['end_order']))
        return cls(obj['scope'],obj['bucket_bytes'],obj['corpus_bit_offset'],tuple(rounds))


def _corpus_bytes(corpus: bytes, count: int, bit_offset: int) -> bytes:
    if type(corpus) is not bytes or not corpus:
        raise Refused('actual nonempty corpus bytes required')
    start, shift = divmod(bit_offset % (8*len(corpus)), 8)
    if shift == 0:
        whole = corpus[start:] + corpus[:start]
        return (whole*((count+len(whole)-1)//len(whole)))[:count]
    return bytes(((corpus[(start+i)%len(corpus)] << shift) & 255)
                 | (corpus[(start+i+1)%len(corpus)] >> (8-shift)) for i in range(count))


def normalize(message: bytes, corpus: bytes, profile: Profile,
              limits: CycleLimits = CycleLimits()) -> bytes:
    """Selected corpus-tail bucket profile; original length remains inside the cycle."""
    if type(message) is not bytes:
        raise Refused('exact message bytes required')
    if len(message) > limits.input_bytes:
        raise ResourceLimit('message exceeds input byte budget')
    if type(corpus) is not bytes or not corpus:
        raise Refused('actual nonempty corpus bytes required')
    if len(corpus) > limits.round_bytes:
        raise ResourceLimit('corpus exceeds input material budget')
    header = NORMAL_MAGIC + len(message).to_bytes(8,'big') + sha256(corpus).digest()
    occupied = len(header)+len(message)
    target = (occupied//profile.bucket_bytes+1)*profile.bucket_bytes
    if target > limits.round_bytes:
        raise ResourceLimit('normalized frame exceeds round byte budget')
    return header + message + _corpus_bytes(corpus,target-occupied,profile.corpus_bit_offset)


def denormalize(data: bytes, corpus: bytes, profile: Profile,
                limits: CycleLimits = CycleLimits()) -> bytes:
    if type(data) is not bytes or len(data) < 45 or data[:4] != NORMAL_MAGIC:
        raise Refused('invalid normalized source frame')
    if type(corpus) is not bytes or not corpus:
        raise Refused('actual nonempty corpus required')
    length = int.from_bytes(data[4:12],'big')
    if length > limits.input_bytes or len(data) > limits.round_bytes or len(corpus) > limits.round_bytes:
        raise ResourceLimit('normalization recovery exceeds byte budget')
    occupied = 44+length
    if occupied >= len(data) or len(data) != (occupied//profile.bucket_bytes+1)*profile.bucket_bytes:
        raise Refused('normalized bucket or original length mismatch')
    if data[12:44] != sha256(corpus).digest():
        raise Refused('corpus source identity differs')
    if data[occupied:] != _corpus_bytes(corpus,len(data)-occupied,profile.corpus_bit_offset):
        raise Refused('corpus normalization content differs')
    return data[44:occupied]


def _symbol(index: int) -> str:
    if index < 6400:
        return chr(0xE000+index)
    index -= 6400
    if index < 65534:
        return chr(0xF0000+index)
    index -= 65534
    if index < 65534:
        return chr(0x100000+index)
    raise ResourceLimit('private-use symbol inventory exhausted')


def _fraction(reader: _Reader) -> Fraction:
    numerator, denominator = reader.uint(),reader.uint()
    if denominator == 0:
        raise Refused('zero coordinate denominator')
    value = Fraction(numerator,denominator)
    if not 0 <= value < 2 or (value.numerator,value.denominator) != (numerator,denominator):
        raise Refused('noncanonical complete-circle position')
    return value


def affix(data: bytes, *, api, geometry, scope: str, root: str, round_id: int,
          spec: RoundSpec, limits: CycleLimits = CycleLimits()):
    partition = discover(data,max_bytes=limits.round_bytes,visit_budget=limits.discovery_visits)
    if len(partition.order) > limits.native_occurrences:
        raise ResourceLimit('native occurrence count exceeds execution budget')
    origin = api.ByteOrigin(data,scope,round_id,geometry,root)
    circles = tuple(spec.circle_order[i%7] for i in range(len(partition.blocks)))
    table = api.close_sequences(origin,partition.blocks,partition.order,circles,spec.spaces)
    entries = tuple(Entry(_symbol(i),BitBlock.from_bytes(d.data),geometry.lift(d.state),circles[i])
                    for i,d in enumerate(table.definitions))
    wire_items = table.wire_occurrences()
    symbols = ''.join(entries[i].symbol for i,_ in wire_items)
    packet = Packet(origin.identity,round_id,entries,symbols)
    encoded = encode_numeral(packet,limits.numeral())
    counts = tuple(sum(o.circle==c for _,o in wire_items) for c in range(1,8))
    out = bytearray(AFFIX_MAGIC + _uint(len(data)) + _blob(encoded))
    for count in counts:
        out.extend(_uint(count))
    for _,occurrence in wire_items:
        position = geometry.lift(occurrence.source_state)
        out.extend(_uint(position.numerator)+_uint(position.denominator))
        if len(out) > limits.round_bytes:
            raise ResourceLimit('affixiation coordinates exceed round byte budget')
    if len(out) > limits.round_bytes:
        raise ResourceLimit('affixiation frame exceeds round byte budget')
    counts_by_id = Counter(partition.order)
    stats = {'input_bytes':len(data),'definitions':len(entries),
             'repeated_definitions':len(partition.repeat_ids),'occurrences':len(symbols),
             'repeated_occurrences':sum(counts_by_id[i] for i in partition.repeat_ids),
             'longest_definition_bytes':max(map(len,partition.blocks),default=0),
             'discovery_candidate_visits':partition.candidate_visits,
             'numeral_bytes':len(encoded),'native_coordinate_and_frame_bytes':len(out)-len(encoded),
             'output_bytes':len(out)}
    return bytes(out),stats


def unaffix(data: bytes, *, api, geometry, scope: str, root: str, round_id: int,
            spec: RoundSpec, limits: CycleLimits = CycleLimits()) -> bytes:
    if type(data) is not bytes:
        raise Refused('affixiation input must be bytes')
    if len(data) > limits.round_bytes:
        raise ResourceLimit('affixiation input exceeds byte budget')
    reader = _Reader(data)
    if reader.take(4) != AFFIX_MAGIC:
        raise Refused('unrecognized affixiation frame')
    source_length = reader.uint()
    if source_length > limits.round_bytes:
        raise ResourceLimit('affixiation source length exceeds byte budget')
    packet = decode_numeral(reader.blob(limits.round_bytes),limits.numeral())
    if packet.round_id != round_id:
        raise Refused('round identity mismatch')
    # decode_numeral already validates/replays recipes under one budget. Do not
    # reset that budget by replaying them again just to sum the output length.
    by_symbol = {e.symbol: e for e in packet.entries}
    if sum(by_symbol[s].block.length for s in packet.symbols) != source_length*8:
        raise Refused('affixiation source bit length mismatch')
    if len(packet.symbols) > limits.native_occurrences:
        raise ResourceLimit('native occurrence count exceeds execution budget')
    if any(e.block.length % 8 for e in packet.entries):
        raise Refused('cycle affixiation definitions must be byte aligned')
    counts = tuple(reader.uint() for _ in range(7))
    if sum(counts) != len(packet.symbols) or len(packet.symbols) > source_length:
        raise Refused('circle counts disagree with occurrence stream')
    positions = tuple(_fraction(reader) for _ in packet.symbols)
    if reader.pos != len(data):
        raise Refused('trailing affixiation bytes')
    ids = {e.symbol:i for i,e in enumerate(packet.entries)}
    if tuple(e.symbol for e in packet.entries) != tuple(_symbol(i) for i in range(len(packet.entries))):
        raise Refused('cycle reference inventory is not canonical')
    circles = tuple(e.circle for e in packet.entries)
    if circles != tuple(spec.circle_order[i%7] for i in range(len(packet.entries))):
        raise Refused('definition circle assignments disagree with profile')
    table = api.recover_sequences(geometry,scope=scope,message_origin=root,round_id=round_id,
        origin_identity=packet.origin,byte_length=source_length,
        blocks=tuple(e.block.to_bytes() for e in packet.entries),circles=circles,spaces=spec.spaces,
        counts=counts,wire_order=tuple(ids[s] for s in packet.symbols),source_turns=positions,
        max_bytes=limits.round_bytes)
    if tuple(geometry.lift(d.state) for d in table.definitions) != tuple(e.angle for e in packet.entries):
        raise Refused('whole-circle sequence attachments do not reconstruct')
    return table.restore()


def _prepared(profile: Profile, limits: CycleLimits):
    if type(profile) is not Profile:
        raise Refused('Profile required')
    if len(profile.rounds) > limits.rounds:
        raise ResourceLimit('round count exceeds execution budget')
    engine = _Primes(limits.numeral())
    return tuple(Route.evaluate(s.path,limits.numeral(),engine=engine) for s in profile.rounds)


def _native_identity() -> bytes:
    return sha256((ROOT/'CYCLE_NATIVE.json').read_bytes()).digest()


def forward(message: bytes, corpus: bytes, profile: Profile, sources: str | Path,
            limits: CycleLimits = CycleLimits()):
    """Run the stated cycle; return its full research record and size-only report."""
    routes = _prepared(profile,limits)
    api,geometry = load_native(sources)
    data = normalize(message,corpus,profile,limits)
    root = api.ByteOrigin(data,profile.scope,0,geometry).message_origin
    normalized_size = len(data)
    rows = []
    for i,(spec,route) in enumerate(zip(profile.rounds,routes)):
        packed,stats = affix(data,api=api,geometry=geometry,scope=profile.scope,root=root,
                            round_id=i,spec=spec,limits=limits)
        split = plan(len(packed)*8,route,spec.arities)
        data = interleave(packed,split,end_order=spec.end_order)
        rows.append({'round':i,**stats,'permutation_bit_count':split.bit_length})
    header = MAGIC + _native_identity() + profile.identity + bytes.fromhex(root) + _uint(len(rows))
    wire = header + _blob(data)
    if len(wire) > limits.round_bytes+128:
        raise ResourceLimit('cycle record exceeds final byte budget')
    report = {'schema':'weave.sequence-cycle-evidence/v1','classification':'CONSTRUCTION_EXPERIMENT',
              'source_bytes':len(message),'corpus_bytes':len(corpus),'normalized_bytes':normalized_size,
              'rounds':rows,'final_payload_bytes':len(data),'outer_frame_bytes':len(wire)-len(data),
              'total_bytes':len(wire),'security':'not established; no asymmetric key generation'}
    return wire,report


def reverse(wire: bytes, corpus: bytes, profile: Profile, sources: str | Path,
            limits: CycleLimits = CycleLimits()) -> bytes:
    """Recover from final bytes, corpus, profile and fixed producer sources only."""
    if type(wire) is not bytes:
        raise Refused('cycle record must be bytes')
    if len(wire) > limits.round_bytes+128:
        raise ResourceLimit('cycle record exceeds final byte budget')
    routes = _prepared(profile,limits)
    api,geometry = load_native(sources)
    reader = _Reader(wire)
    if reader.take(4) != MAGIC:
        raise Refused('unrecognized cycle record')
    if reader.take(32) != _native_identity() or reader.take(32) != profile.identity:
        raise Refused('native source lock or profile identity mismatch')
    root = reader.take(32).hex()
    if reader.uint() != len(profile.rounds):
        raise Refused('cycle round count mismatch')
    data = reader.blob(limits.round_bytes)
    if reader.pos != len(wire):
        raise Refused('trailing cycle bytes')
    for i in range(len(profile.rounds)-1,-1,-1):
        spec,route = profile.rounds[i],routes[i]
        split = plan(len(data)*8,route,spec.arities)
        packed = interleave(data,split,inverse=True,end_order=spec.end_order)
        data = unaffix(packed,api=api,geometry=geometry,scope=profile.scope,root=root,
                      round_id=i,spec=spec,limits=limits)
    if api.ByteOrigin(data,profile.scope,0,geometry).message_origin != root:
        raise Refused('message-origin root does not reconstruct')
    return denormalize(data,corpus,profile,limits)


def _read(path: Path, limit: int) -> bytes:
    with path.open('rb') as source:
        data = source.read(limit+1)
    if len(data) > limit:
        raise ResourceLimit(f'file exceeds byte budget: {path.name}')
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=('demo','forward','reverse'))
    parser.add_argument('input',nargs='?',type=Path)
    parser.add_argument('output',nargs='?',type=Path)
    parser.add_argument('--profile',type=Path,default=ROOT/'profiles/cycle-v1.json')
    parser.add_argument('--corpus',type=Path)
    parser.add_argument('--sources',type=Path,default=Path(os.environ.get('WEAVE_SOURCES',ROOT/'sources')))
    args = parser.parse_args()
    try:
        limits = CycleLimits()
        profile = Profile.read(_read(args.profile,65536),limits)
        if args.command == 'demo':
            message = b'Weave repeats byte sequences. '*24 + bytes(range(64))
            corpus = bytes(range(256)) + b'nonsecret corpus material'
            wire,report = forward(message,corpus,profile,args.sources,limits)
            restored = reverse(wire,corpus,profile,args.sources,limits)
            if restored != message:
                raise Refused('demo failed exact recovery')
            report['exact_recovery'] = True
            print(json.dumps(report,indent=2))
            return 0
        if args.input is None or args.output is None or args.corpus is None:
            raise Refused('input, output, and --corpus are required')
        if args.output.exists():
            raise Refused('output already exists; refusing overwrite')
        corpus = _read(args.corpus,limits.round_bytes)
        if args.command == 'forward':
            data = _read(args.input,limits.input_bytes)
            output,report = forward(data,corpus,profile,args.sources,limits)
        else:
            data = _read(args.input,limits.round_bytes+128)
            output = reverse(data,corpus,profile,args.sources,limits)
            report = {'output_bytes':len(output),'standing':'exact construction recovery; not security evidence'}
        write_new(args.output, output)
        print(json.dumps(report,indent=2))
        return 0
    except (OSError, ValueError, UnicodeError) as exc:
        parser.exit(2,f'refused: {exc}\n')


if __name__ == '__main__':
    raise SystemExit(main())
