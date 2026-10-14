"""Reconstruct inherited character definitions on the selected ordinal base.

The existing character table and final-y implementation remain their owners.
Only data/behavior is consumed from that historical module; its constructor is
never called. Every admitted scalar receives its prior entry or explicit hmmm.

Usage with an ordinal_construct.Factory:
    payload = build_definitions(factory)
    layer = verify_definitions(factory, payload)
    assert layer.final_y_realization('y', 'r', 'ing', True) == 'preserve-y'

The main ordinal build owns persistence. This file neither mutates a carrier nor
admits a missing number-name word. Pronunciation/numerology remain source-owned
candidate definition content, not added identity rules or validated science.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
from types import MappingProxyType
from typing import Mapping

from ucns.ordinal_affixiation import Participant, affixiate
from .language import character_definitions as inherited

# === MODULE_BUILD ===
# id: english_ordinal_inherited_definitions
#   module_name: ordinal_definitions
#   module_kind: engine
#   summary: reuse inherited definitions and behavior, reconstruct with UCNS ordinal geometry
#   owner: Erin Spencer
#   public_surface: build_definitions, verify_definitions, VerifiedDefinitions
#   internal_surface: inherited source admission, relation iteration, independent placement replay
#   auth_boundary: read
#   user_data_boundary: none
#   admin_only: false
#   network_boundary: none
#   storage_boundary: read
#   tests: tests/test_ordinal_definitions.py
#   rollout: constitutive required component of the selected ordinal artifact
#   rollback: rebuild explicitly; no historical constructor fallback
#   unresolved: source-uncovered definitions remain hmmm; global attachment transport is separate
# === END MODULE_BUILD ===
# === CONTRACTS ===
# id: ordinal_inherited_definition_preservation
#   given: the existing character definition source and the expanded public carrier
#   then: retain entries, overlapping roles, word links, order, provenance and explicit unknowns
# id: ordinal_definition_replay
#   given: serialized character and definition closures on the selected carriers
#   then: independently replay every placement and interior without invoking affixiate
# === END CONTRACTS ===

SCHEMA = 'english.ordinal-character-definitions/1'
SOURCE_PATH = 'english_gonol/language/data/character_definitions_v1.json'


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(',', ':'), allow_nan=False).encode('utf-8')


def _digest(value):
    return sha256(_canonical(value)).hexdigest()


def _inputs(factory):
    path = Path(inherited.__file__).parent / 'data' / 'character_definitions_v1.json'
    raw = path.read_bytes()
    entries = inherited.load_character_definition_table(path)
    # Source is local repository input, not an artifact's self-declared authority.
    if path.read_bytes() != raw:
        raise ValueError('definition source changed while loading')
    admitted = factory.glyph_carrier.identities
    if any(c not in admitted for c, e in entries.items() if not e.hmmm):
        raise ValueError('curated definition scalar is not admitted by this carrier')
    current = {c: entries.get(c, inherited.CharacterDefinitionEntry(
        c, (), None, (), None, (), True)) for c in admitted}
    missing = {e.number_name for e in current.values()
               if e.number_name and e.number_name not in factory.word_ids}
    if missing:
        raise ValueError('definition number-name words are not admitted: '
                         + ', '.join(sorted(missing)))
    return current, {
        'path': SOURCE_PATH, 'sha256': sha256(raw).hexdigest(),
        'text': raw.decode('utf-8'),
        'loader_sha256': sha256(Path(inherited.__file__).read_bytes()).hexdigest(),
    }


def _relations(char, entry):
    """Preserve the prior builder's relation order and source identifiers."""
    for role in entry.classes:
        yield f'char-def:{char}:{role}', f'char-class:{role}', None
    if entry.pronunciation:
        yield (f'char-def:{char}:letter-pronunciation',
               f'letter-pronunciation:{entry.pronunciation}', None)
    for behavior in entry.orthographic:
        yield (f'char-def:{char}:orthographic:{behavior}',
               f'orthographic-behavior:{behavior}', None)
    if entry.number_name:
        yield f'char-def:{char}:number-name', 'digit-number-name', entry.number_name
    for index, meaning in enumerate(entry.numerology):
        yield f'char-def:{char}:numerology:{index}', f'numerology:{meaning}', None
    if entry.hmmm:
        yield f'char-def:{char}:hmmm', 'definition:hmmm', None


def _reference_frame(identity, participants, relation, source):
    """Independent exact formula; never calls affixiate, Placement or record."""
    placements = []
    for i, (carrier, name, interior) in enumerate(participants):
        index = carrier.index(name)
        turn = Fraction(index, len(carrier.identities))
        placements.append({
            'identity': name, 'carrier_receipt': carrier.receipt,
            'index': index, 'arity': len(carrier.identities),
            'turn': [turn.numerator, turn.denominator],
            'radius': {'numerator': 1,
                       'power_of_two_denominator': len(participants) - i},
            'interior_receipt': None if interior is None else interior['receipt'],
        })
    record = {'schema': 'ucns.ordinal-affixiation.v1', 'identity': identity,
              'origin': 'SPACE', 'relation': relation, 'source': source,
              'placements': placements}
    return {'receipt': _digest(record), 'construction': record}


def _construct(factory, *, reference):
    entries, source = _inputs(factory)
    prefix = f'{factory.source_receipt}:definitions:{source["sha256"]}'
    objects = {}

    def frame(identity, participants, relation, source_id):
        if reference:
            return _reference_frame(identity, participants, relation, source_id)
        actual = tuple(Participant.atom(carrier, name) if interior is None else
                       Participant.closed(carrier, objects[interior['receipt']])
                       for carrier, name, interior in participants)
        closed = affixiate(identity, actual, origin='SPACE', relation=relation,
                           source=source_id)
        objects[closed.receipt] = closed
        return {'receipt': closed.receipt, 'construction': closed.record()}

    characters, words, definitions, registry = {}, {}, [], []
    for char, entry in entries.items():
        character = frame(char, ((factory.glyph_carrier, char, None),),
                          'character', f'{prefix}:char:{char}')
        characters[char] = character
        owned = []
        for source_id, relation, name in _relations(char, entry):
            participants = [(factory.glyph_carrier, char, character)]
            if name is not None:
                if name not in words:
                    # Use the existing closed word's exact identity and source.
                    wid = factory.word_ids[name]
                    words[name] = frame(name, tuple(
                        (factory.glyph_carrier, c, None) for c in name),
                        'ordered-glyphs', f'{factory.source_receipt}:word:{wid}')
                participants.append((factory.word_carrier, name, words[name]))
            definition = frame(source_id, tuple(participants), relation,
                               f'{prefix}:{source_id}')
            owned.append(definition['receipt'])
            definitions.append({'owner': char, 'source_id': source_id, **definition})
        registry.append({'scalar': char, 'entry': asdict(entry),
                         'character_receipt': character['receipt'],
                         'definition_receipts': owned})
    payload = {
        'schema': SCHEMA, 'profile': 'english.ordinal/1',
        'source_receipt': factory.source_receipt, 'source': source,
        'implementation_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'glyph_carrier_receipt': factory.glyph_carrier.receipt,
        'word_carrier_receipt': factory.word_carrier.receipt,
        'entries': registry, 'characters': characters,
        'number_names': words, 'definitions': definitions,
        'counts': {'characters': len(characters), 'definitions': len(definitions),
                   'number_names': len(words),
                   'unresolved': sum(e.hmmm for e in entries.values())},
        'hmmm': ['Uncovered scalar definitions remain explicit hmmm.',
                 'Local SPACE frames do not prove global attachment transport.',
                 'Inherited table content remains candidate evidence, not linguistic or cultural canon.'],
    }
    # Normalize dataclass tuples once to the actual JSON representation.
    return json.loads(_canonical(payload)), entries


def build_definitions(factory):
    """Construct every current-carrier definition; no old geometry fallback."""
    return _construct(factory, reference=False)[0]


@dataclass(frozen=True)
class VerifiedDefinitions:
    """Verified immutable entries retain the prior implementation's behavior."""
    entries: Mapping[str, inherited.CharacterDefinitionEntry]
    receipt: str
    counts: Mapping[str, int]

    def final_y_realization(self, final_character_surface,
                            preceding_character_surface, suffix_bare,
                            suffix_vowel_initial):
        return inherited.CharacterDefinitionLayer.final_y_realization(
            self, final_character_surface, preceding_character_surface,
            suffix_bare, suffix_vowel_initial)


def verify_definitions(factory, payload):
    """Check complete coverage, content, receipts, all local placements and links."""
    expected, entries = _construct(factory, reference=True)
    # Canonical bytes distinguish booleans from integer placement/count fields.
    if _canonical(payload) != _canonical(expected):
        raise ValueError('ordinal inherited-definition replay mismatch')
    return VerifiedDefinitions(MappingProxyType(entries), _digest(expected),
                               MappingProxyType(expected['counts']))
